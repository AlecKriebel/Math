#!/usr/bin/env python3
"""Record this verified publication through gws, with duplicate reconciliation.

Run only after the repository Zenodo tool has confirmed the public record.
The receipt contains this project's own row, never other tracker entries.
"""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SPREADSHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
SHEET_ID = 1254632077
GWS = "/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
HEADERS = ["Original Problem", "Solution Chat URL", "DOI", "Notes"]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def call(resource, operation, params, body=None):
    args = [GWS, "sheets", "spreadsheets", *resource, operation,
            "--params", json.dumps(params)]
    if body is not None:
        args += ["--json", json.dumps(body, ensure_ascii=False)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main():
    publication = json.loads((ROOT / "receipts/zenodo_published_inspect.json").read_text())
    require(publication["state"] == "published", "Record is not confirmed published")
    require(publication["environment"] == "production", "Record is not in production")
    doi = publication["doi"]
    record_id = publication["id"]
    require(doi == "10.5281/zenodo." + str(record_id), "DOI does not match record ID")
    doi_url = "https://doi.org/" + doi
    record_url = "https://zenodo.org/records/" + str(record_id)
    manifest = json.loads((ROOT / "zenodo-deposit.json").read_text())
    title = manifest["metadata"]["title"]
    require(publication["title"] == title, "Publication receipt belongs to another title")
    candidate = json.loads((ROOT / "receipts/candidate_v3.json").read_text())
    require(candidate["manifest_sha256"] == hashlib.sha256(
        (ROOT / "zenodo-deposit.json").read_bytes()).hexdigest(), "Manifest differs from reviewed candidate")
    expected = {f["name"]: (f["bytes"], f["sha256"]) for f in candidate["payload"]}
    observed = {f["name"]: (f["size"], f["sha256"]) for f in publication["files"]}
    require(observed == expected, "Publication receipt differs from reviewed payload")
    for item in manifest["files"]:
        path = ROOT / item["path"]
        require((path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) == expected[path.name],
                "Local file differs from reviewed payload: " + path.name)
    date = manifest["metadata"]["publication_date"]
    metadata = call([], "get", {"spreadsheetId": SPREADSHEET})
    targets = [s["properties"] for s in metadata["sheets"]
               if s["properties"]["sheetId"] == SHEET_ID]
    require(len(targets) == 1, "Numeric target tab was not uniquely resolved")
    properties = targets[0]
    tab = "'" + properties["title"].replace("'", "''") + "'"
    full_range = tab + "!A1:AQ" + str(properties["gridProperties"]["rowCount"])
    rows = call(["values"], "get", {"spreadsheetId": SPREADSHEET,
        "range": full_range, "valueRenderOption": "UNFORMATTED_VALUE"}).get("values", [])
    require(rows and rows[0][:4] == HEADERS, "Tracker headers differ from expected columns")
    values = [
        "Sperner property for every standard graded Artinian complete intersection "
        "over an arbitrary characteristic-zero field: max over all ideals of the "
        "minimal generator count equals the maximal Hilbert-function value.",
        "",
        doi_url,
        f"{title}. Alec Kriebel (ORCID 0009-0001-9320-500X); preprint/publication date {date}. "
        "Includes nonhomogeneous ideals, degree-one elimination and the empty/all-linear case; "
        "equality is attained by a power of the maximal ideal. Immediate corollary of OpenAI's "
        "Artinian EGH result and the known Harima–Wachi–Watanabe implication; no first-priority, "
        "Lefschetz, nongraded or unrestricted positive-characteristic claim. Two independent "
        "complete-package automated adversarial reviews completed; AI used extensively; "
        "not conventionally human-refereed at publication. PDF, source and verification: " + record_url
    ]
    matches = [(i, row) for i, row in enumerate(rows, 1)
               if any(doi in str(cell) or title in str(cell)
                      or re.search(r"(?:records/|zenodo\.)" + str(record_id) + r"(?:\D|$)", str(cell))
                      for cell in row)]
    receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "spreadsheet_id": SPREADSHEET, "numeric_sheet_id": SHEET_ID,
               "tab_title": properties["title"], "headers": HEADERS,
               "doi": doi, "record_id": record_id}
    if matches:
        require(len(matches) == 1, "Multiple matching rows require reconciliation")
        row_number, row = matches[0]
        require(len(row) >= 3 and row[2] == doi_url, "Matching title with a different DOI")
        require(row[:4] == values, "Existing matching row differs from intended project entry")
        updated_range = tab + f"!A{row_number}:D{row_number}"
        receipt["action"] = "existing row reconciled; no append"
    else:
        response = call(["values"], "append", {
            "spreadsheetId": SPREADSHEET, "range": tab + "!A:D",
            "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS",
            "includeValuesInResponse": True,
            "responseValueRenderOption": "UNFORMATTED_VALUE"},
            {"majorDimension": "ROWS", "values": [values]})
        updated_range = response["updates"]["updatedRange"]
        require(response["updates"]["updatedRows"] == 1, "Append did not report exactly one row")
        require(response["updates"]["updatedColumns"] == 4, "Append did not report exactly four columns")
        receipt.update({"action": "appended one row", "append_response": response})
        (ROOT / "receipts/tracker_append.json").write_text(json.dumps(receipt, indent=2) + "\n")
    readback = call(["values"], "get", {"spreadsheetId": SPREADSHEET,
        "range": updated_range, "valueRenderOption": "UNFORMATTED_VALUE"})
    require(readback["values"] == [values], "Tracker readback differs from intended row")
    receipt.update({"verified": True, "updated_range": updated_range,
                    "values": values, "readback": readback})
    (ROOT / "receipts/tracker_verified.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"verified": True, "range": updated_range, "doi": doi,
                      "action": receipt["action"]}, indent=2))


if __name__ == "__main__":
    main()
