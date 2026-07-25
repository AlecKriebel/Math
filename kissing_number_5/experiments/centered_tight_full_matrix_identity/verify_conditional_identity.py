#!/usr/bin/env python3
"""Exact verifier for the type-conditional full-identity relaxation.

Only Python's standard library and Fraction arithmetic are used.  The
verified object is a pair/triple pseudodistribution, not a labeled matrix.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "conditional_identity_capacity_pseudodistribution.json"
PAIR_SOURCE = (
    HERE.parent
    / "centered_tight_frame_endpoint"
    / "centered_tight_bv_pseudodistribution.json"
)


def common_pair_capacity(projected: Q) -> int | None:
    if projected > 1:
        return 0
    if projected > Q(3, 4):
        return 1
    if projected > Q(2, 3):
        return 2
    if projected > Q(5, 8):
        return 3
    if projected > Q(1, 2):
        return 4
    if projected == Q(1, 2):
        return 6
    return None


def verify(
    certificate_path: Path = CERTIFICATE,
    pair_source_path: Path = PAIR_SOURCE,
) -> dict[str, object]:
    source_bytes = pair_source_path.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "centered-tight-conditional-identity-capacity-"
        "pseudodistribution-v1"
    )
    assert certificate["status"] == (
        "EXACT CONDITIONAL RELAXATION CERTIFICATE; NOT A MATRIX OR CODE"
    )
    assert certificate["source_pair_certificate"] == pair_source_path.name
    assert certificate["source_pair_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["dimension"] == 5
    assert certificate["cardinality"] == 41
    assert "No labeled common-source matrix" in certificate["known_failure"]

    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    assert nodes == [
        Q(-4, 5),
        Q(-3, 4),
        Q(-1, 2),
        Q(-7, 20),
        Q(-3, 10),
        Q(-1, 4),
        Q(-3, 20),
        Q(-1, 20),
        Q(0),
        Q(3, 10),
        Q(1, 2),
    ]
    assert alpha == [2, 2, 4, 2, 2, 2, 2, 8, 2, 2, 12]

    atoms = certificate["atoms"]
    atom_triples = [tuple(atom["triple"]) for atom in atoms]
    weights = [Q(atom["weight"]) for atom in atoms]
    assert len(atoms) == len(set(atom_triples)) == 46
    assert all(weight > 0 for weight in weights)
    assert all(triple in triples for triple in atom_triples)
    weight_of = dict(zip(atom_triples, weights))
    nu = [weight_of.get(triple, Q(0)) for triple in triples]
    assert sum(nu) == 1560

    # Every atomic triple lies in the full closed triangle-Gram domain.
    for triple in atom_triples:
        u, v, t = (nodes[index] for index in triple)
        assert 1 + 2 * u * v * t - u * u - v * v - t * t >= 0

    # Conditional identities, averaged over all base pairs of a fixed
    # inner-product type.  A stored orbit weight is spread uniformly over
    # its distinct ordered permutations.
    conditional_records = []
    for base_index, base in enumerate(nodes):
        mass = Q(0)
        first = Q(0)
        square = Q(0)
        cross = Q(0)
        for triple, weight in zip(triples, nu):
            values = tuple(nodes[index] for index in triple)
            orbit = sorted(set(itertools.permutations(values)))
            coefficient = weight / len(orbit)
            for u, v, t in orbit:
                if t != base:
                    continue
                mass += coefficient
                first += coefficient * u
                square += coefficient * u * u
                cross += coefficient * u * v
        assert mass == 39 * alpha[base_index]
        assert first == alpha[base_index] * (-1 - base)
        assert square == alpha[base_index] * (
            Q(36, 5) - base * base
        )
        assert cross == alpha[base_index] * Q(31, 5) * base

        # This is exactly the off-diagonal B^2 identity after averaging
        # over the base type, with b=1-2t.
        b = 1 - 2 * base
        averaged_b_cross = (
            mass - 4 * first + 4 * cross
        ) / alpha[base_index]
        assert averaged_b_cross == Q(287, 5) - Q(72, 5) * b
        conditional_records.append(
            {
                "base": str(base),
                "mass_per_base_pair": str(mass / alpha[base_index]),
                "b_cross_per_base_pair": str(averaged_b_cross),
            }
        )

    assert sum(weight * node for weight, node in zip(alpha, nodes)) == -1
    assert sum(
        weight * node * node for weight, node in zip(alpha, nodes)
    ) == Q(36, 5)
    triple_cycle = sum(
        weight * nodes[i] * nodes[j] * nodes[k]
        for weight, (i, j, k) in zip(nu, triples)
    )
    assert triple_cycle == Q(1116, 25)

    # The fixed pair measure obeys the robust depth consequences.
    negative_mass = sum(
        weight
        for weight, node in zip(alpha, nodes)
        if node < Q(-1, 300)
    )
    positive_mass = sum(
        weight
        for weight, node in zip(alpha, nodes)
        if node > Q(1, 300)
    )
    assert negative_mass >= 7 and positive_mass >= 7

    # All corrected contiguous-band/exact-stratum capacity inequalities.
    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(
        index for index, node in enumerate(nodes) if node > 0
    )
    stratified_slacks = []
    stratified_positive_bound_slacks = []
    for lower in range(len(nonpositive)):
        for upper in range(lower, len(nonpositive)):
            base_indices = nonpositive[lower : upper + 1]
            base_set = set(base_indices)
            base_upper = nodes[base_indices[-1]]
            for high_index in positive:
                high = nodes[high_index]
                capacity = common_pair_capacity(
                    2 * high * high / (1 + base_upper)
                )
                if capacity is None:
                    continue
                left = sum(
                    weight
                    * sum(
                        triple[position] in base_set
                        and all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    for triple, weight in zip(triples, nu)
                )
                right = (
                    3
                    * capacity
                    * sum(alpha[index] for index in base_indices)
                )
                slack = right - left
                assert slack >= 0
                stratified_slacks.append(slack)
                if right > 0:
                    stratified_positive_bound_slacks.append(slack)
    assert len(stratified_slacks) == 48

    weighted_slacks = []
    for high_index in positive:
        high = nodes[high_index]
        capacities: dict[int, int] = {}
        for base_index, base in enumerate(nodes):
            if base <= 0:
                capacity = common_pair_capacity(
                    2 * high * high / (1 + base)
                )
                if capacity is None:
                    continue
            elif high == Q(1, 2):
                capacity = 7
            else:
                continue
            capacities[base_index] = capacity
        left = sum(
            weight
            * sum(
                triple[position] in capacities
                and all(
                    nodes[triple[other]] >= high
                    for other in range(3)
                    if other != position
                )
                for position in range(3)
            )
            for triple, weight in zip(triples, nu)
        )
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in capacities.items()
        )
        slack = right - left
        assert slack >= 0
        weighted_slacks.append(slack)
    assert len(weighted_slacks) == 2

    # Precise limitation: this sparse conditional witness already fails
    # the k=0 BV node block.  Indices 5 and 8 have diagonal entries two;
    # their off-diagonal entry is the following exact value.
    node_zero = [[Q(0) for _ in nodes] for _ in nodes]
    for index, weight in enumerate(alpha):
        node_zero[index][index] += weight
    index_of = {node: index for index, node in enumerate(nodes)}
    for triple, weight in zip(triples, nu):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        for u, v, _t in orbit:
            node_zero[index_of[u]][index_of[v]] += weight / len(orbit)
    assert node_zero[5][8] == Q(986873711, 120000000)
    negative_bv_minor = (
        node_zero[5][5] * node_zero[8][8] - node_zero[5][8] ** 2
    )
    assert negative_bv_minor == Q(
        -2830461431707995511321694029528648251232619878927921793,
        47487042874438301580423367503413578715200000000000000,
    )
    assert negative_bv_minor < 0

    return {
        "status": "PASS",
        "scope": "exact type-conditional relaxation; not a matrix or code",
        "source_pair_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "positive_triple_orbits": len(atoms),
        "conditional_base_types_checked": len(conditional_records),
        "triple_cycle_moment": str(triple_cycle),
        "robust_negative_pair_mass": str(negative_mass),
        "robust_positive_pair_mass": str(positive_mass),
        "stratified_capacity_rows": len(stratified_slacks),
        "minimum_positive_bound_stratified_slack": str(
            min(stratified_positive_bound_slacks)
        ),
        "weighted_capacity_rows": len(weighted_slacks),
        "minimum_weighted_capacity_slack": str(min(weighted_slacks)),
        "known_negative_bv_order_two_minor": str(negative_bv_minor),
        "conclusion": (
            "type-averaging the complete off-diagonal identity, even with "
            "capacity constraints, does not recover a labeled matrix"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
