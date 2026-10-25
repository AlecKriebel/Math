#!/usr/bin/env python3
"""Independent algebraic/finite-matrix controls; never a proof of EPnI.

Uses only the Python standard library. Finite annihilators do NOT obey CCR:
the negative control below explicitly measures the otherwise hidden defect.
"""
from fractions import Fraction as Q
from math import sinh, cosh, log, sqrt, pi
from cmath import exp
from pathlib import Path
import json


class P:
    def __init__(self, value=0):
        if isinstance(value, P): self.c = dict(value.c)
        elif isinstance(value, str): self.c = {(value,): Q(1)}
        elif isinstance(value, dict): self.c = {k: Q(v) for k, v in value.items() if v}
        else: self.c = {(): Q(value)} if value else {}
    def __add__(a, b):
        b=P(b); c=dict(a.c)
        for k,v in b.c.items(): c[k]=c.get(k,Q(0))+v
        return P(c)
    __radd__=__add__
    def __neg__(a): return P({k:-v for k,v in a.c.items()})
    def __sub__(a,b): return a+-P(b)
    def __rsub__(a,b): return P(b)+-a
    def __mul__(a,b):
        b=P(b); c={}
        for k,v in a.c.items():
            for l,w in b.c.items():
                key=tuple(sorted(k+l));c[key]=c.get(key,Q(0))+v*w
        return P(c)
    __rmul__=__mul__
    def __pow__(a,n):
        z=P(1)
        for _ in range(n):z=z*a
        return z
    def record(a): return {"*".join(k) or "1":str(v) for k,v in sorted(a.c.items())}


def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def adj(a): return [list(x) for x in zip(*[[z.conjugate() for z in row] for row in a])]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a): return [[c*x for x in row] for row in a]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def diag(v):return [[v[i] if i==j else 0j for j in range(len(v))] for i in range(len(v))]


def main():
    out={"scope":"Exact algebra and illustrative finite matrix controls only; the analytic proof audit is DERIVATIONS.md."}
    A,B,E,K,M,eps,zeta,T,Delta=[P(x) for x in ("A","B","E","K","M","eps","zeta","P","Delta")]
    station=(B-(E+K))-(1+eps)*(A-E)+eps*(-E-M)+zeta*T
    expected=B-(1+eps)*A-eps*M-K+zeta*T
    assert not (station-expected).c
    wrong=(B-(E+K))-(1+eps)*(A-E)+(eps+Delta)*(-E-M)+zeta*T
    assert (wrong-expected).c
    out["stationarity"]={"exact_identity_difference":(station-expected).record(),"wrong_energy_penalty_residual":(wrong-expected).record()}

    N,n,r=[P(x) for x in ("N","n","r")]
    drift=(r+1)*N*(N**4-(N+1)**4)+r*(N+n)*((N+2)**4-(N+1)**4)
    max_degree=max(k.count("N") for k in drift.c)
    top={k:v for k,v in drift.c.items() if k.count("N")==4}
    assert max_degree==4 and top=={("N",)*4:Q(-4)}
    out["fourth_moment_drift"]={"expanded":drift.record(),"max_N_degree":max_degree,"leading_N_coefficient":-4}

    def f(x): return x/sinh(x) if x else 1.0
    def b(x): return x*cosh(x)/sinh(x) if x else 1.0
    scalar=[]
    for x,y in [(0,0),(0,1.2),(1.2,0),(1.2,1.2),(1.2,-1.2),(7,-7),(-3,2),(1.1,-.7),(-2.4,-.8)]:
        s,t=f(x)**2,f(y)**2; a=b(x)+b(y)
        if x*x==y*y:
            e=.5 if not x else s*(b(x)-1)/(b(x)-s)
        else: e=(t-s)/(2*(b(x)-b(y)))
        minimum=(a-(x-y)**2/(a+2*e))/2
        target=f(x)*f(y)/f(x+y)
        err=abs(minimum-target)
        assert e>0 and err<2e-12
        scalar.append({"x":x,"y":y,"E_over_m":e,"absolute_error":err})
    x,y=1.1,-.7;s,t=f(x)**2,f(y)**2;a=b(x)+b(y);e=(t-s)/(2*(b(x)-b(y)))
    wrong_e_residual=(a-(x-y)**2/(a+4*e))/2-f(x)*f(y)/f(x+y)
    assert abs(wrong_e_residual)>1e-3
    out["scalar_interpolation"]={"controls":scalar,"doubled_E_negative_control_residual":wrong_e_residual}

    d=4;p=[.5,.25,.125,.125];rr=.7;h=log(1+1/rr)
    U=[[exp(2j*pi*i*j/d)/sqrt(d) for j in range(d)] for i in range(d)]
    rho=mm(mm(U,diag(p)),adj(U));H=mm(mm(U,diag([-log(x) for x in p])),adj(U))
    ann=[[sqrt(j) if i+1==j else 0j for j in range(d)] for i in range(d)]
    cre=adj(ann);mu=tr(mm(rho,ann));I=diag([1]*d)
    centered=add(ann,scale(-mu,I));dc=mm(mm(adj(U),centered),U)
    def dissipator(op):
        gram=mm(adj(op),op)
        return add(mm(mm(op,rho),adj(op)),scale(-.5,add(mm(gram,rho),mm(rho,gram))))
    delta=add(scale(rr+1,dissipator(ann)),scale(rr,dissipator(cre)))
    sigma=(tr(mm(delta,H))/h).real
    norm=0.0
    for l in range(d):
        for k in range(d):
            v=log(p[l]/p[k])/h; kk=(rr+1)*p[k]-rr*p[l]
            norm+=(1-v)*kk*abs(dc[l][k])**2
    energy=tr(mm(rho,mm(adj(centered),centered))).real
    comm=add(mm(ann,cre),scale(-1,mm(cre,ann)))
    commmean=tr(mm(rho,comm)).real
    corrected_residual=norm-sigma-(energy-rr*commmean)
    naive_ccr_residual=norm-sigma-(energy-rr)
    predicted_boundary=rr*d*rho[-1][-1].real
    assert abs(mu)>.01 and abs(tr(mm(rho,H))-sum(-q*log(q) for q in p))<1e-12
    assert abs(corrected_residual)<2e-12
    assert abs(naive_ccr_residual-predicted_boundary)<2e-12 and abs(naive_ccr_residual)>.1
    out["noncommuting_finite_matrix_control"]={
        "dimension":d,"spectral_probabilities":p,"reference_r":rr,"mean_abs":abs(mu),
        "sigma":sigma,"centered_defect_norm_squared":norm,"centered_energy":energy,
        "actual_commutator_mean":commmean,"corrected_identity_residual":corrected_residual,
        "incorrect_infinite_CCR_residual":naive_ccr_residual,"predicted_top_boundary_residual":predicted_boundary,
        "interpretation":"Finite Fock truncation falsely used as exact CCR is detected. This is a control on the audit, not evidence for all-dimensional EPnI."}
    Path(__file__).with_name("control_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"algebraic_checks":"verified","negative_controls":"detected","finite_matrix_CCR_correction_residual":corrected_residual},indent=2))


if __name__=="__main__": main()
