"""Independent finite controls. Standard library only. Never imports deposited code.

Exact rational statements and illustrative floating controls are reported separately.
Finite-dimensional tests do not prove a universal/asymptotic stochastic statement.
"""
from fractions import Fraction as Q
from math import sqrt, pi, gamma, sin
import json


def deriv(p):
    return [i * p[i] for i in range(1, len(p))]


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def integral(p, left=Q(0), right=Q(1)):
    return sum((c * (right ** (i + 1) - left ** (i + 1)) / (i + 1)
                for i, c in enumerate(p)), Q(0))


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


phi = list(map(Q, [0, 0, 0, 0, 1, -4, 6, -4, 1]))
f = deriv(phi)
fp = deriv(f)
a = integral(mul(f, f))
b = integral(mul(fp, fp))
check(a == Q(4, 45045), 'pairing mismatch')
check(integral(phi) == Q(1, 630), 'g norm mismatch')
check(2 * integral(f, Q(0), Q(1, 2)) == Q(1, 128), 'f norm mismatch')
g3 = deriv(deriv(deriv(phi)))
f3 = deriv(g3)
check(g3 == list(map(Q, [0, 24, -240, 720, -840, 336])), 'g third derivative')
check(f3 == list(map(Q, [24, -480, 2160, -3360, 1680])), 'f third derivative')
# g''=4q²(3-14q), q=x(1-x); its extrema have q=1/7 and q=1/4.
Ng = 4 * Q(4, 49) + 2 * Q(1, 8)
check(Ng == Q(113, 196), 'g third derivative norm')
exact = {
    'pairing_a': str(a), 'b_brownian': str(b), 'L_g': str(integral(phi)),
    'L_f': '1/128', 'N_g': str(Ng),
    'brownian_bump_constant_squared': str(a / b),
    'brownian_bump_constant_below_exact_optimum': a / b < Q(1, 4),
    'canonical_correction_H_quarter_diagonal_T_equals_1': '1/4',
}
exact_brownian = []
for n in [1, 2, 3, 8]:
    for r in [1, 2, 4, 16]:
        N = n * r
        # N² terms of bilinear area, covariance I/N.
        finevar = Q(N * (N - 1), 2 * N * N) + Q(1, 4 * N)
        coarsevar = Q(n * (n - 1), 2 * n * n) + Q(1, 4 * n)
        res = finevar - coarsevar
        check(res == Q(1, 4) * (Q(1, n) - Q(1, N)), 'Brownian projection normalization')
        exact_brownian.append({'n': n, 'fine_per_coarse': r, 'residual_variance': str(res),
                               'limit_residual_variance': str(Q(1, 4 * n))})


def transpose(A):
    return [list(row) for row in zip(*A)]


def product(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def inv(A):
    n = len(A)
    aug = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(A)]
    for j in range(n):
        k = max(range(j, n), key=lambda i: abs(aug[i][j]))
        aug[j], aug[k] = aug[k], aug[j]
        check(abs(aug[j][j]) > 1e-13, 'illustrative inverse too unstable')
        d = aug[j][j]
        aug[j] = [x / d for x in aug[j]]
        for i in range(n):
            if i != j:
                factor = aug[i][j]
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def bilinear_var(A, covariance):
    # tr(A^T Γ A Γ).
    result = product(product(product(transpose(A), covariance), A), covariance)
    return sum(result[i][i] for i in range(len(A)))


def finite_conditional(H, n, r):
    N = n * r
    rho = lambda j: .5 * (abs(j + 1) ** (2 * H) + abs(j - 1) ** (2 * H) - 2 * abs(j) ** (2 * H))
    covariance = [[N ** (-2 * H) * rho(i - j) for j in range(N)] for i in range(N)]
    obs = [[float(i // r == j) for i in range(N)] for j in range(n)]
    joint = product(covariance, transpose(obs))
    obsvar = product(obs, joint)
    observed_covariance = product(product(joint, inv(obsvar)), transpose(joint))
    A = [[.5 if i == j else float(i < j) for j in range(N)] for i in range(N)]
    residual = bilinear_var(A, covariance) - bilinear_var(A, observed_covariance)
    check(residual >= -1e-12, 'negative conditional residual')
    if H == .5:
        check(abs(residual - .25 * (1 / n - 1 / N)) < 1e-12, 'general conditional code Brownian control')
    return {'H': H, 'n': n, 'fine_per_coarse': r, 'polygonal_residual_variance': residual,
            'scaled_polygonal_RMS': sqrt(max(0, residual)) * n ** (2 * H - .5)}


finite = [finite_conditional(H, n, r)
          for H in [.2501, .26, .37, .5, .73, .75, .9, .99]
          for n in [1, 2, 4] for r in [2, 4, 8]]

# N_f can be bounded rigorously for this diagnostic by the sum of absolute
# coefficients. The result is a smaller valid theorem constant, not a numeric
# certification of the manuscript's literal c_H.
Nf_coefficient_upper = sum(abs(x) / Q(i + 1) for i, x in enumerate(f3))
smaller_constant = []
for H in [.2501, .26, .5, .75, .99, .9999]:
    alpha = 2 * H + 1
    D = 2 * pi / (gamma(1 + 2 * H) * sin(pi * H))
    def Pbar(L, Nr):
        return pi ** alpha * L ** 2 + 2 * Nr ** 2 * pi ** (alpha - 6) * (1 + 1 / (2 * (5 - alpha)))
    csmall = 2 * pi * float(a) / (D * sqrt(Pbar(1 / 128, float(Nf_coefficient_upper)) * Pbar(1 / 630, float(Ng))))
    smaller_constant.append({'H': H, 'c_with_rigorous_Nf_upper_but_float_evaluation': csmall})
print(json.dumps({'exact_rational': exact, 'exact_brownian_projection': exact_brownian,
                  'illustrative_general_gaussian_conditional_controls': finite,
                  'illustrative_smaller_constants': smaller_constant,
                  'limitations': 'Floating controls are nonvalidated diagnostics of finite polygonal targets; no finite test proves the universal lower theorem or limit.'}, indent=2))
