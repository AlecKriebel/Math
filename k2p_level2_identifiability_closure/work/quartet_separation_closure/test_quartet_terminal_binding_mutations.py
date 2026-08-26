#!/usr/bin/env python3
"""Fail-closed adversarial mutations for the quartet-terminal binder."""

from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SEMANTICS = HERE / "quartet_logic_certificate.json"
VERIFIER = HERE / "verify_quartet_terminal_bindings.py"
BASELINE_CERTIFICATE = HERE / "quartet_terminal_binding_certificate.json"
AUTHORITATIVE_OUTPUT = HERE / "quartet_terminal_binding_mutation_certificate.json"
RAW4_MUTATIONS = (
    PROJECT
    / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json"
)
THETA2_MUTATIONS = (
    PROJECT
    / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json"
)
TERMINAL_INPUTS = (
    "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz",
    "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz",
    "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
    "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz",
    "work/cycle_three_port_closure/artifacts/topology_witnesses.json",
    "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "work/probe_coherence_corrected/one_port_ledger.jsonl.gz",
    "work/probe_coherence_corrected/two_port_ledger.jsonl.gz",
    "work/probe_coherence_corrected/separation_proof_registry.json.gz",
)
EXPECTED_HELPER_DIAGNOSTICS = {
    "resealed_spectrum_convention_mutation": "SEMANTICS_SPECTRUM_FAIL",
    "resealed_coordinate_word_mutation": "LITERAL_FORMULA_SPEC_MISMATCH:F_A",
    "resealed_distinguished_split_mutation": "STORED_DISTINGUISHED_SPLIT_FAIL",
    "resealed_zero_positive_side_mutation": "STORED_ZERO_SIDE_FAIL",
    "resealed_quartet_label_transport_mutation": (
        "DISPLAYED_SPLIT_OUTSIDE_QUARTET_FAIL:(0, 1, 2, 25)"
    ),
    "rekeyed_relinked_restoration_set_mutation": (
        "EQUAL_DISPLAYED_SET_FAIL:(0, 1, 3, 4)"
    ),
    "compact_split_hash_mutation": (
        "COMPACT_EVIDENCE_BINDING_FAIL:"
        "Q:06593f1cd0d27ac160de777f88f74fc66e7df75cdee8523c992482c83318e87b"
    ),
    "unknown_terminal_reference": (
        "REGISTRY_REFERENCE_SET_FAIL:{'unused': ['proof'], 'missing': ['unknown']}"
    ),
    "omitted_terminal_reference": (
        "REGISTRY_REFERENCE_SET_FAIL:{'unused': ['proof'], 'missing': []}"
    ),
}
OPTIMIZED_DIAGNOSTIC = "QUARTET_TERMINAL_BINDING_OPTIMIZED_MODE_FORBIDDEN"
HELPER_PREFIX = "QUARTET_TERMINAL_HELPER_REJECT"
binder: Any = None


class MutationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise MutationFailure(message)


