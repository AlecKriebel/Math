#!/usr/bin/env python3
"""Exact, source-free certificates for the scoped results in PROOF.md.

Python 3 standard library only. No numerical optimizer, downloaded coordinates,
floating point arithmetic, random sampling, or external data is used.
Run: python3 verify.py > CHECK_RESULTS.replay.json
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product, permutations
from math import comb, factorial
import json


def gram40():
    edges = list(combinations(range(5), 2))
    vectors = []
    for i in range(5):
        active = [k for k, edge in enumerate(edges) if i not in edge]
        for signs in product([1, -1], repeat=6):
            negative = [edges[active[k]] for k in range(6) if signs[k] == -1]
            e = len(negative) % 2
            degree = {j: sum(j in edge for edge in negative) % 2
                      for j in range(5) if j != i}
            if (all(degree[(i+j) % 5] == e for j in (1, 2)) and
                    all(degree[(i+j) % 5] != e for j in (3, 4))):
                vector = [0] * 10
                for k, sign in zip(active, signs):
                    vector[k] = sign
                vectors.append(vector)
    assert len(vectors) == len(set(map(tuple, vectors))) == 40
    return [[sum(a*b for a, b in zip(v, w)) for w in vectors] for v in vectors]


def gf8_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011  # z^3+z+1
    return result


def gram64():
    points = list(product(range(8), repeat=2))
    H = []
    for a, b in points:
        row = []
        for c, d in points:
            if (a, b) == (c, d):
                h = 7
            elif a == c:
                h = -1
            else:
                z = a ^ c
                forbidden = (gf8_mul(gf8_mul(z, z), z),
                             gf8_mul(gf8_mul(a, c), z))
                h = -3 if b ^ d in forbidden else 1
            row.append(h)
        H.append(row)
    return H


def exact_psd(A, stop_rank=None):
    """Symmetric exact elimination, with explicit zero-pivot row checks.

    The Schur complement updates preserve congruence. A zero diagonal pivot
    must have a zero remaining row; otherwise positivity is rejected.
    When stop_rank is set, A is already known PSD and only a basis is sought.
    """
    A = [[F(x) for x in row] for row in A]
    indices, pivots = [], []
    for k in range(len(A)):
        q = A[k][k]
        assert q >= 0
        if not q:
            assert all(A[k][j] == 0 for j in range(k+1, len(A)))
            continue
        indices.append(k)
        pivots.append(q)
        if stop_rank is not None and len(indices) == stop_rank:
            return indices, pivots
        for i in range(k+1, len(A)):
            for j in range(i, len(A)):
                A[i][j] -= A[i][k] * A[k][j] / q
                A[j][i] = A[i][j]
    return indices, pivots


def gegenbauer_values(n, t, degree):
    p = [F(1), t]
    for k in range(2, degree+1):
        p.append(((2*k+n-4)*t*p[-1]-(k-1)*p[-2])/F(k+n-3))
    return p


def check_code(H, n, denominator, expected, frame_bound):
    N, d = len(H), denominator
    assert F(N*d, n).denominator == 1
    eigenvalue = N*d//n
    for i in range(N):
        assert H[i][i] == d and sum(H[i]) == 0
        assert Counter(H[i][j] for j in range(N) if j != i) == expected
        for j in range(N):
            assert H[i][j] == H[j][i]
            assert sum(H[i][k]*H[k][j] for k in range(N)) == eigenvalue*H[i][j]
    assert sum(h**3 for row in H for h in row) == 0
    # Gram PSD, rank and frame tightness follow from the verified quadratic identity.
    shells = sorted(expected)
    for a in shells:
        m = expected[a]
        assert F(m*a, d).denominator == 1
        for i in range(N):
            for j in range(N):
                assert sum(H[i][k] for k in range(N) if H[k][j] == a) == m*a*H[i][j]//d
    moments = []
    for k in range(1, 8):
        value = 1+sum(m*gegenbauer_values(n, F(a, d), 7)[k]
                      for a, m in expected.items())
        assert (value == 0) if k <= 3 else (value > 0)
        moments.append(str(value))
    b = max(F(a*a, d*d) for a in shells)
    u = [F(1)]
    for j in range(1, 5):
        u.append(u[-1]*F(2*j-1, n+2*j-3))
    tail_bound = sum(comb(4, j)*b**(4-j)*(1-b)**j*u[j] for j in range(5))
    assert (N-1)*tail_bound < 1
    frame_certificates = []
    for i in range(N):
        h = H[i]
        # V = d^2 times the Gram matrix of tangent projections y_j.
        V = [[d*H[a][b]-h[a]*h[b] for b in range(N)] for a in range(N)]
        indices, basis_pivots = exact_psd(V, n-1)
        assert len(indices) == n-1
        nearest = [j for j in range(N) if j != i and h[j] == max(shells)]
        matrix = [[sum(V[a][j]*V[b][j] for j in nearest)
                   - frame_bound*d*d*V[a][b] for b in indices] for a in indices]
        _, bound_pivots = exact_psd(matrix)
        frame_certificates.append({"point": i, "basis": indices,
                                   "bound_rank": len(bound_pivots),
                                   "bound_pivots": list(map(str, bound_pivots))})
    s, m = F(max(shells), d), expected[max(shells)]
    quartic_hessian_lower_bound = 3*frame_bound/(1+s)-m*s
    assert quartic_hessian_lower_bound > 0
    return {"N": N, "dimension": n, "integer_gram_denominator": d,
            "nonzero_integer_gram_eigenvalue": eigenvalue,
            "valencies": {str(F(a, d)): m for a, m in sorted(expected.items())},
            "normalized_Gegenbauer_moments_degrees_1_to_7": moments,
            "Laplace_bound_degrees_at_least_8": str(tail_bound),
            "positive_tail_margin": str(1-(N-1)*tail_bound),
            "nearest_shell_frame_bound": str(frame_bound),
            "quartic_hessian_bound_divided_by_g_prime_s": str(quartic_hessian_lower_bound),
            "frame_certificates": frame_certificates}


def rival_polynomial(k):
    """Ascending integer coefficients of 18^k*(E_k(rival)-E_k(C40))."""
    p = [0]*(2*k+1)
    p[0] = 48*12**k+72*20**k-160*9**k-60*12**k-80*18**k-480*21**k
    for j in range(k+1):
        p[j] += comb(k, j)*(96*18**(k-j)*(-54)**j+288*18**k)
        p[2*j] += comb(k, j)*(36*36**(k-j)*(-648)**j+96*36**(k-j)*(-486)**j)
    p[2*k] += 72*(648**k+324**k)
    return p


def bernstein_integer_coefficients(p):
    """Bernstein coefficients on [0,1/5], scaled by positive 5^D D!."""
    D = len(p)-1
    c = [p[i]*5**(D-i)*factorial(i)*factorial(D-i) for i in range(D+1)]
    return [sum(c[i]*comb(j, i) for i in range(j+1)) for j in range(D+1)]


def subdivide(b):
    """Midpoint de Casteljau subdivision, each child scaled by positive 2^D."""
    D = len(b)-1
    left, right = [b[0] << D], [b[-1] << D]
    row = b
    for j in range(1, D+1):
        row = [row[i]+row[i+1] for i in range(len(row)-1)]
        left.append(row[0] << (D-j))
        right.append(row[-1] << (D-j))
    return left, right[::-1]


def certify_positive(b, path=""):
    if min(b) > 0:
        return [path]
    assert len(path) < 20
    left, right = subdivide(b)
    return certify_positive(left, path+"0")+certify_positive(right, path+"1")


def evaluate(p, a):
    value = F(0)
    for c in reversed(p):
        value = value*a+c
    return value


def check_rival():
    # Recover the unordered v_sigma/v_tau distribution directly from S_4.
    P = list(permutations(range(4)))
    parity = lambda p: (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
    types = Counter((sum(x == y for x, y in zip(p, q)), parity(p)*parity(q))
                    for p, q in combinations(P, 2))
    assert types == {(2, -1): 72, (0, 1): 36, (1, 1): 96, (0, -1): 72}
    assert sum([48, 72, 96, 288, 72, 36, 96, 72]) == comb(40, 2)
    assert rival_polynomial(0) == [0]
    assert rival_polynomial(1) == [0, 0, 0]
    assert rival_polynomial(2) == [72000, 0, -4665600, 0, 75582720]
    # This equals 18^2 * (80/9)*(162*a^2-5)^2.
    certificates = {}
    for k in range(3, 100):
        p = rival_polynomial(k)
        paths = certify_positive(bernstein_integer_coefficients(p))
        assert sum(F(1, 2**len(path)) for path in paths) == 1
        certificates[str(k)] = paths
    for a in (F(1, 6), F(1, 8), F(13, 75)):
        distribution = [(F(-1, 3), 48), (F(1, 9), 72), (-3*a, 96), (a, 288),
                        (36*a*a-1, 72), (1-36*a*a, 36),
                        (1-27*a*a, 96), (18*a*a-1, 72)]
        target = [(F(-1, 2), 160), (F(-1, 3), 60), (F(0), 80), (F(1, 6), 480)]
        for k in range(12):
            energy_gap = sum(m*(1+t)**k for t, m in distribution)-sum(m*(1+t)**k for t, m in target)
            assert evaluate(rival_polynomial(k), a) == 18**k*energy_gap
    assert F(1, 27) < F(1, 25)  # every positive admissible a is below 1/5
    assert F(7, 6)**100 > 300
    assert 288*F(176, 175)**100 > 481
    assert 96*F(4458, 4375)**100 > 481
    return {"certified_positive_powers": [3, 99], "interval": ["0", "1/5"],
            "dyadic_Bernstein_leaf_paths": certificates,
            "total_leaves": sum(map(len, certificates.values())),
            "maximum_subdivision_depth": max(len(p) for paths in certificates.values() for p in paths),
            "tail_starts_at": 100, "tail_split_alpha": "13/75",
            "tail_integer_inequalities_verified": 3,
            "permutation_pair_types": {str(key): value for key, value in sorted(types.items())}}


def check_hermite_bases():
    result = []
    for n, nodes in ((10, [F(-1, 2), F(-1, 3), F(0), F(1, 6)]),
                     (14, [F(-3, 7), F(-1, 7), F(1, 7)])):
        p, basis = [F(1)], []
        for root in [x for x in nodes for _ in range(2)]:
            basis.append(list(map(str, p)))
            q = [F(0)]*(len(p)+1)
            for i, c in enumerate(p):
                q[i] -= root*c
                q[i+1] += c
            p = q
        for node in nodes:
            assert evaluate(p, node) == 0
            assert evaluate([i*p[i] for i in range(1, len(p))], node) == 0
        distribution = ([(F(-1, 2), 160), (F(-1, 3), 60), (F(0), 80), (F(1, 6), 480)]
                        if n == 10 else [(F(-3, 7), 448), (F(-1, 7), 224), (F(1, 7), 1344)])
        energies = [sum(m*evaluate(list(map(F, coefficients)), t) for t, m in distribution)
                    for coefficients in basis]
        assert energies[4:] == ([F(500, 9), F(80, 9), F(40, 27), F(0)]
                                if n == 10 else [F(12288, 343), F(0)])
        result.append({"dimension": n, "nodes": list(map(str, nodes)),
                       "ascending_Newton_basis_coefficients": basis,
                       "target_unordered_pair_energies": list(map(str, energies)),
                       "annihilator": list(map(str, p))})
    return result


def main():
    result = {"arithmetic": "Python standard-library integers and Fraction only",
              "scope": "Scoped partial certificates; original universal optimality question remains unsolved",
              "codes": [check_code(gram40(), 10, 6, Counter({-3: 8, -2: 3, 0: 4, 1: 24}), F(2)),
                        check_code(gram64(), 14, 7, Counter({-3: 14, -1: 7, 1: 42}), F(20, 7))],
              "rival_family": check_rival(), "Hermite_reduction": check_hermite_bases()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
