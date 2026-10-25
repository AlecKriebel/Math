#!/usr/bin/env python3
"""Independent exact falsifier for the two law-only Paper B interfaces.

This verifier intentionally does not import the Paper B implementation or any
handoff helper.  Its input consists only of scalar observable tables: prefix
masses, future-cylinder probabilities, Kingman survival factors, and marked
first-contact entries.  It never accepts a selected graph fan, a routing role,
or a raw reticulation clock.

The finite fixtures below are supporting falsification evidence.  They are not
a proof of either universal graph-realization theorem.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


MANIFEST_SCHEMA = "nmsc-independent-law-interfaces-v1"
CERTIFICATE_SCHEMA = "nmsc-local-certificate-v3"
JOB = "independent_law_interfaces"

_FORBIDDEN_KEY_TOKENS = {
    "fan",
    "graph",
    "occupancy",
    "parent",
    "physical",
    "reticulation",
    "route",
    "routing",
    "clock",
}
_FORBIDDEN_VALUE_PREFIXES = (
    "fan:",
    "graph:",
    "hidden-clock:",
    "occupancy:",
    "parent-role:",
    "physical-port:",
    "raw-clock:",
    "raw-route:",
    "reticulation-time:",
    "route:",
    "routing-role:",
)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _rational(value: Any, field: str) -> sp.Rational:
    if isinstance(value, (bool, float)):
        raise ValueError(f"{field} must be an exact integer/rational string")
    try:
        result = sp.Rational(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError(f"invalid exact rational at {field}: {value!r}") from error
    return result


def _require_keys(value: dict[str, Any], required: set[str], field: str) -> None:
    if set(value) != required:
        missing = sorted(required.difference(value))
        extra = sorted(set(value).difference(required))
        raise ValueError(f"{field} keys differ; missing={missing}, extra={extra}")


def _law_only(value: Any, field: str = "manifest") -> None:
    """Reject raw graph-role fields recursively before doing any computation."""
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_").replace(" ", "_")
            tokens = {token for token in normalized.split("_") if token}
            if tokens.intersection(_FORBIDDEN_KEY_TOKENS):
                raise ValueError(f"raw graph/route/clock key forbidden at {field}.{key}")
            _law_only(child, f"{field}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _law_only(child, f"{field}[{index}]")
    elif isinstance(value, str):
        lowered = value.strip().lower()
        if lowered.startswith(_FORBIDDEN_VALUE_PREFIXES):
            raise ValueError(f"raw graph/route/clock value forbidden at {field}")
    elif isinstance(value, float):
        raise ValueError(f"floating-point input forbidden at {field}")


def _matrix_rows(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.factor(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def _is_zero(value: Any) -> bool:
    return bool(sp.simplify(value) == 0)


def _matrix_equal(left: sp.MatrixBase, right: sp.MatrixBase) -> bool:
    if left.shape != right.shape:
        return False
    return all(_is_zero(left[i, j] - right[i, j]) for i in range(left.rows) for j in range(left.cols))


def _matrix_differs(left: sp.MatrixBase, right: sp.MatrixBase) -> bool:
    return not _matrix_equal(left, right)


def _kingman_kernel(survival: sp.Rational) -> sp.Matrix:
    if not 0 < survival < 1:
        raise ValueError("Kingman survival must lie strictly between zero and one")
    return sp.Matrix([[survival, 1 - survival], [0, 1]])


def _normalization_case(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bool]]:
    _require_keys(
        case,
        {"case_id", "observable_completion_table", "epochs", "terminal_continuation"},
        "normalization case",
    )
    case_id = case["case_id"]
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("normalization case_id must be nonempty")
    table = case["observable_completion_table"]
    if (
        not isinstance(table, list)
        or len(table) != 2
        or any(not isinstance(row, list) or len(row) < 3 for row in table)
        or len({len(row) for row in table}) != 1
    ):
        raise ValueError(f"{case_id}: need a 2 by at-least-3 observable completion table")
    hankel = sp.Matrix(
        [
            [_rational(value, f"{case_id}.observable_completion_table") for value in row]
            for row in table
        ]
    )
    if any(value <= 0 for value in hankel):
        raise ValueError(f"{case_id}: observable completion entries must be positive")
    row_sums = [sp.factor(sum(hankel[i, j] for j in range(hankel.cols))) for i in range(hankel.rows)]
    recovered_rows = [
        [sp.factor(hankel[i, j] / row_sums[i]) for j in range(hankel.cols)]
        for i in range(hankel.rows)
    ]
    minors = []
    for first_col in range(hankel.cols):
        for second_col in range(first_col + 1, hankel.cols):
            minors.append(
                sp.factor(
                    hankel[0, first_col] * hankel[1, second_col]
                    - hankel[0, second_col] * hankel[1, first_col]
                )
            )

    swapped_hankel = hankel.copy()
    swapped_hankel[1, 0], swapped_hankel[1, 1] = hankel[1, 1], hankel[1, 0]
    swapped_minors = []
    for first_col in range(swapped_hankel.cols):
        for second_col in range(first_col + 1, swapped_hankel.cols):
            swapped_minors.append(
                sp.factor(
                    swapped_hankel[0, first_col] * swapped_hankel[1, second_col]
                    - swapped_hankel[0, second_col] * swapped_hankel[1, first_col]
                )
            )

    if not isinstance(case["epochs"], list) or len(case["epochs"]) != 2:
        raise ValueError(f"{case_id}: exactly two spanning epochs required")
    rates: list[sp.Rational] = []
    survivals: list[sp.Rational] = []
    durations: list[sp.Expr] = []
    for index, epoch in enumerate(case["epochs"]):
        _require_keys(epoch, {"rate", "survival"}, f"{case_id}.epochs[{index}]")
        rate = _rational(epoch["rate"], f"{case_id}.epochs[{index}].rate")
        survival = _rational(epoch["survival"], f"{case_id}.epochs[{index}].survival")
        if rate <= 0 or not 0 < survival < 1:
            raise ValueError(f"{case_id}: rate positive and survival in (0,1) required")
        rates.append(rate)
        survivals.append(survival)
        durations.append(sp.log(1 / survival) / rate)

    continuation_rows = case["terminal_continuation"]
    if not isinstance(continuation_rows, list) or len(continuation_rows) != 2:
        raise ValueError(f"{case_id}: terminal continuation must have two state rows")
    if any(not isinstance(row, list) or len(row) != 2 for row in continuation_rows):
        raise ValueError(f"{case_id}: terminal continuation must be 2 by 2")
    continuation = sp.Matrix(
        [
            [_rational(value, f"{case_id}.terminal_continuation") for value in row]
            for row in continuation_rows
        ]
    )
    k1, k2 = (_kingman_kernel(value) for value in survivals)
    composed = k1 * k2
    collapsed = _kingman_kernel(sp.factor(survivals[0] * survivals[1]))
    spanning = composed * continuation
    collapsed_spanning = collapsed * continuation
    swap = sp.Matrix([[0, 1], [1, 0]])
    swapped_boundary = k1 * swap * k2 * continuation

    checks = {
        "prefix_all_completions_sum_one": _is_zero(sum(row_sums) - 1),
        "future_all_completions_sum_one": all(_is_zero(sum(row) - 1) for row in recovered_rows),
        "row_sums_recover_positive_prefix_mass": all(value > 0 for value in row_sums),
        "every_row_recovers_same_future_law": all(
            _is_zero(recovered_rows[i][j] - recovered_rows[0][j])
            for i in range(1, 2)
            for j in range(hankel.cols)
        ),
        "rank_one_all_minors_zero": all(_is_zero(value) for value in minors),
        "single_row_continuation_swap_killed": any(not _is_zero(value) for value in swapped_minors),
        "terminal_rows_are_all_completions": all(
            _is_zero(sum(continuation[i, j] for j in range(continuation.cols)) - 1)
            for i in range(continuation.rows)
        ),
        "terminal_state_rows_are_separated": any(
            not _is_zero(continuation[0, j] - continuation[1, j])
            for j in range(continuation.cols)
        ),
        "kingman_cocycle_spans_both_epochs": _matrix_equal(composed, collapsed),
        "future_cylinders_respect_spanning_cocycle": _matrix_equal(spanning, collapsed_spanning),
        "spanning_rows_are_all_completions": all(
            _is_zero(sum(spanning[i, j] for j in range(spanning.cols)) - 1)
            for i in range(spanning.rows)
        ),
        "swapped_boundary_continuation_killed": _matrix_differs(spanning, swapped_boundary),
        "duration_word_reconstructs_survivals": all(
            _is_zero(sp.exp(-rates[i] * durations[i]) - survivals[i]) for i in range(2)
        ),
    }
    checks = {name: bool(value) for name, value in checks.items()}
    witness = {
        "case_id": case_id,
        "recovered_prefix_masses": [str(value) for value in row_sums],
        "recovered_future_law": [str(value) for value in recovered_rows[0]],
        "rank_one_table": _matrix_rows(hankel),
        "row_sums": [str(value) for value in row_sums],
        "normalized_rows": [[str(value) for value in row] for row in recovered_rows],
        "rank_one_minors": [str(value) for value in minors],
        "swapped_row_minors": [str(value) for value in swapped_minors],
        "rate_word": [str(value) for value in rates],
        "survival_word": [str(value) for value in survivals],
        "duration_word": [str(value) for value in durations],
        "spanning_response": _matrix_rows(spanning),
        "swapped_boundary_response": _matrix_rows(swapped_boundary),
        "checks": checks,
    }
    return witness, checks


def _canonical_atom_key(value: Any, field: str) -> str:
    if not isinstance(value, list) or not value or not all(isinstance(part, str) and part for part in value):
        raise ValueError(f"{field} must be a nonempty list of observable string labels")
    return _canonical_bytes(value).decode("ascii")


def _column_minor(left: list[sp.Rational], right: list[sp.Rational]) -> list[sp.Expr]:
    if len(left) != len(right):
        raise ValueError("continuation columns must have equal length")
    return [
        sp.factor(left[i] * right[j] - left[j] * right[i])
        for i in range(len(left))
        for j in range(i + 1, len(left))
    ]


def _typed_code(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    return sorted(
        (
            {
                "atom_key": record["atom_key"],
                "incidence_fingerprint": record["incidence_fingerprint"],
                "weight": str(record["weight"]),
            }
            for record in records
        ),
        key=lambda record: (record["atom_key"], record["incidence_fingerprint"]),
    )


def _incidence_fingerprint(
    *,
    lower_shell_key: Any,
    atom_key: Any,
    incidence_key: Any,
    onset: sp.Rational,
    continuation_column: list[sp.Rational],
) -> str:
    """Build a matching key only from labelled observable scalar entries."""
    payload = {
        "lower_shell_key": lower_shell_key,
        "atom_key": atom_key,
        "observable_incidence_key": incidence_key,
        "support_onset": str(onset),
        "normalized_continuation_column": [str(value) for value in continuation_column],
    }
    return _digest(payload)


def _first_contact_case(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bool]]:
    _require_keys(case, {"case_id", "lower_shell_key", "gamma", "common_rate", "atoms"}, "first-contact case")
    case_id = case["case_id"]
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("first-contact case_id must be nonempty")
    lower_shell_canonical = _canonical_atom_key(case["lower_shell_key"], f"{case_id}.lower_shell_key")
    gamma = _rational(case["gamma"], f"{case_id}.gamma")
    common_rate = _rational(case["common_rate"], f"{case_id}.common_rate")
    if not 0 < gamma < 1 or common_rate <= 0:
        raise ValueError(f"{case_id}: gamma in (0,1) and positive rate required")
    if not isinstance(case["atoms"], list) or len(case["atoms"]) != 2:
        raise ValueError(f"{case_id}: the hostile fixture requires exactly two scalar atoms")

    parsed: list[dict[str, Any]] = []
    raw_key_to_atom: dict[str, dict[str, Any]] = {}
    atom_required = {
        "atom_key",
        "incidence_key",
        "support_onset",
        "observed_entry_mass",
        "predecessor_transports",
        "continuation_column",
    }
    for index, atom in enumerate(case["atoms"]):
        allowed = atom_required.union({"contact_filter"})
        if not isinstance(atom, dict) or not atom_required.issubset(atom) or set(atom).difference(allowed):
            raise ValueError(f"{case_id}.atoms[{index}] has missing or extra fields")
        atom_key = _canonical_atom_key(atom["atom_key"], f"{case_id}.atoms[{index}].atom_key")
        incidence_key = _canonical_atom_key(atom["incidence_key"], f"{case_id}.atoms[{index}].incidence_key")
        onset = _rational(atom["support_onset"], f"{case_id}.atoms[{index}].support_onset")
        entry_mass = _rational(atom["observed_entry_mass"], f"{case_id}.atoms[{index}].observed_entry_mass")
        column = [
            _rational(value, f"{case_id}.atoms[{index}].continuation_column")
            for value in atom["continuation_column"]
        ]
        if onset <= 0 or entry_mass <= 0 or len(column) < 2 or any(value < 0 for value in column):
            raise ValueError(f"{case_id}: invalid scalar first-contact entry")
        if not _is_zero(sum(column) - 1):
            raise ValueError(f"{case_id}: continuation columns must be all-completions normalized")
        if not isinstance(atom["predecessor_transports"], list):
            raise ValueError(f"{case_id}: predecessor_transports must be a list")
        parsed_atom = {
            "raw_atom": atom,
            "atom_key": atom_key,
            "incidence_key": incidence_key,
            "onset": onset,
            "entry_mass": entry_mass,
            "column": column,
        }
        if atom_key in raw_key_to_atom:
            raise ValueError(f"{case_id}: duplicate observable atom key")
        raw_key_to_atom[atom_key] = parsed_atom
        parsed.append(parsed_atom)

    parsed.sort(key=lambda atom: (atom["onset"], atom["atom_key"]))
    if not parsed[0]["onset"] < parsed[1]["onset"]:
        raise ValueError(f"{case_id}: fixture must have unequal, ordered outlet support onsets")

    residuals: dict[str, sp.Rational] = {}
    renewal_terms: dict[str, list[sp.Rational]] = {}
    typed_records: list[dict[str, Any]] = []
    for atom in parsed:
        subtractions: list[sp.Rational] = []
        seen_predecessors: set[str] = set()
        for transport_index, transport in enumerate(atom["raw_atom"]["predecessor_transports"]):
            _require_keys(
                transport,
                {"predecessor_atom_key", "no_contact_transport"},
                f"{case_id}.predecessor_transports[{transport_index}]",
            )
            predecessor = _canonical_atom_key(
                transport["predecessor_atom_key"],
                f"{case_id}.predecessor_transports[{transport_index}].predecessor_atom_key",
            )
            if predecessor in seen_predecessors:
                raise ValueError(f"{case_id}: duplicate predecessor in one renewal row")
            seen_predecessors.add(predecessor)
            if predecessor not in residuals:
                raise ValueError(f"{case_id}: predecessor is absent or not at an earlier support onset")
            transport_mass = _rational(
                transport["no_contact_transport"],
                f"{case_id}.predecessor_transports[{transport_index}].no_contact_transport",
            )
            if not 0 <= transport_mass <= 1:
                raise ValueError(f"{case_id}: no-contact transport must lie in [0,1]")
            subtractions.append(sp.factor(residuals[predecessor] * transport_mass))
        residual = sp.factor(atom["entry_mass"] - sum(subtractions, sp.Rational(0)))
        residuals[atom["atom_key"]] = residual
        renewal_terms[atom["atom_key"]] = subtractions
        fingerprint = _incidence_fingerprint(
            lower_shell_key=case["lower_shell_key"],
            atom_key=atom["raw_atom"]["atom_key"],
            incidence_key=atom["raw_atom"]["incidence_key"],
            onset=atom["onset"],
            continuation_column=atom["column"],
        )
        typed_records.append(
            {
                "atom_key": atom["atom_key"],
                "incidence_fingerprint": fingerprint,
                "weight": residual,
            }
        )

    columns = [atom["column"] for atom in parsed]
    separation_minors = _column_minor(columns[0], columns[1])
    typed = _typed_code(typed_records)
    permuted_typed = _typed_code(list(reversed(typed_records)))

    false_match_records = copy.deepcopy(typed_records)
    first_fingerprint = false_match_records[0]["incidence_fingerprint"]
    false_match_records[0]["incidence_fingerprint"] = false_match_records[1]["incidence_fingerprint"]
    false_match_records[1]["incidence_fingerprint"] = first_fingerprint
    false_match_typed = _typed_code(false_match_records)

    naive_later_mass = parsed[1]["entry_mass"]
    expected_weights = [gamma, 1 - gamma]
    filters = parsed[0]["raw_atom"].get("contact_filter")
    if not isinstance(filters, dict):
        raise ValueError(f"{case_id}: earlier atom needs its scalar contact-filter table")
    _require_keys(
        filters,
        {"predecessor_contact_mass", "survival_factor", "merge_cell_mass", "survive_cell_mass", "density_coefficient"},
        f"{case_id}.contact_filter",
    )
    predecessor_contact_mass = _rational(filters["predecessor_contact_mass"], f"{case_id}.predecessor_contact_mass")
    survival_factor = _rational(filters["survival_factor"], f"{case_id}.survival_factor")
    merge_mass = _rational(filters["merge_cell_mass"], f"{case_id}.merge_cell_mass")
    survive_mass = _rational(filters["survive_cell_mass"], f"{case_id}.survive_cell_mass")
    density = _rational(filters["density_coefficient"], f"{case_id}.density_coefficient")
    first_residual = residuals[parsed[0]["atom_key"]]

    wrong_transport_second = parsed[1]["entry_mass"]
    wrong_transport_weights = [first_residual, wrong_transport_second]
    checks = {
        "unequal_outlet_support_onsets": parsed[0]["onset"] < parsed[1]["onset"],
        "renewal_residuals_positive": all(value > 0 for value in residuals.values()),
        "renewal_residuals_sum_one": _is_zero(sum(residuals.values(), sp.Rational(0)) - 1),
        "renewal_recovers_gamma_and_complement": all(
            _is_zero(residuals[parsed[index]["atom_key"]] - expected_weights[index]) for index in range(2)
        ),
        "naive_later_entry_is_not_complement_weight": not _is_zero(naive_later_mass - (1 - gamma)),
        "wrong_zero_transport_is_killed": not _is_zero(sum(wrong_transport_weights) - 1),
        "continuation_columns_scalar_separated": any(not _is_zero(value) for value in separation_minors),
        "incidence_fingerprints_distinct": len({record["incidence_fingerprint"] for record in typed_records}) == 2,
        "typed_code_invariant_under_input_order": typed == permuted_typed,
        "swapped_incidence_false_match_killed": false_match_typed != typed,
        "first_contact_filter_has_no_predecessor_contact": _is_zero(predecessor_contact_mass),
        "first_contact_merge_cell_recomputed": _is_zero(merge_mass - first_residual * (1 - survival_factor)),
        "first_contact_survive_cell_recomputed": _is_zero(survive_mass - (1 - first_residual + first_residual * survival_factor)),
        "first_contact_cells_all_completions": _is_zero(merge_mass + survive_mass - 1),
        "first_contact_density_recomputed": _is_zero(density - first_residual * common_rate),
    }
    checks = {name: bool(value) for name, value in checks.items()}
    witness = {
        "case_id": case_id,
        "lower_shell_key": lower_shell_canonical,
        "support_onsets": [str(atom["onset"]) for atom in parsed],
        "observed_entry_masses": [str(atom["entry_mass"]) for atom in parsed],
        "renewal_subtractions": {
            atom["atom_key"]: [str(value) for value in renewal_terms[atom["atom_key"]]] for atom in parsed
        },
        "renewal_residuals": [str(residuals[atom["atom_key"]]) for atom in parsed],
        "naive_later_entry_mass": str(naive_later_mass),
        "continuation_separation_minors": [str(value) for value in separation_minors],
        "typed_q8_code": typed,
        "false_match_code": false_match_typed,
        "contact_filter": {
            "survival_factor": str(survival_factor),
            "merge_cell_mass": str(merge_mass),
            "survive_cell_mass": str(survive_mass),
            "density_coefficient": str(density),
        },
        "checks": checks,
    }
    return witness, checks


def _parse_lower_survival(value: Any, rate: sp.Rational, u: sp.Symbol, field: str) -> sp.Expr:
    if value == "1" or value == 1:
        return sp.Integer(1)
    expected = f"exp(-{rate}*u)"
    if value != expected:
        raise ValueError(f"{field} accepts only 1 or the declared exact Kingman exponential {expected!r}")
    return sp.exp(-rate * u)


def _breakpoint_case(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bool]]:
    _require_keys(case, {"case_id", "gamma", "rate", "one_child", "two_child"}, "breakpoint_pair")
    case_id = case["case_id"]
    gamma = _rational(case["gamma"], f"{case_id}.gamma")
    rate = _rational(case["rate"], f"{case_id}.rate")
    if gamma != sp.Rational(1, 2) or rate <= 0:
        raise ValueError("breakpoint hostile fixture must exercise gamma=1/2 and a positive equal rate")
    child_keys = {"lower_pair_survival", "lower_pair_density_at_zero"}
    _require_keys(case["one_child"], child_keys, f"{case_id}.one_child")
    _require_keys(case["two_child"], child_keys, f"{case_id}.two_child")

    u = sp.symbols("u", nonnegative=True)
    one_upper = 1 - gamma + gamma * sp.exp(-rate * u)
    two_upper = 2 * gamma * (1 - gamma) + (gamma**2 + (1 - gamma) ** 2) * sp.exp(-rate * u)
    one_invariant = sp.factor(
        one_upper.subs(u, 0) * sp.diff(one_upper, u, 2).subs(u, 0)
        - sp.diff(one_upper, u).subs(u, 0) ** 2
    )
    pure_kingman = sp.exp(-rate * u)
    pure_invariant = sp.factor(
        pure_kingman.subs(u, 0) * sp.diff(pure_kingman, u, 2).subs(u, 0)
        - sp.diff(pure_kingman, u).subs(u, 0) ** 2
    )
    one_lower = _parse_lower_survival(case["one_child"]["lower_pair_survival"], rate, u, f"{case_id}.one_child")
    two_lower = _parse_lower_survival(case["two_child"]["lower_pair_survival"], rate, u, f"{case_id}.two_child")
    one_density = _rational(case["one_child"]["lower_pair_density_at_zero"], f"{case_id}.one_child.density")
    two_density = _rational(case["two_child"]["lower_pair_density_at_zero"], f"{case_id}.two_child.density")

    one_upper_constant = sp.factor(1 - gamma)
    two_upper_constant = sp.factor(2 * gamma * (1 - gamma))

    def scalar_split_classifier(lower: sp.Expr, density_at_zero: sp.Rational, upper_constant: sp.Expr) -> bool:
        positive_kingman_pair = (
            density_at_zero > 0
            and _is_zero(density_at_zero - rate)
            and _is_zero(lower - sp.exp(-rate * u))
        )
        return bool(positive_kingman_pair and upper_constant > 0)

    one_class = scalar_split_classifier(one_lower, one_density, one_upper_constant)
    two_class = scalar_split_classifier(two_lower, two_density, two_upper_constant)
    naive_upper_only_one = bool(one_upper_constant > 0)
    naive_upper_only_two = bool(two_upper_constant > 0)

    checks = {
        "balanced_equal_rate_upper_germs_coincide": _is_zero(one_upper - two_upper),
        "one_child_mixed_germ_is_not_pure_kingman_bridge": one_invariant > 0 and _is_zero(pure_invariant),
        "one_child_has_no_lower_positive_pair": _is_zero(one_density) and _is_zero(one_lower - 1),
        "two_child_has_positive_lower_kingman_pair": two_density > 0 and _is_zero(two_density - rate),
        "one_child_not_split_breakpoint": not one_class,
        "two_child_is_split_breakpoint": two_class,
        "upper_constant_only_mutant_killed": naive_upper_only_one and naive_upper_only_two and one_class != two_class,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    witness = {
        "case_id": case_id,
        "gamma": str(gamma),
        "equal_rate": str(rate),
        "one_child_upper_germ": str(one_upper),
        "two_child_upper_germ": str(two_upper),
        "mixed_germ_log_curvature_invariant": str(one_invariant),
        "pure_kingman_log_curvature_invariant": str(pure_invariant),
        "one_child_lower_pair_survival": str(one_lower),
        "two_child_lower_pair_survival": str(two_lower),
        "one_child_split_classification": one_class,
        "two_child_split_classification": two_class,
        "checks": checks,
    }
    return witness, checks


def _raw_field_mutants_killed(manifest: dict[str, Any]) -> dict[str, bool]:
    route_mutant = copy.deepcopy(manifest)
    route_mutant["first_contact_cases"][0]["atoms"][0]["route"] = "left-parent"
    clock_mutant = copy.deepcopy(manifest)
    clock_mutant["first_contact_cases"][0]["hidden_clock"] = "2"
    nested_clock_value_mutant = copy.deepcopy(manifest)
    nested_clock_value_mutant["first_contact_cases"][0]["atoms"][0]["atom_key"].append("raw-clock:2")

    killed: dict[str, bool] = {}
    for name, mutant in (
        ("raw_route_field_rejected", route_mutant),
        ("hidden_clock_field_rejected", clock_mutant),
        ("nested_raw_clock_value_rejected", nested_clock_value_mutant),
    ):
        try:
            _law_only(mutant)
        except ValueError:
            killed[name] = True
        else:
            killed[name] = False
    return killed


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _law_only(manifest)
    _require_keys(
        manifest,
        {"schema", "proof_boundary", "normalization_cases", "first_contact_cases", "breakpoint_pair"},
        "manifest",
    )
    if manifest["schema"] != MANIFEST_SCHEMA:
        raise ValueError(f"unexpected manifest schema {manifest['schema']!r}")
    if not isinstance(manifest["proof_boundary"], str) or "does not prove" not in manifest["proof_boundary"]:
        raise ValueError("manifest must state the finite-fixture proof boundary explicitly")
    if not isinstance(manifest["normalization_cases"], list) or len(manifest["normalization_cases"]) != 2:
        raise ValueError("manifest must contain exactly two normalization/cocycle cases")
    if not isinstance(manifest["first_contact_cases"], list) or len(manifest["first_contact_cases"]) != 2:
        raise ValueError("manifest must contain exactly two first-contact cases")
    ids = [case.get("case_id") for case in manifest["normalization_cases"] + manifest["first_contact_cases"]]
    ids.append(manifest["breakpoint_pair"].get("case_id"))
    if any(not isinstance(case_id, str) or not case_id for case_id in ids) or len(ids) != len(set(ids)):
        raise ValueError("every fixture needs a unique nonempty case_id")


def _make_record(manifest: dict[str, Any], witness: dict[str, Any], status: str) -> dict[str, Any]:
    input_hash = _digest(manifest)
    record = {
        "schema_version": CERTIFICATE_SCHEMA,
        "job": JOB,
        "case_id": input_hash[:24],
        "input_hash": input_hash,
        "status": status,
        "graph": None,
        "system": {
            "manifest_schema": manifest["schema"],
            "normalization_case_ids": [case["case_id"] for case in manifest["normalization_cases"]],
            "first_contact_case_ids": [case["case_id"] for case in manifest["first_contact_cases"]],
            "breakpoint_case_id": manifest["breakpoint_pair"]["case_id"],
        },
        "exact_witness": witness,
        "declared_quotient_orbit": {
            "interfaces": [
                "law-only all-completions continuation cocycle",
                "law-only first-contact renewal and typed split atoms",
            ],
            "graph_selected_fan_input": False,
        },
        "notes": (
            "Independent exact scalar falsification only: no Paper B imports, selected graph fan, "
            "raw route, physical port, or hidden reticulation clock. Passing is supporting evidence, "
            "not a universal reconstruction proof."
        ),
    }
    required = {
        "schema_version",
        "job",
        "case_id",
        "input_hash",
        "status",
        "graph",
        "system",
        "exact_witness",
        "declared_quotient_orbit",
        "notes",
    }
    if set(record) != required or status not in {"PASS", "BLOCKING"}:
        raise ValueError("internal certificate schema failure")
    if record["case_id"] != record["input_hash"][:24] or len(record["input_hash"]) != 64:
        raise ValueError("internal certificate digest failure")
    if (record["graph"] is None) == (record["system"] is None):
        raise ValueError("certificate must have exactly one replay system")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text())
    if not isinstance(manifest, dict):
        raise ValueError("manifest root must be an object")
    _validate_manifest(manifest)

    normalization_witnesses: list[dict[str, Any]] = []
    all_checks: list[bool] = []
    for case in manifest["normalization_cases"]:
        witness, checks = _normalization_case(case)
        normalization_witnesses.append(witness)
        all_checks.extend(checks.values())

    first_contact_witnesses: list[dict[str, Any]] = []
    for case in manifest["first_contact_cases"]:
        witness, checks = _first_contact_case(case)
        first_contact_witnesses.append(witness)
        all_checks.extend(checks.values())

    breakpoint_witness, breakpoint_checks = _breakpoint_case(manifest["breakpoint_pair"])
    all_checks.extend(breakpoint_checks.values())
    raw_mutants = _raw_field_mutants_killed(manifest)
    all_checks.extend(raw_mutants.values())

    mixed_germ_fixtures = []
    u = sp.symbols("u", nonnegative=True)
    for case in manifest["first_contact_cases"]:
        gamma = _rational(case["gamma"], f"{case['case_id']}.gamma")
        rate = _rational(case["common_rate"], f"{case['case_id']}.common_rate")
        germ = 1 - gamma + gamma * sp.exp(-rate * u)
        invariant = sp.factor(
            germ.subs(u, 0) * sp.diff(germ, u, 2).subs(u, 0)
            - sp.diff(germ, u).subs(u, 0) ** 2
        )
        killed = bool(invariant > 0 and _is_zero(invariant - gamma * (1 - gamma) * rate**2))
        all_checks.append(killed)
        mixed_germ_fixtures.append(
            {
                "case_id": case["case_id"],
                "gamma": str(gamma),
                "rate": str(rate),
                "germ": str(germ),
                "log_curvature_invariant": str(invariant),
                "mixed_routing_as_kingman_mutant_killed": killed,
            }
        )

    status = "PASS" if all(all_checks) else "BLOCKING"
    witness = {
        "normalization_and_spanning_cocycle": normalization_witnesses,
        "first_contact_renewal": first_contact_witnesses,
        "breakpoint_pair": breakpoint_witness,
        "mixed_routing_germs": mixed_germ_fixtures,
        "raw_input_mutants_killed": raw_mutants,
        "independence": {
            "imports_paper_b": False,
            "imports_handoff_helpers": False,
            "accepts_graph_selected_fan": False,
            "accepts_raw_route_or_clock": False,
            "arithmetic": "exact SymPy rationals and symbolic exponentials",
        },
        "proof_boundary": manifest["proof_boundary"],
        "check_count": len(all_checks),
        "all_checks_pass": all(all_checks),
    }
    record = _make_record(manifest, witness, status)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")

    if status != "PASS":
        print(f"INDEPENDENT_LAW_INTERFACES_BLOCKING checks={len(all_checks)}")
        raise SystemExit(1)
    print(
        "INDEPENDENT_LAW_INTERFACES_OK "
        f"normalization={len(normalization_witnesses)} "
        f"first_contact={len(first_contact_witnesses)} "
        f"checks={len(all_checks)}"
    )


if __name__ == "__main__":
    main()
