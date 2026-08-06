#!/usr/bin/env python3
"""Audit that the Phase-V sign proof does not order independent rate monomials.

Rates enter only through:
  (i) the finite additive constant C0;
  (ii) positive conditional path probabilities q_e;
  (iii) exact embedded-chain source probabilities.
The asymptotic source separation is supplied solely by falling-factorial
ratios with a strictly positive normalized-log exponent gap.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
from typing import Iterable

ALLOWED_RATE_PHRASES = (
    "positive reaction rates",
    "conditional edge probability",
    "entropy-rate constant",
    "no comparison",
)
PROHIBITED_PATTERNS = (
    re.compile(r"rate monomial.*dominates.*rate monomial", re.I),
    re.compile(r"replace(?:s|d)? .* reaction edge", re.I),
)


def scan_text(text: str) -> list[str]:
    findings: list[str] = []
    for pattern in PROHIBITED_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(match.group(0))
    return findings


def scan_files(paths: Iterable[str | Path]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for raw in paths:
        path = Path(raw)
        findings = scan_text(path.read_text())
        if findings:
            result[str(path)] = findings
    return result


def conditional_probability(rate: Fraction, outgoing_sum: Fraction) -> Fraction:
    if rate <= 0 or outgoing_sum < rate:
        raise ValueError("invalid positive rate data")
    return rate / outgoing_sum


def self_test() -> None:
    assert conditional_probability(Fraction(2), Fraction(5)) == Fraction(2, 5)
    assert not scan_text("The proof makes no comparison of independent rate monomials.")
    assert scan_text("A rate monomial dominates another rate monomial")


if __name__ == "__main__":
    self_test()
    print("rate_monomial_audit.py self-test: OK")
