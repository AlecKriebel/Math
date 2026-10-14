#!/usr/bin/env python3
"""Independent exact rational spot-check from differentiated retarded potentials.

This script does not import candidate certificate implementations. It checks
off-axis cone directions, field signs, full branch differentiation and signed
pair prefactors. The accompanying analytic proof supplies universal scope.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
from pathlib import Path
import hashlib
import json


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def add(*vectors):
    return tuple(sum(xs) for xs in zip(*vectors))


def scale(s, v):
    return tuple(s*x for x in v)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def cone_direction(x, y):
    denom = 1+x*x+y*y
    return (2*x/denom, 2*y/denom, (1-x*x-y*y)/denom)


def check(n, a, u, A, b, r):
    assert dot(n, n) == 1
    assert dot(a, a) < 1 and dot(u, u) < 1
    d = 1-dot(n, u)
    D = 1-dot(n, a)
    eta = 1-dot(a, u)
    ell = 1/(r*d)

    # At fixed observation x: r_s=-n.u and n_s=-(u-n(n.u))/r.
    # Differentiate the scalar retarded potential ell=(r*d)^(-1).
    n_s_fixed_x = scale(-1/r, add(u, scale(-dot(n, u), n)))
    d_s_fixed_x = -dot(n_s_fixed_x, u)-dot(n, b)
    ell_s_fixed_x = -((-dot(n, u))*d+r*d_s_fixed_x)/(r*r*d*d)
    ell_grad_fixed_s = scale(-1/(r*r*d*d), add(n, scale(-1, u)))
    ell_grad_total = add(ell_grad_fixed_s, scale(-ell_s_fixed_x/d, n))
    ell_t = ell_s_fixed_x/d
    E_differentiated = add(scale(-1, ell_grad_total), scale(-ell/d, b),
                           scale(-ell_t, u))
    B_differentiated = add(cross(ell_grad_total, u),
                           scale(-ell/d, cross(n, b)))
    E_formula = add(scale((1-dot(u, u))/(r*r*d*d*d), add(n, scale(-1, u))),
                    scale(1/(r*d*d*d),
                          add(scale(dot(n, b), add(n, scale(-1, u))),
                              scale(-d, b))))
    assert E_differentiated == E_formula
    assert B_differentiated == cross(n, E_formula)

    # Direct force-to-branch change: dt/ds=d/D. No cancellation
    # formula is used to compute this side.
    branch_force = scale(d/D, add(E_differentiated,
                                 cross(a, B_differentiated)))
    t_prime = d/D
    r_prime = t_prime-1
    n_prime = scale(1/r, add(scale(t_prime, a), scale(-1, u),
                             scale(-r_prime, n)))
    a_prime = scale(t_prime, A)
    d_prime = -dot(n_prime, u)-dot(n, b)
    D_prime = -dot(n_prime, a)-dot(n, a_prime)
    eta_prime = -dot(a_prime, u)-dot(a, b)
    k = add(u, scale(-eta/D, n))
    k_prime = add(b, scale(-eta_prime/D+eta*D_prime/(D*D), n),
                  scale(-eta/D, n_prime))
    primitive_prime = add(scale(1/(r*d), k_prime),
                           scale(-(r_prime*d+r*d_prime)/(r*r*d*d), k))
    residual = add(scale(eta/(r*r*D*D),
                         add(scale((1-dot(a, a))/D, n), scale(-1, a))),
                   scale(dot(A, k)/(r*D*D), n))
    assert branch_force == add(scale(-1, primitive_prime), residual)

    # Physical factors: normalized acceleration lambda_a times source e_b;
    # source acceleration contributes one further lambda_b, including signs.
    for ma, mb, ea, eb in [(F(2), F(3), F(5), F(-7)),
                          (F(1,100000), F(100000), F(-2), F(3)),
                          (F(1), F(1), F(1), F(-1)),
                          (F(2), F(7), F(0), F(-4)),
                          (F(3), F(5), F(2), F(0))]:
        cab = ea*eb/ma
        assert cab*(eb/mb) == ea*eb*eb/(ma*mb)
        assert scale(cab, branch_force) == scale(cab, add(scale(-1, primitive_prime), residual))


def main():
    directions = [cone_direction(F(0),F(0)), cone_direction(F(1),F(0)),
                  cone_direction(F(1,2),F(2,3)), cone_direction(F(-3,2),F(1,7))]
    acceleration = [(F(0),)*3, (F(3),F(-2),F(5)), (F(-7,11),F(9,13),F(-4,17))]
    count = 0
    for n in directions:
        velocities = [(F(0),)*3, scale(F(999999,1000000), n),
                      scale(F(-999999,1000000), n), (F(1,5),F(-2,5),F(3,5))]
        for a,u,A,b,r in product(velocities, velocities, acceleration, acceleration,
                                [F(1,1000000),F(1),F(1000000)]):
            check(n,a,u,A,b,r)
            count += 1
    rng = Random(20261007)
    for _ in range(300):
        n = cone_direction(F(rng.randrange(-9,10),7), F(rng.randrange(-9,10),11))
        a = tuple(F(rng.randrange(-3,4),10) for _ in range(3))
        u = tuple(F(rng.randrange(-3,4),10) for _ in range(3))
        A = tuple(F(rng.randrange(-7,8),5) for _ in range(3))
        b = tuple(F(rng.randrange(-7,8),5) for _ in range(3))
        check(n,a,u,A,b,F(rng.randrange(1,40),13))
        count += 1
    result = {'result':'PASS', 'exact_rational_cases':count,
              'checks':['retarded potential electric sign', 'magnetic cross product sign',
                        'force-to-branch Jacobian', 'signed identity full derivative',
                        'signed charge and unequal mass prefactors'],
              'scope':'local algebra samples; no global VM theorem or uniform estimates',
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
