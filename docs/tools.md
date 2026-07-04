# Tool reference (v2.0.0)

Authoritative schemas live in the unauthenticated server card:
`https://mcp.pasal.id/.well-known/mcp/server-card.json`.

Shared v2 contract: every response carries `request_id` and `disclaimer`;
errors are typed (`error_code`, `message`, `recovery.suggestion`,
`valid_values`); text-bearing tools declare budgets (`limit`, `max_chars`,
cursors, truncation flags). Workflow: `resolve_law` -> `get_law_context` ->
`read_law`; use `search_legal` when the relevant law is unknown.

## `search_legal`

WHEN the relevant law is unknown, search Indonesian legal text with validated filters. Canonical workflow: search_legal -> resolve_law/get_law_context -> read_law. Use normal Bahasa Indonesia terms; avoid boolean operator syntax.

| Parameter | Type | Notes |
|---|---|---|
| `query` | string | **required** — Indonesian legal terms, topic, or citation fragment. |
| `law_id` | integer | Optional canonical law_id for within-law search. |
| `regulation_types` | array | Optional regulation type filters, e.g. ['UU', 'PP']. |
| `year` | integer | Exact enactment year filter. |
| `year_from` | integer | Inclusive start year. |
| `year_to` | integer | Inclusive end year. |
| `status` | string | Optional status filter: berlaku, diubah, dicabut, tidak_berlaku. |
| `issuing_body` | string | Optional issuing body or abbreviation, e.g. DPR, Presiden, DKI Jakarta. |
| `region` | string | Optional region hint for regional regulations. |
| `limit` | integer | Maximum results. Default 10; server clamp 1-20. |

Granular search: governor regulations about wastewater in DKI Jakarta.

```json
{"query": "pengelolaan air limbah", "regulation_types": ["PERGUB"], "region": "dki jakarta"}
```

Topic search with a year floor; diagnostics explain any relaxation applied.

```json
{"query": "perlindungan konsumen fintech", "year_from": 2016}
```

## `resolve_law`

WHEN a law is named by citation, title, or shorthand, resolve it to one canonical law_id. Canonical workflow: resolve_law -> get_law_context -> read_law.

| Parameter | Type | Notes |
|---|---|---|
| `reference` | string | **required** — Citation or title-like reference, e.g. 'UU 27 tahun 2022' or 'UU PDP'. |
| `region` | string | Optional region hint, e.g. 'DKI Jakarta'. |

Region-qualified citation resolves to the exact Jakarta regulation.

```json
{"reference": "Pergub DKI Jakarta 220 tahun 2010"}
```

Ambiguous shorthand returns candidates (UU 1/2023 vs UU 1/1946) instead of guessing.

```json
{"reference": "kuhp"}
```

## `get_law_context`

WHEN a law_id is known, get compact status, outline, or relationship context before reading text. Canonical workflow: resolve_law -> get_law_context -> read_law.

| Parameter | Type | Notes |
|---|---|---|
| `law` | integer \| string | **required** — Canonical law_id or a citation string accepted by resolve_law. |
| `detail` | string | Context detail level. summary is compact; outline helps choose read_law selectors. |

~2KB orientation: status, structure counts, top-level outline.

```json
{"law": "UU 27 tahun 2022", "detail": "summary"}
```

Typed relationship groups: amendments, court reviews, related works.

```json
{"law": 776, "detail": "relationships"}
```

## `read_law`

WHEN a law is known and text is needed, read by forgiving selector strings. Canonical workflow: resolve_law -> get_law_context -> read_law. Invalid selectors return typed invalid_selector errors with recovery guidance.

| Parameter | Type | Notes |
|---|---|---|
| `law` | integer \| string | **required** — Canonical law_id or a citation string accepted by resolve_law. |
| `selector` | string | **required** — Selector string: all, pasal 27, pasal 27-30, bab III, menimbang, mengingat, penjelasan umum, penjelasan pasal 5, lampiran. |
| `max_chars` | integer | Maximum aggregate characters. Default 30000; server clamp 1000-100000. |
| `cursor` | string | Opaque cursor from a prior truncated response. |

Read a pasal range.

```json
{"law": "UU 27 tahun 2022", "selector": "pasal 65-67"}
```

Read the official elucidation of one article.

```json
{"law": 702, "selector": "penjelasan pasal 27"}
```

## `search_court_decisions`

WHEN the user asks about Mahkamah Konstitusi decisions, search PUU/judicial review, SKLN, PHPU, or PHPKADA decisions. Use reviewed_law with any citation/law_id accepted by resolve_law.

| Parameter | Type | Notes |
|---|---|---|
| `query` | string | Optional topic/classification keyword, e.g. 'pemilu' or 'kebebasan berserikat'. |
| `reviewed_law` | string | Law being reviewed, e.g. 'UU 13 tahun 2003', 'UU PDP', or a law_id. |
| `lane` | string | Case lane: puu, skln, phpu, phpkada. |
| `amar` | string | Decision outcome filter, e.g. dikabulkan_sebagian, ditolak, inkonstitusional_bersyarat. |
| `year` | integer | Decision year. |
| `jenis_pengujian` | string | Review type, e.g. materiil or formil. |
| `has_dissent` | boolean | True for decisions with dissenting opinion; false for decisions without dissent. |
| `judge` | string | Constitutional justice name matched through curated aliases. |
| `limit` | integer | Maximum results. Default 20; server clamp 1-50. |

Judicial-review decisions touching the Manpower Law.

```json
{"reviewed_law": "uu 13 2003", "lane": "puu"}
```

## `report_issue`

WHEN the user finds a real Pasal.id data problem, submit structured feedback. Use search_failure only when a query should have found a known expected law.

| Parameter | Type | Notes |
|---|---|---|
| `report_type` | string | **required** — Issue type. |
| `title` | string | Optional short Indonesian title; auto-derived when omitted. |
| `description` | string | Context; for search_failure this is the failed query. |
| `expected_citation` | string | Expected law citation for search_failure, e.g. 'UU No. 27 Tahun 2022'. |
| `law_id` | integer | Pasal.id law_id if known. |
| `law_type` | string | Legacy law type, e.g. UU or PP. |
| `law_number` | string | Legacy law number. |
| `year` | integer | Legacy law year. |
| `pasal_number` | string | Article number if relevant. |
| `node_id` | integer | node_id for OCR correction. |
| `current_content` | string | Current text for OCR correction. |
| `suggested_content` | string | Suggested corrected text for OCR correction. |
| `reference_url` | string | Supporting official URL, if available. |
| `contact_email` | string | Optional contact email. |

Failed-search reports feed the search regression suite.

```json
{"report_type": "search_failure", "description": "cari 'baku mutu udara jakarta'", "expected_citation": "Kepgub DKI 551/2001"}
```

## Legacy tools

`search_laws`, `get_pasal`, `get_law_status`, `get_law_overview`,
`get_law_structure`, `get_law_part`, `read_law_section`,
`search_within_law`, and `list_laws` remain callable for existing
integrations but are deprecated (off-card since 2.0.0) and scheduled for
removal after August 2026. Migrate: reading -> `read_law`,
orientation/status -> `get_law_context`, all search -> `search_legal`.
