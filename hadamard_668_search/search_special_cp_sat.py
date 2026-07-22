#!/usr/bin/env python3
"""CP-SAT search for an exact special Golay quadruple at length 167.

For Eliahou's fixed q=(83,2,81,1), write

    X = s[0:83],  Y = s[85:166],  u=s[84],  v=s[166].

The 83 nontrivial fixed-q equations reduce to

    c_k(X)+c_k(Y)=0       (1 <= k <= 80),
    x_0*x_81+x_1*x_82=0  (k=81),
    x_0*x_82+u*v=0        (k=82).

The isolated coordinate s[83] is absent.  Evaluating the resulting Laurent
identity at +1 modulo 8 forces x_0*x_82=-1, u*v=+1, and the ordinary sums of
X and Y to have absolute value 9.  Evaluation at -1 likewise forces both
alternating sums to have absolute value 9.  Sign and reversal symmetries let us
impose sum(X)=sum(Y)=9, x_0=u=v=+1, x_82=-1.  We do *not* also fix y_0:
once the sign of sum(Y) is fixed, a class whose two endpoints are both -1 has
no equivalent representative with y_0=+1.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ortools.sat.python import cp_model

from seed import (
    ELIAHOU_Q,
    ELIAHOU_S,
    assemble_reduced_blocks,
    reduced_blocks,
    special_quadruple,
    summed_aperiodic_correlations,
)


def equality_literal(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    equal = model.new_bool_var(name)
    model.add(left == right).only_enforce_if(equal)
    model.add(left != right).only_enforce_if(equal.negated())
    return equal


def add_alternating_sum(
    model: cp_model.CpModel,
    bits: list[cp_model.IntVar],
    target: int,
    name: str,
) -> None:
    # If signs are 2*bit-1 and len(bits) is odd, the alternating sum is
    # 2*(sum_even(bit)-sum_odd(bit))-1.
    difference = model.new_int_var(-len(bits), len(bits), name)
    model.add(
        difference
        == sum(bits[0::2]) - sum(bits[1::2])
    )
    model.add(2 * difference - 1 == target)


def residue_sign_sums(
    model: cp_model.CpModel,
    bits: list[cp_model.IntVar],
    modulus: int,
    name: str,
) -> list[cp_model.IntVar]:
    """Sign sums in each coordinate class modulo ``modulus``."""

    result = []
    for residue in range(modulus):
        selected = bits[residue::modulus]
        value = model.new_int_var(-len(selected), len(selected), f"{name}_{residue}")
        model.add(value == 2 * sum(selected) - len(selected))
        result.append(value)
    return result


def square(
    model: cp_model.CpModel, value: cp_model.IntVar, bound: int, name: str
) -> cp_model.IntVar:
    result = model.new_int_var(0, bound * bound, name)
    model.add_multiplication_equality(result, [value, value])
    return result


def product(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    bound: int,
    name: str,
) -> cp_model.IntVar:
    result = model.new_int_var(-bound * bound, bound * bound, name)
    model.add_multiplication_equality(result, [left, right])
    return result


def add_small_root_spectral_invariants(
    model: cp_model.CpModel,
    x: list[cp_model.IntVar],
    y: list[cp_model.IntVar],
) -> None:
    """Add exact consequences at primitive 3rd, 4th, and 6th roots.

    The Laurent identity is

        |X(z)|^2 + |Y(z)|^2 = 164 - z^82 - z^-82.

    Reducing the two polynomials in the quadratic cyclotomic rings gives
    small integer norm equations.  They are redundant logically, but expose
    global propagation that is otherwise hidden behind thousands of pairwise
    equality literals.
    """

    # z^2+z+1=0; norm(a+b*z)=a^2-a*b+b^2; right side 165.
    norms_3 = []
    for label, bits in (("x", x), ("y", y)):
        residues = residue_sign_sums(model, bits, 3, f"{label}_mod3")
        a = model.new_int_var(-len(bits), len(bits), f"{label}_z3_a")
        b = model.new_int_var(-len(bits), len(bits), f"{label}_z3_b")
        model.add(a == residues[0] - residues[2])
        model.add(b == residues[1] - residues[2])
        norms_3.extend(
            (
                square(model, a, len(bits), f"{label}_z3_a2"),
                square(model, b, len(bits), f"{label}_z3_b2"),
                -product(model, a, b, len(bits), f"{label}_z3_ab"),
            )
        )
    model.add(sum(norms_3) == 165)

    # z=i; norm=(r0-r2)^2+(r1-r3)^2; right side 166.
    norms_4 = []
    for label, bits in (("x", x), ("y", y)):
        residues = residue_sign_sums(model, bits, 4, f"{label}_mod4")
        real = model.new_int_var(-len(bits), len(bits), f"{label}_z4_real")
        imag = model.new_int_var(-len(bits), len(bits), f"{label}_z4_imag")
        model.add(real == residues[0] - residues[2])
        model.add(imag == residues[1] - residues[3])
        norms_4.extend(
            (
                square(model, real, len(bits), f"{label}_z4_real2"),
                square(model, imag, len(bits), f"{label}_z4_imag2"),
            )
        )
    model.add(sum(norms_4) == 166)

    # z^2-z+1=0; norm(a+b*z)=a^2+a*b+b^2; right side 165.
    norms_6 = []
    for label, bits in (("x", x), ("y", y)):
        residues = residue_sign_sums(model, bits, 6, f"{label}_mod6")
        a = model.new_int_var(-len(bits), len(bits), f"{label}_z6_a")
        b = model.new_int_var(-len(bits), len(bits), f"{label}_z6_b")
        model.add(a == residues[0] - residues[2] - residues[3] + residues[5])
        model.add(b == residues[1] + residues[2] - residues[4] - residues[5])
        norms_6.extend(
            (
                square(model, a, len(bits), f"{label}_z6_a2"),
                square(model, b, len(bits), f"{label}_z6_b2"),
                product(model, a, b, len(bits), f"{label}_z6_ab"),
            )
        )
    model.add(sum(norms_6) == 165)


def add_lexicographic_greater_or_equal(
    model: cp_model.CpModel,
    left: list[cp_model.IntVar],
    right: list[cp_model.IntVar],
    name: str,
) -> None:
    """Break an involutive symmetry by imposing ``left >=lex right``."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    prefix_equal = model.new_bool_var(f"{name}_prefix_0")
    model.add(prefix_equal == 1)
    for index, (left_bit, right_bit) in enumerate(zip(left, right, strict=True)):
        model.add(left_bit >= right_bit).only_enforce_if(prefix_equal)
        if index + 1 == len(left):
            break
        equal = equality_literal(model, left_bit, right_bit, f"{name}_eq_{index}")
        next_prefix = model.new_bool_var(f"{name}_prefix_{index + 1}")
        model.add(next_prefix <= prefix_equal)
        model.add(next_prefix <= equal)
        model.add(next_prefix >= prefix_equal + equal - 1)
        prefix_equal = next_prefix


