# Install the Pasal.id plugin

The plugin includes four workflows and an OAuth-protected legal-research connection. It uses MCP name `pasal-id-plugin` and endpoint `https://mcp.pasal.id/mcp/openai`. A standalone `pasal-id` connection uses `/mcp` and has a separate diagnostic policy. Keep the names distinct and verify which connection a workflow uses.

## Codex CLI

These commands were checked against Codex CLI 0.156.0. If `codex plugin --help` does not expose them, update your supported client or use its Plugins interface.

After the public marketplace files are published on `main`, run:

```bash
codex plugin marketplace add Aturio/pasal-id-mcp --ref main
codex plugin list --marketplace pasal-id-plugins --available --json
codex plugin add pasal-id@pasal-id-plugins
```

Before publication, maintainers can test the prepared source by running `codex plugin marketplace add .` from the checkout root, followed by the same list and add commands. The marketplace path `./plugins/pasal-id` resolves from that root. [OpenAI marketplace documentation](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)

Complete the Pasal.id browser OAuth flow using the plugin endpoint:

```bash
codex mcp login pasal-id-plugin --oauth-client-registration dcr \
  -c 'mcp_servers.pasal-id-plugin.url="https://mcp.pasal.id/mcp/openai"'
```

This command-scoped URL override is needed on the tested CLI because its MCP commands do not directly expose the installed plugin's connection. It stores OAuth credentials through Codex's normal credential handling without registering a persistent standalone MCP entry. The `dcr` strategy was verified with Pasal.id's authorization server. Sign in through the browser; do not paste tokens or callback URLs into a conversation or public issue.

Start a new Codex session. Confirm the installed plugin, four skills and its `pasal-id-plugin` connection. `codex mcp list` lists standalone configuration and is not proof that an installed plugin failed. Inspect the session's MCP tools or connection details; the plugin should expose `resolve_law`, `search_legal`, `get_law_context`, `read_law`, `search_court_decisions` and `report_issue`. It does not expose `ping`.

Try asking: “Use Pasal.id to verify Pasal 65 of UU 27 Tahun 2022; quote only retrieved text and give its source link.” Check that calls use the plugin connection and preserve missing-text and status caveats. Do not submit feedback as a test side effect.

## Codex desktop

Register the marketplace with the CLI commands above. Restart the desktop app if its plugin sources have not refreshed, open **Plugins**, choose **Pasal.id**, and install or enable the **Pasal.id** plugin. Complete its connection setup and start a new chat. Account and workspace policies may restrict these controls. Current OpenAI guidance describes local marketplaces and their install surfaces in [Package your plugin](https://developers.openai.com/plugins/build/plugins).

## ChatGPT archive import

Download the ZIP and matching checksum from a published [GitHub Release](https://github.com/Aturio/pasal-id-mcp/releases), or [build the reviewed source](../plugins/pasal-id/README.md). Follow **Plugins → Add → Upload plugin archive → New Plugin → click to upload**, select the plugin ZIP, and complete OAuth. This path was observed in the ChatGPT Plugins UI; availability depends on account and workspace policy.

Import the plugin ZIP, not GitHub's automatic repository source archive. The plugin ZIP contains exactly the 18 runtime files and includes its four workflows. Personal import and repository marketplace distribution do not establish approval in OpenAI's public directory.

## Updates and troubleshooting

To refresh the configured Git marketplace, run:

```bash
codex plugin marketplace upgrade pasal-id-plugins
codex plugin add pasal-id@pasal-id-plugins
```

Restart the client or start a new session after refreshing. Installed skills are snapshots. If an earlier draft used MCP name `pasal-id`, refresh or reimport the corrected package and reconnect before evaluating it.

If authentication expires, repeat the browser OAuth step for `pasal-id-plugin`. If only canonical `pasal-id` tools appear, inspect the installed package and its connection binding. Do not solve that problem by registering the canonical endpoint with the plugin's name. Support: [pasal.id/hubungkan](https://pasal.id/hubungkan), halo@pasal.id.
