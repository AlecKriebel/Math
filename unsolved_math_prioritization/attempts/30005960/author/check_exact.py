#!/usr/bin/env python3
"""Exact, dependency-free arithmetic controls for the authored toric example.

These checks do not prove the cited stability-condition existence theorem.
Run: python3 check_exact.py > CHECK_RESULTS.json
"""
from fractions import Fraction as F
from itertools import combinations
import json

assertions = 0


def check(condition, label):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(label)


def det2(v, w):
    return v[0]*w[1] - v[1]*w[0]


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def mul(M, x):
    return [dot(row, x) for row in M]


def pairing(x, y):
    return dot(x, mul(Q, y))


def determinant(M):
    if len(M) == 1:
        return M[0][0]
    return sum((-1)**j * M[0][j] * determinant(
        [row[:j]+row[j+1:] for row in M[1:]]) for j in range(len(M)))


def solve_vertex(v, w, dv, dw):
    d = det2(v, w)
    return (F(-dv*w[1] + dw*v[1], d), F(-v[0]*dw + w[0]*dv, d))


def strings(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, (list, tuple)):
        return [strings(a) for a in x]
    if isinstance(x, dict):
        return {k: strings(v) for k, v in x.items()}
    return x


# Cyclic fan order: D1, D2, A1, A2, D0, B1, B2.
rays = [(1, 0), (0, 1), (-1, -2), (-2, -5), (-3, -8), (-1, -3), (0, -1)]
N = len(rays)
coarse = [rays[0], rays[1], rays[4]]
check([det2(coarse[i], coarse[(i+1) % 3]) for i in range(3)] == [1, 3, 8], 'coarse determinants')
check(tuple(rays[4][j]+3*rays[0][j]+8*rays[1][j] for j in range(2)) == (0, 0), 'weighted relation')
for i in range(N):
    check(det2(rays[i], rays[(i+1) % N]) == 1, f'smooth cone {i}')
for a, v, b in [(rays[1], rays[2], rays[4]), (rays[1], rays[3], rays[4]),
                (rays[4], rays[5], rays[0]), (rays[4], rays[6], rays[0])]:
    check(det2(a, v) > 0 and det2(v, b) > 0, 'strictly inside coarse cone')

self_intersections = [-det2(rays[i-1], rays[(i+1) % N]) for i in range(N)]
check(self_intersections == [0, 2, -2, -2, -1, -3, -3], 'invariant self intersections')
Q = [[self_intersections[i] if i == j else
      (1 if (i-j) % N in (1, N-1) else 0) for j in range(N)] for i in range(N)]
for j in range(2):
    check(mul(Q, [v[j] for v in rays]) == [0]*N, 'principal divisor relation')

exceptional = [2, 3, 5, 6]
M = [[Q[i][j] for j in exceptional] for i in exceptional]
check(M == [[-2, 1, 0, 0], [1, -2, 0, 0], [0, 0, -3, 1], [0, 0, 1, -3]], 'exceptional matrix')
negative_minors = [determinant([[-M[i][j] for j in range(k)] for i in range(k)]) for k in range(1, 5)]
check(negative_minors == [2, 3, 9, 24], 'negative definiteness via Sylvester')
check(all(Q[i][i]+1 < 0 for i in exceptional), 'strict chain negativity')

lam = [F(x) for x in [0, 0, 8, 16, 24, 9, 3]]
D = [F(int(i in exceptional)) for i in range(N)]
beta = [F(0), F(0), F(-1, 4), F(-1, 4), F(0), F(-3, 8), F(-3, 8)]
check(mul(Q, lam) == [3, 8, 0, 0, 1, 0, 0], 'pullback curve intersections')
check(pairing(lam, lam) == 24, 'pullback square')
check(pairing(lam, D) == 0 and pairing(D, D) == -6, 'exceptional sum square')
check(pairing(lam, beta) == 0, 'beta orthogonal to pullback')
check(pairing(beta, beta) == F(-11, 16), 'beta square')
beta_curves = [mul(Q, beta)[i] for i in exceptional]
check(beta_curves == [F(1, 4), F(1, 4), F(3, 4), F(3, 4)], 'beta pairings')
check(F(24, 2)-pairing(beta, beta)/2 == F(395, 32), 'rank coefficient of central charge')

# Cartier data of pullback of 24 D0 on the three coarse cones.
for ids, local_m in [([0, 1], (0, 0)), ([1, 2, 3, 4], (8, 0)), ([4, 5, 6, 0], (0, 3))]:
    for i in ids:
        check(lam[i] == -dot(local_m, rays[i]), 'Cartier pullback coefficient')

# Explicit lattice polygon proves projectivity of the smooth fan.
ample_divisor = [4*x-y for x, y in zip(lam, D)]
vertices = [solve_vertex(rays[i], rays[(i+1) % N], ample_divisor[i], ample_divisor[(i+1) % N]) for i in range(N)]
expected_vertices = [(0, 0), (31, 0), (29, 1), (24, 3), (8, 9), (2, 11), (0, 11)]
check(vertices == expected_vertices, 'polygon vertices')
for i, v in enumerate(vertices):
    for j in range(N):
        slack = dot(v, rays[j]) + ample_divisor[j]
        check(slack == 0 if j in (i, (i+1) % N) else slack > 0, 'polygon exact active facets')
