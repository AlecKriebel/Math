#!/usr/bin/env python3
"""Exact CNF/SAT encoding of the reduced fixed-q special Golay search.

This is intentionally independent of the CP-SAT model.  Pair products are
XNOR literals, every correlation equation is an exact cardinality constraint,
and the forced ordinary/alternating sums are encoded in CNF.  A candidate is
accepted only after direct integer autocorrelation verification.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from seed import (
    ELIAHOU_Q,
    ELIAHOU_S,
    assemble_reduced_blocks,
    reduced_blocks,
    special_quadruple,
    summed_aperiodic_correlations,
)


ENCODINGS = {
    "seqcounter": EncType.seqcounter,
    "sortnetwrk": EncType.sortnetwrk,
    "cardnetwrk": EncType.cardnetwrk,
    "totalizer": EncType.totalizer,
    "mtotalizer": EncType.mtotalizer,
    "kmtotalizer": EncType.kmtotalizer,
}


def add_xnor(cnf: CNF, left: int, right: int, equal: int) -> None:
    """Add ``equal <-> (left == right)`` for possibly signed literals."""

    cnf.append([-equal, -left, right])
    cnf.append([-equal, left, -right])
    cnf.append([equal, -left, -right])
    cnf.append([equal, left, right])


def add_equals(
    cnf: CNF,
    pool: IDPool,
    literals: list[int],
    bound: int,
    encoding: int,
) -> None:
    encoded = CardEnc.equals(literals, bound=bound, vpool=pool, encoding=encoding)
    cnf.extend(encoded.clauses)


def add_gated_equals(
    cnf: CNF,
    pool: IDPool,
    literals: list[int],
    bound: int,
    encoding: int,
    gate: int,
) -> None:
    """Enforce an exact cardinality only when the signed gate is true."""

    encoded = CardEnc.equals(literals, bound=bound, vpool=pool, encoding=encoding)
    cnf.extend([[-gate, *clause] for clause in encoded.clauses])


def add_lex_ge(
    cnf: CNF,
    pool: IDPool,
    left: list[int],
    right: list[int],
    name: str,
) -> None:
    """Impose ``left >=lex right`` for vectors of possibly signed literals."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    prefix = pool.id(f"{name}_prefix_0")
    cnf.append([prefix])
    for index, (left_literal, right_literal) in enumerate(
        zip(left, right, strict=True)
    ):
        # If all earlier positions agree, 0 < 1 is forbidden here.
        cnf.append([-prefix, left_literal, -right_literal])
        if index + 1 == len(left):
            break
        equal = pool.id(f"{name}_equal_{index}")
        add_xnor(cnf, left_literal, right_literal, equal)
        next_prefix = pool.id(f"{name}_prefix_{index + 1}")
        # next_prefix <-> prefix AND equal.
        cnf.append([-next_prefix, prefix])
        cnf.append([-next_prefix, equal])
        cnf.append([-prefix, -equal, next_prefix])
        prefix = next_prefix


