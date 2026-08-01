#!/usr/bin/env python3
"""Exact, dependency-free audit of the five-replica Omega constraint.

The calculation is done in the raw qutrit tensor basis.  In particular, it
does not use numerical Schur--Weyl matrices or representation labels.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations


SiteWord = tuple[int, int, int, int, int]
Key = tuple[SiteWord, SiteWord, SiteWord]
Vector = dict[Key, int]


def add_term(vector, key, value):
    if value:
        vector[key] += value
        if vector[key] == 0:
            del vector[key]


def point_word(position: int) -> SiteWord:
    word = [0] * 5
    word[position] = 1
    return tuple(word)


def pair_word(first: int, second: int) -> SiteWord:
    word = [0] * 5
    word[first] = word[second] = 1
    return tuple(word)


def linear_combination(*terms):
    result = defaultdict(int)
    for coefficient, word in terms:
        add_term(result, word, coefficient)
    return dict(result)


def f(index: int):
    return linear_combination(
        (1, point_word(index)),
        (-1, point_word(4)),
    )


def rectangle(a: int, b: int, c: int, d: int):
    return linear_combination(
        (1, pair_word(a, c)),
        (-1, pair_word(a, d)),
        (-1, pair_word(b, c)),
        (1, pair_word(b, d)),
    )


def add_tensor_product(output, left, middle, right, coefficient=1):
    for left_word, left_value in left.items():
        for middle_word, middle_value in middle.items():
            for right_word, right_value in right.items():
                add_term(
                    output,
                    (left_word, middle_word, right_word),
                    coefficient * left_value * middle_value * right_value,
                )


def obstruction_vector() -> Vector:
    """Return the integer vector xi from the cloud handoff."""

    xi = defaultdict(int)
    for index in (1, 3):
        add_tensor_product(
            xi, f(index), f(index), rectangle(0, 1, 2, 3), -1
        )
    add_tensor_product(xi, f(3), f(3), rectangle(0, 1, 2, 4), 1)
    add_tensor_product(xi, f(2), f(2), rectangle(0, 1, 2, 4), -1)
    add_tensor_product(xi, f(1), f(1), rectangle(0, 4, 2, 3), 1)
    add_tensor_product(xi, f(0), f(0), rectangle(0, 4, 2, 3), -1)
    return dict(xi)


def inner(left, right):
    return sum(value * right.get(key, 0) for key, value in left.items())


def norm_squared(vector):
    return inner(vector, vector)


def permute_replicas(vector, permutation):
    """Apply one simultaneous permutation to all three physical sites."""

    result = defaultdict(int)
    for key, value in vector.items():
        new_key = tuple(
            tuple(site_word[permutation[j]] for j in range(5))
            for site_word in key
        )
        add_term(result, new_key, value)
    return dict(result)


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def fourfold_antisymmetrize(vector):
    result = defaultdict(F)
    for permutation in permutations(range(4)):
        extended = permutation + (4,)
        sign = permutation_sign(permutation)
        for key, value in permute_replicas(vector, extended).items():
            add_term(result, key, F(sign * value, 24))
    return dict(result)


def epsilon(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    return permutation_sign((i, j, k))


def raw_omega_contraction(vector, contracted_pair):
    """Apply the unnormalized epsilon contraction E_pair,5.

    The two uncontracted positions among replicas 1,...,4 form the output
    bivector.  The actual scalar Omega functional is -2^(-3/2) times this
    map.  Output keys have two entries at each physical site.
    """

    remaining = [index for index in range(4) if index not in contracted_pair]
    result = defaultdict(int)
    for key, value in vector.items():
        factor = 1
        output_key = []
        for site_word in key:
            factor *= epsilon(
                site_word[4],
                site_word[contracted_pair[0]],
                site_word[contracted_pair[1]],
            )
            output_key.append(
                (site_word[remaining[0]], site_word[remaining[1]])
            )
        add_term(result, tuple(output_key), value * factor)
    return dict(result)


def sqrt2_times_c_omega(vector):
    """Return sqrt(2) C_Omega(vector) with either output pair identified.

    Since C_Omega is the average of two contractions and
    Omega=-E/(2 sqrt(2)), the exact rational prefactor here is -1/4.
    """

    result = defaultdict(F)
    for contracted_pair in ((0, 1), (2, 3)):
        for key, value in raw_omega_contraction(
            vector, contracted_pair
        ).items():
            add_term(result, key, -F(value, 4))
    return dict(result)


def swap_at_site(key, site: int, first: int, second: int):
    result = list(key)
    word = list(result[site])
    word[first], word[second] = word[second], word[first]
    result[site] = tuple(word)
    return tuple(result)


def product_antisymmetrizer_expectation(vector, first: int, second: int):
    """Expectation of product_i (I-F_first,second^(i))/2."""

    answer = F(0)
    for mask in range(8):
        permuted = defaultdict(int)
        sign = -1 if mask.bit_count() % 2 else 1
        for key, value in vector.items():
            new_key = key
            for site in range(3):
                if (mask >> site) & 1:
                    new_key = swap_at_site(
                        new_key, site, first, second
                    )
            add_term(permuted, new_key, value)
        answer += F(sign, 8) * inner(vector, permuted)
    return answer


def physical_test_vector():
    """Build (w tensor w) tensor z for an unnormalized decomposable w.

    Here w=|000>|111>-|111>|000> and z=|222>.  For this convention
    Tr(D_z W)=-1/sqrt(2).  Hence sqrt(2) C_Omega(eta)=-w.
    """

    zero = (0, 0, 0)
    one = (1, 1, 1)
    two = (2, 2, 2)
    w = {(zero, one): 1, (one, zero): -1}
    eta = defaultdict(int)
    for (a, b), first_value in w.items():
        for (c, d), second_value in w.items():
            key = tuple(
                (a[site], b[site], c[site], d[site], two[site])
                for site in range(3)
            )
            add_term(eta, key, first_value * second_value)
    expected = {
        tuple((zero[site], one[site]) for site in range(3)): F(-1),
        tuple((one[site], zero[site]) for site in range(3)): F(1),
    }
    return dict(eta), expected


xi = obstruction_vector()
assert len(xi) == 52
assert norm_squared(xi) == 64

# Pair antisymmetry and pair-exchange symmetry.
f12_xi = permute_replicas(xi, (1, 0, 2, 3, 4))
f34_xi = permute_replicas(xi, (0, 1, 3, 2, 4))
pair_exchange_xi = permute_replicas(xi, (2, 3, 0, 1, 4))
assert f12_xi == {key: -value for key, value in xi.items()}
assert f34_xi == {key: -value for key, value in xi.items()}
assert pair_exchange_xi == xi

# First Plucker compatibility.
assert fourfold_antisymmetrize(xi) == {}

# Each Omega half-map vanishes separately, hence so does C_Omega.
assert raw_omega_contraction(xi, (0, 1)) == {}
assert raw_omega_contraction(xi, (2, 3)) == {}
assert sqrt2_times_c_omega(xi) == {}

# Check the normalization of C_Omega on a physical monomial.
physical_eta, physical_expected = physical_test_vector()
assert sqrt2_times_c_omega(physical_eta) == physical_expected

# Exact minimal-DTH witness calculation.
norm_xi = F(norm_squared(xi))
antisymmetric_125 = product_antisymmetrizer_expectation(xi, 0, 4)
antisymmetric_345 = product_antisymmetrizer_expectation(xi, 2, 4)
assert antisymmetric_125 == 16
assert antisymmetric_345 == 16
o0_125 = norm_xi / 4 - 2 * antisymmetric_125
o0_345 = norm_xi / 4 - 2 * antisymmetric_345
o0_lifted = (o0_125 + o0_345) / 2
assert o0_125 == -16
assert o0_345 == -16
assert o0_lifted == -16
assert o0_lifted / norm_xi == -F(1, 4)

print("verified exact five-replica Omega lift and cloud obstruction")
print("support(xi) = 52, norm^2(xi) = 64")
print("A4 xi = 0 and C_Omega xi = 0 (both Omega halves vanish)")
print("<xi, O0_tilde xi> = -16, quotient = -1/4")
