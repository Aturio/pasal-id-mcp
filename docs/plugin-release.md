# Plugin distribution

The plugin is maintained in `plugins/pasal-id/`. It contains the portable manifests, four skills and their supporting templates, existing brand marks, license, README, reproducible builder and vendored validation schemas. `.agents/plugins/marketplace.json` makes the same package discoverable through supported Codex marketplace workflows; [installation](plugin-install.md) includes the actual OAuth setup. Marketplace files stay outside the 20-member plugin ZIP. This public repository contains no hosted service implementation, credentials, user data, evaluation payloads or private fixtures.

Plugin package versions are independent of the MCP Registry version in `server.json`. Updating the plugin does not require changing that registry manifest or trigger its publication workflow.

## Prepare a release

1. Verify the chosen production endpoint, browser OAuth, reviewed tools, grounding and privacy behavior through the real MCP transport. Test with an existing standalone `pasal-id` connection: the installed plugin must resolve its distinct `pasal-id-plugin` connection to `/mcp/openai` and use tools associated with the plugin. An ordinary `/mcp` connection has a separate diagnostic policy. Confirm accessible support, privacy and terms pages. Keep public-directory submission requirements, including the actual demo and reviewer access, separate from personal archive distribution.
2. Review the package's public source, version and release notes. Use a new semantic version when published skill or listing content changes. Do not replace an existing version's archive with different bytes.
3. From `plugins/pasal-id/`, run:

   ```bash
   uv run build_release.py
   uv run build_release.py --output /tmp/pasal-id-0.1.1.zip
   ```

   Match the output filename to the manifest version for later releases. The builder writes the ZIP and adjacent `.zip.sha256` file outside the source folder. Its archive allowlist excludes the builder, schemas and repository configuration. Check the archive member list printed by the builder.
4. Verify the checksum from the output directory:

   ```bash
   cd /tmp
   shasum -a 256 -c pasal-id-0.1.1.zip.sha256
   ```

5. Commit and push only the reviewed public package and documentation. Create a GitHub Release from that exact public commit with tag `pasal-id-plugin-v0.1.1`, a matching versioned title, and the ZIP plus its SHA-256 file as assets. Draft the release first, inspect the assets and notes, then publish after the runtime gates pass. Do not attach a private repository archive.

A dedicated reviewer account must work without MFA approval, email/SMS codes, magic links, or private network access. Supply its access details only through the secure portal form, never the archive or public repository.

Release notes should identify the four supported workflows, enduring endpoint, authentication, tested clients and material capability limits. State directory approval only if it has actually been granted. No demo recording or successful host evaluation should be invented.

## Maintain compatibility

Hosted tools remain live independently of installed skill snapshots. Preserve the reviewed tool contracts during server rollout. A package change needs a new version and archive; a server rollback does not replace skills already imported by users. Public-directory updates follow the [current OpenAI submission flow](https://developers.openai.com/plugins/deploy/submission).
