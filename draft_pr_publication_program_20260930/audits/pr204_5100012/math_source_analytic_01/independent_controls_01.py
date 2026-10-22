#!/usr/bin/env python3
"""Small adversarial controls. Explicit failures remain active under optimization."""
from pathlib import Path
from math import gcd
import json,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'pr200_5100007'/'math_algebra_family_01'/'runtime_packages'))
import mpmath as mp
import sympy as sy
mp.mp.dps=80
checks=[]
def require(label,truth,detail=None):
    if not truth: raise RuntimeError(f'{label}: {detail}')
    checks.append(label)
def close(label,x,y,tol='1e-55'):
    err=abs(x-y)/max(1,abs(x),abs(y))
    require(label,err<mp.mpf(tol),mp.nstr(err,12))
    return mp.nstr(err,12)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(points): return sum(det(p,q) for p,q in zip(points,points[1:]+points[:1]))/2
# Independent symbolic residue reduction, using d²=1-k²s² and c²=1-s².
s,d,k=sy.symbols('s d k')
# H=k² cn/(1+dn); H'= -k² sn dn/(1+dn)+k^4 sn cn²/(1+dn)².
hprime=-k*k*s*d/(1+d)+k**4*s*(1-s*s)/(1+d)**2
claimed=-k*k*s*(d+1-k*k)/(1+d)**2
num=sy.factor((hprime-claimed)*(1+d)**2)
require('symbolic_residue_derivative',sy.rem(num,sy.Poly(d*d-1+k*k*s*s,d).as_expr(),d)==0,str(num))
records=[];repeated=None
for kval in ['0.00001','0.8','0.999']:
    k=mp.mpf(kval);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m);Ki=mp.ellipk(1-m)
    sn=lambda u:mp.ellipfun('sn',u,m)
    cn=lambda u:mp.ellipfun('cn',u,m)
    dn=lambda u:mp.ellipfun('dn',u,m)
    for n,tau in [(3,1),(4,1),(5,2),(6,1),(7,3),(8,3),(12,5)]:
        require('coprime winding',gcd(n,tau)==1)
        v=2*K*tau/n;step=2*v;aa=dn(v)/cn(v);bb=kp/cn(v)
        Q=lambda u:(-kp*kp*sn(u)/dn(u)**2,kp*cn(u)/dn(u)**2)
        S=lambda w:sum(dn(w+j*step) for j in range(n))
        T=lambda u:area([Q(u+j*step) for j in range(n)])
        predicted=sn(step)*(dn(step)+kp*kp)/(1+dn(step))**2
        require('coefficient strictly positive',predicted>0)
        errs=[];vals=[]
        for phase in ['0.13','0.41','1.1']:
            w=mp.mpf(phase)*K
            P=[(-aa*sn(w+j*step),bb*cn(w+j*step)) for j in range(n)]
            feet=[]
            for p,q in zip(P,P[1:]+P[:1]):
                z=(q[0]-p[0],q[1]-p[1]);cross=det(p,q);norm=z[0]**2+z[1]**2
                feet.append((cross*z[1]/norm,-cross*z[0]/norm))
            A,B=area(P),area(feet)
            errs.append(close('explicit coefficient vs direct chord feet',B,predicted*S(w+K+v)))
            vals.append(A*B)
        if n%4!=2:
            for val in vals[1:]:close('required product constant',val,vals[0])
        else:
            require('wrong parity variation',max(vals)-min(vals)>mp.mpf('1e-60'))
        r=K+1j*Ki
        # At r, the combined area has residue (N/m)*(-i)*C_T.
        multiplicity=1 if n%2 else 2
        residue_errors=[]
        for eps in [mp.mpf('1e-12'),mp.mpf('1e-16')]:
            residue_errors.append(close('combined simple residue including N3 N4',eps*T(r+eps),-1j*multiplicity*predicted,'1e-20'))
        records.append({'modulus':kval,'N':n,'winding':tau,'C_T':mp.nstr(predicted,20),'real_formula_max_scaled_error':str(max(map(mp.mpf,errs))),'residue_scaled_errors':residue_errors})
        if kval=='0.8' and n==6:
            repeated={'least_period':6,'listed_period':12,'repetitions':2,'caustic_axes':['1',mp.nstr(kp,30)],'outer_axes':[mp.nstr(aa,30),mp.nstr(bb,30)],'lambda':mp.nstr(bb*bb-kp*kp,30),'phases_in_units_K':['0.13','0.41','1.1'],'listed_signed_area_products':[mp.nstr(4*x,35) for x in vals],'counterexample':'Repeated least-six orbit listed twice satisfies listed N=12 but product varies. Thus unrestricted listed-N reading is false.'}
# Test explicit enforcement in this new code.
try:
    require('deliberately_false_sentinel',False)
except RuntimeError:
    enforcement=True
else:
    enforcement=False
if not enforcement: raise RuntimeError('False sentinel incorrectly accepted')
result={'status':'PASS','precision_digits':mp.mp.dps,'active_checks':len(checks),'optimization_flag':sys.flags.optimize,'explicit_false_rejection':enforcement,'records':records,'repeated_list_counterexample':repeated,'limits':'Noninterval high precision diagnostics; residue formula and general proof are supplied in AUDIT_REPORT_01.md. These finite controls do not prove universal constancy.'}
print(json.dumps(result,indent=2))
