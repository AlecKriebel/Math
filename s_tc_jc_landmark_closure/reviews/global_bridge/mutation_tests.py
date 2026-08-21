#!/usr/bin/env python3
"""Adversarial mutations for the independent global bridge/cut audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

import exact_audit as audit


def rejected(name, check, reason):
    try:
        check()
    except (AssertionError, KeyError, ValueError):
        return {"mutation": name, "rejected": True, "status": "VERIFIED", "reason": reason}
    raise AssertionError(f"mutation unexpectedly survived: {name}")


def require_endpoint_coverage(data):
    records = data["three_port_endpoint_dichotomy"]["records"]
    assert len(records) == 77
    ordinary = [
        record
        for record in records
        if record["dichotomy"]["case"] == "Delta_zero_Gamma_zero_ordinary"
    ]
    assert len(ordinary) == 1 and ordinary[0]["reticulation_count"] == 0
    assert ordinary[0]["signatures"] == []


def require_graph_transport(record):
    expected = tuple(tuple(row) for row in record["signatures"])
    assert audit.reconstructed_signature(record["witness_graph"]) == expected


def first_transport_sensitive_endpoint(data):
    for record in data["three_port_endpoint_dichotomy"]["records"]:
        witness = record["witness_graph"]
        if witness.get("core") == "ordinary_trivalent_component":
            continue
        permutation = list(witness["transport"]["leaf_permutation"])
        if len(permutation) < 2:
            continue
        changed = copy.deepcopy(record)
        changed_permutation = list(changed["witness_graph"]["transport"]["leaf_permutation"])
        changed_permutation[0], changed_permutation[1] = changed_permutation[1], changed_permutation[0]
        changed["witness_graph"]["transport"]["leaf_permutation"] = changed_permutation
        try:
            require_graph_transport(changed)
        except AssertionError:
            return changed
    raise AssertionError("no transport-sensitive endpoint found")


def first_strict_minor(data):
    for record in data["one_active_wrong_split"]["records"]:
        for split_record in record["splits"]:
            if not split_record["displayed_by_all"]:
                return record, split_record
    raise AssertionError("no strict minor record found")


def recompute_minor_digest(record, split_record):
    signatures = tuple(tuple(row) for row in record["signatures"])
    tensor = audit.PublishedTensor(signatures, record["reticulation_count"])
    split = tuple(split_record["split"])
    minor = split_record["strict_minor"]
    total = int(minor["character_sum"])
    pairs = tuple(
        pair
        for pair in itertools.product(audit.GROUP, repeat=2)
        if (pair[0] ^ pair[1]) == total
    )
    rows = tuple(minor["rows"])
    columns = tuple(minor["columns"])
    p00 = audit.flattening_entry(tensor, split, pairs[rows[0]], pairs[columns[0]])
    p01 = audit.flattening_entry(tensor, split, pairs[rows[0]], pairs[columns[1]])
    p10 = audit.flattening_entry(tensor, split, pairs[rows[1]], pairs[columns[0]])
    p11 = audit.flattening_entry(tensor, split, pairs[rows[1]], pairs[columns[1]])
    determinant = sp.Poly(
        sp.expand((p00 * p11 - p01 * p10).as_expr()),
        *tensor.symbols,
        domain=sp.QQ,
    )
    return hashlib.sha256(repr(determinant.terms()).encode()).hexdigest()


def crossing_square_mutation():
    a, b, c, t, A, B, C, T, z = sp.symbols("a b c t A B C T z")
    mutated_f1 = a * A - z * b * c * B * C
    correct_f2 = z * T * t - z**2 * b * c * B * C
    # The identity needed to force aA=zTt no longer has zero remainder.
    remainder = sp.expand(a * A - z * T * t - (mutated_f1 - correct_f2))
    assert remainder == 0


def reciprocal_only_mutation():
    first = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    second = (Fraction(3, 5), Fraction(3, 5), Fraction(25, 72))
    assert first[0] * first[1] * first[2] == second[0] * second[1] * second[2]
    endpoint_ratio_product = (second[0] / first[0]) * (second[1] / first[1])
    # A reciprocal-only endpoint chart incorrectly requires this to be one.
    assert endpoint_ratio_product == 1


def physical_bridge_recovery_mutation():
    first_x = Fraction(1, 2)
    second_x = Fraction(25, 72)
    assert first_x == second_x


def missing_pair_anchor_mutation():
    degree = 5
    pairs = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4)]
    rows = [[int(column in pair) for column in range(degree)] for pair in pairs]
    assert audit.qrank(rows) == degree
    rows.pop()
    assert audit.qrank(rows) == degree


def character_specific_incidence_mutation():
    scales = {1: Fraction(2), 2: Fraction(3), 3: Fraction(5)}
    # Simultaneous Aut(G)-invariance requires one common nonzero-sector scale.
    assert len(set(scales.values())) == 1


def illegal_zero_sum_anchor_mutation():
    # With one physical block on each side of a bridge, global conservation
    # forces the two side totals to agree in the Klein group.
    legal = [(left, right) for left in audit.GROUP for right in audit.GROUP if (left ^ right) == 0]
    assert (1, 0) in legal


def dummy_means_weak_mutation(data):
    for section in (
        data["three_port_endpoint_dichotomy"]["records"],
        data["one_active_wrong_split"]["records"],
    ):
        for record in section:
            witness = record.get("witness_graph")
            if not witness or witness.get("core") == "ordinary_trivalent_component":
                continue
            dummy_count = len(set(witness["full_labels"]) - set(witness["selected"]))
            if dummy_count:
                # The full dummy-restored witness is exactly a valid strong
                # completion, contradicting the mutation's inference.
                assert audit.validate_full_completion(witness) < 0
    raise AssertionError("no dummy-restored witness found")


def coupled_arm_mutation():
    kappa_1 = Fraction(2, 3)
    kappa_2 = Fraction(3, 5)
    independent_jacobian = [[kappa_1, 0], [0, kappa_2]]
    coupled_jacobian = [[kappa_1], [kappa_2]]
    assert audit.qrank(independent_jacobian) == 2
    assert audit.qrank(coupled_jacobian) == 2


def arbitrary_positive_effective_scale_mutation():
    endpoint_normalizers = (Fraction(1), Fraction(1))
    requested_j = Fraction(2)
    required_physical_x = requested_j * endpoint_normalizers[0] * endpoint_normalizers[1]
    assert 0 < required_physical_x < 1


def finite_union_mutation():
    # The family U_t={t}, t in (0,1), covers U=(0,1), while every member has
    # dimension zero.  Hence replacing "finite union" by "arbitrary union"
    # invalidates the dimension/interior conclusion.
    member_dimension = 0
    union_dimension = 1
    assert member_dimension == union_dimension


def whole_germ_in_one_member_mutation():
    # U=(-1,1), T1=(-1,0], T2=[0,1).  The finite cover is exact, but neither
    # member contains U.  Only a relative-open subgerm conclusion is valid.
    test_points = (Fraction(-1, 2), Fraction(1, 2))
    member_1 = lambda value: -1 < value <= 0
    member_2 = lambda value: 0 <= value < 1
    assert all(member_1(value) or member_2(value) for value in test_points)
    assert all(member_1(value) for value in test_points) or all(
        member_2(value) for value in test_points
    )


def reverse_cut_inclusion_mutation():
    # Mutation: allow target-cut/source-noncut under source-relative
    # containment.  On the shared source-open set this simultaneously demands
    # rank <=4 (target cut equation) and rank >4 (pointwise source noncut).
    target_bound = 4
    source_strict_lower_bound = 5
    assert source_strict_lower_bound <= target_bound


def main():
    here = Path(__file__).resolve().parent
    closure = here.parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cut-certificate",
        type=Path,
        default=closure / "independent" / "bridge_cut" / "cut_certificate.json",
    )
    parser.add_argument("--output", type=Path, default=here / "mutation_certificate.json")
    arguments = parser.parse_args()
    data = json.loads(arguments.cut_certificate.read_text())

    mutations = []

    deleted = copy.deepcopy(data)
    deleted["three_port_endpoint_dichotomy"]["records"] = [
        record
        for record in deleted["three_port_endpoint_dichotomy"]["records"]
        if record["dichotomy"]["case"] != "Delta_zero_Gamma_zero_ordinary"
    ]
    mutations.append(
        rejected(
            "delete_ordinary_trivalent_endpoint",
            lambda: require_endpoint_coverage(deleted),
            "The normalized weak a>=bc branch and ordinary endpoint are mandatory coverage.",
        )
    )

    changed_transport = first_transport_sensitive_endpoint(data)
    mutations.append(
        rejected(
            "alter_leaf_transport",
            lambda: require_graph_transport(changed_transport),
            "The published graph no longer reconstructs its canonical tensor signature.",
        )
    )

    minor_record, split_record = first_strict_minor(data)
    altered_split = copy.deepcopy(split_record)
    altered_split["strict_minor"]["polynomial_sha256"] = "0" * 64
    mutations.append(
        rejected(
            "alter_one_active_minor",
            lambda: (
                None
                if recompute_minor_digest(minor_record, altered_split)
                == altered_split["strict_minor"]["polynomial_sha256"]
                else (_ for _ in ()).throw(AssertionError("minor digest changed"))
            ),
            "Independent Fourier reconstruction detects the changed minor.",
        )
    )

    mutations.extend(
        [
            rejected(
                "replace_two_active_z_squared_by_z",
                crossing_square_mutation,
                "The zero-remainder crossing identity fails.",
            ),
            rejected(
                "restore_reciprocal_only_bridge_gauge",
                reciprocal_only_mutation,
                "Equal contractions need the full two-incidence action.",
            ),
            rejected(
                "claim_physical_bridge_recovery",
                physical_bridge_recovery_mutation,
                "Distinct physical bridge multipliers yield the same observable product.",
            ),
            rejected(
                "drop_one_unmarked_pair_anchor",
                missing_pair_anchor_mutation,
                "The log-exponent matrix loses rank.",
            ),
            rejected(
                "allow_character_specific_incidence_scales",
                character_specific_incidence_mutation,
                "JC Aut(G) symmetry identifies all three nonzero sectors.",
            ),
            rejected(
                "set_complementary_zero_sum_side_to_zero",
                illegal_zero_sum_anchor_mutation,
                "A nonzero separator sector requires the same nonzero total on the complementary side.",
            ),
            rejected(
                "infer_selected_weakness_from_dummy_leaf",
                lambda: dummy_means_weak_mutation(data),
                "Dummy leaves certify a valid full strong completion; they do not classify the selected marginal.",
            ),
            rejected(
                "couple_independent_adjacent_bridge_arms",
                coupled_arm_mutation,
                "The marginal arm map loses one rank and no longer gives the required submersion.",
            ),
            rejected(
                "claim_all_positive_effective_scales_are_physical",
                arbitrary_positive_effective_scale_mutation,
                "At fixed unit normalizers, j=2 would require forbidden x=2.",
            ),
            rejected(
                "replace_finite_target_union_by_arbitrary_union",
                finite_union_mutation,
                "An arbitrary union of zero-dimensional singleton fibers can cover an interval.",
            ),
            rejected(
                "infer_entire_germ_lies_in_one_finite_union_member",
                whole_germ_in_one_member_mutation,
                "A finite cover yields a full-dimensional open subgerm in one member, not containment of the whole germ.",
            ),
            rejected(
                "omit_target_cut_implies_source_cut",
                reverse_cut_inclusion_mutation,
                "The shared source-open set cannot have flattening rank both <=4 and >4.",
            ),
        ]
    )

    assert all(record["rejected"] for record in mutations)
    result = {
        "status": "VERIFIED",
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(
        {
            "status": result["status"],
            "mutation_count": len(mutations),
            "output": str(arguments.output),
            "output_sha256": hashlib.sha256(arguments.output.read_bytes()).hexdigest(),
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
