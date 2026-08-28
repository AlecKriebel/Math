#!/usr/bin/env python3
"""Fail-closed mutations for the literal K2P quartet semantics gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import StrictJSONError, decode_json_document  # noqa: E402

SPEC = HERE / "QUARTET_SEMANTICS_SPEC.json"
VERIFIER = HERE / "verify_quartet_logic.py"
BASELINE_CERTIFICATE = HERE / "quartet_logic_certificate.json"
AUTHORITATIVE_OUTPUT = HERE / "quartet_semantics_mutation_certificate.json"
EXPECTED_DIAGNOSTICS = {
    "spectrum_G_T_swap": (
        "QUARTET_LOGIC_VERIFY_FAIL:EQUAL_SECTOR_SPECTRUM_FAIL:"
        "{'0': '1', 'C': 's', 'G': 's', 'T': 'g'}"
    ),
    "wrong_F_coordinate": (
        "QUARTET_LOGIC_VERIFY_FAIL:CANONICAL_PULLBACK_FAIL:"
        "{'formula': 'F_A', 'topology': '12|34', "
        "'observed': 'g1*g2*g3*g4 - s1*s2*s3*s4', 'expected': '0'}"
    ),
    "wrong_J_coefficient": (
        "QUARTET_LOGIC_VERIFY_FAIL:CANONICAL_PULLBACK_FAIL:"
        "{'formula': 'J_B', 'topology': '12|34', "
        "'observed': '-2*gI*s1*s2*s3*s4', 'expected': '0'}"
    ),
    "wrong_character_order": "QUARTET_LOGIC_VERIFY_FAIL:CHARACTER_ORDER_CONTRACT_FAIL",
    "wrong_coordinate_dictionary": (
        "QUARTET_LOGIC_VERIFY_FAIL:CANONICAL_COORDINATE_CONTRACT_FAIL"
    ),
    "wrong_D_plus_declaration": (
        "QUARTET_LOGIC_VERIFY_FAIL:DOMAIN_DECLARATION_CONTRACT_FAIL"
    ),
    "printed_formula_reverted_to_wrong_sector": (
        "QUARTET_LOGIC_VERIFY_FAIL:DOCUMENT_LITERAL_BINDING_FAIL:"
        "{'path': 'proof_compression_submission/article/main.tex', "
        "'literal': 'F_A&=q_{CCCC}-q_{CCTT}', 'count': 0}"
    ),
    "optimized_python": "QUARTET_LOGIC_OPTIMIZED_MODE_FORBIDDEN",
}


class MutationFailure(RuntimeError):
    pass


def load_plain_json(path: Path):
    try:
        return decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise MutationFailure(f"strict JSON:{path}:{error}") from error


def require(condition: bool, message: str) -> None:
    if not condition:
        raise MutationFailure(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_inputs() -> set[Path]:
    spec = load_plain_json(SPEC)
    documents = {PROJECT / row["path"] for row in spec["document_contracts"]}
    return {
        Path(__file__).resolve(),
        SPEC.resolve(),
        VERIFIER.resolve(),
        BASELINE_CERTIFICATE.resolve(),
        *(path.resolve() for path in documents),
    }


def source_fingerprints() -> dict[str, str]:
    return {
        path.relative_to(PROJECT).as_posix(): sha_file(path)
        for path in sorted(source_inputs())
    }


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if lexical.is_symlink():
        raise SystemExit("QUARTET_MUTATION_OUTPUT_POLICY_FAIL:output symlink")
    if lexical.exists() and any(
        source.exists() and os.path.samefile(lexical, source)
        for source in source_inputs()
    ):
        raise SystemExit("QUARTET_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source")
    if allow_authoritative_output:
        if normalized != authoritative:
            raise SystemExit(
                "QUARTET_MUTATION_OUTPUT_POLICY_FAIL:wrong authoritative path"
            )
        return normalized
    try:
        normalized.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "QUARTET_MUTATION_OUTPUT_POLICY_FAIL:routine output must be external"
    )


def clear_stale_output(path: Path) -> None:
    path.unlink(missing_ok=True)
    require(not path.exists(), f"stale output remains:{path.name}")


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
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def run_verifier(
    *,
    project: Path,
    spec: Path,
    output: Path,
    timeout: float,
    skip_documents: bool = False,
    optimized: bool = False,
    clear_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    if clear_output:
        output.unlink(missing_ok=True)
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(
        [
            "-B",
            str(VERIFIER),
            "--project",
            str(project),
            "--spec",
            str(spec),
            "--output",
            str(output),
        ]
    )
    if skip_documents:
        command.append("--skip-document-binding")
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=timeout,
        env={
            **os.environ,
            "PYTHONHASHSEED": "47",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


def qualify_failure(
    completed: subprocess.CompletedProcess[str], expected: str, output: Path
) -> tuple[bool, str | None]:
    combined = (completed.stderr or "") + (completed.stdout or "")
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    exact = [line for line in lines if line == expected]
    forbidden = (
        "Traceback (most recent call last):",
        "ModuleNotFoundError",
        "ImportError:",
        "TimeoutExpired",
    )
    qualified = (
        completed.returncode == 1
        and exact == [expected]
        and len(lines) == 1
        and not output.exists()
        and not any(marker in combined for marker in forbidden)
        and '"status": "PASS"' not in combined
        and '"status":"PASS"' not in combined
    )
    return qualified, exact[0] if exact else None


def record_failure(
    rows: list[dict[str, Any]],
    name: str,
    completed: subprocess.CompletedProcess[str],
    output: Path,
    test_type: str,
    *,
    preexisting_removed: bool = False,
) -> None:
    expected = EXPECTED_DIAGNOSTICS[name]
    qualified, observed = qualify_failure(completed, expected, output)
    require(
        qualified,
        f"unqualified rejection:{name}:{completed.returncode}:{observed}",
    )
    row = {
        "case": name,
        "test_type": test_type,
        "production_verifier_invoked": True,
        "production_verifier_sha256": sha_file(VERIFIER),
        "expected_exception_type": (
            "SystemExit" if name == "optimized_python" else "QuartetFailure"
        ),
        "expected_semantic_diagnostic": expected,
        "observed_semantic_diagnostic": observed,
        "semantic_diagnostic_matched": True,
        "verifier_exit_code": completed.returncode,
        "success_artifact_created": False,
        "traceback_observed": False,
        "import_failure_observed": False,
        "success_token_observed": False,
        "rejected": True,
        "status": "REJECTED",
    }
    if preexisting_removed:
        row["preexisting_success_artifact_removed"] = True
    rows.append(row)


def write_mutated_spec(
    root: Path,
    name: str,
    mutate: Callable[[dict[str, Any]], None],
) -> Path:
    spec = load_plain_json(SPEC)
    mutate(spec)
    path = root / f"{name}.json"
    path.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
    return path


def document_project(root: Path) -> Path:
    project = root / "document-project"
    spec = load_plain_json(SPEC)
    for contract in spec["document_contracts"]:
        relative = Path(contract["path"])
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT / relative, destination)
    article = project / "proof_compression_submission/article/main.tex"
    text = article.read_text(encoding="utf-8")
    old = "F_A&=q_{CCCC}-q_{CCTT}"
    require(text.count(old) == 1, "article mutation anchor")
    article.write_text(text.replace(old, "F_A&=q_{GGGG}-q_{GGTT}"))
    return project


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    arguments = parser.parse_args()
    require(arguments.timeout_seconds > 0, "invalid timeout")
    output = validate_output_path(arguments.output, arguments.allow_authoritative_output)
    clear_stale_output(output)
    if not __debug__:
        raise SystemExit("QUARTET_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")

    before = source_fingerprints()
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="k2p-quartet-mutations-") as directory:
        root = Path(directory)
        clean_output = root / "clean-quartet-logic.json"
        clean = run_verifier(
            project=PROJECT,
            spec=SPEC,
            output=clean_output,
            timeout=arguments.timeout_seconds,
        )
        require(
            clean.returncode == 0
            and clean_output.is_file()
            and clean_output.read_bytes() == BASELINE_CERTIFICATE.read_bytes()
            and "Traceback (most recent call last):" not in clean.stderr + clean.stdout,
            "clean baseline",
        )
        clean_payload = load_plain_json(clean_output)
        clean_unsigned = dict(clean_payload)
        clean_claimed = clean_unsigned.pop("payload_sha256")
        require(clean_claimed == sha_object(clean_unsigned), "clean payload hash")
        require(
            clean_payload.get("schema") == "k2p-displayed-quartet-semantics-v2"
            and clean_payload.get("status") == "PASS"
            and clean_payload.get("canonical_formula_count") == 6
            and clean_payload.get("formula_transport_count") == 288
            and clean_payload.get("displayed_set_count") == 7
            and clean_payload.get("unequal_pair_count") == 21
            and len(clean_payload.get("document_sha256", {})) == 5,
            "clean baseline census",
        )

        mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            (
                "spectrum_G_T_swap",
                lambda spec: spec["edge_spectrum"].update({"G": "s", "T": "g"}),
            ),
            (
                "wrong_F_coordinate",
                lambda spec: spec["canonical_formulas"]["F_A"][0].__setitem__(
                    1, "GGGG"
                ),
            ),
            (
                "wrong_J_coefficient",
                lambda spec: spec["canonical_formulas"]["J_B"][2].__setitem__(0, -1),
            ),
            (
                "wrong_character_order",
                lambda spec: spec.__setitem__(
                    "character_order", ["0", "C", "T", "G"]
                ),
            ),
            (
                "wrong_coordinate_dictionary",
                lambda spec: spec["canonical_coordinates"].__setitem__("QA", "GGTT"),
            ),
            (
                "wrong_D_plus_declaration",
                lambda spec: spec["domain"].__setitem__(
                    "principal", "0<s<1, 0<g<1, g>=2s-1"
                ),
            ),
        ]
        for name, mutate in mutations:
            mutated = write_mutated_spec(root, name, mutate)
            child_output = root / f"{name}-certificate.json"
            completed = run_verifier(
                project=PROJECT,
                spec=mutated,
                output=child_output,
                timeout=arguments.timeout_seconds,
                skip_documents=True,
            )
            record_failure(
                rows,
                name,
                completed,
                child_output,
                "complete_disposable_semantics_spec_attack",
            )

        project = document_project(root)
        document_output = root / "document-certificate.json"
        completed = run_verifier(
            project=project,
            spec=SPEC,
            output=document_output,
            timeout=arguments.timeout_seconds,
        )
        record_failure(
            rows,
            "printed_formula_reverted_to_wrong_sector",
            completed,
            document_output,
            "complete_disposable_document_binding_attack",
        )

        optimized_output = root / "optimized-certificate.json"
        optimized_output.write_text('{"status":"PASS"}\n')
        optimized = run_verifier(
            project=PROJECT,
            spec=SPEC,
            output=optimized_output,
            timeout=arguments.timeout_seconds,
            optimized=True,
            clear_output=False,
        )
        record_failure(
            rows,
            "optimized_python",
            optimized,
            optimized_output,
            "optimized_production_verifier_attack",
            preexisting_removed=True,
        )

        expected = EXPECTED_DIAGNOSTICS["wrong_character_order"]
        control_output = root / "control-output.json"
        controls = {
            "wrong_diagnostic_not_qualified": subprocess.CompletedProcess(
                [], 1, "", "QUARTET_LOGIC_VERIFY_FAIL:WRONG\n"
            ),
            "traceback_not_qualified": subprocess.CompletedProcess(
                [], 1, "", f"Traceback (most recent call last):\n{expected}\n"
            ),
            "import_error_not_qualified": subprocess.CompletedProcess(
                [], 1, "", f"ImportError: missing\n{expected}\n"
            ),
            "signal_not_qualified": subprocess.CompletedProcess(
                [], -9, "", expected + "\n"
            ),
            "non_one_exit_not_qualified": subprocess.CompletedProcess(
                [], 2, "", expected + "\n"
            ),
            "pass_token_not_qualified": subprocess.CompletedProcess(
                [], 1, '{"status":"PASS"}\n', expected + "\n"
            ),
        }
        for label, completed in controls.items():
            require(
                not qualify_failure(completed, expected, control_output)[0],
                f"negative control qualified:{label}",
            )
        control_output.write_text('{"status":"PASS"}\n')
        require(
            not qualify_failure(
                subprocess.CompletedProcess([], 1, "", expected + "\n"),
                expected,
                control_output,
            )[0],
            "preexisting PASS artifact qualified",
        )
        control_output.unlink()
        timed_out = False
        try:
            subprocess.run(
                [sys.executable, "-B", "-c", "import time; time.sleep(1)"],
                capture_output=True,
                text=True,
                timeout=0.01,
                check=False,
            )
        except subprocess.TimeoutExpired:
            timed_out = True
        require(timed_out, "timeout control did not time out")

        shadow = root / "missing-sympy"
        shadow.mkdir()
        (shadow / "sympy.py").write_text("raise ImportError('shadowed sympy')\n")
        import_output = root / "missing-import-stale.json"
        import_output.write_text('{"status":"PASS"}\n')
        missing_import = subprocess.run(
            [
                sys.executable,
                "-B",
                str(VERIFIER),
                "--project",
                str(PROJECT),
                "--spec",
                str(SPEC),
                "--output",
                str(import_output),
            ],
            capture_output=True,
            text=True,
            check=False,
            env={
                **os.environ,
                "PYTHONPATH": str(shadow),
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )
        require(
            missing_import.returncode == 1
            and "ImportError: shadowed sympy" in missing_import.stderr
            and not import_output.exists()
            and not qualify_failure(missing_import, expected, import_output)[0],
            "missing dependency stale-output control",
        )

        optimized_runner_output = root / "optimized-runner-stale.json"
        optimized_runner_output.write_text('{"status":"PASS"}\n')
        optimized_runner = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(Path(__file__).resolve()),
                "--output",
                str(optimized_runner_output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            optimized_runner.returncode == 1
            and optimized_runner.stderr.strip()
            == "QUARTET_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN"
            and not optimized_runner_output.exists(),
            "optimized runner stale-output control",
        )

        policy_target = root / "policy-target.json"
        policy_target.write_text("source\n")
        policy_symlink = root / "policy-symlink.json"
        policy_symlink.symlink_to(policy_target)
        try:
            validate_output_path(policy_symlink, False)
        except SystemExit as error:
            require(
                str(error) == "QUARTET_MUTATION_OUTPUT_POLICY_FAIL:output symlink",
                "symlink output wrong diagnostic",
            )
        else:
            raise MutationFailure("symlink output accepted")
        policy_symlink.unlink()
        policy_hardlink = root / "policy-hardlink.json"
        os.link(SPEC, policy_hardlink)
        try:
            validate_output_path(policy_hardlink, False)
        except SystemExit as error:
            require(
                str(error)
                == "QUARTET_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source",
                "hardlink output wrong diagnostic",
            )
        else:
            raise MutationFailure("hardlink output accepted")
        policy_hardlink.unlink()

    require(source_fingerprints() == before, "authoritative source drift")
    require(
        [row["case"] for row in rows] == list(EXPECTED_DIAGNOSTICS)
        and len(rows) == 8,
        "mutation census/order",
    )
    report = {
        "schema": "k2p-quartet-semantics-mutations-v4",
        "status": "PASS",
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "production_verifier_sha256": sha_file(VERIFIER),
        "spec_sha256": sha_file(SPEC),
        "source_certificate_sha256": sha_file(BASELINE_CERTIFICATE),
        "source_certificate_payload_sha256": clean_payload["payload_sha256"],
        "expected_diagnostics": EXPECTED_DIAGNOSTICS,
        "clean_baseline": {
            "production_verifier_invoked": True,
            "verifier_exit_code": 0,
            "success_artifact_created": True,
            "success_artifact_byte_identical_to_stored": True,
            "success_artifact_sha256": sha_file(BASELINE_CERTIFICATE),
            "canonical_formula_count": 6,
            "formula_transport_count": 288,
            "displayed_set_count": 7,
            "unequal_pair_count": 21,
            "document_count": 5,
            "status": "PASS",
        },
        "qualification_negative_controls": {
            "wrong_diagnostic_not_qualified": True,
            "traceback_not_qualified": True,
            "import_error_not_qualified": True,
            "timeout_not_qualified": True,
            "signal_not_qualified": True,
            "non_one_exit_not_qualified": True,
            "pass_token_not_qualified": True,
            "preexisting_pass_artifact_not_qualified": True,
            "import_failure_stale_pass_removed_before_failure": True,
            "optimized_mode_stale_pass_removed_before_rejection": True,
        },
        "output_policy_negative_controls": {
            "symlink_output_rejected": True,
            "hardlink_source_output_rejected": True,
        },
        "execution_contract": {
            "clean_baseline_required": True,
            "exact_full_diagnostic_and_exception_type_required": True,
            "return_code_one_required": True,
            "traceback_import_timeout_signal_non_one_rejected": True,
            "success_tokens_and_artifacts_rejected": True,
            "routine_output_caller_owned_external": True,
            "authoritative_output_requires_exact_override": True,
            "atomic_output_publication": True,
            "stale_output_removed_before_optimized_and_import_work": True,
            "absolute_paths_recorded": False,
            "runtime_fields_recorded": False,
        },
        "source_fingerprints_unchanged": True,
        "case_count": len(rows),
        "survived": 0,
        "cases": rows,
    }
    report["payload_sha256"] = sha_object(report)
    atomic_write(
        output, json.dumps(report, indent=2, sort_keys=True).encode() + b"\n"
    )
    print("K2P_QUARTET_SEMANTICS_MUTATIONS_PASS")
    print(
        json.dumps(
            {
                "cases": len(rows),
                "payload_sha256": report["payload_sha256"],
                "survived": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (
        MutationFailure,
        KeyError,
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as exc:
        print(f"QUARTET_SEMANTICS_MUTATION_FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
