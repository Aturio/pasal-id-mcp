# Directory maintenance

## Sources of truth

- `server.json` is the Official MCP Registry manifest. Its schema describes installation and discovery metadata, not tool arguments.
- The live [server card](https://mcp.pasal.id/.well-known/mcp/server-card.json) is public discovery metadata. `server-card.json` is a snapshot, refreshed by `python3 scripts/sync-server-card.py`.
- Authenticated MCP `tools/list` is authoritative for the executable tool contract. Verify that it agrees with the public card after a runtime change.
- [Hubungkan AI](https://pasal.id/hubungkan) and [methodology](https://pasal.id/metodologi) describe the user-facing setup and data claims.

The current surface has six research/feedback tools plus `ping`. Legacy tool names should not be promoted as the discovery interface. The listed court search supports MK only.

## Publish a metadata update

1. Refresh the public card and update the relevant parameter examples in `docs/tools.md`.
2. Run `python3 scripts/sync-server-card.py --check`. Review changes; never publish credentials in metadata.
3. Validate `server.json` against its declared schema and `glama.json` against Glama's server schema. The released registry schema remains `2025-12-11`; unreleased drafts are not a required migration.
4. Increment the registry manifest version for each publication. Metadata releases can advance independently of the live MCP implementation version.
5. Push the reviewed change to `main`. The existing Publish to MCP Registry workflow publishes `server.json` through GitHub OIDC. Verify its result and the registry's latest record.
6. Request the Glama repository sync and a successful authenticated connector inspection. A repository sync alone does not replace the connector's tool snapshot.

## Glama ownership

Glama has separate [repository](https://glama.ai/mcp/servers/Aturio/pasal-id-mcp/admin) and [remote connector](https://glama.ai/mcp/connectors/io.github.Aturio/pasal-id-mcp/admin) administration.

The repository's `glama.json` declares GitHub maintainer `ilhamfp`. Organization repositories require this declaration; GitHub admin permission alone does not automatically make the listing editable. Refresh the claim flow after changing it.

The remote connector uses GitHub namespace verification, an HTTP challenge, or a DNS challenge. Its current schema uses an account-bound `claim` token; email-based `maintainers` declarations are deprecated. Claim tokens belong at the remote service's `/.well-known/glama.json` or the displayed DNS record, not in this repository's differently shaped `glama.json`. Retain the ownership proof after verification.

References: [repository ownership](https://glama.ai/blog/2025-07-08-what-is-glamajson), [server schema](https://glama.ai/mcp/schemas/server.json), [connector schema](https://glama.ai/mcp/schemas/connector.json).

## Recover the connector test profile

The directory's **Admin → Test Profile** supplies credentials for health checks and schema inspection. It is separate from personal Glama connections and the repository listing.

1. Inspect the saved profile and its failure before changing credentials.
2. Reauthorize the existing OAuth connection, or replace its dedicated read-only health-check token if that is its configured authentication method. Preserve the intended account and scope.
3. Clear or replace the failed saved authorization in Glama so it cannot keep retrying a revoked or missing refresh token. Making a second working profile does not prove the first retry loop stopped.
4. Run an inspection. Verify healthy status and all seven current tools, including their argument schemas.
5. Check the authentication logs over several subsequent scheduled checks. A green listing is not sufficient evidence that the invalid-refresh loop ended.

Keep authentication required. Do not expose a service-role credential, create feedback reports as probes, or hide provider errors to make a directory appear healthy.
