# Install Pasal.id - Hukum Indonesia

The plugin includes four workflows and an OAuth-protected legal-research connection. It uses MCP name `pasal-id-plugin` and endpoint `https://mcp.pasal.id/mcp/openai`. A standalone `pasal-id` connection uses `/mcp` and has a separate diagnostic policy. Keep the names distinct and verify which connection a workflow uses.

## Codex CLI

These commands were checked against Codex CLI 0.156.0. If `codex plugin --help` does not expose them, update your supported client or use its Plugins interface.

Register the public marketplace and install the plugin:

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

This tested command pins login to the plugin endpoint for that invocation without registering a persistent standalone MCP entry. Later checks on Codex CLI 0.156.0 also confirmed that `codex mcp get pasal-id-plugin --json` resolves the installed plugin's server without that URL override; the override is not a general requirement for plugin visibility. OAuth credentials use Codex's normal credential handling, and the `dcr` strategy was verified with Pasal.id's authorization server. Sign in through the browser; do not paste tokens or callback URLs into a conversation or public issue.

Start a new Codex session. Confirm the installed plugin, four skills and its `pasal-id-plugin` connection. Inspect the session's MCP tools or connection details; the plugin should expose `resolve_law`, `search_legal`, `get_law_context`, `read_law`, `search_court_decisions` and `report_issue`. It does not expose `ping`. A missing connection or an unsuccessful login is a setup problem, not evidence that a law is absent.

Try asking: “Use Pasal.id to verify Pasal 65 of UU 27 Tahun 2022; quote only retrieved text and give its source link.” Check that calls use the plugin connection and preserve missing-text and status caveats. Do not submit feedback as a test side effect.

## Codex desktop

Register the marketplace with the CLI commands above. Restart the desktop app if its plugin sources have not refreshed, open **Plugins**, choose the **Pasal.id** marketplace, and install or enable **Pasal.id - Hukum Indonesia**. Complete its connection setup and start a new chat. Account and workspace policies may restrict these controls. Current OpenAI guidance describes local marketplaces and their install surfaces in [Package your plugin](https://developers.openai.com/plugins/build/plugins).

## ChatGPT archive import

Download the plugin ZIP and matching checksum from a [GitHub Release](https://github.com/Aturio/pasal-id-mcp/releases), or [build the reviewed source](../plugins/pasal-id/README.md). Where available, follow **Plugins → Add → Upload plugin archive → New Plugin → click to upload** and select the plugin ZIP. Availability depends on your account and workspace policy; this optional path is separate from the verified Codex CLI setup above.

The observed personal import displayed the bundled MCP server and all four skills, then offered **Open in desktop app**. Starting its citation workflow handed off to the ChatGPT desktop launcher; it did not produce a browser answer or establish an OAuth connection. If your host offers that handoff, open the same account in its desktop app, follow its installation or enablement prompts, and complete the Pasal.id browser connection when prompted. These native ChatGPT steps and desktop/mobile workflow execution have not been verified by our Codex tests. Do not treat successful archive import alone as a completed setup.

Import the plugin ZIP, not GitHub's automatic repository source archive. Version 0.1.5 contains 20 archive members, including all four workflows. The package is submitted for OpenAI review and is not published in its public directory. Personal import and repository marketplace distribution do not establish directory approval.

## Get a useful first answer

The [Pasal.id plugin setup and usage guide](https://pasal.id/hubungkan/plugin) is live, with an [English version](https://pasal.id/en/hubungkan/plugin). It covers installation, browser sign-in, the first successful connection check, all four workflows and troubleshooting. Use the prompts and checks below after a successful Codex connection.

Choose the workflow that matches your task:

| Workflow | Starter prompt |
| --- | --- |
| Verify a citation | Cek Pasal 65 ayat (1) UU 27 Tahun 2022. Berikan bunyi yang berhasil diambil dan tautan sumbernya. |
| Research legislation | Cari dasar hukum perlindungan data pribadi dan jelaskan kewajiban yang didukung pasal yang berhasil dibaca. |
| Trace recorded amendments | Telusuri perubahan UU ITE dan bandingkan ketentuan pencemaran nama baik yang berhasil ditemukan. |
| Discover MK cases | Temukan putusan MK yang menguji UU 13 Tahun 2003, beserta nomor, tanggal, kategori amar, dan tautannya. |

For a focused result, name the instrument and provision when you know them. Otherwise, describe the legal topic with Indonesian legal terms. For local regulations, specify the issuing province, city or regency. State any relevant date, and request the text actually read, pinpoint links and remaining uncertainty. Prefer one bounded question before expanding the research.

Check your first result:

1. Confirm the plugin is installed or enabled and the Pasal.id connection has completed sign-in. Start a new chat or session after installation or an update.
2. Use the citation starter above. A successful answer should identify UU 27/2022 on Pelindungan Data Pribadi, read Pasal 65 and distinguish the retrieved quotation from recorded status and interpretation.
3. Open the supplied Pasal 65 reader link and compare the quotation with the displayed provision. An answer without retrieved text, or one reporting missing text, a service error or incomplete evidence, has not verified the quotation.
4. Continue with the other workflow prompts when the first check succeeds. Request explicit limitations where text is damaged or missing, relationships are incomplete, or legal conditions depend on one another. Do not ask the plugin to certify complete historical consolidation or infer an MK holding from case metadata.

All four workflows have actual installed Codex CLI evidence. Those scenarios do not certify general legal accuracy or native ChatGPT compatibility. MK results are metadata and links, not full judgment analysis; MA reasoning is outside this plugin. Research does not automatically submit feedback. `report_issue` is a separate write for a diagnosed issue that you explicitly ask to report. Use general legal terms where possible and avoid confidential matter details; see [Pasal.id privacy](https://pasal.id/privasi).

## Updates and troubleshooting

To refresh the configured Git marketplace, run:

```bash
codex plugin marketplace upgrade pasal-id-plugins
codex plugin add pasal-id@pasal-id-plugins
```

Restart the client or start a new session after refreshing. Installed skills are snapshots. If an earlier draft used MCP name `pasal-id`, refresh or reimport the corrected package and reconnect before evaluating it.

If authentication expires, repeat the browser OAuth step for `pasal-id-plugin`. If only canonical `pasal-id` tools appear, inspect the installed package and its connection binding. Do not solve that problem by registering the canonical endpoint with the plugin's name. Support: [pasal.id/hubungkan](https://pasal.id/hubungkan), halo@pasal.id.
