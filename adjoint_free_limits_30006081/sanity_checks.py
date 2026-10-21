"""Reproducible numerical sanity checks; not proof or continuum certification."""
import json
import numpy as np
rng = np.random.default_rng(1855)
checks = {}
for field in ('real', 'complex'):

    def rand(shape):
        x = rng.normal(size=shape)
        return x if field == 'real' else x + 1j * rng.normal(size=shape)
    n, r = (13, 4)
    U = np.linalg.qr(rand((n, r)))[0]
    C = rand((r, r)) + 3 * np.eye(r)
    A = U @ C @ U.conj().T
    X = rand((n, r))
    Y = A @ X
    Q = np.linalg.qr(Y)[0]
    recovered = Y @ np.linalg.inv(Q.conj().T @ X) @ Q.conj().T
    checks[field + '_ep_relative_error'] = float(np.linalg.norm(A - recovered) / np.linalg.norm(A))
    m, n, d, k = (11, 14, 6, 3)
    A = rand((m, n))
    V = np.linalg.qr(rand((n, d)))[0]
    B = A @ V
    U, s, W = np.linalg.svd(B, full_matrices=False)
    hat = U[:, :k] * s[:k] @ W[:k] @ V.conj().T
    delta = A @ (np.eye(n) - V @ V.conj().T)
    sa = np.linalg.svd(A, compute_uv=False)
    checks[field + '_row_prior_frobenius_slack'] = float(np.linalg.norm(delta) ** 2 + sum(sa[k:] ** 2) - np.linalg.norm(A - hat) ** 2)
    checks[field + '_row_prior_spectral_slack'] = float(np.linalg.norm(delta, 2) ** 2 + sa[k] ** 2 - np.linalg.norm(A - hat, 2) ** 2)
    u = np.linalg.qr(rand((n, 1)))[0][:, 0]
    z = rand((n,))
    z -= u * np.vdot(u, z)
    z /= np.linalg.norm(z)
    alpha = 1.2 if field == 'real' else 1.2 + 0.7j
    a = 0.8
    radius = abs(alpha) * np.sqrt(a ** (-2) - 1)
    vp = np.conj(alpha) * u + radius * z
    vm = np.conj(alpha) * u - radius * z
    Ap = np.outer(u, vp.conj())
    Am = np.outer(u, vm.conj())
    checks[field + '_ball_diameter_error'] = float(abs(np.linalg.norm(Ap - Am, 2) - 2 * radius))
    checks[field + '_ball_query_error'] = float(np.linalg.norm(Ap @ u - alpha * u))
N = 80
D = np.zeros((N, N))
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j and (i + j) % 2:
            D[i - 1, j - 1] = 4 * i * j / (i * i - j * j)
if not np.linalg.norm(D + D.T) == 0:
    raise AssertionError()
records = []
for c in (0.0, 1.0, 10.0, 100.0, 1000.0):
    A = np.linalg.inv(np.diag((np.pi * np.arange(1, N + 1)) ** 2) + c * D)
    for s in (2, 5, 10):
        err = np.linalg.norm(A[:, s:], 2)
        bound = min((1 + abs(c) / np.pi) / (np.pi ** 2 * (s + 1) ** 2), 1 / (np.pi ** 2 * (s + 1)))
        records.append({'c': c, 's': s, 'galerkin_error': float(err), 'proved_continuum_bound': float(bound), 'within_bound': bool(err <= bound + 1e-12)})
checks['sine_galerkin_checks'] = records
if not all((v < 1e-10 for k, v in checks.items() if k.endswith('_error'))):
    raise AssertionError()
if not all((v >= -1e-10 for k, v in checks.items() if k.endswith('_slack'))):
    raise AssertionError()
if not all((x['within_bound'] for x in records)):
    raise AssertionError()
print(json.dumps(checks, indent=2))
