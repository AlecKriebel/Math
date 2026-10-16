"""Replay the actual frozen scripts in a private copy; preserve environment failures."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SRC = AUDIT / "source_snapshot"
RUN = HERE / "original_replay"


def invoke(argv, cwd):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    return {"argv": argv, "returncode": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr}


def main():
    assert not RUN.exists(), "Preserve existing replay; do not overwrite it."
    shutil.copytree(SRC, RUN)
    before = {str(p.relative_to(SRC)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in SRC.rglob("*") if p.is_file()}
    env = invoke(["python3", "-c",
                  "import sys; print(sys.executable); print(sys.version); import sympy; print(sympy.__version__)"], HERE)
    (HERE / "default_python_failure.json").write_text(json.dumps(env, indent=2) + "\n")
    system = invoke(["/usr/bin/python3", "-c",
                     "import sys,sympy; print(sys.executable); print(sys.version); print(sympy.__version__)"], HERE)
    assert system["returncode"] == 0, system
    runs = []
    for rel, output, expected in [
        ("verify.py", "verification.json", SRC / "verification.json"),
        ("review/submitted_verify.py", "review/verification.json", SRC / "review/submitted_results.json"),
        ("review/independent_checks.py", "review/independent_results.json", SRC / "review/independent_results.json"),
    ]:
        result = invoke(["/usr/bin/python3", str(RUN / rel)], RUN)
        assert result["returncode"] == 0, result
        result["relative_script"] = rel
        result["script_sha256"] = hashlib.sha256((RUN / rel).read_bytes()).hexdigest()
        result["generated_output"] = output
        result["output_bytes_equal_frozen"] = (RUN / output).read_bytes() == expected.read_bytes()
        assert result["output_bytes_equal_frozen"], rel
        runs.append(result)
    after = {str(p.relative_to(SRC)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in SRC.rglob("*") if p.is_file()}
    assert before == after
    out = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "default_python_probe": env, "working_python_probe": system,
           "source_snapshot_untouched": before == after, "runs": runs}
    (HERE / "ORIGINAL_DIAGNOSTIC_REPLAY.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"all_three_passed": True, "default_probe_failed": env["returncode"] != 0,
                      "outputs_byte_equal": True, "source_snapshot_untouched": True}, indent=2))


if __name__ == "__main__":
    main()
