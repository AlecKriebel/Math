#!/usr/bin/env python3
"""Sign-symmetry block SOS search for the flat-kernel quartic.

The quartic has a 14-dimensional group of coordinate sign symmetries.
Averaging any SOS Gram matrix over that group splits it into character
blocks.  This gives blocks of size at most 24, in contrast to the much
larger unrestricted Gram problem.  Numerical output remains discovery
only until rationally reconstructed and independently verified.
"""

from __future__ import annotations

from collections import defaultdict
import importlib.util
import itertools
import os
from pathlib import Path

import cvxpy as cp
import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_n3_boundary_quartic_sos.py"
SPEC = importlib.util.spec_from_file_location("quartic_source", SOURCE)
quartic_source = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quartic_source)


def gf2_span_basis(rows: list[int]) -> dict[int, int]:
    basis: dict[int, int] = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
                continue
            basis[pivot] = value
            for other_pivot, other in tuple(basis.items()):
                if other_pivot != pivot and ((other >> pivot) & 1):
                    basis[other_pivot] = other ^ value
            break
    return basis


def quotient_representative(value: int, basis: dict[int, int]) -> int:
    for pivot in sorted(basis, reverse=True):
        if (value >> pivot) & 1:
            value ^= basis[pivot]
    return value


def main() -> None:
    if os.environ.get("N3_QUARTIC_EFFECTIVE"):
        effective_source = HERE / "build_n3_boundary_effective_quartic.py"
        effective_spec = importlib.util.spec_from_file_location(
            "effective_quartic", effective_source
        )
        effective_module = importlib.util.module_from_spec(effective_spec)
        assert effective_spec.loader is not None
        effective_spec.loader.exec_module(effective_module)
        _, _, _, effective = effective_module.build()
        dimension = 55
        terms = {}
        for monomial, coefficient in effective.items():
            exponent = [0] * dimension
            for index in monomial:
                exponent[index] += 1
            terms[tuple(exponent)] = coefficient
    else:
        variables, polynomial = quartic_source.build_quartic()
        dimension = len(variables)
        terms = dict(polynomial.terms())

    parity_rows = []
    for exponent in terms:
        parity_rows.append(
            sum(1 << index for index, power in enumerate(exponent) if power & 1)
        )
    parity_basis = gf2_span_basis(parity_rows)
    print(
        "coordinate sign-symmetry dimension",
        dimension - len(parity_basis),
    )

    active = []
    for index in range(dimension):
        exponent = [0] * dimension
        exponent[index] = 4
        if terms.get(tuple(exponent), 0):
            active.append(index)
    active_set = set(active)

    # Exact zero-diagonal elimination for a hypothetical PSD Gram matrix.
    monomials = [(index, index) for index in active]
    for first, second in itertools.combinations(range(dimension), 2):
        exponent = [0] * dimension
        exponent[first] = exponent[second] = 2
        coefficient = terms.get(tuple(exponent), 0)
        if coefficient or (
            first in active_set and second in active_set
        ):
            monomials.append((first, second))
    monomials.sort()

    blocks_by_character: defaultdict[int, list[int]] = defaultdict(list)
    for number, (first, second) in enumerate(monomials):
        parity = 0 if first == second else (1 << first) ^ (1 << second)
        character = quotient_representative(parity, parity_basis)
        blocks_by_character[character].append(number)
    blocks = list(blocks_by_character.values())
    print(
        "Gram monomials",
        len(monomials),
        "character blocks",
        len(blocks),
        "largest",
        max(map(len, blocks)),
    )

    grams = [
        cp.Variable((len(block), len(block)), symmetric=True)
        for block in blocks
    ]
    use_dsos = bool(os.environ.get("N3_QUARTIC_DSOS"))
    if use_dsos:
        constraints = []
        for gram in grams:
            for row in range(gram.shape[0]):
                constraints.append(
                    gram[row, row]
                    >= cp.sum(
                        cp.abs(
                            cp.hstack(
                                [
                                    gram[row, column]
                                    for column in range(gram.shape[0])
                                    if column != row
                                ]
                            )
                        )
                    )
                    if gram.shape[0] > 1
                    else gram[row, row] >= 0
                )
    else:
        constraints = [gram >> 0 for gram in grams]
    coefficient_expressions = defaultdict(lambda: 0)
    for block_number, block in enumerate(blocks):
        for local_first, global_first in enumerate(block):
            for local_second in range(local_first, len(block)):
                global_second = block[local_second]
                exponent = [0] * dimension
                for index in monomials[global_first]:
                    exponent[index] += 1
                for index in monomials[global_second]:
                    exponent[index] += 1
                multiplier = 1 if local_first == local_second else 2
                coefficient_expressions[tuple(exponent)] += (
                    multiplier
                    * grams[block_number][local_first, local_second]
                )

    all_exponents = set(coefficient_expressions) | set(terms)
    for exponent in all_exponents:
        constraints.append(
            coefficient_expressions[exponent]
            == float(terms.get(exponent, 0))
        )
    logdet_ridge = os.environ.get("N3_QUARTIC_LOGDET_RIDGE")
    if logdet_ridge:
        ridge = float(logdet_ridge)
        objective = cp.Maximize(
            sum(
                cp.log_det(gram + ridge * np.eye(gram.shape[0]))
                for gram in grams
            )
        )
    elif os.environ.get("N3_QUARTIC_MIN_FROBENIUS"):
        objective = cp.Minimize(
            sum(cp.sum_squares(gram) for gram in grams)
        )
    else:
        objective = cp.Minimize(sum(cp.trace(gram) for gram in grams))
    problem = cp.Problem(objective, constraints)
    solver = os.environ.get("N3_QUARTIC_SOS_SOLVER", "CLARABEL")
    options = {"verbose": bool(os.environ.get("N3_QUARTIC_SOS_VERBOSE"))}
    if solver == "CLARABEL":
        options.update(
            {
                "tol_gap_abs": 1e-10,
                "tol_feas": 1e-10,
                "tol_gap_rel": 1e-10,
                "max_iter": 1000,
            }
        )
    problem.solve(solver=solver, **options)
    print(
        "status",
        problem.status,
        "trace",
        problem.value,
        "DSOS",
        use_dsos,
    )
    if not all(gram.value is not None for gram in grams):
        return
    eigenvalues = [np.linalg.eigvalsh(gram.value) for gram in grams]
    print(
        "smallest eigenvalues",
        sorted(float(values[0]) for values in eigenvalues)[:30],
    )
    output = os.environ.get(
        "N3_QUARTIC_SYMMETRY_GRAM_OUTPUT",
        "/tmp/n3_boundary_quartic_symmetry_grams.npz",
    )
    np.savez_compressed(
        output,
        monomials=np.asarray(monomials, dtype=np.int16),
        blocks=np.asarray(blocks, dtype=object),
        **{
            f"gram_{number}": gram.value
            for number, gram in enumerate(grams)
        },
    )


if __name__ == "__main__":
    main()
