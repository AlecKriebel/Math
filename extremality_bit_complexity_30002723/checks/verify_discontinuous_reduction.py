"""Exact dense validation of the proposed discontinuous coarse-face reduction.
No AHT implementation: union-find/orbit compression is a separate theorem.
Coordinates of a q-grid PL function: point p_k, right limit r_k, left limit l_k.
"""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import json,random
import numpy as np
from scipy.optimize import linprog
from sympy import Matrix
DIRECTIONS=[(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1),(2,-1),(1,-2),(-2,1),(-1,2)]
def sign(x):return (x>0)-(x<0)
def unit(q,k,state=0):
 a=[F(0)]*(3*q);a[(0 if state==0 else 1 if state>0 else 2)*q+k%q]=F(1);return a

def add(*terms):return [sum(x) for x in zip(*terms)]
def scale(a,t):return [t*x for x in a]
def sector(q,i,j,d):
 dx,dy=d
 return add(unit(q,i,sign(dx)),unit(q,j,sign(dy)),scale(unit(q,i+j,sign(dx+dy)),-1))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def full_ineq(q):return [sector(q,i,j,d) for i in range(q) for j in range(q) for d in DIRECTIONS]
def normalization(q,f):return [unit(q,0),unit(q,f)]
def full_tight(q,f,v):return normalization(q,f)+[a for a in full_ineq(q) if dot(a,v)==0]
def branch_value(q,v,cell,x):
 a,b=cell
 if a==b:return v[int(a*q)%q]
 k=int(a*q);k2=int(b*q)
 # cell lies inside an original input affine interval; use endpoint right/left values
 return ((b-x)*v[q+k%q]+(x-a)*v[2*q+k2%q])/(b-a)
def inrel(x,c):return x==c[0] if c[0]==c[1] else c[0]<x<c[1]
def feasible_dir(v,d,I,J,K):
 for x,t,c in [(v[0],d[0],I),(v[1],d[1],J),(sum(v),sum(d),K)]:
  a,b=c
  if a==b:
   if x!=a or t!=0:return False
  elif x==a:
   if t<=0:return False
  elif x==b:
   if t>=0:return False
  elif not a<x<b:return False
 return True

def poly(I,J,K):
 # Boundary equations A*x+B*y=C
 lines=[(1,0,I[0]),(1,0,I[1]),(0,1,J[0]),(0,1,J[1]),(1,1,K[0]),(1,1,K[1])]
 vs=set()
 for (a,b,c),(d,e,f) in combinations(lines,2):
  det=a*e-b*d
  if not det:continue
  x=(c*e-b*f)/det;y=(a*f-c*d)/det
  if I[0]<=x<=I[1] and J[0]<=y<=J[1] and K[0]<=x+y<=K[1]:vs.add((x,y))
 if not vs:return None
 vs=sorted(vs);m=(sum(x for x,y in vs)/len(vs),sum(y for x,y in vs)/len(vs))
 if not (inrel(m[0],I) and inrel(m[1],J) and inrel(sum(m),K)):return None
 dim=0 if len(vs)==1 else 1
 if len(vs)>2:
  x0,y0=vs[0];x1,y1=vs[1]
  if any((x1-x0)*(y-y0)!=(y1-y0)*(x-x0) for x,y in vs[2:]):dim=2
 return vs,dim

def cells(B,end=1):
 ext=sorted(set(x+t for t in range(end) for x in B if x<1)|{F(end)})
 return [(x,x) for x in ext]+list(zip(ext[:-1],ext[1:]))
def projections(vs):return [(min(v[i] for v in vs),max(v[i] for v in vs)) for i in (0,1)]+[(min(sum(v) for v in vs),max(sum(v) for v in vs))]
def slope(q,i):return scale(add(unit(q,i+1,-1),scale(unit(q,i,1),-1)),q)
def jump(q,k):return add(unit(q,k,1),scale(unit(q,k,-1),-1))
def spike2(q,k):return add(scale(unit(q,k),2),scale(unit(q,k,1),-1),scale(unit(q,k,-1),-1))
def structured(q,f,v,B):
 out=normalization(q,f);stats={'full_faces':0,'actual_edges':0,'limit_edges':0,'zero_vertex_sector_rows':0}
 def eq(a,b):out.append(add(a,scale(b,-1)))
 def force_cont(c):
  a,b=c
  for k in range(int(q*a)+1,int(q*b)):
   out.extend([jump(q,k),spike2(q,k)])
 def pair(P,limit=False):
  singleton=[i for i,c in enumerate(P) if c[0]==c[1]]
  assert len(singleton)==1
  t=singleton[0];val=P[t][0]
  if t==2:dom=P[0];mapping=lambda k:int(val*q)-1-k;pointmap=lambda k:int(val*q)-k;eps=-1
  elif t==1:dom=P[0];mapping=lambda k:k+int(val*q);pointmap=lambda k:k+int(val*q);eps=1
  else:dom=P[1];mapping=lambda k:k+int(val*q);pointmap=lambda k:k+int(val*q);eps=1
  for k in range(int(dom[0]*q),int(dom[1]*q)):eq(slope(q,k),slope(q,mapping(k)))
  if limit:
   for c in P:
    if c[0]!=c[1]:force_cont(c)
  else:
   for k in range(int(dom[0]*q)+1,int(dom[1]*q)):
    eq(jump(q,k),jump(q,pointmap(k)))
    eq(spike2(q,pointmap(k)),scale(spike2(q,k),eps))
 for I,J,K in product(cells(B),cells(B),cells(B,2)):
  data=poly(I,J,K)
  if data is None:continue
  vs,dim=data
  zs=[]
  for x,y in vs:
   slack=branch_value(q,v,I,x)+branch_value(q,v,J,y)-branch_value(q,v,K,x+y)
   assert slack>=0
   if slack==0:
    zs.append((x,y))
    for d in DIRECTIONS:
     if feasible_dir((x,y),d,I,J,K):
      out.append(sector(q,int(x*q),int(y*q),d));stats['zero_vertex_sector_rows']+=1
  if not zs:continue
  zdim=dim if len(zs)==len(vs) else (0 if len(zs)==1 else 1)
  if zdim==2:
   stats['full_faces']+=1
   P=projections(zs);first=None
   for c in P:
    force_cont(c)
    for k in range(int(c[0]*q),int(c[1]*q)):
     if first is None:first=slope(q,k)
     else:eq(slope(q,k),first)
  elif zdim==1:
   P=projections(zs)
   if dim==1:stats['actual_edges']+=1;pair(P)
   else:stats['limit_edges']+=1;pair(P,True)
 return out,stats

