#!/usr/bin/env python3
"""Independent exact controls, using only the standard library.

Builds the Levi-Civita connection directly from the non-diagonal metric
and the two su(2) brackets, without importing the candidate verifier.
Finite checks support, and do not replace, the global isometry proof.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

N = 6
zero = (Q(0),) * N
basis = [tuple(Q(i == j) for j in range(N)) for i in range(N)]
M = [[Q(((3, -1), (-1, 1))[i // 3][j // 3] * (i % 3 == j % 3))
      for j in range(N)] for i in range(N)]
Mi = [[Q(((1, 1), (1, 3))[i // 3][j // 3] * (i % 3 == j % 3), 2)
       for j in range(N)] for i in range(N)]

def dot(x, y):
    return sum(a*b for a, b in zip(x, y))

def add(x, y):
    return tuple(a+b for a, b in zip(x, y))

def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))

def scale(a, x):
    return tuple(a*b for b in x)

def metric(x, y):
    return dot(x, [dot(row, y) for row in M])

def cross(x, y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0])

def bracket(x, y):
    return scale(2, cross(x[:3], y[:3]) + cross(x[3:], y[3:]))

def koszul(x, y):
    cov = [Q(1, 2)*(metric(bracket(x, y), z)-metric(bracket(y, z), x)
                    +metric(bracket(z, x), y)) for z in basis]
    return tuple(dot(row, cov) for row in Mi)

Gamma = [[koszul(x, y) for y in basis] for x in basis]

def nabla(x, y):
    return tuple(sum(x[i]*y[j]*Gamma[i][j][k] for i in range(N) for j in range(N))
                 for k in range(N))

def curvature(x, y, z):
    return sub(sub(nabla(x, nabla(y, z)), nabla(y, nabla(x, z))), nabla(bracket(x, y), z))

def shear_d(x):
    return x[:3] + sub(x[3:], x[:3])

def inverse_d(x):
    return x[:3] + add(x[3:], x[:3])

def round_curvature(x, y, z):
    return sub(scale(dot(y, z), x), scale(dot(x, z), y))

def product_curvature(x, y, z):
    x, y, z = map(shear_d, (x, y, z))
    return inverse_d(round_curvature(x[:3], y[:3], z[:3])
                     +round_curvature(x[3:], y[3:], z[3:]))

def mm(A, B):
    return [[dot(row, col) for col in zip(*B)] for row in A]

def trace(A):
    return sum(A[i][i] for i in range(len(A)))

def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]

def charpoly(A):
    # Faddeev-LeVerrier, entirely rational.
    n = len(A)
    B = eye(n)
    coefficients = [Q(1)]
    for k in range(1, n+1):
        B = mm(A, B)
        c = -trace(B)/k
        coefficients.append(c)
        for i in range(n):
            B[i][i] += c
    return coefficients

def polynomial_from_roots(roots):
    coeff = [Q(1)]
    for r in roots:
        nxt = [Q(0)]*(len(coeff)+1)
        for i, c in enumerate(coeff):
            nxt[i] += c
            nxt[i+1] -= r*c
        coeff = nxt
    return coeff

def run():
    assert mm(M, Mi) == eye(N)
    for x, y in product(basis, repeat=2):
        assert sub(nabla(x, y), nabla(y, x)) == bracket(x, y)
        for z in basis:
            assert metric(nabla(x, y), z) + metric(y, nabla(x, z)) == 0
            assert curvature(x, y, z) == product_curvature(x, y, z)

    # Curvature Jacobi spectra for every ternary velocity, independently
    # derived from Koszul coefficients rather than imposed parity formulae.
    spectrum_cases = 0
    for raw in product((-1, 0, 1), repeat=6):
        v = tuple(map(Q, raw))
        columns = [curvature(e, v, v) for e in basis]
        J = [list(row) for row in zip(*columns)]
        c1sq = dot(v[:3], v[:3])
        w = sub(v[3:], v[:3])
        c2sq = dot(w, w)
        assert charpoly(J) == polynomial_from_roots([0, 0, c1sq, c1sq, c2sq, c2sq])
        spectrum_cases += 1

    # Finite adjoint witness, independent of the infinitesimal -2 test:
    # Ad_(i,1) changes j in the first ideal to -j, fixing second ideal.
    x, y = basis[1], basis[4]
    assert metric(x, y) == -1
    assert metric(scale(-1, x), y) == 1
    # Positive control: the diagonal adjoint action flips both j directions.
    assert metric(scale(-1, x), scale(-1, y)) == -1

    # Discrete Euler-Arnold consistency control: the actual g-geodesic is
    # (exp(tA), exp(t(B-A))exp(tA)). Its left velocity is
    # (A, Ad_exp(-tA)(B-A)+A), whose derivative at zero is (0,-[A,B-A]).
    geodesic_cases = 0
    for raw in product((-1, 0, 1), repeat=6):
        v = tuple(map(Q, raw))
        expected_acceleration = (Q(0),)*3 + scale(-2, cross(v[:3], sub(v[3:], v[:3])))
        assert expected_acceleration == scale(-1, nabla(v, v))
        geodesic_cases += 1

    # Non-tautological index/nullity oracle: enumerate signs of exact
    # normalized Dirichlet eigenvalues m^2-r^2. Excluding T is necessary.
    ratios = sorted({Q(n, d) for d in range(1, 10) for n in range(0, 42)})
    endpoint_cases = 0
    inclusive_negative_controls = 0
    for r in ratios:
        eig = [Q(m*m)-r*r for m in range(1, 43)]
        nneg = sum(a < 0 for a in eig)
        nzero = sum(a == 0 for a in eig)
        expected_negative = max(0, (r.numerator+r.denominator-1)//r.denominator-1)
        assert nneg == expected_negative
        assert nzero == int(r > 0 and r.denominator == 1)
        if r > 0 and r.denominator == 1:
            assert sum(Q(m) <= r for m in range(1, 43)) == nneg+1
            inclusive_negative_controls += 1
        endpoint_cases += 1
    # Odd-dimensional sphere is crucial; S^2 at r=3/2 has odd index 1.
    assert sum(Q(m*m)-Q(3,2)**2 < 0 for m in range(1, 43)) == 1

    return {
        'status':'PASS',
        'koszul_curvature_basis_triples':216,
        'exact_jacobi_characteristic_polynomial_cases':spectrum_cases,
        'euler_arnold_initial_acceleration_cases':geodesic_cases,
        'independent_endpoint_sign_cases':endpoint_cases,
        'strict_endpoint_negative_controls':inclusive_negative_controls,
        'finite_ad_invariance_cross_term_before':-1,
        'finite_ad_invariance_cross_term_after':1,
        'diagonal_ad_positive_control':'PASS',
        'sphere_dimension_odd_index_negative_control':'PASS',
        'limitations':'Finite algebra controls; all-geodesic conclusion rests on the global isometry and split Jacobi proof.'
    }

if __name__ == '__main__':
    result = json.dumps(run(), indent=2)+'\n'
    print(result, end='')
    Path(__file__).with_name('independent_controls_results.json').write_text(result)
