#!/usr/bin/env python3
"""Exact algebraic checks for PROOF.md. Requires Python 3 and SymPy.

This checks identities and a finite positivity grid. It does not prove the
parabolic existence theorem or replace the analytic proof of the inequalities.
Run: python verify.py --output verification_results.json
"""
import argparse
import json
import platform
from pathlib import Path
import sympy as S


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    checks = []

    def eq(name, lhs, rhs=0):
        assert S.simplify(lhs-rhs) == 0, (name, S.simplify(lhs-rhs))
        checks.append(name)

    u, v, p, x, q = S.symbols("u v p x q", nonnegative=True)
    e, d = S.Rational(1, 96), S.Rational(1, 4)
    phi = (2*S.log(1+u)+(2-e)/(1+u)+2*S.log(1+v)
           +d*u/(1+u)*(v/(1+v))**2)
    # For F(|s|^2, |z|^2), the diagonal Hessians are F_u+u F_uu
    # and F_v+v F_vv, while |F_{s bar z}|^2 = u v F_uv^2.
    a = S.diff(phi,u)+u*S.diff(phi,u,2)
    b = S.diff(phi,v)+v*S.diff(phi,v,2)
    cross = u*v*S.diff(phi,u,v)**2
    A = 4*p+(e+d*x*x)*(1-2*p)
    B = 2+2*d*p*x*(2-3*x)
    Q = 4*d*d*p*(1-p)*x**3*(1-x)
    px = {p:u/(1+u), x:v/(1+v)}
    eq("base Hessian identity", (1+u)**2*a, A.subs(px))
    eq("fiber Hessian identity", (1+v)**2*b, B.subs(px))
    eq("mixed Hessian identity", (1+u)**2*(1+v)**2*cross, Q.subs(px))
    eq("central initial second jet", a.subs(u,0), e+d*(v/(1+v))**2)
    eq("central fiber Hessian", b.subs(u,0), 2/(1+v)**2)
    eq("central mixed term", cross.subs(u,0), 0)

    # Explicit nonnegative-factor certificates on 0 <= p,x <= 1.
    Alow = e+(4-2*e-2*d)*p
    Blow = 2-2*d
    Qhigh = 4*d*d*p
    eq("A lower-bound certificate", A-Alow, d*x*x+2*d*p*(1-x*x))
    eq("B lower-bound certificate", B-Blow,
       2*d*((1-p)+p*(1-x)*(1+3*x)))
    eq("Q upper-bound certificate", Qhigh-Q,
       4*d*d*p*(p+(1-p)*((1-x)*(1+x+x*x)+x**4)))
    eq("determinant lower bound", Alow*Blow-Qhigh, S.Rational(1,64)+S.Rational(159,32)*p)
    eq("A slope", 4-2*e-2*d, S.Rational(167,48))

    # Coordinate-infinity chart checks on the curvature coefficients.
    U,V=S.symbols("U V", positive=True)
    base_inf = (2*S.log(1+U)+(2-e)*U/(1+U)+2*S.log(1+v)
                +d/(1+U)*(v/(1+v))**2)
    fiber_inf = (2*S.log(1+u)+(2-e)/(1+u)+2*S.log(1+V)
                 +d*u/(1+u)/(1+V)**2)
    both_inf = (2*S.log(1+U)+(2-e)*U/(1+U)+2*S.log(1+V)
                +d/(1+U)/(1+V)**2)
    for name, pot, su, zv, pp, xx in [
        ("base infinity",base_inf,U,v,1/(1+U),v/(1+v)),
        ("fiber infinity",fiber_inf,u,V,u/(1+u),1/(1+V)),
        ("both infinities",both_inf,U,V,1/(1+U),1/(1+V))]:
        aa=(1+su)**2*(S.diff(pot,su)+su*S.diff(pot,su,2))
        bb=(1+zv)**2*(S.diff(pot,zv)+zv*S.diff(pot,zv,2))
        cc=(1+su)**2*(1+zv)**2*su*zv*S.diff(pot,su,zv)**2
        subs={p:pp,x:xx}
        eq(name+": A",aa,A.subs(subs))
        eq(name+": B",bb,B.subs(subs))
        eq(name+": Q",cc,Q.subs(subs))

    def lap(f):
        return (x*(1-x)*S.diff(f,x,2)+(1-2*x)*S.diff(f,x))/2
    P1=2*x-1
    P2=6*x*x-6*x+1
    eq("P1 mean", S.integrate(P1,(x,0,1)))
    eq("P2 mean", S.integrate(P2,(x,0,1)))
    eq("P1 eigenvalue", lap(P1),-P1)
    eq("P2 eigenvalue", lap(P2),-3*P2)
    eq("quadratic decomposition", x*x,S.Rational(1,3)+P1/2+P2/6)
    eq("pushforward probability density", S.diff(v/(1+v),v),1/(1+v)**2)
    # Independently check the radial Laplacian coordinate change for degrees 0..5.
    for degree in range(6):
        f=x**degree
        fv=f.subs(x,v/(1+v))
        lhs=(1+v)**2*(S.diff(fv,v)+v*S.diff(fv,v,2))/2
        eq(f"radial Laplacian degree {degree}",lhs,lap(f).subs(x,v/(1+v)))
    w=e+d/S.Integer(3)+d*P1/2+d*q*P2/6
    mean=S.integrate(w,(x,0,1))
    eq("initial second jet",w.subs(q,1),e+d*x*x)
    eq("constant mean",mean,e+d/3)
    eq("exact PDE; q'= -2q",-2*q*S.diff(w,q),lap(w)+w-mean)
    eq("pole curvature formula",w.subs(x,0),e-d*(1-q)/6)
    target=w.subs({x:0,q:S.Rational(1,2)})
    eq("negative curvature at log(2)/2",target,-S.Rational(1,96))
    eq("first loss threshold",w.subs({x:0,q:S.Rational(3,4)}),0)
    initial=e+d*x*x
    eq("normalized initial pole derivative",(lap(initial)+initial-S.integrate(initial,(x,0,1))).subs(x,0),-d/3)
    eq("negative control: omit integral normalization",(lap(initial)+initial).subs(x,0),e)

    grid_checks=0
    for i in range(21):
        for j in range(21):
            subs={p:S.Rational(i,20),x:S.Rational(j,20)}
            av,bv,qv=(z.subs(subs) for z in [A,B,Q])
            assert av>0 and bv>0 and av*bv-qv>0
            assert av*bv-qv >= S.Rational(1,64)+S.Rational(159,32)*subs[p]
            grid_checks+=1
    report={
        "problem_id":30003571,
        "status":"PASS",
        "symbolic_identities":len(checks),
        "identity_names":checks,
        "exact_grid_points":grid_checks,
        "parameters":{"epsilon":str(e),"delta":str(d)},
        "negative_curvature":str(target),
        "time":"log(2)/2",
        "universal_positivity_certificate":"A*B-Q >= 1/64 + (159/32)*p > 0",
        "limitations":"Checks algebra only. Analytic flow existence, differentiation, and symmetry are justified in PROOF.md.",
        "python":platform.python_version(),
        "sympy":S.__version__,
    }
    text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text,end="")


if __name__=="__main__":
    main()
