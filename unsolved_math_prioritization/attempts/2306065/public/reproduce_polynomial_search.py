#!/usr/bin/env python3
"""Exploratory reproduction; requires NumPy/SciPy. Results are not proof certificates."""
import numpy as np,json
from scipy.optimize import linprog
from pathlib import Path
N=40; J=2000; L=1.098; ns=np.arange(1,N+1); th=np.linspace(0,np.pi,J+1); C=np.cos(th[:,None]*ns[None,:]); A=np.vstack([C,-C*ns]); rhs=np.r_[np.full(J+1,L),np.ones(J+1)]; obj=np.zeros(N);obj[1]=-1
best=(-100,None)
rows=[]
for a in np.linspace(0,4/3,101):
 bounds=[(-2/n,2/n) for n in ns];bounds[0]=(a,a)
 r=linprog(obj,A_ub=A,b_ub=rhs,bounds=bounds,method='highs')
 if r.success:
  val=r.x[1]+a*a/2;rows.append([float(a),float(val)])
  if val>best[0]:best=(val,r.x.copy())
print('best',best[0],best[1][0],flush=True)
D=Path(__file__).parent
(D/'polynomial-search.json').write_text(json.dumps({'N':N,'J':J,'L':L,'best':best[0],'coefficients':best[1].tolist(),'scan':rows},indent=2))
