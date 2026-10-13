#!/usr/bin/env python3
"""Exact symbolic controls for the affine-torus Hessian obstruction.

Read-only and current-directory independent. The global positivity/Stokes step
is an analytical proof in PROOF.md, not a claim established by finite tests.
"""
import json
import sympy as s

checks = []


def equal(name, actual, expected):
    if isinstance(actual, s.MatrixBase):
        residual = actual - expected
        ok = all(s.simplify(v) == 0 for v in residual)
    else:
        ok = s.simplify(actual - expected) == 0
    if not ok:
        raise AssertionError((name, actual, expected))
    checks.append(name)


x, y, t = s.symbols("x y t", real=True)
m, n, p, q = s.symbols("m n p q", integer=True)
z = (x, y)
F = s.Matrix([x, y + t*x*x/2])
J = F.jacobian(z)
equal("developing_map_jacobian_determinant", J.det(), 1)
equal("developing_map_inverse", F.subs(y, y-t*x*x/2), s.Matrix(z))


def G(k, i, j):
    return t if (k, i, j) == (1, 0, 0) else s.S.Zero


for i in range(2):
    for j in range(2):
        pulled = J.inv()*F.diff(z[i], z[j])
        equal(f"pullback_connection_{i}{j}", pulled,
              s.Matrix([G(k, i, j) for k in range(2)]))
        for k in range(2):
            equal(f"torsion_{k}{i}{j}", G(k, i, j)-G(k, j, i), 0)

for k in range(2):
    for ell in range(2):
        for i in range(2):
            for j in range(2):
                curvature = s.diff(G(k, j, ell), z[i])-s.diff(G(k, i, ell), z[j])
                curvature += sum(G(k, i, a)*G(a, j, ell)
                                 -G(k, j, a)*G(a, i, ell) for a in range(2))
                equal(f"curvature_{k}{ell}{i}{j}", curvature, 0)


def rho(a, b):
    return s.Matrix([[1, 0, a], [t*a, 1, b+t*a*a/2], [0, 0, 1]])


equal("holonomy_composition", rho(m, n)*rho(p, q), rho(m+p, n+q))
equal("holonomy_identity", rho(0, 0), s.eye(3))
equal("holonomy_inverse", rho(m, n)*rho(-m, -n), s.eye(3))
equal("holonomy_linear_determinant", rho(m, n)[:2, :2].det(), 1)
equal("developing_equivariance",
      F.subs({x: x+m, y: y+n}, simultaneous=True),
      (rho(m, n)*s.Matrix([*F, 1]))[:2, 0])

A, B, C = [s.Function(v)(x, y) for v in ["A", "B", "C"]]
g = s.Matrix([[A, B], [B, C]])


def Dg(i, j, k):
    return s.diff(g[j, k], z[i])-sum(G(a, i, j)*g[a, k]
                                    +G(a, i, k)*g[j, a] for a in range(2))


equal("codazzi_obstruction_all_metrics", Dg(0, 1, 0)-Dg(1, 0, 0),
      s.diff(B, x)-s.diff(A, y)-t*C)
equal("second_codazzi_component", Dg(0, 1, 1)-Dg(1, 0, 1),
      s.diff(C, x)-s.diff(B, y))
equal("central_metric_local_potential", s.hessian((x*x+y*y)/2, z), s.eye(2))

r, x0, y0, a, b = s.symbols("r x0 y0 a b", real=True)
gx = x0+a*r
gy = y0+b*r-t*a*a*r*r/2
equal("geodesic_x_equation", s.diff(gx, r, 2), 0)
equal("geodesic_y_equation", s.diff(gy, r, 2)+t*s.diff(gx, r)**2, 0)

# Constant coefficients already exhibit the obstruction. This is only a
# diagnostic; the arbitrary-function Codazzi calculation and Stokes argument
# handle all smooth metrics.
aa, bb, cc = s.symbols("aa bb cc", real=True)
equal("constant_metric_diagnostic",
      (Dg(0, 1, 0)-Dg(1, 0, 0)).subs({A: aa, B: bb, C: cc}).doit(), -t*cc)

print(json.dumps({"status": "PASS", "exact_identity_count": len(checks),
                  "checks": checks,
                  "analytic_step": "Periodicity or Stokes makes the derivative integral zero; positive definiteness makes the integral of C strictly positive.",
                  "limitations": "No finite sampling is used to certify the positivity or universal nonexistence assertion."},
                 indent=2, sort_keys=True))
