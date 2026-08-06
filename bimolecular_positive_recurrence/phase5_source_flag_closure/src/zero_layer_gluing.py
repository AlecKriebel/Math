#!/usr/bin/env python3
"""Exact zero-layer gluing certificates.

The global proof never infers conservation from unrelated local coboundaries.
Instead, the normalized-log top alternative returns one of three explicit
species-linear invariants, each constant on every complex and therefore on
every reaction of the original one-linkage network.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from phase5_source_flag_closure.src.source_rate_flag import TopAlternative, dot

Complex = tuple[int, ...]


def verify_global_complex_conservation(
    complexes: Sequence[Complex], certificate: TopAlternative
) -> tuple[Fraction, ...]:
    vector = certificate.conservation
    if vector is None:
        raise ValueError("certificate is not a conservation alternative")
    values = {dot(vector, y) for y in complexes}
    if len(values) != 1:
        raise AssertionError("linear form is not constant on the full linkage")
    return vector


def divergence_contradiction(
    sequence: Sequence[Sequence[int]], vector: Sequence[Fraction]
) -> bool:
    """Check on a finite prefix that the invariant values are not constant.

    The theorem uses the analytic fact that a positive-weight divergent
    coordinate and bounded negative-weight coordinates force divergence.
    This helper is only a deterministic audit for explicit examples.
    """
    values = [sum(v * x for v, x in zip(vector, state)) for state in sequence]
    return len(set(values)) > 1


def self_test() -> None:
    C = ((0, 0), (1, 1))
    cert = TopAlternative(
        "service_token_conservation",
        ((1, 1),),
        conservation=(Fraction(1), Fraction(-1)),
        service_species=(1,),
    )
    assert verify_global_complex_conservation(C, cert) == (Fraction(1), Fraction(-1))
    assert divergence_contradiction(((1, 0), (2, 0)), cert.conservation or ())


if __name__ == "__main__":
    self_test()
    print("zero_layer_gluing.py self-test: OK")
