#!/usr/bin/env python3
"""Export one seed-frontier root instance to deterministic DIMACS CNF.

This exporter is intentionally independent of OR-Tools.  It rebuilds the
mathematical root relaxation from a pinned frontier artifact:

* fixed ordinary and alternating margins;
* raw Hamming-distance interval from Eliahou's seed;
* even flip parity in every paired-endpoint quad; and
* the primitive 3rd-, 4th-, and 6th-root norm identities.

Linear forms are encoded by deterministic finite-state sum automata.  Each
quadratic norm is encoded by an explicit allowed-row selector, and the four
norms at each root are added by a one-hot finite-state sum.  The resulting CNF
can be solved with a proof-producing SAT solver and checked with a small DRAT
or LRAT checker.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from verify_variable_q_seed_quad_radius import (  # noqa: E402
    MarginTarget,
    check_radius,
    coordinate_class_sums,
)
from verify_variable_q_seed_radius import SEED  # noqa: E402


ENERGY = 334
ROOT_COEFFICIENT_PAIRS = {
    3: ((1, 0, -1), (0, 1, -1), -1),
    4: ((1, 0, -1, 0), (0, 1, 0, -1), 0),
    6: ((1, 0, -1, -1, 0, 1), (0, 1, 1, 0, -1, -1), 1),
}
ENCODINGS = {
    "baseline": "seed-frontier-root-cnf-v1",
    "cp-sat": "seed-frontier-root-cnf-v2",
}
QuadPosition = tuple[int, int]
EndpointQuad = tuple[QuadPosition, QuadPosition, QuadPosition, QuadPosition]


def _declare_exchangeable_quad_partition() -> tuple[
    tuple[EndpointQuad, ...], ...
]:
    """Declare the root-layer partition consumed by the CNF exporter.

    This declaration is audited independently in ``test_seed_frontier_cnf``;
    that audit reconstructs exchangeability from complete observable
    contribution signatures rather than reusing this grouping key.
    """

    partition = []
    for first_index, second_index in ((0, 1), (2, 3)):
        length = len(SEED[first_index])
        groups: dict[tuple, list[EndpointQuad]] = defaultdict(list)
        for left in range(length // 2):
            right = length - 1 - left
            coordinates: EndpointQuad = (
                (first_index, left),
                (first_index, right),
                (second_index, left),
                (second_index, right),
            )
            key = (
                first_index,
                left % 12,
                right % 12,
                tuple(
                    SEED[index][coordinate]
                    for index, coordinate in coordinates
                ),
            )
            groups[key].append(coordinates)
        partition.extend(tuple(group) for group in groups.values())
    return tuple(partition)


EXCHANGEABLE_QUAD_PARTITION = _declare_exchangeable_quad_partition()
EXCHANGEABLE_QUAD_COMPARISONS = tuple(
    (earlier, later)
    for orbit in EXCHANGEABLE_QUAD_PARTITION
    for earlier, later in zip(orbit, orbit[1:])
)


class CNF:
    """A small deterministic CNF builder with named variables."""

    def __init__(self) -> None:
        self.variable_names: list[str] = [""]
        self.clauses: list[tuple[int, ...]] = []
        self.section_clause_counts: dict[str, int] = {}
        self._section = "unclassified"

    @property
    def variable_count(self) -> int:
        return len(self.variable_names) - 1

    def new_var(self, name: str) -> int:
        self.variable_names.append(name)
        return self.variable_count

    def start_section(self, name: str) -> None:
        self._section = name
        self.section_clause_counts.setdefault(name, 0)

    def add_clause(self, literals: Iterable[int]) -> None:
        seen: set[int] = set()
        normalized = []
        for literal in literals:
            if literal == 0:
                raise ValueError("zero is not a CNF literal")
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                normalized.append(literal)
        self.clauses.append(tuple(normalized))
        self.section_clause_counts[self._section] = (
            self.section_clause_counts.get(self._section, 0) + 1
        )

    def exactly_one(self, variables: Sequence[int], name: str) -> None:
        """Encode exactly one by an at-least-one clause and Sinz AMO."""

        variables = tuple(variables)
        if not variables:
            self.add_clause(())
            return
        self.add_clause(variables)
        if len(variables) == 1:
            return
        auxiliaries = [
            self.new_var(f"{name}_amo_{index}")
            for index in range(len(variables) - 1)
        ]
        self.add_clause((-variables[0], auxiliaries[0]))
        for index in range(1, len(variables) - 1):
            self.add_clause((-variables[index], auxiliaries[index]))
            self.add_clause((-auxiliaries[index - 1], auxiliaries[index]))
            self.add_clause((-variables[index], -auxiliaries[index - 1]))
        self.add_clause((-variables[-1], -auxiliaries[-1]))

    def weighted_sum_states(
        self,
        variables: Sequence[int],
        weights: Sequence[int],
        name: str,
        *,
        lower_bound: int | None = None,
        upper_bound: int | None = None,
    ) -> dict[int, int]:
        """Return final one-hot states for ``sum(weight[i] * variable[i])``.

        Every transition is encoded in both directions conditional on its
        input bit.  Starting from a single unit state, this inductively makes
        exactly one state true at every layer without a separate cardinality
        encoding.  Bounds may prune states when all excluded assignments are
        intended to be forbidden, as for a nonnegative Hamming sum.
        """

        if len(variables) != len(weights):
            raise ValueError("weighted sum inputs and weights differ in length")
        start = self.new_var(f"{name}_state_0_sum_0")
        self.add_clause((start,))
        states = {0: start}
        layer = 0
        for variable, weight in zip(variables, weights, strict=True):
            if weight == 0:
                continue
            layer += 1
            next_sums = set()
            for value in states:
                for successor in (value, value + weight):
                    if lower_bound is not None and successor < lower_bound:
                        continue
                    if upper_bound is not None and successor > upper_bound:
                        continue
                    next_sums.add(successor)
            next_states = {
                value: self.new_var(f"{name}_state_{layer}_sum_{value}")
                for value in sorted(next_sums)
            }

            for value, previous in states.items():
                unchanged = next_states.get(value)
                changed = next_states.get(value + weight)
                self.add_clause(
                    (-previous, variable)
                    if unchanged is None
                    else (-previous, variable, unchanged)
                )
                self.add_clause(
                    (-previous, -variable)
                    if changed is None
                    else (-previous, -variable, changed)
                )

            for value, successor in next_states.items():
                unchanged_predecessor = states.get(value)
                changed_predecessor = states.get(value - weight)
                self.add_clause(
                    (-successor, variable)
                    if unchanged_predecessor is None
                    else (-successor, variable, unchanged_predecessor)
                )
                self.add_clause(
                    (-successor, -variable)
                    if changed_predecessor is None
                    else (-successor, -variable, changed_predecessor)
                )
            states = next_states
        return states

    def write_dimacs(
        self,
        path: Path,
        *,
        comments: Sequence[str] = (),
    ) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="ascii", newline="\n") as handle:
            for comment in comments:
                handle.write(f"c {comment}\n")
            handle.write(f"p cnf {self.variable_count} {len(self.clauses)}\n")
            for clause in self.clauses:
                if clause:
                    handle.write(" ".join(map(str, clause)))
                    handle.write(" 0\n")
                else:
                    handle.write("0\n")
        return hashlib.sha256(path.read_bytes()).hexdigest()


def _target(value: object) -> MarginTarget:
    if not isinstance(value, list):
        raise ValueError("target is not a list")
    result = tuple(tuple(int(entry) for entry in pair) for pair in value)
    if len(result) != 4 or any(len(pair) != 2 for pair in result):
        raise ValueError("target has the wrong shape")
    return result  # type: ignore[return-value]


def _artifact_instance(
    artifact_path: Path,
    result_index: int,
    expected_status: str,
) -> tuple[dict, dict, MarginTarget, str]:
    raw = artifact_path.read_bytes()
    payload = json.loads(raw)
    if payload.get("kind") != "variable-q-seed-frontier-filter":
        raise ValueError("not a seed-frontier artifact")
    results = payload.get("results")
    if not isinstance(results, list) or not 0 <= result_index < len(results):
        raise ValueError("result index is outside the artifact")
    result = results[result_index]
    if (
        expected_status != "ANY"
        and result.get("status") != expected_status
    ):
        raise ValueError(
            "selected artifact result status differs from --expect-status"
        )
    layers = payload.get("layers", {})
    if (
        layers.get("small_roots") is not True
        or layers.get("full_correlations") is not False
    ):
        raise ValueError("selected result is not a supported frontier layer")
    compression_7 = bool(layers.get("compression_7"))
    compression_7_alternating = bool(
        layers.get("compression_7_alternating")
    )
    compression = {
        (False, False): "none",
        (True, False): "z7",
        (False, True): "z14",
        (True, True): "both",
    }[(compression_7, compression_7_alternating)]
    payload["_sha256"] = hashlib.sha256(raw).hexdigest()
    return payload, result, _target(result["target"]), compression


def _minimum_flips_by_sequence(target: MarginTarget) -> tuple[int, ...]:
    result = []
    for sequence, (ordinary, alternating) in zip(SEED, target, strict=True):
        desired = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current = coordinate_class_sums(sequence)
        result.append(
            sum(
                abs(wanted - present) // 2
                for wanted, present in zip(desired, current, strict=True)
            )
        )
    return tuple(result)


def _validate_instance(
    payload: dict, result: dict, target: MarginTarget
) -> tuple[int, int, tuple[int, int]]:
    radius = int(payload["radius"])
    minimum_distance = int(payload.get("minimum_distance", 0))
    if radius < 0 or not 0 <= minimum_distance <= radius:
        raise ValueError("artifact has an invalid distance interval")
    expected = {
        (record.shard, record.target): record
        for record in check_radius(radius).targets
    }
    key = (int(result["shard"]), target)
    if key not in expected:
        raise ValueError("artifact target is not in the reconstructed radius set")
    record = expected[key]
    if (
        result.get("margin_distance") != record.margin_distance
        or result.get("quad_distance") != record.quad_distance
    ):
        raise ValueError("artifact target metadata differs from reconstruction")
    if record.quad_distance is None or record.quad_distance > radius:
        raise ValueError("artifact target is not margin-plus-quad feasible")
    if record.long_distance is None or record.short_distance is None:
        raise ValueError("artifact target lacks pair-distance lower bounds")
    first_possible = max(minimum_distance, record.quad_distance)
    if (first_possible - record.margin_distance) % 2:
        first_possible += 1
    if first_possible > radius:
        raise ValueError("artifact target is excluded by distance parity")
    ordinary = tuple(pair[0] for pair in target)
    alternating = tuple(pair[1] for pair in target)
    if sum(value * value for value in ordinary) != ENERGY:
        raise ValueError("target ordinary margins are off the exact norm shell")
    if sum(value * value for value in alternating) != ENERGY:
        raise ValueError("target alternating margins are off the exact norm shell")
    return (
        radius,
        minimum_distance,
        (record.long_distance, record.short_distance),
    )


def _add_endpoint_quad_parities(
    cnf: CNF, flips: tuple[tuple[int, ...], ...]
) -> None:
    for first_index, second_index in ((0, 1), (2, 3)):
        length = len(flips[first_index])
        for left in range(length // 2):
            right = length - 1 - left
            variables = (
                flips[first_index][left],
                flips[first_index][right],
                flips[second_index][left],
                flips[second_index][right],
            )
            for assignment in itertools.product((0, 1), repeat=4):
                if sum(assignment) % 2 == 0:
                    continue
                cnf.add_clause(
                    variable if value == 0 else -variable
                    for variable, value in zip(
                        variables, assignment, strict=True
                    )
                )


def _cardinality_states(
    cnf: CNF,
    variables: Sequence[int],
    name: str,
    maximum: int,
) -> dict[int, int]:
    return cnf.weighted_sum_states(
        variables,
        (1,) * len(variables),
        name,
        lower_bound=0,
        upper_bound=maximum,
    )


def _add_flip_direction_budgets(
    cnf: CNF,
    flips: tuple[tuple[int, ...], ...],
    target: MarginTarget,
    radius: int,
    minimum_distance: int,
) -> int:
    """Add the exact classwise flip decomposition implied by margins.

    In a coordinate class, all flips required in the target direction are
    fixed up to ``wrong`` cancelling pairs.  The sum of the eight ``wrong``
    counts is at most half the distance excess over the margin minimum, and
    is equal to it on an exact-distance shell.
    """

    minimum_by_sequence = _minimum_flips_by_sequence(target)
    margin_minimum = sum(minimum_by_sequence)
    extra_pairs = (radius - margin_minimum) // 2
    wrong_groups: list[dict[int, int]] = []
    for sequence_index, (sequence, variables, margins) in enumerate(
        zip(SEED, flips, target, strict=True)
    ):
        ordinary, alternating = margins
        desired_classes = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current_classes = coordinate_class_sums(sequence)
        for parity, (current, desired) in enumerate(
            zip(current_classes, desired_classes, strict=True)
        ):
            change = desired - current
            if change % 2:
                raise ValueError("target class change has odd parity")
            delta = change // 2
            plus_variables = tuple(
                variables[index]
                for index in range(parity, len(sequence), 2)
                if sequence[index] == 1
            )
            minus_variables = tuple(
                variables[index]
                for index in range(parity, len(sequence), 2)
                if sequence[index] == -1
            )
            if delta >= 0:
                plus_maximum = extra_pairs
                minus_maximum = delta + extra_pairs
            else:
                plus_maximum = -delta + extra_pairs
                minus_maximum = extra_pairs
            plus_states = _cardinality_states(
                cnf,
                plus_variables,
                f"direction_s{sequence_index}_p{parity}_plus",
                plus_maximum,
            )
            minus_states = _cardinality_states(
                cnf,
                minus_variables,
                f"direction_s{sequence_index}_p{parity}_minus",
                minus_maximum,
            )
            selectors: dict[int, int] = {}
            for wrong in range(extra_pairs + 1):
                plus_count = wrong if delta >= 0 else -delta + wrong
                minus_count = delta + wrong if delta >= 0 else wrong
                if (
                    plus_count not in plus_states
                    or minus_count not in minus_states
                ):
                    continue
                selector = cnf.new_var(
                    f"direction_s{sequence_index}_p{parity}_wrong_{wrong}"
                )
                cnf.add_clause((-selector, plus_states[plus_count]))
                cnf.add_clause((-selector, minus_states[minus_count]))
                selectors[wrong] = selector
            cnf.exactly_one(
                tuple(selectors.values()),
                f"direction_s{sequence_index}_p{parity}_wrong",
            )
            wrong_groups.append(selectors)
    _add_one_hot_weighted_total(
        cnf,
        wrong_groups,
        extra_pairs,
        "direction_extra_pairs",
        require_target=minimum_distance == radius,
    )
    return extra_pairs


def _add_pair_distance_lower_bounds(
    cnf: CNF,
    flips: tuple[tuple[int, ...], ...],
    pair_bounds: tuple[int, int],
    radius: int,
) -> None:
    for name, groups, lower in (
        ("long", flips[:2], pair_bounds[0]),
        ("short", flips[2:], pair_bounds[1]),
    ):
        variables = tuple(variable for group in groups for variable in group)
        states = _cardinality_states(
            cnf, variables, f"{name}_pair_distance", radius
        )
        cnf.add_clause(
            states[value] for value in sorted(states) if value >= lower
        )


def _add_exchangeable_quad_symmetry(
    cnf: CNF, flips: tuple[tuple[int, ...], ...]
) -> int:
    """Sort four-bit flip masks inside the root model's exact quad orbits."""

    for earlier_quad, later_quad in EXCHANGEABLE_QUAD_COMPARISONS:
        earlier = tuple(
            flips[index][coordinate] for index, coordinate in earlier_quad
        )
        later = tuple(
            flips[index][coordinate] for index, coordinate in later_quad
        )
        _add_four_bit_mask_order(cnf, earlier, later)
    return len(EXCHANGEABLE_QUAD_COMPARISONS)


