#!/usr/bin/env python3
"""No credentials, network, production tool import, or mutation: driver controls.

The real six files are read. A fake subprocess stands in only for the independently
replayed closed-source checker. Remote and upload objects are in-memory fakes.
Controls evaluate guard behavior, not the honesty of authenticated review reports.
"""
import argparse, contextlib, copy, hashlib, io, json, os, runpy, shutil, sys, types
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[2]
SCRATCH = Path(__file__).resolve().parents[1] / "scratch" / "driver_controls"
MF = "50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de"
HEAD = "aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def execute(driver):
    source = driver.read_bytes()
    env = runpy.run_path(str(driver), run_name="__admin_guard_audit__")
    # Functions retain the global dictionary supplied by runpy.
    ns = env["gate"].__globals__
    runroot = SCRATCH / sha(source)
    runroot.mkdir(parents=True, exist_ok=True)
    ns["T"] = runroot
    ns["U"] = runroot
    inv = json.loads((T / "preprint/PACKAGE_INVENTORY.json").read_text())
    plan = json.loads((T / "READINESS_PLAN.json").read_text())
    assert inv["source_manifest_sha256"] == MF
    actual = [{"path": r["path"], "bytes": len((T/"preprint"/r["path"]).read_bytes()),
               "sha256": sha((T/"preprint"/r["path"]).read_bytes())} for r in inv["files"]]
    assert actual == inv["files"] and len(actual) == 6
    cases = []

    def gate_case(name, obj, expected=None):
        gatepath = ns["T"] / "FINAL_READINESS.json"
        if obj is None:
            gatepath.unlink(missing_ok=True)
        else:
            gatepath.write_text(json.dumps(obj))
        calls = []
        def fake_run(args, **kwargs):
            calls.append(args)
            assert args[:3] == [sys.executable, "-I", "-B"]
            assert "source/verify_source.py" in args[3]
            return types.SimpleNamespace(returncode=0, stderr="", stdout='{"result":"PASS"}')
        try:
            with patch.object(ns["subprocess"], "run", fake_run):
                env["gate"]()
            accepted, error = True, None
        except (RuntimeError, FileNotFoundError, KeyError, AssertionError, TypeError, ValueError) as e:
            accepted, error = False, type(e).__name__ + ": " + str(e)
        cases.append({"case": name, "accepted": accepted, "error": error,
                      "mocked_source_replay_invocations": len(calls)})
        if expected is not None:
            cases[-1].update(expected=expected, control_pass=accepted == expected)
        return accepted

    gate_case("absent_final_gate", None, False)
    gate_case("pending_plan_cannot_authorize", plan, False)
    forged = copy.deepcopy(plan)
    forged.update(result="PASS", actual_whole_preprint_rounds=2, final_current_round_clean=True)
    forged.pop("completed_whole_reviews", None)
    gate_case("unbound_completion_flags_only", forged, False)
    truthy = copy.deepcopy(forged)
    truthy["final_current_round_clean"] = "false"
    gate_case("truthy_string_clean_flag", truthy, False)
    floatcount = copy.deepcopy(forged)
    floatcount["actual_whole_preprint_rounds"] = 2.0
    gate_case("float_review_count", floatcount, False)
    boolcount = copy.deepcopy(forged)
    boolcount["actual_whole_preprint_rounds"] = True
    gate_case("boolean_review_count", boolcount, False)

    def bound_fixture(name):
        base = runroot/"fixtures"/name
        if base.exists():
            shutil.rmtree(base)
        base.mkdir(parents=True)
        ns["T"] = base
        result = copy.deepcopy(forged)
        result["completed_whole_reviews"] = []
        for i in (1, 2):
            packet = "whole_preprint_round%02d" % i
            folder = base/packet; folder.mkdir()
            entries = []
            for name, raw in (("CHECKS.py", b"# MOCK fixture; never executed\n"),
                              ("VERDICT.json", b'{"control":"fixture"}\n')):
                (folder/name).write_bytes(raw)
                entries.append({"path": name, "bytes": len(raw), "sha256": sha(raw)})
            mf = (json.dumps({"files": entries}, sort_keys=True)+"\n").encode()
            (folder/"MANIFEST.json").write_bytes(mf)
            checker_sha = sha((folder/"CHECKS.py").read_bytes())
            receipt = {"result": "PASS", "completed": True,
                       "problem": "30001478", "pr": 789, "original_scientific_head": HEAD,
                       "reviewer": "/root/pr789_whole_preprint_round%02d_mock_fixture" % i,
                       "manifest_sha256": sha(mf), "checker_sha256": checker_sha,
                       "source_manifest_sha256": MF, "publication_files": inv["files"],
                       "review_actionable_issues": 0}
            relative = "root-receipts/MOCK_WHOLE%02d.json" % i
            (base/"root-receipts").mkdir(exist_ok=True)
            raw = (json.dumps(receipt, sort_keys=True)+"\n").encode()
            (base/relative).write_bytes(raw)
            result["completed_whole_reviews"].append({
                "round": i, "freshly_initialized": True, "reviewer": receipt["reviewer"],
                "packet": packet, "manifest_sha256": sha(mf), "checker_name": "CHECKS.py",
                "checker_sha256": checker_sha, "root_replay_receipt": relative,
                "root_replay_sha256": sha(raw), "reviewed_source_manifest_sha256": MF,
                "reviewed_publication_files": copy.deepcopy(inv["files"]), "actionable_issues": 0})
        return result, base

    def bound_control(name, mutate, expected=False):
        obj, base = bound_fixture(name)
        mutate(obj, base)
        gate_case(name, obj, expected)

    bound_control("bound_two_fresh_current_clean_reviews", lambda g, p: None, True)
    bound_control("duplicate_reviewer", lambda g, p: g["completed_whole_reviews"][1].update(reviewer=g["completed_whole_reviews"][0]["reviewer"]))
    bound_control("reviewer_not_fresh", lambda g, p: g["completed_whole_reviews"][1].update(freshly_initialized=False))
    bound_control("missing_completed_round", lambda g, p: g["completed_whole_reviews"].pop())
    bound_control("manifest_bytes_changed", lambda g, p: (p/"whole_preprint_round02/MANIFEST.json").write_text("{}"))
    bound_control("checker_bytes_changed", lambda g, p: (p/"whole_preprint_round02/CHECKS.py").write_text("# changed\n"))
    bound_control("unexpected_review_packet_file", lambda g, p: (p/"whole_preprint_round02/EXTRA.txt").write_text("extra"))
    bound_control("unexpected_review_packet_empty_directory", lambda g, p: (p/"whole_preprint_round02/empty_directory").mkdir())
    bound_control("unexpected_review_packet_fifo", lambda g, p: os.mkfifo(p/"whole_preprint_round02/FIFO"))
    bound_control("missing_review_packet_file", lambda g, p: (p/"whole_preprint_round02/VERDICT.json").unlink())
    def symlink(g, p):
        f = p/"whole_preprint_round02/VERDICT.json"; f.unlink(); f.symlink_to(p/"whole_preprint_round01/VERDICT.json")
    bound_control("review_leaf_symlink", symlink)
    def hardlink(g, p):
        f = p/"whole_preprint_round02/VERDICT.json"; f.unlink(); os.link(p/"whole_preprint_round01/VERDICT.json", f)
    bound_control("review_leaf_hardlink", hardlink)
    def edit_receipt(g, p, **updates):
        row = g["completed_whole_reviews"][1]; f = p/row["root_replay_receipt"]
        receipt = json.loads(f.read_text()); receipt.update(updates)
        raw = (json.dumps(receipt, sort_keys=True)+"\n").encode(); f.write_bytes(raw)
        row["root_replay_sha256"] = sha(raw)
    bound_control("incomplete_root_replay_receipt", lambda g, p: edit_receipt(g, p, completed=False))
    bound_control("truthy_root_replay_completed_string", lambda g, p: edit_receipt(g, p, completed="false"))
    bound_control("changed_root_replay_target_problem", lambda g, p: edit_receipt(g, p, problem="30001479"))
    bound_control("changed_root_replay_target_PR", lambda g, p: edit_receipt(g, p, pr=788))
    bound_control("changed_root_replay_scientific_head", lambda g, p: edit_receipt(g, p, original_scientific_head="0"*40))
    bound_control("damaged_root_replay_receipt_digest", lambda g, p: (p/g["completed_whole_reviews"][1]["root_replay_receipt"]).write_text("{}"))
    bound_control("boolean_actionable_issue_count", lambda g, p: g["completed_whole_reviews"][1].update(actionable_issues=False))
    def final_issue(g, p):
        g["completed_whole_reviews"][1]["actionable_issues"] = 1
        edit_receipt(g, p, review_actionable_issues=1)
    bound_control("final_round_actionable_issue", final_issue)
    def stale_source(g, p):
        g["completed_whole_reviews"][1]["reviewed_source_manifest_sha256"] = "0"*64
        edit_receipt(g, p, source_manifest_sha256="0"*64)
    bound_control("final_round_stale_source_manifest", stale_source)
    def stale_six(g, p):
        files = copy.deepcopy(inv["files"]); files[0]["sha256"] = "0"*64
        g["completed_whole_reviews"][1]["reviewed_publication_files"] = files
        edit_receipt(g, p, publication_files=files)
    bound_control("final_round_stale_six_artifacts", stale_six)
    bound_control("changed_gate_scientific_head_without_original_binding",
                  lambda g, p: (g.pop("original_scientific_head", None), g.update(reviewed_head="0"*40)))
    bound_control("changed_gate_statement_identity", lambda g, p: g.update(statement_hash="0"*64))
    bound_control("changed_gate_full_review_identity", lambda g, p: g.update(review_hash="0"*64))
    bound_control("changed_explicit_original_scientific_head", lambda g, p: g.update(original_scientific_head="0"*40))
    bound_control("postpublication_read_only_integration_keeps_original_identity",
                  lambda g, p: g.update(original_scientific_head=HEAD, reviewed_head="1"*40), True)
    def historical_issue(g, p):
        row = g["completed_whole_reviews"][0]; row["actionable_issues"] = 2
        f = p/row["root_replay_receipt"]; receipt = json.loads(f.read_text())
        receipt["review_actionable_issues"] = 2
        raw = (json.dumps(receipt, sort_keys=True)+"\n").encode(); f.write_bytes(raw)
        row["root_replay_sha256"] = sha(raw)
    bound_control("historical_issue_round_preserved_final_clean", historical_issue, True)
    ns["T"] = runroot

    # If a real terminal gate exists, its files are never copied or altered. Run
    # the same gate with T restored so completed-review custody is exercised.
    terminal = T / "FINAL_READINESS.json"
    if terminal.exists():
        ns["T"] = T
        try:
            env["gate"]()
            cases.append({"case": "actual_terminal_gate_read_only", "accepted": True,
                          "expected": True, "control_pass": True})
        except Exception as e:
            cases.append({"case": "actual_terminal_gate_read_only", "accepted": False,
                          "expected": True, "control_pass": False,
                          "error": type(e).__name__ + ": " + str(e)})
        ns["T"] = runroot

    baseline = "| 827 | 30001478 / OWR-4335-003 | Prime Ideals and Coordinate-Ring Maps of $R(\\alpha,\\beta)$ | 0.0983 | 5.5 | 3 | 2010 | queued | 0/5 |  |  |  |"
    candidate = json.loads((T/"intake/ELIGIBILITY_GATE.json").read_text())["head_queue_row"]
    selected = {"id": "30001478", "statement_hash": plan["statement_hash"], "review_hash": plan["review_hash"]}
    state = {"pr_state": "open", "merged": False, "head": HEAD,
             "candidate": candidate, "main": baseline, "acceptance": None,
             "selected": selected}
    fake = types.ModuleType("graphql_scoped_commit")
    fake.get_pr = lambda n: {"state": state["pr_state"], "merged": state["merged"], "head": {"sha": state["head"]}}
    fake.head_oid = lambda: "mock-main"
    class Remote:
        def __init__(self, oid):
            self.is_main = oid == "mock-main"
        def entry(self, path):
            assert path == "unsolved_math_prioritization/attempts/30001478/acceptance.json"
            return state["acceptance"]
        def read(self, path):
            if path == "unsolved_math_prioritization/QUEUE.md":
                return state["main" if self.is_main else "candidate"] + "\n"
            assert path == "unsolved_math_prioritization/catalog.json"
            return json.dumps([state["selected"]])
    fake.Remote = Remote
    def eligibility(name, change, expected):
        old = copy.deepcopy(state)
        state.update(change)
        try:
            with patch.dict(sys.modules, {"graphql_scoped_commit": fake}):
                env["fresh_eligibility"](plan)
            accepted, error = True, None
        except (RuntimeError, AssertionError, KeyError, TypeError, ValueError) as e:
            accepted, error = False, type(e).__name__ + ": " + str(e)
        state.clear(); state.update(old)
        cases.append({"case": name, "accepted": accepted, "expected": expected,
                      "control_pass": accepted == expected, "error": error})
    eligibility("exact_original_parent_queue_baseline", {}, True)
    eligibility("exact_candidate_main_queue_row", {"main": candidate}, True)
    eligibility("main_weaker_different_queued_budget", {"main": baseline.replace("0/5", "1/5")}, False)
    eligibility("main_different_claimed_candidate_note", {"main": candidate.replace("characteristic scope", "changed scope")}, False)
    eligibility("PR_weaker_status", {"candidate": candidate.replace("claimed_solved", "queued")}, False)
    eligibility("changed_immutable_PR_head", {"head": "0"*40}, False)
    eligibility("already_merged", {"merged": True}, False)
    eligibility("closed_PR", {"pr_state": "closed"}, False)
    eligibility("existing_acceptance", {"acceptance": {"sha": "x"}}, False)
    eligibility("changed_statement_identity", {"selected": dict(selected, statement_hash="0"*64)}, False)
    eligibility("changed_full_review_identity", {"selected": dict(selected, review_hash="0"*64)}, False)

    # Execute main only with fake upload object and fake gate. Stale eligibility
    # raises before the fake publication method if the publish path is guarded.
    calls = []
    class UploadFake:
        def run(self, args):
            calls.append("fake_upload_" + args.command)
            return {"state": "published", "id": 123, "doi": "10.fake/control",
                    "metadata_normalizations": [], "doi_resolution": {"status": 200}}
    ns["load_tool"] = lambda: UploadFake()
    ns["gate"] = lambda: (forged, inv)
    def stale(g):
        calls.append("fresh_eligibility_called")
        raise RuntimeError("CONTROL: fresh eligible state changed")
    ns["fresh_eligibility"] = stale
    (runroot/"STAGE_RECEIPT.json").write_text(json.dumps({"state": "ready_to_publish", "metadata_normalizations": [], "id": 123}))
    (runroot/"PUBLICATION_INTENT.json").unlink(missing_ok=True)
    try:
        with patch.object(sys, "argv", [str(driver), "publish"]), contextlib.redirect_stdout(io.StringIO()):
            env["main"]()
        error = None
    except RuntimeError as e:
        error = str(e)
    cases.append({"case": "publish_rechecks_eligibility_before_any_fake_upload", "calls": list(calls),
                  "control_pass": calls == ["fresh_eligibility_called"], "error": error})
    drifted = copy.deepcopy(forged)
    drifted.update(original_scientific_head=HEAD, reviewed_head="1"*40)
    ns["gate"] = lambda: (drifted, inv)
    for command in ("stage", "publish"):
        calls.clear()
        try:
            with patch.object(sys, "argv", [str(driver), command]), contextlib.redirect_stdout(io.StringIO()):
                env["main"]()
            error = None
        except RuntimeError as e:
            error = str(e)
        cases.append({"case": command+"_rejects_coupled_gate_and_remote_head_drift_before_eligibility_or_upload",
                      "calls": list(calls), "control_pass": not calls and error is not None,
                      "error": error})
    vulnerabilities = [r["case"] for r in cases if
        (r["case"] in {"unbound_completion_flags_only", "truthy_string_clean_flag", "float_review_count"} and r["accepted"])
        or ("control_pass" in r and not r["control_pass"])]
    result = {"driver_sha256": sha(source), "source_manifest_sha256": MF,
              "real_six_files_exact": True, "FINAL_READINESS_present": terminal.exists(),
              "controls": cases, "required_guard_repairs_remaining": vulnerabilities,
              "credentials_loaded": False, "network_or_real_upload_invocations": 0,
              "result": "GUARD_REPAIRS_REQUIRED" if vulnerabilities else "MOCKED_GUARDS_PASS"}
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--driver", type=Path, default=T/"publication_driver.py")
    p.add_argument("--out", type=Path); a = p.parse_args()
    r = execute(a.driver)
    raw = json.dumps(r, indent=2) + "\n"
    if a.out:
        assert a.out.resolve().is_relative_to(Path(__file__).resolve().parents[1])
        a.out.write_text(raw)
    print(raw)
