"""Recompute every bounded rank and the additional exact controls.
Run: python3 -B verify.py
The program writes nothing; stdout is deterministic JSON.
"""
import itertools,json,math,sys
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
if not __debug__:
 raise RuntimeError('Run without -O: exact verification uses assertions.')
from pbw_algebra import add,mul,bracket,pbw,words,vwords,neck,check
COUNTS=defaultdict(int)
def demand(ok,kind):
 if not ok:raise AssertionError(kind)
 COUNTS[kind]+=1

def deletion(p,a):
 r=defaultdict(int)
 for w,z in p.items():
  for k,b in enumerate(w):
   if b==a:r[w[:k]+w[k+1:]]+=z
 return {w:z for w,z in r.items() if z}
def multi(c):
 r=math.factorial(sum(c))
 for x in c:r//=math.factorial(x)
 return r

def dimensions(c):
 v=0
 for bits in itertools.product((0,1),repeat=len(c)):
  cc=tuple(x-b for x,b in zip(c,bits))
  if min(cc)>=0:v+=(-1)**sum(bits)*multi(cc)
 demand(len(vwords(c))==v,'PBW dimension')

def sign(w):return (-1)**sum(w[i]>w[j] for i in range(len(w)) for j in range(i+1,len(w)))
def alternating(n):
 om={w:sign(w) for w in words((1,)*n)}
 for a in range(n):demand(not deletion(om,a),'alternating deletion')
 cyc=defaultdict(int)
 for w,z in om.items():cyc[neck(w)]+=z
 demand(not any(cyc.values()),'alternating cyclic zero')
 pair=sum(z*math.prod(1 if w.index(a)<w.index(a+1) else -1 for a in range(0,n,2)) for w,z in om.items())
 demand(pair==2**(n//2)*math.factorial(n//2),'alternating area pairing')
 return {'degree':n,'pairing':pair}

def sparse_product(a,b):
 out=defaultdict(int);byrow=defaultdict(list)
 for (r,c),x in b.items():byrow[r].append((c,x))
 for (r,k),x in a.items():
  for c,y in byrow[k]:out[(r,c)]+=x*y
 return {k:v for k,v in out.items() if v}
def comm(a,b):return add(sparse_product(a,b),sparse_product(b,a),-1)
def matrix_control(m):
 basis=[()]
 for n in range(1,m+1):basis.extend(itertools.product(range(2),repeat=n))
 ix={w:i for i,w in enumerate(basis)};A=[]
 for a in range(2):
  mat={}
  for w in basis:
   if len(w)<m:
    i,j=ix[(a,)+w],ix[w];mat[(i,j)]=mat[(j,i)]=1
  A.append(mat)
 P=A[1];poly={(1,):1}
 for _ in range(m-1):P=comm(A[0],P);poly=add(mul({(0,):1},poly),mul(poly,{(0,):1}),-1)
 eps=(-1)**(m-1)
 demand(P=={(c,r):eps*x for (r,c),x in P.items()},'trace transpose parity')
 top={w:P.get((ix[w],0),0) for w in basis if len(w)==m};top={w:x for w,x in top.items() if x}
 demand(top==poly,'trace top component')
 tr=sum(x*P.get((c,r),0) for (r,c),x in P.items());norm=sum(x*x for x in P.values())
 demand(tr==eps*norm and tr!=0,'trace square nonzero')
 return {'m':m,'matrix_size':len(basis),'trace_square':tr,'squared_norm':norm}

def path_signature(segments,N):
 r={():F(1)}
 for a,sgn in segments:
  s={(a,)*k:F(sgn**k,math.factorial(k)) for k in range(N+1)}
  r={w:z for w,z in mul(r,s).items() if len(w)<=N}
 return r

def path_control(m):
 seg=[(0,1),(1,1),(0,-1),(1,-1)]
 poly=add(mul({(0,):1},{(1,):1}),mul({(1,):1},{(0,):1}),-1)
 for j in range(2,m):
  seg=[(0,1)]+seg+[(0,-1)]+[(a,-s) for a,s in reversed(seg)]
  poly=add(mul({(0,):1},poly),mul(poly,{(0,):1}),-1)
 sig=path_signature(seg,m)
 demand(all(z==0 for w,z in sig.items() if 0<len(w)<m),'commutator path lower zero')
 demand({w:z for w,z in sig.items() if len(w)==m}==poly,'commutator path leading term')
 demand(poly[(0,)*(m-1)+(1,)]==1,'commutator path nontrivial')
 demand(all(sum(s for a,s in seg if a==b)==0 for b in (0,1)),'commutator path closed')
 return {'m':m,'segments':len(seg),'leading_nonzero_coefficients':len(poly)}

def run():
 out={'multilinear':[],'binary':[],'alternating':[],'trace':[],'paths':[]}
 for n in range(2,9):
  c=(1,)*n;dimensions(c)
  if n<=6:
   for w in vwords(c):
    for a in range(n):demand(not deletion(pbw(w),a),'PBW deletion')
  row=check(c);out['multilinear'].append(row)
  demand(row['linear_cyclic_defect']==(1 if n%2==0 else 0),'multilinear defect')
 for n in range(2,14):
  for a in range(n+1):
   c=(a,n-a);dimensions(c);row=check(c);out['binary'].append(row)
   demand(row['linear_cyclic_defect']==(1 if c==(1,1) else 0),'binary defect')
 for n in (2,4,6,8):out['alternating'].append(alternating(n))
 for m in range(2,7):
  out['trace'].append(matrix_control(m));out['paths'].append(path_control(m))
 # Negative controls distinguish the commutator convention and the parity rule.
 demand(bool(deletion({(0,1,2):1},0)),'negative nonconstant deletion')
 demand(sign((1,0))==-1 and sign((0,1))==1,'negative permutation sign')
 out['explicit_control_counts']=dict(sorted(COUNTS.items()))
 out['rank_cases']=len(out['multilinear'])+len(out['binary'])
 out['status']='PASS_BOUNDED_PARTIALS_NOT_FULL_CONJECTURE'
 return out
if __name__=='__main__':
 result=run();expected=json.loads(Path(__file__).with_name('EXPECTED_RESULTS.json').read_text())
 if result!=expected:raise AssertionError('Exact result differs from frozen expectation')
 print(json.dumps(result,sort_keys=True,indent=2))
