#!/usr/bin/env python3
"""Adversarial search for a full-rank balanced weight-three Gram.

Minimize

    lambda_max(D) + penalty/2 * sum_{T<bar(T)} (A_T-A_bar(T))^2

on the complex Stiefel manifold of 81-by-2 code frames.  On the balanced
slice, D=-(9/2)W_3, so a strictly negative lambda_max(D) would make W_3
positive definite and refute the proposed rank-two Gram lemma.

The eigenvalue gradient uses Hellmann--Feynman.  This is discovery code;
floating-point output is not a certificate.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np

sys.path.insert(0, "discovery")
from optimize_hodge_frames import load_frame  # noqa: E402


PAULI = (
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
)
SINGLES = (1, 2, 4, 8)
PAIRS = (3, 5, 6, 9, 10, 12)
BALANCE_REPRESENTATIVES = tuple(range(1, 8))


def trace_replace_site(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape((3,) * 8)
    other = [i for i in range(4) if i != site]
    permutation = [site, *other, 4 + site, *(4 + i for i in other)]
    moved = tensor.transpose(permutation).reshape(3, 27, 3, 27)
    reduced = np.trace(moved, axis1=0, axis2=2)
    replaced = np.einsum("ab,ij->aibj", np.eye(3), reduced)
    inverse = np.argsort(permutation)
    return replaced.reshape((3,) * 8).transpose(inverse).reshape(81, 81)


def trace_maps(matrix: np.ndarray) -> list[np.ndarray]:
    maps = [np.empty((0, 0), dtype=complex) for _ in range(16)]
    maps[0] = matrix
    for mask in range(1, 16):
        bit = mask & -mask
        site = bit.bit_length() - 1
        maps[mask] = trace_replace_site(maps[mask ^ bit], site)
    return maps


def tangent_projection(frame: np.ndarray, gradient: np.ndarray) -> np.ndarray:
    gram = frame.conj().T @ gradient
    hermitian = (gram + gram.conj().T) / 2
    return gradient - frame @ hermitian


def retract(frame: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(frame)
    phases = np.exp(-1j * np.angle(np.diag(r)))
    return q * phases[None, :]


def evaluate(
    frame: np.ndarray, penalty: float, need_gradient: bool
) -> tuple[float, float, np.ndarray, np.ndarray | None]:
    projection = frame @ frame.conj().T
    p_maps = trace_maps(projection)
    moment = np.array(
        [
            np.vdot(projection, p_maps[15 ^ subset]).real
            for subset in range(16)
        ]
    )
    defects = np.array(
        [
            moment[subset] - moment[15 ^ subset]
            for subset in BALANCE_REPRESENTATIVES
        ]
    )
    loss = 0.5 * float(defects @ defects)

    encoded = [frame @ pauli @ frame.conj().T for pauli in PAULI]
    encoded_maps = [trace_maps(operator) for operator in encoded]
    d_matrix = np.empty((3, 3))
    for a in range(3):
        for b in range(3):
            d_matrix[a, b] = (
                sum(
                    np.vdot(
                        encoded[a], encoded_maps[b][15 ^ subset]
                    ).real
                    for subset in PAIRS
                )
                - 2
                * sum(
                    np.vdot(
                        encoded[a], encoded_maps[b][15 ^ subset]
                    ).real
                    for subset in SINGLES
                )
            )
    d_matrix = (d_matrix + d_matrix.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(d_matrix)
    top = float(eigenvalues[-1])
    direction = eigenvectors[:, -1]
    objective = top + penalty * loss
    if not need_gradient:
        return objective, loss, eigenvalues, None

    # Balance-penalty gradient.
    coefficients = np.zeros(16)
    for defect, subset in zip(defects, BALANCE_REPRESENTATIVES):
        coefficients[subset] += penalty * defect
        coefficients[15 ^ subset] -= penalty * defect
    p_operator = sum(
        coefficients[subset] * p_maps[15 ^ subset]
        for subset in range(16)
    )
    gradient = 4 * p_operator @ frame

    # Hellmann--Feynman gradient of lambda_max(D).
    logical = sum(direction[a] * PAULI[a] for a in range(3))
    physical = frame @ logical @ frame.conj().T
    physical_maps = trace_maps(physical)
    d_operator = sum(
        physical_maps[15 ^ subset] for subset in PAIRS
    ) - 2 * sum(
        physical_maps[15 ^ subset] for subset in SINGLES
    )
    gradient += 4 * d_operator @ frame @ logical
    gradient = tangent_projection(frame, gradient)
    return objective, loss, eigenvalues, gradient


def balance_data(
    frame: np.ndarray,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """Four singleton/triple defects and their tangent gradients."""
    projection = frame @ frame.conj().T
    maps = trace_maps(projection)
    moment = np.array(
        [
            np.vdot(projection, maps[15 ^ subset]).real
            for subset in range(16)
        ]
    )
    representatives = (1, 2, 4, 7)
    defects = np.array(
        [moment[subset] - moment[15 ^ subset]
         for subset in representatives]
    )
    gradients: list[np.ndarray] = []
    for subset in representatives:
        operator = maps[15 ^ subset] - maps[subset]
        gradients.append(
            tangent_projection(frame, 4 * operator @ frame)
        )
    return defects, gradients


def real_inner(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.vdot(left, right).real)


def restore_balance(
    frame: np.ndarray, tolerance: float = 1e-13, iterations: int = 20
) -> np.ndarray:
    """Newton projection onto the four balance equations."""
    for _ in range(iterations):
        defects, gradients = balance_data(frame)
        if np.max(np.abs(defects)) <= tolerance:
            return frame
        gram = np.array(
            [[real_inner(left, right) for right in gradients]
             for left in gradients]
        )
        multipliers = np.linalg.lstsq(gram, defects, rcond=1e-12)[0]
        correction = sum(
            multipliers[i] * gradients[i] for i in range(4)
        )
        # Backtrack only to make the equality residual decrease.
        old_norm = float(defects @ defects)
        step = 1.0
        for _ in range(20):
            candidate = retract(frame - step * correction)
            new_defects, _ = balance_data(candidate)
            if float(new_defects @ new_defects) < old_norm:
                frame = candidate
                break
            step *= 0.5
        else:
            return frame
    return frame


def constrained_descent(
    frame: np.ndarray,
    iterations: int,
    initial_step: float,
) -> np.ndarray:
    """Descend lambda_max(D) while restoring balance after every step."""
    frame = restore_balance(frame)
    step = initial_step
    best = frame.copy()
    best_top = evaluate(frame, 0.0, False)[2][-1]
    for iteration in range(iterations):
        _, _, eigenvalues, objective_gradient = evaluate(
            frame, 0.0, True
        )
        assert objective_gradient is not None
        defects, constraint_gradients = balance_data(frame)
        gram = np.array(
            [
                [real_inner(left, right)
                 for right in constraint_gradients]
                for left in constraint_gradients
            ]
        )
        pairing = np.array(
            [real_inner(gradient, objective_gradient)
             for gradient in constraint_gradients]
        )
        multipliers = np.linalg.lstsq(
            gram, pairing, rcond=1e-12
        )[0]
        projected = objective_gradient - sum(
            multipliers[i] * constraint_gradients[i]
            for i in range(4)
        )
        gradient_squared = real_inner(projected, projected)
        top = float(eigenvalues[-1])
        if top < best_top:
            best_top = top
            best = frame.copy()
        if iteration % 10 == 0:
            print(
                f"constrained iter={iteration} "
                f"maxdef={np.max(np.abs(defects)):.3e} "
                f"D={eigenvalues} "
                f"projected_grad2={gradient_squared:.3e}"
            )
        if gradient_squared < 1e-22:
            break
        accepted = False
        trial_step = step
        for _ in range(25):
            candidate = retract(frame - trial_step * projected)
            candidate = restore_balance(candidate)
            new_defects, _ = balance_data(candidate)
            new_eigenvalues = evaluate(
                candidate, 0.0, False
            )[2]
            if (
                np.max(np.abs(new_defects)) < 2e-11
                and new_eigenvalues[-1]
                <= top - 1e-6 * trial_step * gradient_squared
            ):
                frame = candidate
                step = min(initial_step, 1.2 * trial_step)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
    return best


def descend(
    frame: np.ndarray,
    penalty: float,
    iterations: int,
    initial_step: float,
) -> np.ndarray:
    step = initial_step
    best = frame.copy()
    best_value = evaluate(frame, penalty, False)[0]
    for iteration in range(iterations):
        value, loss, eigenvalues, gradient = evaluate(
            frame, penalty, True
        )
        assert gradient is not None
        norm_squared = float(np.vdot(gradient, gradient).real)
        if value < best_value:
            best_value = value
            best = frame.copy()
        if iteration % 25 == 0:
            print(
                f"iter={iteration} objective={value:.12g} "
                f"loss={loss:.3e} D={eigenvalues}"
            )
        if norm_squared < 1e-22:
            break
        accepted = False
        trial_step = step
        for _ in range(30):
            candidate = retract(frame - trial_step * gradient)
            candidate_value = evaluate(candidate, penalty, False)[0]
            if candidate_value <= (
                value - 1e-5 * trial_step * norm_squared
            ):
                frame = candidate
                step = min(initial_step, 1.25 * trial_step)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frame")
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument(
        "--penalties",
        default="1e3,1e4,1e5,1e6,1e7",
        help="comma-separated balance penalties",
    )
    parser.add_argument("--step", type=float, default=0.01)
    parser.add_argument(
        "--constrained",
        action="store_true",
        help="use Newton restoration of the four balance equations",
    )
    args = parser.parse_args()
    u, v = load_frame(args.frame)
    frame = np.stack((u, v), axis=1)
    if args.constrained:
        frame = constrained_descent(
            frame, args.iterations, args.step
        )
        defects, _ = balance_data(frame)
        eigenvalues = evaluate(frame, 0.0, False)[2]
        print(
            f"constrained result maxdef={np.max(np.abs(defects)):.3e} "
            f"D={eigenvalues}"
        )
        return
    for penalty in map(float, args.penalties.split(",")):
        print(f"penalty={penalty:g}")
        frame = descend(
            frame, penalty, args.iterations, args.step
        )
        _, loss, eigenvalues, _ = evaluate(frame, penalty, False)
        print(f"result loss={loss:.3e} D={eigenvalues}")


if __name__ == "__main__":
    main()
