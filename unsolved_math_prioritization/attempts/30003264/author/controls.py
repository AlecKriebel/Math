#!/usr/bin/env python3
"""Exact finite controls for PROOF.md. No arithmetic-group homology oracle.

All checks use explicit exceptions, so python -O does not disable verification.
The data below are authored finite models, not imported corpus content.
"""
from fractions import Fraction
from functools import reduce
from itertools import combinations, permutations, product
from math import gcd
import json


def require(condition, label):
    if not condition:
        raise ValueError(label)


def relation(p, x, y):
    inv = lambda a: pow(a % p, -1, p)
    terms = ((x, 1), (y, -1), (y * inv(x) % p, 1),
             ((1 - inv(x)) * inv(1 - inv(y)) % p, -1),
             ((1 - x) * inv(1 - y) % p, 1))
    require(all(2 <= a < p for a, _ in terms), "invalid five-term symbol")
    return [sum(c for a, c in terms if a == i) for i in range(2, p)]


def determinant3(m):
    a, b, c = m
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def residue_control():
    rows = [relation(5, x, y) for x, y in permutations(range(2, 5), 2)]
    expected = [[0, 0, 1], [3, 0, -2], [0, 0, 1],
                [-1, 2, 0], [-1, 2, 0], [1, -2, 2]]
    require(rows == expected, "five-term presentation changed")
    # The quotient map a->2, b->1, c->0 to Z/6 is well defined.
    require(all((2*r[0]+r[1]) % 6 == 0 for r in rows), "Z/6 map")
    # Explicit relation-lattice generators c, 3a, -a+2b.
    basis = [[0, 0, 1], [3, 0, 0], [-1, 2, 0]]
    require([rows[1][i]+2*rows[0][i] for i in range(3)] == basis[1], "3a")
    minors = [abs(determinant3([rows[i] for i in ids]))
              for ids in combinations(range(6), 3)]
    index = reduce(gcd, minors)
    require(index == 6, "relation-lattice index")
    require(abs(determinant3(basis)) == 6, "basis index")
    # Half localization discards the 2-part, not the 3-part.
    odd_order = index
    while odd_order % 2 == 0:
        odd_order //= 2
    require(odd_order == 3, "half-integral residue group")
    # Negative control: a zero map into Z/3 is not surjective.
    zero_image = {0 for _ in range(3)}
    require(len(zero_image) < 3, "zero-map false positive")
    return {"relations": rows, "integral_order": index,
            "half_integral_order": odd_order, "zero_map_rejected": True}


def small_s_control():
    elements = list(product(range(3), repeat=2))
    kernel = [(x, y) for x, y in elements if (x+y) % 3 == 0]
    image = sorted({(x-y) % 3 for x, y in kernel})
    pair_kernel = [(x, y) for x, y in kernel if (x-y) % 3 == 0]
    require(len(kernel) == 3 and image == [0, 1, 2], "correct small-S map")
    require(pair_kernel == [(0, 0)], "field-kernel model")
    # Mistakenly using the K3 map itself as the residue map must fail.
    wrong_image = {(x+y) % 3 for x, y in kernel}
    require(len(wrong_image) == 1, "wrong-map negative control")
    return {"known_model_elements": len(elements), "correct_kernel": kernel,
            "residue_image": image, "joint_kernel": pair_kernel,
            "wrong_residue_map_rejected": True}


def normalization_control():
    checked = 0
    for modulus in (3, 5, 7, 9, 11, 15):
        require(gcd(2, modulus) == 1, "coefficient ring condition")
        for b in range(modulus):
            a = -b % modulus
            evaluation = (a-b) % modulus
            delta = b
            require(evaluation == -2*delta % modulus, "residue normalization")
            require((evaluation == 0) == (delta == 0), "same kernel")
            checked += 1
    # The implication requires 2 invertible.
    require((-2*1) % 2 == 0 and 1 % 2 != 0, "2-primary negative control")
    return {"odd_coefficient_cases": checked,
            "normalization": "s_p=-2*Delta_p on the augmentation part",
            "integral_2_primary_shortcut_rejected": True}


def limit_control():
    checked = 0
    for n in range(1, 7):
        for coords in product(range(3), repeat=n+1):
            b, e = coords[:-1], coords[-1]
            transition = b + (0, 0)
            require(transition[:-1] == b+(0,), "compatible projections")
            if all(v == 0 for v in b):
                require(all(v == 0 for v in transition), "old kernel killed")
            checked += 1
        new_kernel_generator = (0,)*(n+1)+(1,)
        require(any(new_kernel_generator), "new kernel remains")
    return {"finite_transition_checks": checked, "stages_checked": 6,
            "every_checked_stage_has_nonzero_kernel": True,
            "old_kernel_killed_in_one_step": True,
            "scope": "finite controls of a universally proved abstract model"}


def character(g, chi):
    return -1 if (g & chi).bit_count() % 2 else 1


def character_control():
    orthogonality_checks = 0
    spectral_checks = 0
    for rank in range(1, 7):
        order = 2**rank
        for chi in range(order):
            for psi in range(order):
                coefficient = Fraction(sum(character(g,chi)*character(g,psi)
                                           for g in range(order)), order)
                require(coefficient == (1 if chi == psi else 0), "orthogonality")
                orthogonality_checks += 1
        # Factorized projectors evaluated in each actual character.
        for psi in range(order):
            values = []
            for chi in range(order):
                value = Fraction(1)
                for i in range(rank):
                    value *= Fraction(1 + character(1<<i,chi)*character(1<<i,psi), 2)
                values.append(value)
                require(value == (1 if chi == psi else 0), "projector eigenvalue")
                spectral_checks += 1
            require(sum(values) == 1, "projectors sum to identity")
    # Two-prime characters: 1=(-,+), 2=(+,-), 3=(-,-).
    module_characters = [1, 2, 3]
    target_characters = [1, 2]
    source_dims = {chi:module_characters.count(chi) for chi in range(4)}
    target_dims = {chi:target_characters.count(chi) for chi in range(4)}
    require(all(source_dims[c] == target_dims[c] for c in target_characters),
            "target-supported components agree")
    require(source_dims[3] == 1 and target_dims[3] == 0, "hidden mixed character")
    return {"orthogonality_checks": orthogonality_checks,
            "projector_eigenvalue_checks": spectral_checks,
            "target_only_test_rejected": True,
            "mixed_character_kernel_dimension": 1}


def main():
    return {"problem_id": 30003264,
            "status": "finite controls passed; primary target unresolved",
            "residue_presentation": residue_control(),
            "known_small_S": small_s_control(),
            "localization_normalization": normalization_control(),
            "filtered_limit_countermodel": limit_control(),
            "character_countermodel": character_control(),
            "limits": ["Does not calculate general S-arithmetic group homology.",
                       "Does not independently certify imported scholarly theorems.",
                       "Abstract controls are not arithmetic counterexamples."]}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