area = abs(sum(det2(vertices[i], vertices[(i+1) % N]) for i in range(N)))/2
check(area == 189 and pairing(ample_divisor, ample_divisor) == 378, 'polygon area and divisor square')

intervals = []
for chain in [[2, 3], [5, 6]]:
    for start in range(2):
        for end in range(start, 2):
            ids = chain[start:end+1]
            m = len(ids)
            q = sum(mul(Q, beta)[i]+F(Q[i][i], 2) for i in ids)
            check(q == F(-3*m, 4), 'interval residue formula')
            check(q.denominator != 1, 'Condition 4.1 for a chain')
            check(-m < q < -(m-1), 'Condition 5.5 with every k equal to zero')
            intervals.append({'curves': ids, 'length': m, 'q': q, 'strict_interval': [-m, -(m-1)]})

# Exact polynomial identity: (1+s^2)^2 - 4 s^2 == (1-s^2)^2.
check([1, 0, 2-4, 0, 1] == [1, 0, -2, 0, 1], 'constant volume polynomial identity')
path_samples = []
for denominator in range(9, 257):
    s = F(1, denominator)
    a = (1+s*s)/(1-s*s)
    b = 4*s/(1-s*s)
    omega = [a*x-b*y for x, y in zip(lam, D)]
    check(all(x > 0 for x in mul(Q, omega)), 'ample path intersections')
    check(pairing(omega, omega) == 24, 'constant volume along path')
    check(0 < b/a < F(1, 2), 'ample path range')
    if denominator in (9, 16, 256):
        path_samples.append({'s': s, 'a': a, 'b': b, 'intersections': mul(Q, omega)})

# Charge of a line bundle of total degree d on a connected reduced subchain.
support_tests = 0
for chain in [[2, 3], [5, 6]]:
    for start in range(2):
        for end in range(start, 2):
            ids = chain[start:end+1]
            m = len(ids)
            cycle = [int(i in ids) for i in range(N)]
            c2 = pairing(cycle, cycle)
            bound = F(1, 4) if m == 1 else F(1, 2)
            for degree in range(-20, 21):
                ch2 = F(degree) - sum(F(Q[i][i], 2) for i in ids) - (m-1)
                twisted_ch2 = ch2-pairing(beta, cycle)
                check(twisted_ch2 == degree+1-F(m, 4), 'GRR chain charge')
                check(abs(twisted_ch2) >= bound, 'nonzero charge lower bound')
                check(twisted_ch2**2+F(1, 48)*c2 >= 0, 'exceptional-factor quadratic bound')
                support_tests += 1
for i in exceptional:
    n = -Q[i][i]
    z_oc = -F(n, 2)+mul(Q, beta)[i]
    z_oc_minus_one_shift = -(1-F(n, 2)+mul(Q, beta)[i])
    check(z_oc == F(-3, 4) and z_oc_minus_one_shift == F(-1, 4), 'point destabilization charges')
    check(z_oc+z_oc_minus_one_shift == -1, 'point exact-sequence additivity')

# Separate D4 source warning: centre first, then its three leaves.
D4 = [[-2, 1, 1, 1], [1, -2, 0, 0], [1, 0, -2, 0], [1, 0, 0, -2]]
rho = [1, 1, 1, 1]
theta = [2, 1, 1, 1]
check(dot(rho, mul(D4, rho)) == -2, 'D4 reduced root square')
check(dot(theta, mul(D4, theta)) == -2, 'D4 fundamental root square')
check(mul(D4, rho) == [1, -1, -1, -1], 'D4 reduced cycle is not anti-nef')
check(mul(D4, theta) == [-1, 0, 0, 0], 'D4 fundamental cycle is anti-nef')
check(rho != theta and all(a > 0 for a in rho+theta), 'different full-support positive roots')
connected_count = 0
for size in range(1, 5):
    for ids in combinations(range(4), size):
        if size > 1 and 0 not in ids:
            continue
        connected_count += 1
        fundamental = theta if size == 4 else [int(i in ids) for i in range(4)]
        test = F(sum(fundamental), 4)-size
        check(test.denominator != 1, 'D4 beta quarter passes stated fundamental-cycle tests')
check(F(sum(rho), 4) == 1, 'D4 reduced cycle lies on an omitted integral hyperplane')

result = {
    'result': 'PASS',
    'assertions': assertions,
    'arithmetic': 'fractions.Fraction and integers; no external packages',
    'scope_limit': 'Arithmetic controls only; existence, HN, support property and convergence use the cited literature theorem.',
    'fan_rays': rays,
    'self_intersections': self_intersections,
    'exceptional_matrix': M,
    'negative_matrix_leading_minors': negative_minors,
    'lambda_coefficients': lam,
    'lambda_square': pairing(lam, lam),
    'beta_coefficients': beta,
    'beta_exceptional_pairings': beta_curves,
    'beta_square': pairing(beta, beta),
    'ample_polygon_vertices': vertices,
    'six_chamber_tests': intervals,
    'constant_volume_path_test_count': 248,
    'path_samples': path_samples,
    'exceptional_line_bundle_tests': support_tests,
    'exceptional_delta_squared': F(1, 48),
    'D4_connected_subgraphs_tested': connected_count,
    'D4_warning': 'Two distinct full-support positive roots have square -2; the reduced cycle is not the fundamental cycle.'
}
print(json.dumps(strings(result), indent=2, sort_keys=True))
