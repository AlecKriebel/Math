"""Exact controls for the Markov-tower obstruction, not boundary realization.

No external packages, randomness fixed, no sampled conclusion about an infinite
space. The cellular models below are two-dimensional mapping-cylinder prototypes.
"""
import json
import random
from fractions import Fraction
from exact_linear import eye, mm, rank, zeros
from simplicial import barycentric, boundaries, closure

rng = random.Random(62000045)
counts = {}


def check(condition, category):
    assert condition, category
    counts[category] = counts.get(category, 0) + 1


def change_of_basis(n):
    u, inv = eye(n), eye(n)
    for _ in range(12):
        if n < 2:
            break
        i, j = rng.sample(range(n), 2)
        a = rng.choice([-3, -2, -1, 1, 2, 3])
        u[i] = [x + a * y for x, y in zip(u[i], u[j])]
        for row in inv:
            row[j] -= a * row[i]
    check(mm(u, inv) == eye(n), "unimodular_inverse")
    return u, inv


def nullspace(a, p):
    """Return a matrix whose columns form the mod-p nullspace; a is nonempty."""
    m, n = len(a), len(a[0])
    a = [[x % p for x in row] for row in a]
    pivots = []
    row = 0
    for col in range(n):
        k = next((k for k in range(row, m) if a[k][col]), None)
        if k is None:
            continue
        a[row], a[k] = a[k], a[row]
        z = pow(a[row][col], -1, p)
        a[row] = [x * z % p for x in a[row]]
        for k in range(m):
            if k != row:
                z = a[k][col]
                a[k] = [(x - z * y) % p for x, y in zip(a[k], a[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    free = [j for j in range(n) if j not in pivots]
    ans = zeros(n, len(free))
    for col, j in enumerate(free):
        ans[j][col] = 1
        for k, pivot in enumerate(pivots):
            ans[pivot][col] = -a[k][j] % p
    return ans


def modzero(a, p):
    return all(x % p == 0 for row in a for x in row)


# The simplified relative CW chain complex replaces each triangle by the
# mapping cylinder of a degree-p circle map. Collapse its connecting edge,
# leaving one new core loop per face and one 2-cell with boundary old_d2 - p*a.
# This is a relative homotopy model, not a claim of a simplicial no-square nerve.
disk = closure([(0, 1, 2)])
sphere = closure([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)])
models = []
for name, k in [("disk", disk), ("sphere", sphere)]:
    for subdivision in range(2):
        if subdivision:
            k, _ = barycentric(k)
        cs, ds = boundaries(k)
        d1, d2 = ds
        faces, edges, vertices = len(cs[2]), len(cs[1]), len(cs[0])
        boundary_edge_rows = [i for i, row in enumerate(d2)
                              if sum(bool(x) for x in row) == 1]
        interior = [i for i in range(edges) if i not in boundary_edge_rows]
        original_top = faces - rank(d2, 2)
        check(original_top == int(name == "sphere"), "seed_global_top")
        for p in [2, 3, 5, 7]:
            new_d1 = [row + [0] * faces for row in d1]
            new_d2 = d2 + [[-p * int(i == j) for j in range(faces)]
                           for i in range(faces)]
            check(mm(new_d1, new_d2) == zeros(vertices, faces), "cellular_chain_identity")
            check(new_d2[:edges] == d2, "collapse_chain_map")
            check(faces - rank(new_d2, p) == original_top, "prime_top_preserved")
            check(faces - rank(new_d2) == 0, "rational_top_zero")
            for ell in [2, 3, 5, 7, 11]:
                expected = original_top if ell == p else 0
                check(faces - rank(new_d2, ell) == expected, "field_profile")
            if name == "disk":
                relative_d2 = [d2[i] for i in interior] + new_d2[edges:]
                check(faces - rank(relative_d2, p) == 1, "disk_relative_top_survives")
                check(faces - rank(relative_d2) == 0, "disk_relative_rational_top_zero")
            models.append({"seed": name, "subdivision": subdivision,
                           "prime": p, "two_cells": faces,
                           "global_top_mod_p": original_top})

# beta * delta_tilde = delta * alpha. Invertibility of alpha and beta
# gives the induced kernel isomorphism used in the exact-sequence argument.
kernel_models = 0
for p in [2, 3, 5, 7]:
    for v in range(1, 7):
        for e in range(1, 7):
            for _ in range(4):
                delta = [[rng.randrange(p) for _ in range(v)] for _ in range(e)]
                alpha, alpha_inv = change_of_basis(v)
                beta, beta_inv = change_of_basis(e)
                tilde = mm(mm(beta_inv, delta), alpha)
                check(mm(beta, tilde) == mm(delta, alpha), "commutative_square")
                kernel = nullspace(tilde, p)
                image = mm(alpha, kernel)
                nullity = v - rank(delta, p)
                check(modzero(mm(tilde, kernel), p), "source_kernel")
                check(modzero(mm(delta, image), p), "target_kernel")
                check(rank(image, p) == nullity, "kernel_isomorphism")
                check(v - rank(tilde, p) == nullity, "equal_nullities")
                kernel_models += 1

# These controls test the hypotheses, not infinite-limit existence.
for p in [2, 3, 5, 7]:
    for n in range(1, 7):
        product = eye(n)
        for _ in range(10):
            u, _ = change_of_basis(n)
            product = mm(u, product)
            check(rank(product, p) == n, "isomorphism_system_persistence")
            check(mm(product, zeros(n, 1)) == zeros(n, 1), "zero_seed_stays_zero")
for n in range(2, 31):
    check((Fraction(2, n + 1) < Fraction(2, 3)) == (n >= 3), "shifted_strict_ratio")

print(json.dumps({
    "assertions": sum(counts.values()),
    "categories": counts,
    "cellular_prototypes": models,
    "kernel_models": kernel_models,
    "scope": "Exact finite algebra and two-dimensional cellular controls; no hyperbolic group or higher-dimensional Markov block is constructed computationally."
}, indent=2, sort_keys=True))
