#!/usr/bin/env python3
"""Independently authored finite exact checks; no imports of frozen checkers.

Distinct computational mechanism: colored Gaussian Wick contractions in the
projected two-dimensional covariance matrix, divided by exact radial moments.
Explicit failures use exceptions rather than assert and survive Python -O.
This program supplies bounded algebra evidence, never numerical OT evidence.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial, prod
import argparse
import json


class InvalidClaim(ValueError):
    pass


COUNTS = {}


def require(label, condition):
    if not condition:
        raise InvalidClaim(label)
    COUNTS[label] = COUNTS.get(label, 0) + 1


def zadd(z, w):
    return (z[0]+w[0], z[1]+w[1])


def zmul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def zpow(z, k):
    out = (Q(1), Q(0))
    for _ in range(k):
        out = zmul(out, z)
    return out


def colored_wick(c00, c01, c11, r, s):
    """Gaussian moment of r real and s imaginary projected linear factors."""
    @lru_cache(None)
    def contract(a, b):
        if a+b == 0:
            return Q(1)
        if (a+b) % 2:
            return Q(0)
        if a:
            value = (a-1)*c00*contract(a-2, b) if a >= 2 else Q(0)
            if b:
                value += b*c01*contract(a-1, b-1)
            return value
        return (b-1)*c11*contract(0, b-2)
    return contract(r, s)


def projected_complex_moment(n, u, k):
    require('scope_dimension', n >= 2)
    require('unit_vector', len(u) == n and sum(x*x for x in u) == 1)
    d = n-1
    c00, c01, c11 = 1-u[0]*u[0], -u[0]*u[1], 1-u[1]*u[1]
    if k % 2:
        return (Q(0), Q(0))
    radial = prod(d+2*j for j in range(k//2))
    out = (Q(0), Q(0))
    for s in range(k+1):
        coeff = Q(comb(k, s), radial)*colored_wick(c00, c01, c11, k-s, s)
        out = zadd(out, zmul(zpow((Q(0), Q(1)), s), (coeff, Q(0))))
    return out


def eigen_product(n, k):
    if n < 2 or k < 0 or k % 2:
        raise InvalidClaim('invalid even-degree eigenvalue input')
    return (-1)**(k//2)*prod(Q(2*j+1, n-1+2*j) for j in range(k//2))


def gamma_half(z2):
    """Exact Gamma(z2/2): rational coefficient and exponent of sqrt(pi)."""
    if z2 <= 0 or not isinstance(z2, int):
        raise InvalidClaim('positive integer half-Gamma input required')
    if z2 % 2 == 0:
        return Q(factorial(z2//2-1)), 0
    j = (z2-1)//2
    return Q(factorial(2*j), 4**j*factorial(j)), 1


def gamma_ratio_eigen(n, k):
    m = k//2
    a, pa = gamma_half(n-1)
    b, pb = gamma_half(2*m+1)
    c, pc = gamma_half(2*m+n-1)
    require('eigen_gamma_pi_cancellation', pa+pb-1-pc == 0)
    return (-1)**m*a*b/c


def beta_moment(n, q):
    """Exact M(q), q even, from half-Gamma evaluation rather than recurrence."""
    if n < 3 or q < 0 or q % 2:
        raise InvalidClaim('beta control requires n>=3 and nonnegative even q')
    a, pa = gamma_half(n)
    b, pb = gamma_half(q+2)
    c, pc = gamma_half(q+n)
    require('beta_gamma_pi_cancellation', pa+pb-pc == 0)
    return a*b/c


def radial_by_wick(n, ell):
    """Integrate (X1^2+X2^2)^ell via Gaussian pairings."""
    radial = prod(n+2*j for j in range(ell))
    return sum(Q(comb(ell,j), radial)*colored_wick(Q(1), Q(0), Q(1), 2*j, 2*(ell-j))
               for j in range(ell+1))


def harmonic_square_by_wick(n, k):
    """Integrate [Re(X1+i X2)^k]^2 by colored contractions directly."""
    radial = prod(n+2*j for j in range(k))
    value = Q(0)
    for j in range(0, k+1, 2):
        for ell in range(0, k+1, 2):
            coeff = (-1)**((j+ell)//2)*comb(k,j)*comb(k,ell)
            value += Q(coeff, radial)*colored_wick(Q(1), Q(0), Q(1), 2*k-j-ell, j+ell)
    return value


def rational_unit(n, seed):
    t = [Q(seed+j+1, 2*n+seed+1) for j in range(n-1)]
    norm = sum(x*x for x in t)
    return [(1-norm)/(1+norm)]+[2*x/(1+norm) for x in t]


def tangent_gradient(u, k):
    z = (u[0], u[1])
    zk = zpow(z, k)
    zkm1 = zpow(z, k-1)
    ambient = [k*zkm1[0], -k*zkm1[1]] + [Q(0)]*(len(u)-2)
    return [a-k*zk[0]*x for a,x in zip(ambient,u)], zk[0]


def ratio_exponent(n, p):
    if n < 3 or p < 1:
        raise InvalidClaim('finite-real-p theorem scope')
    alpha = Q(n-2, 2)
    return -alpha-(-alpha-alpha/p)


def falsify(control):
    """Each control substitutes one concrete false alternative."""
    if control == 'hermitian_projection':
        n, k, u = 4, 2, [Q(1), Q(0), Q(0), Q(0)]
        actual = projected_complex_moment(n, u, k)[0]
        wrong = Q(2-u[0]**2-u[1]**2, n-1)
        require('Hermitian contraction rejected', actual == wrong)
    elif control == 'equator_dimension':
        actual = projected_complex_moment(4, [Q(1),Q(0),Q(0),Q(0)], 2)[0]
        wrong = Q(-1, 4)
        require('ambient/equator dimension confusion rejected', actual == wrong)
    elif control == 'radial_beta_parameter':
        actual = radial_by_wick(3, 1)
        wrong = Q(2, 4)
        require('Beta(1,(n-1)/2) rejected', actual == wrong)
    elif control == 'ambient_gradient_energy':
        n, k = 3, 2
        wrong = k*k*beta_moment(n, 2*k-2)
        true = Q(k*(k+n-2), 2)*harmonic_square_by_wick(n, k)*2
        require('omitted tangential gradient correction rejected', true == wrong)
    elif control == 'ratio_exponent':
        n, p = 3, Q(1)
        wrong = Q(n-2,2)*(1-1/p)
        require('alpha*(1-1/p) exponent rejected', ratio_exponent(n,p) == wrong)
    elif control == 'gamma_shift':
        actual = gamma_ratio_eigen(3, 2)
        wrong = Q(-1, 3)
        require('shifted Gamma denominator rejected', actual == wrong)
    elif control == 'reversed_flow':
        n,k,b,H = 3,2,Q(1,5),Q(1)
        L = k*(k+n-2)
        wrong_div = -b*(-L*H)/L
        require('reversed flow rejected', b*H+wrong_div == 0)
    elif control == 'circle_decay':
        require('circle smoothing decay rejected', abs(eigen_product(2,20)) < 1)
    elif control == 'dimension_one':
        projected_complex_moment(1, [Q(1)], 2)
    else:
        raise InvalidClaim('unknown control')


def run():
    for n in range(2,11):
        for seed in (0,1,4):
            u = rational_unit(n,seed)
            c00,c01,c11 = 1-u[0]**2,-u[0]*u[1],1-u[1]**2
            contraction = (c00-c11,2*c01)
            neg_z2 = tuple(-z for z in zpow((u[0],u[1]),2))
            require('complex_bilinear_projection', contraction == neg_z2)
            for k in range(0,25,2):
                actual = projected_complex_moment(n,u,k)
                expected = tuple(eigen_product(n,k)*z for z in zpow((u[0],u[1]),k))
                require('wick_complex_equator_eigenvalue', actual == expected)
                require('product_vs_half_gamma', eigen_product(n,k) == gamma_ratio_eigen(n,k))
                require('nonzero_eigenvalue', eigen_product(n,k) != 0)
            for k in range(1,24,2):
                require('wick_odd_cancellation', projected_complex_moment(n,u,k) == (0,0))
            for k in range(1,13):
                gradient,H = tangent_gradient(u,k)
                r2 = u[0]**2+u[1]**2
                g2 = sum(x*x for x in gradient)
                require('tangential_gradient', sum(x*y for x,y in zip(gradient,u)) == 0)
                require('pointwise_gradient_projection', g2 == k*k*(r2**(k-1)-H*H))
                require('gradient_majorant', g2 <= k*k*r2**(k-1))
    for n in range(3,13):
        for k in range(1,17):
            moment = beta_moment(n,2*k)
            require('radial_wick_vs_beta_gamma', radial_by_wick(n,k) == moment)
            square = harmonic_square_by_wick(n,k)
            require('harmonic_square_angular_average', square == moment/2)
            energy = k*k*(radial_by_wick(n,k-1)-square)
            require('integrated_gradient_energy', energy == k*(k+n-2)*square)
        for p in (Q(1),Q(7,6),Q(5,4),Q(3,2),Q(2),Q(17,3),Q(1000000)):
            alpha = Q(n-2,2)
            require('finite_p_positive_exponent', ratio_exponent(n,p) == alpha/p > 0)
    for k in range(0,101,2):
        require('circle_eigenvalue', eigen_product(2,k) == (-1)**(k//2))
    controls = ['hermitian_projection','equator_dimension','radial_beta_parameter',
                'ambient_gradient_energy','ratio_exponent','gamma_shift','reversed_flow',
                'circle_decay','dimension_one']
    rejected = []
    for control in controls:
        try:
            falsify(control)
        except InvalidClaim as exc:
            rejected.append({'control':control,'exception':str(exc)})
        else:
            raise InvalidClaim('false alternative escaped rejection: '+control)
    return {
        'status':'PASS', 'mechanism':'colored Gaussian Wick contractions and exact half-Gamma algebra',
        'original_module_imports':False, 'counts':COUNTS, 'total_positive_checks':sum(COUNTS.values()),
        'rejected_false_alternatives':rejected, 'rejection_count':len(rejected),
        'scope':{'sphere_ambient_dimensions':'2..12 by check family', 'degrees':'bounded, up to 100 in circle family',
                 'finite_p_samples':'exact positive rational orders only; all-real-p conclusion is analytic'},
        'limitations':['Finite algebra checks do not prove all n, k, or real p.',
                       'No numerical or discretized Wasserstein result is claimed.',
                       'The flow existence and Gamma asymptotics require analytic reasoning in REPORT.md.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--false-alternative')
    args = parser.parse_args()
    if args.false_alternative:
        falsify(args.false_alternative)
        raise InvalidClaim('false alternative unexpectedly passed')
    print(json.dumps(run(), indent=2, sort_keys=True))
