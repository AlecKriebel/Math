"""Independent elementary check reconstructed directly from pinned PROOF.md.

Does not import or execute any original program or consume its certificate.
No claim to compute a link signature is made by this script.
The default replay writes JSON to stdout only; it never rewrites the sealed output.
"""
from collections import Counter
import argparse
import json


def inverse(word):
    return [-letter for letter in word[::-1]]


def commutator(left, right):
    return left + right + inverse(left) + inverse(right)


def reduce_word(word):
    result = []
    for letter in word:
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return result


def calculate():
    a, b = [1, 1], [2, 2]
    c = commutator(a, b)
    d, e = inverse(a) + c + a, inverse(b) + c + b
    u, v = commutator(c, d), commutator(d, e)
    word = reduce_word(commutator(u, v))
    A = [2, -4, 2, 2, -2, 2, -4, 2, 2, -2, -2, 4, -2, -2, 4, -2, 2, -2, -2, 4, -2, -2, 2]
    B = [2, -2, 2, -2, -2, 2, 2, -2, -2, 4, -2, 2, -2, 2, -2, -2, 2, 2, -2, -2, 2, 2, -2]
    listed = [letter for aa, bb in zip(A, B)
              for generator, exponent in [(1, aa), (2, bb)]
              for letter in [generator if exponent > 0 else -generator] * abs(exponent)]
    labels = [0, 1, 2]
    crossings = Counter({(0, 1): 0, (0, 2): 0, (1, 2): 0})
    matrix = [[1, 0], [0, 1]]
    generators = {1: [[1, 0], [-1, 1]], -1: [[1, 0], [1, 1]],
                  2: [[1, 1], [0, 1]], -2: [[1, -1], [0, 1]]}
    for letter in word:
        i = abs(letter) - 1
        pair = tuple(sorted(labels[i:i + 2]))
        crossings[pair] += 1 if letter > 0 else -1
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
        right = generators[letter]
        matrix = [[sum(matrix[i][k] * right[k][j] for k in range(2))
                   for j in range(2)] for i in range(2)]
    return {
        "method": "independent free reduction, strand labels, integer 2x2 multiplication",
        "signature_computation_performed": False,
        "reduced_length": len(word), "listed_word_length": len(listed),
        "listed_word_equals_reduced_nested_word": listed == word,
        "sums": [sum(A), sum(B)], "sum_abs_B": sum(map(abs, B)),
        "all_abs_B_at_least_two": all(abs(x) >= 2 for x in B),
        "pure_permutation": labels,
        "signed_pair_crossings": {str(k): crossings[k] for k in sorted(crossings)},
        "pairwise_linking_numbers": {str(k): crossings[k] // 2 for k in sorted(crossings)},
        "burau": matrix,
        "burau_det": matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0],
    }


def verify(result, expected_reduced_length=104):
    """Fail closed in every Python optimization mode, before emitting output."""
    if result["listed_word_equals_reduced_nested_word"] is not True:
        raise ValueError("listed word does not equal reduced nested word")
    if result["reduced_length"] != expected_reduced_length:
        raise ValueError(
            f"reduced length mismatch: expected {expected_reduced_length}, "
            f"got {result['reduced_length']}"
        )
    if result["pure_permutation"] != [0, 1, 2]:
        raise ValueError("strand permutation is not the identity")
    if set(result["pairwise_linking_numbers"].values()) != {0}:
        raise ValueError("pairwise linking numbers are not all zero")
    if result["burau_det"] != 1:
        raise ValueError("Burau determinant is not one")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expected-reduced-length", type=int, default=104,
        help="expected length to validate; defaults to the pinned claim's 104",
    )
    arguments = parser.parse_args()
    result = calculate()
    verify(result, expected_reduced_length=arguments.expected_reduced_length)
    print(json.dumps(result, indent=2))
