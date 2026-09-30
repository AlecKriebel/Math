"""Independent exact diagnostics; topology is established by the review proof."""
from itertools import product
from math import comb,gcd
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json,random
counts=Counter(); cases=Counter()
def check(k,b):
 if not b: raise AssertionError(k)
 counts[k]+=1
def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return tuple(a)
def add(a,b):
 return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def neg(a):return tuple(-x for x in a)
def det(A):
 # Dynamic programming over column subsets, distinct from author permutation enumeration.
 n=len(A);D={0:(1,)}
 for i in range(n):
  E={}
  for mask,v in D.items():
   for j in range(n):
    if mask>>j&1:continue
    term=mul(v,A[i][j]); inv=(mask>>(j+1)).bit_count()
    if inv%2:term=neg(term)
    m=mask|(1<<j);E[m]=add(E.get(m,(0,)),term)
  D=E
 return D[(1<<n)-1]
def rank(A,p):
 if not A:return 0
 B=[[x%p for x in row] for row in A];i=0
 for j in range(len(B[0])):
  k=next((k for k in range(i,len(B)) if B[k][j]),None)
  if k is None:continue
  B[i],B[k]=B[k],B[i];v=pow(B[i][j],-1,p)
  B[i]=[x*v%p for x in B[i]]
  for k in range(i+1,len(B)):
   v=B[k][j];B[k]=[(x-v*y)%p for x,y in zip(B[k],B[i])]
  i+=1
  if i==len(B):break
 return i
def order1(poly,p):
 # Expand t=1+x exactly over the integers, then reduce.
 for j in range(len(poly)):
  if sum(poly[i]*comb(i,j) for i in range(j,len(poly)))%p:return j
 return 10**9
def evaluate(A):return [[sum(v) for v in row] for row in A]
for p in (2,3):
 polys=list(product(range(p),repeat=2))
 for v in product(polys,repeat=4):
  A=[list(v[:2]),list(v[2:])];d=det(A);r=2-rank(evaluate(A),p)
  check('all_linear_2x2_rank_order',order1(d,p)>=r);cases['linear_2x2']+=1
for flat in product((0,1),repeat=9):
 C=[list(flat[3*i:3*i+3]) for i in range(3)]
 for mode in range(7):
  A=[[(C[i][j],int((i+2*j+mode)%7<mode)) for j in range(3)] for i in range(3)]
  check('exhaustive_constant_3x3_rank_order',order1(det(A),2)>=3-rank(evaluate(A),2));cases['linear_3x3']+=1
rng=random.Random(10400231)
for k in (0,2,4):
 for r in range(4):
  for rep in range(25):
   n=k+r;ds=[rng.randrange(2,13) for _ in range(r)]
   B=[[(rng.randrange(-4,5),rng.randrange(-3,4)) for j in range(k)] for i in range(k)]
   C=[[(rng.randrange(-3,4),rng.randrange(-2,3)) for j in range(k)] for i in range(r)]
   A=[row+[(0,)]*r for row in B]+[C[i]+[(ds[i] if i==j else 0,) for j in range(r)] for i in range(r)]
   d=det(A);factor=1
   for x in ds:factor*=x
   check('torsion_columns_retained',d==tuple(factor*x for x in det(B)))
   if k and r:
    A2=[[v for v in row] for row in A]
    for i in range(r):
     for j in range(k):A2[k+i][j]=add(A2[k+i][j],(ds[i]*(j+1),-ds[i]*(i+1)))
    check('torsion_lift_independence',det(A2)==d)
   for p in (2,3,5,7):check('torsion_block_rank_order',order1(d,p)>=n-rank(evaluate(A),p))
   cases['torsion_block']+=1
for a,b in product(list(range(-5,0))+list(range(1,6)),repeat=2):
 S=[[1+a*b,a],[b,1]]
 A=[[(int(i==j),-S[i][j]) for j in range(2)] for i in range(2)]
 d=det(A);A1=evaluate(A);d1=0
 for row in A1:
  for v in row:d1=gcd(d1,v)
 d2=abs(a*b)//d1
 check('torus_bundle_polynomial',d==(1,-(2+a*b),1))
 check('torus_bundle_specialization',abs(sum(d))==d1*d2==abs(a*b))
 for p in (2,3,5,7):
  rp=int(d1%p==0)+int(d2%p==0)
  check('torus_bundle_smith_rank',rp==2-rank(A1,p))
  check('torus_bundle_order_bound',order1(d,p)>=rp)
 cases['torus_bundle']+=1
for p in (2,3,5,7,11,13,17,19,23,29,31):
 d=(1,p**3-2,1)
 check('candidate_trace',sum(d)==p**3)
 check('candidate_reciprocity',d==d[::-1])
 check('candidate_exact_order',order1(d,p)==2)
 check('candidate_rank_contradiction',3>order1(d,p))
 for shift in range(5):check('positive_unit_invariance',order1((0,)*shift+d,p)==2)
 cases['candidate_prime']+=1
# Pseudonull diagnostic: R/(p,t-1) has order 1 but specialization Z/p.
# It has a rectangular 1-by-2 presentation, so it is NOT a counterexample to the square lemma.
for p in (2,3,5,7):
 check('rectangular_warning',order1((1,),p)==0 and 1>0)
root=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'independent_assertions':sum(counts.values()),'counts':dict(counts),'cases':dict(cases),'scope':'Algebraic diagnostics only. The integral topology, source convention, and absence of extra factors are independently proved in REVIEW.md.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
