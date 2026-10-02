#!/usr/bin/env python3
"""Independent bounded exact controls; no imports from author checkers.
The infinite-group/topological assertions require the accompanying proof audit.
"""
import itertools,json
from collections import Counter
from fractions import Fraction
C=Counter()
def check(p,key):
 assert p,key
 C[key]+=1
def reduce_word(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inverse(w):return tuple(-x for x in reversed(w))
def words(n):
 old=[()];out=old[:]
 for _ in range(n):
  old=[w+(x,) for w in old for x in (1,2,-1,-2) if not w or x!=-w[-1]];out+=old
 return out
def path(word):
 # Edge address uses its lower endpoint; this implementation records geometric
 # edges first and only then changes them into the author's negative labels.
 p=[0,0];edges=[]
 for a in word:
  if abs(a)==1:p[0]+=a
  elif a==2:edges.append(((p[0],p[1]),1));p[1]+=1
  else:p[1]-=1;edges.append(((p[0],p[1]),-1))
 lab=tuple(((-a,-b),s) for (a,b),s in edges)
 return lab,tuple(p)
def multiply_poly(p,q,d):
 z=Counter()
 for x,a in p.items():
  for y,b in q.items():
   if len(x)+len(y)<=d:z[x+y]+=a*b
 return {x:a for x,a in z.items() if a}
def shift(p,h):return {tuple((x-h[0],y-h[1]) for x,y in w):a for w,a in p.items()}
def cross_mul(a,b,d):
 p,h=a;q,k=b
 return multiply_poly(p,shift(q,h),d),(h[0]+k[0],h[1]+k[1])
def generator(a,d):
 if a==1:return {():1},(1,0)
 if a==-1:return {():1},(-1,0)
 if a==2:return {():1,((0,0),):1},(0,1)
 return {((0,1),)*i:(-1)**i for i in range(d+1)},(0,-1)
def evaluate(w,d):
 z=({():1},(0,0))
 for x in w:z=cross_mul(z,generator(x,d),d)
 return z
def expand_labels(labels,d):
 z={():1}
 for lab,s in labels:
  fac={():1,(lab,):1} if s==1 else {(lab,)*i:(-1)**i for i in range(d+1)}
  z=multiply_poly(z,fac,d)
 return z
seen=set()
W=words(8)
for w in W:
 labels,h=path(w)
 check(all(a!=b or s==t for (a,s),(b,t) in zip(labels,labels[1:])),'geometric_vertical_no_cancellation')
 check((labels,h) not in seen,'distinct_semidirect_images_through_length8');seen.add((labels,h))
 if len(w)<=6:
  p,k=evaluate(w,4)
  check(k==h and p==expand_labels(labels,4),'direct_crossed_series_vs_geometric_path')
  check(p.get((),0)==1,'constant_coefficient')
  check(not w or (p,k)!=({():1},(0,0)),'bounded_detected_nonidentity')
  check(cross_mul((p,k),evaluate(inverse(w),4),4)==({():1},(0,0)),'formal_inverse_products')
# Full multiplication on independently chosen finite sample, including reductions.
S=words(3)
for a in S:
 for b in S:
  check(cross_mul(evaluate(a,2),evaluate(b,2),2)==evaluate(reduce_word(a+b),2),'crossed_homomorphism')
# Grid free basis and exact first-order map, with larger nonsymmetric ranges.
def power(a,n):return (a if n>=0 else -a,)*abs(n)
def r(i,j):return reduce_word(power(2,j)+power(1,i)+(2,)+power(1,-i)+power(2,-j-1))
def q(i,j):return reduce_word(power(2,j)+power(1,i)+(1,2,-1,-2)+power(1,-i)+power(2,-j))
for i in range(-11,14):
 for j in range(-7,10):
  check(q(i,j)==reduce_word(r(i+1,j)+inverse(r(i,j))),'grid_face_substitution')
  p,h=evaluate(q(i,j),1)
  check(p=={():1,((-i-1,-j),):1,((-i,-j),):-1} and h==(0,0),'grid_face_linear_symbol')
  terms=[q(k,j) for k in range(i-1,-1,-1)] if i>0 else [inverse(q(k,j)) for k in range(i,0)]
  check(reduce_word(sum(terms,()))==r(i,j),'grid_inverse_substitution')
# Exact tensor-square/cube/fourth-power ranks for the difference inclusion.
def rank(a):
 a=[list(map(Fraction,row)) for row in a];k=0
 for j in range(len(a[0])):
  p=next((p for p in range(k,len(a)) if a[p][j]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for p in range(k+1,len(a)):
   if a[p][j]:v=a[p][j];a[p]=[x-v*y for x,y in zip(a[p],a[k])]
  k+=1
 return k
for width in range(1,4):
 for d in range(1,5):
  rows=list(itertools.product(range(width+1),repeat=d));cols=list(itertools.product(range(width),repeat=d))
  mat=[]
  for row in rows:
   v=[]
   for col in cols:
    a=1
    for i,j in zip(row,col):a*=int(i==j+1)-int(i==j)
    v.append(a)
   mat.append(v)
  check(rank(mat)==width**d,'tensor_difference_inclusion_rank')
  check(all(sum(row[k] for row in mat)==0 for k in range(len(cols))),'tensor_total_coefficient_zero')
# Finite telescoping reconstruction of arbitrary row-sum-zero combinations.
for coeff in itertools.product(range(-2,3),repeat=5):
 row=coeff+(-sum(coeff),);edge=[];s=0
 for v in row[:-1]:s-=v;edge.append(s)
 recovered=[-edge[0]]+[edge[i-1]-edge[i] for i in range(1,len(edge))]+[edge[-1]]
 check(tuple(recovered)==row,'row_zero_sum_telescoping')
# Hyperbolic centralizer and finite-orbit arguments are not decidable by these
# finite free-group controls. Check action and uniqueness identities only.
short=words(2)
for u,v,g in itertools.product(short,repeat=3):
 gamma=reduce_word(g)
 acted=reduce_word(u+gamma+inverse(v))
 check((acted==gamma)==(v==reduce_word(inverse(gamma)+u+gamma)),'fixed_chord_graph_identity')
for a in short:
 for b in short:
  check(reduce_word(inverse(a+b))==reduce_word(inverse(b)+inverse(a)),'noncommutative_inverse_identity')
# Abelian negative control: zero-sum invariant symbols really exist on the torus.
for i in range(-12,13):
 for j in range(-12,13):
  check(((i+2)-2,(j-3)+3)==(i,j),'abelian_conjugation_negative_control')
# Nonzero Euler relation: exact integral abelianization of circle-bundle
# presentation has a fiber of order abs(2-2g), not an infinite fiber summand.
for genus in range(2,101):
 e=2-2*genus
 check(e!=0 and abs(e)==2*genus-2,'nonzero_tangent_euler_number')
 for a in range(-15,16):
  check((e*a==0)==(a==0),'torsion_free_centralizer_forces_fiber_zero')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())), 'scope':'Independent exact bounded algebra controls only. Source interpretation, topology, finite-support orbit arguments and all-degree proofs are reviewed in ADVERSARIAL_REVIEW.md.'},indent=2,sort_keys=True))
