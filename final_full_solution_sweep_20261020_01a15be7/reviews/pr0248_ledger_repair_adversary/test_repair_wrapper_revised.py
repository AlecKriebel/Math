#!/usr/bin/env python3
"""Synthetic revised-wrapper review; no network, credential or shared Git use."""
import ast
import contextlib
import copy
import datetime as dt
import hashlib
import io
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import types
import uuid

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parent.parent
SOURCE = PROGRAM / "repair_ledger_identity.py"
DOI = "10.5281/zenodo.23334001"
HEAD = "a" * 40
OLD = "Synthetic reviewed original notes."
NEW = OLD + " Original problem 30006003 / AMR-050-0020. Reviewed PR: https://github.com/AlecKriebel/Math/pull/254."
_DOI_HELPER = None


def doi_function():
    global _DOI_HELPER
    if _DOI_HELPER is None:
        # Import the actual helper and dependencies, with bytecode writes off.
        sys.dont_write_bytecode = True
        prior_path = sys.path[:]
        try:
            sys.path.insert(0, str(PROGRAM))
            spec = importlib.util.spec_from_file_location("review_publication_check", PROGRAM / "publication_check.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _DOI_HELPER = module.zenodo_dois
        finally:
            sys.path[:] = prior_path
    return _DOI_HELPER


def exercise(run_root, case):
    root = run_root / case
    (root / "raw" / "pr0254").mkdir(parents=True)
    (root / "eligibility").mkdir()
    (root / "rest_inventory.json").write_text(json.dumps({"pull_requests": [{"number": 254, "headRefOid": HEAD}]}))
    evidence = {"inventory_head_sha": HEAD, "added_queue_rows": [{"problem_id": "30006003", "problem_alias": "30006003 / AMR-050-0020"}]}
    if case == "stale_evidence_head_rejected":
        evidence["inventory_head_sha"] = "c" * 40
    (root / "eligibility" / "pr0254.json").write_text(json.dumps(evidence))
    files = [{"name": "paper.pdf", "size": 1, "checksum": "md5:example", "download_verified": True}]
    (root / "PR0254_PUBLICATION_LEADS.json").write_text(json.dumps({"records": [{"doi": DOI, "published": True, "doi_resolution": {"status": 200}, "files": files}]}))
    values = [[] for _ in range(79)]
    values[78] = ["https://www.unsolvedmath.com/problems/AMR-050-0020", "", "https://doi.org/" + DOI, OLD]
    baseline_row = copy.deepcopy(values[78])
    if case == "wrong_doi_rejected":
        values[78][2] = "https://doi.org/10.5281/zenodo.99999999"
    if case.startswith("duplicate_"):
        forms = {"duplicate_exact_rejected": "https://doi.org/" + DOI,
                 "duplicate_http_rejected": "http://doi.org/" + DOI,
                 "duplicate_dx_uppercase_rejected": "HTTPS://DX.DOI.ORG/10.5281/ZENODO.23334001",
                 "duplicate_record_url_rejected": "https://zenodo.org/records/23334001",
                 "duplicate_beyond_fixed_range_rejected": "https://doi.org/" + DOI}
        if case == "duplicate_beyond_fixed_range_rejected":
            values += [[] for _ in range(1170 - len(values))]
            values[1169] = ["source", "", forms[case], "Existing duplicate beyond former cutoff"]
        else:
            values.append(["source", "", forms[case], "Existing duplicate"])
    baseline_before = None
    prior_proposal_bytes = None
    if case in ("recover_prior_applied_value", "prior_concurrent_notes_preserved", "prior_same_old_snapshot_retention", "prior_identity_change_rejected", "prior_append_change_rejected"):
        prior = {"pr": 254, "doi": DOI, "row": 79, "old_notes": OLD, "new_notes": NEW,
                 "original_row": baseline_row, "at": "original-checkpoint", "reason": "Synthetic retained proposal"}
        if case == "prior_append_change_rejected":
            prior["new_notes"] += " Unreviewed different append."
        prior_proposal_bytes = json.dumps(prior)
        (root / "PR0254_LEDGER_REPAIR_PROPOSAL.json").write_text(prior_proposal_bytes)
        original_values = [[] for _ in range(78)] + [baseline_row]
        if case == "prior_same_old_snapshot_retention":
            original_values[0] = ["Earlier unrelated record"]
            values[0] = ["Later unrelated concurrent record"]
        baseline_before = json.dumps({"values": original_values})
        (root / "raw/pr0254/ledger_repair_before.json").write_text(baseline_before)
        values[78][3] = NEW if case == "recover_prior_applied_value" else OLD + " Concurrent edit." if case == "prior_concurrent_notes_preserved" else OLD
        if case == "prior_identity_change_rejected":
            values[78][1] = "Concurrent change to another identity field"
    if case == "orphan_before_snapshot_rejected":
        baseline_before = json.dumps({"values": [[] for _ in range(78)] + [baseline_row]})
        (root / "raw/pr0254/ledger_repair_before.json").write_text(baseline_before)
    reads, writes, artifacts = [], [], []

    def atomic_json(path, value):
        path = Path(path)
        assert path.resolve().is_relative_to(root.resolve()), path
        artifacts.append(str(path.relative_to(root)))
        if case == "postmutation_persistence_failures" and path.name in ("ledger_repair_response.json", "ledger_repair_after.json", "PR0254_LEDGER_REPAIR.json"):
            raise OSError("synthetic ENOSPC at " + path.name)
        path.write_text(json.dumps(value, indent=2) + "\n")

    def fake_gws(resource, params, body=None):
        if resource == ["values", "get"]:
            reads.append(params)
            formatted = [p for p in reads if p.get("valueRenderOption") == "FORMATTED_VALUE"]
            if case == "prewrite_identity_change_rejected" and params.get("valueRenderOption") == "FORMATTED_VALUE" and len(formatted) == 2:
                values[78][2] = "https://doi.org/10.5281/zenodo.99999999"
            rows = copy.deepcopy(values if params["range"] == "'Math Puzzles'!A:AQ" else values[:1169])
            if params.get("valueRenderOption") == "FORMULA" and case == "formula_rejected":
                rows[78][3] = '=CONCAT("Synthetic reviewed original notes.")'
            return {"values": rows, "range": params["range"]}
        assert resource == ["batchUpdate"] and len(body["requests"]) == 1
        fr = body["requests"][0]["findReplace"]
        assert fr["range"] == {"sheetId": 1254632077, "startRowIndex": 78, "endRowIndex": 79, "startColumnIndex": 3, "endColumnIndex": 4}
        assert fr["matchEntireCell"] and not fr["includeFormulas"]
        if not writes and case == "concurrent_notes_preserved":
            values[78][3] += " Concurrent independent addition."
        if not writes and case in ("identity_race_append_rolled_back", "identity_race_concurrent_notes_not_rolled_back"):
            values[78][0] = "https://www.unsolvedmath.com/problems/DIFFERENT-PROBLEM"
            values[78][2] = "https://doi.org/10.5281/zenodo.99999999"
        if writes and case == "identity_race_concurrent_notes_not_rolled_back":
            values[78][3] += " Concurrent independent addition."
        changed = int(values[78][3] == fr["find"])
        if changed:
            values[78][3] = fr["replacement"]
        writes.append({"applied": bool(changed), "find": fr["find"], "replacement": fr["replacement"], "target_doi_at_write": values[78][2]})
        return {"replies": [{"findReplace": {"occurrencesChanged": changed, "valuesChanged": changed, "rowsChanged": changed, "sheetsChanged": changed}}]}

    def get(url):
        if "api/records/" in url:
            return (json.dumps({"doi": DOI, "state": "done", "submitted": True,
                                "files": [{"key": "paper.pdf", "size": 1, "checksum": "md5:example"}]}).encode(), {})
        assert url == "https://doi.org/" + DOI
        return (b"", {})

    def fake_run(args, **kwargs):
        assert args == ["gh", "api", "--hostname", "github.com", "repos/AlecKriebel/Math/pulls/254"]
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps({"head": {"sha": HEAD}, "body": DOI, "state": "closed", "merged": True}), stderr="")

    tree = ast.parse(SOURCE.read_text(), filename=str(SOURCE))
    tree.body = [n for n in tree.body if not (isinstance(n, ast.ImportFrom) and n.module in ("publication_check", "checkpoint", "sweep_io"))]
    ns = {"__file__": str(root / "repair_ledger_identity.py"), "__name__": "wrapper_under_test",
          "ROOT": root, "SHEET": "synthetic", "get": get, "zenodo_dois": doi_function(),
          "live_main": lambda: "b" * 40, "atomic_json": atomic_json}
    exec(compile(tree, str(SOURCE), "exec"), ns)
    ns["subprocess"] = types.SimpleNamespace(run=fake_run)
    ns["gws"] = fake_gws
    prior_argv = sys.argv
    pid = "30006004" if case == "wrong_numeric_id_rejected" else "30006003"
    sys.argv = ["repair_ledger_identity.py", "254", "--problem-id", pid, "--alias", "AMR-050-0020", "--row", "79", "--doi", DOI, "--reason", "Synthetic fixture only", "--execute"]
    captured = io.StringIO()
    error = None
    try:
        with contextlib.redirect_stdout(captured):
            ns["main"]()
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        sys.argv = prior_argv
    receipt_path = root / "PR0254_LEDGER_REPAIR.json"
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    printed_receipt = json.loads(captured.getvalue()) if captured.getvalue().strip() else None
    return {"case": case, "error": error, "receipt_status": receipt.get("status") if receipt else None,
            "printed_receipt_status": printed_receipt.get("status") if printed_receipt else None,
            "persistence_errors": printed_receipt.get("persistence_errors") if printed_receipt else None,
            "recovered_prior_intended_value": receipt.get("recovered_prior_intended_value") if receipt else None,
            "retained_before_unchanged": (root / "raw/pr0254/ledger_repair_before.json").read_text() == baseline_before if baseline_before is not None else None,
            "retained_proposal_unchanged": (root / "PR0254_LEDGER_REPAIR_PROPOSAL.json").read_text() == prior_proposal_bytes if prior_proposal_bytes is not None else None,
            "execution_artifacts": [p for p in artifacts if Path(p).name.startswith("ledger_repair_execution_")],
            "writes": writes, "formatted_read_ranges": [r["range"] for r in reads if r.get("valueRenderOption") == "FORMATTED_VALUE"],
            "actual_same_doi_rows": [i + 1 for i, r in enumerate(values) if len(r) > 2 and DOI in doi_function()(r[2])],
            "final_target_row": values[78], "artifacts_confined": True}


