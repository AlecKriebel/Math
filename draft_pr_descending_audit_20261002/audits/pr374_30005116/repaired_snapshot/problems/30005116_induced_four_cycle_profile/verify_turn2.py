#!/usr/bin/env python3
"""Exact finite controls for join replacement and non-multipartite ties."""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb,prod
import json
counts={}
def ck(x,s):
 assert x,s
 counts[s]=counts.get(s,0)+1
E4=list(combinations(range(4),2))
matchings=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
for bits in range(64):
 edges={e for i,e in enumerate(E4) if bits>>i&1}
 degrees=[sum(i in e for e in edges) for i in range(4)]
 isc4=all(d==2 for d in degrees)
 match=sum(all(e in edges for e in M) for M in matchings)
 ck(2*int(isc4)<=match,'pointwise_four_vertex_matching_bound')
 if isc4:ck(match==2,'c4_matching_normalization')

def kernel_profile(weights,A):
 n=len(weights)
 p=sum(weights[i]*weights[j]*A[i][j] for i,j in product(range(n),repeat=2))
 c=Q(0)
 for I in product(range(n),repeat=4):
  w=prod(weights[i] for i in I)
  for M in matchings:
   z=w
   for j,k in E4:
    a=A[I[j]][I[k]]
    z*=1-a if (j,k) in M else a
   c+=z
 return p,c

def Ldata(q):
 r=1//q;d=((r+1)*q-1)/r
 A=(1+6*r*d+r*(r*r-r+1)*d*d)/(r+1)**3
 B=4*r*(r-1)*d/(r+1)**3
 return d,A,B

def at_least_L(z,q):
 d,A,B=Ldata(q)
 return z>=A or B*B*d>=(A-z)**2

modules=[([Q(1) ],[[Q(0)]]),
 ([Q(1)],[[Q(1,3)]]),
 ([Q(1,2),Q(1,2)],[[Q(0),Q(1)],[Q(1),Q(0)]]),
 ([Q(4,5),Q(1,10),Q(1,10)],[[Q(i!=j) for j in range(3)] for i in range(3)]),
 ([Q(1,3)]*3,[[Q(abs(i-j)==1) for j in range(3)] for i in range(3)])]
profiles=[]
for w,A in modules:
 p,c=kernel_profile(w,A);profiles.append((p,c))
 ck(p<=Q(1,2),'module_density_hypothesis');ck(c<=Q(3,2)*p*p,'module_low_density_bound')
join_cases=0
for i,j in combinations(range(len(modules)),2):
 for h in (Q(1,3),Q(2,5),Q(3,4)):
  wi,Ai=modules[i];wj,Aj=modules[j]
  w=[h*a for a in wi]+[(1-h)*b for b in wj];n=len(wi);m=len(wj)
  A=[[Q(1)]*(n+m) for _ in range(n+m)]
  for a,b in product(range(n),repeat=2):A[a][b]=Ai[a][b]
  for a,b in product(range(m),repeat=2):A[n+a][n+b]=Aj[a][b]
  p,c=kernel_profile(w,A);p1,c1=profiles[i];p2,c2=profiles[j]
  q1,q2=1-p1,1-p2;qq=h*h*q1+(1-h)**2*q2
  expected=h**4*c1+(1-h)**4*c2+6*h*h*(1-h)**2*q1*q2
  ck(p==1-qq,'join_edge_identity');ck(c==expected,'join_c4_direct_integral')
  gain=h**4*(Q(3,2)*p1*p1-c1)+(1-h)**4*(Q(3,2)*p2*p2-c2)
  p4=h**4*(q1*q1-p1*p1/2)+(1-h)**4*(q2*q2-p2*p2/2)
  ck(c+gain==3*(qq*qq-p4),'replacement_exact_gain')
  ck(gain>=0,'replacement_nondecrease');ck(at_least_L(p4,qq),'refined_multipartite_bound')
  join_cases+=1

# Direct 0/1 step-graphon integrals with integer masses, independent of join formula.
def integer_profile(mass,A):
 n=len(mass);D=sum(mass)
 e=sum(mass[i]*mass[j]*A[i][j] for i,j in product(range(n),repeat=2))
 t=one=c4=paw=0
 for I in product(range(n),repeat=3):
  w=prod(mass[i] for i in I);e3=sum(A[I[i]][I[j]] for i,j in combinations(range(3),2))
  if e3==3:t+=w
  if e3==1:one+=w
 for I in product(range(n),repeat=4):
  deg=[sum(A[I[i]][I[j]] for j in range(4) if j!=i) for i in range(4)]
  w=prod(mass[i] for i in I)
  if all(d==2 for d in deg):c4+=w
  if sorted(deg)==[1,2,2,3]:paw+=w
 return Q(e,D*D),Q(t,D**3),Q(one,D**3),Q(c4,D**4),Q(paw,D**4)

family=[]
for r in range(2,11):
 for lo,hi in [(1,2),(1,3),(2,3)]:
  den=r*hi*hi+lo*lo;a=Q(hi*hi,den);b=Q(lo*lo,den)
  u=v=Q(lo*hi,den);z=Q((hi-lo)**2,den)
  masses=[hi*hi]*(r-1)+[lo*hi,lo*hi,(hi-lo)**2]
  k=len(masses);U,V,Z=r-1,r,r+1
  A=[[int(i!=j and (i<r-1 or j<r-1 or {i,j}=={U,V})) for j in range(k)] for i in range(k)]
  edge,tri,one,c4,paw=integer_profile(masses,A)
  original=[a]*r+[b];q=sum(t*t for t in original)
  expected_c=3*(q*q-sum(t**4 for t in original))
  expected_tri=6*sum(x*y*z for x,y,z in combinations(original,3))
  ck(r*a+b==1 and u*v==a*b and u+v+z==a+b,'tie_mass_constraints')
  ck(edge==1-q,'tie_edge_direct_count');ck(c4==expected_c,'tie_c4_direct_count')
  ck(tri==expected_tri,'credited_triangle_family_count')
  ck(one==6*a*b*z>0,'one_edge_obstruction_direct_count')
  ck(paw==24*(r-1)*a*a*b*z>0,'paw_direct_count')
  ck(one/3==2*a*b*z,'edit_separation_constant')
  if (r,lo,hi)==(2,1,2):
   ck((edge,c4,tri,one,one/3)==(Q(16,27),Q(64,243),Q(32,243),Q(8,243),Q(8,729)),'explicit_rational_example')
   example={'edge':str(edge),'c4':str(c4),'triangle':str(tri),'one_edge_triple':str(one),'edit_lower_bound':str(one/3)}
  family.append((r,lo,hi))
for n in range(4,101):
 ck(Q(comb(n,2)*comb(n-2,2),comb(n,4))==6,'finite_edit_lipschitz')
 ck(Q(6,n)>=1-Q(n*(n-1)*(n-2)*(n-3),n**4),'collision_union_bound')
print(json.dumps({'assertions':sum(counts.values()),'by_scope':counts,
 'arithmetic':'exact integers and fractions; direct kernel integrations and motif counts',
 'four_vertex_graphs':64,'internal_modules':len(modules),'direct_join_cases':join_cases,
 'nonmultipartite_tie_cases':len(family),'max_part_count_in_tie_checks':12,
 'rational_example':example,
 'scope':'Finite controls supplement the universal join theorem; Pikhurko–Razborov stability is a credited external theorem.'},indent=2)+'\n',end='')
