"""Numerical discovery only: probe candidate cross inequalities.

This file is not a verifier and none of its floating-point output is evidence.
"""

import argparse
import numpy as np


def haar_isometry(rows: int, cols: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(rows, cols)) + 1j * rng.normal(size=(rows, cols))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1)
    return q * phases.conj()


def partial_swap_action(
    vector: np.ndarray, subset: int, d: int, n: int
) -> np.ndarray:
    tensor = vector.reshape((d,) * (2 * n))
    axes = list(range(2 * n))
    for i in range(n):
        if subset & (1 << i):
            axes[i], axes[n + i] = axes[n + i], axes[i]
    return np.transpose(tensor, axes).reshape(-1)


def y_action(vector: np.ndarray, d: int, n: int) -> np.ndarray:
    result = np.zeros_like(vector)
    for subset in range(1 << n):
        result += ((-0.5) ** bin(subset).count("1")) * partial_swap_action(
            vector, subset, d, n
        )
    return result


def probe(d: int, n: int, trials: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    dim = d**n
    min_h_det = np.inf
    min_cross_ratio = np.inf
    max_diag_ratio = 0.0
    min_strengthened_eig = np.inf
    min_strengthened_copos = np.inf
    worst = None
    for _ in range(trials):
        u = haar_isometry(dim, 2, rng)
        v = haar_isometry(dim, 2, rng)
        products = {
            (i, j): np.kron(u[:, i], v[:, j]) for i in range(2) for j in range(2)
        }
        yp = {key: y_action(value, d, n) for key, value in products.items()}
        h = np.empty((2, 2), dtype=np.complex128)
        for i in range(2):
            for j in range(2):
                h[i, j] = np.vdot(products[(i, j)], yp[(j, i)])
        h = (h + h.conj().T) / 2
        det = np.linalg.det(h).real
        target = (0.5 ** n) * np.array([[1.0, -1.0], [-1.0, 1.0]])
        min_strengthened_eig = min(
            min_strengthened_eig, np.linalg.eigvalsh(h - target)[0]
        )
        acoef = h[0, 0].real - 0.5 ** n
        bcoef = h[0, 1].real + 0.5 ** n
        ccoef = h[1, 1].real - 0.5 ** n
        if bcoef < 0 and acoef > 0:
            copos_gap = ccoef - bcoef * bcoef / acoef
        else:
            copos_gap = min(acoef, ccoef)
        min_strengthened_copos = min(min_strengthened_copos, copos_gap)
        max_diag_ratio = max(
            max_diag_ratio, abs(h[0, 1]) / max(min(h[0, 0].real, h[1, 1].real), 1e-300)
        )
        k = {(i, j): np.vdot(products[(i, j)], yp[(i, j)]).real
             for i in range(2) for j in range(2)}
        ratio_gap = k[(0, 0)] * k[(1, 1)] - k[(0, 1)] * k[(1, 0)]
        if det < min_h_det:
            min_h_det = det
            worst = (h.copy(), k.copy())
        min_cross_ratio = min(min_cross_ratio, ratio_gap)
    print(f"d={d} n={n} trials={trials}")
    print(f"min det(H)={min_h_det:.12g}")
    print(f"min matched-minus-mismatched K product={min_cross_ratio:.12g}")
    print(f"max |H12|/min(diagonal)={max_diag_ratio:.12g}")
    print(f"min eig(H-2^-n[[1,-1],[-1,1]])={min_strengthened_eig:.12g}")
    print(f"min positive-quadrant strengthened gap={min_strengthened_copos:.12g}")
    print("worst H=", worst[0])
    print("worst K=", worst[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=int, default=3)
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    probe(args.d, args.n, args.trials, args.seed)
