#!/usr/bin/env python3
"""Exact symbolic regression tests for row 1793, shared pass 1.

These verify examples and identity conventions. They are not a proof of the
general inverse-signature criterion. No numerical approximation is used.
"""
import json
from pathlib import Path
import sympy as s

I = s.I
t, r, x, y, u, v, b = s.symbols("t r x y u v b")
checks = []

def equal(label, actual, expected=0):
    residual = s.cancel(actual - expected)
    assert residual == 0, (label, residual)
    checks.append({"name": label, "result": "PASS"})

def truth(label, condition):
    assert condition, label
    checks.append({"name": label, "result": "PASS"})

def invariants(z, w, variable):
    p, q = s.diff(z, variable), s.diff(w, variable)
    h = s.cancel(s.diff(p, variable)/p - s.diff(q, variable)/q)
    U = s.cancel(-h*h/(4*p*q))
    V = s.cancel(I*s.diff(U, variable)/h)
    return h, U, V

# Formula convention and resonances.
h, U, V = invariants(t, t*t, t)
equal("monomial curvature square", U, -1/(8*t**3))
equal("monomial signed derivative", V, -3*I/(8*t**3))
equal("monomial slope", V/U, 3*I)
hr, Ur, Vr = invariants(t*t, t, t)
equal("reflection preserves u", Ur, U)
equal("reflection negates v", Vr, -V)

# A nonhomogeneous rational signature with a genuinely quadratic cover.
h, U, V = invariants(t, t**3+t, t)
equal("cubic source u", U, -9*t*t/(3*t*t+1)**3)
equal("cubic source v", V, -3*I*(6*t*t-1)/(3*t*t+1)**3)
Ur = -9*r/(3*r+1)**3
Vr = -3*I*(6*r-1)/(3*r+1)**3
equal("cubic signature rational inverse", I*Ur/(3*(2*I*Ur-Vr)), r)
F = 27*u**3+27*I*u*u*v+12*u*u-9*u*v*v+12*I*u*v-I*v**3-3*v*v
equal("cubic implicit signature", F.subs({u:Ur,v:Vr}))
eta = s.cancel(I*s.diff(Ur,r)/Vr)
omega = s.cancel((eta-s.diff(Ur,r)/Ur)/2)
froot = -(3*r+1)**2/(9*r)
equal("cubic eta logarithmic on base", eta, -3/(3*r+1))
equal("cubic square-root logarithmic identity", 2*omega, s.diff(froot,r)/froot)
a = (3*t*t+1)/(3*I*t)
rho = s.cancel(s.diff(U,t)/(2*V))
sigma = s.cancel(rho/U)
equal("cubic root square", a*a, froot.subs(r,t*t))
equal("cubic alpha exact", a*rho, 1)
equal("cubic beta exact", sigma/a, 3*t*t+1)
A = 3*I*r/(3*r+1)
B = (r+1)*(3*r+1)/(3*I)
equal("cubic base positive ODE", s.diff(A,r)+omega*A, s.diff(Ur,r)/(2*Vr))
equal("cubic base negative ODE", s.diff(B,r)-omega*B, s.diff(Ur,r)/(2*Ur*Vr))

# Elliptic source w^2=z^3-z. Expressions in y satisfy y^2=f.
f = x**3-x
fp = s.diff(f,x)
AA = 3*x**4-6*x*x-1
BB = 15*x**8-68*x**6+10*x**4+28*x*x-1
hh = s.cancel(fp/(2*f)-s.diff(fp,x)/fp)
UU = -AA**2/(8*f*f*fp**3)  # u=y*UU
VV = -3*I*BB/(8*f*f*fp**3) # v=y*VV
equal("elliptic h", hh, -AA/(2*f*fp))
equal("elliptic u coefficient", UU, -hh*hh/(2*fp))
equal("elliptic v coefficient", VV, I*(s.diff(UU,x)+UU*fp/(2*f))/hh)
equal("elliptic ratio", VV/(I*UU), 3*BB/(AA*AA))
U2 = AA**4/(64*f**3*fp**6)
equal("elliptic squared u", f*UU*UU, U2)
truth("elliptic u-square numerator denominator coprime", s.gcd(AA**4,f**3*fp**6)==1)
truth("elliptic ratio numerator denominator coprime", s.gcd(BB,AA*AA)==1)
truth("elliptic rational degree 21", max(s.degree(AA**4,x),s.degree(f**3*fp**6,x))==21)
truth("elliptic rational degree 8", max(s.degree(BB,x),s.degree(AA*AA,x))==8)
truth("elliptic degrees coprime", s.igcd(21,8)==1)
ae = 2*I/hh
omegae = (hh-(s.diff(UU,x)/UU+fp/(2*f)))/2
equal("elliptic canonical root already on base", s.diff(ae,x)/ae, omegae)
equal("elliptic alpha coefficient", ae*hh/(2*I), 1)
equal("elliptic beta coefficient times y", hh/(2*I*ae*UU), fp/2)

