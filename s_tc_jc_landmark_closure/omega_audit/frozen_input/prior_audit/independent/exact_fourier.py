"""Independent exact Fourier engine for rooted group-based network models.

The implementation follows the displayed-tree definition directly and has no
dependency on the discovery Fourier engine.  The group Z2 x Z2 is encoded by
the integers 0,1,2,3 with XOR as addition.  Arithmetic is generic: callers may
use Fraction, the Dual class below, or symbolic expressions.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


Assignment = Tuple[int, ...]
Arc = Tuple[str, str]


def zero_sum_assignments(number_of_leaves: int) -> Tuple[Assignment, ...]:
    if number_of_leaves < 1:
        raise ValueError("at least one leaf is required")
    result = []
    for prefix in itertools.product(range(4), repeat=number_of_leaves - 1):
        total = 0
        for character in prefix:
            total ^= character
        result.append(tuple(prefix) + (total,))
    return tuple(result)


JC_FOUR_LEAF_REPRESENTATIVES: Tuple[Assignment, ...] = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)


def reticulations(arcs: Sequence[Arc]) -> Tuple[str, ...]:
    incoming: Dict[str, int] = {}
    outgoing: Dict[str, int] = {}
    for tail, head in arcs:
        incoming[head] = incoming.get(head, 0) + 1
        incoming.setdefault(tail, 0)
        outgoing[tail] = outgoing.get(tail, 0) + 1
        outgoing.setdefault(head, 0)
    return tuple(sorted(v for v in incoming if (incoming[v], outgoing[v]) == (2, 1)))


def displayed_trees(
    arcs: Sequence[Arc], leaf_labels: Mapping[str, int]
) -> Tuple[Tuple[str, ...], Tuple[Tuple[Tuple[int, ...], Tuple[int, ...], Dict[int, Tuple[int, ...]]], ...]]:
    retics = reticulations(arcs)
    incoming_indices = {
        retic: tuple(index for index, (_tail, head) in enumerate(arcs) if head == retic)
        for retic in retics
    }
    if any(len(indices) != 2 for indices in incoming_indices.values()):
        raise ValueError("every reticulation must have exactly two incoming arcs")
    trees = []
    for choices in itertools.product((0, 1), repeat=len(retics)):
        excluded = {
            incoming_indices[retic][1 - choice]
            for retic, choice in zip(retics, choices)
        }
        selected = tuple(index for index in range(len(arcs)) if index not in excluded)
        children: Dict[str, List[str]] = {}
        for index in selected:
            tail, head = arcs[index]
            children.setdefault(tail, []).append(head)
        cache: Dict[str, Tuple[int, ...]] = {}

        def descendants(vertex: str) -> Tuple[int, ...]:
            if vertex in cache:
                return cache[vertex]
            if vertex in leaf_labels:
                answer = (leaf_labels[vertex],)
            else:
                answer = tuple(sorted(
                    leaf
                    for child in children.get(vertex, ())
                    for leaf in descendants(child)
                ))
            cache[vertex] = answer
            return answer

        edge_descendants = {index: descendants(arcs[index][1]) for index in selected}
        trees.append((tuple(choices), selected, edge_descendants))
    return retics, tuple(trees)


def edge_multiplier(model: str, parameter, character: int):
    if character == 0:
        return 1
    model = model.upper()
    if model == "JC":
        return parameter
    if model == "K2P":
        singleton, pair = parameter
        return singleton if character == 1 else pair
    if model == "K3P":
        return parameter[character - 1]
    raise ValueError(model)


def evaluate(
    arcs: Sequence[Arc],
    leaf_labels: Mapping[str, int],
    assignments: Sequence[Assignment],
    edge_parameters: Sequence[object],
    inheritance_parameters: Mapping[str, object],
    model: str = "JC",
) -> Tuple[object, ...]:
    if len(edge_parameters) != len(arcs):
        raise ValueError("one edge parameter tuple is required per arc")
    retics, trees = displayed_trees(arcs, leaf_labels)
    if set(inheritance_parameters) != set(retics):
        raise ValueError("inheritance keys do not match reticulations")
    outputs = []
    number_of_leaves = len(leaf_labels)
    for assignment in assignments:
        if len(assignment) != number_of_leaves:
            raise ValueError("assignment length does not match leaves")
        total_character = 0
        for character in assignment:
            total_character ^= character
        if total_character:
            outputs.append(0)
            continue
        by_label = {label: assignment[label - 1] for label in range(1, number_of_leaves + 1)}
        coordinate = 0
        for choices, selected, descendants in trees:
            term = 1
            for retic, choice in zip(retics, choices):
                inheritance = inheritance_parameters[retic]
                term = term * (inheritance if choice == 0 else 1 - inheritance)
            for edge_index in selected:
                character = 0
                for label in descendants[edge_index]:
                    character ^= by_label[label]
                term = term * edge_multiplier(model, edge_parameters[edge_index], character)
            coordinate = coordinate + term
        outputs.append(coordinate)
    return tuple(outputs)


@dataclass(frozen=True)
class Dual:
    value: Fraction
    gradient: Tuple[Fraction, ...]

    @staticmethod
    def constant(value, size: int) -> "Dual":
        return Dual(Fraction(value), (Fraction(0),) * size)

    def _coerce(self, other) -> "Dual":
        if isinstance(other, Dual):
            if len(other.gradient) != len(self.gradient):
                raise ValueError("dual dimensions differ")
            return other
        return Dual.constant(other, len(self.gradient))

    def __add__(self, other):
        other = self._coerce(other)
        return Dual(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        return Dual(
            self.value * other.value,
            tuple(self.value * b + other.value * a for a, b in zip(self.gradient, other.gradient)),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._coerce(other)
        if other.value == 0:
            raise ZeroDivisionError
        denominator = other.value * other.value
        return Dual(
            self.value / other.value,
            tuple((a * other.value - self.value * b) / denominator
                  for a, b in zip(self.gradient, other.gradient)),
        )

    def __rtruediv__(self, other):
        return self._coerce(other) / self


def dual_variables(values: Sequence[Fraction]) -> Tuple[Dual, ...]:
    size = len(values)
    result = []
    for index, value in enumerate(values):
        gradient = [Fraction(0)] * size
        gradient[index] = Fraction(1)
        result.append(Dual(Fraction(value), tuple(gradient)))
    return tuple(result)


def determinant(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    if not matrix:
        return Fraction(1)
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a square matrix")
    work = [[Fraction(entry) for entry in row] for row in matrix]
    answer = Fraction(1)
    for column in range(size):
        pivot_row = next((row for row in range(column, size) if work[row][column]), None)
        if pivot_row is None:
            return Fraction(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            answer = -answer
        pivot = work[column][column]
        answer *= pivot
        for row in range(column + 1, size):
            if work[row][column] == 0:
                continue
            factor = work[row][column] / pivot
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return answer


def matrix_rank(matrix: Sequence[Sequence[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(entry) for entry in row] for row in matrix]
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        selected = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b for a, b in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row