def sparse_map(q,B):
 n=len(B)-1;T=[[F(0)]*(3*n) for _ in range(3*q)]
 for k in range(q):
  x=F(k,q)
  if x in B[:-1]:
   i=B.index(x)
   for st in range(3):T[st*q+k][st*n+i]=1
  else:
   i=next(i for i in range(n) if B[i]<x<B[i+1]);a,b=B[i],B[i+1]
   r=[F(0)]*(3*n);r[n+i]=(b-x)/(b-a);r[2*n+(i+1)%n]=(x-a)/(b-a)
   for st in range(3):T[st*q+k]=r.copy()
 return T

def sample_case(q,f,B,rng):
 T=sparse_map(q,B);n=len(T[0]);A=full_ineq(q)
 A=np.array([[float(dot(a,col)) for col in zip(*T)] for a in A])
 E=[];b=[]
 for i in range(q):
  for d in [(0,0),(1,-1),(-1,1)]:
   row=sector(q,i,(f-i)%q,d)
   # delta pi=0 and p_f=1.
   E.append([float(dot(row,col)) for col in zip(*T)]);b.append(0)
 for k,rhs in [(0,0),(f,1)]:E.append([float(x) for x in T[k]]);b.append(rhs)
 res=linprog([rng.uniform(-1,1) for _ in range(n)],A_ub=-A,b_ub=np.zeros(len(A)),A_eq=E,b_eq=b,bounds=(0,1),method='highs')
 if not res.success:return None
 w=[F(float(x)).limit_denominator(10**7) for x in res.x];v=[dot(r,w) for r in T]
 if v[0]!=0 or v[f]!=1 or any(dot(a,v)<0 for a in full_ineq(q)):return None
 for i in range(q):
  for d in [(0,0),(1,-1),(-1,1)]:
   if dot(sector(q,i,(f-i)%q,d),v)!=0:return None
 return v

def run():
 rng=random.Random(1827);results=[]
 specs=[(5,1,[0,1,2,4,5]),(6,3,[0,1,3,5,6]),(7,2,[0,2,4,7]),(8,3,[0,1,3,5,8]),(9,4,[0,2,4,6,9]),(10,3,[0,1,3,7,10]),(12,5,[0,1,5,7,11,12])]
 for q,f,ints in specs:
  B=[F(i,q) for i in ints]
  for trial in range(5):
   v=sample_case(q,f,B,rng)
   if v is None:continue
   A=full_tight(q,f,v);C,stats=structured(q,f,v,B)
   ra=Matrix(A).rank();rc=Matrix(C).rank();ru=Matrix(A+C).rank()
   assert ra==rc==ru,(q,f,trial,ra,rc,ru)
   results.append({'q':q,'f_index':f,'breakpoint_indices':ints,'trial':trial,'full_rank':ra,'structured_rank':rc,'joint_rank':ru,'dimension':3*q,'two_sided_discontinuous_at_0':bool(v[q]>0 and v[2*q]>0),'values':[str(x) for x in v],'stats':stats})
 out={'description':'Exact equality of row spaces for full q-grid tight system and coarse zero-stratum slope/jump/spike reduction. Dense validation only.','case_count':len(results),'two_sided_count':sum(r['two_sided_discontinuous_at_0'] for r in results),'all_checks':'PASS','cases':results}
 Path(__file__).with_name('discontinuous_reduction_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
def verify_saved():
 data=json.loads(Path(__file__).with_name('discontinuous_reduction_results.json').read_text())
 for c in data['cases']:
  q=c['q'];f=c['f_index'];v=list(map(F,c['values']));B=[F(i,q) for i in c['breakpoint_indices']]
  assert v[0]==0 and v[f]==1 and all(dot(a,v)>=0 for a in full_ineq(q))
  for i in range(q):
   for d in [(0,0),(1,-1),(-1,1)]:assert dot(sector(q,i,(f-i)%q,d),v)==0
  A=full_tight(q,f,v);C,_=structured(q,f,v,B)
  def r(M):return int(Matrix(sorted(set(map(tuple,M)))).to_DM().rank())
  assert r(A)==r(C)==r(A+C)==c['full_rank']
 print(json.dumps({'all_checks':'PASS','saved_exact_case_count':len(data['cases'])}))
if __name__=='__main__':
 import sys
 verify_saved() if '--saved' in sys.argv else run()
