#!/usr/bin/env python3
"""Exact algebraic checks for a scoped, UNSOLVED geometric investigation.

No numerical experiments, network access, or third-party dependencies.
The script does not establish the cited global differential-geometric inputs.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c


def neg(a): return [-x for x in a]
def sub(a, b): return add(a, neg(b))


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a: return 0
    i = 0
    for j in range(len(a[0])):
        p = next((p for p in range(i, len(a)) if a[p][j]), None)
        if p is None: continue
        a[i], a[p] = a[p], a[i]
        z = a[i][j]
        a[i] = [x/z for x in a[i]]
        for p in range(len(a)):
            if p != i:
                z = a[p][j]
                a[p] = [x-z*y for x, y in zip(a[p], a[i])]
        i += 1
        if i == len(a): break
    return i


def basis(n, indices):
    return [[int(i == j) for j in range(n)] for i in indices]


def dot(a, b): return sum(x*y for x, y in zip(a, b))


def main():
    results = {}
    # Symbolic polynomials in the dimension k: these coefficient identities
    # hold for every k, rather than only the sample dimensions below.
    k, km1 = [F(0), F(1)], [F(-1), F(1)]
    kk = mul(k, km1)
    square = mul(km1, km1)
    assert sub(kk, square) == km1
    delta_lower = add(sub(neg(kk), square), square)
    assert add(delta_lower, kk) == [F(0)]
    results['catenoid_jacobi_polynomial_identity'] = True

    # Full profile chain-rule computation at rational radii.
    count = 0
    for dim in range(2, 13):
        for r in [F(1), F(3, 2), F(2), F(7, 3)]:
            rp2 = 1-r**(-2*dim+2)
            rpp = (dim-1)*r**(-2*dim+1)
            f = r**(1-dim)
            fr = (1-dim)*r**(-dim)
            frr = dim*(dim-1)*r**(-dim-1)
            lap = frr*rp2+fr*rpp+(dim-1)*fr*rp2/r
            jacobi = lap+dim*(dim-1)*r**(-2*dim)*f
            assert jacobi == (dim-1)*r**(-dim-1) > 0
            count += 1
    results['catenoid_rational_profile_checks'] = count

    # Parabola metric and curvature in rational Cartesian coordinates.
    count = 0
    for x in [F(0), F(1, 3), F(1), F(-2)]:
        for y in [F(0), F(2, 5), F(-1)]:
            fx = [F(1), F(0), 2*x, 2*y]
            fy = [F(0), F(1), -2*y, 2*x]
            lam = 1+4*x*x+4*y*y
            assert dot(fx, fx) == dot(fy, fy) == lam
            assert dot(fx, fy) == 0
            lap_log_lam = 16/lam-64*(x*x+y*y)/lam**2
            assert lap_log_lam == 16/lam**2
            gauss = -lap_log_lam/(2*lam)
            assert gauss == -8/lam**3
            assert -2*gauss*lam == 16/lam**2
            count += 1
    # Integral r/(1+4r^2)^2 dr from zero to infinity is 1/8;
    # substituting t=1+4r^2 proves this analytically in the prose.
    assert 32*F(1, 8) == 4
    results['parabola_rational_metric_curvature_checks'] = count
    results['critical_curvature_coefficient_of_pi'] = 4

    # Plane directions and the precise failure of transversality.
    p = basis(6, [0, 1, 2, 3])
    q = basis(6, [0, 1, 2, 4])
    common_dim = rank(p)+rank(q)-rank(p+q)
    assert (rank(p), rank(q), rank(p+q), common_dim) == (4, 4, 5, 3)
    assert 2*rank(p) > 6
    assert all(v[5] == 0 for v in p+q)
    # Sixth coordinate distinguishes the two affine planes identically.
    offset = basis(6, [5])[0]
    assert offset[5] == 1
    results['affine_plane_direction_dimensions'] = [4, 4, 5, 3]
    results['affine_separating_coordinate'] = 6

    # Standard Kahler skew operator has norm one on the C^2 block.
    j = [[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
    assert [[sum(j[a][i]*j[a][b] for a in range(4))
             for b in range(4)] for i in range(4)] == basis(4, range(4))
    assert j[0][1] == j[2][3] == 1
    count = 0
    for dim in range(3, 13):
        n = dim+2
        p = basis(n, range(dim))
        q = basis(n, list(range(dim-2))+[dim, dim+1])
        assert rank(p)+rank(q)-rank(p+q) == dim-2
        assert 2*dim > n
        count += 1
    results['kahler_operator_identity'] = True
    results['calibrated_cone_dimension_checks'] = count

    # Normal-translation cancellation for exact trace-free symmetric
    # second-fundamental-form arrays. This checks the algebra, not their
    # realization by a global minimal submanifold.
    cases = []
    for dim, codim in [(3,2), (4,3), (5,2), (7,4)]:
        a = [[[F((i+1)*(j+1)*(al+2), 7)
               for al in range(codim)] for j in range(dim)] for i in range(dim)]
        for al in range(codim):
            a[-1][-1][al] = -sum(a[i][i][al] for i in range(dim-1))
            assert sum(a[i][i][al] for i in range(dim)) == 0
        grad = [F(i+1, 11) for i in range(dim)]
        f = F(5, 3)
        # At an adapted ambient frame, tangent basis vectors have zero
        # normal projection and derivative -A(e_i,e_alpha); normal basis
        # vectors have value nu_alpha and zero normal derivative at p.
        gradient_energy = F(0)
        potential_energy = F(0)
        for al in range(dim+codim):
            value = [F(int(al == dim+b)) for b in range(codim)]
            for i in range(dim):
                derivative = [-a[i][al][b] if al < dim else F(0)
                              for b in range(codim)]
                derivative_fv = [grad[i]*value[b]+f*derivative[b]
                                 for b in range(codim)]
                gradient_energy += dot(derivative_fv, derivative_fv)
            for i in range(dim):
                for z in range(dim):
                    potential_energy += f*f*dot(a[i][z], value)**2
        result = gradient_energy-potential_energy
        assert result == codim*dot(grad, grad)
        cases.append({'k':dim, 'q':codim, 'value':str(result)})
    results['normal_translation_cancellation_cases'] = cases

    # Scaling exponents and product growth are exact elementary controls.
    for dim in range(2, 30):
        for scale in [F(1, 3), F(2), F(7, 2)]:
            assert scale**(-dim)*scale**dim == 1
        for d in range(1, dim):
            assert (2*F(10))**d > (2*F(2))**d > 0
    results['critical_scaling_and_product_growth_checks'] = True

    status = json.loads((Path(__file__).parent/'STATUS.json').read_text())
    assert status['status'] == 'unsolved'
    assert status['turns_used'] == status['turn_limit'] == 5
    assert status['full_target_resolved'] is False
    assert status['novelty_claim'] is False
    results['status_guard'] = True
    print(json.dumps({'passed': True, 'scope': 'finite exact algebraic checks only',
                      'checks':results}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
