#!/usr/bin/python3
"""Fresh geometry diagnostics, distinct from historical repeated margins."""
import json,pathlib,sympy as s
checks={}
def ck(n,v):
    assert bool(v),n
    checks[n]='PASS'
x,y,b=s.symbols('x y b',real=True)
a,u,t=s.symbols('a u t',positive=True)
z=x+s.I*y
disk=1-x*x-y*y
den=(1-b*x)**2+b*b*y*y
num=(x-b)**2+y*y
# Assumptions in the written proof: |b|<1 and |z|<1, hence den>0.
ck('mobius_norm_defect_factorization',s.expand(den-num-(1-b*b)*disk)==0)
q=s.symbols('q')
M=(q-b)/(1-b*q)
ck('mobius_complex_derivative',s.cancel(s.diff(M,q)-(1-b*b)/(1-b*q)**2)==0)
ck('mobius_pullback_density',s.cancel(((1-b*b)/den)/(1-num/den)-1/disk)==0)
lam=1/disk
curvature=-(s.diff(s.log(lam),x,2)+s.diff(s.log(lam),y,2))/lam**2
ck('disk_curvature_minus_four',s.cancel(curvature+4)==0)
# Half-plane coordinates for exp(-a*w): intrinsic metric curvature is -4.
L=a/(2*s.sinh(a*u))
ck('exponential_pullback_curvature',s.simplify(-s.diff(s.log(L),u,2)/L**2+4)==0)
ck('halfplane_hyperbolic_ratio',s.cancel(L/(1/(2*u))-a*u/s.sinh(a*u))==0)
ck('positive_parameter_unrestricted_limit',s.limit(a*u/s.sinh(a*u),u,0,dir='+')==1)
ck('positive_parameter_second_order_deficit',s.simplify(s.limit((1-a*u/s.sinh(a*u))/u**2,u,0)-a*a/6)==0)
f=M**2
F=s.cancel(f.subs(q,z));Fbar=s.conjugate(F)
modF=s.cancel(F*Fbar)
Q=(1-b*b)/den*(1+num/den)
ck('squared_mobius_real_analytic_division',s.cancel(1-modF-disk*Q)==0)
ck('squared_mobius_boundary_Q',s.cancel(Q.subs({x:1,y:0})-2*(1+b)/(1-b))==0)
ck('squared_mobius_boundary_derivative',s.cancel(s.diff(f,q).subs(q,1)-2*(1+b)/(1-b))==0)
ck('squared_mobius_interior_critical_point',s.diff(f,q).subs(q,b)==0)
ck('squared_mobius_value_at_one',s.cancel(f.subs(q,1)-1)==0)
# Actual tangential disk paths demonstrate why a generic O(|z-1|²) Taylor
# remainder cannot be divided by the boundary defining function.
for m in [4,6,8]:
    rho=1-t**m
    ratio=(1+rho*rho-2*rho*s.cos(t))/(1-rho*rho)
    ck('tangential_scaled_remainder_m%d'%m,s.limit(ratio*t**(m-2),t,0,dir='+')==s.Rational(1,2))
    ck('tangential_unscaled_remainder_m%d'%m,s.limit(ratio,t,0,dir='+')==s.oo)
    ck('tangential_path_disk_defect_m%d'%m,s.expand(1-rho*rho-(2*t**m-t**(2*m)))==0)
# Negative control for the forbidden global distance inference. The image
# endpoints under z² coincide while the original endpoints are distinct.
r=s.symbols('r',positive=True)
ck('square_fold_endpoints',(r**2-(-r)**2)==0)
ck('square_distinct_original_endpoints',s.simplify(r-(-r))==2*r)
ck('square_nonzero_distortion_away_zero',s.simplify(2*r/(1+r*r))!=0)
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact diagnostics for metric normalization/curvature, boundary factorization and tangential-path failure of naive Taylor division. Written universal argument imports the authenticated arc reflection theorem; these finite controls do not certify that theorem.'}
pathlib.Path(__file__).with_name('hyperbolic_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
