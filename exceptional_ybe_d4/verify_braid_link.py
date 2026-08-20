#!/usr/bin/env python3
"""Exact checks for the global braid and enhanced-link consequences.

The local matrix calculations use exact arithmetic in
Q(sqrt(2), sqrt(3), i).  The n=3,4 all-strand calculations use an exact
Pauli-sum representation, so they do not construct dense 64- or
256-dimensional matrices.
"""

from fractions import Fraction
from pathlib import Path
import sys


if sys.flags.optimize:
    raise RuntimeError("optimized Python is not permitted for scientific verification")

# Normal package runs import the sibling module directly.  The cwd fallback
# lets the negative-test harness execute a mutated temporary copy while still
# using the frozen exact-arithmetic implementation from the package root.
SCRIPT_DIR = Path(__file__).resolve().parent
if not (SCRIPT_DIR / "verify_concurrent_equivalence.py").is_file():
    SCRIPT_DIR = Path.cwd()
sys.path.insert(0, str(SCRIPT_DIR))
import verify_concurrent_equivalence as exact


ZERO = exact.ZERO
ONE = exact.ONE
IUNIT = exact.IUNIT
SQRT2 = exact.SQRT2
SQRT3 = exact.SQRT3


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def scalar_power(value, exponent):
    """Power for kappa, whose exact inverse is kappa squared."""

    if exponent < 0:
        value = value * value
        exponent = -exponent
    result = ONE
    for _ in range(exponent):
        result *= value
    return result


def matrix_power(value, exponent):
    require(exponent >= 0, "matrix_power requires a nonnegative exponent")
    result = exact.eye(len(value))
    for _ in range(exponent):
        result = exact.mmul(result, value)
    return result


def matrix_trace(value):
    return sum((value[index][index] for index in range(len(value))), ZERO)


def partial_trace_left(value, local_dimension=4):
    return exact.matrix(
        [
            [
                sum(
                    (
                        value[left * local_dimension + row][
                            left * local_dimension + column
                        ]
                        for left in range(local_dimension)
                    ),
                    ZERO,
                )
                for column in range(local_dimension)
            ]
            for row in range(local_dimension)
        ]
    )


def partial_trace_right(value, local_dimension=4):
    return exact.matrix(
        [
            [
                sum(
                    (
                        value[row * local_dimension + right][
                            column * local_dimension + right
                        ]
                        for right in range(local_dimension)
                    ),
                    ZERO,
                )
                for column in range(local_dimension)
            ]
            for row in range(local_dimension)
        ]
    )


def build_five_word_data():
    identity16 = exact.eye(16)
    m = exact.smul(
        Fraction(1, 2),
        exact.add(
            exact.neg(exact.pauli_word("ZIZZ")),
            exact.neg(exact.pauli_word("ZIJJ")),
            exact.neg(exact.pauli_word("JIZJ")),
            exact.pauli_word("JIJZ"),
        ),
    )
    e = exact.pauli_word("XIXX")
    h = exact.add(
        exact.smul(exact.CQ23(exact.Q23(0, 0, 0, Fraction(1, 3))), m),
        exact.smul(-SQRT3 / 3, e),
    )
    q = (ONE + IUNIT * SQRT3) / 2
    kappa = q - ONE
    kappa_inverse = kappa * kappa
    r = exact.add(
        exact.smul(kappa / 2, identity16),
        exact.smul((q + ONE) / 2, h),
    )
    r_inverse = exact.add(
        exact.smul(kappa_inverse / 2, identity16),
        exact.smul((kappa_inverse + 2 * ONE) / 2, h),
    )
    return identity16, m, e, h, q, kappa, kappa_inverse, r, r_inverse


