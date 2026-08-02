#!/usr/bin/env python3
"""Strong-pair dB separated generator and a Bd one-excursion diagnostic.

There is one center and ``q`` pair blades.  Blade j has equal center edge
weight ``a_j`` and internal edge weight ``b_j``.  In the limit
``lambda_j=a_j/b_j -> 0`` each blade is monomorphic between rare events.
For dB this script solves the leading separated ``2^(q+1)``-state generator.
It is not literally the trace on center/monomorphic-blade states because a
center death can overlap pair resolution; the subsequent fast-center
reduction is nevertheless exact.  The Bd rates are an isolated-excursion
surrogate: center births can overlap pair resolution at order one, so Bd
output is reconnaissance, not a proved trace.  Floating optimization is
discovery only.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def macro_fixation(
    outer_probability: np.ndarray,
    pair_ratio: np.ndarray,
    fitness: float,
    rule: str,
):
    """Return values of the separated dB generator or Bd surrogate."""

    p = np.asarray(outer_probability, dtype=float)
    lam = np.asarray(pair_ratio, dtype=float)
    blades = len(p)
    assert len(lam) == blades and np.all(p > 0) and np.all(lam > 0)
    p = p / p.sum()
    full_mask = (1 << blades) - 1
    extinction = 0  # encoded state = (mask << 1) | center
    fixation = (full_mask << 1) | 1
    states = [state for state in range(fixation + 1) if state not in (extinction, fixation)]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))

    for state, row in index.items():
        center = state & 1
        mask = state >> 1
        mutant = np.array([(mask >> j) & 1 for j in range(blades)], dtype=float)
        p_mutant = float(p @ mutant)
        p_resident = 1.0 - p_mutant
        lam_mutant = float(lam @ mutant)
        lam_resident = float(lam.sum() - lam_mutant)
        changes: list[tuple[int, float]] = []

        if rule == "dB":
            neighbor_denominator = fitness * p_mutant + p_resident
            if not center and p_mutant:
                changes.append((state | 1, fitness * p_mutant / neighbor_denominator))
            if center and p_resident:
                changes.append((state & ~1, p_resident / neighbor_denominator))
            for blade in range(blades):
                bit = 1 << blade
                if center and not (mask & bit):
                    changes.append((((mask | bit) << 1) | 1, fitness * lam[blade]))
                elif not center and (mask & bit):
                    changes.append(((mask & ~bit) << 1, lam[blade] / fitness))
        elif rule == "Bd":
            if not center and lam_mutant:
                changes.append((state | 1, 2.0 * fitness * lam_mutant))
            if center and lam_resident:
                changes.append((state & ~1, 2.0 * lam_resident))
            for blade in range(blades):
                bit = 1 << blade
                if center and not (mask & bit):
                    changes.append(
                        (((mask | bit) << 1) | 1, p[blade] * fitness**2 / (fitness + 1.0))
                    )
                elif not center and (mask & bit):
                    changes.append(((mask & ~bit) << 1, p[blade] / (fitness + 1.0)))
        else:
            raise ValueError(rule)

        total = sum(rate for _, rate in changes)
        if not total > 0:
            raise ArithmeticError((state, center, mask, rule))
        rows.append(row)
        columns.append(row)
        entries.append(total)
        for target, rate in changes:
            if target == fixation:
                rhs[row] += rate
            elif target != extinction:
                rows.append(row)
                columns.append(index[target])
                entries.append(-rate)

    matrix = sp.csr_matrix(
        (entries, (rows, columns)), shape=(len(states), len(states))
    )
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    if residual > 2e-7 or np.min(values) < -2e-7 or np.max(values) > 1 + 2e-7:
        raise FloatingPointError((residual, float(np.min(values)), float(np.max(values))))
    center_value = float(values[index[1]])
    blade_values = np.array(
        [float(values[index[(1 << blade) << 1]]) for blade in range(blades)]
    )
    return center_value, blade_values, residual


def population_fixation(p: np.ndarray, lam: np.ndarray, fitness: float):
    blades = len(p)
    order = 2 * blades + 1
    answer = {}
    for rule in ("Bd", "dB"):
        center, blade, residual = macro_fixation(p, lam, fitness, rule)
        local = fitness / (fitness + 1.0) if rule == "Bd" else 0.5
        rho = (center + 2.0 * local * float(blade.sum())) / order
        answer[rule] = (rho, center, blade, residual)
    return answer


def decode(blades: int, vector: np.ndarray, lambda_cap: float):
    outer_logs = np.asarray(vector[:blades], dtype=float)
    outer = np.exp(outer_logs - np.max(outer_logs))
    outer /= outer.sum()
    ratio_logs = np.asarray(vector[blades:], dtype=float)
    ratio = lambda_cap * np.exp(ratio_logs - np.max(ratio_logs))
    return outer, ratio


def evaluate(
    blades: int,
    fitness: float,
    lambda_cap: float,
    vector: np.ndarray,
    mode: str = "simultaneous",
):
    outer, ratio = decode(blades, vector, lambda_cap)
    values = population_fixation(outer, ratio, fitness)
    baseline = 1.0 - 1.0 / fitness
    if mode == "simultaneous":
        score = min(values["Bd"][0] - baseline, values["dB"][0] - baseline)
    elif mode == "db":
        score = values["dB"][0] - baseline
    elif mode == "bd":
        score = values["Bd"][0] - baseline
    else:
        raise ValueError(mode)
    return score, values, outer, ratio


def local_search(
    vector: np.ndarray,
    blades: int,
    fitness: float,
    lambda_cap: float,
    mode: str,
    rng: np.random.Generator,
    steps: int,
    span: float,
):
    current = vector.copy()
    current_score = evaluate(blades, fitness, lambda_cap, current, mode)[0]
    best = (current_score, current.copy())
    for step in range(steps):
        fraction = step / max(1, steps - 1)
        scale = 1.1 * (0.035 / 1.1) ** fraction
        proposal = current.copy()
        count = 1 if rng.random() < 0.8 else int(rng.integers(2, min(5, len(current)) + 1))
        positions = rng.choice(len(current), count, replace=False)
        proposal[positions] += rng.normal(0.0, scale, count)
        proposal = np.clip(proposal, -span, 0.0)
        score = evaluate(blades, fitness, lambda_cap, proposal, mode)[0]
        temperature = 0.02 * (0.0003 / 0.02) ** fraction
        if score >= current_score or rng.random() < math.exp((score - current_score) / temperature):
            current, current_score = proposal, score
        if score > best[0]:
            best = (score, proposal.copy())
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blades", type=int, default=5)
    parser.add_argument("--fitness", type=float, default=1.51)
    parser.add_argument("--lambda-cap", type=float, default=1e-3)
    parser.add_argument("--mode", choices=("simultaneous", "db", "bd"), default="simultaneous")
    parser.add_argument("--span", type=float, default=18.0)
    parser.add_argument("--random", type=int, default=2000)
    parser.add_argument("--elite", type=int, default=6)
    parser.add_argument("--steps", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    elite: list[tuple[float, np.ndarray]] = []
    for sample in range(args.random):
        if rng.random() < 0.5:
            vector = rng.uniform(-args.span, 0.0, 2 * args.blades)
        else:
            outer = np.sort(rng.uniform(-args.span, 0.0, args.blades))
            ratio = np.sort(rng.uniform(-args.span, 0.0, args.blades))
            if rng.random() < 0.5:
                ratio = ratio[::-1]
            vector = np.r_[outer, ratio]
        try:
            score = evaluate(
                args.blades, args.fitness, args.lambda_cap, vector, args.mode
            )[0]
        except (ArithmeticError, FloatingPointError, RuntimeError):
            continue
        if len(elite) < args.elite or score > elite[-1][0]:
            elite.append((score, vector.copy()))
            elite.sort(key=lambda item: item[0], reverse=True)
            elite = elite[: args.elite]
        if (sample + 1) % 250 == 0:
            print(f"random={sample+1} best={elite[0][0]:+.10g}", flush=True)
    best = elite[0]
    for rank, (_, vector) in enumerate(elite):
        candidate = local_search(
            vector,
            args.blades,
            args.fitness,
            args.lambda_cap,
            args.mode,
            rng,
            args.steps,
            args.span,
        )
        if candidate[0] > best[0]:
            best = candidate
        print(f"local={rank+1}/{len(elite)} best={best[0]:+.10g}", flush=True)
    score, values, outer, ratio = evaluate(
        args.blades, args.fitness, args.lambda_cap, best[1], args.mode
    )
    print(
        f"RESULT q={args.blades} r={args.fitness:.12g} "
        f"lambda_cap={args.lambda_cap:.4g} mode={args.mode} score={score:+.12g}"
    )
    for rule in ("Bd", "dB"):
        rho, center, blade, residual = values[rule]
        print(
            f"{rule} rho={rho:.12g} center={center:.12g} residual={residual:.3g} "
            + "blade=" + " ".join(f"{x:.9g}" for x in blade)
        )
    print("outer", " ".join(f"{x:.12g}" for x in outer))
    print("lambda", " ".join(f"{x:.12g}" for x in ratio))


if __name__ == "__main__":
    main()
