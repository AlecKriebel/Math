#!/usr/bin/env python3
"""Bounded floating diagnostics; not a stability or no-Hopf certificate."""
from pathlib import Path
import numpy as np,json,random
rng=random.Random(351805)
rows=[];positive=[]
for N in [2,3,4,6,10,20,30]:
 for trial in range(64):
  ex=[rng.randrange(-8,9) for _ in range(8)]
  u,v,w,nu,e,c0,r,m=[2.**k for k in ex]
  a=u/(v+w);q=w*a;ss=q*e/(nu+q*e)
  cs=np.array([c0*ss**i for i in range(N)]+[c0*(q*e/nu)*ss**(N-1)])
  bs=a*e*cs[:N];T=sum(cs);Et=e+sum(bs);W=T+sum(bs);Rt=r+W;Mt=m+W;kap=nu*T/(r*m)
  J=np.zeros((2*N+1,2*N+1));h=-kap*(r+m)
  J[0,:]=h;J[0,0]-=nu+u*e;J[0,N+1:]+=u*cs[0];J[0,N+1]+=v
  for i in range(1,N):
   J[i,i]=-nu-u*e;J[i,N+1:]=u*cs[i];J[i,N+i]+=w;J[i,N+i+1]+=v
  J[N,N]=-nu;J[N,2*N]=w
  for i in range(N):
   J[N+1+i,i]=u*e;J[N+1+i,N+1:]=-u*cs[i];J[N+1+i,N+1+i]-=v+w
  vals=np.linalg.eigvals(J);scale=max(1,float(np.linalg.norm(J,ord=np.inf)));real=float(max(vals.real))
  row={'N':N,'trial':trial,'exponents':ex,'largest_real_part':real,'matrix_inf_norm':scale,'scaled_largest_real_part':real/scale}
  rows.append(row)
  if real>1e-8*scale:positive.append(row)
out={'status':'DIAGNOSTIC_ONLY','families':len(rows),'chain_lengths':[2,3,4,6,10,20,30],'positive_real_part_candidates':positive,'largest_scaled_real_part':max(x['scaled_largest_real_part'] for x in rows),'scope':'Eigenvalue sampling cannot prove global convergence, even if all sampled equilibria are locally stable','all_cases':rows}
Path(__file__).with_name('shared_stability_scan.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_cases'},indent=2))
