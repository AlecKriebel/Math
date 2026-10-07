# Tracker CLI preflight — 2026-10-07

Prepared at 2026-10-07 15:29 UTC from `research/PROJECT_BRIEF.txt`, item 7, the repository's independent-research instructions, and the installed CLI's current help/schema. This document is a local protocol, not a tracker receipt. No live spreadsheet or account data was fetched, no row was written, and no Git operation or communication with an external individual was performed.

Tracker-protocol preparation: **100%**. Verified tracker completion: **0%**. Mathematical and publication readiness are assessed by the lead researcher, not by this CLI preflight.

## Scope and instruction fallback

The lead researcher read `/Users/alec/.agents/skills/gws-sheets/SKILL.md`. Its required `../gws-shared/SKILL.md` was missing, and the lead's search across `.agents`, `.codex/skills`, and plugins found no copy. The missing prerequisite was handled by direct documentation from the installed CLI rather than generating skills. No `generate-skills` command was run. The project brief expressly prohibits using skill generation to obtain help in the research checkout.

The publication/tracker authorization is already present in the project brief. The gate for executing this protocol is **confirmed production Zenodo publication with an assigned DOI**, not a reserved draft DOI. Root owns all live publication state, tracker requests, and receipts; this subagent prepared only this document and disposable local schema scratch.

## Verified installed interface

Executable: `/Users/alec/.nvm/versions/node/v22.16.0/bin/gws`.

Version checked: `gws 0.22.5`. Current documentation commands inspected successfully:

```text
gws --help
gws sheets --help
gws schema sheets.spreadsheets.get
gws schema sheets.spreadsheets.get --resolve-refs
gws schema sheets.spreadsheets.values.get
gws schema sheets.spreadsheets.values.append
gws schema sheets.spreadsheets.values.append --resolve-refs
gws sheets spreadsheets values get --help
gws sheets spreadsheets values append --help
```

Local validation finished at 2026-10-07 15:31:39 UTC. All six Python blocks below parse successfully. A second local dry-run of the resource append command returned `dry_run: true`, method `POST`, a `ROWS` one-row body, and the exact query parameters `valueInputOption=RAW`, `insertDataOption=INSERT_ROWS`, `includeValuesInResponse=true`, and `responseValueRenderOption=UNFORMATTED_VALUE`. Its test range was the nonexistent, documentation-only `Preflight!A1:Z`; no API request was sent and no actual target title was assumed. Concise dry-run/schema evidence is retained in the owned ignored scratch directory.

The resource command is:

```text
gws sheets spreadsheets values append --params <JSON> --json <JSON>
```

Do not use the `+append` convenience helper: the resource command exposes the explicit target range and required input/insert options. `--dry-run` is documented to validate locally without sending the request. A metadata-get dry-run accepted `fields` in `--params`, even though `fields` is a common API query parameter rather than a property in this resource's parameter listing. The dry-run produced a GET description with `dry_run: true`, `includeGridData: false`, and the requested field mask; it did not fetch the spreadsheet.

Relevant schema facts:

| Operation | Verified fields and behavior |
| --- | --- |
| `spreadsheets.get` | Required `spreadsheetId`; optional `ranges`, `includeGridData`. `sheets[].properties` includes numeric `sheetId`, `title`, `sheetType`, and `gridProperties.rowCount` / `columnCount`. Default grid data is omitted. A supplied field mask controls whether grid data is included. |
| `values.get` | Required `spreadsheetId`, `range`; optional `majorDimension: ROWS`, `valueRenderOption: FORMATTED_VALUE / UNFORMATTED_VALUE / FORMULA`, `dateTimeRenderOption: SERIAL_NUMBER / FORMATTED_STRING`. Output excludes empty trailing rows/columns; pad missing cells with empty strings for comparison. |
| `values.append` | Required spreadsheet ID and A1 range; explicitly supply `valueInputOption: RAW`, `insertDataOption: INSERT_ROWS`, `includeValuesInResponse: true`, and `responseValueRenderOption: UNFORMATTED_VALUE`. The input range finds a logical table; the server chooses the row after that table. It is not an instruction to write at an assumed row number. |
| Request body | `majorDimension: ROWS`, `values: [[...]]`; booleans, strings and doubles are supported. `null` skips a cell, whereas `""` explicitly supplies an empty value. Use strings for DOI, title, URLs, author, and publication-date text. |
| Append response | `spreadsheetId`, `tableRange` before the append, and `updates.updatedRange`, `updatedRows`, `updatedColumns`, `updatedCells`; `updates.updatedData` is returned when `includeValuesInResponse` is true. |
| Hyperlink coverage | A displayed cell label need not contain its URL. Structured `CellData` supports `hyperlink`, `userEnteredValue.formulaValue`, `textFormatRuns[].format.link.uri`, and `chipRuns[].chip.richLinkProperties.uri`. `hyperlink` can be empty when a cell contains multiple links. |