# Standard Hermitian Pauli multiplication.  A Pauli sum is a dictionary from
# a word in I,X,Y,Z to an exact scalar.
PAULI_PRODUCT = {
    ("I", "I"): (ONE, "I"),
    ("I", "X"): (ONE, "X"),
    ("I", "Y"): (ONE, "Y"),
    ("I", "Z"): (ONE, "Z"),
    ("X", "I"): (ONE, "X"),
    ("Y", "I"): (ONE, "Y"),
    ("Z", "I"): (ONE, "Z"),
    ("X", "X"): (ONE, "I"),
    ("Y", "Y"): (ONE, "I"),
    ("Z", "Z"): (ONE, "I"),
    ("X", "Y"): (IUNIT, "Z"),
    ("Y", "X"): (-IUNIT, "Z"),
    ("Y", "Z"): (IUNIT, "X"),
    ("Z", "Y"): (-IUNIT, "X"),
    ("Z", "X"): (IUNIT, "Y"),
    ("X", "Z"): (-IUNIT, "Y"),
}

STANDARD_PAULI_MATRIX = {
    "I": exact.I2,
    "X": exact.X,
    "Y": exact.smul(IUNIT, exact.J),
    "Z": exact.Z,
}


def standard_pauli_word_matrix(word):
    return exact.kron(*(STANDARD_PAULI_MATRIX[letter] for letter in word))


def pauli_sum_matrix(value):
    result = exact.zero(2 ** len(next(iter(value))))
    for word, coefficient in value.items():
        result = exact.add(
            result,
            exact.smul(coefficient, standard_pauli_word_matrix(word)),
        )
    return result


def matrix_frobenius_squared(value):
    return sum(
        (entry.conjugate() * entry for row in value for entry in row),
        ZERO,
    )


def pauli_word_product(left, right):
    require(len(left) == len(right), "Pauli-word dimensions")
    phase = ONE
    product = []
    for left_letter, right_letter in zip(left, right):
        local_phase, local_product = PAULI_PRODUCT[(left_letter, right_letter)]
        phase *= local_phase
        product.append(local_product)
    return phase, "".join(product)


def pauli_sum_add(*values):
    result = {}
    for value in values:
        for word, coefficient in value.items():
            result[word] = result.get(word, ZERO) + coefficient
            if not result[word]:
                del result[word]
    return result


def pauli_sum_scale(scalar, value):
    return {
        word: scalar * coefficient
        for word, coefficient in value.items()
        if scalar * coefficient
    }


def pauli_sum_product(left, right):
    result = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            phase, word = pauli_word_product(left_word, right_word)
            result[word] = (
                result.get(word, ZERO)
                + left_coefficient * right_coefficient * phase
            )
            if not result[word]:
                del result[word]
    return result


def literal_five_word_pauli_operators(q, kappa):
    """Encode R_K and its inverse directly in the standard Pauli basis."""

    sqrt6 = exact.CQ23(exact.Q23(0, 0, 0, 1))
    h = {
        "ZIZZ": -sqrt6 / 6,
        "ZIYY": sqrt6 / 6,
        "YIZY": sqrt6 / 6,
        "YIYZ": -sqrt6 / 6,
        "XIXX": -SQRT3 / 3,
    }
    identity = {"IIII": ONE}
    kappa_inverse = kappa * kappa
    r = pauli_sum_add(
        pauli_sum_scale(kappa / 2, identity),
        pauli_sum_scale((q + ONE) / 2, h),
    )
    r_inverse = pauli_sum_add(
        pauli_sum_scale(kappa_inverse / 2, identity),
        pauli_sum_scale((kappa_inverse + 2 * ONE) / 2, h),
    )
    require(
        pauli_sum_product(r, r_inverse) == identity,
        "literal Pauli R inverse",
    )
    return r, r_inverse


def embed_pauli_sum(value, strand_count, site):
    return {
        embed_local_word(word, strand_count, site): coefficient
        for word, coefficient in value.items()
    }


