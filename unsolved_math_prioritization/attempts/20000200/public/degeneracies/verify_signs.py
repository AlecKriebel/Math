"""Exact symbolic audit of fixed-pair signs and reparametrization invariance.

Supplementary tests; the general arguments are in DEGENERACIES_AND_IMAGE_AUDIT.md.
"""
import json
from pathlib import Path
import sympy as s

t = s.symbols("t")
I = s.I
checks = []


def equal(label, got, expected):
    error = s.factor(s.cancel(got - expected))
    assert error == 0, (label, error)
    checks.append({"check": label, "passed": True})


def invariants(z, w):
    x, y = (z + w) / 2, (z - w) / (2 * I)
    g = s.factor(s.diff(x, t) ** 2 + s.diff(y, t) ** 2)
    delta = s.factor(s.diff(x, t) * s.diff(y, t, 2) - s.diff(y, t) * s.diff(x, t, 2))
    u = s.factor(delta ** 2 / g ** 3)
    v = s.factor((g * s.diff(delta, t) - s.Rational(3, 2) * delta * s.diff(g, t)) / g ** 3)
    return g, delta, u, v


for a, b in [(1, 2), (2, 1), (1, -2), (-2, 1), (-1, -2), (1, 3), (3, -1), (2, 3), (3, 4)]:
    z, w = t ** a, t ** b
    g, delta, u, v = invariants(z, w)
    N, D = a + b, a - b
    equal(f"monomial({a},{b}): metric", g, a * b * t ** (N - 2))
    equal(f"monomial({a},{b}): u", u, -s.Rational(D * D, 4 * a * b) * t ** (-N))
    equal(f"monomial({a},{b}): v", v, -s.Rational(N * D, 4 * a * b) / I * t ** (-N))
    equal(f"monomial({a},{b}): slope", v / u, -I * s.Rational(N, D))

for idx, (z, w) in enumerate([(t, t ** 2 + 3 * t), (t ** 3 + t, t ** 2 - t), ((t + 1) / (t - 2), t ** 2 + 1 / t)]):
    g, delta, u, v = invariants(z, w)
    R = s.factor(s.diff(z, t) / s.diff(w, t))
    alpha = s.factor(s.diff(R, t) / R)
    equal(f"rational({idx}): alpha sign", alpha, 2 * I * delta / g)
    equal(f"rational({idx}): intrinsic u", -alpha ** 2 / (4 * g), u)
    equal(f"rational({idx}): intrinsic v", I * s.diff(u, t) / alpha, v)
    _, _, reflected_u, reflected_v = invariants(w, z)
    equal(f"rational({idx}): reflection u", reflected_u, u)
    equal(f"rational({idx}): reflection v", reflected_v, -v)
    for m in [2, 3]:
        _, _, cover_u, cover_v = invariants(z.subs(t, t ** m), w.subs(t, t ** m))
        equal(f"rational({idx}): cover({m}) u", cover_u, u.subs(t, t ** m))
        equal(f"rational({idx}): cover({m}) v", cover_v, v.subs(t, t ** m))

A = s.symbols("A", nonzero=True)
_, _, circle_u, circle_v = invariants(t, 1 / (A * t))
equal("circle: point u", circle_u, A)
equal("circle: point v", circle_v, 0)
_, _, line_u, line_v = invariants(t, 2 * t + 1)
equal("nonisotropic line: point u", line_u, 0)
equal("nonisotropic line: point v", line_v, 0)

result = {"all_passed": True, "count": len(checks), "checks": checks, "sympy_version": s.__version__}
path = Path(__file__).with_name("SIGN_CHECKS.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"all_passed": True, "count": len(checks), "output": str(path)}))