def _add_four_bit_mask_order(
    cnf: CNF, earlier: Sequence[int], later: Sequence[int]
) -> None:
    if len(earlier) != 4 or len(later) != 4:
        raise ValueError("quad masks must contain four bits")
    for earlier_mask in range(16):
        for later_mask in range(16):
            if earlier_mask <= later_mask:
                continue
            clause = []
            for bit, variable in enumerate(earlier):
                clause.append(
                    -variable if earlier_mask >> bit & 1 else variable
                )
            for bit, variable in enumerate(later):
                clause.append(
                    -variable if later_mask >> bit & 1 else variable
                )
            cnf.add_clause(clause)


def _add_fixed_margins(
    cnf: CNF,
    flips: tuple[tuple[int, ...], ...],
    target: MarginTarget,
) -> None:
    for sequence_index, (sequence, variables, margins) in enumerate(
        zip(SEED, flips, target, strict=True)
    ):
        ordinary, alternating = margins
        desired_classes = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        for parity, desired in enumerate(desired_classes):
            indices = tuple(range(parity, len(sequence), 2))
            base = sum(sequence[index] for index in indices)
            difference = base - desired
            if difference % 2:
                raise ValueError("target class sum has unreachable parity")
            wanted = difference // 2
            states = cnf.weighted_sum_states(
                tuple(variables[index] for index in indices),
                tuple(sequence[index] for index in indices),
                f"margin_s{sequence_index}_p{parity}",
            )
            if wanted not in states:
                cnf.add_clause(())
            else:
                cnf.add_clause((states[wanted],))


