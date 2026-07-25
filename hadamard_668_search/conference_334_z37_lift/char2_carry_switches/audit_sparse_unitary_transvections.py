#!/usr/bin/env python3
"""Exact audit of the smallest C37 Hermitian transvections.

Let K=F_2[x]/Phi_37 with star x -> x^-1, and let E be the rank-four
Hermitian projection attached to a frozen support witness.  For

    u = e_a + x^s e_b,                 a < b,  s in Z/37,

we have u^*u=0.  For any fixed scalar c=bar(c),

    U = I + c u u^*

is a Hermitian unitary involution.  Thus E'=UEU is another exact
Hermitian projection.  The associated binary D'=E'+eta I automatically
satisfies the complete characteristic-two adjacency equation.

This audit exhausts all 36*37 binomial isotropic directions and the 37
small fixed scalars represented by

    1,
    x^t+x^-t,
    1+x^t+x^-t,                         1 <= t <= 18.

It then checks exact prescribed block margins, diagonal looplessness,
and every coefficient of the 6/3 diagonal trace law.  No solver or
random sampling is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


P = 37
N = 9
DEGREE = 36
FIELD_MASK = (1 << DEGREE) - 1
WORD_MASK = (1 << P) - 1


def semantic_hash(payload: dict[str, object]) -> str:
    stripped = dict(payload)
    stripped.pop("semantic_sha256", None)
    encoded = json.dumps(
        stripped, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def multiply(left: int, right: int) -> int:
    product = 0
    bits = left
    while bits:
        bit = bits & -bits
        shift = bit.bit_length() - 1
        product ^= right << shift
        bits ^= bit
    for degree in range(2 * DEGREE - 2, DEGREE - 1, -1):
        if (product >> degree) & 1:
            product ^= 1 << degree
            product ^= FIELD_MASK << (degree - DEGREE)
    return product & FIELD_MASK


def square(value: int) -> int:
    return multiply(value, value)


def star(value: int) -> int:
    result = value & 1
    if (value >> 1) & 1:
        result ^= FIELD_MASK
    for degree in range(2, DEGREE):
        if (value >> degree) & 1:
            result ^= 1 << (P - degree)
    return result


def bits_to_field(bits: int) -> int:
    result = bits & FIELD_MASK
    if (bits >> DEGREE) & 1:
        result ^= FIELD_MASK
    return result


def word_to_bits(value: int, trivial_bit: int) -> int:
    correction = trivial_bit ^ (value.bit_count() & 1)
    low = value ^ (FIELD_MASK if correction else 0)
    return low | (correction << DEGREE)


def quadratic_residue(value: int) -> bool:
    value %= P
    if value == 0:
        return False
    return pow(value, (P - 1) // 2, P) == 1


def class_indicator(residues: bool) -> int:
    bits = 0
    for value in range(1, P):
        if quadratic_residue(value) == residues:
            bits |= 1 << value
    return bits_to_field(bits)


def field_powers_x() -> list[int]:
    powers = [1]
    x = 1 << 1
    for _ in range(1, P):
        powers.append(multiply(powers[-1], x))
    assert multiply(powers[-1], x) == 1
    return powers


def matrix_multiply(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    return [
        [
            _xor_all(
                multiply(left[i][middle], right[middle][j])
                for middle in range(N)
            )
            for j in range(N)
        ]
        for i in range(N)
    ]


def _xor_all(values: object) -> int:
    result = 0
    for value in values:  # type: ignore[union-attr]
        result ^= value
    return result


def load(
    path: Path,
) -> tuple[dict[str, object], list[list[int]], list[list[int]]]:
    payload = json.loads(path.read_text())
    assert payload["schema"] == "h668-c37-char2-support-witness-v1"
    assert payload["semantic_sha256"] == semantic_hash(payload)
    encoded = payload["word_hex"]
    quotient = payload["quotient"]
    assert isinstance(encoded, list) and isinstance(quotient, list)
    words = [[int(value, 16) for value in row] for row in encoded]
    integer_quotient = [
        [int(value) for value in row] for row in quotient
    ]
    assert len(words) == len(integer_quotient) == N
    assert all(len(row) == N for row in words)
    assert all(len(row) == N for row in integer_quotient)
    return payload, words, integer_quotient


def projection_from_words(words: list[list[int]], eta: int) -> list[list[int]]:
    projection = [
        [bits_to_field(words[i][j]) for j in range(N)]
        for i in range(N)
    ]
    for i in range(N):
        projection[i][i] ^= eta
    assert all(
        projection[i][j] == star(projection[j][i])
        for i in range(N)
        for j in range(N)
    )
    assert matrix_multiply(projection, projection) == projection
    return projection


def small_fixed_scalars(x_power: list[int]) -> list[tuple[str, int]]:
    result = [("1", 1)]
    for t in range(1, (P + 1) // 2):
        pair = x_power[t] ^ x_power[P - t]
        result.append((f"pair_{t}", pair))
        result.append((f"one_plus_pair_{t}", 1 ^ pair))
    assert len(result) == P
    assert len({value for _, value in result}) == P
    assert all(value != 0 and star(value) == value for _, value in result)
    return result


def conjugate_transvection(
    projection: list[list[int]],
    first: int,
    second: int,
    shift: int,
    scalar: int,
    x_power: list[int],
) -> list[list[int]]:
    # u_first=1, u_second=x^shift, and w=E*u.
    u = {first: 1, second: x_power[shift]}
    w = [
        projection[i][first]
        ^ multiply(projection[i][second], x_power[shift])
        for i in range(N)
    ]
    h = w[first] ^ multiply(x_power[P - shift if shift else 0], w[second])
    assert star(h) == h
    scalar_squared_h = multiply(square(scalar), h)

    result = [row[:] for row in projection]
    affected = {first, second}
    for i in range(N):
        for j in range(N):
            if i not in affected and j not in affected:
                continue
            delta = 0
            if i in affected:
                delta ^= multiply(
                    multiply(scalar, u[i]), star(w[j])
                )
            if j in affected:
                delta ^= multiply(
                    multiply(scalar, w[i]), star(u[j])
                )
            if i in affected and j in affected:
                delta ^= multiply(
                    multiply(scalar_squared_h, u[i]), star(u[j])
                )
            result[i][j] ^= delta
    assert all(
        result[i][j] == star(result[j][i])
        for i in range(N)
        for j in range(N)
    )
    return result


def physical_score(
    projection: list[list[int]],
    quotient: list[list[int]],
    eta: int,
) -> tuple[tuple[int, int, int, int], dict[str, object], list[list[int]]]:
    d = [row[:] for row in projection]
    for i in range(N):
        d[i][i] ^= eta
    parity = [[quotient[i][j] & 1 for j in range(N)] for i in range(N)]
    words = [
        [word_to_bits(d[i][j], parity[i][j]) for j in range(N)]
        for i in range(N)
    ]

    bad_margins = 0
    margin_l1 = 0
    for i in range(N):
        for j in range(i, N):
            difference = words[i][j].bit_count() - quotient[i][j]
            bad_margins += difference != 0
            margin_l1 += abs(difference)

    loop_defects = sum(words[i][i] & 1 for i in range(N))
    residues = {value * value % P for value in range(1, P)}
    bad_trace_lags = 0
    trace_l1 = 0
    for lag in range(1, P):
        incidence = sum((words[i][i] >> lag) & 1 for i in range(N))
        target = 6 if lag in residues else 3
        bad_trace_lags += incidence != target
        trace_l1 += abs(incidence - target)

    score = (bad_margins + bad_trace_lags + loop_defects,
             bad_margins, bad_trace_lags, margin_l1 + trace_l1)
    report = {
        "bad_block_margins": bad_margins,
        "block_margin_l1": margin_l1,
        "diagonal_loop_defects": loop_defects,
        "bad_trace_lags": bad_trace_lags,
        "trace_l1": trace_l1,
        "exact_block_margins": bad_margins == 0,
        "exact_trace_law": bad_trace_lags == 0,
        "loopless": loop_defects == 0,
    }
    return score, report, words


def verify_mod2_words(words: list[list[int]]) -> None:
    for i in range(N):
        for j in range(N):
            value = words[i][j]
            for middle in range(N):
                left = words[i][middle]
                right = words[middle][j]
                product = 0
                bits = left
                while bits:
                    bit = bits & -bits
                    shift = bit.bit_length() - 1
                    if shift == 0:
                        product ^= right
                    else:
                        product ^= (
                            (right << shift) | (right >> (P - shift))
                        ) & WORD_MASK
                    bits ^= bit
                value ^= product
            target = WORD_MASK ^ (1 if i == j else 0)
            assert value == target


def audit(path: Path) -> dict[str, object]:
    payload, original_words, quotient = load(path)
    eta = class_indicator(False)
    x_power = field_powers_x()
    scalars = small_fixed_scalars(x_power)
    projection = projection_from_words(original_words, eta)

    total = 0
    margin_exact = 0
    trace_exact = 0
    loopless = 0
    fully_physical = 0
    best_score: tuple[int, int, int, int] | None = None
    best: dict[str, object] | None = None
    checked_projection_samples = 0
    physical_hashes: list[str] = []

    for first in range(N):
        for second in range(first + 1, N):
            for shift in range(P):
                for scalar_index, (scalar_name, scalar) in enumerate(scalars):
                    candidate = conjugate_transvection(
                        projection,
                        first,
                        second,
                        shift,
                        scalar,
                        x_power,
                    )
                    score, physical, words = physical_score(
                        candidate, quotient, eta
                    )
                    total += 1
                    margin_exact += bool(physical["exact_block_margins"])
                    trace_exact += bool(physical["exact_trace_law"])
                    loopless += bool(physical["loopless"])

                    # Re-square a deterministic transversal of the family.
                    if first == 0 and second == 1 and shift == 0:
                        assert matrix_multiply(candidate, candidate) == candidate
                        verify_mod2_words(words)
                        checked_projection_samples += 1

                    is_physical = (
                        physical["exact_block_margins"]
                        and physical["exact_trace_law"]
                        and physical["loopless"]
                    )
                    if is_physical:
                        fully_physical += 1
                        verify_mod2_words(words)
                        encoded = json.dumps(
                            [[f"{word:010x}" for word in row] for row in words],
                            separators=(",", ":"),
                        )
                        physical_hashes.append(
                            hashlib.sha256(encoded.encode()).hexdigest()
                        )

                    key = (
                        score,
                        first,
                        second,
                        shift,
                        scalar_index,
                    )
                    if best_score is None or key < (
                        best_score,
                        int(best["first_fiber"]),  # type: ignore[index]
                        int(best["second_fiber"]),  # type: ignore[index]
                        int(best["shift"]),  # type: ignore[index]
                        int(best["scalar_index"]),  # type: ignore[index]
                    ):
                        best_score = score
                        best = {
                            "first_fiber": first,
                            "second_fiber": second,
                            "shift": shift,
                            "scalar_index": scalar_index,
                            "scalar_name": scalar_name,
                            **physical,
                        }

    assert total == (N * (N - 1) // 2) * P * P
    assert checked_projection_samples == P
    assert best is not None
    return {
        "witness_file": path.name,
        "quotient_type": payload["quotient_type"],
        "semantic_sha256": payload["semantic_sha256"],
        "binomial_isotropic_directions": (
            N * (N - 1) // 2
        ) * P,
        "small_fixed_scalars": len(scalars),
        "transvections_exhausted": total,
        "exact_margin_candidates": margin_exact,
        "exact_trace_candidates": trace_exact,
        "loopless_candidates": loopless,
        "fully_physical_candidates": fully_physical,
        "best_physical_constraint_score": best,
        "physical_word_matrix_hashes": sorted(physical_hashes),
        "projection_and_mod2_transversal_checks": checked_projection_samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path, nargs="+")
    args = parser.parse_args()
    reports = [audit(path) for path in args.witness]
    encoded = json.dumps(reports, sort_keys=True, separators=(",", ":"))
    output = {
        "reports": reports,
        "semantic_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
