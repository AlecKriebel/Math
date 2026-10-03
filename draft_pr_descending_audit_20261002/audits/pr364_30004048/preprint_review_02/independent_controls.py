#!/usr/bin/env python3
"""Exact weighted feasibility/dual certificates and irregular ordinary graphs.
New reviewer controls; no universal proof or minimizer evaluation by finite tests.
"""
from fractions import Fraction as Q
from math import lcm
from itertools import product
import json
counts={};details=[]
def ck(family,test):
 assert test,family
 counts[family]=counts.get(family,0)+1
def times(M,q):return [sum(Q(a)*b for a,b in zip(row,q)) for row in M]
def transpose(M):return list(map(list,zip(*M)))
def regular(M,b,q,theta):
 return sum(b)==sum(q)==1 and min(b+q)>0 and times(M,q)==[theta]*len(M) and times(transpose(M),b)==[theta]*len(q) and len(set(map(tuple,transpose(M))))==len(q)
def weighted(M,b,q,theta):
 D=max(map(sum,M));n=len(q);t=theta/D;residual=1-n*t
 a=[t]*n+([residual] if residual else [])
 P=[[1-x for x in col] for col in transpose(M)]+([[1]*len(b)] if residual else [])
 ck('weighted_primal',residual>=0 and min(a)>0 and sum(a)==1)
 ck('weighted_primal',min(times(P,b))>=1-theta)
 ck('weighted_primal',min(times(transpose(P),a))>=1-theta)
 ck('weighted_primal',min(times(M,q))>=theta and min(times(transpose(M),b))>=theta)
 R=[[int(any(x*y for x,y in zip(row,col))) for col in transpose(M)] for row in P]
 ck('weighted_primal',times(transpose(R),a)==[1-t]*n)
 # Concrete elementary LP dual: a maximum-degree row's inequalities imply D*t<=theta.
 v=max(range(len(M)),key=lambda j:sum(M[j]));ck('dual_row',sum(M[v])==D)
 ck('dual_row',sum(M[v][j]*a[j] for j in range(n))==theta)
 eps=Q(1,10000);ck('dual_row',sum(M[v][j]*(t+eps) for j in range(n))>theta)
 # Normalize feasibility obstruction differs from the row-dual obstruction.
 ck('dual_average',sum(b[v]*sum(M[v]) for v in range(len(M)))==n*theta)
 ck('dual_average',n*t<=1)
 return P,a,t,residual

def copies(weights):
 den=lcm(*(v.denominator for v in weights));return [i for i,v in enumerate(weights) for _ in range(int(den*v))]
def ordinary(P,M,a,b,q,theta):
 aa,bb,cc=copies(a),copies(b),copies(q)
 AB=[{j for j,u in enumerate(bb) if P[v][u]} for v in aa]
 CB=[{j for j,u in enumerate(bb) if M[u][v]} for v in cc]
 return AB,CB,aa,bb,cc

def extract(AB,CB,m,theta):
 na,nc=len(AB),len(CB);BA=[{a for a,s in enumerate(AB) if v in s} for v in range(m)];BC=[{c for c,s in enumerate(CB) if v in s} for v in range(m)]
 ck('ordinary_four_degrees',min(map(len,AB))>=m*(1-theta))
 ck('ordinary_four_degrees',min(map(len,BA))>=na*(1-theta))
 ck('ordinary_four_degrees',min(map(len,CB))>=m*theta)
 ck('ordinary_four_degrees',min(map(len,BC))>=nc*theta)
 reached=[set().union(*(BA[v] for v in s)) for s in CB];F=Q(max(map(len,reached)),na)
 if F<1:
  ck('irregular_extraction',set(map(len,CB))=={m*theta} and set(map(len,BC))=={nc*theta})
  supports=sorted(set(map(frozenset,CB)),key=lambda s:tuple(sorted(s)));missing=[{a for a,s in enumerate(AB) if not (s&T)} for T in supports]
  for T,inds in zip(supports,missing):ck('irregular_extraction',bool(inds) and all(AB[a]==set(range(m))-T for a in inds))
  ck('irregular_extraction',sum(map(len,missing))==len(set().union(*missing)))
  mass=[Q(len(s),na) for s in missing];t=min(mass);D=max(sum(v in T for T in supports) for v in range(m))
  ck('irregular_extraction',F==1-t and t*D<=theta)
  ck('irregular_extraction',all(sum(mass[i] for i,T in enumerate(supports) if v in T)<=theta for v in range(m)))
  details.append(dict(parts=[na,m,nc],theta=str(theta),F=str(F),distinct_C=len(supports),extra_A=na-len(set().union(*missing)),AB_degree_count=len(set(map(len,AB)))))
 return F

