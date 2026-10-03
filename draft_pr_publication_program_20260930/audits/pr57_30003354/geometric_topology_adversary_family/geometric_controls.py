"""Independent exact geometric controls, not a finite surrogate for the endpoint proof."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    x, y, u, v = sp.symbols('x y u v', real=True)
    rho, eps = sp.symbols('rho eps', positive=True)
    results = []

    # Nonorthogonal coordinates distinguish the two possible matrix orders.
    J = sp.Matrix([[2, 1], [0, 3]])
    A = J.inv() * J.inv().T
    wrong_A = J.inv().T * J.inv()
    potential = x*x + 3*x*y + 2*y*y
    inverse = J.inv() * sp.Matrix([u, v])
    composed = potential.subs({x: inverse[0], y: inverse[1]}, simultaneous=True)
    direct = sp.diff(composed, u, 2) + sp.diff(composed, v, 2)
    hessian = sp.hessian(potential, (x, y))
    operator = sum(A[i,j] * hessian[i,j] for i in range(2) for j in range(2))
    wrong = sum(wrong_A[i,j] * hessian[i,j] for i in range(2) for j in range(2))
    assert sp.simplify(direct - operator) == 0 and direct == sp.Rational(2,3)
    assert wrong == sp.Rational(5,9) and wrong != direct
    results.append({'control': 'affine pulled-back Laplacian matrix order', 'correct': str(direct),
                    'wrong_order': str(wrong), 'purpose': 'Detects a genuinely different operator, not numerical grid agreement'})

    # An inverse-map drift term cannot be dropped even when J=I at a point.
    t = sp.symbols('t', real=True)
    local_inverse = (sp.sqrt(1 + 4*t) - 1) / 2
    drift = sp.diff(local_inverse, t, 2).subs(t, 0)
    assert drift == -2
    results.append({'control': 'nonlinear inverse-map first-order coefficient', 'drift_at_origin': str(drift),
                    'purpose': 'The second inverse derivative is required in the exact operator'})

    # Critical logarithmic scale: remove the harmonic -2 rho xi jet exactly.
    q = x*x + y*y
    M_real = x * (sp.log(1 + q) + q / (2*(1 + q)))
    lap_M = sp.simplify(sp.diff(M_real, x, 2) + sp.diff(M_real, y, 2))
    value = sp.simplify(lap_M.subs({x: -1, y: 0}))
    assert value == -sp.Rational(7,2)
    results.append({'control': 'uncorrected r1 curvature leading coefficient', 'point': 'scaled (-1,0)',
                    'laplacian_Re_M': str(value), 'purpose': 'Negative leading curvature shows the correction has mathematical work to do'})

    radius = sp.sqrt(q + 1)
    lap_radius = sp.simplify(sp.diff(radius, x, 2) + sp.diff(radius, y, 2))
    correction_value = sp.simplify(lap_radius.subs({x: -1, y: 0}))
    assert correction_value == 3*sp.sqrt(2)/4
    results.append({'control': 'convex radius correction leading coefficient', 'point': 'scaled (-1,0)',
                    'laplacian_radius': str(correction_value), 'pointwise_K_threshold': str(7*sp.sqrt(2)/3)})

    # At r1, failure is also seen in the function factor; no inverse formula is needed
    # because the exact Jacobian at the normalization point is the identity.
    L = sp.log(q + rho*rho) / 2
    f = sp.Matrix([x + eps*(x*x - y*y)*L, y + eps*2*x*y*L])
    jacobian = f.jacobian((x, y))
    assert jacobian.subs({x: 0, y: 0}) == sp.eye(2)
    # f_z has real part (f1_x+f2_y)/2 and imaginary part (f2_x-f1_y)/2.
    real_fz = (jacobian[0,0] + jacobian[1,1])/2
    imag_fz = (jacobian[1,0] - jacobian[0,1])/2
    h = sp.log(real_fz*real_fz + imag_fz*imag_fz)/2
    grad_h = [sp.simplify(sp.diff(h, coord).subs({x: 0, y: 0})) for coord in (x, y)]
    assert grad_h == [2*eps*sp.log(rho), 0]
    results.append({'control': 'r1 conformal factor jet at the fixed normalization point',
                    'gradient_h': [str(a) for a in grad_h], 'epsilon_log_rho': '-1',
                    'resulting_gradient_u_difference': ['-2', '0']})

    out = {'schema': 'pr57-independent-geometric-exact-controls/v1', 'operator_pid': os.getpid(),
           'utc': datetime.now(timezone.utc).isoformat(), 'symbolic_engine': 'sympy',
           'symbolic_engine_version': sp.__version__, 'control_count': len(results), 'controls': results,
           'every_control_exact': True, 'universal_proof_provided_separately': True,
           'finite_controls_claim_full_source_solved': False, 'author_checker_read_or_replayed': False}
    (ROOT / 'GEOMETRIC_CONTROL_RESULTS.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__': main()
