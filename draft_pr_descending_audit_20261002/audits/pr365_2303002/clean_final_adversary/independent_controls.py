#!/usr/bin/env python3
"""Independent symbolic and negative controls; no finite existence claim."""
import json
import sympy as s

R,r,t=s.symbols('R r t',positive=True)
n=s.symbols('n',integer=True,positive=True)
x,y,z=s.symbols('x y z',real=True)
out={}

# In n=3, normalized angular surface probability reduces to dt/2.
kernel=R*(R**2-r**2)/(R**2+r**2-2*R*r*t)**s.Rational(3,2)
anti=(R**2-r**2)/(2*r*s.sqrt(R**2+r**2-2*R*r*t))
assert s.simplify(s.diff(anti,t)-kernel/2)==0
# Here 0<r<R, so square roots at +/-1 are R-r and R+r.
integral=s.factor((R**2-r**2)/(2*r)*(1/(R-r)-1/(R+r)))
assert integral==1
assert s.limit(R*(R**2-r**2)/(R**2)**s.Rational(3,2),r,0)==1
out['poisson_n3_exact_normalization']=str(integral)

q=s.symbols('q',nonnegative=True)
upper=(1-q**2)/(1-q)**n
lower=(1-q**2)/(1+q)**n
assert s.simplify(upper-(1+q)/(1-q)**(n-1))==0
assert s.simplify(lower-(1-q)/(1+q)**(n-1))==0
assert s.limit(upper,q,0)==s.limit(lower,q,0)==1
out['symbolic_bounds_limit']='both exactly 1 for each fixed dimension'

alpha=2-n
assert s.expand(alpha*(alpha+n-2))==0
assert s.simplify(s.diff(-r**(2-n),r).subs(r,1))==n-2
out['radial_laplacian_coefficient']='0'
out['source_example_boundary_derivative_jump']=str(n-2)
out['source_example_origin']='-1 because the entire unit ball is the constant branch'

# Harmonic high vertices alone do not imply an all-tail path.
u=x*x-y*y
assert s.diff(u,x,2)+s.diff(u,y,2)+s.diff(u,z,2)==0
k=s.symbols('k',positive=True)
assert u.subs({x:k,y:0})==u.subs({x:-k,y:0})==k*k
assert u.subs({x:0,y:0})==0
out['negative_control_vertices']='(+k,0,0) and (-k,0,0) both have u=k^2; their straight chord has u=0 at midpoint for every k'

# A bounded positive disjoint bump fails the SH condition in its interior.
bump=1-x*x-y*y-z*z
lap=s.diff(bump,x,2)+s.diff(bump,y,2)+s.diff(bump,z,2)
assert lap==-6
out['negative_control_disjoint_bumps']='max(0,1-|x|^2), translated to disjoint balls, is continuous/nonnegative/bounded but has interior Laplacian -6'

# Entire-domain assumption is indispensable in one-sided Liouville.
h=1+x
assert s.diff(h,x,2)+s.diff(h,y,2)+s.diff(h,z,2)==0
assert s.diff(h,x)==1
out['negative_control_domain']='1+x is positive nonconstant harmonic on x>0; it is not nonnegative on all R^3'

# Disconnected domains can have arbitrarily many bounded positive components.
out['negative_control_infinite_bounds']='Union of disjoint unit balls B((3j,0,0),1) with function j on ball j is continuous harmonic on that proper disconnected domain, unbounded globally with every component bounded in value. Entire-space subharmonic pasting is the missing hypothesis.'
out['topology_proof_dependency']='Reachability by finite polygonal chains in a connected open Euclidean set is relatively open and relatively closed. This logical argument, and the analytic component obstruction, cannot be replaced by these finite controls.'
out['theorem_certified_by_finite_controls']=False
print(json.dumps(out,indent=2,sort_keys=True))
