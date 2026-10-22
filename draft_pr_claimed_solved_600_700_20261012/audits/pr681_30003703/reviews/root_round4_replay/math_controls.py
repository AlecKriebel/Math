#!/usr/bin/env python3
"""Independent round4 arithmetic; no candidate imports, files or transports."""
import hashlib,itertools,json,random

def need(c,m):
 if not c:raise RuntimeError(m)
checks=[]
def check(m,c):need(c,m);checks.append(m)
def add(a,b,sign=1):
 r=dict(a)
 for w,c in b.items():r[w]=r.get(w,0)+sign*c
 return {w:c for w,c in r.items()if c}
def mul(a,b,N=99):
 r={}
 for u,c in a.items():
  for v,d in b.items():
   if len(u+v)<=N:r[u+v]=r.get(u+v,0)+c*d
 return {w:c for w,c in r.items()if c}
def br(a,b):return add(mul(a,b),mul(b,a),-1)
def inv(w):return tuple(-i for i in w[::-1])
def comm(a,b):return a+b+inv(a)+inv(b)
x,y,z=(1,),(2,),(3,);xy=comm(x,y)
w=comm(comm(xy,comm(x,z)),x);v=comm(comm(xy,comm(x,xy)),x)
X,Y,Z={x:1},{y:1},{z:1}
P=br(br(br(X,Y),br(X,Z)),X);Q=br(br(br(X,Y),br(X,br(X,Y))),X)
def magnus(w,N):
 out={():1}
 for i in w:
  factor={():1,(i,):1}if i>0 else{(-i,)*k:(-1)**k for k in range(N+1)}
  out=mul(out,factor,N)
 return out
for name,word,N,p,target,c in [('w',w,5,P,(1,1,2,1,3),-1),('v',v,6,Q,(1,1,1,2,1,2),1)]:
 check(name+'_all_Magnus_coefficients_through_leading_degree',magnus(word,N)==add({():1},p))
 check(name+'_no_lower_degree_terms',magnus(word,N-1)=={():1})
 check(name+'_decisive_integral_coefficient',p[target]==c)
 check(name+'_inverse_Magnus_leading_sign',magnus(inv(word),N)==add({():1},p,-1))
 check(name+'_nonzero_integer_doubled_word',magnus(word+word,N)==add({():1},p,2))
# Matrices over Z/4[epsilon]/epsilon^2: includes nilpotents, zero divisors, and
# characteristic four. Deterministic finite samples supplement universal CH.
zero=(0,0)
def ra(a,b):return((a[0]+b[0])%4,(a[1]+b[1])%4)
def rn(a):return((-a[0])%4,(-a[1])%4)
def rm(a,b):return(a[0]*b[0]%4,(a[0]*b[1]+a[1]*b[0])%4)
def mm(a,b):return[[ra(rm(a[i][0],b[0][j]),rm(a[i][1],b[1][j]))for j in range(2)]for i in range(2)]
def mb(a,b):
 c,d=mm(a,b),mm(b,a)
 return[[ra(c[i][j],rn(d[i][j]))for j in range(2)]for i in range(2)]
def poly(a,b,c):return mb(mb(mb(a,b),mb(a,c)),a)
rg=random.Random(68130003703);samples=[]
for i in range(1024):
 a,b,c=[[[ (rg.randrange(4),rg.randrange(4))for j in range(2)]for k in range(2)]for q in range(3)]
 need(poly(a,b,c)==[[zero,zero],[zero,zero]],'dual-ring P sample')
 need(poly(a,b,mb(a,b))==[[zero,zero],[zero,zero]],'dual-ring Q sample')
 samples.append([a,b,c])
check('1024_P_and_Q_samples_over_nonreduced_characteristic4_ring',True)
# An unrelated, changed outer matrix has no universal vanishing property.
h=[[(1,0),zero],[zero,(3,0)]];e=[[zero,(1,0)],[zero,zero]];f=[[zero,zero],[(1,0),zero]]
# characteristic four kills this usual -8 witness; use exact integers instead.
def im(a,b):return[[sum(a[i][k]*b[k][j]for k in range(len(a)))for j in range(len(a))]for i in range(len(a))]
def ib(a,b):
 c,d=im(a,b),im(b,a);return[[c[i][j]-d[i][j]for j in range(len(a))]for i in range(len(a))]
H=[[1,0],[0,-1]];E=[[0,1],[0,0]];F=[[0,0],[1,0]]
check('changed_outer_variable_fails_integrally',ib(ib(ib(H,E),ib(H,F)),E)==[[0,-8],[0,0]])
def eye(n):return[[int(i==j)for j in range(n)]for i in range(n)]
def ii(a):
 n=len(a);I=eye(n);d=[[a[i][j]-I[i][j]for j in range(n)]for i in range(n)];p=I;out=eye(n)
 for k in range(1,n):
  p=im(p,d);out=[[out[i][j]+(-1)**k*p[i][j]for j in range(n)]for i in range(n)]
 need(im(a,out)==im(out,a)==I,'two-sided integer inverse');return out
for name,word,target,c,rank in [('w',w,(1,1,2,1,3),-1,3),('v',v,(1,1,1,2,1,2),1,2)]:
 n=len(target)+1;m=[eye(n)for j in range(rank)]
 for j,col in enumerate(target):m[col-1][j][j+1]=1
 out=eye(n);mi=[ii(a)for a in m]
 for letter in word:out=im(out,m[letter-1]if letter>0 else mi[-letter-1])
 expected=eye(n);expected[0][-1]=c
 check(name+'_complete_untruncated_unitriangular_witness',out==expected)
 # Mod 2 retains these odd coefficients; no rational-isolator weakening.
 check(name+'_integral_witness_remains_nonzero_mod2',out[0][-1]%2==1)
check('P_full_free_polynomial_has_12_terms',len(P)==12)
check('Q_full_free_polynomial_has_10_terms',len(Q)==10)
print(json.dumps({'schema':'pr681-round4-math-controls-v1','status':'PASS','count':len(checks),'checks':checks,'new_nonreduced_ring_samples':1024,'sample_sha256':hashlib.sha256(json.dumps(samples,sort_keys=True).encode()).hexdigest(),'leading_P':[[list(k),c]for k,c in sorted(P.items())],'leading_Q':[[list(k),c]for k,c in sorted(Q.items())],'candidate_code_imported':False,'universal_proof_recorded_separately':True,'positive_characteristic_filtration_claim':False},indent=2,sort_keys=True))
