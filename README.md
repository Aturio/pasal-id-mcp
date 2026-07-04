# Pasal.id — Indonesian Law MCP Server

**The first open, AI-native Indonesian legal database.** Gives Claude and any MCP-compatible AI assistant grounded, citation-ready access to 100,000+ Indonesian regulations — UU, PP, Perpres, PERMEN, PERDA, and 20+ other regulation types — directly from authoritative sources (peraturan.go.id, BPK JDIH, JDIH MK, JDIHN).

- **Live server:** `https://mcp.pasal.id/mcp`
- **Transport:** Streamable HTTP
- **Auth:** OAuth 2.0 — free account at [pasal.id](https://pasal.id)
- **Setup in 30 seconds:** [pasal.id/hubungkan](https://pasal.id/hubungkan)
- **License:** AGPL-3.0

## Why this exists

Indonesian law is scattered across dozens of government portals, each with its own PDF quirks and status ambiguities. Most LLM answers about Indonesian regulations are hallucinated — the training data is thin, and the live web isn't indexed for precise legal retrieval.

Pasal.id consolidates 100,000+ regulations into structured data (pasal-level granularity, whole-law hierarchy, preamble sections, amendment history, and legal-status provenance) and exposes it to AI assistants via MCP. Every answer an LLM gives using this server can be grounded in a specific article, regulation part, and authoritative source.

## Connect

Pick your client. All use the same server URL: `https://mcp.pasal.id/mcp`.

### Claude Code — one command

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp
```

Claude Code will open a browser window for OAuth on first use. For CI/automation, use a personal access token from [pasal.id/akun](https://pasal.id/akun):

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp \
  --header "Authorization: Bearer ${PASAL_MCP_TOKEN}"
```

### Claude Desktop / Cursor / Windsurf / VS Code

All consume the same JSON. Paste into the relevant config file:

```json
{
  "mcpServers": {
    "pasal-id": {
      "type": "http",
      "url": "https://mcp.pasal.id/mcp",
      "headers": {
        "Authorization": "Bearer ${PASAL_MCP_TOKEN}"
      }
    }
  }
}
```

| Client            | Config file                                                          |
|-------------------|----------------------------------------------------------------------|
| Claude Desktop    | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) · `%APPDATA%\Claude\claude_desktop_config.json` (Windows) |
| Cursor            | `~/.cursor/mcp.json` or `.cursor/mcp.json` (workspace)               |
| Windsurf          | `~/.codeium/windsurf/mcp_config.json`                                |
| VS Code MCP       | `.vscode/mcp.json` (workspace)                                       |
| Claude Code       | `.mcp.json` (project root)                                           |

Full per-client walkthrough: [docs/clients.md](./docs/clients.md).

### ChatGPT Desktop (April 2026+)

Settings → Developer Tools → Add MCP Server → paste `https://mcp.pasal.id/mcp`.

## Tools

The server exposes six task-oriented tools to AI assistants (v2.0.0 — the earlier
eleven-tool surface keeps working for existing integrations but is deprecated and
scheduled for removal after August 2026):

| Tool | Purpose |
|---|---|
| `search_legal` | Find regulations when you do not yet know which law applies — topics, keywords, or messy citations, with validated granular filters (multiple types, year, status, issuing body, region) and diagnostics that explain zero results. |
| `resolve_law` | Turn any reference — "KUHP", "UU 13/2003", "Pergub DKI 220 tahun 2010", a pasted title — into a canonical `law_id`, or get disambiguation candidates instead of a guess. |
| `get_law_context` | Compact orientation on one law: summary (status, structure counts, top-level outline), a pasal-range-compressed outline, or typed relationship groups (amendments, court reviews) — token-budgeted. |
| `read_law` | Read text with forgiving selectors: `pasal 27`, `pasal 27-30`, `bab III`, `menimbang`, `penjelasan pasal 5`, `lampiran`, `all` — with cursors, char budgets, and explicit `missing` reporting. |
| `search_court_decisions` | Search Constitutional Court (Mahkamah Konstitusi) decisions by reviewed law, lane (PUU/SKLN/PHPU/PHPKADA), ruling, year, dissent, or judge. |
| `report_issue` | Report data problems; the `search_failure` type ("I searched X and expected law Y") feeds the search regression suite directly. |

Every v2 response carries a `request_id` and structured `diagnostics`; errors are
typed (`error_code` + `recovery` guidance + `valid_values`) so assistants can
self-correct instead of retrying blindly. The canonical workflow: `resolve_law`
when you know the law → `get_law_context` to orient → `read_law` for text;
`search_legal` when you don't.

Schemas + example calls: [docs/tools.md](./docs/tools.md).

## Example prompts

Once connected, ask your AI assistant questions like:

- "Explain Pasal 81 of the UU Cipta Kerja on employment."
- "Is the 1974 Marriage Law still in force?"
- "What are contract workers' rights under Indonesian law?"
- "Compare worker rights before and after the Job Creation Law."
- "What is the minimum marriage age in Indonesia?"
- "Tampilkan struktur UU ITE dan ambil bagian Menimbang serta Pasal 27."
- "Cari dalam UU PDP bagian tentang pengendali data, lalu cek status peraturannya."
- "Saya menemukan OCR yang salah di Pasal ini; laporkan koreksinya ke Pasal.id."

The assistant should search first, retrieve only the needed Pasal or regulation part, verify status/provenance when the answer depends on currency, and use `report_issue` when the parsed corpus has a real data problem.

## About the data

- **Primary source:** [peraturan.go.id](https://peraturan.go.id) (Ministry of State Secretariat).
- **Secondary sources:** [BPK JDIH](https://peraturan.bpk.go.id) (69 regulation types), [JDIH MK](https://jdih.mkri.id) (Constitutional Court), [JDIHN](https://jdihn.go.id) (regional regulations).
- **Verification:** Gemini 3 Flash cross-checks every parsed document against the source PDF. Unverified regulations are flagged.
- **Updates:** New regulations ingested within 24–48 hours of publication.
- **Gaps:** See [pasal.id/metodologi](https://pasal.id/metodologi) for known limitations.

## Contributing

Pasal.id itself lives in a private repository — but this repo is public and we welcome:

- **Corrections** to the public MCP surface (README, install snippets, docs).
- **Bug reports** against the live server via [GitHub Issues](https://github.com/Aturio/pasal-id-mcp/issues) or [pasal.id/masukan](https://pasal.id/masukan).
- **Feature requests** — especially new MCP tools or improvements to existing ones.

PRs to the source regulations database happen through the crowd-correction workflow at [pasal.id](https://pasal.id): any user can highlight a passage and suggest a fix; our team reviews and merges within days.

## Related projects

- [pasal.id](https://pasal.id) — web reader with full search, law detail pages, and crowd corrections.
- [pasal.id/api](https://pasal.id/api) — REST API (same data, same authentication, for non-MCP integrations).

## License

AGPL-3.0 — see [LICENSE](./LICENSE).

The MCP server code and the regulation data are both open. Attribution is appreciated; commercial derivatives must remain open-source under the same license.

---

Built by [Aturio](https://github.com/Aturio) · Maintained by [Ilham Firdausi Putra](https://github.com/ilhamfp).
