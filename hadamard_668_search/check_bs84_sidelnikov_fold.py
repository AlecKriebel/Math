#!/usr/bin/env python3
"""Exact prime-83 Sidelnikov-fold identities and finite template exclusions.

The checker studies

    S_a(i) = chi(2^i + a),  i in Z/83,

where ``chi`` is the quadratic character of ``F_167``.  It verifies the
closed correlation formula, excludes the direct endpoint-fold construction
for every phase and sign, and hash-joins the natural degree-at-most-two
product extension.  It never searches arbitrary BS(84,83) signs.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass


PRIME = 167
ORDER = 83
HALF = 41


def character(value: int) -> int:
    value %= PRIME
    if value == 0:
        return 0
    return 1 if pow(value, (PRIME - 1) // 2, PRIME) == 1 else -1


H = tuple(pow(2, index, PRIME) for index in range(ORDER))
H_INDEX = {value: index for index, value in enumerate(H)}


def shift(sequence: Sequence[int], amount: int) -> tuple[int, ...]:
    """Return ``result[i] = sequence[i-amount]`` on Z/83."""

    return tuple(sequence[(index - amount) % ORDER] for index in range(ORDER))


def decimate(sequence: Sequence[int], multiplier: int) -> tuple[int, ...]:
    """Return ``result[i] = sequence[multiplier*i]`` on Z/83."""

    return tuple(
        sequence[(multiplier * index) % ORDER] for index in range(ORDER)
    )


def periodic_paf(sequence: Sequence[int]) -> tuple[int, ...]:
    if len(sequence) != ORDER:
        raise ValueError("expected a length-83 sequence")
    return tuple(
        sum(
            sequence[index] * sequence[(index + lag) % ORDER]
            for index in range(ORDER)
        )
        for lag in range(1, HALF + 1)
    )


def decimate_paf(paf: Sequence[int], multiplier: int) -> tuple[int, ...]:
    """Permute a half-PAF under an index multiplier, identifying +/- lags."""

    result = []
    for lag in range(1, HALF + 1):
        oriented = multiplier * lag % ORDER
        unoriented = min(oriented, ORDER - oriented)
        result.append(paf[unoriented - 1])
    return tuple(result)


def sidelnikov(parameter: int) -> tuple[int, ...]:
    return tuple(character(value + parameter) for value in H)


BINARY = sidelnikov(1)
ZERO = sidelnikov(-1)
BINARY_PAF = periodic_paf(BINARY)
ZERO_PAF = periodic_paf(ZERO)


def verify_parameter_classification() -> None:
    if len(set(H)) != ORDER or H[-1] * 2 % PRIME != 1:
        raise AssertionError("2 does not have order 83 modulo 167")
    if any(character(value) != 1 for value in H):
        raise AssertionError("the powers of 2 are not the quadratic residues")

    for parameter in range(PRIME):
        sequence = sidelnikov(parameter)
        if parameter == 0:
            if sequence != (1,) * ORDER:
                raise AssertionError("S_0 should be constant one")
            continue
        if character(parameter) == 1:
            phase = H_INDEX[parameter]
            expected = shift(BINARY, phase)
            expected_sum = -1
            expected_zeros = 0
        else:
            phase = H_INDEX[-parameter % PRIME]
            expected = shift(ZERO, phase)
            expected_sum = 0
            expected_zeros = 1
        if sequence != expected:
            raise AssertionError(f"S_{parameter} phase classification failed")
        if sum(sequence) != expected_sum or sequence.count(0) != expected_zeros:
            raise AssertionError(f"S_{parameter} row data failed")

    if any(BINARY[index] != BINARY[-index % ORDER] for index in range(ORDER)):
        raise AssertionError("the binary Sidelnikov sequence is not symmetric")
    if any(ZERO[index] != -ZERO[-index % ORDER] for index in range(ORDER)):
        raise AssertionError("the zero Sidelnikov sequence is not skew")


def jacobsthal_trace(lag: int) -> int:
    """Return sum_x chi(x(x+1)(h_lag*x+1))."""

    multiplier = H[lag % ORDER]
    return sum(
        character(value * (value + 1) * (multiplier * value + 1))
        for value in range(PRIME)
    )


def verify_correlation_formula() -> None:
    if (sum(BINARY), sum(ZERO), BINARY.count(0), ZERO.count(0)) != (-1, 0, 0, 1):
        raise AssertionError("base Sidelnikov row fingerprint failed")
    for lag in range(1, ORDER):
        trace = jacobsthal_trace(lag)
        if trace % 2:
            raise AssertionError("the Jacobsthal trace should be even")
        binary = sum(
            BINARY[index] * BINARY[(index + lag) % ORDER]
            for index in range(ORDER)
        )
        zero = sum(
            ZERO[index] * ZERO[(index + lag) % ORDER]
            for index in range(ORDER)
        )
        if binary != -1 + trace // 2:
            raise AssertionError(f"binary PAF formula failed at lag {lag}")
        if zero != -1 - trace // 2:
            raise AssertionError(f"zero PAF formula failed at lag {lag}")
        if binary + zero != -2:
            raise AssertionError(f"complementary PAF failed at lag {lag}")

    expected_distribution = {
        -13: 3,
        -9: 5,
        -5: 7,
        -1: 11,
        3: 7,
        7: 5,
        11: 3,
    }
    if dict(sorted(Counter(BINARY_PAF).items())) != expected_distribution:
        raise AssertionError("binary half-PAF distribution changed")
    if any(left + right != -2 for left, right in zip(BINARY_PAF, ZERO_PAF)):
        raise AssertionError("half-PAF complementarity failed")


def modified_binary(
    base: Sequence[int], phase: int, sign: int
) -> tuple[int, ...]:
    result = [sign * value for value in shift(base, phase)]
    result[0] = 2
    return tuple(result)


def verify_direct_family_exclusion() -> None:
    """Exclude U=Z, V=B with V[0]=2, C,D shifted copies of B."""

    v_sum_distribution: Counter[int] = Counter()
    periodic_matches = 0
    for phase in range(ORDER):
        for sign in (-1, 1):
            v = modified_binary(BINARY, phase, sign)
            v_sum_distribution[sum(v)] += 1
            v_paf = periodic_paf(v)
            total = tuple(
                ZERO_PAF[index]
                + v_paf[index]
                + 2 * BINARY_PAF[index]
                for index in range(HALF)
            )
            periodic_matches += not any(total)

            # Independently pin the one-coordinate update formula.
            underlying = tuple(sign * value for value in shift(BINARY, phase))
            delta = 2 - underlying[0]
            expected = tuple(
                BINARY_PAF[lag - 1]
                + delta * (underlying[lag] + underlying[-lag])
                for lag in range(1, HALF + 1)
            )
            if v_paf != expected:
                raise AssertionError("raised-coordinate PAF formula failed")

            # At every lag, the desired correction is 4 mod 8, while an odd
            # delta times {-2,0,2} is 0,2,or 6 mod 8.
            for lag in range(1, HALF + 1):
                desired = 2 - 2 * BINARY_PAF[lag - 1]
                correction = delta * (
                    underlying[lag] + underlying[-lag]
                )
                if desired % 8 != 4 or correction % 8 not in (0, 2, 6):
                    raise AssertionError("mod-8 obstruction fingerprint failed")
                if desired == correction:
                    raise AssertionError("direct Sidelnikov lag unexpectedly matched")

    if v_sum_distribution != Counter({2: 84, 0: 41, 4: 41}):
        raise AssertionError("modified-binary row-sum distribution changed")
    if periodic_matches != 0:
        raise AssertionError("direct Sidelnikov endpoint fold unexpectedly matched")

    # U has sum 0 and C,D have squared sums 1.  Thus the possible total
    # squared row sums are 2,6,18, never the required 334.
    norm_values = {
        v_sum * v_sum + 2 for v_sum in v_sum_distribution
    }
    if norm_values != {2, 6, 18}:
        raise AssertionError("direct-family row norm fingerprint changed")

    # Anchoring the unique zero of U at coordinate zero leaves its sign,
    # while V,C,D each have 83 phases and two signs.
    labeled_states = 2 * (2 * ORDER) ** 3
    if labeled_states != 9_148_592:
        raise AssertionError("direct-family labeled-state count changed")


def verify_zero_fill_variant() -> None:
    """Exclude the obvious variant obtained by filling Z[0] with a sign."""

    filled_plus = (1,) + ZERO[1:]
    filled_minus = (-1,) + ZERO[1:]
    if periodic_paf(filled_plus) != ZERO_PAF:
        raise AssertionError("positive zero-fill changed the PAF")
    if periodic_paf(filled_minus) != ZERO_PAF:
        raise AssertionError("negative zero-fill changed the PAF")
    if (sum(filled_plus), sum(filled_minus)) != (1, -1):
        raise AssertionError("zero-fill row sums changed")

    # Every ordinary block from B or a filled Z has squared row sum one.
    # A modified such V still has row sum 0,2,or4, so the same norm
    # obstruction gives at most 18 rather than 334.
    for base in (BINARY, filled_plus, filled_minus):
        for phase in range(ORDER):
            for sign in (-1, 1):
                total = sum(modified_binary(base, phase, sign)) ** 2 + 2
                if total not in (2, 6, 18):
                    raise AssertionError("zero-fill row-norm obstruction failed")


@dataclass(frozen=True)
class Template:
    kind: str
    parameter: int
    sequence: tuple[int, ...]
    paf: tuple[int, ...]
    row_sum: int


def template(kind: str, parameter: int, sequence: Sequence[int]) -> Template:
    values = tuple(sequence)
    return Template(kind, parameter, values, periodic_paf(values), sum(values))


def product_libraries() -> tuple[tuple[Template, ...], tuple[Template, ...]]:
    """Return the raw degree-at-most-two binary and one-zero libraries."""

    binary = [template("B", -1, BINARY)]
    zero = [
        template("Z", -1, ZERO),
        template("Z2", -1, tuple(value * value for value in ZERO)),
    ]
    for phase in range(ORDER):
        translated = shift(BINARY, phase)
        binary.append(
            template(
                "BB",
                phase,
                tuple(
                    BINARY[index] * translated[index]
                    for index in range(ORDER)
                ),
            )
        )
        zero.append(
            template(
                "ZB",
                phase,
                tuple(
                    ZERO[index] * translated[index]
                    for index in range(ORDER)
                ),
            )
        )
    if len(binary) != 84 or len(zero) != 85:
        raise AssertionError("raw product-library size changed")
    if any(0 in item.sequence for item in binary):
        raise AssertionError("binary product library contains a zero")
    if any(
        item.sequence.count(0) != 1 or item.sequence[0] != 0
        for item in zero
    ):
        raise AssertionError("one-zero product library is malformed")
    return tuple(binary), tuple(zero)


def generalized_product_scan() -> tuple[int, int, int]:
    """Hash-join the complete raw degree-at-most-two product extension."""

    binary, zero = product_libraries()

    cd_by_key: defaultdict[
        tuple[int, tuple[int, ...]], list[tuple[int, int]]
    ] = defaultdict(list)
    cd_norms: set[int] = set()
    for left_index, left in enumerate(binary):
        for right_index in range(left_index, len(binary)):
            right = binary[right_index]
            norm = left.row_sum * left.row_sum + right.row_sum * right.row_sum
            signature = tuple(
                x + y for x, y in zip(left.paf, right.paf)
            )
            cd_by_key[(norm, signature)].append((left_index, right_index))
            cd_norms.add(norm)

    if sum(len(values) for values in cd_by_key.values()) != 3_570:
        raise AssertionError("raw C/D product-pair count changed")
    if len(cd_by_key) != 946 or len(cd_norms) != 33:
        raise AssertionError("C/D signature catalog fingerprint changed")
    if len({item.paf for item in binary}) != 43:
        raise AssertionError("binary product PAF count changed")
    if len({item.paf for item in zero}) != 44:
        raise AssertionError("one-zero product PAF count changed")

    uv_states = 0
    row_compatible = 0
    matches = 0
    remainder_distribution: Counter[int] = Counter()
    for u in zero:
        for v_base in binary:
            for phase in range(ORDER):
                translated = shift(v_base.sequence, phase)
                for sign in (-1, 1):
                    underlying = tuple(sign * value for value in translated)
                    delta = 2 - underlying[0]
                    v_sum = sign * v_base.row_sum + delta
                    remaining_norm = (
                        334 - u.row_sum * u.row_sum - v_sum * v_sum
                    )
                    uv_states += 1
                    if remaining_norm not in cd_norms:
                        continue
                    row_compatible += 1
                    remainder_distribution[remaining_norm] += 1
                    v_paf = tuple(
                        v_base.paf[lag - 1]
                        + delta * (underlying[lag] + underlying[-lag])
                        for lag in range(1, HALF + 1)
                    )
                    needed = tuple(
                        -u.paf[index] - v_paf[index]
                        for index in range(HALF)
                    )
                    matches += len(
                        cd_by_key.get((remaining_norm, needed), ())
                    )

    if uv_states != 1_185_240:
        raise AssertionError("generalized U/V state count changed")
    if row_compatible != 83_982:
        raise AssertionError("generalized row-compatible count changed")
    expected_remainders = Counter(
        {218: 34_062, 170: 23_328, 90: 13_236, 122: 7_056, 74: 6_300}
    )
    if remainder_distribution != expected_remainders:
        raise AssertionError("generalized row-norm distribution changed")
    if matches != 0:
        raise AssertionError("degree-two product extension unexpectedly matched")
    return uv_states, row_compatible, matches


def orientation_signature(sequence: Sequence[int]) -> int:
    """Encode whether each inverse pair has equal or opposite signs."""

    return sum(
        (sequence[lag] == sequence[-lag]) << (lag - 1)
        for lag in range(1, HALF + 1)
    )


def independent_decimation_exclusion() -> tuple[int, int, int, int, int, int]:
    """Exclude independent template decimations by their mod-4 signatures.

    A common multiplier normalizes the one-zero U template.  Multipliers d
    and -d induce the same half-PAF, so 1..41 represent all relative
    decimations.  Before a 41-coordinate PAF join is necessary, the two
    ordinary binary blocks force a 41-bit inverse-pair condition on U,V.
    """

    binary_raw, zero_raw = product_libraries()

    def representatives(items: Sequence[Template]) -> tuple[Template, ...]:
        by_signature: dict[tuple[int, tuple[int, ...]], Template] = {}
        for item in items:
            key = (item.row_sum * item.row_sum, item.paf)
            by_signature.setdefault(key, item)
        return tuple(by_signature.values())

    binary_bases = representatives(binary_raw)
    zero_bases = representatives(zero_raw)
    if (len(binary_bases), len(zero_bases)) != (43, 44):
        raise AssertionError("base signature quotient changed")

    binary_catalog: dict[
        tuple[int, tuple[int, ...]], tuple[Template, int, tuple[int, ...]]
    ] = {}
    zero_catalog: set[tuple[int, tuple[int, ...]]] = set()
    for item in binary_bases:
        for multiplier in range(1, HALF + 1):
            sequence = decimate(item.sequence, multiplier)
            paf = decimate_paf(item.paf, multiplier)
            if periodic_paf(sequence) != paf:
                raise AssertionError("binary decimation PAF formula failed")
            key = (item.row_sum * item.row_sum, paf)
            previous = binary_catalog.setdefault(
                key, (item, multiplier, sequence)
            )
            if previous[2] != sequence:
                raise AssertionError(
                    "a binary PAF collision does not preserve the V family"
                )
    for item in zero_bases:
        for multiplier in range(1, HALF + 1):
            paf = decimate_paf(item.paf, multiplier)
            zero_catalog.add((item.row_sum * item.row_sum, paf))
    if (len(binary_catalog), len(zero_catalog)) != (1_723, 1_723):
        raise AssertionError("independent-decimation catalog size changed")

    u_counts = Counter(
        orientation_signature(item.sequence) for item in zero_bases
    )
    v_counts: Counter[int] = Counter()
    for _item, _multiplier, sequence in binary_catalog.values():
        for phase in range(ORDER):
            v_counts[orientation_signature(shift(sequence, phase))] += 1

    intersection = set(u_counts).intersection(v_counts)
    all_symmetric = (1 << HALF) - 1
    if (
        len(u_counts) != 43
        or len(v_counts) != 35_302
        or intersection != {all_symmetric}
    ):
        raise AssertionError("orientation-signature fingerprint changed")

    compatible_u = [
        item
        for item in zero_bases
        if orientation_signature(item.sequence) == all_symmetric
    ]
    if (
        len(compatible_u) != 1
        or compatible_u[0].kind != "Z2"
        or compatible_u[0].row_sum != 82
        or v_counts[all_symmetric] != 1_805
    ):
        raise AssertionError("unique orientation intersection changed")

    # Every exact prime-fold object would need equal U/V inverse-pair
    # signatures.  The only intersection uses U=Z^2, whose squared row sum
    # alone is 82^2 > 334.
    if compatible_u[0].row_sum**2 <= 334:
        raise AssertionError("orientation survivor unexpectedly has valid energy")

    normalized_uv_states = len(zero_bases) * len(binary_catalog) * ORDER * 2
    if normalized_uv_states != 12_584_792:
        raise AssertionError("normalized independent-decimation count changed")

    binary_states = tuple(binary_catalog.values())
    cd_norms: set[int] = set()
    norm_admissible_pairs = 0
    for left_index, (left, _left_d, _left_sequence) in enumerate(binary_states):
        left_norm = left.row_sum**2
        for right, _right_d, _right_sequence in binary_states[left_index:]:
            norm = left_norm + right.row_sum**2
            cd_norms.add(norm)
            norm_admissible_pairs += norm <= 334
    if norm_admissible_pairs != 1_475_877:
        raise AssertionError("decimated C/D norm-admissible count changed")

    row_compatible = 0
    remainder_distribution: Counter[int] = Counter()
    for u in zero_bases:
        for v, _multiplier, _sequence in binary_states:
            positive = (ORDER + v.row_sum) // 2
            negative = ORDER - positive
            # Across all phases, the raised V row sums for signs +/- are:
            # q[0]=+1: r+1 and -r+3; q[0]=-1: r+3 and -r+1.
            for v_sum, multiplicity in (
                (v.row_sum + 1, positive),
                (-v.row_sum + 3, positive),
                (v.row_sum + 3, negative),
                (-v.row_sum + 1, negative),
            ):
                remaining = 334 - u.row_sum**2 - v_sum**2
                if remaining in cd_norms:
                    row_compatible += multiplicity
                    remainder_distribution[remaining] += multiplicity
    expected_remainders = Counter(
        {74: 64_575, 90: 135_669, 122: 72_324, 170: 239_112, 218: 351_657}
    )
    if (
        row_compatible != 863_337
        or remainder_distribution != expected_remainders
    ):
        raise AssertionError("decimated U/V row-norm fingerprint changed")
    return (
        len(binary_catalog),
        len(zero_catalog),
        normalized_uv_states,
        2 * v_counts[all_symmetric],
        norm_admissible_pairs,
        row_compatible,
    )


def main() -> None:
    verify_parameter_classification()
    verify_correlation_formula()
    verify_direct_family_exclusion()
    verify_zero_fill_variant()
    uv_states, row_compatible, matches = generalized_product_scan()
    (
        binary_decimated,
        zero_decimated,
        independently_decimated_uv,
        orientation_survivors,
        decimated_cd_pairs,
        decimated_row_compatible,
    ) = independent_decimation_exclusion()
    print("PASS: all 166 nonzero S_a classified as binary/one-zero phases")
    print("PASS: row sums, symmetry, and exact Jacobsthal PAF formulas")
    print("PASS: PAF_B(k)+PAF_Z(k)=-2 at every nonzero lag")
    print(
        "DIRECT FAMILY EXCLUDED: 9,148,592 labeled phase/sign states "
        "(row norm and mod-8 certificates)"
    )
    print("ZERO-FILL BINARY VARIANT EXCLUDED by the row-norm certificate")
    print(
        "DEGREE-2 PRODUCT FAMILY EXCLUDED: "
        f"{uv_states} U/V states, {row_compatible} row-compatible, "
        f"{matches} PAF joins"
    )
    print(
        "INDEPENDENT DECIMATIONS EXCLUDED: "
        f"{binary_decimated}/{zero_decimated} binary/one-zero signatures, "
        f"{decimated_cd_pairs} norm-admissible C/D pairs, "
        f"{independently_decimated_uv} normalized U/V states, "
        f"{decimated_row_compatible} row-compatible; "
        f"the only {orientation_survivors} mod-4 survivors use "
        "row-inadmissible U=Z^2"
    )


if __name__ == "__main__":
    main()
