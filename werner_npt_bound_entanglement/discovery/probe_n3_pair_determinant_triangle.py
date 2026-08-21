#!/usr/bin/env python3
"""Discovery-only probes for the residual 3x3 pair-sector determinant."""

import argparse

import numpy as np


def traceless_basis():
    out = []
    for i in range(3):
        for j in range(3):
            x = np.zeros((3, 3), dtype=complex)
            x[i, j] = 1
            x -= np.trace(x) * np.eye(3) / 3
            for y in out:
                x -= np.vdot(y, x) * y
            norm = np.linalg.norm(x)
            if norm > 1e-10:
                out.append(x / norm)
    assert len(out) == 8
    return out


def component_bases():
    tb = traceless_basis()
    ident = np.eye(3)
    pair = [np.kron(a, b) for a in tb for b in tb]
    global_bases = [[], [], []]
    for a in tb:
        for b in tb:
            global_bases[0].append(np.kron(ident, np.kron(a, b)))
            global_bases[1].append(np.kron(a, np.kron(ident, b)))
            global_bases[2].append(np.kron(a, np.kron(b, ident)))
    return np.asarray(pair), [np.asarray(x) for x in global_bases]


def random_isometry(rng):
    x = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    q, _ = np.linalg.qr(x)
    return q[:, :2]


def random_components(rng, global_bases):
    ds = []
    norms = []
    for basis in global_bases:
        z = rng.normal(size=64) + 1j * rng.normal(size=64)
        z /= np.linalg.norm(z)
        ds.append(np.einsum("a,aij->ij", z, basis))
        norms.append(float(np.vdot(z, z).real))
    return ds, norms


def deficit_matrix(v, ds, norms):
    xs = [d @ v for d in ds]
    h = np.array([[np.vdot(x, y) for y in xs] for x in xs])
    return 2 * np.diag(norms) - h, h


def optimized_components(v, global_bases):
    maps = []
    for basis in global_bases:
        maps.append(np.stack([(d @ v).reshape(-1) for d in basis], axis=1))
    total = np.concatenate(maps, axis=1)
    left_values, left_vectors = np.linalg.eigh(total @ total.conj().T)
    sigma = np.sqrt(max(0.0, left_values[-1]))
    coeff = total.conj().T @ left_vectors[:, -1] / sigma
    ds = []
    norms = []
    for i, basis in enumerate(global_bases):
        z = coeff[64 * i : 64 * (i + 1)]
        ds.append(np.einsum("a,aij->ij", z, basis))
        norms.append(float(np.vdot(z, z).real))
    return sigma * sigma, ds, norms


def frustrated_value(v, global_bases, phase):
    maps = [
        np.stack([(d @ v).reshape(-1) for d in basis], axis=1)
        for basis in global_bases
    ]
    block = np.zeros((192, 192), dtype=complex)
    factors = {
        (0, 1): 1.0,
        (1, 2): 1.0,
        (0, 2): np.exp(1j * phase),
    }
    for i in range(3):
        block[64 * i : 64 * (i + 1), 64 * i : 64 * (i + 1)] = (
            maps[i].conj().T @ maps[i]
        )
        for j in range(i + 1, 3):
            value = factors[(i, j)] * (maps[i].conj().T @ maps[j])
            block[64 * i : 64 * (i + 1), 64 * j : 64 * (j + 1)] = value
            block[64 * j : 64 * (j + 1), 64 * i : 64 * (i + 1)] = (
                value.conj().T
            )
    return float(np.linalg.eigvalsh(block)[-1])


