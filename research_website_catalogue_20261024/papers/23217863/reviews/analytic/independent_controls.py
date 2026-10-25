"""Bounded exact diagnostics; not an infinite-dimensional cohomology proof."""
from itertools import product
from collections import Counter
from fractions import Fraction
import random,json,math,time
from pathlib import Path
start=time.monotonic(); rng=random.Random(23217863)
Z=(0j,)*4
pairs=((0,0),(0,1),(1,0),(1,1))
def matadd(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def star(a):return tuple(a[j*2+i].conjugate() for i,j in pairs)
def mul(a,b):return tuple(sum(a[i*2+k]*b[k*2+j] for k in range(2)) for i,j in pairs)
B=[tuple(complex(int(j==i)) for j in range(4)) for i in range(4)]
def df(f,n,args,wrong=False):
 out=mul(B[args[0]],f(args[1:]))
 for j in range(1,n if wrong else n+1):
  x=mul(B[args[j-1]],B[args[j]])
  if any(x):out=matadd(out,scale((-1)**j,f(args[:j-1]+(x.index(1+0j),)+args[j+1:])))
 out=matadd(out,scale((-1)**(n if wrong else n+1),mul(f(args[:-1]),B[args[-1]])))
 return out
reversal_checks=0; wrong_sign_detected=0; d2checks=0; wrong_d2_detected=0
for n in range(1,5):
 data={a:tuple(complex(rng.randrange(-2,3),rng.randrange(-2,3))for _ in range(4))for a in product(range(4),repeat=n)}
 f=lambda a:data[a]
 sf=lambda a:scale((-1)**((n-1)*(n-2)//2),star(f(tuple((x%2)*2+x//2 for x in reversed(a)))))
 for a in product(range(4),repeat=n+1):
  lhs=df(sf,n,a);rhs=scale((-1)**(n*(n-1)//2),star(df(f,n,tuple((x%2)*2+x//2 for x in reversed(a)))))
  if lhs!=rhs:raise RuntimeError(('S failure',n,a,lhs,rhs))
  reversal_checks+=1
  naive=lambda b:star(f(tuple((x%2)*2+x//2 for x in reversed(b))))
  naive_rhs=star(df(f,n,tuple((x%2)*2+x//2 for x in reversed(a))))
  wrong_sign_detected+=int(df(naive,n,a)!=naive_rhs)
 if n<=2:
  for a in product(range(4),repeat=n+2):
   if df(lambda b:df(f,n,b),n+1,a)!=Z:raise RuntimeError('d2 failure')
   d2checks+=1
   wrong_d2_detected+=int(df(lambda b:df(f,n,b,True),n+1,a,True)!=Z)
# Central homotopy, A=M2 direct-sum C and output module zA=M2.
AB=B+[Z]; scalar=lambda i:int(i==4)
def abmul(i,j):
 if i==4 or j==4:return 4 if i==j==4 else None
 v=mul(B[i],B[j]);return v.index(1+0j)if any(v)else None
def cd(f,n,a):
 out=mul(AB[a[0]],f(a[1:]))
 for j in range(1,n+1):
  v=abmul(a[j-1],a[j]);
  if v is not None:out=matadd(out,scale((-1)**j,f(a[:j-1]+(v,)+a[j+1:])))
 return matadd(out,scale((-1)**(n+1),mul(f(a[:-1]),AB[a[-1]])))
def J(f,n,a):
 if n<2:return Z
 out=Z
 for i in range(n-1):
  if any(x==4 for x in a[:i])or a[i]!=4:continue
  out=matadd(out,scale((-1)**(i+1),f(a[:i]+(4,4)+a[i+1:])))
 return out
central_checks=0; omitted_J_detected=0
for n in range(1,6):
 data={a:tuple(complex(rng.randrange(-2,3),rng.randrange(-2,3))for _ in range(4))for a in product(range(5),repeat=n)}
 f=lambda a:data[a]
 for a in product(range(5),repeat=n):
  lhs=J(lambda b:cd(f,n,b),n+1,a)
  if n>=2:lhs=matadd(lhs,cd(lambda b:J(f,n,b),n-1,a))
  rhs=Z if 4 not in a else f(a)
  if lhs!=rhs:raise RuntimeError(('central identity',n,a,lhs,rhs))
  central_checks+=1;omitted_J_detected+=int(rhs!=Z)
# Rational exact transport and associativity on M2 using SymPy rational arithmetic.
import sympy as s
bas=[s.Matrix(2,2,lambda x,y:s.Integer(int(x*2+y==i)))for i in range(4)]
weights=[s.Rational(21,20),s.Rational(51,50),s.Rational(51,50),s.Rational(31,30)]
hweights=[s.Rational(1,13),s.Rational(1,17),s.Rational(1,17),s.Rational(1,19)]
def lin(X,w):return s.Matrix(2,2,lambda i,j:X[i,j]*w[i*2+j])
def mu(X,Y):return lin(lin(X,weights)*lin(Y,weights),[1/w for w in weights])
def delta(X,Y):return mu(X,Y)-X*Y
def h(X):return lin(X,hweights)
def dh(X,Y):return X*h(Y)-h(X*Y)+h(X)*Y
def g(X):return X+h(X)
def b(X):return lin(X,[1/(1+w)for w in hweights])
transport=associativity=0
for X,Y in product(bas,repeat=2):
 lhs=g(mu(b(X),b(Y)))-X*Y
 U,V=b(X),b(Y);rhs=delta(U,V)-dh(U,V)+h(delta(U,V))-h(U)*h(V)
 if lhs!=rhs:raise RuntimeError('transport')
 transport+=1
 for W in bas:
  if mu(mu(X,Y),W)!=mu(X,mu(Y,W)):raise RuntimeError('association')
  if X*delta(Y,W)-delta(X*Y,W)+delta(X,Y*W)-delta(X,Y)*W!=delta(delta(X,Y),W)-delta(X,delta(Y,W)):raise RuntimeError('MaurerCartan')
  associativity+=1
# Upstream distinct-surviving-word mechanism and Catalan leading counts.
def red(seq):
 out=[]
 for x in seq:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
block_cases=block_terms=0
for ds in ((0,),(1,),(2,),(3,),(0,0),(1,0),(0,1),(1,1),(2,0),(1,0,1)):
 signs=tuple(x for d in ds for x in (1,)+(-1,1)*d);L=len(signs)
 for r in range(1,5):
  counts=Counter(red(tuple(j*sgn for j,sgn in zip(js,signs)))for js in product(range(1,r+1),repeat=L));block_terms+=r**L
  for w,c in counts.items():
   if not w or w[0]<0 or w[-1]<0:raise RuntimeError('block endpoints')
   if c>3**L*r**((L-len(w))//2):raise RuntimeError('coefficient bound')
  for q in range(2,L+1):
   numer=sum(c*c for w,c in counts.items()if len(w)==q and len(set(map(abs,w)))<q)
   if Fraction(numer,r**L)>Fraction(3**(2*L)*2**q*math.comb(q,2),r):raise RuntimeError('repeated index bound')
  block_cases+=1
catalan_cases=0
for d in range(1,6):
 signs=(-1,1)*d;cat=math.comb(2*d,d)//(d+1)
 for r in range(1,5 if d<=4 else 4):
  leading=0;total=0
  for js in product(range(1,r+1),repeat=2*d):
   if not red(tuple(a*b for a,b in zip(js,signs))):
    total+=1;leading+=int(len(set(js))==d)
  falling=math.prod(range(r-d+1,r+1))if r>=d else 0
  if leading!=cat*falling:raise RuntimeError('Catalan leading')
  catalan_cases+=1
rank_cases=0;rank_solutions=[]
for n in range(3,32,2):
 for m in range(1,40):
  for qrank in range(m+1):
   if 0<qrank<m and m-qrank==1 and qrank==n-1:
    if m!=n:raise RuntimeError('odd reconstruction')
    rank_solutions.append((n,m,qrank))
   rank_cases+=1
# Noncommuting ordered polynomial negative control in the free group ring.
def pmul(A,B):
 C=Counter()
 for a,x in A.items():
  for b,y in B.items():C[red(a+b)]+=x*y
 return +C
def padj(A):return Counter({tuple(-x for x in reversed(w)):c for w,c in A.items()})
p=Counter({(1,):1,(2,):1});A=pmul(padj(p),p)
ordered=pmul(pmul(p,A),pmul(p,A));commuted=pmul(pmul(p,p),pmul(A,A))
if ordered==commuted:raise RuntimeError('failed ordered negative control')
res={'status':'ALL_POSITIVE_IDENTITIES_CHECKED_NEGATIVE_CONTROLS_DETECTED','scope_limit':'Exact finite diagnostics supplement universal proofs; do not establish H2/H3 or an all-vNa theorem. Gaussian integer matrix additions/multiplications use exactly represented values; no operation approaches 2^53. Rational identities use SymPy Rational.','S_commutation_basis_checks':reversal_checks,'naive_reversal_without_sign_failures':wrong_sign_detected,'d_squared_checks':d2checks,'malformed_Roydor_printed_d_squared_failures':wrong_d2_detected,'central_homotopy_M2_plus_C_basis_checks':central_checks,'uncorrected_mixed_input_failures':omitted_J_detected,'rational_transport_basis_checks':transport,'rational_associativity_and_Maurer_Cartan_checks':associativity,'upstream_ordered_block_cases':block_cases,'block_original_terms_examined':block_terms,'catalan_leading_counts_cases':catalan_cases,'odd_rank_cases':rank_cases,'odd_rank_solutions':rank_solutions,'noncommuting_ordered_power_negative_control':True,'elapsed_seconds':time.monotonic()-start}
Path('independent-controls-results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
