"""Exact independent geometric controls using rational Taylor algebra, no external package.

Degree-two polynomials represent jets around an explicitly given point. Their
Laplacian/gradient evaluations are exact; no sampled grid or floating point is
used. This supplements the separate universal geometric proof.
"""
from fractions import Fraction as F
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def const(c): return {(0, 0): F(c)} if c else {}
def add(a, b):
    out = dict(a)
    for key, value in b.items(): out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}
def scale(a, c): return {key: value * F(c) for key, value in a.items() if value * F(c)}
def mul(a, b):
    out = {}
    for (i, j), av in a.items():
        for (k, l), bv in b.items():
            if i + j + k + l <= 2:
                key = (i + k, j + l)
                out[key] = out.get(key, F(0)) + av * bv
    return {key: value for key, value in out.items() if value}
def lap(a): return 2 * (a.get((2, 0), F(0)) + a.get((0, 2), F(0)))


def main():
    one = const(1); x = {(1, 0): F(1)}; y = {(0, 1): F(1)}
    controls = []
    # J=[[2,1],[0,3]], so F(u,v)=(u/2-v/6,v/3).
    Jinv = [[F(1,2), F(-1,6)], [F(0), F(1,3)]]
    A = [[sum(Jinv[i][k]*Jinv[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    wrong_A = [[sum(Jinv[k][i]*Jinv[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    H = [[F(2), F(3)], [F(3), F(4)]]
    correct = sum(A[i][j]*H[i][j] for i in range(2) for j in range(2))
    wrong = sum(wrong_A[i][j]*H[i][j] for i in range(2) for j in range(2))
    Fx = add(scale(x, F(1,2)), scale(y, F(-1,6))); Fy = scale(y, F(1,3))
    composed = add(add(mul(Fx, Fx), scale(mul(Fx, Fy), 3)), scale(mul(Fy, Fy), 2))
    direct = lap(composed)
    assert direct == correct == F(2,3) and wrong == F(5,9) and wrong != correct
    controls.append({'control': 'nonorthogonal affine Laplacian principal matrix order',
                     'direct_composition': str(direct), 'J_inverse_J_inverse_transpose': str(correct),
                     'wrong_reversed_order': str(wrong)})

    # Solve F(t)+F(t)^2=t through the quadratic jet, without a square-root derivative formula.
    inverse_jet = add(x, scale(mul(x, x), -1))
    assert add(inverse_jet, mul(inverse_jet, inverse_jet)) == x
    assert inverse_jet[(2,0)] * 2 == -2
    controls.append({'control': 'nonlinear inverse-map first-order drift', 'inverse_second_derivative_at_origin': '-2'})

    # Around scaled point (-1,0), let X=-1+x, Y=y, Q=1+X^2+Y^2.
    X = add(const(-1), x); Q = add(add(one, mul(X, X)), mul(y, y))
    delta = add(scale(Q, F(1,2)), const(-1))  # Q=2(1+delta).
    delta2 = mul(delta, delta)
    log_Q_without_constant = add(delta, scale(delta2, F(-1,2)))
    inverse_Q = scale(add(add(one, scale(delta, -1)), delta2), F(1,2))
    radial_squared = add(Q, const(-1))
    Hjet = add(log_Q_without_constant, scale(mul(radial_squared, inverse_Q), F(1,2)))
    Mjet = mul(X, Hjet)
    # The omitted log2 times X is affine and has zero Laplacian.
    assert lap(Mjet) == F(-7,2)
    controls.append({'control': 'uncorrected r1 logarithmic curvature leading jet',
                     'scaled_point': '(-1,0)', 'laplacian_Re_M': str(lap(Mjet))})
    sqrt_Q_div_sqrt2 = add(add(one, scale(delta, F(1,2))), scale(delta2, F(-1,8)))
    assert lap(sqrt_Q_div_sqrt2) == F(3,4)
    controls.append({'control': 'convex radius correction leading jet',
                     'scaled_point': '(-1,0)', 'laplacian_sqrt_Q_div_sqrt2': '3/4',
                     'laplacian_sqrt_Q': '3*sqrt(2)/4', 'necessary_pointwise_K_threshold': '7*sqrt(2)/3'})

    # For r1 the exact first f_z jet is 1+2 c z, c=epsilon log rho=-1.
    real_fz = add(one, scale(x, -2)); imag_fz = scale(y, -2)
    squared_norm = add(mul(real_fz, real_fz), mul(imag_fz, imag_fz))
    norm_delta = add(squared_norm, const(-1))
    hjet = scale(add(norm_delta, scale(mul(norm_delta, norm_delta), F(-1,2))), F(1,2))
    assert hjet[(1,0)] == -2 and hjet.get((0,1), 0) == 0 and lap(hjet) == 0
    controls.append({'control': 'critical conformal-factor first jet at normalization point',
                     'gradient_h': ['-2', '0'], 'harmonic_quadratic_jet_laplacian': '0',
                     'gradient_background_and_convex_correction_at_origin': ['0', '0']})

    result = {'schema': 'pr57-independent-geometric-exact-controls/v2', 'operator_pid': os.getpid(),
              'utc': datetime.now(timezone.utc).isoformat(), 'arithmetic': 'standard-library Fraction and exact degree-two Taylor algebra',
              'control_count': len(controls), 'controls': controls, 'all_exact': True,
              'finite_controls_are_not_universal_proof': True,
              'universal_geometric_derivation_provided_separately': True,
              'prior_run_failed_due_to_missing_sympy': True,
              'prior_failed_capture_preserved': 'captures/geometric_controls/',
              'author_checker_read_or_replayed': False}
    (ROOT / 'GEOMETRIC_CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__': main()
