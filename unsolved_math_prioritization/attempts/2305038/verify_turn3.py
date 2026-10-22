#!/usr/bin/env python3
"""Exact identities for the defect-monotonicity proof. Requires SymPy."""
import sympy as s, json
from pathlib import Path
r,a,u,x,k,k0,v,t=s.symbols('r a u x k k0 v t', real=True)
checks=0
def ck(z):
 global checks
 assert s.simplify(z)==0,z
 checks+=1
B=1-a*a; S=1-r*r; L=1+u+2*a*x
Den=1-a*a*r*r+(a*a-r*r)*u+2*a*S*x
P2=a*a*(1-u)**2+4*u+4*a*(1+u)*x+4*a*a*x*x
ck(Den-S*L-B*(r*r-u));ck(L**2-P2-B*(1-u)**2)
ck(((r*r-u)/(S*(1+u))).subs(u,(1-k)/(1+k))-(k/((1-r*r)/(1+r*r))-1)/2)
ck((L/(1+u)).subs({u:(1-k)/(1+k),x:v/(1+k)})-(1+a*v))
# Differentiate Q treating T'=-Bk/T and b'=B/(2k0).
D=1+a*v;b=B*(k/k0-1)/2
Q=(t+b)/(D+b)
qd=s.diff(Q,k)+s.diff(Q,t)*(-B*k/t)
ck(qd-B/(D+b)**2*((D-t)/(2*k0)-k*(D+b)/t))
R=3-2*s.sqrt(2); K0=2*s.sqrt(2)/3
ck((1-R*R)/(1+R*R)-K0)
ck(s.Rational(4,3)/(2*K0)-1/s.sqrt(2))
ck(1/s.sqrt(2)-K0+s.sqrt(2)/6)
# The exact displacement-odds formula becomes (1-a)^2(1-v)/(32(D+b)).
odds=r*r*(1-a)**2*(1+u-2*x)/(S*Den)
ck(odds.subs({u:(1-k)/(1+k),x:v/(1+k),r:R})-(1-a)**2*(1-v)/(32*(D+b.subs(k0,K0))))
# Numerical diagnostics are omitted: all identities above are exact.
out={'status':'PASS','symbolic_identity_checks':checks,'scope':'Exact interior-jet normalization, displacement, and monotonicity derivative; interval signs and reduction justified in TURN_3.md','full_bundled_target_solved':False}
print(json.dumps(out,indent=2));Path(__file__).with_name('TURN_3_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
