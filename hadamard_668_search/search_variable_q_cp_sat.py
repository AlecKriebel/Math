#!/usr/bin/env python3
"""Sharded exact CP-SAT search for a variable-q special Golay quadruple.

The model searches for a base sequence ``BS(84,83)``.  Every solution maps
bijectively to ``(s,s',sq,(sq)')`` at length 167 and hence to a Hadamard
matrix of order 668.  Evaluations of the base-sequence norm identity at
``z=1`` and ``z=-1`` divide the exhaustive search into 288 nominal margin
shards after safe sign, swap, and reversal normalizations.  Global coordinate
alternation reduces these to 156 search representatives.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from seed import ELIAHOU_Q, ELIAHOU_S, special_quadruple, summed_aperiodic_correlations
from variable_q_base import (
    ALTERNATION_FIXED_SHARDS,
    LONG,
    MARGIN_SHARDS,
    SHORT,
    base_correlations,
    base_to_special,
    alternating_sum,
    canonical_alternated_margins,
    sign_sum,
    special_to_base,
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


def add_lexicographic_greater_or_equal(
    model: cp_model.CpModel,
    left: list[cp_model.IntVar],
    right: list[cp_model.IntVar],
    name: str,
) -> None:
    """Impose ``left >=lex right`` using a linear-size prefix encoding."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    prefix = model.new_bool_var(f"{name}_prefix_0")
    model.add(prefix == 1)
    for index, (lhs, rhs) in enumerate(zip(left, right, strict=True)):
        model.add(lhs >= rhs).only_enforce_if(prefix)
        if index + 1 == len(left):
            break
        equal = equality_literal(model, lhs, rhs, f"{name}_equal_{index}")
        next_prefix = model.new_bool_var(f"{name}_prefix_{index + 1}")
        model.add(next_prefix <= prefix)
        model.add(next_prefix <= equal)
        model.add(next_prefix >= prefix + equal - 1)
        prefix = next_prefix


def add_sign_sum(model: cp_model.CpModel, bits: list[cp_model.IntVar], target: int) -> None:
    model.add(2 * sum(bits) - len(bits) == target)


def add_alternating_sum(
    model: cp_model.CpModel, bits: list[cp_model.IntVar], target: int
) -> None:
    model.add(
        2 * (sum(bits[0::2]) - sum(bits[1::2]))
        - (len(bits[0::2]) - len(bits[1::2]))
        == target
    )


def canonical_alternation_literal_image(
    sequences: tuple[list[cp_model.IntVar], ...],
    ordinary: tuple[int, int, int, int],
    alternating: tuple[int, int, int, int],
) -> tuple[list[cp_model.IntVar], ...]:
    """Return the globally alternated image in the canonical margin chamber.

    Coordinate alternation sends a sign ``x_i`` to ``(-1)^i x_i`` and swaps
    its ordinary and alternating sums.  The static negations, even-length
    reversals, and equal-length swaps below are precisely those used by
    :func:`variable_q_base.canonical_alternated_margins`.
    """

    images: list[list[cp_model.IntVar]] = []
    new_ordinary = list(alternating)
    new_alternating = list(ordinary)
    for sequence_index, bits in enumerate(sequences):
        negate_sequence = new_ordinary[sequence_index] < 0
        image = [
            bit.negated()
            if bool(position % 2) != negate_sequence
            else bit
            for position, bit in enumerate(bits)
        ]
        if negate_sequence:
            new_ordinary[sequence_index] = -new_ordinary[sequence_index]
            new_alternating[sequence_index] = -new_alternating[sequence_index]
        images.append(image)
    for sequence_index in (0, 1):
        if new_alternating[sequence_index] < 0:
            images[sequence_index].reverse()
            new_alternating[sequence_index] = -new_alternating[sequence_index]
    for left, right in ((0, 1), (2, 3)):
        if new_ordinary[left] < new_ordinary[right]:
            images[left], images[right] = images[right], images[left]
            new_ordinary[left], new_ordinary[right] = (
                new_ordinary[right],
                new_ordinary[left],
            )
            new_alternating[left], new_alternating[right] = (
                new_alternating[right],
                new_alternating[left],
            )
    expected = canonical_alternated_margins(ordinary, alternating)
    if (tuple(new_ordinary), tuple(new_alternating)) != expected:
        raise AssertionError("literal alternation margin mismatch")
    return tuple(images)


