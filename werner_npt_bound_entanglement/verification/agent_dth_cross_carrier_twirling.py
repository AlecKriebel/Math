#!/usr/bin/env python3
"""Exact audits for the local-unitary reduction of the mixed-PPT DTH cone.

The script uses dependency-free integer/modular arithmetic.  It checks:

* the holomorphic and mixed one-site representation dimensions;
* the common commutant dimension 103;
* exact rank 103 of the five-replica permutation operators in dimension 3;
* preservation of that rank by partial transpose on the first two replicas;
* the three-site commutant size, maximal block sizes, and site-orbit counts.

The modular rank is an exact lower-bound certificate.  The independently
computed representation decomposition gives the matching upper bound 103.
"""

from itertools import combinations_with_replacement, permutations, product
from math import factorial, gcd


PRIME = 1_000_003
LOCAL_DIMENSION = 3
REPLICAS = 5


def partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def hook_product(shape):
    result = 1
    for row, width in enumerate(shape):
        for col in range(width):
            below = sum(1 for lower in shape[row + 1 :] if lower > col)
            right = width - col - 1
            result *= 1 + right + below
    return result


def specht_dimension(shape):
    return factorial(sum(shape)) // hook_product(shape)


def u3_dimension(shape):
    padded = shape + (0,) * (3 - len(shape))
    numerator = 1
    denominator = 1
    for i in range(3):
        for j in range(i + 1, 3):
            numerator *= padded[i] - padded[j] + j - i
            denominator *= j - i
    assert numerator % denominator == 0
    return numerator // denominator


def su3_dimension(weight):
    p, q = weight
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def digits(number, base=LOCAL_DIMENSION, length=REPLICAS):
    out = [0] * length
    for position in range(length - 1, -1, -1):
        out[position] = number % base
        number //= base
    return tuple(out)


def index(word, base=LOCAL_DIMENSION):
    result = 0
    for letter in word:
        result = base * result + letter
    return result


WORDS = [digits(number) for number in range(LOCAL_DIMENSION**REPLICAS)]
WORD_INDEX = {word: number for number, word in enumerate(WORDS)}
MATRIX_SIDE = len(WORDS)


def permutation_operator(permutation):
    """Sparse vectorization of P_pi, with row word[i]=column word[pi[i]]."""
    out = {}
    for column, word in enumerate(WORDS):
        row_word = tuple(word[permutation[position]] for position in range(REPLICAS))
        row = WORD_INDEX[row_word]
        out[row * MATRIX_SIDE + column] = 1
    return out


def partial_transpose_first_pair(operator):
    out = {}
    for coordinate, coefficient in operator.items():
        row, column = divmod(coordinate, MATRIX_SIDE)
        row_word = WORDS[row]
        column_word = WORDS[column]
        new_row_word = column_word[:2] + row_word[2:]
        new_column_word = row_word[:2] + column_word[2:]
        new_coordinate = (
            WORD_INDEX[new_row_word] * MATRIX_SIDE + WORD_INDEX[new_column_word]
        )
        out[new_coordinate] = out.get(new_coordinate, 0) + coefficient
    return {key: value for key, value in out.items() if value}


def sparse_modular_rank(columns, prime=PRIME):
    """Column rank over F_prime by sparse pivot elimination."""
    pivots = {}
    rank = 0
    for original in columns:
        vector = {key: value % prime for key, value in original.items() if value % prime}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {
                    key: (value * inverse) % prime
                    for key, value in vector.items()
                    if (value * inverse) % prime
                }
                pivots[pivot] = vector
                rank += 1
                break
            scale = vector[pivot]
            old = pivots[pivot]
            for key, value in old.items():
                new_value = (vector.get(key, 0) - scale * value) % prime
                if new_value:
                    vector[key] = new_value
                else:
                    vector.pop(key, None)
    return rank


def multiset_count(types, sites):
    # Number of multisets of size sites drawn from types.
    return factorial(types + sites - 1) // (factorial(sites) * factorial(types - 1))


def sparse_add(left, right, right_scale=1):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, 0) + right_scale * value
        if not out[key]:
            del out[key]
    return out


def target_words():
    return list(product(range(3), repeat=3))


TARGET_WORDS = target_words()
TARGET_INDEX = {word: position for position, word in enumerate(TARGET_WORDS)}


def target_identity():
    return {(position, position): 1 for position in range(27)}


def target_swap():
    out = {}
    for column, (a, b, c) in enumerate(TARGET_WORDS):
        out[(TARGET_INDEX[(b, a, c)], column)] = 1
    return out


