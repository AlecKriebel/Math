#!/usr/bin/env python3
"""Independent exact checks; the analytic proofs are in the written audit."""
import hashlib
import json
from pathlib import Path
import sympy as S

root = Path(__file__).resolve().parents[1]
checks = []

def check(name, statement):
    assert bool(statement), name
    checks.append({"name": name, "passed": True})

m, b, c = S.symbols("m b c", real=True)
s = m+b+c
gamma = s-3
eta = 2*(3*m+b+2*c-6)
tau = m+b-2-3*gamma
check("barrier third-row stress exponent gap", S.expand(4*m+c-5-tau-eta) == 0)
check("third-row cofactor stress relative order", S.expand(3*m+b+c-5-(4*m+c-5)-(b-m)) == 0)
check("third-row determinant-square relative order", S.expand(2*m+2*b+c-5-(4*m+c-5)-2*(b-m)) == 0)
base = 5*m-5
check("first-row cofactor gap", S.expand(2*m+3*b-5-base-3*(b-m)) == 0)
check("first-row determinant-square gap", S.expand(gamma+b+c-2-base-(2*s-6*m)) == 0)
check("first-row barrier gap", S.expand(b+c-2-3*gamma-base-2*(6-s-3*m)) == 0)
check("tied minimum puts profile in positive-eta range", S.expand(eta.subs(b,m)-4*(s.subs(b,m)-3)) == 0)
check("annular positive-energy exponent", S.expand(3+6*(m-1)-(6*m-3)) == 0)
check("annular barrier exponent", S.expand(3-2*gamma-(9-2*s)) == 0)
check("scalar removability flux exponent", S.expand(2+5*(m-1)-(5*m-3)) == 0)

t, u, v, d = S.symbols("t u v d", positive=True)
jt = (1-t)*u+t*v
check("mixed moment barrier derivative", S.simplify(S.diff(jt**-2,t).subs(t,0)-(2/u**2-2*v/u**3)) == 0)
check("zero-endpoint secant exact formula", S.factor(((1-t)**-2-1)/t-(2-t)/(1-t)**2) == 0)
check("secant upper bound at one half", ((1-t)**-2-1).subs(t,S.Rational(1,2))/S.Rational(1,2) == 6)
check("small-amplitude source tends to two", S.limit((2-t)/(1-t)**2,t,0) == 2)

F = S.Matrix([[2,1,0],[0,2,1],[1,0,2]])
A = S.Matrix([[1,0,2],[0,1,0],[1,1,1]])
B = S.Matrix([[2,0,1],[1,2,0],[0,1,1]])
H = F.inv()
Dk = A*F+B
Du = A+B*H
check("graph-transform derivative identity", Du == Dk*H)
check("graph-transform determinant change of variables", S.simplify(Du.det()*F.det()-Dk.det()) == 0)
check("graph-transform cofactor change of variables", Du.cofactor_matrix()*F.det() == Dk.cofactor_matrix()*F.T)
q = S.Matrix([2,-1,3])
check("graph-transform test gradient identity", Du.cofactor_matrix()*q*F.det() == Dk.cofactor_matrix()*(F.T*q))
R = S.Matrix([1,2,-1])*S.Matrix([[2,-1,1]])
Ft = F+t*R
check("rank-one determinant is affine", S.expand(Ft.det()-F.det()-t*(F+R).det()+t*F.det()) == 0)
check("rank-one cofactor is affine", (Ft.cofactor_matrix()-F.cofactor_matrix()-t*((F+R).cofactor_matrix()-F.cofactor_matrix())).applyfunc(S.expand) == S.zeros(3))
check("inverse addition determinant identity", S.factor((H-t*S.diag(1,0,0)).det()-H.det()*(1-t*F[0,0])) == 0)

L = S.symbols("L", positive=True)
H1 = S.diag(L**5,L**-1,L**-1)
H2 = S.diag(L**-1,L**5,L**-1)
mixed = (H1+H2).cofactor_matrix()-H1.cofactor_matrix()-H2.cofactor_matrix()
check("matrix endpoint determinant scale", H1.det() == L**3 and H2.det() == L**3)
check("matrix mixed cofactor obstruction", S.expand(mixed[2,2]-L**10-L**-2) == 0)

