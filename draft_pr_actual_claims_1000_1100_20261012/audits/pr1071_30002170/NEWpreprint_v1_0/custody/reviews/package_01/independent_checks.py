#!/usr/bin/env python3
"""Independent finite mechanism checks; exact rational where identified.

This is finite evidence, not a proof of universal Gaussian/analytic assertions.
No original implementation or prior verdict is imported. Explicit guards work -O.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from functools import lru_cache
from math import comb, pi
import json, sys

def require(x, message):
    if not x:
        raise RuntimeError(message)

def reject(fn, name):
    try:
        fn()
    except RuntimeError:
        return {"name": name, "rejected": True}
    raise RuntimeError("Fault was not rejected: " + name)

def derivative(p):
    return [F(i) * p[i] for i in range(1, len(p))]

def multiply(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out

def evaluate(p, x):
    total = F(0)
    for coefficient in reversed(p):
        total = total * x + coefficient
    return total

def integrate(p):
    return sum((a / F(i + 1) for i, a in enumerate(p)), F(0))

phi = [F(0)] * 4 + [F((-1) ** k * comb(4, k)) for k in range(5)]
derivatives = [phi]
for _ in range(4):
    derivatives.append(derivative(derivatives[-1]))
f = derivatives[1]
g = phi
a = integrate(multiply(f, f))
require(a == F(4, 45045), "exact positive area pairing")
traces = [[str(evaluate(p, F(0))), str(evaluate(p, F(1)))] for p in derivatives[:4]]
require(all(t == ["0", "0"] for t in traces), "zero-extension traces")
lf = 2 * evaluate(phi, F(1, 2))
lg = integrate(phi)
require(lf == F(1, 128) and lg == F(1, 630), "independent L1 norms")

# Evaluate phi'' at (7-sqrt(21))/14 in Q(sqrt(21)); its radical cancels.
def qadd(z, w):
    return (z[0] + w[0], z[1] + w[1])

def qmul(z, w):
    return (z[0] * w[0] + 21 * z[1] * w[1], z[0] * w[1] + z[1] * w[0])

root = (F(1, 2), F(-1, 14))
value = (F(0), F(0))
for coefficient in reversed(derivatives[2]):
    value = qadd(qmul(value, root), (coefficient, F(0)))
require(value == (F(4, 49), F(0)), "phi'' critical value in Q(sqrt(21))")
factor = multiply(multiply([F(0), F(1)], [F(-1), F(1)]), multiply([F(-1), F(2)], [F(1), F(-7), F(7)]))
require([24 * x for x in factor] == derivatives[3], "third derivative critical-root factorization")
ng = 4 * value[0] - 2 * evaluate(derivatives[2], F(1, 2))
require(ng == F(113, 196), "exact total variation for N_g")
brownian_f_norm2 = integrate(multiply(derivatives[2], derivatives[2]))
require(0 < 4 * a <= brownian_f_norm2, "Brownian local witness below exact optimum")

def transpose(x):
    return [list(t) for t in zip(*x)]

def matmul(x, y):
    return [[sum((u * v for u, v in zip(row, col)), F(0)) for col in transpose(y)] for row in x]

def matrix_trace(x):
    return sum((x[i][i] for i in range(len(x))), F(0))

def upper(x):
    return max(sum(abs(t) for t in row) for row in x)

signed_psd = []
for seed in range(1, 101):
    n = 3
    l = [[F(((seed * (i + 2) + j * 3) % 11) - 5, i + j + 2) for j in range(n)] for i in range(n)]
    q = [[F(((seed * (j + 1) + i * 5) % 13) - 6, i + j + 3) for j in range(n)] for i in range(n)]
    A, C = matmul(l, transpose(l)), matmul(q, transpose(q))
    ma, mc = upper(A), upper(C)
    tr = matrix_trace(matmul(A, C))
    require(0 <= tr <= ma * matrix_trace(C) <= n * ma * mc, "signed PSD trace bound")
    signed_psd.append({"seed": seed, "trace_AC": str(tr), "M_f": str(ma), "M_g": str(mc),
                       "negative_offdiagonal": any(A[i][j] < 0 or C[i][j] < 0 for i in range(n) for j in range(n) if i != j),
                       "noncommuting": matmul(A, C) != matmul(C, A)})
require(any(x["negative_offdiagonal"] and x["noncommuting"] for x in signed_psd), "test exercises signed noncommuting case")

# Exact Wick-moment check for nonlinear estimators of four observed coordinates.
# U0,U1,V0,V1 are hidden; the two component families are independent.
cov = [[F(0)] * 8 for _ in range(8)]
for start, block in [(0, [[2, 1], [1, 3]]), (2, [[3, -1], [-1, 2]]),
                     (4, [[2, -1], [-1, 2]]), (6, [[3, 1], [1, 1]])]:
    for i in range(2):
        for j in range(2):
            cov[start + i][start + j] = F(block[i][j])

@lru_cache(None)
def moment(indices):
    if not indices:
        return F(1)
    if len(indices) % 2:
        return F(0)
    i = indices[0]
    return sum((cov[i][indices[j]] * moment(tuple(sorted(indices[1:j] + indices[j+1:])))
                for j in range(1, len(indices))), F(0))

nonlinear_count = 0
for degree in range(7):
    for observed_monomial in combinations_with_replacement(range(4), degree):
        pairing = sum((moment(tuple(sorted(observed_monomial + (4 + j, 6 + j)))) for j in range(2)), F(0))
        require(pairing == 0, "nonlinear complete-grid invisibility")
        nonlinear_count += 1
witness_variance = sum((moment(tuple(sorted((4 + j, 6 + j, 4 + k, 6 + k)))) for j in range(2) for k in range(2)), F(0))
hidden_A = [[F(2), F(-1)], [F(-1), F(2)]]
hidden_C = [[F(3), F(1)], [F(1), F(1)]]
require(witness_variance == matrix_trace(matmul(hidden_A, hidden_C)), "independent fourth-moment witness variance")

def compact(p, x):
    return evaluate(p, x) if 0 <= x <= 1 else F(0)

pairings = []
for n in [1, 3, 5]:
    for j in range(n):
        for m in [47, 113, 257]:
            # H=1/2: the product of two cell scalings is Delta=1/n.
            exact = sum((compact(f, F(n*k, m) - j) *
                         (compact(g, F(n*(k+1), m) - j) - compact(g, F(n*k, m) - j))
                         for k in range(m)), F(0)) / n
            expected = a / n
            lipschitz_bound = sum(abs(t) for t in derivatives[2])
            require(abs(exact - expected) <= lipschitz_bound * lf / m, "fixed-mesh deterministic pairing convergence bound")
            if m == 257:
                require(abs(exact / expected - 1) < F(1, 100), "fine misaligned-grid pairing")
            pairings.append({"n": n, "cell": j, "Euler_cells": m, "pairing": str(exact), "limit": str(expected)})

period_tail = []
for alpha in [1.500001, 1.75, 2., 2.25, 2.5, 2.75, 2.999999]:
    partial = sum((2*k - 1) ** (alpha - 6) for k in range(1, 10001))
    bound = 1 + 1 / (2 * (5 - alpha))
    require(partial <= bound, "decreasing odd-power tail bound")
    period_tail.append({"alpha": alpha, "partial_10000": partial, "bound": bound})

corrections = []
for H in [0.250001, 0.3, 0.375, 0.499999, 0.5, 0.6, 0.75, 0.9, 0.999999]:
    def rho(r):
        return ((abs(r + 1)) ** (2*H) + (abs(r-1)) ** (2*H) - 2*(abs(r)) ** (2*H))/2
    for n in [1, 2, 3, 7, 17, 31]:
        direct = sum(rho(j-k) ** 2 for j in range(n) for k in range(n)) / (4*n**(4*H))
        lag = (n + 2*sum((n-r)*rho(r)**2 for r in range(1, n))) / (4*n**(4*H))
        require(abs(direct-lag) < 1e-12 * max(1, direct), "polygonal correction pair-count identity")
        if H == 0.5:
            require(lag == 1/(4*n), "Brownian half-correction variance")
        corrections.append({"H": H, "n": n, "variance": lag})

def conjugation_test(conjugated):
    # Wrong conjugation reverses t in the Fourier inversion. For t in (0,1),
    # a compact positive-support g then has g(-t)=0 although g(t)>0.
    target = compact(g, F(1, 3))
    received = compact(g, F(1, 3) if conjugated else F(-1, 3))
    require(target == received, "Fourier sign changes covariance path")

def scaling_test(exponent):
    for H in [F(3, 8), F(1, 2), F(3, 4), F(9, 10)]:
        alpha = 2*H + 1
        require(2*H + exponent - alpha - 1 == 0, "wrong Gram scale exponent")

def zero_extension_test(p):
    for _ in range(3):
        require(evaluate(p, F(0)) == evaluate(p, F(1)) == 0, "boundary delta mass in weak third derivative")
        p = derivative(p)

def covariance_block_test(mutated):
    require(all(mutated[i][j] == 0 for i in range(4) for j in range(4, 8)), "witness no longer invisible to whole grid")

def lag_test(discard_all):
    H = F(3, 8)
    c2_lower = float(H**2*(2*H-1)**2)/4 * 3**(float(4*H-4))
    require(not discard_all and c2_lower > 0, "all-lag little-o conflicts with positive lag 2")

badcov = [row[:] for row in cov]
badcov[0][4] = badcov[4][0] = F(1, 10)
controls = [reject(lambda: conjugation_test(False), "remove Fourier conjugation"),
            reject(lambda: scaling_test(F(3)), "change Delta Fourier exponent"),
            reject(lambda: zero_extension_test(derivative([F(0), F(0), F(1), F(-2), F(1)])), "replace order-four bump by order-two bump"),
            reject(lambda: covariance_block_test(badcov), "leak one hidden coordinate to observation vector"),
            reject(lambda: lag_test(True), "discard all distant lag terms")]
conjugation_test(True); scaling_test(F(2)); zero_extension_test(f); zero_extension_test(g); covariance_block_test(cov); lag_test(False)

out = {"optimized": not __debug__, "exact_polynomial": {"a": str(a), "L_f": str(lf), "L_g": str(lg), "N_g": str(ng), "traces": traces, "Brownian_f_norm2": str(brownian_f_norm2), "Brownian_unloosened_constant_squared": str(a/brownian_f_norm2)},
       "signed_noncommuting_PSD_cases": signed_psd, "exact_nonlinear_Wick_monomials": nonlinear_count,
       "exact_witness_variance": str(witness_variance), "misaligned_deterministic_pairings": pairings,
       "sampled_period_tail": period_tail, "polygonal_correction_cases": corrections, "negative_controls": controls,
       "limits": "Exact polynomial/rational identities and exact finite Wick moments where identified; sampled floating series/covariance checks are not intervals. No universal proof or source novelty certification."}
print(json.dumps(out, indent=2))
