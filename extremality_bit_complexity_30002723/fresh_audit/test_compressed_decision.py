"""Fresh end-to-end dense simulation of the proposed compressed decision.
Independent from candidate scripts. Uses auditor's geometry helper only.
The dense lifts simulate the imported AHT oracle, not its time bound.
"""
from test_local_factorization import *

class Union:
 def __init__(self,n):self.p=list(range(n))
 def root(self,i):
  while self.p[i]!=i:self.p[i]=self.p[self.p[i]];i=self.p[i]
  return i
 def join(self,i,j):self.p[self.root(i)]=self.root(j)
 def count(self):return len({self.root(i) for i in range(len(self.p))})

def lift(N,edges,zero):
 A=Union(N);B=Union(2*N)
 for i,j,e in edges:
  i%=N;j%=N;A.join(i,j)
  for s in (0,1):B.join(i+s*N,j+(s^(e<0))*N)
 for i in zero:B.join(i%N,i%N+N)
 return A,B

def basis(N,edges,zero):
 A,B=lift(N,edges,zero);D=B.count()-A.count();killed=set(zero);reps=[]
 def dimension(z):return lift(N,edges,z)[1].count()-A.count()
 while dimension(killed):
  d=dimension(killed);a,b=0,N-1
  while a<b:
   m=(a+b)//2
   if dimension(killed|set(range(m+1)))<d:b=m
   else:a=m+1
  assert dimension(killed|{a})==d-1
  reps.append(a);killed.add(a)
 assert len(reps)==D
 cols=[]
 for r in reps:
  C=B.root(r)
  col=[int(B.root(k)==C)-int(B.root(N+k)==C) for k in range(N)]
  assert col[r]==1
  cols.append(col)
 return D,cols

def refine(old,m):
 q=len(old)//3;N=m*q;v=[Q(0)]*(3*N)
 for k in range(N):
  a,t=divmod(k,m)
  if t==0:
   for j in range(3):v[3*k+j]=old[j*q+a]
  else:
   p=((m-t)*old[q+a]+t*old[2*q+(a+1)%q])/m
   for j in range(3):v[3*k+j]=p
 return v

def test_case(q,f,old,B,m):
 N=q*m;v=refine(old,m);B=[b*m for b in B];f*=m
 def value(c,x):
  a,b=c
  if a==b:return v[3*(int(a)%N)]
  return ((b-x)*v[3*(int(a)%N)+1]+(x-a)*v[3*(int(b)%N)+2])/(b-a)
 def slack(cells,p):return value(cells[0],p[0])+value(cells[1],p[1])-value(cells[2],sum(p))
 full=[vec(N,0,0),vec(N,f,0)]
 for x,y in product(range(N),repeat=2):
  for d in DIRECTIONS.values():
   r=row(N,x,y,d)
   z=sum(a*b for a,b in zip(r,v));assert z>=0
   if z==0:full.append(r)
 edges=[[] for _ in range(3)];zeros=[set() for _ in range(3)];residual=[vec(N,f,0)]
 def join(fam,a,b,e=1):edges[fam].append((a%N,b%N,e))
 def regular(c):
  for k in range(c[0]+1,c[1]):zeros[1].add(k%N);zeros[2].add(k%N)
 points=sorted(set(B+[x+N for x in B]));xy=[(x,x) for x in B]+list(zip(B[:-1],B[1:]));z=[(x,x) for x in points]+list(zip(points[:-1],points[1:]))
 for cells in product(xy,xy,z):
  V=vertices(cells)
  if V is None:continue
  Z=[p for p in V if slack(cells,p)==0]
  assert all(slack(cells,p)>=0 for p in V)
  if not Z:continue
  for x,y in Z:
   for d in DIRECTIONS.values():
    if feasible(cells,(x,y),d):residual.append(row(N,int(x),int(y),d))
  P=[tuple(map(int,c)) for c in projected(Z)]
  if dim(Z)==2:
   first=None
   for c in P:
    regular(c)
    for k in range(*c):
     if first is None:first=k
     else:join(0,first,k)
  elif dim(Z)==1:
   j=next(i for i,c in enumerate(P) if c[0]==c[1]);t=P[j][0];dom=P[1] if j==0 else P[0]
   cm=(lambda k:t-k-1) if j==2 else (lambda k:k+t)
   pm=(lambda k:t-k) if j==2 else (lambda k:k+t)
   for k in range(*dom):join(0,k,cm(k))
   if dim(V)==2:
    for c in P:regular(c)
   else:
    for k in range(dom[0]+1,dom[1]):join(1,k,pm(k));join(2,k,pm(k),-1 if j==2 else 1)
 dimensions=[];parametercols=[]
 for fam in range(3):
  D,C=basis(N,edges[fam],zeros[fam]);dimensions.append(D)
  for col in C:
   z=[0]*(3*N);z[fam*N:(fam+1)*N]=col;parametercols.append(z)
 D=sum(dimensions)
 tracecols=[];period=[]
 for z in parametercols:
  s,j,p=z[:N],z[N:2*N],z[2*N:]
  period.append(sum(s,Q(0))/N+sum(j,Q(0)))
  t=[Q(0)]*(3*N)
  for k in range(N):
   left=(-Q(j[0],2)-p[0]) if k==0 else Q(j[0],2)-p[0]+sum(s[:k],Q(0))/N+sum(j[1:k],Q(0))
   t[3*k+2]=left;t[3*k+1]=left+j[k];t[3*k]=Q(0) if k==0 else left+Q(j[k],2)+p[k]
  tracecols.append(t)
 M=[period]+[[sum(a*b for a,b in zip(r,c)) for c in tracecols] for r in residual]
 dense_null=3*N-rank(full);compressed_null=D-rank(M)
 assert dense_null==compressed_null,(q,m,dimensions,dense_null,compressed_null)
 # Any cutoff-triggered nonextremality must agree with the dense answer.
 K=len(residual)+1
 if D>K:assert dense_null>0
 return {'q':q,'N':N,'signed_family_dimensions':dimensions,'K':K,'dense_nullity':dense_null,'compressed_nullity':compressed_null,'cutoff_triggered':D>K}

def run():
 source=json.loads(Path(__file__).resolve().parents[1].joinpath('checks/discontinuous_reduction_results.json').read_text())['cases']
 chosen=[source[i] for i in (0,4,5,10,15,20,21,22,24,25,30,34)]
 results=[]
 for c in chosen:
  results.append(test_case(c['q'],c['f_index'],list(map(Q,c['values'])),c['breakpoint_indices'],1))
 for c in (source[0],source[21],source[22]):
  results.append(test_case(c['q'],c['f_index'],list(map(Q,c['values'])),c['breakpoint_indices'],4))
 for m in (1,2,4,8,16):
  results.append(test_case(2,1,list(map(Q,[0,1,Q(1,2),Q(1,2),Q(1,2),Q(1,2)])),[0,1,2],m))
 out={'status':'PASS','case_count':len(results),'cutoff_exercised':any(x['cutoff_triggered'] for x in results),'cases':results}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
