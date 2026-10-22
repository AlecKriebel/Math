#!/usr/bin/env python3
"""Portable explicit-guard replay; outputs only sanitized deterministic results.

All executions and generated false claims use a temporary directory. Original
history and bundled payloads are read-only. No network or system paths appear
in the result. Finite checks support, but do not replace, the analytic proof.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
FORBIDDEN = {"private_sources", "private_cases", "mutation_fixtures", "__pycache__", ".venv", ".secrets", ".zenodo-state"}
PAYLOAD_PATHS = {
    ".gitignore", "README.md", "CURRENT_ATTRIBUTION_AND_SCOPE.md", "RESEARCH_LOG.md",
    "SOURCE_BINDINGS.json", "requirements.txt", "run_verification.py",
    "controls/check_geometry.py", "controls/check_curvature.py", "controls/areal_metric_controls.py", "controls/direct_connection_checks.py",
    "expected/source_geometry.json", "expected/curvature_flux.json", "expected/reproduction.json", "expected/whole_adversary.json",
    "reports/source_geometry.md", "reports/curvature_flux.md", "reports/reproduction.md",
    "provenance/original_source_receipt.json", "provenance/code_origins.json",
    "results/bundle_normal.json", "results/bundle_optimized.json",
    "frozen_history/PUBLICATION_NOTES.md",
    "frozen_history/audit/AUDIT_MANIFEST.json", "frozen_history/audit/AUDIT_REPORT.md",
    "frozen_history/audit/FROZEN_INPUTS.json", "frozen_history/audit/audit_controls.json",
    "frozen_history/audit/audit_controls.py", "frozen_history/audit/author_rerun.json",
    "frozen_history/release/PROOF.md", "frozen_history/release/README.md",
    "frozen_history/release/RESEARCH_LOG.md", "frozen_history/release/SOURCE_GATE.md",
    "frozen_history/release/checks/verification_results.json",
    "frozen_history/release/checks/verify_bianchi_counterexample.py",
}


class VerificationError(Exception):
    """A specific failed verification requirement, active even under -O."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON object key: " + key)
        result[key] = value
    return result


def parse_json(data):
    return json.loads(data, object_pairs_hook=no_duplicate_keys)


def load_json(path):
    return parse_json(path.read_bytes())


def safe_path(text):
    require(type(text) is str and text != "", "Invalid package path")
    part = PurePosixPath(text)
    require(not part.is_absolute() and ".." not in part.parts, "Unsafe package path")
    require(part.as_posix() == text and not set(part.parts) & FORBIDDEN, "Unpublishable package path")
    path = ROOT.joinpath(*part.parts)
    current = ROOT
    for component in part.parts:
        current = current / component
        require(not current.is_symlink(), "Symlink in package path")
    require(path.is_file() and path.resolve().is_relative_to(ROOT), "Missing or escaped payload")
    return path


def check_manifest():
    manifest = load_json(ROOT / "VERIFICATION_MANIFEST.json")
    require(manifest.get("manifest_self_hash_excluded") is True, "Manifest must exclude its own digest")
    entries = manifest.get("files")
    require(type(entries) is list, "Missing package file list")
    require(len(entries) == len(PAYLOAD_PATHS), "Wrong package payload count")
    paths = [item.get("path") for item in entries if type(item) is dict]
    require(len(paths) == len(entries) and len(set(paths)) == len(paths), "Malformed or duplicate package paths")
    require(set(paths) == PAYLOAD_PATHS, "Package payload inventory differs from positive list")
    for item in entries:
        data = safe_path(item["path"]).read_bytes()
        require(type(item.get("bytes")) is int and len(data) == item["bytes"], "Payload byte count differs")
        require(digest(data) == item.get("sha256"), "Payload SHA-256 differs")
    return len(entries)


