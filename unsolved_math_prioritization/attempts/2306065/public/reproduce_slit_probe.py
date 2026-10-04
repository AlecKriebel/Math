#!/usr/bin/env python3
"""Exploratory reproduction; requires NumPy/SciPy. Results are not proof certificates."""
import numpy as np,json,math
from scipy.optimize import minimize
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
from pathlib import Path
x,w=leggauss(256);t=(x+1)/2;w=w/2

def vals(v):
 a,b,c=v
 Ds=np.sqrt((1-2*a*t+t*t)*(1-2*c*t+t*t));Dm=np.sqrt((1+2*a*t+t*t)*(1+2*c*t+t*t))
 pp=(1-2*b*t+t*t)/Ds;pm=(1+2*b*t+t*t)/Dm
 gp=np.dot(w,(pp-1)/t);gm=np.dot(w,(pm-1)/t)
 S=a+c; q1=S-2*b;q2=1.5*S*S-2*b*S-2*a*c
 return gp,gm,(q1*q1+q2)/2
out=[]
for M in [2.72,2.8,2.9,3.,3.25,3.5,4.,4.5,4.9]:
 best=None
 for init in [[.7,-.3,-.95],[.3,-.6,-.97],[.9,0,-.9],[.4,-.4,-.9]]:
  r=minimize(lambda v:-vals(v)[2],init,method='SLSQP',bounds=[(-.999999,.999999)]*3,constraints=[{'type':'eq','fun':lambda v:np.array(vals(v)[:2])-np.log(M)},{'type':'ineq','fun':lambda v:np.diff(-np.array(v))}],options={'ftol':1e-11,'maxiter':1000})
  if r.success and (best is None or r.fun<best.fun):best=r
 if best is not None: row={'M':M,'params':best.x.tolist(),'value':-best.fun,'constraint_residual':float(np.max(np.abs(np.array(vals(best.x)[:2])-np.log(M)))),'status':best.message}
 else:row={'M':M,'failed':True}
 if best is not None:
  a,b,c=best.x;checks=[]
  for sign in (1,-1):
   def integrand(t):
    if t==0:return sign*(a+c-2*b)
    return ((1-2*b*sign*t+t*t)/math.sqrt((1-2*a*sign*t+t*t)*(1-2*c*sign*t+t*t))-1)/t
   value,error=quad(integrand,0,1,epsabs=1e-11,epsrel=1e-11,limit=300)
   checks.append([value,error,value-math.log(M)])
  row['adaptive_check']=checks
 out.append(row);print(row,flush=True)
Path(__file__).with_name('slit-search.json').write_text(json.dumps({'quadrature_nodes':256,'exploratory_only':True,'rows':out},indent=2))
