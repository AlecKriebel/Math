#!/usr/bin/env python3
"""Exact Gram-polynomial controls for the fixed-affine refinement obstruction.
Uses no author turn1 code and no numerical logarithms or square roots.
"""
from fractions import Fraction as Q
from itertools import product,combinations
from collections import Counter,defaultdict
import json
checks=Counter()
def ck(x,label):
 assert x,label;checks[label]+=1
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def form(v):return (v[0]*v[0],2*v[0]*v[1],v[1]*v[1])
def polynomial_product(a,b):
 return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[0]*b[2]+a[2]*b[0],a[1]*b[1],a[1]*b[2]+a[2]*b[1],a[2]*b[2])
def proportional(a,b):return all(a[i]*b[j]==a[j]*b[i] for i,j in combinations(range(len(a)),2))
def value(a,G):return sum(x*y for x,y in zip(a,G))
def ratio(points,G):
 a,b,c,d=points
 return value(form(sub(a,c)),G)*value(form(sub(b,d)),G)/(value(form(sub(b,c)),G)*value(form(sub(a,d)),G))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
Gs=[tuple(map(Q,(a,b,c))) for a,c in product(range(1,5),repeat=2) for b in range(-2,3) if a*c>b*b]
quads=0;witnesses=[]
for r,t in product((-1,0,1,2),repeat=2):
 for s,v in product((Q(1,2),Q(1),Q(2)),repeat=2):
  P=((Q(0),Q(0)),(Q(1),Q(0)),(Q(r),s),(Q(t),-v));a,b,c,d=P
  forms=[form(sub(x,y)) for x,y in [(a,c),(b,d),(b,c),(a,d)]]
  num=polynomial_product(forms[0],forms[1]);den=polynomial_product(forms[2],forms[3])
  ck(not proportional(num,den),'nonproportional_crossratio_polynomials')
  ck(not ((proportional(forms[0],forms[2]) and proportional(forms[1],forms[3])) or (proportional(forms[0],forms[3]) and proportional(forms[1],forms[2]))),'both_factor_pairings_excluded')
  q0=ratio(P,(Q(1),Q(0),Q(1)));G=next(G for G in Gs if ratio(P,G)!=q0)
  ck(ratio(P,G)!=q0,'exact_SPD_variation_witness')
  for x,y in combinations([sub(a,c),sub(b,d),sub(b,c),sub(a,d)],2):
   ck(proportional(form(x),form(y))==(det(x,y)==0),'linear_form_parallelism_equivalence')
  quads+=1
# Several actual proper triangulations of the standard reference triangle.
A=(Q(0),Q(0));B=(Q(1),Q(0));C=(Q(0),Q(1));m01=(Q(1,2),Q(0));m12=(Q(1,2),Q(1,2));m20=(Q(0),Q(1,2));g=(Q(1,3),Q(1,3))
patterns={
 'midpoint':([A,B,C,m01,m12,m20],[(0,3,5),(1,4,3),(2,5,4),(3,4,5)]),
 'barycentric':([A,B,C,m01,m12,m20,g],[(0,3,6),(3,1,6),(1,4,6),(4,2,6),(2,5,6),(5,0,6)]),
 'centroid_star':([A,B,C,g],[(0,1,3),(1,2,3),(2,0,3)]),
 'asymmetric_star':([A,B,C,(Q(1,4),Q(1,5))],[(0,1,3),(1,2,3),(2,0,3)]),
 'one_third_edge_split':([A,B,C,(Q(1,3),Q(0))],[(0,3,2),(3,1,2)])}
records=[]
for name,(pts,faces) in patterns.items():
 around=defaultdict(list);area=0
 for f in faces:
  p,q,r=[pts[i] for i in f];twice=det(sub(q,p),sub(r,p));ck(twice>0,'reference_triangles_nondegenerate');area+=twice
  for i,j in combinations(f,2):around[tuple(sorted((i,j)))].append(next(k for k in f if k not in (i,j)))
 ck(area==1,'reference_area_cover_control')
 interior=[(ij,opps) for ij,opps in around.items() if len(opps)==2];ck(bool(interior),'proper_pattern_interior_edge')
 for (i,j),(k,l) in interior:
  P=pts[i],pts[j],pts[k],pts[l];q0=ratio(P,(Q(1),Q(0),Q(1)))
  G=next(G for G in Gs if ratio(P,G)!=q0);q1=ratio(P,G)
  ck(q0!=q1,'proper_pattern_changes_refined_invariant')
  # Original squared side lengths remain a nondegenerate triangle via SPD.
  ck(G[0]>0 and G[0]*G[2]>G[1]*G[1],'original_metric_positive_definite')
  records.append({'pattern':name,'edge':[i,j],'opposite':[k,l],'G':[str(x) for x in G],'squared_crossratio_at_identity':str(q0),'squared_crossratio_at_G':str(q1)})
# Exact inverse of the three-vertex scaling map (working with formal rational log changes).
for a,b,c in product(range(-3,4),repeat=3):
 w=(a+b,b+c,c+a);u=((Q(w[0]+w[2]-w[1],2)),Q(w[0]+w[1]-w[2],2),Q(w[1]+w[2]-w[0],2))
 ck(u==(a,b,c),'local_log_scaling_map_invertible')
print(json.dumps({'status':'PASS','arithmetic':'exact rational Gram-polynomial coefficients','assertions':sum(checks.values()),'by_scope':dict(checks),'adjacent_quadruples':quads,'SPD_control_matrices':len(Gs),'proper_pattern_witnesses':records,'scope':'Excludes only proper fixed-barycentric-coordinate refinements with induced metrics. Metric-dependent and non-isometric schemes, and the source-formulation ambiguity, remain open.'},indent=2,sort_keys=True))
