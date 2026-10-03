#!/usr/bin/env python3
"""Exact, dependency-free algebra checks. These are not a geometric proof."""
from fractions import Fraction as Q
from itertools import permutations, combinations
import json
from pathlib import Path


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    return trim([(p[i] if i < len(p) else 0) +
                 (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def neg(p):
    return [-x for x in p]


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return trim(out)


def mod(p, q):
    p, q = trim(p), trim(q)
    while len(p) >= len(q) and p != [0]:
        shift, c = len(p)-len(q), p[-1]/q[-1]
        p = add(p, [0]*shift + [-c*x for x in q])
    return trim(p)


def ev(p, x):
    result = Q(0)
    for a in reversed(p):
        result = result*x+a
    return result


def det_poly(M):
    total = [Q(0)]
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i+1, 3))
        term = [Q((-1)**inversions)]
        for i in range(3):
            term = mul(term, M[i][perm[i]])
        total = add(total, term)
    return total


def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def sign(x):
    return (x > 0) - (x < 0)


def serial(p):
    return [int(x) if x.denominator == 1 else str(x) for x in p]


def main():
    identity = [[int(i == j) for j in range(3)] for i in range(3)]
    family = []
    for m in range(3, 101):
        P = [[0,1,0],[0,0,1],[-1,m,0]]
        Pinv = [[m,0,-1],[1,0,0],[0,1,0]]
        assert mm(P, Pinv) == identity == mm(Pinv, P)
        matrix = [[[Q(-P[i][j]), Q(1)] if i == j else [Q(-P[i][j])]
                   for j in range(3)] for i in range(3)]
        characteristic = det_poly(matrix)
        assert characteristic == [1, -m, 0, 1]
        determinant = det_poly([[[Q(x)] for x in row] for row in P])
        assert determinant == [-1]
        intervals = [(-m-1,-1), (0,1), (1,m+1)]
        signs = [[sign(ev(characteristic, Q(x))) for x in I] for I in intervals]
        assert signs == [[-1,1],[1,-1],[-1,1]]
        family.append({"m":m, "determinant":-1,
                       "characteristic_ascending":serial(characteristic),
                       "root_brackets":intervals,"endpoint_signs":signs})

    phi7 = [Q(1)]*7
    zeta = [Q(0),Q(1)]
    powers = [[Q(1)]]
    for k in range(1, 8):
        powers.append(mod(mul(powers[-1], zeta), phi7))
    unit = add([1], powers[1])
    inverse = neg(add(add(powers[1],powers[3]),powers[5]))
    assert mod(mul(unit,inverse),phi7) == [1]
    w = [mod(add(add([2],powers[a]),powers[7-a]),phi7) for a in (1,2,4)]
    s1 = mod(add(add(w[0],w[1]),w[2]),phi7)
    s2 = mod(add(add(mul(w[0],w[1]),mul(w[0],w[2])),mul(w[1],w[2])),phi7)
    s3 = mod(mul(mul(w[0],w[1]),w[2]),phi7)
    assert (s1,s2,s3) == ([5],[6],[1])
    minimal = [Q(-1),Q(6),Q(-5),Q(1)]
    for r in w:
        pr = [Q(0)]
        for c in reversed(minimal):
            pr = mod(add(mul(pr,r),[c]),phi7)
        assert pr == [0]
    brackets = [(Q(1,8),Q(1,4)),(Q(3,2),Q(8,5)),(Q(16,5),Q(13,4))]
    signs = [[sign(ev(minimal,t)) for t in I] for I in brackets]
    assert signs == [[-1,1],[1,-1],[-1,1]]
    # These establish c < 1 < b < a. The trigonometric identification is in PROOF.md.
    assert brackets[0][1] < 1 < brackets[1][0] < brackets[1][1] < brackets[2][0]

    h21 = {}
    for k, exponents in [(3,[1,1,1]),(7,[1,2,4])]:
        weights = [(exponents[i]+exponents[j]-exponents[l]) % k
                   for i,j in combinations(range(3),2) for l in range(3)]
        assert 0 not in weights
        h21[str(k)] = weights
    # Only invariant-form weights on the covering torus are checked here.
    # A statement about a resolution's Hodge numbers requires geometry.

    result = {
        "status":"all exact algebra checks passed",
        "scope":"Algebra only; no new threefold or geometric classification certified.",
        "matrix_family":family,
        "x7":{
            "cyclotomic_polynomial_ascending":serial(phi7),
            "unit_inverse_product_mod_phi7":[1],
            "squared_modulus_elementary_symmetric_values":[5,6,1],
            "squared_modulus_polynomial_ascending":serial(minimal),
            "ascending_root_brackets":[[str(x) for x in I] for I in brackets],
            "endpoint_signs":signs,
            "degree_relation":"d1=a, d2=a*b=1/c>d1>1"
        },
        "invariant_h21_weights_on_cover_only":h21,
        "rank_two_cubic_absolute_weight_exponents":[2*i-3 for i in range(4)],
        "scalar_orders_preserving_three_form":[k for k in [2,3,4,6] if 3 % k == 0]
    }
    assert 0 not in result["rank_two_cubic_absolute_weight_exponents"]
    out = Path(__file__).with_name("exact_results.json")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"matrix_instances":len(family),
                      "cyclotomic_inverse":"verified", "x7_degree_order":"d2>d1>1",
                      "output":out.name},sort_keys=True))


if __name__ == "__main__":
    main()
