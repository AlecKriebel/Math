"""Independent literal affine-flow audit for two direct K-S-L examples.

Uses matrix exponential of the augmented affine system in each substep.
Numerical agreement supports but does not replace AUDIT_COUNTEREXAMPLE.md.
"""
import json
import mpmath as mp


def affine_flow(M, g, x, tau):
    n = len(x)
    H = mp.zeros(n + 1)
    for i in range(n):
        for j in range(n):
            H[i, j] = M[i, j]
        H[i, n] = g[i]
    E = mp.expm(tau * H)
    z = mp.matrix(list(x) + [mp.mpf(1)])
    return (E * z)[:n, 0]


def exact_ksl(A, B, C, u0, v0, tau):
    I = mp.eye(len(u0))
    b = (v0.T * B * v0)[0]
    K = affine_flow(A + b * I, C * v0, u0, tau)
    s = mp.norm(K)
    u = K / s
    a = (u.T * A * u)[0]
    d = (u.T * C * v0)[0]
    middle = affine_flow(mp.matrix([[-a - b]]), mp.matrix([-d]), mp.matrix([s]), tau)[0]
    L = affine_flow(B.T + a * mp.eye(len(v0)), C.T * u, v0 * middle, tau)
    return u * L.T, u, K, middle


def plain(M):
    return [[mp.nstr(M[i, j], 32) for j in range(M.cols)] for i in range(M.rows)]


def two_sided(n):
    mp.mp.dps = max(100, n + 60)
    n = mp.mpf(n)
    lam = n**2
    h = eta = 1/n
    A = B = mp.diag([0, -lam])
    C = eta * mp.eye(2)
    v = mp.matrix([1, 1]) / mp.sqrt(2)
    Y, u, K, middle = exact_ksl(A, B, C, v, v, h)
    exact = mp.matrix([[mp.mpf('.5') + eta*h, mp.exp(-lam*h)/2],
                       [mp.exp(-lam*h)/2, mp.exp(-2*lam*h)/2 + eta*(-mp.expm1(-2*lam*h))/(2*lam)]])
    target = mp.matrix([[mp.mpf(3)/8, 0], [mp.mpf(1)/8, 0]])
    return {'n': int(n), 'precision': mp.mp.dps, 'Y': plain(Y),
            'error': mp.nstr(mp.norm(Y-exact), 32),
            'distance_to_limiting_Y': mp.nstr(mp.norm(Y-target), 32),
            'K_norm': mp.nstr(mp.norm(K), 15)}


def one_sided(n, convergent_initial=False):
    mp.mp.dps = max(100, n + 60) if not convergent_initial else max(100, int(mp.sqrt(n)) + 60)
    n = mp.mpf(n)
    lam = n**2
    h = eta = 1/n
    A = mp.zeros(2)
    B = mp.diag([0, -lam])
    C = mp.matrix([[0, 0], [eta, 0]])
    u0 = mp.matrix([1, 0])
    alpha = n**(-mp.mpf(1)/4) if convergent_initial else 1/mp.sqrt(2)
    v = mp.matrix([mp.sqrt(1-alpha**2), alpha])
    Y, u, K, middle = exact_ksl(A, B, C, u0, v, h)
    exact_from_Y0 = mp.matrix([[v[0], v[1]*mp.exp(-lam*h)], [eta*h, 0]])
    projection = u * u.T * exact_from_Y0
    E = mp.exp(-lam*alpha**2*h)
    K_formula = mp.matrix([E, eta*v[0]/(lam*alpha**2)*(1-E)])
    exact_reference = mp.matrix([[1, 0], [eta*h, 0]]) if convergent_initial else exact_from_Y0
    Y0 = u0*v.T
    X0 = mp.matrix([[1,0],[0,0]]) if convergent_initial else Y0
    return {'n': int(n), 'precision': mp.mp.dps, 'Y': plain(Y),
            'error': mp.nstr(mp.norm(Y-exact_reference), 32),
            'initial_delta': mp.nstr(mp.norm(Y0-X0), 32),
            'K_formula_residual': mp.nstr(mp.norm(K-K_formula), 8),
            'S_cancellation_residual': mp.nstr(abs(middle-u[0]), 8),
            'projection_identity_residual': mp.nstr(mp.norm(Y-projection), 8)}


if __name__ == '__main__':
    result = {'method': 'Literal augmented-matrix affine flow for K, negative S, and L; mpmath arbitrary precision.',
              'two_sided': [two_sided(n) for n in [30,100,300]],
              'one_sided': [one_sided(n) for n in [30,100,300]],
              'vanishing_rough_initial_perturbation': [one_sided(n, True) for n in [100,1000,10000]],
              'status': 'numerical validation only; analytic proof in AUDIT_COUNTEREXAMPLE.md'}
    print(json.dumps(result, indent=2))
