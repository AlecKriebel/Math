#!/usr/bin/env python3
"""Own exact-rational diagnostics; no deposited or foreign program is executed."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
from datetime import datetime, timezone
import json

E = Path(__file__).resolve().parent


def const(v, d=2): return {(0,) * d: F(v)} if v else {}
def var(i, d=2): return {tuple(int(i == j) for j in range(d)): F(1)}
def clean(p): return {m: F(v) for m, v in p.items() if v}
def add(*ps):
    out = {}
    for p in ps:
        for m, v in p.items(): out[m] = out.get(m, F(0)) + v
    return clean(out)
def scale(p, v): return clean({m: q * v for m, q in p.items()})
def mul(p, q):
    out = {}
    for a, v in p.items():
        for b, w in q.items():
            m = tuple(i + j for i, j in zip(a, b))
            out[m] = out.get(m, F(0)) + v * w
    return clean(out)
def power(p, n, d=2):
    out = const(1, d)
    for _ in range(n): out = mul(out, p)
    return out
def deriv(p, i):
    out = {}
    for m, v in p.items():
        if m[i]:
            a = list(m); a[i] -= 1; out[tuple(a)] = v * m[i]
    return clean(out)
def same(p, q): return not add(p, scale(q, -1))
def substitute(p, xs):
    out = {}
    for m, v in p.items():
        term = const(v)
        for x, n in zip(xs, m): term = mul(term, power(x, n))
        out = add(out, term)
    return out
def homogeneous(p, degree): return all(sum(m) == degree for m in p)
def cmul(a, b):
    return (add(mul(a[0], b[0]), scale(mul(a[1], b[1]), -1)),
            add(mul(a[0], b[1]), mul(a[1], b[0])))
def cpow(z, m, d):
    out = const(1, d), {}
    for _ in range(m): out = cmul(out, z)
    return out


def derivative_checks():
    x, y, rho = [var(i, 3) for i in range(3)]
    S = add(power(x, 2, 3), power(y, 2, 3), power(rho, 2, 3))
    current = {(1, 0): x, (0, 1): y}; count = 0
    for j in range(1, 10):
        for p in current.values():
            assert homogeneous(p, j)
            assert sum(abs(v) for v in p.values()) <= 5 ** (j - 1) * factorial(j - 1)
            count += 1
        nxt = {}
        for counts, p in current.items():
            for i, coordinate in enumerate([x, y]):
                q = add(mul(S, deriv(p, i)), scale(mul(coordinate, p), -2 * j))
                key = tuple(c + int(i == k) for k, c in enumerate(counts))
                if key in nxt: assert same(q, nxt[key])
                nxt[key] = q
        current = nxt
    anti_count = 0
    for r in range(1, 9):
        z = x, y
        H = cpow(z, r + 1, 3)
        # The logarithmic term in dbar(H L) cancels by the polynomial CR identity.
        assert same(deriv(H[0], 0), deriv(H[1], 1))
        assert same(deriv(H[1], 0), scale(deriv(H[0], 1), -1))
        numerator = cmul(H, z)
        target = cpow(z, r + 2, 3)
        assert all(same(a, b) for a, b in zip(numerator, target))
        current = {(0, 0): tuple(scale(p, F(1, 2)) for p in numerator)}
        for k in range(r + 1):
            for pair in current.values():
                assert all(homogeneous(p, r + 2 + k) for p in pair)
                # Denominator S^(k+1) leaves homogeneity r-k, nonnegative here.
                assert r - k >= 0
                anti_count += 1
            nxt = {}
            for counts, pair in current.items():
                for i, coordinate in enumerate([x, y]):
                    qq = tuple(add(mul(S, deriv(p, i)), scale(mul(coordinate, p), -2 * (k + 1))) for p in pair)
                    key = tuple(c + int(i == a) for a, c in enumerate(counts))
                    if key in nxt: assert all(same(a, b) for a, b in zip(qq, nxt[key]))
                    nxt[key] = qq
            current = nxt
    return {'log_derivative_orders': 9, 'distinct_log_multiindices': count,
            'mixed_derivatives_commute_exactly': True,
            'coefficient_l1_inductive_bound_holds_on_checked_orders': True,
            'endpoint_r_values': list(range(1, 9)), 'antiholomorphic_multiindices': anti_count,
            'polynomial_CR_cancellation_exact': True,
            'nonnegative_scaling_exponent_through_k_equals_r': True,
            'universal_claim_relies_on_written_induction': True}


def pmm(A, B):
    return [[add(*[mul(a, b) for a, b in zip(row, column)]) for column in zip(*B)] for row in A]
def trans(A): return [list(row) for row in zip(*A)]


def operator_checks():
    x, y = var(0), var(1)
    scalars = [x, y, power(x, 2), mul(x, y), power(y, 2),
               add(power(x, 3), scale(mul(x, power(y, 2)), 3), y)]
    count = 0; wrong_order_rejected = False; dropped_drift_rejected = False
    for a in [F(1, 3), F(-2, 5)]:
        for b in [F(1, 2), F(3, 2), F(2)]:
            f = [add(x, scale(power(y, 2), a)), scale(y, b)]
            inverse = [add(x, scale(power(y, 2), -a / b ** 2)), scale(y, 1 / b)]
            H = [[const(1), scale(y, -2 * a / b)], [{}, const(1 / b)]]
            A = pmm(H, trans(H)); wrong = pmm(trans(H), H)
            B = [const(-2 * a / b ** 2), {}]
            for v in scalars:
                composed = substitute(v, inverse)
                direct = substitute(add(deriv(deriv(composed, 0), 0), deriv(deriv(composed, 1), 1)), f)
                principal = add(*[mul(A[i][j], deriv(deriv(v, i), j)) for i in range(2) for j in range(2)])
                drift = add(*[mul(B[i], deriv(v, i)) for i in range(2)])
                assert same(direct, add(principal, drift))
                incorrect = add(*[mul(wrong[i][j], deriv(deriv(v, i), j)) for i in range(2) for j in range(2)], drift)
                wrong_order_rejected |= not same(direct, incorrect)
                dropped_drift_rejected |= not same(direct, principal)
                count += 1
    assert wrong_order_rejected and dropped_drift_rejected
    return {'explicit_nonlinear_triangular_diffeomorphisms': 6,
            'exact_global_polynomial_operator_identities': count,
            'direct_inverse_composition_laplacian_matches_HHT_plus_drift': True,
            'HTH_negative_control_rejected': True, 'dropped_drift_negative_control_rejected': True}


def metric_checks():
    cases = 0
    for p in [(F(1), F(0)), (F(3, 2), F(1, 3)), (F(-2), F(1))]:
        for q in [(F(1, 5), F(2, 7)), (F(-1, 4), F(1, 8))]:
            pr, pi = p; qr, qi = q; norm = pr * pr + pi * pi
            ar = (qr * pr + qi * pi) / norm; ai = (qi * pr - qr * pi) / norm
            J = [[pr + qr, -pi + qi], [pi + qi, pr - qr]]
            gram = [[sum(J[k][i] * J[k][j] for k in range(2)) / norm for j in range(2)] for i in range(2)]
            mu2 = ar * ar + ai * ai
            assert mu2 < 1
            assert gram == [[1 + mu2 + 2 * ar, 2 * ai], [2 * ai, 1 + mu2 - 2 * ar]]
            assert gram[0][0] * gram[1][1] - gram[0][1] ** 2 == (1 - mu2) ** 2
            cases += 1
    return {'rational_complex_derivative_cases': cases,
            'exact_pullback_metric_factor_and_distortion_coefficients_match': True,
            'positive_determinant_and_orientation_match': True}


def radius_checks():
    count = 0
    for scale0 in [F(1, 2), F(1, 10 ** 12)]:
        for x0, y0, r0, s0 in [(0, 0, 1, 1), (3, 0, 4, 5), (3, 4, 12, 13)]:
            x, y, rho, s = [F(a) * scale0 for a in (x0, y0, r0, s0)]
            assert s * s == x * x + y * y + rho * rho
            D = [[F(i == j) / s - [x, y][i] * [x, y][j] / s ** 3 for j in range(2)] for i in range(2)]
            delta = D[0][0] + D[1][1]
            assert delta == (x * x + y * y + 2 * rho * rho) / s ** 3 >= 1 / s
            assert D[0][0] > 0 and D[0][0] * D[1][1] - D[0][1] ** 2 == rho * rho / s ** 4 > 0
            for t in [F(-1, 4), F(0), F(1, 4)]:
                A = [[1 + t * t, -t], [-t, F(1)]]
                trace = sum(A[i][j] * D[i][j] for i in range(2) for j in range(2))
                assert trace >= delta / 2
                count += 1
    return {'exact_positive_radius_Hessian_and_elliptic_trace_cases': count,
            'origin_and_small_regularization_included': True,
            'laplacian_at_least_inverse_radius': True,
            'scope': 'Finite exact controls; written estimates handle all radii, drift and n.'}


def run_checks():
    return {'derivative_controls': derivative_checks(), 'inverse_laplacian': operator_checks(),
            'metric_reconstruction': metric_checks(), 'convex_radius': radius_checks(), 'all_pass': True}


if __name__ == '__main__':
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'arithmetic': 'Python Fraction; no external dependency', **run_checks(),
              'scope': 'Own diagnostics corroborate identities and reject operator errors; universal proof, global geometry and priority are not certified by finite tests.'}
    (E / 'independent-exact-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