def _root_rows(
    sequence: Sequence[int],
    maximum_flips: int,
    modulus: int,
    first_pattern: Sequence[int],
    second_pattern: Sequence[int],
    cross_sign: int,
    first_states: dict[int, int],
    second_states: dict[int, int],
) -> tuple[tuple[int, int, int, int, int], ...]:
    bound = len(sequence)
    first_base = sum(
        first_pattern[index % modulus] * value
        for index, value in enumerate(sequence)
    )
    second_base = sum(
        second_pattern[index % modulus] * value
        for index, value in enumerate(sequence)
    )
    maximum_change = 2 * maximum_flips
    first_low = max(-bound, first_base - maximum_change)
    first_high = min(bound, first_base + maximum_change)
    second_low = max(-bound, second_base - maximum_change)
    second_high = min(bound, second_base + maximum_change)
    rows = []
    for first in range(first_low, first_high + 1):
        first_difference = first_base - first
        if first_difference % 2:
            continue
        first_sum = first_difference // 2
        if first_sum not in first_states:
            continue
        for second in range(second_low, second_high + 1):
            second_difference = second_base - second
            if second_difference % 2:
                continue
            second_sum = second_difference // 2
            if second_sum not in second_states:
                continue
            norm = (
                first * first
                + cross_sign * first * second
                + second * second
            )
            if norm <= ENERGY:
                rows.append(
                    (first, second, norm, first_sum, second_sum)
                )
    return tuple(rows)