def check_history():
    bindings = load_json(ROOT / "SOURCE_BINDINGS.json")
    receipt = load_json(ROOT / "provenance/original_source_receipt.json")
    require(bindings.get("head_sha") == receipt.get("head_sha") == "97b2ed225574ca61bd03cb8db021a533e04938dc", "Wrong frozen PR head")
    require(type(bindings.get("frozen_history_file_count")) is int and bindings["frozen_history_file_count"] == 13, "Wrong frozen count")
    entries = bindings.get("files")
    require(type(entries) is list and len(entries) == 13, "Missing frozen source bindings")
    originals = receipt.get("files")
    require(type(originals) is list and len(originals) == 13, "Missing original source receipt")
    by_original = {entry["path"]: entry for entry in originals}
    require(len(by_original) == 13 and len({entry.get("package_path") for entry in entries}) == 13, "Duplicate history paths")
    prefix = "unsolved_math_prioritization/attempts/30004807/"
    for entry in entries:
        original = entry.get("original_repository_path")
        require(type(original) is str and original.startswith(prefix) and original in by_original, "Unknown historical source path")
        require(entry.get("package_path") == "frozen_history/" + original[len(prefix):], "Historical path mapping differs")
        require(entry.get("bytes") == by_original[original]["bytes"] and entry.get("sha256") == by_original[original]["sha256"], "Historical source receipt differs")
        data = safe_path(entry["package_path"]).read_bytes()
        require(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "Historical payload changed")

    frozen = load_json(ROOT / "frozen_history/audit/FROZEN_INPUTS.json")
    audit = load_json(ROOT / "frozen_history/audit/AUDIT_MANIFEST.json")
    references = []
    require(type(frozen.get("files")) is list and len(frozen["files"]) == 6, "Wrong author reference count")
    for entry in frozen["files"]:
        references.append(("frozen_history/release/" + entry["path"], entry))
    require(type(audit.get("portable_files")) is dict and len(audit["portable_files"]) == 5, "Wrong audit reference count")
    for path, entry in audit["portable_files"].items():
        references.append(("frozen_history/audit/" + path, entry))
    for path, entry in references:
        require(path in {item["package_path"] for item in entries}, "Historical manifest references an unbound path")
        data = safe_path(path).read_bytes()
        require(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "Extant historical reference differs")
    unattested = bindings.get("unattested_reference")
    require(type(unattested) is dict and unattested.get("status") == "UNATTESTED", "Unattested digest mislabeled")
    require(unattested.get("sha256") == frozen.get("author_manifest_sha256") == "b64fa97f0194f55cf516cb473a032b1a0bda8ab7c8550cc64e32a098ab6c156f", "Wrong unattested standalone digest")
    return {"frozen_history_files": 13, "extant_manifest_payload_references": len(references), "standalone_author_manifest_digest": "UNATTESTED"}


def check_code_origins():
    origins = load_json(ROOT / "provenance/code_origins.json")
    entries = origins.get("copied_programs")
    require(type(entries) is list and len(entries) == 4, "Wrong independent code-origin count")
    expected = {"source_geometry": "controls/check_geometry.py", "curvature_flux": "controls/check_curvature.py",
                "reproduction": "controls/areal_metric_controls.py", "whole_adversary": "controls/direct_connection_checks.py"}
    require({entry.get("family"): entry.get("package_path") for entry in entries} == expected, "Independent code origins differ")
    for entry in entries:
        data = safe_path(entry["package_path"]).read_bytes()
        require(type(entry.get("bytes")) is int and len(data) == entry["bytes"] and digest(data) == entry.get("sha256"), "Independent copied code differs from origin binding")
        original = entry.get("original_repository_path")
        require(type(original) is str and not PurePosixPath(original).is_absolute() and ".." not in PurePosixPath(original).parts, "Code-origin repository path is not portable")
        if "report_package_path" in entry:
            require(digest(safe_path(entry["report_package_path"]).read_bytes()) == entry.get("report_sha256"), "Copied family report differs from origin binding")
    return len(entries)


def strict_count(value, expected, label):
    require(type(value) is int and value == expected, label + " exact integer count")


def check_bool_result(result, expected, count, count_field=None):
    require(type(result) is dict and type(expected) is dict, "Boolean result must be an object")
    require(result.get("all_passed") is True, "Missing or false all_passed")
    checks = result.get("checks")
    wanted = expected.get("checks")
    require(type(checks) is dict and type(wanted) is dict, "Missing Boolean check map")
    require(len(wanted) == count and len(checks) == count, "Wrong Boolean check count")
    require(set(checks) == set(wanted), "Missing or substituted check names")
    require(all(type(value) is bool and value is True for value in checks.values()), "False or non-Boolean check")
    require(all(type(value) is bool and value is True for value in wanted.values()), "Invalid expected Boolean checks")
    if count_field is not None:
        strict_count(result.get(count_field), count, count_field)


def guard_self_checks():
    valid = {"all_passed": True, "exact_check_count": 2, "checks": {"first": True, "second": True}}
    mutations = [
        {"checks": {"first": True, "second": True}, "exact_check_count": 2},
        {**valid, "all_passed": False}, {**valid, "all_passed": 1},
        {**valid, "checks": {"first": True, "second": False}},
        {**valid, "checks": {"first": True, "second": 1}},
        {**valid, "checks": {"first": True}}, {**valid, "checks": {"first": True, "substitute": True}},
        {**valid, "checks": []}, {**valid, "exact_check_count": "2"},
        {**valid, "exact_check_count": True}, {**valid, "exact_check_count": 3},
        {key: value for key, value in valid.items() if key != "exact_check_count"},
    ]
    check_bool_result(valid, valid, 2, "exact_check_count")
    for malformed in mutations:
        try:
            check_bool_result(malformed, valid, 2, "exact_check_count")
        except VerificationError:
            pass
        else:
            raise VerificationError("False or missing Boolean/count guard was accepted")
    try:
        parse_json('{"same": true, "same": false}')
    except VerificationError:
        pass
    else:
        raise VerificationError("Duplicate JSON key was accepted")
    return len(mutations) + 1


