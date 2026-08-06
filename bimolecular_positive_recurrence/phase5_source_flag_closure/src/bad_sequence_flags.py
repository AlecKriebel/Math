#!/usr/bin/env python3
"""Normalized-log compactification and deterministic finite audits."""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import log
from pathlib import Path
from typing import Iterable, Sequence

from phase5_source_flag_closure.src.source_rate_flag import (
    TopAlternative,
    bimolecular_complexes,
    dot,
    top_availability_or_conservation,
)

Complex = tuple[int, ...]


def normalized_log_weight(
    residual: Sequence[int], divergent_species: Iterable[int]
) -> tuple[float, ...]:
    """Finite-state approximation to the compactified log direction."""
    I = frozenset(divergent_species)
    denominator = sum(log(residual[i] + 1) for i in I)
    if denominator <= 0:
        raise ValueError("at least one declared divergent coordinate must be positive")
    return tuple(
        log(residual[i] + 1) / denominator if i in I else 0.0
        for i in range(len(residual))
    )


def verify_certificate(
    complexes: Sequence[Complex],
    I: Iterable[int],
    weight: Sequence[Fraction],
    certificate: TopAlternative,
) -> None:
    C = tuple(sorted(set(complexes)))
    I = frozenset(I)
    if certificate.is_available_pair:
        s = certificate.source
        c = certificate.terminal
        assert s is not None and c is not None
        if s not in C or c not in C:
            raise AssertionError("availability pair is not in the complex set")
        if dot(weight, s) <= dot(weight, c):
            raise AssertionError("availability pair lacks strict logarithmic separation")
        # At r+c, every fixed coordinate outside I needed by s must already
        # be supplied by c.  Divergent I coordinates supply the rest.
        for j in range(len(s)):
            if j not in I and s[j] > c[j]:
                raise AssertionError("terminal does not supply a bounded source reactant")
        return
    vector = certificate.conservation
    if vector is None:
        raise AssertionError("certificate has neither pair nor conservation")
    values = {dot(vector, y) for y in C}
    if len(values) != 1:
        raise AssertionError("claimed conservation is not constant on complexes")


def exhaustive_three_species_audit() -> dict[str, int | str]:
    """Exhaust every 3-species complex subset and a finite weight atlas.

    This is a calibration of the finite combinatorial case split, not the
    universal proof.  It includes zero normalized weights on divergent
    species, which stress-tests hidden slower tiers.
    """
    all_complexes = bimolecular_complexes(3)
    counts: dict[str, int] = {}
    h = sha256()
    cases = 0
    for mask in range(1, 1 << len(all_complexes)):
        C = tuple(all_complexes[k] for k in range(len(all_complexes)) if mask & (1 << k))
        for imask in range(1, 1 << 3):
            I = tuple(i for i in range(3) if imask & (1 << i))
            # Values 0,1,2 on I, outside zero; discard all-zero.
            total_assignments = 3 ** len(I)
            for code in range(1, total_assignments):
                digits: list[int] = []
                value = code
                for _ in I:
                    digits.append(value % 3)
                    value //= 3
                if not any(digits):
                    continue
                w = [Fraction(0)] * 3
                for i, digit in zip(I, digits):
                    w[i] = Fraction(digit)
                cert = top_availability_or_conservation(C, I, w)
                verify_certificate(C, I, w, cert)
                cases += 1
                counts[cert.kind] = counts.get(cert.kind, 0) + 1
                record = (mask, imask, tuple(digits), cert.kind, cert.source, cert.terminal, cert.conservation)
                h.update(repr(record).encode("utf-8"))
    result: dict[str, int | str] = {
        "complexes": len(all_complexes),
        "cases": cases,
        "sha256": h.hexdigest(),
    }
    for key in sorted(counts):
        result[key] = counts[key]
    return result


def write_audit(path: str | Path) -> dict[str, int | str]:
    result = exhaustive_three_species_audit()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def self_test() -> None:
    weight = normalized_log_weight((100, 10, 0), {0, 1})
    assert abs(sum(weight) - 1.0) < 1e-15
    assert weight[0] > weight[1] > 0 and weight[2] == 0


if __name__ == "__main__":
    self_test()
    print(json.dumps(exhaustive_three_species_audit(), indent=2, sort_keys=True))
