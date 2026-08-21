#!/usr/bin/env /usr/bin/python3
"""Probe the local effect Hessian on code-invisible qutrit directions.

This is discovery code only.  For a rank-two code projection P on four
qutrits and a chosen physical site, it forms

    N(A) = [t^2] Q_4(sqrt(I+tA) P sqrt(I+tA))

on the nine-dimensional real space of Hermitian qutrit matrices, then
restricts N to ker(A -> U^*(A tensor I)U).
"""

import argparse
import itertools

import numpy as np
import scipy.linalg


def hermitian_basis():
    out = []
    for i in range(3):
        a = np.zeros((3, 3), dtype=complex)
        a[i, i] = 1
        out.append(a)
    for i in range(3):
        for j in range(i + 1, 3):
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = a[j, i] = 1 / np.sqrt(2)
            out.append(a)
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = -1j / np.sqrt(2)
            a[j, i] = 1j / np.sqrt(2)
            out.append(a)
    return out


def partial_trace_matrix(h, traced):
    n = 4
    tensor = h.reshape((3,) * (2 * n))
    live = n
    for site in sorted(traced, reverse=True):
        tensor = np.trace(tensor, axis1=site, axis2=live + site)
        live -= 1
    return tensor.reshape(3**live, 3**live)


def endpoint_q(h):
    value = 0.0
    for r in range(5):
        for traced in itertools.combinations(range(4), r):
            reduced = partial_trace_matrix(h, traced)
            value += (-0.5) ** r * np.vdot(reduced, reduced).real
    return value


def filter_projection(p, effect, site):
    vals, vecs = np.linalg.eigh(effect)
    if np.min(vals) < -1e-10:
        raise ValueError("effect is not positive")
    root = (vecs * np.sqrt(np.maximum(vals, 0))) @ vecs.conj().T
    tensor = p.reshape((3,) * 8)
    tensor = np.tensordot(root, tensor, axes=(1, site))
    tensor = np.moveaxis(tensor, 0, site)
    tensor = np.tensordot(tensor, root, axes=(4 + site, 0))
    tensor = np.moveaxis(tensor, -1, 4 + site)
    return tensor.reshape(81, 81)


def n_value(p, a, site, eps=0.2):
    ident = np.eye(3)
    scale = max(1.0, np.linalg.norm(a, 2))
    t = eps / scale
    qp = endpoint_q(filter_projection(p, ident + t * a, site))
    qm = endpoint_q(filter_projection(p, ident - t * a, site))
    q0 = endpoint_q(p)
    return (qp + qm - 2 * q0) / (2 * t * t)


def random_isometry(rng):
    z = rng.normal(size=(81, 2)) + 1j * rng.normal(size=(81, 2))
    q, _ = np.linalg.qr(z)
    return q


def logical_constraint(u, basis, site):
    tensor = u.reshape((3,) * 4 + (2,))
    rows = []
    for a in basis:
        acted = np.tensordot(a, tensor, axes=(1, site))
        acted = np.moveaxis(acted, 0, site).reshape(81, 2)
        m = u.conj().T @ acted
        rows.append(
            [m[0, 0].real, m[1, 1].real,
             np.sqrt(2) * m[0, 1].real,
             np.sqrt(2) * m[0, 1].imag]
        )
    return np.asarray(rows).T


def hessian_matrix(p, basis, site):
    diagonal = np.array([n_value(p, a, site) for a in basis])
    matrix = np.diag(diagonal)
    for i in range(9):
        for j in range(i + 1, 9):
            nij = (
                n_value(p, basis[i] + basis[j], site)
                - diagonal[i] - diagonal[j]
            ) / 2
            matrix[i, j] = matrix[j, i] = nij
    return matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    basis = hermitian_basis()
    for sample in range(args.samples):
        u = random_isometry(rng)
        p = u @ u.conj().T
        q = endpoint_q(p)
        for site in range(4):
            nmat = hessian_matrix(p, basis, site)
            phi = logical_constraint(u, basis, site)
            kernel = scipy.linalg.null_space(phi)
            restricted = kernel.conj().T @ nmat @ kernel
            eig = np.linalg.eigvalsh(restricted)
            full = np.linalg.eigvalsh(nmat)
            print(
                sample,
                site,
                f"Q={q:.9g}",
                "K=" + ",".join(f"{x:.5g}" for x in eig),
                "full+=" + str(np.count_nonzero(full > 1e-8)),
            )


if __name__ == "__main__":
    main()
