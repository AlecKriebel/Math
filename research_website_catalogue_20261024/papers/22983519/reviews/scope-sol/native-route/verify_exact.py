#!/usr/bin/env python3
"""Standard-library exact check of the pointwise curvature obstruction.

No assertions or floats. The input tensor is the product-curvature formula;
verify_symbolic.py independently derives it from the coordinate metric.
This script does not certify the analytic first-variation argument.
"""
from fractions import Fraction
from itertools import product


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        found = next((r for r in range(pivot, len(a)) if a[r][col]), None)
        if found is None:
            continue
        a[pivot], a[found] = a[found], a[pivot]
        scale = a[pivot][col]
        a[pivot] = [x / scale for x in a[pivot]]
        for r in range(len(a)):
            if r != pivot and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def delta(i, j):
    return int(i == j)


def space_form(i, j, k, ell):
    # Component ell of R(e_i,e_j)e_k, sectional curvature +1.
    return delta(j, k) * delta(i, ell) - delta(i, k) * delta(j, ell)


def cylinder(i, j, k, ell):
    return space_form(i, j, k, ell) if max(i, j, k, ell) < 2 else 0


def system(n, tensor):
    equations, rhs = [], []
    for i, j, k, ell in product(range(n), repeat=4):
        row = [0] * (n * n)
        row[ell * n + i] += delta(j, k)
        row[ell * n + j] -= delta(i, k)
        equations.append(row)
        rhs.append(tensor(i, j, k, ell))
    return equations, rhs


def main():
    for n in (3, 4, 5):
        coefficients, rhs = system(n, cylinder)
        r = rank(coefficients)
        augmented = rank([row + [b] for row, b in zip(coefficients, rhs)])
        require((r, augmented) == (n * n, n * n + 1), "Obstruction failed")
        print(f"PASS cylinder n={n}: ranks {r} < {augmented}; no endomorphism A")

    # Controls: the same linear solver must accept known compatible tensors.
    for curvature in (0, 1, -1):
        coefficients, rhs = system(3, lambda i, j, k, ell:
                                   curvature * space_form(i, j, k, ell))
        a = [curvature * delta(ell, i) for ell in range(3) for i in range(3)]
        require(all(sum(x * y for x, y in zip(row, a)) == b
                    for row, b in zip(coefficients, rhs)), "Control residual")
        require(rank(coefficients) == rank([row + [b] for row, b
                                          in zip(coefficients, rhs)]),
                "Compatible control rejected")
        print(f"PASS constant sectional curvature {curvature}: A={curvature}I")

    # n=2 sphere is a boundary control; do not claim the three-vector argument.
    coefficients, rhs = system(2, cylinder)
    require(rank(coefficients) == rank([row + [b] for row, b
                                      in zip(coefficients, rhs)]),
            "Dimension-two boundary control rejected")
    ricci = [[sum(cylinder(i, j, k, i) for i in range(3))
              for k in range(3)] for j in range(3)]
    require(ricci == [[1, 0, 0], [0, 1, 0], [0, 0, 0]], "Ricci mismatch")
    component = Fraction(cylinder(2, 0, 0, 2)) - Fraction(ricci[0][0], 2)
    require(component == Fraction(-1, 2), "Projective Weyl mismatch")
    print("PASS dimension-two sphere control; no obstruction claimed there")
    print("PASS Ricci=diag(1,1,0); W(e3,e1)e1=-e3/2")
    print("All exact pointwise checks passed. See paper for the analytic proof.")


if __name__ == "__main__":
    main()
