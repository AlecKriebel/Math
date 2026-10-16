#!/usr/bin/env python3
"""One read-only GWS +read of the exact four supplied tracker cells.

Never reads a credential/config file, changes authentication, writes a sheet,
or prints raw CLI responses. The private configuration override is passed only
to the GWS child process after actual administrative details are supplied.
"""
import argparse, copy, datetime, hashlib, json, os, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
OWN = Path(__file__).resolve().parents[1]

def need(value, message):
    if not value: raise RuntimeError(message)

def canonical_range(value):
    need(isinstance(value, str) and "!" in value, "Named exact four-cell range required")
    sheet, cells = value.rsplit("!", 1)
    if sheet.startswith("'") and sheet.endswith("'"):
        sheet = sheet[1:-1].replace("''", "'")
    found = re.fullmatch(r"\$?([A-Z]+)\$?([1-9][0-9]*):\$?([A-Z]+)\$?([1-9][0-9]*)", cells)
    need(sheet and found, "Explicit single-row A1 interval required")
    first, row1, last, row2 = found.groups()
    def col(s):
        n = 0
        for c in s: n = 26*n+ord(c)-ord("A")+1
        return n
    need(row1 == row2 and col(last)-col(first) == 3, "Read must request exactly four cells in one row")
    return sheet, first, row1, last, row2

def compare(response, wanted, requested_range):
    need(isinstance(wanted, list) and len(wanted) == 4 and all(isinstance(x, str) for x in wanted), "Exactly four expected string cells required")
    need(isinstance(response, dict) and response.get("majorDimension", "ROWS") == "ROWS", "Unexpected GWS response layout")
    need(canonical_range(response.get("range")) == canonical_range(requested_range), "Returned tracker range differs from exact requested four cells")
    cells = response.get("values")
    need(isinstance(cells, list) and len(cells) == 1 and isinstance(cells[0], list)
         and len(cells[0]) == 4 and cells[0] == wanted, "Tracker exact four cells differ")
    return [{"column_offset": i, "UTF8_bytes": len(v.encode()), "sha256": hashlib.sha256(v.encode()).hexdigest(), "exact": True} for i,v in enumerate(cells[0])]

def controls():
    wanted = ["30001478", "https://doi.org/10.5281/zenodo.CONTROL", "Exact accepted scope", "Priority unresolved"]
    good = {"values": [wanted], "majorDimension": "ROWS", "range": "Sheet1!A1:D1"}
    cases = []
    def test(name, response, expected):
        try: compare(response, wanted, "Sheet1!A1:D1"); accepted = True
        except RuntimeError: accepted = False
        cases.append({"case": name, "accepted": accepted, "control_pass": accepted == expected})
    test("exact_four_cells", good, True)
    for i in range(4):
        response = copy.deepcopy(good); response["values"][0][i] += " changed"
        test("changed_cell_%d" % i, response, False)
    response = copy.deepcopy(good); response["values"][0].pop(); test("missing_cell", response, False)
    response = copy.deepcopy(good); response["values"][0].append("extra"); test("extra_cell", response, False)
    response = copy.deepcopy(good); response["values"].append(wanted); test("extra_row", response, False)
    response = copy.deepcopy(good); response["range"] = "Sheet1!A2:D2"; test("wrong_returned_row", response, False)
    response = copy.deepcopy(good); response["range"] = "OtherSheet!A1:D1"; test("wrong_returned_sheet", response, False)
    response = copy.deepcopy(good); response["range"] = "Sheet1!A1:E1"; test("range_spans_extra_cell", response, False)
    response = copy.deepcopy(good); response["range"] = "'Sheet1'!$A$1:$D$1"; test("same_exact_range_standard_A1_quoting", response, True)
    need(all(c["control_pass"] for c in cases), "Tracker parser control failed")
    return cases

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--controls-only", action="store_true"); p.add_argument("--gws-bin", type=Path)
    p.add_argument("--config-dir", type=Path); p.add_argument("--spreadsheet"); p.add_argument("--range")
    p.add_argument("--expected-row", type=Path); p.add_argument("--out", type=Path)
    a = p.parse_args()
    result = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "controls": controls(),
              "sheet_mutation_methods_invoked": 0, "private_auth_or_raw_response_saved_in_packet": False}
    if a.controls_only:
        need(not any((a.gws_bin, a.config_dir, a.spreadsheet, a.range, a.expected_row)), "Controls cannot imply actual tracker verification")
        result["result"] = "PASS_TRACKER_PARSER_CONTROLS_ONLY"
    else:
        need(all((a.gws_bin, a.config_dir, a.spreadsheet, a.range, a.expected_row)), "Parent-supplied actual read-only parameters required")
        canonical_range(a.range)
        wanted = json.loads(a.expected_row.read_text())
        if isinstance(wanted, dict): wanted = wanted["values"]
        if isinstance(wanted, list) and len(wanted) == 1 and isinstance(wanted[0], list): wanted = wanted[0]
        env = os.environ.copy(); env["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = str(a.config_dir)
        command = [str(a.gws_bin), "sheets", "+read", "--spreadsheet", a.spreadsheet, "--range", a.range]
        run = subprocess.run(command, env=env, capture_output=True, text=True, timeout=90)
        need(run.returncode == 0 and not run.stderr, "Read-only GWS did not return a clean successful response")
        try: response = json.loads(run.stdout)
        except ValueError: raise RuntimeError("Read-only GWS response was not JSON") from None
        cell_receipts = compare(response, wanted, a.range)
        result.update(result="PASS_TRACKER_EXACT_FOUR_CELLS", spreadsheet_id=a.spreadsheet,
                      requested_range=a.range, returned_range=response.get("range"),
                      exact_requested_and_returned_four_cell_range=True,
                      exact_row_sha256=hashlib.sha256(json.dumps(wanted, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest(),
                      cells=cell_receipts, read_only_GWS_private_override_used=True)
    raw = json.dumps(result, indent=2)+"\n"
    if a.out:
        need(a.out.resolve().is_relative_to(OWN), "Output outside owned admin area")
        a.out.write_text(raw)
    print(raw)

if __name__ == "__main__": main()
