"""Launch and retain two exact-code root replays from an unrelated own cwd.

Arguments: SOURCE_DIRECTORY OUTPUT_DIRECTORY.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

source, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
observer = Path(__file__).with_name("observe_root.py").resolve()
cwd = output / "unrelated_cwd"
cwd.mkdir(exist_ok=True)
results = []
for name, flags in (("baseline", ["-I", "-S", "-B"]), ("optimized", ["-I", "-S", "-B", "-O"])):
    run_output = output / ("root_" + name)
    command = [sys.executable, *flags, str(observer), str(source), str(run_output)]
    run = subprocess.run(command, cwd=cwd, capture_output=True, timeout=1800)
    run_output.mkdir(exist_ok=True)
    (run_output / "ROOT_STDOUT.json").write_bytes(run.stdout)
    (run_output / "ROOT_STDERR.private").write_bytes(run.stderr)
    result = {"root_mode": name, "requested_flags": flags, "returncode": run.returncode, "stdout_actual_bytes": len(run.stdout), "stdout_actual_sha256": hashlib.sha256(run.stdout).hexdigest(), "stderr_actual_bytes": len(run.stderr), "stderr_actual_sha256": hashlib.sha256(run.stderr).hexdigest(), "cwd_role": "audit-owned-unrelated-directory", "execution_mechanism": "observer compiles exact authenticated root bytes with optimize=0, unchanged subprocess arguments"}
    if run.returncode == 0:
        parsed = json.loads(run.stdout)
        frozen = json.loads((source / "REPLAY_RESULTS.json").read_bytes())
        result["all_passed"] = parsed.get("all_passed")
        result["matches_frozen_replay_except_python_version"] = {k:v for k,v in parsed.items() if k != "python"} == {k:v for k,v in frozen.items() if k != "python"}
        result["current_python"] = parsed["python"]
        result["frozen_python"] = frozen["python"]
    results.append(result)
    (output / "ROOT_REPLAY_SUMMARY.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True), flush=True)
    if run.returncode:
        raise RuntimeError("Root replay failed; inspect retained stderr and trace")
