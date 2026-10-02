#!/usr/bin/env python3
from fractions import Fraction as Q
import json,itertools,sys,contextlib,io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'turn2'))
with contextlib.redirect_stdout(io.StringIO()):
 from check_block_products import solve
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def mv(A,x):return [sum(a*b for a,b in zip(row,x)) for row in A]
def tr(A):return list(map(list,zip(*A)))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def independent(a,b):return any(a[i]*b[j]!=a[j]*b[i] for i in range(len(a)) for j in range(i+1,len(a)))
def section(a,b):
 n=len(a)
 for i in range(n):
  for j in range(i+1,n):
   D=a[i]*b[j]-a[j]*b[i]
   if D:
    y=[Q(0)]*n;y[i]=Q(b[j],D);y[j]=Q(-b[i],D);return y
 raise AssertionError('dependent')
models=attachments=0;records=[]
for m in range(2,8):
 catalog=[]
 for vals in itertools.product((-1,0,1),repeat=m):
  if len(catalog)>=30:break
  C=[[Q(vals[i] if i==j else 0) for j in range(m)] for i in range(m)];catalog.append(C)
 # Include nilpotent and nonreal blocks and Jordan degeneracies.
 for lam in (-1,0,1):
  C=[[Q(lam if i==j else 1 if j==i+1 else 0) for j in range(m)] for i in range(m)];catalog.append(C)
 C=[[Q(0)]*m for _ in range(m)];C[0][1]=1;catalog.append(C)
 C=[[Q(0)]*m for _ in range(m)];C[0][1]=-1;C[1][0]=1;catalog.append(C)
 for C in catalog:
  models+=1;rank=solve(C,[0]*m,m)[2];scalar=all(C[i][j]==(C[0][0] if i==j else 0) for i in range(m) for j in range(m))
  if scalar or rank<2:continue
  CT=tr(C);K=solve(CT,[0]*m,m)[1]
  for x in K:
   if not any(x):continue
   found=None
   for j in range(m):
    delta=[Q(int(i==j)) for i in range(m)];v=mv(CT,delta)
    if independent(x,v):found=(delta,v);break
   ck(found is not None);delta,v=found
   for den in range(10,15):
    a=[x[i]+Q(1,den)*delta[i] for i in range(m)]
    if not independent(a,v):continue
    y=section(a,v);ck(dot(a,y)==1);ck(dot(mv(CT,a),y)==0);attachments+=1
  # Every real codimension-one eigenspace among the constructed real eigenvalues.
  h=0
  for lam in (-1,1):
   M=[[C[i][j]-(lam if i==j else 0) for j in range(m)] for i in range(m)]
   if solve(M,[0]*m,m)[2]==1:h+=1
  ck(h<= (2 if m==2 else 1));records.append({'m':m,'rank':rank,'nonzero_eigen_hyperplanes':h})
# Rank-one nilpotent m=2 has two disjoint two-component branches.
for s,t in itertools.product((-2,-1,1,2),repeat=2):
 x=[Q(s),Q(0)];y=[Q(1,s),Q(t)];ck(dot(x,y)==1 and x[1]*y[0]==0)
 x=[Q(t),Q(s)];y=[Q(0),Q(1,s)];ck(dot(x,y)==1 and x[1]*y[0]==0)
# For m>=3 both branches meet at the third-coordinate unit solution.
for m in range(3,9):
 x=[Q(0)]*m;y=x.copy();x[2]=y[2]=1;ck(dot(x,y)==1 and x[1]==y[0]==0)
print(json.dumps({'assertions':checks,'matrix_models':models,'rank_drop_attachment_samples':attachments,'rank_at_least_two_records':records,'scope':'Exact ranks and local attachment sections supplement the analytic component proof; no numerical topology inference.'},indent=2))
