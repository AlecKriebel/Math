#!/usr/bin/env python3
"""Audit the 37,194-pair quotient for order-7 side gluing."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import automorphism7_side_orbit_cover as one_side


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_lines(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def global_action(
    edge_table: dict[tuple[int, int], int],
    vertex_image: tuple[int, ...],
) -> dict[int, int]:
    variable_image: dict[int, int] = {}
    for (left, right), variable in edge_table.items():
        new_edge = tuple(sorted((vertex_image[left], vertex_image[right])))
        new_variable = edge_table[new_edge]
        if (
            variable in variable_image
            and variable_image[variable] != new_variable
        ):
            raise AssertionError("vertex map is not well-defined on edge orbits")
        variable_image[variable] = new_variable
    if (
        set(variable_image) != set(range(1, 130))
        or set(variable_image.values()) != set(range(1, 130))
    ):
        raise AssertionError("global action is not a variable bijection")
    return variable_image


def mapped_clause_set(
    clauses: tuple[tuple[int, ...], ...],
    variable_image: dict[int, int],
    complement: bool,
) -> set[tuple[int, ...]]:
    return {
        tuple(
            sorted(
                (
                    variable_image[abs(literal)]
                    if (literal > 0) != complement
                    else -variable_image[abs(literal)]
                )
                for literal in clause
            )
        )
        for clause in clauses
    }


def vertex_permutation(
    *,
    block_permutation: tuple[int, ...] = (0, 1, 2, 3, 4, 5),
    shifts: tuple[int, ...] = (0, 0, 0, 0, 0, 0),
    multiplier: int = 1,
) -> tuple[int, ...]:
    image = []
    for vertex in range(42):
        block, offset = divmod(vertex, 7)
        image.append(
            block_permutation[block] * 7
            + (multiplier * offset + shifts[block]) % 7
        )
    image.append(42)
    if sorted(image) != list(range(43)):
        raise AssertionError("not a vertex permutation")
    return tuple(image)


def units_for_pair(
    left_model: int,
    right_model: int,
    fixed_units: list[int],
    map_a: list[int],
    map_b: list[int],
) -> set[int]:
    units = set(fixed_units)
    units.update(
        variable if left_model >> index & 1 else -variable
        for index, variable in enumerate(map_a)
    )
    # The second side model describes the complement of the actual induced
    # graph on the fixed vertex's nonneighbors.
    units.update(
        -variable if right_model >> index & 1 else variable
        for index, variable in enumerate(map_b)
    )
    if len(units) != 66 or len({abs(literal) for literal in units}) != 66:
        raise AssertionError("pair does not fix 66 distinct variables")
    return units


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    edge_orbits, side_table = one_side.side_edge_orbits()
    side_clauses = one_side.side_formula(side_table)
    side_models = one_side.enumerate_models(side_clauses)
    h_actions = {
        one_side.edge_variable_permutation(
            edge_orbits,
            side_table,
            block_permutation,
            (0, shift_1, shift_2),
        )
        for block_permutation in itertools.permutations(range(3))
        for shift_1 in range(7)
        for shift_2 in range(7)
    }
    k_actions = tuple(
        one_side.edge_variable_permutation(
            edge_orbits, side_table, (0, 1, 2), (0, 0, 0), multiplier
        )
        for multiplier in range(1, 7)
    )
    if len(h_actions) != 294 or len(set(k_actions)) != 6:
        raise AssertionError("unexpected side action count")

    side_class: dict[int, int] = {}
    class_representatives: list[int] = []
    for model in sorted(side_models):
        if model in side_class:
            continue
        orbit = {
            one_side.transform_bits(model, action) for action in h_actions
        }
        if not orbit <= side_models or orbit & side_class.keys():
            raise AssertionError("H-orbit coverage failed")
        class_index = len(class_representatives)
        for image in orbit:
            side_class[image] = class_index
        class_representatives.append(min(orbit))
    if len(side_class) != 191394 or len(class_representatives) != 664:
        raise AssertionError("unexpected H quotient")

    class_multiplier_actions: list[tuple[int, ...]] = []
    for action in k_actions:
        class_action = tuple(
            side_class[one_side.transform_bits(model, action)]
            for model in class_representatives
        )
        if sorted(class_action) != list(range(664)):
            raise AssertionError("multiplier does not permute H-classes")
        class_multiplier_actions.append(class_action)

    pair_representatives: list[tuple[int, int]] = []
    covered_unordered_pairs: set[tuple[int, int]] = set()
    for left_class in range(664):
        for right_class in range(left_class, 664):
            pair = (left_class, right_class)
            if pair in covered_unordered_pairs:
                continue
            orbit = {
                tuple(sorted((action[left_class], action[right_class])))
                for action in class_multiplier_actions
            }
            representative = min(orbit)
            if pair != representative:
                raise AssertionError("pair traversal reached a noncanonical orbit first")
            pair_representatives.append(pair)
            covered_unordered_pairs.update(orbit)
    if len(covered_unordered_pairs) != 664 * 665 // 2:
        raise AssertionError("unordered H-class pair coverage failed")
    if len(pair_representatives) != 37194:
        raise AssertionError("unexpected pair quotient size")

    variable_count, global_clauses = one_side.parse_dimacs(args.cnf)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if variable_count != 129 or not isinstance(metadata, dict):
        raise ValueError("unexpected global formula")
    edge_table = one_side.global_edge_table(metadata)
    global_clause_set = {
        tuple(sorted(clause)) for clause in global_clauses
    }
    if len(global_clause_set) != len(global_clauses):
        raise AssertionError("duplicate global clause")

    generator_specs: list[tuple[str, tuple[int, ...], bool]] = []
    for side_name, first_block in (("A", 0), ("B", 3)):
        for relative_block in (1, 2):
            shifts = [0] * 6
            shifts[first_block + relative_block] = 1
            generator_specs.append(
                (
                    f"{side_name}_shift_{relative_block}",
                    vertex_permutation(shifts=tuple(shifts)),
                    False,
                )
            )
        for transposition in ((0, 1), (1, 2)):
            blocks = list(range(6))
            left = first_block + transposition[0]
            right = first_block + transposition[1]
            blocks[left], blocks[right] = blocks[right], blocks[left]
            generator_specs.append(
                (
                    f"{side_name}_swap_{transposition[0]}_{transposition[1]}",
                    vertex_permutation(block_permutation=tuple(blocks)),
                    False,
                )
            )
    generator_specs.append(
        (
            "common_multiplier_3",
            vertex_permutation(multiplier=3),
            False,
        )
    )
    side_swap_blocks = (3, 4, 5, 0, 1, 2)
    generator_specs.append(
        (
            "side_swap_with_color_complement",
            vertex_permutation(block_permutation=side_swap_blocks),
            True,
        )
    )

    fixed_orbits = sorted(
        {
            variable
            for (left, right), variable in edge_table.items()
            if right == 42
        },
        key=lambda variable: min(
            left
            for (left, right), observed in edge_table.items()
            if right == 42 and observed == variable
        ),
    )
    fixed_units = fixed_orbits[:3] + [
        -variable for variable in fixed_orbits[3:]
    ]
    map_a = [edge_table[orbit[0]] for orbit in edge_orbits]
    map_b = [
        edge_table[(orbit[0][0] + 21, orbit[0][1] + 21)]
        for orbit in edge_orbits
    ]

    generator_checks: list[dict[str, object]] = []
    side_swap_variable_image: dict[int, int] | None = None
    for name, vertex_image, complement in generator_specs:
        variable_image = global_action(edge_table, vertex_image)
        mapped = mapped_clause_set(
            global_clauses, variable_image, complement
        )
        mapped_fixed_units = {
            (
                variable_image[abs(literal)]
                if (literal > 0) != complement
                else -variable_image[abs(literal)]
            )
            for literal in fixed_units
        }
        check = {
            "name": name,
            "color_complement": complement,
            "variable_bijection": True,
            "cnf_invariant": mapped == global_clause_set,
            "missing_clause_count": len(mapped - global_clause_set),
            "extra_clause_count": len(global_clause_set - mapped),
            "fixed_units_invariant": mapped_fixed_units == set(fixed_units),
        }
        generator_checks.append(check)
        if not check["cnf_invariant"] or not check["fixed_units_invariant"]:
            raise AssertionError(f"global generator check failed: {name}")
        if name == "side_swap_with_color_complement":
            side_swap_variable_image = variable_image
    assert side_swap_variable_image is not None

    # Check the sign convention, not only the abstract clause symmetry, on
    # every retained pair representative.
    for left_class, right_class in pair_representatives:
        left_model = class_representatives[left_class]
        right_model = class_representatives[right_class]
        units = units_for_pair(
            left_model, right_model, fixed_units, map_a, map_b
        )
        swapped_units = {
            (
                side_swap_variable_image[abs(literal)]
                if literal < 0
                else -side_swap_variable_image[abs(literal)]
            )
            for literal in units
        }
        expected = units_for_pair(
            right_model, left_model, fixed_units, map_a, map_b
        )
        if swapped_units != expected:
            raise AssertionError("side swap does not implement pair reversal")

    pair_lines = [
        f"{left_class},{right_class}"
        for left_class, right_class in pair_representatives
    ]
    class_model_lines = [
        format(model, "030b") for model in class_representatives
    ]
    result = {
        "audit": "order43_automorphism7_side_pair_orbit_cover_v1",
        "evidence_label": "EXACT ACTION AND FINITE-QUOTIENT REPLAY",
        "claim_boundary": (
            "This verifies the pair quotient relative to the proof-free "
            "enumeration of 191,394 side models. It does not determine any "
            "pair formula and is not an UNSAT certificate."
        ),
        "dependency": {
            "path": str(Path(one_side.__file__).resolve()),
            "sha256": sha256_file(Path(one_side.__file__)),
        },
        "cnf": {
            "path": str(args.cnf.resolve()),
            "sha256": sha256_file(args.cnf),
            "variable_count": variable_count,
            "clause_count": len(global_clauses),
        },
        "metadata": {
            "path": str(args.metadata.resolve()),
            "sha256": sha256_file(args.metadata),
        },
        "side_model_count": len(side_models),
        "h_action_count": len(h_actions),
        "h_class_count": len(class_representatives),
        "h_class_representative_sha256": sha256_lines(class_model_lines),
        "ordered_h_class_pair_count": len(class_representatives) ** 2,
        "unordered_h_class_pair_count": len(covered_unordered_pairs),
        "pair_orbit_count": len(pair_representatives),
        "pair_schedule_sha256": sha256_lines(pair_lines),
        "pair_schedule_first": pair_lines[0],
        "pair_schedule_last": pair_lines[-1],
        "generator_checks": generator_checks,
        "side_swap_pair_unit_checks": len(pair_representatives),
        "coverage_valid": (
            len(side_models) == 191394
            and len(class_representatives) == 664
            and len(pair_representatives) == 37194
            and all(
                check["cnf_invariant"] and check["fixed_units_invariant"]
                for check in generator_checks
            )
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["coverage_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
