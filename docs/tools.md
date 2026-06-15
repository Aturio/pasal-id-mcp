# MCP Tools

The Pasal.id MCP server exposes ten intent-level tools. The live server is Indonesian-first: tool descriptions, parameter descriptions, and workflow prompts are written for Indonesian legal research, while the returned regulation names preserve official nomenclature. (A `ping` health-check tool is also available for connection testing.)

All tools require an authenticated MCP session.

## Recommended Workflow

1. Start with `search_laws` for topics, keywords, and loose references.
2. Use `get_law_overview` or `get_law_structure` when the assistant needs provenance or the regulation map.
3. Use `get_pasal` for an exact Pasal, `read_law_section` to read several Pasal at once (a range, a whole Bab, or a list), or `get_law_part` for a bounded part such as Bab II, Menimbang, Mengingat, Penutup, or Lampiran.
4. Use `search_within_law` only after the relevant `law_id` is clear.
5. Use `get_law_status` before final citation when currency matters.
6. Use `report_issue` only for real data problems, not for every exploratory zero-result search.

## 1. `search_laws`

Search-first entry point across Indonesian regulations. It accepts Indonesian legal topics, keywords, and citation-like references, then returns law metadata, Pasal-level hits, snippets, stable Pasal.id URLs, and provenance/trust fields where available.

**Input:**

```json
{
  "query": "pemutusan hubungan kerja pesangon",
  "regulation_type": "PP",
  "year_from": 2020,
  "year_to": 2026,
  "language": "id",
  "limit": 10
}
```

## 2. `get_pasal`

Retrieve a specific Pasal from a known regulation. Use the `law_id` returned by `search_laws`, `list_laws`, or `get_law_structure` whenever possible.

**Input:**

```json
{
  "law_id": 3019,
  "pasal_number": "27"
}
```

**Also supports:**

```json
{
  "law_type": "UU",
  "law_number": "11",
  "year": 2008,
  "pasal_number": "27"
}
```

Successful responses include `node_id`, full untruncated `content_text`, per-ayat content, `pasal_url`, `law_url`, `source_pdf_url`, `source_family`, `content_verified`, and `correction_url` so users can inspect or correct OCR issues.

## 3. `get_law_status`

Check whether a regulation is currently in force, amended, revoked, or otherwise not current. This is the canonical status and relationship check.

**Input:**

```json
{
  "law_id": 3019
}
```

Responses include human-readable relationship labels plus normalized relationship codes for amendment and revocation chains.

## 4. `get_law_overview`

Return canonical metadata, issuing body, status, provenance, source URLs, source PDF URL, verification/freshness fields, and compact outline/count summaries.

**Input:**

```json
{
  "law_type": "UU",
  "law_number": "11",
  "year": 2008
}
```

Use this when the assistant needs to explain why the retrieved law is trustworthy before reading details.

## 5. `get_law_structure`

Inspect a regulation hierarchy without loading the full text. This is the progressive-disclosure tool for "UU ini isinya apa saja?"

**Input:**

```json
{
  "law_id": 3019,
  "depth": 2,
  "include_special_parts": true
}
```

Returns compact nodes with `node_id`, `node_type`, `number`, `heading`, `parent_id`, `children_count`, `pasal_count`, and special-part flags/counts for `preamble`, `penutup`, `penjelasan`, and `lampiran`.

For preamble-heavy research, responses also include a `preamble_sections_summary` indicating whether parsed `menimbang`, `mengingat`, `memutuskan`, and `menetapkan` sections were detected.

## 6. `get_law_part`

Fetch one bounded part of a regulation. Prefer `node_id` from `get_law_structure` for deterministic reads; use selectors when the part is obvious.

**By node:**

```json
{
  "law_id": 3019,
  "node_id": 11966151,
  "include_children": true,
  "max_chars": 12000
}
```

**By selector:**

```json
{
  "law_id": 3019,
  "node_type": "bab",
  "number": "II"
}
```

**Special parts:**

```json
{
  "law_id": 3019,
  "part_type": "menimbang"
}
```

`part_type` accepts `preamble`, `menimbang`, `mengingat`, `memutuskan`, `menetapkan`, `penutup`, `penjelasan`, and `lampiran` (case-insensitive).

Large parts return `truncated: true` and `next_cursor`; call again with the cursor to continue.

## 7. `read_law_section`

Batch reader for multiple Pasal in a single call — the preferred tool for reading 5+ Pasal in sequence (an article-by-article walk-through, a full Bab, or a range like Pasal 5–12). Each returned section carries the full `content_text`, and cross-references are resolved server-side.

