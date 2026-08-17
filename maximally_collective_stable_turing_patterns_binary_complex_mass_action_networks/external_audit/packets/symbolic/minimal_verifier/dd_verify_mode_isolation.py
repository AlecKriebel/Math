#!/usr/bin/env python3
import json,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
cert=json.loads((HERE/'improved_modulus_certificate.json').read_text())
assert cert['homogeneous']['term_count']==35
assert cert['improved_mode']['term_count']==77
for sec in cert.values():
 for term in sec['terms']: assert sp.Rational(term['coefficient'])>0
# Reconstruct the homogeneous polynomial as well.
xh,yh,zh=sp.symbols('xh yh zh',real=True);lh=xh+sp.I*yh
Ph=lh**4+12*lh**3+42*lh**2+47*lh+16
Rh=5*lh**2+33*lh+16
def yh2z(expr):
 out=0
 for (k,),c in sp.Poly(sp.expand(expr),yh).terms(): assert k%2==0;out+=c*zh**(k//2)
 return sp.expand(out)
Eh=sp.Poly(yh2z((1+lh)*(1+sp.conjugate(lh))*Ph*sp.conjugate(Ph)-Rh*sp.conjugate(Rh)),xh,zh)
hterms={(tuple(t['powers']),sp.Rational(t['coefficient'])) for t in cert['homogeneous']['terms']}
assert hterms=={(mon,sp.factor(c)) for mon,c in Eh.terms()}

# Reconstruct the improved polynomial rather than trusting the JSON.
x,y,z,s=sp.symbols('x y z s',real=True);lam=x+sp.I*y;t=1+s
q=sp.Rational(91,90);d1=sp.Rational(23,63);dm=sp.Rational(1,7);dz=sp.Rational(16,45)
g1=lam+2+t*d1;gm=lam+5+t*dm;gz=lam+4+t*dz
F=sp.expand(g1*gm*gz-4*g1-4*gm+gz);G=sp.expand(gz*(4*g1+gm)-36)
def y2z(expr):
 out=0
 for (k,),c in sp.Poly(sp.expand(expr),y).terms(): assert k%2==0;out+=c*z**(k//2)
 return sp.expand(out)
E=sp.Poly(sp.expand((q*q+z)*y2z(F*sp.conjugate(F))-y2z(G*sp.conjugate(G))),x,z,s)
terms={(tuple(t['powers']),sp.Rational(t['coefficient'])) for t in cert['improved_mode']['terms']}
assert terms=={(mon,sp.factor(c)) for mon,c in E.terms()}

# Exact finite reconstruction of the sparse determinant formula.
from common import Avec,selected
for mm in [3,4,5]:
    lamv,tv=sp.symbols(f'lam{mm} t{mm}')
    A=Avec(mm);_,ds,_=selected(mm)
    g1=lamv+2+tv*ds[0];gm=lamv+5+tv*ds[mm-1];gz=lamv+4+tv*ds[mm]
    Q=sp.prod(lamv+1+tv*ds[i-1] for i in range(2,mm))
    F=g1*gm*gz-4*g1-4*gm+gz
    G=gz*(4*g1+gm)-36
    assert sp.factor((lamv*sp.eye(mm+1)-A+tv*sp.diag(*ds)).det()-(Q*F-G))==0

print('MODE_ISOLATION_PASS')
