#!/usr/bin/env python3
"""Refresh or compare the public card without credentials or MCP tool calls."""

import argparse
import json
import pathlib
import sys
import urllib.request

URL = "https://mcp.pasal.id/.well-known/mcp/server-card.json"
DEST = pathlib.Path(__file__).resolve().parents[1] / "server-card.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the snapshot differs")
    args = parser.parse_args()
    with urllib.request.urlopen(URL, timeout=30) as response:
        card = json.load(response)
    if not isinstance(card.get("serverInfo"), dict) or not card.get("tools"):
        raise ValueError("The endpoint did not return a nonempty MCP server card")
    names = [tool["name"] for tool in card["tools"]]
    if len(names) != len(set(names)) or any("inputSchema" not in tool for tool in card["tools"]):
        raise ValueError("The server card has duplicate tools or missing input schemas")
    rendered = json.dumps(card, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not DEST.exists() or json.loads(DEST.read_text()) != card:
            print("Public server card has changed; run scripts/sync-server-card.py and review the diff.", file=sys.stderr)
            return 1
        print(f"Public server card matches: {len(names)} tools")
    else:
        DEST.write_text(rendered)
        print(f"Updated {DEST.name}: {len(names)} tools; runtime {card['serverInfo'].get('version')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
