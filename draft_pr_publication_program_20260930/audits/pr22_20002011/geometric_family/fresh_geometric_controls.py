#!/usr/bin/env python3
"""Exact independent cubic-tensor and full-density boundary controls.

This is not copied from either stored checker. It tests the whole 56-dimensional
space of six-variable cubic jets, including nonharmonic and negative witnesses.
The accompanying first-pass proof supplies the universal and closed-manifold
arguments. The finite controls cannot resolve a repaired variational conjecture.
"""
from pathlib import Path
from itertools import combinations_with_replacement, product
from math import factorial
import hashlib
import json
import sympy as s

x = s.symbols("x0:6")
zero = dict.fromkeys(x, 0)
checks = 0


def check(condition, label):
    global checks
    assert bool(condition), label
    checks += 1


def at0(expr):
    return s.expand(expr).subs(zero)


def lap(expr):
    return sum(s.diff(expr, z, 2) for z in x)


def monomial(exponent):
    return s.prod(z ** e for z, e in zip(x, exponent))


# Each basis polynomial has coefficient one, not a normalized tensor coefficient.
exponents = []
for indices in combinations_with_replacement(range(6), 3):
    e = [0] * 6
    for i in indices:
        e[i] += 1
    exponents.append(tuple(e))
check(len(exponents) == 56, "all six-variable cubic monomials")
basis = [monomial(e) for e in exponents]
ordered = list(product(range(6), repeat=3))
tensors = []
traces = []
for e in exponents:
    scale = s.Integer(s.prod(factorial(v) for v in e))
    row = []
    for indices in ordered:
        count = tuple(indices.count(i) for i in range(6))
        row.append(scale if count == e else s.S.Zero)
    tensors.append(row)
    traces.append([sum(row[ordered.index((i, i, j))] for i in range(6)) for j in range(6)])

# Construct directly from polynomial Hessians and their divergences. This is a
# second route to the tensor contraction, including every trace correction.
H = [s.hessian(f, x) for f in basis]
grad_lap = [[s.diff(lap(f), z) for z in x] for f in basis]
M = s.zeros(56)
for a in range(56):
    for b in range(56):
        inner = sum(tensors[a][i] * tensors[b][i] for i in range(216))
        trace_inner = sum(traces[a][j] * traces[b][j] for j in range(6))
        # At a flat metric two-jet, Delta T = -Delta(Hess f : Hess psi).
        direct_delta_T = -lap(sum(H[a][i, j] * H[b][i, j] for i in range(6) for j in range(6)))
        # The adjoint has the extra trace term, absent in harmonic-only tests.
        direct_Tadj_delta = -2 * sum(grad_lap[a][j] * grad_lap[b][j] for j in range(6))
        check(s.expand(-2 * (direct_delta_T - direct_Tadj_delta) - 4 * (inner - trace_inner)) == 0,
              "complete cubic basis pair %d,%d" % (a, b))
        M[a, b] = inner - trace_inner

D = s.diag(*[sum(v * v for v in row) for row in tensors])
Tr = s.Matrix(6, 56, lambda j, a: traces[a][j])
check(M == D - Tr.T * Tr, "Gram-minus-trace matrix")
check(Tr * D.inv() * Tr.T == s.Rational(8, 3) * s.eye(6), "trace-adjoint scalar")
check(Tr.rank() == 6, "trace rank")
check(M.rank() == 56, "no accidental nullspace of whole skew bilinear form")
check(M.det() == D.det() * s.Rational(-5, 3) ** 6, "matrix determinant lemma")


