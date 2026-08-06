#!/usr/bin/env python3
"""Exact quadratic-support and dominant-molecule graph lemmas.

The routines in this module are finite graph checks.  They do not infer
asymptotic population scales numerically.  A caller supplies a candidate
species set I and the module verifies the exact conclusions used in the
Phase-II proof.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
PHASE1 = HERE.parent.parent
sys.path.insert(0, str(PHASE1))

from src.class_analyzer import linkage_classes, safe_supports, support  # type: ignore  # noqa:E402
from src.generator import Complex, Reaction  # type: ignore  # noqa:E402


def q_count(y: Sequence[int], I: Iterable[int]) -> int:
    """Number of molecules of complex ``y`` whose species index lies in I."""
    J = frozenset(I)
    return sum(y[i] for i in J)


@dataclass(frozen=True, slots=True)
class SafeSupportCertificate:
    species: frozenset[int]
    pure_binary_linkages: tuple[tuple[Complex, ...], ...]
    mixed_linkages: tuple[tuple[Complex, ...], ...]
    q_monotone_edges: tuple[tuple[Complex, Complex, int, int], ...]
    strict_q_descents: tuple[tuple[Complex, Complex], ...]
    q_is_conserved: bool


def _linkage_reactions(
    reactions: Sequence[Reaction], linkage: set[Complex]
) -> tuple[Reaction, ...]:
    return tuple(r for r in reactions if r.source in linkage)


def certify_safe_support(
    reactions: Sequence[Reaction], I: Iterable[int]
) -> SafeSupportCertificate:
    """Verify the finite safe-support lemmas for a candidate set I.

    The candidate must be quadratically safe in the literal graph sense:
    every binary source supported in I has a binary product supported in I.

    Conclusions checked and returned:

    1. Any linkage containing a binary complex supported in I consists
       entirely of binary complexes supported in I.
    2. For every reaction with q_I(source)>0,
           q_I(target) <= q_I(source).
    3. In every mixed linkage, q_I takes only the values 0 and 1.
    4. If no strict q_I descent exists, q_I is a global linear conservation
       law (checked edge by edge).
    """
    rs = tuple(reactions)
    if not rs:
        raise ValueError("reaction list is empty")
    I = frozenset(I)
    if I not in safe_supports(rs):
        raise ValueError("I is not a quadratically safe nonempty support")

    pure: list[tuple[Complex, ...]] = []
    mixed: list[tuple[Complex, ...]] = []
    for linkage in linkage_classes(rs):
        has_supported_binary = any(
            sum(y) == 2 and support(y).issubset(I) for y in linkage
        )
        if has_supported_binary:
            if not all(sum(y) == 2 and support(y).issubset(I) for y in linkage):
                raise AssertionError(
                    "safe-support linkage lemma failed: supported binary complex "
                    "shares a linkage with a non-supported/non-binary complex"
                )
            pure.append(tuple(sorted(linkage)))
        else:
            mixed.append(tuple(sorted(linkage)))
            if any(q_count(y, I) == 2 for y in linkage):
                raise AssertionError("mixed linkage contains q_I=2 complex")

    monotone: list[tuple[Complex, Complex, int, int]] = []
    descents: list[tuple[Complex, Complex]] = []
    for r in rs:
        qs = q_count(r.source, I)
        qt = q_count(r.target, I)
        if qs > 0:
            if qt > qs:
                raise AssertionError("q_I increases from a positive source")
            monotone.append((r.source, r.target, qs, qt))
            if qt < qs:
                descents.append((r.source, r.target))

    conserved = all(q_count(r.source, I) == q_count(r.target, I) for r in rs)
    if not descents and not conserved:
        raise AssertionError("absence of strict descent did not imply conservation")

    return SafeSupportCertificate(
        species=I,
        pure_binary_linkages=tuple(pure),
        mixed_linkages=tuple(mixed),
        q_monotone_edges=tuple(monotone),
        strict_q_descents=tuple(descents),
        q_is_conserved=conserved,
    )


def conservation_vector_for_support(d: int, I: Iterable[int]) -> tuple[Fraction, ...]:
    I = frozenset(I)
    return tuple(Fraction(1 if i in I else 0) for i in range(d))


def self_test() -> None:
    # Canonical mixed linkage. I={A} and I={B} are safe.  For I={A}, q descends
    # on A+B -> B.  No q=2 complex occurs.
    rs = (
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    )
    c = certify_safe_support(rs, {0})
    assert c.strict_q_descents == (((1, 1), (0, 1)),)
    assert not c.q_is_conserved
    assert all(qs in (1,) and qt in (0, 1) for _, _, qs, qt in c.q_monotone_edges)

    # A<->A+B conserves A exactly on the safe support {A}.
    rs2 = (Reaction((1, 0), (1, 1)), Reaction((1, 1), (1, 0)))
    c2 = certify_safe_support(rs2, {0})
    assert c2.q_is_conserved
    assert not c2.strict_q_descents

    # A pure binary linkage can coexist with a mixed linkage.  The former is
    # classified separately and preserves q_I=2.
    rs3 = (
        Reaction((2, 0, 0), (1, 1, 0)),
        Reaction((1, 1, 0), (2, 0, 0)),
        Reaction((0, 0, 0), (1, 0, 1)),
        Reaction((1, 0, 1), (0, 0, 1)),
        Reaction((0, 0, 1), (0, 0, 0)),
    )
    c3 = certify_safe_support(rs3, {0, 1})
    assert len(c3.pure_binary_linkages) == 1
    assert len(c3.mixed_linkages) == 1


if __name__ == "__main__":
    self_test()
    print("support_regimes.py self-test: OK")
