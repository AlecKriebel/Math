#!/usr/bin/env python3
"""Additional independent exact controls. Analytic claims require REPORT.md."""
import json
from fractions import Fraction
import sympy as S

x,z,a,b,r,u,w,p,q=S.symbols('x z a b r u w p q')
checks={}

def zero(expr):
    assert S.cancel(S.expand(expr)) == 0

def moment(poly):
    terms=S.Poly(poly,x).terms()
    return S.expand(sum(c*S.factorial(k)/(4**(k//2)*S.factorial(k//2))
                        for (k,),c in terms if k%2==0))

# Derive H directly from Rodrigues, independently of the author's recurrence.
H=[]
for k in range(13):
    value=S.expand((-1)**k*S.diff(S.exp(-x*x),x,k)/S.exp(-x*x))
    zero(value-S.hermite(k,x))
    H.append(value)
checks['rodrigues_normalization']=13

count=0
for n in range(3,12):
    for m in range(n+1,13):
        P=1+2*x+a*H[n]+b*H[m]
        for power,want in [(0,1),(1,1),(2,S.Rational(1,2))]:
            zero(moment(x**power*P)-want)
            count+=1
        zero(moment((x-1)**2*P)+S.Rational(1,2))
        count+=1
checks['both_high_terms_gaussian_moments']=count

# Derive the cubic family relation directly from its power coefficients.
A0,A1,A2,A3=S.symbols('A0 A1 A2 A3')
coeff=[1-2*a,2-12*b,4*a,8*b]
zero(coeff[0]+coeff[2]/2-coeff[1]/2-3*coeff[3]/4)
rr=S.symbols('r1 r2 r3')
rootpoly=S.Poly(S.prod(z-v for v in rr),z)
relation=rootpoly.nth(0)+rootpoly.nth(2)/2-rootpoly.nth(1)/2-3*rootpoly.nth(3)/4
ww=S.symbols('w1 w2 w3')
zero(relation.subs(dict(zip(rr,[(v-1)/2 for v in ww])))+(S.prod(ww)+sum(ww)+2)/8)
checks['cubic_relation_from_coefficients']=2

# Check the mixed-half-plane numerator, including the sharp sign threshold.
X,Y,V,T=S.symbols('X Y V T',real=True)
A=X+S.I*Y;B=V+S.I*T
numerator=S.expand(S.im(-(A+B+2)*S.conjugate(A*B+1)))
zero(numerator-(T*(X+1)**2+Y*(V+1)**2+(Y+T)*(Y*T-2)))
zero(numerator.subs({X:-1,V:-1,Y:S.sqrt(2),T:S.sqrt(2)}))
checks['mixed_halfplane_numerator_and_boundary']=2

f=w**3+3*w+2
zero(f+(p-w)*S.diff(f,w)/3-(p*w*w+2*w+p+2))
g=p*w*w+2*w+p+2
zero(g+(q-w)*S.diff(g,w)/2-(p*q*w+p+q+w+2))
checks['successive_polar_derivatives']=2

# Independent factorization and denominator nonvanishing certificates.
phi=4*u**3+3*u-1
assert S.rem(S.expand((w+2*u)*(w*w-2*u*w+3+4*u*u)-f),phi,u)==0
Qr=4*r**3+6*r*r+6*r+3
D=S.Rational(3,4)+S.Rational(3,2)*r*r
assert S.resultant(Qr,4*D,r)!=0
K=1/D
P=1+2*z-3*r*K*S.hermite(2,z)/4+K*S.hermite(3,z)/8
numer,denom=S.fraction(S.factor(P-K*(z-r)**3))
assert S.rem(numer,Qr,r)==0
zero((2*r+1)**3+3*(2*r+1)+2-2*Qr)
checks['diagonal_factorization_and_triple_root']=4

# Quadratic degeneration, coefficient normalization, and exact extremizer.
quad=S.Poly((1+2*z+a*S.hermite(2,z)).subs(z,(w-1)/2),w)
zero(quad.nth(0)+quad.nth(2))
zero(1+2*z+(1+S.I)*S.hermite(2,z)/4-(1+S.I)*(z+S.Rational(1,2)-S.I/2)**2)
checks['quadratic_boundary']=2

# Rational interval arithmetic with an independently tighter bracket.
lo=Fraction(298035818991,10**12);hi=Fraction(298035818992,10**12)
F=lambda value:4*value**3+3*value-1
assert 0<lo<hi<Fraction(1,3)
assert F(lo)<0<F(hi)
assert Fraction(903669747,10**9)**2<Fraction(3,4)*(1+lo*lo)
assert Fraction(3,4)*(1+hi*hi)<Fraction(903669748,10**9)**2
assert 4*Fraction(3,4)*(1+lo*lo)>2
checks['rational_constant_controls']=5

print(json.dumps({'all_passed':True,'total_assertions':sum(checks.values()),'checks':checks,
                  'scope':'Finite independent controls; no degree-uniform conclusion'},indent=2,sort_keys=True))