x, y, eps, rho = S.symbols("x y eps rho", real=True, positive=True)
Q = S.Matrix([x/S.sqrt(x*x+y*y+eps*eps),y/S.sqrt(x*x+y*y+eps*eps)])
check("regularized axial second minor", S.simplify(Q.jacobian([x,y]).det()-eps**2/(x*x+y*y+eps*eps)**2) == 0)
mass = S.integrate(2*S.pi*eps**2*rho/(rho*rho+eps*eps)**2,(rho,0,1))
check("axial cofactor mass", S.simplify(mass-S.pi/(1+eps*eps)) == 0)
theta = S.symbols("theta", real=True)
check("axial defect flux coefficient", S.integrate(S.cos(theta)**2,(theta,0,2*S.pi)) == S.pi)

z = S.symbols("z", real=True, positive=True)
rr = x*x+y*y+z*z
f = z**3*rr**(-S.Rational(3,4))+z*S.sqrt(rr)
expected_j = rr**S.Rational(1,4)*(z*z/rr)*(3-S.Rational(3,2)*z*z/rr)+S.sqrt(rr)*(1+z*z/rr)
check("angularly repaired diagnostic Jacobian", S.simplify(S.diff(f,z)-expected_j) == 0)
axis_j = S.Rational(3,2)*S.sqrt(t)+2*t
check("diagnostic barrier divergence coefficient", S.limit(6*d*S.diff(axis_j,t)*axis_j**-4*t**S.Rational(5,2),t,0,dir="+") == S.Rational(8,9)*d)
check("diagnostic angular scaling", -1-S.Rational(3,2)*S.Rational(1,2) == -S.Rational(7,4))
check("diagnostic radial barrier integrability exponent", 2-S.Rational(7,4) == S.Rational(1,4))
check("isolated inverse-amplitude threshold", 2-9*S.Rational(1,3) == -1)

Delta = S.symbols("Delta", positive=True)
J = eps*Delta
remainder = J**-2-eps**-2+2*eps**-3*(J-eps)
check("barrier-normalized relative excess", S.simplify(eps**2*remainder-(Delta**-2+2*Delta-3)) == 0)
Aeps = S.diag(1,1,eps)
M = S.diag(2,S.Rational(1,2),1)
check("volume-preserving normalized strain stays nonzero", sum(q*q for q in Aeps*M-Aeps) == S.Rational(5,4))
bad = S.diag(-2,-S.Rational(1,2),1)
check("positive endpoint has negative midpoint determinant", bad.det() == 1 and ((bad+S.eye(3))/2).det() == -S.Rational(1,8))

r, kap = S.symbols("r kap", positive=True)
logr = S.log(S.E/r)
radius = r**S.Rational(3,2)*logr**kap
stretch = r**S.Rational(1,2)*logr**kap
qrad = S.Rational(3,2)-kap/logr
jrad = r**S.Rational(3,2)*logr**(3*kap)*qrad
check("projection-obstruction radial derivative", S.simplify(S.diff(radius,r)-stretch*qrad) == 0)
check("projection-obstruction Jacobian", S.simplify(stretch**2*S.diff(radius,r)-jrad) == 0)
check("projection-obstruction inverse target formula", S.simplify(jrad**-1-radius**-1*logr**(-2*kap)/qrad) == 0)
check("projection-obstruction critical barrier density", S.simplify(r*r*jrad**-2-1/(r*logr**(6*kap)*qrad*qrad)) == 0)
ell = S.symbols("ell", positive=True)
check("target logarithm relation", S.expand(1-S.Rational(3,2)*(1-ell)-kap*S.log(ell)-(S.Rational(3,2)*ell-S.Rational(1,2)-kap*S.log(ell))) == 0)

meta = json.loads((root/"literature/SOURCE_INSPECTION_MANIFEST.json").read_text())["sources"][0]
data = (root/"literature/private_sources/hajlasz_schikorra_tyson2013v3.pdf").read_bytes()
check("primary weak-pullback source bytes and hash", len(data) == meta["bytes"] and hashlib.sha256(data).hexdigest() == meta["sha256"])

result = {
    "purpose": "Exact algebra and source-metadata checks supporting the independent analytic audit.",
    "total_checks": len(checks),
    "checks": checks,
    "benchmark_proved": False,
    "benchmark_counterexample": False,
}
Path(__file__).with_name("AUDIT_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"passed": True, "total_checks": len(checks)},indent=2))
