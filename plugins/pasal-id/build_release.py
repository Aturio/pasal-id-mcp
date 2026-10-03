#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["PyYAML==6.0.3", "jsonschema==4.26.0"]
# ///
"""Validate Pasal's portable package and create a deterministic, allowlisted ZIP.

This does not connect accounts, verify public URLs, submit, or publish anything.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

import jsonschema
import yaml


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
# Existing users commonly have a standalone `pasal-id` connection. Some hosts
# resolve equal raw MCP names to that connection, bypassing the plugin route.
MCP_SERVER_NAME = "pasal-id-plugin"
SKILLS = frozenset({
    "verify-indonesian-law-citation",
    "research-indonesian-law",
    "check-law-status-and-amendments",
    "find-mk-decisions",
})
PUBLIC_TOOLS = frozenset({
    "search_legal", "resolve_law", "get_law_context", "read_law",
    "search_court_decisions", "report_issue",
})
RELEASE_ROOT_FILES = ("plugin.json", "mcp.json", "LICENSE", "README.md")


class PackageValidationError(ValueError):
    """A local package contract failed; no archive should be released."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise PackageValidationError(message)


def text_field(value: object, label: str, maximum: int, *, one_line: bool = False) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty text required")
    require(len(value) <= maximum, f"{label}: exceeds {maximum} characters")
    require(not any(unicodedata.category(c) in {"Cc", "Cf", "Zl", "Zp"}
                    for c in value if c != "\n"), f"{label}: unsupported control characters")
    require(not one_line or "\n" not in value, f"{label}: one line required")
    return value


def https_url(value: object, label: str) -> str:
    url = text_field(value, label, 1024, one_line=True)
    parsed = urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname, f"{label}: public HTTPS URL required")
    require(not parsed.username and not parsed.password, f"{label}: credentials are forbidden")
    require(not parsed.fragment and not any(c.isspace() for c in url), f"{label}: invalid URL")
    host = parsed.hostname.lower()
    require(host not in {"localhost", "127.0.0.1", "::1", "example.com"}
            and not host.endswith((".localhost", ".example", ".test", ".invalid")),
            f"{label}: placeholder/local endpoint is forbidden")
    return url


def member_path(root: Path, relative: str) -> Path:
    """Reject traversal and symlinks before reading or packaging a referenced file."""
    require(isinstance(relative, str) and relative, "Package path must be text")
    require("\\" not in relative, f"Unsafe package path: {relative}")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, f"Unsafe package path: {relative}")
    candidate = root / path
    for part in (candidate, *candidate.parents):
        if part == root.parent:
            break
        require(not part.is_symlink(), f"Symlink is forbidden: {relative}")
    require(candidate.resolve().is_relative_to(root.resolve()), f"Path escapes package: {relative}")
    require(candidate.is_file(), f"Missing package file: {relative}")
    return candidate