def execute(program, cwd, optimized, extra=()):
    command = [sys.executable] + (["-O"] if optimized else []) + [str(program)] + list(extra)
    return subprocess.run(command, cwd=cwd, capture_output=True, check=False)


def check_independent_standard_library(work):
    results = []
    specs = [
        ("source_geometry", "check_geometry.py", "verdict", "exact_check_count", 396),
        ("curvature_flux", "check_curvature.py", "status", "exact_equalities", 1557),
    ]
    for family, filename, status_field, count_field, count in specs:
        expected = load_json(ROOT / "expected" / (family + ".json"))
        outputs = []
        for optimized in (False, True):
            proc = execute(ROOT / "controls" / filename, work, optimized)
            require(proc.returncode == 0 and proc.stderr == b"", family + " subprocess failed")
            result = parse_json(proc.stdout)
            require(type(result) is dict and result.get(status_field) == "PASS", family + " missing PASS")
            strict_count(result.get(count_field), count, family)
            require(result == expected, family + " expected result differs")
            outputs.append(proc.stdout)
        require(outputs[0] == outputs[1], family + " normal/optimized bytes differ")
        results.append({"family": family, "modes": ["normal", "optimized"], "explicit_exact_checks_per_mode": count, "normal_optimized_output_identical": True, "matches_shipped_expected_object": True})
    expected = load_json(ROOT / "expected/whole_adversary.json")
    outputs = []
    for optimized in (False, True):
        case = work / ("whole_adversary_optimized" if optimized else "whole_adversary_normal")
        case.mkdir()
        program = case / "direct_connection_checks.py"
        shutil.copyfile(safe_path("controls/direct_connection_checks.py"), program)
        proc = execute(program, case, optimized)
        require(proc.returncode == 0 and proc.stderr == b"", "Whole adversary subprocess failed")
        data = (case / "DIRECT_CONNECTION_RESULTS.json").read_bytes()
        result = parse_json(data)
        require(type(result) is dict and result.get("verdict") == "PASS", "Whole adversary missing PASS")
        strict_count(result.get("check_count"), 2916, "Whole adversary")
        strict_count(result.get("metric_points"), 72, "Whole adversary metric points")
        require(result == expected, "Whole adversary expected result differs")
        require(parse_json(proc.stdout) == {key: value for key, value in expected.items() if key != "records"}, "Whole adversary stdout differs")
        outputs.append(data)
    require(outputs[0] == outputs[1], "Whole adversary normal/optimized bytes differ")
    results.append({"family": "whole_adversary", "modes": ["normal", "optimized"], "explicit_exact_checks_per_mode": 2916, "normal_optimized_output_identical": True, "matches_shipped_expected_object": True})
    return results


def check_dependencies():
    import sympy
    import mpmath
    require(sympy.__version__ == "1.14.0", "SymPy must be exactly 1.14.0")
    require(mpmath.__version__ == "1.3.0", "mpmath must be exactly 1.3.0")
    return {"sympy": sympy.__version__, "mpmath": mpmath.__version__}


def check_historical_execution(work):
    specs = [
        ("author", "release/checks/verify_bianchi_counterexample.py", "release/checks/verification_results.json", 17, None),
        ("historical_independent", "audit/audit_controls.py", "audit/audit_controls.json", 35, "assertions_passed"),
    ]
    outputs = []
    for label, program, expected_path, count, count_field in specs:
        stored = safe_path("frozen_history/" + expected_path).read_bytes()
        expected = parse_json(stored)
        for optimized in (False, True):
            case = work / (label + ("_optimized" if optimized else "_normal"))
            case.mkdir()
            copied = case / Path(program).name
            shutil.copyfile(safe_path("frozen_history/" + program), copied)
            proc = execute(copied, case, optimized)
            require(proc.returncode == 0 and proc.stderr == b"", label + " historical subprocess failed")
            generated = (case / Path(expected_path).name).read_bytes()
            result = parse_json(generated)
            check_bool_result(result, expected, count, count_field)
            require(result.get("sympy_version") == "1.14.0", label + " incorrect dependency metadata")
            require(generated == stored and proc.stdout == stored, label + " historical stdout/generated bytes differ")
            outputs.append({"program": label, "mode": "optimized" if optimized else "normal", "explicit_boolean_checks": count, "output_sha256": digest(generated), "matches_historical_bytes": True, "exit_code": 0, "external_explicit_guards_active": True})
    return outputs