def build_cnf(encoding: int) -> tuple[CNF, IDPool, list[int], list[int]]:
    pool = IDPool()
    cnf = CNF()
    x = [pool.id(f"x_{index}") for index in range(83)]
    y = [pool.id(f"y_{index}") for index in range(81)]

    for lag in range(1, 81):
        equalities = []
        for index in range(83 - lag):
            equal = pool.id(f"xx_{lag}_{index}")
            add_xnor(cnf, x[index], x[index + lag], equal)
            equalities.append(equal)
        for index in range(81 - lag):
            equal = pool.id(f"yy_{lag}_{index}")
            add_xnor(cnf, y[index], y[index + lag], equal)
            equalities.append(equal)
        add_equals(cnf, pool, equalities, len(equalities) // 2, encoding)

    lag_81 = []
    for index in range(2):
        equal = pool.id(f"xx_81_{index}")
        add_xnor(cnf, x[index], x[index + 81], equal)
        lag_81.append(equal)
    add_equals(cnf, pool, lag_81, 1, encoding)

    # Safe endpoint/sign normalizations and forced ordinary sums.
    cnf.append([x[0]])
    cnf.append([-x[82]])
    add_equals(cnf, pool, x, 46, encoding)
    add_equals(cnf, pool, y, 45, encoding)

    # Alternating sign sums have absolute value 9.  If a Boolean sign bit is
    # b, the alternating-sequence plus bit is b at even indices and not b at
    # odd indices.  Once the ordinary sums are +9, block-size parity forces
    # alt(X)=-9 and alt(Y)=+9, so no disjunction remains.
    for variables, forced_weight in (
        (x, 37),
        (y, 45),
    ):
        alternating = [
            variable if index % 2 == 0 else -variable
            for index, variable in enumerate(variables)
        ]
        add_equals(cnf, pool, alternating, forced_weight, encoding)

    # Safe involutive symmetry breaks.
    add_lex_ge(cnf, pool, x, [-literal for literal in reversed(x)], "x_neg_reverse")
    add_lex_ge(cnf, pool, y, list(reversed(y)), "y_reverse")
    return cnf, pool, x, y


def normalized_seed_phases(x: list[int], y: list[int]) -> list[int]:
    seed_x, seed_y, _, _ = reduced_blocks(ELIAHOU_S)
    if sum(seed_y) < 0:
        seed_y = tuple(-value for value in seed_y)
    return [
        variable if value == 1 else -variable
        for variable, value in zip(x + y, seed_x + seed_y, strict=True)
    ]


def decoded_signs(model: set[int], variables: list[int]) -> tuple[int, ...]:
    return tuple(1 if variable in model else -1 for variable in variables)


def solve_worker(
    clauses: list[list[int]],
    solver_name: str,
    phases: list[int],
    x_variables: list[int],
    y_variables: list[int],
    result_queue: multiprocessing.Queue,
) -> None:
    """Solve in a child process so a wall-clock deadline is enforceable."""

    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        solver.set_phases(phases)
        result = solver.solve()
        payload: dict[str, object] = {
            "result": result,
            "stats": solver.accum_stats(),
        }
        if result:
            model = set(solver.get_model())
            payload["x"] = decoded_signs(model, x_variables)
            payload["y"] = decoded_signs(model, y_variables)
        result_queue.put(payload)


def save_solution(path: Path, x: tuple[int, ...], y: tuple[int, ...]) -> None:
    s = assemble_reduced_blocks(x, y, u=1, v=1, isolated=1)
    correlations = summed_aperiodic_correlations(special_quadruple(s, ELIAHOU_Q))
    if any(correlations[1:]):
        raise AssertionError("SAT output failed direct aperiodic verification")
    payload = {
        "kind": "exact-special-golay-quadruple",
        "solver_family": "cnf-sat",
        "length": 167,
        "q": list(ELIAHOU_Q),
        "s": list(s),
        "x": list(x),
        "y": list(y),
        "aperiodic_correlation_sums": list(correlations),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--encoding", choices=sorted(ENCODINGS), default="totalizer")
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/special_golay_167_sat.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    cnf, pool, x_variables, y_variables = build_cnf(ENCODINGS[args.encoding])
    print(
        f"encoding={args.encoding} variables={pool.top} clauses={len(cnf.clauses)} "
        f"build_time={time.monotonic() - started:.3f}",
        flush=True,
    )
    # PySAT's in-process interrupt callback is not reliably scheduled while
    # every native solver holds the Python GIL.  A forked worker gives a real
    # wall-clock limit and shares the large immutable clause list copy-on-write.
    context = multiprocessing.get_context("fork")
    result_queue = context.Queue()
    process = context.Process(
        target=solve_worker,
        args=(
            cnf.clauses,
            args.solver,
            normalized_seed_phases(x_variables, y_variables),
            x_variables,
            y_variables,
            result_queue,
        ),
    )
    process.start()
    process.join(args.time_limit)
    if process.is_alive():
        process.terminate()
        process.join()
        print(f"status=None elapsed={time.monotonic() - started:.3f}", flush=True)
        print("stats={}", flush=True)
        return 2

    if result_queue.empty():
        raise RuntimeError(f"SAT worker exited with code {process.exitcode} without a result")
    payload = result_queue.get()
    result = payload["result"]
    print(f"status={result} elapsed={time.monotonic() - started:.3f}", flush=True)
    print(f"stats={payload['stats']}", flush=True)
    if result is True:
        x = tuple(payload["x"])
        y = tuple(payload["y"])
        save_solution(args.output, x, y)
        print(f"solution={args.output}")
        return 0
    if result is False:
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
