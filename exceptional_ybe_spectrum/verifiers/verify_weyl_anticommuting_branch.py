#!/usr/bin/env python3
"""Exact verifier for the anticommuting product branch seen numerically."""

from __future__ import annotations

import argparse
from pathlib import Path

import sympy as sp


def kron(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.ones(1, 1)
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    identity_two = sp.eye(2)
    identity_three = sp.eye(3)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)

    # The one-site reflections lie in the retained Weyl frame.
    s = kron(z, identity_three)
    t = kron(x, identity_three)
    identity_six = sp.eye(6)
    assert s * s == identity_six
    assert t * t == identity_six
    assert s * t + t * s == sp.zeros(6)
    assert sp.trace(s) == sp.trace(t) == 0

    k = kron(s, t)
    identity_thirty_six = sp.eye(36)
    assert k * k == identity_thirty_six
    assert sp.trace(k) == 0

    k_one = kron(k, identity_six)
    k_two = kron(identity_six, k)
    assert k_one * k_two + k_two * k_one == sp.zeros(216)
    assert (
        k_one * k_two * k_one - k_two * k_one * k_two
        == k_one - k_two
    )
    assert k_one != k_two
    assert (
        k_one * k_two * k_one
        - k_two * k_one * k_two
        - (k_one - k_two) / 3
        != sp.zeros(216)
    )

    # For H=uK, derive the normalized weighted objective exactly.
    u, w, y = sp.symbols("u w y", real=True)
    objective = (u**2 - 1) ** 2 + 2 * w * u**2 * (u**2 - sp.Rational(1, 3)) ** 2
    derivative_in_y = sp.diff(
        (y - 1) ** 2 + 2 * w * y * (y - sp.Rational(1, 3)) ** 2,
        y,
    )
    expected = 2 * (
        y
        - 1
        + w
        * (y - sp.Rational(1, 3))
        * (3 * y - sp.Rational(1, 3))
    )
    assert sp.expand(derivative_in_y - expected) == 0

    lines = [
        "S^2=T^2=I and ST=-TS: exact",
        "K=S tensor T is a balanced Hermitian involution: exact",
        "{K_12,K_23}=0: exact",
        "K_12 K_23 K_12-K_23 K_12 K_23=K_12-K_23: exact",
        "exceptional coefficient 1/3 fails for K: exact",
        f"scalar-branch objective: {objective}",
        f"scalar-branch stationarity: {expected}",
        "PASS",
    ]
    rendered = "\n".join(lines) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
