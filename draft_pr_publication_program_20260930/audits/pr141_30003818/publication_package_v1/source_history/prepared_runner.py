"""Preparation-only portable diagnostics with bounded and reaped subprocesses."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
import os
import signal
import subprocess
import sys

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output-directory", required=True, help="A new directory outside the scaffold source tree")
parser.add_argument("--stdlib-python", default=sys.executable)
parser.add_argument("--library-python", default=sys.executable, help="Existing interpreter providing mpmath1.3.0 and SymPy1.14.0")
args = parser.parse_args()
output = Path(args.output_directory).resolve()
if output == root or root in output.parents:
    raise RuntimeError("output directory must be outside the scaffold source tree")
output.mkdir(parents=True, mode=0o700, exist_ok=False)
specifications = json.loads((root / "DIAGNOSTIC_SPECIFICATIONS.json").read_text())
source_manifest = json.loads((root / "PORTABLE_SOURCE_MANIFEST.json").read_text())
journal = []


def authenticate_sources():
    expected = {item["path"] for item in source_manifest["members"]}
    actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name != "PORTABLE_SOURCE_MANIFEST.json"}
    if actual != expected:
        raise RuntimeError("source-tree member set changed")
    for pin in source_manifest["members"]:
        p = root / pin["path"]
        data = p.read_bytes()
        if len(data) != pin["size"] or sha256(data).hexdigest() != pin["sha256"] or p.stat().st_mode & 0o777 != pin["mode"]:
            raise RuntimeError("source-tree full-body/mode pin changed")


def child(name, command, timeout=45):
    authenticate_sources()
    begin = datetime.now(timezone.utc).isoformat()
    process = subprocess.Popen(command, cwd=output, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        out, err = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        out, err = process.communicate()
    finish = datetime.now(timezone.utc).isoformat()
    try:
        os.killpg(process.pid, 0)
        group_absent = False
    except ProcessLookupError:
        group_absent = True
    (output / (name + ".stdout")).write_bytes(out)
    (output / (name + ".stderr")).write_bytes(err)
    journal.append({"name": name, "command": command, "pid": process.pid,
                    "started_utc": begin, "finished_utc": finish, "returncode": process.returncode,
                    "timeout_seconds": timeout, "timed_out": timed_out,
                    "reaped": process.poll() is not None, "process_group_absent": group_absent,
                    "stdout_size": len(out), "stdout_sha256": sha256(out).hexdigest(),
                    "stderr_size": len(err), "stderr_sha256": sha256(err).hexdigest()})
    (output / "CHILD_JOURNAL.json").write_text(json.dumps({"actual_runner_PID": os.getpid(), "children": journal}, indent=2) + "\n")
    if process.returncode or timed_out or not group_absent or err:
        raise RuntimeError("bounded diagnostic child failed: " + name)
    authenticate_sources()
    return json.loads(out)


authenticate_sources()
version_code = "import json,sys,mpmath,sympy; print(json.dumps({'python':sys.version,'mpmath':mpmath.__version__,'sympy':sympy.__version__}))"
versions = child("library_versions", [args.library_python, "-E", "-B", "-P", "-c", version_code])
if versions["mpmath"] != "1.3.0" or versions["sympy"] != "1.14.0":
    raise RuntimeError("existing library versions differ from the declared diagnostic environment")
standard_versions = child("stdlib_version", [args.stdlib_python, "-E", "-S", "-B", "-P", "-c", "import json,sys; print(json.dumps({'python':sys.version}))"])
ignore = set(specifications["known_nondeterministic_top_level_fields"])
mode_results = {}
guard_results = []
for spec in specifications["roles"]:
    role_results = {}
    for optimized in (False, True):
        mode = "optimized" if optimized else "normal"
        interpreter = args.library_python if spec["uses_library_environment"] else args.stdlib_python
        flags = ["-E", "-B", "-P"] if spec["uses_library_environment"] else ["-E", "-S", "-B", "-P"]
        command = [interpreter, *flags, *(["-O"] if optimized else []), str(root / spec["path"])]
        result = child(spec["role"] + "_" + mode, command, spec["timeout_seconds"])
        scientific = {key: value for key, value in result.items() if key not in ignore}
        if scientific != spec["scientific_baseline"]:
            (output / (spec["role"] + "_" + mode + "_SCIENTIFIC_MISMATCH.json")).write_text(json.dumps({"expected": spec["scientific_baseline"], "actual": scientific}, indent=2) + "\n")
            raise RuntimeError("scientific source replay mismatch: " + spec["role"] + "/" + mode)
        role_results[mode] = scientific
        guard_command = [args.stdlib_python, "-E", "-S", "-B", "-P", *(["-O"] if optimized else []), str(root / "guard_false_controls.py"), spec["role"]]
        guard = child(spec["role"] + "_false_guard_" + mode, guard_command)
        if not guard["false_rejected"] or not guard["positive_accepted"] or guard["optimized"] != optimized:
            raise RuntimeError("guard polarity/mode mismatch")
        guard_results.append({"role": spec["role"], "optimized": optimized, "false_rejected": True, "positive_accepted": True})
    if role_results["normal"] != role_results["optimized"]:
        raise RuntimeError("normal/optimized scientific mismatch")
    mode_results[spec["role"]] = {"scientific_baseline_matches_in_both_modes": True,
                                  "full_portable_source_sha256": sha256((root / spec["path"]).read_bytes()).hexdigest()}
    print(json.dumps({"role": spec["role"], "normal_and_optimized": "PASS", "false_guards_both_modes": "REJECTED"}), flush=True)

authenticate_sources()
result = {"schema": "pr141-portable-preparation-diagnostic-run/v1",
          "status": "PREPARATION_ONLY_PRIORITY_AND_PACKAGE_CLEARANCE_PENDING",
          "verdict": "PASS_PORTABLE_DIAGNOSTIC_REPRODUCTION",
          "actual_runner_PID": os.getpid(), "UTC": datetime.now(timezone.utc).isoformat(),
          "library_environment": versions, "stdlib_environment": standard_versions,
          "sources_full_body_mode_unchanged": True, "proof_sha256": specifications["proof_sha256"],
          "role_results": mode_results, "guard_controls": guard_results,
          "child_process_count": len(journal), "all_children_reaped": all(x["reaped"] for x in journal),
          "all_process_groups_absent": all(x["process_group_absent"] for x in journal),
          "all_child_returncodes_zero": all(x["returncode"] == 0 for x in journal),
          "priority_approval": False, "publication_package_approval": False,
          "scope": "Portable replay of distinct finite/algebraic/high-precision diagnostics; no proof by control counts, Brownian limit, Monte Carlo, certified quadrature, or uniform numerical-error certificate."}
(output / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"verdict": result["verdict"], "actual_runner_PID": os.getpid(), "children": len(journal), "output_directory": str(output)}))