def enhanced_braid_closure_value(
    braid_word, strand_count, r, r_inverse, kappa
):
    identity_word = "I" * (2 * strand_count)
    represented_braid = {identity_word: ONE}
    writhe = 0
    for site, exponent in braid_word:
        require(exponent in (-1, 1), "signed braid letter")
        local_operator = r if exponent == 1 else r_inverse
        represented_braid = pauli_sum_product(
            represented_braid,
            embed_pauli_sum(local_operator, strand_count, site),
        )
        writhe += exponent
    identity_coefficient = represented_braid.get(identity_word, ZERO)
    # Tr(P)=0 for every nonidentity Pauli word, while
    # 2^(-n) Tr(I_(4^n))=2^n.
    return (
        scalar_power(kappa, -writhe)
        * (2 ** strand_count)
        * identity_coefficient
    )


def embed_local_word(local_word, strand_count, site):
    require(len(local_word) == 4, "four-qubit local word")
    require(0 <= site < strand_count - 1, "local braid-generator index")
    return (
        "I" * (2 * site)
        + local_word
        + "I" * (2 * (strand_count - site - 2))
    )


def galindo_rowell_generator(strand_count, site, kappa, opposite=False):
    p_z = "IZZI"
    p_x = "XIXX"
    if opposite:
        p_z = p_z[2:] + p_z[:2]
        p_x = p_x[2:] + p_x[:2]
    p_z = embed_local_word(p_z, strand_count, site)
    p_x = embed_local_word(p_x, strand_count, site)
    p_z_p_x_phase, p_z_p_x = pauli_word_product(p_z, p_x)
    identity = "I" * (2 * strand_count)
    return pauli_sum_add(
        {identity: kappa / 2},
        {p_z: kappa * IUNIT / 2},
        {p_x: kappa * IUNIT / 2},
        {p_z_p_x: -kappa * p_z_p_x_phase / 2},
    )


def reverse_tensor_sites(value, strand_count):
    result = {}
    for word, coefficient in value.items():
        blocks = [word[2 * site : 2 * site + 2] for site in range(strand_count)]
        result["".join(reversed(blocks))] = coefficient
    return result


def pauli_words_commute(left, right):
    left_phase, _ = pauli_word_product(left, right)
    right_phase, _ = pauli_word_product(right, left)
    return left_phase == right_phase


def quarter_turn_conjugate_word(word, axis, inverse=False):
    """Conjugate by exp(i*pi*axis/4), or by its inverse."""

    if pauli_words_commute(word, axis):
        return ONE, word
    phase, product = pauli_word_product(axis, word)
    return (-IUNIT if inverse else IUNIT) * phase, product


def quarter_turn_conjugate(value, axis, inverse=False):
    result = {}
    for word, coefficient in value.items():
        phase, product = quarter_turn_conjugate_word(word, axis, inverse)
        result[product] = result.get(product, ZERO) + coefficient * phase
        if not result[product]:
            del result[product]
    return result


def braid_generator_conjugate(value, strand_count, site, inverse=False):
    """Conjugate by R_GR at one site; its scalar kappa cancels."""

    p_z = embed_local_word("IZZI", strand_count, site)
    p_x = embed_local_word("XIXX", strand_count, site)
    if inverse:
        # R^dagger T R = C_x^dagger C_z^dagger T C_z C_x.
        value = quarter_turn_conjugate(value, p_z, inverse=True)
        return quarter_turn_conjugate(value, p_x, inverse=True)
    # R T R^dagger = C_z C_x T C_x^dagger C_z^dagger.
    value = quarter_turn_conjugate(value, p_x)
    return quarter_turn_conjugate(value, p_z)


def garside_word(strand_count):
    """Delta=(s1)(s2 s1)...(s_{n-1}...s1), with zero-based indices."""

    return [
        site
        for last in range(1, strand_count)
        for site in range(last - 1, -1, -1)
    ]


def garside_conjugate(value, strand_count, inverse=False):
    if inverse:
        # D^dagger T D: inverse-conjugate by the factors from left to right.
        for site in garside_word(strand_count):
            value = braid_generator_conjugate(
                value, strand_count, site, inverse=True
            )
        return value
    # D T D^dagger: conjugate by the factors from right to left.
    for site in reversed(garside_word(strand_count)):
        value = braid_generator_conjugate(value, strand_count, site)
    return value


