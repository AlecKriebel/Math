#!/usr/bin/env python3
"""Exact S5 highest-weight-carrier census for the corrected DTH lift.

This file is developed as a dependency-free exact verifier.  It constructs
Specht modules of S_5 as integer polytabloids in qutrit word modules, applies
the first-Pluecker and combined Omega constraints, and computes the exact
inertia of the lifted minimal witness.  The corrected mixed-support ranks are
then evaluated on the blocks with negative witness spectrum.

The census is a highest-weight-carrier census.  The companion note carefully
separates it from a complete census over every Schur-carrier index.
"""

from fractions import Fraction as F
from itertools import combinations, permutations, product
import sys


PARTITIONS = (
    (5,),
    (4, 1),
    (3, 2),
    (3, 1, 1),
    (2, 2, 1),
)

PRIME = 1_000_003


# (raw dimension, first-Pluecker dimension, combined-Omega kernel dimension,
#  exact O0 inertia).  Keys are unordered triples in PARTITIONS order.
EXPECTED = {
    ((5,), (5,), (5,)): (1, 0, 0, (0, 0, 0)),
    ((5,), (5,), (4, 1)): (4, 0, 0, (0, 0, 0)),
    ((5,), (5,), (3, 2)): (5, 1, 1, (1, 0, 0)),
    ((5,), (5,), (3, 1, 1)): (6, 0, 0, (0, 0, 0)),
    ((5,), (5,), (2, 2, 1)): (5, 1, 1, (1, 0, 0)),
    ((5,), (4, 1), (4, 1)): (16, 1, 1, (1, 0, 0)),
    ((5,), (4, 1), (3, 2)): (20, 2, 2, (2, 0, 0)),
    ((5,), (4, 1), (3, 1, 1)): (24, 2, 2, (2, 0, 0)),
    ((5,), (4, 1), (2, 2, 1)): (20, 2, 2, (2, 0, 0)),
    ((5,), (3, 2), (3, 2)): (25, 2, 2, (2, 0, 0)),
    ((5,), (3, 2), (3, 1, 1)): (30, 2, 2, (2, 0, 0)),
    ((5,), (3, 2), (2, 2, 1)): (25, 2, 2, (2, 0, 0)),
    ((5,), (3, 1, 1), (3, 1, 1)): (36, 4, 4, (4, 0, 0)),
    ((5,), (3, 1, 1), (2, 2, 1)): (30, 2, 2, (2, 0, 0)),
    ((5,), (2, 2, 1), (2, 2, 1)): (25, 2, 2, (2, 0, 0)),
    ((4, 1), (4, 1), (4, 1)): (64, 5, 5, (5, 0, 0)),
    ((4, 1), (4, 1), (3, 2)): (80, 7, 7, (6, 1, 0)),
    ((4, 1), (4, 1), (3, 1, 1)): (96, 8, 8, (7, 1, 0)),
    ((4, 1), (4, 1), (2, 2, 1)): (80, 7, 7, (6, 1, 0)),
    ((4, 1), (3, 2), (3, 2)): (100, 8, 8, (7, 1, 0)),
    ((4, 1), (3, 2), (3, 1, 1)): (120, 10, 10, (8, 2, 0)),
    ((4, 1), (3, 2), (2, 2, 1)): (100, 8, 8, (6, 2, 0)),
    ((4, 1), (3, 1, 1), (3, 1, 1)): (144, 12, 12, (9, 3, 0)),
    ((4, 1), (3, 1, 1), (2, 2, 1)): (120, 10, 10, (7, 2, 1)),
    ((4, 1), (2, 2, 1), (2, 2, 1)): (100, 8, 8, (5, 2, 1)),
    ((3, 2), (3, 2), (3, 2)): (125, 11, 11, (8, 3, 0)),
    ((3, 2), (3, 2), (3, 1, 1)): (150, 12, 12, (8, 4, 0)),
    ((3, 2), (3, 2), (2, 2, 1)): (125, 11, 11, (7, 3, 1)),
    ((3, 2), (3, 1, 1), (3, 1, 1)): (180, 16, 16, (11, 5, 0)),
    ((3, 2), (3, 1, 1), (2, 2, 1)): (150, 12, 12, (7, 5, 0)),
    ((3, 2), (2, 2, 1), (2, 2, 1)): (125, 11, 11, (5, 5, 1)),
    ((3, 1, 1), (3, 1, 1), (3, 1, 1)): (216, 16, 16, (9, 5, 2)),
    ((3, 1, 1), (3, 1, 1), (2, 2, 1)): (180, 16, 15, (9, 5, 1)),
    ((3, 1, 1), (2, 2, 1), (2, 2, 1)): (150, 12, 12, (6, 5, 1)),
    ((2, 2, 1), (2, 2, 1), (2, 2, 1)): (125, 11, 10, (4, 6, 0)),
}


