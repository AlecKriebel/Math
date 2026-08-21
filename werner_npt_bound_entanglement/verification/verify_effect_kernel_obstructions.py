#!/usr/bin/env python3
"""Exact audit of the two local effect-kernel obstruction codes.

Only Python's standard library and rational Gaussian arithmetic are used.
The script verifies the endpoint value, the proposed local-kernel basis,
and every entry of the restricted Hessian.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product


@dataclass(frozen=True)
class QC:
    re: Fraction = Fraction(0)
    im: Fraction = Fraction(0)

    def __add__(self, other):
        other = qc(other)
        return QC(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return QC(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-qc(other))

    def __rsub__(self, other):
        return qc(other) - self

    def __mul__(self, other):
        other = qc(other)
        return QC(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = qc(other)
        den = other.re * other.re + other.im * other.im
        return QC(
            (self.re * other.re + self.im * other.im) / den,
            (self.im * other.re - self.re * other.im) / den,
        )

    def conj(self):
        return QC(self.re, -self.im)

    def abs2(self):
        return self.re * self.re + self.im * self.im


def qc(value):
    if isinstance(value, QC):
        return value
    if isinstance(value, Fraction):
        return QC(value)
    return QC(Fraction(value))


ZERO = QC()
ONE = QC(1)
I = QC(0, 1)


def add_entry(matrix, key, value):
    value = qc(value)
    if value == ZERO:
        return
    new_value = matrix.get(key, ZERO) + value
    if new_value == ZERO:
        matrix.pop(key, None)
    else:
        matrix[key] = new_value


def projection(code_vectors):
    """Return sum |u><u|; vector coefficients are unnormalized."""
    out = {}
    for vector in code_vectors:
        norm = sum(value.abs2() for value in vector.values())
        for row, a in vector.items():
            for col, b in vector.items():
                add_entry(out, (row, col), a * b.conj() / norm)
    return out


def partial_trace(matrix, kept):
    kept = tuple(sorted(kept))
    traced = tuple(site for site in range(4) if site not in kept)
    out = {}
    for (row, col), value in matrix.items():
        if all(row[site] == col[site] for site in traced):
            r = tuple(row[site] for site in kept)
            c = tuple(col[site] for site in kept)
            add_entry(out, (r, c), value)
    return out


def trace_product(left, right):
    return sum(
        (value * right.get((col, row), ZERO)
         for (row, col), value in left.items()),
        ZERO,
    )


def right_local_multiply(matrix, local, site=0):
    out = {}
    for (row, mid), value in matrix.items():
        for (z, col_digit), coefficient in local.items():
            if z != mid[site]:
                continue
            col = list(mid)
            col[site] = col_digit
            add_entry(out, (row, tuple(col)), value * coefficient)
    return out


def endpoint(matrix):
    value = ZERO
    for size in range(5):
        coefficient = Fraction(-1, 2) ** (4 - size)
        for kept in combinations(range(4), size):
            reduced = partial_trace(matrix, kept)
            value += coefficient * trace_product(reduced, reduced)
    return value


def effect_hessian(matrix, left, right, site=0):
    p_left = right_local_multiply(matrix, left, site)
    p_right = right_local_multiply(matrix, right, site)
    value = ZERO
    for size in range(5):
        coefficient = Fraction(-1, 2) ** (4 - size)
        for kept in combinations(range(4), size):
            value += coefficient * trace_product(
                partial_trace(p_left, kept),
                partial_trace(p_right, kept),
            )
    return value


def hs_inner(left, right):
    return sum(
        (value.conj() * right.get((row, col), ZERO)
         for (row, col), value in left.items()),
        ZERO,
    )


def local_matrix(diagonal=(), entries=()):
    out = {}
    for index, value in enumerate(diagonal):
        add_entry(out, (index, index), value)
    for row, col, value in entries:
        add_entry(out, (row, col), value)
    return out


def compression_numerator(local, left, right):
    """Unnormalized <left|A_0|right>; zero is normalization-independent."""
    value = ZERO
    for row, a in left.items():
        for col, b in right.items():
            if row[1:] != col[1:]:
                continue
            value += a.conj() * local.get((row[0], col[0]), ZERO) * b
    return value


def assert_kernel(local, code_vectors):
    for left, right in product(code_vectors, repeat=2):
        assert compression_numerator(local, left, right) == ZERO


def word(text):
    return tuple(int(char) for char in text)


def vector(terms):
    return {word(label): qc(value) for label, value in terms}


def audit(code_vectors, kernel, expected_endpoint, expected_eigenvalues):
    p = projection(code_vectors)
    assert endpoint(p) == qc(expected_endpoint)

    for local in kernel:
        assert_kernel(local, code_vectors)

    for i, left in enumerate(kernel):
        norm = hs_inner(left, left)
        assert norm.im == 0 and norm.re > 0
        diagonal = effect_hessian(p, left, left) / norm
        assert diagonal == qc(expected_eigenvalues[i])
        for right in kernel[:i]:
            assert hs_inner(left, right) == ZERO
            assert effect_hessian(p, left, right) == ZERO


def main():
    x02 = local_matrix(entries=((0, 2, 1), (2, 0, 1)))
    y02 = local_matrix(entries=((0, 2, -I), (2, 0, I)))
    x12 = local_matrix(entries=((1, 2, 1), (2, 1, 1)))
    y12 = local_matrix(entries=((1, 2, -I), (2, 1, I)))

    first_code = (
        vector((("1001", 1), ("1022", 1), ("2202", 2))),
        vector((("0022", 2), ("0220", 1))),
    )
    first_kernel = (
        local_matrix(diagonal=(0, -2, 1)),
        x02,
        y02,
        x12,
        y12,
    )
    first_spectrum = (
        Fraction(-1, 18),
        Fraction(1, 12),
        Fraction(1, 12),
        Fraction(-1, 36),
        Fraction(-1, 36),
    )
    audit(first_code, first_kernel, Fraction(121, 450), first_spectrum)
    assert sum(first_spectrum) == Fraction(1, 18)
    assert Fraction(1, 18) > Fraction(121, 450) / 8

    x01 = local_matrix(entries=((0, 1, 1), (1, 0, 1)))
    y01 = local_matrix(entries=((0, 1, -I), (1, 0, I)))
    second_code = (
        vector((("1212", -I), ("0010", 1))),
        vector((
            ("2212", I),
            ("0111", -1 + I),
            ("1111", 1 - I),
        )),
    )
    second_kernel = (
        local_matrix(diagonal=(1, -1, 0)),
        local_matrix(
            diagonal=(0, 0, 4),
            entries=((0, 1, 1), (1, 0, 1)),
        ),
        y01,
        x02,
        y02,
    )
    second_spectrum = (
        Fraction(-7, 160),
        Fraction(-59, 2400),
        Fraction(3, 160),
        Fraction(1, 400),
        Fraction(1, 400),
    )
    audit(second_code, second_kernel, Fraction(163, 400), second_spectrum)
    determinant = Fraction(1)
    for eigenvalue in second_spectrum:
        determinant *= eigenvalue
    assert determinant > 0

    print("effect-kernel exact obstruction audit passed")


if __name__ == "__main__":
    main()