def verify_local_matrix_consequences():
    (
        identity16,
        m,
        e,
        h,
        q,
        kappa,
        kappa_inverse,
        r,
        r_inverse,
    ) = build_five_word_data()

    mathsf_a = exact.smul(-IUNIT * SQRT2, m)
    mathsf_b = exact.smul(IUNIT, e)
    u_k = exact.smul(
        Fraction(1, 2), exact.add(mathsf_a, exact.mmul(mathsf_a, mathsf_b))
    )
    v_k = exact.smul(
        Fraction(1, 2), exact.sub(mathsf_a, exact.mmul(mathsf_a, mathsf_b))
    )
    require(exact.equal(exact.dagger(u_k), exact.neg(u_k)), "U_K skew-Hermitian")
    require(exact.equal(exact.dagger(v_k), exact.neg(v_k)), "V_K skew-Hermitian")
    require(
        exact.equal(exact.mmul(exact.dagger(u_k), u_k), identity16),
        "U_K unitary",
    )
    require(
        exact.equal(exact.mmul(exact.dagger(v_k), v_k), identity16),
        "V_K unitary",
    )
    print("[ok] U_K and V_K are skew-Hermitian unitaries")

    ukvk = exact.mmul(u_k, v_k)
    require(exact.equal(exact.mmul(u_k, u_k), exact.neg(identity16)), "U_K^2")
    require(exact.equal(exact.mmul(v_k, v_k), exact.neg(identity16)), "V_K^2")
    require(exact.equal(ukvk, exact.neg(exact.mmul(v_k, u_k))), "U_K V_K anticommutation")
    require(exact.equal(ukvk, mathsf_b), "U_K V_K = mathsf B")
    intrinsic_sum = exact.add(u_k, v_k, ukvk)
    require(
        exact.equal(intrinsic_sum, exact.smul(-IUNIT * SQRT3, h)),
        "intrinsic H factorization",
    )
    zeta = (SQRT3 + IUNIT) / 2
    require(
        exact.equal(
            r,
            exact.smul(
                IUNIT * zeta / 2,
                exact.add(identity16, u_k, v_k, ukvk),
            ),
        ),
        "intrinsic Family III formula",
    )

    # Independently bind the displayed change of basis and the literal
    # Galindo--Rowell Section 13 tensor placements in this verification path.
    p_z = exact.kron(exact.I2, exact.Z, exact.Z, exact.I2)
    p_x = exact.kron(exact.X, exact.I2, exact.X, exact.X)
    u_gr = exact.smul(IUNIT, p_z)
    v_gr = exact.smul(IUNIT, p_x)
    r_gr = exact.smul(
        IUNIT * zeta / 2,
        exact.add(identity16, u_gr, v_gr, exact.mmul(u_gr, v_gr)),
    )
    two = exact.CQ23(2)
    s = exact.smul(
        Fraction(1, 4),
        exact.matrix(
            [
                [two + SQRT2, -IUNIT * SQRT2, IUNIT * SQRT2, two - SQRT2],
                [SQRT2, IUNIT * (two + SQRT2), IUNIT * (two - SQRT2), -SQRT2],
                [-(two - SQRT2), -IUNIT * SQRT2, IUNIT * SQRT2, -(two + SQRT2)],
                [-SQRT2, IUNIT * (two - SQRT2), IUNIT * (two + SQRT2), SQRT2],
            ]
        ),
    )
    require(exact.equal(exact.mmul(exact.dagger(s), s), exact.eye(4)), "S unitary")
    sigma = exact.site_swap()
    local_change = exact.kron(s, s)
    comparison = exact.mmul(
        exact.mmul(
            exact.dagger(local_change),
            exact.mmul(exact.mmul(sigma, r_gr), sigma),
        ),
        local_change,
    )
    require(exact.equal(r, comparison), "exact two-site comparison")
    print("[ok] intrinsic factorization, S unitarity, and exact two-site comparison")

    # This exact eight-term image witnesses that the literal five-word matrix
    # is not Clifford in the unmodified standard computational Pauli frame.
    # Its Clifford structure is instead in the fixed conjugated frame used in
    # the manuscript.
    standard_frame_witness = {
        "YIYY": SQRT2 / 4,
        "YIYZ": -SQRT2 / 4,
        "YIZY": SQRT2 / 4,
        "YIZZ": -SQRT2 / 4,
        "ZIYY": -SQRT2 / 4,
        "ZIYZ": SQRT2 / 4,
        "ZIZY": -SQRT2 / 4,
        "ZIZZ": SQRT2 / 4,
    }
    standard_frame_image = exact.mmul(
        exact.mmul(r, standard_pauli_word_matrix("XIII")),
        exact.dagger(r),
    )
    standard_frame_residual = exact.sub(
        standard_frame_image,
        pauli_sum_matrix(standard_frame_witness),
    )
    require(
        matrix_frobenius_squared(standard_frame_residual) == ZERO,
        "standard-frame eight-term witness",
    )
    require(len(standard_frame_witness) == 8, "standard-frame witness support")
    print("[ok] standard-frame eight-term witness for R(XIII)R^dagger (residual^2=0)")

    identity4 = exact.eye(4)
    enhancement_positive = 2 * kappa
    enhancement_negative = 2 * kappa_inverse
    for label, actual, expected in (
        ("Tr_1(R)", partial_trace_left(r), exact.smul(enhancement_positive, identity4)),
        ("Tr_2(R)", partial_trace_right(r), exact.smul(enhancement_positive, identity4)),
        (
            "Tr_1(R^-1)",
            partial_trace_left(r_inverse),
            exact.smul(enhancement_negative, identity4),
        ),
        (
            "Tr_2(R^-1)",
            partial_trace_right(r_inverse),
            exact.smul(enhancement_negative, identity4),
        ),
    ):
        require(exact.equal(actual, expected), label)
    print("[ok] scalar enhancement: Tr_1,Tr_2(R^+/-1)=2 kappa^+/-1 I_4")

    require(exact.equal(exact.mmul(r, r_inverse), identity16), "R inverse")
    require(
        exact.equal(
            exact.sub(r, exact.smul(q, r_inverse)),
            exact.smul(kappa, identity16),
        ),
        "R - q R^-1 = kappa I",
    )
    require(q * kappa_inverse * kappa_inverse == -ONE, "HOMFLYPT skein sign")
    print("[ok] R - q R^-1 = kappa I and q kappa^-2 = -1")

    require(
        exact.equal(matrix_power(r, 3), exact.neg(identity16)),
        "R^3 = -I",
    )
    require(exact.equal(matrix_power(r, 6), identity16), "R^6 = I")
    require(scalar_power(kappa, 3) == ONE, "kappa^3 = 1")
    print("[ok] R^3 = -I, R^6 = I, and kappa^3 = 1")

    # Ordinary unnormalized traces, followed by the enhanced factor 2^-n.
    hopf_writhe_factor = scalar_power(kappa, -2)
    hopf = hopf_writhe_factor * matrix_trace(matrix_power(r, 2)) / 4
    trefoil = scalar_power(kappa, -3) * matrix_trace(matrix_power(r, 3)) / 4
    mirror_hopf = scalar_power(kappa, 2) * matrix_trace(
        matrix_power(r_inverse, 2)
    ) / 4
    mirror_trefoil = scalar_power(kappa, 3) * matrix_trace(
        matrix_power(r_inverse, 3)
    ) / 4
    unknot = matrix_trace(identity4) / 2
    two_component_unlink = matrix_trace(identity16) / 4
    require(unknot == 2, "unknot value")
    require(two_component_unlink == 4, "two-component unlink value")
    require(hopf == -2 and mirror_hopf == -2, "oriented Hopf values")
    require(trefoil == -4 and mirror_trefoil == -4, "oriented trefoil values")

    def two_strand_value(exponent):
        return (
            scalar_power(kappa, -exponent)
            * matrix_trace(matrix_power(r, exponent))
            / 4
        )

    for exponent in range(3):
        require(
            two_strand_value(exponent + 3) == -two_strand_value(exponent),
            "three-twist sign",
        )
    print("[ok] low links: unknot 2, unlink_2 4, Hopf -2, trefoil -4")
    print("[ok] enhanced two-strand values acquire a minus sign after three twists")
    return q, kappa