# Exact modular support ranks already replayed.  Every recorded rank is full.
SUPPORT_RANKS = {
    ((4, 1), (4, 1), (3, 2)): (49, 49),
    ((4, 1), (4, 1), (3, 1, 1)): (64, 64),
    ((4, 1), (4, 1), (2, 2, 1)): (49, 49),
    ((4, 1), (3, 2), (3, 2)): (64, 64),
    ((4, 1), (3, 2), (3, 1, 1)): (100, 100),
    ((4, 1), (3, 2), (2, 2, 1)): (64, 64),
    ((4, 1), (3, 1, 1), (3, 1, 1)): (144, 144),
    ((4, 1), (3, 1, 1), (2, 2, 1)): (100, 100),
    ((4, 1), (2, 2, 1), (2, 2, 1)): (64, 64),
    ((3, 2), (3, 2), (3, 2)): (121, 121),
    ((3, 2), (3, 2), (3, 1, 1)): (144, 144),
    ((3, 2), (3, 2), (2, 2, 1)): (121, 121),
    ((3, 2), (3, 1, 1), (3, 1, 1)): (256, 256),
    ((3, 2), (3, 1, 1), (2, 2, 1)): (144, 144),
}


def add(*vectors):
    out = {}
    for v in vectors:
        for k, x in v.items():
            out[k] = out.get(k, F(0)) + x
            if not out[k]:
                del out[k]
    return out


def scale(c, v):
    c = F(c)
    return {k: c * x for k, x in v.items() if c * x}


def inner(v, w):
    if len(v) > len(w):
        v, w = w, v
    return sum((x * w.get(k, F(0)) for k, x in v.items()), F(0))


def permutation_sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i + 1, len(p))) % 2 else 1


def transposition(a, b):
    p = list(range(5))
    p[a], p[b] = p[b], p[a]
    return tuple(p)


def permute_word(word, p):
    out = [None] * 5
    for old in range(5):
        out[p[old]] = word[old]
    return tuple(out)


def apply_local_perm(v, site, p):
    out = {}
    for key, x in v.items():
        q = list(key)
        q[site] = permute_word(q[site], p)
        q = tuple(q)
        out[q] = out.get(q, F(0)) + x
    return {k: x for k, x in out.items() if x}


def apply_global_perm(v, p):
    out = v
    for site in range(3):
        out = apply_local_perm(out, site, p)
    return out


def standard_tableaux(shape):
    cells = [(r, c) for r, length in enumerate(shape) for c in range(length)]
    out = []
    for values in permutations(range(5)):
        tab = {cell: values[i] for i, cell in enumerate(cells)}
        good = True
        for r, length in enumerate(shape):
            if any(tab[(r, c)] >= tab[(r, c + 1)] for c in range(length - 1)):
                good = False
                break
        if not good:
            continue
        for c in range(max(shape)):
            rows = [r for r, length in enumerate(shape) if c < length]
            if any(tab[(rows[i], c)] >= tab[(rows[i + 1], c)]
                   for i in range(len(rows) - 1)):
                good = False
                break
        if good:
            out.append(tab)
    return out


def polytabloid(shape, tableau):
    columns = []
    for c in range(max(shape)):
        columns.append(tuple(tableau[(r, c)] for r, length in enumerate(shape)
                             if c < length))
    base_word = [None] * 5
    for (r, _), label in tableau.items():
        base_word[label] = r
    out = {}
    choices = [tuple(permutations(col)) for col in columns]
    for images in product(*choices):
        p = list(range(5))
        sign = 1
        for col, image in zip(columns, images):
            local = tuple(col.index(x) for x in image)
            sign *= permutation_sign(local)
            for old, new in zip(col, image):
                p[old] = new
        word = permute_word(tuple(base_word), tuple(p))
        out[word] = out.get(word, F(0)) + sign
    return {k: x for k, x in out.items() if x}


def specht_basis(shape):
    return [polytabloid(shape, t) for t in standard_tableaux(shape)]


def tensor3(x, y, z):
    return {(a, b, c): p * q * r
            for a, p in x.items() for b, q in y.items() for c, r in z.items()
            if p * q * r}


def global_pair_project(v, a, b, antisymmetric=True):
    t = apply_global_perm(v, transposition(a, b))
    return scale(F(1, 2), add(v, scale(-1 if antisymmetric else 1, t)))


def global_A4(v):
    out = {}
    for q in permutations(range(4)):
        p = tuple(q) + (4,)
        out = add(out, scale(permutation_sign(q), apply_global_perm(v, p)))
    return scale(F(1, 24), out)