CLI exit codes are 0 success, 1 API error, 2 auth error, 3 argument validation, 4 discovery error, and 5 internal error. Do not interpret nonzero return codes or malformed/truncated output as proof that a write did not happen.

## Execution protocol after the publication gate

Spreadsheet ID: `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`.

Required numeric target tab ID: **1254632077**.

Use the exact verified published title, author, publication date, DOI, and public Zenodo record URL from the publication receipt. Do not infer those fields from a draft manifest or the current system date. Carry the Zenodo deposit/record ID separately for duplicate detection.

The following Python helper produces argument arrays and JSON strings, so titles containing apostrophes, dollar signs, backticks, quotes, Unicode, or newlines are not interpreted as shell code. It is an invocation scaffold, not an executable request saved by this preflight:

```python
import json
import subprocess

GWS = "/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
SPREADSHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
TARGET_SHEET_ID = 1254632077

def gws(resource, params, body=None, *, dry_run=False):
    args = [GWS, "sheets", *resource,
            "--params", json.dumps(params, ensure_ascii=False),
            "--format", "json"]
    if body is not None:
        args += ["--json", json.dumps(body, ensure_ascii=False)]
    if dry_run:
        args += ["--dry-run"]
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    # Persist nonsecret response/request receipts in root-owned locations.
    # On a nonzero return code or invalid JSON, reconcile before any retry.
    if result.returncode != 0:
        raise RuntimeError(f"gws returned exit code {result.returncode}")
    return json.loads(result.stdout)

def column_name(n):
    assert isinstance(n, int) and n > 0
    result = ""
    while n:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def quote_tab(title):
    return "'" + title.replace("'", "''") + "'"
```

### 1. Resolve the actual tab and dimensions

```python
metadata = gws(["spreadsheets", "get"], {
    "spreadsheetId": SPREADSHEET,
    "includeGridData": False,
    "fields": (
        "spreadsheetId,spreadsheetUrl,"
        "sheets(properties(sheetId,title,sheetType,"
        "gridProperties(rowCount,columnCount)))"
    ),
})
assert metadata["spreadsheetId"] == SPREADSHEET
matches = [s["properties"] for s in metadata["sheets"]
           if s["properties"]["sheetId"] == TARGET_SHEET_ID]
assert len(matches) == 1
tab = matches[0]
assert tab.get("sheetType", "GRID") == "GRID"
quoted_tab = quote_tab(tab["title"])
row_count = tab["gridProperties"]["rowCount"]
column_count = tab["gridProperties"]["columnCount"]
last_column = column_name(column_count)
full_range = f"{quoted_tab}!A1:{last_column}{row_count}"
```

The numeric `gid` is not an A1 sheet name. Never substitute the spreadsheet's first tab, assume the URL fragment is a title, or rely on a title from another project. Record the resolved title and dimensions. Re-fetch metadata before the final scan/append if another writer may have changed the tab or its dimensions.

### 2. Inspect actual headers, nearby rows, and the whole target tab

