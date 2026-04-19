# Client Setup

Per-client instructions for connecting to the Pasal.id MCP server at `https://mcp.pasal.id/mcp`.

All clients need the same two things:

1. **A free Pasal.id account** — sign up at [pasal.id](https://pasal.id) (Google OAuth or email).
2. **Either (a) OAuth device-code flow** (Claude Code handles this) **or (b) a personal access token** from [pasal.id/akun](https://pasal.id/akun) for clients that expect a static bearer header.

---

## Claude Code

**Option A — OAuth (recommended for interactive use).**

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp
```

On first tool call, Claude Code opens your browser. Log in, approve access, and the token is cached automatically.

**Option B — personal access token (for CI / automation).**

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp \
  --header "Authorization: Bearer ${PASAL_MCP_TOKEN}"
```

Set `PASAL_MCP_TOKEN` in your shell or secret manager before running.

**Verify:**

```bash
claude mcp list
```

You should see `pasal-id ✓ Connected`.

---

## Claude Desktop

1. Open Claude Desktop → **Settings → Developer → Edit Config**.
2. Paste into the `mcpServers` object:

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

3. Set `PASAL_MCP_TOKEN` in your environment (macOS: `~/.zshrc`; Windows: System Environment Variables).
4. Fully quit and reopen Claude Desktop.

**Config file location:**

| OS      | Path                                                              |
|---------|-------------------------------------------------------------------|
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                     |

---

## Cursor

1. **Settings → MCP → Add Server** *(Cursor 0.41+)* or edit `~/.cursor/mcp.json` directly.
2. Add:

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

3. Restart Cursor.

**Project-scoped alternative:** put the same JSON in `.cursor/mcp.json` at the workspace root — overrides the global config for that project only.

---

## Windsurf

1. **Settings → Cascade → MCP Servers** or edit `~/.codeium/windsurf/mcp_config.json`.
2. Add the same JSON block as Cursor above.
3. Restart Windsurf.

---

## VS Code (MCP extension)

1. **Command Palette → MCP: Add Server** or create `.vscode/mcp.json` in your workspace:

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

2. Reload the VS Code window.

---

## ChatGPT Desktop *(April 2026+)*

1. **Settings → Developer Tools → Add MCP Server**.
2. Paste `https://mcp.pasal.id/mcp` as the URL.
3. ChatGPT Desktop handles OAuth automatically on first tool call.

---

## Generic `.mcp.json` template

Any MCP client that supports the Streamable HTTP transport can use this:

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

## Troubleshooting

| Symptom | Fix |
|---|---|
| `401 token_missing` on first tool call | Token not set, expired, or header malformed. Regenerate at [pasal.id/akun](https://pasal.id/akun). |
| Client never calls tools | Make sure the client was fully restarted after editing config; MCP servers aren't hot-reloaded. |
| `307 Temporary Redirect` | Use the exact URL `https://mcp.pasal.id/mcp` — no trailing slash. |
| Search returns 0 results but you know the law exists | Try the law's short reference (e.g. "uu 13 2003" or "UUD 1945") — Pasal.id's identity fast-path matches these directly. |

For anything else: open an issue at [github.com/Aturio/pasal-id-mcp/issues](https://github.com/Aturio/pasal-id-mcp/issues) or contact us via [pasal.id/masukan](https://pasal.id/masukan).
