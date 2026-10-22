"""Replay every shipped mathematical checker in an isolated temporary directory."""
import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not pass -O or -OO.")
    root = pathlib.Path(__file__).resolve().parent
    script = "audit_set_cover.py"
    result = "audit_set_cover_results.json"
    expected_bytes = (root / result).read_bytes()
    expected = json.loads(expected_bytes)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="initial-odd-ears-check-") as tmp:
        work = pathlib.Path(tmp)
        for name in (script, result):
            shutil.copyfile(root / name, work / name)
        completed = subprocess.run(
            [sys.executable, "-I", "-S", "-B", script],
            cwd=work,
            text=True,
            capture_output=True,
            timeout=600,
            check=False,
        )
        if completed.returncode:
            raise SystemExit("Checker failed:\n" + completed.stderr + completed.stdout)
        if completed.stderr:
            raise SystemExit("Unexpected checker stderr:\n" + completed.stderr)
        actual = json.loads(completed.stdout)
        if actual != expected:
            raise SystemExit("Checker stdout differs from the expected JSON result.")
        if (work / result).read_bytes() != expected_bytes:
            raise SystemExit("Generated result bytes differ from the shipped result.")
    report = {
        "status": "PASS",
        "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "execution": "Fresh temporary directory; Python -I -S -B; standard library only; no network or external inputs.",
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "checks": [{
            "script": script,
            "script_sha256": hashlib.sha256((root / script).read_bytes()).hexdigest(),
            "exit_code": completed.returncode,
            "stderr": completed.stderr,
            "stdout_json_matches": True,
            "generated_result_bytes_match": True,
            "result_file": result,
            "result_sha256": hashlib.sha256(expected_bytes).hexdigest(),
            "result": actual,
        }],
        "claim_limit": "Finite exact corroboration only; the mathematical proof and audit establish the unrestricted result.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
