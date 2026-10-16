#!/usr/bin/env python3
"""Dependency-free exact controls in Q(sqrt(2),sqrt(3),sqrt(5)).

This checks the finite matrices in DERIVATION.md. It does not replace the
proofs of continuity, the GNS factorization, or the generator obstruction.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

PRIMES = (2, 3, 5)


class R:
    def __init__(self, value=0):
        if isinstance(value, R):
            self.v = dict(value.v)
        elif isinstance(value, dict):
            self.v = {k: F(v) for k, v in value.items() if v}
        else:
            self.v = {0: F(value)} if value else {}

    def __add__(self, other):
        result = dict(self.v)
        for k, v in R(other).v.items():
            result[k] = result.get(k, F(0)) + v
        return R(result)

    __radd__ = __add__

    def __neg__(self):
        return R({k: -v for k, v in self.v.items()})

    def __sub__(self, other):
        return self + -R(other)

    def __rsub__(self, other):
        return R(other) + -self

    def __mul__(self, other):
        result = {}
        for k, v in self.v.items():
            for ell, w in R(other).v.items():
                repeated = k & ell
                factor = 1
                for bit, prime in enumerate(PRIMES):
                    if repeated & (1 << bit):
                        factor *= prime
                key = k ^ ell
                result[key] = result.get(key, F(0)) + factor * v * w
        return R(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.v == R(other).v

    def ledger(self):
        return {str(k): str(v) for k, v in sorted(self.v.items())}


def matrix(rows):
    return [[R(v) for v in row] for row in rows]


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def zeros(n):
    return matrix([[0] * n for _ in range(n)])


def transpose(a):
    return [list(col) for col in zip(*a)]


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(r, a):
    return [[R(r) * x for x in row] for row in a]


def W(c, s):
    return matrix([[c, 0, 0, -s], [0, c, -s, 0],
                   [0, s, c, 0], [s, 0, 0, c]])


def conjugate(a, b):
    return multiply(multiply(a, b), transpose(a))


checks = {}


def check(name, actual, expected):
    assert actual == expected, name
    checks[name] = True


sq3, sq5 = R({2: 1}), R({4: 1})
sq6, sq10 = R({3: 1}), R({5: 1})
w1 = W(F(1, 2) * sq3, R(F(1, 2)))
w2 = W(F(1, 4) * sq10, F(1, 4) * sq6)
check("W_log2_unitary", multiply(transpose(w1), w1), eye(4))
check("W_2log2_unitary", multiply(transpose(w2), w2), eye(4))

q = matrix([[1, 0, 0, 0], [0, 0, 0, 0],
            [0, 0, 1, 0], [0, 0, 0, 0]])
q_at_zero = conjugate(transpose(w1), q)
a_at_zero = add(multiply(multiply(q, q_at_zero), q), scale(-F(3, 4), q))
check("a_evaluation_zero_as_full_M4_matrix", a_at_zero, zeros(4))

u_at_log2 = multiply(w1, transpose(w2))
q_at_log2 = conjugate(u_at_log2, q)
a_at_log2 = add(multiply(multiply(q, q_at_log2), q), scale(-F(3, 4), q))
d = F(3, 16) * (sq5 - 1)
check("a_at_log2_equals_dq", a_at_log2, scale(d, q))
theta_a_at_zero = conjugate(transpose(w1), a_at_log2)
check("shifted_full_evaluation_equals_dQ", theta_a_at_zero, scale(d, q_at_zero))
compression = matrix([[theta_a_at_zero[0][0], 0],
                      [0, theta_a_at_zero[1][1]]])
expected_compression = matrix([[F(3, 4) * d, 0], [0, F(1, 4) * d]])
check("shifted_expectation_nonzero_exact", compression, expected_compression)
assert compression != zeros(2)
checks["nonzero_not_merely_vector_null"] = True

J = matrix([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
K = matrix([[F(1, 2), -F(1, 2)], [-F(1, 2), F(1, 2)]])
check("J_idempotent", multiply(J, J), J)
check("K_idempotent", multiply(K, K), K)
check("JK_zero", multiply(J, K), zeros(2))
check("KJ_zero", multiply(K, J), zeros(2))
check("J_plus_K_identity", add(J, K), eye(2))
# Hence (J+uK)(J+vK)=J+(uv)K for all u,v, proving the entire semigroup law.
X = matrix([[0, 1], [1, 0]])
q2 = matrix([[1, 0], [0, 0]])
check("bitflip_involution", multiply(X, X), eye(2))
check("projection_generator_diagonal", scale(F(1, 2), add(conjugate(X, q2), scale(-1, q2))),
      matrix([[-F(1, 2), 0], [0, F(1, 2)]]))

report = {
    "status": "PASS",
    "method": "exact arithmetic in multiquadratic field Q(sqrt2,sqrt3,sqrt5)",
    "radical_basis": {"mask_bits": {"0": 2, "1": 3, "2": 5}},
    "checks": checks,
    "witness_time": "log(2)",
    "d_coefficients": d.ledger(),
    "positivity_certificate": "d=3*(sqrt5-1)/16>0 because sqrt5>1",
    "all_time_semigroup_certificate": "P_t=J+exp(-t)K; J^2=J, K^2=K, JK=KJ=0",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Finite compression controls only; analytic proof is in DERIVATION.md",
}
destination = Path(__file__).with_name("EXACT_COMPRESSION_RESULTS.json")
destination.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"status": report["status"], "check_count": len(checks),
                  "output": str(destination)}, indent=2))
