"""Use the requested GWS CLI to append the verified DOI exactly once."""
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess

HERE = Path(__file__).resolve().parent
PUB = HERE.parent / "publication"
OUT = PUB / "tracker-private"
OUT.mkdir(parents=True, exist_ok=True)
GWS = "/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
SPREADSHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"

def call(label, args):
    r = subprocess.run([GWS, *args], capture_output=True, text=True)
    (OUT / (label + ".stdout.json")).write_text(r.stdout)
    (OUT / (label + ".stderr.txt")).write_text(r.stderr)
    if r.returncode:
        raise RuntimeError(label + " failed; reconcile saved outputs before any retry")
    return json.loads(r.stdout)

assert not (PUB / 'TRACKER_VERIFIED_APPEND.json').exists(), 'Verified append already recorded; read-only reconciliation only'
record = json.loads((PUB / "ZENODO_VERIFIED_PUBLICATION.json").read_text())
assert record["submitted"] and record["metadata_and_files_verified"]
doi = record["doi_url"]
meta = call("01-sheet-metadata", ["sheets", "spreadsheets", "get", "--params",
            json.dumps({"spreadsheetId": SPREADSHEET,
                        "fields": "sheets.properties"})])
matches = [x["properties"] for x in meta["sheets"]
           if x["properties"]["sheetId"] == 1254632077]
assert len(matches) == 1 and matches[0]["title"] == "Math Puzzles"
allrows = call("02-before-rows", ["sheets", "+read", "--spreadsheet", SPREADSHEET,
              "--range", "'Math Puzzles'!A:D"])
values = allrows.get("values", [])
assert values[0] == ["Original Problem", "Solution Chat URL", "DOI", "Notes"]
existing = [row for row in values if doi in row]
assert not existing, "DOI already exists; use read-only reconciliation, not append"
row = [
    "https://www.unsolvedmath.com/problems/AMR-050-0020",
    "",
    doi,
    "An odd-period pedal-antipedal area invariant in elliptic billiards — "
    "Alec Kriebel, v1.0, 2026-10-13. Proof of k403,a for the original orbit, "
    "least odd periods, strict confocal elliptical caustics and admitted coprime "
    "stars; all real antipedal intersections finite. Direct circular extension "
    "and exact even-period counterexample. Independent mathematical reproduction "
    "and two fresh sequential adversarial preprint reviews passed. Bounded "
    "priority audit; original observation, classical methods and prior pedal "
    "argument credited; no firstness certificate. AI tools used extensively; "
    "unrefereed, no external human peer review. Includes source and verification package."
]
payload = {"majorDimension": "ROWS", "values": [row]}
(OUT / "APPEND_VALUES.json").write_text(json.dumps(payload, indent=2) + "\n")
response = call("03-append", ["sheets", "spreadsheets", "values", "append",
                "--params", json.dumps({"spreadsheetId": SPREADSHEET,
                "range": "'Math Puzzles'!A:D", "valueInputOption": "RAW",
                "insertDataOption": "INSERT_ROWS", "includeValuesInResponse": True}),
                "--json", json.dumps(payload)])
updates = response["updates"]
assert updates["updatedRows"] == 1 and updates["updatedCells"] == 4
target = updates["updatedRange"]
readback = call("04-row-readback", ["sheets", "+read", "--spreadsheet", SPREADSHEET,
                "--range", target])
assert readback["values"] == [row]
receipt = {"utc": datetime.now(timezone.utc).isoformat(), "verified": True,
           "spreadsheet_id": SPREADSHEET, "sheet_id": 1254632077,
           "updated_range": target, "doi_url": doi, "values": row,
           "cli": "Google Workspace CLI", "append_count": 1}
(PUB / "TRACKER_VERIFIED_APPEND.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
