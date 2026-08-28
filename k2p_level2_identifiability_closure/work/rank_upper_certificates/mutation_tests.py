#!/usr/bin/env python3
"""Adversarial fail-closed mutations for the exact rank-upper package."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import pickle
import shutil
import subprocess
import sys
import tempfile
import time
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
WORK = Path(__file__).resolve().parent
VERIFIER = WORK / "verify_rank_upper_certificates.py"
AUTHORITATIVE_OUTPUT = WORK / "mutation_report.json"
HELPER_EXPECTED = {
    "omitted_descriptor_coverage": {
        "error_type": "AssertionError",
        "diagnostic": "coverage count mismatch",
    },
    "duplicated_descriptor_coverage": {
        "error_type": "AssertionError",
        "diagnostic": "descriptor index mismatch",
    },
    "altered_syzygy_coefficient": {
        "error_type": "AssertionError",
        "diagnostic": (
            "(1, 2, ((0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 2, 0, 0, 1), 1))"
        ),
    },
    "reassigned_representative_certificate": {
        "error_type": "AssertionError",
        "diagnostic": "representative digest mismatch",
    },
    "broken_port_transport": {
        "error_type": "AssertionError",
        "diagnostic": "broken port transport",
    },
    "false_rank_upper_claim": {
        "error_type": "AssertionError",
        "diagnostic": "claimed 7, exact certificate 8",
    },
}


def load_semantic_dependencies() -> None:
    """Import fallible mathematical dependencies only after output cleanup."""

    global port_transform_canonical_retic, verify_log_syzygy
    global default_exact_point, output_sparse_polynomials, upper_certificate
    global decode_field, descriptor_key, validate_coverage_shape
    global verify_exception_representative

    from descriptor_actions import port_transform_canonical_retic as port_transform
    from generate_exception_syzygies import verify_log_syzygy as verify_syzygy
    from k2p_atlas_core import (
        default_exact_point as default_point,
        output_sparse_polynomials as sparse_polynomials,
    )
    from syzygy_upper import upper_certificate as upper_certificate_function
    import verify_rank_upper_certificates as verifier_module

    verifier_module.load_semantic_dependencies()
    port_transform_canonical_retic = port_transform
    verify_log_syzygy = verify_syzygy
    default_exact_point = default_point
    output_sparse_polynomials = sparse_polynomials
    upper_certificate = upper_certificate_function
    decode_field = verifier_module.decode_field
    descriptor_key = verifier_module.descriptor_key
    validate_coverage_shape = verifier_module.validate_coverage_shape
    verify_exception_representative = verifier_module.verify_exception_representative


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def clear_stale_output(path: Path) -> None:
    path.unlink(missing_ok=True)
    require(not path.exists(), f"stale output remains:{path.name}")


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if lexical.is_symlink():
        raise SystemExit("K2P_RANK_MUTATION_OUTPUT_POLICY_FAIL:output symlink")
    source_inputs = {
        Path(__file__).resolve(),
        VERIFIER.resolve(),
        (WORK / "rank_upper_coverage.json").resolve(),
        (WORK / "exception_syzygies/orbit_000.json").resolve(),
    }
    if lexical.exists() and any(
        source.exists() and os.path.samefile(lexical, source)
        for source in source_inputs
    ):
        raise SystemExit("K2P_RANK_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source")
    if allow_authoritative_output:
        if normalized != authoritative:
            raise SystemExit("K2P_RANK_MUTATION_OUTPUT_POLICY_FAIL:wrong authoritative path")
        return normalized
    resolved = lexical.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return normalized
    raise SystemExit("K2P_RANK_MUTATION_OUTPUT_POLICY_FAIL:routine output must be external")


def must_reject(name, action, results):
    expected = HELPER_EXPECTED[name]
    try:
        action()
    except Exception as error:
        observed_type = type(error).__name__
        observed_diagnostic = str(error)
        require(
            observed_type == expected["error_type"],
            f"helper exception type mismatch:{name}:{observed_type}",
        )
        require(
            observed_diagnostic == expected["diagnostic"],
            f"helper diagnostic mismatch:{name}:{observed_diagnostic}",
        )
        results.append({
            "mutation": name,
            "test_type": "focused_exact_helper_attack",
            "status": "rejected",
            "error": observed_diagnostic,
            "expected_error_type": expected["error_type"],
            "observed_error_type": observed_type,
            "expected_diagnostic": expected["diagnostic"],
            "observed_diagnostic": observed_diagnostic,
            "diagnostic_matched": True,
            "production_verifier_invoked": False,
            "rejected": True,
        })
        return
    raise AssertionError(f"mutation survived: {name}")


def reseal_manifest(root: Path) -> dict[str, Any]:
    paths = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in {
            "MANIFEST.sha256",
            "manifest.json",
            "mutation_report.json",
        }
        and "__pycache__" not in path.parts
    )
    rows = [(path.relative_to(root).as_posix(), sha_file(path)) for path in paths]
    lines = b"".join(f"{digest}  {relative}\n".encode() for relative, digest in rows)
    (root / "MANIFEST.sha256").write_bytes(lines)
    manifest = {
        "schema": "k2p-rank-upper-manifest-v1",
        "file_count": len(rows),
        "aggregate_sha256": hashlib.sha256(lines).hexdigest(),
        "files": [
            {"path": relative, "sha256": digest}
            for relative, digest in rows
        ],
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return manifest


def validate_authoritative_manifest(root: Path) -> dict[str, Any]:
    """Verify both stored manifest encodings against every current input."""

    paths = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in {
            "MANIFEST.sha256",
            "manifest.json",
            "mutation_report.json",
        }
        and "__pycache__" not in path.parts
    )
    rows = [(path.relative_to(root).as_posix(), sha_file(path)) for path in paths]
    expected_lines = b"".join(
        f"{digest}  {relative}\n".encode() for relative, digest in rows
    )
    manifest_path = root / "MANIFEST.sha256"
    json_path = root / "manifest.json"
    require(manifest_path.read_bytes() == expected_lines, "authoritative SHA manifest drift")
    manifest = json.loads(json_path.read_text())
    expected_files = [
        {"path": relative, "sha256": digest} for relative, digest in rows
    ]
    aggregate = hashlib.sha256(expected_lines).hexdigest()
    require(
        manifest
        == {
            "schema": "k2p-rank-upper-manifest-v1",
            "file_count": len(rows),
            "aggregate_sha256": aggregate,
            "files": expected_files,
        },
        "authoritative JSON manifest drift",
    )
    require(len(rows) == 94, f"authoritative manifest census:{len(rows)}")
    return {
        "file_count": len(rows),
        "aggregate_sha256": aggregate,
        "sha256_manifest_sha256": sha_file(manifest_path),
        "json_manifest_sha256": sha_file(json_path),
    }


def copy_complete_package(destination: Path) -> dict[str, Any]:
    shutil.copytree(
        WORK,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "mutation_report.json"),
    )
    return reseal_manifest(destination)


def invoke_production_verifier(
    certificate_dir: Path, output: Path, timeout: float
) -> tuple[subprocess.CompletedProcess[str], float]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = os.pathsep.join((str(ATLAS), str(WORK)))
    started = time.monotonic()
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(VERIFIER),
            "--atlas",
            str(ATLAS),
            "--certificate-dir",
            str(certificate_dir),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    return completed, time.monotonic() - started


def diagnostic_line(output: str, expected: str) -> str | None:
    matches = [line.strip() for line in output.splitlines() if line.strip() == expected]
    require(len(matches) <= 1, f"duplicate diagnostic:{expected}")
    return matches[0] if matches else None


def qualifies_failure(
    completed: subprocess.CompletedProcess[str], expected: str, success_artifact: Path
) -> tuple[bool, str | None]:
    combined = completed.stdout or ""
    observed = diagnostic_line(combined, expected)
    forbidden = (
        "Traceback (most recent call last):",
        "ModuleNotFoundError",
        "ImportError:",
        "TimeoutExpired",
    )
    qualified = (
        completed.returncode == 1
        and observed == expected
        and not success_artifact.exists()
        and not any(marker in combined for marker in forbidden)
        and "K2P_RANK_UPPER_REPLAY_PASS " not in combined
    )
    return qualified, observed


def source_fingerprints() -> dict[str, str]:
    paths = [
        Path(__file__).resolve(),
        VERIFIER.resolve(),
        WORK / "rank_upper_coverage.json",
        WORK / "exception_syzygies/orbit_000.json",
        WORK / "exception_orbit_representatives.pkl",
        WORK / "exception_orbits.json",
        WORK / "build_manifest.py",
        WORK / "MANIFEST.sha256",
        WORK / "manifest.json",
    ]
    return {path.relative_to(ROOT).as_posix(): sha_file(path) for path in paths}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "invalid timeout")
    output = validate_output_path(args.output, args.allow_authoritative_output)
    clear_stale_output(output)
    if not __debug__:
        raise SystemExit("K2P_RANK_MUTATION_OPTIMIZED_MODE_FORBIDDEN")
    load_semantic_dependencies()
    authoritative_manifest = validate_authoritative_manifest(WORK)
    before = source_fingerprints()

    with (ATLAS / "descriptors_4.pkl").open("rb") as handle:
        _, _, _, source_descriptors, descriptor_map = pickle.load(handle)
    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    unique = sorted(set(source_descriptors) | set(descriptor_map.values()), key=descriptor_key)
    coverage = json.loads((WORK / "rank_upper_coverage.json").read_text())
    orbit_ledger = json.loads((WORK / "exception_orbits.json").read_text())
    results = []

    omitted = copy.deepcopy(coverage)
    omitted["descriptors"].pop()
    must_reject(
        "omitted_descriptor_coverage",
        lambda: validate_coverage_shape(omitted, unique),
        results,
    )

    duplicated = copy.deepcopy(coverage)
    duplicated["descriptors"][1] = copy.deepcopy(duplicated["descriptors"][0])
    must_reject(
        "duplicated_descriptor_coverage",
        lambda: validate_coverage_shape(duplicated, unique),
        results,
    )

    cert0_path = WORK / "exception_syzygies/orbit_000.json"
    cert0 = json.loads(cert0_path.read_text())
    altered = copy.deepcopy(cert0)
    altered["fields"][0]["log_multipliers"][0][0]["coefficient"] += 1

    def replay_altered_syzygy():
        support, vector = decode_field(altered["fields"][0])
        verify_log_syzygy(representatives[0], support, vector)

    must_reject("altered_syzygy_coefficient", replay_altered_syzygy, results)

    must_reject(
        "reassigned_representative_certificate",
        lambda: verify_exception_representative(
            representatives[1], orbit_ledger["orbits"][1], cert0
        ),
        results,
    )

    exception_row = next(
        row
        for row in coverage["descriptors"]
        if row["upper_mechanism"]
        == "base_fields_plus_primitive_log_field_port_transport"
    )
    member = unique[exception_row["descriptor_index"]]
    orbit_index = exception_row["representative_orbit_index"]
    good = tuple(exception_row["representative_to_member_port_permutation"])
    bad = next(
        permutation
        for permutation in permutations(range(4))
        if permutation != good
        and port_transform_canonical_retic(representatives[orbit_index], permutation) != member
    )
    must_reject(
        "broken_port_transport",
        lambda: (
            port_transform_canonical_retic(representatives[orbit_index], bad) == member
        )
        or (_ for _ in ()).throw(AssertionError("broken port transport")),
        results,
    )

    base_row = next(
        row
        for row in coverage["descriptors"]
        if row["upper_mechanism"] == "multilinear_lambda_polynomial_vector_fields"
    )
    base_desc = unique[base_row["descriptor_index"]]
    exact_upper = upper_certificate(
        base_desc, output_sparse_polynomials, default_exact_point
    )["certified_rank_upper"]
    false_claim = exact_upper - 1
    must_reject(
        "false_rank_upper_claim",
        lambda: (false_claim == exact_upper)
        or (_ for _ in ()).throw(
            AssertionError(f"claimed {false_claim}, exact certificate {exact_upper}")
        ),
        results,
    )

    wrong_helper_diagnostic_rejected = False
    try:
        must_reject(
            "omitted_descriptor_coverage",
            lambda: (_ for _ in ()).throw(AssertionError("unrelated helper crash")),
            [],
        )
    except AssertionError as error:
        wrong_helper_diagnostic_rejected = str(error).startswith(
            "helper diagnostic mismatch:omitted_descriptor_coverage:"
        )
    require(
        wrong_helper_diagnostic_rejected,
        "wrong helper diagnostic qualified",
    )
    wrong_helper_type_rejected = False
    try:
        must_reject(
            "omitted_descriptor_coverage",
            lambda: (_ for _ in ()).throw(ValueError("coverage count mismatch")),
            [],
        )
    except AssertionError as error:
        wrong_helper_type_rejected = str(error).startswith(
            "helper exception type mismatch:omitted_descriptor_coverage:"
        )
    require(wrong_helper_type_rejected, "wrong helper exception type qualified")

    with tempfile.TemporaryDirectory(prefix="k2p-rank-upper-mutations-") as temporary:
        scratch = Path(temporary)
        clean_root = scratch / "clean-package"
        clean_manifest = copy_complete_package(clean_root)
        require(
            clean_manifest["file_count"] == authoritative_manifest["file_count"]
            and clean_manifest["aggregate_sha256"]
            == authoritative_manifest["aggregate_sha256"],
            "disposable clean copy differs from authoritative package",
        )
        clean_output = scratch / "clean-replay.json"
        clean_result, clean_runtime = invoke_production_verifier(
            WORK, clean_output, args.timeout_seconds
        )
        clean_pass_lines = [
            line.strip()
            for line in clean_result.stdout.splitlines()
            if line.startswith("K2P_RANK_UPPER_REPLAY_PASS ")
        ]
        require(
            clean_result.returncode == 0
            and len(clean_pass_lines) == 1
            and clean_output.is_file()
            and json.loads(clean_output.read_text())
            == {
                "base_ansatz_descriptor_count": 3515,
                "base_recomputed": True,
                "descriptor_count": 4379,
                "exceptional_descriptor_count": 864,
                "exceptional_representative_count": 75,
                "schema": "k2p-four-port-exact-rank-upper-replay-v1",
                "status": "pass",
                "zero_unresolved": True,
            }
            and clean_output.read_bytes()
            == (WORK / "rank_upper_replay.json").read_bytes()
            and "Traceback (most recent call last):" not in clean_result.stdout,
            "clean production verifier baseline",
        )
        clean_payload = json.loads(clean_output.read_text())

        mutant_root = scratch / "sampled-substitution-package"
        shutil.copytree(clean_root, mutant_root)
        mutant_certificate_path = mutant_root / "exception_syzygies/orbit_000.json"
        mutant_certificate = json.loads(mutant_certificate_path.read_text())
        original_certificate_sha256 = sha_file(mutant_certificate_path)
        mutant_certificate["fields"] = []
        mutant_certificate["combined_evaluated_field_rank"] = 4
        mutant_certificate["sampled_point_evidence"] = {
            "kind": "sampled_jacobian_rank_lower_bound",
            "rank": mutant_certificate["lower_rank"],
            "sample_point": "default_exact_point",
            "claimed_use": "generic_rank_upper_bound",
        }
        mutant_certificate_path.write_text(
            json.dumps(mutant_certificate, indent=2, sort_keys=True) + "\n"
        )
        mutant_manifest = reseal_manifest(mutant_root)
        # The copied complete package contains its authoritative canonical PASS
        # replay.  Direct the mutant invocation to that canonical path so the
        # production verifier must consume/remove the stale success artifact
        # before doing any fallible semantic work.
        mutant_output = mutant_root / "rank_upper_replay.json"
        require(
            json.loads(mutant_output.read_text()).get("status") == "pass",
            "mutant lacks pre-existing canonical PASS artifact",
        )
        preexisting_mutant_success_sha256 = sha_file(mutant_output)
        expected = (
            "K2P_RANK_UPPER_REPLAY_FAIL:"
            "RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6"
        )
        mutant_result, mutant_runtime = invoke_production_verifier(
            mutant_root, mutant_output, args.timeout_seconds
        )
        qualified, observed = qualifies_failure(
            mutant_result, expected, mutant_output
        )
        require(qualified, f"sampled substitution not semantically rejected:{observed}")
        results.append({
            "mutation": "sampled_rank_substituted_for_symbolic_upper",
            "test_type": "complete_disposable_rank_certificate_package_attack",
            "complete_mutant_package_created": True,
            "mutated_certificate": "exception_syzygies/orbit_000.json",
            "original_certificate_sha256": original_certificate_sha256,
            "mutated_certificate_sha256": sha_file(mutant_certificate_path),
            "mutant_manifest_file_count": mutant_manifest["file_count"],
            "mutant_manifest_aggregate_sha256": mutant_manifest["aggregate_sha256"],
            "sampled_evidence_cannot_prove_global_upper_bound": True,
            "production_verifier_invoked": True,
            "production_verifier_sha256": sha_file(VERIFIER),
            "verifier_exit_code": mutant_result.returncode,
            "expected_semantic_diagnostic": expected,
            "observed_semantic_diagnostic": observed,
            "semantic_diagnostic_matched": True,
            "preexisting_canonical_success_artifact_present": True,
            "preexisting_canonical_success_artifact_sha256": (
                preexisting_mutant_success_sha256
            ),
            "canonical_success_artifact_removed_before_mutant_work": True,
            "success_artifact_created": False,
            "traceback_observed": False,
            "status": "rejected",
            "rejected": True,
        })

        wrong = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="K2P_RANK_UPPER_REPLAY_FAIL:wrong gate\n"
        )
        crash = subprocess.run(
            [sys.executable, "-B", "-c", "raise RuntimeError('unrelated crash control')"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        control_artifact = scratch / "control-success.json"
        signal = subprocess.CompletedProcess(
            args=[], returncode=-9, stdout=expected + "\n"
        )
        non_one = subprocess.CompletedProcess(
            args=[], returncode=2, stdout=expected + "\n"
        )
        pass_token = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout=expected + "\nK2P_RANK_UPPER_REPLAY_PASS {\"mutant\":true}\n",
        )
        stale_control = scratch / "stale-pass-report.json"
        stale_control.write_text('{"status":"pass"}\n')
        clear_stale_output(stale_control)
        timeout_rejected = False
        try:
            subprocess.run(
                [sys.executable, "-B", "-c", "import time; time.sleep(1)"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                timeout=0.01,
            )
        except subprocess.TimeoutExpired:
            timeout_rejected = True
        require(timeout_rejected, "timeout control did not time out")
        optimized_output = scratch / "optimized-stale-pass-report.json"
        optimized_output.write_text('{"status":"pass"}\n')
        optimized_environment = dict(os.environ)
        optimized_environment["PYTHONPATH"] = os.pathsep.join((str(ATLAS), str(WORK)))
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(Path(__file__).resolve()),
                "--output",
                str(optimized_output),
            ],
            cwd=ROOT,
            env=optimized_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            optimized.returncode == 1
            and optimized.stdout.strip() == "K2P_RANK_MUTATION_OPTIMIZED_MODE_FORBIDDEN"
            and not optimized_output.exists(),
            "optimized stale-output control",
        )
        require(not qualifies_failure(wrong, expected, control_artifact)[0], "wrong diagnostic qualified")
        require(not qualifies_failure(crash, expected, control_artifact)[0], "unrelated crash qualified")
        require(not qualifies_failure(signal, expected, control_artifact)[0], "signal exit qualified")
        require(not qualifies_failure(non_one, expected, control_artifact)[0], "non-one exit qualified")
        require(not qualifies_failure(pass_token, expected, control_artifact)[0], "PASS token output qualified")
        require(not stale_control.exists(), "stale PASS output survived")

        coverage_path = clean_root / "rank_upper_coverage.json"
        coverage_sha256 = sha_file(coverage_path)
        collision_result, _ = invoke_production_verifier(
            clean_root, coverage_path, args.timeout_seconds
        )
        collision_expected = (
            "K2P_RANK_UPPER_OUTPUT_POLICY_FAIL:output hardlinks or collides with input"
        )
        collision_observed = diagnostic_line(collision_result.stdout, collision_expected)
        require(
            collision_result.returncode == 1
            and collision_observed == collision_expected
            and sha_file(coverage_path) == coverage_sha256
            and "Traceback (most recent call last):" not in collision_result.stdout,
            "certificate input collision not rejected",
        )
        symlink_output = scratch / "symlink-output.json"
        symlink_output.symlink_to(coverage_path)
        symlink_result, _ = invoke_production_verifier(
            clean_root, symlink_output, args.timeout_seconds
        )
        symlink_expected = "K2P_RANK_UPPER_OUTPUT_POLICY_FAIL:output symlink"
        symlink_observed = diagnostic_line(symlink_result.stdout, symlink_expected)
        require(
            symlink_result.returncode == 1
            and symlink_observed == symlink_expected
            and sha_file(coverage_path) == coverage_sha256,
            "symlink output not rejected",
        )
        symlink_output.unlink()
        hardlink_output = scratch / "hardlink-output.json"
        os.link(coverage_path, hardlink_output)
        hardlink_result, _ = invoke_production_verifier(
            clean_root, hardlink_output, args.timeout_seconds
        )
        hardlink_observed = diagnostic_line(hardlink_result.stdout, collision_expected)
        require(
            hardlink_result.returncode == 1
            and hardlink_observed == collision_expected
            and sha_file(coverage_path) == coverage_sha256,
            "hardlink output not rejected",
        )
        hardlink_output.unlink()
        verifier_optimized_output = scratch / "verifier-optimized-stale.json"
        verifier_optimized_output.write_text('{"status":"pass"}\n')
        verifier_optimized_environment = dict(os.environ)
        verifier_optimized_environment["PYTHONPATH"] = os.pathsep.join(
            (str(ATLAS), str(WORK))
        )
        verifier_optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(VERIFIER),
                "--atlas",
                str(ATLAS),
                "--certificate-dir",
                str(clean_root),
                "--output",
                str(verifier_optimized_output),
            ],
            cwd=ROOT,
            env=verifier_optimized_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            verifier_optimized.returncode == 1
            and verifier_optimized.stdout.strip()
            == "K2P_RANK_UPPER_OPTIMIZED_MODE_FORBIDDEN"
            and not verifier_optimized_output.exists(),
            "verifier optimized stale-output control",
        )

        # Copy only the two entry points into an otherwise isolated tree.
        # Their local mathematical imports must fail, but only *after* each
        # validated stale output has been removed.
        shadow = scratch / "missing-dependency-shadow"
        shadow_scripts = shadow / "work/rank_upper_certificates"
        shadow_scripts.mkdir(parents=True)
        shadow_runner = shadow_scripts / "mutation_tests.py"
        shadow_verifier = shadow_scripts / "verify_rank_upper_certificates.py"
        shutil.copyfile(Path(__file__).resolve(), shadow_runner)
        shutil.copyfile(VERIFIER, shadow_verifier)
        shadow_strict = shadow / "work/final_theorem_release/strict_json.py"
        shadow_strict.parent.mkdir(parents=True)
        shutil.copyfile(
            ROOT / "work/final_theorem_release/strict_json.py", shadow_strict
        )
        shadow_environment = dict(os.environ)
        shadow_environment["PYTHONPATH"] = ""
        shadow_environment["PYTHONDONTWRITEBYTECODE"] = "1"

        runner_dependency_output = scratch / "runner-missing-dependency-stale.json"
        runner_dependency_output.write_text('{"status":"pass"}\n')
        runner_dependency = subprocess.run(
            [
                sys.executable,
                "-B",
                str(shadow_runner),
                "--output",
                str(runner_dependency_output),
            ],
            cwd=shadow,
            env=shadow_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            runner_dependency.returncode != 0
            and not runner_dependency_output.exists()
            and "ModuleNotFoundError" in runner_dependency.stdout
            and "K2P_RANK_UPPER_MUTATIONS_PASS " not in runner_dependency.stdout,
            "runner missing-dependency stale-output control",
        )

        verifier_dependency_root = shadow / "empty-certificate"
        verifier_dependency_root.mkdir()
        verifier_dependency_output = (
            verifier_dependency_root / "rank_upper_replay.json"
        )
        verifier_dependency_output.write_text('{"status":"pass"}\n')
        verifier_dependency = subprocess.run(
            [
                sys.executable,
                "-B",
                str(shadow_verifier),
                "--certificate-dir",
                str(verifier_dependency_root),
            ],
            cwd=shadow,
            env=shadow_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        require(
            verifier_dependency.returncode != 0
            and not verifier_dependency_output.exists()
            and "ModuleNotFoundError" in verifier_dependency.stdout
            and "K2P_RANK_UPPER_REPLAY_PASS " not in verifier_dependency.stdout,
            "verifier missing-dependency stale-output control",
        )

    require(
        validate_authoritative_manifest(WORK) == authoritative_manifest,
        "authoritative rank package drift",
    )
    after = source_fingerprints()
    require(before == after, "rank mutation source fingerprint drift")
    require(len(results) == 7 and all(row["status"] == "rejected" for row in results), str(results))
    report = {
        "schema": "k2p-rank-upper-adversarial-mutations-v2",
        "status": "pass",
        "mutation_count": len(results),
        "complete_production_verifier_attacks": 1,
        "survivors": 0,
        "production_verifier_sha256": sha_file(VERIFIER),
        "mutation_runner_sha256": sha_file(Path(__file__)),
        "helper_expected_diagnostics": HELPER_EXPECTED,
        "clean_baseline": {
            "authoritative_package_verified_in_place": True,
            "authoritative_package_unmodified": True,
            "authoritative_manifest_verified": True,
            "authoritative_manifest_file_count": authoritative_manifest["file_count"],
            "authoritative_manifest_aggregate_sha256": authoritative_manifest[
                "aggregate_sha256"
            ],
            "authoritative_sha256_manifest_sha256": authoritative_manifest[
                "sha256_manifest_sha256"
            ],
            "authoritative_json_manifest_sha256": authoritative_manifest[
                "json_manifest_sha256"
            ],
            "production_verifier_invoked": True,
            "full_symbolic_base_recompute": True,
            "descriptor_count": clean_payload["descriptor_count"],
            "zero_unresolved": clean_payload["zero_unresolved"],
            "base_recomputed": clean_payload["base_recomputed"],
            "stored_authoritative_replay_byte_identical": True,
            "stored_authoritative_replay_sha256": sha_file(
                WORK / "rank_upper_replay.json"
            ),
            "verifier_exit_code": clean_result.returncode,
            "success_artifact_created": True,
            "pass_token_count": len(clean_pass_lines),
            "status": "pass",
        },
        "qualification_negative_controls": {
            "wrong_diagnostic_not_qualified": True,
            "wrong_helper_diagnostic_not_qualified": True,
            "wrong_helper_exception_type_not_qualified": True,
            "unrelated_traceback_not_qualified": True,
            "signal_or_non_one_exit_not_qualified": True,
            "timeout_not_qualified": True,
            "failure_output_with_pass_token_not_qualified": True,
            "stale_pass_output_removed_before_work": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
            "runner_missing_dependency_stale_pass_removed_before_import_failure": True,
        },
        "production_output_policy_negative_controls": {
            "certificate_input_collision_rejected": True,
            "symlink_output_rejected": True,
            "hardlink_output_rejected": True,
            "verifier_optimized_mode_stale_pass_removed_before_rejection": True,
            "verifier_missing_dependency_stale_pass_removed_before_import_failure": True,
        },
        "source_fingerprints_unchanged": True,
        "results": results,
    }
    report["payload_sha256"] = sha(report)
    atomic_write(output, canonical_bytes(report) + b"\n")
    print(
        "K2P_RANK_UPPER_MUTATIONS_PASS "
        + json.dumps({
            "complete_production_verifier_attacks": 1,
            "mutations_rejected": len(results),
            "payload_sha256": report["payload_sha256"],
            "production_runtime_seconds": round(clean_runtime + mutant_runtime, 3),
            "survivors": 0,
        }, sort_keys=True)
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"K2P_RANK_UPPER_MUTATIONS_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