seed=[[1,0,1,1,1,0,0],[0,1,1,1,1,0,0],[0,0,1,0,0,1,1],[0,0,0,1,0,1,1],[0,0,0,0,1,1,0],[1,1,0,0,0,1,0],[1,1,0,0,0,0,1]]
# Deliberate wrong incidence is rejected, then PRIMARY figure transcription supplies the correct row.
b=[Q(v,27) for v in [5,5,3,3,3,4,4]];q=[Q(v,27) for v in [4,4,3,3,3,5,5]]
ck('wrong_source_mutation',not regular(seed,b,q,Q(13,27)));seed[4]=[0,0,0,0,1,1,1]
for numerator in [13,14]:
 M=seed if numerator==13 else [[1-x for x in row] for row in seed];theta=Q(numerator,27)
 ck('regular_linear_feasibility',regular(M,b,q,theta));P,a,t,residual=weighted(M,b,q,theta)
 # Split each row into unequal rational twins. This preserves equations/degree yet rectangularity changes.
 Ms=[row[:] for row in M for _ in range(2)];bs=[v*f for v in b for f in [Q(1,3),Q(2,3)]]
 ck('repeated_rows',regular(Ms,bs,q,theta));weighted(Ms,bs,q,theta)
 AB,CB,aa,bb,cc=ordinary(P,M,a,b,q,theta);baseline=extract(AB,CB,len(bb),theta)
 # Perturb universal residual edges only along rows with strict B-to-A slack.
 # A vertices no longer all have type-complete adjacency: ordinary graph is intentionally irregular.
 spare=[j for j,v in enumerate(bb) if sum(M[v])<max(map(sum,M))]
 extras=[i for i,v in enumerate(aa) if v==len(q)]
 for i in extras:AB[i].remove(spare[i%len(spare)])
 ck('irregular_mutation',len({frozenset(AB[i]) for i in extras})>1)
 ck('irregular_mutation',extract(AB,CB,len(bb),theta)==baseline)
 # Add one missing B-C edge: all degrees remain admissible, exact regularity is lost and max reach is full.
 modified=[set(s) for s in CB];k=next(c for c,s in enumerate(modified) if len(s)<len(bb));v=next(j for j in range(len(bb)) if j not in modified[k]);modified[k].add(v)
 ck('full_case_separate',extract(AB,modified,len(bb),theta)==1)

# A broad cyclic family challenges rational weights and zero residual.
for r in range(2,13):
 for p in range(1,r):
  M=[[int((i-j)%r<p) for j in range(r)] for i in range(r)];w=[Q(1,r)]*r;theta=Q(p,r)
  ck('regular_linear_feasibility',regular(M,w,w,theta));P,a,t,delta=weighted(M,w,w,theta)
  ck('zero_residual',delta==0 and len(a)==r)
# Repeated columns satisfy weighted equations but cannot be used without grouping.
M=[[1,1,0],[0,0,1]];b2=[Q(1,2)]*2;q2=[Q(1,4),Q(1,4),Q(1,2)]
ck('duplicate_columns',times(M,q2)==[Q(1,2)]*2 and times(transpose(M),b2)==[Q(1,2)]*3)
ck('duplicate_columns',not regular(M,b2,q2,Q(1,2)))
P=[[1-x for x in col] for col in transpose(M)]+[[1,1]];a=[Q(1,4)]*4
R=[[int(any(x*y for x,y in zip(row,col))) for col in transpose(M)] for row in P]
ck('duplicate_columns',times(transpose(R),a)==[Q(1,2),Q(1,2),Q(3,4)])
# Zero row mass keeps equations but violates the antichain and support-preserving hypotheses.
Z=[[1,1,0,0],[0,0,1,1],[0,1,1,0]];bz=[Q(1,2),Q(1,2),Q(0)];qz=[Q(1,4)]*4
ck('zero_mass',times(Z,qz)==[Q(1,2)]*3 and times(transpose(Z),bz)==[Q(1,2)]*4)
ck('zero_mass',not regular(Z,bz,qz,Q(1,2)))
T=[{i for i,row in enumerate(Z) if row[j]} for j in range(4)]
ck('zero_mass',T[0]<T[1] and T[3]<T[2])
ck('zero_mass',len({frozenset(s-{2}) for s in T})==2)
# All sixteen rational possibilities remain separated, without using actual d or e values.
gaps=[abs(Q(13,27*d)-Q(14,27*e)) for d,e in product(range(1,5),repeat=2)]
ck('gap',min(gaps)==Q(1,108) and all(g>=Q(1,108) for g in gaps))
print(json.dumps(dict(status='PASS',assertions=sum(counts.values()),categories=counts,irregular_ordinary_graphs=details,scope='New finite exact affine-feasibility, row-dual/average, rational row-splitting, irregular ordinary graph and invalid-hypothesis controls. No census proof, true invariant minima, exact psi values, sign or priority claim.'),indent=2,sort_keys=True))
