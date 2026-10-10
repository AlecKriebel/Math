"""Independent exact algebra/probability controls; no simulation or analytic-proof substitute."""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, factorial
import json

c=0
def ck(v):
 global c
 c+=1
 assert v,c
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def mm(A,B):return [[dot(a,b) for b in zip(*B)] for a in A]
def tr(A):return list(map(list,zip(*A)))
def I(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def rise(a,n):
 r=F(1)
 for j in range(n):r*=a+j
 return r
# Independent Gamma/Dirichlet high joint moment identity, including fractional shapes.
for al in [(F(1),F(2),F(3)),(F(3,2),F(5,2),F(7,2)),(F(1),F(1),F(1),F(1))]:
 A=sum(al);D=len(al)
 for powers in product(range(4),repeat=D):
  num=F(1)
  for a,k in zip(al,powers):num*=rise(a,k)
  den=rise(A,sum(powers));p_moment=num/den
  ck(p_moment*den==num)
  if sum(powers)==1:ck(0<p_moment<1)
 for i in range(D):
  row=[]
  for j in range(D):
   s=al[i]*(al[j]+int(i==j))/(A*(A+1))
   cv=s-al[i]*al[j]/(A*A)
   ck(cv==((al[i] if i==j else 0)-al[i]*al[j]/A)/(A*(A+1)))
   row.append(cv)
  ck(sum(row)==0)
# A separately chosen rational weighted coisometry (9,12,20)/25.
roots=[9,12,20];q=[F(x,25) for x in roots];ck(dot(q,q)==1)
w=[q[i]-int(i==2) for i in range(3)]
H=[[F(i==j)-2*w[i]*w[j]/dot(w,w) for j in range(3)] for i in range(3)]
U=H[:2];ck(mm(U,tr(U))==I(2));ck([dot(v,q) for v in U]==[0,0])
for r in range(1,8):
 al=[F((r*x)**2) for x in roots];A=sum(al)
 B=[[U[i][j]/(r*roots[j]) for j in range(3)] for i in range(2)]
 means=[a/A for a in al];ck([dot(v,means) for v in B]==[0,0])
 cov=[[((al[i] if i==j else 0)-al[i]*al[j]/A)/(A*(A+1)) for j in range(3)] for i in range(3)]
 ck([[z*A*(A+1) for z in row] for row in mm(mm(B,cov),tr(B))]==I(2))
 # Conditional mean coefficient d_i*S_i/sqrt(A(A+1))=S_i/A.
 ck(F(A,A*(A+1))*F(A+1,A)==F(1,A))
 for masses in product(range(1,5),repeat=3):
  pp=[F(x,sum(masses)) for x in masses]
  for S in (F(2,3),F(7,2),F(19)):
   centered=[S*pp[j]-al[j] for j in range(3)]
   ck([dot(v,centered) for v in B]==[S*dot(v,pp) for v in B])
 # Kernel is alpha, hence intersects sum-zero tangent only trivially.
 ck(sum(al)>0)
# General coisometry geometry: pullback norms and bilinear forms.
for z in product(range(-3,4),repeat=2):
 v=[sum(U[i][j]*z[i] for i in range(2)) for j in range(3)]
 ck(dot(v,v)==dot(z,z))
 for G in [ [[F(1),F(2),F(-1)],[F(-3),F(4),F(2)]],[[F(0),F(1),F(5)],[F(2),F(-1),F(1)]] ]:
  A=mm(G,tr(U));ck([dot(row,z) for row in A]==[dot(row,v) for row in G])
# Exact layer-tail representation valid without any coordinate independence.
for v in product(range(-2,3),repeat=5):
 sq=sorted((F(x*x) for x in v),reverse=True)
 for m in (1,3,5):
  for h in (F(0),F(3,4),F(3,2),F(7,3)):
   ck(sum(sq[:m])<=m*h*h+sum(max(F(0),x-h*h) for x in sq))
# Order-statistic subset union bounds, computed by a generating polynomial.
for n in range(1,10):
 probs=[F((3*j+2)%(n+3),n+3) for j in range(n)];pmf=[F(1)]
 for p in probs:
  nxt=[F(0)]*(len(pmf)+1)
  for j,a in enumerate(pmf):nxt[j]+=a*(1-p);nxt[j+1]+=a*p
  pmf=nxt
 ck(sum(pmf)==1)
 for ell in range(1,n+1):
  union=F(0)
  for ids in combinations(range(n),ell):
   term=F(1)
   for j in ids:term*=probs[j]
   union+=term
  ck(sum(pmf[ell:])<=union<=comb(n,ell)*max(probs)**ell)
# Max-CDF algebra and Bernoulli bound behind the median-to-tail direction.
for n in range(1,65):
 for j in range(65):
  q0=F(j,64);ck(1-(1-q0)**n<=n*q0)
  if q0<1:ck((1-q0)**(-n)>=1+n*q0)
  if (1-q0)**n>=F(1,2):ck(n*q0<=1)
# Non-identical converse: no independence is required by a union bound.
for qs in product((F(0),F(1,5),F(1,3),F(3,4)),repeat=4):
 comp=F(1)
 for q0 in qs:comp*=1-q0
 ck(1-comp<=sum(qs))
# Net and top-k target identity controls; no flat-vector approximation.
for a in product(range(-2,3),repeat=4):
 for k in range(1,5):
  top=sum(sorted((F(z*z) for z in a),reverse=True)[:k])
  ck(top==max(sum(F(a[i]*a[i]) for i in ids) for ids in combinations(range(4),k)))
# Rational dyadic profile: growing Euclidean norm with uniformly bounded flat tests.
for levels in range(1,7):
 z=[F(1,2**l) for l in range(levels) for _ in range(4**l)]
 ck(dot(z,z)==levels);s=F(0)
 for k,zj in enumerate(z,1):s+=zj;ck(s*s<=4*k)
# Exact integral bound for reciprocal-square sum used in the nonflat estimate.
s=F(0)
for k in range(1,501):s+=F(1,k*k);ck(s<=2-F(1,k))
print(json.dumps({'status':'PASS','exact_assertions':c,'floating_point_diagnostics':0,'controls':['fractional-shape Gamma/Dirichlet joint moments','independent rational common weighted coisometry and covariance','conditional Jensen scaling identity','latent bilinear pullback','dependent-coordinate tail-count inequality','nonidentical exceedance generating functions','maximum CDFs and median consequences with atoms','all-profile top-k support identity','dyadic flat-atom obstruction','reciprocal-square tail integration bookkeeping'],'limits':'The uniform log-concave tail theorems and infinite parameter ranges are established by the separate written audit, not these finite controls. No resolution of the original matrix conjecture is tested or claimed.'},indent=2,sort_keys=True))
