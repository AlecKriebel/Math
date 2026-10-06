"""Exploratory floating-point scan; it certifies no eigenvalue or derivative sign.
Needs NumPy and SciPy. Galerkin/quadrature/truncation errors are not enclosed.
Run with -B to avoid bytecode. Exact acceptance is certificate.py, not this file.
"""
import numpy as np
from scipy.special import roots_jacobi, eval_jacobi, gammaln
from scipy.linalg import eigh
from math import factorial

def spectrum(n,fun,J=55,Q=35):
 x,w=roots_jacobi(300,(n-2)/2,(n-2)/2)
 norm=(np.dot(w,fun(x)**(n/2))/sum(w))**(-2/n)
 vals=[]; mult=[]
 for q in range(Q+1):
  alpha=q+(n-2)/2
  x,w=roots_jacobi(max(2*J,150),alpha,alpha)
  P=np.array([eval_jacobi(j,alpha,alpha,x) for j in range(J)])
  P/=np.sqrt(np.sum(P*P*w,axis=1))[:,None]
  B=(P*(w*norm*fun(x)))@P.T
  ls=np.arange(J)+q
  A=np.diag(ls*(ls+n-1)+n*(n-2)/4)
  eig=eigh(A,B,eigvals_only=True)
  deg=(2*q+n-2)*factorial(q+n-3)//(factorial(q)*factorial(n-2))
  vals.extend(eig);mult.extend([deg]*len(eig))
 return np.array(vals),np.array(mult)

if __name__=='__main__':
 import json,sys
 records=[]
 modes=[0,1,2,3,4,6,8,12]
 for k in modes:
  for a in ([0] if k==0 else [.1,.5,1,2,4]):
   for J,Q in ([(55,35),(160,100)] if (k,a) in [(1,4),(2,2),(2,4),(4,1),(4,2),(4,4)] else [(55,35)]):
    fun=lambda x: np.exp(a*np.cos(k*np.arccos(x)))
    v,m=spectrum(4,fun,J,Q)
    out=[]
    for t in np.geomspace(.015,1,120):
     out.append((float(np.sum(m*(2-t*v)*np.exp(-t*v))*t),float(t)))
    mx=max(out)
    records.append({'n':4,'mode':k,'amplitude':a,'J':J,'Q':Q,'max_approx_derivative':mx[0],'time_at_max':mx[1]})
 data={'status':'exploratory_only','certified_signs':False,'warning':'No eigenvalue, quadrature, or omitted-tail error bounds. Positive coarse-truncation values are not counterexamples.','records':records}
 print(json.dumps(data,indent=2,sort_keys=True))