def residue_sign_sums(
    model: cp_model.CpModel,
    bits: list[cp_model.IntVar],
    modulus: int,
    name: str,
    *,
    coordinate_alternation: bool = False,
) -> list[cp_model.IntVar]:
    result = []
    for residue in range(modulus):
        positions = tuple(range(residue, len(bits), modulus))
        selected = [bits[index] for index in positions]
        value = model.new_int_var(-len(selected), len(selected), f"{name}_{residue}")
        if coordinate_alternation:
            model.add(
                value
                == sum(
                    (1 if index % 2 == 0 else -1) * (2 * bits[index] - 1)
                    for index in positions
                )
            )
        else:
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
    sequences: tuple[list[cp_model.IntVar], ...],
) -> None:
    """Expose the norm identity at primitive 3rd, 4th, and 6th roots."""

    labels = "abcd"

    # z^2+z+1=0 and norm(a+b*z)=a^2-a*b+b^2.
    norm_3 = []
    for label, bits in zip(labels, sequences, strict=True):
        residues = residue_sign_sums(model, bits, 3, f"{label}_mod3")
        a = model.new_int_var(-len(bits), len(bits), f"{label}_z3_a")
        b = model.new_int_var(-len(bits), len(bits), f"{label}_z3_b")
        model.add(a == residues[0] - residues[2])
        model.add(b == residues[1] - residues[2])
        norm_3.extend(
            (
                square(model, a, len(bits), f"{label}_z3_a2"),
                square(model, b, len(bits), f"{label}_z3_b2"),
                -product(model, a, b, len(bits), f"{label}_z3_ab"),
            )
        )
    model.add(sum(norm_3) == 2 * (LONG + SHORT))

    # z=i and norm(real+i*imag)=real^2+imag^2.
    norm_4 = []
    for label, bits in zip(labels, sequences, strict=True):
        residues = residue_sign_sums(model, bits, 4, f"{label}_mod4")
        real = model.new_int_var(-len(bits), len(bits), f"{label}_z4_real")
        imag = model.new_int_var(-len(bits), len(bits), f"{label}_z4_imag")
        model.add(real == residues[0] - residues[2])
        model.add(imag == residues[1] - residues[3])
        norm_4.extend(
            (
                square(model, real, len(bits), f"{label}_z4_real2"),
                square(model, imag, len(bits), f"{label}_z4_imag2"),
            )
        )
    model.add(sum(norm_4) == 2 * (LONG + SHORT))

    # z^2-z+1=0 and norm(a+b*z)=a^2+a*b+b^2.
    norm_6 = []
    for label, bits in zip(labels, sequences, strict=True):
        residues = residue_sign_sums(model, bits, 6, f"{label}_mod6")
        a = model.new_int_var(-len(bits), len(bits), f"{label}_z6_a")
        b = model.new_int_var(-len(bits), len(bits), f"{label}_z6_b")
        model.add(a == residues[0] - residues[2] - residues[3] + residues[5])
        model.add(b == residues[1] + residues[2] - residues[4] - residues[5])
        norm_6.extend(
            (
                square(model, a, len(bits), f"{label}_z6_a2"),
                square(model, b, len(bits), f"{label}_z6_b2"),
                product(model, a, b, len(bits), f"{label}_z6_ab"),
            )
        )
    model.add(sum(norm_6) == 2 * (LONG + SHORT))