def source_project(v):
    out = global_pair_project(v, 0, 1, True)
    out = global_pair_project(out, 2, 3, True)
    swap = apply_global_perm(out, (2, 3, 0, 1, 4))
    out = scale(F(1, 2), add(out, swap))
    return add(out, scale(-1, global_A4(out)))


def local_pair_antisym(v, site, a, b):
    t = apply_local_perm(v, site, transposition(a, b))
    return scale(F(1, 2), add(v, scale(-1, t)))


def product_pair_antisym(v, a, b):
    out = v
    for site in range(3):
        out = local_pair_antisym(out, site, a, b)
    return out


def O0(v, first):
    return add(scale(F(1, 4), v), scale(-2, product_pair_antisym(v, first, 4)))


def lifted_O0(v):
    return scale(F(1, 2), add(O0(v, 0), O0(v, 2)))


def state_at(key, replica):
    return tuple(word[replica] for word in key)


def state_index(state):
    k = 0
    for x in state:
        k = 3 * k + x
    return k


def wedge_coordinates(v):
    """Canonical coordinates in Lambda^2(H)_12 x Lambda^2(H)_34 x H_5."""
    out = {}
    for key, x in v.items():
        states = tuple(state_index(state_at(key, r)) for r in range(5))
        a, b, c, d, z = states
        if a < b and c < d:
            out[((a, b), (c, d), z)] = x
    return {k: x for k, x in out.items() if x}


def epsilon(i, p, q):
    if len({i, p, q}) < 3:
        return 0
    return permutation_sign((i, p, q))


def omega_half(v, first):
    """Raw epsilon contraction on (first, first+1, 5), retaining other pair."""
    retained = (2, 3) if first == 0 else (0, 1)
    out = {}
    for key, x in v.items():
        coeff = 1
        for word in key:
            coeff *= epsilon(word[4], word[first], word[first + 1])
        if not coeff:
            continue
        row = (state_index(state_at(key, retained[0])),
               state_index(state_at(key, retained[1])))
        out[row] = out.get(row, F(0)) + coeff * x
    return {k: x for k, x in out.items() if x}


def combined_omega(v):
    return add(omega_half(v, 0), omega_half(v, 2))


def exact_column_echelon(columns):
    """Return independent indices and exact kernel relations among columns."""
    pivots = {}
    independent = []
    kernel = []
    for j, column in enumerate(columns):
        v = dict(column)
        relation = {j: F(1)}
        while v:
            pivot = min(v)
            if pivot not in pivots:
                inv = F(1) / v[pivot]
                v = {k: inv * x for k, x in v.items() if inv * x}
                relation = {k: inv * x for k, x in relation.items() if inv * x}
                pivots[pivot] = (v, relation)
                independent.append(j)
                break
            old_v, old_relation = pivots[pivot]
            c = v[pivot]
            v = add(v, scale(-c, old_v))
            relation = add(relation, scale(-c, old_relation))
        else:
            kernel.append(relation)
    return independent, kernel


def frac_mod(x, p=PRIME):
    return x.numerator % p * pow(x.denominator % p, -1, p) % p


def modular_rank(columns, p=PRIME):
    pivots = {}
    rank = 0
    for column in columns:
        v = {k: frac_mod(x, p) for k, x in column.items() if frac_mod(x, p)}
        while v:
            pivot = min(v)
            if pivot not in pivots:
                inv = pow(v[pivot], -1, p)
                v = {k: x * inv % p for k, x in v.items() if x * inv % p}
                pivots[pivot] = v
                rank += 1
                break
            c = v[pivot]
            old = pivots[pivot]
            for k, x in old.items():
                y = (v.get(k, 0) - c * x) % p
                if y:
                    v[k] = y
                elif k in v:
                    del v[k]
    return rank


def support_pt_column(vi, vj):
    """Mixed support contraction of PT_A(|vi><vj|)."""
    lookup = {}
    for (a, pair_bprime, zprime), y in vj.items():
        p, q = a
        lookup.setdefault(p, []).append((q, 1, pair_bprime, zprime, y))
        lookup.setdefault(q, []).append((p, -1, pair_bprime, zprime, y))
    out = {}
    for (a_prime, pair_b, z), x in vi.items():
        for other, sign, pair_bprime, zprime, y in lookup.get(z, ()):
            row = (pair_b, other, a_prime, pair_bprime, zprime)
            out[row] = out.get(row, F(0)) + sign * x * y
    return {k: x for k, x in out.items() if x}


def support_rank(good_basis):
    wedge_basis = [wedge_coordinates(v) for v in good_basis]
    # Stream columns.  Retaining all d^2 large sparse outputs simultaneously
    # caused multi-gigabyte memory use on dense three-row carriers.
    columns = (support_pt_column(x, y) for x in wedge_basis for y in wedge_basis)
    return modular_rank(columns), len(wedge_basis) ** 2


