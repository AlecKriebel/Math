from fractions import Fraction as Q
from itertools import combinations,product
from collections import defaultdict,Counter
from math import factorial,prod
import json
counts=Counter()
def ck(x,kind):
 assert x,kind
 counts[kind]+=1
def basis(rows):
 a=[[Q(x) for x in row] for row in rows];r=0
 for j in range(len(a[0])):
  z=next((i for i in range(r,len(a)) if a[i][j]),None)
  if z is None:continue
  a[z],a[r]=a[r],a[z];d=a[r][j];a[r]=[x/d for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    d=a[i][j];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return tuple(tuple(row) for row in a[:r])
def inside(v,B):return len(basis(list(B)+[v]))==len(B)
# Every generated rational subspace containing constants for dimensions <=4.
for k in range(2,5):
 cube=list(product([0,1],repeat=k));seen={basis([(1,)*k])};todo=list(seen)
 while todo:
  B=todo.pop();members=[v for v in cube if inside(v,B)]
  classes={tuple(x-v[0] for x in v) for v in members}
  ck(len(members)<=2**len(B),'cube_dimension')
  ck(len(classes)<=2**len(B)-1,'diagonal_quotient')
  for v in cube:
   C=basis(list(B)+[v])
   if C not in seen:seen.add(C);todo.append(C)
# Exact flags for every pair/triple of equal-sum subsets of [2,8].
A=list(range(2,9));fib=defaultdict(list)
for mask in range(1<<len(A)):
 B={a for j,a in enumerate(A) if mask>>j&1};fib[sum(B)].append(B)
for fiber in fib.values():
 for k in (2,3):
  for tup in combinations(fiber,k):
   ws={a:tuple(int(a in S) for S in tup) for a in A};sp=[basis([(1,)*k])];K=[];W=[]
   for a in reversed(A):
    C=basis(list(sp[-1])+[ws[a]])
    if len(C)>len(sp[-1]):K.append(a);W.append(ws[a]);sp.append(C)
   t=len(K);ck(2**t>=k,'flag_distinct_patterns')
   # Integer power-of-two rounding tests bins with ties without transcendental error.
   U=[1<<(a-1).bit_length() for a in K];remaining=set(A)-set(K)
   for j in range(t):
    low=U[j+1] if j+1<t else 0
    for a in remaining:
     if low<a<=U[j]:ck(inside(ws[a],sp[j+1]),'rounded_support')
   residual=tuple(sum(a*ws[a][i] for a in remaining) for i in range(k))
   totals=[residual[i]+sum(a*w[i] for a,w in zip(K,W)) for i in range(k)]
   ck(len(set(totals))==1,'quotient_reconstruction')
   cols=[tuple(w[i]-w[0] for i in range(1,k)) for w in W]
   ck(len(basis(cols))==t,'recorded_injectivity')
# Exact full laws and tilt moments, with deterministic first indicator.
for n in range(1,10):
 moments={q:Q(0) for q in (1,2,3)};tiltnorm={l:Q(0) for l in (Q(1,3),Q(3,2),Q(4))}
 for mask in range(1<<(n-1)):
  A={1}|{i for i in range(2,n+1) if mask>>(i-2)&1};p=prod(Q(1,i) if i in A else Q(i-1,i) for i in range(1,n+1));f={0:1}
  for a in A:
   g=f.copy()
   for s,v in f.items():g[s+a]=g.get(s+a,0)+v
   f=g
  N=len(A);S=sum(A);M=max(f.values());ck(M*(S+1)>=2**N,'pigeonhole')
  for q in moments:moments[q]+=p*M**q
  for l in tiltnorm:
   Z=prod(1+(l-1)/i for i in range(1,n+1));v=prod(l/(i+l-1) if i in A else (i-1)/(i+l-1) for i in range(1,n+1))
   ck(v==p*l**N/Z,'tilt_density');tiltnorm[l]+=v
 for v in tiltnorm.values():ck(v==1,'tilt_normalization')
 for q,v in moments.items():
  l=2**q;Z=prod(Q(i+l-1,i) for i in range(1,n+1));ck(v>=Z/(l*n+1)**q,'raw_moment_bound')
# Count every signed relation in finite ranges by its largest entry and length.
for m in range(3,11):
 actual=defaultdict(lambda:Q(0))
 for eps in product((-1,0,1),repeat=m-1):
  if m+sum((i+1)*e for i,e in enumerate(eps)):continue
  support=[i+1 for i,e in enumerate(eps) if e];ell=len(support)+1
  actual[ell]+=Q(1,m)*prod(Q(1,i) for i in support)
 H=sum(Q(1,i) for i in range(1,m))
 for ell,v in actual.items():
  bound=Q(2**(ell-1)*(ell-1),factorial(ell-2))*H**(ell-2)/m**2
  ck(v<=bound,'relation_first_moment')
# Exact summation-by-parts / coefficient maximization over exhaustive grids.
for t in range(1,6):
 h=[Q(0),Q(11,10)]+[Q(11,10)+Q(7,10)*(j-1) for j in range(2,t+1)]
 for xs in product(range(1,5),repeat=t):
  cs=sorted([Q(x,4) for x in xs],reverse=True);c=cs[-1]/2;ds=cs+[c]
  z=-sum(cs)+sum((ds[j]-ds[j+1])*h[j+1] for j in range(t))
  ck(z<=Q(1,10)-c*(t+Q(1,10)),'uniform_negative_gap_algebra')
print(json.dumps({'exact_assertions':sum(counts.values()),'categories':dict(counts),'scope':'Finite rational controls supplement the analytic review; no probabilistic limit tested'},indent=2,sort_keys=True))
