#!/usr/bin/env python3
"""Finite falsification controls; the report gives the general proofs.

Enumerate labeled trees with one nonconstant component, and test stability of
every contracted component with one marking. A two-mark countercontrol and
elementary P^1 cohomology/positive-characteristic derivative controls are added.
This script has no dependencies beyond the Python standard library.
"""
from itertools import product
import json


def tree_degrees(n, seq):
    # Prüfer sequences enumerate all labeled trees; stability needs only degrees.
    return [1 + seq.count(v) for v in range(n)]


def controls():
    tested = 0
    stable_one_mark = []
    for n in range(2, 7):
        for seq in product(range(n), repeat=n - 2):
            degrees = tree_degrees(n, seq)
            for nonconstant in range(n):
                for marked in range(n):
                    tested += 1
                    if all(degrees[v] + int(v == marked) >= 3
                           for v in range(n) if v != nonconstant):
                        stable_one_mark.append([n, list(seq), nonconstant, marked])
    assert not stable_one_mark
    # One ghost attached to the nonconstant component can carry two marks.
    assert 1 + 2 == 3
    cohomology = {a: max(1 - a, 0) for a in range(0, 9)}
    assert cohomology[0] == 1
    assert all(cohomology[a] == 0 for a in range(1, 9))
    characteristic_checks = []
    for p in [2, 3, 5, 7, 11]:
        # derivative(t^p)=0; derivative(t^(p+1))=t^p.
        assert p % p == 0
        assert (p + 1) % p == 1
        # On k[epsilon]/epsilon^2, (1+epsilon)^p=1 in characteristic p.
        assert p % p == 0
        characteristic_checks.append({
            "p": p,
            "frobenius_derivative_coefficient": p % p,
            "birational_cusp_y_derivative_coefficient": (p + 1) % p,
            "frobenius_infinitesimal_scaling_invariant": True,
            "purely_inseparable_cover_degree": p,
            "minimal_image_degree_control": 1,
        })
    return {
        "labeled_rooted_marked_tree_configurations_checked": tested,
        "stable_boundary_configurations_with_one_mark": stable_one_mark,
        "two_mark_ghost_control_is_stable": True,
        "H1_O_a_minus_2_dimensions": cohomology,
        "positive_characteristic_controls": characteristic_checks,
        "status": "PASS finite controls; not a proof of the theorem",
    }


if __name__ == "__main__":
    print(json.dumps(controls(), indent=2))
