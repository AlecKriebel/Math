#!/usr/bin/env python3
"""Check the adjacent cyclic-fold formulation of ``BS(84,83)``.

For four binary sequences of lengths ``n+1,n+1,n,n``, let ``R[k]`` be
their summed aperiodic autocorrelation.  There are two natural cyclic
images:

* pad the short pair by a trailing zero and work modulo ``n+1``;
* fold the two endpoints of each long sequence together and work modulo
  ``n``.

The two cyclic images are complementary with energy ``4*n+2`` if and only
if every positive aperiodic residual vanishes.  The file also checks the
oriented supplementary-difference-set (OSDS) equations obtained from the
prime-83 fold and performs a small, exact quadratic-character template
scan.  It is a theorem checker and template diagnostic, not a search over
the 334 signs.
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections import defaultdict
from collections.abc import Iterable, Sequence


SignSequence = tuple[int, ...]


def aperiodic(sequence: Sequence[int], lag: int) -> int:
    return sum(
        sequence[index] * sequence[index + lag]
        for index in range(len(sequence) - lag)
    )


def periodic(sequence: Sequence[int], lag: int) -> int:
    length = len(sequence)
    return sum(
        sequence[index] * sequence[(index + lag) % length]
        for index in range(length)
    )


def residuals(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[int, ...]:
    n = len(c)
    if (len(a), len(b), len(d)) != (n + 1, n + 1, n):
        raise ValueError("expected lengths n+1,n+1,n,n")
    return tuple(
        sum(
            aperiodic(sequence, lag)
            for sequence in (a, b, c, d)
            if lag < len(sequence)
        )
        for lag in range(n + 1)
    )


def padded_fold(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Return the four length-``n+1`` vectors for the first cyclic fold."""

    return tuple(tuple(sequence) for sequence in (a, b, (*c, 0), (*d, 0)))


