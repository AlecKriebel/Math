#!/usr/bin/env python3
"""Exact ancillary priority implications; SymPy required; no numerical claims."""
from pathlib import Path
import datetime, hashlib, json
import sympy as sp

checks = []
def zero(label, expression):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    if sp.expand(numerator) != 0:
        raise ArithmeticError(label + ": nonzero residual " + str(numerator))
    checks.append({"check": label, "exact_zero": True})

k,s,cu,du,h,cv,dv,a,b = sp.symbols("k s cu du h cv dv a b", nonzero=True)
D=1-k*k*h*h*s*s
sm=(s*cv*dv-h*cu*du)/D
sp_=(s*cv*dv+h*cu*du)/D
cm=(cu*cv+s*h*du*dv)/D
cp=(cu*cv-s*h*du*dv)/D
qx=-a*s*dv/cv
qy=b*cu/cv
sub={cu**2:1-s*s,dv**2:1-k*k*h*h}
def reduce_quadrics(e):
    n,d=sp.fraction(sp.cancel(e))
    for _ in range(3):
        n=sp.expand(n).subs(sub);d=sp.expand(d).subs(sub)
    return sp.cancel(n/d)
zero("intersection on tangent at u-v",reduce_quadrics(-qx*sm/a+qy*cm/b-1))
zero("intersection on tangent at u+v",reduce_quadrics(-qx*sp_/a+qy*cp/b-1))
zero("determinant of tangent normal matrix",reduce_quadrics(sp_*cm-sm*cp-2*h*cv*du/D))
x1,y1,x2,y2=sp.symbols("x1 y1 x2 y2")
zero("linear map cross product scaling",(x1*dv/cv)*(y2/cv)-(y1/cv)*(x2*dv/cv)-(dv/cv**2)*(x1*y2-y1*x2))
CA,CR,C,Lam,kp=sp.symbols("CA CR C Lambda kp",nonzero=True)
AQ,Sw=sp.symbols("AQ Sw")
zero("focal inverse to tangent polygon area ratio",(CR*Sw)-CR*cv**2/(2*CA*dv)*(2*CA*dv/cv**2*Sw))
# The explicit formula substitutes the independently established C_R=2 C Lambda/kp.
zero("explicit inverse to tangent ratio",(CR*cv**2/(2*CA*dv)).subs(CR,2*C*Lam/kp)-C*Lam*cv**2/(CA*dv*kp))
# Universal combinatorial identity: all even/odd ordered pairs occur once in each direction.
from collections import Counter
for m in range(2,41):
    p=2*m
    lhs=Counter()
    for r in range(1,p,2):
        for j in range(p):
            lhs[tuple(sorted((j,(j+r)%p)))]+=1
    rhs=Counter({(j,l):2 for j in range(0,p,2) for l in range(1,p,2)})
    rhs=Counter({tuple(sorted(key)):val for key,val in rhs.items()})
    if lhs != rhs:
        raise ArithmeticError("cyclic cross correlation partition, m="+str(m))
checks.append({"check":"generic even-odd pair partition finite diagnostics m=2..40", "exact_zero":True,"universal_proof":"Each even-odd pair appears once for each direction j->j+r and j+r->j; r ranges over all odd residues."})
source=Path(__file__).read_bytes()
result={"schema":"pr207-general-method-priority-exact-controls-v1","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_sha256":hashlib.sha256(source).hexdigest(),"sympy_version":sp.__version__,"all_checks_pass":True,"checks":checks,"limitation":"Ancillary exact implications only; this is not a rerun of the target theorem's universal focal-edge proof and not a novelty certificate."}
print(json.dumps(result,indent=2))
