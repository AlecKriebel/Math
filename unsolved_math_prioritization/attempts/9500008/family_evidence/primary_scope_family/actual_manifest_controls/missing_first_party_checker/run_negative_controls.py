"""Exercise actual packet, source, code, and budget corruptions in private copies."""
from pathlib import Path
import datetime
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source_snapshot"
CONTROL = HERE / "actual_negative_controls"


def run(argv):
    p = subprocess.run(argv, cwd=HERE, capture_output=True, text=True)
    return {"argv": argv, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def main():
    assert not CONTROL.exists(), "Preserve controls rather than overwrite history."
    CONTROL.mkdir()
    results = []
    checker = str(HERE / "check_original_packet.py")
    baseline = run(["/usr/bin/python3", checker])
    assert baseline["returncode"] == 0
    results.append({"control": "actual_original_baseline", **baseline})
    for name in ["source_statement_narrowed", "source_actual_report_erased", "budget_six_attempts", "code_rotation_corrupted"]:
        target = CONTROL / name
        shutil.copytree(SOURCE, target)
        if name == "source_statement_narrowed":
            p = json.loads((target / "source_record.json").read_text())
            p["statement"] += " Assume that the stopped pairs are identically distributed."
            save_json(target / "source_record.json", p)
        elif name == "source_actual_report_erased":
            save_json(target / "prior_report.json", {})
        elif name == "budget_six_attempts":
            t = json.loads((target / "turns.json").read_text())
            t["count"] = 6
            t["attempts"] = [{"number": n, "route": "extra unsupported route", "outcome": "unresolved", "gap": "not proved"} for n in range(1, 7)]
            save_json(target / "turns.json", t)
            r = json.loads((target / "readiness.json").read_text())
            r["budget"]["used"] = 6
            save_json(target / "readiness.json", r)
        else:
            script = target / "review/independent_checks.py"
            before = script.read_text()
            assert "rot=a+d-e" in before
            script.write_text(before.replace("rot=a+d-e", "rot=a+d+e", 1))
            actual_run = run(["/usr/bin/python3", str(script)])
            assert actual_run["returncode"] != 0 and "rotation_difference" in actual_run["stderr"]
            results.append({"control": "actual_corrupt_code_execution", **actual_run})
        checked = run(["/usr/bin/python3", checker, str(target)])
        assert checked["returncode"] != 0, name
        results.append({"control": name, **checked})
    out = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "all_expected_outcomes_observed": True, "actual_controls": results,
           "scope": "Mutations of actual original packet and code. Rejections do not constitute mathematical proof."}
    save_json(HERE / "NEGATIVE_CONTROL_RESULTS.json", out)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
