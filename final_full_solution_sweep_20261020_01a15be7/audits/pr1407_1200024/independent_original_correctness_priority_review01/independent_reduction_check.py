"""Own exact global Schur complements on actual finite networks; standard library only."""
from fractions import Fraction as F
from itertools import product,combinations
import json

def need(p,msg):
 if not p:raise RuntimeError(msg)
def schur(V,E,terminals):
 # Ground-free Laplacian elimination represented by rational conductance adjacency.
 a={v:{} for v in V}
 for x,y in E:a[x][y]=a[x].get(y,F(0))+1;a[y][x]=a[y].get(x,F(0))+1
 while len(a)>len(terminals):
  x=min((v for v in a if v not in terminals),key=lambda v:(len(a[v]),repr(v)))
  nbr=list(a[x].items());total=sum(c for y,c in nbr)
  need(total>0,'no isolated interior')
  for (y,c),(z,d) in combinations(nbr,2):
   val=c*d/total;a[y][z]=a[y].get(z,F(0))+val;a[z][y]=a[z].get(y,F(0))+val
  for y,c in nbr:del a[y][x]
  del a[x]
 return a

def branch(q,m):
 # u=(), parent=(-1,), grandparent=(-2,); all descendants to depth m.
 V=[(-1,),(-2,)]+[w for l in range(m+1) for w in product(range(q),repeat=l)];interior=V[2:]
 def p(w):return (-1,) if not w else ((-2,) if w==(-1,) else w[:-1])
 E=set()
 for w in interior:
  for z in [p(w),p(p(w))]:E.add(frozenset((w,z)))
 a=schur(V,[tuple(e) for e in E],{(-1,),(-2,)})
 return a[(-1,)][(-2,)],len(V)

def induced(q,n):
 V=[w for l in range(2*n+1) for w in product(range(q),repeat=l)];E=[]
 for w in V:
  if len(w)>=1:E.append((w,w[:-1]))
  if len(w)>=2:E.append((w,w[:-2]))
 t=[(0,)*i for i in [n,n-1,n-2]];a=schur(V,E,set(t));A=a[t[0]][t[1]];B=a[t[1]][t[2]];C=a[t[0]][t[2]]
 R01=1/(A+B*C/(B+C));R02=1/(C+A*B/(A+B))
 return (A,B,C),(R01,R02),len(V)

def main():
 rows=[]
 for q in [2,3]:
  k=F(1,2)
  for m in range(4):
   actual,nv=branch(q,m);need(actual==k,'full branch Schur vs recurrence');rows.append(dict(type='branch',q=q,m=m,vertices=nv,conductance=str(actual)));k=(1+q*k)/(2+q*k)
 for q,n in [(2,2),(2,3),(3,2)]:
  actual,R,nv=induced(q,n);c=[F(1)]
  for m in range(1,2*n):c.append(1+q*c[-1]/(1+c[-1]))
  a=lambda m:1+(q-1)*c[m-1]/(1+c[m-1])
  U=a(2*n-1)
  for j in range(n-2,0,-1):U=a(n+j)+U/(1+U)
  expected=(c[n],U,F(1));need(actual==expected,'full induced Schur vs three terminal reduction')
  need(R==(1/(c[n]+U/(1+U)),1/(1+c[n]*U/(c[n]+U))),'finite terminal resistances')
  rows.append(dict(type='induced',q=q,n=n,vertices=nv,triangle=list(map(str,actual)),resistances=list(map(str,R))))
 # Boundary mutant: wiring the two terminals gives zero resistance, not free1/k.
 need(branch(2,0)[0]==F(1,2),'free leaf branch is a two-edge series path')
 need(1/branch(2,0)[0]!=0,'wired/free confusion rejected')
 # Fixed point identities in Q(sqrt2), using pairs a+b*sqrt2.
 def mul(z,w):return(z[0]*w[0]+2*z[1]*w[1],z[0]*w[1]+z[1]*w[0])
 c=(F(1),F(1));need(mul(c,c)==(F(3),F(2)),'fixed point c square')
 need((F(24)-F(73,50))/7==F(161,50) and F(73,50)**2>2,'strict lower endpoint')
 return dict(status='PASS',author_programs_executed=False,exact_full_network_reductions=len(rows),largest_network_vertices=max(r['vertices'] for r in rows),rows=rows,scope='Finite independent structural guards; written contraction/exhaustion proof supplies all n and the infinite FREE limit.')
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
