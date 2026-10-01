#!/usr/bin/env python3
"""Independent exact controls for the scoped single-step Lck proof.
No simulation, author code, remote execution, or external downloads.
The universal convergence theorem is established by the written audit.
"""
import json
from collections import deque
from fractions import Fraction as Q
from pathlib import Path
import sympy as s
checks=0
def ck(v):
 global checks
 assert bool(v)
 checks+=1
r,m,e,c,b,z=s.symbols('r m e c b z')
k1,k2,k3,k4,k5,k6=s.symbols('k1 k2 k3 k4 k5 k6',positive=True)
# Columns are six individual reactions, species order r,m,e,c,b,z.
nu=s.Matrix([[-1,1,0,0,0,1],[-1,1,0,0,0,1],[0,0,-1,1,1,0],[1,-1,-1,1,0,0],[0,0,1,-1,-1,0],[0,0,0,0,1,-1]])
vel=s.Matrix([k1*r*m,k2*c,k3*c*e,k4*b,k5*b,k6*z])
full=nu*vel
Rrow=s.Matrix([[1,0,0,1,1,1]]);Mrow=s.Matrix([[0,1,0,1,1,1]]);Erow=s.Matrix([[0,0,1,0,1,0]])
for row in [Rrow,Mrow,Erow]:
 for v in row*nu:ck(v==0)
D,E=s.symbols('D E',real=True)
red=s.Matrix([full[i].subs({m:r+D,e:E-b}) for i in [0,3,4,5]])
f=k1*r*(r+D)
expected=s.Matrix([-f+k2*c+k6*z,f-k2*c-k3*c*(E-b)+k4*b,k3*c*(E-b)-(k4+k5)*b,k5*b-k6*z])
for v in red-expected:ck(s.expand(v)==0)
J=red.jacobian([r,c,b,z])
Jexpect=s.Matrix([[-k1*(2*r+D),k2,0,k6],[k1*(2*r+D),-k2-k3*(E-b),k3*c+k4,0],[0,k3*(E-b),-k3*c-k4-k5,0],[0,0,k5,-k6]])
for v in J-Jexpect:ck(s.expand(v)==0)
for v in s.ones(1,4)*J:ck(s.expand(v)==0)
th=s.symbols('th');rs,cs,bs,zs=s.symbols('rs cs bs zs')
A=J.subs({r:rs+th*(r-rs),c:cs+th*(c-cs),b:bs+th*(b-bs),z:zs+th*(z-zs)},simultaneous=True).applyfunc(lambda x:s.integrate(x,(th,0,1)))
for v in red-red.subs({r:rs,c:cs,b:bs,z:zs},simultaneous=True)-A*s.Matrix([r-rs,c-cs,b-bs,z-zs]):ck(s.expand(v)==0)
ck(s.expand(A[1,0]-k1*(r+rs+D))==0)
ck(s.expand(A[2,1]-k3*(2*E-b-bs)/2)==0)
# Equilibrium algebra from b and strict monotonicity of w.
cb=(k4+k5)*b/(k3*(E-b));zb=k5*b/k6;w=cb+b+zb
R,M=s.symbols('R M',positive=True)
fb=k1*(R-w)*(M-w)-k2*cb-k5*b
for expr in [s.diff(cb,b)-(k4+k5)*E/(k3*(E-b)**2),s.diff(w,b)-s.diff(cb,b)-1-k5/k6,s.diff(fb,b)+k1*s.diff(w,b)*(R+M-2*w)+k2*s.diff(cb,b)+k5]:ck(s.simplify(expr)==0)
xe={r:R-w,c:cb,b:b,z:zb,D:M-R}
y=red.subs(xe,simultaneous=True)
for v in y-s.Matrix([-fb,fb,0,0]):ck(s.simplify(v)==0)
# Constant lower-bound directed edges, columns are origins.
edges=[(1,0),(2,1),(0,1),(1,2),(3,2),(0,3)]
graph={i:[] for i in range(4)}
for target,source in edges:graph[source].append(target)
paths={}
for origin in range(4):
 dist={origin:0};queue=deque([origin])
 while queue:
  a=queue.popleft()
  for target in graph[a]:
   if target not in dist:dist[target]=dist[a]+1;queue.append(target)
 for target in range(4):ck(target in dist and dist[target]<=3)
 paths[str(origin)]=dist
# Rational checks include either free-pool boundary, c/b/z boundaries, enzyme saturation,
# unequal totals, and convex averages. Totals are derived from physical six-species data.
ratesets=[[Q(1)]*6,[Q(1,100),Q(5),Q(7,3),Q(1,8),Q(23),Q(2)],[Q(99),Q(1,10),Q(1,7),Q(20),Q(3,2),Q(1,99)]]
points=[(Q(0),Q(2),Q(1),Q(0),Q(0),Q(1)),(Q(2),Q(0),Q(0),Q(1),Q(3),Q(0)),(Q(0),Q(0),Q(1),Q(0),Q(1),Q(0)),(Q(1),Q(1),Q(0),Q(0),Q(1),Q(0)),(Q(1),Q(4),Q(2),Q(0),Q(0),Q(0)),(Q(4),Q(1),Q(2),Q(1),Q(0),Q(0))]
for ks in ratesets:
 for rr,mm,ee,cc,bb,zz in points:
  RT=rr+cc+bb+zz;MT=mm+cc+bb+zz;ET=ee+bb;delta=MT-RT
  ck(RT>0 and MT>0 and ET>0)
  sub=dict(zip([r,D,E,c,b,z,k1,k2,k3,k4,k5,k6],[rr,delta,ET,cc,bb,zz,*ks]))
  v=red.subs(sub);mat=J.subs(sub)
  ck(sum(v)==0)
  for i,x in enumerate([rr,cc,bb,zz]):
   if x==0:ck(v[i]>=0)
  if mm==0:ck(v[0]>=0)
  if ee==0:ck(v[2]<0)
  for i in range(4):
   for j in range(4):
    if i!=j:ck(mat[i,j]>=0)
  Mshift=1+ks[0]*(RT+MT)+ks[1]+ks[2]*(ET+RT)+ks[3]+ks[4]+ks[5]
  for i in range(4):ck(mat[i,i]+Mshift>0)
# Exact generic stochastic contraction identity and l1 controls.
eps=Q(1,32)
for n in range(1,10):
 weights=[[Q(1+((i+2*j+n)%7)) for j in range(4)] for i in range(4)]
 P=[[weights[i][j]/sum(weights[a][j] for a in range(4)) for j in range(4)] for i in range(4)]
 for row in P:
  for v in row:ck(v>=eps)
 for j in range(4):ck(sum(P[i][j] for i in range(4))==1)
 for v in [(Q(n),Q(-n),Q(0),Q(0)),(Q(n),Q(2),Q(-1),Q(-n-1)),(Q(-1),Q(-1),Q(1),Q(1))]:
  pv=[sum(P[i][j]*v[j] for j in range(4)) for i in range(4)]
  qv=[sum((P[i][j]-eps)*v[j] for j in range(4)) for i in range(4)]
  ck(pv==qv)
  ck(sum(abs(a) for a in pv)<=(1-4*eps)*sum(abs(a) for a in v))
print(json.dumps({'status':'pass','exact_assertions':checks,'max_directed_path_length':max(max(d.values()) for d in paths.values()),'shortest_paths':paths,'numerical_simulations':0,'scope':'N=1 Lck-only, positive rates and totals, every nonnegative point in the fixed physical class','limitations':'finite controls supplement the separate universal proof; no general-chain conclusion'},indent=2,sort_keys=True))
