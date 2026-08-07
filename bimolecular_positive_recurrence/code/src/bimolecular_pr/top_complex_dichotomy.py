from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .network import Complex, molecularity


@dataclass(frozen=True)
class TopClassification:
    case: str
    top: tuple[Complex, ...]
    witness: object


def dot(weight: tuple[Fraction, ...], y: Complex) -> Fraction:
    return sum((a * b for a, b in zip(weight, y)), Fraction(0))


def classify_top_complexes(
    complexes: Iterable[Complex],
    weights: tuple[Fraction, ...],
    divergent: frozenset[int],
) -> TopClassification:
    complexes = tuple(sorted(set(complexes)))
    if not complexes:
        raise ValueError("complex set must be nonempty")
    if any(molecularity(y) > 2 for y in complexes):
        raise ValueError("classification is binary only")
    if any(w < 0 for w in weights) or sum(weights) != 1:
        raise ValueError("weights must be nonnegative and sum to one")
    heights = {y: dot(weights, y) for y in complexes}
    a = max(heights.values())
    top = tuple(y for y in complexes if heights[y] == a)
    if len(top) == len(complexes):
        return TopClassification("all_top_invariant", top, weights)

    for y in top:
        divergent_particles = sum(y[i] for i in divergent)
        if divergent_particles >= 2:
            lower = next(c for c in complexes if heights[c] < a)
            return TopClassification("two_divergent_availability", top, (y, lower))

    K = frozenset(i for y in top for i, count in enumerate(y) if count and i in divergent)
    if not K:
        raise AssertionError("positive top height requires a divergent top species")
    qK = {y: sum(y[i] for i in K) for y in complexes}
    if any(qK[y] not in (0, 1) for y in complexes):
        raise AssertionError("binary top configuration violated")
    if all(qK[y] == 1 for y in complexes):
        return TopClassification("K_mass_invariant", top, K)

    unary = next((y for y in top if sum(y) == 1), None)
    if unary is not None:
        lower = next(c for c in complexes if qK[c] == 0)
        return TopClassification("unary_top_availability", top, (unary, lower))

    services: dict[int, tuple[Complex, int]] = {}
    for y in top:
        k_indices = [i for i in K if y[i] == 1]
        if len(k_indices) != 1 or sum(y) != 2:
            raise AssertionError("top complex should be one K particle plus one service")
        service = next(i for i, count in enumerate(y) if count and i not in K)
        services.setdefault(service, (y, k_indices[0]))

    for c in complexes:
        if qK[c] == 0:
            for service, (source, _) in services.items():
                if c[service] > 0:
                    return TopClassification("service_availability", top, (source, c, service))

    signed = tuple(
        Fraction(1) if i in K else Fraction(-1) if i in services else Fraction(0)
        for i in range(len(weights))
    )
    values = {dot(signed, y) for y in complexes}
    if len(values) != 1:
        raise AssertionError("signed invariant certificate failed")
    return TopClassification("signed_invariant", top, signed)