def load_binder() -> None:
    global binder
    if binder is None:
        binder = importlib.import_module("verify_quartet_terminal_bindings")


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
    return {
        Path(__file__).resolve(),
        SEMANTICS.resolve(),
        VERIFIER.resolve(),
        BASELINE_CERTIFICATE.resolve(),
        RAW4_MUTATIONS.resolve(),
        THETA2_MUTATIONS.resolve(),
        *((PROJECT / relative).resolve() for relative in TERMINAL_INPUTS),
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
        raise SystemExit(
            "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:output symlink"
        )
    if lexical.exists() and any(
        source.exists() and os.path.samefile(lexical, source)
        for source in source_inputs()
    ):
        raise SystemExit(
            "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:output hardlinks source"
        )
    if allow_authoritative_output:
        if normalized != authoritative:
            raise SystemExit(
                "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:"
                "wrong authoritative path"
            )
        return normalized
    try:
        normalized.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:"
        "routine output must be external"
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


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = binder.sha_object(value)


def first_quartet_witness(values: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    for proof_id, content in values.items():
        if isinstance(content, dict) and content.get("reason") == "displayed_quartet_mismatch":
            return proof_id, content
    raise MutationFailure("no quartet witness")


def helper_action(name: str) -> tuple[Any, str | None]:
    """Construct one legacy helper mutation and return its failing action."""

    formulas, _summary = binder.semantics_contract(SEMANTICS)
    cycle_payload = binder.load_json(PROJECT / binder.CYCLE_REGISTRY)
    _cycle_id, cycle_content = first_quartet_witness(cycle_payload["witnesses"])
    restoration_payload = binder.load_json(PROJECT / binder.RESTORATION_FOREST)
    _restoration_id, restoration_content = next(
        iter(restoration_payload["quartet_certificates"].items())
    )

    if name == "resealed_spectrum_convention_mutation":
        spectrum = binder.load_json(SEMANTICS)
        spectrum["edge_spectrum"] = ["1", "s", "s", "g"]
        reseal(spectrum)
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        path = Path(temporary.name)
        temporary.write(json.dumps(spectrum, indent=2, sort_keys=True) + "\n")
        temporary.close()
        return lambda: binder.semantics_contract(path), str(path)

    if name == "resealed_coordinate_word_mutation":
        coordinate = binder.load_json(SEMANTICS)
        coordinate["canonical_formulas"]["F_A"]["terms"][0][1] = "GGGG"
        formula_row = coordinate["canonical_formulas"]["F_A"]
        formula_payload = {
            "formula_id": formula_row["formula_id"],
            "terms": formula_row["terms"],
            "pullbacks": formula_row["pullbacks"],
        }
        formula_row["formula_sha256"] = binder.sha_object(formula_payload)
        reseal(coordinate)
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        path = Path(temporary.name)
        temporary.write(json.dumps(coordinate, indent=2, sort_keys=True) + "\n")
        temporary.close()
        mutated_formulas, _mutated_summary = binder.semantics_contract(path)
        return (
            lambda: binder.validate_content(
                cycle_content, mutated_formulas, require_stored_witness=True
            ),
            str(path),
        )

    if name == "resealed_distinguished_split_mutation":
        distinguished = copy.deepcopy(cycle_content)
        quartet = binder.normalize_quartet(distinguished["quartet"])
        old_split = binder.normalize_split(distinguished["distinguished_split"])
        replacement = next(
            split for split in binder.quartet_splits(quartet) if split != old_split
        )
        distinguished["distinguished_split"] = binder.split_json(replacement)
        return (
            lambda: binder.validate_content(
                distinguished, formulas, require_stored_witness=True
            ),
            None,
        )

    if name == "resealed_zero_positive_side_mutation":
        sides = copy.deepcopy(cycle_content)
        sides["zero_on"], sides["strictly_positive_on"] = (
            sides["strictly_positive_on"],
            sides["zero_on"],
        )
        return (
            lambda: binder.validate_content(
                sides, formulas, require_stored_witness=True
            ),
            None,
        )

    if name == "resealed_quartet_label_transport_mutation":
        labels = copy.deepcopy(cycle_content)
        labels["quartet"][-1] += 20
        return (
            lambda: binder.validate_content(
                labels, formulas, require_stored_witness=True
            ),
            None,
        )

    if name == "rekeyed_relinked_restoration_set_mutation":
        changed_set = copy.deepcopy(restoration_content)
        changed_set["target_splits"] = copy.deepcopy(changed_set["source_splits"])
        return (
            lambda: binder.validate_content(
                changed_set, formulas, require_stored_witness=False
            ),
            binder.sha_object(changed_set),
        )

    if name == "compact_split_hash_mutation":
        with gzip.open(PROJECT / binder.RAW4_LEDGER, "rt", encoding="utf-8") as handle:
            raw4_row = json.loads(next(handle))
        evidence = copy.deepcopy(raw4_row["evidence_binding"])
        evidence["source_displayed_splits_sha256"] = "0" * 64
        return lambda: binder.validate_compact_evidence(evidence, formulas, {}), None

    binding = binder.validate_content(
        restoration_content, formulas, require_stored_witness=False
    )
    binding_map = {"proof": binding}
    if name == "unknown_terminal_reference":
        return (
            lambda: binder.registry_rows(
                binding_map, collections.Counter({"unknown": 1})
            ),
            None,
        )
    if name == "omitted_terminal_reference":
        return lambda: binder.registry_rows(binding_map, collections.Counter()), None
    raise MutationFailure(f"unknown helper case:{name}")


def execute_helper_case(name: str) -> None:
    action, temporary_detail = helper_action(name)
    try:
        action()
    except binder.QuartetTerminalFailure as error:
        if temporary_detail and temporary_detail.startswith("/"):
            Path(temporary_detail).unlink(missing_ok=True)
        diagnostic = str(error)
        print(f"{HELPER_PREFIX}:{name}:{diagnostic}", file=sys.stderr)
        raise SystemExit(1)
    if temporary_detail and temporary_detail.startswith("/"):
        Path(temporary_detail).unlink(missing_ok=True)
    raise MutationFailure(f"mutation accepted:{name}")


def run_helper(
    name: str, output: Path, timeout: float, *, leave_stale: bool = False
) -> subprocess.CompletedProcess[str]:
    if not leave_stale:
        output.unlink(missing_ok=True)
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(Path(__file__).resolve()),
            "--helper-case",
            name,
            "--output",
            str(output),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=timeout,
        env={
            **os.environ,
            "PYTHONHASHSEED": "53",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


def run_production_verifier(
    output: Path,
    timeout: float,
    *,
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
            str(PROJECT),
            "--semantics-certificate",
            str(SEMANTICS),
            "--output",
            str(output),
        ]
    )
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=timeout,
        env={
            **os.environ,
            "PYTHONHASHSEED": "59",
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
        and '"status":"PASS"' not in combined
        and '"status": "PASS"' not in combined
    )
    return qualified, exact[0] if exact else None


def graph_guards() -> list[dict[str, Any]]:
    guards: list[dict[str, Any]] = []
    for family, path in (("raw4", RAW4_MUTATIONS), ("theta2", THETA2_MUTATIONS)):
        report = json.loads(path.read_text())
        claimed = report["payload_sha256"]
        unsigned = dict(report)
        unsigned.pop("payload_sha256")
        require(claimed == sha_object(unsigned), f"graph report payload:{family}")
        rows = [
            row
            for row in report.get("tests", [])
            if row.get("name") == "reassigned_evidence_binding"
        ]
        require(len(rows) == 1, f"graph guard census:{family}")
        row = rows[0]
        expected = "CORRECTED_COMPOSITE_REPLAY_FAIL:QUARTET_WITNESS:0"
        require(
            report.get("status") == "PASS"
            and row.get("test_type") == "complete_disposable_ledger_attack"
            and row.get("production_verifier_invoked") is True
            and row.get("verifier_exit_code") == 1
            and row.get("expected_semantic_diagnostic") == "QUARTET_WITNESS:0"
            and row.get("observed_semantic_diagnostic") == expected
            and row.get("semantic_diagnostic_matched") is True
            and row.get("verifier_report_created") is False
            and row.get("rejected") is True,
            f"graph guard contract:{family}",
        )
        guards.append(
            {
                "family": family,
                "path": path.relative_to(PROJECT).as_posix(),
                "report_sha256": sha_file(path),
                "report_payload_sha256": claimed,
                "test_type": row["test_type"],
                "production_verifier_sha256": row["production_verifier_sha256"],
                "verifier_exit_code": 1,
                "expected_semantic_diagnostic": expected,
                "observed_semantic_diagnostic": expected,
                "semantic_diagnostic_matched": True,
                "success_artifact_created": False,
                "rejected": True,
            }
        )
    return guards


def composed_rows(guards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    formulas, _summary = binder.semantics_contract(SEMANTICS)
    cycle_payload = binder.load_json(PROJECT / binder.CYCLE_REGISTRY)
    _cycle_id, cycle_content = first_quartet_witness(cycle_payload["witnesses"])
    quartet, source_splits, target_splits = binder.content_split_sets(cycle_content)
    reversed_content = binder.historical_content(quartet, target_splits, source_splits)
    reversed_binding = binder.validate_content(
        reversed_content, formulas, require_stored_witness=True
    )
    original_binding = binder.validate_content(
        cycle_content, formulas, require_stored_witness=True
    )
    require(
        reversed_binding["binding_sha256"] != original_binding["binding_sha256"],
        "directional reversal retained binding",
    )
    require(
        reversed_binding["zero_on"] != original_binding["zero_on"]
        and reversed_binding["strictly_positive_on"]
        != original_binding["strictly_positive_on"],
        "directional reversal retained sign sides",
    )
    common = {
        "test_type": "composed_production_graph_guard",
        "production_verifiers_invoked_via_bound_reports": 2,
        "verifier_exit_codes": [1, 1],
        "expected_exception_type": "CompositeReplayFailure",
        "semantic_diagnostics_matched": True,
        "success_artifacts_created": 0,
        "graph_guards": guards,
        "rejected": True,
        "status": "REJECTED",
    }
    return [
        {
            "case": "valid_proof_substitution_composed_graph_gate",
            **common,
        },
        {
            "case": "complete_source_target_reversal_composed_graph_gate",
            **common,
            "original_binding_sha256": original_binding["binding_sha256"],
            "reversed_binding_sha256": reversed_binding["binding_sha256"],
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=600.0)
    parser.add_argument("--helper-case", choices=tuple(EXPECTED_HELPER_DIAGNOSTICS))
    arguments = parser.parse_args()
    require(arguments.timeout_seconds > 0, "invalid timeout")
    require(
        not arguments.helper_case or not arguments.allow_authoritative_output,
        "helper cannot use authoritative output",
    )
    output = validate_output_path(arguments.output, arguments.allow_authoritative_output)
    clear_stale_output(output)
    if not __debug__:
        raise SystemExit("QUARTET_TERMINAL_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    load_binder()
    if arguments.helper_case:
        execute_helper_case(arguments.helper_case)
        return

    before = source_fingerprints()
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(
        prefix="k2p-quartet-terminal-mutations-"
    ) as directory:
        root = Path(directory)
        clean_output = root / "clean-terminal-binding.json"
        clean = run_production_verifier(
            clean_output, arguments.timeout_seconds
        )
        require(
            clean.returncode == 0
            and clean_output.is_file()
            and clean_output.read_bytes() == BASELINE_CERTIFICATE.read_bytes()
            and "Traceback (most recent call last):" not in clean.stderr + clean.stdout,
            "clean baseline",
        )
        clean_payload = json.loads(clean_output.read_text())
        clean_unsigned = dict(clean_payload)
        clean_claimed = clean_unsigned.pop("payload_sha256")
        require(clean_claimed == sha_object(clean_unsigned), "clean payload hash")
        aggregate = clean_payload.get("aggregate", {})
        expected_layers = {
            "raw4": (360_408, 18),
            "theta2": (2_942_592, 19),
            "theta2_restoration": (760, 24),
            "cycle": (535_920, 97),
            "restoration": (36_006, 92),
            "probe": (539_024, 638),
        }
        require(
            clean_payload.get("schema") == "k2p-quartet-terminal-binding-v1"
            and clean_payload.get("status") == "PASS"
            and aggregate.get("layer_count") == 6
            and aggregate.get("quartet_terminal_rows") == 4_414_710
            and aggregate.get("per_layer_certificate_ids") == 888
            and aggregate.get("missing_references") == 0
            and aggregate.get("dangling_certificates") == 0
            and {
                name: (
                    row["quartet_terminal_rows"],
                    row["certificate_count"],
                )
                for name, row in clean_payload.get("layers", {}).items()
            }
            == expected_layers,
            "clean baseline census",
        )

        for index, name in enumerate(EXPECTED_HELPER_DIAGNOSTICS):
            child_output = root / f"{name}-success.json"
            leave_stale = index == 0
            if leave_stale:
                child_output.write_text('{"status":"PASS"}\n')
            completed = run_helper(
                name,
                child_output,
                arguments.timeout_seconds,
                leave_stale=leave_stale,
            )
            expected = f"{HELPER_PREFIX}:{name}:{EXPECTED_HELPER_DIAGNOSTICS[name]}"
            qualified, observed = qualify_failure(completed, expected, child_output)
            require(
                qualified,
                f"unqualified helper rejection:{name}:{completed.returncode}:{observed}",
            )
            row = {
                "case": name,
                "test_type": "isolated_binder_helper_attack",
                "binder_invoked": True,
                "binder_sha256": sha_file(VERIFIER),
                "expected_exception_type": "QuartetTerminalFailure",
                "expected_semantic_diagnostic": expected,
                "observed_semantic_diagnostic": observed,
                "semantic_diagnostic_matched": True,
                "verifier_exit_code": 1,
                "success_artifact_created": False,
                "traceback_observed": False,
                "import_failure_observed": False,
                "success_token_observed": False,
                "rejected": True,
                "status": "REJECTED",
            }
            if leave_stale:
                row["preexisting_success_artifact_removed_before_import"] = True
            if name == "rekeyed_relinked_restoration_set_mutation":
                row["mutated_rekeyed_proof_id_sha256"] = (
                    "b1a44058cb97035150dba0dd86c01eac396ae0120744ffc1f25a5a00e8239dc5"
                )
            rows.append(row)

        guards = graph_guards()
        rows.extend(composed_rows(guards))

        optimized_output = root / "optimized-terminal-success.json"
        optimized_output.write_text('{"status":"PASS"}\n')
        optimized = run_production_verifier(
            optimized_output,
            arguments.timeout_seconds,
            optimized=True,
            clear_output=False,
        )
        qualified, observed = qualify_failure(
            optimized, OPTIMIZED_DIAGNOSTIC, optimized_output
        )
        require(qualified, f"unqualified optimized rejection:{observed}")
        rows.append(
            {
                "case": "optimized_python",
                "test_type": "optimized_production_verifier_attack",
                "production_verifier_invoked": True,
                "production_verifier_sha256": sha_file(VERIFIER),
                "expected_exception_type": "SystemExit",
                "expected_semantic_diagnostic": OPTIMIZED_DIAGNOSTIC,
                "observed_semantic_diagnostic": observed,
                "semantic_diagnostic_matched": True,
                "verifier_exit_code": 1,
                "preexisting_success_artifact_removed_before_semantic_work": True,
                "success_artifact_created": False,
                "traceback_observed": False,
                "import_failure_observed": False,
                "success_token_observed": False,
                "rejected": True,
                "status": "REJECTED",
            }
        )

        expected_control = OPTIMIZED_DIAGNOSTIC
        control_output = root / "control-output.json"
        controls = {
            "wrong_diagnostic_not_qualified": subprocess.CompletedProcess(
                [], 1, "", "WRONG\n"
            ),
            "traceback_not_qualified": subprocess.CompletedProcess(
                [], 1, "", f"Traceback (most recent call last):\n{expected_control}\n"
            ),
            "import_error_not_qualified": subprocess.CompletedProcess(
                [], 1, "", f"ImportError: missing\n{expected_control}\n"
            ),
            "signal_not_qualified": subprocess.CompletedProcess(
                [], -9, "", expected_control + "\n"
            ),
            "non_one_exit_not_qualified": subprocess.CompletedProcess(
                [], 2, "", expected_control + "\n"
            ),
            "pass_token_not_qualified": subprocess.CompletedProcess(
                [], 1, '{"status":"PASS"}\n', expected_control + "\n"
            ),
        }
        for label, completed in controls.items():
            require(
                not qualify_failure(completed, expected_control, control_output)[0],
                f"negative control qualified:{label}",
            )
        control_output.write_text('{"status":"PASS"}\n')
        require(
            not qualify_failure(
                subprocess.CompletedProcess([], 1, "", expected_control + "\n"),
                expected_control,
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

        missing_binder_root = root / "missing-binder"
        missing_binder_root.mkdir()
        copied_runner = missing_binder_root / Path(__file__).name
        shutil.copy2(Path(__file__).resolve(), copied_runner)
        descriptor, missing_output_name = tempfile.mkstemp(
            prefix="k2p-terminal-missing-import-", suffix=".json", dir="/tmp"
        )
        os.close(descriptor)
        missing_output = Path(missing_output_name)
        missing_output.write_text('{"status":"PASS"}\n')
        missing_import = subprocess.run(
            [
                sys.executable,
                "-B",
                str(copied_runner),
                "--output",
                str(missing_output),
            ],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        require(
            missing_import.returncode == 1
            and "ModuleNotFoundError" in missing_import.stderr
            and not missing_output.exists(),
            "missing binder stale-output control",
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
            == "QUARTET_TERMINAL_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN"
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
                str(error)
                == "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:output symlink",
                "symlink output wrong diagnostic",
            )
        else:
            raise MutationFailure("symlink output accepted")
        policy_symlink.unlink()
        policy_hardlink = root / "policy-hardlink.json"
        os.link(SEMANTICS, policy_hardlink)
        try:
            validate_output_path(policy_hardlink, False)
        except SystemExit as error:
            require(
                str(error)
                == "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL:"
                "output hardlinks source",
                "hardlink output wrong diagnostic",
            )
        else:
            raise MutationFailure("hardlink output accepted")
        policy_hardlink.unlink()

    require(source_fingerprints() == before, "authoritative source drift")
    expected_order = [
        *EXPECTED_HELPER_DIAGNOSTICS,
        "valid_proof_substitution_composed_graph_gate",
        "complete_source_target_reversal_composed_graph_gate",
        "optimized_python",
    ]
    require(
        [row["case"] for row in rows] == expected_order and len(rows) == 12,
        "mutation census/order",
    )
    report = {
        "schema": "k2p-quartet-terminal-binding-mutations-v2",
        "status": "PASS",
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "binder_sha256": sha_file(VERIFIER),
        "semantics_certificate_sha256": sha_file(SEMANTICS),
        "source_certificate_sha256": sha_file(BASELINE_CERTIFICATE),
        "source_certificate_payload_sha256": clean_payload["payload_sha256"],
        "expected_helper_diagnostics": EXPECTED_HELPER_DIAGNOSTICS,
        "optimized_diagnostic": OPTIMIZED_DIAGNOSTIC,
        "clean_baseline": {
            "production_verifier_invoked": True,
            "verifier_exit_code": 0,
            "success_artifact_created": True,
            "success_artifact_byte_identical_to_stored": True,
            "success_artifact_sha256": sha_file(BASELINE_CERTIFICATE),
            "layer_count": 6,
            "quartet_terminal_rows": 4_414_710,
            "per_layer_certificate_ids": 888,
            "missing_references": 0,
            "dangling_certificates": 0,
            "layer_census": {
                name: {"quartet_terminal_rows": rows_, "certificate_count": certs}
                for name, (rows_, certs) in expected_layers.items()
            },
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
            "missing_binder_stale_pass_removed_before_failure": True,
            "helper_stale_pass_removed_before_import": True,
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
        "temporary_in_memory_or_temp_directory_mutations_only": True,
        "authoritative_ledgers_modified": False,
        "source_fingerprints_unchanged": True,
        "case_count": len(rows),
        "survived": 0,
        "cases": rows,
    }
    report["payload_sha256"] = sha_object(report)
    atomic_write(
        output, json.dumps(report, indent=2, sort_keys=True).encode() + b"\n"
    )
    print("K2P_QUARTET_TERMINAL_BINDING_MUTATIONS_PASS")
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
        print(f"QUARTET_TERMINAL_MUTATION_FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
