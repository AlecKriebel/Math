#!/usr/bin/env python3
"""Root operator for an already reviewed PR411 publication phase; no retries.

Existing-draft recovery uses GETs only; create/upload/metadata writes are absent.
Loads the exact accepted V2 helper bytes, uses the repository kit's token loader
without printing credentials, retains original Python CLI output privately,
and records a fresh native exact claimed_solved gate before each phase.
"""
import argparse
import base64
import contextlib
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASE = HERE.parent
HELPER = HERE / "admin_helper_v2/publication_admin_v2.py"
ADOPTION_SHA = "ccc384738d0a1c81ee4eb42c389dac28acd024ec0d11f88dbf419243560a9fca"
NATIVE_SHA = "0743c2bed2a7081bd4417ee5e5f594d6856bbe35eedcbcb7be70fb446d69d6ee"
SPEC_SHA = "905ad377e80d68421b12ce9dc3bb6905814117134e9fa8e1f9423bd3f6189b3c"
HEAD = "ff7a7521458c1d2d9ae6f762eac04a3c3d9b9568"
BODY_SHA = "959f075e0bfff3fccc2411235000bbefd491177ba078878265182806ca0500a0"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase", choices=("recover", "publish", "tracker", "reconcile"))
    p.add_argument("--whole-accept-sha256", required=True)
    p.add_argument("--component-accept-sha256", required=True)
    p.add_argument("--helper-sha256", required=True)
    p.add_argument("--confirm-id", type=int)
    p.add_argument("--approved-native-sha256")
    p.add_argument("--run-name", required=True)
    a = p.parse_args()
    if not a.run_name.replace("_", "").isalnum():
        raise RuntimeError("unsafe run name")
    # One no-follow regular-file read: compiled bytes are the bytes hashed.
    fd = os.open(HELPER, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        raw = stream.read()
    if sha(raw) != a.helper_sha256:
        raise RuntimeError("accepted helper drift")
    spec = importlib.util.spec_from_file_location("root_pr411_publication", HELPER)
    m = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), m.__dict__)
    acceptance_path = CASE / "ROOT_WHOLE_REVIEW_2_ACCEPTANCE.json"
    acceptance_raw, _ = m.g.read_regular(acceptance_path)
    acceptance = json.loads(acceptance_raw)
    m.need(sha(acceptance_raw) == a.whole_accept_sha256 and acceptance["result"] == "PASS_WHOLE_PACKAGE_ZERO_FINDINGS"
           and acceptance["scientific_head"] == HEAD, "whole-package acceptance missing/different")
    component_raw, _ = m.g.read_regular(HERE / "ROOT_PUBLICATION_V2_COMPONENT_ACCEPTANCE.json")
    component = json.loads(component_raw)
    m.need(sha(component_raw) == a.component_accept_sha256
           and component["result"] == "PASS_PUBLICATION_V2_COMPONENT"
           and component["helper_sha256"] == a.helper_sha256
           and component["adoption_sha256"] == ADOPTION_SHA
           and component["whole_acceptance_sha256"] == a.whole_accept_sha256,
           "root-reviewed publication V2 component differs")
    m.need(a.confirm_id == 23331232 and a.approved_native_sha256 == NATIVE_SHA,
           "exact existing production draft/native pin required")
    m.need(sha(m.g.read_regular(m.ORIGINAL_STATE, private=True)[0]) == m.ORIGINAL_STATE_SHA,
           "original stage history changed")
    private = CASE / "private_sources/root_publication_runs" / a.run_name
    private.mkdir(parents=True, exist_ok=False)
    e = m.g.Engine(m.g.Native(), private / "scope_native")
    pr = e.call("GET", "pulls/411")
    ref = e.call("GET", "git/ref/heads/research/ricci-pinching-6800014")
    m.need(pr["number"] == 411 and pr["state"] == "open" and pr["draft"] is True and pr["merged"] is False
           and pr["head"]["sha"] == HEAD and ref["object"]["sha"] == HEAD
           and sha(pr["body"].encode()) == BODY_SHA, "current reviewed native PR drift")
    q = e.call("GET", "contents/unsolved_math_prioritization/QUEUE.md?ref=" + HEAD)
    queue = base64.b64decode(q["content"], validate=False)
    m.need(q["sha"] == m.g.QBLOB and sha(queue) == m.g.QHASH, "reviewed native QUEUE bytes changed")
    # Exact whole QUEUE pin binds the selected row already inspected by root.
    m.need(acceptance["queue_status"] == "claimed_solved" and acceptance["turns"] == "2/5", "scope acceptance mismatch")
    m.g.durable(private / "ROOT_PHASE_INTENT.json", {"phase": a.phase, "helper_sha256": a.helper_sha256,
        "spec_sha256": SPEC_SHA, "whole_acceptance_sha256": a.whole_accept_sha256,
        "head": HEAD, "utc": dt.datetime.now(dt.timezone.utc).isoformat(), "no_retry": True}, exclusive=True, private=True)
    argv = [str(HELPER), a.phase, "--approved-spec-sha256", SPEC_SHA,
            "--approved-adoption-sha256", ADOPTION_SHA]
    if a.phase == "recover": argv += ["--adoption", str(HERE / "admin_helper_v2/PROPOSED_RECOVERY_ADOPTION.json")]
    if a.confirm_id is not None: argv += ["--confirm-id", str(a.confirm_id)]
    if a.approved_native_sha256: argv += ["--approved-native-sha256", a.approved_native_sha256]
    captured_out, captured_err = io.StringIO(), io.StringIO()
    result, exit_code = None, 0
    try:
        os.environ["ZENODO_TOKEN"] = m.z.token_for("production")
        sys.argv = argv
        with contextlib.redirect_stdout(captured_out), contextlib.redirect_stderr(captured_err):
            m.main()
        result = json.loads(captured_out.getvalue())
    except Exception as exc:
        exit_code = 2
        m.g.durable(private / "ROOT_FAILURE_CLASS.json", {"kind": type(exc).__name__,
            "safe_guard_message": str(exc) if isinstance(exc, m.g.Stop) else None}, exclusive=True, private=True)
        captured_err.write("STOP: " + type(exc).__name__ + "; preserve custody, GET-only reconciliation, no write retry\n")
    finally:
        os.environ.pop("ZENODO_TOKEN", None)
        m.need(sha(m.g.read_regular(m.ORIGINAL_STATE, private=True)[0]) == m.ORIGINAL_STATE_SHA,
               "historical stage state changed during V2 operation")
    m.g.durable(private / "ROOT_CLI_NATIVE.json", {"argv": argv, "returncode": exit_code,
        "stdout_base64": base64.b64encode(captured_out.getvalue().encode()).decode(),
        "stderr_base64": base64.b64encode(captured_err.getvalue().encode()).decode(),
        "evidence_kind": "actual_root_in_process_python_cli_capture", "result": result}, exclusive=True, private=True)
    print(json.dumps({"returncode": exit_code, "phase": a.phase, "result": result,
                      "custody": str(private.relative_to(CASE))}, sort_keys=True))
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
