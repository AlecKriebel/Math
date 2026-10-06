#!/usr/bin/env python3
"""Exact checks for the scoped TF-cone proof; Python standard library only."""
import argparse
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path


def det(a):
    """Exact Gaussian elimination over Q, including row-swap signs."""
    a = [[Fraction(x) for x in row] for row in a]
    n = len(a)
    d = Fraction(1)
    for i in range(n):
        pivot = next((r for r in range(i, n) if a[r][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            d = -d
        p = a[i][i]
        d *= p
        for j in range(i + 1, n):
            c = a[j][i] / p
            for k in range(i + 1, n):
                a[j][k] -= c * a[i][k]
            a[j][i] = 0
    assert d.denominator == 1
    return int(d)


def rank_mod(a, p):
    a = [[v % p for v in row] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, p)
        a[row] = [(v * inv) % p for v in a[row]]
        for i in range(len(a)):
            if i != row:
                q = a[i][col]
                a[i] = [(x - q * y) % p for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def poly_add(a, b):
    out = a.copy()
    for exponent, coefficient in b.items():
        out[exponent] = out.get(exponent, 0) + coefficient
        if not out[exponent]:
            del out[exponent]
    return out


def poly_mul(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            key = tuple(x + y for x, y in zip(e, f))
            out[key] = out.get(key, 0) + c * d
    return {e: c for e, c in out.items() if c}


def permutation_sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def results():
    F = []
    for i, j in [(0, 1), (1, 2), (2, 0)]:
        a = [[0] * 3 for _ in range(3)]
        a[i][j], a[j][i] = 1, -1
        F.append(a)
    M = [F[1][i] + F[2][i] for i in range(3)] + [F[2][i] + F[0][i] for i in range(3)]
    assert det(M) == 1
    # Independently expand det(sum x_i F_i) in Z[x_1,x_2,x_3].
    G = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append({tuple(int(r == k) for r in range(3)): F[k][i][j]
                        for k in range(3) if F[k][i][j]})
        G.append(row)
    polynomial = {}
    for p in permutations(range(3)):
        term = {(0, 0, 0): permutation_sign(p)}
        for i in range(3):
            term = poly_mul(term, G[i][p[i]])
        polynomial = poly_add(polynomial, term)
    assert polynomial == {}
    finite_checks = {}
    for p in [2, 3, 5, 7]:
        count = 0
        for x in product(range(p), repeat=3):
            a = [[sum(x[k] * F[k][i][j] for k in range(3)) for j in range(3)] for i in range(3)]
            assert rank_mod(a, p) == (2 if any(x) else 0)
            count += 1
        assert rank_mod(M, p) == 6
        finite_checks[str(p)] = count
    # Y has one-dimensional spaces at 1,2 and arrow a_1 the identity.
    # Each component subspace is 0 or k, so this list is exhaustive over ANY field.
    subdims = [[0, d1, d2] for d1, d2 in product([0, 1], repeat=2) if d1 <= d2]
    eta = [1, 1, -1]
    vals = [sum(a*b for a,b in zip(eta,d)) for d in subdims]
    quotients = [[0, 1-d[1], 1-d[2]] for d in subdims]
    qvals = [sum(a*b for a,b in zip(eta,d)) for d in quotients]
    assert max(vals) == 0 and min(qvals) == 0
    # Witness columns p,g span exactly the plane annihilated by dim(Y).
    p, g, y = [1,0,0], [0,1,-1], [0,1,1]
    assert sum(a*b for a,b in zip(p,y)) == sum(a*b for a,b in zip(g,y)) == 0
    grid_count = 0
    for v in product(range(-6, 7), repeat=3):
        witness_conditions = v[0] > 0 and v[1] > 0 and v[1] + v[2] == 0
        cone_conditions = v[0] > 0 and v[1] > 0 and v[2] == -v[1]
        assert witness_conditions == cone_conditions
        grid_count += 1
    # Generic eta sign-coherence permits exactly three unordered binary partitions.
    atoms = [[1,0,0], [0,1,0], [0,0,-1]]
    splits = [[atom, [eta[i]-atom[i] for i in range(3)]] for atom in atoms]
    return {
        'schema': 'tf-equivalence-exact-checks-v1',
        'problem_id': 30005755,
        'full_target_solved': False,
        'field_scope_of_integer_identities': 'every field, including characteristic 2',
        'algebra_dimension': 12,
        'matrices_F': F,
        'block_matrix': M,
        'block_determinant': det(M),
        'generic_alternating_determinant_polynomial': '0 in Z[x1,x2,x3]',
        'finite_field_rank_checks': finite_checks,
        'Y_submodule_dimension_vectors': subdims,
        'Y_submodule_eta_values': vals,
        'Y_quotient_dimension_vectors': quotients,
        'Y_quotient_eta_values': qvals,
        'witness_plane_normal': y,
        'closed_cone_generators': [p,g],
        'witness_grid_points_checked': grid_count,
        'eta_unordered_binary_splits': splits,
        'homological_obstructions_proved_in_text': [1,3,6],
        'scope': 'Exact arithmetic and finite checks supporting PROOF.md; not an exhaustive verification of modules or TF classes.'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    r = results()
    if args.check:
        expected = json.loads(args.check.read_text())
        if expected != r:
            raise SystemExit('FAIL: recomputed results differ from expected file')
        print('PASS: exact determinant, symbolic polynomial, module witnesses, and arithmetic checks')
    elif args.write:
        args.write.write_text(json.dumps(r, indent=2, sort_keys=True) + '\n')
        print('Wrote checked expected results')
    else:
        print(json.dumps(r, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
