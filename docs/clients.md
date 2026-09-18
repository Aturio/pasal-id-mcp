# Connect an MCP client

Use `https://mcp.pasal.id/mcp` with **Streamable HTTP** and a free Pasal.id account. Interactive clients should complete browser OAuth. Personal tokens from [Akun → Akses API & MCP](https://pasal.id/akun) are an alternative for automation and clients without browser OAuth.

The [website connection guide](https://pasal.id/hubungkan) is the central Pasal.id walkthrough. Client interfaces and workspace policies can change.

## Claude Code

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp
```

Complete OAuth when prompted; use `/mcp` in Claude Code to inspect the connection or authenticate. For automation, set `PASAL_MCP_TOKEN` in your shell or secret manager and use:

```bash
claude mcp add --transport http pasal-id https://mcp.pasal.id/mcp \
  --header "Authorization: Bearer ${PASAL_MCP_TOKEN}"
```

## Claude Desktop and Claude on the web

Open **Settings → Connectors → Add custom connector**, enter the endpoint, and connect your Pasal.id account. Enable the connector in the conversation. Remote connectors use this interface; the local desktop stdio configuration file is not interchangeable with a hosted HTTP connector.

## Codex CLI and app

```bash
codex mcp add pasal-id --url https://mcp.pasal.id/mcp
codex mcp login pasal-id
```

For automation, configure an environment-variable reference instead of putting a token in a checked-in file:

```bash
codex mcp add pasal-id --url https://mcp.pasal.id/mcp \
  --bearer-token-env-var PASAL_MCP_TOKEN
```

Run `codex mcp list` to inspect configured servers. See [OpenAI's MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

## Cursor

Put this in `.cursor/mcp.json` for a project or `~/.cursor/mcp.json` for your user:

```json
{
  "mcpServers": {
    "pasal-id": { "url": "https://mcp.pasal.id/mcp" }
  }
}
```

Complete browser OAuth, then refresh the available tools. See the [Cursor MCP guide](https://cursor.com/docs/context/mcp).

## VS Code

Run **MCP: Add Server** and choose an HTTP server, or create `.vscode/mcp.json`:

```json
{
  "servers": {
    "pasal-id": {
      "type": "http",
      "url": "https://mcp.pasal.id/mcp"
    }
  }
}
```

VS Code uses the top-level `servers` key. Start the server and finish OAuth. See [VS Code's MCP documentation](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

## Windsurf

Use Windsurf's MCP settings to add the remote endpoint. If using a personal token, store it through the client's supported secret or environment configuration, then supply `Authorization: Bearer <token>`. Do not assume shell-style `${...}` substitution works in every client's JSON. Follow the [Windsurf MCP guide](https://docs.windsurf.com/windsurf/cascade/mcp) for the current configuration format.

## ChatGPT

Use ChatGPT's current custom MCP/app connection flow with the endpoint above and OAuth. Availability depends on the account and workspace policy. Follow [OpenAI's connection guide](https://developers.openai.com/plugins/deploy/connect-chatgpt) for the current interface; desktop JSON configuration from another client does not apply.

## Verify and troubleshoot

After connecting, refresh tool discovery and check for `search_legal`, `resolve_law`, `get_law_context`, `read_law`, `search_court_decisions`, `report_issue`, and `ping`. Call `ping`, then try `resolve_law` with `{"reference":"UU 27 tahun 2022"}`.

| Symptom | Action |
|---|---|
| OAuth session expired or refresh token invalid | Reauthorize the affected saved connection. Stop retrying the same invalid refresh token. |
| Personal token rejected | Check its expiry/revocation and the `Bearer ` prefix; replace that connection's token if necessary. |
| Old 11-tool list | Reconnect and refresh the client's tool cache. The current discovery surface has seven tools. |
| Redirect | Use the exact endpoint with no trailing slash. |
| Empty search | Read `diagnostics`, try Indonesian terms or fewer filters, or resolve a known citation. |
| Glama says unhealthy but a personal connection works | The directory test profile is separate. See [directory maintenance](directories.md). |

Never include tokens or account session data in public issues. Report reproducible integration problems through [GitHub Issues](https://github.com/Aturio/pasal-id-mcp/issues).