def target_contraction_second_third():
    out = {}
    for column, (a, b, c) in enumerate(TARGET_WORDS):
        if b == c:
            for k in range(3):
                out[(TARGET_INDEX[(a, k, k)], column)] = 1
    return out


def conjugate_by_target_swap(operator, left=False, right=False):
    """Multiply an integer sparse matrix by s on the requested sides."""
    out = {}
    for (row, column), value in operator.items():
        row_word = TARGET_WORDS[row]
        column_word = TARGET_WORDS[column]
        if left:
            row_word = (row_word[1], row_word[0], row_word[2])
        if right:
            column_word = (column_word[1], column_word[0], column_word[2])
        key = (TARGET_INDEX[row_word], TARGET_INDEX[column_word])
        out[key] = out.get(key, 0) + value
    return {key: value for key, value in out.items() if value}


def real_trace_transpose_product(left, right):
    # Tr(left^T right) for real matrices.
    return sum(value * right.get(key, 0) for key, value in left.items())


def gaussian_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gaussian_mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_scale(value, scalar):
    return (scalar * value[0], scalar * value[1])


def gaussian_phase(exponent):
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[exponent % 4]


def target_local_basis():
    """Return real parts and i-phases of I,s,e,ses,se+es,i(se-es)."""
    identity = target_identity()
    swap = target_swap()
    e = target_contraction_second_third()
    ses = conjugate_by_target_swap(e, left=True, right=True)
    se = conjugate_by_target_swap(e, left=True)
    es = conjugate_by_target_swap(e, right=True)
    symmetric = sparse_add(se, es)
    skew = sparse_add(se, es, -1)
    return [identity, swap, e, ses, symmetric, skew], [0, 0, 0, 0, 0, 1]


def target_trace_table():
    basis, phases = target_local_basis()
    table = {}
    for first in range(6):
        for second in range(6):
            for left_swap in range(2):
                for right_swap in range(2):
                    transformed = conjugate_by_target_swap(
                        basis[second], bool(left_swap), bool(right_swap)
                    )
                    real_trace = real_trace_transpose_product(
                        basis[first], transformed
                    )
                    # The dagger conjugates the phase on the first factor.
                    phase = gaussian_phase(phases[second] - phases[first])
                    table[(first, second, left_swap, right_swap)] = (
                        real_trace * phase[0],
                        real_trace * phase[1],
                    )
    return table


def distinct_permutations(word):
    return sorted(set(permutations(word)))


