#!/usr/bin/env python3
"""Independent active-guard challenges; malformed cases stay private."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "private_sources/extracted/verification"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    spec = importlib.util.spec_from_file_location("audited_driver", SOURCE / "run_verification.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    valid = {"all_passed": True, "checks": {"a": True, "b": True}, "count": 2}
    cases = []
    for label, field, value in [
        ("false_flag", "all_passed", False), ("integer_flag", "all_passed", 1),
        ("string_flag", "all_passed", "true"), ("null_flag", "all_passed", None),
        ("boolean_count", "count", True), ("float_count", "count", 2.0),
        ("string_count", "count", "2"), ("off_by_one_count", "count", 3),
        ("false_check", "checks", {"a": True, "b": False}),
        ("integer_check", "checks", {"a": True, "b": 1}),
        ("string_check", "checks", {"a": True, "b": "true"}),
        ("missing_name", "checks", {"a": True}),
        ("substituted_name", "checks", {"a": True, "c": True}),
        ("added_name", "checks", {"a": True, "b": True, "c": True}),
        ("list_map", "checks", [True, True]), ("null_map", "checks", None)]:
        value_object = copy.deepcopy(valid)
        value_object[field] = value
        cases.append((label, value_object))
    for key in ["all_passed", "checks", "count"]:
        value_object = copy.deepcopy(valid)
        del value_object[key]
        cases.append(("absent_" + key, value_object))
    driver.check_bool_result(valid, valid, 2, "count")
    rejections = []
    for label, value in cases:
        try:
            driver.check_bool_result(value, valid, 2, "count")
        except driver.VerificationError:
            rejections.append({"case": label, "intended_rejection": True})
        else:
            raise ValueError("Accepted malformed guard case: " + label)
    for label, value in [("duplicate_top_key", '{"all_passed":true,"all_passed":false}'), ("duplicate_nested_key", '{"checks":{"a":true,"a":false}}')]:
        try:
            driver.parse_json(value)
        except driver.VerificationError:
            rejections.append({"case": label, "intended_rejection": True})
        else:
            raise ValueError("Accepted duplicate-key input")
    original_root = driver.ROOT
    private = HERE / "private_cases"
    private.mkdir(exist_ok=True)
    path_rejections, process_rejections = [], []
    with tempfile.TemporaryDirectory(dir=private, prefix="guard_probe_") as temporary:
        root = Path(temporary)
        driver.ROOT = root
        (root / "valid.txt").write_text("benign control\n")
        for text in ["", "../valid.txt", "/valid.txt", "./valid.txt", "a//b", "private_cases/valid.txt", "private_sources/valid.txt", "__pycache__/valid.txt", ".secrets/valid.txt"]:
            try:
                driver.safe_path(text)
            except driver.VerificationError:
                path_rejections.append({"case": text, "intended_rejection": True})
            else:
                raise ValueError("Accepted unsafe path")
        (root / "link.txt").symlink_to(root / "valid.txt")
        try:
            driver.safe_path("link.txt")
        except driver.VerificationError:
            path_rejections.append({"case": "direct_symlink", "intended_rejection": True})
        else:
            raise ValueError("Accepted symlink")
        for label in ["payload_hash", "manifest_duplicate", "manifest_symlink"]:
            case = root / label
            shutil.copytree(SOURCE, case)
            if label == "payload_hash":
                target = case / "expected/curvature_flux.json"
                target.write_bytes(target.read_bytes() + b"\n")
            elif label == "manifest_duplicate":
                target = case / "VERIFICATION_MANIFEST.json"
                value = json.loads(target.read_bytes())
                value["files"][-1] = value["files"][0]
                target.write_text(json.dumps(value))
            else:
                target = case / "VERIFICATION_MANIFEST.json"
                value = json.loads(target.read_bytes())
                payload = case / "expected/curvature_flux.json"
                payload.unlink()
                payload.symlink_to(SOURCE / "expected/curvature_flux.json")
                target.write_text(json.dumps(value))
            for optimized in [False, True]:
                command = [sys.executable] + (["-O"] if optimized else []) + [str(case / "run_verification.py"), "--stdlib-only"]
                proc = subprocess.run(command, capture_output=True)
                require(proc.returncode == 2 and proc.stdout == b"" and proc.stderr.startswith(b"VerificationError: ") and b"Traceback" not in proc.stderr, "Wrong actual payload rejection")
                process_rejections.append({"case": label, "mode": "optimized" if optimized else "normal", "exit_code": 2, "intended_VerificationError": True, "diagnostic_sha256": hashlib.sha256(proc.stderr).hexdigest(), "accidental_crash": False})
    driver.ROOT = original_root
    result = {"status": "PASS", "optimization_of_probe": not __debug__, "explicit_boolean_and_duplicate_key_rejections": len(rejections), "guard_cases": rejections, "unsafe_path_rejections": len(path_rejections), "path_cases": path_rejections, "actual_manifest_payload_subprocess_rejections": len(process_rejections), "subprocess_cases": process_rejections, "malformed_fixtures_kept_private_and_removed": True, "candidate_inputs_unchanged": True}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