def _add_one_hot_weighted_total(
    cnf: CNF,
    groups: Sequence[dict[int, int]],
    target: int,
    name: str,
    *,
    require_target: bool = True,
) -> None:
    start = cnf.new_var(f"{name}_sum_layer_0_value_0")
    cnf.add_clause((start,))
    states = {0: start}
    for layer, choices in enumerate(groups, start=1):
        next_values = sorted(
            {
                partial + weight
                for partial in states
                for weight in choices
                if partial + weight <= target
            }
        )
        next_states = {
            value: cnf.new_var(f"{name}_sum_layer_{layer}_value_{value}")
            for value in next_values
        }
        cnf.exactly_one(
            tuple(next_states.values()), f"{name}_sum_layer_{layer}"
        )
        for partial, partial_variable in states.items():
            for weight, choice_variable in choices.items():
                successor = next_states.get(partial + weight)
                if successor is None:
                    cnf.add_clause((-partial_variable, -choice_variable))
                else:
                    cnf.add_clause(
                        (-partial_variable, -choice_variable, successor)
                    )
        states = next_states
    if require_target:
        if target not in states:
            cnf.add_clause(())
        else:
            cnf.add_clause((states[target],))


def _add_one_hot_weighted_equality(
    cnf: CNF,
    groups: Sequence[dict[int, int]],
    target: int,
    name: str,
) -> None:
    """Encode a signed weighted sum over exactly-one groups.

    State values are pruned against the minimum and maximum contribution of
    the remaining groups.  Each layer is exactly-one, so the forward
    transition clauses alone identify the unique arithmetic successor.
    """

    suffix_minimum = [0] * (len(groups) + 1)
    suffix_maximum = [0] * (len(groups) + 1)
    for index in range(len(groups) - 1, -1, -1):
        if not groups[index]:
            cnf.add_clause(())
            return
        suffix_minimum[index] = (
            suffix_minimum[index + 1] + min(groups[index])
        )
        suffix_maximum[index] = (
            suffix_maximum[index + 1] + max(groups[index])
        )

    start = cnf.new_var(f"{name}_sum_layer_0_value_0")
    cnf.add_clause((start,))
    states = {0: start}
    for index, choices in enumerate(groups):
        remaining_minimum = suffix_minimum[index + 1]
        remaining_maximum = suffix_maximum[index + 1]
        next_values = sorted(
            {
                partial + weight
                for partial in states
                for weight in choices
                if (
                    target - remaining_maximum
                    <= partial + weight
                    <= target - remaining_minimum
                )
            }
        )
        next_states = {
            value: cnf.new_var(
                f"{name}_sum_layer_{index + 1}_value_{value}"
            )
            for value in next_values
        }
        cnf.exactly_one(
            tuple(next_states.values()), f"{name}_sum_layer_{index + 1}"
        )
        for partial, partial_variable in states.items():
            for weight, choice_variable in choices.items():
                successor = next_states.get(partial + weight)
                if successor is None:
                    cnf.add_clause((-partial_variable, -choice_variable))
                else:
                    cnf.add_clause(
                        (-partial_variable, -choice_variable, successor)
                    )
        states = next_states
    if target not in states:
        cnf.add_clause(())
    else:
        cnf.add_clause((states[target],))