def linear_combination(coefficients, vectors):
    out = {}
    for j, c in coefficients.items():
        out = add(out, scale(c, vectors[j]))
    return out


def symmetric_inertia(matrix):
    """Exact congruence inertia of a rational symmetric matrix."""
    a = [list(map(F, row)) for row in matrix]
    pos = neg = zero = 0
    while a:
        n = len(a)
        diagonal = next((i for i in range(n) if a[i][i]), None)
        if diagonal is not None:
            if diagonal:
                a[0], a[diagonal] = a[diagonal], a[0]
                for row in a:
                    row[0], row[diagonal] = row[diagonal], row[0]
            pivot = a[0][0]
            pos += pivot > 0
            neg += pivot < 0
            a = [[a[i][j] - a[i][0] * a[0][j] / pivot
                  for j in range(1, n)] for i in range(1, n)]
            continue
        off = next(((i, j) for i in range(n) for j in range(i + 1, n)
                    if a[i][j]), None)
        if off is None:
            zero += n
            break
        i, j = off
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[r][c] for c in order] for r in order]
        b = a[0][1]
        pos += 1
        neg += 1
        # Inverse of [[0,b],[b,0]] is [[0,1/b],[1/b,0]].
        a = [[a[r][c] - (a[r][0] * a[1][c] + a[r][1] * a[0][c]) / b
              for c in range(2, n)] for r in range(2, n)]
    return pos, neg, zero


def block_data(shapes, bases):
    raw = [tensor3(x, y, z) for x in bases[shapes[0]]
           for y in bases[shapes[1]] for z in bases[shapes[2]]]
    projected = [source_project(v) for v in raw]
    src_indices, _ = exact_column_echelon(projected)
    src_basis = [projected[j] for j in src_indices]
    omega_columns = [combined_omega(v) for v in src_basis]
    _, omega_kernel = exact_column_echelon(omega_columns)
    good_basis = [linear_combination(q, src_basis) for q in omega_kernel]
    q = [[inner(good_basis[i], lifted_O0(good_basis[j]))
          for j in range(len(good_basis))] for i in range(len(good_basis))]
    inertia = symmetric_inertia(q)
    return len(raw), len(src_basis), len(good_basis), inertia, good_basis


def unordered_triples(items):
    for i in range(len(items)):
        for j in range(i, len(items)):
            for k in range(j, len(items)):
                yield (items[i], items[j], items[k])


def shape_name(shape):
    return "".join(map(str, shape))


def main():
    bases = {shape: specht_basis(shape) for shape in PARTITIONS}
    expected = {(5,): 1, (4, 1): 4, (3, 2): 5, (3, 1, 1): 6, (2, 2, 1): 5}
    assert {s: len(b) for s, b in bases.items()} == expected

    triples = list(unordered_triples(PARTITIONS))
    assert set(triples) == set(EXPECTED) and len(triples) == 35

    if "--full" in sys.argv:
        print("shape triple | raw | Pluecker | Omega kernel | O0 inertia (+,-,0) | support")
        for shapes in triples:
            raw, src, good, inertia, good_basis = block_data(shapes, bases)
            observed = (raw, src, good, inertia)
            assert observed == EXPECTED[shapes], (shapes, observed, EXPECTED[shapes])
            sr = None
            if "--support" in sys.argv and inertia[1]:
                sr = support_rank(good_basis)
                if shapes in SUPPORT_RANKS:
                    assert sr == SUPPORT_RANKS[shapes]
            label = "/".join(shape_name(s) for s in shapes)
            print(f"{label:13s} {raw:4d} {src:4d} {good:4d} {inertia} {sr}", flush=True)
        return

    # Quick exact replay: the original cloud obstruction block.  The full
    # 35-row calculation is deterministic but deliberately opt-in because the
    # densest three-row polytabloid carriers take several minutes.
    key = ((4, 1), (4, 1), (3, 2))
    raw, src, good, inertia, good_basis = block_data(key, bases)
    assert (raw, src, good, inertia) == EXPECTED[key]
    sr = support_rank(good_basis)
    assert sr == SUPPORT_RANKS[key]

    print("exact highest-weight S5 DTH block census checkpoint")
    print("35 recorded unordered partition triples")
    print("19 have negative O0 spectrum")
    print(f"14 negative carriers have replayed full mixed-support rank modulo {PRIME}")
    print("quick replay 41/41/32:", EXPECTED[key], "support", sr)
    print("use --full to replay all 35 inertia rows")
    print("use --full --support to recompute negative support ranks (memory bounded, slow)")


if __name__ == "__main__":
    main()
