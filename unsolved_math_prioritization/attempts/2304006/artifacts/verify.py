#!/usr/bin/env python3
"""Exact finite controls for the accompanying proofs, not a global zero search.
Requires Python 3 and SymPy; writes deterministic JSON to stdout.
"""
import json
import sympy as s
from fractions import Fraction

checks={}
z,x,a,b,r,w,t,v,xi,eta=s.symbols('z x a b r w t v xi eta')

def assert_zero(expr):
    assert s.cancel(s.expand(expr)) == 0, expr

def gaussian(poly):
    p=s.Poly(s.expand(poly),x)
    total=0
    for (k,),c in p.terms():
        if k%2==0:
            total += c*s.factorial(k)/(4**(k//2)*s.factorial(k//2))
    return s.expand(total)

# Exact Rodrigues/recurrence and low Gaussian moment identities.
H=[s.Integer(1),2*x]
for k in range(1,24): H.append(s.expand(2*x*H[k]-2*k*H[k-1]))
for k in range(25): assert_zero(H[k]-s.hermite(k,x))
checks['hermite_recurrence']=25
n_orth=0
for k in range(1,25):
    for j in range(k):
        assert_zero(gaussian(H[k]*x**j));n_orth+=1
checks['gaussian_orthogonality']=n_orth
for k in range(3,25):
    assert_zero(gaussian((x-1)**2*(1+2*x+a*H[k]))+s.Rational(1,2))
checks['negative_variance_identity']=22

# Taylor coefficients used in the exact Rouché criterion.
for k in range(25):
    expansion=sum(s.binomial(k,j)*(2*z)**j*s.hermite(k-j,-s.Rational(1,2)) for j in range(k+1))
    assert_zero(s.hermite(k,z-s.Rational(1,2))-expansion)
checks['rouche_taylor_identity']=25

# Spectral annihilation for a finite set of indices.
def Lop(poly):return s.diff(poly,z,2)-2*z*s.diff(poly,z)
nop=0
for n in range(2,13):
    for m in range(n+1,14):
        p=1+2*z+a*s.hermite(n,z)+b*s.hermite(m,z)
        q=Lop(p)+2*m*p
        assert_zero(Lop(q)+2*n*q-4*n*m-8*(n-1)*(m-1)*z)
        nop+=1
checks['operator_elimination']=nop

# Shifted Vieta relation for the cubic.
r1,r2,r3=s.symbols('r1 r2 r3')
w1,w2,w3=s.symbols('w1 w2 w3')
p=s.Poly((z-r1)*(z-r2)*(z-r3),z)
relation=p.nth(0)+p.nth(2)/2-p.nth(1)/2-3*p.nth(3)/4
shifted=s.expand(relation.subs({r1:(w1-1)/2,r2:(w2-1)/2,r3:(w3-1)/2}))
assert_zero(shifted+(w1*w2*w3+w1+w2+w3+2)/8)
checks['cubic_vieta']=1

# Triple zero with exactly the required Hermite coefficients, modulo q(r)=0.
q=4*r**3+6*r**2+6*r+3
D=s.Rational(3,4)+s.Rational(3,2)*r**2
K=1/D;aa=-3*r*K/4;bb=K/8
remainder=s.together(1+2*z+aa*s.hermite(2,z)+bb*s.hermite(3,z)-K*(z-r)**3)
assert s.rem(s.fraction(remainder)[0],q,r)==0
assert s.degree(s.gcd(q,s.fraction(D)[0]),r)==0
checks['attaining_triple_zero']=2

# Quadratic bound after w=2z+1: root product -1.
pp=s.Poly((1+2*z+a*s.hermite(2,z)).subs(z,(w-1)/2),w)
assert_zero(pp.nth(0)+pp.nth(2))
checks['quadratic_product']=1

# The half-plane sign calculation, with real x,y,u,v.
X,Y,U,V=s.symbols('X Y U V',real=True)
N=X+U+2+s.I*(Y+V)
Den=(X+s.I*Y)*(U+s.I*V)+1
num=s.expand(s.im(-N*s.conjugate(Den)))
positive=V*(X+1)**2+Y*(U+1)**2+(Y+V)*(Y*V-2)
assert_zero(num-positive)
checks['cubic_halfplane_sign']=1

# Explicit polarization by successive polar derivatives.
f=w**3+3*w+2
g=s.expand(f+(xi-w)*s.diff(f,w)/3)
h=s.expand(g+(eta-w)*s.diff(g,w)/2)
assert_zero(g-(xi*w*w+2*w+xi+2))
assert_zero(h-(xi*eta*w+xi+eta+w+2))
checks['polarization_steps']=2

# Exact rational brackets for the unique positive u and C3.
lo=Fraction(298035818991,10**12)
hi=Fraction(298035818992,10**12)
F=lambda t:4*t**3+3*t-1
assert F(lo)<0<F(hi)
clo=Fraction(903669747,10**9);chi=Fraction(903669748,10**9)
# Enclosures are deliberately wider than the root-interval-induced one.
assert clo*clo < Fraction(3,4)*(1+lo*lo)
assert Fraction(3,4)*(1+hi*hi) < chi*chi
assert Fraction(3,4)*(1+lo*lo)>Fraction(1,2)
checks['exact_constant_brackets']=4

print(json.dumps({'all_passed':True,'kind':'exact finite algebraic controls; analytic proofs remain in text',
'checks':checks,'total_assertions':sum(checks.values()),
'cubic_constant_interval':['0.903669747','0.903669748'],
'full_problem_resolved':False},indent=2,sort_keys=True))
