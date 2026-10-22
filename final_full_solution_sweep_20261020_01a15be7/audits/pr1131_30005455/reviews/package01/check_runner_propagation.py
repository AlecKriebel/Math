"""Review-only faults against a disposable extracted runner; no candidate mutation."""
import copy
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parent
MIRROR = ROOT / "mirror/source"
os.environ["TMPDIR"] = str(ROOT / "private/tmp")
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
spec = importlib.util.spec_from_file_location("copied_runner", MIRROR / "verification/run_checks.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
expected = json.loads((MIRROR / "verification/EXPECTED.json").read_text())
real_run = runner.subprocess.run
old_argv = sys.argv


def demand(ok, why):
    if not ok:
        raise ValueError(why)


def change_nested_bool(value):
    value["negative_controls_rejected"]["critical_triangle_strict_stability"] = 1


faults = {
    "changed_math_value": lambda v: v.__setitem__("attached_triangle_at_4_over_3_positive_form", "0"),
    "missing_math_field": lambda v: v.pop("boundary_jacobian"),
    "extra_status_field": lambda v: v.__setitem__("status", "PASS"),
    "nested_bool_becomes_int": change_nested_bool,
    "string_becomes_number": lambda v: v.__setitem__("parallel_pair_positive_form", 250),
    "nested_list_reordered": lambda v: v["bare_triangle_spectra"]["5/4"].reverse(),
    "false_negative_control": lambda v: v["negative_controls_rejected"].__setitem__("loop_as_forest", False),
}
later_faults = {"whisker_disclaimer_changed": 2, "prior24_scope_claim_changed": 3, "second_mode_math_changed": 4}
results = []
for label in ["complete_positive", *faults, *later_faults, "duplicate_key", "nan", "nonzero_exit", "invalid_json"]:
    calls = []

    def fake_run(cmd, **kwargs):
        suite = ["forest", "whisker", "prior24"][len(calls) % 3]
        calls.append(suite)
        value = copy.deepcopy(expected[suite])
        if len(calls) == 1 and label in faults:
            faults[label](value)
        if len(calls) == later_faults.get(label):
            if label == "whisker_disclaimer_changed":
                value["written_proof_and_published_dependency_still_required"] = False
            elif label == "prior24_scope_claim_changed":
                value["literature_absence_certified"] = True
            elif label == "second_mode_math_changed":
                value["attached_triangle_at_4_over_3_positive_form"] = "0"
        stdout = json.dumps(value)
        code = 0
        if len(calls) == 1:
            if label == "duplicate_key":
                stdout = '{"x":1,"x":2}'
            elif label == "nan":
                stdout = '{"x":NaN}'
            elif label == "invalid_json":
                stdout = "not JSON"
            elif label == "nonzero_exit":
                code = 3
        return types.SimpleNamespace(returncode=code, stdout=stdout, stderr="injected fault" if code else "")

    runner.subprocess.run = fake_run
    sys.argv = ["run_checks.py"]
    stream = io.StringIO()
    caught = None
    try:
        with contextlib.redirect_stdout(stream):
            runner.main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        caught = str(exc)
    if label == "complete_positive":
        demand(caught is None and len(calls) == 9, "positive complete-output control failed")
        demand(json.loads(stream.getvalue())["status"] == "PASS", "positive status failed")
    else:
        demand(caught is not None and len(calls) == later_faults.get(label, 1), "runner accepted or failed to stop on fault: " + label)
    results.append({"fault": label, "rejected": caught is not None, "calls": len(calls), "reason": caught})
runner.subprocess.run = real_run
sys.argv = old_argv
print(json.dumps({"scope": "Result-propagation faults with mocked child outputs; genuine nine-run replay is separate", "optimization": sys.flags.optimize, "results": results}, indent=2))
