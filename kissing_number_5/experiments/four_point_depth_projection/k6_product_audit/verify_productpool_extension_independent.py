#!/usr/bin/env python3
"""Exact independent audit of the 74-atom product-valid K6 mixture."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from experiments.four_point_depth_projection.centered_quarter_pair_depth import (
    verify as direction_audit,
)
from experiments.four_point_depth_projection.k6_product_audit import (
    verify_direct_k6_product_semantics as semantics,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CERTIFICATE = Path(__file__).with_name("productpool_extension.json")

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CERTIFICATE_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)
SEMANTICS_SHA256 = (
    "0f178d357f70a40974a760cda1dca32c393c6bd5628ec6660fdb861f9a3e8922"
)
ATOM_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstring(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def verify(
    source_path: Path = SOURCE,
    certificate_path: Path = CERTIFICATE,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(certificate_path) == CERTIFICATE_SHA256
    assert digest(Path(semantics.__file__).resolve()) == SEMANTICS_SHA256

    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "kissing5.rank5_k6_product_extension.v1"
    )
    assert certificate["source_sha256"] == SOURCE_SHA256
    assert certificate["source_certificate"] == str(
        source_path.relative_to(ROOT)
    )

    grid = tuple(Q(value) for value in source["grid"])
    scaled_grid = tuple(int(4 * value) for value in grid)
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert all(Q(value, 4) == node for value, node in zip(scaled_grid, grid))

    pool_path = ROOT / certificate["pool_file"]
    assert digest(pool_path) == certificate["pool_sha256"]
    active = tuple(certificate["active_pool_indices"])
    assert len(active) == len(set(active)) == 74
    assert tuple(sorted(active)) == active

    atoms = certificate["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert len(atoms) == len(weights) == certificate[
        "positive_atom_count"
    ] == 74
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    parsed_atoms = []
    edge_marginal = [Q(0)] * len(grid)
    triangle_marginal = [Q(0)] * len(triples)
    canonical_atoms = set()
    orbit_sizes: Counter[int] = Counter()
    minimum_principal = {size: None for size in range(1, 7)}
    minimum_positive_fifth = None
    for atom, weight in zip(atoms, weights):
        edges = tuple(atom[ATOM_KEY])
        assert len(edges) == 15
        assert all(0 <= color < len(grid) for color in edges)
        matrix = semantics.scaled_gram(edges, scaled_grid)
        minors = semantics.principal_determinants(matrix)
        assert all(
            value >= 0 for values in minors.values() for value in values
        )
        assert minors[6] == [0]
        positive_fifth = [value for value in minors[5] if value > 0]
        assert positive_fifth
        local_fifth = min(positive_fifth)
        minimum_positive_fifth = (
            local_fifth
            if minimum_positive_fifth is None
            else min(minimum_positive_fifth, local_fifth)
        )
        for size, values in minors.items():
            local = min(values)
            old = minimum_principal[size]
            minimum_principal[size] = (
                local if old is None else min(old, local)
            )

        feature = semantics.triangle_indices(edges, triple_index)
        assert feature == tuple(atom["triangle_orbit_indices"])
        canonical, orbit_size = semantics.canonical_orbit(edges)
        assert canonical not in canonical_atoms
        canonical_atoms.add(canonical)
        orbit_sizes[orbit_size] += 1
        for color in edges:
            edge_marginal[color] += weight
        for index in feature:
            triangle_marginal[index] += weight
        parsed_atoms.append((edges, weight))

    assert edge_marginal == [3 * value / 8 for value in alpha]
    assert triangle_marginal == [value / 78 for value in nu]
    assert minimum_principal[6] == 0
    assert minimum_positive_fifth is not None

    # Authenticate every selected pool row.
    selected_lines = {}
    with pool_path.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == certificate["pool_header"]
        wanted = set(active)
        for column, line in enumerate(stream):
            if column in wanted:
                selected_lines[column] = tuple(map(int, line.split(",")))
    assert set(selected_lines) == set(active)
    for column, atom in zip(active, atoms):
        fields = selected_lines[column]
        assert len(fields) == 35
        assert fields[:15] == tuple(atom[ATOM_KEY])
        assert fields[15:] == tuple(atom["triangle_orbit_indices"])

    states_by_base = {}
    feasible_by_base = {}
    for base_index in range(1, len(grid)):
        states, _coverage, feasible = semantics.state_audit.direction_states(
            base_index, grid, triples
        )
        states_by_base[base_index] = states
        feasible_by_base[base_index] = feasible

    families = semantics.state_audit.capacity_families(grid)
    rows_checked = 0
    zero_keys = []
    minimum_positive = None
    family_reports = []
    for family_index, (
        base_index,
        threshold_index,
        bound,
    ) in enumerate(families):
        feasible = feasible_by_base[base_index]
        for edges, _weight in parsed_atoms:
            edge = semantics.edge_map(edges)
            for first, second in semantics.PAIRS6:
                if edge[(first, second)] != base_index:
                    continue
                for vertex in range(6):
                    if vertex in (first, second):
                        continue
                    pair = (
                        edge[tuple(sorted((first, vertex)))],
                        edge[tuple(sorted((second, vertex)))],
                    )
                    assert pair in feasible
                    assert (pair[1], pair[0]) in feasible

        family_minimum = None
        family_zeros = 0
        for state_index, (required, table) in enumerate(
            states_by_base[base_index]
        ):
            slack = sum(
                weight
                * semantics.atom_state_slack_twice(
                    edges,
                    base_index,
                    threshold_index,
                    bound,
                    required,
                    table,
                )
                for edges, weight in parsed_atoms
            )
            assert slack >= 0
            rows_checked += 1
            family_minimum = (
                slack
                if family_minimum is None
                else min(family_minimum, slack)
            )
            if slack == 0:
                family_zeros += 1
                zero_keys.append([family_index, state_index, required])
            elif minimum_positive is None or slack < minimum_positive:
                minimum_positive = slack
        family_reports.append(
            {
                "base_inner_product": qstring(grid[base_index]),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "direction_states": len(states_by_base[base_index]),
                "zero_rows": family_zeros,
                "minimum_twice_symmetrized_slack": qstring(
                    family_minimum
                ),
            }
        )

    assert rows_checked == 560
    assert zero_keys == certificate["zero_product_row_keys"]
    assert len(zero_keys) == 113
    assert minimum_positive is not None and minimum_positive > 0
    assert [
        {
            "base_inner_product": item["base_inner_product"],
            "high_threshold": item["high_threshold"],
            "capacity": item["capacity"],
            "distinct_direction_states": item["direction_states"],
        }
        for item in family_reports
    ] == certificate["product_family_summary"]

    # The previously violated symmetric negative-sum row is now exact
    # equality.
    base_index = grid.index(Q(-1, 4))
    threshold_index = grid.index(Q(1, 2))
    table = tuple(
        int(
            direction_audit.direction_qualifies(
                first,
                second,
                Q(-1, 4),
                (Q(-1), Q(-1)),
            )
        )
        for first in grid
        for second in grid
    )
    negative_sum_slack = sum(
        weight
        * semantics.atom_state_slack_twice(
            edges,
            base_index,
            threshold_index,
            3,
            7,
            table,
        )
        for edges, weight in parsed_atoms
    )
    assert negative_sum_slack == 0

    return {
        "status": "PASS",
        "conclusion": (
            "the 74-atom rank-exact-five K6 mixture exactly repairs the "
            "stored extension and passes all 560 depth/common product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "pool_sha256": certificate["pool_sha256"],
        "positive_atoms": len(atoms),
        "rank": "every atom exactly 5",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "orbit_size_histogram": {
            str(size): count for size, count in sorted(orbit_sizes.items())
        },
        "edge_marginal": "exact 3*alpha/8; uniform edge alpha/40",
        "triangle_marginal": "exact nu/78; uniform face nu/1560",
        "rows_checked": rows_checked,
        "zero_rows": len(zero_keys),
        "minimum_positive_twice_symmetrized_slack": qstring(
            minimum_positive
        ),
        "formerly_violated_negative_sum_slack": "0",
        "family_reports": family_reports,
        "scope": (
            "positive local rank-five K6 marginal certificate over an "
            "incomplete discovery pool; not a global 41-point code and "
            "not a six-point Lasserre moment-PSD certificate"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
