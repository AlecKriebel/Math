#!/usr/bin/env python3
"""Rebuild S9 from reactions, proving signs with Bernstein coefficients.

This deliberately uses interval Bernstein coefficients in epsilon, rather than
the submission's reciprocal epsilon substitution. No submitted code is imported.
"""
from pathlib import Path
import json
import time
import sympy as S
from independent_nonlinear_checks import network, gauge_solve, zero, R

OUT=Path(__file__).resolve().parent
e,t,s,lam=S.symbols("epsilon t s lambda")
report={"interval":"0 < epsilon <= 1/1000", "certificates":[]}


def require(condition,label):
    if not condition:
        raise RuntimeError(label)


def bernstein(poly):
    """Exact Bernstein coefficients on [0,1/1000], stripping epsilon zeros."""
    p=S.Poly(poly,e)
    power=min(mon[0] for mon in p.monoms())
    p=S.Poly(S.cancel(p.as_expr()/e**power),e)
    n=p.degree()
    coefficients=[sum(p.nth(k)*R(1,1000)**k*R(S.binomial(i,k),S.binomial(n,k)) for k in range(i+1)) for i in range(n+1)]
    require(all(b>0 for b in coefficients),"strict Bernstein positivity")
    return {"epsilon_zero_order":power,"degree":n,"minimum_bernstein_coefficient":str(min(coefficients))}


def positive(expr,label):
    numerator,denominator=S.fraction(S.cancel(expr))
    if denominator.subs({s:0,e:R(1,1000)})<0:
        numerator=-numerator
        denominator=-denominator
    record={"name":label}
    for part,p in [("numerator",numerator),("denominator",denominator)]:
        polys=S.Poly(p,s)
        entries=[]
        for powers,coefficient in polys.terms():
            entries.append({"s_power":powers[0],**bernstein(coefficient)})
        require(polys.coeff_monomial(1)!=0,label+": s=0 coefficient is present")
        record[part]=entries
    report["certificates"].append(record)


if __name__=="__main__":
    started=time.time()
    A,B,c,rho=network(3)
    p=e
    u=1+R(16,9)*e+e**2/2
    q=R(1,2)-R(13,18)*e
    r=S.Matrix([1,-u,-p,q])
    d=[e*(3*e+8)/6,e*(4-9*e)/(9*e**2+32*e+18),e,16*e/(9-13*e)]
    D=S.diag(*d)
    M=A-D
    require(zero(M*r),"reaction-derived critical vector")
    ell3=(M[:3,:3].T).inv(method="DM")*(-M[3,:3].T)
    ell=S.Matrix([*ell3,1]).applyfunc(S.cancel)
    require(zero(M.T*ell),"reaction-derived left vector")
    rhs=-B(r,r)/4
    w0=gauge_solve(A,rhs,c)
    w2=((A-4*D).inv(method="DM")*rhs).applyfunc(S.cancel)
    require(zero((A-4*D)*w2-rhs),"reaction-derived second harmonic")
    forcing=(B(r,w0)+B(r,w2)/2).applyfunc(S.cancel)
    ip=S.cancel(ell.dot(r))
    cubic=S.cancel(sum(S.cancel(ell[i]*forcing[i]) for i in range(4))/ip)
    crossing=S.cancel(ell.dot(D*r)/ip)
    require(S.limit(cubic,e,0)==R(6,1379),"exact cubic constant term")
    require(S.limit(S.diff(cubic,e),e,0)==R(421985,11409846),"exact cubic linear term")
    positive(cubic,"reaction-derived cubic")
    positive(crossing,"reaction-derived mu crossing coefficient")
    for i,di in enumerate(d):
        positive(di,f"diffusion entry {i+1}")
    characteristic=(lam*S.eye(4)-A+t*D).det(method="domain-ge")
    coeffs=[S.cancel(S.Poly(characteristic,lam).coeff_monomial(lam**k)) for k in range(3,-1,-1)]
    a1,a2,a3,a4=coeffs
    require(zero(a4.subs(t,1)),"zero eigenvalue at t=1")
    H2=S.cancel(a1*a2-a3)
    H3=S.cancel(a3*H2-a1**2*a4)
    for name,expression in [("a1",a1),("a2",a2),("a3",a3),("a4/(t-1)",S.cancel(a4/(t-1))),("H2",H2),("H3",H3)]:
        positive(S.cancel(expression.subs(t,1+s)),name)
    report["cubic_fraction"]={"numerator":str(S.fraction(cubic)[0]),"denominator":str(S.fraction(cubic)[1])}
    report["cubic_series"]="6/1379 + (421985/11409846)*epsilon + O(epsilon**2)"
    report["elapsed_seconds"]=round(time.time()-started,3)
    report["status"]="PASS"
    (OUT/"INDEPENDENT_NEAR_THRESHOLD_RESULTS.json").write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: {len(report['certificates'])} Bernstein positivity certificates in {report['elapsed_seconds']} seconds")
