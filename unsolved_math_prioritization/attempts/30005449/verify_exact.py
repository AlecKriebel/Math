"""Exact finite controls for the five-turn partial package; not a proof substitute."""
from fractions import Fraction
import json,random
import sympy as s
rng=random.Random(5449)
checks=0

def green(edges,w,N,F):
 verts=sorted({v for e in edges for v in e}-{F});idx={v:i for i,v in enumerate(verts)};L=s.zeros(len(verts))
 for (u,v),t in zip(edges,w):
  if u!=F:L[idx[u],idx[u]]+=t
  if v!=F:L[idx[v],idx[v]]+=t
  if u!=F and v!=F:L[idx[u],idx[v]]-=t;L[idx[v],idx[u]]-=t
 return idx,L,L.inv()

def probabilities(edges,w,N,F):
 idx,L,G=green(edges,w,N,F);out=[]
 for (u,v),t in zip(edges,w):
  A=L.copy();rhs=s.zeros(L.rows,1)
  if u==F or v==F:rhs[idx[v if u==F else u]]=t
  else:A[idx[u],idx[v]]+=t;A[idx[v],idx[u]]+=t;rhs[idx[u]]=t;rhs[idx[v]]=t
  out.append(s.factor((A.inv()*rhs)[idx[N]]))
 return out

examples=[([(0,1),(1,2)],0,2), ([(0,1),(0,2),(1,2)],0,2), ([(0,1),(1,2),(2,3),(3,0),(1,3),(3,4)],0,4), ([(0,1),(0,2),(1,2),(1,3),(2,3),(3,4)],0,4)]
for edges,N,F in examples:
 for rep in range(8):
  w=[s.Rational(rng.randint(1,7),rng.randint(1,5)) for _ in edges]
  idx,L,G=green(edges,w,N,F);p=probabilities(edges,w,N,F)
  assert sum(p[j] for j,e in enumerate(edges) if F in e)==1;checks+=1
  assert probabilities(edges,[s.Rational(3,2)*x for x in w],N,F)==p;checks+=1
  for j,((u,v),t) in enumerate(zip(edges,w)):
   assert 0<p[j]<=1;checks+=1
   if F in (u,v):
    x=v if u==F else u;assert p[j]==t*G[idx[N],idx[x]];checks+=1
   else:
    a=G[idx[u],idx[u]];b=G[idx[v],idx[v]];c=G[idx[u],idx[v]];x=G[idx[N],idx[u]];y=G[idx[N],idx[v]]
    den=(1+t*c)**2-t*t*a*b
    assert den>0;checks+=1
    assert p[j]==s.factor(t*(x*(1+t*(c-b))+y*(1+t*(c-a)))/den);checks+=1

a,b,c=s.symbols('a b c',positive=True);D=a*b+a*c+b*c
q1=(b+c)/D;q2=1/(a+b)
assert s.simplify(s.diff(q1,b)+c*c/D**2)==0;checks+=1
assert s.simplify(s.diff(q2,a)+1/(a+b)**2)==0;checks+=1
assert (s.diff(q1,b)-s.diff(q2,a)).subs({a:1,b:1,c:1})==s.Rational(5,36);checks+=1

cores=[(2,[(0,1)]),(3,[(0,1),(1,2)]),(3,[(0,1),(0,2),(1,2)]),(4,[(0,1),(1,2),(2,3),(3,0)]),(4,[(0,1),(0,2),(1,2),(1,3),(2,3)])]
def cap(n,edges,w,j):
 A=s.zeros(n)
 for k,((u,v),t) in enumerate(zip(edges,w)):
  A[u,u]+=t;A[v,v]+=t
  if j!=k:A[u,v]-=t;A[v,u]-=t
 return s.factor(A[0,0]-(A[0,1:]*A[1:,1:].inv()*A[1:,0])[0])
for n,edges in cores:
 for d in (2,3,5):
  for rep in range(4):
   w=[s.Rational(rng.randint(1,7),rng.randint(1,5)) for _ in edges]
   path=[(0,n)]+[(n+j,n+j+1) for j in range(d-1)];F=n+d-1
   p=probabilities(edges+path,w+[s.Integer(1)]*d,0,F)
   for j in range(len(edges)):
    C=cap(n,edges,w,j)
    assert C>0;checks+=1
    assert p[j]==d*C/(1+d*C);checks+=1
    assert cap(n,edges,[2*x for x in w],j)==2*C;checks+=1
   assert p[len(edges):]==[1]*d;checks+=1
# Exact tree equilibrium at all depths for several food-stem lengths.
n=5;edges=[(0,1),(1,2),(1,3),(3,4)];depth=[1,2,2,3]
for d in range(2,10):
 w=[s.Rational(d-1,d)**k for k in depth];path=[(0,n)]+[(n+j,n+j+1) for j in range(d-1)]
 assert probabilities(edges+path,w+[s.Integer(1)]*d,0,n+d-1)[:4]==w;checks+=4
x=s.symbols('x',positive=True)
assert probabilities([(0,1),(1,2),(1,3)],[1,1,x],0,2)[2]==x/(1+x);checks+=1
# Nontrivial cyclic equilibrium as an exact consistency check of Turn 5.
z=(s.sqrt(42)-4)/4;t=3*z/(1+4*z)
p=probabilities([(0,1),(0,2),(1,2),(0,3),(3,4)],[z,z,t,1,1],0,4)
for actual,target in zip(p,[z,z,t,1,1]):assert s.simplify(actual-target)==0;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'checks':['killed-edge versus rank-two probabilities','terminal flux and homogeneity','triangle gradient obstruction','cyclic-core effective conductance formula','tree fixed points and critical boundary drift','explicit positive triangular-core equilibrium'],'cyclic_example':{'food_stem_length':2,'root_edges':'(sqrt(42)-4)/4','opposite_edge':'3s/(1+4s)'},'limits':'Finite exact controls do not establish the stochastic convergence theorems or the unresolved arbitrary-graph conjecture; those require the written arguments.'},indent=2))
