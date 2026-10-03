# Pasal.id - Hukum Indonesia

This package combines Pasal.id's OAuth-protected research MCP with four workflows for Indonesian legislation and Constitutional Court case discovery. The publisher is Aturio. It is source for local testing and a public submission; a ZIP or passing local validator does not establish directory approval.

The plugin's MCP connection is named `pasal-id-plugin`, and the server configuration and each skill target `https://mcp.pasal.id/mcp/openai`. This distinct name prevents a host from selecting an existing standalone `pasal-id` connection to `/mcp` in its place. Verify the endpoint's deployment, OAuth contract and actual connection binding before installation or submission. Existing clients can continue using their established `/mcp` connection. Never paste a PAT, password, or service key into the package or conversation; use the host's browser OAuth flow.

After installing or updating, inspect the host's connection/tool inventory: plugin research must use `pasal-id-plugin` at `/mcp/openai`, associated with the installed plugin. Restricted logging applies to that endpoint; calls through an existing standalone `/mcp` connection follow its separate diagnostic policy. If an earlier draft was installed with MCP name `pasal-id`, refresh or reimport this package and reconnect it before testing in a new conversation. Do not register a separate standalone connection with the plugin's name and a different URL.

| Workflow | Useful outcome | Boundary |
| --- | --- | --- |
| Verify an Indonesian law citation | Exact retrieved Pasal text, comparison, pinpoint and link | Missing/suppressed text cannot certify a quote |
| Research Indonesian law | A concise memo from provisions actually read | Keyword discovery and bounded corpus coverage |
| Check law status and amendments | Recorded relationship evidence and focused text comparison | No complete historical consolidation |
| Find MK decisions | Case identities, recorded dates/outcomes and reader links | Metadata discovery; no MA corpus or full MK reasoning |

The plugin does not submit feedback as a research side effect. A user-requested report is a separate write, limited to a diagnosed problem and necessary nonsensitive detail.

## Validate and build

From `plugins/pasal-id/` in a source checkout, use the builder's pinned dependencies:

```bash
uv run build_release.py
uv run build_release.py --output /tmp/pasal-id-0.1.2.zip
```

The source builder declares pinned PEP 723 dependencies. The validator uses vendored Agent Plugins 1.0.0 schemas offline, then checks the OpenAI listing, exact review-case counts, local references, SVG dimensions, dependency consistency, path safety and the allowlisted runtime contents. ZIP members are sorted, uncompressed and have fixed metadata; identical source produces identical bytes and an adjacent SHA-256 file. Maintainers in the implementation repository also run `uv run --project apps/mcp-server pytest apps/mcp-server/test_plugin_package.py -q` from its root to check the package against the server's actual tool signatures.

The archive includes `plugin.json`, `mcp.json`, this README, the license, assets and complete skill folders. Builder code, validation schemas, tests, private service implementation, credentials and repository configuration are excluded. Do not add a registered `.app.json` mapping or lifecycle hooks to the public package.

Use `--submission-ready` after recording a real demo and adding its accessible URL as `extensions.com.openai.review.demo_recording_url`. This stricter check deliberately fails while that URL is absent. It checks local submission metadata, not identity verification, reachable policy URLs, working OAuth, domain ownership, human evaluation, or portal approval. Review cases describe expected behavior; they are not a claim that the host evaluation has already passed.

## Test the installed experience

1. Inspect and call the deployed Streamable HTTP tools, including error/suppression paths. Verify that only the reviewed tools are advertised and that OAuth and reading cursors work. With a standalone `pasal-id` connection already configured, confirm the imported plugin still resolves `pasal-id-plugin` to `/mcp/openai` and uses its own tools.
2. To import the complete package in ChatGPT, use **Plugins → Add → Upload plugin archive**. In the **New Plugin** dialog, choose **click to upload** and select the built ZIP. Follow the host's connection and browser OAuth steps. This path imports the packaged workflows as well as the MCP configuration; it was observed in the current ChatGPT Plugins UI. Use a new conversation for each evaluation.
3. For MCP-only testing in ChatGPT developer mode, register the exact endpoint, authenticate through Pasal.id and inspect its tools. Refresh after metadata changes. Registering a remote endpoint alone does not import these four skills.
4. For supported local Codex clients, install the complete package from a local marketplace. A marketplace can point at this folder using a path relative to its own root. Registered-server mappings, if needed for a particular local host, belong in a separate testing configuration.
5. Test direct and indirect triggers, ambiguous references, local-regulation filters, missing/suppressed text, capped relationships, MK metadata boundaries, quotas and OAuth expiration. Run paired requests with MCP alone and with the skills. Inspect actual answers, not just successful tool calls.

Archive import, developer mode and local marketplace availability depend on host/account/workspace policy. Personal archive import and a public directory submission are separate flows. This package does not change those settings or install itself.

## Public release checks

Use the [current submission flow](https://developers.openai.com/plugins/deploy/submission): upload a ZIP containing the remote MCP from the initial submission, connect its server, complete domain/OAuth setup, review skill/tool scans, submit the concrete draft, then publish only after approval. Currently only one MCP can be connected per plugin.

Before submission:

- Confirm the enduring endpoint, real OAuth flow, and reviewed tool contracts. The selected URL is difficult to change after publication.
- Verify Aturio's publisher identity and organization permissions in the portal. The directory uses the selected verified identity.
- Serve the exact portal challenge token at the eligible host's `/.well-known/openai-apps-challenge`, without authentication.
- Confirm accessible [website](https://pasal.id), [support/contact](https://pasal.id/hubungkan), [privacy](https://pasal.id/privasi) and [terms](https://pasal.id/ketentuan), with actual collection/retention matching disclosures. Support email: halo@pasal.id.
- Run the five positive and three negative cases on supported ChatGPT/Codex surfaces with current legal evidence. Add the real demo recording URL and update release notes/version.
- Enter dedicated reviewer account access through the secure dashboard form, outside this ZIP. It must work without inaccessible MFA or private approvals.
- Read current usage policies, verify source rights, resolve required portal findings, and retain evaluation/scan receipts. A local check cannot replace these release decisions.

Hosted tools and server implementations remain live while metadata is reviewed. Preserve approved schemas during rollout; deploy backward-compatible fixes, rescan tool changes, and upload a new ZIP for skill/listing updates. A Git rollback does not replace installed skill snapshots. No claim of complete corpus coverage, guaranteed correctness, current legal force, or judgment reasoning is made by this package.

## Asset and schema provenance

`assets/icon.svg` and `assets/icon-dark.svg` are unchanged copies of the repository's existing `logo/icon-primary.svg` and `logo/icon-dark-bg.svg`. Both are square 200-unit marks; the listing reuses them for composer and logo. Brand definitions remain in the repository's `DESIGN.md`.

`schemas/plugin-1.0.0.schema.json` and `schemas/mcp-1.0.0.schema.json` were obtained from the [Agent Plugins 1.0.0 plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) on October 2, 2026. They validate the portable format, while OpenAI-specific checks follow its current documentation. The published OpenAI documents contain older contradictory `.app.json`, annotation-justification and endpoint-update examples; the current submission page controls this package's release process.

This package preserves the repository's AGPL-3.0 license; see `LICENSE`.
