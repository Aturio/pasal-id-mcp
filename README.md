# Pasal.id — Indonesian Law MCP

Search Indonesian regulations, resolve legal citations, and read the articles you need with links to the original sources. Pasal.id gives AI assistants structured legal text, amendment relationships, and available legal-status context, alongside Constitutional Court (Mahkamah Konstitusi) decision search.

This repository contains the public manifest, schema snapshot, and connection guides for the **hosted** Pasal.id MCP service. No local server installation or Docker build is needed.

| | |
|---|---|
| Endpoint | `https://mcp.pasal.id/mcp` |
| Transport | Streamable HTTP |
| Authentication | Free Pasal.id account with browser OAuth; personal access token for automation |
| Website and setup | [pasal.id](https://pasal.id) · [Hubungkan AI](https://pasal.id/hubungkan) |
| Live schema | [Public server card](https://mcp.pasal.id/.well-known/mcp/server-card.json) |
| Directory | [Glama connector](https://glama.ai/mcp/connectors/io.github.Aturio/pasal-id-mcp) |

## Connect

### Claude Code

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp
```

Complete the browser login when prompted. In Claude Desktop or Claude on the web, add the same URL through **Settings → Connectors → Add custom connector**, then connect your Pasal.id account.

### Codex CLI and app

```bash
codex mcp add pasal-id --url https://mcp.pasal.id/mcp
codex mcp login pasal-id
```

### Cursor

Add this to `.cursor/mcp.json` or `~/.cursor/mcp.json`, then complete OAuth:

```json
{
  "mcpServers": {
    "pasal-id": {
      "url": "https://mcp.pasal.id/mcp"
    }
  }
}
```

For VS Code, Windsurf, ChatGPT, and personal-token examples, use the [client-specific guide](docs/clients.md). Their configuration formats differ.

## Available tools

The live v2 interface provides **six research and feedback tools plus `ping`**. Directories should discover seven tools after authenticating.

| Tool | Use it to |
|---|---|
| `search_legal` | Find regulations by Indonesian topic, keyword, or citation, with type, year, status, issuer, region, and within-law filters. |
| `resolve_law` | Resolve a title, citation, or abbreviation to a canonical `law_id`, or receive candidates when ambiguous. |
| `get_law_context` | Check a law's summary, structure, legal status, and amendment or court-review relationships before reading. |
| `read_law` | Read selected articles, multiple ranges, chapters, preambles, elucidation, or appendices using character budgets and continuation cursors. |
| `search_court_decisions` | Search **Mahkamah Konstitusi** decisions by topic, reviewed law, case lane, outcome, year, dissent, or judge. |
| `report_issue` | Submit a real data correction or failed-search report. This tool writes feedback; it is not a health probe. |
| `ping` | Check authenticated MCP liveness without a legal search or feedback submission. |

When a law is named, use `resolve_law` → `get_law_context` → `read_law`. When the relevant law is unknown, start with `search_legal`. Reuse returned IDs, inspect diagnostics and recovery guidance, and cite the supplied reader and official-source links. Court search currently covers MK; this interface does not advertise Mahkamah Agung search.

[Parameter reference and examples](docs/tools.md) · [Checked-in public schema](server-card.json)

## Try asking

- “Cari peraturan tentang pelindungan data pribadi, lalu baca pasal yang relevan.”
- “Apa status UU ITE dan peraturan mana yang mengubahnya?”
- “Tampilkan kerangka UU 27 Tahun 2022, lalu baca Pasal 65–67.”
- “Cari pergub DKI Jakarta tentang pengelolaan air limbah.”
- “Cari putusan MK yang menguji UU Ketenagakerjaan.”

## Sources and verification

Pasal.id processes official government documents into searchable chapters, articles, paragraphs, and related sections. Reader pages expose source links, available status information, and a correction route. Coverage and processing quality vary; a missing search result does not establish that a regulation does not exist.

The website distinguishes human review, certified golden references, automated source checks, unreviewed processing, and limited evidence. A golden certification measures reproducibility against a reference; it is not a claim of human review. Text-verification evidence also does not determine whether a law remains in force. See the [methodology](https://pasal.id/metodologi) for the current definitions and limitations.

Use the official source to check the text and current legal status before relying on a citation. Pasal.id provides research material, not legal advice. Corpus totals change; the [website](https://pasal.id) shows current counts.

## Feedback and maintenance

Report integration problems in [GitHub Issues](https://github.com/Aturio/pasal-id-mcp/issues). Submit data corrections through [Pasal.id feedback](https://pasal.id/masukan), the reader, or `report_issue`. Corrections are reviewed before application.

Maintainers: see [directory maintenance](docs/directories.md) for schema sync, registry publication, and Glama test-profile recovery.

The files in this repository are licensed under [AGPL-3.0](LICENSE). This public documentation repository does not contain the production service implementation or grant a blanket license over third-party source documents.

Built by [Aturio](https://github.com/Aturio) · Maintained by [Ilham Firdausi Putra](https://github.com/ilhamfp) · [REST API](https://pasal.id/api)
