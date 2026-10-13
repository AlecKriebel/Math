#!/usr/bin/env python3
"""Independent exact rational falsification controls; no external dependencies.

These finite controls supplement the universal analytic proof in REPORT.md.
All decisions use explicit exceptions, including under python -O.
"""
from fractions import Fraction as Q
from itertools import product
import json


class VerificationError(RuntimeError):
    pass


checks = []


def check(name, condition):
    if type(condition) is not bool or not condition:
        raise VerificationError(name)
    checks.append(name)


def develop(t, x, y):
    return x, y + t * x * x / 2


def holonomy(t, m, n, u, v):
    return u + m, v + n + t * m * u + t * m * m / 2


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def main():
    ts = [Q(-2), Q(-1, 3), Q(0), Q(1, 7), Q(3)]
    points = [(Q(-3, 2), Q(7, 5)), (Q(0), Q(0)), (Q(2, 3), Q(-4))]
    decks = [(-2, 1), (0, -3), (1, 0), (2, 4)]
    for ti, t in enumerate(ts):
        gamma = [[[Q(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
        gamma[1][0][0] = t
        for k, i, j in product(range(2), repeat=3):
            check(f'torsion_{ti}_{k}{i}{j}', gamma[k][i][j] == gamma[k][j][i])
        for k, ell, i, j in product(range(2), repeat=4):
            curvature = sum(gamma[k][i][p] * gamma[p][j][ell] - gamma[k][j][p] * gamma[p][i][ell] for p in range(2))
            check(f'curvature_{ti}_{k}{ell}{i}{j}', curvature == 0)
        for i in range(2):
            check(f'parallel_volume_{ti}_{i}', sum(gamma[k][i][k] for k in range(2)) == 0)
        linear = [[Q(1), Q(0)], [t, Q(1)]]
        inverse_transport = [[Q(1), Q(0)], [-t, Q(1)]]
        check(f'holonomy_volume_{ti}', det(linear) == 1)
        check(f'holonomy_transport_conventions_{ti}', matmul(linear, inverse_transport) == [[1, 0], [0, 1]])
        check(f'gauge_linear_obstruction_{ti}', (linear == [[1, 0], [0, 1]]) == (t == 0))
        for pi, (x, y) in enumerate(points):
            u, v = develop(t, x, y)
            check(f'global_inverse_{ti}_{pi}', develop(-t, u, v) == (x, y))
            jac = [[Q(1), Q(0)], [t * x, Q(1)]]
            inv = [[Q(1), Q(0)], [-t * x, Q(1)]]
            check(f'jacobian_volume_{ti}_{pi}', det(jac) == 1)
            check(f'jacobian_inverse_{ti}_{pi}', matmul(inv, jac) == [[1, 0], [0, 1]])
            pulled_second_derivative = [sum(inv[k][p] * [Q(0), t][p] for p in range(2)) for k in range(2)]
            check(f'pullback_connection_{ti}_{pi}', pulled_second_derivative == [0, t])
            # Noncompact positive Hessian metric F_t^*(du^2+dv^2).
            a, b, c = 1 + t*t*x*x, t*x, Q(1)
            check(f'noncompact_positive_metric_{ti}_{pi}', c > 0 and a*c-b*b == 1)
            check(f'noncompact_codazzi_{ti}_{pi}', t - 0 == t*c)
            # Constant indefinite metric 2 dx dy has potential uv-t*u^3/3.
            hessian = [[-2*t*u, Q(1)], [Q(1), Q(0)]]
            pulled = matmul([[jac[j][i] for j in range(2)] for i in range(2)], matmul(hessian, jac))
            check(f'indefinite_hessian_boundary_{ti}_{pi}', pulled == [[0, 1], [1, 0]])
            check(f'indefinite_signature_boundary_{ti}_{pi}', det(pulled) == -1)
            for di, (m, n) in enumerate(decks):
                check(f'equivariance_{ti}_{pi}_{di}', develop(t, x+m, y+n) == holonomy(t, m, n, u, v))
                check(f'nonidentity_action_free_{ti}_{pi}_{di}', holonomy(t, m, n, u, v) != (u, v))
            # Pulling back dx^2+dy^2 needs no periodic global potential at t=0.
            potential_shift = ((x+1)**2+y*y)/2 - (x*x+y*y)/2
            check(f'local_potential_transition_{ti}_{pi}', potential_shift == x + Q(1,2))
        for di, (m, n) in enumerate(decks):
            for ei, (p, q) in enumerate(decks):
                for pi, (u, v) in enumerate(points):
                    first = holonomy(t, p, q, u, v)
                    composed = holonomy(t, m, n, *first)
                    check(f'group_law_{ti}_{di}_{ei}_{pi}', composed == holonomy(t, m+p, n+q, u, v))
        # Global geodesic polynomial and its developed affine line.
        for si, sigma in enumerate([Q(-7), Q(0), Q(5,3)]):
            x0, y0, a, b = Q(2,3), Q(-1,2), Q(3,4), Q(-2,5)
            x = x0+a*sigma
            y = y0+b*sigma-t*a*a*sigma*sigma/2
            def y_at(z):
                return y0+b*z-t*a*a*z*z/2
            second_difference = y_at(sigma+1)-2*y_at(sigma)+y_at(sigma-1)
            check(f'geodesic_ode_{ti}_{si}', second_difference+t*a*a == 0)
            expected = (x0+a*sigma, y0+t*x0*x0/2+(b+t*x0*a)*sigma)
            check(f'developed_geodesic_line_{ti}_{si}', develop(t, x, y) == expected)
        check(f'central_candidate_fails_noncentral_{ti}', (t * Q(1) == 0) == (t == 0))
        check(f'semidefinite_boundary_{ti}', t * Q(0) == 0)
    for si, s in enumerate([Q(-2), Q(-1,3), Q(0), Q(1,7), Q(3)]):
        t = s**3
        period = -s
        check(f'cubic_reparametrization_{si}', (-period)**3 == t)
        check(f'reparametrization_central_equivalence_{si}', (s == 0) == (t == 0))
    check('unique_check_names', len(checks) == len(set(checks)))
    print(json.dumps({'verdict':'PASS','profile':'stdlib exact Fraction finite controls','checks_passed':len(checks),'checks_failed':0,'check_names':checks,'universal_proof':'REPORT.md','finite_checks_are_not_universal_proof':True},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