def alternate_frustrated(v, global_bases, phase, iterations=100):
    factors = {
        (0, 1): 1.0,
        (1, 2): 1.0,
        (0, 2): np.exp(1j * phase),
    }
    value = -float("inf")
    coefficients = None
    for _ in range(iterations):
        maps = [
            np.stack([(d @ v).reshape(-1) for d in basis], axis=1)
            for basis in global_bases
        ]
        block = np.zeros((192, 192), dtype=complex)
        for i in range(3):
            block[64 * i : 64 * (i + 1), 64 * i : 64 * (i + 1)] = (
                maps[i].conj().T @ maps[i]
            )
            for j in range(i + 1, 3):
                entry = factors[(i, j)] * (maps[i].conj().T @ maps[j])
                block[64 * i : 64 * (i + 1), 64 * j : 64 * (j + 1)] = entry
                block[64 * j : 64 * (j + 1), 64 * i : 64 * (i + 1)] = (
                    entry.conj().T
                )
        values, vectors = np.linalg.eigh(block)
        value = float(values[-1])
        coefficients = vectors[:, -1]
        ds = []
        for i, basis in enumerate(global_bases):
            z = coefficients[64 * i : 64 * (i + 1)]
            ds.append(np.einsum("a,aij->ij", z, basis))
        physical = sum(d.conj().T @ d for d in ds)
        for i in range(3):
            for j in range(i + 1, 3):
                entry = factors[(i, j)] * (ds[i].conj().T @ ds[j])
                physical += entry + entry.conj().T
        _, vectors = np.linalg.eigh(physical)
        v = vectors[:, -2:]
    return value, v, coefficients


def inverse_square_root(matrix, tolerance=1e-10):
    values, vectors = np.linalg.eigh(matrix)
    weights = np.zeros_like(values)
    weights[values > tolerance] = 1 / np.sqrt(values[values > tolerance])
    return (vectors * weights) @ vectors.conj().T


