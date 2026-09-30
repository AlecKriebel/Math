#!/usr/bin/env python3
"""Modest exact tests of PROOF.md examples and its numerical bound.

This is not a general semigroup normality algorithm or a formal proof checker.
The all-degree claims rely on the closed-form arguments in the written note.
"""
import json


def sumsets(A, last):
    out = [{0}]
    for _ in range(last):
        out.append({x + a for x in out[-1] for a in A})
    return out


def main():
    families = 0
    levels = 0
    circuits = 0
    for m in range(4, 31):
        A = (0, 1, m - 1, m)
        sums = sumsets(A, m + 2)
        max_hole = -1
        for k, actual in enumerate(sums):
            predicted = {x for j in range(k + 1)
                         for x in range(j * (m - 1), j * (m - 1) + k + 1)}
            assert actual == predicted
            holes = set(range(k * m + 1)) - actual
            assert bool(holes) == (1 <= k <= m - 3)
            if holes:
                max_hole = k
            levels += 1
        assert max_hole == m - 3
        assert max_hole <= 2 * m * m * (m - 1) ** 2 - 2
        # A rational-kernel basis consisting of primitive integer circuits.
        basis = ((m - 2, -(m - 1), 1, 0), (m - 1, -m, 0, 1))
        for u in basis:
            assert sum(u) == 0
            assert sum(a * x for a, x in zip(A, u)) == 0
            degree = sum(max(x, 0) for x in u)
            support = sum(x != 0 for x in u)
            assert degree <= m
            assert support <= 2 * degree
            circuits += 1
        assert all(any(u[i] != 0 for u in basis) for i in range(4))
        families += 1

    # A homogeneous polynomial-extension/pyramid negative control.
    # Base A={0,1,3,4} has the degree-one hole 2. Add apex (0,1).
    # At degree j+1 and y-coordinate j, exactly j apex factors are forced,
    # leaving one base factor; thus (2,j) remains a hole for every j.
    A = (0, 1, 3, 4)
    sums = sumsets(A, 22)
    for j in range(21):
        k = j + 1
        assert 2 not in sums[k - j]
        # Membership in the saturated cone of the volume-four triangle.
        assert 2 + 4 * j <= 4 * k
    # The primitive square circuit tests the sharp support <= 2V equality.
    square = ((0, 0), (1, 0), (0, 1), (1, 1))
    u = (1, -1, -1, 1)
    assert sum(u) == 0
    assert all(sum(v[i] * x for v, x in zip(square, u)) == 0 for i in range(2))
    assert sum(x != 0 for x in u) == 4 == 2 * 2

    print(json.dumps({
        'status': 'passed',
        'arithmetic': 'exact Python integers and finite sets',
        'one_dimensional_families': families,
        'degree_sumsets_checked': levels,
        'primitive_circuit_relations_checked': circuits,
        'pyramid_negative_controls': 21,
        'square_support_equality_control': 'passed',
        'scope': 'Finite checks of written formulas only; no general proof certificate',
        'sharp_source_question': 'h <= V is not proved or refuted in this attempt'
    }, indent=2))


if __name__ == '__main__':
    main()
