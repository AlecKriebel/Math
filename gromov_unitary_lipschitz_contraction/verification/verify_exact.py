#!/usr/bin/env python3
"""Exact finite algebra checks; NOT a proof of the analytic theorem.

Uses Python's standard library only. Words in U,V,W and their adjoints do
not commute; the scalar indeterminate t does. Adjacent unitary inverse
pairs cancel. All coefficients are rational and all checks are exact.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import platform
import sys


INVERSE = {"U": "u", "u": "U", "V": "v", "v": "V", "W": "w", "w": "W"}


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and INVERSE.get(letter) == stack[-1]:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


class Poly:
    """Sparse Q[t] group algebra; keys are (t exponent, ordered word)."""

    def __init__(self, terms=None):
        self.terms = {}
        for (power, word), coefficient in (terms or {}).items():
            key = power, reduce_word(word)
            self.terms[key] = self.terms.get(key, Fraction(0)) + Fraction(coefficient)
        self.terms = {key: value for key, value in self.terms.items() if value}

    def __add__(self, other):
        result = self.terms.copy()
        for key, value in other.terms.items():
            result[key] = result.get(key, Fraction(0)) + value
        return Poly(result)

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        result = {}
        for (a, word_a), coefficient_a in self.terms.items():
            for (b, word_b), coefficient_b in other.terms.items():
                key = a + b, reduce_word(word_a + word_b)
                result[key] = result.get(key, Fraction(0)) + coefficient_a * coefficient_b
        return Poly(result)

    def adjoint(self):
        return Poly({(p, tuple(INVERSE[x] for x in reversed(w))): c
                     for (p, w), c in self.terms.items()})

    def is_zero(self):
        return not self.terms

    def readable(self):
        return [{"t_power": p, "word": "".join(w) or "I", "coefficient": str(c)}
                for (p, w), c in sorted(self.terms.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("results_exact.json"))
    args = parser.parse_args()
    one = Poly({(0, ()): 1})
    t = Poly({(1, ()): 1})
    U, V, W = [Poly({(0, (letter,)): 1}) for letter in "UVW"]
    X, Y = W + t, one + t * W
    checks = []

    def check(name, condition, **detail):
        checks.append({"name": name, "passed": bool(condition), **detail})

    # Sanity checks must detect an implementation that commutes the letters
    # or incorrectly treats t as zero.
    check("word_order_is_retained", not (U * V - V * U).is_zero())
    check("scalar_indeterminate_is_retained", not (t - one).is_zero())
    check("unitary_relations", (U.adjoint() * U - one).is_zero()
          and (U * U.adjoint() - one).is_zero())
    check("adjoint_reverses_word_order",
          ((U * V).adjoint() - V.adjoint() * U.adjoint()).is_zero())

    numerator = ((U + t) * (one + t * V)
                 - (one + t * U) * (V + t)
                 - (one - t * t) * (U - V))
    check("noncommutative_difference_numerator", numerator.is_zero(),
          remainder=numerator.readable())
    check("unitarity_numerator", (X.adjoint() * X - Y.adjoint() * Y).is_zero())
    check("resolvent_gram_expansion",
          (Y.adjoint() * Y - (one + t * t) - t * (W + W.adjoint())).is_zero())
    check("left_right_resolvent_commutation",
          (Y * X - X * Y).is_zero())

    # Exact scalar evidence that the semicircle assumption cannot simply be
    # deleted: at W=-1 and t=1/2 the angular derivative is 3, versus q=3/5.
    scalar_t = Fraction(1, 2)
    q = (1 - scalar_t**2) / (1 + scalar_t**2)
    outside_derivative = (1 - scalar_t**2) / (1 - scalar_t)**2
    check("outside_semicircle_derivative_exceeds_bound",
          outside_derivative > q and outside_derivative > 1,
          derivative=str(outside_derivative), q=str(q))
    check("outside_semicircle_endpoint_can_be_singular", 1 + 1 * (-1) == 0)

    passed = all(item["passed"] for item in checks)
    result = {
        "scope": "Exact finite algebra identities and scalar counterchecks only; not a proof of the analytic theorem.",
        "limitations": ["No automatic verification of matrix order inequalities, curve lengths, or mapping-space continuity.",
                        "Formal inverses are eliminated before checking; their existence requires the analytic proof."],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "arithmetic": "fractions.Fraction; ordered unitary words",
        "passed": passed,
        "checks": checks,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Exact algebra: {sum(c['passed'] for c in checks)}/{len(checks)} passed; {args.output}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