def maximum_row_l1(v, global_bases, rng, starts=16, iterations=100):
    maps = [
        np.stack([(d @ v).reshape(-1) for d in basis], axis=1)
        for basis in global_bases
    ]
    defects = [2 * np.eye(64) - e.conj().T @ e for e in maps]
    roots = [inverse_square_root(a) for a in defects]
    contractions = {}
    for i in range(3):
        for j in range(3):
            if i != j:
                contractions[i, j] = (
                    roots[i] @ (maps[i].conj().T @ maps[j]) @ roots[j]
                )
    best = (-float("inf"), None)
    for i in range(3):
        js = [j for j in range(3) if j != i]
        positive = [
            contractions[i, j] @ contractions[i, j].conj().T for j in js
        ]
        seeds = []
        _, vectors = np.linalg.eigh(positive[0] + positive[1])
        seeds.append(vectors[:, -1])
        seeds += [
            rng.normal(size=64) + 1j * rng.normal(size=64)
            for _ in range(starts - 1)
        ]
        for x in seeds:
            x /= np.linalg.norm(x)
            for _ in range(iterations):
                p = max(1e-30, float(np.vdot(x, positive[0] @ x).real))
                q = max(1e-30, float(np.vdot(x, positive[1] @ x).real))
                y = positive[0] @ x / np.sqrt(p) + positive[1] @ x / np.sqrt(q)
                x = y / np.linalg.norm(y)
            p = max(0.0, float(np.vdot(x, positive[0] @ x).real))
            q = max(0.0, float(np.vdot(x, positive[1] @ x).real))
            value = np.sqrt(p) + np.sqrt(q)
            if value > best[0]:
                ys = []
                for k in contractions[i, js[0]], contractions[i, js[1]]:
                    y = k.conj().T @ x
                    ys.append(y / np.linalg.norm(y))
                coefficients = [None, None, None]
                coefficients[i] = roots[i] @ x
                coefficients[js[0]] = roots[js[0]] @ ys[0]
                coefficients[js[1]] = roots[js[1]] @ ys[1]
                best = (value, (i, coefficients))
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--optimized", action="store_true")
    parser.add_argument("--frustrated", action="store_true")
    parser.add_argument("--row-probe", action="store_true")
    parser.add_argument("--alternate-frustrated", action="store_true")
    args = parser.parse_args()

    _, global_bases = component_bases()
    rng = np.random.default_rng(args.seed)
    minimum = (float("inf"), None)
    minimum_absolute = (float("inf"), None)
    maximum_cycle = (-float("inf"), None)
    maximum_row_sum = (-float("inf"), None)
    maximum_abs_determinant_demand = (-float("inf"), None)
    maximum_frustrated = (-float("inf"), None)
    maximum_l1 = (-float("inf"), None)
    maximum_alternating = (-float("inf"), None)
    for _ in range(args.trials):
        if args.row_probe and _ % 2:
            v = np.zeros((27, 2), dtype=complex)
            v[0, 0] = 1
            v[4 * 3, 1] = 1  # |110>
            epsilon = 10 ** rng.uniform(-5, 0)
            v += epsilon * (
                rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
            )
            v, _ = np.linalg.qr(v)
        else:
            v = random_isometry(rng)
        if args.alternate_frustrated:
            phase = 2 * np.pi * (_ % 24) / 24
            value, final_v, coefficients = alternate_frustrated(
                v, global_bases, phase
            )
            if value > maximum_alternating[0]:
                maximum_alternating = (
                    value,
                    (final_v, coefficients, phase),
                )
            continue
        if args.row_probe:
            value, details = maximum_row_l1(v, global_bases, rng)
            if value > maximum_l1[0]:
                maximum_l1 = (value, (v, details))
            continue
        if args.frustrated:
            for phase in np.linspace(0, 2 * np.pi, 17, endpoint=False):
                value = frustrated_value(v, global_bases, phase)
                if value > maximum_frustrated[0]:
                    maximum_frustrated = (value, (v, phase))
            continue
        if args.optimized:
            top, ds, norms = optimized_components(v, global_bases)
        else:
            top = None
            ds, norms = random_components(rng, global_bases)
        m, h = deficit_matrix(v, ds, norms)
        evals = np.linalg.eigvalsh(m)
        if evals[0] < minimum[0]:
            minimum = (float(evals[0]), (m, h))
        m_abs = np.diag(np.diag(m).real) - (
            np.abs(h) - np.diag(np.diag(np.abs(h)))
        )
        evals_abs = np.linalg.eigvalsh(m_abs)
        if evals_abs[0] < minimum_absolute[0]:
            minimum_absolute = (float(evals_abs[0]), (m, h))
        cycle = np.real(h[0, 1] * h[1, 2] * np.conj(h[0, 2]))
        if cycle > maximum_cycle[0]:
            maximum_cycle = (float(cycle), (m, h))
        diagonal = np.diag(m).real
        if np.min(diagonal) > 1e-12:
            r01 = abs(h[0, 1]) / np.sqrt(diagonal[0] * diagonal[1])
            r02 = abs(h[0, 2]) / np.sqrt(diagonal[0] * diagonal[2])
            r12 = abs(h[1, 2]) / np.sqrt(diagonal[1] * diagonal[2])
            row_sum = max(r01 + r02, r01 + r12, r02 + r12)
            demand = r01**2 + r02**2 + r12**2 + 2 * r01 * r02 * r12
            maximum_row_sum = max(maximum_row_sum, (row_sum, (m, h)), key=lambda x: x[0])
            maximum_abs_determinant_demand = max(
                maximum_abs_determinant_demand,
                (demand, (m, h)),
                key=lambda x: x[0],
            )

    if args.frustrated:
        print("maximum frustrated block value", maximum_frustrated[0])
        print("phase", maximum_frustrated[1][1])
        return
    if args.row_probe:
        print("maximum normalized row l1", maximum_l1[0])
        np.savez(
            "n3_pair_row_l1_best.npz",
            v=maximum_l1[1][0],
            central=maximum_l1[1][1][0],
            coefficients=np.stack(maximum_l1[1][1][1]),
        )
        return
    if args.alternate_frustrated:
        print("maximum alternating frustrated value", maximum_alternating[0])
        print("phase", maximum_alternating[1][2])
        np.savez(
            "n3_pair_frustrated_best.npz",
            v=maximum_alternating[1][0],
            coefficients=maximum_alternating[1][1],
            phase=maximum_alternating[1][2],
        )
        return
    print("minimum M eigenvalue", minimum[0])
    print("minimum absolute-comparison eigenvalue", minimum_absolute[0])
    print("maximum positive cycle", maximum_cycle[0])
    print("maximum normalized row sum", maximum_row_sum[0])
    print("maximum absolute determinant demand", maximum_abs_determinant_demand[0])
    if args.optimized:
        print("last optimized frame value", top)
    print("M at minimum absolute comparison")
    print(minimum_absolute[1][0])
    print("H at minimum absolute comparison")
    print(minimum_absolute[1][1])


if __name__ == "__main__":
    main()