def main():
    run_root = HERE / "wrapper_recheck_fixtures" / uuid.uuid4().hex
    cases = ["ordinary_existing_row_repair", "wrong_doi_rejected", "wrong_numeric_id_rejected", "stale_evidence_head_rejected",
             "duplicate_exact_rejected", "duplicate_http_rejected", "duplicate_dx_uppercase_rejected", "duplicate_record_url_rejected", "duplicate_beyond_fixed_range_rejected",
             "formula_rejected", "concurrent_notes_preserved", "prewrite_identity_change_rejected", "identity_race_append_rolled_back", "identity_race_concurrent_notes_not_rolled_back",
             "recover_prior_applied_value", "prior_concurrent_notes_preserved", "prior_same_old_snapshot_retention", "prior_identity_change_rejected", "prior_append_change_rejected", "orphan_before_snapshot_rejected", "postmutation_persistence_failures"]
    results = [exercise(run_root, case) for case in cases]
    by_case = {r["case"]: r for r in results}
    report = {"reviewed_at": dt.datetime.now(dt.timezone.utc).isoformat(), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "normalizer_sha256": hashlib.sha256((PROGRAM / "publication_check.py").read_bytes()).hexdigest(),
              "scope": "Synthetic revised-wrapper execution only. No network/credentials/live mutations/Git actions.", "results": results}
    (HERE / "WRAPPER_RECHECK.json").write_text(json.dumps(report, indent=2) + "\n")
    assert by_case["ordinary_existing_row_repair"]["receipt_status"] == "verified"
    for case in [c for c in cases if c.startswith("duplicate_")] + ["wrong_doi_rejected", "wrong_numeric_id_rejected", "stale_evidence_head_rejected", "formula_rejected", "prewrite_identity_change_rejected", "prior_concurrent_notes_preserved", "prior_identity_change_rejected", "prior_append_change_rejected", "orphan_before_snapshot_rejected"]:
        assert by_case[case]["error"] and not by_case[case]["writes"], by_case[case]
    assert by_case["concurrent_notes_preserved"]["writes"][0]["applied"] is False
    rolled = by_case["identity_race_append_rolled_back"]
    assert len(rolled["writes"]) == 2 and all(w["applied"] for w in rolled["writes"]) and rolled["final_target_row"][3] == OLD and rolled["error"], rolled
    concurrent = by_case["identity_race_concurrent_notes_not_rolled_back"]
    assert len(concurrent["writes"]) == 2 and concurrent["writes"][1]["applied"] is False and "Concurrent independent addition." in concurrent["final_target_row"][3], concurrent
    recovered = by_case["recover_prior_applied_value"]
    assert recovered["receipt_status"] == "verified" and recovered["recovered_prior_intended_value"] and not recovered["writes"] and recovered["retained_before_unchanged"] and recovered["retained_proposal_unchanged"], recovered
    pending = by_case["prior_same_old_snapshot_retention"]
    assert pending["receipt_status"] == "verified" and pending["retained_before_unchanged"] and pending["retained_proposal_unchanged"], pending
    for case in ("ordinary_existing_row_repair", "recover_prior_applied_value", "prior_same_old_snapshot_retention"):
        assert len(by_case[case]["execution_artifacts"]) == 1, by_case[case]
    for case in ("prior_identity_change_rejected", "prior_append_change_rejected"):
        assert by_case[case]["retained_before_unchanged"] and by_case[case]["retained_proposal_unchanged"], by_case[case]
    assert by_case["orphan_before_snapshot_rejected"]["retained_before_unchanged"]
    failed = by_case["postmutation_persistence_failures"]
    assert failed["error"].startswith("OSError:") and failed["printed_receipt_status"] == "verified" and len(failed["persistence_errors"]) == 2 and len(failed["writes"]) == 1, failed
    print(json.dumps({"reviewed_at": report["reviewed_at"], "source_sha256": report["source_sha256"], "cases": [{"case": r["case"], "error": r["error"], "receipt_status": r["receipt_status"], "printed_receipt_status": r["printed_receipt_status"], "write_count": len(r["writes"])} for r in results], "assertions_passed": True}, indent=2))


if __name__ == "__main__":
    main()
