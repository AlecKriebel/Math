"""End-to-end dense orbit implementation of the compressed mathematical reduction.
Uses dense signed union-find, NOT AHT. Compare residual nullity to BHK full matrix.
"""
from verify_discontinuous_reduction import *
from verify_fourfold_refinements import refine,rank
class SignedUF:
 def __init__(self,n):self.p=list(range(n));self.w=[1]*n;self.zero=set()
 def find(self,i):
  if self.p[i]!=i:
   r,w=self.find(self.p[i]);self.w[i]*=w;self.p[i]=r
  return self.p[i],self.w[i]
 def union(self,i,j,e=1):
  # z_j=e*z_i
  ri,wi=self.find(i);rj,wj=self.find(j)
  if ri==rj:
   if wj!=e*wi:self.zero.add(ri)
  else:
   dead=ri in self.zero or rj in self.zero
   self.p[rj]=ri;self.w[rj]=e*wi*wj
   if dead:self.zero.add(ri)
 def kill(self,i):self.zero.add(self.find(i)[0])
 def basis(self):
  roots={self.find(i)[0] for i in range(len(self.p))}
  # zero flags may sit on old roots; push to canonical roots
  dead={self.find(i)[0] for i in self.zero}
  return [[F(self.find(i)[1]) if self.find(i)[0]==r else F(0) for i in range(len(self.p))] for r in sorted(roots-dead)]

def model(N,f,v,B):
 ufs=[SignedUF(N) for _ in range(3)];res=[];desc=[[],[],[]];zeros=[[],[],[]]
 def pairing(fam,a,b,c,d,e=1):
  # g:[a,b]->[c,d], orientation from relative endpoint order
  if a>b:return
  assert b-a==abs(d-c)
  ori=1 if d>=c else -1
  desc[fam].append([a,b,c,d,e])
  for k in range(a,b+1):ufs[fam].union(k%N,(c+ori*(k-a))%N,e)
 def killrange(fam,a,b):
  if a>b:return
  zeros[fam].append([a,b])
  for k in range(a,b+1):ufs[fam].kill(k%N)
 def cont(c):
  a,b=map(lambda x:int(x*N),c)
  for fam in (1,2):killrange(fam,a+1,b-1)
 def edge(P,lim=False):
  t=next(i for i,c in enumerate(P) if c[0]==c[1]);val=int(P[t][0]*N)
  dom=P[0] if t!=0 else P[1];a,b=[int(x*N) for x in dom]
  if t==2:
   pairing(0,a,b-1,val-a-1,val-b)
   if not lim:
    pairing(1,a+1,b-1,val-a-1,val-b+1)
    pairing(2,a+1,b-1,val-a-1,val-b+1,-1)
  else:
   pairing(0,a,b-1,a+val,b+val-1)
   if not lim:
    pairing(1,a+1,b-1,a+1+val,b-1+val)
    pairing(2,a+1,b-1,a+1+val,b-1+val)
  if lim:
   for c in P:
    if c[0]!=c[1]:cont(c)
 for I,J,K in product(cells(B),cells(B),cells(B,2)):
  data=poly(I,J,K)
  if data is None:continue
  vs,dim=data;zs=[]
  for x,y in vs:
   if branch_value(N,v,I,x)+branch_value(N,v,J,y)==branch_value(N,v,K,x+y):
    zs.append((x,y))
    for d in DIRECTIONS:
     if feasible_dir((x,y),d,I,J,K):res.append(sector(N,int(x*N),int(y*N),d))
  if not zs:continue
  zdim=dim if len(zs)==len(vs) else (0 if len(zs)==1 else 1)
  if zdim==2:
   P=projections(zs);rep=None
   for c in P:
    a,b=[int(x*N) for x in c];cont(c)
    pairing(0,a,b-2,a+1,b-1)
    if rep is None:rep=a
    else:pairing(0,rep,rep,a,a)
  elif zdim==1:edge(projections(zs),dim==2)
 bases=[]
 for fam,uf in enumerate(ufs):
  for b in uf.basis():
   t=[[F(0)]*N for _ in range(3)];t[fam]=b;bases.append(t)
 cols=[];period=[]
 for s,j,p in bases:
  val=[F(0)]*(3*N);left0=-j[0]/2-p[0];right0=j[0]/2-p[0]
  val[0]=0;val[N]=right0;val[2*N]=left0
  left=right0
  for k in range(1,N):
   left+=s[k-1]/N
   if k>1:left+=j[k-1]
   val[k]=left+j[k]/2+p[k];val[N+k]=left+j[k];val[2*N+k]=left
  cols.append(val);period.append(sum(s)/N+sum(j))
 res.append(unit(N,f))
 M=[[dot(a,c) for c in cols] for a in res]+[period]
 rr=0 if not bases else rank(M)
 return {'free_dimensions':[len(u.basis()) for u in ufs],'D':len(bases),'K':len(M),'residual_rank':rr,'nullity':len(bases)-rr,'pairing_counts':list(map(len,desc)),'zero_range_counts':list(map(len,zeros))}

def run():
 old=json.loads(Path(__file__).with_name('discontinuous_reduction_results.json').read_text())['cases']
 out=[]
 for q,t in [(5,0),(6,0),(9,1),(9,2)]:
  c=next(r for r in old if r['q']==q and r['trial']==t);N=4*q
  v=refine(list(map(F,c['values'])));B=[F(i,q) for i in c['breakpoint_indices']]
  r=model(N,4*c['f_index'],v,B);dense=3*N-rank(full_tight(N,4*c['f_index'],v))
  assert r['nullity']==dense,(q,t,r,dense)
  r.update({'q':q,'N':N,'trial':t,'dense_nullity':dense});out.append(r);print(json.dumps(r),flush=True)
 final={'all_checks':'PASS','case_count':len(out),'checks':out}
 Path(__file__).with_name('orbit_pipeline_results.json').write_text(json.dumps(final,indent=2)+'\n')
if __name__=='__main__':run()
