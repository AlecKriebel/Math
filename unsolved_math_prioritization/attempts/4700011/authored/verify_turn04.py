#!/usr/bin/env python3
"""Exact checks for Turn 4's all-order arithmetic and cubic obstructions."""
from pathlib import Path
import json, math
import sympy as sp
z,c,t,p1,p2,s,v=sp.symbols('z c t p1 p2 s v')
checks=[]

# The universal self-cubic coefficient, before substitution t=z^k.
U=-t/p2;V=-(t+1/t)/p1
source=U*(t*t+1/t)+V*(1+t)
G=p1*t*(t**3+1)+p2*(t*t+1)*(t+1)
assert sp.cancel(-source*p1*p2*t-G)==0
checks.append({'name':'cubic_coefficient_derivation','passed':True})

# The weighted-variance expression follows exactly from the cubic identity.
second_moment=v+1-(2-s)/(4*v)
variance=second_moment-2*(v+1)/s
claimed=(2-s)*(s+4*v*(v+1))/(-4*s*v)
assert sp.cancel(variance-claimed)==0
checks.append({'name':'weighted_variance_identity','passed':True})

# The two-fixed-point normalized unit identity is exact.
c0=sp.symbols('c0',nonzero=True)
assert sp.cancel(1+(1-c0)/c0-1/c0)==0
checks.append({'name':'negative_fixed_point_unit_identity','passed':True})

# GCD of the complete cubic-remainder equations, not just one coefficient.
gcd_results=[]
for k in [2,3]:
    P=z**k+1-c*sum(z**j for j in range(1,k))
    total=(k-1)*c
    G=(2-total)*z**k*(z**(3*k)+1)+P.subs(z,z*z)*(z**(2*k)+1)*(z**k+1)
    remainder=sp.Poly(sp.rem(G,P,z),z)
    common=sp.Poly(0,c)
    for coeff in remainder.all_coeffs():common=sp.gcd(common,sp.Poly(coeff,c))
    common=common.monic().as_expr()
    expected=(c*(c-2)*(c-1)*(c*c+c-1) if k==2 else
              c*(c-1)*(c*c+2*c-1)*(c**3+4*c*c+2*c-2))
    assert sp.expand(common-expected)==0
    gcd_results.append({'order':k,'gcd':str(sp.factor(common))})
checks.append({'name':'complete_low_order_cubic_remainders','results':gcd_results,'passed':True})

# All four decreasing classical families satisfy the cubic obstruction,
# including nontrivial index dilations.
classical=[]
for ell in range(1,5):
    for name,k,coeff in [
        ('reciprocal',ell,{}),
        ('six_period',2*ell,{ell:sp.Integer(1)}),
        ('five_period',2*ell,{ell:(sp.sqrt(5)-1)/2}),
        ('eight_period',3*ell,{ell:sp.sqrt(2)-1,2*ell:sp.sqrt(2)-1}),
    ]:
        P=z**k+1-sum(a*z**j for j,a in coeff.items());total=sum(coeff.values())
        G=(2-total)*z**k*(z**(3*k)+1)+P.subs(z,z*z)*(z**(2*k)+1)*(z**k+1)
        rem=sp.rem(G,P,z,extension=True)
        assert sp.expand(rem)==0,(name,ell,rem)
        classical.append({'family':name,'dilation':ell,'passed':True})
checks.append({'name':'classical_cubic_controls','results':classical,'passed':True})

# A genuine insufficient-test control: the extra cubic root in order three.
h=c**3+4*c*c+2*c-2
assert h.subs(c,sp.Rational(12,25))<0<h.subs(c,sp.Rational(49,100))
assert h.subs(c,-4)<0<h.subs(c,-3)
assert sp.Poly(h,c).is_irreducible
assert sp.gcd(h,c*c+2*c-1)==1
checks.append({'name':'spurious_cubic_candidate_control','polynomial':str(h),
               'positive_root_interval':['12/25','49/100'],
               'bad_conjugate_interval':[-4,-3],'passed':True})

# Audit the support-index arithmetic used in the uniform sparse theorem.
for k in range(3,101):
    for j in range(1,(k+1)//2):
        if 2*j==k:continue
        g=math.gcd(k,j);K=k//g;r=j//g
        assert math.gcd(K,r)==1
        if K%2==0:assert r%2==1 and (K-r)%2==1
        if K%3==0 and r in [K//3,2*K//3]:assert K==3
checks.append({'name':'sparse_support_gcd_consistency','orders_checked':[3,100],'passed':True,
               'scope':'Finite consistency check; the document supplies the general proof.'})

result={'all_passed':True,'sympy_version':sp.__version__,'checks':checks,
        'scope':'Exact consistency checks for general proofs; no bounded numerical search is used to infer an all-order theorem.'}
Path(__file__).with_name('turn04_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
