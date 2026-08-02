#!/usr/bin/env python3
"""Fast search of finite weighted modules of orders 6--8.

Two successive rare-edge architectures are scored.

``center`` is the separated module / large-center trace used in the proved
triangle construction.  For a fixed module the attachment functional is
optimized globally.  After normalizing the attachment vector to have sum one,
its only nonlinear factor is

    (a.h) / ((b.h) (c.h)).

At a maximizer fix the value of ``b.h``.  The remaining problem is a linear-
fractional optimization over a simplex slice, hence has an optimum at a point
supported on at most two vertices.  We enumerate those supports and solve the
resulting one-variable rational problem exactly up to floating arithmetic.

``repeated`` is a weak complete coupling of identical modules.  For a proposed
common fixation value T, feasibility of both update rules is the intersection
of the convex hull of n two-dimensional vertex vectors with the nonnegative
quadrant.  Thus a feasible attachment again exists on at most two vertices.
We biselect the globally optimal T and retain a witnessing support.

The outer randomized/local search is numerical reconnaissance.  A positive
candidate must subsequently be rationalized, certified symbolically, and
given a uniform timescale-separation / post-establishment proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scan_satellite_module import module_data  # noqa: E402


@dataclass(frozen=True)
class PairWitness:
    i: int
    j: int
    t: float

    def vector(self, size: int) -> np.ndarray:
        result = np.zeros(size)
        result[self.i] += self.t
        result[self.j] += 1.0 - self.t
        return result


def weights_from_logs(size: int, logs: np.ndarray) -> np.ndarray:
    logs = np.asarray(logs, dtype=float)
    logs = logs - np.max(logs)
    weights = np.zeros((size, size))
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            weights[i, j] = weights[j, i] = math.exp(float(logs[cursor]))
            cursor += 1
    return weights


def _linear_value(x0: float, x1: float, t: float) -> float:
    return x1 + t * (x0 - x1)


def best_product_ratio(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    """Maximize ``(a.h)/((b.h)(c.h))`` over the probability simplex.

    A global optimizer has support at most two.  On a pair its stationary
    equation is a polynomial of degree at most two; endpoints are included.
    """

    size = len(a)
    best = (-math.inf, PairWitness(0, 0, 1.0))
    for i in range(size):
        for j in range(i, size):
            # Polynomial coefficients in increasing order for
            # A' B C - A (B' C + B C').
            A = np.array((a[j], a[i] - a[j]))
            B = np.array((b[j], b[i] - b[j]))
            C = np.array((c[j], c[i] - c[j]))
            Ap = A[1]
            Bp = B[1]
            Cp = C[1]
            numerator = (
                Ap * np.polynomial.polynomial.polymul(B, C)
                - np.polynomial.polynomial.polymul(
                    A, Bp * C + Cp * B
                )
            )
            candidates = [0.0, 1.0]
            # Trim roundoff-only leading coefficients before root finding.
            scale = max(1.0, float(np.max(np.abs(numerator))))
            while len(numerator) > 1 and abs(numerator[-1]) <= 1e-13 * scale:
                numerator = numerator[:-1]
            if len(numerator) > 1:
                for root in np.polynomial.polynomial.polyroots(numerator):
                    if abs(root.imag) <= 2e-10 and 0.0 < root.real < 1.0:
                        candidates.append(float(root.real))
            for t in candidates:
                av = _linear_value(a[i], a[j], t)
                bv = _linear_value(b[i], b[j], t)
                cv = _linear_value(c[i], c[j], t)
                value = av / (bv * cv)
                if value > best[0]:
                    best = (value, PairWitness(i, j, t))
    return best


def center_score(weights: np.ndarray, fitness: float):
    """Return exact separated-center log window and a two-vertex witness."""

    data = module_data(weights, fitness)
    degree = weights.sum(axis=1)
    f_bd, beta_bd = data["Bd"]
    f_db, beta_db = data["dB"]
    alpha_bd = float(f_bd.mean())
    alpha_db = float(f_db.mean())
    q = 1.0 - 1.0 / fitness
    if alpha_bd <= q or alpha_db <= q:
        # Alpha feasibility is a necessary condition independent of attachment.
        return min(alpha_bd - q, alpha_db - q), -math.inf, None, data
    a = 1.0 / degree
    b = beta_bd
    c = beta_db / degree
    product_ratio, witness = best_product_ratio(a, b, c)
    constant = (
        fitness
        * (fitness - 1.0) ** 2
        * (alpha_bd - q)
        * (alpha_db - q)
        / (q * q)
    )
    log_window = math.log(constant * product_ratio)
    # The raw objective uses comparable dimensionless margins.
    score = min((alpha_bd - q) / q, (alpha_db - q) / q, log_window)
    return score, log_window, witness, data


def _segment_hits_quadrant(p: np.ndarray, q: np.ndarray):
    """Return t with t*p+(1-t)*q >= 0 coordinatewise, if one exists."""

    lower, upper = 0.0, 1.0
    for coordinate in range(2):
        slope = p[coordinate] - q[coordinate]
        intercept = q[coordinate]
        if abs(slope) <= 1e-15:
            if intercept < 0.0:
                return None
        elif slope > 0.0:
            lower = max(lower, -intercept / slope)
        else:
            upper = min(upper, -intercept / slope)
    if lower <= upper + 2e-14 and upper >= 0.0 and lower <= 1.0:
        return min(1.0, max(0.0, 0.5 * (max(0.0, lower) + min(1.0, upper))))
    return None


def repeated_feasible(
    target: float,
    fitness: float,
    degree: np.ndarray,
    f_bd: np.ndarray,
    beta_bd: np.ndarray,
    f_db: np.ndarray,
    beta_db: np.ndarray,
):
    alpha_bd = float(f_bd.mean())
    alpha_db = float(f_db.mean())
    if target >= min(alpha_bd, alpha_db):
        return None
    q_bd = alpha_bd / (alpha_bd - target)
    q_db = alpha_db / (alpha_db - target)
    points = np.column_stack(
        (
            fitness * f_bd - q_bd * beta_bd,
            (fitness * fitness * f_db - q_db * beta_db) / degree,
        )
    )
    size = len(points)
    for i in range(size):
        for j in range(i, size):
            t = _segment_hits_quadrant(points[i], points[j])
            if t is not None:
                return PairWitness(i, j, t)
    return None


def repeated_score(weights: np.ndarray, fitness: float):
    """Globally optimize the common repeated-module fixation limit."""

    data = module_data(weights, fitness)
    degree = weights.sum(axis=1)
    f_bd, beta_bd = data["Bd"]
    f_db, beta_db = data["dB"]
    alpha_bd = float(f_bd.mean())
    alpha_db = float(f_db.mean())
    low, high = 0.0, min(alpha_bd, alpha_db) * (1.0 - 1e-13)
    witness = repeated_feasible(
        low, fitness, degree, f_bd, beta_bd, f_db, beta_db
    )
    for _ in range(58):
        middle = 0.5 * (low + high)
        candidate = repeated_feasible(
            middle, fitness, degree, f_bd, beta_bd, f_db, beta_db
        )
        if candidate is None:
            high = middle
        else:
            low = middle
            witness = candidate
    baseline = 1.0 - 1.0 / fitness
    return low - baseline, low, witness, data


def objective(weights: np.ndarray, fitness: float, architecture: str) -> float:
    if architecture == "center":
        return center_score(weights, fitness)[0]
    if architecture == "repeated":
        return repeated_score(weights, fitness)[0]
    raise ValueError(architecture)


def random_logs(rng: np.random.Generator, edge_count: int, span: float) -> np.ndarray:
    # Half the starts are continuous, half have a small number of separated
    # weight scales.  The latter efficiently explores singular modules.
    if rng.random() < 0.5:
        return rng.uniform(-span, 0.0, edge_count)
    levels = rng.integers(2, 6)
    raw = rng.integers(0, levels, edge_count)
    return -span * raw / max(1, levels - 1) + rng.normal(0.0, 0.06, edge_count)


def local_search(
    logs: np.ndarray,
    size: int,
    fitness: float,
    architecture: str,
    rng: np.random.Generator,
    steps: int,
    span: float,
):
    current = np.asarray(logs, dtype=float).copy()
    current -= np.max(current)
    current_score = objective(weights_from_logs(size, current), fitness, architecture)
    best = (current_score, current.copy())
    for step in range(steps):
        fraction = step / max(1, steps - 1)
        scale = 1.2 * (0.08 / 1.2) ** fraction
        proposal = current.copy()
        count = 1 if rng.random() < 0.72 else int(rng.integers(2, min(6, len(current)) + 1))
        indices = rng.choice(len(current), size=count, replace=False)
        proposal[indices] += rng.normal(0.0, scale, count)
        proposal = np.clip(proposal, -span, 0.0)
        proposal -= np.max(proposal)
        score = objective(weights_from_logs(size, proposal), fitness, architecture)
        temperature = 0.025 * (0.001 / 0.025) ** fraction
        if score >= current_score or rng.random() < math.exp((score - current_score) / temperature):
            current, current_score = proposal, score
        if score > best[0]:
            best = (score, proposal.copy())
    return best


def describe(logs: np.ndarray, size: int, fitness: float, architecture: str) -> None:
    weights = weights_from_logs(size, logs)
    print(f"architecture={architecture} size={size} r={fitness:.12g}")
    if architecture == "center":
        score, log_window, witness, data = center_score(weights, fitness)
        print(f"score={score:+.12g} log_window={log_window:+.12g} witness={witness}")
    else:
        score, common, witness, data = repeated_score(weights, fitness)
        print(f"score={score:+.12g} common={common:.12g} witness={witness}")
    baseline = 1.0 - 1.0 / fitness
    print(
        f"alpha_Bd={data['Bd'][0].mean():.12g} "
        f"alpha_dB={data['dB'][0].mean():.12g} baseline={baseline:.12g}"
    )
    print("logs", " ".join(f"{x:.9g}" for x in logs))
    for row in weights:
        print(" ".join(f"{x:.9g}" for x in row))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, choices=(6, 7, 8), default=6)
    parser.add_argument("--fitness", type=float, default=1.51)
    parser.add_argument("--architecture", choices=("center", "repeated"), default="center")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--random", type=int, default=3000)
    parser.add_argument("--elite", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1500)
    parser.add_argument("--span", type=float, default=14.0)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    edge_count = args.size * (args.size - 1) // 2
    elite: list[tuple[float, np.ndarray]] = []
    for sample in range(args.random):
        logs = random_logs(rng, edge_count, args.span)
        score = objective(weights_from_logs(args.size, logs), args.fitness, args.architecture)
        if len(elite) < args.elite or score > elite[-1][0]:
            elite.append((score, logs.copy()))
            elite.sort(key=lambda item: item[0], reverse=True)
            elite = elite[: args.elite]
        if (sample + 1) % 500 == 0:
            print(f"random={sample+1} best={elite[0][0]:+.10g}", flush=True)

    best = elite[0]
    for rank, (_, logs) in enumerate(elite):
        candidate = local_search(
            logs,
            args.size,
            args.fitness,
            args.architecture,
            rng,
            args.steps,
            args.span,
        )
        if candidate[0] > best[0]:
            best = candidate
        print(f"local={rank+1}/{len(elite)} best={best[0]:+.10g}", flush=True)
    describe(best[1], args.size, args.fitness, args.architecture)


if __name__ == "__main__":
    main()