**Input:**

```json
{
  "law_id": 3019,
  "scope": { "type": "pasal_numbers", "numbers": ["27", "28", "45"] }
}
```

**`scope` shapes** (choose one):

- `{ "type": "whole" }` — walk the entire law (paged).
- `{ "type": "pasal_numbers", "numbers": ["5", "6", "12"] }` — a specific list.
- `{ "type": "pasal_range", "from": "5", "to": "12" }` — an inclusive range.
- `{ "type": "bab", "number": "II" }` — every Pasal under a Bab.
- `{ "type": "node_ids", "ids": [11966151] }` — explicit node ids.

**`include`** (optional) selects extra per-section fields and **replaces** the default `["cross_refs"]`:

- `cross_refs` *(default)* — citations resolved against the corpus.
- `ayats` — per-ayat breakdown (`node_id` + text). Opt-in: each section already carries the full `content_text`, so request this only when you need per-ayat node ids/segmentation. For both, pass `["ayats", "cross_refs"]`.
- `node_metadata` — PDF page spans and structural ids.

Returns a `sections` list keyed by `kind` (`"pasal"` or `"bab"` — Bab rows act as delimiters during `whole`/`pasal_range` walks), bounded by `max_chars` (default 30k, hard cap 100k). Large reads return `truncated: true` + an opaque `next_cursor`; call again with `cursor` to continue. `pasal_numbers` supports partial success — missing entries land in `missing_pasals` with a hint rather than failing the whole call.

## 8. `search_within_law`

Search terms inside one known regulation. This keeps the context bounded after the relevant `law_id` is known.

**Input:**

```json
{
  "law_id": 3019,
  "query": "penghinaan pencemaran nama baik",
  "limit": 10
}
```

No-hit responses encourage retrying with broader terms and suggest `report_issue` only when the user expected specific text to exist in the parsed law.

## 9. `report_issue`

Report data quality problems from inside the MCP workflow. This is the escape hatch for OCR mistakes, missing regulations, missing Pasal, incorrect content, broken links, stale content, or other corpus issues.

**Input:**

```json
{
  "report_type": "missing_pasal",
  "title": "Pasal 74 tidak ditemukan",
  "description": "Pengguna mencari Pasal 74 UU Perseroan Terbatas tetapi hasil struktur tidak menampilkan pasal tersebut.",
  "law_type": "UU",
  "law_number": "40",
  "year": 2007,
  "pasal_number": "74",
  "reference_url": "https://peraturan.go.id"
}
```

`report_type` accepts `ocr_correction`, `missing_regulation`, `missing_pasal`, `incorrect_content`, `broken_link`, `outdated_content`, and `other`.

For `ocr_correction`, include `node_id`, `current_content`, and `suggested_content` from `get_pasal`. OCR corrections are routed to the same review queue as `/koreksi`; general reports are routed to the `/masukan` feedback queue.

## 10. `list_laws`

Browse regulations with filters when the user asks for a class of laws rather than a topical search.

**Input:**

```json
{
  "regulation_type": "UU",
  "year": 2023,
  "status": "berlaku",
  "search": "kesehatan",
  "page": 1,
  "per_page": 20
}
```

## 11. `search_court_decisions`

Search Indonesian Constitutional Court (Mahkamah Konstitusi) decisions across all four lanes — judicial review (PUU), inter-institutional disputes (SKLN), national-election results (PHPU), and regional-election results (PHPKADA). Filter by the reviewed law, lane, ruling (`amar`), year, type of review, presence of a dissenting opinion, or judge name; use `query` for topic or classification keywords.

**Input:**

```json
{
  "reviewed_law": "uu 13 2003",
  "lane": "puu",
  "amar": "dikabulkan_sebagian",
  "year": 2024,
  "has_dissent": true,
  "limit": 20
}
```

Answers questions such as "which laws did the Constitutional Court strike down in 2024" or "decisions with a dissenting opinion". `amar` accepts values like `dikabulkan_sebagian`, `ditolak`, and `inkonstitusional_bersyarat`; pass `__ketetapan__` for final orders without a merits ruling. Each result carries the ruling, decision date, reviewed-UU references, and a canonical Pasal.id reader URL.

## Language

Use Bahasa Indonesia queries for best results. Do not translate official regulation names. It is fine to answer the user in English after retrieving Indonesian source text, but citations should preserve official Indonesian titles.

## Rate Limits

Free-tier limits are enforced per authenticated user. If a client receives `429`, back off before retrying. For research or commercial limits, contact Pasal.id through [pasal.id/masukan](https://pasal.id/masukan).