```python
top = gws(["spreadsheets", "values", "get"], {
    "spreadsheetId": SPREADSHEET,
    "range": f"{quoted_tab}!A1:{last_column}{min(30, row_count)}",
    "majorDimension": "ROWS",
    "valueRenderOption": "FORMATTED_VALUE",
})
formatted = gws(["spreadsheets", "values", "get"], {
    "spreadsheetId": SPREADSHEET,
    "range": full_range,
    "majorDimension": "ROWS",
    "valueRenderOption": "FORMATTED_VALUE",
})
formulas = gws(["spreadsheets", "values", "get"], {
    "spreadsheetId": SPREADSHEET,
    "range": full_range,
    "majorDimension": "ROWS",
    "valueRenderOption": "FORMULA",
})
```

Determine the actual header row, table start/end columns, existing date convention, and required column order. Inspect the last few populated table rows as well as the top rows. Blank rows, notes, or multiple tables require choosing the explicit logical-table range deliberately; do not assume the table starts in A or the header is row 1. `full_range` is for complete duplicate scanning, not necessarily the final append range. If the tab is very large, read all rows in disjoint bounded chunks covering the full grid; values.get has no pagination that substitutes for missing ranges. Record every covered range.

Obtain structured hyperlink data for complete identity checking, since `values.get` can return only display labels for rich links:

```python
link_data = gws(["spreadsheets", "get"], {
    "spreadsheetId": SPREADSHEET,
    "ranges": [full_range],
    "fields": (
        "spreadsheetId,sheets(properties(sheetId),"
        "data(startRow,startColumn,rowData(values("
        "userEnteredValue,effectiveValue,formattedValue,hyperlink,"
        "textFormatRuns(format(link)),"
        "chipRuns(chip(richLinkProperties(uri)))"
        "))))"
    ),
})
```

Keep only the sheet with `properties.sheetId == TARGET_SHEET_ID`. Grid data `startRow` / `startColumn` are zero-based and may be omitted when zero; combine them with array indices to recover exact cell and row coordinates. For chunked reads preserve each chunk's offsets. This field mask includes actual text, formula and link destinations but does not request comments or people-chip identities.

### 3. Detect an existing exact publication before writing

Search **every row of this target tab**, not merely the header preview or a handful of recent rows. Compare each displayed/literal value and each actual hyperlink destination against the verified publication identities. Do not rely on substring grep of raw JSON.

- DOI: accept an exact bare DOI, an exact `doi:` form, or an exact DOI resolver URL (`https://doi.org/…` or the legacy `http(s)://dx.doi.org/…`). Remove only those recognized wrappers and surrounding whitespace; compare the complete canonical DOI case-insensitively. Do not accept a shared prefix or a DOI embedded inside a different identifier. The canonical DOI remains exactly the confirmed one.
- Deposit/record: compare exact public Zenodo URL paths `/records/<id>` or legacy `/record/<id>`, with the complete decimal ID equal to the verified record ID. Ignore only a trailing slash and URL query/fragment. Compare a bare numeric/string record ID only in an identified deposit/record-ID column; a matching number in another column could be a year or index.
- Title: compare the complete exact published title, allowing only surrounding whitespace removal, against literal/displayed values. An exact title is a candidate duplicate requiring row inspection even if DOI/URL is absent; do not append past such a candidate without resolving it.
- For a `HYPERLINK` formula, compare the link destination exposed by structured `hyperlink`/run-link data rather than treating a matching substring in a formula as proof. Structured link-run and rich-link URI lists cover multiple links where `hyperlink` may be empty. If a formula-built link cannot be resolved, inspect the formula and corresponding row before appending.

Record every candidate's exact row/cells and match reason. If a DOI or record-ID match exists, inspect the whole row and check it refers to this publication. If one correct row already exists, read it back and use it as the tracker receipt; append nothing. If multiple candidates or conflicting fields exist, resolve them within the tracker only; do not publish a second Zenodo record. A title-only match is an unresolved identity check, not automatically proof of either duplication or novelty.

### 4. Build one row from the actual schema

Build one array in the inspected physical column order, with one cell per table column. Include the confirmed DOI and fields actually required by the existing sheet: the precise title, `Alec Kriebel`, the verified publication date in the sheet's convention, the subject/problem and DOI/Zenodo links. If the sheet has a meaningful status/type field, use its existing vocabulary and the confirmed publication state. Keep genuinely unknown optional fields as `""`; do not invent problem numbers, citations, novelty labels, affiliations, or review statuses. Do not create columns, reorder headers, rewrite existing rows, or replace existing formulas.