def add_primitive_eighth_root_invariants(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
) -> None:
    """Expose both coefficients of the norm identity over ``Q(sqrt(2))``.

    At ``z=exp(pi*i/4)``, write the eight residue sums as ``c_0,...,c_7`` and
    set

        x=c_0-c_4, y=c_2-c_6, alpha=c_1-c_5, beta=c_3-c_7.

    The squared norm is

        x^2+y^2+alpha^2+beta^2
        + sqrt(2)*(alpha*(x+y)+beta*(y-x)).

    Its rational coefficient must be 334 and its irrational coefficient zero.
    These equations are redundant with the full lag model but give a compact,
    strong propagator; they also underlie the dependency-free distance-33
    obstruction in ``variable_q_root8.py``.
    """

    rational_terms = []
    irrational_terms = []
    for label, bits in zip("abcd", sequences, strict=True):
        residues = residue_sign_sums(model, bits, 8, f"{label}_mod8")
        coordinates = []
        for name, left, right in (
            ("x", 0, 4),
            ("y", 2, 6),
            ("alpha", 1, 5),
            ("beta", 3, 7),
        ):
            coordinate = model.new_int_var(
                -len(bits), len(bits), f"{label}_z8_{name}"
            )
            model.add(coordinate == residues[left] - residues[right])
            coordinates.append(coordinate)
            rational_terms.append(
                square(
                    model,
                    coordinate,
                    len(bits),
                    f"{label}_z8_{name}2",
                )
            )
        x, y, alpha, beta = coordinates
        irrational_terms.extend(
            (
                product(model, alpha, x, len(bits), f"{label}_z8_alpha_x"),
                product(model, alpha, y, len(bits), f"{label}_z8_alpha_y"),
                product(model, beta, y, len(bits), f"{label}_z8_beta_y"),
                -product(model, beta, x, len(bits), f"{label}_z8_beta_x"),
            )
        )
    model.add(sum(rational_terms) == 2 * (LONG + SHORT))
    model.add(sum(irrational_terms) == 0)


def add_length_seven_compression_invariants(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    *,
    coordinate_alternation: bool = False,
) -> None:
    """Add the exact factor-12 periodic compression at length seven.

    The length-83 sequences are implicitly padded by a trailing zero.  Since
    that zero is index 83, it belongs to residue six modulo seven and does not
    change the residue sum.  The four compressed PAFs must total
    ``(334, 0, 0, 0)`` at the independent lags zero through three.

    These equations follow from the full aperiodic equations.  The ordinary
    form exposes primitive-seventh-root propagation.  With
    ``coordinate_alternation=True``, every source sign is first multiplied by
    ``(-1)^i``; this exposes the equally necessary primitive-fourteenth-root
    constraints because coordinate alternation sends ``R_k`` to
    ``(-1)^k R_k``.
    """

    prefix = "mod7_alt" if coordinate_alternation else "mod7"
    compressed = tuple(
        residue_sign_sums(
            model,
            bits,
            7,
            f"{label}_{prefix}",
            coordinate_alternation=coordinate_alternation,
        )
        for label, bits in zip("abcd", sequences, strict=True)
    )
    paf_name = "compressed7_alt" if coordinate_alternation else "compressed7"
    for lag, target in enumerate((2 * (LONG + SHORT), 0, 0, 0)):
        terms = []
        for label, cells in zip("abcd", compressed, strict=True):
            terms.extend(
                product(
                    model,
                    cells[index],
                    cells[(index + lag) % 7],
                    12,
                    f"{label}_{paf_name}_paf_{lag}_{index}",
                )
                for index in range(7)
            )
        model.add(sum(terms) == target)


def add_endpoint_product_parities(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
) -> None:
    """Add the telescoped parity consequence of consecutive lag equations.

    The product of all correlation terms is -1 at each positive lag and +1
    at lag zero.  Dividing the products at lags k+1 and k leaves only the two
    endpoints of each sequence's overlap.
    """

    for lag in range(LONG - 1):
        positions = (
            (0, lag),
            (0, LONG - 1 - lag),
            (1, lag),
            (1, LONG - 1 - lag),
            (2, lag),
            (2, SHORT - 1 - lag),
            (3, lag),
            (3, SHORT - 1 - lag),
        )
        # A central coordinate occurs twice and cancels from the sign product.
        active: set[tuple[int, int]] = set()
        for position in positions:
            if position in active:
                active.remove(position)
            else:
                active.add(position)
        literals = [sequences[which][index] for which, index in sorted(active)]
        # Every surviving product has even arity, so in the encoding +1->True
        # its sign is (-1)^(number of true literals).  Only lag zero is -1.
        parity = int(lag == 0)
        if parity:
            model.add_bool_xor(literals)
        else:
            # AddBoolXOr requires odd parity; complementing one literal turns
            # the desired even parity into that native form.
            model.add_bool_xor([literals[0].negated(), *literals[1:]])


