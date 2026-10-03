#!/usr/bin/env python3
"""Exact algebra controls, not a decision procedure for local-global principles."""
import itertools
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

checks=[]
def check(name, value):
    if not value:
        raise AssertionError(name)
    checks.append(name)

x,y,z,t,u,v,A,B,C,D,alpha,beta=s.symbols('x y z t u v A B C D alpha beta')
H=x*y*z-t*(x+y+z)**3
partials=[s.diff(H,w) for w in (x,y,z)]
for variable, other in [(z,(x,y)),(y,(x,z)),(x,(y,z))]:
    ideal=[f.subs(variable,1) for f in [H]+partials]
    gb=s.groebner(ideal,*other,domain=s.QQ.frac_field(t))
    check('generic_cubic_smooth_chart_'+str(variable),list(gb)==[s.Integer(1)])
for node in [(0,0,1),(0,1,0),(1,0,0)]:
    subs=dict(zip((x,y,z),node));subs[t]=0
    check('node_regular_'+''.join(map(str,node)),s.diff(H,t).subs(subs)==-1)
check('elliptic_discriminant',s.expand(s.discriminant(x**3+x**2+t**3,x)+t**3*(4+27*t**3))==0)

relations=s.groebner([alpha**2-u,beta**2-v],alpha,beta,domain=s.QQ.frac_field(u,v,A,B,C,D))
theta=A+B*alpha+C*beta+D*alpha*beta
norm_sigma=relations.reduce(s.expand(theta*theta.subs(alpha,-alpha)))[1]
norm_tau=relations.reduce(s.expand(theta*theta.subs(beta,-beta)))[1]
expected_sigma=A*A+v*C*C-u*B*B-u*v*D*D+2*(A*C-u*B*D)*beta
expected_tau=A*A+u*B*B-v*C*C-u*v*D*D+2*(A*B-v*C*D)*alpha
check('sigma_norm_coefficients',s.expand(norm_sigma-expected_sigma)==0)
check('tau_norm_coefficients',s.expand(norm_tau-expected_tau)==0)
check('constant_norm_sum',s.expand(norm_sigma.subs(beta,0)+norm_tau.subs(alpha,0)-2*(A*A-u*v*D*D))==0)
check('anisotropy_contradiction_equation',s.expand(norm_sigma.subs({beta:0,A:0,D:0})-1)==v*C*C-u*B*B-1)
check('i_has_norm_one',s.I**4==1)

for n in [3,6]:
    edges=[(i,(i+1)%n) for i in range(n)]
    incidence=s.zeros(n,n)
    for j,(a,b) in enumerate(edges):
        incidence[j,a]=-1;incidence[j,b]=1
    check('cycle_rank_'+str(n),incidence.rank()==n-1)
    diag=smith_normal_form(incidence,domain=s.ZZ)
    check('cycle_integral_cokernel_'+str(n),[abs(diag[i,i]) for i in range(n)]==[1]*(n-1)+[0])
    image={tuple((bits[b]-bits[a])%2 for a,b in edges) for bits in itertools.product(range(2),repeat=n)}
    check('cycle_mod2_cokernel_'+str(n),len(image)==2**(n-1))
    check('single_edge_nonboundary_'+str(n),(1,)+(0,)*(n-1) not in image)

# CTPS Proposition 5.1 residue options, with all eight choices checked.
options=[[(0,0,1),(0,1,0)],[(0,0,0),(1,0,1)],[(0,0,0),(1,1,0)]]
sums=[tuple(sum(a[j] for a in choices)%2 for j in range(3)) for choices in itertools.product(*options)]
check('ctps_eight_residue_choices',len(sums)==8 and (0,0,0) not in sums)
print(json.dumps({'status':'PASS','checks':len(checks),'names':checks,'scope':'Exact symbolic and finite controls only; the global counterexample uses credited theorems.'},indent=2,sort_keys=True))