def geometric_pair(f, psi, expected):
    """Reconstruct actual connection/Hessian jets, without density Frechet code."""
    df = [s.diff(f, z) for z in x]
    dpsi = [s.diff(psi, z) for z in x]
    norm_df = sum(v * v for v in df)
    P = s.Matrix(6, 6, lambda i, j: -s.diff(f, x[i], x[j]) + df[i] * df[j]
                 - (norm_df / 2 if i == j else 0))

    def gamma(k, i, j):
        return (df[i] if k == j else 0) + (df[j] if k == i else 0) - (df[k] if i == j else 0)

    covH = s.Matrix(6, 6, lambda i, j: s.diff(psi, x[i], x[j])
                    - sum(gamma(k, i, j) * dpsi[k] for k in range(6)))
    check(P.subs(zero) == s.zeros(6), "Schouten zero")
    check(covH.subs(zero) == s.zeros(6), "covariant Hessian zero")
    check(all(at0(gamma(k, i, j)) == 0 and all(at0(s.diff(gamma(k, i, j), z)) == 0 for z in x)
              for k in range(6) for i in range(6) for j in range(6)), "connection and first jet vanish")
    check(all(at0(s.diff(P[i, j], x[k])) == -at0(s.diff(f, x[i], x[j], x[k]))
              for i, j, k in ordered), "covariant Schouten first jet")
    check(all(at0(s.diff(covH[i, j], x[k])) == at0(s.diff(psi, x[i], x[j], x[k]))
              for i, j, k in ordered), "covariant Hessian first jet")
    # exp(-4f) and exp(-2f) have vanished first and second jets, hence do not
    # change this value. Keeping the actual Christoffel contribution above
    # independently checks that it cannot leak into the needed quadratic jet.
    delta_T = at0(lap(sum(P[i, j] * covH[i, j] for i in range(6) for j in range(6))))
    # In the coordinate adjoint 1/v partial_ij(v P^{ij} h), v P^{ij}=exp(2f)P_ij.
    # exp(2f) has the same harmless lower jets; h=Delta_g psi has linear jet
    # equal to Delta_0 psi. The extra first-order Christoffel term has degree
    # at least four and contributes zero after a single derivative at zero.
    adj_delta = at0(sum(s.diff(P[i, j] * lap(psi), x[i], x[j])
                       for i in range(6) for j in range(6)))
    got = (-2 * delta_T, -2 * adj_delta, -2 * (delta_T - adj_delta))
    check(got == expected, "direct geometric values")
    return {"f": str(f), "psi": str(psi), "D_at_zero": int(got[0]),
            "D_adjoint_at_zero": int(got[1]), "skew_at_zero": int(got[2])}


xyz = x[0] * x[1] * x[2]
radial = x[0] * sum(z * z for z in x)
cases = [
    (xyz, xyz, (24, 0, 24)),
    (2 * xyz, -3 * xyz, (-144, 0, -144)),
    (xyz, x[0] * x[1] * x[3], (0, 0, 0)),
    (x[0] ** 3, x[0] ** 3, (144, 144, 0)),
    (x[0] ** 2 * x[1], x[0] ** 2 * x[1], (48, 16, 32)),
    (radial, radial, (384, 1024, -640)),
    (xyz + x[3] ** 4, xyz + x[4] ** 5, (24, 0, 24)),
    (x[3] * x[4] * x[5], x[3] * x[4] * x[5], (24, 0, 24)),
]
values = [geometric_pair(*case) for case in cases]

# Check critical-dimension cancellation at general function jets, where
# setting psi(0)=0 would conceal omission of the volume variation.
z = s.symbols("z")
u = s.Function("u")(z)
b = s.Function("b")(z)
v = s.Function("v")(z)
n = s.symbols("n", integer=True)
full = (n - 2) * u * s.diff(b, z, 2) + (n - 2) * s.diff(u, z) * s.diff(b, z)
full += s.diff(-4 * u * b - 2 * v, z, 2)
normal = (n - 6) * u * s.diff(b, z, 2) + (n - 10) * s.diff(u, z) * s.diff(b, z)
normal += -4 * b * s.diff(u, z, 2) - 2 * s.diff(v, z, 2)
check(s.expand(full - normal) == 0, "general dimension full-density identity")
critical = -4 * s.diff(b * s.diff(u, z), z) - 2 * s.diff(v, z, 2)
check(s.expand(full.subs(n, 6) - critical) == 0, "dimension six divergence form")
scalar_only = full - n * u * s.diff(b, z, 2)
check(s.expand((full - scalar_only).subs(n, 6) - 6 * u * s.diff(b, z, 2)) == 0,
      "volume variation is present")
check(s.expand(full.subs(n, 4) - critical) != 0, "four-dimensional formula differs")

result = {
    "status": "PASS", "assertions": checks, "sympy_version": s.__version__,
    "complete_cubic_basis_size": 56, "complete_cubic_pairs": 3136,
    "skew_matrix_rank": 56, "skew_matrix_signature": {"positive": 50, "negative": 6, "zero": 0},
    "signature_justification": "positive tensor norm on kernel(trace), trace-adjoint Gram=8/3 I, residual trace-space coefficient=-5/3",
    "geometric_cases": values,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Exact finite cubic-jet, connection, adjoint-trace, dimension and volume controls. Universal counterexample and smooth closed-torus/integral witness are proved in FIRST_PASS_DERIVATION.md. No repaired-conjecture claim."
}
Path(__file__).with_name("FRESH_GEOMETRIC_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
