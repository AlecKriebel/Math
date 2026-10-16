#!/usr/bin/env python3
"""Independent source/quantifier audit. No submitted verification code imported.
Requires mpmath 1.3.0 and SymPy 1.14.0; optional --packages points to runtime.
Numerics are falsification diagnostics, not interval-certified proof.
"""
import argparse, json, sys, math
from pathlib import Path
from datetime import datetime, timezone
ap=argparse.ArgumentParser(); ap.add_argument('--packages'); ap.add_argument('--output')
args=ap.parse_args()
if args.packages: sys.path.insert(0,args.packages)
import mpmath as mp
import sympy as sp
mp.mp.dps=65
kap,t,S=sp.symbols('kap t S')
q=1-t; U=1-2*kap*t+kap*t*t; V=1-2*t+kap*t*t
raw=(U+kap*V*S)**2-4*kap*(1-kap*t)**2*q*q*S
fac=(1-kap*S)*(U*U-kap*V*V*S)
assert sp.expand(raw-fac)==0
assert sp.expand(U+V-2*q*(1-kap*t))==0

def serial(x): return mp.nstr(x,35)
def cross(v,w): return v[0]*w[1]-v[1]*w[0]
def norm(v): return mp.sqrt(v[0]*v[0]+v[1]*v[1])
def diff(v,w): return (v[0]-w[0],v[1]-w[1])
def evaluate(k,N,tau,phase):
    m=k*k; K=mp.ellipk(m); v=2*K*tau/N; delta=2*v
    alpha=mp.mpf(2); beta=alpha*mp.sqrt(1-m); c=alpha*k
    sn=lambda z: mp.ellipfun('sn',z,m)
    cn=lambda z: mp.ellipfun('cn',z,m)
    dn=lambda z: mp.ellipfun('dn',z,m)
    C=cn(v); D=dn(v); a=alpha*D/C; b=beta/C
    def P(u): return (-a*sn(u),b*cn(u))
    def Qdirect(u):
        A=P(u-v); B=P(u+v)
        nx1=A[0]/(a*a); ny1=A[1]/(b*b)
        nx2=B[0]/(a*a); ny2=B[1]/(b*b)
        det=nx1*ny2-nx2*ny1
        return ((ny2-ny1)/det,(nx1-nx2)/det),abs(det)
    Rplus=mp.mpf(1); Rminus=mp.mpf(1); outer_error=mp.mpf(0)
    caustic_error=mp.mpf(0); reflection_error=mp.mpf(0); mindet=mp.inf
    for j in range(N):
        u=phase*K+j*delta
        Q,det=Qdirect(u); mindet=min(mindet,det)
        Qformula=(-a*D/C*sn(u),b/C*cn(u))
        outer_error=max(outer_error,norm(diff(Q,Qformula))/(1+norm(Q)))
        Rplus*=norm(diff(Q,(c,0))); Rminus*=norm(diff(Q,(-c,0)))
        Pm=P(u-v); Pp=P(u+v)
        nl=(Pp[1]-Pm[1],Pm[0]-Pp[0]); d=nl[0]*Pm[0]+nl[1]*Pm[1]
        scale=alpha*alpha*nl[0]**2+beta*beta*nl[1]**2
        caustic_error=max(caustic_error,abs(d*d-scale)/(1+scale))
        Pb=P(u-v-delta)
        incoming=diff(Pm,Pb); outgoing=diff(Pp,Pm)
        ni=norm(incoming); no=norm(outgoing)
        ref=(outgoing[0]/no-incoming[0]/ni,outgoing[1]/no-incoming[1]/ni)
        nn=(Pm[0]/(a*a),Pm[1]/(b*b))
        reflection_error=max(reflection_error,abs(cross(ref,nn))/(1+norm(nn)))
    return Rplus,Rminus,outer_error,caustic_error,reflection_error,mindet

rows=[]; max_const=mp.mpf(0); max_focus=mp.mpf(0)
max_outer=mp.mpf(0); max_caustic=mp.mpf(0); max_reflect=mp.mpf(0)
for kstr in ['0.05','0.65','0.98']:
    k=mp.mpf(kstr)
    for N in [4,8,12,16,20,24]:
        for tau in range(1,N//2):
            if math.gcd(tau,N)!=1: continue
            vals=[evaluate(k,N,tau,mp.mpf(x)) for x in ['0','0.37','1.13']]
            error=max(abs(z[0]/vals[0][0]-1) for z in vals)
            focus=max(abs(z[1]/z[0]-1) for z in vals)
            max_const=max(max_const,error); max_focus=max(max_focus,focus)
            max_outer=max(max_outer,max(z[2] for z in vals))
            max_caustic=max(max_caustic,max(z[3] for z in vals))
            max_reflect=max(max_reflect,max(z[4] for z in vals))
            rows.append({'modulus':kstr,'least_period':N,'turning_number':tau,
                         'relative_product_spread':serial(error),'focus_relative_error':serial(focus)})
assert max_const<mp.mpf('1e-55')
assert max_focus<mp.mpf('1e-55')
assert max_outer<mp.mpf('1e-55')
assert max_caustic<mp.mpf('1e-55')
assert max_reflect<mp.mpf('1e-55')
# Deliberately violate least-period convention: cover primitive six twice.
control=[evaluate(mp.mpf('0.65'),6,1,mp.mpf(x))[0] for x in ['0','0.37','1.13']]
assert abs(control[1]/control[0]-1)>mp.mpf('1e-5')
cover=[x*x for x in control]
# Exact finite rational-orbit control, independent of function evaluation.
from fractions import Fraction as F
for N in range(4,101,4):
    for tau in range(1,N//2):
        if math.gcd(tau,N)!=1: continue
        m=N//2; orbit={F(j*tau,m)%1 for j in range(m)}
        assert len(orbit)==m and F(1,2) in orbit
assert F(1,2) not in {F(j,3)%1 for j in range(3)}
result={'utc':datetime.now(timezone.utc).isoformat(),'software':{'python':sys.version,
        'mpmath':mp.__version__,'sympy':sp.__version__},
        'symbolic_factorization':'zero expanded polynomial residual',
        'families_checked':len(rows),'phases_per_family':3,'mpmath_decimal_digits':mp.mp.dps,
        'max_relative_product_spread':serial(max_const),'max_focus_relative_error':serial(max_focus),
        'max_tangent_formula_relative_error':serial(max_outer),
        'max_caustic_tangency_relative_error':serial(max_caustic),
        'max_reflection_cross_residual':serial(max_reflect),
        'negative_control':{'modulus':'0.65','least_period':6,'turning_number':1,
            'phases_as_K_multiples':['0','0.37','1.13'],
            'six_product':[serial(x) for x in control],
            'nominal_twelve_double_cover_product':[serial(x) for x in cover],
            'relative_variation_first_to_second':serial(cover[1]/cover[0]-1)},
        'rational_orbit_tests':'all primitive N divisible by4 up to100; primitive6 negative control',
        'families':rows,'limitations':'Numerical outputs are not interval certificates; exact analytic arguments are in DERIVATIONS.md.'}
if args.output: Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='families'},indent=2))
