#!/usr/bin/env python3
"""Independent hostile replay for the deletion-agnostic RUP repair.

The preserved v1-v3 referee modules are imported only for their synthetic
fixtures and already-established hostile cases.  Their main routines are not
called and their artifacts are never changed.  This script launches the pinned
DRAT checker on the frozen attempt-1 bytes and on tiny hostile fixtures, but it
never launches a SAT solver or mutates the live production tree.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from unittest.mock import patch


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
sys.path.insert(0, str(REVIEW))
sys.path.insert(0, str(CAMPAIGN / "src"))

import referee_regressions_v3 as prior3  # noqa: E402

from search.order13_k3.normalize_bdrat import (  # noqa: E402
    NormalizationError,
    normalize_binary_drat,
)


base = prior3.base
prior2 = prior3.prior
production = prior3.production

LIVE = CAMPAIGN / "results/order13_k3_hole9_production"
LIVE_ATTEMPT = LIVE / "attempts/attempt-000001"
DRAT = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
DRAT_SOURCE = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim.c"

PIPELINE_V2 = (
    "raw-binary-drat-plain-rup-forward-normalize-rup-forward-"
    "backward-lrat-replay-v2"
)
PIPELINE_V1 = (
    "raw-binary-drat-forward-normalize-rup-forward-backward-lrat-replay-v1"
)

FINAL_FROZEN = {
    "src/search/order13_k3/production.py": (
        "7223e9c789b50aa021371f07670af9ee1a2406fd649e1d84713ed4b566a7f11e"
    ),
    "src/search/order13_k3/normalize_bdrat.py": (
        "a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c"
    ),
    "src/search/order13_k3/PRODUCTION_PROTOCOL.md": (
        "cec85e105e1372dc09de055f2b74bc80709b1a732c64541869c8106b6f2316a9"
    ),
    "tests/test_order13_k3_production.py": (
        "51655e8764db2ad436e84041a8b81e83e07131bfdd88084158d6b8800052cc0a"
    ),
}

PRESERVED_HISTORY = {
    "REVIEW.md": "81773a5295046a7e37eaf16897edfe710aff7f1ae873402cda64da9d5e32131f",
    "evidence.json": "3d849ca9493dba7786a899ce9a0cf7c35101b7f342d531103cbc65c510db29fe",
    "referee_regressions.py": (
        "5681a4672abf882b408de287ef781b72063915d31e6d068cef143face119e1f8"
    ),
    "run_readonly_upstream_tests.py": (
        "713ec705aa77aa7f316ef7357473d7466fd00fdd82f84aff799fbc97f882b022"
    ),
    "RESEARCH_LOG.md": (
        "6c02761363fe8420b300f4f0c8764d478c93df9c85398684be6d22bf8b21647b"
    ),
    "ADDENDUM.md": "9c450c0a37e96d191bf5e9534babd418da44e0a76133bad7e3ba4dab80993f17",
    "evidence_v2.json": (
        "f9e1ad4fcc5e7ddaa8c446a7b28527622b0f78d790d2b15746668462400d489b"
    ),
    "referee_regressions_v2.py": (
        "aa69db3f287fea20fa9de426e406c8843f47abd65a94fa09966bd6333e841fa7"
    ),
    "run_readonly_upstream_tests_v2.py": (
        "07029364acff8acca83918841db82ad66951e419e93c2e3fee609b23b3a90bc4"
    ),
    "RESEARCH_LOG_V2.md": (
        "5c91df7c1ee62b96291682fc850012dfbe6b7632aa1f42c7bc512417e3626d19"
    ),
    "ADDENDUM_V3.md": (
        "8881c11b23302f8ae19e8913ead2588fbfdea054bd1585b887f9d96a89a2c9c0"
    ),
    "evidence_v3.json": (
        "7e86ee0692125e6782e4a9e7c5ff673f6a0dc92bdb73cae52aa7f8329b75a23f"
    ),
    "referee_regressions_v3.py": (
        "6b906927eb38736d19db3bc05c8320611940379c579f62501abf70aa1f52f0f7"
    ),
    "run_readonly_upstream_tests_v3.py": (
        "0ba5734313b739670a75fb279cfa2f03f27346e399fb8230566c6fd720db0f2e"
    ),
    "RESEARCH_LOG_V3.md": (
        "21a8917210ddc1e2ffb6b8a6565481dc7d2463a35927c0c781f8ec1d90ab05b5"
    ),
}

PINNED_TOOLS = {
    "drat-trim": "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
    "drat-trim.c": "f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26",
    "lrat-check": "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
}

LIVE_CRITICAL = {
    "run-manifest.json": "40fe9e77e4da79e8b70f3d3f836d3a595e1d3b8bae25c4c607a2e1f63dc4be54",
    "checkpoints/checkpoint-000000.json": (
        "106afa51de8197303dbd762a4d234dd0a5bb32b687bb5d655848687f5027358e"
    ),
    "checkpoints/checkpoint-000001.json": (
        "599cf1c52c9cc41f49e708d215bc31fe0ab5253cabd420915a35e9e30672f696"
    ),
    "checkpoints/checkpoint-000002.json": (
        "be3aa0a50f31a61ba7655c5795f21b4e88468eacd348183ada2f2a6e38c368d4"
    ),
    "attempts/attempt-000001/attempt-config.json": (
        "980c8819492c87e97abfbed6e35979e46b7bb5ea692eebc3df38b393ca98dc18"
    ),
    "attempts/attempt-000001/child-raw_forward.json": (
        "af42968bf8dd572a0a0c4509e781a6f6e2a0167ef700fd2d1a8320190f7098e3"
    ),
    "attempts/attempt-000001/outcome.json": (
        "aa943916e4bb3e46cc2dd2d00f0593f959ad52e45c14202c497f968cd0ab915f"
    ),
    "attempts/attempt-000001/proof.raw.bdrat": (
        "ecfb35ba56b5ce2a04437f381e357525581f3bcb6403290272984700d805dbeb"
    ),
    "attempts/attempt-000001/raw_forward.stdout": (
        "515b864b194cc4ca1c08394da049b2eaf15df48b3af0bc320d254edfcf795058"
    ),
    "attempts/attempt-000001/raw_forward.stderr": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ),
}


def sha256(path: Path) -> str:
    return base.sha256(path)


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, allow_nan=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return prior3.read_json(path)


def verify_bound_bytes() -> tuple[dict[str, str], dict[str, str]]:
    frozen = {
        relative: sha256(CAMPAIGN / relative)
        for relative in FINAL_FROZEN
    }
    preserved = {
        name: sha256(REVIEW / name)
        for name in PRESERVED_HISTORY
    }
    tools = {
        "drat-trim": sha256(DRAT),
        "drat-trim.c": sha256(DRAT_SOURCE),
        "lrat-check": sha256(
            CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
        ),
    }
    live = {
        relative: sha256(LIVE / relative)
        for relative in LIVE_CRITICAL
    }
    if frozen != FINAL_FROZEN:
        raise AssertionError("v4 frozen implementation bytes changed")
    if preserved != PRESERVED_HISTORY:
        raise AssertionError("a preserved v1-v3 referee artifact changed")
    if tools != PINNED_TOOLS:
        raise AssertionError("pinned checker bytes changed")
    if live != LIVE_CRITICAL:
        raise AssertionError("frozen live attempt bytes changed")
    return frozen, preserved


def _clean_marker(stdout: bytes, marker: bytes) -> bool:
    lines = [
        line.strip()
        for line in stdout.replace(b"\r", b"\n").splitlines()
        if line.strip()
    ]
    lowered = b"\n".join(lines).lower()
    return (
        lines.count(marker) == 1
        and b"warning" not in lowered
        and b"error" not in lowered
        and b"not verified" not in lowered
    )


def _semantic_stdout_digest(stdout: bytes) -> str:
    lines = [
        line.strip()
        for line in stdout.replace(b"\r", b"\n").splitlines()
        if line.strip()
    ]
    stable = [
        line
        for line in lines
        if not line.lower().startswith(b"c verification time:")
    ]
    return hashlib.sha256(b"\n".join(stable) + b"\n").hexdigest()


def _run(command: Sequence[str], timeout: int = 60) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        list(command),
        cwd=CAMPAIGN,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def _encode_unsigned(value: int) -> bytes:
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        result.append(byte | (0x80 if value else 0))
        if not value:
            return bytes(result)


def _record(prefix: bytes, clause: Iterable[int]) -> bytes:
    payload = bytearray(prefix)
    for literal in clause:
        encoded = 2 * abs(literal) + (1 if literal < 0 else 0)
        payload.extend(_encode_unsigned(encoded))
    payload.append(0)
    return bytes(payload)


def _tiny_command(cnf: Path, proof: Path, *, plain: bool = True) -> list[str]:
    flags = ["-i", "-f"]
    if plain:
        flags.append("-p")
    flags.extend(["-W", "-U", "-t", "30"])
    return [str(DRAT), str(cnf), str(proof), *flags]


def case_real_checker() -> dict[str, object]:
    instance = LIVE_ATTEMPT / production.INSTANCE_NAME
    raw = LIVE_ATTEMPT / "proof.raw.bdrat"
    command = [
        str(DRAT),
        str(instance),
        str(raw),
        "-i",
        "-f",
        "-p",
        "-W",
        "-U",
        "-t",
        "1800",
    ]
    completed = _run(command)
    if (
        completed.returncode != 0
        or completed.stderr
        or not _clean_marker(completed.stdout, b"s VERIFIED")
        or b"0 RAT lemmas in core" not in completed.stdout
    ):
        raise AssertionError("exact frozen raw proof failed the v4 checker gate")

    with tempfile.TemporaryDirectory(prefix="referee-v4-checker-") as temporary:
        root = Path(temporary)
        sat_cnf = root / "sat.cnf"
        sat_cnf.write_bytes(b"p cnf 2 1\n1 0\n")
        rat_only = root / "rat-only.bdrat"
        rat_only.write_bytes(_record(b"a", (2,)))
        rejected_rup = _run(_tiny_command(sat_cnf, rat_only))
        if (
            rejected_rup.returncode == 0
            or b"RUP check failed" not in rejected_rup.stdout
            or b"s VERIFIED" in rejected_rup.stdout
            or rejected_rup.stderr
        ):
            raise AssertionError("-U did not reject a RAT-only addition")

        xor_cnf = root / "xor.cnf"
        xor_cnf.write_bytes(
            b"p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n"
        )
        deletion_noise = root / "deletion-noise.bdrat"
        deletion_noise.write_bytes(
            _record(b"d", (2,)) + _record(b"a", (1,))
        )
        plain = _run(_tiny_command(xor_cnf, deletion_noise, plain=True))
        deletion_aware = _run(
            _tiny_command(xor_cnf, deletion_noise, plain=False)
        )
        if (
            plain.returncode != 0
            or plain.stderr
            or not _clean_marker(plain.stdout, b"s VERIFIED")
            or deletion_aware.returncode != 80
            or b"deleted clause" not in deletion_aware.stdout
        ):
            raise AssertionError("plain-mode deletion isolation differs")

        up_unsat = root / "up-unsat.cnf"
        up_unsat.write_bytes(b"p cnf 2 3\n1 0\n-1 2 0\n-2 0\n")
        warning_then_valid = root / "warning-then-valid.bdrat"
        warning_then_valid.write_bytes(_record(b"a", ()) + b"x")
        warning = _run(_tiny_command(up_unsat, warning_then_valid))
        stdout_path = root / "warning.stdout"
        stderr_path = root / "warning.stderr"
        stdout_path.write_bytes(warning.stdout)
        stderr_path.write_bytes(warning.stderr)
        strict_rejected = False
        try:
            production._strict_verified(
                stdout_path, stderr_path, "s VERIFIED"
            )
        except ValueError:
            strict_rejected = True
        normalized = root / "warning.normalized.bdrat"
        report = root / "warning-normalization.json"
        normalizer_rejected = False
        try:
            normalize_binary_drat(
                warning_then_valid,
                normalized,
                report,
                max_variable=2,
            )
        except NormalizationError:
            normalizer_rejected = True
        if (
            warning.returncode != 0
            or b"WARNING: wrong binary prefix" not in warning.stdout
            or b"s VERIFIED" not in warning.stdout
            or not strict_rejected
            or not normalizer_rejected
            or normalized.exists()
            or report.exists()
        ):
            raise AssertionError("nonfatal checker warning was not fail-closed")

    return {
        "exact_command": command,
        "instance_sha256": sha256(instance),
        "raw_proof_sha256": sha256(raw),
        "raw_proof_size_bytes": raw.stat().st_size,
        "exit_code": completed.returncode,
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        "stdout_semantic_sha256": _semantic_stdout_digest(
            completed.stdout
        ),
        "strict_verified_marker_count": 1,
        "zero_RAT_reported": True,
        "RAT_only_addition_rejected_by_U": True,
        "bogus_deletion_ignored_only_in_plain_mode": True,
        "nonfatal_W_warning_rejected_by_runner_and_normalizer": True,
        "real_drat_trim_execution_count": 5,
        "real_solver_execution_count": 0,
    }


Clause = tuple[int, ...]


def _models(formula: Sequence[Clause]) -> list[dict[int, bool]]:
    result: list[dict[int, bool]] = []
    for values in itertools.product((False, True), repeat=2):
        assignment = {1: values[0], 2: values[1]}
        if all(
            any(assignment[abs(lit)] == (lit > 0) for lit in clause)
            for clause in formula
        ):
            result.append(assignment)
    return result


def _unit_conflict(formula: Sequence[Clause], assumptions: Clause) -> bool:
    clauses = [tuple(clause) for clause in formula]
    clauses.extend((literal,) for literal in assumptions)
    assignment: dict[int, bool] = {}
    while True:
        changed = False
        for clause in clauses:
            if any(
                abs(lit) in assignment
                and assignment[abs(lit)] == (lit > 0)
                for lit in clause
            ):
                continue
            pending = [
                lit for lit in clause if abs(lit) not in assignment
            ]
            if not pending:
                return True
            if len(pending) == 1:
                literal = pending[0]
                variable = abs(literal)
                value = literal > 0
                if variable in assignment:
                    if assignment[variable] != value:
                        return True
                else:
                    assignment[variable] = value
                    changed = True
        if not changed:
            return False


def case_rup_soundness_exhaustive() -> dict[str, object]:
    clauses = tuple(
        tuple(
            literal
            for variable, sign in enumerate(signs, start=1)
            if sign
            for literal in (variable if sign > 0 else -variable,)
        )
        for signs in itertools.product((-1, 0, 1), repeat=2)
    )
    nonempty = tuple(clause for clause in clauses if clause)
    formula_count = 0
    pair_count = 0
    rup_pair_count = 0
    empty_rup_count = 0
    for mask in range(1 << len(nonempty)):
        formula = tuple(
            clause
            for index, clause in enumerate(nonempty)
            if mask & (1 << index)
        )
        formula_count += 1
        models = _models(formula)
        for clause in clauses:
            pair_count += 1
            rup = _unit_conflict(formula, tuple(-lit for lit in clause))
            if not rup:
                continue
            rup_pair_count += 1
            if any(
                not any(
                    model[abs(lit)] == (lit > 0) for lit in clause
                )
                for model in models
            ):
                raise AssertionError("RUP did not entail its added clause")
            if not clause:
                empty_rup_count += 1
                if models:
                    raise AssertionError("RUP empty clause had a model")
    return {
        "variables": 2,
        "non_tautological_clause_count": len(clauses),
        "formula_count": formula_count,
        "formula_clause_pairs_checked": pair_count,
        "RUP_pairs": rup_pair_count,
        "RUP_empty_formula_count": empty_rup_count,
        "counterexamples": 0,
        "induction": (
            "Each retained RUP clause is entailed by the original formula "
            "plus earlier retained RUP clauses, so adding it preserves the "
            "model set. Ignored deletions never enter that monotone sequence."
        ),
    }


def case_v4_command_binding(
    foundation: base.Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("v4-command-shape")
    manifest, _, _, _ = production._load_run(run_directory)
    command = production._commands(
        manifest, foundation.root / "fresh-attempt"
    )["raw_forward"]
    if (
        manifest["proof_pipeline"] != PIPELINE_V2
        or command[-7:] != ["-i", "-f", "-p", "-W", "-U", "-t", "2"]
        or any(command.count(flag) != 1 for flag in ("-p", "-W", "-U"))
    ):
        raise AssertionError("v4 command or pipeline identifier differs")

    mutations: dict[str, object] = {}
    for flag in ("-p", "-W", "-U"):
        changed, _ = prior2.new_success(
            foundation, f"v4-command-missing-{flag[1:]}"
        )
        attempt = changed / "attempts/attempt-000001"
        config_path = attempt / "attempt-config.json"
        config = read_json(config_path)
        commands = config["commands"]
        assert isinstance(commands, dict)
        raw_command = commands["raw_forward"]
        assert isinstance(raw_command, list)
        raw_command.remove(flag)
        prior3.write_json(config_path, config)
        prior2.refresh_terminal(changed, sync_certificate=True)
        mutations[flag] = prior3.expect_rejection(
            lambda changed=changed: base.audit_without_children(changed),
            "attempt configuration differs from frozen inputs",
        )

    old_live_rejection: dict[str, object]
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("v4 audit launched a child"),
    ) as child:
        old_live_rejection = prior3.expect_rejection(
            lambda: production.audit(LIVE),
            "run manifest semantics differ",
        )
    if child.call_count:
        raise AssertionError("v4 audit launched a child")

    return {
        "pipeline": manifest["proof_pipeline"],
        "raw_forward_suffix": command[-7:],
        "exact_flag_multiplicity": True,
        "coherently_rehashed_missing_flag_mutations": mutations,
        "old_v1_live_tree_refused_by_v4": old_live_rejection,
        "real_solver_or_checker_executions": 0,
    }


def case_live_nonclaim() -> dict[str, object]:
    manifest = read_json(LIVE / "run-manifest.json")
    checkpoint = read_json(
        LIVE / "checkpoints/checkpoint-000002.json"
    )
    outcome = read_json(LIVE_ATTEMPT / "outcome.json")
    raw_child = read_json(LIVE_ATTEMPT / "child-raw_forward.json")
    if (
        manifest.get("proof_pipeline") != PIPELINE_V1
        or checkpoint.get("status") != "RETRYABLE_NONCLAIM"
        or outcome.get("status") != "RETRYABLE_NONCLAIM"
        or outcome.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or not isinstance(outcome.get("details"), dict)
        or outcome["details"].get("phase_status")
        != "RAW_FORWARD_REJECTED_NONCLAIM"
        or raw_child.get("child", {}).get("exit_code") != 80
    ):
        raise AssertionError("live attempt is not the frozen v1 nonclaim")
    return {
        "manifest_pipeline": manifest["proof_pipeline"],
        "checkpoint_status": checkpoint["status"],
        "outcome_status": outcome["status"],
        "claim_status": outcome["claim_status"],
        "phase_status": outcome["details"]["phase_status"],
        "recorded_raw_forward_exit_code": raw_child["child"]["exit_code"],
        "critical_sha256": {
            relative: sha256(LIVE / relative)
            for relative in LIVE_CRITICAL
        },
    }


def replay_v1_v3_regressions(
    foundation: base.Foundation,
) -> tuple[dict[str, object], dict[str, object]]:
    checks = {
        "pre_RUN_STARTED_crash_windows": (
            prior3.case_pre_run_started_windows(foundation)
        ),
        "malformed_symlink_extra_orphans": (
            prior3.case_malformed_orphans(foundation)
        ),
        "opaque_orphan_contents": (
            prior3.case_opaque_orphan_contents(foundation)
        ),
        "pre_RUN_STARTED_orphan_after_RETRYABLE": (
            prior3.case_orphan_after_retryable(foundation)
        ),
        "partial_and_complete_opaque_outcomes": (
            prior3.case_opaque_outcomes(foundation)
        ),
        "crash_during_orphan_quarantine": (
            prior3.case_orphan_quarantine_crash_safety(foundation)
        ),
        "crash_during_quarantine": (
            prior3.case_quarantine_crash_safety(foundation)
        ),
        "positive_phase_records": prior2.case_positive_phase_records(
            foundation
        ),
        "readonly_complete_chain_audit": base.case_readonly_success(
            foundation
        ),
        "sat_candidate_semantic_replay": prior2.case_sat_semantic_replay(
            foundation
        ),
        "resource_limits_and_prelaunch_gate": base.case_resource_limits(
            foundation
        ),
        "runtime_source_binding": base.case_runtime_source_binding(
            foundation
        ),
        "binary_proof_normalization": base.case_normalization(foundation),
        "ordinary_interruption_recovery_and_fresh_restart": (
            base.case_recovery_and_restart(foundation)
        ),
        "malformed_metadata_v1_regressions": (
            base.case_v1_malformed_metadata_regressions(foundation)
        ),
        "adjacent_output_crosslink_matrix": (
            prior2.case_output_crosslink_matrix(foundation)
        ),
    }
    findings = {
        "F1_attempt_formula_content_equality": (
            prior2.case_f1_attempt_formula(foundation)
        ),
        "F2_phase_input_output_crosslinks": (
            prior2.case_f2_phase_crosslinks(foundation)
        ),
        "F3_exact_certificate_and_details_shape": (
            prior2.case_f3_exact_claim_shapes(foundation)
        ),
        "F4_all_adjacent_interruption_windows": {
            "pre_RUN_STARTED": checks["pre_RUN_STARTED_crash_windows"],
            "partial_and_complete_outcomes": checks[
                "partial_and_complete_opaque_outcomes"
            ],
            "crash_during_orphan_quarantine": checks[
                "crash_during_orphan_quarantine"
            ],
            "crash_during_outcome_quarantine": checks[
                "crash_during_quarantine"
            ],
        },
    }
    required = (
        findings["F1_attempt_formula_content_equality"][
            "exact_attack_rejected"
        ]
        and findings["F2_phase_input_output_crosslinks"][
            "exact_postcheck_substitution_rejected"
        ]
        and findings["F2_phase_input_output_crosslinks"][
            "conversion_output_refresh_still_caught_by_checker_input"
        ]
        and findings["F3_exact_certificate_and_details_shape"][
            "rejected_count"
        ]
        == 3
        and checks["pre_RUN_STARTED_crash_windows"]["recovered_count"] == 4
        and checks["pre_RUN_STARTED_crash_windows"][
            "all_windows_claim_safe_and_freshly_retryable"
        ]
        and checks["partial_and_complete_opaque_outcomes"][
            "recovered_count"
        ]
        == 2
        and checks["crash_during_quarantine"]["safe_retry_count"] == 4
        and checks["malformed_symlink_extra_orphans"]["rejected_count"] == 6
        and checks["opaque_orphan_contents"]["fresh_retry_attempt_number"] == 1
        and checks["pre_RUN_STARTED_orphan_after_RETRYABLE"][
            "fresh_retry_attempt_number"
        ]
        == 2
        and checks["crash_during_orphan_quarantine"][
            "safe_continuation_count"
        ]
        == 3
        and checks["malformed_metadata_v1_regressions"]["rejected_count"] == 6
        and checks["adjacent_output_crosslink_matrix"]["rejected_count"] == 4
    )
    if not required:
        raise AssertionError("a preserved v1-v3 regression failed")
    return checks, findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REVIEW / "evidence_v4.json"
    )
    arguments = parser.parse_args()
    if arguments.output.parent.resolve() != REVIEW.resolve():
        raise ValueError("v4 evidence must be written in the review directory")

    frozen_before, preserved_before = verify_bound_bytes()
    live_tree_before = base.tree_digest(LIVE)
    live_tree_digest_before = canonical_digest(live_tree_before)

    checker = case_real_checker()
    rup_soundness = case_rup_soundness_exhaustive()
    live_nonclaim = case_live_nonclaim()

    with tempfile.TemporaryDirectory(
        prefix=".referee-v4-fixtures-", dir=REVIEW
    ) as temporary:
        foundation = base.Foundation(Path(temporary).resolve())
        tools = base.tool_evidence()
        with foundation.frozen_context():
            command_binding = case_v4_command_binding(foundation)
            checks, findings = replay_v1_v3_regressions(foundation)

    frozen_after, preserved_after = verify_bound_bytes()
    live_tree_after = base.tree_digest(LIVE)
    live_tree_digest_after = canonical_digest(live_tree_after)
    if (
        frozen_before != frozen_after
        or preserved_before != preserved_after
        or live_tree_before != live_tree_after
    ):
        raise AssertionError("v4 replay changed frozen, historical, or live bytes")

    verdict = "ACCEPT"
    evidence = {
        "schema": "order13-k3-production-independent-referee-evidence-v4",
        "verdict": verdict,
        "scope": (
            "Current v4 local bytes, exact frozen attempt-1 raw-proof replay, "
            "and synthetic v1-v3 hostile fixtures. No SAT solver launched and "
            "no live production state changed."
        ),
        "final_frozen_file_sha256": frozen_after,
        "preserved_v1_v3_artifact_sha256": preserved_after,
        "pinned_tool_sha256": PINNED_TOOLS,
        "tool_evidence": tools,
        "deletion_agnostic_RUP_soundness": rup_soundness,
        "exact_frozen_raw_checker": checker,
        "v4_command_and_provenance_binding": command_binding,
        "live_attempt_remains_nonclaim": live_nonclaim,
        "live_tree_digest_sha256_before": live_tree_digest_before,
        "live_tree_digest_sha256_after": live_tree_digest_after,
        "live_tree_unchanged": True,
        "preserved_regression_checks": checks,
        "preserved_repaired_findings": findings,
        "checker_caveat": (
            "Pinned -W is not fatal on every warning path. The runner's "
            "strict marker/output gate and mandatory strict normalizer were "
            "independently exercised and fail closed on such output."
        ),
        "real_solver_execution_count": 0,
        "real_drat_trim_execution_count": checker[
            "real_drat_trim_execution_count"
        ],
    }
    arguments.output.write_bytes(
        (json.dumps(evidence, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
