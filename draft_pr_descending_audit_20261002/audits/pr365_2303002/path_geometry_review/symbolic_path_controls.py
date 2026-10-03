#!/usr/bin/env python3
"""Independent symbolic identities and constructive continuum controls."""
import json
import sympy as s

n = s.symbols('n', integer=True, positive=True)
q = s.symbols('q', real=True)
r = s.symbols('r', positive=True)
a = s.symbols('a', real=True)
x, y, z, t = s.symbols('x y z t', real=True)
lower = (1-q)*(1+q)**(1-n)
upper = (1+q)*(1-q)**(1-n)
identities = {}
identities['lower_derivative'] = s.simplify(s.diff(lower,q) - ((n-2)*q-n)*(1+q)**(-n))
identities['upper_derivative'] = s.simplify(s.diff(upper,q) - (n+(n-2)*q)*(1-q)**(-n))
identities['lower_at_zero'] = lower.subs(q,0)-1
identities['upper_at_zero'] = upper.subs(q,0)-1
radial = s.diff(r**a,r,2) + (n-1)/r*s.diff(r**a,r)
identities['radial_laplacian'] = s.simplify(radial-a*(a+n-2)*r**(a-2))
identities['newtonian_harmonic_away_origin'] = s.simplify(radial.subs(a,2-n))
identities['shell_derivative_jump'] = s.diff(-r**(2-n),r).subs(r,1)-(n-2)
u = x*x-y*y
identities['harmonic_polynomial'] = sum(s.diff(u,v,2) for v in [x,y,z])

# Constructive all-tail path gamma(t)=(t,0,0), t>=1.
identities['good_path_value'] = u.subs({x:t,y:0,z:0})-t*t
# Bad high vertices have alternating signs. For j>=1, choose p_j=(-1)^j*j;
# p_(j+1) has opposite sign, and the segment has zero at lambda=j/(2*j+1).
j = s.symbols('j', integer=True, positive=True)
lam = s.symbols('lam', real=True)
segment_x = (-1)**j*j + lam*((-1)**(j+1)*(j+1)-(-1)**j*j)
zero_lam = j/(2*j+1)
identities['bad_segment_hits_origin'] = s.simplify(segment_x.subs(lam,zero_lam))
identities['bad_vertex_high_value'] = s.simplify(u.subs({x:(-1)**j*j,y:0,z:0})-j*j)
# The parameter j+zero_lam -> infinity, so the all-tail value and properness fail.
identities['bad_crossing_parameter_unbounded'] = s.limit(j+zero_lam,j,s.oo)-s.oo
# Infinity-infinity is nan; encode this limit explicitly below instead.
del identities['bad_crossing_parameter_unbounded']
assert all(v == 0 for v in identities.values())
assert s.limit(j+zero_lam,j,s.oo) == s.oo
assert s.limit(zero_lam,j,s.oo) == s.Rational(1,2)

# Negative mutation: wrong Newtonian exponent cannot be harmonic.
wrong_radial = s.simplify(radial.subs(a,2+n))
assert s.simplify(wrong_radial - 2*n*(n+2)*r**n) == 0
assert wrong_radial.subs({n:3,r:1}) != 0
# Negative geometry claim: endpoint heights imply segment interior height.
assert s.simplify((segment_x**2).subs(lam,zero_lam)) == 0
assert s.simplify(j*j).is_positive

out = {'status':'PASS', 'identities':{k:str(v) for k,v in identities.items()},
       'continuum_sign_argument':'For integers n>=3 and 0<=q<1: (n-2)q-n<-2 and n+(n-2)q>=n>0. Thus the exact lower derivative is negative and upper positive; both start at 1, proving all-parameter bounds rather than sampled inequalities.',
       'radial_distribution_argument':'The example is constant -1 inside r=1 and -r^(2-n) outside; normal derivative jump n-2>0 gives Delta u=(n-2) dS on the unit sphere, with no origin mass.',
       'good_path':'u=x^2-y^2 in R^3; gamma(t)=(t,0,0), t>=1; u=t^2 and norm=t. Entire tails and spatial local finiteness follow exactly.',
       'bad_vertex_path':'vertices p_j=((-1)^j j,0,0) have norm j and value j^2, but every joining segment hits the origin at lambda=j/(2j+1), with u=0. Crossing times tend to infinity: no properness and no u-tail limit.',
       'negative_controls':'wrong radial exponent 2+n has Delta coefficient 2n(n+2)>0; endpoint-only inference is explicitly falsified by the harmonic polynomial construction.',
       'limits':'Symbolic identities and explicit examples test mechanisms; the general continuum theorem is supplied by the separately sealed analytic proof, not a finite pass count.'}
print(json.dumps(out,indent=2,sort_keys=True))
