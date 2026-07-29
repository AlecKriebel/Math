#!/usr/bin/env python3
"""Adversarial frozen-H4 search constrained toward nonzero UU leakage.

This supplements d6_one_sided_fixed_h4_search.py by minimizing

    ||cubic residual||_F^2 + weight * (delta-target)^2,

where delta is the exact UU-to-mixed coupling norm squared.  It is a
candidate generator only.  A small penalized objective is not a proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm

import d6_one_sided_fixed_h4_search as base


def leakage_value_gradient(
    complement: np.ndarray, field: str
) -> tuple[float, np.ndarray]:
    h = base.assemble(complement)
    dimension = base.DIMENSION
    f_local = np.diag([0.0, 0.0, 0.0, 0.0, 1.0, 1.0])
    e_local = np.eye(dimension) - f_local
    square_u = np.kron(f_local, f_local)
    mixed = (
        np.kron(e_local, f_local) + np.kron(f_local, e_local)
    )
    delta = float(
        np.trace(h @ mixed @ h @ square_u).real / 4.0
    )
    ambient_gradient = (
        mixed @ h @ square_u + square_u @ h @ mixed
    ) / 4.0
    tangent = base.complement_tangent(
        ambient_gradient, complement, field
    )
    return delta, tangent


def value_gradient(
    complement: np.ndarray,
    field: str,
    target: float,
    weight: float,
    need_gradient: bool = True,
) -> tuple[float, np.ndarray, float, float, float] | float:
    if need_gradient:
        base_value, base_gradient, residual, _ = base.value_gradient(
            complement, field, 0.0
        )
        delta, delta_gradient = leakage_value_gradient(complement, field)
        gradient = (
            base_gradient
            + 2.0 * weight * (delta - target) * delta_gradient
        )
        value = base_value + weight * (delta - target) ** 2
        return (
            value,
            gradient,
            residual,
            float(np.linalg.norm(gradient)),
            delta,
        )
    base_value = base.value_gradient(
        complement, field, 0.0, need_gradient=False
    )
    delta, _ = leakage_value_gradient(complement, field)
    return base_value + weight * (delta - target) ** 2


def emit(event: dict[str, object], output: Path | None) -> None:
    line = json.dumps(event, sort_keys=True)
    print(line, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def initial(args: argparse.Namespace) -> np.ndarray:
    if args.initial == "leakage_model":
        result = base.leakage_limitation_complement()
        return result.real if args.field == "real" else result
    rng = np.random.default_rng(args.seed)
    return base.random_complement(rng, args.field)


def gradient_check(args: argparse.Namespace) -> int:
    complement = initial(args)
    rng = np.random.default_rng(args.seed + 1)
    ambient = rng.normal(size=(36, 36))
    if args.field == "complex":
        ambient = ambient + 1j * rng.normal(size=(36, 36))
    direction = base.complement_tangent(
        ambient, complement, args.field
    )
    direction /= np.linalg.norm(direction)
    value, gradient, _, _, delta = value_gradient(
        complement, args.field, args.target, args.weight
    )
    generator = (direction @ complement - complement @ direction) / 4.0
    analytic = float(np.vdot(gradient, direction).real)
    checks = []
    for epsilon in (1e-4, 1e-5, 1e-6):
        plus_unitary = expm(epsilon * generator)
        minus_unitary = expm(-epsilon * generator)
        plus = plus_unitary @ complement @ plus_unitary.conj().T
        minus = minus_unitary @ complement @ minus_unitary.conj().T
        quotient = (
            value_gradient(
                plus,
                args.field,
                args.target,
                args.weight,
                need_gradient=False,
            )
            - value_gradient(
                minus,
                args.field,
                args.target,
                args.weight,
                need_gradient=False,
            )
        ) / (2.0 * epsilon)
        checks.append(
            {
                "epsilon": epsilon,
                "analytic": analytic,
                "central_difference": quotient,
                "absolute_error": abs(quotient - analytic),
            }
        )
    print(
        json.dumps(
            {
                "script_sha256": source_sha256(),
                "base_script_sha256": base.source_sha256(),
                "seed": args.seed,
                "initial_delta": delta,
                "target": args.target,
                "weight": args.weight,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run(args: argparse.Namespace) -> int:
    complement = initial(args)
    output = Path(args.output).resolve() if args.output else None
    run_id = (
        f"d6_fixed_h4_leakage_target_{args.field}_{args.initial}"
        f"_seed{args.seed}_target{args.target:g}_weight{args.weight:g}"
    )
    emit(
        {
            "event": "start",
            "run_id": run_id,
            "unix_time": time.time(),
            "seed": args.seed,
            "field": args.field,
            "initial": args.initial,
            "target": args.target,
            "weight": args.weight,
            "max_iterations": args.max_iterations,
            "script_sha256": source_sha256(),
            "base_script_sha256": base.source_sha256(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
        },
        output,
    )

    step = 0.02
    previous_gradient: np.ndarray | None = None
    previous_direction: np.ndarray | None = None
    start = time.monotonic()
    for iteration in range(args.max_iterations + 1):
        value, gradient, residual, gradient_norm, delta = value_gradient(
            complement, args.field, args.target, args.weight
        )
        if iteration in (0, args.max_iterations):
            emit(
                {
                    "event": "progress",
                    "run_id": run_id,
                    "iteration": iteration,
                    "elapsed_seconds": time.monotonic() - start,
                    "objective": value,
                    "residual_frobenius": residual,
                    "gradient_frobenius": gradient_norm,
                    "delta": delta,
                },
                output,
            )
        if iteration == args.max_iterations or gradient_norm < 1e-9:
            break
        if previous_gradient is None:
            direction = -gradient
        else:
            transported_gradient = (
                previous_gradient
                - complement @ previous_gradient @ complement
            ) / 2.0
            transported_direction = (
                previous_direction
                - complement @ previous_direction @ complement
            ) / 2.0
            denominator = max(
                float(np.vdot(previous_gradient, previous_gradient).real),
                np.finfo(float).tiny,
            )
            beta = max(
                0.0,
                float(
                    np.vdot(
                        gradient, gradient - transported_gradient
                    ).real
                )
                / denominator,
            )
            direction = -gradient + beta * transported_direction
            if np.vdot(gradient, direction).real >= 0:
                direction = -gradient

        derivative = float(np.vdot(gradient, direction).real)
        generator = (
            direction @ complement - complement @ direction
        ) / 4.0
        trial_step = min(step, 0.5)
        accepted = False
        for line_search_iteration in range(40):
            unitary = expm(trial_step * generator)
            trial = unitary @ complement @ unitary.conj().T
            trial_value = value_gradient(
                trial,
                args.field,
                args.target,
                args.weight,
                need_gradient=False,
            )
            if trial_value <= value + 1e-4 * trial_step * derivative:
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
        previous_gradient = gradient
        previous_direction = direction
        complement = trial
        step = min(1.8 * trial_step, 0.5) if line_search_iteration == 0 else trial_step

    final_base = base.diagnostics(complement, args.field, 0.0)
    final_delta, _ = leakage_value_gradient(complement, args.field)
    emit(
        {
            "event": "final",
            "run_id": run_id,
            "iteration": iteration,
            "elapsed_seconds": time.monotonic() - start,
            "target": args.target,
            "weight": args.weight,
            "penalized_objective": value_gradient(
                complement,
                args.field,
                args.target,
                args.weight,
                need_gradient=False,
            ),
            "target_error": final_delta - args.target,
            **final_base,
        },
        output,
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--seed", required=True, type=int)
    result.add_argument("--field", choices=("real", "complex"), default="complex")
    result.add_argument(
        "--initial", choices=("random", "leakage_model"), default="random"
    )
    result.add_argument("--target", type=float, default=0.25)
    result.add_argument("--weight", type=float, default=1000.0)
    result.add_argument("--max-iterations", type=int, default=800)
    result.add_argument("--output")
    result.add_argument("--gradient-check", action="store_true")
    return result


if __name__ == "__main__":
    arguments = parser().parse_args()
    if arguments.gradient_check:
        raise SystemExit(gradient_check(arguments))
    raise SystemExit(run(arguments))
