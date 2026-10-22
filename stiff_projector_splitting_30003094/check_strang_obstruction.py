"""Literal exact affine-subflow regression for the stiff Strang obstruction.

Numerical corroboration only. The proof is in STRANG_OBSTRUCTION.md.
Uses the independently written augmented-matrix subflow implementation.
"""
import json
import mpmath as mp
from audit_exact_subflows import exact_ksl


def evaluate(n):
    mp.mp.dps = max(100, n + 80)
    nn = mp.mpf(n)
    alpha = 1 / nn
    c = mp.sqrt(1 - alpha**2)
    lam = nn**4
    tau = eta = 1 / nn
    h = tau / 2
    A = mp.zeros(2)
    B = mp.diag([0, -lam])
    C = mp.matrix([[0, 0], [eta, 0]])
    u0 = mp.matrix([1, 0])
    v0 = mp.matrix([c, alpha])
    Z, u, K, middle_first = exact_ksl(A, B, C, u0, v0, h)
    row = Z.T * u
    s = mp.norm(row)
    v = row / s
    # Transposing KSL on the transposed equation is LSK on this equation.
    WT, v1, L, middle_second = exact_ksl(B.T, A.T, C.T, v * s, u, h)
    W = WT.T
    X = mp.matrix([[1, 0], [eta * tau, 0]])
    L_expected = mp.matrix([row[0] + eta*u[1]*h,
                            row[1] * mp.exp(-lam*h)])
    b = (v1.T * B * v1)[0]
    jb = h if b == 0 else mp.expm1(h*b)/b
    I = mp.eye(2)
    endpoint = u * L_expected.T + (I-u*u.T)*C*v1*jb*v1.T
    exact_second = Z * mp.diag([1, mp.exp(-lam*h)]) + C * mp.diag([h, -mp.expm1(-lam*h)/lam])
    identity_residual = mp.norm(W-endpoint)
    bound = 2*h*mp.norm(C)
    error_second = mp.norm(W-exact_second)
    assert identity_residual < mp.mpf('1e-50')
    assert error_second <= bound + mp.mpf('1e-50')
    assert middle_first > 0 and middle_second > 0
    assert mp.norm(K) > 0 and mp.norm(L) > 0 and mp.norm(W) > 0
    return {
        'n': n, 'precision_digits': mp.mp.dps,
        'initial_error': mp.nstr(mp.sqrt(2-2*c), 25),
        'KSL_half_output_norm': mp.nstr(mp.norm(Z), 25),
        'Strang_output_norm': mp.nstr(mp.norm(W), 25),
        'Strang_error': mp.nstr(mp.norm(W-X), 25),
        'LSK_endpoint_identity_residual': mp.nstr(identity_residual, 8),
        'LSK_error': mp.nstr(error_second, 25),
        'LSK_error_bound': mp.nstr(bound, 25),
        'first_S_positive': bool(middle_first > 0),
        'second_S_positive': bool(middle_second > 0),
        'all_QR_endpoints_nonzero': True,
    }


if __name__ == '__main__':
    print(json.dumps({
        'description': 'Exact KSL(tau/2) followed by exact LSK(tau/2), implemented by transposition; augmented-matrix exponentials in all six subflows.',
        'parameter_sequence': 'alpha=eta=tau=1/n, lambda=n^4',
        'analytic_error_limit': 1,
        'checks': [evaluate(n) for n in [10, 30, 100, 300]],
        'all_pass': True,
    }, indent=2))
