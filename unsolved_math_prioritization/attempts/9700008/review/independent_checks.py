from itertools import combinations
from fractions import Fraction
from pathlib import Path
import sympy as s,json,hashlib
checks=0; models=0; graphs=[]
def ck(v):
 global checks
 assert v; checks+=1
for n in range(2,6):
 E=list(combinations(range(n),2))
 for mask in range(1,1<<len(E)):
  edges=[e for i,e in enumerate(E) if mask>>i&1];deg=[sum(i in e for e in edges) for i in range(n)]
  if min(deg)==0 or len(set(deg))!=1:continue
  seen={0}
  while True:
   nxt=seen|{j for i,j in edges if i in seen}|{i for i,j in edges if j in seen}
   if nxt==seen:break
   seen=nxt
  if len(seen)==n:graphs.append((n,edges))
graphs += [(6,[(i,j) for i in range(3) for j in range(3,6)]),(6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)])]
for n,edges in graphs:
 d=2*len(edges)//n;A=s.zeros(n)
 for i,j in edges:A[i,j]=A[j,i]=1
 P=A/d
 for p in [s.Rational(1,9),s.Rational(2,3),s.Rational(19,20)]:
  mu=(s.eye(n)-(1-p)*P).inv()*s.Matrix([p]+[0]*(n-1));ck(sum(mu)==1);ck(all(x>0 for x in mu))
  L=s.zeros(n)
  for i,j in edges:
   c=min(mu[i],mu[j])/d;L[i,i]+=c;L[j,j]+=c;L[i,j]-=c;L[j,i]-=c
   if mu[i]!=mu[j]:
    x,y=(i,j) if mu[i]>mu[j] else (j,i)
    ck((1-p)*(mu[x]-mu[y])/(d*p)<=mu[y]/p)
  Q=d*(n-1)/p*L-(s.diag(*mu)-mu*mu.T)
  ck(Q*s.ones(n,1)==s.zeros(n,1))
  # Q annihilates constants. Positive leading principal minors on the
  # coordinate section f[-1]=0 certify the Poincare inequality for all f.
  for k in range(1,n):ck(Q[:k,:k].det()>0)
  for i in range(n):ck((1-p)/(d*p)*sum(mu[i]-mu[j] for j in range(n) if A[i,j])==int(i==0)-mu[i])
  models+=1
p,n=s.symbols('p n',positive=True)
tau=(n-1)*(1+(n-2)*p)/(n-p)
ck(s.simplify(s.diff(tau,p)-(n-1)**3/(n-p)**2)==0)
ck(s.simplify(tau.subs(p,s.Rational(1,2))/tau.subs(p,0)-n*n/(2*n-1))==0)
for N in range(2,11):
 for pp in [s.Rational(1,2),s.Rational(3,4)]:
  r=(1-pp)/(1+(N-2)*pp);K=s.ones(N)/(N-1)
  for i in range(N):K[i,i]=0
  for j in range(1,N):K[0,j]=r/(N-1)
  K[0,0]=1-r;x=s.symbols('x')
  expect=(x-1)*(x-(s.Rational(N-2,N-1)-r))*(x+s.Rational(1,N-1))**(N-2)
  ck(s.expand(K.charpoly(x).as_expr()-expect)==0)
result={'status':'PASS','exact_assertions':checks,'regular_graphs':len(graphs),'regular_models':models,'coverage':'All connected labeled regular simple graphs on 2–5 vertices; K3,3 and triangular prism; direct exact Poincare matrix certificates; complete characteristic polynomials for N=2–10; symbolic derivative and endpoint ratio. No floating-point eigenvalues.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
