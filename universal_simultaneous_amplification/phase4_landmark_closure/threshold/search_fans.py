#!/usr/bin/env python3
"""Numerical search over exactly lumpable asymmetric weighted fans.

There is one hub and ``m`` identical two-vertex blades.  Within every blade
the A--B edge has weight ``pair``; hub--A and hub--B edges have weights
``spoke_a`` and ``spoke_b``.  A state records the hub type and counts of blade
types 10, 01, and 11.  The formulas below are direct sums of the update-rule
events.  Floating-point output is reconnaissance only.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from typing import Sequence

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "phase3_asymptotic"))
from scan_lumpable import _gauss_seidel, baseline  # noqa: E402


State = tuple[int, int, int, int]


def _gauss_seidel_keyed(
    states: Sequence[tuple[int, ...]],
    transitions: Sequence[Sequence[tuple[int, float]]],
    extinction: int,
    fixation: int,
    key,
    tolerance: float = 2e-12,
    max_iterations: int = 1_000_000,
) -> tuple[list[float], int, float]:
    values = [0.0] * len(states)
    values[fixation] = 1.0
    order = sorted(range(len(states)), key=lambda i: key(states[i]), reverse=True)
    for iteration in range(max_iterations):
        error = 0.0
        for source in order:
            if source in (extinction, fixation):
                continue
            value = sum(p * values[target] for target, p in transitions[source])
            error = max(error, abs(value - values[source]))
            values[source] = value
        if error < tolerance:
            return values, iteration + 1, error
    raise RuntimeError((error, max_iterations))


@dataclass(frozen=True)
class ThetaPathFan:
    """Two hubs joined by exchangeable internally disjoint weighted paths."""

    modules: int
    edge_weights: tuple[float, ...]  # left--0, internals, L-1--right

    @property
    def arm_length(self) -> int:
        return len(self.edge_weights) - 1

    @property
    def n(self) -> int:
        return 2 + self.modules * self.arm_length

    def states(self) -> list[tuple[int, ...]]:
        histograms = PathArmFan._histograms(self.modules, 1 << self.arm_length)
        return [(left, right, *counts) for left in (0, 1) for right in (0, 1) for counts in histograms]

    def changing_transitions(self, state: tuple[int, ...], r: float, rule: str):
        left, right, *counts_tuple = state
        counts = list(counts_tuple)
        length, m, n = self.arm_length, self.modules, self.n
        weights = self.edge_weights
        degrees = []
        for p in range(length):
            degrees.append(weights[p] + weights[p + 1])
        arm_mutants = sum(number * bin(pattern).count("1") for pattern, number in enumerate(counts))
        empty = (0, 0, m, *([0] * ((1 << length) - 1)))
        full_counts = [0] * (1 << length)
        full_counts[-1] = m
        full = (1, 1, *full_counts)
        if state in (empty, full):
            return []
        out = []

        def moved(pattern: int, position: int, mutant: bool, hubs=None):
            target = pattern | (1 << position) if mutant else pattern & ~(1 << position)
            new = counts.copy(); new[pattern] -= 1; new[target] += 1
            h0, h1 = (left, right) if hubs is None else hubs
            return (h0, h1, *new)

        if rule == "Bd":
            total = n + (r - 1.0) * (left + right + arm_mutants)
            # Hub reproductions into endpoints.
            for hub, position in ((left, 0), (right, length - 1)):
                fit = r if hub else 1.0
                for pattern, number in enumerate(counts):
                    if number and bool(pattern >> position & 1) != bool(hub):
                        out.append((moved(pattern, position, bool(hub)), number * fit / (total * m)))
            # Arm reproduction events.
            for pattern, number in enumerate(counts):
                if not number: continue
                bits = [(pattern >> p) & 1 for p in range(length)]
                if bits[0] != left:
                    fit = r if bits[0] else 1.0
                    out.append(((bits[0], right, *counts), number * fit * weights[0] / (total * degrees[0])))
                if bits[-1] != right:
                    fit = r if bits[-1] else 1.0
                    out.append(((left, bits[-1], *counts), number * fit * weights[-1] / (total * degrees[-1])))
                for parent in range(length):
                    fit = r if bits[parent] else 1.0
                    for target in (parent - 1, parent + 1):
                        if 0 <= target < length and bits[target] != bits[parent]:
                            edge = weights[max(parent, target) + 0]  # corrected below
                            # Internal p--p+1 carries weights[p+1].
                            edge = weights[min(parent, target) + 1]
                            out.append((moved(pattern, target, bool(bits[parent])), number * fit * edge / (total * degrees[parent])))
        elif rule == "dB":
            # Hub deaths; common hub-edge weights cancel.
            for which, hub, position in ((0, left, 0), (1, right, length - 1)):
                mutant_neighbors = sum(number * bool(pattern >> position & 1) for pattern, number in enumerate(counts))
                mm, rm = r * mutant_neighbors, m - mutant_neighbors
                if not hub and mm:
                    hubs = (1, right) if which == 0 else (left, 1)
                    out.append(((*hubs, *counts), mm / (n * (mm + rm))))
                elif hub and rm:
                    hubs = (0, right) if which == 0 else (left, 0)
                    out.append(((*hubs, *counts), rm / (n * (mm + rm))))
            for pattern, number in enumerate(counts):
                if not number: continue
                bits = [(pattern >> p) & 1 for p in range(length)]
                for target in range(length):
                    neighbors = []
                    if target == 0: neighbors.append((left, weights[0]))
                    else: neighbors.append((bits[target - 1], weights[target]))
                    if target == length - 1: neighbors.append((right, weights[-1]))
                    else: neighbors.append((bits[target + 1], weights[target + 1]))
                    mm = sum(r * w for kind, w in neighbors if kind)
                    rm = sum(w for kind, w in neighbors if not kind)
                    if not bits[target] and mm:
                        out.append((moved(pattern, target, True), number * mm / (n * (mm + rm))))
                    elif bits[target] and rm:
                        out.append((moved(pattern, target, False), number * rm / (n * (mm + rm))))
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def fixation(self, r: float, rule: str) -> tuple[float, int, float]:
        states = self.states(); index = {s: i for i, s in enumerate(states)}
        empty = (0, 0, self.modules, *([0] * ((1 << self.arm_length) - 1)))
        full_counts = [0] * (1 << self.arm_length); full_counts[-1] = self.modules
        full = (1, 1, *full_counts)
        rows = []
        for state in states:
            changes = self.changing_transitions(state, r, rule); mass = sum(p for _, p in changes)
            rows.append([(index[t], p / mass) for t, p in changes] if mass else [])
        def mutant_count(state):
            h0, h1, *counts = state
            return h0 + h1 + sum(bin(pattern).count("1") * number for pattern, number in enumerate(counts))
        values, iterations, residual = _gauss_seidel_keyed(states, rows, index[empty], index[full], mutant_count)
        total = values[index[(1, 0, self.modules, *([0] * ((1 << self.arm_length) - 1)))]]
        total += values[index[(0, 1, self.modules, *([0] * ((1 << self.arm_length) - 1)))]]
        for position in range(self.arm_length):
            counts = [0] * (1 << self.arm_length); counts[0] = self.modules - 1; counts[1 << position] = 1
            total += self.modules * values[index[(0, 0, *counts)]]
        return total / self.n, iterations, residual


@dataclass(frozen=True)
class PathArmFan:
    """One hub and exchangeable weighted path arms of arbitrary fixed length."""

    modules: int
    edge_weights: tuple[float, ...]  # hub--0, 0--1, ..., L-2--L-1

    @property
    def arm_length(self) -> int:
        return len(self.edge_weights)

    @property
    def n(self) -> int:
        return 1 + self.modules * self.arm_length

    @staticmethod
    def _histograms(total: int, bins: int) -> list[tuple[int, ...]]:
        answer: list[tuple[int, ...]] = []

        def rec(prefix: tuple[int, ...], remaining: int, slots: int) -> None:
            if slots == 1:
                answer.append((*prefix, remaining))
                return
            for value in range(remaining + 1):
                rec((*prefix, value), remaining - value, slots - 1)

        rec((), total, bins)
        return answer

    def states(self) -> list[tuple[int, ...]]:
        histograms = self._histograms(self.modules, 1 << self.arm_length)
        return [(h, *counts) for h in (0, 1) for counts in histograms]

    def changing_transitions(
        self, state: tuple[int, ...], r: float, rule: str
    ) -> list[tuple[tuple[int, ...], float]]:
        h, *counts_tuple = state
        counts = list(counts_tuple)
        length, m, n = self.arm_length, self.modules, self.n
        weights = self.edge_weights
        arm_degree = []
        for position in range(length):
            degree = weights[position]
            if position + 1 < length:
                degree += weights[position + 1]
            arm_degree.append(degree)
        hub_degree = m * weights[0]
        arm_mutants = sum(number * bin(pattern).count("1") for pattern, number in enumerate(counts))
        if state == (0, m, *([0] * ((1 << length) - 1))):
            return []
        full_counts = [0] * (1 << length)
        full_counts[-1] = m
        if state == (1, *full_counts):
            return []
        out: list[tuple[tuple[int, ...], float]] = []

        def moved(pattern: int, position: int, mutant: bool, hub_value: int | None = None) -> tuple[int, ...]:
            target = pattern | (1 << position) if mutant else pattern & ~(1 << position)
            new = counts.copy()
            new[pattern] -= 1
            new[target] += 1
            return (h if hub_value is None else hub_value, *new)

        if rule == "Bd":
            total = n + (r - 1.0) * (h + arm_mutants)
            # Hub reproduction into the first arm vertex.
            hub_fit = r if h else 1.0
            for pattern, number in enumerate(counts):
                if number and bool(pattern & 1) != bool(h):
                    out.append((moved(pattern, 0, bool(h)), number * hub_fit / (total * m)))
            for pattern, number in enumerate(counts):
                if not number:
                    continue
                bits = [(pattern >> position) & 1 for position in range(length)]
                # First vertex reproduction into hub.
                if bits[0] != h:
                    fit = r if bits[0] else 1.0
                    out.append(((bits[0], *counts), number * fit * weights[0] / (total * arm_degree[0])))
                # Every oriented internal edge.
                for parent in range(length):
                    fit = r if bits[parent] else 1.0
                    for target in (parent - 1, parent + 1):
                        if target < 0 or target >= length or bits[target] == bits[parent]:
                            continue
                        edge = weights[max(parent, target)]
                        out.append(
                            (
                                moved(pattern, target, bool(bits[parent])),
                                number * fit * edge / (total * arm_degree[parent]),
                            )
                        )
        elif rule == "dB":
            # Hub death.
            mutant_neighbors = sum(number * (pattern & 1 != 0) for pattern, number in enumerate(counts))
            mm = r * mutant_neighbors
            rm = m - mutant_neighbors
            if not h and mm:
                out.append(((1, *counts), mm / (n * (mm + rm))))
            elif h and rm:
                out.append(((0, *counts), rm / (n * (mm + rm))))
            # An arm vertex death in a specified pattern.
            for pattern, number in enumerate(counts):
                if not number:
                    continue
                bits = [(pattern >> position) & 1 for position in range(length)]
                for target in range(length):
                    mutant_mass = 0.0
                    resident_mass = 0.0
                    neighbors: list[tuple[int, float]] = []
                    if target == 0:
                        neighbors.append((h, weights[0]))
                    if target:
                        neighbors.append((bits[target - 1], weights[target]))
                    if target + 1 < length:
                        neighbors.append((bits[target + 1], weights[target + 1]))
                    for kind, weight in neighbors:
                        if kind:
                            mutant_mass += r * weight
                        else:
                            resident_mass += weight
                    if not bits[target] and mutant_mass:
                        out.append(
                            (
                                moved(pattern, target, True),
                                number * mutant_mass / (n * (mutant_mass + resident_mass)),
                            )
                        )
                    elif bits[target] and resident_mass:
                        out.append(
                            (
                                moved(pattern, target, False),
                                number * resident_mass / (n * (mutant_mass + resident_mass)),
                            )
                        )
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def fixation(self, r: float, rule: str) -> float:
        states = self.states()
        index = {state: k for k, state in enumerate(states)}
        empty = (0, self.modules, *([0] * ((1 << self.arm_length) - 1)))
        full_counts = [0] * (1 << self.arm_length)
        full_counts[-1] = self.modules
        full = (1, *full_counts)
        rows = []
        for state in states:
            changes = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in changes)
            rows.append([(index[target], p / mass) for target, p in changes] if mass else [])
        values, _, _ = _gauss_seidel(states, rows, index[empty], index[full])
        hub_singleton = (1, self.modules, *([0] * ((1 << self.arm_length) - 1)))
        total = values[index[hub_singleton]]
        for position in range(self.arm_length):
            counts = [0] * (1 << self.arm_length)
            counts[0] = self.modules - 1
            counts[1 << position] = 1
            total += self.modules * values[index[(0, *counts)]]
        return total / self.n


@dataclass(frozen=True)
class CompletedPairFan:
    """Weighted fan with a common weak edge between every nonpaired leaf pair."""

    modules: int
    pair: float
    background: float

    @property
    def n(self) -> int:
        return 2 * self.modules + 1

    def changing_transitions(
        self, state: tuple[int, int, int], r: float, rule: str
    ) -> list[tuple[tuple[int, int, int], float]]:
        h, mixed, mutant_pairs = state
        m, q, e, n = self.modules, self.pair, self.background, self.n
        resident_pairs = m - mixed - mutant_pairs
        mutants = mixed + 2 * mutant_pairs
        residents = 2 * m - mutants
        if state in ((0, 0, 0), (1, 0, m)):
            return []
        out: list[tuple[tuple[int, int, int], float]] = []
        if rule == "Bd":
            total = n + (r - 1.0) * (h + mutants)
            dl = 1.0 + q + (2 * m - 2) * e
            dh = 2 * m
            if not h and mutants:
                out.append(((1, mixed, mutant_pairs), r * mutants / (total * dl)))
            if h and residents:
                out.append(((0, mixed, mutant_pairs), residents / (total * dl)))
            if resident_pairs:
                up = resident_pairs * r / total * (2 * mutants * e / dl + 2 * h / dh)
                if up:
                    out.append(((h, mixed + 1, mutant_pairs), up))
            if mixed:
                up = mixed * r / total * ((q + (mutants - 1) * e) / dl + h / dh)
                down = mixed / total * ((q + (residents - 1) * e) / dl + (1 - h) / dh)
                if up:
                    out.append(((h, mixed - 1, mutant_pairs + 1), up))
                if down:
                    out.append(((h, mixed - 1, mutant_pairs), down))
            if mutant_pairs:
                down = mutant_pairs / total * (2 * residents * e / dl + 2 * (1 - h) / dh)
                if down:
                    out.append(((h, mixed + 1, mutant_pairs - 1), down))
        elif rule == "dB":
            if not h and mutants:
                out.append(((1, mixed, mutant_pairs), r * mutants / (n * (r * mutants + residents))))
            if h and residents:
                out.append(((0, mixed, mutant_pairs), residents / (n * (r * mutants + residents))))
            if resident_pairs:
                mm = r * (e * mutants + h)
                rm = q + e * (residents - 2) + 1 - h
                if mm:
                    out.append(((h, mixed + 1, mutant_pairs), 2 * resident_pairs * mm / (n * (mm + rm))))
            if mixed:
                mm_up = r * (q + e * (mutants - 1) + h)
                rm_up = e * (residents - 1) + 1 - h
                if mm_up:
                    out.append(((h, mixed - 1, mutant_pairs + 1), mixed * mm_up / (n * (mm_up + rm_up))))
                mm_down = r * (e * (mutants - 1) + h)
                rm_down = q + e * (residents - 1) + 1 - h
                if rm_down:
                    out.append(((h, mixed - 1, mutant_pairs), mixed * rm_down / (n * (mm_down + rm_down))))
            if mutant_pairs:
                mm = r * (q + e * (mutants - 2) + h)
                rm = e * residents + 1 - h
                if rm:
                    out.append(((h, mixed + 1, mutant_pairs - 1), 2 * mutant_pairs * rm / (n * (mm + rm))))
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def fixation(self, r: float, rule: str) -> float:
        states = [
            (h, mixed, mutant_pairs)
            for h in (0, 1)
            for mutant_pairs in range(self.modules + 1)
            for mixed in range(self.modules - mutant_pairs + 1)
        ]
        index = {state: k for k, state in enumerate(states)}
        rows = []
        for state in states:
            changes = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in changes)
            rows.append([(index[target], p / mass) for target, p in changes] if mass else [])
        values, _, _ = _gauss_seidel(
            states, rows, index[(0, 0, 0)], index[(1, 0, self.modules)]
        )
        return (
            values[index[(1, 0, 0)]]
            + 2 * self.modules * values[index[(0, 1, 0)]]
        ) / self.n


@dataclass(frozen=True)
class SubdividedFan:
    """One hub with exchangeable two-edge paths hub--A--B."""

    modules: int
    spoke: float

    @property
    def n(self) -> int:
        return 2 * self.modules + 1

    def changing_transitions(self, state: State, r: float, rule: str) -> list[tuple[State, float]]:
        h, a, b, c = state
        counts = [self.modules - a - b - c, b, a, c]  # module bits 00,01,10,11
        m, s, n = self.modules, self.spoke, self.n
        mutant_a = a + c
        mutant_b = b + c
        total_mutants = h + mutant_a + mutant_b
        if state in ((0, 0, 0, 0), (1, 0, 0, m)):
            return []
        out: list[tuple[State, float]] = []

        def decoded(index: int) -> tuple[int, int]:
            return divmod(index, 2)

        def moved(index: int, new_a: int, new_b: int) -> State:
            aa, bb, cc = a, b, c
            old_a, old_b = decoded(index)
            if (old_a, old_b) == (1, 0):
                aa -= 1
            elif (old_a, old_b) == (0, 1):
                bb -= 1
            elif (old_a, old_b) == (1, 1):
                cc -= 1
            if (new_a, new_b) == (1, 0):
                aa += 1
            elif (new_a, new_b) == (0, 1):
                bb += 1
            elif (new_a, new_b) == (1, 1):
                cc += 1
            return h, aa, bb, cc

        if rule == "Bd":
            total = n + (r - 1.0) * total_mutants
            if not h and mutant_a:
                out.append(((1, a, b, c), r * mutant_a * s / (total * (1 + s))))
            if h and mutant_a < m:
                out.append(((0, a, b, c), (m - mutant_a) * s / (total * (1 + s))))
            for index, number in enumerate(counts):
                if not number:
                    continue
                av, bv = decoded(index)
                if not av:
                    rate = number * r / total * (bv + h / m)
                    if rate:
                        out.append((moved(index, 1, bv), rate))
                else:
                    rate = number / total * ((1 - bv) + (1 - h) / m)
                    if rate:
                        out.append((moved(index, 0, bv), rate))
                if not bv and av:
                    out.append((moved(index, av, 1), number * r / (total * (1 + s))))
                elif bv and not av:
                    out.append((moved(index, av, 0), number / (total * (1 + s))))
        elif rule == "dB":
            if not h and mutant_a:
                out.append(((1, a, b, c), r * mutant_a / (n * (r * mutant_a + m - mutant_a))))
            if h and mutant_a < m:
                out.append(((0, a, b, c), (m - mutant_a) / (n * (r * mutant_a + m - mutant_a))))
            for index, number in enumerate(counts):
                if not number:
                    continue
                av, bv = decoded(index)
                mm = r * (bv + h * s)
                rm = (1 - bv) + (1 - h) * s
                if not av and mm:
                    out.append((moved(index, 1, bv), number * mm / (n * (mm + rm))))
                elif av and rm:
                    out.append((moved(index, 0, bv), number * rm / (n * (mm + rm))))
                if av != bv:
                    out.append((moved(index, av, av), number / n))
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def fixation(self, r: float, rule: str) -> float:
        states = [
            (h, a, b, c)
            for h in (0, 1)
            for c in range(self.modules + 1)
            for b in range(self.modules - c + 1)
            for a in range(self.modules - b - c + 1)
        ]
        index = {state: k for k, state in enumerate(states)}
        rows = []
        for state in states:
            changes = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in changes)
            rows.append([(index[target], p / mass) for target, p in changes] if mass else [])
        values, _, _ = _gauss_seidel(states, rows, index[(0, 0, 0, 0)], index[(1, 0, 0, self.modules)])
        return (
            values[index[(1, 0, 0, 0)]]
            + self.modules * values[index[(0, 1, 0, 0)]]
            + self.modules * values[index[(0, 0, 1, 0)]]
        ) / self.n


@dataclass(frozen=True)
class CliqueFan:
    """One hub and ``modules`` disjoint k-cliques joined to the hub."""

    modules: int
    blade_size: int
    internal: float

    @property
    def n(self) -> int:
        return self.modules * self.blade_size + 1

    def changing_transitions(
        self, state: tuple[int, ...], r: float, rule: str
    ) -> list[tuple[tuple[int, ...], float]]:
        h, *counts_tuple = state
        counts = list(counts_tuple)
        m, k, q = self.modules, self.blade_size, self.internal
        mutants = sum(j * counts[j] for j in range(k + 1))
        residents = m * k - mutants
        if state == (0, m, *([0] * k)) or state == (1, *([0] * k), m):
            return []
        out: list[tuple[tuple[int, ...], float]] = []

        def moved(j: int, direction: int) -> tuple[int, ...]:
            new = counts.copy()
            new[j] -= 1
            new[j + direction] += 1
            return (h, *new)

        if rule == "Bd":
            total = self.n + (r - 1.0) * (h + mutants)
            leaf_degree = 1.0 + (k - 1) * q
            hub_degree = m * k
            if not h and mutants:
                out.append(((1, *counts), r * mutants / (total * leaf_degree)))
            if h and residents:
                out.append(((0, *counts), residents / (total * leaf_degree)))
            for j, number in enumerate(counts):
                if not number:
                    continue
                if j < k:
                    up = number * r / total * (
                        j * (k - j) * q / leaf_degree
                        + h * (k - j) / hub_degree
                    )
                    if up:
                        out.append((moved(j, 1), up))
                if j:
                    down = number / total * (
                        (k - j) * j * q / leaf_degree
                        + (1 - h) * j / hub_degree
                    )
                    if down:
                        out.append((moved(j, -1), down))
        elif rule == "dB":
            n = self.n
            if not h and mutants:
                out.append(
                    ((1, *counts), r * mutants / (n * (r * mutants + residents)))
                )
            if h and residents:
                out.append(
                    ((0, *counts), residents / (n * (r * mutants + residents)))
                )
            for j, number in enumerate(counts):
                if not number:
                    continue
                if j < k:
                    mm = r * (q * j + h)
                    rm = q * (k - j - 1) + 1 - h
                    if mm:
                        out.append((moved(j, 1), number * (k - j) * mm / (n * (mm + rm))))
                if j:
                    mm = r * (q * (j - 1) + h)
                    rm = q * (k - j) + 1 - h
                    if rm:
                        out.append((moved(j, -1), number * j * rm / (n * (mm + rm))))
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def states(self) -> list[tuple[int, ...]]:
        k, m = self.blade_size, self.modules
        compositions: list[tuple[int, ...]] = []

        def rec(prefix: tuple[int, ...], remaining: int, slots: int) -> None:
            if slots == 1:
                compositions.append((*prefix, remaining))
                return
            for value in range(remaining + 1):
                rec((*prefix, value), remaining - value, slots - 1)

        rec((), m, k + 1)
        return [(h, *counts) for h in (0, 1) for counts in compositions]

    def fixation(self, r: float, rule: str) -> float:
        states = self.states()
        index = {state: i for i, state in enumerate(states)}
        rows: list[list[tuple[int, float]]] = []
        for state in states:
            changes = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in changes)
            rows.append([(index[target], p / mass) for target, p in changes] if mass else [])
        extinction = (0, self.modules, *([0] * self.blade_size))
        fixation = (1, *([0] * self.blade_size), self.modules)
        values, _, _ = _gauss_seidel(states, rows, index[extinction], index[fixation])
        hub_singleton = (1, self.modules, *([0] * self.blade_size))
        leaf_counts = [self.modules - 1, 1, *([0] * (self.blade_size - 1))]
        leaf_singleton = (0, *leaf_counts)
        return (
            values[index[hub_singleton]]
            + self.modules * self.blade_size * values[index[leaf_singleton]]
        ) / self.n


@dataclass(frozen=True)
class AsymmetricFan:
    modules: int
    pair: float
    spoke_a: float
    spoke_b: float

    @property
    def n(self) -> int:
        return 2 * self.modules + 1

    def changing_transitions(self, state: State, r: float, rule: str) -> list[tuple[State, float]]:
        h, a, b, c = state
        m = self.modules
        d = m - a - b - c
        q, x, y = self.pair, self.spoke_a, self.spoke_b
        A = a + c
        B = b + c
        RA = m - A
        RB = m - B
        if state in ((0, 0, 0, 0), (1, 0, 0, m)):
            return []
        out: list[tuple[State, float]] = []

        if rule == "Bd":
            total = self.n + (r - 1.0) * (h + A + B)
            dh = m * (x + y)
            da, db = q + x, q + y
            if not h and A + B:
                out.append(((1, a, b, c), r * (A * x / da + B * y / db) / total))
            if h and RA + RB:
                out.append(((0, a, b, c), (RA * x / da + RB * y / db) / total))

            # 00 -> 10/01, driven only by a mutant hub.
            if d and h:
                out.append(((h, a + 1, b, c), d * r * x / (total * dh)))
                out.append(((h, a, b + 1, c), d * r * y / (total * dh)))
            # 10: lose A through B/h, or gain B through A/h.
            if a:
                loss = a * ((1 - h) * x / dh + q / db) / total
                gain = a * r * (q / da + h * y / dh) / total
                if loss:
                    out.append(((h, a - 1, b, c), loss))
                out.append(((h, a - 1, b, c + 1), gain))
            # 01: lose B or gain A.
            if b:
                loss = b * ((1 - h) * y / dh + q / da) / total
                gain = b * r * (q / db + h * x / dh) / total
                if loss:
                    out.append(((h, a, b - 1, c), loss))
                out.append(((h, a, b - 1, c + 1), gain))
            # 11 can lose A/B only through a resident hub.
            if c and not h:
                out.append(((h, a, b + 1, c - 1), c * x / (total * dh)))
                out.append(((h, a + 1, b, c - 1), c * y / (total * dh)))

        elif rule == "dB":
            n = self.n
            mut_h_mass = r * (x * A + y * B)
            res_h_mass = x * RA + y * RB
            if not h and mut_h_mass:
                out.append(((1, a, b, c), mut_h_mass / (n * (mut_h_mass + res_h_mass))))
            if h and res_h_mass:
                out.append(((0, a, b, c), res_h_mass / (n * (mut_h_mass + res_h_mass))))

            def mutant_parent_probability(partner: int, hub: int, internal: float, spoke: float) -> float:
                mm = r * (internal * partner + spoke * hub)
                rm = internal * (1 - partner) + spoke * (1 - hub)
                return mm / (mm + rm) if mm else 0.0

            # 00 leaf deaths.
            if d:
                pa = mutant_parent_probability(0, h, q, x)
                pb = mutant_parent_probability(0, h, q, y)
                if pa:
                    out.append(((h, a + 1, b, c), d * pa / n))
                if pb:
                    out.append(((h, a, b + 1, c), d * pb / n))
            if a:
                # A dies and may become resident; B dies and may become mutant.
                pa = mutant_parent_probability(0, h, q, x)
                pb = mutant_parent_probability(1, h, q, y)
                if pa < 1:
                    out.append(((h, a - 1, b, c), a * (1 - pa) / n))
                if pb:
                    out.append(((h, a - 1, b, c + 1), a * pb / n))
            if b:
                pa = mutant_parent_probability(1, h, q, x)
                pb = mutant_parent_probability(0, h, q, y)
                if pb < 1:
                    out.append(((h, a, b - 1, c), b * (1 - pb) / n))
                if pa:
                    out.append(((h, a, b - 1, c + 1), b * pa / n))
            if c:
                pa = mutant_parent_probability(1, h, q, x)
                pb = mutant_parent_probability(1, h, q, y)
                if pa < 1:
                    out.append(((h, a, b + 1, c - 1), c * (1 - pa) / n))
                if pb < 1:
                    out.append(((h, a + 1, b, c - 1), c * (1 - pb) / n))
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in out if p > 0.0]

    def fixation(self, r: float, rule: str) -> float:
        states = [
            (h, a, b, c)
            for h in (0, 1)
            for c in range(self.modules + 1)
            for b in range(self.modules - c + 1)
            for a in range(self.modules - b - c + 1)
        ]
        index = {state: k for k, state in enumerate(states)}
        rows: list[list[tuple[int, float]]] = []
        for state in states:
            changes = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in changes)
            rows.append([(index[target], p / mass) for target, p in changes] if mass else [])
        values, _, _ = _gauss_seidel(
            states, rows, index[(0, 0, 0, 0)], index[(1, 0, 0, self.modules)]
        )
        return (
            values[index[(1, 0, 0, 0)]]
            + self.modules * values[index[(0, 1, 0, 0)]]
            + self.modules * values[index[(0, 0, 1, 0)]]
        ) / self.n


def scan(modules: int, r: float, values: Sequence[float]) -> None:
    records = []
    for pair, spoke_b in product(values, repeat=2):
        graph = AsymmetricFan(modules, pair, 1.0, spoke_b)
        delta = tuple(graph.fixation(r, rule) - baseline(graph.n, r, rule) for rule in ("Bd", "dB"))
        records.append((min(delta), pair, spoke_b, delta))
    for score, pair, spoke_b, delta in sorted(records, reverse=True)[:30]:
        print(
            f"score={score:+.10g} pair={pair:g} spoke_b={spoke_b:g} "
            f"Bd={delta[0]:+.10g} dB={delta[1]:+.10g}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", type=int, default=5)
    parser.add_argument("--r", type=float, default=1.1)
    args = parser.parse_args()
    m = args.modules
    values = [m * x for x in (0.05, 0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.0, 3.0)]
    scan(m, args.r, values)


if __name__ == "__main__":
    main()
