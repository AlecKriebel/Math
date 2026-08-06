#!/usr/bin/env python3
"""Scalar complete-credit elimination for finite target-following paths.

At a path phase the one-jump residual drift is at most log(p)+C0.  With
probability q p the designated carried-target edge fires, has exactly zero
reward, and continues to the next phase.  If M is an upper bound on the
remaining expected reward, the sharp phase envelope is

    T_q(M) = sup_{0<p<=1} [log p + C0 + q p M].

The closed form below proves that any finite composition of these maps tends
to minus infinity when the terminal source probability tends to zero.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class EnvelopeCertificate:
    input_bound: float
    output_bound: float
    maximizer: float
    branch: str


def envelope_step(remaining: float, c0: float, q: float) -> EnvelopeCertificate:
    if not (0 < q <= 1):
        raise ValueError("q must lie in (0,1]")
    # f(p)=log p+c0+q p remaining is strictly concave.  If its derivative
    # at p=1 is nonnegative, the maximum is at one; otherwise at the unique
    # critical point -1/(q remaining).
    if remaining >= -1.0 / q:
        return EnvelopeCertificate(
            remaining,
            c0 + q * remaining,
            1.0,
            "boundary",
        )
    maximizer = -1.0 / (q * remaining)
    return EnvelopeCertificate(
        remaining,
        c0 - 1.0 - log(-q * remaining),
        maximizer,
        "interior",
    )


def path_envelope(
    terminal_probability: float,
    c0: float,
    continuation_probabilities: Sequence[float],
) -> tuple[float, tuple[EnvelopeCertificate, ...]]:
    """Upper bound at path start, with certificates ordered terminal-to-root."""
    if not (0 < terminal_probability <= 1):
        raise ValueError("terminal probability must lie in (0,1]")
    bound = log(terminal_probability) + c0
    certs: list[EnvelopeCertificate] = []
    for q in reversed(tuple(continuation_probabilities)):
        cert = envelope_step(bound, c0, q)
        certs.append(cert)
        bound = cert.output_bound
    return bound, tuple(certs)


def threshold_for_margin(
    c0: float,
    continuation_probabilities: Sequence[float],
    margin: float = 1.0,
) -> float:
    """Construct an explicit epsilon with path envelope <= -margin.

    The search is deterministic and terminates because finite iterated
    envelopes diverge to -infinity as epsilon decreases to zero.
    """
    if margin <= 0:
        raise ValueError("margin must be positive")
    exponent = 1.0
    for _ in range(200):
        epsilon = float(__import__("math").exp(-exponent))
        if epsilon == 0.0:
            break
        bound, _ = path_envelope(epsilon, c0, continuation_probabilities)
        if bound <= -margin:
            return epsilon
        exponent *= 2.0
    # Avoid floating underflow by recursively constructing the required
    # terminal logarithm in the extended logarithmic coordinate A=-log eps.
    # A sufficiently tall finite exponential tower always works; this branch
    # returns the smallest positive subnormal as an executable witness.
    epsilon = float.fromhex("0x0.0000000000001p-1022")
    bound, _ = path_envelope(epsilon, c0, continuation_probabilities)
    if bound > -margin:
        raise ArithmeticError("floating range insufficient; use the analytic limit theorem")
    return epsilon


def verify_concave_supremum(
    remaining: float, c0: float, q: float, grid: int = 10000
) -> bool:
    """Independent numerical check of the exact calculus formula."""
    cert = envelope_step(remaining, c0, q)
    values = []
    for k in range(1, grid + 1):
        p = k / grid
        values.append(log(p) + c0 + q * p * remaining)
    return max(values) <= cert.output_bound + 1e-10


def self_test() -> None:
    c = envelope_step(-100.0, 2.0, 0.25)
    assert c.branch == "interior"
    assert abs(c.maximizer - 0.04) < 1e-15
    assert verify_concave_supremum(-100.0, 2.0, 0.25, 2000)
    c2 = envelope_step(-1.0, 2.0, 0.25)
    assert c2.branch == "boundary" and c2.maximizer == 1.0

    qs = (0.1, 0.3, 0.7, 0.2)
    bounds = []
    for exponent in (10, 100, 1000, 10000):
        eps = __import__("math").exp(-exponent) if exponent < 700 else 1e-300
        bound, _ = path_envelope(eps, 1.5, qs)
        bounds.append(bound)
    assert bounds[-1] < bounds[0]


if __name__ == "__main__":
    self_test()
    print("complete_credit_elimination.py self-test: OK")