The physical row array must align with the first column of the selected logical table. In particular, a table starting in B needs a B-starting append range and an array whose first item is that B column; it does not need a fabricated A value. If required column meanings cannot be inferred from headers and nearby rows, that concrete schema issue remains pending until resolved.

Save the nonsecret request payload, verified publication identities, header mapping, explicit target range and duplicate-search result before issuing the mutation. The append range must cover the intended table's actual columns and header through its data; a whole-column range is suitable only when the inspected tab has one unambiguous table in those columns.

### 5. Dry-run, append once, and validate the response

```python
# Set append_range and row only after inspecting the actual sheet schema.
params = {
    "spreadsheetId": SPREADSHEET,
    "range": append_range,
    "valueInputOption": "RAW",
    "insertDataOption": "INSERT_ROWS",
    "includeValuesInResponse": True,
    "responseValueRenderOption": "UNFORMATTED_VALUE",
}
body = {"majorDimension": "ROWS", "values": [row]}
validated = gws(["spreadsheets", "values", "append"], params, body,
                dry_run=True)
assert validated["dry_run"] is True

# Execute only after the verified publication gate and duplicate check.
response = gws(["spreadsheets", "values", "append"], params, body)
assert response["spreadsheetId"] == SPREADSHEET
updates = response["updates"]
assert updates["updatedRows"] == 1
inserted_range = updates["updatedRange"]
```

Persist the actual append response immediately and inspect `tableRange` plus `updates.updatedRange`; the latter is authoritative for where the row landed. Check its quoted tab name and exact columns/row against the chosen table and resolved target. Do not manufacture a row number from the old last row. `updatedColumns` / `updatedCells` are additional diagnostics; empty trailing values can be omitted from returned value arrays, so pad to the intended width when comparing. If the append went to an unexpected range, preserve the evidence and reconcile that tracker row before retrying.

There is no append idempotency key in the inspected schema. Re-run the complete identity scan immediately before the append if time or other work elapsed. If the process times out, JSON is truncated, an API/internal error is ambiguous, or the connection drops, **do not immediately repeat the append**. Re-fetch metadata and the target tab, re-run exact identity checks, and locate/read back any matching row. Retry the tracker write only if reconciliation establishes that no row was added. No tracker failure authorizes republishing the paper.

### 6. Independent readback and final tracker receipt

```python
readback = gws(["spreadsheets", "values", "get"], {
    "spreadsheetId": SPREADSHEET,
    "range": inserted_range,
    "majorDimension": "ROWS",
    "valueRenderOption": "UNFORMATTED_VALUE",
    "dateTimeRenderOption": "FORMATTED_STRING",
})
returned = readback.get("values", [])
assert len(returned) == 1
actual = returned[0] + [""] * (len(row) - len(returned[0]))
assert actual == row
```

Reconfirm metadata still maps `1254632077` to the inserted range's tab and perform a final exact-identity scan to establish one correct row. Keep the exact inserted/readback range, actual ordered values, resolved numeric tab/title, publication DOI and record ID, UTC timestamp, request, append response, and readback as nonsecret receipts. If an existing row was found instead of appending, retain its exact range/readback and explicitly record that no mutation was needed.

## Exact remaining steps

1. Root confirms the published production Zenodo record, assigned DOI, exact metadata and intended files.
2. Root fetches spreadsheet metadata, resolves numeric tab **1254632077**, and inspects the actual headers/table.
3. Root scans all target rows and actual link destinations for the exact confirmed DOI, record ID and title; reconciles any candidate.
4. Root prepares and locally validates one schema-aligned RAW / INSERT_ROWS request, then appends at most once if no matching row exists.
5. Root reads the exact affected row back, reconciles uniqueness, and records the exact range/values with the publication receipt.
6. Root checkpoints the final owned sources and nonsecret receipts using the project's main-only Git/publication protocol.

Until those steps finish, this preflight is not evidence of tracker completion or proof of spreadsheet access.