def verify_global_pauli_consequences(q, kappa):
    # R_GR = kappa C(P_Z) C(P_X), with the displayed order.
    identity = "IIII"
    quarter_z = {identity: ONE, "IZZI": IUNIT}
    quarter_x = {identity: ONE, "XIXX": IUNIT}
    quarter_product = pauli_sum_product(quarter_z, quarter_x)
    require(
        pauli_sum_scale(2, galindo_rowell_generator(2, 0, kappa))
        == pauli_sum_scale(kappa, quarter_product),
        "ordered Pauli quarter-turn factorization",
    )

    # X_j,Z_j generate the four-qubit Pauli group.  Conjugation by the scalar
    # kappa is invisible, so signed-Pauli output certifies Clifford membership.
    for qubit in range(4):
        for letter in ("X", "Z"):
            word = "I" * qubit + letter + "I" * (3 - qubit)
            image = braid_generator_conjugate({word: ONE}, 2, 0)
            require(len(image) == 1, "Clifford Pauli support")
            (_, coefficient), = image.items()
            require(coefficient in (ONE, -ONE), "Clifford Pauli phase")
    print("[ok] ordered quarter-turn factorization and full Pauli normalization")

    for strand_count in (3, 4):
        for site in range(strand_count - 1):
            target = strand_count - 2 - site
            opposite = galindo_rowell_generator(
                strand_count, site, kappa, opposite=True
            )
            require(
                reverse_tensor_sites(opposite, strand_count)
                == galindo_rowell_generator(strand_count, target, kappa),
                "all-strand tensor reversal",
            )
            require(
                garside_conjugate(
                    galindo_rowell_generator(strand_count, site, kappa),
                    strand_count,
                )
                == galindo_rowell_generator(strand_count, target, kappa),
                "Delta sigma_i Delta^-1 orientation",
            )
            require(
                garside_conjugate(
                    galindo_rowell_generator(strand_count, target, kappa),
                    strand_count,
                    inverse=True,
                )
                == galindo_rowell_generator(strand_count, site, kappa),
                "D^dagger reversal D orientation",
            )
        print(
            f"[ok] exact site-reversal and direct Garside conjugacies for n={strand_count}"
        )

    # These braid words use the literal five-word R_K, not the transported
    # Galindo--Rowell frame.  Positive Artin generators are represented by R.
    r_k, r_k_inverse = literal_five_word_pauli_operators(q, kappa)
    figure_eight_word = [(0, 1), (1, -1)] * 2
    borromean_word = [(0, 1), (1, -1)] * 3
    figure_eight = enhanced_braid_closure_value(
        figure_eight_word, 3, r_k, r_k_inverse, kappa
    )
    borromean = enhanced_braid_closure_value(
        borromean_word, 3, r_k, r_k_inverse, kappa
    )
    require(figure_eight == -4, "figure-eight closure value")
    require(borromean == 2, "Borromean-rings closure value")
    print("[ok] literal five-word closures: figure-eight=-4, Borromean rings=2")


def main():
    q, kappa = verify_local_matrix_consequences()
    verify_global_pauli_consequences(q, kappa)
    print("All global braid-and-link checks passed exactly.")


if __name__ == "__main__":
    main()