def json_file(root: Path, name: str) -> dict:
    try:
        result = json.loads(member_path(root, name).read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        raise PackageValidationError(f"Invalid JSON in {name}: {error}") from error
    require(isinstance(result, dict), f"{name}: JSON object required")
    return result


def schema_check(root: Path, data: dict, filename: str) -> None:
    schema = json_file(root, f"schemas/{filename}")
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as error:
        raise PackageValidationError(f"Schema violation: {error.message}") from error


def skill_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    require(match, f"{path.name}: YAML frontmatter required")
    metadata = yaml.safe_load(match[1])
    require(isinstance(metadata, dict), f"{path.name}: frontmatter mapping required")
    return metadata, match[2]


def release_members(root: Path) -> list[str]:
    members = list(RELEASE_ROOT_FILES)
    for directory in ("assets", "skills"):
        base = root / directory
        require(base.is_dir() and not base.is_symlink(), f"Missing/unsafe directory: {directory}")
        for path in sorted(base.rglob("*")):
            require(not path.is_symlink(), f"Symlink is forbidden: {path.relative_to(root)}")
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                require(not any(part.startswith(".") or part == "__pycache__"
                                for part in path.relative_to(root).parts),
                        f"Hidden/development file in runtime package: {relative}")
                require(path.suffix in {".md", ".yaml", ".svg", ".png", ".jpg", ".jpeg", ".webp"},
                        f"Unexpected runtime file: {relative}")
                members.append(relative)
    normalized: set[str] = set()
    for relative in sorted(members):
        member_path(root, relative)
        key = unicodedata.normalize("NFC", relative).casefold()
        require(key not in normalized, f"Case/Unicode path collision: {relative}")
        normalized.add(key)
    return sorted(members)


def validate_icon(root: Path, relative: str) -> None:
    require(relative.startswith("./assets/"), "Icons must be ./assets/ paths")
    path = member_path(root, relative)
    require(path.stat().st_size <= 5 * 1024 * 1024, f"Icon exceeds 5 MiB: {relative}")
    # Source package uses the repository's square SVG marks; no raster rewriting.
    require(path.suffix == ".svg", "This validator supports the shipped SVG icon assets")
    svg = ET.fromstring(path.read_bytes())
    require(svg.tag == "{http://www.w3.org/2000/svg}svg", f"Invalid SVG: {relative}")
    box = svg.attrib.get("viewBox", "").split()
    require(len(box) == 4, f"SVG square viewBox required: {relative}")
    width, height = float(box[2]), float(box[3])
    require(width == height and width >= 48, f"Icon must be square and at least 48px: {relative}")


def validate_package(root: Path, *, submission_ready: bool = False) -> dict:
    root = root.resolve()
    manifest = json_file(root, "plugin.json")
    mcp = json_file(root, "mcp.json")
    schema_check(root, manifest, "plugin-1.0.0.schema.json")
    schema_check(root, mcp, "mcp-1.0.0.schema.json")
    require(manifest.get("$schema") == PLUGIN_SCHEMA and mcp.get("$schema") == MCP_SCHEMA,
            "Portable Agent Plugins 1.0.0 schemas required")
    require(manifest.get("name") == "pasal-id", "Preserve the pasal-id package identity")
    require(re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
                         manifest.get("version", "")), "Semantic package version required")
    extension = manifest.get("extensions", {}).get("com.openai", {})
    require(not any(key in extension for key in ("apps", "hooks", "mcpServers", "skills")),
            "Public portable packages cannot use app references, hooks or component overlays")
    require(not (root / ".app.json").exists() and not (root / "hooks").exists(),
            "Public package must not contain app references or hooks")
    interface = extension.get("interface", {})
    for field, maximum, single_line in (
        ("displayName", 30, True), ("shortDescription", 30, True),
        ("longDescription", 4000, False), ("developerName", 80, True),
    ):
        text_field(interface.get(field), field, maximum, one_line=single_line)
    require(interface.get("category") == "Education & Research", "Use the intended Education & Research listing category")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        https_url(interface.get(field), field)
    capabilities = interface.get("capabilities", [])
    require(isinstance(capabilities, list) and len(capabilities) <= 20, "Invalid capabilities")
    for value in capabilities:
        text_field(value, "capability", 120, one_line=True)
    prompts = interface.get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "Supply one to three starter prompts")
    normalized_prompts = set()
    for prompt in prompts:
        text_field(prompt, "starter prompt", 128, one_line=True)
        require("@" not in prompt, "Starter prompts must not contain MCP @mentions")
        normalized_prompts.add(" ".join(unicodedata.normalize("NFKC", prompt).split()).casefold())
    require(len(normalized_prompts) == len(prompts), "Starter prompts must be unique")
    for field in ("composerIcon", "logo", "composerIconDark", "logoDark"):
        validate_icon(root, interface.get(field, ""))

    servers = mcp.get("mcpServers", {})
    require(set(servers) == {MCP_SERVER_NAME},
            "Exactly one MCP server named pasal-id-plugin is required to avoid standalone connection collisions")
    server = servers[MCP_SERVER_NAME]
    require(set(server) == {"type", "url"}, "Keep OAuth credentials/headers out of MCP configuration")
    require(server["type"] == "streamable-http", "Streamable HTTP required")
    endpoint = https_url(server["url"], "MCP endpoint")
    require(not endpoint.endswith("/"), "MCP endpoint must not redirect from a trailing slash")

    skill_root = root / "skills"
    require(skill_root.is_dir() and not skill_root.is_symlink(), "skills/ must be a real directory")
    require({p.name for p in skill_root.iterdir()} == SKILLS, "Exactly the four reviewed skills are required")
    for name in sorted(SKILLS):
        skill_path = member_path(root, f"skills/{name}/SKILL.md")
        metadata, body = skill_frontmatter(skill_path)
        require(metadata.get("name") == name, f"Skill folder/frontmatter mismatch: {name}")
        text_field(metadata.get("description"), f"{name} description", 1024)
        require(bool(body.strip()), f"Empty workflow: {name}")
        require(skill_path.stat().st_size <= 256 * 1024, f"Skill entry too large: {name}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
            require(not urlsplit(target).scheme, f"Skill reference must be packaged locally: {name}/{target}")
            member_path(root, f"skills/{name}/{target}")
        agent = yaml.safe_load(member_path(root, f"skills/{name}/agents/openai.yaml").read_text(encoding="utf-8"))
        require(isinstance(agent, dict), f"Invalid skill config: {name}")
        deps = agent.get("dependencies", {}).get("tools", [])
        require(len(deps) == 1, f"One Pasal MCP dependency required: {name}")
        dep = deps[0]
        require(dep.get("type") == "mcp" and dep.get("value") == MCP_SERVER_NAME
                and dep.get("transport") == "streamable_http" and dep.get("url") == endpoint,
                f"Skill MCP dependency differs from package endpoint: {name}")
        skill_interface = agent.get("interface", {})
        text_field(skill_interface.get("display_name"), f"{name} display name", 80, one_line=True)
        short = text_field(skill_interface.get("short_description"), f"{name} short description", 64, one_line=True)
        require(len(short) >= 25, f"Skill short description too short: {name}")
        require(f"${name}" in skill_interface.get("default_prompt", ""), f"Default prompt must invoke its skill: {name}")

    review = extension.get("review", {})
    require(not any(key in review for key in ("test_credentials", "reviewer_instructions")),
            "Reviewer secrets/instructions belong in the secure dashboard form")
    cases = review.get("test_cases", {})
    for kind, count in (("positive", 5), ("negative", 3)):
        rows = cases.get(kind, [])
        require(isinstance(rows, list) and len(rows) == count, f"Exactly {count} {kind} review cases required")
        for case in rows:
            text_field(case.get("description"), f"{kind} case description", 4000)
            text_field(case.get("prompt"), f"{kind} case prompt", 4000)
            text_field(case.get("expected_behavior"), f"{kind} expected behavior", 4000)
            if kind == "positive":
                tools = text_field(case.get("tools_triggered"), "Expected tool names", 1000)
                require(set(re.split(r"[\s,]+", tools)) <= PUBLIC_TOOLS, "Review cases reference an unexposed tool")
    text_field(extension.get("publication", {}).get("release_notes"), "Release notes", 4000)
    demo = review.get("demo_recording_url")
    if submission_ready:
        require(demo, "Submission needs an actual reviewer-accessible demo_recording_url; no demo was fabricated")
    if demo:
        https_url(demo, "Demo recording")

    members = release_members(root)
    size = sum(member_path(root, member).stat().st_size for member in members)
    require(len(members) <= 5000 and size <= 100 * 1024 * 1024, "Runtime archive exceeds submission size limits")
    return {"name": manifest["name"], "version": manifest["version"],
            "mcp_server_name": MCP_SERVER_NAME, "endpoint": endpoint,
            "skills": sorted(SKILLS), "members": members, "uncompressed_bytes": size,
            "demo_recording_present": bool(demo), "submission_metadata_checked": submission_ready}


def build_release(root: Path, output: Path, *, submission_ready: bool = False) -> dict:
    report = validate_package(root, submission_ready=submission_ready)
    require(not output.resolve().is_relative_to(root.resolve()), "Write release output outside the source package")
    output.parent.mkdir(parents=True, exist_ok=True)
    # ZIP_STORED avoids zlib-dependent bytes. Fixed metadata and sorted members
    # produce the same archive on supported systems for the same source files.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for member in report["members"]:
            info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, member_path(root, member).read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return {**report, "archive": str(output.resolve()), "sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Build ZIP at this path outside the package directory")
    parser.add_argument("--submission-ready", action="store_true", help="Also require actual demo URL; external review checks remain manual")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        report = (build_release(root, args.output, submission_ready=args.submission_ready)
                  if args.output else validate_package(root, submission_ready=args.submission_ready))
    except (PackageValidationError, OSError, yaml.YAMLError, ET.ParseError, ValueError) as error:
        print(f"Package validation failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
