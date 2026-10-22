#!/usr/bin/env python3
"""Optional finite-box heuristic search. No completeness or certification claim.
Used NumPy2.3.5 and SciPy1.17.0; seeded outputs may vary across library versions.
Coefficients are scaled by sqrt(2**k*k!), with four coordinates in [-5,5].
"""
import numpy as np,json,math
from scipy.optimize import differential_evolution
from numpy.polynomial.hermite import hermroots
from pathlib import Path
rows=[]
for n,m in [(2,3),(2,4),(2,5),(3,4),(3,5),(4,5),(4,6),(5,6),(2,10),(5,10),(9,10),(10,11),(10,20),(19,20),(20,30)]:
 sn=math.sqrt(2**n*math.factorial(n));sm=math.sqrt(2**m*math.factorial(m))
 def roots(v):
  c=np.zeros(m+1,dtype=complex);c[0]=c[1]=1;c[n]=(v[0]+1j*v[1])/sn;c[m]=(v[2]+1j*v[3])/sm
  return hermroots(c)
 def objective(v):
  try: return -float(min(abs(roots(v).imag)))
  except: return 0
 r=differential_evolution(objective,[(-5,5)]*4,seed=2304006+n*100+m,popsize=10,maxiter=160,tol=1e-8,polish=False)
 rr=roots(r.x); row={'n':n,'m':m,'scaled_parameters':r.x.tolist(),'a':[(r.x[0]/sn),(r.x[1]/sn)],'b':[(r.x[2]/sm),(r.x[3]/sm)],'min_abs_imag':-r.fun,'roots':[[x.real,x.imag] for x in rr],'nfev':r.nfev}; rows.append(row)
 print(n,m,-r.fun,flush=True)
 Path(__file__).with_name('numerical_exploration.json').write_text(json.dumps(rows,indent=2)+'\n')
