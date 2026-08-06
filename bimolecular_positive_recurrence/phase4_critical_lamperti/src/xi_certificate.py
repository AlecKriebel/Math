#!/usr/bin/env python3
"""Exact no-criticality certificate for a safe dominant set.

For a mixed one-linkage bimolecular network and a quadratically safe set I,
every complex has q_I in {0,1}.  A q_I=1 complex is either a unary I complex
or I_i + D for one outside species D.  The latter D is called a service token.

The certificate proves the exact dichotomy used in Phase IV:

* an unpaired service is structurally present (hence the limiting slow
  macrochain has a strict negative reward); or
* M_I minus the number of service tokens is an exact linear conservation law.

This is a finite edge-by-edge assertion; it makes no comparison between
independent rate monomials.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from src.generator import Complex, Reaction  # type: ignore  # noqa:E402
from src.class_analyzer import is_weakly_reversible, linkage_classes  # type: ignore  # noqa:E402
from phase2_trigger_drain.src.support_regimes import (  # type: ignore  # noqa:E402
    certify_safe_support,
    q_count,
)


@dataclass(frozen=True, slots=True)
class ServiceTokenCertificate:
    I: tuple[int, ...]
    J: tuple[int, ...]
    unary_q1_complexes: tuple[Complex, ...]
    service_species: tuple[int, ...]
    q0_complexes_with_service: tuple[Complex, ...]
    alternative: str  # "strict_drain" or "conservation"
    conservation_vector: tuple[Fraction, ...] | None

    @property
    def has_unpaired_service(self) -> bool:
        return self.alternative == "strict_drain"


def _complexes(reactions: Sequence[Reaction]) -> tuple[Complex, ...]:
    return tuple(sorted({r.source for r in reactions} | {r.target for r in reactions}))


def service_token_dichotomy(
    reactions: Sequence[Reaction], I: Iterable[int]
) -> ServiceTokenCertificate:
    """Return and independently verify the service-token dichotomy.

    Hypotheses: nonempty, weakly reversible, one linkage class, bimolecular,
    mixed molecularity, and I quadratically safe.  The safe-support theorem
    then supplies q_I(C) subset {0,1}.
    """
    rs = tuple(reactions)
    if not rs:
        raise ValueError("empty reaction list")
    if not is_weakly_reversible(rs):
        raise ValueError("weak reversibility is required")
    if len(linkage_classes(rs)) != 1:
        raise ValueError("the certificate is for one linkage class")
    if any(sum(y) > 2 for y in _complexes(rs)):
        raise ValueError("network is not bimolecular")
    mols = {sum(y) for y in _complexes(rs)}
    if len(mols) == 1:
        raise ValueError("pure-molecularity linkage is conservative and not the mixed case")

    I = tuple(sorted(set(I)))
    if not I:
        raise ValueError("I must be nonempty")
    d = rs[0].dimension
    J = tuple(i for i in range(d) if i not in I)
    certify_safe_support(rs, I)
    C = _complexes(rs)
    if any(q_count(y, I) not in (0, 1) for y in C):
        raise AssertionError("safe mixed one-linkage conclusion q_I in {0,1} failed")

    unary_q1 = tuple(y for y in C if q_count(y, I) == 1 and sum(y) == 1)
    K: set[int] = set()
    for y in C:
        if q_count(y, I) != 1 or sum(y) != 2:
            continue
        outside = [j for j in J if y[j]]
        if len(outside) != 1 or y[outside[0]] != 1:
            raise AssertionError("a binary q_I=1 complex must be I_i + D")
        K.add(outside[0])
    q0_with_K = tuple(
        y for y in C if q_count(y, I) == 0 and any(y[j] for j in K)
    )

    if unary_q1 or q0_with_K:
        return ServiceTokenCertificate(
            I=I,
            J=J,
            unary_q1_complexes=unary_q1,
            service_species=tuple(sorted(K)),
            q0_complexes_with_service=q0_with_K,
            alternative="strict_drain",
            conservation_vector=None,
        )

    # No unary q1 and no q0 complex contains a service species.  Therefore
    # each q1 complex contains exactly one K-particle and each q0 complex none.
    w = [Fraction(0)] * d
    for i in I:
        w[i] += 1
    for j in K:
        w[j] -= 1
    for y in C:
        q = q_count(y, I)
        token = sum(y[j] for j in K)
        if q == 1 and token != 1:
            raise AssertionError("q1 complex does not carry exactly one service token")
        if q == 0 and token != 0:
            raise AssertionError("q0 complex unexpectedly carries a service token")
    for r in rs:
        if sum(w[i] * r.vector[i] for i in range(d)) != 0:
            raise AssertionError("service-token conservation failed edge by edge")
    return ServiceTokenCertificate(
        I=I,
        J=J,
        unary_q1_complexes=(),
        service_species=tuple(sorted(K)),
        q0_complexes_with_service=(),
        alternative="conservation",
        conservation_vector=tuple(w),
    )


def self_test() -> None:
    # Canonical catalytic drain: B is an unpaired service token because B is
    # itself a q_A=0 complex.
    rs = (
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    )
    c = service_token_dichotomy(rs, {0})
    assert c.alternative == "strict_drain" and c.service_species == (1,)

    # Exact paired token: 0 <-> A+B conserves A-B.
    rs2 = (Reaction((0, 0), (1, 1)), Reaction((1, 1), (0, 0)))
    c2 = service_token_dichotomy(rs2, {0})
    assert c2.alternative == "conservation"
    assert c2.conservation_vector == (Fraction(1), Fraction(-1))

    # Several I types and service conversion, still exact token conservation.
    # 0 -> A+C -> B+D -> 0, with I={A,B}, K={C,D}.
    rs3 = (
        Reaction((0, 0, 0, 0), (1, 0, 1, 0)),
        Reaction((1, 0, 1, 0), (0, 1, 0, 1)),
        Reaction((0, 1, 0, 1), (0, 0, 0, 0)),
    )
    c3 = service_token_dichotomy(rs3, {0, 1})
    assert c3.alternative == "conservation"
    assert c3.conservation_vector == (
        Fraction(1), Fraction(1), Fraction(-1), Fraction(-1)
    )

    # Unary q1 source is an unpaired service architecture.
    rs4 = (
        Reaction((0, 0), (1, 0)),
        Reaction((1, 0), (0, 1)),
        Reaction((0, 1), (0, 0)),
    )
    c4 = service_token_dichotomy(rs4, {0})
    assert c4.alternative == "strict_drain" and c4.unary_q1_complexes


if __name__ == "__main__":
    self_test()
    print("xi_certificate.py self-test: OK")
