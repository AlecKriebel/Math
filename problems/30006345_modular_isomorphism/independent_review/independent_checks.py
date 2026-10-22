"""Independent exact controls; imports no author code or author data."""
from itertools import product,permutations
from collections import Counter
import json
n=Counter()
def ck(v,k):
 assert v,k
 n[k]+=1
# Formal center-layer reconstruction with a separately written coefficient solver.
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def power(a,k):
 b=[1]
 for _ in range(k):b=mul(b,a)
 return b
def quotient_prefix(a,b,N):
 assert b[0]==1
 c=[]
 for j in range(N+1):c.append((a[j] if j<len(a) else 0)-sum(b[i]*c[j-i] for i in range(1,min(j,len(b)-1)+1)))
 return c
def parts(n,lo=1):
 if n==0:yield ()
 for i in range(lo,n+1):
  for tail in parts(n-i,i):yield (i,)+tail
for p in [3,5,7]:
 A=[1]*p;seen={}
 for rr in range(7):
  for es in parts(rr):
   for a in range(4):
    hs=[]
    for e in es:
     h=power(A,e);h[1]+=p**(2*e)-1;hs.append(h)
    L=power(A,a)
    for h in hs:L=mul(L,h)
    orderexp=a+3*rr;degree=len(L)-1;ss=degree//(p-1)
    recovered_r=(orderexp-ss)//2;recovered_a=(3*ss-orderexp)//2
    ck((recovered_r,recovered_a)==(rr,a),'center_degree_recovery')
    key=(orderexp,tuple(L));ck(key not in seen or seen[key]==(a,es),'center_parameter_uniqueness');seen[key]=(a,es)
    rem=list(reversed(L));remaining_degree=ss;ans=[]
    for e in range(1,rr+1):
     de=e*(p-1)-1;ce=p**(2*e)-1
     count=quotient_prefix(rem,power(A,remaining_degree),de)[de]//ce
     ans += [e]*count
     h=power(A,e);h[1]+=ce;h=list(reversed(h))
     for _ in range(count):
      # Exact polynomial division from the leading end, distinct from series step.
      q=[0]*(len(rem)-len(h)+1);rest=rem[:]
      for j in range(len(q)-1,-1,-1):
       q[j]=rest[j+len(h)-1]//h[-1]
       for k,v in enumerate(h):rest[j+k]-=q[j]*v
      ck(not any(rest),'center_exact_factor_removal');rem=q;remaining_degree-=e
    ck(tuple(ans)==es,'center_multiset_recovery')
# Construct H(F3) directly and verify the actual class-sum square-zero law.
p=3;elts=list(product(range(p),repeat=3))
def gm(g,h):a,b,c=g;d,e,f=h;return ((a+d)%p,(b+e)%p,(c+f+a*e)%p)
def gi(g):a,b,c=g;return((-a)%p,(-b)%p,(-c+a*b)%p)
classes={frozenset(gm(gm(h,g),gi(h)) for h in elts) for g in elts}
ck(len(classes)==11,'actual_H3_class_count')
noncentral=[C for C in classes if len(C)>1]
for C in noncentral:
 for D in noncentral:
  values=Counter(gm(g,h) for g in C for h in D)
  ck(all(c%p==0 for c in values.values()),'actual_center_square_zero')
for C in noncentral:
 for z in [(0,0,a) for a in range(p)]:ck({gm(z,g) for g in C}==set(C),'actual_center_augmentation_action')
# Exact F9 arithmetic with encoding a+3b, s^2=2.
def plus(a,b):return (a%3+b%3)%3+3*((a//3+b//3)%3)
def neg(a):return (-a)%3+3*((-(a//3))%3)
def times(a,b):u,v=a%3,a//3;x,y=b%3,b//3;return (u*x+2*v*y)%3+3*((u*y+v*x)%3)
def sub(a,b):return plus(a,neg(b))
def inv(a):return next(b for b in range(1,9) if times(a,b)==1)
def rank(M):
 M=[r[:] for r in M];rr=0
 for j in range(len(M[0])):
  pivot=next((i for i in range(rr,len(M)) if M[i][j]),None)
  if pivot is None:continue
  M[rr],M[pivot]=M[pivot],M[rr];c=inv(M[rr][j]);M[rr]=[times(c,x) for x in M[rr]]
  for i in range(len(M)):
   if i!=rr:
    c=M[i][j];M[i]=[sub(x,times(c,y)) for x,y in zip(M[i],M[rr])]
  rr+=1
  if rr==len(M):break
 return rr
def block(t,u,v):
 A=[[sub(u if i==j else 0,times(v,t[i][j])) for j in range(2)] for i in range(2)]
 return [[0,0]+A[0],[0,0]+A[1],[neg(A[0][0]),neg(A[1][0]),0,0],[neg(A[0][1]),neg(A[1][1]),0,0]]
def diag(A,B):return [r+[0]*len(B) for r in A]+[[0]*len(A)+r for r in B]
T0=[[0,2],[1,0]];T1=[[0,1],[1,2]]
Rp=Counter();Rq=Counter()
for u,v in [(a,1) for a in range(9)]+[(1,0)]:
 A=block(T0,u,v);B=block(T1,u,v);rp=rank(diag(A,A));rq=rank(diag(A,B));Rp[rp]+=1;Rq[rq]+=1
 ck(rp in [4,8] and rq in [6,8],'geometric_pencil_ranks')
ck(Rp=={4:2,8:8} and Rq=={6:4,8:6},'geometric_rank_loci_counts')
for T in [T0,T1]:
 for u,v in [(a,1) for a in range(3)]+[(1,0)]:ck(rank(block(T,u,v))==4,'rational_pencil_nonsingularity')
# Nonabelian finite component groups. Inner Frobenius actions test order/signs.
def compose(a,b):return tuple(a[i] for i in b)
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
for size in [3,4]:
 G=list(permutations(range(size)));one=tuple(range(size))
 for t in G:
  ti=inverse(t);tau=lambda x:compose(compose(t,x),ti)
  cob={compose(inverse(x),tau(x)) for x in G}
  for a in G:
   state=one;norm=one;fa=a
   for d in range(1,len(G)+1):
    state=compose(a,tau(state));norm=compose(norm,fa);fa=tau(fa)
    ck(state==norm,'nonabelian_component_norm_order')
    if state==one:break
   ck(d<=len(G) and norm==one,'nonabelian_return_bound')
   for x in G:
    changed=compose(compose(x,a),inverse(tau(x)))
    ck((a in cob)==(changed in cob),'twisted_class_basis_independence')
# Semilinear factor-swap fixed basis: all pairs of a three-dimensional model.
# This tests descent as vector spaces, independent of algebra multiplication.
for size in [2,3,5]:
 basis=[]
 for i in range(size):
  row=[0]*(size*size);row[i*size+i]=1;basis.append(row)
 for i in range(size):
  for j in range(i+1,size):
   row=[0]*(size*size);row[i*size+j]=1;row[j*size+i]=1;basis.append(row)
   row=[0]*(size*size);row[i*size+j]=3;row[j*size+i]=6;basis.append(row)
 def frob(a):return times(times(a,a),a)
 for row in basis:ck(all(row[i*size+j]==frob(row[j*size+i]) for i in range(size) for j in range(size)),'fixed_swap_basis')
 ck(rank(basis)==size*size,'fixed_swap_basis_full_rank')
print(json.dumps({'status':'PASS','assertions':sum(n.values()),'by_scope':dict(sorted(n.items())),'limits':'Finite exact controls supplement the reviewed general proofs and primary Lang/exponent/class inputs; no author search or full group-algebra collision search.'},indent=2))
