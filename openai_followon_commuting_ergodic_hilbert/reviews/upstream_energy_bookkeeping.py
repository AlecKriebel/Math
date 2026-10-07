"""Exact saved procedure for the upstream_energy_audit numerical claims.

This reproduces the inline procedure originally run during the audit.
The check is limited to floating-point matrix bookkeeping. In particular,
the numerical support cutoff is not a proof for singular or tiny spectra.
Requires NumPy; no arguments or input files are used.
"""

import numpy as np

rng = np.random.default_rng(812606)


def cost(P, K):
    p, U = np.linalg.eigh((P + P.conj().T) / 2)
    p = np.maximum(p, 0)
    k = U.conj().T @ K @ U
    den = np.sqrt(p)[:, None] + np.sqrt(p)[None, :]
    cutoff = max(np.max(p), 1) * 1e-12
    keep = (p[:, None] > cutoff) & (p[None, :] > cutoff)
    return 1.5 * np.sum(np.abs(k[keep]) ** 2 / den[keep])


max_mixed = 0.0
max_neighbor = 0.0
for trial in range(5000):
    dims = rng.integers(1, 6, size=3)
    W = [
        rng.normal(size=(dims[v], dims[(v + 1) % 3]))
        + 1j * rng.normal(size=(dims[v], dims[(v + 1) % 3]))
        for v in range(3)
    ]
    if trial % 2 == 0:
        W = [x[:, :1] @ rng.normal(size=(1, x.shape[1])) for x in W]
    D = []
    for d in dims:
        x = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        D.append((x + x.conj().T) / 2)
    R = [
        np.concatenate([W[v], W[(v - 1) % 3].conj().T], axis=1)
        for v in range(3)
    ]
    T = [x.conj().T @ x for x in R]
    S = [x @ x.conj().T for x in R]
    V = [cost(T[v], R[v].conj().T @ D[v] @ R[v]) for v in range(3)]
    lhs = abs(np.trace(D[0] @ W[0] @ D[1] @ W[1] @ D[2] @ W[2]))
    rhs = (5 / 3) * max(np.linalg.norm(x, 2) for x in D) * sum(V)
    max_mixed = max(max_mixed, lhs / rhs)
    for w in range(3):
        A = W[w]
        B = W[(w - 1) % 3].conj().T
        Yplus = cost(S[(w + 1) % 3], A.conj().T @ D[w] @ A)
        Yminus = cost(S[(w - 1) % 3], B.conj().T @ D[w] @ B)
        max_neighbor = max(
            max_neighbor, (Yplus + Yminus) / (np.sqrt(2) * V[w])
        )

print("5000 random/rank-deficient cyclic tests; max mixed ratio", max_mixed)
print("15000 neighbor tests; max neighbor ratio", max_neighbor)