def _compression_cell_values(
    cnf: CNF,
    sequence: Sequence[int],
    variables: Sequence[int],
    sequence_index: int,
    residue: int,
    maximum_flips: int,
    *,
    coordinate_alternation: bool,
) -> dict[int, int]:
    positions = tuple(range(residue, len(sequence), 7))
    factors = tuple(
        -1 if coordinate_alternation and index % 2 else 1
        for index in positions
    )
    base = sum(
        factor * sequence[index]
        for index, factor in zip(positions, factors, strict=True)
    )
    states = cnf.weighted_sum_states(
        tuple(variables[index] for index in positions),
        tuple(
            factor * sequence[index]
            for index, factor in zip(positions, factors, strict=True)
        ),
        (
            f"compression_{'z14' if coordinate_alternation else 'z7'}_"
            f"s{sequence_index}_r{residue}"
        ),
    )
    values = {
        base - 2 * change: state
        for change, state in states.items()
        if abs(2 * change) <= 2 * maximum_flips
    }
    cnf.add_clause(tuple(values.values()))
    return dict(sorted(values.items()))


def _product_choice_group(
    cnf: CNF,
    left: dict[int, int],
    right: dict[int, int],
    name: str,
    *,
    same_cell: bool,
) -> dict[int, int]:
    rows = []
    for left_value, left_variable in left.items():
        for right_value, right_variable in right.items():
            if same_cell and left_value != right_value:
                continue
            rows.append(
                (
                    left_value,
                    right_value,
                    left_value * right_value,
                    left_variable,
                    right_variable,
                )
            )
    row_variables = [
        cnf.new_var(f"{name}_row_{left_value}_{right_value}")
        for left_value, right_value, _product, _left, _right in rows
    ]
    cnf.exactly_one(row_variables, f"{name}_rows")
    product_to_rows: dict[int, list[int]] = defaultdict(list)
    for row, row_variable in zip(rows, row_variables, strict=True):
        _left_value, _right_value, product, left_variable, right_variable = row
        cnf.add_clause((-row_variable, left_variable))
        cnf.add_clause((-row_variable, right_variable))
        product_to_rows[product].append(row_variable)
    product_variables = {
        product: cnf.new_var(f"{name}_product_{product}")
        for product in sorted(product_to_rows)
    }
    cnf.exactly_one(
        tuple(product_variables.values()), f"{name}_products"
    )
    for product, rows_for_product in product_to_rows.items():
        for row_variable in rows_for_product:
            cnf.add_clause((-row_variable, product_variables[product]))
    return product_variables


