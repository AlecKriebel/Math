#!/usr/bin/env python3
"""Definition-level mass-action flux and Jacobian routines."""
from __future__ import annotations

from typing import Sequence

import sympy as sp

from network_parser import Network


def monomial(source: Sequence[int], x: Sequence[sp.Expr]) -> sp.Expr:
    return sp.prod(sp.sympify(xi) ** exponent for xi, exponent in zip(x, source))


def rates_to_flux(network: Network, rates: Sequence[sp.Expr], equilibrium: Sequence[sp.Expr]) -> sp.Matrix:
    if len(rates) != network.m or len(equilibrium) != network.n:
        raise ValueError("dimension mismatch")
    return sp.Matrix([
        sp.sympify(rates[r]) * monomial(network.reactions[r].source, equilibrium)
        for r in range(network.m)
    ])


def factorized_jacobian(network: Network, flux: Sequence[sp.Expr], h: Sequence[sp.Expr]) -> sp.Matrix:
    if len(flux) != network.m or len(h) != network.n:
        raise ValueError("dimension mismatch")
    Gamma = network.stoichiometric_matrix()
    Y = network.source_matrix()
    return sp.simplify(Gamma * sp.diag(*map(sp.sympify, flux)) * Y.T * sp.diag(*map(sp.sympify, h)))


def direct_symbolic_jacobian(network: Network, rates: Sequence[sp.Expr], equilibrium: Sequence[sp.Expr]) -> sp.Matrix:
    if len(rates) != network.m or len(equilibrium) != network.n:
        raise ValueError("dimension mismatch")
    if network.m == 0:
        return sp.zeros(network.n, network.n)
    symbols = sp.symbols(f"x0:{network.n}", positive=True)
    reaction_rates = sp.Matrix([
        sp.sympify(rates[r]) * monomial(network.reactions[r].source, symbols)
        for r in range(network.m)
    ])
    field = network.stoichiometric_matrix() * reaction_rates
    jac = field.jacobian(symbols)
    return sp.simplify(jac.subs(dict(zip(symbols, map(sp.sympify, equilibrium)))))


def reconstruct_rates(network: Network, flux: Sequence[sp.Expr], equilibrium: Sequence[sp.Expr]) -> tuple[sp.Expr, ...]:
    if len(flux) != network.m or len(equilibrium) != network.n:
        raise ValueError("dimension mismatch")
    rates = []
    for r, reaction in enumerate(network.reactions):
        denominator = monomial(reaction.source, equilibrium)
        rates.append(sp.simplify(sp.sympify(flux[r]) / denominator))
    return tuple(rates)
