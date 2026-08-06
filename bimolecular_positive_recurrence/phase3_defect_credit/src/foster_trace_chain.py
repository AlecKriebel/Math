#!/usr/bin/env python3
"""Finite arithmetic checks accompanying the random-time Foster proof.

The mathematical theorem is stated in foster_trace_chain.md.  This module
checks the deterministic finite-set constants used in applications.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


@dataclass(frozen=True, slots=True)
class FiniteTraceBounds:
    path_success_probability: Fraction
    maximum_attempt_duration: Fraction
    maximum_failed_return_duration: Fraction

    @property
    def expected_time_to_reference_bound(self) -> Fraction:
        if self.path_success_probability <= 0:
            raise ValueError("success probability must be positive")
        return (self.maximum_attempt_duration + self.maximum_failed_return_duration) / self.path_success_probability


def product_lower_bound(probabilities: Sequence[Fraction]) -> Fraction:
    out=Fraction(1)
    for p in probabilities:
        if not (0<p<=1): raise ValueError("probabilities must lie in (0,1]")
        out*=p
    return out


def self_test() -> None:
    p=product_lower_bound([Fraction(1,2),Fraction(1,3)])
    b=FiniteTraceBounds(p,Fraction(5),Fraction(7))
    assert b.expected_time_to_reference_bound==72


if __name__=="__main__":
    self_test();print("foster_trace_chain.py self-test: OK")
