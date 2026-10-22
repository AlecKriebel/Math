"""Check fail-closed validation and stdout-only replay in four execution modes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


BASE = Path(__file__).resolve().parent
SCRIPT = BASE / "elementary_check.py"
SEALED_OUTPUT = BASE / "ELEMENTARY_WITNESS_CHECK.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def snapshot():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in BASE.iterdir() if p.is_file()}


def run_tests():
    expected = SEALED_OUTPUT.read_bytes()
    expected_hash = hashlib.sha256(expected).hexdigest()
    before = snapshot()
    base_env = os.environ.copy()
    base_env.pop("PYTHONOPTIMIZE", None)
    rows = []
    for name, flags, inherited_value, optimization in [
        ("normal", [], None, 0),
        ("-O", ["-O"], None, 1),
        ("-OO", ["-OO"], None, 2),
        ("inherited_PYTHONOPTIMIZE_2", [], "2", 2),
    ]:
        env = base_env.copy()
        if inherited_value is not None:
            env["PYTHONOPTIMIZE"] = inherited_value
        runtime = subprocess.run(
            [sys.executable, *flags, "-c",
             "import os,sys,json; print(json.dumps({'optimize':sys.flags.optimize,"
             "'PYTHONOPTIMIZE':os.environ.get('PYTHONOPTIMIZE')}))"],
            env=env, capture_output=True, check=True,
        )
        state = json.loads(runtime.stdout)
        require(state["optimize"] == optimization, f"wrong actual optimization for {name}")
        require(state["PYTHONOPTIMIZE"] == inherited_value, f"wrong inherited mode for {name}")
        normal = subprocess.run([sys.executable, *flags, str(SCRIPT)], env=env, capture_output=True)
        require(normal.returncode == 0, f"valid replay failed in {name}")
        require(normal.stdout == expected, f"stdout differs from sealed result in {name}")
        require(not normal.stderr, f"unexpected stderr on valid replay in {name}")
        wrong = subprocess.run(
            [sys.executable, *flags, str(SCRIPT), "--expected-reduced-length", "105"],
            env=env, capture_output=True,
        )
        require(wrong.returncode != 0, f"wrong expectation was accepted in {name}")
        require(not wrong.stdout, f"failed replay leaked successful stdout in {name}")
        require(b"expected 105, got 104" in wrong.stderr, f"wrong failure reason in {name}")
        rows.append({
            "mode": name, "flags": flags, "actual_runtime": state,
            "valid_exit_code": normal.returncode,
            "valid_stdout_sha256": hashlib.sha256(normal.stdout).hexdigest(),
            "valid_stdout_equals_sealed_output": normal.stdout == expected,
            "wrong_expected_length": 105, "actual_length": 104,
            "wrong_expected_exit_code": wrong.returncode,
            "wrong_expected_stdout_empty": not wrong.stdout,
            "wrong_expected_correct_failure_reason": b"expected 105, got 104" in wrong.stderr,
        })
    after = snapshot()
    require(before == after, "replays changed a file in the family directory")
    require(SEALED_OUTPUT.read_bytes() == expected, "sealed elementary result was rewritten")
    return {
        "python_executable": sys.executable,
        "pass": True, "execution_modes": 4, "subprocess_cases": 8,
        "sealed_output_before_sha256": expected_hash,
        "sealed_output_after_sha256": hashlib.sha256(SEALED_OUTPUT.read_bytes()).hexdigest(),
        "all_existing_family_files_preserved_by_replays": before == after,
        "validation_uses_no_assert_statements": "assert " not in SCRIPT.read_text(),
        "rows": rows,
    }


if __name__ == "__main__":
    result = run_tests()
    print(json.dumps(result, indent=2))
