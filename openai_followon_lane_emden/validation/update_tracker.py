#!/usr/bin/env python3
"""One authorized tracker append, with preflight reconciliation and readback.

Existing spreadsheet contents remain in ignored tracker_private/ only.
This script refuses to append if any identifier is already present.
"""
import datetime
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "validation" / "tracker_private"
GWS = "/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
SPREADSHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
SHEET_ID = 1254632077
DOI = "10.5281/zenodo.23203323"
TITLE = "A priori estimates across the subcritical Lane–Emden hyperbola"
HEADERS = ["Original Problem", "Solution Chat URL", "DOI", "Notes"]
ROW = [
    "Complete subcritical Lane–Emden a priori estimates: n>=3, p,q>1, "
    "1/(p+1)+1/(q+1)>(n-2)/n; classical nonnegative solutions of "
    "-Delta u=v^p, -Delta v=u^q.",
    "",
    "https://doi.org/" + DOI,
    TITLE + " — Alec Kriebel (ORCID 0009-0001-9320-500X), preprint date "
    "2026-10-06; production publication confirmed 2026-10-07 UTC. Universal "
    "distance/gradient estimates and exterior decay; unrestricted classical "
    "zero-Dirichlet half-space nonexistence; fixed bounded C2-domain uniform "
    "bounds and strong W2,r/C1,gamma compactness. Global C2,theta bounds require "
    "C2,theta boundary, with compactness in C2,eta for eta<theta. Immediate "
    "consequence of OpenAI family370's audited entire Liouville theorem and "
    "established Polacik–Quittner–Souplet/Quittner–Souplet transfers; no "
    "independent base-conjecture solution, new transfer mechanism or first "
    "priority claim. Two complete-package independent AI adversarial reviews "
    "passed after documentation repair; extensive AI use; no conventional human "
    "peer review; complete upstream Lean kernel build/axiom audit not reproduced. "
    "Public PDF/archive hashes verified. https://zenodo.org/records/23203323",
]


def call(parts, params, stem, body=None):
    argv = [GWS, "sheets", "spreadsheets", *parts, "--params", json.dumps(params)]
    if body is not None:
        argv += ["--json", json.dumps(body)]
    result = subprocess.run(argv, capture_output=True, text=True)
    (PRIVATE / (stem + ".json")).write_text(result.stdout)
    (PRIVATE / (stem + ".stderr.txt")).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(f"gws {stem} returned {result.returncode}; reconcile before retry")
    return json.loads(result.stdout)


def matches(rows):
    identifiers = (DOI, "23203323", TITLE)
    return [(i + 1, row) for i, row in enumerate(rows)
            if any(token in str(cell) for cell in row for token in identifiers)]


def main():
    PRIVATE.mkdir(exist_ok=True)
    publication = json.loads((ROOT / "receipts" / "zenodo_inspect_final.json").read_text())
    assert publication["state"] == "published" and publication["doi"] == DOI
    assert publication["doi_resolution"]["status"] == "resolved"
    metadata = call(["get"], {"spreadsheetId": SPREADSHEET,
        "fields": "spreadsheetId,sheets(properties(sheetId,title,gridProperties))"}, "append_metadata")
    targets = [s["properties"] for s in metadata["sheets"]
               if s["properties"]["sheetId"] == SHEET_ID]
    assert len(targets) == 1
    target = targets[0]
    tab = "'" + target["title"].replace("'", "''") + "'"
    full_range = tab + "!A1:AQ" + str(target["gridProperties"]["rowCount"])
    before = call(["values", "get"], {"spreadsheetId": SPREADSHEET,
        "range": full_range, "valueRenderOption": "FORMULA"}, "append_before")
    assert before["values"][0] == HEADERS, "Actual tracker headers changed"
    existing = matches(before["values"])
    if existing:
        raise RuntimeError(f"Existing candidate at row(s) {[r for r, _ in existing]}; do not append")
    intent = {"spreadsheet_id": SPREADSHEET, "sheet_id": SHEET_ID,
        "tab_title": target["title"], "headers": HEADERS, "intended_values": ROW,
        "duplicate_matches_before": 0, "value_input_option": "RAW"}
    (ROOT / "receipts" / "tracker_intent.json").write_text(json.dumps(intent, indent=2) + "\n")
    appended = call(["values", "append"], {"spreadsheetId": SPREADSHEET,
        "range": tab + "!A:D", "valueInputOption": "RAW",
        "insertDataOption": "INSERT_ROWS", "includeValuesInResponse": True,
        "responseValueRenderOption": "FORMULA"}, "append_response",
        {"majorDimension": "ROWS", "values": [ROW]})
    update = appended["updates"]
    assert update["updatedRows"] == 1 and update["updatedColumns"] == 4
    actual_range = update["updatedRange"]
    readback = call(["values", "get"], {"spreadsheetId": SPREADSHEET,
        "range": actual_range, "valueRenderOption": "FORMULA"}, "readback")
    assert readback["values"] == [ROW], "Readback values mismatch"
    after = call(["values", "get"], {"spreadsheetId": SPREADSHEET,
        "range": full_range, "valueRenderOption": "FORMULA"}, "append_after")
    found = matches(after["values"])
    assert len(found) == 1 and found[0][1] == ROW, "Candidate duplication/mismatch"
    # Require all preexisting values/formulas to be identical. Concurrent
    # appenders may add later rows, which does not affect this prefix check.
    assert after["values"][:len(before["values"])] == before["values"]
    receipt = dict(intent, status="verified", range=actual_range, values=readback["values"],
        actual_row=found[0][0], matching_rows_after=1,
        existing_value_and_formula_prefix_preserved=True,
        verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        spreadsheet_url="https://docs.google.com/spreadsheets/d/" + SPREADSHEET
            + "/edit?gid=" + str(SHEET_ID) + "#gid=" + str(SHEET_ID))
    (ROOT / "receipts" / "tracker_verified.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