# A rational conic whose canonical cover has genus one; alpha is holomorphic.
Uc = (t-1)*(t-2)
Vc = I*t*(2*t-3)
equal("conic parameter recovered from signature", (-I*Vc-2*Uc+4)/3, t)
Fc = -4*u*u-4*I*u*v+7*u+v*v-I*v+2
equal("conic implicit signature", Fc.subs({u:Uc,v:Vc}))
etac = I*s.diff(Uc,t)/Vc
omegac = (etac-s.diff(Uc,t)/Uc)/2
equal("conic logarithmic eta", etac, 1/t)
equal("conic canonical square root", 2*omegac, s.diff(t/Uc,t)/(t/Uc))
# y^2=t*Uc and a=t/y. Compare coefficients after multiplying by y.
equal("conic alpha coefficient times y", t*s.diff(Uc,t)/(2*Vc), 1/(2*I))
equal("conic beta coefficient times y", (t*Uc)/t*s.diff(Uc,t)/(2*Uc*Vc), 1/(2*I*t))
truth("conic cover polynomial squarefree", s.gcd(t*Uc,s.diff(t*Uc,t))==1)

# Simpler logarithmic-pass / residue-fail graph.
Ug = t
Vg = I*t*(t-1)
etag = I*s.diff(Ug,t)/Vg
equal("quadratic graph eta", etag, 1/(t-1)-1/t)
ag = b/(b*b+1)
tg = b*b+1
alphag = s.cancel(ag*2*b/(2*Vg.subs(t,tg)))
betag = s.cancel((1/ag)*2*b/(2*Ug.subs(t,tg)*Vg.subs(t,tg)))
equal("quadratic graph alpha", alphag, -I/(b*b+1)**2)
equal("quadratic graph beta", betag, -I/(b*b*(b*b+1)))
equal("quadratic graph alpha residue i", s.residue(alphag,b,I), -s.Rational(1,4))
equal("quadratic graph alpha residue -i", s.residue(alphag,b,-I), s.Rational(1,4))
equal("quadratic graph beta residue i", s.residue(betag,b,I), s.Rational(1,2))
equal("quadratic graph beta residue -i", s.residue(betag,b,-I), -s.Rational(1,2))
equal("quadratic graph beta residue zero", s.residue(betag,b,0), 0)

# Two rational ODE solutions do not establish algebraicity of the root.
Ui, Vi = t*t, t**3
etai = I*s.diff(Ui,t)/Vi
omegai = (etai-s.diff(Ui,t)/Ui)/2
Ai, Bi = -t-I, I/t**2-1/t
equal("irregular eta double pole", etai, 2*I/t**2)
equal("irregular positive rational ODE", s.diff(Ai,t)+omegai*Ai, 1/t**2)
equal("irregular negative rational ODE", s.diff(Bi,t)-omegai*Bi, 1/t**4)

# Extra parametrization covers do not mean a different plane normalization.
_, Uextra, Vextra = invariants(t*t,t**4,t)
equal("redundant cover u", Uextra, -1/(8*t**6))
equal("redundant cover v", Vextra, -3*I/(8*t**6))

receipt = {
    "scope": "Exact regression checks, not a general theorem",
    "coefficient_field": "Q(i), symbolic rational-function arithmetic",
    "sympy_version": s.__version__,
    "checks_count": len(checks),
    "all_passed": True,
    "checks": checks,
}
out = Path(__file__).with_name("CHECK_RECEIPT.json")
out.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"all_passed":True,"checks_count":len(checks),"receipt":str(out)},indent=2))