def _add_length_seven_compression(
    cnf: CNF,
    flips: tuple[tuple[int, ...], ...],
    maximum_flips: tuple[int, ...],
    *,
    coordinate_alternation: bool,
) -> dict[str, int]:
    label = "z14" if coordinate_alternation else "z7"
    cells = []
    for sequence_index, (sequence, variables, flip_limit) in enumerate(
        zip(SEED, flips, maximum_flips, strict=True)
    ):
        cells.append(
            tuple(
                _compression_cell_values(
                    cnf,
                    sequence,
                    variables,
                    sequence_index,
                    residue,
                    flip_limit,
                    coordinate_alternation=coordinate_alternation,
                )
                for residue in range(7)
            )
        )

    product_rows = 0
    product_values = 0
    for lag, target in enumerate((ENERGY, 0, 0, 0)):
        groups = []
        for sequence_index in range(4):
            for residue in range(7):
                other = (residue + lag) % 7
                group = _product_choice_group(
                    cnf,
                    cells[sequence_index][residue],
                    cells[sequence_index][other],
                    (
                        f"compression_{label}_lag{lag}_s{sequence_index}_"
                        f"r{residue}_{other}"
                    ),
                    same_cell=lag == 0,
                )
                groups.append(group)
                product_values += len(group)
        _add_one_hot_weighted_equality(
            cnf,
            groups,
            target,
            f"compression_{label}_lag{lag}_total",
        )
        product_rows += len(groups)
    return {
        f"{label}_product_groups": product_rows,
        f"{label}_distinct_product_values": product_values,
    }


def _add_small_root_invariants(
    cnf: CNF,
    flips: tuple[tuple[int, ...], ...],
    maximum_flips: tuple[int, ...],
) -> dict[str, int]:
    statistics: dict[str, int] = {}
    for modulus, (
        first_pattern,
        second_pattern,
        cross_sign,
    ) in ROOT_COEFFICIENT_PAIRS.items():
        norm_groups = []
        modulus_rows = 0
        for sequence_index, (sequence, variables, flip_limit) in enumerate(
            zip(SEED, flips, maximum_flips, strict=True)
        ):
            first_weights = tuple(
                value * first_pattern[index % modulus]
                for index, value in enumerate(sequence)
            )
            second_weights = tuple(
                value * second_pattern[index % modulus]
                for index, value in enumerate(sequence)
            )
            first_states = cnf.weighted_sum_states(
                variables,
                first_weights,
                f"root_z{modulus}_s{sequence_index}_first",
            )
            second_states = cnf.weighted_sum_states(
                variables,
                second_weights,
                f"root_z{modulus}_s{sequence_index}_second",
            )
            rows = _root_rows(
                sequence,
                flip_limit,
                modulus,
                first_pattern,
                second_pattern,
                cross_sign,
                first_states,
                second_states,
            )
            modulus_rows += len(rows)
            row_variables = [
                cnf.new_var(
                    f"root_z{modulus}_s{sequence_index}_row_"
                    f"{first}_{second}_{norm}"
                )
                for first, second, norm, _first_sum, _second_sum in rows
            ]
            cnf.exactly_one(
                row_variables, f"root_z{modulus}_s{sequence_index}_rows"
            )
            norm_to_rows: dict[int, list[int]] = defaultdict(list)
            for row, row_variable in zip(rows, row_variables, strict=True):
                first, second, norm, first_sum, second_sum = row
                del first, second
                cnf.add_clause((-row_variable, first_states[first_sum]))
                cnf.add_clause((-row_variable, second_states[second_sum]))
                norm_to_rows[norm].append(row_variable)
            norm_variables = {
                norm: cnf.new_var(
                    f"root_z{modulus}_s{sequence_index}_norm_{norm}"
                )
                for norm in sorted(norm_to_rows)
            }
            cnf.exactly_one(
                tuple(norm_variables.values()),
                f"root_z{modulus}_s{sequence_index}_norms",
            )
            for norm, rows_for_norm in norm_to_rows.items():
                norm_variable = norm_variables[norm]
                for row_variable in rows_for_norm:
                    cnf.add_clause((-row_variable, norm_variable))
            norm_groups.append(norm_variables)
        _add_one_hot_weighted_total(
            cnf, norm_groups, ENERGY, f"root_z{modulus}_energy"
        )
        statistics[f"z{modulus}_allowed_rows"] = modulus_rows
    return statistics


