# MCP Tools

The Pasal.id MCP server exposes four tools. All are discoverable via the standard MCP `tools/list` method — the schemas below are what the server returns verbatim.

## 1. `search_laws`

Full-text search across all regulations. Uses a 3-layer architecture: identity fast-path (regulation codes like "UU 13 2003" score 1000 and short-circuit), works FTS (title/topic match), content FTS (article-body match with `ts_headline` highlights). Returns pasal-level hits with work metadata.

**Input:**

```json
{
  "query": "cuti hamil",
  "type": "UU",
  "year_from": 2000,
  "year_to": 2026,
  "limit": 10
}
```

- `query` *(required)* — Indonesian-language query. Supports short-codes: `"UU 13 2003"`, `"UUD 1945"`, `"PP 21 2019"`.
- `type` *(optional)* — `"UU" | "PP" | "PERPRES" | "PERMEN" | "PERDA" | ...` (26 types).
- `year_from` / `year_to` *(optional)* — inclusive.
- `limit` *(optional, 1-50, default 10)*.

**Returns:**

```json
{
  "results": [
    {
      "law_id": "uu-no-13-tahun-2003",
      "title": "Undang-Undang Nomor 13 Tahun 2003 tentang Ketenagakerjaan",
      "type": "UU",
      "year": 2003,
      "status": "diubah",
      "pasal_number": "82",
      "pasal_text": "Pekerja/buruh perempuan yang menggunakan hak cuti hamil...",
      "relevance_score": 0.87
    }
  ],
  "did_you_mean": null
}
```

Empty-result queries include a `did_you_mean` field with a similarity-ranked alternative when the input looks like a misspelled regulation name.

---

## 2. `get_pasal`

Retrieve a specific article (pasal) from a specific law. The most precise citation tool — pass `law_id` (from `search_laws`) and `pasal_number` directly.

**Input:**

```json
{
  "law_id": "uu-no-13-tahun-2003",
  "pasal_number": "82"
}
```

- `law_id` *(required)* — the slug returned by `search_laws`. Also accepts short forms like `"uu-13-2003"`, which redirect to the canonical.
- `pasal_number` *(required)* — exact pasal number as a string (e.g. `"82"`, `"81A"`, `"155"`).

**Returns:**

```json
{
  "law_id": "uu-no-13-tahun-2003",
  "pasal_number": "82",
  "title": "UU No. 13 Tahun 2003 tentang Ketenagakerjaan",
  "content": "(1) Pekerja/buruh perempuan berhak memperoleh istirahat...",
  "ayat_count": 2,
  "parent_bab": "BAB X — PERLINDUNGAN, PENGUPAHAN, DAN KESEJAHTERAAN",
  "source_url": "https://pasal.id/peraturan/uu/uu-no-13-tahun-2003#pasal-82"
}
```

Assistants should cite the `source_url` back to the user for verifiability.

---

## 3. `get_law_status`

Check whether a regulation is currently in force, amended, or revoked. Returns the full amendment chain so the assistant can tell the user *why* the law's text differs from what they might find elsewhere.

**Input:**

```json
{
  "law_id": "uu-no-11-tahun-2008"
}
```

**Returns:**

```json
{
  "law_id": "uu-no-11-tahun-2008",
  "title": "UU No. 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik",
  "status": "diubah",
  "status_label": "Amended",
  "amendments": [
    {
      "by": "uu-no-19-tahun-2016",
      "title": "UU No. 19 Tahun 2016",
      "date": "2016-11-25"
    },
    {
      "by": "uu-no-1-tahun-2024",
      "title": "UU No. 1 Tahun 2024",
      "date": "2024-01-02"
    }
  ],
  "replaced_by": null,
  "current_text_note": "Read the consolidated version — see amendments[] above."
}
```

Status values: `"berlaku"` (in force), `"diubah"` (amended), `"dicabut"` (revoked), `"tidak berlaku"` (not in force).

---

## 4. `list_laws`

Browse regulations without a full-text search. Useful when the user wants "all UUs from 2023" or "every amendment of the labor code."

**Input:**

```json
{
  "type": "UU",
  "year": 2023,
  "status": "berlaku",
  "limit": 20,
  "offset": 0
}
```

All fields optional. Default: most-recently-enacted first, no type/year filter, 20 per page.

**Returns:**

```json
{
  "results": [
    {
      "law_id": "uu-no-1-tahun-2023",
      "title": "UU No. 1 Tahun 2023 tentang KUHP",
      "type": "UU",
      "year": 2023,
      "status": "berlaku",
      "date_enacted": "2023-01-02"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

---

## Recommended call order

For most user questions:

1. **`search_laws`** → find the relevant law + pasal from a topic query. Capture `law_id`.
2. **`get_pasal`** → retrieve the exact article text when the user asks for detail.
3. **`get_law_status`** → verify the law is still in force before citing (critical — many high-traffic laws have been amended).
4. **`list_laws`** → browse when the user's question is categorical ("all tax laws enacted after 2020") rather than topical.

## Language

The tools accept and return Indonesian text. Regulation names are never translated (they're official legal nomenclature). Ask the assistant to translate *answer* text into English after retrieval — do not translate the regulation name itself.

## Authentication

All tools require an authenticated MCP session. See [clients.md](./clients.md) for setup; first-tool-call triggers OAuth in clients that support it (Claude Code, Claude Desktop via `mcp-proxy`), or expects a bearer token in the `Authorization` header for stateless clients.

## Rate limits

Free-tier limits per user:

- `search_laws` · `list_laws`: 60/min, 600/hour
- `get_pasal` · `get_law_status`: 120/min, 1200/hour

Hit a 429? Back off 60 seconds. For higher limits (research, commercial use), contact us via [pasal.id/masukan](https://pasal.id/masukan).
