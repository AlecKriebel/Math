"""Exact Fourier parameterizations for the inherited four-leaf theta pair.

The group Z_2 x Z_2 is represented by integers 0,1,2,3 with XOR as the
group operation.  Every returned coordinate is indexed by a four-tuple whose
XOR is zero.  This module deliberately contains no phylogenetics-specific
dependencies; it implements the displayed-tree definition directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, Mapping, Sequence, Tuple

import sympy as sp


Character = int
Assignment = Tuple[Character, Character, Character, Character]


@dataclass(frozen=True)
class Edge:
    name: str
    parent: str
    child: str


# Parameters are attached to graph positions, not leaf labels.  Consequently
# SOURCE and TARGET use the same edge names and differ only in the labels at
# the B and E pendant positions.
INTERNAL_EDGES: Tuple[Edge, ...] = (
    Edge("rA", "rho", "A"),
    Edge("rC", "rho", "C"),
    Edge("AB", "A", "B"),
    Edge("BC", "B", "C"),
    Edge("CD", "C", "D"),
    Edge("DE", "D", "E"),
    Edge("AF", "A", "F"),
    Edge("EF", "E", "F"),
)

PENDANT_EDGES: Tuple[Edge, ...] = (
    Edge("pB", "B", "leafB"),
    Edge("pD", "D", "leafD"),
    Edge("pF", "F", "leafF"),
    Edge("pE", "E", "leafE"),
)

ALL_EDGES: Tuple[Edge, ...] = INTERNAL_EDGES + PENDANT_EDGES
EDGE_NAMES: Tuple[str, ...] = tuple(edge.name for edge in ALL_EDGES)

SOURCE_LABELS: Mapping[str, int] = {
    "leafB": 1,
    "leafD": 2,
    "leafF": 3,
    "leafE": 4,
}

TARGET_LABELS: Mapping[str, int] = {
    "leafB": 4,
    "leafD": 2,
    "leafF": 3,
    "leafE": 1,
}

RETICULATION_INCOMING = {
    "C": ("rC", "BC"),
    "F": ("AF", "EF"),
}


def zero_sum_assignments() -> Tuple[Assignment, ...]:
    """Return all 64 ordered zero-sum assignments in lexicographic order."""
    return tuple((g1, g2, g3, g1 ^ g2 ^ g3) for g1, g2, g3 in product(range(4), repeat=3))


def model_symbols(model: str, prefix: str = ""):
    """Create edge-multiplier symbols and the two inheritance symbols.

    K2P convention: character 1 is the singleton class and characters 2,3
    share a multiplier.  K3P has one multiplier for each nonzero character.
    """
    model = model.upper()
    if model not in {"JC", "K2P", "K3P"}:
        raise ValueError(model)

    multipliers: Dict[str, Tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]] = {}
    parameters = []
    for edge in EDGE_NAMES:
        if model == "JC":
            x = sp.Symbol(f"{prefix}x_{edge}")
            parameters.append(x)
            multipliers[edge] = (sp.Integer(1), x, x, x)
        elif model == "K2P":
            s, t = sp.symbols(f"{prefix}s_{edge} {prefix}t_{edge}")
            parameters.extend((s, t))
            multipliers[edge] = (sp.Integer(1), s, t, t)
        else:
            x1, x2, x3 = sp.symbols(
                f"{prefix}x1_{edge} {prefix}x2_{edge} {prefix}x3_{edge}"
            )
            parameters.extend((x1, x2, x3))
            multipliers[edge] = (sp.Integer(1), x1, x2, x3)

    lambda_c, lambda_f = sp.symbols(f"{prefix}lambda_C {prefix}lambda_F")
    parameters.extend((lambda_c, lambda_f))
    return multipliers, lambda_c, lambda_f, tuple(parameters)


def _selected_edges(choice_c: int, choice_f: int) -> Tuple[Edge, ...]:
    chosen = {
        RETICULATION_INCOMING["C"][choice_c],
        RETICULATION_INCOMING["F"][choice_f],
    }
    excluded = {
        RETICULATION_INCOMING["C"][1 - choice_c],
        RETICULATION_INCOMING["F"][1 - choice_f],
    }
    assert chosen.isdisjoint(excluded)
    return tuple(edge for edge in ALL_EDGES if edge.name not in excluded)


def _descendant_labels(
    selected: Sequence[Edge], labels: Mapping[str, int]
) -> Dict[str, frozenset[int]]:
    children: Dict[str, list[str]] = {}
    for edge in selected:
        children.setdefault(edge.parent, []).append(edge.child)

    cache: Dict[str, frozenset[int]] = {}

    def descend(node: str) -> frozenset[int]:
        if node in cache:
            return cache[node]
        if node in labels:
            ans = frozenset((labels[node],))
        else:
            ans = frozenset().union(*(descend(child) for child in children.get(node, ())))
        cache[node] = ans
        return ans

    return {edge.name: descend(edge.child) for edge in selected}


def displayed_splits(labels: Mapping[str, int]):
    """Return exact descendant sets for each of the four displayed trees."""
    result = {}
    for choice_c, choice_f in product((0, 1), repeat=2):
        selected = _selected_edges(choice_c, choice_f)
        result[(choice_c, choice_f)] = _descendant_labels(selected, labels)
    return result


def fourier_parameterization(
    labels: Mapping[str, int], model: str, prefix: str = ""
):
    """Return the 64 exact Fourier coordinates and ordered parameters."""
    multipliers, lambda_c, lambda_f, parameters = model_symbols(model, prefix)
    assignments = zero_sum_assignments()
    coordinates: Dict[Assignment, sp.Expr] = {}

    for assignment in assignments:
        by_leaf = {i + 1: assignment[i] for i in range(4)}
        total = sp.Integer(0)
        for choice_c, choice_f in product((0, 1), repeat=2):
            selected = _selected_edges(choice_c, choice_f)
            descendants = _descendant_labels(selected, labels)
            weight_c = lambda_c if choice_c == 0 else 1 - lambda_c
            weight_f = lambda_f if choice_f == 0 else 1 - lambda_f
            monomial = weight_c * weight_f
            for edge in selected:
                character = 0
                for leaf in descendants[edge.name]:
                    character ^= by_leaf[leaf]
                monomial *= multipliers[edge.name][character]
            total += monomial
        coordinates[assignment] = sp.factor(total)

    assert coordinates[(0, 0, 0, 0)] == 1
    return coordinates, parameters


def source_parameterization(model: str, prefix: str = "s_"):
    return fourier_parameterization(SOURCE_LABELS, model, prefix)


def target_parameterization(model: str, prefix: str = "t_"):
    return fourier_parameterization(TARGET_LABELS, model, prefix)


def inverse_fourier_transition_probabilities(multiplier: Sequence[sp.Expr]):
    """Return the four row probabilities for a Z2xZ2 group-based edge.

    For multiplier (1,a1,a2,a3), these are the probabilities of increments
    0,1,2,3.  Strict positivity of these four expressions is the stochastic
    domain used for K2P and K3P.
    """
    if len(multiplier) != 4 or multiplier[0] != 1:
        raise ValueError("expected (1,a1,a2,a3)")
    a1, a2, a3 = multiplier[1:]
    return (
        (1 + a1 + a2 + a3) / 4,
        (1 + a1 - a2 - a3) / 4,
        (1 - a1 + a2 - a3) / 4,
        (1 - a1 - a2 + a3) / 4,
    )


if __name__ == "__main__":
    for model in ("JC", "K2P", "K3P"):
        source, source_parameters = source_parameterization(model)
        target, target_parameters = target_parameterization(model)
        print(
            model,
            "coordinates=", len(source),
            "source_parameters=", len(source_parameters),
            "target_parameters=", len(target_parameters),
            "different_formulas=", sum(source[g] != target[g] for g in source),
        )