def build_instance_cnf(
    target: MarginTarget,
    radius: int,
    minimum_distance: int,
    pair_bounds: tuple[int, int],
    propagation: str,
    compression: str,
    exchangeable_quad_symmetry: bool,
) -> tuple[CNF, dict[str, int], tuple[tuple[int, ...], ...]]:
    if propagation not in ENCODINGS:
        raise ValueError("unknown propagation mode")
    if compression not in {"none", "z7", "z14", "both"}:
        raise ValueError("unknown compression mode")
    cnf = CNF()
    flips = tuple(
        tuple(
            cnf.new_var(f"flip_{label}_{index}")
            for index in range(len(sequence))
        )
        for label, sequence in zip("abcd", SEED, strict=True)
    )

    cnf.start_section("fixed_margins")
    _add_fixed_margins(cnf, flips, target)

    cnf.start_section("distance")
    flat_flips = tuple(variable for group in flips for variable in group)
    distance_states = cnf.weighted_sum_states(
        flat_flips,
        (1,) * len(flat_flips),
        "hamming_distance",
        lower_bound=0,
        upper_bound=radius,
    )
    allowed_distances = tuple(
        distance_states[value]
        for value in sorted(distance_states)
        if minimum_distance <= value <= radius
    )
    cnf.add_clause(allowed_distances)

    cnf.start_section("endpoint_quad_parity")
    _add_endpoint_quad_parities(cnf, flips)

    minimum_flips = _minimum_flips_by_sequence(target)
    total_minimum = sum(minimum_flips)
    if total_minimum > radius:
        raise ValueError("target is outside the margin Hamming ball")
    extra_pairs = (radius - total_minimum) // 2
    symmetry_comparisons = 0
    if propagation == "cp-sat":
        cnf.start_section("redundant_direction_budgets")
        _add_flip_direction_budgets(
            cnf, flips, target, radius, minimum_distance
        )

        cnf.start_section("redundant_pair_distance_bounds")
        _add_pair_distance_lower_bounds(cnf, flips, pair_bounds, radius)

        if exchangeable_quad_symmetry:
            if compression != "none":
                raise ValueError(
                    "exchangeable quad symmetry is invalid with compression"
                )
            cnf.start_section("exchangeable_quad_symmetry")
            symmetry_comparisons = _add_exchangeable_quad_symmetry(cnf, flips)

    maximum_flips = tuple(
        minimum + 2 * extra_pairs for minimum in minimum_flips
    )

    cnf.start_section("small_root_norms")
    statistics = _add_small_root_invariants(cnf, flips, maximum_flips)
    if compression in {"z7", "both"}:
        cnf.start_section("compression_z7")
        statistics.update(
            _add_length_seven_compression(
                cnf,
                flips,
                maximum_flips,
                coordinate_alternation=False,
            )
        )
    if compression in {"z14", "both"}:
        cnf.start_section("compression_z14")
        statistics.update(
            _add_length_seven_compression(
                cnf,
                flips,
                maximum_flips,
                coordinate_alternation=True,
            )
        )
    statistics.update(
        {
            "primary_flip_variables": len(flat_flips),
            "minimum_margin_distance": total_minimum,
            "extra_flip_pairs": extra_pairs,
            "exchangeable_quad_comparisons": symmetry_comparisons,
            "maximum_flips_a": maximum_flips[0],
            "maximum_flips_b": maximum_flips[1],
            "maximum_flips_c": maximum_flips[2],
            "maximum_flips_d": maximum_flips[3],
        }
    )
    return cnf, statistics, flips


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--result-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--propagation",
        choices=tuple(ENCODINGS),
        default="cp-sat",
        help=(
            "baseline reproduces v1; cp-sat adds independently derived "
            "redundant budgets and exact root-layer symmetry"
        ),
    )
    parser.add_argument(
        "--expect-status",
        choices=("INFEASIBLE", "FEASIBLE", "OPTIMAL", "UNKNOWN", "ANY"),
        default="INFEASIBLE",
        help="guard against exporting the wrong artifact record",
    )
    parser.add_argument(
        "--compression",
        choices=("artifact", "none", "z7", "z14", "both"),
        default="artifact",
        help=(
            "use the artifact layer or soundly strengthen a root instance "
            "with primitive-7/14 compression"
        ),
    )
    parser.add_argument(
        "--pin-stored-witness",
        action="store_true",
        help=(
            "add 334 unit clauses fixing the primary flips to the selected "
            "artifact record's stored sequences"
        ),
    )
    parser.add_argument(
        "--exchangeable-quad-symmetry",
        choices=("auto", "on", "off"),
        default="auto",
        help=(
            "auto enables the exact quotient for v2 root models; off keeps "
            "the unquotiented root model needed to pin arbitrary witnesses"
        ),
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        help="default: OUTPUT with .metadata.json suffix",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload, result, target, artifact_compression = _artifact_instance(
            args.artifact, args.result_index, args.expect_status
        )
        compression = (
            artifact_compression
            if args.compression == "artifact"
            else args.compression
        )
        if artifact_compression != "none" and compression != artifact_compression:
            raise ValueError(
                "compression overrides are supported only for root artifacts"
            )
        if args.exchangeable_quad_symmetry == "auto":
            exchangeable_quad_symmetry = (
                args.propagation == "cp-sat" and compression == "none"
            )
        else:
            exchangeable_quad_symmetry = (
                args.exchangeable_quad_symmetry == "on"
            )
        if exchangeable_quad_symmetry and (
            args.propagation != "cp-sat" or compression != "none"
        ):
            raise ValueError(
                "exchangeable quad symmetry requires a v2 root model"
            )
        radius, minimum_distance, pair_bounds = _validate_instance(
            payload, result, target
        )
        cnf, statistics, flips = build_instance_cnf(
            target,
            radius,
            minimum_distance,
            pair_bounds,
            args.propagation,
            compression,
            exchangeable_quad_symmetry,
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    pinned_witness_sha256 = None
    if args.pin_stored_witness:
        try:
            stored = result.get("sequences")
            if not isinstance(stored, dict):
                raise ValueError("selected artifact result has no stored sequences")
            stored_sequences = tuple(
                tuple(int(value) for value in stored.get(label, ()))
                for label in "abcd"
            )
            if tuple(map(len, stored_sequences)) != tuple(map(len, SEED)):
                raise ValueError("stored witness has the wrong sequence lengths")
            if any(
                value not in (-1, 1)
                for sequence in stored_sequences
                for value in sequence
            ):
                raise ValueError("stored witness contains a non-sign")
            cnf.start_section("pinned_primary_flips")
            for variables, seed, sequence in zip(
                flips, SEED, stored_sequences, strict=True
            ):
                for variable, seed_value, value in zip(
                    variables, seed, sequence, strict=True
                ):
                    cnf.add_clause(
                        (variable,) if value != seed_value else (-variable,)
                    )
            pinned_witness_sha256 = hashlib.sha256(
                json.dumps(
                    {
                        label: list(sequence)
                        for label, sequence in zip(
                            "abcd", stored_sequences, strict=True
                        )
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("ascii")
            ).hexdigest()
        except (ValueError, TypeError) as error:
            print(f"error={error}", file=sys.stderr)
            return 2

    seed_payload = {
        label: list(sequence)
        for label, sequence in zip("abcd", SEED, strict=True)
    }
    seed_sha256 = hashlib.sha256(
        json.dumps(seed_payload, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    encoding = ENCODINGS[args.propagation]
    comments = [
        f"encoding {encoding}",
        f"artifact_sha256 {payload['_sha256']}",
        f"artifact_result_index {args.result_index}",
        f"radius {radius}",
        f"minimum_distance {minimum_distance}",
        f"shard {int(result['shard'])}",
        f"seed_sha256 {seed_sha256}",
    ]
    for label, sequence, variables in zip("abcd", SEED, flips, strict=True):
        for index, (seed_value, variable) in enumerate(
            zip(sequence, variables, strict=True)
        ):
            comments.append(
                f"primary {variable} flip_{label}_{index} seed={seed_value}"
            )
    cnf_sha256 = cnf.write_dimacs(args.output, comments=comments)
    metadata_path = args.metadata or args.output.with_suffix(
        args.output.suffix + ".metadata.json"
    )
    metadata = {
        "kind": "seed-frontier-root-cnf",
        "encoding": encoding,
        "propagation": args.propagation,
        "artifact": str(args.artifact),
        "artifact_sha256": payload["_sha256"],
        "artifact_result_index": args.result_index,
        "artifact_status": result["status"],
        "artifact_compression": artifact_compression,
        "compression": compression,
        "exchangeable_quad_symmetry": exchangeable_quad_symmetry,
        "radius": radius,
        "minimum_distance": minimum_distance,
        "shard": int(result["shard"]),
        "margin_distance": int(result["margin_distance"]),
        "quad_distance": int(result["quad_distance"]),
        "target": [list(pair) for pair in target],
        "seed_sha256": seed_sha256,
        "pinned_stored_witness": args.pin_stored_witness,
        "pinned_witness_sha256": pinned_witness_sha256,
        "cnf": str(args.output),
        "cnf_sha256": cnf_sha256,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "section_clause_counts": cnf.section_clause_counts,
        "statistics": statistics,
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"encoding={encoding}")
    print(f"artifact_sha256={payload['_sha256']}")
    print(f"result_index={args.result_index}")
    print(f"radius={radius} minimum_distance={minimum_distance}")
    print(f"compression={compression}")
    print(f"shard={result['shard']} target={target}")
    print(f"pinned_stored_witness={args.pin_stored_witness}")
    if pinned_witness_sha256 is not None:
        print(f"pinned_witness_sha256={pinned_witness_sha256}")
    print(f"variables={cnf.variable_count}")
    print(f"clauses={len(cnf.clauses)}")
    print(f"cnf_sha256={cnf_sha256}")
    print(f"wrote={args.output}")
    print(f"metadata={metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
