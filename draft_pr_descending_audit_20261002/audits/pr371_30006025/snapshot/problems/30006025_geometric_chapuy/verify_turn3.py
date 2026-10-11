#!/usr/bin/env python3
"""Exact combinatorial and rational bounds for the regular-polygon scope test."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  out.append(c)
 return out
def power(p,k):
 out=list(range(len(p)))
 for _ in range(k):out=[p[i] for i in out]
 return out
for g in range(2,101):
 E=6*g-3;V=4*g-2;N=2*E
 ck(3*V==2*E and V-E+1==2-2*g,'trivalent_map_counts')
 A=Q(N-2)-Q(2*N,3);orb=Q(1,3)-Q(2,N)
 ck(A==4*(g-1),'polygon_area_coefficient')
 ck(orb>0 and A/orb==N,'triangle_orbifold_index')
 ck(Q(1,2)+Q(1,3)+Q(1,N)<1 and N>12,'hyperbolic_triangle_and_angle_bound')
 # CFF cubic restriction: leaves in triples, internal vertices singleton.
 leaves=3*g;internal=3*g-2
 ck(leaves+internal==E+1 and leaves+3*internal==2*E,'decorated_tree_degree_counts')
 ck(leaves//3+internal==V,'decorated_tree_merged_vertices')
examples=json.loads(Path(__file__).with_name('TURN_1_CHECKS.json').read_text())['one_face_examples']
for ex in examples:
 w=ex['edge_word'];N=len(w);positions={j:[i for i,e in enumerate(w) if e==j] for j in set(w)};alpha=[None]*N
 for pair in positions.values():
  ck(len(pair)==2,'paired_side_occurrences');a,b=pair;alpha[a]=b;alpha[b]=a
 sigma=[(alpha[i]+1)%N for i in range(N)]
 ck(power(alpha,2)==list(range(N)) and all(alpha[i]!=i for i in range(N)),'clean_dessin_order_two')
 ck(all(len(v)==3 for v in cycles(sigma)) and power(sigma,3)==list(range(N)),'clean_dessin_order_three')
 face=[sigma[alpha[i]] for i in range(N)]
 ck(len(cycles(face))==1 and power(face,N)==list(range(N)),'transitive_full_face_cycle')
 ck(all(Q(2,3)*len(v)==2 for v in cycles(sigma)),'smooth_vertex_angle_sums')
ck(Q(3)>Q(25,9),'sqrt3_exceeds_5thirds_squared_certificate')
cosh_upper=1+Q(1,8)/(1-Q(1,48));ck(cosh_upper==Q(53,47) and cosh_upper<Q(4,3),'cosh_half_rational_upper_bound')
for k in range(1,51):ck(Q(1,4*(2*k+1)*(2*k+2))<=Q(1,48),'cosh_tail_ratio_bound')
mu_first=(Q(1)-Q(1,2)**2)/4
ck(mu_first==Q(3,16),'poisson_mean_first_term_lower_bound')
ck(mu_first/(1+mu_first)==Q(3,19),'count_law_gap_rational_lower_bound')
mu_lower=sum((1-Q(1,2)**(2*k))/((2*k)*factorial(2*k)) for k in range(1,11));next_upper=Q(1,22*factorial(22));mu_upper=mu_lower+2*next_upper
ck(mu_lower>Q(3,16),'positive_higher_intensity_terms')
print(json.dumps({'status':'PASS','arithmetic':'exact integers and rational bounds; standard library only','assertions':sum(C.values()),'by_scope':dict(C),'genera_checked_as_controls':[2,100],'clean_dessin_examples':len(examples),'intensity_integral_rational_bounds':{'lower':str(mu_lower),'upper':str(mu_upper)},'strict_count_law_distance_lower_bound':'3/19','scope':'Philippe triangle-group systoles and Mirzakhani-Petri Poisson convergence are credited external theorems. These controls do not certify new systole classifications or a full geometric Chapuy solution.'},indent=2,sort_keys=True))
