#!/usr/bin/env python3
"""One verified publication, one append, exact read-back and uncertain-outcome guard."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from publication_check import zenodo_dois
from sweep_io import atomic_json
from publication_live_gates import collect, require_release_clearance

SHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
RANGE = "'Math Puzzles'!A:D"


def desired_row(identifier):
    return [
        "9700002 / AMR-096-0002: Aldous congestion toy model; joint designed-tree outer phases",
        "", "https://doi.org/10.5281/zenodo." + str(identifier),
        "A designed tree model with a sharp congestion–fragmentation transition — Alec Kriebel "
        "(ORCID0009-0001-9320-500X), v1.0 (2026-10-21). Five-page unrefereed research note: "
        "an exact specialized existence model motivated by Aldous's conceptual request, with a complete "
        "analytic joint marginal-admission/spare-connectivity theorem. Sparse binary physical trees carry "
        "dense k² cross-root streams; positive linear capacity prices give the unique cheapest doubled-unit-demand "
        "design, with capacities growing with k. Independent fixed-law Exp(1) affine slopes have quadratic time "
        "variance; exact finite right marginal uses the actual offered slope. The explicit all-cuts bound confines "
        "both changes to width16sqrt(log(k)/k) with high probability; every optimizer has the whole tree spare "
        "below the lower endpoint and every edge saturated above the upper endpoint. Width is an upper bound, "
        "not optimal scaling; no critical r(2), generic-network, adaptive-growth, canonical-right-model or first-transition "
        "claim. Classical transport/concentration, HOT, prior congestion/percolation models and Aldous's2005 tree-realism "
        "reservation credited. Bounded primary priority audit found no authenticated exact earlier construction/theorem; "
        "final1993 KMN journal body, unindexed/unpublished work and editions remain coverage limits. "
        "Three independent mathematical/source families and two sequential new full-package AI adversaries completed. "
        "Original24 files preserved; PDF plus editable-source/verification ZIP and a narrowly tested replay derivative "
        "with exact active output and only enumerated old diagnostic allowances. Historical unpinned byte replay is not claimed. "
        "Extensive AI use in research, proof/model development, computation, writing and auditing; no formal independent human "
        "peer review. Primary problem: https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html. "
        "Record: https://zenodo.org/records/" + str(identifier) +
        ". PR: https://github.com/AlecKriebel/Math/pull/397."
    ]


def gws(action, params, body=None):
    command = ["gws", "sheets", "spreadsheets", "values", action, "--params", json.dumps(params)]
    if body is not None:
        command += ["--json", json.dumps(body)]
    run = subprocess.run(command, capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError("GWS failed; inspect saved intent/live sheet before any retry: " + run.stderr[:700])
    return json.loads(run.stdout)


def read(label, operation):
    value = gws("get", {"spreadsheetId": SHEET, "range": "'Math Puzzles'!A:AQ",
                        "valueRenderOption": "FORMATTED_VALUE"})
    atomic_json(ROOT / "raw/pr0397" / (label + "_" + operation + ".json"), value)
    rows = value["values"]
    if rows[0] != ["Original Problem", "Solution Chat URL", "DOI", "Notes"]:
        raise RuntimeError("Tracker schema changed")
    return rows


def matches(rows, identifier):
    doi = "10.5281/zenodo." + str(identifier)
    found = []
    for number, row in enumerate(rows[1:], 2):
        text = " ".join(map(str, row))
        compact = re.sub(r"[^a-z0-9]", "", text.casefold())
        if (re.search(r"(?<!\d)9700002(?!\d)", text)
                or "amr0960002" in compact
                or any(doi in zenodo_dois(v) for v in row)
                or re.search(r"github\.com/AlecKriebel/Math/pull/397(?!\d)", text, re.I)
                or "designedtreemodelwithasharpcongestion" in compact
                or ("congestion" in compact and "spare" in compact and "exponential" in compact)
                or ("crossroot" in compact and "spare" in compact)):
            found.append((number, row))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-pr-head", required=True)
    parser.add_argument("--deposit-id", type=int, required=True)
    args = parser.parse_args()
    require_release_clearance()
    identifier = args.deposit_id
    doi = "https://doi.org/10.5281/zenodo." + str(identifier)
    publication = json.loads((AUDIT / "ZENODO_PUBLISH.json").read_text())
    inspection = json.loads((AUDIT / "ZENODO_PUBLISHED_INSPECTION.json").read_text())
    public = json.loads((AUDIT / "ZENODO_PUBLIC_FILE_VERIFICATION.json").read_text())
    if (publication["id"] != identifier or inspection["id"] != identifier
            or publication["state"] != "published" or inspection["state"] != "published"
            or inspection["doi_url"] != doi or inspection["doi_resolution"]["http_status"] != 200
            or public["record"] != identifier or public["all_public_file_bytes_match_reviewed"] is not True
            or public["doi_resolution"]["status"] != 200):
        raise RuntimeError("Published public record/files/DOI verification incomplete")
    gate, acceptance = collect("before_ledger", args.expected_pr_head, identifier, allow_target_row=True)
    operation = uuid.uuid4().hex
    row = desired_row(identifier)
    before = read("ledger_before_append", operation)
    found = matches(before, identifier)
    intent = AUDIT / "LEDGER_APPEND_INTENT.json"
    appended = False
    if found:
        if len(found) != 1 or found[0][1] != row:
            raise RuntimeError("Existing result/DOI lead requires row reconciliation, no append attempted")
        row_number = found[0][0]
    else:
        if intent.exists():
            raise RuntimeError("Earlier append intent has no matching live row; resolve its outcome before retry")
        atomic_json(intent, {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), "pr": 397,
            "spreadsheet_id": SHEET, "range": RANGE, "row": row, "before_rows": len(before),
            "before_sha256": hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
            "gate_receipt": gate["receipt"], "operation": operation,
            "uncertain_outcome_rule": "Read current sheet for exact DOI/result before any retry; never blindly repeat append."
        })
        reply = gws("append", {"spreadsheetId": SHEET, "range": RANGE, "valueInputOption": "RAW",
                               "insertDataOption": "INSERT_ROWS", "includeValuesInResponse": True},
                    {"majorDimension": "ROWS", "values": [row]})
        atomic_json(AUDIT / "LEDGER_APPEND_RESPONSE.json", reply)
        if (reply["updates"]["updatedRows"] != 1 or reply["updates"]["updatedColumns"] != 4
                or reply["updates"]["updatedData"]["values"] != [row]):
            raise RuntimeError("Unexpected append response; read live sheet before further action")
        appended, row_number = True, None
    after = read("ledger_after_append", operation)
    found = matches(after, identifier)
    if len(found) != 1 or found[0][1] != row:
        raise RuntimeError("Read-back or uniqueness mismatch; reconcile without another append")
    if row_number is not None and row_number != found[0][0]:
        raise RuntimeError("Existing row moved during verification")
    row_number = found[0][0]
    if sum(len(r) > 2 and zenodo_dois(r[2]) == {"10.5281/zenodo." + str(identifier)} for r in after) != 1:
        raise RuntimeError("DOI is not unique in the primary column")
    receipt = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), "pr": 397, "status": "verified",
        "spreadsheet_id": SHEET, "sheet_gid": 1254632077, "row_number": row_number,
        "range": "'Math Puzzles'!A" + str(row_number) + ":D" + str(row_number),
        "values": row, "doi": publication["doi"], "new_row": appended,
        "appended_this_invocation": appended, "unique_target_and_DOI": True, "read_back_exact": True,
        "ledger_rows_before": len(before), "ledger_rows_after": len(after),
        "gate_receipt": str(Path(gate["receipt"]).relative_to(ROOT)), "operation": operation,
    }
    atomic_json(AUDIT / "LEDGER_PUBLICATION_VERIFICATION.json", receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
