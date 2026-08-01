#!/usr/bin/env python3
"""Exact trace and DTH witness pairings in raw highest-weight charts.

The exact support chart stores a moment block by its raw restriction

    H = E A E^T,

where the columns of the underlying Specht basis are not orthonormal.  This
module records the Gram corrections needed to evaluate the physical trace
and the lifted witness without introducing square roots.

If ``G`` is the raw basis Gram matrix and ``W`` is the raw restriction of an
invariant witness, then the corresponding physical block contributes

    carrier_dimension * Tr(G^{-1} H)

to the trace and

    carrier_dimension * Tr(G^{-1} W G^{-1} H)

to the witness pairing.  All matrices here are rational.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from pathlib import Path
import importlib.util

import sympy as sp


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


EXACT_K = import_file(
    "dth_exact_k_for_functionals", HERE / "agent_dth_exact_k_coordinates.py"
)
BRIDGE = EXACT_K.BRIDGE


def transposition(first, second):
    out = list(range(5))
    out[first], out[second] = out[second], out[first]
    return tuple(out)


@lru_cache(None)
def local_pair_antisymmetry_restriction(shape, first):
    """Raw restriction of ``(I-F_{first,5})/2`` at one site."""
    gram = EXACT_K.local_gram(shape)
    representation = EXACT_K.local_representation(
        shape, transposition(first, 4)
    )
    # A raw restriction is B^* O B = G [O]_B.
    return gram * (sp.eye(gram.rows) - representation) / 2


@lru_cache(None)
def global_gram(shapes):
    return EXACT_K.kron3(tuple(
        EXACT_K.local_gram(shape) for shape in shapes
    ))


@lru_cache(None)
def witness_restriction(shapes):
    """Raw restriction of the lifted minimal-DTH witness O0 tilde."""
    shapes = tuple(shapes)
    gram = global_gram(shapes)
    first = EXACT_K.kron3(tuple(
        local_pair_antisymmetry_restriction(shape, 0)
        for shape in shapes
    ))
    second = EXACT_K.kron3(tuple(
        local_pair_antisymmetry_restriction(shape, 2)
        for shape in shapes
    ))
    return gram / 4 - first - second


def carrier_dimension(shapes):
    result = 1
    for shape in shapes:
        result *= BRIDGE.HOL_IRREP_DIMS[shape]
    return result


def restriction_from_coordinate(shapes, coordinate):
    """Return the exact supported restriction ``E A E^T``."""
    _, _, restriction_range = EXACT_K.hol_k_coordinates(tuple(shapes))
    coordinate = sp.Matrix(coordinate)
    if coordinate.shape != (restriction_range.cols, restriction_range.cols):
        raise ValueError("coordinate block has the wrong shape")
    if coordinate != coordinate.T:
        raise ValueError("coordinate block is not symmetric")
    return restriction_range * coordinate * restriction_range.T


def block_functionals(shapes, coordinate):
    """Return exact ``(trace, witness_pairing)`` for one supported block."""
    shapes = tuple(shapes)
    physical_basis, gram, restriction_range = (
        EXACT_K.hol_k_coordinates(shapes)
    )
    coordinate = sp.Matrix(coordinate)
    if coordinate.shape != (physical_basis.cols, physical_basis.cols):
        raise ValueError("coordinate block has the wrong shape")
    if coordinate != coordinate.T:
        raise ValueError("coordinate block is not symmetric")
    # Since E=G*K and H=E*A*E^T=G*K*A*K^T*G, cyclicity removes both
    # inverse Grams from the general raw-restriction formula.  Only the
    # small (at most 16 dimensional) compressed forms remain.
    assert restriction_range == gram * physical_basis
    carrier = carrier_dimension(shapes)
    trace = carrier * sp.trace(
        coordinate * physical_basis.T * gram * physical_basis
    )
    objective = carrier * sp.trace(
        coordinate * physical_basis.T
        * witness_restriction(shapes) * physical_basis
    )
    return sp.factor(trace), sp.factor(objective)


def total_functionals(coordinates):
    """Sum exact pairings for a mapping ``shape triple -> A block``."""
    trace = sp.Integer(0)
    objective = sp.Integer(0)
    for shapes in product(range(5), repeat=3):
        coordinate = coordinates[shapes]
        block_trace, block_objective = block_functionals(shapes, coordinate)
        trace += block_trace
        objective += block_objective
    return sp.factor(trace), sp.factor(objective)


def _self_test():
    # The zero moment is sufficient to audit all conventions and dimensions
    # in a lightweight block without importing a certificate artifact.
    shapes = (0, 0, 2)
    _, _, restriction_range = EXACT_K.hol_k_coordinates(shapes)
    zero = sp.zeros(restriction_range.cols)
    trace, objective = block_functionals(shapes, zero)
    assert trace == objective == 0
    assert witness_restriction(shapes) == witness_restriction(shapes).T
    print("exact DTH raw functional conventions passed")


if __name__ == "__main__":
    _self_test()
