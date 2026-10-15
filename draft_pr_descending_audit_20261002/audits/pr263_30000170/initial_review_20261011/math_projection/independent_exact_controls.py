"""Independent rational controls; no imports from frozen author/reviewer code.

These finite controls check identities and boundary handling. The accompanying
report gives the proof for all positive t and all fixed positive-definite metrics.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from datetime import datetime, timezone


def cadd(z, w):
    return (z[0] + w[0], z[1] + w[1])


def cneg(z):
    return (-z[0], -z[1])


def cmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def cdiv(z, w):
    den = w[0]**2 + w[1]**2
    assert den > 0
    return ((z[0]*w[0] + z[1]*w[1])/den,
            (z[1]*w[0] - z[0]*w[1])/den)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def mv(A, x):
    return [dot(row, x) for row in A]


def solve(A, b):
    rows = [list(row) + [rhs] for row, rhs in zip(A, b)]
    for j in range(len(b)):
        k = next(k for k in range(j, len(b)) if rows[k][j])
        rows[j], rows[k] = rows[k], rows[j]
        den = rows[j][j]
        rows[j] = [a/den for a in rows[j]]
        for k in range(len(b)):
            if k != j:
                scale = rows[k][j]
                rows[k] = [a-scale*c for a, c in zip(rows[k], rows[j])]
    return [row[-1] for row in rows]


def coupled_spd(d):
    # G=A^T A. A has unit diagonal and rational superdiagonal, so is invertible.
    A = [[F(i == j) + (F(1, 2) if j == i+1 else F(0))
          for j in range(d)] for i in range(d)]
    return [[sum(A[k][i]*A[k][j] for k in range(d))
             for j in range(d)] for i in range(d)]


counts = {}


def check(family, claim):
    assert claim, family
    counts[family] = counts.get(family, 0) + 1


# Root-map controls, including stable, unstable, trace-zero, repeated-root,
# frequency-zero and B-zero cases. No complex floating-point arithmetic is used.
grid = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
for r in grid:
    for s in grid:
        for w1 in grid:
            for w2 in grid:
                root1, root2 = (-r, w1), (-s, w2)
                a = cneg(cadd(root1, root2))
                b = cmul(root1, root2)
                x, y, u, v = a[0], a[1], b[0], b[1]
                B, V = u+y*y/4, v-x*y/2
                check("root_parameter_B_identity", B == r*s+(w1-w2)**2/4)
                check("root_parameter_V_identity", V == (r-s)*(w1-w2)/2)
                check("root_parameter_gap_identity",
                      x*x*B-V*V == r*s*((r+s)**2+(w1-w2)**2))
                coefficient_stable = x >= 0 and B >= 0 and V*V <= x*x*B
                root_stable = r >= 0 and s >= 0
                check("stability_equivalence_grid", coefficient_stable == root_stable)


for den in [1, 2, 3, 5, 8, 13, 21, 34]:
    t = F(1, den)
    lam, other = (F(0), -t), (-t*t, t)
    a, b = cneg(cadd(lam, other)), cmul(lam, other)
    check("p_t_factorization", a == (t*t, F(0)) and b == (t*t, t**3))
    derivative_den = (t*t, -2*t)
    scalar = 2/(t*(t*t+4))
    n = [-t, -t*t/2, -t/2, F(1)]
    # d lambda=-(lambda da+db)/p'(lambda).
    e = [(F(1), F(0)), (F(0), F(1))]
    ga = [cdiv(cneg(cmul(lam, direction)), derivative_den)[0] for direction in e]
    gb = [cdiv(cneg(direction), derivative_den)[0] for direction in e]
    check("monic_root_derivative_normal", ga+gb == [scalar*a for a in n])
    # Add dl, using -(lambda^2 dl)/p'(lambda), independently of normalization.
    gl = [cdiv(cneg(cmul(cmul(lam, lam), direction)), derivative_den)[0]
          for direction in e]
    N = [t**3/2, -t*t] + n
    check("full_root_derivative_normal", gl+ga+gb == [scalar*a for a in N])
    point = [t*t, F(0), t*t, t**3]
    delta0 = [-a for a in point]
    support = dot(n, delta0)
    norm2 = dot(delta0, delta0)
    check("constant_comparison_support", support == t**3/2)
    check("constant_comparison_norm", norm2 == 2*t**4+t**6)
    check("constant_comparison_quotient", support/norm2 == 1/(2*t*(2+t*t)))
    check("limiting_normal_at_origin_obstruction",
          point[-1]/norm2 == 1/(t*(2+t*t)))
    for kappa in [F(1, 2), F(3, 2), F(2), F(3)]:
        delta = [(kappa*kappa-1)*t*t, F(0),
                 (kappa*kappa-1)*t*t, (kappa**3-1)*t**3]
        check("general_secant_support",
              dot(n, delta) == (kappa-1)**2*(2*kappa+1)*t**3/2 > 0)
    epigraph_covector = n+[-t*(t*t+4)/2]
    full_epi_covector = N+[-t*(t*t+4)/2]
    for covector, displacement in [
        (n, delta0), (N, [F(0), F(0)]+delta0),
        (epigraph_covector, delta0+[F(0)]),
        (full_epi_covector, [F(0), F(0)]+delta0+[F(0)])
    ]:
        G = coupled_spd(len(covector))
        normal = solve(G, covector)
        check("coupled_metric_normal_duality", dot(normal, mv(G, displacement)) == support)
        check("coupled_metric_positive_norm", dot(displacement, mv(G, displacement)) > 0)


for rho in [F(1), F(10), F(100), F(1000)]:
    t = 1/(10*rho)
    check("finite_uniform_support_threshold_controls",
          t**3/2 > (rho/2)*(2*t**4+t**6))

result = {
    "status": "PASS",
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "arithmetic": "Python fractions.Fraction only; no floats or author imports",
    "control_counts": counts,
    "total_exact_assertions": sum(counts.values()),
    "limit": "Finite controls supplement, but do not replace, the written universal proof."
}
Path(__file__).with_name("EXACT_CONTROLS.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
