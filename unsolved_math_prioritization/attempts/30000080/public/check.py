#!/usr/bin/env python3
"""Exact bounded controls; Python 3.12 + NumPy, no network or external CAS."""
import itertools, json, random, pathlib, time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent

def mons(n,d):
 if n==1:return [(d,)]
 return [(i,)+a for i in range(d+1) for a in mons(n-1,d-i)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def rref(A,p,need_kernel=False):
 A=np.array(A,dtype=np.int64,copy=True)%p
 rows,cols=A.shape; piv=[]; r=0
 for c in range(cols):
  nz=np.flatnonzero(A[r:,c])
  if not len(nz):continue
  j=r+int(nz[0]);A[[r,j]]=A[[j,r]]; A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  nz=np.flatnonzero(A[:,c]);nz=nz[nz!=r]
  if len(nz):A[nz]=(A[nz]-A[nz,c,None]*A[r])%p
  piv.append(c);r+=1
  if r==rows:break
 if not need_kernel:return r
 free=[i for i in range(cols) if i not in piv];B=np.zeros((cols,len(free)),dtype=np.int64)
 for j,c in enumerate(free):
  B[c,j]=1
  for i,k in enumerate(piv):B[k,j]=-A[i,c]%p
 return r,B

def multiplication(gens,n,d,e):
 target=mons(n,e);idx={a:i for i,a in enumerate(target)};mult=mons(n,e-d)
 A=np.zeros((len(target),len(gens)*len(mult)),dtype=np.int64)
 for j,g in enumerate(gens):
  for k,b in enumerate(mult):
   for a,v in g.items():A[idx[add(a,b)],j*len(mult)+k]+=v
 return A

def syzygy_multiples(B,n,d,e,r):
 small=mons(n,1); big=mons(n,e-d);ix={a:i for i,a in enumerate(big)};mm=mons(n,e-d-1)
 C=np.zeros((r*len(big),B.shape[1]*len(mm)),dtype=np.int64)
 for s in range(B.shape[1]):
  for j,b in enumerate(mm):
   for g in range(r):
    for i,a in enumerate(small):C[g*len(big)+ix[add(a,b)],s*len(mm)+j]+=B[g*len(small)+i,s]
 return C

def product_polys(f,g,p):
 h={}
 for a,c in f.items():
  for b,d in g.items():h[add(a,b)]=(h.get(add(a,b),0)+c*d)%p
 return {a:c for a,c in h.items() if c}
def power_rank(gens,n,d,t,p):
 target=mons(n,d*t);ix={a:i for i,a in enumerate(target)};cs=[]
 for comb in itertools.combinations_with_replacement(range(len(gens)),t):
  f={(0,)*n:1}
  for j in comb:f=product_polys(f,gens[j],p)
  c=np.zeros(len(target),dtype=np.int64)
  for a,v in f.items():c[ix[a]]=v
  cs.append(c)
 return rref(np.array(cs).T,p),len(target)

def pack(a,d):
 """Partition degree k*d on at most k+1 coordinates into k binary factors."""
 a=list(a);k=sum(a)//d
 assert sum(a)==k*d and sum(x>0 for x in a)<=k+1
 if k==0:return []
 pos=[i for i,x in enumerate(a) if x]
 if len(pos)<=k:
  big=[i for i in pos if a[i]>=d]
  if big:i=big[0];u=[0]*len(a);u[i]=d
  else:
   i=max(pos,key=lambda j:a[j]);j=next(j for j in pos if j!=i and a[i]+a[j]>=d);u=[0]*len(a);u[i]=a[i];u[j]=d-a[i]
 else:
  under=[i for i in pos if a[i]<=d];i=max(under,key=lambda j:a[j])
  if a[i]==d:u=[0]*len(a);u[i]=d
  else:
   j=next(j for j in pos if j!=i and a[i]+a[j]>=d);u=[0]*len(a);u[i]=a[i];u[j]=d-a[i]
 b=[x-y for x,y in zip(a,u)];return [tuple(u)]+pack(b,d)

def main():
 start=time.time();packing=[]
 for n in range(2,7):
  for d in range(1,6):
   count=0
   # Grid contains exactly 234026 monomials in total.
   for a in mons(n,(n-1)*d):
    fs=pack(a,d);assert len(fs)==n-1
    assert all(sum(f)==d and sum(x>0 for x in f)<=2 for f in fs)
    assert tuple(map(sum,zip(*fs)))==a;count+=1
   packing.append({'n':n,'d':d,'monomials':count})
 finite=[];rng=random.Random(30000080)
 for p in [2,3,5]:
  n=4;d=2;pure=[a for a in mons(n,d) if 2 in a];cross=[a for a in mons(n,d) if 2 not in a]
  for w in [3,4,5,6]:
   for trial in range(3):
    while True:
     M=np.array([[rng.randrange(p) for _ in cross] for _ in range(w)],dtype=np.int64)
     if rref(M,p)==w:break
    gens=[{a:1} for a in pure]+[{a:int(v) for a,v in zip(cross,row) if v} for row in M]
    rank3,B=rref(multiplication(gens,n,d,3),p,True);checks=[]
    for e in [4,5,6]:
     A=multiplication(gens,n,d,e);ker=A.shape[1]-rref(A,p);span=rref(syzygy_multiples(B,n,d,e,len(gens)),p)
     checks.append({'degree':e,'kernel_dim':ker,'linear_span_dim':span})
    linear=all(c['kernel_dim']==c['linear_span_dim'] for c in checks)
    pr,target=power_rank(gens,n,d,3,p)
    if linear:assert pr==target
    finite.append({'field':p,'cross_dim':w,'trial':trial,'cross_matrix':M.tolist(),'generators':len(gens),'linear_syzygies':B.shape[1],'complete_linearity_checks':checks,'linearly_presented':linear,'cube_rank':pr,'cube_target_dimension':target})
 obstruction=[]
 for p in [2,3,5,7]:
  # d/dz: Sym^p(Kb+Kz)->Sym^(p-1)(Kb+Kz) tensor Kz.
  diag=list(range(p+1));rank=sum(j%p!=0 for j in diag)
  assert rank==p-1
  obstruction.append({'p':p,'source_dim':p+1,'target_dim':p,'derivative_rank':rank,'kernel_dimension':2,'expected_kernel_if_exact':1})
 sanity=[]
 for p in [2,3,5]:
  allm=mons(4,2);sq=[{a:1} for a in allm if 2 in a];full=[{a:1} for a in allm]
  for label,gs,expect in [('pure_squares',sq,False),('maximal_ideal_square',full,True)]:
   _,B=rref(multiplication(gs,4,2,3),p,True);checks=[]
   for e in [4,5,6]:
    A=multiplication(gs,4,2,e);checks.append(A.shape[1]-rref(A,p)==rref(syzygy_multiples(B,4,2,e,len(gs)),p))
   linear=all(checks);pr,tr=power_rank(gs,4,2,3,p)
   assert linear==expect and pr==(84 if expect else 20)
   sanity.append({'field':p,'control':label,'linearly_presented':linear,'cube_rank':pr,'target':tr})
 out={'sanity_controls':sanity,'packing':packing,'finite_field_samples':finite,'polarization_obstruction':obstruction,'summary':{'packing_count':sum(x['monomials'] for x in packing),'sample_count':len(finite),'certified_linear':sum(x['linearly_presented'] for x in finite),'failures_among_certified_linear':sum(x['linearly_presented'] and x['cube_rank']!=x['cube_target_dimension'] for x in finite)},'limits':{'packing_n':'2..6','packing_d':'1..5','sample_n':4,'sample_d':2,'fields':[2,3,5],'cross_dimensions':[3,4,5,6],'trials_each':3,'seed':30000080,'syzygy_degrees':[3,4,5,6],'power_test':3,'scope':'All sampled ideals contain the four variable squares. No exhaustive all-ideal or all-field conclusion.'}}
 (ROOT/'control-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary'],indent=2));print('seconds',round(time.time()-start,3))
if __name__=='__main__':main()
