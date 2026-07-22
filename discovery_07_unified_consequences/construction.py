#!/usr/bin/env python3
"""Exact constructions used by the unified Discovery 07 paper.

This module deliberately treats Discoveries 03 and 06 as immutable technical
precursors.  It imports their exact constructions and adds only the new
inverse-series targets, observables, coefficient formulas, and symmetric
companions needed by the canonical consequence paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from importlib import util
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
D3 = ROOT / "discovery_03_small_vanishing_counterexample"
D6 = ROOT / "discovery_06_unipotent_three_point"


def _load_module(name: str, path: Path):
    spec = util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


if str(D3) not in sys.path:
    sys.path.insert(0, str(D3))

from compressed_construction import (  # noqa: E402
    compressed_cubic_map,
    cubic_component_factorization,
)
from stable_reduction import degree_reduction  # noqa: E402

_d6 = _load_module("discovery06_exact_construction", D6 / "construction.py")


WEIGHTS_14 = (1, 1, 1, 2, 3, 2, 3, 4, 5, 2, 3, 4, 5, 6)


@dataclass(frozen=True)
class EveryOrderData:
    """A nilpotent map, fixed inverse target, and linear observable."""

    variables: tuple[sp.Symbol, ...]
    nonlinear: tuple[sp.Expr, ...]
    target: tuple[sp.Rational, ...]
    observable_indices: tuple[int, ...]


@lru_cache(maxsize=1)
def d6_construction():
    return _d6.build_construction()


@lru_cache(maxsize=1)
def d6_homogeneous_data() -> EveryOrderData:
    data = d6_construction()
    variables, nonlinear = _d6.homogeneous_companion(data)
    target = (
        sp.Rational(1, 2),
        sp.Rational(0),
        sp.Rational(1),
    ) + (sp.Rational(0),) * 11 + (sp.Rational(1),)
    return EveryOrderData(
        variables=tuple(variables),
        nonlinear=tuple(nonlinear),
        target=target,
        observable_indices=(0, 1, 3),
    )


@lru_cache(maxsize=1)
def d6_direct_data() -> EveryOrderData:
    data = d6_construction()
    target = (
        sp.Rational(1, 2),
        sp.Rational(0),
        sp.Rational(1),
    ) + (sp.Rational(0),) * 11
    return EveryOrderData(
        variables=tuple(data.variables),
        nonlinear=tuple(data.g),
        target=target,
        observable_indices=(0, 1, 3),
    )


@lru_cache(maxsize=1)
def d3_quartic_data() -> EveryOrderData:
    reduction = degree_reduction()
    variables, nonlinear, _, _ = compressed_cubic_map(reduction)
    raw_target = sp.Matrix(
        [sp.Rational(1, 2), sp.Rational(0), sp.Rational(1)] + [0] * 10
    )
    normalized_target = reduction.linear_part.inv() * raw_target
    target = tuple(sp.Rational(value) for value in normalized_target)
    target += (sp.Rational(0),) * 8 + (sp.Rational(1),)
    g3a_index = tuple(map(str, variables)).index("g3a")
    return EveryOrderData(
        variables=tuple(variables),
        nonlinear=tuple(nonlinear),
        target=target,
        observable_indices=(0, 1, g3a_index),
    )


def q_coefficient(m: int) -> Fraction:
    """Coefficient of the Discovery 06 observable at inverse order ``m``."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    if m % 3 == 0:
        k = m // 3
        return Fraction((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
    if m % 3 == 1:
        k = (m - 1) // 3
        return Fraction(
            (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
            (3 * k + 1) * 2 ** (2 * k + 1),
        )
    k = (m - 2) // 3
    return Fraction(
        (-1) ** k * comb(3 * k + 4, k + 1),
        2 ** (2 * k + 3),
    )


def r_coefficient(m: int) -> Fraction:
    """Coefficient of the Discovery 03 quartic-route inverse observable."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    if m % 3 == 0:
        k = m // 3
        return Fraction((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
    if m % 3 == 1:
        k = (m - 1) // 3
        return Fraction(
            (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
            (3 * k + 1) * 2 ** (2 * k + 1),
        )
    k = (m - 2) // 3
    return Fraction(
        (-1) ** k * 3 * comb(3 * k + 2, k),
        2 ** (2 * k + 2),
    )


def symmetrized_potential(
    data: EveryOrderData,
    first_prefix: str = "a",
    second_prefix: str = "b",
):
    """Return ``P(A,B)=i H(A+iB).B`` and its ordered variables."""
    n = len(data.variables)
    first = tuple(sp.symbols(f"{first_prefix}1:{n + 1}"))
    second = tuple(sp.symbols(f"{second_prefix}1:{n + 1}"))
    substitutions = {
        variable: first[index] + sp.I * second[index]
        for index, variable in enumerate(data.variables)
    }
    potential = sp.expand(
        sp.I
        * sum(
            component.subs(substitutions) * second[index]
            for index, component in enumerate(data.nonlinear)
        )
    )
    return first + second, potential


def source_fiber_groebner():
    """Exact source-fiber Groebner basis at ``(0,0,-1/4)``."""
    data = d6_construction()
    x, y, z = data.base_variables
    equations = [
        sp.together(data.phi[0]),
        sp.together(data.phi[1]),
        sp.together(data.phi[2] + sp.Rational(1, 4)),
    ]
    cleared = [sp.Poly(equation, x, y, z).clear_denoms()[1] for equation in equations]
    return sp.groebner(cleared, z, y, x, order="lex")


__all__ = [
    "EveryOrderData",
    "ROOT",
    "WEIGHTS_14",
    "compressed_cubic_map",
    "cubic_component_factorization",
    "d3_quartic_data",
    "d6_construction",
    "d6_direct_data",
    "d6_homogeneous_data",
    "degree_reduction",
    "q_coefficient",
    "r_coefficient",
    "source_fiber_groebner",
    "symmetrized_potential",
]
