#!/usr/bin/env python3
"""Exact mod-4 adjacency lift for a semiregular C37 conference core.

For a 333-vertex conference graph with adjacency matrix A,

    A^2 + A = 83 (I + J).

The binary C37 block variables below impose this identity modulo four,
fixed integral orbit sums, and the universal 6/3 diagonal trace law.  In
the equivalent sign-core formulation this is the conference equation
modulo 16.  The model is a necessary condition for an exact H(668), not
the exact integer construction problem.

Eight independent shifts of the nine C37 fibers act by rotating the eight
root blocks A[0,j].  Each of those nonconstant words is constrained to be
the lexicographically least of its 37 rotations, removing the full 37^8
gauge exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ortools.sat.python import cp_model


P = 37
N = 9


QUOTIENTS = {
    1: [
        [16, 18, 18, 18, 22, 22, 22, 13, 17],
        [18, 16, 18, 18, 22, 22, 13, 22, 17],
        [18, 18, 16, 18, 22, 13, 22, 22, 17],
        [18, 18, 18, 16, 13, 22, 22, 22, 17],
        [22, 22, 22, 13, 18, 17, 17, 17, 18],
        [22, 22, 13, 22, 17, 18, 17, 17, 18],
        [22, 13, 22, 22, 17, 17, 18, 17, 18],
        [13, 22, 22, 22, 17, 17, 17, 18, 18],
        [17, 17, 17, 17, 18, 18, 18, 18, 26],
    ],
    2: [
        [24, 20, 20, 20, 18, 18, 16, 15, 15],
        [20, 22, 14, 14, 19, 19, 17, 22, 19],
        [20, 14, 18, 17, 24, 15, 19, 18, 21],
        [20, 14, 17, 18, 15, 24, 19, 18, 21],
        [18, 19, 24, 15, 14, 16, 21, 20, 19],
        [18, 19, 15, 24, 16, 14, 21, 20, 19],
        [16, 17, 19, 19, 21, 21, 20, 21, 12],
        [15, 22, 18, 18, 20, 20, 21, 12, 20],
        [15, 19, 21, 21, 19, 19, 12, 20, 20],
    ],
}


def quadratic_residues() -> set[int]:
    return {value * value % P for value in range(1, P)}


def verify_quotient(quotient: list[list[int]]) -> None:
    assert len(quotient) == N
    assert all(len(row) == N for row in quotient)
    assert quotient == [list(row) for row in zip(*quotient)]
    assert all(sum(row) == 166 for row in quotient)
    for i in range(N):
        assert quotient[i][i] % 2 == 0
        for j in range(N):
            square = sum(
                quotient[i][k] * quotient[k][j] for k in range(N)
            )
            target = 83 * (1 if i == j else 0) + 83 * P
            assert square + quotient[i][j] == target


@dataclass
class VariableGeometry:
    model: cp_model.CpModel
    variables: list[cp_model.IntVar]
    ids: dict[tuple[int, int, int], int]

    @classmethod
    def build(cls, model: cp_model.CpModel) -> "VariableGeometry":
        variables: list[cp_model.IntVar] = []
        ids: dict[tuple[int, int, int], int] = {}
        for i in range(N):
            for j in range(i, N):
                lags: Iterable[int]
                if i == j:
                    lags = range(1, (P + 1) // 2)
                else:
                    lags = range(P)
                for lag in lags:
                    ids[(i, j, lag)] = len(variables)
                    variables.append(
                        model.new_bool_var(f"a_{i}_{j}_{lag}")
                    )
        assert len(variables) == 1494
        return cls(model=model, variables=variables, ids=ids)

    def variable_id(self, i: int, j: int, lag: int) -> int | None:
        lag %= P
        if i == j:
            if lag == 0:
                return None
            return self.ids[(i, i, min(lag, P - lag))]
        if i < j:
            return self.ids[(i, j, lag)]
        return self.ids[(j, i, (-lag) % P)]

    def variable(
        self, i: int, j: int, lag: int
    ) -> cp_model.IntVar | int:
        identifier = self.variable_id(i, j, lag)
        return 0 if identifier is None else self.variables[identifier]

    def block(self, i: int, j: int) -> list[cp_model.IntVar | int]:
        return [self.variable(i, j, lag) for lag in range(P)]


def add_binary_equality(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    equal = model.new_bool_var(name)
    model.add(left == right).only_enforce_if(equal)
    model.add(left != right).only_enforce_if(equal.negated())
    return equal


def add_lex_rotation_leader(
    model: cp_model.CpModel,
    word: list[cp_model.IntVar],
    rotation: int,
    prefix: str,
) -> None:
    """Impose word <=lex rotate(word, rotation)."""

    equal_prefix: cp_model.IntVar | None = None
    for position in range(P):
        left = word[position]
        right = word[(position + rotation) % P]
        # A violation is an equal prefix followed by 1 > 0.
        if equal_prefix is None:
            model.add_bool_or([left.negated(), right])
        else:
            model.add_bool_or(
                [equal_prefix.negated(), left.negated(), right]
            )
        if position == P - 1:
            break
        same = add_binary_equality(
            model, left, right, f"{prefix}_same_{position}"
        )
        if equal_prefix is None:
            equal_prefix = same
        else:
            next_prefix = model.new_bool_var(
                f"{prefix}_prefix_{position + 1}"
            )
            model.add_bool_and([equal_prefix, same]).only_enforce_if(
                next_prefix
            )
            model.add_bool_or(
                [equal_prefix.negated(), same.negated(), next_prefix]
            )
            model.add_implication(next_prefix, equal_prefix)
            model.add_implication(next_prefix, same)
            equal_prefix = next_prefix


def add_fiber_shift_gauge(
    model: cp_model.CpModel, geometry: VariableGeometry
) -> None:
    for fiber in range(1, N):
        word = geometry.block(0, fiber)
        assert all(not isinstance(entry, int) for entry in word)
        typed_word = [entry for entry in word if not isinstance(entry, int)]
        assert len(typed_word) == P
        for rotation in range(1, P):
            add_lex_rotation_leader(
                model,
                typed_word,
                rotation,
                f"gauge_{fiber}_{rotation}",
            )


def add_margins_and_trace(
    model: cp_model.CpModel,
    geometry: VariableGeometry,
    quotient: list[list[int]],
) -> None:
    for i in range(N):
        for j in range(i, N):
            model.add(sum(geometry.block(i, j)) == quotient[i][j])

    residues = quadratic_residues()
    for lag in range(1, P):
        target = 6 if lag in residues else 3
        model.add(
            sum(geometry.variable(i, i, lag) for i in range(N))
            == target
        )


class ProductCache:
    def __init__(
        self, model: cp_model.CpModel, variables: list[cp_model.IntVar]
    ) -> None:
        self.model = model
        self.variables = variables
        self.products: dict[tuple[int, int], cp_model.IntVar] = {}

    def term(self, left: int, right: int) -> cp_model.IntVar:
        if left == right:
            return self.variables[left]
        key = (min(left, right), max(left, right))
        product = self.products.get(key)
        if product is not None:
            return product
        product = self.model.new_bool_var(f"p_{key[0]}_{key[1]}")
        self.model.add_multiplication_equality(
            product, [self.variables[key[0]], self.variables[key[1]]]
        )
        self.products[key] = product
        return product


def add_mod4_equations(
    model: cp_model.CpModel,
    geometry: VariableGeometry,
    products: ProductCache,
    modulus: int,
) -> tuple[int, int]:
    true_literal = model.new_bool_var("constant_true_for_xor")
    model.add(true_literal == 1)
    equation_count = 0
    term_count = 0
    for i in range(N):
        for j in range(i, N):
            lags: Iterable[int]
            if i == j:
                lags = range((P + 1) // 2)
            else:
                lags = range(P)
            for lag in lags:
                multiplicities: Counter[
                    tuple[str, int] | tuple[str, int, int]
                ] = Counter()
                for middle in range(N):
                    for source in range(P):
                        left = geometry.variable_id(i, middle, source)
                        right = geometry.variable_id(
                            middle, j, lag - source
                        )
                        if left is None or right is None:
                            continue
                        if left == right:
                            multiplicities[("v", left)] += 1
                        else:
                            multiplicities[
                                ("p", min(left, right), max(left, right))
                            ] += 1

                terms: list[cp_model.LinearExpr] = []
                parity_literals: list[cp_model.IntVar] = []
                for key, coefficient in multiplicities.items():
                    coefficient %= 4
                    if coefficient == 0:
                        continue
                    if key[0] == "v":
                        term = geometry.variables[key[1]]
                    else:
                        term = products.term(key[1], key[2])
                    terms.append(coefficient * term)
                    if coefficient & 1:
                        parity_literals.append(term)
                edge = geometry.variable(i, j, lag)
                if not isinstance(edge, int):
                    terms.append(edge)
                    parity_literals.append(edge)
                target = 83 * (
                    1 + (1 if i == j and lag == 0 else 0)
                )
                if target % 2 == 0:
                    parity_literals.append(true_literal)
                model.add_bool_xor(parity_literals)
                if modulus == 4:
                    quotient_variable = model.new_int_var(
                        -42, 63, f"q_{i}_{j}_{lag}"
                    )
                    model.add(
                        sum(terms) - target == 4 * quotient_variable
                    )
                equation_count += 1
                term_count += len(terms)
    assert equation_count == 1503
    return equation_count, term_count


def extract_words(
    solver: cp_model.CpSolver, geometry: VariableGeometry
) -> list[list[int]]:
    words = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            value = 0
            for lag in range(P):
                variable = geometry.variable(i, j, lag)
                bit = 0 if isinstance(variable, int) else solver.value(variable)
                value |= bit << lag
            words[i][j] = value
    return words


def load_hint(path: Path) -> list[list[int]]:
    text = path.read_text()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        words = [[0] * N for _ in range(N)]
        seen: set[tuple[int, int]] = set()
        for line in text.splitlines():
            fields = line.split()
            if len(fields) < 4 or fields[0] != "block":
                continue
            i, j = int(fields[1]), int(fields[2])
            word = int(fields[3], 16)
            reverse = word & 1
            for lag in range(1, P):
                reverse |= ((word >> lag) & 1) << (P - lag)
            words[i][j] = word
            words[j][i] = reverse
            seen.add((i, j))
        if len(seen) != N * (N + 1) // 2:
            raise ValueError(
                "text hint must contain all 45 upper block records"
            )
        return words
    encoded = payload.get("word_hex", payload.get("words"))
    if not isinstance(encoded, list) or len(encoded) != N:
        raise ValueError("hint must contain a 9x9 word_hex matrix")
    words: list[list[int]] = []
    for row in encoded:
        if not isinstance(row, list) or len(row) != N:
            raise ValueError("hint must contain a 9x9 word_hex matrix")
        words.append(
            [
                int(value, 16) if isinstance(value, str) else int(value)
                for value in row
            ]
        )
    return words


def rotate_coefficients(word: int, amount: int) -> int:
    """Return new[t] = old[t+amount] on Z/37."""

    amount %= P
    result = 0
    for lag in range(P):
        result |= ((word >> ((lag + amount) % P)) & 1) << lag
    return result


def canonicalize_fiber_gauge(words: list[list[int]]) -> list[list[int]]:
    shifts = [0] * N
    for fiber in range(1, N):
        shifts[fiber] = min(
            range(P),
            key=lambda shift: tuple(
                (words[0][fiber] >> ((lag + shift) % P)) & 1
                for lag in range(P)
            ),
        )
    return [
        [
            rotate_coefficients(
                words[i][j], shifts[j] - shifts[i]
            )
            for j in range(N)
        ]
        for i in range(N)
    ]


def add_solution_hint(
    model: cp_model.CpModel,
    geometry: VariableGeometry,
    products: ProductCache,
    words: list[list[int]],
) -> None:
    base_values = [0] * len(geometry.variables)
    for key, identifier in geometry.ids.items():
        i, j, lag = key
        base_values[identifier] = (words[i][j] >> lag) & 1
        model.add_hint(
            geometry.variables[identifier], base_values[identifier]
        )
    for (left, right), variable in products.products.items():
        model.add_hint(variable, base_values[left] & base_values[right])


def verify_solution(
    words: list[list[int]], quotient: list[list[int]], modulus: int
) -> dict[str, object]:
    mask = (1 << P) - 1
    for i in range(N):
        for j in range(N):
            reversed_word = words[j][i] & 1
            for lag in range(1, P):
                reversed_word |= ((words[j][i] >> lag) & 1) << (P - lag)
            assert words[i][j] == reversed_word
            assert words[i][j].bit_count() == quotient[i][j]
        assert words[i][i] & 1 == 0

    residues = quadratic_residues()
    for lag in range(1, P):
        incidence = sum((words[i][i] >> lag) & 1 for i in range(N))
        assert incidence == (6 if lag in residues else 3)

    bad: list[tuple[int, int, int, int]] = []
    for i in range(N):
        for j in range(N):
            for lag in range(P):
                value = (words[i][j] >> lag) & 1
                for middle in range(N):
                    for source in range(P):
                        value += (
                            (words[i][middle] >> source)
                            & 1
                            & (
                                words[middle][j]
                                >> ((lag - source) % P)
                            )
                        )
                target = 83 * (
                    1 + (1 if i == j and lag == 0 else 0)
                )
                residue = (value - target) % modulus
                if residue:
                    bad.append((i, j, lag, residue))
    assert not bad

    payload = {
        "word_hex": [
            [f"{word:010x}" for word in row] for row in words
        ],
        "quotient": quotient,
        "trace_orientation": "QR=6,NR=3",
        "adjacency_modulus": modulus,
        "conference_core_modulus": 4 * modulus,
    }
    semantic = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["semantic_sha256"] = hashlib.sha256(semantic).hexdigest()
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quotient-type", type=int, choices=(1, 2), default=1)
    parser.add_argument("--modulus", type=int, choices=(2, 4), default=4)
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-memory-mb", type=int, default=6144)
    parser.add_argument("--random-seed", type=int, default=66833437)
    parser.add_argument("--hint-json", type=Path)
    parser.add_argument("--no-gauge", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    quotient = QUOTIENTS[args.quotient_type]
    verify_quotient(quotient)

    started = time.monotonic()
    model = cp_model.CpModel()
    geometry = VariableGeometry.build(model)
    add_margins_and_trace(model, geometry, quotient)
    if not args.no_gauge:
        add_fiber_shift_gauge(model, geometry)
    products = ProductCache(model, geometry.variables)
    equation_count, term_count = add_mod4_equations(
        model, geometry, products, args.modulus
    )
    if args.hint_json is not None:
        hint_words = load_hint(args.hint_json)
        if not args.no_gauge:
            hint_words = canonicalize_fiber_gauge(hint_words)
        # A hint must already satisfy the lower characteristic-two layer,
        # the exact margins, and the trace law.
        verify_solution(hint_words, quotient, 2)
        add_solution_hint(model, geometry, products, hint_words)
    build_seconds = time.monotonic() - started
    proto = model.proto
    print(
        "model",
        f"quotient_type={args.quotient_type}",
        f"base_bits={len(geometry.variables)}",
        f"product_bits={len(products.products)}",
        f"mod4_equations={equation_count}",
        f"adjacency_modulus={args.modulus}",
        f"mod4_terms={term_count}",
        f"proto_variables={len(proto.variables)}",
        f"proto_constraints={len(proto.constraints)}",
        f"gauge={'off' if args.no_gauge else '37^8'}",
        f"hint={'none' if args.hint_json is None else args.hint_json}",
        f"build_seconds={build_seconds:.3f}",
        f"max_rss_mb={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.1f}",
        flush=True,
    )
    if args.build_only:
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    print(
        "result",
        f"status={solver.status_name(status)}",
        f"wall_seconds={solver.wall_time:.3f}",
        f"branches={solver.num_branches}",
        f"conflicts={solver.num_conflicts}",
        f"max_rss_mb={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.1f}",
        flush=True,
    )
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        payload = verify_solution(
            extract_words(solver, geometry), quotient, args.modulus
        )
        print(json.dumps(payload, sort_keys=True, indent=2))
    elif status == cp_model.INFEASIBLE:
        print(
            "INFEASIBLE is a solver result, not an independently checked "
            "UNSAT certificate.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
