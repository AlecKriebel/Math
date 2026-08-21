#!/usr/local/bin/python
"""Discover the quartic Schur complement at a rank-one product-corner ray."""

import itertools
import numpy as np


def eps(p, i, j):
    return ((p, i, j) in ((0, 1, 2), (1, 2, 0), (2, 0, 1))) - (
        (p, i, j) in ((0, 2, 1), (2, 1, 0), (1, 0, 2)))


def d_basis(p, q, r):
    out = np.zeros((27, 27), dtype=complex)
    for aa in itertools.product(range(3), repeat=3):
        for ii in itertools.product(range(3), repeat=3):
            x = eps(p, aa[0], ii[0]) * eps(q, aa[1], ii[1]) * eps(r, aa[2], ii[2])
            if x:
                out[9 * aa[0] + 3 * aa[1] + aa[2], 9 * ii[0] + 3 * ii[1] + ii[2]] = x
    return out


DB = [d_basis(*idx) for idx in itertools.product(range(3), repeat=3)]


def dmat(z):
    return sum((z[i] * DB[i] for i in range(27)), np.zeros((27, 27), complex))


def q4(eta, delta=None):
    # Dhat(z)=D0+t D1+t^2 D2.  D0=000, D1=110.
    if delta is None:
        delta = np.zeros(27, complex); delta[12] = 1
    d0, d1, d2 = DB[0], dmat(delta), dmat(eta)
    ss = [
        d0.conj().T @ d0,
        d0.conj().T @ d1 + d1.conj().T @ d0,
        d1.conj().T @ d1 + d0.conj().T @ d2 + d2.conj().T @ d0,
        d1.conj().T @ d2 + d2.conj().T @ d1,
        d2.conj().T @ d2,
    ]
    pind = [9 * a + 3 * b + c for a, b, c in itertools.product((1, 2), repeat=3)]
    qind = [i for i in range(27) if i not in pind]
    def blk(m, rows, cols):
        return m[np.ix_(rows, cols)]
    a2 = blk(ss[2], pind, pind)
    a3 = blk(ss[3], pind, pind)
    a4 = blk(ss[4], pind, pind)
    b1 = blk(ss[1], pind, qind)
    b2 = blk(ss[2], pind, qind)
    b3 = blk(ss[3], pind, qind)
    c2 = blk(ss[2], qind, qind)
    h2 = a2 + b1 @ b1.conj().T
    h3 = a3 + b1 @ b2.conj().T + b2 @ b1.conj().T
    h40 = (a4 + b2 @ b2.conj().T + b1 @ b3.conj().T + b3 @ b1.conj().T
           + b1 @ c2 @ b1.conj().T)
    vals, vecs = np.linalg.eigh(h2)
    # The desired four-dimensional cluster is the four largest eigenvalues.
    order = np.argsort(vals)
    r = vecs[:, order[-4:]]
    q = vecs[:, order[:-4]]
    assert r.shape[1] == q.shape[1] == 4
    coeff = 0j
    for aa in order[-4:]:
        va, ha = vecs[:, aa], vals[aa]
        coeff += np.vdot(va, (h40 - ha * b1 @ b1.conj().T) @ va)
        for bb in order[:-4]:
            vb, hb = vecs[:, bb], vals[bb]
            coeff += abs(np.vdot(vb, h3 @ va)) ** 2 / (ha - hb)
    norm4 = 4 * np.vdot(eta, eta).real
    return float(np.real_if_close(norm4 - coeff))


def main():
    support = []
    for idx in itertools.product(range(3), repeat=3):
        wt = sum(i != 0 for i in idx)
        if wt >= 2:
            support.append(9 * idx[0] + 3 * idx[1] + idx[2])
    variables = []
    labels = []
    for i in support:
        e = np.zeros(27, complex); e[i] = 1
        variables.append(e); labels.append((i, "re"))
        variables.append(1j * e); labels.append((i, "im"))
    n = len(variables)
    gram = np.zeros((n, n))
    diag = [q4(v) for v in variables]
    for i in range(n):
        gram[i, i] = diag[i]
        for j in range(i):
            gram[i, j] = gram[j, i] = (q4(variables[i] + variables[j]) - diag[i] - diag[j]) / 2
    vals = np.linalg.eigvalsh(gram)
    print("variables", n)
    for value in sorted(set(np.round(vals, 10))):
        print(value, np.sum(np.isclose(vals, value, atol=1e-8)))
    print("diagonal nonzero")
    for lab, x in zip(labels, diag):
        if abs(x) > 1e-9:
            print(lab, x)

    rng = np.random.default_rng(17)
    eta = np.zeros(27, complex)
    eta[support] = rng.normal(size=len(support)) + 1j * rng.normal(size=len(support))
    predicted = q4(eta)
    for t in (1e-2, 5e-3, 2e-3):
        z = np.zeros(27, complex); z[0] = 1; z[12] = t; z += t * t * eta
        singular2 = np.linalg.eigvalsh(dmat(z).conj().T @ dmat(z))
        deficit = 4 * np.vdot(z, z).real - np.sum(singular2[-4:])
        print("numeric quotient", t, deficit / t**4, "predicted", predicted)


if __name__ == "__main__":
    main()