def compressed_target_gram(monomials):
    """Gram of P_- T P_- for site-symmetric target monomials.

    P_-=(I-s tensor s tensor s)/2.  Every result is a Gaussian integer;
    Hermiticity forces the imaginary part to vanish.
    """
    table = target_trace_table()
    gram = []
    for left_word in monomials:
        row = []
        for right_word in monomials:
            numerator = (0, 0)
            for left_term in distinct_permutations(left_word):
                for right_term in distinct_permutations(right_word):
                    for left_swap, right_swap, sign in (
                        (0, 0, 1),
                        (1, 0, -1),
                        (0, 1, -1),
                        (1, 1, 1),
                    ):
                        value = (1, 0)
                        for first, second in zip(left_term, right_term):
                            value = gaussian_mul(
                                value,
                                table[(first, second, left_swap, right_swap)],
                            )
                        numerator = gaussian_add(
                            numerator, gaussian_scale(value, sign)
                        )
            assert numerator[0] % 4 == 0 and numerator[1] % 4 == 0
            value = (numerator[0] // 4, numerator[1] // 4)
            assert value[1] == 0
            row.append(value[0])
        gram.append(row)
    return gram


def dense_modular_rank(matrix, prime=PRIME):
    columns = []
    if not matrix:
        return 0
    for column in range(len(matrix[0])):
        columns.append(
            {
                row: matrix[row][column] % prime
                for row in range(len(matrix))
                if matrix[row][column] % prime
            }
        )
    return sparse_modular_rank(columns, prime)


def dense_modular_independent_columns(matrix, prime=PRIME):
    pivots = {}
    independent = []
    for column in range(len(matrix[0])):
        vector = {
            row: matrix[row][column] % prime
            for row in range(len(matrix))
            if matrix[row][column] % prime
        }
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {
                    key: value * inverse % prime
                    for key, value in vector.items()
                    if value * inverse % prime
                }
                pivots[pivot] = vector
                independent.append(column)
                break
            scale = vector[pivot]
            old = pivots[pivot]
            for key, value in old.items():
                new_value = (vector.get(key, 0) - scale * value) % prime
                if new_value:
                    vector[key] = new_value
                else:
                    vector.pop(key, None)
    return independent


def main():
    holomorphic = []
    for shape in partitions(5):
        if len(shape) <= 3:
            holomorphic.append(
                (shape, u3_dimension(shape), specht_dimension(shape))
            )

    expected_holomorphic = [
        ((5,), 21, 1),
        ((4, 1), 24, 4),
        ((3, 2), 15, 5),
        ((3, 1, 1), 6, 6),
        ((2, 2, 1), 3, 5),
    ]
    assert holomorphic == expected_holomorphic
    assert sum(dimension * multiplicity for _, dimension, multiplicity in holomorphic) == 3**5
    holomorphic_commutant = sum(
        multiplicity**2 for _, _, multiplicity in holomorphic
    )
    assert holomorphic_commutant == 103

    mixed_weights = [
        ((3, 2), 1),
        ((2, 1), 6),
        ((1, 0), 6),
        ((1, 3), 2),
        ((0, 2), 5),
        ((4, 0), 1),
    ]
    mixed = [
        (weight, su3_dimension(weight), multiplicity)
        for weight, multiplicity in mixed_weights
    ]
    assert [dimension for _, dimension, _ in mixed] == [42, 15, 3, 24, 6, 15]
    assert sum(dimension * multiplicity for _, dimension, multiplicity in mixed) == 3**5
    mixed_commutant = sum(multiplicity**2 for _, _, multiplicity in mixed)
    assert mixed_commutant == 103

    operators = [permutation_operator(pi) for pi in permutations(range(5))]
    rank_holomorphic = sparse_modular_rank(operators)
    assert rank_holomorphic == 103

    mixed_operators = [partial_transpose_first_pair(operator) for operator in operators]
    # Partial transpose is exactly involutive.
    assert all(
        partial_transpose_first_pair(mixed_operator) == operator
        for operator, mixed_operator in zip(operators, mixed_operators)
    )
    rank_mixed = sparse_modular_rank(mixed_operators)
    assert rank_mixed == 103

    assert holomorphic_commutant**3 == 1_092_727
    assert max(multiplicity for _, _, multiplicity in holomorphic) ** 3 == 216
    assert max(multiplicity for _, _, multiplicity in mixed) ** 3 == 216
    assert multiset_count(5, 3) == 35
    assert multiset_count(6, 3) == 56

    # Exact target-side support-ideal counts.
    target_irreps = [((2, 1), 1), ((1, 0), 2), ((0, 2), 1)]
    assert sum(su3_dimension(weight) * multiplicity for weight, multiplicity in target_irreps) == 27
    assert sum(multiplicity**2 for _, multiplicity in target_irreps) == 6
    assert 6**3 == 216

    all_target_monomials = list(combinations_with_replacement(range(6), 3))
    real_target_monomials = [
        word for word in all_target_monomials if word.count(5) % 2 == 0
    ]
    assert len(all_target_monomials) == 56
    assert len(real_target_monomials) == 40
    full_target_gram = compressed_target_gram(all_target_monomials)
    real_target_gram = compressed_target_gram(real_target_monomials)
    assert dense_modular_rank(full_target_gram) == 16
    assert dense_modular_rank(real_target_gram) == 14
    effective_real_monomials = [
        real_target_monomials[index]
        for index in dense_modular_independent_columns(real_target_gram)
    ]
    assert effective_real_monomials == [
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 2),
        (0, 0, 4),
        (0, 1, 2),
        (0, 2, 2),
        (0, 2, 3),
        (0, 2, 4),
        (0, 4, 4),
        (0, 5, 5),
        (2, 2, 2),
        (2, 2, 3),
        (2, 2, 4),
        (2, 3, 4),
    ]

    # General equivariant affine support intertwiners.
    local_affine_intertwiners = 6 * 1 + 6 * 2 + 5 * 1
    assert local_affine_intertwiners == 23
    assert multiset_count(23, 3) == 2300

    print("exact DTH cross-carrier twirling audit passed")
    print("holomorphic local types:", holomorphic)
    print("mixed local types:", mixed)
    print("local commutant ranks:", rank_holomorphic, rank_mixed)
    print("three-site commutant dimension:", holomorphic_commutant**3)
    print("site-permutation type orbits: 35 holomorphic, 56 mixed")
    print("quadratic support-ideal parameters: 216 -> 40 -> effective rank 14")
    print("general affine support intertwiners: 23 local, 2300 site-symmetric")


if __name__ == "__main__":
    main()
