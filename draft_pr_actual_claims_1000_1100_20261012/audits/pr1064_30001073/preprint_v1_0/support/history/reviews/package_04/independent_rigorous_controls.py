"""Independent finite rational interval / formal-log controls; no floats/asserts."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations,product
from math import factorial
from pathlib import Path
import json,sys,argparse,hashlib
p=argparse.ArgumentParser();p.add_argument('--fault',default='none',choices=['none','endpoint','drop-entry-mass','drop-sequential']);a=p.parse_args()
def require(c,m):
 if not c:raise ValueError(m)
@lru_cache(None)
def logint(x):
 x=F(x);require(x>0,'positive log input');k=0
 while x<1:x*=2;k-=1
 while x>=2:x/=2;k+=1
 def series(y):
  t=(y-1)/(y+1);N=64;s=sum((2*t**(2*j+1)/F(2*j+1) for j in range(N)),F(0));tail=2*t**(2*N+1)/((2*N+1)*(1-t*t));return s,s+tail
 lo,hi=series(x);l2,u2=series(F(2))
 return (lo+k*l2,hi+k*u2) if k>=0 else (lo+k*u2,hi+k*l2)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def scale(x,k):return (x[0]*k,x[1]*k) if k>=0 else (x[1]*k,x[0]*k)
def qint(b):
 if b==0:return F(0),F(0)
 if b==1:return (F(0),F(0)) if a.fault=='endpoint' else (F(1),F(1))
 return scale(logint(b),-b*b/(1-b))
def hint(x):
 if x==0:return F(0),F(0)
 return add((x*x,x*x),scale(logint(x),-x*x))
def dint(b,x):
 if x==0:require(b==0,'support');return F(0),F(0)
 if b==0:return (F(0),F(0)) if a.fault=='drop-entry-mass' else (x,x)
 return add(scale(logint(b/x),b),(x-b,x-b))
# Rigorous e^4 enclosure: after term N, ratios <=4/(N+2).
N=64;el=sum((F(4)**j/factorial(j) for j in range(N+1)),F(0));eu=el+(F(4)**(N+1)/factorial(N+1))/(1-F(4,N+2))
scalar=[]
vals=[F(i,13) for i in range(14)]+[F(1,2**40),1-F(1,2**40)]
for x,b in product(vals,vals):
 if x==0 and b!=0:continue
 qi=qint(b);hi=hint(x);di=dint(b,x)
 slack=el*hi[0]+di[0]-qi[1]
 require(slack>=0,'rigorous scalar enclosure failed')
 scalar.append({'a':str(x),'b':str(b),'slack_lower_positive':slack>0})
require(qint(F(1))==(F(1),F(1)),'deterministic endpoint q(1)=1')
require(dint(F(0),F(2,5))==(F(2,5),F(2,5)),'positive input zero marginal retains mass')
# Formal logs reduce exact rational arguments to prime bases. Zero coefficient
# identity is an algebraic certificate independent of numerical evaluation.
def factors(n):
 d=2;out={}
 while d*d<=n:
  while n%d==0:out[d]=out.get(d,0)+1;n//=d
  d+=1
 if n>1:out[n]=out.get(n,0)+1
 return out
def term(c,x):
 if c==0:return {}
 x=F(x);out={}
 for n,s in [(x.numerator,1),(x.denominator,-1)]:
  for prime,e in factors(n).items():out[prime]=out.get(prime,F(0))+c*s*e
 return {k:v for k,v in out.items() if v}
def plus(*terms):
 out={}
 for t in terms:
  for k,v in t.items():out[k]=out.get(k,F(0))+v
 return {k:v for k,v in out.items() if v}
def times(t,k):return {p:c*k for p,c in t.items() if c*k}
A=[[F(1,2),F(1,3),F(1,6)],[F(1,5),F(3,5),F(1,5)],[F(2,7),F(1,7),F(4,7)]]
perms=list(permutations(range(3)));weights={s:A[0][s[0]]*A[1][s[1]]*A[2][s[2]] for s in perms};P=sum(weights.values());mu={s:w/P for s,w in weights.items()}
B=[[sum(w for s,w in mu.items() if s[i]==j) for j in range(3)] for i in range(3)]
H=plus(*(term(-w,w) for w in mu.values()));cross=plus(*(term(B[i][j],A[i][j]) for i,j in product(range(3),repeat=2)));Dmat=plus(*(term(B[i][j],B[i][j]/A[i][j]) for i,j in product(range(3),repeat=2)))
require(not plus(term(1,P),times(H,-1),times(cross,-1)),'formal exact Gibbs identity')
Dseq={};T={};all_orders=list(permutations(range(3)))
for order in all_orders:
 for s,w in mu.items():
  nu=F(1)
  for depth,i in enumerate(order):
   suffix=sum(B[i][s[k]] for k in order[depth:]);nu*=B[i][s[i]]/suffix;T=plus(T,term(w/len(all_orders),suffix))
  Dseq=plus(Dseq,term(w/len(all_orders),w/nu))
require(bool(Dseq) and Dseq!=Dmat,'distinct nonzero formal divergence objects')
used={} if a.fault=='drop-sequential' else Dseq
require(not plus(term(1,P),Dmat,times(T,-1),used),'formal exact sequential identity')
# Exhaustive exact permanent/norm boundary controls in a new denom-3 row family.
rows=[(F(i,3),F(j,3),F(3-i-j,3)) for i in range(4) for j in range(4-i)]
mats=0;zero=0;noncol=0;unused=0
for M in product(rows,repeat=3):
 mats+=1;weights2={s:M[0][s[0]]*M[1][s[1]]*M[2][s[2]] for s in perms};P2=sum(weights2.values());S=sum(x*x for row in M for x in row)
 require(1<=S<=3 and 0<=P2<=1,'exact stochastic range')
 if not P2:zero+=1
 if any(sum(M[i][j] for i in range(3))!=1 for j in range(3)):noncol+=1
 if P2:
  B2=[[sum(w for s,w in weights2.items() if s[i]==j)/P2 for j in range(3)] for i in range(3)]
  require(all(sum(row)==1 for row in B2),'Gibbs rows');require(all(sum(B2[i][j] for i in range(3))==1 for j in range(3)),'Gibbs columns')
  unused+=sum(M[i][j]>0 and B2[i][j]==0 for i,j in product(range(3),repeat=2))
# Exact n=1 counterexample to the prefactor-free form: exp(-1)<1, since exp(1)>1.
require(sum(F(1,factorial(j)) for j in range(2))>1,'n1 pure power false')
report={'pass':True,'scope':'Finite exact rational arithmetic and rigorously bounded rational log/exp series, plus formal prime-log identities; not universal numerical certification. The frozen analytic derivation supplies all-n proof.','fault':a.fault,'scalar_pairs':len(scalar),'rational_log_series_terms':64,'rational_log_range_reduction':'powers of two to [1,2), atanh positive series with geometric tail','rational_exp4_tail':'Taylor through degree 64, positive geometric tail','scalar_results':scalar,'formal_gibbs_residual':{},'formal_sequential_residual':{},'Dmat_prime_log_coefficients':{str(k):str(v) for k,v in Dmat.items()},'Dseq_prime_log_coefficients':{str(k):str(v) for k,v in Dseq.items()},'denom3_order3_stochastic_matrices':mats,'zero_permanent':zero,'noncolumn_stochastic':noncol,'positive_input_zero_marginal_occurrences':unused,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(report,indent=2))
