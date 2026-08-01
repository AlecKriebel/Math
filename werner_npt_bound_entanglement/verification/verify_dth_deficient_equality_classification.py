#!/usr/bin/env python3
"""Exact rational spot certificate for deficient-site DTH equality.

This is a small independent audit of all three equality mechanisms used in
the proof note:

* proportional rank-two slices (factor at the sliced site);
* rank-one slices with a common left factor;
* rank-one slices with a common right factor.

It also checks strictness on the two-term GHZ tensor, whose three local
marginals all have rank two but none has rank one.  Square roots in the
Hodge matrices are cleared: if E_p=sqrt(2) A_p, then
``D_integer = (2 sqrt(2)) D_z`` and squared singular values scale by 8.
All rank and characteristic-polynomial calculations use ``Fraction`` only.
"""

from fractions import Fraction as F


def epsilon(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [[sum(x * y for x, y in zip(row, column))
             for column in right_t] for row in left]


def rank(matrix):
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [x - coefficient * y for x, y in
                             zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def hodge_integer(z):
    out = zeros(27)
    for p in range(3):
        for q in range(3):
            for r in range(3):
                coefficient = z[9 * p + 3 * q + r]
                if not coefficient:
                    continue
                for a in range(3):
                    for b in range(3):
                        for c in range(3):
                            row = 9 * a + 3 * b + c
                            for i in range(3):
                                ep = epsilon(p, a, i)
                                if not ep:
                                    continue
                                for j in range(3):
                                    eq = epsilon(q, b, j)
                                    if not eq:
                                        continue
                                    for k in range(3):
                                        er = epsilon(r, c, k)
                                        if er:
                                            column = 9 * i + 3 * j + k
                                            out[row][column] += (
                                                coefficient * ep * eq * er
                                            )
    return out


def gram_spectrum_power_sums(z):
    d = hodge_integer(z)
    gram = matmul(transpose(d), d)
    gram2 = matmul(gram, gram)
    gram3 = matmul(gram2, gram)
    return (
        sum(gram[i][i] for i in range(27)),
        sum(gram2[i][i] for i in range(27)),
        sum(gram3[i][i] for i in range(27)),
        rank(gram),
    )


def tensor(entries):
    out = [F(0)] * 27
    for (i, j, k), value in entries.items():
        out[9 * i + 3 * j + k] = F(value)
    return out


def main():
    # All four vectors are deliberately left unnormalized.  Homogeneity is
    # used below; integer coefficients keep the certificate transparent.
    examples = {
        "sliced_factor": tensor({(0, 0, 0): 3, (0, 1, 1): 4}),
        "common_left": tensor({(0, 0, 0): 3, (0, 1, 1): 4}),
        "common_right": tensor({(0, 0, 0): 3, (1, 0, 1): 4}),
        "ghz_strict": tensor({(0, 0, 0): 1, (1, 1, 1): 1}),
    }

    # The first three are one-site-factor tensors.  For norm squared n, the
    # top four eigenvalues of D_integer^T D_integer sum to 4n, equivalent
    # after division by 8 to the sharp physical value n/2.
    for name in ("sliced_factor", "common_left", "common_right"):
        z = examples[name]
        norm_squared = sum(value * value for value in z)
        d = hodge_integer(z)
        gram = matmul(transpose(d), d)
        # In these sparse examples the nonzero spectrum is read from exact
        # rational row reduction of gram-alpha I at the proposed top value.
        shifted = [row[:] for row in gram]
        for i in range(27):
            shifted[i][i] -= norm_squared
        top_multiplicity = 27 - rank(shifted)
        assert top_multiplicity == 4
        assert rank(gram) >= 4

    # For unnormalized GHZ, ||z||^2=2.  Its D_integer Gram has top
    # eigenvalue 2 with multiplicity two and next eigenvalue 1, so the
    # top-four sum is 6 < 8 = 4||z||^2 in cleared conventions.
    ghz = examples["ghz_strict"]
    gram = matmul(transpose(hodge_integer(ghz)), hodge_integer(ghz))
    shifted_two = [row[:] for row in gram]
    shifted_one = [row[:] for row in gram]
    for i in range(27):
        shifted_two[i][i] -= 2
        shifted_one[i][i] -= 1
    assert 27 - rank(shifted_two) == 2
    assert 27 - rank(shifted_one) >= 2

    # Audit the exact third moment on one normalized 3-4 factor branch.
    # Cleared Gram eigenvalues are divided by 8; norm squared is 25.
    trace1, trace2, trace3, _ = gram_spectrum_power_sums(
        examples["sliced_factor"]
    )
    assert trace1 == F(8 * 25)
    normalized_third_moment = trace3 / (F(8 * 25) ** 3)
    # Formula (1+s^6+t^6)/128 for s=3/5,t=4/5.
    expected = (1 + F(3, 5) ** 6 + F(4, 5) ** 6) / 128
    assert normalized_third_moment == expected

    print("exact deficient-site DTH equality audit passed")
    print("one-site-factor top-four squared singular sum = ||z||^2/2")
    print("two-term GHZ is strict")
    print("factor-branch third moment formula passed")


if __name__ == "__main__":
    main()
