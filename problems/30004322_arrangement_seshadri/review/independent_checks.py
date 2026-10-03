#!/usr/bin/env python3
"""Independent exact source-scoped controls. Requires SymPy for cyclotomic polynomials."""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt,comb
import sympy as S
import json
C={}
def ck(x,s):
 assert x,s
 C[s]=C.get(s,0)+1

# Degree cutoff checked by exact polynomial signs, not by floating roots.
cutoffs=0
for k in range(2,41):
 for r in range(k,k*k):
  A=k*k-r;B=2*k-r*k+3*r;C0=1-3*r;delta=B*B-4*A*C0
  root=(-B+isqrt(delta))//(2*A);D=max((r+2*k-1)//(2*k),root)
  f=lambda d:A*d*d+B*d+C0
  ck(f(root)<=0<f(root+1),'integer_root_isolation')
  d=D+1
  ck(f(d)>0 and 2*A*d+B>0,'cutoff_positive_tail')
  ck(2*(k*d+1)>=r,'monotonicity_threshold')
  ck((k*d+1)**2-r*(k*d+1)-r*(d*d-3*d+2)==f(d),'genus_quadratic_identity')
  cutoffs+=1

def norm(v):
 a=next(t for t in v if t);return tuple(Q(t,a) for t in v)
def cross(a,b):return norm((a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(M):
 M=[list(map(Q,row)) for row in M];j=0
 for col in range(len(M[0])):
  pivot=next((i for i in range(j,len(M)) if M[i][col]),None)
  if pivot is None:continue
  M[j],M[pivot]=M[pivot],M[j];a=M[j][col];M[j]=[x/a for x in M[j]]
  for i in range(len(M)):
   if i!=j:
    a=M[i][col];M[i]=[x-a*y for x,y in zip(M[i],M[j])]
  j+=1
  if j==len(M):break
 return j
# A different off-conic eighth point from the author fixture.
points=[(Q(t),Q(t*t),Q(1)) for t in range(7)]+[(Q(1),Q(2),Q(1))]
lines={cross(a,b) for a,b in combinations(points,2)}
ck(max(sum(dot(L,p)==0 for p in points) for L in lines)==3,'independent_conic_mpl')
rows=[[x*x,x*y,y*y,x*z,y*z,z*z] for x,y,z in points]
ck(rank(rows)==6,'off_conic_full_rank')
for subset in combinations(range(8),7):
 ck(rank([rows[i] for i in subset])==(5 if 7 not in subset else 6),'conic_seven_point_kernels')

# New rational modular-point arrangements and arbitrary added-line fixtures.
P=(Q(0),Q(0),Q(1));pool=list(map(norm,[(1,1,1),(1,-1,1),(2,3,1),(3,-2,1),(2,0,1),(0,2,1),(1,-4,0)]))
addsets=[(),*( (x,) for x in pool),*( (pool[i],pool[j]) for i,j in [(0,1),(0,4),(1,5),(2,6),(3,4),(4,5),(5,6)])]
branches={};arrangements=0
for slopes in [(0,1),(0,1,-1),(0,1,-1,2)]:
 base={norm((1,-t,0)) for t in slopes}|{norm((0,1,0)),norm((0,0,1)),norm((-1,0,1)),norm((0,-1,1))}
 oldZ={cross(a,b) for a,b in combinations(base,2)}
 pen0={L for L in base if dot(L,P)==0}
 ck(all(any(dot(L,z)==0 for L in pen0) for z in oldZ),'base_modularity')
 for adds in addsets:
  A=base|set(adds);Z={cross(a,b) for a,b in combinations(A,2)}
  pen={L for L in A if dot(L,P)==0};m=len(pen)
  new={L for L in A-base if dot(L,P)!=0}
  W={z for z in Z if not any(dot(L,z)==0 for L in pen)}
  kA=max(sum(dot(L,z)==0 for z in Z) for L in A)
  if not W:cover=set(pen);case='pencil'
  elif kA>=m+len(new):cover=pen|new;case='full_added_cover'
  else:
   ck(len(new)==2 and len(W)<=2,'outside_case_bound')
   H=cross(*tuple(W)) if len(W)==2 else next(L for L in new if dot(L,next(iter(W)))==0)
   cover=pen|{H};case='auxiliary_join'
  branches[case]=branches.get(case,0)+1
  ck(len(cover)<=kA,'new_cover_cost')
  ck(all(any(dot(L,z)==0 for L in cover) for z in Z),'new_cover_coverage')
  support=cover|A;k0=max(sum(dot(L,z)==0 for z in Z) for L in support)
  spans={cross(a,b) for a,b in combinations(Z,2)}
  for L in spans:
   hits=sum(dot(L,z)==0 for z in Z)
   ck(hits<=k0,'all_spanned_line_maximum')
   if L not in cover:ck(hits<=len(cover),'outside_cover_bezout_control')
  arrangements+=1

# Cyclotomic integer arithmetic: no approximate roots or copied cyclic incidence code.
class Field:
 def __init__(self,n):
  x=S.Symbol('x');co=[int(z) for z in S.Poly(S.cyclotomic_poly(n,x),x).all_coeffs()][::-1]
  self.n=n;self.d=len(co)-1;self.mod=co;self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
  z=(0,1)+(0,)*(self.d-2);self.roots=[self.one]
  for i in range(1,n):self.roots.append(self.mul(self.roots[-1],z))
  ck(self.mul(self.roots[-1],z)==self.one,'cyclotomic_order')
  ck(len(set(self.roots))==n,'primitive_root_distinctness')
 def neg(self,a):return tuple(-v for v in a)
 def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
 def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
 def mul(self,a,b):
  if a==self.zero or b==self.zero:return self.zero
  if a==self.one:return b
  if b==self.one:return a
  c=[0]*(2*self.d-1)
  for i,x in enumerate(a):
   if x:
    for j,y in enumerate(b):
     if y:c[i+j]+=x*y
  for k in range(len(c)-1,self.d-1,-1):
   v=c[k]
   if v:
    for j in range(self.d):c[k-self.d+j]-=v*self.mod[j]
  return tuple(c[:self.d])
 def dot(self,a,b):
  v=self.zero
  for x,y in zip(a,b):v=self.add(v,self.mul(x,y))
  return v
 def cross(self,a,b):
  return(self.sub(self.mul(a[1],b[2]),self.mul(a[2],b[1])),self.sub(self.mul(a[2],b[0]),self.mul(a[0],b[2])),self.sub(self.mul(a[0],b[1]),self.mul(a[1],b[0])))
 def incident(self,L,p):return self.dot(L,p)==self.zero

# Independent Hesse/Fermat auxiliary certificate in Q(zeta_3).
f=Field(3);o,z=f.one,f.zero;roots=f.roots
centers=[(o,z,z),(z,o,z),(z,z,o)]
H=centers+[(o,roots[a],roots[b]) for a in range(3) for b in range(3)]
Qpts=[(z,o,f.neg(t)) for t in roots]+[(o,z,f.neg(t)) for t in roots]+[(o,f.neg(t),z) for t in roots]
Dpts=centers+[(o,roots[a],roots[b]) for a in range(3) for b in range(3)]
Z=Qpts+Dpts;F=[(o,f.neg(t),z) for t in roots]+[(z,o,f.neg(t)) for t in roots]+[(f.neg(t),z,o) for t in roots]
incH=[{j for j,p in enumerate(Z) if f.incident(L,p)} for L in H]
incF=[{j for j,p in enumerate(Z) if f.incident(L,p)} for L in F]
ck(len(set(Z))==21,'hesse_distinct_catalog')
for I in incH:ck((len(I&set(range(9))),len(I&set(range(9,21))))==(3,2),'hesse_actual_line_incidence')
for I in incF:ck(len(I)==4 and min(I)>=9,'fermat_aux_actual_incidence')
for i,j in combinations(range(12),2):ck(len(incH[i]&incH[j])==1,'hesse_pair_intersection_exhaustion')
for j in range(21):
 h=sum(j in I for I in incH);a=sum(j in I for I in incF)
 ck((h,a)==((4,0) if j<9 else(2,3)),'hesse_actual_point_incidence')
 ck(Q(h,4)+Q(a,6)==1,'hesse_primal_exact_cover')
y=[Q(1,6)]*9+[Q(1,4)]*12
for I in incH+incF:ck(sum(y[j] for j in I)==1,'hesse_support_dual')
for p,t in combinations(Z,2):
 L=f.cross(p,t);I={j for j,v in enumerate(Z) if f.incident(L,v)}
 ck(len(I)<=5,'hesse_all_lines_mpl')
 ck(sum(y[j] for j in I)<=1,'hesse_all_lines_dual')
 if len(I)==5:ck(I in incH,'hesse_only_computing_lines')
ck(sum(y)==Q(9,2),'hesse_dual_objective')

# Actual projective equations for q=1,2,3, independent of residue-count enumeration.
geom=[]
for q in (1,2,3):
 n=5*q;f=Field(n);o,z=f.one,f.zero;kept=[a for a in range(n) if a%5 in(0,2,3)]
 L=[];labels=[]
 for family in range(3):
  for a in kept:
   t=f.roots[a];L.append((o,f.neg(t),z) if family==0 else ((z,o,f.neg(t)) if family==1 else(f.neg(t),z,o)));labels.append((family,a))
 candidates=[(f.roots[(a+b)%n],f.roots[b],o) for a in range(n) for b in range(n)]
 grid=[];inc=[];dual=[]
 for p in candidates:
  I={i for i,l in enumerate(L) if f.incident(l,p)}
  if len(I)>=2:
   grid.append(p);inc.append(I)
   dual.append(Q(1,2*q) if len(I)==2 else(Q(1,q) if all(labels[i][1]%5==0 for i in I) else Q(0)))
 Z=grid+[(o,z,z),(z,o,z),(z,z,o)]
 for p in Z[len(grid):]:inc.append({i for i,l in enumerate(L) if f.incident(l,p)});dual.append(Q(0))
 ck(len(grid)==13*q*q and len(Z)==13*q*q+3,'subfamily_geometric_point_count')
 ck(sum(len(I)==2 for I in inc[:len(grid)])==6*q*q,'subfamily_geometric_doubles')
 ck(sum(len(I)==3 for I in inc[:len(grid)])==7*q*q,'subfamily_geometric_triples')
 w=[Q(1,3) if a%5==0 else Q(1,2) for _,a in labels]
 for I in inc:ck(sum(w[i] for i in I)>=1,'subfamily_geometric_primal')
 supports=[]
 for i,(_,a) in enumerate(labels):
  J={j for j,I in enumerate(inc) if i in I};supports.append(J)
  ck(len(J)==(3*q+1 if a%5==0 else 4*q+1),'subfamily_geometric_line_count')
  ck(sum(dual[j] for j in J)==1,'subfamily_geometric_component_dual')
 for i,j in combinations(range(len(L)),2):ck(len(supports[i]&supports[j])==1,'subfamily_geometric_pair_exhaustion')
 ck(sum(w)==sum(dual)==4*q,'subfamily_geometric_optimal_cost')
 maxline=None
 if q<=2:
  maxline=0
  for p,t in combinations(Z,2):
   line=f.cross(p,t);I={j for j,v in enumerate(Z) if f.incident(line,v)}
   maxline=max(maxline,len(I));ck(len(I)<=4*q+1,'subfamily_all_spanned_lines')
   if len(I)==4*q+1:ck(I in supports,'subfamily_only_component_minimizers')
  ck(maxline==4*q+1,'subfamily_mpl_exact')
 geom.append({'q':q,'field_degree':f.d,'actual_lines':len(L),'actual_points':len(Z),'all_spanned_lines_checked':q<=2})

# Additional deletion tests use only finite set loss counting; no theorem inferred from scan.
delcases=0
for n in range(3,16):
 samples=[(set(range(a)),set(range(0,n,2)) if b else set(),set(range(1,n,3)) if c else set()) for a in range(min(n-1,4)) for b in(0,1) for c in(0,1)]
 for A,B,D in samples:
  if min(n-len(s) for s in(A,B,D))<2:continue
  kept=0;T=0
  for a in range(n):
   for b in range(n):
    c=(-a-b)%n;deleted=(a in A)+(b in B)+(c in D)
    kept+=deleted<=1;T+=deleted==3
  P=len(A)*len(B)+len(B)*len(D)+len(D)*len(A)
  ck(kept==n*n-P+2*T,'independent_deleted_grid_count');delcases+=1
print(json.dumps({'assertions':sum(C.values()),'by_scope':C,'arithmetic':'exact rational and cyclotomic integer arithmetic; SymPy only supplies cyclotomic polynomials','degree_cutoff_cases':cutoffs,'new_rational_arrangements':arrangements,'certificate_branches':branches,'projective_subfamily_controls':geom,'deletion_controls':delcases,'scope':'Independent verification of frozen scoped claims; no new author search or general-conjecture conclusion.'},indent=2)+'\n',end='')
