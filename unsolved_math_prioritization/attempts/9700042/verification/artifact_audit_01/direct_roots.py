"""Invoke the frozen verifier script directly, with no observer or code wrapper.

Arguments: SOURCE_DIRECTORY OUTPUT_DIRECTORY.
Two independent runs have distinct owned temporary roots and the same unrelated
owned cwd. Each original script is launched with -I -S -B and optional -O.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

source, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
cwd = output / "unrelated_cwd"
cwd.mkdir(exist_ok=True)
root = source / "verify_packet.py"
if hashlib.sha256(root.read_bytes()).hexdigest() != "13233e679fd24dffcf87407d934dcce80af7eb23132fe490227ce6edb62d85b9":
    raise RuntimeError("Direct root pin failed")

def one(mode):
    name, optional = mode
    destination = output / ("direct_root_" + name)
    destination.mkdir(exist_ok=True)
    scratch = destination / "scratch"
    scratch.mkdir()
    env = os.environ.copy()
    env["TMPDIR"] = str(scratch)
    flags = ["-I", "-S", "-B", *optional]
    run = subprocess.run([sys.executable, *flags, str(root)], cwd=cwd, env=env, capture_output=True, timeout=1800)
    (destination / "ROOT_STDOUT.json").write_bytes(run.stdout)
    (destination / "ROOT_STDERR.private").write_bytes(run.stderr)
    record = {"root_mode": name, "requested_flags": flags, "returncode": run.returncode, "stdout_actual_bytes": len(run.stdout), "stdout_actual_sha256": hashlib.sha256(run.stdout).hexdigest(), "stderr_actual_bytes": len(run.stderr), "stderr_actual_sha256": hashlib.sha256(run.stderr).hexdigest(), "invocation": "direct-original-script-no-observer", "cwd_role": "audit-owned-unrelated-directory", "temporary_root_role": "distinct-audit-owned-directory"}
    if run.returncode == 0:
        parsed, frozen = json.loads(run.stdout), json.loads((source / "REPLAY_RESULTS.json").read_bytes())
        record["all_passed"] = parsed["all_passed"]
        record["matches_frozen_replay_except_python_version"] = {k:v for k,v in parsed.items() if k != "python"} == {k:v for k,v in frozen.items() if k != "python"}
    (destination / "RECEIPT.json").write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    shutil.rmtree(scratch)
    print(json.dumps(record, sort_keys=True), flush=True)
    if run.returncode:
        raise RuntimeError("Direct root failed")
    return record

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(one, (("baseline", []), ("optimized", ["-O"]))))
(output / "DIRECT_ROOT_SUMMARY.json").write_text(json.dumps(results, indent=2, sort_keys=True)+"\n")
