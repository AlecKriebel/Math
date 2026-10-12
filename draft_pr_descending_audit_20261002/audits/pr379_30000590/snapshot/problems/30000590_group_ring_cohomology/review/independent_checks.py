#!/usr/bin/env python3
"""Independent exact controls; imports no author checker."""
from itertools import permutations,product
from collections import defaultdict
from math import gcd
import random,json
rng=random.Random(300005907)
counts={k:0 for k in ['finite_index','prism','height_support','tor_bockstein','nonsplit_lifts','hnn_fox','free_group_shifts','orbit_coinvariants']}
def check(v,k):
 assert v,k
 counts[k]+=1
def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):return tuple(p.index(i) for i in range(len(p)))
G=list(permutations(range(4)));one=tuple(range(4));H=[g for g in G if g[3]==3]
# S4, nonnormal index-four point stabilizer. Pairing at all group elements.
check(any(mul(mul(g,h),inv(g)) not in H for g in G for h in H),'finite_index')
def phi(a,g):
 z=mul(g,a);return z if z in H else None
for a in G:
 check(sum(phi(a,g) is not None for g in G)==len(H),'finite_index')
 for g in G:
  for h in H:
   lhs=phi(mul(a,h),g);v=phi(a,g)
   check(lhs==(None if v is None else mul(v,h)),'finite_index')
  for k in G[::3]:
   check(phi(mul(k,a),g)==phi(a,mul(g,k)),'finite_index')
# Unnormalized homogeneous prism: different random tuples and cyclic groups.
def clean(d):return {x:a for x,a in d.items() if a}
def boundary(d):
 out=defaultdict(int)
 for x,a in d.items():
  for i in range(len(x)):out[x[:i]+x[i+1:]]+=a*(-1)**i
 return clean(out)
def prism(d,n,mod):
 out=defaultdict(int)
 for x,a in d.items():
  for i in range(len(x)):
   y=x[:i+1]+tuple((v+n)%mod for v in x[i:])
   out[y]+=a*(-1)**i
 return clean(out)
for mod in [3,5,7,10]:
 for q in range(5):
  for _ in range(70):
   x=tuple(rng.randrange(mod) for _ in range(q+1));n=rng.randrange(mod)
   lhs=defaultdict(int,boundary(prism({x:1},n,mod)))
   if q:
    for y,c in prism(boundary({x:1}),n,mod).items():lhs[y]+=c
   else:
    # Augmented degree -1 prism is zero; boundary of an edge already gives result.
    pass
   rhs=defaultdict(int);rhs[tuple((v+n)%mod for v in x)]+=1;rhs[x]-=1
   check(clean(lhs)==clean(rhs),'prism')
# Noninjective shift transports, no periodic wrap-around allowed.
for width in range(1,7):
 for _ in range(120):
  low=rng.randrange(-8,2);high=low+rng.randrange(1,8)
  vec={k:[rng.randrange(-3,4) for _ in range(width)] for k in range(low,high+1)}
  vec={k:v for k,v in vec.items() if any(v)}
  if not vec:continue
  mat=[[rng.randrange(-1,2) if j<width-1 else 0 for j in range(width)] for i in range(width)]
  out={k:list(v) for k,v in vec.items()}
  for k,v in vec.items():
   w=[sum(mat[i][j]*v[j] for j in range(width)) for i in range(width)]
   out.setdefault(k+1,[0]*width)
   out[k+1]=[a-b for a,b in zip(out[k+1],w)]
  check(out[min(vec)]==vec[min(vec)] and any(out[min(vec)]),'height_support')
# Integral tensor-complex gcd and fixed-modulus kernel cardinalities.
for a in range(1,61):
 for b in range(1,41):
  g=gcd(a,b);v=(a//g,b//g)
  check(-b*v[0]+a*v[1]==0 and (g*v[0],g*v[1])==(a,b),'tor_bockstein')
  check(sum((a*j)%b==0 for j in range(b))==g,'tor_bockstein')
# Nonsplit cyclic extension Z/16 -> Z/4 with N=4Z/16.
# Regular right G module M=Z[G] restricted to N tests balanced quotient formulas.
mod=16;Ns=[0,4,8,12]
# In a tensor m_basis tensor h, reduction picks h mod4 and transfers N to m.
def balance(m,h):
 r=h%4;n=(h-r)%16
 return ((m+n)%16,r)
def F(q,m,lift=None):
 l=q if lift is None else lift
 return balance((m-l)%16,l)
for q,m,g in product(range(4),range(16),range(16)):
 base=F(q,m)
 for n in Ns:check(F(q,m,(q+n)%16)==base,'nonsplit_lifts')
 # F intertwines right G action (q,m)g=(q+g,m+g).
 rhs=F((q+g)%4,(m+g)%16)
 left=balance(base[0],base[1]+g)
 check(left==rhs,'nonsplit_lifts')
# Fox transport identity inside an exact affine model of BS(1,m).
from fractions import Fraction as F
for mm in range(1,13):
 def gm(g,h):return (g[0]+F(mm)**(-g[1])*h[0],g[1]+h[1])
 def grmul(A,B):
  out=defaultdict(int)
  for g,a in A.items():
   for h,b in B.items():out[gm(g,h)]+=a*b
  return clean(out)
 ident=(F(0),0);aa=(F(1),0);tt=(F(0),1)
 S={(F(j),0):1 for j in range(mm)}
 am={aa:1,ident:-1}
 left=grmul(grmul({tt:1},S),am)
 right=grmul(am,{tt:1})
 for _ in range(50):
  h=(F(rng.randrange(-20,21),mm**rng.randrange(0,4)),rng.randrange(-5,6))
  check(grmul(left,{h:1})==grmul(right,{h:1}),'hnn_fox')
# Free-word normal forms in the two separate free groups.
def reduce(w):
 st=[]
 for a in w:
  if st and st[-1]==-a:st.pop()
  else:st.append(a)
 return tuple(st)
def pw(a,n):return (a,)*n if n>=0 else (-a,)*(-n)
def U(i):return reduce(pw(1,i)+(2,)+pw(1,-i-1))
def V(i):return reduce(pw(3,i)+(4,)+pw(3,-i-1))
for i in range(-40,41):
 check(reduce((1,)+U(i)+(-1,))==U(i+1),'free_group_shifts')
 check(reduce((-3,)+V(i)+(3,))==V(i-1),'free_group_shifts')
 check(sum(1 if x>0 else -1 for x in U(i))==0,'free_group_shifts')
for s in range(-25,26):
 for i in range(-20,21):
  j=s-i
  check((i+1)+(j-1)==s,'orbit_coinvariants')
# Explicit finite telescoping reconstruction on an orbit, not an infinite-support inference.
for _ in range(400):
 d={i:rng.randrange(-4,5) for i in range(-12,13)};d[13]=-sum(d.values())
 running=0;coef={}
 for i in range(-12,13):
  running+=d[i];coef[i]=running
 reconstructed=defaultdict(int)
 for i,c in coef.items():
  reconstructed[i]+=c;reconstructed[i+1]-=c
 check(all(reconstructed[i]==d[i] for i in range(-12,14)),'orbit_coinvariants')
print(json.dumps({'exact_assertions':sum(counts.values()),'categories':counts,'imports_author_code':False,'infinite_claims_established_by_finite_controls':False},indent=2))
