#!/usr/bin/env python3
"""Fail-closed replay for the accepted order-12 frontier.

The default mode checks every hash-bound theorem, source, review, and
certificate artifact named by the acceptance record, and independently
parses the exact DoubleLex DIMACS census.  ``--full`` additionally runs the
publication-sized LRAT verifier.  Neither mode invokes a SAT solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


CAMPAIGN = Path(__file__).resolve().parents[2]
ACCEPTANCE = CAMPAIGN / "results/order12_frontier_acceptance.json"

EXPECTED_ACCEPTANCE_SIZE = 7_726
EXPECTED_ACCEPTANCE_SHA256 = (
    "e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a"
)
EXPECTED_SCHEMA = "gamma-theta-order12-frontier-acceptance-v1"
EXPECTED_STATUS = "ACCEPTED_WITH_EXPLICIT_PUBLISHED_THROUGH_ORDER_11_PREMISE"
EXPECTED_VERDICT = (
    "ACCEPT_CERTIFIED_FINITE_ORDER12_FRONTIER_RELATIVE_TO_PUBLISHED_ORDER11"
)
EXPECTED_CLAIMS = ["C-046", "C-047", "C-048", "C-049", "C-050"]
EXPECTED_FORMULA = {
    "variables": 18_381,
    "clauses": 115_507,
    "literal_occurrences": 1_190_774,
    "maximum_variable": 18_381,
}


class ReplayError(RuntimeError):
    """A fail-closed acceptance or replay error."""


def reject_constant(value: str) -> None:
    raise ReplayError(f"non-finite JSON constant rejected: {value}")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReplayError(f"duplicate JSON key rejected: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReplayError(f"cannot parse {path}: {error}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def check_bound_artifact(
    record: dict[str, Any], location: str
) -> dict[str, Any]:
    relative = record["path"]
    if not isinstance(relative, str) or relative.startswith("/"):
        raise ReplayError(f"{location}: path must be repository-relative")
    path = CAMPAIGN / relative
    if not path.is_file() or path.is_symlink():
        raise ReplayError(f"{location}: missing regular file {relative}")

    actual_size = path.stat().st_size
    actual_sha = sha256_file(path)
    if actual_sha != record["sha256"]:
        raise ReplayError(
            f"{location}: SHA-256 mismatch for {relative}: {actual_sha}"
        )
    if "size_bytes" in record and actual_size != record["size_bytes"]:
        raise ReplayError(
            f"{location}: size mismatch for {relative}: {actual_size}"
        )
    return {
        "path": relative,
        "size_bytes": actual_size,
        "sha256": actual_sha,
    }


def walk_bindings(
    value: Any,
    location: str = "$",
    checked: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if checked is None:
        checked = []
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(
            value.get("sha256"), str
        ):
            checked.append(check_bound_artifact(value, location))
        for key, child in value.items():
            walk_bindings(child, f"{location}.{key}", checked)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_bindings(child, f"{location}[{index}]", checked)
    return checked


def parse_dimacs(path: Path) -> dict[str, int]:
    variables = clauses_declared = None
    clauses = literals = maximum = 0
    pending: list[int] = []

    with path.open("r", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, 1):
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                fields = line.split()
                if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                    raise ReplayError(
                        f"DIMACS line {line_number}: malformed header"
                    )
                if variables is not None:
                    raise ReplayError("DIMACS has multiple headers")
                variables, clauses_declared = map(int, fields[2:])
                continue
            if variables is None:
                raise ReplayError("DIMACS clause appears before header")
            try:
                tokens = [int(token) for token in line.split()]
            except ValueError as error:
                raise ReplayError(
                    f"DIMACS line {line_number}: noninteger token"
                ) from error
            for literal in tokens:
                if literal == 0:
                    clauses += 1
                    literals += len(pending)
                    pending.clear()
                else:
                    if abs(literal) > variables:
                        raise ReplayError(
                            f"DIMACS line {line_number}: variable out of range"
                        )
                    maximum = max(maximum, abs(literal))
                    pending.append(literal)

    if variables is None or clauses_declared is None:
        raise ReplayError("DIMACS header is missing")
    if pending:
        raise ReplayError("DIMACS final clause lacks a zero terminator")
    if clauses != clauses_declared:
        raise ReplayError(
            f"DIMACS clause count {clauses}, declared {clauses_declared}"
        )
    return {
        "variables": variables,
        "clauses": clauses,
        "literal_occurrences": literals,
        "maximum_variable": maximum,
    }


def require_exact_acceptance(record: dict[str, Any]) -> None:
    if record.get("schema") != EXPECTED_SCHEMA:
        raise ReplayError("unexpected acceptance schema")
    if record.get("schema_version") != 1:
        raise ReplayError("unexpected acceptance schema version")
    if record.get("status") != EXPECTED_STATUS:
        raise ReplayError("frontier acceptance is not in accepted status")
    if record.get("verdict") != EXPECTED_VERDICT:
        raise ReplayError("unexpected frontier verdict")
    if record.get("claim_ids") != EXPECTED_CLAIMS:
        raise ReplayError("unexpected accepted claim-ID set or ordering")

    cases = record["order12_parameter_coverage"]
    if cases.get("remaining_integral_cases") != [3, 4, 5]:
        raise ReplayError("order-12 parameter split is not exactly [3,4,5]")
    if (
        cases["k3"]["acceptance"].get("verdict")
        != "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION"
    ):
        raise ReplayError("k=3 acceptance verdict mismatch")
    if (
        cases["k4"]["exact_cnf_hostile_review"].get("verdict")
        != "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY"
    ):
        raise ReplayError("k=4 exact-CNF hostile verdict mismatch")
    if (
        cases["k4"]["graph_implication_review"].get("verdict")
        != "VALID_CONDITIONAL_CONNECTED_EXCLUSION_ONLY"
    ):
        raise ReplayError("k=4 graph-transfer verdict mismatch")
    review = record["independent_frontier_review"]
    if (
        review.get("verdict")
        != "ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE"
        or review.get("blocking_defects") != []
    ):
        raise ReplayError("assembled-frontier review is not an unblocked accept")


def check_nested_verdicts(
    record: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    k3_path = CAMPAIGN / record["order12_parameter_coverage"]["k3"][
        "acceptance"
    ]["path"]
    k3 = load_json(k3_path)
    if (
        k3.get("verdict")
        != "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION"
        or k3.get("claim_id") != "C-035"
    ):
        raise ReplayError("live k=3 acceptance content is inconsistent")

    review_record = record["independent_frontier_review"]
    review_binding = check_bound_artifact(
        {
            "path": review_record["evidence_path"],
            "size_bytes": review_record["evidence_size_bytes"],
            "sha256": review_record["evidence_sha256"],
        },
        "$.independent_frontier_review.evidence",
    )
    review_path = CAMPAIGN / review_record["evidence_path"]
    review = load_json(review_path)
    if (
        review.get("verdict")
        != "ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE"
        or review.get("blocking_defects") != []
        or review.get("solver_invoked") is not False
    ):
        raise ReplayError("live frontier-review evidence is inconsistent")
    if not review.get("case_coverage", {}).get("coverage_complete"):
        raise ReplayError("frontier-review evidence does not assert coverage")
    return (
        {
            "k3_verdict": k3["verdict"],
            "frontier_review_verdict": review["verdict"],
            "frontier_review_blocking_defects": 0,
        },
        review_binding,
    )


def run_full_lrat(record: dict[str, Any]) -> dict[str, Any]:
    verifier = CAMPAIGN / record["order12_parameter_coverage"]["k4"][
        "publication_verifier"
    ]["path"]
    completed = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=CAMPAIGN,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=900,
    )
    if completed.returncode != 0:
        raise ReplayError(
            "publication LRAT verifier failed: "
            + completed.stderr.decode("utf-8", "replace")
        )
    if completed.stderr:
        raise ReplayError(
            "publication LRAT verifier wrote stderr: "
            + completed.stderr.decode("utf-8", "replace")
        )
    try:
        output = json.loads(completed.stdout.decode("utf-8", "strict"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ReplayError("publication LRAT output is not strict JSON") from error
    if (
        output.get("schema")
        != "gamma-theta-doublelex-publication-verifier-v2"
        or output.get("verdict")
        != "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY"
        or output.get("lrat_check", {}).get("verified_marker_count") != 1
    ):
        raise ReplayError("publication LRAT verifier returned wrong scope")
    return {
        "verdict": output["verdict"],
        "verified_marker_count": 1,
        "solver_invoked": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="also decompress and replay the accepted LRAT proof",
    )
    arguments = parser.parse_args()

    if (
        not ACCEPTANCE.is_file()
        or ACCEPTANCE.is_symlink()
        or ACCEPTANCE.stat().st_size != EXPECTED_ACCEPTANCE_SIZE
        or sha256_file(ACCEPTANCE) != EXPECTED_ACCEPTANCE_SHA256
    ):
        raise ReplayError("acceptance-record trust-root binding mismatch")
    record = load_json(ACCEPTANCE)
    if not isinstance(record, dict):
        raise ReplayError("acceptance root is not an object")
    require_exact_acceptance(record)
    bindings = walk_bindings(record)
    bound_paths = [item["path"] for item in bindings]
    if len(bound_paths) != len(set(bound_paths)):
        raise ReplayError("duplicate decisive artifact binding")
    formula_path = CAMPAIGN / record["order12_parameter_coverage"]["k4"][
        "exact_formula"
    ]["path"]
    census = parse_dimacs(formula_path)
    if census != EXPECTED_FORMULA:
        raise ReplayError(f"unexpected exact formula census: {census!r}")
    nested, nested_binding = check_nested_verdicts(record)
    bindings.append(nested_binding)

    result: dict[str, Any] = {
        "schema": "gamma-theta-c050-replay-v1",
        "mode": "full-lrat" if arguments.full else "metadata-only",
        "verdict": (
            "VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT"
            if arguments.full
            else "VERIFIED_ORDER12_FRONTIER_BINDINGS"
        ),
        "acceptance_sha256": sha256_file(ACCEPTANCE),
        "bound_artifact_count": len(bindings),
        "bound_artifact_bytes": sum(item["size_bytes"] for item in bindings),
        "formula_census": census,
        "nested_verdicts": nested,
        "published_premise_explicit": True,
        "universal_resolution_claimed": False,
        "solver_invoked": False,
    }
    if arguments.full:
        result["lrat_replay"] = run_full_lrat(record)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReplayError as error:
        print(f"REJECTED: {error}", file=sys.stderr)
        raise SystemExit(1)