def check_independent_symbolic(work):
    expected = load_json(ROOT / "expected/reproduction.json")
    program = safe_path("controls/areal_metric_controls.py")
    valid_outputs = []
    for optimized in (False, True):
        case = work / ("independent_symbolic_optimized" if optimized else "independent_symbolic_normal")
        case.mkdir()
        output = case / "valid.json"
        proc = execute(program, case, optimized, ("--output", str(output)))
        require(proc.returncode == 0 and proc.stderr == b"", "Independent symbolic subprocess failed")
        data = output.read_bytes()
        require(proc.stdout == data, "Independent symbolic stdout/generated bytes differ")
        result = parse_json(data)
        check_bool_result(result, expected, 67, "exact_check_count")
        require(result.get("sympy_version") == "1.14.0", "Independent symbolic dependency differs")
        require(type(result.get("python_version")) is str, "Missing symbolic runtime version")
        result.pop("python_version")
        require(result == expected, "Independent symbolic expected result differs")
        valid_outputs.append(data)
    require(valid_outputs[0] == valid_outputs[1], "Independent symbolic normal/optimized bytes differ")
    names = expected.get("invalid_claim_names")
    require(type(names) is list and len(names) == 16 and len(set(names)) == 16, "Wrong independent false-claim inventory")

    private = work / "private_cases"
    private.mkdir()

    def reject(item):
        name, optimized = item
        path = private / (name + ("_optimized.json" if optimized else "_normal.json"))
        path.write_text(json.dumps({"claim": name}) + "\n", encoding="utf-8")
        proc = execute(program, work, optimized, ("--claim-file", str(path)))
        diagnostic = ("InvalidClaim:EXPECTED_FALSE_CLAIM_REJECTED:" + name + "\n").encode()
        require(proc.returncode == 4, "False-claim rejection had incorrect exit code")
        require(proc.stdout == b"" and proc.stderr == diagnostic, "False-claim rejection had incorrect diagnostic")
        return {"claim": name, "mode": "optimized" if optimized else "normal", "exit_code": 4, "intended_InvalidClaim_rejection": True, "unexpected_crash": False}

    with ThreadPoolExecutor(max_workers=4) as pool:
        rejections = list(pool.map(reject, [(name, mode) for name in names for mode in (False, True)]))
    return {"explicit_exact_checks_per_mode": 67, "modes": ["normal", "optimized"], "normal_optimized_output_identical": True, "matches_shipped_expected_object_excluding_only_python_version": True, "distinct_false_claims": 16, "actual_intended_rejection_executions": len(rejections), "rejections": rejections, "fixtures_created_only_in_temporary_private_directory": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdlib-only", action="store_true", help="Run payload integrity, source binding, guard controls, and all three independent rational programs; omit symbolic tests explicitly.")
    args = parser.parse_args()
    payload_count = check_manifest()
    history_before = check_history()
    origin_count = check_code_origins()
    guards = guard_self_checks()
    with tempfile.TemporaryDirectory(prefix="pr464_verification_") as temporary:
        work = Path(temporary)
        standard_library = check_independent_standard_library(work)
        if args.stdlib_only:
            dependencies, historical, symbolic = None, [], None
        else:
            dependencies = check_dependencies()
            historical = check_historical_execution(work)
            symbolic = check_independent_symbolic(work)
    require(check_history() == history_before, "History changed during execution")
    require(check_manifest() == payload_count, "Payload integrity changed during execution")
    result = {"status": "PASS", "profile": "stdlib_only" if args.stdlib_only else "full",
              "payload_files_hash_verified": payload_count, "history": history_before,
              "independent_code_origin_copies_verified": origin_count,
              "explicit_guard_rejection_controls": guards, "standard_library_reviews": standard_library,
              "dependencies": dependencies, "historical_runs": historical,
              "independent_symbolic": symbolic, "history_and_payloads_unchanged": True,
              "temporary_inputs_removed": True, "network_used": False,
              "finite_checks_replace_analytic_proof": False,
              "limits": ["The standalone author-manifest digest remains unattested.",
                         "Checks support the scoped static-foliation and boundary-reaching-vector theorem; they do not establish arbitrary tilted-slice, collapsed-point, energy-condition, historical-priority, formal-verification, or human-peer-review claims."]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except VerificationError as error:
        print("VerificationError: " + str(error), file=sys.stderr)
        sys.exit(2)