def add_quad_product_parities(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
) -> None:
    """Add an equivalent, sparser basis for the 83 endpoint XORs.

    Write ``alpha_j`` for the product of the four entries in paired endpoint
    quad ``j`` of ``A,B`` and ``beta_j`` for the corresponding product of
    ``C,D``.  The endpoint equations are equivalent to

        alpha = (-1,+1,...,+1),    beta = (+1,...,+1).

    This is also the standard quad-parity theorem for ``BS(n+1,n)``.  Each
    row below has four literals instead of up to eight.
    """

    a, b, c, d = sequences

    def add_product(literals: list[cp_model.IntVar], negative: bool) -> None:
        # Four +1-as-true literals have negative sign product exactly at odd
        # Boolean parity.  CP-SAT's native XOR enforces odd parity.
        if negative:
            model.add_bool_xor(literals)
        else:
            model.add_bool_xor([literals[0].negated(), *literals[1:]])

    for index in range(LONG // 2):
        add_product(
            [
                a[index],
                a[LONG - 1 - index],
                b[index],
                b[LONG - 1 - index],
            ],
            negative=index == 0,
        )
    for index in range(SHORT // 2):
        add_product(
            [
                c[index],
                c[SHORT - 1 - index],
                d[index],
                d[SHORT - 1 - index],
            ],
            negative=False,
        )


def build_model(
    shard_index: int,
    hint: tuple[tuple[int, ...], ...] | None = None,
    compression_7: bool = False,
    compression_7_alternating: bool = False,
    parity_basis: str = "quad",
    max_hint_distance: int | None = None,
    symmetry_breaking: bool = True,
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    if parity_basis not in {"quad", "endpoint", "both"}:
        raise ValueError("parity_basis must be quad, endpoint, or both")
    if max_hint_distance is not None and max_hint_distance < 0:
        raise ValueError("max_hint_distance must be nonnegative")
    if max_hint_distance is not None and hint is None:
        raise ValueError("max_hint_distance requires a same-shard hint")
    ordinary, alternating = MARGIN_SHARDS[shard_index]
    model = cp_model.CpModel()
    lengths = (LONG, LONG, SHORT, SHORT)
    labels = "abcd"
    sequences = tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(length)]
        for label, length in zip(labels, lengths, strict=True)
    )

    # A product of signs is +1 precisely when its Boolean bits agree.  At
    # every positive lag the total number of product terms is even, so zero
    # correlation is equivalent to exactly half the equality literals true.
    for lag in range(1, LONG):
        terms = []
        for label, bits in zip(labels, sequences, strict=True):
            terms.extend(
                equality_literal(model, bits[index], bits[index + lag], f"{label}{label}_{lag}_{index}")
                for index in range(len(bits) - lag)
            )
        if len(terms) % 2:
            raise AssertionError("base correlation has an odd term count")
        model.add(sum(terms) == len(terms) // 2)

    for bits, row_sum, alt_sum in zip(
        sequences, ordinary, alternating, strict=True
    ):
        add_sign_sum(model, bits, row_sum)
        add_alternating_sum(model, bits, alt_sum)

    add_small_root_spectral_invariants(model, sequences)
    add_primitive_eighth_root_invariants(model, sequences)
    if compression_7:
        add_length_seven_compression_invariants(model, sequences)
    if compression_7_alternating:
        add_length_seven_compression_invariants(
            model, sequences, coordinate_alternation=True
        )
    if parity_basis in {"quad", "both"}:
        add_quad_product_parities(model, sequences)
    if parity_basis in {"endpoint", "both"}:
        add_endpoint_product_parities(model, sequences)

    if symmetry_breaking:
        # Odd-length reversal preserves both selected margins.  Even-length
        # reversal negates the alternating margin and is already used to make
        # it nonnegative; it remains a symmetry only when that margin is zero.
        for label, bits, alt_sum in zip(
            labels, sequences, alternating, strict=True
        ):
            if len(bits) % 2 or alt_sum == 0:
                add_lexicographic_greater_or_equal(
                    model, bits, list(reversed(bits)), f"{label}_reverse"
                )

        # For an even sequence with zero ordinary sum, negated reversal
        # preserves both its ordinary and alternating margins (for every
        # alternating sum).
        for label, bits, row_sum in zip(
            labels[:2], sequences[:2], ordinary[:2], strict=True
        ):
            if row_sum == 0:
                add_lexicographic_greater_or_equal(
                    model,
                    bits,
                    [bit.negated() for bit in reversed(bits)],
                    f"{label}_negated_reverse",
                )

        # When both margins of an even sequence vanish, independent negation
        # is still available after the margin normalization.
        for bits, row_sum, alt_sum in zip(
            sequences[:2], ordinary[:2], alternating[:2], strict=True
        ):
            if row_sum == 0 and alt_sum == 0:
                model.add(bits[0] == 1)

        # Global alternation pairs 264 margin shards.  The scheduler searches
        # only the lower-index member of each pair.  On the 24 fixed shards
        # the same involution remains internal, so retain only its
        # lexicographically larger sequence quadruple.
        if shard_index in ALTERNATION_FIXED_SHARDS:
            alternated = canonical_alternation_literal_image(
                sequences, ordinary, alternating
            )
            add_lexicographic_greater_or_equal(
                model,
                [literal for sequence in sequences for literal in sequence],
                [literal for sequence in alternated for literal in sequence],
                "global_alternation",
            )

    # A local-search checkpoint in this exact shard is the strongest phase
    # hint.  Otherwise retain the published modular seed: it does not respect
    # these margins, but has only 13 nonzero base-correlation lags.
    seed_sequences = hint or special_to_base(ELIAHOU_S, ELIAHOU_Q)
    for variables, seed in zip(sequences, seed_sequences, strict=True):
        for variable, value in zip(variables, seed, strict=True):
            model.add_hint(variable, int(value == 1))

    if max_hint_distance is not None:
        differences = [
            variable.negated() if value == 1 else variable
            for variables, seed in zip(sequences, seed_sequences, strict=True)
            for variable, value in zip(variables, seed, strict=True)
        ]
        model.add(sum(differences) <= max_hint_distance).with_name(
            "maximum_hint_hamming_distance"
        )

    return model, sequences


def load_hint(
    path: Path, shard_index: int
) -> tuple[tuple[int, ...], ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("hint JSON must contain an object")
    lengths = (LONG, LONG, SHORT, SHORT)
    sequences: list[tuple[int, ...]] = []
    for label, length in zip("abcd", lengths, strict=True):
        raw = payload.get(label)
        if not isinstance(raw, list) or len(raw) != length:
            raise ValueError(f"hint field {label} must contain {length} signs")
        sequence = tuple(raw)
        if any(type(value) is not int or value not in (-1, 1) for value in sequence):
            raise ValueError(f"hint field {label} is not a sign sequence")
        sequences.append(sequence)

    ordinary, alternating = MARGIN_SHARDS[shard_index]
    if tuple(sign_sum(sequence) for sequence in sequences) != ordinary:
        raise ValueError("hint ordinary sums do not match the selected shard")
    if tuple(alternating_sum(sequence) for sequence in sequences) != alternating:
        raise ValueError("hint alternating sums do not match the selected shard")
    return tuple(sequences)


def signs(solver: cp_model.CpSolver, variables: list[cp_model.IntVar]) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def save_solution(
    path: Path,
    shard_index: int,
    sequences: tuple[tuple[int, ...], ...],
) -> None:
    if any(base_correlations(*sequences)[1:]):
        raise AssertionError("solver candidate failed base-sequence verification")
    s, q = base_to_special(*sequences)
    special_correlations = summed_aperiodic_correlations(special_quadruple(s, q))
    if any(special_correlations[1:]):
        raise AssertionError("solver candidate failed special-quadruple verification")
    matrix = goethals_seidel(special_quadruple(s, q))
    verify_hadamard(matrix)
    ordinary, alternating = MARGIN_SHARDS[shard_index]
    payload = {
        "kind": "exact-variable-q-special-golay-quadruple",
        "length": 167,
        "hadamard_order": 668,
        "hadamard_construction": "Goethals-Seidel",
        "hadamard_verified": True,
        "base_lengths": [LONG, LONG, SHORT, SHORT],
        "shard": shard_index,
        "ordinary_sums": list(ordinary),
        "alternating_sums": list(alternating),
        "a": list(sequences[0]),
        "b": list(sequences[1]),
        "c": list(sequences[2]),
        "d": list(sequences[3]),
        "s": list(s),
        "q": list(q),
        "base_correlations": list(base_correlations(*sequences)),
        "special_correlations": list(special_correlations),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", type=int, default=0, help="margin shard, 0..287")
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="CP-SAT memory cap in MiB (conservative default for a 16 GiB host)",
    )
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--log-search-progress", action="store_true")
    parser.add_argument("--hint", type=Path, help="same-shard a,b,c,d JSON hint")
    parser.add_argument(
        "--hint-distance",
        type=int,
        help="search only within this Hamming radius of --hint",
    )
    parser.add_argument("--list-shards", action="store_true")
    parser.add_argument("--model-stats", action="store_true")
    parser.add_argument(
        "--compression-7",
        action="store_true",
        help="add the exact factor-12 compressed-length-7 PAF equations",
    )
    parser.add_argument(
        "--compression-7-alternating",
        action="store_true",
        help=(
            "add the coordinate-alternated length-7 PAF equations, exposing "
            "primitive-14th-root propagation"
        ),
    )
    parser.add_argument(
        "--parity-basis",
        choices=("quad", "endpoint", "both"),
        default="quad",
        help="equivalent XOR basis; quad uses the sparsest four-literal rows",
    )
    parser.add_argument(
        "--no-symmetry-breaking",
        action="store_true",
        help=(
            "disable all lex/bit symmetry quotients; required when proving an "
            "unquotiented same-shard Hamming-ball result"
        ),
    )
    parser.add_argument(
        "--output", type=Path, default=Path("output/variable_q_special_golay_167.json")
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_shards:
        for index, (ordinary, alternating) in enumerate(MARGIN_SHARDS):
            print(f"{index:3d} ordinary={ordinary} alternating={alternating}")
        return 0
    if not 0 <= args.shard < len(MARGIN_SHARDS):
        raise SystemExit(f"--shard must be in 0..{len(MARGIN_SHARDS) - 1}")
    if args.workers <= 0 or args.max_memory_mb <= 0:
        raise SystemExit("--workers and --max-memory-mb must be positive")

    ordinary, alternating = MARGIN_SHARDS[args.shard]
    print(f"shard={args.shard} ordinary={ordinary} alternating={alternating}")
    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    try:
        hint = load_hint(args.hint, args.shard) if args.hint else None
        model, variables = build_model(
            args.shard,
            hint=hint,
            compression_7=args.compression_7,
            compression_7_alternating=args.compression_7_alternating,
            parity_basis=args.parity_basis,
            max_hint_distance=args.hint_distance,
            symmetry_breaking=not args.no_symmetry_breaking,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2
    if args.model_stats:
        print(model.model_stats())
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
        sequences = tuple(signs(solver, sequence) for sequence in variables)
        save_solution(args.output, args.shard, sequences)
        print(f"wrote={args.output}")
        return 0
    return 2 if status == cp_model.INFEASIBLE else 1


if __name__ == "__main__":
    raise SystemExit(main())
