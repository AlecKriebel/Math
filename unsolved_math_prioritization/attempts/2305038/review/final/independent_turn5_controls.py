#!/usr/bin/env python3
"""Independent exact audit controls; no author code is imported."""
import argparse,hashlib,json
from math import comb
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--proof-dir',required=True);args=ap.parse_args()
p=Path(args.proof_dir);m=json.loads((p/'TURN_5_MANIFEST.json').read_text())
for name,digest in m['files'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
checks=0
def zero(expr):
 global checks
 assert s.cancel(s.expand(expr))==0
 checks+=1
a,t,K,d=s.symbols('a t K d',real=True)
v=(2*t-1)/3;D=1+a*v;B=1-a*a;M=(1-a)**2*(1-v);W=32*D+M
kappa=8*B/(9*D**2)
# Independently recover the residual by clearing the actual squared inequality.
cleared=s.cancel((kappa*kappa-4*M/W*(4-2*kappa)**2)*81*D**4*W/(64*(1-a)**2))
P=s.Poly(s.expand(cleared),a,t)
zero(P.as_expr()-((1+a)**2*W-(1-v)*(9*D**2-4*B)**2))
assert P.degree(a)==4 and P.degree(t)==5;checks+=1
# Derive tensor-product Bernstein coefficients directly from power coefficients.
# This tests positivity independently of the author's five q-polynomial rewrites.
bs=[]
for i in range(5):
 row=[]
 for j in range(6):
  b=sum(c*s.Rational(comb(i,h),comb(4,h))*s.Rational(comb(j,k),comb(5,k))
        for (h,k),c in P.terms() if h<=i and k<=j)
  assert b>=0;checks+=1;row.append(b)
 bs.append(row)
bern=sum(bs[i][j]*comb(4,i)*a**i*(1-a)**(4-i)*comb(5,j)*t**j*(1-t)**(5-j)
         for i in range(5) for j in range(6))
zero(bern-P.as_expr())
zero((4-3*K)**2-(1-K)*(4-K)**2-K**3)
zero((1-(4-3*K)/(4-K))/(1+(4-3*K)/(4-K))-K/(4-2*K))
zero((1-d)**2*(1+2*d)-(1-2*d)*(1+d)**2-4*d**3)
# Interior monotonicity: differentiate in k before imposing T^2=D^2-B k^2.
k,k0,DD,BB=s.symbols('k k0 DD BB',positive=True)
b=BB*(k/k0-1)/2;T=s.sqrt(DD**2-BB*k*k)
formula=BB/(DD+b)**2*((DD-T)/(2*k0)-k*(DD+b)/T)
assert s.simplify(s.diff((T+b)/(DD+b),k)-formula)==0;checks+=1
# Exact boundary distance and radicand endpoint certificates.
y=s.symbols('y',real=True)
zero((1-a/3)**2-8*(1-a*a)/9-(a-s.Rational(1,3))**2)
# At rho use quotient in Q(sqrt(2)), and derive sharpness without author formula.
r=s.symbols('r',positive=True)
phi=r*(a+r)/(1+a*r)
phipr=s.diff(phi,r)
Fprime=lambda x:(1-x)/(1+x)**3
ratio=Fprime(phi)*phipr/Fprime(r)
assert s.factor(s.diff(ratio,a).subs(a,1)-(r*r-6*r+1)/(1+r)**2)==0;checks+=1
rho=3-2*s.sqrt(2)
assert s.simplify(rho*rho-6*rho+1)==0;checks+=1
assert s.simplify(rho**2/(1-rho**2)**2-s.Rational(1,32))==0;checks+=1
print(json.dumps({'status':'PASS','exact_checks':checks,'frozen_manifest_entries_verified':len(m['files']),
 'independent_certificate':'Nonnegative degree-(4,5) tensor Bernstein coefficient matrix derived from the cleared squared inequality',
 'bernstein_rows':[[str(c) for c in row] for row in bs],
 'scope':'Finite symbolic identities and exact coefficients certify the stated polynomial positivity; analytic hypotheses audited in the report.'},indent=2))
