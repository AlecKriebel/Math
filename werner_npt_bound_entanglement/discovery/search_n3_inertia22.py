"""Discovery search for a negative three-copy Hermitian inertia-(2,2) form.

This is floating-point adversarial testing only.  It minimizes Q_3(H) on
H = U diag(lam) U^*, with U an N-by-4 complex Stiefel frame.  By default
lam=(1,1,-1,-1); the optional ``weights`` mode also updates the four
eigenvalue magnitudes on the unit sphere while preserving their signs.
"""

from __future__ import annotations

import sys

import numpy as np


LOCAL = 3
COPIES = 3
DIMENSION = LOCAL**COPIES
WORDS = np.array(
    [
        [(index // LOCAL ** (COPIES - 1 - site)) % LOCAL for site in range(COPIES)]
        for index in range(DIMENSION)
    ],
    dtype=int,
)


def maps(mask: int) -> tuple[np.ndarray, np.ndarray]:
    keep = [site for site in range(COPIES) if not (mask >> site) & 1]
    retained = np.zeros(DIMENSION, dtype=int)
    for site in keep:
        retained = LOCAL * retained + WORDS[:, site]
    compatible = np.ones((DIMENSION, DIMENSION), dtype=bool)
    for site in range(COPIES):
        if (mask >> site) & 1:
            compatible &= WORDS[:, site, None] == WORDS[None, :, site]
    return retained, compatible


MAPS = [maps(mask) for mask in range(1 << COPIES)]


def partial_trace(matrix: np.ndarray, mask: int) -> np.ndarray:
    retained, compatible = MAPS[mask]
    size = LOCAL ** (COPIES - bin(mask).count("1"))
    out = np.zeros((size, size), dtype=complex)
    rows, cols = np.nonzero(compatible)
    np.add.at(out, (retained[rows], retained[cols]), matrix[rows, cols])
    return out


def embed(matrix: np.ndarray, mask: int) -> np.ndarray:
    retained, compatible = MAPS[mask]
    return compatible * matrix[retained[:, None], retained[None, :]]


def phi(matrix: np.ndarray) -> np.ndarray:
    out = np.zeros_like(matrix)
    for mask in range(1 << COPIES):
        coefficient = (-0.5) ** bin(mask).count("1")
        out += coefficient * embed(partial_trace(matrix, mask), mask)
    return out


def value(frame: np.ndarray, eigenvalues: np.ndarray) -> tuple[float, np.ndarray]:
    matrix = (frame * eigenvalues) @ frame.conj().T
    image = phi(matrix)
    return float(np.vdot(matrix, image).real), image


def retract(frame: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(frame)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return q * phases.conj()


def optimize(
    seed: int, vary_weights: bool
) -> tuple[float, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    frame = retract(
        rng.normal(size=(DIMENSION, 4))
        + 1j * rng.normal(size=(DIMENSION, 4))
    )
    magnitudes = np.ones(4) / 2
    signs = np.array([1.0, 1.0, -1.0, -1.0])
    eigenvalues = signs * magnitudes
    best, _ = value(frame, eigenvalues)
    step = 0.08
    for iteration in range(5000):
        current, image = value(frame, eigenvalues)
        euclidean = 4 * image @ (frame * eigenvalues)
        overlap = frame.conj().T @ euclidean
        tangent = euclidean - frame @ ((overlap + overlap.conj().T) / 2)
        weight_gradient = np.array(
            [
                2 * np.vdot(frame[:, j], image @ frame[:, j]).real * signs[j]
                for j in range(4)
            ]
        )
        weight_tangent = weight_gradient - magnitudes * np.dot(
            magnitudes, weight_gradient
        )
        accepted = False
        local_step = step
        for _ in range(20):
            candidate_frame = retract(frame - local_step * tangent)
            candidate_magnitudes = magnitudes
            if vary_weights:
                candidate_magnitudes = magnitudes - local_step * weight_tangent
                candidate_magnitudes = np.maximum(candidate_magnitudes, 1e-6)
                candidate_magnitudes /= np.linalg.norm(candidate_magnitudes)
            candidate_eigenvalues = signs * candidate_magnitudes
            candidate, _ = value(candidate_frame, candidate_eigenvalues)
            if candidate < current - 1e-12 * local_step:
                frame = candidate_frame
                magnitudes = candidate_magnitudes
                eigenvalues = candidate_eigenvalues
                step = min(0.2, local_step * 1.05)
                best = min(best, candidate)
                accepted = True
                break
            local_step *= 0.5
        if not accepted:
            step *= 0.5
        if iteration % 250 == 0:
            print(seed, iteration, current, *eigenvalues, flush=True)
        if step < 1e-10:
            break
    return best, eigenvalues, frame


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    vary_weights = len(sys.argv) > 3 and sys.argv[3] == "weights"
    for seed in range(start, start + count):
        best, eigenvalues, frame = optimize(seed, vary_weights)
        print("RESULT", seed, best, *eigenvalues, flush=True)
        if best < -1e-8:
            np.savez(
                f"/tmp/n3_inertia22_seed{seed}.npz",
                frame=frame,
                eigenvalues=eigenvalues,
            )


if __name__ == "__main__":
    main()
