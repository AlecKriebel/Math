"""Read-only live gates with exact reconciliation of the two broad Aldous leads."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from publication_check import zenodo_dois
from sweep_io import atomic_json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def identity_projection(record):
    if not isinstance(record.get("metadata"), dict) or not isinstance(record.get("files"), list):
        raise RuntimeError("Unexpected known-record metadata/files schema")
    return {"metadata": record["metadata"], "files": record["files"]}


def require_release_clearance():
    clearance = json.loads((AUDIT / "ROOT_PUBLICATION_CLEARANCE.json").read_text())
    release = json.loads((AUDIT / "preprint/publication/RELEASE_FILES.json").read_text())
    if (clearance.get("publication_ready") is not True
            or clearance.get("unresolved_material_findings") != []
            or len(clearance.get("sequential_new_reviewers", [])) < 2
            or clearance["files"] != release["files"]):
        raise RuntimeError("Exact package has not completed the fresh review loop")
    names = [v["path"] for v in clearance["files"]]
    if len(set(names)) != 5 or set(names) != {
        "congestion-fragmentation.pdf", "congestion-fragmentation.tex",
        "congestion-fragmentation-verification.zip", "zenodo-deposit.json", "README.md"
    }:
        raise RuntimeError("Unexpected publication selection")
    for item in clearance["files"]:
        data = (AUDIT / "preprint/publication" / item["path"]).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise RuntimeError("Cleared publication file changed")
    return clearance


def collect(phase, expected_head, expected_deposit_id=None, allow_target_row=False):
    command = [sys.executable, str(AUDIT / "prepublication_check.py"), "--phase", phase,
               "--expected-pr-head", expected_head]
    if expected_deposit_id is not None:
        command += ["--expected-deposit-id", str(expected_deposit_id)]
    run = subprocess.run(command, capture_output=True, text=True, check=True)
    gate = json.loads(run.stdout)
    cleared = json.loads((AUDIT / "ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json").read_text())
    raw = ROOT / gate["raw_receipts"]
    account = json.loads((raw / "account_complete.json").read_text())
    records = {int(v["id"]): v for v in account["records"]}
    known = {v["record"]: v for v in cleared["all_broad_Aldous_leads_cleared_as_distinct"]}
    for identifier, prior in known.items():
        if (identifier not in records
                or digest(records[identifier]["metadata"]) != prior["metadata_sha256"]
                or digest(identity_projection(records[identifier])) != prior["metadata_and_files_sha256"]):
            raise RuntimeError("A previously cleared non-target record metadata/files changed; root identity recheck required")
    unexpected = {int(v["id"]) for v in gate["unexpected_account_matches"]}
    if not unexpected.issubset(known):
        raise RuntimeError("A new account publication/draft lead requires root identity review")
    prior_rows = {v["values_sha256"] for v in cleared["ledger_leads"]}
    target_rows = []
    for match in gate["ledger_matches"]:
        row = match["values"]
        row_sha = hashlib.sha256(json.dumps(row, ensure_ascii=False).encode()).hexdigest()
        if row_sha in prior_rows:
            continue
        doi = "10.5281/zenodo." + str(expected_deposit_id)
        if (allow_target_row and expected_deposit_id is not None and len(row) > 2
                and zenodo_dois(row[2]) == {doi}):
            target_rows.append(match)
            continue
        raise RuntimeError("New or changed ledger lead requires reconciliation before mutation")
    if gate["local_deposit_state_matches"]:
        if expected_deposit_id is None or any(
            int(v["deposit_id"]) != expected_deposit_id
            for v in gate["local_deposit_state_matches"]
        ):
            raise RuntimeError("Unreconciled local target deposit state")
    acceptance = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "phase": phase, "gate_receipt": Path(gate["receipt"]).relative_to(ROOT).as_posix(),
        "gate_sha256": hashlib.sha256(Path(gate["receipt"]).read_bytes()).hexdigest(),
        "known_non_target_records_metadata_and_complete_files_unchanged": sorted(known),
        "new_unreviewed_publication_or_ledger_leads": [],
        "expected_deposit_id": expected_deposit_id, "target_rows": target_rows,
        "read_only": True,
        "scope": "Saved exact-identity reconciliations plus fresh full account/GWS/head observations; no cross-service atomic lock or worldwide publication-absence certificate."
    }
    name = "LIVE_GATE_ACCEPTANCE_" + phase.upper() + "_" + gate["operation"] + ".json"
    atomic_json(AUDIT / name, acceptance)
    return gate, acceptance
