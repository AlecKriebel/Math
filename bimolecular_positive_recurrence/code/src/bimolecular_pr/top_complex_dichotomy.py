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


AVAILABILITY_CASES = frozenset(
    {
        "two_divergent_availability",
        "unary_top_availability",
        "service_availability",
    }
)
INVARIANT_CASES = frozenset(
    {
        "all_top_invariant",
        "K_mass_invariant",
        "signed_invariant",
    }
)


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


def validate_top_classification(
    complexes: Iterable[Complex],
    weights: tuple[Fraction, ...],
    divergent: frozenset[int],
    certificate: TopClassification,
) -> None:
    """Independently validate a returned availability/invariant witness.

    The validator recomputes the top set and then checks only the mathematical
    certificate: strict height separation plus bounded-coordinate supply for
    an availability pair, or exact constancy on every complex for an
    invariant.  It does not call :func:`classify_top_complexes`.
    """
    complexes = tuple(sorted(set(complexes)))
    if not complexes:
        raise ValueError("complex set must be nonempty")
    dimension = len(weights)
    if any(len(y) != dimension for y in complexes):
        raise ValueError("complex and weight dimensions differ")
    if any(weight < 0 for weight in weights) or sum(weights) != 1:
        raise ValueError("weights must be nonnegative and sum to one")
    if any(i < 0 or i >= dimension for i in divergent):
        raise ValueError("divergent index is out of range")
    support = frozenset(i for i, weight in enumerate(weights) if weight > 0)
    if not support.issubset(divergent):
        raise ValueError("positive-weight support must be declared divergent")

    heights = {y: dot(weights, y) for y in complexes}
    maximum = max(heights.values())
    expected_top = tuple(y for y in complexes if heights[y] == maximum)
    if certificate.top != expected_top:
        raise AssertionError("certificate reports the wrong top-complex set")

    if certificate.case in AVAILABILITY_CASES:
        if not isinstance(certificate.witness, tuple) or len(certificate.witness) < 2:
            raise AssertionError("availability certificate has no source-terminal pair")
        source, terminal = certificate.witness[:2]
        if source not in expected_top or terminal not in complexes:
            raise AssertionError("availability pair is not in the required complex sets")
        if heights[source] <= heights[terminal]:
            raise AssertionError("availability pair lacks strict height separation")
        for index, required in enumerate(source):
            if index not in divergent and required > terminal[index]:
                raise AssertionError("terminal does not supply a bounded source reactant")

        if certificate.case == "two_divergent_availability":
            if sum(source[i] for i in divergent) < 2:
                raise AssertionError("two-divergent witness has fewer than two particles")
        elif certificate.case == "unary_top_availability":
            if sum(source) != 1 or sum(source[i] for i in divergent) != 1:
                raise AssertionError("unary witness is not a divergent unary complex")
        else:
            if len(certificate.witness) != 3:
                raise AssertionError("service witness must identify its bounded species")
            service = certificate.witness[2]
            if (
                not isinstance(service, int)
                or not 0 <= service < dimension
                or service in divergent
                or weights[service] != 0
            ):
                raise AssertionError("companion species must be bounded with zero normalized weight")
            if source[service] == 0 or terminal[service] == 0:
                raise AssertionError("companion species is not shared by source and terminal")
        return

    if certificate.case not in INVARIANT_CASES:
        raise AssertionError(f"unknown top-complex case: {certificate.case}")

    if certificate.case == "K_mass_invariant":
        if not isinstance(certificate.witness, frozenset) or not certificate.witness:
            raise AssertionError("K-mass witness must be a nonempty index set")
        if not certificate.witness.issubset(divergent):
            raise AssertionError("K-mass witness contains a nondivergent coordinate")
        vector = tuple(
            Fraction(1) if i in certificate.witness else Fraction(0)
            for i in range(dimension)
        )
    else:
        if not isinstance(certificate.witness, tuple) or len(certificate.witness) != dimension:
            raise AssertionError("invariant witness has the wrong dimension")
        vector = tuple(Fraction(value) for value in certificate.witness)
    if not any(vector):
        raise AssertionError("invariant witness is the zero vector")
    if any(vector[i] < 0 for i in divergent):
        raise AssertionError("invariant is negative on a divergent coordinate")
    if not any(vector[i] > 0 for i in divergent):
        raise AssertionError("invariant has no positive divergent coefficient")
    values = {dot(vector, y) for y in complexes}
    if len(values) != 1:
        raise AssertionError("invariant witness is not constant on all complexes")