def build_model(minimize_distance: bool) -> tuple[
    cp_model.CpModel,
    list[cp_model.IntVar],
    list[cp_model.IntVar],
]:
    model = cp_model.CpModel()
    x = [model.new_bool_var(f"x_{index}") for index in range(83)]
    y = [model.new_bool_var(f"y_{index}") for index in range(81)]

    # Exact correlation constraints: a product is +1 exactly when its two
    # Boolean sign variables agree.
    for lag in range(1, 81):
        equalities = [
            equality_literal(model, x[i], x[i + lag], f"xx_{lag}_{i}")
            for i in range(83 - lag)
        ]
        equalities.extend(
            equality_literal(model, y[i], y[i + lag], f"yy_{lag}_{i}")
            for i in range(81 - lag)
        )
        model.add(sum(equalities) == len(equalities) // 2)

    lag_81 = [
        equality_literal(model, x[0], x[81], "xx_81_0"),
        equality_literal(model, x[1], x[82], "xx_81_1"),
    ]
    model.add(sum(lag_81) == 1)

    # Necessary endpoint and spectral invariants, with global sign symmetries.
    model.add(x[0] == 1)
    model.add(x[82] == 0)
    model.add(sum(x) == 46)  # sign sum 2*46-83 = 9
    model.add(sum(y) == 45)  # sign sum 2*45-81 = 9
    # Parity fixes the signs after ordinary sums are normalized.  X has 42
    # even-index and 41 odd-index terms, so alt(X)=+9 would give an impossible
    # odd sign sum on a block of even size.  For Y the opposite sign is ruled
    # out by its 41/40 split.
    add_alternating_sum(model, x, -9, "x_alternating_half_sum")
    add_alternating_sum(model, y, 9, "y_alternating_half_sum")
    add_small_root_spectral_invariants(model, x, y)

    # X is equivalent to its negated reversal after endpoint normalization;
    # Y is equivalent to its reversal after its sum has been normalized.
    add_lexicographic_greater_or_equal(
        model, x, [bit.negated() for bit in reversed(x)], "x_neg_reverse"
    )
    add_lexicographic_greater_or_equal(model, y, list(reversed(y)), "y_reverse")

    # Hints use the published modular seed, normalized to positive Y sum by
    # its independent global sign symmetry.
    seed_x, seed_y, _, _ = reduced_blocks(ELIAHOU_S)
    normalized_seed_y = tuple(-value for value in seed_y) if sum(seed_y) < 0 else seed_y
    for variable, value in zip(x, seed_x, strict=True):
        model.add_hint(variable, int(value == 1))
    for variable, value in zip(y, normalized_seed_y, strict=True):
        model.add_hint(variable, int(value == 1))

    if minimize_distance:
        disagreements = []
        for variable, value in zip(x, seed_x, strict=True):
            disagreements.append(variable.negated() if value == 1 else variable)
        for variable, value in zip(y, normalized_seed_y, strict=True):
            disagreements.append(variable.negated() if value == 1 else variable)
        model.minimize(sum(disagreements))

    return model, x, y


def signs(solver: cp_model.CpSolver, variables: list[cp_model.IntVar]) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def save_solution(path: Path, x: tuple[int, ...], y: tuple[int, ...]) -> None:
    # The forced lag-82 invariant has u*v=+1.  Choose both endpoints and the
    # completely isolated coordinate canonically as +1.
    s = assemble_reduced_blocks(x, y, u=1, v=1, isolated=1)
    quadruple = special_quadruple(s, ELIAHOU_Q)
    correlations = summed_aperiodic_correlations(quadruple)
    if any(correlations[1:]):
        raise AssertionError("solver output failed exact aperiodic verification")
    payload = {
        "kind": "exact-special-golay-quadruple",
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
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="CP-SAT memory cap in MiB (conservative default for a 16 GiB host)",
    )
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--log-search-progress", action="store_true")
    parser.add_argument("--minimize-distance", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/special_golay_167.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers <= 0 or args.max_memory_mb <= 0:
        raise SystemExit("--workers and --max-memory-mb must be positive")
    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    model, x_variables, y_variables = build_model(args.minimize_distance)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = args.log_search_progress
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        x = signs(solver, x_variables)
        y = signs(solver, y_variables)
        save_solution(args.output, x, y)
        print(f"solution={args.output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
