#!/usr/bin/env python3
"""Exact controls for the independently reviewable single-step partial theorem."""
import sympy as s,json,hashlib
from pathlib import Path
from collections import Counter,deque
C=Counter()
def ck(cat,test):
 assert test,cat
 C[cat]+=1
r,c,b,z,D,E=s.symbols('r c b z Delta E',real=True)
k1,k2,k3,k4,k5,k6=s.symbols('k1 k2 k3 k4 k5 k6',positive=True)
f=k1*r*(r+D)
F=s.Matrix([-f+k2*c+k6*z,f-k2*c-k3*c*(E-b)+k4*b,k3*c*(E-b)-(k4+k5)*b,k5*b-k6*z])
x=s.Matrix([r,c,b,z]);J=F.jacobian(x)
expected=s.Matrix([[-k1*(2*r+D),k2,0,k6],[k1*(2*r+D),-k2-k3*(E-b),k3*c+k4,0],[0,k3*(E-b),-k3*c-k4-k5,0],[0,0,k5,-k6]])
for i in range(4):
 for j in range(4):ck('exact_jacobian',s.expand(J[i,j]-expected[i,j])==0)
ck('conserved_receptor',s.expand(sum(F))==0)
for j in range(4):ck('zero_column_sums',s.expand(sum(J[:,j]))==0)
rs,cs,bs,zs,t=s.symbols('rs cs bs zs theta',real=True)
xstar=s.Matrix([rs,cs,bs,zs]);sub=dict(zip(x,xstar+t*(x-xstar)))
A=J.subs(sub,simultaneous=True).applyfunc(lambda v:s.integrate(v,(t,0,1)))
for i in range(4):ck('exact_mean_value',s.expand((A*(x-xstar))[i]-F[i]+F[i].subs(dict(zip(x,xstar)),simultaneous=True))==0)
ck('averaged_r_to_c',s.expand(A[1,0]-k1*(r+rs+D))==0)
ck('averaged_c_to_b',s.expand(A[2,1]-k3*(2*E-b-bs)/2)==0)
# Each interval-independent edge is retained in the mean Jacobian.
for i,j,q in [(0,1,k2),(1,2,k4),(3,2,k5),(0,3,k6)]:
 ck('constant_edge_component',s.expand(A[i,j]-q)==0 if (i,j)!=(1,2) else s.expand(A[i,j]-q-k3*(c+cs)/2)==0)
# Path length at most 3 among every ordered pair.
edges={0:[1],1:[0,2],2:[1,3],3:[0]}
for start in range(4):
 dist={start:0};q=deque([start])
 while q:
  a=q.popleft()
  for j in edges[a]:
   if j not in dist:dist[j]=dist[a]+1;q.append(j)
 for end in range(4):ck('strongly_connected_short_paths',end in dist and dist[end]<=3)
# Equilibrium reconstructed parametrically with rates/totals chosen to fit it.
for j in range(1,25):
 vals={k2:s.Rational(j+1,j),k3:s.Rational(j+2,j+1),k4:s.Rational(j+3,j+2),k5:s.Rational(j+4,j+3),k6:s.Rational(j+5,j+4),E:s.Rational(2*j+3,j+1),b:s.Rational(j+1,2*j+3)}
 bb=vals[b];ee=vals[E]-bb;cc=(vals[k4]+vals[k5])*bb/(vals[k3]*ee);zz=vals[k5]*bb/vals[k6];rr=s.Rational(j+2,j+1);mm=s.Rational(j+5,2*j+1)
 vals.update({r:rr,c:cc,z:zz,D:mm-rr,k1:(vals[k2]*cc+vals[k5]*bb)/(rr*mm)})
 for a in [rr,mm,ee,cc,bb,zz]:ck('physical_positive_equilibrium',a>0)
 for v in F:ck('equilibrium_residual',s.cancel(v.subs(vals))==0)
 mat=J.subs(vals)
 for row in range(4):
  for col in range(4):
   if row!=col:ck('metzler_at_controls',mat[row,col]>=0)
root=Path(__file__).resolve().parent
out={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'proof_sha256':hashlib.sha256((root/'SINGLE_STEP_CANDIDATE.md').read_bytes()).hexdigest(),'scope':'Exact supporting controls for N=1 theorem only; universal stochastic-contraction proof is written separately; no numerical simulation'}
(root/'single_step_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
