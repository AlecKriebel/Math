#!/usr/bin/env python3
"""Exact conservation-extension versus nonnegative drain-multiset alternative."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from functools import reduce
from pathlib import Path
import sys
from typing import Iterable, Sequence

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from src.generator import Reaction  # type: ignore  # noqa:E402
from src.class_analyzer import is_weakly_reversible  # type: ignore  # noqa:E402
from phase3_defect_credit.src.cone_lemma import all_return_path_certificates  # type: ignore  # noqa:E402


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else 0


def _integerize(vec: Sequence[sp.Rational]) -> list[int]:
    den = 1
    for q in vec:
        den = _lcm(den, int(q.q))
    ints = [int(q * den) for q in vec]
    g = reduce(gcd, (abs(v) for v in ints if v), 0) or 1
    return [v // g for v in ints]


@dataclass(frozen=True, slots=True)
class ConservationExtension:
    I: tuple[int, ...]
    J: tuple[int, ...]
    b: tuple[Fraction, ...]

    def full_vector(self, d: int) -> tuple[Fraction, ...]:
        out = [Fraction(0)] * d
        for i in self.I:
            out[i] = Fraction(1)
        for idx, j in enumerate(self.J):
            out[j] = self.b[idx]
        return tuple(out)


@dataclass(frozen=True, slots=True)
class DrainMultiset:
    I: tuple[int, ...]
    J: tuple[int, ...]
    counts: tuple[int, ...]
    net_vector: tuple[int, ...]
    drain_amount: int
    signed_kernel_seed: tuple[int, ...]


def _projected_matrix(reactions: Sequence[Reaction], J: Sequence[int]) -> sp.Matrix:
    return sp.Matrix(len(J), len(reactions), lambda a, r: reactions[r].vector[J[a]])


def _mass_row(reactions: Sequence[Reaction], I: Sequence[int]) -> sp.Matrix:
    return sp.Matrix(1, len(reactions), lambda _, r: sum(reactions[r].vector[i] for i in I))


def conservation_extension(
    reactions: Sequence[Reaction], I: Iterable[int]
) -> ConservationExtension | None:
    if not reactions:
        raise ValueError("empty reaction list")
    d = reactions[0].dimension
    I = tuple(sorted(set(I)))
    if not I:
        raise ValueError("I must be nonempty")
    J = tuple(i for i in range(d) if i not in I)
    A = _projected_matrix(reactions, J)
    m = _mass_row(reactions, I)
    if not J:
        return ConservationExtension(I, J, ()) if all(v == 0 for v in m) else None
    # Solve A^T b = -m^T exactly.
    sol = sp.linsolve((A.T, -m.T))
    if sol is sp.EmptySet:
        return None
    tup = next(iter(sol))
    # Substitute all free parameters by zero to obtain one rational solution.
    free = sorted(set().union(*(expr.free_symbols for expr in tup)), key=str)
    sub = {s: sp.Integer(0) for s in free}
    vals = tuple(sp.Rational(expr.subs(sub)) for expr in tup)
    b = tuple(Fraction(int(q.p), int(q.q)) for q in vals)
    # Independent edge-by-edge verification.
    for r in reactions:
        lhs = sum(r.vector[i] for i in I) + sum(b[a] * r.vector[j] for a, j in enumerate(J))
        if lhs != 0:
            raise AssertionError("computed conservation extension failed verification")
    return ConservationExtension(I, J, b)


def drain_multiset(reactions: Sequence[Reaction], I: Iterable[int]) -> DrainMultiset:
    """Construct Alternative D when no conservation extension exists.

    Start from a signed integer kernel vector h of the J-projection with
    negative I-mass.  Every negative coefficient -a_r v_r is replaced by a_r
    copies of a directed return path representing -v_r.  The result is a
    nonnegative integer reaction multiset with zero J displacement and strict
    negative I-mass.
    """
    if not reactions:
        raise ValueError("empty reaction list")
    if not is_weakly_reversible(reactions):
        raise ValueError("weak reversibility is required")
    d = reactions[0].dimension
    I = tuple(sorted(set(I)))
    J = tuple(i for i in range(d) if i not in I)
    if conservation_extension(reactions, I) is not None:
        raise ValueError("Alternative L holds; no drain multiset is required")
    A = _projected_matrix(reactions, J)
    m = _mass_row(reactions, I)
    basis = A.nullspace()
    witness = None
    for h in basis:
        val = (m * h)[0]
        if val != 0:
            witness = h if val < 0 else -h
            break
    if witness is None:
        raise AssertionError("row-space alternative failed: no separating kernel vector")
    h_int = _integerize([sp.Rational(v) for v in witness])
    if sum(int(m[0, r]) * h_int[r] for r in range(len(reactions))) >= 0:
        h_int = [-v for v in h_int]

    return_paths = all_return_path_certificates(reactions)
    counts = [0] * len(reactions)
    for r_idx, coeff in enumerate(h_int):
        if coeff >= 0:
            counts[r_idx] += coeff
        else:
            for p_idx in return_paths[r_idx].return_indices:
                counts[p_idx] += -coeff
    net = [0] * d
    for c, r in zip(counts, reactions):
        for i, v in enumerate(r.vector):
            net[i] += c * v
    if any(net[j] != 0 for j in J):
        raise AssertionError("constructed multiset is not defect balanced")
    mass = sum(net[i] for i in I)
    if mass >= 0:
        raise AssertionError("constructed multiset does not strictly drain I-mass")
    return DrainMultiset(I, J, tuple(counts), tuple(net), -mass, tuple(h_int))


def theorem_of_alternatives(
    reactions: Sequence[Reaction], I: Iterable[int]
) -> ConservationExtension | DrainMultiset:
    c = conservation_extension(reactions, I)
    return c if c is not None else drain_multiset(reactions, I)


def self_test() -> None:
    # Conservation example 0 <-> A+B has A-B conserved.
    rs1 = [Reaction((0, 0), (1, 1)), Reaction((1, 1), (0, 0))]
    c = conservation_extension(rs1, {0})
    assert c is not None and c.b == (Fraction(-1),)

    # Canonical stress cycle has no A+bB conservation and admits a drain word.
    rs2 = [
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    ]
    assert conservation_extension(rs2, {0}) is None
    d = drain_multiset(rs2, {0})
    assert d.drain_amount >= 1 and d.net_vector[1] == 0


if __name__ == "__main__":
    self_test()
    print("conservation_or_drain.py self-test: OK")
