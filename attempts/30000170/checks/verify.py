"""Exact algebra controls for the complex-quadratic normal obstruction.
The primary projection theorem and the source-scope judgment are not finite tests.
"""
import sympy as S
import json
from collections import Counter
C=Counter()
def ck(v,name):
 assert bool(v),name
 C[name]+=1
def ze(v,name):ck(S.simplify(v)==0,name)
z=S.symbols('z');t=S.symbols('t',positive=True);I=S.I
p=z*z+t*t*z+t*t+I*t**3
ze(p-(z+I*t)*(z+t*t-I*t),'stable_factorization')
lam=-I*t;der=t*t-2*I*t
n=S.Matrix([-t,-t*t/2,-t/2,1])
N=S.Matrix([t**3/2,-t*t,-t,-t*t/2,-t/2,1])
gamma=2/(t*(t*t+4))
monic_dirs=[lam,I*lam,1,I]
full_dirs=[lam*lam,I*lam*lam]+monic_dirs
for idx,b in enumerate(monic_dirs):ze(S.re(-b/der)-gamma*n[idx],'full_monic_real_gradient')
for idx,b in enumerate(full_dirs):ze(S.re(-b/der)-gamma*N[idx],'full_nonmonic_real_gradient')
x,y,u,v=S.symbols('x y u v',real=True)
g=v-x*y/2-x*S.sqrt(u+y*y/4)
pt={x:t*t,y:0,u:t*t,v:t**3}
for idx,w in enumerate([x,y,u,v]):ze(S.diff(g,w).subs(pt)-n[idx],'full_chart_normal')
ze(g.subs(pt),'active_chart_boundary')
shift=S.expand((z-I*y/2)**2+(x+I*y)*(z-I*y/2)+u+I*v)
ze(shift-(z*z+x*z+u+y*y/4+I*(v-x*y/2)),'imaginary_center_shift')
delta=S.Matrix([t*t,0,t*t,(2*S.sqrt(2)-1)*t**3]);D=delta.dot(delta)
c0=2*S.sqrt(2)-S.Rational(5,2);d0=(2*S.sqrt(2)-1)**2
ck(c0>0,'strict_positive_support_coefficient')
ze(n.dot(delta)-c0*t**3,'exact_support_numerator')
ze(D-(2*t**4+d0*t**6),'exact_coefficient_distance_squared')
Delta=S.Matrix([0,0]+list(delta))
ze(N.dot(Delta)-c0*t**3,'nonmonic_support_same')
ratio=S.cancel(n.dot(delta)/D)
ze(ratio-c0/(t*(2+d0*t*t)),'support_ratio_closed_form')
ck(S.limit(ratio,t,0,dir='+')==S.oo,'support_ratio_diverges')
ze(n.dot(n)-(1+5*t*t/4+t**4/4),'bounded_monic_normal')
ze(N.dot(N)-(1+5*t*t/4+5*t**4/4+t**6/4),'bounded_full_normal')
epi=S.Matrix(list(n)+[-t*(t*t+4)/2]);epid=S.Matrix(list(delta)+[0])
ze(epi.dot(epid)-c0*t**3,'epigraph_support_same')
for j in range(6):ze(S.limit(N[j],t,0,dir='+')-(1 if j==5 else 0),'full_horizontal_limit')
for j in range(5):ze(S.limit(epi[j],t,0,dir='+')-(1 if j==3 else 0),'epigraph_horizontal_limit')
for j in range(1,61):
 h=S.Rational(1,2**j)
 ck(ratio.subs(t,h)>=c0/(6*h),'dyadic_uniform_lower_bound')
 ck(ratio.subs(t,h/2)>2*ratio.subs(t,h),'dyadic_divergence_rate')
 ck(n.dot(n).subs(t,h)<4,'bounded_monic_sequence')
 ck(N.dot(N).subs(t,h)<4,'bounded_full_sequence')
 # Both stable points are exact factorizations with active imaginary roots.
 for scale in [1,S.sqrt(2)]:
  tt=scale*h
  ze((z*z+tt*tt*z+tt*tt+I*tt**3)-(z+I*tt)*(z+tt*tt-I*tt),'dyadic_stable_pair_factorization')
# Fixed weighted inner products: explicit positive-definite matrices, covectors transformed.
for dim,nn,dd in [(4,n,delta),(6,N,Delta)]:
 for seed in [1,2,4]:
  L=S.Matrix(dim,dim,lambda i,j:S.Rational(((i+2)*(j+1)+seed)%7-3,5))
  G=S.eye(dim)+L.T*L
  ck(all(G[:j,:j].det()>0 for j in range(1,dim+1)),'weighted_metric_positive_definite')
  nv=G.inv()*nn
  ze((nv.T*G*dd)[0]-nn.dot(dd),'weighted_normal_support_identity')
  M=S.trace(G)
  for j in [1,3,7,11,17]:
   h=S.Rational(1,2**j);DG=(dd.T*G*dd)[0].subs(t,h)
   ck(DG<=M*dd.dot(dd).subs(t,h),'weighted_distance_bound')
   ck((nn.dot(dd)).subs(t,h)/DG>=c0/(6*M*h),'weighted_support_divergence_control')
# Real monic quadratic comparison: sign conditions, a closed convex orthant.
for a in range(0,8):
 for b in range(0,8):
  roots=S.solve(z*z+a*z+b,z)
  ck(all(S.re(r)<=0 for r in roots),'real_quadratic_orthant_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'floating_diagnostics':0,'scope':'Exact factorization, full coefficient gradients, normal support divergence, weighted-metric checks and real-quadratic contrast. No explicit nearest-point pair is numerically asserted; nonuniqueness follows analytically from the primary local-projection theorem. Source coverage and the finite-subgradient distinction require independent review.'},indent=2,sort_keys=True))
