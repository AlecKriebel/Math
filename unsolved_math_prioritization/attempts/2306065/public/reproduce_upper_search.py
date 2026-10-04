#!/usr/bin/env python3
"""Exploratory reproduction; requires NumPy/SciPy. Results are not proof certificates."""
import numpy as np,json
from fractions import Fraction as F
from scipy.optimize import linprog
from pathlib import Path
N=40;J=100;intervals=64; U=1.098613
xs=np.arange(-J,J+1)/J;C=np.polynomial.chebyshev.chebvander(xs,N)[:,1:];ns=np.arange(1,N+1);wt=1-ns/(N+1)
A=np.vstack([-C*(wt*ns),C*wt]);B=np.r_[np.ones(len(xs)),np.full(len(xs),U)];rows=[]
for k in range(intervals):
 lo=4*k/(3*intervals);hi=4*(k+1)/(3*intervals);obj=np.zeros(N);obj[0]=(lo+hi)/2;obj[1]=1
 bound=[(lo,hi)]+[(-2/n,2/n) for n in ns[1:]]
 r=linprog(-obj,A_ub=A,b_ub=B,bounds=bound,method='highs')
 if not r.success:print('failed',k,r.message);continue
 upper=-r.fun-lo*hi/2
 rows.append({'k':k,'upper_approx':float(upper),'inequality_dual':(-r.ineqlin.marginals).tolist(),'lower_dual':r.lower.marginals.tolist(),'upper_dual':(-r.upper.marginals).tolist()})
print('maxupper',max(x['upper_approx'] for x in rows),flush=True)
Path(__file__).with_name('upper-search.json').write_text(json.dumps({'N':N,'grid_denominator':J,'intervals':intervals,'L_upper_numerator':1098613,'L_upper_denominator':1000000,'rows':rows},indent=2))
