#!/usr/bin/env python3
"""Clean-room and hostile probes for the frozen k=4 production runner.

This script never edits the author files and never launches the order-12
solver instance.  Its only real proof job is a two-variable UNSAT formula.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))
sys.path.insert(0, str(CAMPAIGN))

from search.k4_production import runner as production  # noqa: E402
from tests.test_k4_production import (  # noqa: E402
    FakeProofPipeline,
    PARENT,
    PARENT_MANIFEST,
    patched_production_environment,
)


FROZEN = {
    "math/lemmas/order12_k4_partition_plan.md":
        "132a1d41c11466b7f4af641049dd7ff10c4622f055d315831254da9978ee1578",
    "src/search/k4_production/__init__.py":
        "d217fa6af4e7273a80cc63ee8ac812e83b6ce8ed64585fef6d2ef8a371dd2c67",
    "src/search/k4_production/__main__.py":
        "a5d3245ca5614aa7b566a1a182d03b48fbc3c40c3ade4d56d9d8114b5dcb432d",
    "src/search/k4_production/runner.py":
        "4e65bc62df18e9bd3a7b17810da00f472a1afda21c6d87c1f13a0d06dba635af",
    "tests/test_k4_production.py":
        "bc386ad5d3759a67eaf735b396ef9461001a403843410f3c1de8d625ffa0ad2a",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def expect_error(action) -> str:
    try:
        action()
    except BaseException as error:
        return type(error).__name__
    raise AssertionError("hostile mutation was unexpectedly accepted")


def parse_dimacs_clean(payload: bytes) -> tuple[int, tuple[tuple[int, ...], ...]]:
    text = payload.decode("ascii")
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("noncanonical line endings")
    lines = text.splitlines()
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise ValueError("bad DIMACS header")
    variables, declared = map(int, header[2:])
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        tokens = tuple(map(int, line.split()))
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise ValueError("bad clause terminator")
        clause = tokens[:-1]
        if any(literal == 0 or abs(literal) > variables for literal in clause):
            raise ValueError("bad literal")
        clauses.append(clause)
    if len(clauses) != declared:
        raise ValueError("clause count mismatch")
    return variables, tuple(clauses)


def clean_partition_probe() -> dict[str, object]:
    parent = PARENT.read_bytes()
    if digest(PARENT) != production.EXPECTED_PARENT_CNF_SHA256:
        raise AssertionError("parent hash changed")
    variables, parent_clauses = parse_dimacs_clean(parent)
    if (
        variables != 18_381
        or len(parent_clauses) != 114_742
        or sum(map(len, parent_clauses)) != 1_180_016
    ):
        raise AssertionError("parent census changed")

    edge_layout = {
        pair: index
        for index, pair in enumerate(combinations(range(12), 2), start=1)
    }
    selected_pairs = ((0, 4), (1, 4), (2, 4), (3, 4))
    selected_variables = tuple(edge_layout[pair] for pair in selected_pairs)
    if selected_variables != (4, 14, 23, 31):
        raise AssertionError("independent edge layout differs")

    first_newline = parent.index(b"\n")
    body = parent[first_newline + 1 :]
    leaves: list[dict[str, object]] = []
    cubes: list[tuple[int, ...]] = []
    for index, bits in enumerate(product((0, 1), repeat=4)):
        literals = tuple(
            variable if bit else -variable
            for variable, bit in zip(selected_variables, bits, strict=True)
        )
        leaf = (
            b"p cnf 18381 114746\n"
            + body
            + b"".join(f"{literal} 0\n".encode("ascii") for literal in literals)
        )
        leaf_variables, clauses = parse_dimacs_clean(leaf)
        if (
            leaf_variables != variables
            or clauses[:-4] != parent_clauses
            or clauses[-4:] != tuple((literal,) for literal in literals)
            or len(clauses) != 114_746
            or sum(map(len, clauses)) != 1_180_020
        ):
            raise AssertionError("clean-room leaf construction differs")
        cubes.append(literals)
        leaves.append(
            {
                "case_id": "".join(map(str, bits)),
                "case_index": index,
                "cube_literals": list(literals),
                "cnf_sha256": sha256(leaf).hexdigest(),
                "cnf_size_bytes": len(leaf),
            }
        )

    assignment_hits: dict[str, int] = {}
    for assignment in product((False, True), repeat=4):
        hits = sum(
            all(
                assignment[selected_variables.index(abs(literal))]
                == (literal > 0)
                for literal in cube
            )
            for cube in cubes
        )
        assignment_hits["".join("1" if bit else "0" for bit in assignment)] = hits
    if set(assignment_hits.values()) != {1}:
        raise AssertionError("Boolean coverage is not exact")
    if len({record["cnf_sha256"] for record in leaves}) != 16:
        raise AssertionError("leaf hashes are not unique")
    return {
        "parent_sha256": digest(PARENT),
        "parent_census": [variables, len(parent_clauses), sum(map(len, parent_clauses))],
        "edge_layout": {
            f"e_{pair[0]}_{pair[1]}": variable
            for pair, variable in zip(
                selected_pairs,
                selected_variables,
                strict=True,
            )
        },
        "assignment_hit_histogram": {"1": 16},
        "leaves": leaves,
    }


def author_partition_mutations() -> dict[str, str]:
    parent = PARENT.read_bytes()
    baseline = production._partition_payload(parent, 0)
    production._validate_partition(baseline, parent)
    mutations: dict[str, str] = {}

    dropped = deepcopy(baseline)
    dropped["cases"] = dropped["cases"][:-1]
    mutations["drop_case"] = expect_error(
        lambda: production._validate_partition(dropped, parent)
    )

    duplicate = deepcopy(baseline)
    duplicate["cases"][1]["cube_bits"] = duplicate["cases"][0]["cube_bits"]
    mutations["duplicate_cube"] = expect_error(
        lambda: production._validate_partition(duplicate, parent)
    )

    wrong_literal = deepcopy(baseline)
    wrong_literal["cases"][0]["cube_literals"][0] *= -1
    mutations["flip_cube_literal"] = expect_error(
        lambda: production._validate_partition(wrong_literal, parent)
    )

    wrong_hash = deepcopy(baseline)
    wrong_hash["cases"][0]["cnf_sha256"] = "0" * 64
    mutations["replace_leaf_hash"] = expect_error(
        lambda: production._validate_partition(wrong_hash, parent)
    )
    return mutations


def strict_output_mutations() -> dict[str, str]:
    production._strict_converter_success(
        b"c forward verification\ns VERIFIED\n",
        b"",
    )
    production._strict_lrat_success(b"c VERIFIED\n", b"")
    return {
        "converter_warning": expect_error(
            lambda: production._strict_converter_success(
                b"s VERIFIED\nc WARNING injected\n",
                b"",
            )
        ),
        "converter_duplicate": expect_error(
            lambda: production._strict_converter_success(
                b"s VERIFIED\ns VERIFIED\n",
                b"",
            )
        ),
        "converter_stderr": expect_error(
            lambda: production._strict_converter_success(
                b"s VERIFIED\n",
                b"noise",
            )
        ),
        "lrat_not_verified": expect_error(
            lambda: production._strict_lrat_success(
                b"c VERIFIED\nc NOT VERIFIED\n",
                b"",
            )
        ),
        "lrat_duplicate": expect_error(
            lambda: production._strict_lrat_success(
                b"c VERIFIED\nc VERIFIED\n",
                b"",
            )
        ),
        "lrat_stderr": expect_error(
            lambda: production._strict_lrat_success(
                b"c VERIFIED\n",
                b"noise",
            )
        ),
    }


def sat_and_aggregation_probe() -> dict[str, object]:
    cnf = b"p cnf 2 2\n1 0\n-1 2 0\n"
    status, candidate = production.classify_solver_result(
        cnf,
        b"s SATISFIABLE\nv 1 2 0\n",
    )
    if status != "SAT" or candidate is None:
        raise AssertionError("valid SAT model was not retained")
    mutations = {
        "incomplete_model": expect_error(
            lambda: production.classify_solver_result(
                cnf,
                b"s SATISFIABLE\nv 1 0\n",
            )
        ),
        "falsifying_model": expect_error(
            lambda: production.classify_solver_result(
                cnf,
                b"s SATISFIABLE\nv 1 -2 0\n",
            )
        ),
        "duplicate_status": expect_error(
            lambda: production.classify_solver_result(
                cnf,
                b"s SATISFIABLE\ns SATISFIABLE\nv 1 2 0\n",
            )
        ),
    }
    all_unsat = [
        {"status": "UNSAT_LRAT_VERIFIED"} for _ in range(16)
    ]
    sat_hold = list(all_unsat)
    sat_hold[7] = {
        "status": "SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION"
    }
    if production._summary_for_cases(all_unsat) != (
        "ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT"
    ):
        raise AssertionError("all-UNSAT aggregation is wrong")
    if production._summary_for_cases(sat_hold) != "SAT_CANDIDATE_HOLD_NONCLAIM":
        raise AssertionError("SAT hold does not dominate aggregation")
    return {
        "valid_sat_assignment_sha256": candidate["assignment_sha256"],
        "mutations": mutations,
        "all_unsat_status": production._summary_for_cases(all_unsat),
        "sat_hold_status": production._summary_for_cases(sat_hold),
    }


def run_tool(command: tuple[str, ...], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        env={},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )


def tiny_real_pipeline() -> dict[str, object]:
    tools = {
        "cadical": {
            "path": str(
                (CAMPAIGN / "tools/cadical_3_0_1/build/cadical").resolve()
            )
        },
        "drat_trim": {
            "path": str(
                (
                    CAMPAIGN
                    / "tools/drat_trim_2023_05_22/drat-trim"
                ).resolve()
            )
        },
        "lrat_check": {
            "path": str(
                (
                    CAMPAIGN
                    / "tools/drat_trim_2023_05_22/lrat-check"
                ).resolve()
            )
        },
    }
    manifest = {
        "tools": tools,
        "limits": {
            "solver_wall_seconds": 10,
            "converter_wall_seconds": 10,
        },
    }
    with tempfile.TemporaryDirectory() as temporary:
        attempt = Path(temporary).resolve()
        # This formula has no initial unit clauses; an empty proof is not
        # enough.  Its four clauses exclude all assignments to two variables.
        cnf = (
            b"p cnf 2 4\n"
            b"1 2 0\n"
            b"1 -2 0\n"
            b"-1 2 0\n"
            b"-1 -2 0\n"
        )
        (attempt / "instance.cnf").write_bytes(cnf)
        case = {"seed": 7}
        solver_command = production._solver_command(manifest, case, attempt)
        raw_forward_command = production._raw_forward_command(
            manifest, attempt
        )
        conversion_command = production._lrat_conversion_command(
            manifest, attempt
        )
        checker_command = production._lrat_check_command(manifest, attempt)

        solver = run_tool(solver_command, CAMPAIGN)
        if solver.returncode != 20:
            raise AssertionError(f"tiny CaDiCaL exit code {solver.returncode}")
        result = (attempt / "solver.result").read_bytes()
        proof = (attempt / "proof.raw.bdrat").read_bytes()
        parsed, candidate = production.classify_solver_result(cnf, result)
        if parsed != "UNSAT" or candidate is not None or not proof:
            raise AssertionError("tiny solver result/proof differs")

        raw_forward = run_tool(raw_forward_command, CAMPAIGN)
        production._strict_converter_success(
            raw_forward.stdout,
            raw_forward.stderr,
        )
        if raw_forward.returncode != 0:
            raise AssertionError("tiny raw forward replay returned nonzero")
        if "-f" not in raw_forward_command or "-L" in raw_forward_command:
            raise AssertionError("raw forward flags are not separated")

        conversion = run_tool(conversion_command, CAMPAIGN)
        production._strict_converter_success(
            conversion.stdout,
            conversion.stderr,
        )
        if conversion.returncode != 0:
            raise AssertionError("tiny backward conversion returned nonzero")
        if "-f" in conversion_command or "-L" not in conversion_command:
            raise AssertionError("backward conversion flags are not separated")
        lrat_path = attempt / "proof.converted.lrat"
        lrat = lrat_path.read_bytes()
        if not lrat:
            raise AssertionError("tiny LRAT is empty")

        checker = run_tool(checker_command, CAMPAIGN)
        production._strict_lrat_success(
            checker.stdout,
            checker.stderr,
        )
        if checker.returncode != 0:
            raise AssertionError("tiny LRAT replay returned nonzero")

        lines = lrat.splitlines(keepends=True)
        if len(lines) < 1:
            raise AssertionError("tiny LRAT has no line")
        truncated_path = attempt / "proof.truncated.lrat"
        truncated_path.write_bytes(b"".join(lines[:-1]))
        truncated = run_tool(
            (
                tools["lrat_check"]["path"],
                str((attempt / "instance.cnf").resolve()),
                str(truncated_path.resolve()),
            ),
            CAMPAIGN,
        )
        truncated_rejected = (
            truncated.returncode != 0
            and b"c NOT VERIFIED" in truncated.stdout
        )
        if not truncated_rejected:
            raise AssertionError("truncated LRAT was not rejected")

        empty_proof = attempt / "proof.empty.bdrat"
        empty_proof.write_bytes(b"")
        empty_lrat = attempt / "proof.empty.lrat"
        empty_conversion = run_tool(
            (
                tools["drat_trim"]["path"],
                str((attempt / "instance.cnf").resolve()),
                str(empty_proof.resolve()),
                "-i",
                "-W",
                "-L",
                str(empty_lrat.resolve()),
                "-t",
                "10",
            ),
            CAMPAIGN,
        )
        empty_rejected = not (
            empty_conversion.returncode == 0
            and empty_conversion.stdout.count(b"s VERIFIED") == 1
        )
        if not empty_rejected:
            raise AssertionError("empty binary proof was accepted")

        legacy_lrat = attempt / "proof.legacy-forward.lrat"
        legacy_conversion = run_tool(
            (
                tools["drat_trim"]["path"],
                str((attempt / "instance.cnf").resolve()),
                str((attempt / "proof.raw.bdrat").resolve()),
                "-i",
                "-f",
                "-W",
                "-L",
                str(legacy_lrat.resolve()),
                "-t",
                "10",
            ),
            CAMPAIGN,
        )
        production._strict_converter_success(
            legacy_conversion.stdout,
            legacy_conversion.stderr,
        )
        legacy_check = run_tool(
            (
                tools["lrat_check"]["path"],
                str((attempt / "instance.cnf").resolve()),
                str(legacy_lrat.resolve()),
            ),
            CAMPAIGN,
        )
        legacy_rejected = (
            legacy_check.returncode != 0
            and b"c NOT VERIFIED" in legacy_check.stdout
        )
        if not legacy_rejected:
            raise AssertionError("legacy combined -f/-L regression disappeared")

        return {
            "commands": {
                "solver": list(solver_command),
                "raw_forward": list(raw_forward_command),
                "lrat_conversion": list(conversion_command),
                "lrat_check": list(checker_command),
            },
            "exit_codes": {
                "solver": solver.returncode,
                "raw_forward": raw_forward.returncode,
                "lrat_conversion": conversion.returncode,
                "lrat_check": checker.returncode,
            },
            "artifact_hashes": {
                "cnf": sha256(cnf).hexdigest(),
                "solver_result": sha256(result).hexdigest(),
                "binary_drat": sha256(proof).hexdigest(),
                "lrat": sha256(lrat).hexdigest(),
            },
            "artifact_sizes": {
                "cnf": len(cnf),
                "solver_result": len(result),
                "binary_drat": len(proof),
                "lrat": len(lrat),
            },
            "four_phase_chain_verified": True,
            "legacy_combined_forward_lrat_rejected": legacy_rejected,
            "truncated_lrat_rejected": truncated_rejected,
            "empty_binary_drat_rejected": empty_rejected,
        }


def initialize_fake_run(directory: Path) -> Path:
    run = directory / "run"
    with patched_production_environment():
        production.initialize_run(
            run_directory=run,
            parent_cnf=PARENT,
            parent_manifest=PARENT_MANIFEST,
            solver_wall_seconds=10,
            converter_wall_seconds=10,
            checker_wall_seconds=10,
            solver_memory_mib=64,
            postprocess_memory_mib=64,
            file_limit_mib=16,
            disk_reserve_mib=4096,
            memory_reserve_mib=512,
            load_max=1000.0,
            validation_gate_open=True,
        )
    return run


def binding_and_provenance_probe() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as temporary:
        temporary_root = Path(temporary).resolve()
        bound_path = temporary_root / "bound.bin"
        bound_path.write_bytes(b"alpha")
        binding = production._file_binding(bound_path, "hostile probe")
        bound_path.write_bytes(b"bravo")
        file_tamper = expect_error(
            lambda: production._verify_file_binding(
                binding,
                "hostile probe",
            )
        )

    tool_bindings = production._tool_bindings()
    bad_tools = deepcopy(tool_bindings)
    bad_tools["cadical"]["sha256"] = "0" * 64
    tool_record_tamper = expect_error(
        lambda: production._verify_tool_bindings(bad_tools)
    )

    with tempfile.TemporaryDirectory() as temporary:
        run = initialize_fake_run(Path(temporary).resolve())
        public_injection = expect_error(
            lambda: production.run_next_case(
                run,
                production_gate_open=True,
                child_runner=FakeProofPipeline(),
            )
        )
        fake = FakeProofPipeline()
        with patched_production_environment(child_runner=fake):
            completed = production.run_next_case(
                run,
                production_gate_open=True,
            )
            accepted_audit = production.audit_run(run)
        attempt = run / "cases/case-0000/attempt-000001"
        lrat_path = attempt / "proof.converted.lrat"
        original_lrat = lrat_path.read_bytes()
        lrat_path.write_bytes(
            bytes([original_lrat[0] ^ 1]) + original_lrat[1:]
        )
        with patched_production_environment():
            completed_artifact_tamper = expect_error(
                lambda: production.audit_run(run)
            )

    with tempfile.TemporaryDirectory() as temporary:
        run = initialize_fake_run(Path(temporary).resolve())
        with patched_production_environment(
            child_runner=FakeProofPipeline("interrupt")
        ):
            try:
                production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            except KeyboardInterrupt:
                pass
            else:
                raise AssertionError("injected interruption did not occur")
        config_path = (
            run
            / "cases/case-0000/attempt-000001/attempt-config.json"
        )
        config = production._strict_json_file(config_path)
        if not isinstance(config, dict):
            raise AssertionError("active attempt config is malformed")
        original_config_hash = digest(config_path)
        raw_forward_command = config.get("raw_forward_command")
        if not isinstance(raw_forward_command, list) or not raw_forward_command:
            raise AssertionError("active raw-forward command is malformed")
        raw_forward_command[0] = "/hostile/not-the-pinned-converter"
        config_path.write_bytes(production.canonical_json_bytes(config))
        tampered_config_hash = digest(config_path)
        with patched_production_environment():
            active_tamper_audit = expect_error(
                lambda: production.audit_run(run)
            )
            with patch.object(
                production,
                "_commands_containing",
                return_value=[],
            ):
                recovery_after_tamper = expect_error(
                    lambda: production.recover_interrupted_attempt(
                        run,
                        recovery_gate_open=True,
                    )
                )
        if original_config_hash == tampered_config_hash:
            raise AssertionError("active config mutation did not change hash")

    return {
        "direct_file_hash_tamper": file_tamper,
        "tool_record_hash_tamper": tool_record_tamper,
        "completed_lrat_tamper": completed_artifact_tamper,
        "public_child_runner_injection": public_injection,
        "mocked_internal_leaf_status": completed["status"],
        "mocked_internal_leaf_audit_status": accepted_audit["status"],
        "active_attempt_config_tamper_audit": active_tamper_audit,
        "active_attempt_config_hashes": {
            "before": original_config_hash,
            "after": tampered_config_hash,
        },
        "recovery_after_config_tamper": recovery_after_tamper,
    }


def crash_window_probe() -> dict[str, object]:
    results: dict[str, object] = {}
    with tempfile.TemporaryDirectory() as temporary:
        run = initialize_fake_run(Path(temporary).resolve())
        fake = FakeProofPipeline()
        with patched_production_environment(
            child_runner=fake
        ), patch.object(
            production,
            "_append_checkpoint_transition",
            side_effect=RuntimeError("injected before reservation"),
        ):
            first_error = expect_error(
                lambda: production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            )
        with patched_production_environment():
            audit_error = expect_error(lambda: production.audit_run(run))
            with patch.object(
                production,
                "_commands_containing",
                return_value=[],
            ):
                recovery = production.recover_interrupted_attempt(
                    run, recovery_gate_open=True
                )
            final_audit = production.audit_run(run)
        results["orphan_attempt_before_reservation"] = {
            "run_error": first_error,
            "pre_recovery_audit": audit_error,
            "recovery_status": recovery["status"],
            "reconciliation_mode": recovery["reconciliation_mode"],
            "post_recovery_audit": final_audit["status"],
            "attempt_directory_exists": (
                run / "cases/case-0000/attempt-000001"
            ).is_dir(),
            "latest_checkpoint_sequence": (
                final_audit["latest_checkpoint_sequence"]
            ),
        }

    with tempfile.TemporaryDirectory() as temporary:
        run = initialize_fake_run(Path(temporary).resolve())
        original = production._append_checkpoint_transition
        calls = 0

        def fail_second(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("injected after durable outcome")
            return original(*args, **kwargs)

        fake = FakeProofPipeline()
        with patched_production_environment(
            child_runner=fake
        ), patch.object(
            production,
            "_append_checkpoint_transition",
            side_effect=fail_second,
        ):
            run_error = expect_error(
                lambda: production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            )
        attempt = run / "cases/case-0000/attempt-000001"
        with patched_production_environment():
            audit_error = expect_error(lambda: production.audit_run(run))
            with patch.object(
                production,
                "_commands_containing",
                return_value=[],
            ):
                recovery = production.recover_interrupted_attempt(
                    run, recovery_gate_open=True
                )
            final_audit = production.audit_run(run)
        results["outcome_before_completion_checkpoint"] = {
            "run_error": run_error,
            "pre_recovery_audit": audit_error,
            "recovery_status": recovery["status"],
            "reconciliation_mode": recovery["reconciliation_mode"],
            "post_recovery_audit": final_audit["status"],
            "outcome_exists": (attempt / "outcome.json").is_file(),
            "latest_checkpoint_sequence": (
                final_audit["latest_checkpoint_sequence"]
            ),
        }
    return results


def main() -> int:
    observed = {
        relative: digest(CAMPAIGN / relative)
        for relative in FROZEN
    }
    if observed != FROZEN:
        raise AssertionError(
            f"author files changed during review: {observed!r}"
        )
    report = {
        "schema": "order12-k4-production-hostile-probe-v2",
        "author_hashes": observed,
        "clean_room_partition": clean_partition_probe(),
        "author_partition_mutations": author_partition_mutations(),
        "strict_output_mutations": strict_output_mutations(),
        "sat_and_aggregation": sat_and_aggregation_probe(),
        "binding_and_provenance": binding_and_provenance_probe(),
        "tiny_real_unsat_pipeline": tiny_real_pipeline(),
        "crash_windows": crash_window_probe(),
        "verdict_signal": "ACCEPT_PRODUCTION_READY_ENGINEERING",
    }
    encoded = (
        json.dumps(report, allow_nan=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    sys.stdout.buffer.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
