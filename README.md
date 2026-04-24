# Pasal.id — Indonesian Law MCP Server

**The first open, AI-native Indonesian legal database.** Gives Claude and any MCP-compatible AI assistant grounded, citation-ready access to 40,000+ Indonesian regulations — UU, PP, Perpres, PERMEN, PERDA, and 20+ other regulation types — directly from authoritative sources (peraturan.go.id, BPK JDIH, JDIH MK, JDIHN).

- **Live server:** `https://mcp.pasal.id/mcp`
- **Transport:** Streamable HTTP
- **Auth:** OAuth 2.0 — free account at [pasal.id](https://pasal.id)
- **Setup in 30 seconds:** [pasal.id/hubungkan](https://pasal.id/hubungkan)
- **License:** AGPL-3.0

## Why this exists

Indonesian law is scattered across dozens of government portals, each with its own PDF quirks and status ambiguities. Most LLM answers about Indonesian regulations are hallucinated — the training data is thin, and the live web isn't indexed for precise legal retrieval.

Pasal.id consolidates 40,000+ regulations into structured data (pasal-level granularity, whole-law hierarchy, preamble sections, amendment history, and legal-status provenance) and exposes it to AI assistants via MCP. Every answer an LLM gives using this server can be grounded in a specific article, regulation part, and authoritative source.

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

The server exposes nine intent-level tools to AI assistants:

| Tool | Purpose |
|---|---|
| `search_laws` | Search-first entry point for Indonesian regulation topics, keywords, and citation-like references. |
| `get_pasal` | Retrieve a specific Pasal with ayat context, source URL, PDF provenance, and correction metadata. |
| `get_law_status` | Check whether a regulation is in force, amended, or revoked, including normalized relationship codes. |
| `get_law_overview` | Read canonical metadata, source/provenance, verification, freshness, and compact outline counts. |
| `get_law_structure` | Inspect the hierarchy of Bab, Bagian, Pasal, Pembukaan, Penutup, Penjelasan, and Lampiran without loading the whole law. |
| `get_law_part` | Fetch a bounded part by `node_id`, selector, or special part such as `menimbang`, `mengingat`, `memutuskan`, `penutup`, or `lampiran`. |
| `search_within_law` | Search inside one known regulation after the relevant `law_id` is clear. |
| `report_issue` | Report OCR mistakes, missing regulations, missing Pasal, broken links, outdated content, or other data quality issues. |
| `list_laws` | Browse regulations with type, year, status, title, issuing body, and pagination filters. |

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
