#!/usr/bin/env python3
"""Strict PR463 frozen-input reproduction and actual rejecting controls.

Run: python reproduce.py [--python PYTHON_WITH_SYMPY]
Output JSON goes to stdout; all temporary/mutated files stay in private_cases.
Validator entrypoint: python reproduce.py --validate-result author|audit FILE
Invalid evidence exits 4 with InvalidEvidence, including under optimized Python.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
SOURCE = AUDIT / "source_snapshot/unsolved_math_prioritization/attempts/6000016"


class InvalidEvidence(ValueError):
    pass


def ensure(condition, message):
    if type(condition) is not bool or not condition:
        raise InvalidEvidence(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise InvalidEvidence("duplicate JSON key")
        result[key] = value
    return result


def load(data):
    try:
        return json.loads(data, object_pairs_hook=pairs)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise InvalidEvidence("invalid JSON") from error


def author_names():
    names = ["developing_map_jacobian_determinant", "developing_map_inverse"]
    for i in range(2):
        for j in range(2):
            names.append(f"pullback_connection_{i}{j}")
            names.extend(f"torsion_{k}{i}{j}" for k in range(2))
    names.extend(f"curvature_{k}{ell}{i}{j}" for k in range(2) for ell in range(2) for i in range(2) for j in range(2))
    names += ["holonomy_composition", "holonomy_identity", "holonomy_inverse", "holonomy_linear_determinant", "developing_equivariance", "codazzi_obstruction_all_metrics", "second_codazzi_component", "central_metric_local_potential", "geodesic_x_equation", "geodesic_y_equation", "constant_metric_diagnostic"]
    return names


def audit_names():
    pinned = ["FROZEN_AUTHOR_MANIFEST.json", "PROOF.md", "README.md", "SOURCE_GATE.md", "RESEARCH_LOG.md", "check_exact.py", "exact_results.json"]
    manifest = ["README.md", "PROOF.md", "SOURCE_GATE.md", "RESEARCH_LOG.md", "check_exact.py", "exact_results.json"]
    names = ["frozen_sha256_"+name for name in pinned]+["manifest_exact_six_author_entries"]
    for name in manifest:
        names.extend(["manifest_size_"+name, "manifest_hash_"+name])
    names += ["author_rerun_byte_identical", "author_all_41_pass"]
    for i in range(2):
        for j in range(2):
            names += [f"matrix_torsion_{i}{j}", f"matrix_curvature_{i}{j}", f"connection_operator_product_{i}{j}"]
        names.append(f"parallel_volume_trace_{i}")
    names += ["global_inverse_left", "global_inverse_right", "developing_jacobian_det_one", "frame_change_connection_0", "frame_change_connection_1", "deck_action_conjugacy", "deck_group_law", "deck_group_inverse", "deck_linear_determinant", "central_developing_identity", "polynomial_parameter_second_derivative", "all_function_Codazzi_components", "obstruction_exterior_derivative_sign", "central_Euclidean_metric_Codazzi", "noncentral_Euclidean_metric_obstruction", "central_metric_Hessian", "noncompact_pullback_metric_Codazzi", "noncompact_pullback_metric_det_one", "noncompact_pullback_B_not_periodic", "indefinite_periodic_metric_Codazzi", "indefinite_metric_negative_determinant", "indefinite_metric_local_potential", "all_initial_data_geodesic_equation", "all_initial_positions", "all_initial_velocities"]
    return names


def validate(kind, data):
    obj = load(data)
    ensure(type(obj) is dict, "result is not an object")
    names = author_names() if kind == "author" else audit_names()
    count_key = "exact_identity_count" if kind == "author" else "audit_control_count"
    keys = {"status", count_key, "checks"}
    keys |= {"analytic_step", "limitations"} if kind == "author" else {"author_exact_identity_count", "analytic_scope", "source_scope"}
    ensure(set(obj) == keys, "incorrect result keys")
    ensure(type(obj["status"]) is str and obj["status"] == "PASS", "incorrect status")
    ensure(type(obj[count_key]) is int and obj[count_key] == len(names), "incorrect strict integer count")
    ensure(type(obj["checks"]) is list and all(type(name) is str for name in obj["checks"]), "check names are not strings")
    ensure(obj["checks"] == names and len(set(obj["checks"])) == len(names), "incorrect ordered check names")
    for key in keys-{count_key, "checks", "status", "author_exact_identity_count"}:
        ensure(type(obj[key]) is str and bool(obj[key]), "empty or nonstring scope")
    if kind == "audit":
        ensure(type(obj["author_exact_identity_count"]) is int and obj["author_exact_identity_count"] == 41, "incorrect strict author count")
    return obj


def canonical(path):
    ensure(type(path) is str, "nonstring manifest path")
    p = PurePosixPath(path)
    ensure(path == p.as_posix() and bool(p.parts) and not p.is_absolute() and all(part not in (".", "..", "") for part in p.parts), "unsafe manifest path")
    return path


def inspect_inputs():
    receipt_bytes = (AUDIT/"SOURCE_RECEIPT.json").read_bytes()
    receipt = load(receipt_bytes)
    ensure(type(receipt["pr"]) is int and receipt["pr"] == 463, "wrong PR")
    ensure(receipt["problem_id"] == "6000016" and receipt["head_sha"] == "982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649", "wrong frozen identity")
    ensure(receipt["scope_gate"] == "exact claimed_solved", "wrong eligibility gate")
    row = (AUDIT/"selected_queue_row.md").read_text().strip()
    ensure(row == receipt["selected_queue_row"], "queue row binding mismatch")
    fields = [item.strip() for item in row.split("|")[1:-1]]
    ensure(fields[7] == "claimed_solved" and fields[8] == "1/5" and fields[1] == "6000016 / AMR-059-0016", "wrong selected queue identity")
    expected = {}
    prefix = "unsolved_math_prioritization/attempts/6000016/"
    for entry in receipt["files"]:
        full = canonical(entry["path"])
        ensure(full.startswith(prefix), "file outside selected attempt")
        rel = full[len(prefix):]
        ensure(rel not in expected, "duplicate receipt path")
        ensure(type(entry["bytes"]) is int and entry["bytes"] >= 0, "incorrect size type")
        content = (SOURCE/rel).read_bytes()
        ensure(len(content) == entry["bytes"] and digest(content) == entry["sha256"], "frozen source mismatch: "+rel)
        expected[rel] = {"bytes": len(content), "sha256": digest(content)}
    actual = {file.relative_to(SOURCE).as_posix() for file in SOURCE.rglob("*") if file.is_file()}
    ensure(len(expected) == 14 and actual == set(expected), "incorrect complete frozen inventory")
    references = []
    for file, parent, count in (("FROZEN_AUTHOR_MANIFEST.json", SOURCE, 6), ("audit/AUDIT_MANIFEST.json", SOURCE/"audit", 4), ("PUBLICATION_MANIFEST.json", SOURCE, 13)):
        manifest = load((SOURCE/file).read_bytes())
        entries = manifest["files"]
        ensure(type(entries) is list and len(entries) == count, "incorrect manifest reference count")
        seen = set()
        for entry in entries:
            rel = canonical(entry["path"])
            ensure(rel not in seen and type(entry["bytes"]) is int, "duplicate manifest or noninteger size")
            seen.add(rel)
            content = (parent/rel).read_bytes()
            ensure(len(content) == entry["bytes"] and digest(content) == entry["sha256"], "historical manifest binding mismatch")
            references.append({"manifest": file, "path": (parent/rel).relative_to(SOURCE).as_posix(), "sha256": digest(content), "bytes": len(content), "verified": True})
    audit = load((SOURCE/"audit/AUDIT_MANIFEST.json").read_bytes())
    ensure(type(audit["author_files_unchanged"]) is bool and audit["author_files_unchanged"] is True, "incorrect historical integrity flag")
    for key, rel in (("frozen_author_manifest_sha256", "FROZEN_AUTHOR_MANIFEST.json"), ("frozen_proof_sha256", "PROOF.md")):
        ensure(audit[key] == expected[rel]["sha256"], "standalone audit binding mismatch")
        references.append({"manifest": "audit/AUDIT_MANIFEST.json", "binding_field": key, "path": rel, **expected[rel], "verified": True})
    no_assert = {}
    for rel in ("check_exact.py", "audit/check_audit.py"):
        count = sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((SOURCE/rel).read_text())))
        ensure(count == 0, "historical checker contains removable assertions")
        no_assert[rel] = count
    validate("author", (SOURCE/"exact_results.json").read_bytes())
    validate("author", (SOURCE/"audit/author_rerun.json").read_bytes())
    validate("audit", (SOURCE/"audit/audit_results.json").read_bytes())
    return {"source_receipt_sha256": digest(receipt_bytes), "head_sha": receipt["head_sha"], "frozen_files": expected,
            "verified_manifest_references": references, "missing_or_unattested_references": [], "assert_statement_counts": no_assert}


def run(python, args, cwd, optimized=False):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONOPTIMIZE"] = "1" if optimized else "0"
    return subprocess.run([python]+(["-O"] if optimized else [])+list(map(str, args)), cwd=cwd,
                          env=env, capture_output=True, timeout=120)


def invalid_variants(kind, original):
    result = []
    def add(name, edit):
        obj = json.loads(json.dumps(original))
        edit(obj)
        result.append((name, json.dumps(obj).encode()))
    key = "exact_identity_count" if kind == "author" else "audit_control_count"
    add("status_false", lambda o: o.update(status=False))
    add("status_lowercase", lambda o: o.update(status="pass"))
    add("count_boolean", lambda o: o.update({key: True}))
    add("count_float", lambda o: o.update({key: float(o[key])}))
    add("count_string", lambda o: o.update({key: str(o[key])}))
    add("count_decremented", lambda o: o.update({key: o[key]-1}))
    add("missing_check", lambda o: o["checks"].pop())
    add("duplicate_check", lambda o: o["checks"].__setitem__(-1, o["checks"][0]))
    add("renamed_check", lambda o: o["checks"].__setitem__(0, "fabricated_check"))
    add("Boolean_check", lambda o: o["checks"].__setitem__(0, True))
    add("reordered_checks", lambda o: o["checks"].reverse())
    add("extra_field", lambda o: o.update(accepted=True))
    add("missing_status", lambda o: o.pop("status"))
    add("empty_scope", lambda o: o.update({"analytic_step" if kind == "author" else "analytic_scope": ""}))
    result.append(("duplicate_JSON_status_key", json.dumps(original).encode()[:-1]+b', "status": "PASS"}'))
    result.append(("malformed_JSON", b'{"status": "PASS"'))
    if kind == "audit":
        add("author_count_boolean", lambda o: o.update(author_exact_identity_count=True))
    return result


def reproduce(python):
    initial = inspect_inputs()
    private = HERE/"private_cases"
    private.mkdir(exist_ok=True)
    replay = []
    rejection = []
    independent = []
    with tempfile.TemporaryDirectory(prefix="actual entrypoints ", dir=private) as temp:
        root = Path(temp)
        frozen = root/"frozen copy"
        shutil.copytree(SOURCE, frozen)
        cwd = root/"unrelated working directory"
        cwd.mkdir()
        for optimized in (False, True):
            for kind, script, args, recorded in (("author", frozen/"check_exact.py", [], frozen/"exact_results.json"),
                    ("audit", frozen/"audit/check_audit.py", ["--author-dir", frozen], frozen/"audit/audit_results.json")):
                completed = run(python, [script]+args, cwd, optimized)
                ensure(completed.returncode == 0 and completed.stderr == b"", "historical checker did not succeed cleanly")
                parsed = validate(kind, completed.stdout)
                ensure(completed.stdout == recorded.read_bytes(), "historical stdout is not byte-identical")
                replay.append({"kind": kind, "optimized": optimized, "exit_code": completed.returncode,
                    "stdout_sha256": digest(completed.stdout), "stdout_bytes": len(completed.stdout),
                    "exact_named_check_count": len(parsed["checks"]), "byte_identical_to_recorded": True})
            completed = run(python, [HERE/"independent_identities.py"], cwd, optimized)
            ensure(completed.returncode == 0 and completed.stderr == b"", "independent derivation failed")
            parsed = load(completed.stdout)
            ensure(parsed["status"] == "PASS" and type(parsed["independent_identity_count"]) is int,
                   "invalid independent derivation result")
            ensure(parsed["independent_identity_count"] == len(parsed["checks"]) and len(set(parsed["checks"])) == len(parsed["checks"]), "invalid independent check inventory")
            independent.append({"optimized": optimized, "exit_code": 0, "stdout_sha256": digest(completed.stdout),
                                "stdout_bytes": len(completed.stdout), "result": parsed})
        ensure(independent[0]["stdout_sha256"] == independent[1]["stdout_sha256"], "optimized independent output changed")

        # Deliberately corrupt actual mathematics in private code copies.
        author_edits = [
            ("connection_wrong_sign", "return t if", "return -t if"),
            ("connection_wrong_slot", "(k, i, j) == (1, 0, 0)", "(k, i, j) == (0, 1, 0)"),
            ("developing_map_missing_half", "y + t*x*x/2", "y + t*x*x"),
            ("holonomy_missing_quadratic_term", "b+t*a*a/2", "b"),
            ("holonomy_wrong_linear_term", "[t*a, 1,", "[-t*a, 1,"),
            ("geodesic_wrong_sign", "gy = y0+b*r-t*a*a*r*r/2", "gy = y0+b*r+t*a*a*r*r/2"),
            ("Codazzi_wrong_obstruction_sign", "s.diff(B, x)-s.diff(A, y)-t*C", "s.diff(B, x)-s.diff(A, y)+t*C"),
            ("central_potential_not_Euclidean", "(x*x+y*y)/2", "(x*x-y*y)/2"),
        ]
        audit_edits = [
            ("connection_wrong_sign", "[t, 0]]", "[-t, 0]]"),
            ("holonomy_missing_quadratic_term", "bb+t*aa*uu+t*aa*aa/2", "bb+t*aa*uu"),
            ("Codazzi_wrong_obstruction_sign", "B.diff(x)-A.diff(y)-t*C", "B.diff(x)-A.diff(y)+t*C"),
            ("geodesic_wrong_sign", "y0+vely*r-t*velx**2*r**2/2", "y0+vely*r+t*velx**2*r**2/2"),
        ]
        for kind, edits, source_rel in (("author", author_edits, "check_exact.py"), ("audit", audit_edits, "audit/check_audit.py")):
            source = (SOURCE/source_rel).read_text()
            for name, old, new in edits:
                ensure(old in source, "mutation anchor absent")
                mutated = root/f"invalid_{kind}_{name}.py"
                mutated.write_text(source.replace(old, new, 1))
                for optimized in (False, True):
                    args = [mutated]+(["--author-dir", frozen] if kind == "audit" else [])
                    completed = run(python, args, cwd, optimized)
                    ensure(completed.returncode != 0 and b"AssertionError" in completed.stderr,
                           "actual historical entrypoint accepted invalid mathematics")
                    rejection.append({"entrypoint": kind+" checker", "case": name, "optimized": optimized,
                                      "exit_code": completed.returncode, "expected_error_observed": "AssertionError"})

        # The actual original audit must reject changed source artifacts even
        # where a malicious payload retains plausible PASS/count information.
        for rel in ("PROOF.md", "check_exact.py", "exact_results.json", "FROZEN_AUTHOR_MANIFEST.json"):
            victim = frozen/rel
            original = victim.read_bytes()
            victim.write_bytes(original+b"\n")
            for optimized in (False, True):
                completed = run(python, [frozen/"audit/check_audit.py", "--author-dir", frozen], cwd, optimized)
                ensure(completed.returncode != 0 and b"AssertionError" in completed.stderr, "audit accepted altered frozen input")
                rejection.append({"entrypoint": "original audit checker", "case": "tampered_"+rel,
                                  "optimized": optimized, "exit_code": completed.returncode,
                                  "expected_error_observed": "AssertionError"})
            victim.write_bytes(original)

        for kind, rel in (("author", "exact_results.json"), ("audit", "audit/audit_results.json")):
            valid = validate(kind, (SOURCE/rel).read_bytes())
            # Legitimate validator controls through the same actual CLI.
            for optimized in (False, True):
                completed = run(python, [HERE/"reproduce.py", "--validate-result", kind, SOURCE/rel], cwd, optimized)
                ensure(completed.returncode == 0, "valid result rejected")
            for name, invalid in invalid_variants(kind, valid):
                payload = root/(kind+"_invalid.json")
                payload.write_bytes(invalid)
                for optimized in (False, True):
                    completed = run(python, [HERE/"reproduce.py", "--validate-result", kind, payload], cwd, optimized)
                    ensure(completed.returncode == 4 and b"InvalidEvidence" in completed.stderr,
                           "actual validator entrypoint accepted invalid evidence")
                    rejection.append({"entrypoint": "strict evidence validator", "result_kind": kind,
                        "case": name, "optimized": optimized, "exit_code": completed.returncode,
                        "expected_error_observed": "InvalidEvidence"})
        ensure({path.relative_to(frozen).as_posix(): digest(path.read_bytes()) for path in frozen.rglob("*") if path.is_file()}
               == {rel: entry["sha256"] for rel, entry in initial["frozen_files"].items()}, "private frozen copy changed")
    ensure(inspect_inputs() == initial, "original frozen source changed during audit")
    return {"status": "PASS", "pr": 463, "problem_id": "6000016", "integrity": initial,
            "historical_replays": replay, "independent_derivations": independent,
            "actual_rejection_controls": rejection, "rejection_count": len(rejection),
            "original_frozen_files_unchanged": True,
            "limitations": "No source interpretation, historical priority, paper readiness, or publication authorization is certified by this program. Analytical all-metric proof is in REPORT.md."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--validate-result", nargs=2, metavar=("KIND", "FILE"))
    args = parser.parse_args()
    if args.validate_result:
        kind, filename = args.validate_result
        ensure(kind in ("author", "audit"), "unknown result kind")
        validate(kind, Path(filename).read_bytes())
        print(json.dumps({"status": "VALID", "kind": kind}, sort_keys=True))
    else:
        print(json.dumps(reproduce(args.python), indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (InvalidEvidence, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print("InvalidEvidence: "+str(error), file=sys.stderr)
        sys.exit(4)
