"""Exact algebraic audit of family 362 cancellation, not a PDE proof.

SymPy 1.14.0; run: python check_kernel.py
Rotational covariance permits n=(0,0,1) after differentiating.
Source acceleration b and receiver velocity acceleration c are arbitrary.
No species or charge assumption is imposed on either acceleration.
"""

import sympy as s

r = s.symbols("r", positive=True)
u = s.Matrix(s.symbols("ux uy uz", real=True))
a = s.Matrix(s.symbols("ax ay az", real=True))
n = s.Matrix(s.symbols("nx ny nz", real=True))
b = s.Matrix(s.symbols("bx by bz", real=True))
c = s.Matrix(s.symbols("cx cy cz", real=True))
d = 1 - n.dot(u)
D = 1 - n.dot(a)
e = 1 - a.dot(u)
H = s.eye(3) + n * a.T / D
g = (u - n) / d
k0 = u - e * n / D
primitive = k0 / (r * d)
n_prime = ((d / D) * (a - n) + n - u) / r
a_prime = c * d / D
r_prime = d / D - 1
primitive_prime = (
    primitive.jacobian(u) * b
    + primitive.jacobian(n) * n_prime
    + primitive.jacobian(a) * a_prime
    + primitive.diff(r) * r_prime
)
kernel = -H * g.jacobian(u) * b / r - H * g * (1 - u.dot(u)) / (r**2 * d)
rhs = (
    -primitive_prime
    + e * (n * (1 - a.dot(a)) / D - a) / (r**2 * D**2)
    + n * c.dot(k0) / (r * D**2)
)
axis = dict(zip(n, [0, 0, 1]))
certificate = [s.factor(expr.subs(axis)) for expr in kernel - rhs]
assert certificate == [0, 0, 0], certificate
print("Signed kernel identity residuals:", certificate)
print("Identity holds for arbitrary independent source and receiver accelerations.")

# Independent exact arithmetic for the final exponent contradiction.
eps = s.Rational(1, 100000)
delta_ratio = 4 * eps / (1 - 5 * eps)
assert delta_ratio < s.Rational(1, 1000)
beta = s.Rational(29, 25)
improved_y_lower = s.Rational(1, 3) - s.Rational(8, 3) * s.Rational(1, 1000)
assert improved_y_lower > s.Rational(33, 100)
near_y_upper = beta / 2 + (beta / 2) * s.Rational(1, 1000)
assert near_y_upper < s.Rational(582, 1000)
h_upper = (s.Rational(582, 1000) - s.Rational(33, 100)) / (s.Rational(1, 3) + beta / 4)
assert h_upper < s.Rational(41, 100)
assert h_upper < s.Rational(496, 1000)
print("Exact exponent margins:", {"Delta/z": delta_ratio, "H/z upper": h_upper})
