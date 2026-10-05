"""Independent exact controls for the nonlinear inverse-coordinate Laplacian.

These finite checks do not prove the manuscript's universal asymptotic estimates.
They exercise a nonsymmetric Jacobian, nonzero drift, and nonlinear test scalar.
"""
import json
import sympy as S

x, y, p, q = S.symbols("x y p q", real=True)
alpha = S.Rational(1, 13)
beta = S.Rational(17, 16)
f = S.Matrix([x + alpha*y*y, beta*y])
inverse = S.Matrix([p - alpha*q*q/(beta*beta), q/beta])
J = f.jacobian([x, y])
H = J.inv()
A = H*H.T
B = S.Matrix([
    -sum(H[i, a]*S.diff(f[a], [x, y][j], [x, y][k])*A[j, k]
         for a in range(2) for j in range(2) for k in range(2))
    for i in range(2)
])
checks = []
for label, v in [
    ("coordinate x: drift survives", x),
    ("coordinate y", y),
    ("mixed quadratic", 3*x*x+5*x*y+7*y*y+11*x+13*y+19),
    ("mixed quartic", x*x*y*y+x*y*y*y+2*x**4),
]:
    pulled = v.subs({x: inverse[0], y: inverse[1]}, simultaneous=True)
    exact = (S.diff(pulled, p, 2)+S.diff(pulled, q, 2)).subs(
        {p: f[0], q: f[1]}, simultaneous=True)
    operator = sum(A[j,k]*S.diff(v, [x,y][j], [x,y][k])
                   for j in range(2) for k in range(2))
    operator += sum(B[i]*S.diff(v, [x,y][i]) for i in range(2))
    assert S.expand(exact-operator) == 0
    checks.append({"label": label, "exact_identity": True})
assert B[0] == -2*alpha/(beta*beta) and B[1] == 0
wrong_A = H.T*H
wrong_value = sum(wrong_A[j,k]*S.diff(3*x*x+5*x*y+7*y*y,
                                    [x,y][j], [x,y][k])
                  for j in range(2) for k in range(2))
right_value = sum(A[j,k]*S.diff(3*x*x+5*x*y+7*y*y,
                               [x,y][j], [x,y][k])
                  for j in range(2) for k in range(2))
point = {x: S.Rational(1,7), y: S.Rational(1,11)}
wrong_difference = S.factor((wrong_value-right_value).subs(point))
assert wrong_difference != 0
checks.append({"label": "H^T H negative control", "nonzero_error": str(wrong_difference)})
checks.append({"label": "omitted drift negative control", "nonzero_error": str(-B[0])})
print(json.dumps({"status": "PASS", "checks": checks,
    "SymPy_version": S.__version__,
    "limitation": "Six exact finite formula controls; no numerical all-r or curvature-positivity certification."}, indent=2))