def endpoint_fold(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Return the four length-``n`` vectors for the adjacent cyclic fold."""

    return (
        (a[0] + a[-1], *a[1:-1]),
        (b[0] + b[-1], *b[1:-1]),
        tuple(c),
        tuple(d),
    )


def cyclic_sum(vectors: Sequence[Sequence[int]], lag: int) -> int:
    return sum(periodic(vector, lag) for vector in vectors)


def check_fold_identities(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> None:
    """Check both wrap identities coefficient by coefficient."""

    n = len(c)
    r = residuals(a, b, c, d)
    first = padded_fold(a, b, c, d)
    second = endpoint_fold(a, b, c, d)

    for lag in range(1, n + 1):
        expected = r[lag] + r[n + 1 - lag]
        actual = cyclic_sum(first, lag)
        if actual != expected:
            raise AssertionError(
                f"mod-{n + 1} fold failed at lag {lag}: {actual} != {expected}"
            )

    expected_zero = r[0] + 2 * r[n]
    actual_zero = cyclic_sum(second, 0)
    if actual_zero != expected_zero:
        raise AssertionError(
            f"mod-{n} energy fold failed: {actual_zero} != {expected_zero}"
        )
    for lag in range(1, n):
        expected = r[lag] + r[n - lag]
        actual = cyclic_sum(second, lag)
        if actual != expected:
            raise AssertionError(
                f"mod-{n} fold failed at lag {lag}: {actual} != {expected}"
            )


def dual_folds_are_exact(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> bool:
    """Return whether both cyclic folds have the target delta correlation."""

    n = len(c)
    energy = 4 * n + 2
    first = padded_fold(a, b, c, d)
    second = endpoint_fold(a, b, c, d)
    return (
        cyclic_sum(first, 0) == energy
        and all(cyclic_sum(first, lag) == 0 for lag in range(1, n + 1))
        and cyclic_sum(second, 0) == energy
        and all(cyclic_sum(second, lag) == 0 for lag in range(1, n))
    )


def is_base_sequence(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> bool:
    r = residuals(a, b, c, d)
    return r[0] == 4 * len(c) + 2 and not any(r[1:])


def difference_count(block: set[int], lag: int, modulus: int) -> int:
    return sum(1 for value in block if (value + lag) % modulus in block)


def osds_sequences(
    x: set[int],
    y: set[int],
    z: set[int],
    w: set[int],
    modulus: int = 83,
) -> tuple[tuple[int, ...], ...]:
    """Build normalized folded vectors from four negative-entry sets."""

    if 0 in x or 0 in y:
        raise ValueError("the anomalous long-fold sets must omit zero")
    u = tuple(
        0 if index == 0 else (-1 if index in x else 1)
        for index in range(modulus)
    )
    v = tuple(
        2 if index == 0 else (-1 if index in y else 1)
        for index in range(modulus)
    )
    c = tuple(-1 if index in z else 1 for index in range(modulus))
    d = tuple(-1 if index in w else 1 for index in range(modulus))
    return u, v, c, d


def check_osds_formula(
    x: set[int],
    y: set[int],
    z: set[int],
    w: set[int],
    modulus: int = 83,
) -> bool:
    """Check the exact OSDS formula against direct periodic correlation.

    The returned Boolean says whether the four folded vectors are periodic
    complementary.  Formula disagreement itself raises an exception.
    """

    vectors = osds_sequences(x, y, z, w, modulus)
    block_sum = len(x) + len(y) + len(z) + len(w)
    target = block_sum - modulus
    exact = True
    for lag in range(1, modulus):
        ex = int(lag in x) + int((-lag) % modulus in x)
        ey = int(lag in y) + int((-lag) % modulus in y)
        numerator = ex - ey
        counts = sum(
            difference_count(block, lag, modulus)
            for block in (x, y, z, w)
        )
        direct = cyclic_sum(vectors, lag)
        formula_twice = 2 * (counts - target) + numerator
        if direct != 2 * formula_twice:
            raise AssertionError(
                f"OSDS formula failed at lag {lag}: "
                f"direct={direct}, formula={2 * formula_twice}"
            )
        if numerator % 2 or counts + numerator // 2 != target:
            exact = False
    return exact


def legendre(value: int, prime: int = 83) -> int:
    value %= prime
    if value == 0:
        return 0
    return 1 if pow(value, (prime - 1) // 2, prime) == 1 else -1


def half_paf(sequence: Sequence[int]) -> tuple[int, ...]:
    modulus = len(sequence)
    return tuple(periodic(sequence, lag) for lag in range(1, modulus // 2 + 1))


def quadratic_character_scan() -> int:
    """Scan one finite prime-83 character template family exactly.

    ``U`` is the quadratic character (zero at the anomalous coordinate).
    The other binary templates are translates of

        i -> chi((i-a)^2-t),  chi(t)=-1,

    which never vanish.  ``V[0]`` is replaced by 2.  Translations do not
    change the PAFs of the two ordinary binary blocks, so a pair-signature
    join checks the whole family without a cubic Cartesian loop.
    """

    prime = 83
    u = tuple(legendre(index, prime) for index in range(prime))
    u_paf = half_paf(u)
    nonresidues = tuple(
        value for value in range(1, prime) if legendre(value, prime) == -1
    )
    binary_templates: list[tuple[int, SignSequence, tuple[int, ...]]] = []
    for parameter in nonresidues:
        sequence = tuple(
            legendre(index * index - parameter, prime)
            for index in range(prime)
        )
        if 0 in sequence:
            raise AssertionError("a nonsquare parameter produced a root")
        binary_templates.append((parameter, sequence, half_paf(sequence)))

    pair_signatures: defaultdict[tuple[int, ...], list[tuple[int, int]]]
    pair_signatures = defaultdict(list)
    for left_index, (left_parameter, _left, left_paf) in enumerate(
        binary_templates
    ):
        for right_parameter, _right, right_paf in binary_templates[left_index:]:
            signature = tuple(
                left_paf[index] + right_paf[index]
                for index in range(len(left_paf))
            )
            pair_signatures[signature].append(
                (left_parameter, right_parameter)
            )

    matches = 0
    for parameter in nonresidues:
        for shift in range(prime):
            baseline = tuple(
                legendre((index - shift) ** 2 - parameter, prime)
                for index in range(prime)
            )
            for sign in (-1, 1):
                v = (2,) + tuple(
                    sign * baseline[index]
                    for index in range(1, prime)
                )
                v_paf = half_paf(v)
                needed = tuple(
                    -u_paf[index] - v_paf[index]
                    for index in range(len(u_paf))
                )
                matches += len(pair_signatures.get(needed, ()))
    return matches


def cubic_character_scan() -> tuple[int, int, int, int, int]:
    """Scan an affine-canonical root-free cubic character family.

    Up to scaling the nonzero linear coefficient of a depressed monic cubic
    has two square classes.  Representatives ``1`` and ``2`` are used
    (``2`` is a nonsquare modulo 83).  For every root-free

        f(i) = i^3 + a*i + t,

    the binary block is ``chi(f(i))``.  All 83 translates are considered.
    The zero-anomaly block is ``chi(i)*chi(f(i-shift))`` away from zero;
    the 2-anomaly block replaces coordinate zero of either sign of a
    translated binary block by 2.  Two ordinary cubic blocks complete the
    template.  PAF-identical states are merged before an exact signature
    join.

    The result tuple contains

        root-free templates, U states, V states, row-compatible joins, matches.
    """

    prime = 83
    templates: list[
        tuple[int, int, SignSequence, int, tuple[int, ...]]
    ] = []
    for linear_coefficient in (1, 2):
        for constant in range(prime):
            sequence = tuple(
                legendre(
                    index**3 + linear_coefficient * index + constant,
                    prime,
                )
                for index in range(prime)
            )
            if 0 not in sequence:
                templates.append(
                    (
                        linear_coefficient,
                        constant,
                        sequence,
                        sum(sequence),
                        half_paf(sequence),
                    )
                )

    ordinary_pairs: dict[
        tuple[int, tuple[int, ...]], tuple[int, int, int, int]
    ] = {}
    for left_index, (
        left_coefficient,
        left_constant,
        _left,
        left_sum,
        left_paf,
    ) in enumerate(templates):
        for (
            right_coefficient,
            right_constant,
            _right,
            right_sum,
            right_paf,
        ) in templates[left_index:]:
            key = (
                left_sum * left_sum + right_sum * right_sum,
                tuple(
                    left_paf[index] + right_paf[index]
                    for index in range(len(left_paf))
                ),
            )
            ordinary_pairs.setdefault(
                key,
                (
                    left_coefficient,
                    left_constant,
                    right_coefficient,
                    right_constant,
                ),
            )
    ordinary_square_totals = {key[0] for key in ordinary_pairs}

    u_states: dict[
        tuple[int, tuple[int, ...]], tuple[int, int, int]
    ] = {}
    v_states: dict[
        tuple[int, tuple[int, ...]], tuple[int, int, int, int]
    ] = {}
    for coefficient, constant, sequence, _row_sum, _paf in templates:
        for shift in range(prime):
            translated = tuple(
                sequence[(index - shift) % prime]
                for index in range(prime)
            )
            u = (0,) + tuple(
                legendre(index, prime) * translated[index]
                for index in range(1, prime)
            )
            u_states.setdefault(
                (sum(u), half_paf(u)),
                (coefficient, constant, shift),
            )
            for sign in (-1, 1):
                v = (2,) + tuple(
                    sign * translated[index]
                    for index in range(1, prime)
                )
                v_states.setdefault(
                    (sum(v), half_paf(v)),
                    (coefficient, constant, shift, sign),
                )

    v_by_sum: defaultdict[
        int,
        list[
            tuple[
                tuple[int, ...],
                tuple[int, int, int, int],
            ]
        ],
    ] = defaultdict(list)
    for (row_sum, paf), witness in v_states.items():
        v_by_sum[row_sum].append((paf, witness))

    row_compatible = 0
    matches = 0
    for (u_sum, u_paf), _u_witness in u_states.items():
        for v_sum, states in v_by_sum.items():
            ordinary_square_total = 334 - u_sum * u_sum - v_sum * v_sum
            if ordinary_square_total not in ordinary_square_totals:
                continue
            for v_paf, _v_witness in states:
                row_compatible += 1
                needed = tuple(
                    -u_paf[index] - v_paf[index]
                    for index in range(len(u_paf))
                )
                if (ordinary_square_total, needed) in ordinary_pairs:
                    matches += 1
    return (
        len(templates),
        len(u_states),
        len(v_states),
        row_compatible,
        matches,
    )


def osds_size_profiles() -> tuple[
    tuple[tuple[int, int, int, int, int, int, int, int], ...],
    tuple[tuple[int, int, int, int, int, int, int, int], ...],
]:
    """Return all raw and anchored-canonical prime-fold size profiles.

    A record is ``(|X|,|Y|,|Z|,|W|,sum(U),sum(V),sum(C),sum(D))``.
    The anomaly ``V[0]=2`` fixes the sign of ``V``.  The zero-anomaly
    sequence ``U`` and the ordinary binary sequences ``C,D`` can be negated,
    and ``C,D`` can be exchanged.  The canonical list uses those operations
    to require ``sum(U)>=0`` and ``sum(C)>=sum(D)>=0``.
    """

    raw = []
    canonical = []
    short_pairs_by_square: defaultdict[
        int, list[tuple[int, int, int, int]]
    ] = defaultdict(list)
    for z_size in range(84):
        c_sum = 83 - 2 * z_size
        for w_size in range(84):
            d_sum = 83 - 2 * w_size
            short_pairs_by_square[c_sum * c_sum + d_sum * d_sum].append(
                (z_size, w_size, c_sum, d_sum)
            )
    for x_size in range(83):
        u_sum = 82 - 2 * x_size
        for y_size in range(83):
            v_sum = 84 - 2 * y_size
            remaining = 334 - u_sum * u_sum - v_sum * v_sum
            for z_size, w_size, c_sum, d_sum in short_pairs_by_square.get(
                remaining, ()
            ):
                record = (
                    x_size,
                    y_size,
                    z_size,
                    w_size,
                    u_sum,
                    v_sum,
                    c_sum,
                    d_sum,
                )
                raw.append(record)
                if u_sum >= 0 and c_sum >= d_sum >= 0:
                    canonical.append(record)
    return tuple(raw), tuple(canonical)


def signs(bit_count: int) -> Iterable[SignSequence]:
    for bits in itertools.product((-1, 1), repeat=bit_count):
        yield tuple(bits)


def self_test() -> None:
    generator = random.Random(668)
    for n in range(1, 12):
        for _ in range(20):
            vectors = tuple(
                tuple(generator.choice((-1, 1)) for _ in range(length))
                for length in (n + 1, n + 1, n, n)
            )
            check_fold_identities(*vectors)
            if dual_folds_are_exact(*vectors) != is_base_sequence(*vectors):
                raise AssertionError(f"dual-fold equivalence failed at n={n}")

    # Exhaustion makes the equivalence independent of the random fixtures.
    for n in range(1, 4):
        lengths = (n + 1, n + 1, n, n)
        for flat in signs(sum(lengths)):
            offset = 0
            vectors = []
            for length in lengths:
                vectors.append(flat[offset : offset + length])
                offset += length
            if dual_folds_are_exact(*vectors) != is_base_sequence(*vectors):
                raise AssertionError(f"exhaustive equivalence failed at n={n}")

    # Check the set formula on arbitrary normalized folded data.
    modulus = 83
    universe_nonzero = tuple(range(1, modulus))
    universe = tuple(range(modulus))
    for _ in range(40):
        x = {value for value in universe_nonzero if generator.randrange(2)}
        y = {value for value in universe_nonzero if generator.randrange(2)}
        z = {value for value in universe if generator.randrange(2)}
        w = {value for value in universe if generator.randrange(2)}
        check_osds_formula(x, y, z, w, modulus)

    order = 1
    value = 2 % 83
    while value != 1:
        value = value * 2 % 83
        order += 1
    if order != 82 or pow(2, 41, 83) != 82:
        raise AssertionError("2 should be primitive modulo 83")
    raw_profiles, canonical_profiles = osds_size_profiles()
    if len(raw_profiles) != 672 or len(canonical_profiles) != 45:
        raise AssertionError("unexpected prime-fold size-profile count")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quadratic-scan",
        action="store_true",
        help="also scan the finite quadratic-character OSDS template",
    )
    parser.add_argument(
        "--cubic-scan",
        action="store_true",
        help="also scan the finite root-free cubic-character OSDS template",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    self_test()
    print("PASS adjacent cyclic-fold identities and equivalence")
    print("PASS prime-83 oriented-SDS coefficient formula")
    print("PASS ord_83(2)=82 and 2^41=-1 mod 83")
    raw_profiles, canonical_profiles = osds_size_profiles()
    print(
        "prime_fold_size_profiles="
        f"{len(raw_profiles)} raw, {len(canonical_profiles)} anchored-canonical"
    )
    if args.quadratic_scan:
        matches = quadratic_character_scan()
        if matches != 0:
            raise AssertionError(
                "the documented quadratic-character scan count changed"
            )
        print(f"quadratic_character_prime_fold_matches={matches}")
        if matches:
            print("SURVIVES: inspect the periodic witnesses")
        else:
            print("NO MATCH in the stated quadratic-character template family")
    if args.cubic_scan:
        templates, u_states, v_states, joins, matches = cubic_character_scan()
        expected = (56, 2324, 4648, 3013755, 0)
        if (templates, u_states, v_states, joins, matches) != expected:
            raise AssertionError(
                "the documented cubic-character scan counts changed"
            )
        print(
            "cubic_character_scan="
            f"{templates} templates, {u_states} U states, {v_states} V states, "
            f"{joins} row-compatible joins"
        )
        print(f"cubic_character_prime_fold_matches={matches}")
        if matches:
            print("SURVIVES: inspect the periodic witnesses")
        else:
            print("NO MATCH in the stated cubic-character template family")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
