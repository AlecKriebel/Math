"""Optional numerical search only; does not certify global optima. Requires NumPy/SciPy."""
import itertools,json,math
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
from pathlib import Path

def graph(n):
 P=list(itertools.permutations(range(n)));idx={p:i for i,p in enumerate(P)};N=len(P);d=n*(n-1)//2;edges=[]
 for i,p in enumerate(P):
  for a,b in itertools.combinations(range(n),2):
   pp=tuple(b if x==a else a if x==b else x for x in p);j=idx[pp]
   if i<j:edges.append((i,j))
 E=np.zeros((len(edges),N))
 for k,(i,j) in enumerate(edges):E[k,i]=-1;E[k,j]=1
 L=-E.T@E/d
 return P,edges,E,L

def matrices(r,edges,E,L):
 I=np.array([x[0] for x in edges]);J=np.array([x[1] for x in edges]);a=r[I];b=r[J];t=np.log(a/b);near=abs(t)<1e-5
 th=np.empty(len(t));ta=th.copy();tb=th.copy();far=~near
 th[far]=(a[far]-b[far])/t[far];ta[far]=(t[far]-1+b[far]/a[far])/t[far]**2;tb[far]=(-t[far]-1+a[far]/b[far])/t[far]**2
 # expansions in log ratio, relative to b
 z=t[near];th[near]=b[near]*(1+z/2+z*z/6+z**3/24+z**4/120);ta[near]=.5-z/6+z*z/24-z**3/120+z**4/720;tb[near]=.5+z/6+z*z/24+z**3/120+z**4/720
 lr=L@r;h=ta*lr[I]+tb*lr[J]
 A=E.T@(th[:,None]*E);D=E.T@(h[:,None]*E);B=D/2-(A@L+L@A)/2
 return A,B
rng=np.random.default_rng(20261005);out=[]
for n in [3,4]:
 P,edges,E,L=graph(n);N=len(P);best=[float('inf'),None,None]
 def fun(z):
  r=np.exp(np.r_[z,0]);r/=r.mean();A,B=matrices(r,edges,E,L)
  vals,vec=eigh(B[:-1,:-1],A[:-1,:-1],subset_by_index=[0,0])
  if vals[0]<best[0]:best[:]=[float(vals[0]),r.copy(),np.r_[vec[:,0],0]]
  return vals[0]
 for k in range(8):
  sol=minimize(fun,rng.normal(0,1.5,N-1),method='L-BFGS-B',bounds=[(-10,10)]*(N-1),options={'maxiter':250,'ftol':1e-11})
  print(n,k,best[0],sol.nit,flush=True)
 out.append({'n':n,'ratio':best[0],'rho':best[1].tolist(),'psi':best[2].tolist(),'permutations':P})
 print(json.dumps({'exploratory_results_so_far':out},indent=2),flush=True)
