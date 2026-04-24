# MCP Tools

The Pasal.id MCP server exposes nine intent-level tools. The live server is Indonesian-first: tool descriptions, parameter descriptions, and workflow prompts are written for Indonesian legal research, while the returned regulation names preserve official nomenclature.

All tools require an authenticated MCP session.

## Recommended Workflow

1. Start with `search_laws` for topics, keywords, and loose references.
2. Use `get_law_overview` or `get_law_structure` when the assistant needs provenance or the regulation map.
3. Use `get_pasal` for an exact Pasal, or `get_law_part` for a bounded part such as Bab II, Menimbang, Mengingat, Penutup, or Lampiran.
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

Successful responses include `node_id`, `content_text`, Pasal/ayat content, `pasal_url`, `law_url`, `source_pdf_url`, `source_family`, `content_verified`, and `correction_url` so users can inspect or correct OCR issues.

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

`part_type` supports `preamble`, `menimbang`, `mengingat`, `memutuskan`, `menetapkan`, `penutup`, `penjelasan`, and `lampiran`.

Large parts return `truncated: true` and `next_cursor`; call again with the cursor to continue.

## 7. `search_within_law`

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

## 8. `report_issue`

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

`report_type` supports `ocr_correction`, `missing_regulation`, `missing_pasal`, `incorrect_content`, `broken_link`, `outdated_content`, and `other`.

For `ocr_correction`, include `node_id`, `current_content`, and `suggested_content` from `get_pasal`. OCR corrections are routed to the same review queue as `/koreksi`; general reports are routed to the `/masukan` feedback queue.

## 9. `list_laws`

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

## Language

Use Bahasa Indonesia queries for best results. Do not translate official regulation names. It is fine to answer the user in English after retrieving Indonesian source text, but citations should preserve official Indonesian titles.

## Rate Limits

Free-tier limits are enforced per authenticated user. If a client receives `429`, back off before retrying. For research or commercial limits, contact Pasal.id through [pasal.id/masukan](https://pasal.id/masukan).
