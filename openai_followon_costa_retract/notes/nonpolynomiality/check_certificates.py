"""Exact identity checks for the pinned nonpolynomiality proof.

Run with the existing `python` runtime (SymPy 1.14.0 in this audit).
These checks verify displayed algebraic identities; they do not replace
the mathematical proof in audit.md.
"""

from pathlib import Path
import sympy as sp

p, s, u, F, J, a, d, b, c = sp.symbols("p s u F J a d b c")
x = s**2 + u**3 + p**2 * F
y = s + x * (x - u**3)
z = s * x + p**2 * J
Htop = x**2 * F - (1 + 2 * s * x) * J - p**2 * J**2

checks = {
    "graded_relation": sp.expand(x * y - z * (z + 1) - p**2 * Htop) == 0,
}

X, Y, Z = a * b, d * c, d * b
h = X - u**3
S = Y - X * h
f, g = X - S**2 - u**3, Z - S * X
v = a**2 * h - d**2
C1 = c**2 - b**2 * h
alpha = a**2 * (1 - 2 * b * d)
beta = d**2 * (3 + 2 * b * d) + alpha * h
groebner = sp.groebner([a * c - b * d - 1], c, a, d, b, u)


def normal_form(expr):
    return sp.expand(groebner.reduce(sp.expand(expr))[1])


checks.update({
    "principal_f": normal_form(f - C1 * v) == 0,
    "principal_g": normal_form(g - b**2 * v) == 0,
    "principal_v": normal_form(v - alpha * f - beta * g) == 0,
    "bezout": normal_form(alpha * C1 + beta * b**2 - 1) == 0,
})


def negative_root(expr):
    return sp.expand(b * sp.diff(expr, a) + c * sp.diff(expr, d))


def positive_root(expr):
    return sp.expand(a * sp.diff(expr, b) + d * sp.diff(expr, c))


negative_second = normal_form(negative_root(negative_root(v)))
positive_first = normal_form(positive_root(v))
checks["positive_second_v"] = normal_form(positive_root(positive_root(v))) == 0
checks["negative_second_v_nonzero"] = negative_second != 0
assert all(checks.values()), checks

lines = [f"{key}: {value}" for key, value in checks.items()]
lines += [
    f"E_negative_squared_v: {negative_second}",
    f"E_positive_v: {positive_first}",
]
output = "\n".join(lines) + "\n"
Path(__file__).with_name("symbolic_audit.txt").write_text(output)
print(output, end="")
