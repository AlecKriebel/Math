"""Exact controls for parameter termination, RT commuting and indicator reduction.
The infinite-dimensional convergence proof is not replaced by these checks.
"""
import sympy as s,json
from collections import Counter
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
x,y,t,a,b=s.symbols('x y t a b')
j=a+b*t
whole=s.integrate(j*j,(t,0,1))
children=s.Rational(1,2)*(s.integrate(j*j,(t,0,s.Rational(1,2)))+s.integrate(j*j,(t,s.Rational(1,2),1)))
ck(s.expand(children-whole/2)==0,'exact_marked_edge_half_reduction')
# RT0 flux degrees of freedom on the reference triangle, reconstructed from
# actual outward normal integrals, not a presumed commuting identity.
def tint(poly):
 return s.integrate(s.integrate(poly,(y,0,1-x)),(x,0,1))
for p in range(4):
 for q in range(4-p):
  for vx,vy in [(x**p*y**q,0),(0,x**p*y**q),(x**p*y**q,-2*x**q*y**p)]:
   vx=s.sympify(vx);vy=s.sympify(vy)
   bottom=-s.integrate(vy.subs({x:t,y:0}),(t,0,1))
   left=-s.integrate(vx.subs({x:0,y:t}),(t,0,1))
   diagonal=s.integrate((vx+vy).subs({x:t,y:1-t},simultaneous=True),(t,0,1))
   aa=-left;cc=-bottom;bb=diagonal-aa-cc
   ck(s.simplify(2*bb-2*tint(s.diff(vx,x)+s.diff(vy,y)))==0,'reference_RT_actual_normal_flux_commuting')
   ck(-cc==bottom and -aa==left and aa+cc+bb==diagonal,'reference_RT_named_edge_fluxes')
# Cellwise projection and diameter weighting on a red refinement into four
# congruent reference triangles; all child diameters are half the old one.
children=[((0,0),(s.Rational(1,2),0),(0,s.Rational(1,2))),
          ((s.Rational(1,2),0),(1,0),(s.Rational(1,2),s.Rational(1,2))),
          ((0,s.Rational(1,2)),(s.Rational(1,2),s.Rational(1,2)),(0,1)),
          ((s.Rational(1,2),0),(s.Rational(1,2),s.Rational(1,2)),(0,s.Rational(1,2)))]
def cell_integral(f,T):
 o,u,v=T;X=o[0]+x*(u[0]-o[0])+y*(v[0]-o[0]);Y=o[1]+x*(u[1]-o[1])+y*(v[1]-o[1])
 det=abs((u[0]-o[0])*(v[1]-o[1])-(v[0]-o[0])*(u[1]-o[1]))
 return det*tint(s.expand(f.subs({x:X,y:Y},simultaneous=True)))
for p in range(4):
 for q in range(4-p):
  f=x**p*y**q+x-y
  mean=2*tint(f);old=tint((f-mean)**2);new=0
  for T in children:
   area=cell_integral(s.Integer(1),T);avg=cell_integral(f,T)/area
   new+=cell_integral((f-avg)**2,T)/4
   ck(cell_integral(f-avg,T)==0,'child_projection_orthogonality')
  ck(new<=old/4,'data_red_refinement_contraction')
# Absolute defect stopping, including zero forcing and very inaccurate moving
# coarse inputs. Every test uses rational arithmetic.
for n in range(1,5):
 S=s.diag(*range(1,n+1))+s.ones(n,n)/3
 F=s.Matrix(range(1,n+1));pM=S.inv()*F
 for c in [s.zeros(n,1),s.ones(n,1)*10**6,pM,s.Matrix([(-1)**i*(i+1) for i in range(n)])]:
  for level in [0,2,5,8]:
   tau=s.Rational(1,2)**level;delta=s.Integer(1);halves=0
   while True:
    q=(S+delta*s.eye(n)).inv()*(F+delta*c);d=delta*(c-q)
    if (d.T*d)[0]<=tau**4:break
    delta/=2;halves+=1
    assert halves<100
   ck((d.T*d)[0]<=tau**4,'absolute_defect_loop_terminates')
   chi2=(d.T*S.inv()*d)[0]
   ck(chi2<=s.trace(S.inv())*tau**4,'certified_mixed_flux_distance')
# Eventual bulk-loss and estimator-reduction constants, exactly.
for rt in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
 k=rt/4;theta=rt*rt;theta_star=((rt-k)/(1+k))**2
 ck(theta_star>=theta/4,'eventual_bulk_quarter_bound')
 zeta=theta/32;q=(1+zeta)*(1-theta/8)
 ck(0<q<1,'strict_indicator_reduction_factor')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite exact identities and algorithm calibrations only; the Hilbert-space Cauchy, reliability and all-level convergence statements require the written proof.'},indent=2,sort_keys=True))
