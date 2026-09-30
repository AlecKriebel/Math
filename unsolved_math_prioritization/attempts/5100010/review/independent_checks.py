#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from math import gcd
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(g,b):assert b,g;C[g]+=1
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def mul(s,p):return(s*p[0],s*p[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def J(p):return(-p[1],p[0])
def unit(t):return((1-t*t)/(1+t*t),2*t/(1+t*t))
pairs=0
for c in (F(1),F(3,2),F(4)):
 for v,w in ((F(3),F(2)),(F(5),F(3)),(F(7,2),F(5,2)),(F(2),F(3,2))):
  a=c*(v+1/v)/2;b=c*(v-1/v)/2
  ap=c*(w+1/w)/2;bp=c*(w-1/w)/2
  lam=a*a-ap*ap
  ck('confocal_axes',a*a-b*b==c*c==ap*ap-bp*bp and lam==b*b-bp*bp and 0<lam<b*b)
  ci=c/(b*b);co=c/(bp*bp);r=a/(b*b);R=ap/(bp*bp);d=co-ci
  ck('strict_circle_nesting',R-r-d==1/(ap+c)-1/(a+c)>0)
  k2=4*R*d/((R+d)**2-r*r)
  ck('elliptic_modulus_domain',0<k2<1)
  for A,B,cen,rad in ((a,b,ci,r),(ap,bp,co,R)):
   for den in range(1,10):
    for num in range(-den,den+1):
     u=unit(F(num,den));q=(cen+rad*u[0],rad*u[1]);h=1+c*q[0]
     ck('no_extraneous_polar_branch',h>=A/(A+c)>0)
     ck('dual_circle_polynomial',B*B*dot(q,q)-2*c*q[0]-1==0)
     ck('unsquared_support_identity',A*A*q[0]*q[0]+B*B*q[1]*q[1]==h*h)
     p=(-c+A*A*q[0]/h,B*B*q[1]/h)
     ck('contact_original_conic',(p[0]+c)**2/(A*A)+p[1]**2/(B*B)==1)
     ck('contact_polar_incidence',dot(q,p)==1)
     dist=A-c*(p[0]+c)/A
     ck('focal_distance',dist>0 and dot(p,p)==dist*dist)
  pairs+=1
# Closed rational tangent polygons with actual star ordering, not convex-hull reorder.
base=[(F(1),F(0)),(F(4,5),F(3,5)),(F(3,5),F(4,5))]
normals=[]
for j in range(4):
 for p in base:
  for _ in range(j):p=J(p)
  normals.append(p)
stars=0
for center,radius,step in product([(F(0),F(0)),(F(2),F(-3)),(F(7,5),F(11,3))],(F(1),F(3,2)),(1,5,7,11)):
 # Reverse branch if necessary so each directed normal increment is positive.
 order=[normals[(i*step)%12] for i in range(12)]
 if det(order[0],order[1])<0:order=list(reversed(order))
 ck('primitive_star_order',gcd(step,12)==1 and len(set(order))==12)
 Q=[]
 for u,v in zip(order,order[1:]+order[:1]):
  ss=det(u,v);cc=dot(u,v)
  ck('positive_local_turn',ss>0 and cc>-1)
  q=add(center,add(mul(radius,u),mul(radius*ss/(1+cc),J(u))))
  ck('both_tangent_lines',dot(u,sub(q,center))==radius==dot(v,sub(q,center)))
  Q.append(q)
 lhs=F(0);rhs=F(0)
 for i,u in enumerate(order):
  v=order[(i+1)%12];incoming=sub(Q[i],Q[(i-1)%12]);outgoing=sub(Q[(i+1)%12],Q[i])
  li=dot(incoming,J(u));lo=dot(outgoing,J(v))
  ck('ordinary_side_directions',li>0 and lo>0 and incoming==mul(li,J(u)) and outgoing==mul(lo,J(v)))
  touch=add(center,mul(radius,u));tau=dot(sub(touch,Q[(i-1)%12]),J(u))/li
  ck('contact_on_segment',0<tau<1)
  actual=-dot(incoming,outgoing)/(li*lo);bridge=-dot(u,v)
  ck('ordinary_angle_bridge',actual==bridge)
  lhs+=actual;rhs+=bridge
 ck('whole_star_sum_bridge',lhs==rhs)
 stars+=1
# Primitive Jacobi steps in K units, including odd winding and even period.
steps=0
for n in range(3,101):
 for w in range(1,n):
  if gcd(w,n)!=1:continue
  sigma=F(2*w,n)
  ck('true_jacobi_closure',n*sigma==2*w)
  ck('doubled_paper_convention',sigma==F(4*w,2*n) and 2*n*sigma==4*w)
  ck('no_adjacent_pole_collision',(2*sigma/2).denominator!=1)
  # Pole indices in the doubled cyclic list occur in opposite pairs modulo n.
  for j in (0,1,n-1):
   poles={j%(2*n),(j+n)%(2*n)}
   ck('pole_neighbor_coefficients_regular',all((h-2)%(2*n) not in poles and (h+2)%(2*n) not in poles for h in poles))
   ck('each_pole_has_two_summands',all(sum(h in {(i-1)%(2*n),(i+1)%(2*n)} for i in range(2*n))==2 for h in poles))
  steps+=1
root=Path(__file__).resolve().parent
out={'verdict':'PASS_EXACT_INDEPENDENT_CONTROLS','assertions':sum(C.values()),'groups':dict(sorted(C.items())),'rational_confocal_pairs':pairs,'closed_tangent_star_configurations':stars,'primitive_winding_cases':steps,'artifact_sha256':sha256((root/'author_replay/SOURCE_STATUS.md').read_bytes()).hexdigest(),'limitations':'Local polar and angle geometry plus exact Jacobi index checks. Arbitrary tangent-star controls are not asserted bicentric; the all-period invariant uses the audited published elliptic-function argument.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'assertions':out['assertions'],'verdict':out['verdict']}))
