#!/usr/bin/env python3
"""Independent hostile audit of the frozen C-050 replay wrapper.

This script is intentionally separate from ``repro/c050/replay.py``.  It
validates the frozen trust root, reparses every direct binding and the
alternate frontier-evidence binding, recomputes the DIMACS census, checks
the exact semantic boundary, runs both replay modes in a private copy, and
requires a collection of corruptions to fail closed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE_REL = "results/order12_frontier_acceptance.json"
REPLAY_REL = "repro/c050/replay.py"
README_REL = "repro/c050/README.md"

EXPECTED_TARGETS = {
    ACCEPTANCE_REL: (
        7_726,
        "e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a",
    ),
    REPLAY_REL: (
        13_041,
        "8e3c9f81e4cc38ecf392f44e750128bb108c20f8f1c53c8f72f0b43600405548",
    ),
    README_REL: (
        1_067,
        "251e393381eb4e61a9ba906b050207660231e96d5725176af2041fec8f6a240e",
    ),
}

EXPECTED_CENSUS = {
    "variables": 18_381,
    "clauses": 115_507,
    "literal_occurrences": 1_190_774,
    "maximum_variable": 18_381,
}

EXPECTED_VERDICTS = {
    "$.status": "ACCEPTED_WITH_EXPLICIT_PUBLISHED_THROUGH_ORDER_11_PREMISE",
    "$.order12_parameter_coverage.k3.acceptance.verdict":
        "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION",
    "$.order12_parameter_coverage.k4.publication_verifier.expected_verdict":
        "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
    "$.order12_parameter_coverage.k4.exact_cnf_hostile_review.verdict":
        "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
    "$.order12_parameter_coverage.k4.publication_package_hostile_review.verdict":
        "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_PUBLICATION_PACKAGE_V2_ONLY",
    "$.order12_parameter_coverage.k4.graph_implication_review.verdict":
        "VALID_CONDITIONAL_CONNECTED_EXCLUSION_ONLY",
    "$.order12_parameter_coverage.k5.simplicial_review.verdict": "ACCEPT",
    "$.independent_frontier_review.verdict":
        "ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE",
    "$.verdict":
        "ACCEPT_CERTIFIED_FINITE_ORDER12_FRONTIER_RELATIVE_TO_PUBLISHED_ORDER11",
}

FULL_REPLAY_EXTRAS = [
    "certificates/order12_k4_doublelex_seed0_lrat_publication/README.md",
    "certificates/order12_k4_doublelex_seed0_lrat_publication/publication-manifest.json",
    "certificates/order12_k4_doublelex_seed0_lrat/certificate.json",
    "certificates/order12_k4_doublelex_seed0_lrat/artifact-manifest.json",
    "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/hostile-evidence.json",
    "tools/drat_trim_2023_05_22/lrat-check",
]


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def strict_json_bytes(payload: bytes, label: str) -> Any:
    def reject_constant(value: str) -> None:
        raise AuditError(f"{label}: non-finite constant {value}")

    def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"{label}: duplicate key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8", "strict")
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise AuditError(f"{label}: invalid strict JSON: {error}") from error


def nested(root: dict[str, Any], dotted: str) -> Any:
    value: Any = root
    for part in dotted.removeprefix("$.").split("."):
        value = value[part]
    return value


def direct_binding_records(
    value: Any,
    location: str = "$",
    output: list[tuple[str, dict[str, Any]]] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    if output is None:
        output = []
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(
            value.get("sha256"), str
        ):
            output.append((location, value))
        for key, child in value.items():
            direct_binding_records(child, f"{location}.{key}", output)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            direct_binding_records(child, f"{location}[{index}]", output)
    return output


def validate_relative_path(relative: str, label: str) -> Path:
    pure = PurePosixPath(relative)
    require(not pure.is_absolute(), f"{label}: absolute path")
    require("\\" not in relative, f"{label}: backslash path")
    require(".." not in pure.parts, f"{label}: parent traversal")
    path = ROOT / relative
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(ROOT.resolve()), f"{label}: escapes root")
    require(path.is_file(), f"{label}: not a file")
    require(not path.is_symlink(), f"{label}: final symlink")
    cursor = path.parent
    while cursor != ROOT:
        require(not cursor.is_symlink(), f"{label}: symlink ancestor {cursor}")
        cursor = cursor.parent
    return path


def validate_binding(
    record: dict[str, Any], label: str
) -> dict[str, Any]:
    relative = record["path"]
    require(isinstance(relative, str), f"{label}: non-string path")
    expected_sha = record["sha256"]
    require(
        isinstance(expected_sha, str)
        and len(expected_sha) == 64
        and all(c in "0123456789abcdef" for c in expected_sha),
        f"{label}: malformed SHA-256",
    )
    path = validate_relative_path(relative, label)
    actual_size = path.stat().st_size
    actual_sha = sha256(path)
    require(actual_sha == expected_sha, f"{label}: SHA-256 mismatch")
    if "size_bytes" in record:
        require(
            type(record["size_bytes"]) is int
            and record["size_bytes"] == actual_size,
            f"{label}: size mismatch",
        )
    return {
        "location": label,
        "path": relative,
        "size_bytes": actual_size,
        "size_declared": "size_bytes" in record,
        "sha256": actual_sha,
    }


def parse_dimacs(path: Path) -> dict[str, int]:
    variables: int | None = None
    declared: int | None = None
    clauses = literals = maximum = 0
    pending = 0
    with path.open("r", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                fields = line.split()
                require(
                    variables is None
                    and len(fields) == 4
                    and fields[:2] == ["p", "cnf"],
                    f"DIMACS malformed header at line {line_number}",
                )
                variables, declared = int(fields[2]), int(fields[3])
                require(variables >= 0 and declared >= 0, "negative DIMACS census")
                continue
            require(variables is not None, "DIMACS clause before header")
            for token in line.split():
                try:
                    literal = int(token)
                except ValueError as error:
                    raise AuditError(
                        f"DIMACS noninteger at line {line_number}"
                    ) from error
                if literal == 0:
                    clauses += 1
                    literals += pending
                    pending = 0
                else:
                    require(
                        0 < abs(literal) <= variables,
                        f"DIMACS variable out of range at line {line_number}",
                    )
                    maximum = max(maximum, abs(literal))
                    pending += 1
    require(variables is not None and declared is not None, "missing DIMACS header")
    require(pending == 0, "unterminated DIMACS clause")
    require(clauses == declared, "DIMACS declared/actual clause mismatch")
    return {
        "variables": variables,
        "clauses": clauses,
        "literal_occurrences": literals,
        "maximum_variable": maximum,
    }


def copy_file(relative: str, destination_root: Path) -> None:
    source = ROOT / relative
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def run_replay(root: Path, full: bool = False) -> dict[str, Any]:
    command = ["python3", str(root / REPLAY_REL)]
    if full:
        command.append("--full")
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=900,
        check=False,
    )
    elapsed = time.monotonic() - started
    result: dict[str, Any] = {
        "command": " ".join(command[-2:] if full else command[-1:]),
        "exit_code": completed.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "stderr": completed.stderr.decode("utf-8", "replace"),
    }
    if completed.stdout:
        result["stdout"] = strict_json_bytes(
            completed.stdout, f"replay {'full' if full else 'metadata'} stdout"
        )
    return result


def require_rejection(root: Path, label: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["python3", str(root / REPLAY_REL)],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    stderr = completed.stderr.decode("utf-8", "replace")
    require(completed.returncode != 0, f"{label}: mutation was accepted")
    require(not completed.stdout, f"{label}: mutation emitted success JSON")
    require("REJECTED:" in stderr, f"{label}: no fail-closed rejection marker")
    return {
        "mutation": label,
        "exit_code": completed.returncode,
        "rejection": stderr.strip().splitlines()[-1],
    }


def restore(relative: str, private_root: Path) -> None:
    shutil.copy2(ROOT / relative, private_root / relative)


def main() -> None:
    target_bindings: dict[str, dict[str, Any]] = {}
    for relative, (expected_size, expected_sha) in EXPECTED_TARGETS.items():
        path = ROOT / relative
        require(path.stat().st_size == expected_size, f"{relative}: target size")
        require(sha256(path) == expected_sha, f"{relative}: target SHA")
        target_bindings[relative] = {
            "size_bytes": expected_size,
            "sha256": expected_sha,
        }

    acceptance = strict_json_bytes(
        (ROOT / ACCEPTANCE_REL).read_bytes(), "C-050 acceptance"
    )
    require(isinstance(acceptance, dict), "acceptance root is not an object")
    require(
        acceptance["schema"] == "gamma-theta-order12-frontier-acceptance-v1"
        and acceptance["schema_version"] == 1,
        "acceptance schema mismatch",
    )
    require(
        acceptance["claim_ids"] == ["C-046", "C-047", "C-048", "C-049", "C-050"],
        "claim coverage mismatch",
    )
    require(
        acceptance["order12_parameter_coverage"]["remaining_integral_cases"]
        == [3, 4, 5],
        "parameter coverage mismatch",
    )
    require(
        acceptance["published_premise"]["campaign_boundary"]
        == (
            "The published coverage claim is used as a cited mathematical "
            "premise; it is not relabeled as a campaign-certified enumeration."
        ),
        "published/campaign boundary mismatch",
    )
    require(
        acceptance["published_premise"]["model"]
        == "one guard moves along one edge to an unoccupied attacked vertex",
        "one-guard model marker mismatch",
    )
    require(
        acceptance["scope_exclusions"]
        == [
            "This is not a universal proof of the gamma-theta conjecture.",
            "This is not a counterexample.",
            (
                "The campaign has not independently reproduced the all-graph "
                "enumeration at orders 10 and 11."
            ),
            (
                "The through-order-12 statement explicitly uses the published "
                "through-order-11 computation as a premise."
            ),
            "No claim is made about graphs of order at least 13.",
        ],
        "scope exclusion set mismatch",
    )
    for location, expected in EXPECTED_VERDICTS.items():
        require(nested(acceptance, location) == expected, f"{location}: verdict")
    require(
        acceptance["independent_frontier_review"]["blocking_defects"] == [],
        "frontier review has blockers",
    )

    direct_records = direct_binding_records(acceptance)
    require(len(direct_records) == 20, "unexpected direct binding count")
    bindings = [
        validate_binding(record, location) for location, record in direct_records
    ]
    review_record = acceptance["independent_frontier_review"]
    evidence_record = {
        "path": review_record["evidence_path"],
        "size_bytes": review_record["evidence_size_bytes"],
        "sha256": review_record["evidence_sha256"],
    }
    bindings.append(
        validate_binding(
            evidence_record, "$.independent_frontier_review.evidence"
        )
    )
    paths = [item["path"] for item in bindings]
    require(len(paths) == len(set(paths)) == 21, "duplicate decisive path")

    formula_record = acceptance["order12_parameter_coverage"]["k4"][
        "exact_formula"
    ]
    census = parse_dimacs(ROOT / formula_record["path"])
    require(census == EXPECTED_CENSUS, "exact formula census mismatch")
    require(
        {
            key: formula_record[key]
            for key in ("variables", "clauses", "literal_occurrences")
        }
        == {
            key: EXPECTED_CENSUS[key]
            for key in ("variables", "clauses", "literal_occurrences")
        },
        "acceptance formula census mismatch",
    )

    tex = (
        ROOT / acceptance["published_premise"]["arxiv_tex"]["path"]
    ).read_text(encoding="utf-8")
    require(
        r"There are no counterexample to the $\gamma-\theta$ conjecture "
        r"of order $n \leq 11$." in tex,
        "published order-11 observation absent",
    )
    require(
        "the attacker selects a vertex $v$ on which there is no guard" in tex
        and "moving a guard on a neighbour of $v$ to $v$" in tex,
        "published one-guard definition absent",
    )

    k3 = strict_json_bytes(
        (ROOT / acceptance["order12_parameter_coverage"]["k3"]["acceptance"][
            "path"
        ]).read_bytes(),
        "C-035 acceptance",
    )
    require(
        k3["claim_id"] == "C-035"
        and k3["verdict"]
        == "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION"
        and k3["complete_slice_proof"]["disconnected_case_explicitly_covered"]
        is True,
        "C-035 nested boundary mismatch",
    )
    frontier_evidence = strict_json_bytes(
        (ROOT / review_record["evidence_path"]).read_bytes(),
        "frontier evidence",
    )
    require(
        frontier_evidence["verdict"]
        == "ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE"
        and frontier_evidence["blocking_defects"] == []
        and frontier_evidence["solver_invoked"] is False
        and frontier_evidence["case_coverage"]["coverage_complete"] is True
        and frontier_evidence["case_coverage"][
            "order12_integral_parameters_after_k_ge_3_and_n_ge_2k_plus_1"
        ]
        == [3, 4, 5],
        "frontier evidence scope/coverage mismatch",
    )

    replay_source = (ROOT / REPLAY_REL).read_text(encoding="utf-8")
    verifier_rel = acceptance["order12_parameter_coverage"]["k4"][
        "publication_verifier"
    ]["path"]
    verifier_source = (ROOT / verifier_rel).read_text(encoding="utf-8")
    require(
        replay_source.count("subprocess.run(") == 1,
        "unexpected replay subprocess call count",
    )
    require(
        verifier_source.count("subprocess.run(") == 2
        and "[zstd, \"-d\"" in verifier_source
        and "[str(CHECKER), str(FORMULA), str(recovered)]" in verifier_source,
        "unexpected publication-verifier child commands",
    )
    for solver in ("cadical", "kissat", "minisat", "lingeling", "cryptominisat"):
        require(
            solver not in replay_source.lower()
            and solver not in verifier_source.lower(),
            f"SAT solver token in replay call graph: {solver}",
        )

    all_copy_paths = set(paths)
    all_copy_paths.update(
        [ACCEPTANCE_REL, REPLAY_REL, README_REL, *FULL_REPLAY_EXTRAS]
    )
    with tempfile.TemporaryDirectory(prefix="c050-hostile-audit-") as temporary:
        private_root = Path(temporary) / "campaign"
        for relative in sorted(all_copy_paths):
            copy_file(relative, private_root)

        metadata_run = run_replay(private_root, full=False)
        require(metadata_run["exit_code"] == 0, "private metadata replay failed")
        require(
            metadata_run["stdout"]["verdict"]
            == "VERIFIED_ORDER12_FRONTIER_BINDINGS"
            and metadata_run["stdout"]["bound_artifact_count"] == 21
            and metadata_run["stdout"]["formula_census"] == EXPECTED_CENSUS
            and metadata_run["stdout"]["solver_invoked"] is False,
            "private metadata replay returned wrong scope",
        )
        full_run = run_replay(private_root, full=True)
        require(full_run["exit_code"] == 0, "private full replay failed")
        require(
            full_run["stdout"]["verdict"]
            == "VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT"
            and full_run["stdout"]["lrat_replay"]["verdict"]
            == "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY"
            and full_run["stdout"]["lrat_replay"]["verified_marker_count"] == 1
            and full_run["stdout"]["solver_invoked"] is False,
            "private full replay returned wrong scope",
        )

        mutations: list[dict[str, Any]] = []
        acceptance_path = private_root / ACCEPTANCE_REL
        original_acceptance = acceptance_path.read_bytes()

        mutated = original_acceptance.replace(b'"campaign_day": 2', b'"campaign_day": 3')
        require(mutated != original_acceptance, "self-hash mutation setup")
        acceptance_path.write_bytes(mutated)
        mutations.append(require_rejection(private_root, "acceptance self-hash"))
        restore(ACCEPTANCE_REL, private_root)

        acceptance_path.write_bytes(original_acceptance + b"\n")
        mutations.append(require_rejection(private_root, "acceptance size"))
        restore(ACCEPTANCE_REL, private_root)

        reductions = private_root / "math/reductions.md"
        reductions.write_bytes(reductions.read_bytes() + b"\n")
        mutations.append(require_rejection(private_root, "bound artifact hash"))
        restore("math/reductions.md", private_root)

        formula_rel = formula_record["path"]
        formula = private_root / formula_rel
        formula_payload = formula.read_bytes()
        formula_mutated = formula_payload.replace(
            b"p cnf 18381 115507", b"p cnf 18381 115506", 1
        )
        require(formula_mutated != formula_payload, "formula mutation setup")
        formula.write_bytes(formula_mutated)
        mutations.append(require_rejection(private_root, "formula census/header"))
        try:
            altered_census = parse_dimacs(formula)
        except AuditError as error:
            altered_census = {"rejected": str(error)}
        require(altered_census != EXPECTED_CENSUS, "mutated census unchanged")
        restore(formula_rel, private_root)

        verdict_mutated = original_acceptance.replace(
            b'"verdict": "ACCEPT_CERTIFIED_FINITE_ORDER12_FRONTIER',
            b'"verdict": "XCCEPT_CERTIFIED_FINITE_ORDER12_FRONTIER',
            1,
        )
        require(verdict_mutated != original_acceptance, "verdict mutation setup")
        acceptance_path.write_bytes(verdict_mutated)
        mutations.append(require_rejection(private_root, "acceptance verdict"))
        restore(ACCEPTANCE_REL, private_root)

        evidence_rel = review_record["evidence_path"]
        evidence_path = private_root / evidence_rel
        evidence_payload = evidence_path.read_bytes()
        evidence_mutated = evidence_payload.replace(
            b"ACCEPT_ORDER12_FRONTIER", b"XCCEPT_ORDER12_FRONTIER", 1
        )
        require(evidence_mutated != evidence_payload, "evidence mutation setup")
        evidence_path.write_bytes(evidence_mutated)
        mutations.append(require_rejection(private_root, "nested review verdict"))
        restore(evidence_rel, private_root)

        missing_rel = "math/lemmas/order12_frontier.md"
        missing_path = private_root / missing_rel
        held_path = missing_path.with_suffix(".held")
        missing_path.rename(held_path)
        mutations.append(require_rejection(private_root, "missing decisive artifact"))
        held_path.rename(missing_path)

        duplicate_probe = private_root / "duplicate.json"
        duplicate_probe.write_text('{"x":1,"x":2}', encoding="utf-8")
        try:
            strict_json_bytes(duplicate_probe.read_bytes(), "duplicate probe")
        except AuditError:
            duplicate_json_rejected = True
        else:
            duplicate_json_rejected = False
        require(duplicate_json_rejected, "independent duplicate JSON accepted")

        nonfinite_probe = private_root / "nonfinite.json"
        nonfinite_probe.write_text('{"x":NaN}', encoding="utf-8")
        try:
            strict_json_bytes(nonfinite_probe.read_bytes(), "nonfinite probe")
        except AuditError:
            nonfinite_json_rejected = True
        else:
            nonfinite_json_rejected = False
        require(nonfinite_json_rejected, "independent nonfinite JSON accepted")

    tracked_required: list[str] = []
    untracked_required: list[str] = []
    for relative in sorted(all_copy_paths):
        completed = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        (tracked_required if completed.returncode == 0 else untracked_required).append(
            relative
        )

    result = {
        "schema": "gamma-theta-c050-acceptance-hostile-audit-v1",
        "verdict": "ACCEPT_EXACT_FROZEN_C050_WRAPPER",
        "targets": target_bindings,
        "acceptance": {
            "direct_binding_count": 20,
            "alternate_evidence_binding_count": 1,
            "unique_bound_artifact_count": len(bindings),
            "unique_bound_artifact_bytes": sum(
                item["size_bytes"] for item in bindings
            ),
            "bindings": bindings,
            "bindings_without_declared_size": [
                item["path"] for item in bindings if not item["size_declared"]
            ],
            "verdicts_checked": EXPECTED_VERDICTS,
            "parameter_cases": [3, 4, 5],
            "published_premise_explicit": True,
            "campaign_did_not_reproduce_orders_10_11": True,
            "universal_resolution_claimed": False,
        },
        "formula_census": census,
        "private_replays": {
            "metadata": metadata_run,
            "full_lrat": full_run,
        },
        "mutation_tests": mutations,
        "strict_json_tests": {
            "duplicate_key_rejected": duplicate_json_rejected,
            "nonfinite_constant_rejected": nonfinite_json_rejected,
        },
        "child_command_audit": {
            "replay_subprocess_calls": 1,
            "publication_verifier_subprocess_calls": 2,
            "commands": ["python verifier", "zstd decompress", "lrat-check"],
            "sat_solver_invoked": False,
        },
        "fresh_clone_inventory": {
            "required_path_count": len(all_copy_paths),
            "tracked_or_staged_count": len(tracked_required),
            "untracked_count": len(untracked_required),
            "untracked_paths": untracked_required,
            "checker_binary_git_ignored": True,
            "checker_bootstrap_required": True,
        },
        "blocking_defects": [],
        "nonblocking_limitations": [
            (
                "Full mode freshly replays the exact k=4 LRAT only; C-035 is "
                "used through its frozen prior acceptance and theorem, as the "
                "README and output verdict state."
            ),
            (
                "One direct hostile-review binding has no declared size_bytes; "
                "the independent audit recomputed its size and SHA-256, and "
                "the frozen acceptance SHA plus artifact SHA remain decisive."
            ),
            (
                "A fresh clone must bootstrap the Git-ignored hash-pinned "
                "lrat-check binary; binary reproducibility depends on the "
                "documented local toolchain."
            ),
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (AuditError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f"AUDIT_REJECTED: {error}")
