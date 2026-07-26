#!/usr/bin/env python3
"""Fail-closed replay for the final order-13 strategy/pilot bytes.

The historical clean-room constructor in ``audit.py`` is retained unchanged.
This wrapper binds that constructor by hash, reruns its four formula
reconstructions and all generic/signature censuses, and validates the final
strategy plus strict v2 pilot record.  It invokes no solver on a formula;
``cadical --version`` is the only solver-binary execution.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
REVIEW_DIR = Path(__file__).resolve().parent
STRATEGY = ROOT / "math/lemmas/order13_strategy.md"
PILOT = ROOT / "results/logs/order13_strategy_k3_template_pilot.json"
HISTORICAL_AUDIT = REVIEW_DIR / "audit.py"
HISTORICAL_EVIDENCE = REVIEW_DIR / "evidence.json"
SOURCE = ROOT / "src/synthesis_k3/encoding.py"
SOLVER = ROOT / "tools/cadical_3_0_1/build/cadical"

EXPECTED_BINDINGS = {
    "strategy": {
        "path": "math/lemmas/order13_strategy.md",
        "sha256": "5b59d8c9fcbf1eb2a3e20157fcef02b4faa02a48e62c6fbda7b9c1fc12e7d6c6",
        "size_bytes": 14924,
    },
    "pilot": {
        "path": "results/logs/order13_strategy_k3_template_pilot.json",
        "sha256": "4383dec046945223a7bd3d6b642996fdd5cfc6da4d03b041b2b1cd351369ed64",
        "size_bytes": 3927,
    },
    "historical_audit": {
        "path": "reviews/order13_strategy_hostile/audit.py",
        "sha256": "451fd9ede28e16c68386de04017625481791121ca524190a89d7ca02ff15adf7",
        "size_bytes": 21057,
    },
    "historical_evidence": {
        "path": "reviews/order13_strategy_hostile/evidence.json",
        "sha256": "74bb9b71a3570abf9a4400c72dc4618c4c50221127dcf2a43b41911423ef87d7",
        "size_bytes": 5211,
    },
    "source": {
        "path": "src/synthesis_k3/encoding.py",
        "sha256": "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
        "size_bytes": 15071,
    },
    "solver": {
        "path": "tools/cadical_3_0_1/build/cadical",
        "sha256": "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
        "size_bytes": 1571160,
    },
}

FINAL_CLAIM_BOUNDARY = (
    "Exploratory sizing and one proofless solver pilot only. At run time "
    "the runtime parameterization, order-13 template coverage theorem, and "
    "formula bytes were unaudited. A later hostile strategy review "
    "independently reconstructed the formula bytes and audited the template "
    "cover, but the UNSAT solver return has no retained proof and is not a "
    "mathematical claim."
)


class AuditError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_binding(path: Path, relative: str) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": relative,
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
    }


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def strict_json(path: Path) -> object:
    payload = path.read_bytes()
    text = payload.decode("utf-8")

    def reject_constant(token: str) -> object:
        raise AuditError(f"non-finite JSON constant {token!r}")

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    return json.loads(
        text,
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
    )


def exact_keys(value: object, keys: set[str], role: str) -> Mapping[str, object]:
    require(isinstance(value, dict), f"{role} is not an object")
    require(set(value) == keys, f"{role} has unexpected keys")
    return value


def finite_positive(value: object, role: str) -> float:
    require(type(value) in (int, float), f"{role} is not numeric")
    result = float(value)
    require(math.isfinite(result) and result > 0, f"{role} is not finite-positive")
    return result


def load_historical_audit():
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(
        "order13_historical_cleanroom", HISTORICAL_AUDIT
    )
    require(
        specification is not None and specification.loader is not None,
        "cannot load historical audit module",
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def expected_template_view(records: Sequence[Mapping[str, object]]):
    keys = {
        "base_clauses",
        "base_literal_occurrences",
        "complete_coloring_rows",
        "full_clauses",
        "full_literal_occurrences",
        "full_size_bytes",
        "full_sha256",
        "template",
        "variables",
    }
    return [{key: record[key] for key in keys} for record in records]


def validate_final_json(
    parsed: object,
    reconstructions: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    root = exact_keys(
        parsed,
        {
            "claim_boundary",
            "classification",
            "campaign_protocol_compliance",
            "formula_generation",
            "hardware",
            "pilot",
            "repository_head",
            "schema",
            "schema_version",
            "timestamp_utc",
        },
        "pilot root",
    )
    require(root["claim_boundary"] == FINAL_CLAIM_BOUNDARY, "claim boundary mismatch")
    require(root["classification"] == "OBSERVED", "classification was promoted")
    require(
        root["schema"] == "gamma-theta-order13-strategy-k3-template-pilot-v2"
        and root["schema_version"] == 2,
        "final schema/version mismatch",
    )

    compliance = exact_keys(
        root["campaign_protocol_compliance"],
        {
            "cpu_seconds_recorded",
            "disposition",
            "exact_argv_recorded",
            "historical_invocation_replayable",
            "stdout_stderr_retained",
        },
        "protocol compliance",
    )
    require(compliance["cpu_seconds_recorded"] is False, "CPU time invented")
    require(compliance["exact_argv_recorded"] is False, "argv invented")
    require(
        compliance["historical_invocation_replayable"] is False,
        "historical run marked replayable",
    )
    require(compliance["stdout_stderr_retained"] is False, "transcript invented")
    require(
        compliance["disposition"]
        == "Historical exploratory nonclaim only. Missing metadata were not "
        "reconstructed; every future run must record them before launch.",
        "protocol disposition mismatch",
    )

    generation = exact_keys(
        root["formula_generation"], {"method", "source", "templates"}, "generation"
    )
    source = exact_keys(
        generation["source"], {"path", "sha256", "size_bytes"}, "source"
    )
    require(
        source
        == {
            "path": EXPECTED_BINDINGS["source"]["path"],
            "sha256": EXPECTED_BINDINGS["source"]["sha256"],
            "size_bytes": EXPECTED_BINDINGS["source"]["size_bytes"],
        },
        "source binding mismatch",
    )
    require(
        generation["templates"] == expected_template_view(reconstructions),
        "template records differ from reconstructed bytes",
    )

    hardware = exact_keys(
        root["hardware"],
        {"logical_cpus", "model", "physical_memory_bytes"},
        "hardware",
    )
    require(hardware["logical_cpus"] == os.cpu_count() == 10, "CPU count mismatch")
    require(hardware["model"] == "Apple M1 Pro", "CPU model mismatch")
    require(hardware["physical_memory_bytes"] == 17179869184, "memory mismatch")

    pilot = exact_keys(
        root["pilot"], {"formula_sha256", "formula_template", "result", "solver"}, "pilot"
    )
    require(pilot["formula_template"] == "hole11", "pilot template mismatch")
    require(pilot["formula_sha256"] == reconstructions[-1]["full_sha256"], "formula mismatch")
    require(pilot["result"] == "UNSAT_UNCERTIFIED", "pilot result was promoted")

    solver = exact_keys(
        pilot["solver"],
        {
            "cpu_seconds",
            "exact_argv",
            "exit_code",
            "internal_time_limit_seconds",
            "maximum_resident_set_size_bytes",
            "path",
            "seed",
            "sha256",
            "size_bytes",
            "stderr_sha256",
            "stdout_sha256",
            "version",
            "version_binding",
            "wall_seconds",
        },
        "solver",
    )
    for key in ("cpu_seconds", "exact_argv", "stderr_sha256", "stdout_sha256"):
        require(solver[key] is None, f"missing historical field {key} was invented")
    require(solver["exit_code"] == 20, "historical exit code mismatch")
    require(solver["internal_time_limit_seconds"] == 30, "time limit mismatch")
    require(
        type(solver["maximum_resident_set_size_bytes"]) is int
        and solver["maximum_resident_set_size_bytes"] == 6209536,
        "RSS mismatch",
    )
    require(solver["path"] == EXPECTED_BINDINGS["solver"]["path"], "solver path mismatch")
    require(solver["seed"] == 0, "seed mismatch")
    require(solver["sha256"] == EXPECTED_BINDINGS["solver"]["sha256"], "solver hash mismatch")
    require(solver["size_bytes"] == EXPECTED_BINDINGS["solver"]["size_bytes"], "solver size mismatch")
    require(solver["version"] == "3.0.1", "post-hoc version mismatch")
    require(
        solver["version_binding"]
        == "Post-hoc query of the exact hash-bound binary during the independent "
        "hostile audit; not a retained field from the historical invocation.",
        "post-hoc version disclosure mismatch",
    )
    finite_positive(solver["wall_seconds"], "wall time")

    require(
        root["repository_head"] == "9df3a414e6ba9f631ff68bff69d5ab0a37048f5e",
        "historical repository head mismatch",
    )
    require(root["timestamp_utc"] == "2026-07-26T14:32:55Z", "timestamp mismatch")

    return {
        "claim_boundary_is_time_indexed": True,
        "classification": root["classification"],
        "historical_missing_fields_remain_null": True,
        "historical_invocation_replayable": False,
        "posthoc_solver_version_disclosed": True,
        "result": pilot["result"],
        "schema": root["schema"],
        "schema_version": root["schema_version"],
        "strict_json_no_duplicate_or_nonfinite_values": True,
    }


def validate_strategy_text() -> dict[str, bool]:
    text = STRATEGY.read_text(encoding="utf-8")
    checks = {
        "dependency_ledger_corrected": (
            "accepted claims C-003, C-006,\nC-036, C-049, and C-050" in text
        ),
        "old_dependency_ledger_absent": (
            "accepted claims C-006, C-036,\nC-049, C-050, and C-051" not in text
        ),
        "rounded_time_correct": "returned UNSAT in 0.0202 seconds" in text,
        "old_rounded_time_absent": "returned UNSAT in 0.021 seconds" not in text,
        "missing_metadata_disclosed": (
            "failed to retain the exact solver\nargument vector, CPU time, "
            "or stdout/stderr transcript" in text
        ),
        "proofless_nonclaim_preserved": (
            "no proof was retained or checked" in text
            and "An UNSAT solver exit or a timeout is not evidence" in text
        ),
    }
    require(all(checks.values()), "final strategy prose validation failed")
    return checks


def main() -> int:
    observed_bindings = {
        "strategy": file_binding(STRATEGY, EXPECTED_BINDINGS["strategy"]["path"]),
        "pilot": file_binding(PILOT, EXPECTED_BINDINGS["pilot"]["path"]),
        "historical_audit": file_binding(
            HISTORICAL_AUDIT, EXPECTED_BINDINGS["historical_audit"]["path"]
        ),
        "historical_evidence": file_binding(
            HISTORICAL_EVIDENCE, EXPECTED_BINDINGS["historical_evidence"]["path"]
        ),
        "source": file_binding(SOURCE, EXPECTED_BINDINGS["source"]["path"]),
        "solver": file_binding(SOLVER, EXPECTED_BINDINGS["solver"]["path"]),
    }
    require(observed_bindings == EXPECTED_BINDINGS, "frozen byte binding mismatch")

    historical = load_historical_audit()
    reconstructions = [
        historical.reconstruct_template(length) for length in (5, 7, 9, 11)
    ]
    generic = [historical.generic_census(13, k) for k in (3, 4, 5)]
    signatures = {
        f"hole{length}": historical.signature_census(length)
        for length in (5, 7, 9, 11)
    }

    parsed = strict_json(PILOT)
    final_json = validate_final_json(parsed, reconstructions)
    strategy_checks = validate_strategy_text()

    version = subprocess.run(
        [str(SOLVER), "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
    )
    require(version.stderr == "", "cadical --version wrote stderr")
    require(version.stdout.strip() == "3.0.1", "bound solver version query mismatch")

    report = {
        "schema": "gamma-theta-order13-strategy-final-hostile-replay-v1",
        "verdict": "ACCEPT_FINAL_REVISED_BYTES_AND_UNCHANGED_STRATEGY_CONTENT",
        "bindings": observed_bindings,
        "strategy_checks": strategy_checks,
        "final_pilot_json": final_json,
        "solver_version_stdout": version.stdout.strip(),
        "template_reconstructions": reconstructions,
        "generic_census": generic,
        "signature_breaker_census": signatures,
        "limitations": [
            "No SAT solver was run on any formula.",
            "The historical proofless UNSAT return remains uncertified.",
            "This replay validates strategy/formula bytes and counts, not an order-13 exclusion.",
        ],
    }
    sys.stdout.buffer.write(canonical_json_bytes(report))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        AuditError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
    ) as error:
        print(f"FINAL_AUDIT_FAILURE: {error}", file=sys.stderr)
        raise SystemExit(1)
