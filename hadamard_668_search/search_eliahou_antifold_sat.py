#!/usr/bin/env python3
"""Exact SAT feasibility search for the distance-41 anti-fold support.

This is an exploratory solver.  It requires python-sat.  Every reported SAT
support is replayed using direct integer negacyclic correlations before it is
printed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
from itertools import product
import json
from math import gcd
import multiprocessing as mp
from pathlib import Path
from queue import Empty
import time

from pysat.card import CardEnc, EncType as CardEncType
from pysat.formula import CNF, IDPool
from pysat.pb import PBEnc, EncType as PBEncType
from pysat.solvers import Solver

import verify_eliahou_adjacent42_repair as adjacent


FOLD = 42


@dataclass(frozen=True)
class PairCase:
    block: str
    index: int
    signature: tuple[int, int]
    profiles: tuple[
        tuple[tuple[int, int], tuple[int, int]],
        tuple[tuple[int, int], tuple[int, int]],
    ]


PROFILES = {
    ("L", (-2, 0)): (
        ((-3, 4), (-5, -4)),
        ((6, -5), (4, 5)),
    ),
    ("L", (0, 2)): (
        ((-4, -5), (-6, 5)),
        ((5, 4), (3, -4)),
    ),
    ("S", (0, 0)): (
        ((-4, -5), (4, 5)),
        ((5, 4), (-5, -4)),
    ),
}


def cases() -> tuple[PairCase, ...]:
    long_catalog, short_catalog = adjacent.q_pair_signature_catalogs()
    result = []
    for signature in ((-2, 0), (0, 2)):
        for index in long_catalog[signature]:
            result.append(
                PairCase("L", index, signature, PROFILES[("L", signature)])
            )
    for index in short_catalog[(0, 0)]:
        result.append(
            PairCase("S", index, (0, 0), PROFILES[("S", (0, 0))])
        )
    assert len(result) == 39
    return tuple(result)


def antifold(sequence: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sequence[index]
        - (
            sequence[index + FOLD]
            if index + FOLD < len(sequence)
            else 0
        )
        for index in range(FOLD)
    )


def seed_antifold() -> tuple[tuple[int, ...], ...]:
    return tuple(antifold(row) for row in adjacent.eliahou_base())


def q_cells(case: PairCase) -> tuple[int, int]:
    length = adjacent.LONG if case.block == "L" else adjacent.SHORT
    return case.index % FOLD, (length - 1 - case.index) % FOLD


def support_variables(
    pool: IDPool, case: PairCase
) -> tuple[dict[tuple[str, int], int], tuple[int, ...]]:
    removed = set(q_cells(case))
    variables: dict[tuple[str, int], int] = {}
    for cell in range(41):
        if case.block == "L" and cell in removed:
            continue
        variables[("L", cell)] = pool.id(f"L_{cell}")
    for cell in range(1, 40):
        if case.block == "S" and cell in removed:
            continue
        variables[("S", cell)] = pool.id(f"S_{cell}")
    return variables, tuple(variables.values())


def add_and(cnf: CNF, left: int, right: int, output: int) -> None:
    cnf.append([-output, left])
    cnf.append([-output, right])
    cnf.append([output, -left, -right])


def add_xor(cnf: CNF, left: int, right: int, output: int) -> None:
    """Encode output iff the two possibly signed literals differ."""

    cnf.append([-left, -right, -output])
    cnf.append([left, right, -output])
    cnf.append([left, -right, output])
    cnf.append([-left, right, output])


def add_parity(
    cnf: CNF, pool: IDPool, literals: list[int], parity: int, name: str
) -> None:
    if not literals:
        if parity:
            cnf.append([])
        return
    state = literals[0]
    for index, literal in enumerate(literals[1:], start=1):
        next_state = pool.id(f"{name}_xor_{index}")
        add_xor(cnf, state, literal, next_state)
        state = next_state
    cnf.append([state if parity else -state])


def add_modular_sum(
    cnf: CNF,
    pool: IDPool,
    coefficients: dict[int, int],
    constant: int,
    modulus: int,
    name: str,
) -> None:
    """Expose an implied weighted congruence as a one-hot automaton."""

    terms = [
        (variable, coefficient % modulus)
        for variable, coefficient in coefficients.items()
        if coefficient % modulus
    ]
    state = [pool.id(f"{name}_state_0_{residue}") for residue in range(modulus)]
    cnf.append([state[0]])
    for residue in range(1, modulus):
        cnf.append([-state[residue]])

    for step, (variable, coefficient) in enumerate(terms, start=1):
        next_state = [
            pool.id(f"{name}_state_{step}_{residue}")
            for residue in range(modulus)
        ]
        cnf.append(next_state)
        for left in range(modulus):
            for right in range(left + 1, modulus):
                cnf.append([-next_state[left], -next_state[right]])
        for residue in range(modulus):
            cnf.append(
                [-state[residue], variable, next_state[residue]]
            )
            cnf.append(
                [
                    -state[residue],
                    -variable,
                    next_state[(residue + coefficient) % modulus],
                ]
            )
        state = next_state

    target = (-constant) % modulus
    cnf.append([state[target]])


def retained_literal(
    row: int,
    cell: int,
    case: PairCase,
    variables: dict[tuple[str, int], int],
    seed_rows: tuple[tuple[int, ...], ...],
) -> bool | int | None:
    if seed_rows[row][cell] == 0:
        return None
    active_row = 1 if case.block == "L" else 3
    if row == active_row and cell in q_cells(case):
        return None
    block = "L" if row < 2 else "S"
    variable = variables.get((block, cell))
    if variable is None:
        return True
    return -variable


def product_literal(
    cnf: CNF,
    pool: IDPool,
    cache: dict[tuple[int, int], int],
    left: bool | int,
    right: bool | int,
) -> bool | int:
    if left is True:
        return right
    if right is True:
        return left
    if left == right:
        return left
    key = tuple(sorted((int(left), int(right))))
    if key not in cache:
        output = pool.id(f"and_{key[0]}_{key[1]}")
        add_and(cnf, int(left), int(right), output)
        cache[key] = output
    return cache[key]


def add_integer_equation(
    cnf: CNF,
    pool: IDPool,
    coefficients: dict[int, int],
    constant: int,
    parity_name: str | None = None,
    add_mod4: bool = False,
) -> None:
    common_divisor = abs(constant)
    for coefficient in coefficients.values():
        common_divisor = gcd(common_divisor, abs(coefficient))
    if common_divisor > 1:
        constant //= common_divisor
        coefficients = {
            variable: coefficient // common_divisor
            for variable, coefficient in coefficients.items()
        }

    if parity_name is not None:
        odd_variables = [
            variable
            for variable, coefficient in coefficients.items()
            if coefficient & 1
        ]
        add_parity(
            cnf,
            pool,
            odd_variables,
            constant & 1,
            parity_name,
        )
        if add_mod4:
            add_modular_sum(
                cnf,
                pool,
                coefficients,
                constant,
                4,
                f"{parity_name}_mod4",
            )

    literals = []
    weights = []
    negative_weight = 0
    for variable, coefficient in coefficients.items():
        if not coefficient:
            continue
        if coefficient > 0:
            literals.append(variable)
            weights.append(coefficient)
        else:
            literals.append(-variable)
            weights.append(-coefficient)
            negative_weight += -coefficient
    bound = -constant + negative_weight
    if not literals:
        if bound:
            cnf.append([])
        return
    encoded = PBEnc.equals(
        lits=literals,
        weights=weights,
        bound=bound,
        vpool=pool,
        encoding=PBEncType.best,
    )
    cnf.extend(encoded.clauses)


def add_antifold_equations(
    cnf: CNF,
    pool: IDPool,
    case: PairCase,
    variables: dict[tuple[str, int], int],
    modulus: int = FOLD,
    add_mod4: bool = False,
) -> None:
    if FOLD % modulus != 0 or modulus % 2:
        raise ValueError("the anti-fold modulus must be an even divisor of 42")
    seed_rows = seed_antifold()
    product_cache: dict[tuple[int, int], int] = {}
    first_lag = 1 if modulus == FOLD else 0
    for target_lag in range(first_lag, modulus // 2):
        coefficients: dict[int, int] = {}
        constant = 0
        for row, left, right in product(range(4), range(FOLD), range(FOLD)):
            quotient, exponent = divmod(left - right, modulus)
            wrap_sign = -1 if quotient % 2 else 1
            if exponent != target_lag:
                continue
            left_retained = retained_literal(
                row, left, case, variables, seed_rows
            )
            right_retained = retained_literal(
                row, right, case, variables, seed_rows
            )
            if left_retained is None or right_retained is None:
                continue
            coefficient = (
                wrap_sign * seed_rows[row][left] * seed_rows[row][right]
            )
            term = product_literal(
                cnf,
                pool,
                product_cache,
                left_retained,
                right_retained,
            )
            if term is True:
                constant += coefficient
            elif term < 0:
                constant += coefficient
                coefficients[-term] = coefficients.get(-term, 0) - coefficient
            else:
                coefficients[term] = coefficients.get(term, 0) + coefficient
        if target_lag == 0:
            constant -= 334
        add_integer_equation(
            cnf,
            pool,
            coefficients,
            constant,
            f"lag_{target_lag}_mod2",
            add_mod4,
        )


def add_profile_constraints(
    cnf: CNF,
    pool: IDPool,
    variables: dict[tuple[str, int], int],
    profile: tuple[tuple[int, int], tuple[int, int]],
) -> None:
    ordinary, alternating = profile
    targets = {
        ("L", 0): (ordinary[0] + alternating[0]) // 2,
        ("L", 1): (ordinary[0] - alternating[0]) // 2,
        ("S", 0): (ordinary[1] + alternating[1]) // 2,
        ("S", 1): (ordinary[1] - alternating[1]) // 2,
    }
    for (block, parity), target in targets.items():
        group = [
            variable
            for (variable_block, cell), variable in variables.items()
            if variable_block == block and cell % 2 == parity
        ]
        minimum = abs(target)
        cnf.extend(
            CardEnc.atleast(
                group,
                bound=minimum,
                vpool=pool,
                encoding=CardEncType.seqcounter,
            ).clauses
        )
        add_parity(
            cnf,
            pool,
            group,
            target & 1,
            f"{block}_{parity}_parity",
        )


def build(
    case: PairCase,
    profile: tuple[tuple[int, int], tuple[int, int]] | None,
    modulus: int = FOLD,
    add_mod4: bool = False,
) -> tuple[CNF, IDPool, dict[tuple[str, int], int]]:
    pool = IDPool()
    cnf = CNF()
    variables, flat = support_variables(pool, case)
    cnf.extend(
        CardEnc.equals(
            flat,
            bound=39,
            vpool=pool,
            encoding=CardEncType.totalizer,
        ).clauses
    )
    add_parity(cnf, pool, list(flat), 1, "support_weight_parity")
    if profile is not None:
        add_profile_constraints(cnf, pool, variables, profile)
    add_antifold_equations(
        cnf, pool, case, variables, modulus, add_mod4
    )
    return cnf, pool, variables


def direct_rows(
    case: PairCase,
    selected: set[tuple[str, int]],
) -> tuple[tuple[int, ...], ...]:
    rows = [list(row) for row in seed_antifold()]
    active_row = 1 if case.block == "L" else 3
    for cell in q_cells(case):
        rows[active_row][cell] = 0
    for block, cell in selected:
        first_row = 0 if block == "L" else 2
        rows[first_row][cell] = 0
        rows[first_row + 1][cell] = 0
    return tuple(tuple(row) for row in rows)


def negacyclic_correlations(
    rows: tuple[tuple[int, ...], ...]
) -> tuple[int, ...]:
    result = [0] * FOLD
    for row in rows:
        for left, right in product(range(FOLD), repeat=2):
            exponent = left - right
            wrap_sign = 1
            if exponent < 0:
                exponent += FOLD
                wrap_sign = -1
            result[exponent] += (
                wrap_sign * row[left] * row[right]
            )
    return tuple(result)


def reduce_negacyclic_coefficients(
    coefficients: tuple[int, ...], modulus: int
) -> tuple[int, ...]:
    result = [0] * modulus
    for exponent, coefficient in enumerate(coefficients):
        quotient, residue = divmod(exponent, modulus)
        result[residue] += (-1 if quotient % 2 else 1) * coefficient
    return tuple(result)


def solve_case(
    case: PairCase,
    profile: tuple[tuple[int, int], tuple[int, int]] | None,
    solver_name: str,
    with_proof: bool,
    modulus: int,
    add_mod4: bool,
) -> tuple[
    bool,
    tuple[tuple[str, int], ...] | None,
    tuple[int, int],
    CNF,
    list[str] | None,
]:
    cnf, pool, variables = build(case, profile, modulus, add_mod4)
    with Solver(
        name=solver_name,
        bootstrap_with=cnf.clauses,
        with_proof=with_proof,
    ) as solver:
        result = solver.solve()
        if not result:
            proof = solver.get_proof() if with_proof else None
            return (
                False,
                None,
                (pool.top, len(cnf.clauses)),
                cnf,
                proof,
            )
        model = set(solver.get_model())
    selected = tuple(
        key for key, variable in variables.items() if variable in model
    )
    full_correlations = negacyclic_correlations(
        direct_rows(case, set(selected))
    )
    correlations = reduce_negacyclic_coefficients(
        full_correlations, modulus
    )
    assert correlations == (334,) + (0,) * (modulus - 1)
    assert len(selected) == 39
    return True, selected, (pool.top, len(cnf.clauses)), cnf, None


def timed_solve_worker(
    messages: mp.Queue,
    case: PairCase,
    profile: tuple[tuple[int, int], tuple[int, int]] | None,
    solver_name: str,
    modulus: int,
    add_mod4: bool,
) -> None:
    """Build and solve one formula in a disposable child process."""

    try:
        cnf, pool, variables = build(case, profile, modulus, add_mod4)
        messages.put(("ready", (pool.top, len(cnf.clauses))))
        with Solver(
            name=solver_name,
            bootstrap_with=cnf.clauses,
        ) as solver:
            result = solver.solve()
            model = set(solver.get_model()) if result else set()
        selected = tuple(
            key for key, variable in variables.items() if variable in model
        )
        if result:
            full_correlations = negacyclic_correlations(
                direct_rows(case, set(selected))
            )
            correlations = reduce_negacyclic_coefficients(
                full_correlations, modulus
            )
            if correlations != (334,) + (0,) * (modulus - 1):
                raise AssertionError("solver model failed integer replay")
            if len(selected) != 39:
                raise AssertionError("solver model has wrong support weight")
        messages.put(("result", (result, selected if result else None)))
    except BaseException as error:
        messages.put(("error", repr(error)))


def solve_case_with_timeout(
    case: PairCase,
    profile: tuple[tuple[int, int], tuple[int, int]] | None,
    solver_name: str,
    modulus: int,
    add_mod4: bool,
    time_limit: float,
) -> tuple[
    bool | None,
    tuple[tuple[str, int], ...] | None,
    tuple[int, int],
]:
    """Return None after a hard per-solver wall-clock limit."""

    context = mp.get_context("spawn")
    messages = context.Queue()
    process = context.Process(
        target=timed_solve_worker,
        args=(
            messages,
            case,
            profile,
            solver_name,
            modulus,
            add_mod4,
        ),
    )
    process.start()
    first_kind, first_payload = messages.get()
    if first_kind == "error":
        process.join()
        raise RuntimeError(first_payload)
    if first_kind != "ready":
        process.terminate()
        process.join()
        raise RuntimeError(f"unexpected worker message {first_kind!r}")
    size = first_payload
    process.join(time_limit)
    if process.is_alive():
        process.terminate()
        process.join()
        messages.close()
        return None, None, size
    try:
        second_kind, second_payload = messages.get(timeout=5)
    except Empty as error:
        raise RuntimeError(
            f"solver worker exited with code {process.exitcode} "
            "without a result"
        ) from error
    finally:
        messages.close()
    if second_kind == "error":
        raise RuntimeError(second_payload)
    if second_kind != "result":
        raise RuntimeError(f"unexpected worker message {second_kind!r}")
    result, selected = second_payload
    return result, selected, size


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=78)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--modulus", type=int, choices=(2, 6, 14, 42), default=42)
    parser.add_argument(
        "--ignore-profiles",
        action="store_true",
        help="solve one support-only problem per q pair",
    )
    parser.add_argument(
        "--hensel-mod4",
        action="store_true",
        help="add redundant one-hot modulo-4 chains",
    )
    parser.add_argument(
        "--list-instances",
        action="store_true",
        help="print deterministic CNF sizes and SHA-256 hashes without solving",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        help=(
            "interrupt each solver call after this many seconds and report "
            "UNKNOWN; formula construction is not included"
        ),
    )
    return parser.parse_args()


def canonical_cnf_sha256(cnf: CNF, variable_count: int) -> str:
    digest = hashlib.sha256()
    digest.update(
        f"p cnf {variable_count} {len(cnf.clauses)}\n".encode("ascii")
    )
    for clause in cnf.clauses:
        digest.update(
            (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        )
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    if args.time_limit is not None and args.time_limit <= 0:
        raise ValueError("--time-limit must be positive")
    if args.time_limit is not None and args.proof_dir is not None:
        raise ValueError(
            "--time-limit and --proof-dir cannot be combined; interrupted "
            "proof traces are not certificates"
        )
    flat_cases = (
        [(case, -1, None) for case in cases()]
        if args.ignore_profiles
        else [
            (case, profile_index, profile)
            for case in cases()
            for profile_index, profile in enumerate(case.profiles)
        ]
    )
    total_cases = len(flat_cases)
    effective_stop = min(args.stop, total_cases)
    if not 0 <= args.start <= effective_stop <= total_cases:
        raise ValueError(
            f"require 0 <= start <= stop <= {total_cases} in this mode"
        )
    if args.list_instances:
        manifest = []
        for flat_index in range(args.start, effective_stop):
            case, profile_index, profile = flat_cases[flat_index]
            cnf, pool, _ = build(
                case, profile, args.modulus, args.hensel_mod4
            )
            manifest.append(
                {
                    "case": flat_index,
                    "block": case.block,
                    "q_index": case.index,
                    "profile": (
                        None if profile_index < 0 else profile_index
                    ),
                    "variables": pool.top,
                    "clauses": len(cnf.clauses),
                    "sha256": canonical_cnf_sha256(cnf, pool.top),
                }
            )
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return
    survivors = 0
    infeasible = 0
    unknown = 0
    started = time.monotonic()
    for flat_index in range(args.start, effective_stop):
        case, profile_index, profile = flat_cases[flat_index]
        case_started = time.monotonic()
        try:
            if args.time_limit is None:
                result, selected, size, cnf, proof = solve_case(
                    case,
                    profile,
                    args.solver,
                    args.proof_dir is not None,
                    args.modulus,
                    args.hensel_mod4,
                )
            else:
                result, selected, size = solve_case_with_timeout(
                    case,
                    profile,
                    args.solver,
                    args.modulus,
                    args.hensel_mod4,
                    args.time_limit,
                )
                cnf = None
                proof = None
        except KeyboardInterrupt:
            print(
                f"flat={flat_index}",
                case.block,
                case.index,
                case.signature,
                ("support-only" if profile_index < 0 else profile_index),
                "UNKNOWN_INTERRUPTED",
                f"seconds={time.monotonic() - case_started:.3f}",
                flush=True,
            )
            unknown += 1
            break
        survivors += result is True
        infeasible += result is False
        unknown += result is None
        if args.proof_dir is not None and result is False:
            if cnf is None:
                raise AssertionError("proof mode lost its formula")
            args.proof_dir.mkdir(parents=True, exist_ok=True)
            stem = f"antifold_{flat_index:02d}"
            cnf.to_file(args.proof_dir / f"{stem}.cnf")
            if proof is None:
                raise AssertionError("proof mode returned no proof")
            with gzip.open(
                args.proof_dir / f"{stem}.drat.gz",
                "wt",
                encoding="ascii",
            ) as proof_file:
                proof_file.write("\n".join(proof))
                proof_file.write("\n")
        print(
            f"flat={flat_index}",
            case.block,
            case.index,
            case.signature,
            ("support-only" if profile_index < 0 else profile_index),
            (
                "SAT"
                if result is True
                else "UNSAT"
                if result is False
                else "UNKNOWN_TIMEOUT"
            ),
            f"vars={size[0]}",
            f"clauses={size[1]}",
            f"modulus={args.modulus}",
            f"seconds={time.monotonic() - case_started:.3f}",
            (
                "support="
                + ",".join(f"{block}{cell}" for block, cell in selected)
                if selected
                else ""
            )
            ,
            flush=True,
        )
    print(
        f"SUMMARY range=[{args.start},{effective_stop}) "
        f"SAT={survivors} UNSAT={infeasible} UNKNOWN={unknown} "
        f"seconds={time.monotonic() - started:.3f}"
    )


if __name__ == "__main__":
    main()
