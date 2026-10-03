#!/usr/bin/env python3
"""Original symbolic controls: no author imports, no finite scans as proofs."""
import json
import sympy as S

r,a,b,t,u,q,p,m,s,d,z,x=S.symbols('r a b t u q p m s d z x', real=True)
checks={}
def zero(name,expr):
    result=S.factor(expr)
    assert result==0,(name,result)
    checks[name]=str(result)

# Universal second-order obstruction when two small masses are repeated.
zero('hessian_two_small',2*(12*t*t-4*(t*t+t*u+u*u))-8*(t-u)*(2*t+u))
# The derivative uses both equality constraints, rather than a stationary guess.
zero('profile_derivative',-6*((r*a*a+b*b)-(a*a+a*b+b*b))+6*((r-1)*a*a-a*b))
# Rational field representation of the all-part moment minimum.
D=S.symbols('D',real=True)
A=(1+6*r*D+r*(r*r-r+1)*D*D)/(r+1)**3
B=4*r*(r-1)*D/(r+1)**3
large=(1+z)/(r+1); small=(1-r*z)/(r+1)
zero('minimum_radical',S.expand(r*large**4+small**4-(A-B*z)).subs(D,z*z))
# Local radius: exactly 171 nonlinear terms, no independence of overlapping pairs.
terms=3*sum(S.binomial(6,k) for k in range(2,7))
assert terms==171
zero('local_radius',-3+terms/S.Integer(114)+S.Rational(3,2))
# Fixed-space exact tying surgery: its nonlinear remainder is of first order in L1.
U=a-s; E=b*s/U; Z=s-E; V=b+E
zero('tie_edge',U*V-a*b)
zero('tie_mass',U+V+Z-a-b)
zero('tie_C4',6*U**2*V**2-6*a*a*b*b)
zero('tie_L1',2*U*E+2*b*(E+Z)-4*b*s)
zero('tie_first_variation',6*((-q+a*a)*2*U*E-((a+b)**2-q)*2*b*(E+Z))+12*b*b*s*(2*a+b))
# Localizing polynomial certificates are valid for every probability law on [0,1].
poly=S.expand(x*(x-s/m)**2)
zero('lower_moment_localizer',poly-(x**3-2*s/m*x*x+s*s/m**2*x))
poly=S.expand((1-x)*(x-d)**2)
zero('upper_moment_localizer',poly-(-x**3+(1+2*d)*x*x-(2*d+d*d)*x+d*d))
zero('upper_bound_after_expectation',(s-t-2*d*(m-s)+d*d*(1-m)).subs(d,(m-s)/(1-m))-(s-t-(m-s)**2/(1-m)))
# Exact rank-one integral expansion and optimization derivative.
zero('rankone_factorization',s**4-2*s*s*t*t+t**4-(s*s-t*t)**2)
zero('rankone_stationary',S.diff(s*s-s**4/m**2,s)-2*s*(1-2*s*s/m**2))
zero('rankone_global_derivative',S.diff(3*p**4*(1-p)**2,p)-6*p**3*(1-p)*(2-3*p))
zero('high_gap_factorization',3*(1-p)**2*(1-(1-p)/p**2-p**4)-3*(1-p)**3/p**2*(p*p*(1+p+p*p+p**3)-1))
assert (p*p*(1+p+p*p+p**3)-1).subs(p,S.Rational(3,4))==S.Rational(551,1024)
assert S.Rational(3,2)-3*S.Rational(3,4)**4==S.Rational(141,256)
assert 3*S.Rational(2,3)**4*S.Rational(1,3)**2==S.Rational(16,243)
print(json.dumps({'status':'PASS','identities':checks,'remainder_terms':int(terms),'scope':'symbolic identities supplement universal sign and equality proofs in mathematical_verdict.md'},sort_keys=True))
