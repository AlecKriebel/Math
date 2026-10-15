#!/usr/bin/env python3
"""Independent exact probes over Z[q,u,u^-1]; no external dependencies.

These finite checks corroborate, but do not replace, the all-index proof.
"""
from fractions import Fraction
import json
from datetime import datetime, timezone
from pathlib import Path


class Laurent:
    def __init__(self, terms=None):
        if isinstance(terms, int):
            terms = {(0, 0): terms}
        self.terms = {e: int(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Laurent) else Laurent(value)

    def __add__(self, other):
        terms = dict(self.terms)
        for e, c in self.coerce(other).terms.items():
            terms[e] = terms.get(e, 0) + c
        return Laurent(terms)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        terms = {}
        for (a, b), c in self.terms.items():
            for (d, e), f in self.coerce(other).terms.items():
                exponent = (a + d, b + e)
                terms[exponent] = terms.get(exponent, 0) + c * f
        return Laurent(terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        if power < 0:
            assert len(self.terms) == 1
            ((a, b), c), = self.terms.items()
            assert c in (1, -1)
            return Laurent({(a * power, b * power): c ** power})
        result = Laurent(1)
        for _ in range(power):
            result = result * self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def evaluate(self, qvalue, uvalue):
        qvalue, uvalue = Fraction(qvalue), Fraction(uvalue)
        return sum((c * qvalue ** a * uvalue ** b
                    for (a, b), c in self.terms.items()), Fraction(0))

    def substitute_u_power(self, power):
        terms = {}
        for (a, b), c in self.terms.items():
            exponent = (a + power * b, 0)
            terms[exponent] = terms.get(exponent, 0) + c
        return Laurent(terms)

    def json_terms(self):
        return [[a, b, c] for (a, b), c in sorted(self.terms.items())]


ZERO = Laurent()
ONE = Laurent(1)
Q = Laurent({(1, 0): 1})
U = Laurent({(0, 1): 1})


def identity(size):
    return [[ONE if i == j else ZERO for j in range(size)] for i in range(size)]


def add(a, b):
    return [[x + y for x, y in zip(arow, brow)] for arow, brow in zip(a, b)]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def subtract(a, b):
    return add(a, scale(-1, b))


def multiply(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def is_zero(matrix):
    return all(entry == ZERO for row in matrix for entry in row)


def braid_matrices(size):
    positive, negative = {}, {}
    for i in range(1, size):
        matrix = identity(size)
        matrix[i-1][i-1], matrix[i-1][i] = 1 - U, U
        matrix[i][i-1], matrix[i][i] = ONE, ZERO
        positive[i] = matrix
        matrix = identity(size)
        matrix[i-1][i-1], matrix[i-1][i] = ZERO, ONE
        matrix[i][i-1], matrix[i][i] = U ** -1, 1 - U ** -1
        negative[i] = matrix
    return positive, negative


def word(indices, matrices, size):
    result = identity(size)
    for i in indices:
        result = multiply(result, matrices[i])
    return result


def whole_word_inverse(indices, inverse_matrices, size):
    # Reverse the complete word, then invert every generator.
    return word(list(reversed(indices)), inverse_matrices, size)


def expected_x(index, size):
    coefficient = ONE
    for j in range(1, index):
        coefficient *= Q ** j - U
    result = [[ZERO for _ in range(size)] for _ in range(size)]
    # v_(index-1) times lambda, lambda=(-1,1,0,...).
    result[index-2][0] = -coefficient * U ** (2-index)
    result[index-2][1] = coefficient * U ** (2-index)
    result[index-1][0] = coefficient * U ** (1-index)
    result[index-1][1] = -coefficient * U ** (1-index)
    return result


checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


cases = []
models = {}
for m in range(3, 11):
    positive, negative = braid_matrices(m)
    ident = identity(m)
    for i in range(1, m):
        check(multiply(positive[i], negative[i]) == ident, f"inverse right m={m},i={i}")
        check(multiply(negative[i], positive[i]) == ident, f"inverse left m={m},i={i}")
    for i in range(1, m-1):
        check(word([i, i+1, i], positive, m) == word([i+1, i, i+1], positive, m),
              f"braid m={m},i={i}")
    for i in range(1, m):
        for j in range(i+2, m):
            check(word([i, j], positive, m) == word([j, i], positive, m),
                  f"disjoint m={m},i={i},j={j}")
    x = {2: subtract(add(scale(Q, negative[1]), scale(1-Q, ident)), positive[1])}
    for k in range(3, m+1):
        descending = list(range(k-1, 0, -1))
        ascending = list(range(1, k))
        inverse = whole_word_inverse(descending, negative, m)
        check(multiply(word(descending, positive, m), inverse) == ident,
              f"whole-word inverse m={m},k={k}")
        x[k] = multiply(subtract(scale(Q ** (k-1), inverse), word(ascending, positive, m)), x[k-1])
    for k in range(2, m+1):
        check(x[k] == expected_x(k, m), f"rank-one formula m={m},k={k}")
        check(all(a >= 0 for row in x[k] for entry in row for a, b in entry.terms),
              f"Laurent model needs no q inverse m={m},k={k}")
    first_left = subtract(add(scale(Q, negative[2]), scale(1-Q, ident)), positive[2])
    first_right = subtract(scale(Q, whole_word_inverse([2, 1], negative, m)), word([1, 2], positive, m))
    check(is_zero(multiply(subtract(first_left, first_right), x[2])), f"R2 m={m}")
    for k in range(3, m):
        left = subtract(scale(Q ** (k-1), whole_word_inverse(list(range(k, 1, -1)), negative, m)),
                        word(list(range(2, k+1)), positive, m))
        right = subtract(scale(Q ** (k-1), whole_word_inverse(list(range(k, 0, -1)), negative, m)),
                         word(list(range(1, k+1)), positive, m))
        check(is_zero(multiply(subtract(left, right), x[k])), f"R{k} m={m}")
    check(multiply(positive[1], x[2]) == scale(-U, x[2]), f"sigma1 twist m={m}")
    full_twist = word([1, 2, 1, 2, 1, 2], positive, m)
    check(multiply(full_twist, x[3]) == scale(U ** 3, x[3]), f"three-strand twist m={m}")
    for power, must_vanish in [(1, True), (2, True), (3, False)]:
        specialized = [[entry.substitute_u_power(power) for entry in row] for row in x[3]]
        check(is_zero(specialized) == must_vanish, f"X3 u=q^{power} m={m}")
    check(is_zero([[entry.substitute_u_power(1) for entry in row] for row in x[2]]),
          f"X2 u=q m={m}")
    if m >= 4:
        check(is_zero([[entry.substitute_u_power(3) for entry in row] for row in x[4]]),
              f"X4 u=q^3 m={m}")
    cases.append({"strands": m, "legal_rows": list(range(2, m)),
                  "A_n": m, "C_n": m-1 if m >= 4 else None})
    models[m] = (positive, negative, x)


positive, negative, x = models[3]
ident = identity(3)
correct_left = subtract(add(scale(Q, negative[2]), scale(1-Q, ident)), positive[2])
wrong_right = subtract(scale(Q, word([2, 1], negative, 3)), word([1, 2], positive, 3))
wrong_order_defect = multiply(subtract(correct_left, wrong_right), x[2])
check(not is_zero(wrong_order_defect), "wrong inverse order must be detected")
correct_right = subtract(scale(Q, whole_word_inverse([2, 1], negative, 3)), word([1, 2], positive, 3))
uniform_left = subtract(scale(Q, negative[2]), positive[2])
missing_constant_defect = multiply(subtract(uniform_left, correct_right), x[2])
check(not is_zero(missing_constant_defect), "missing exceptional constant must be detected")
check(missing_constant_defect == scale(Q-1, x[2]), "missing constant exact defect")


def evaluated(matrix, qvalue, uvalue):
    return [[str(entry.evaluate(qvalue, uvalue)) for entry in row] for row in matrix]


results = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "implementation": "Independent sparse integer Laurent-polynomial arithmetic; standard library only",
    "coefficient_ring": "Z[q,u,u^-1]",
    "symbolic_assertions": checks,
    "finite_symbolic_cases": cases,
    "negative_control_q2_u3": {
        "wrong_inverse_order_R2": evaluated(wrong_order_defect, 2, 3),
        "missing_R2_constant": evaluated(missing_constant_defect, 2, 3),
        "correct_X3": evaluated(x[3], 2, 3),
    },
    "X3_at_q2_u8": evaluated(x[3], 2, 8),
    "X3_at_q1_u1": evaluated(x[3], 1, 1),
    "X3_at_q_minus1_u_minus1": evaluated(x[3], -1, -1),
    "X3_nonzero_entry_symbolic": x[3][1][0].json_terms(),
    "limits": "Finite matrix checks supplement the all-index derivation in REPORT.md. They do not repair the literal source or bound universal quotients with extra relations."
}
Path(__file__).with_name("probe_results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({"symbolic_assertions": checks, "status": "pass", "strands": [3, 10]}))
