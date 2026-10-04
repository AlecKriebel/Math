import numpy as np
from scipy.optimize import differential_evolution
from numpy.polynomial.legendre import leggauss
X,W=leggauss(128);X=(X+1)/2;W=W/2

def measure(x):
    beta=x[0]; ang=np.array(x[1:4]); raw=np.array([x[4],x[5],1.]);w=raw/sum(raw);u=np.exp(1j*ang)
    d=np.exp(-beta*np.sum(w*np.log(1-u)))
    q=np.sum(W*np.exp(-beta*np.sum(w*np.log(1-X[:,None]*u),axis=1)))
    a=abs(d)**2;b=4*abs(q)**2;c=2*(d*np.conj(q)).imag
    sv2=max(0,(a+b-np.hypot(a-b,2*c))/2)
    return np.sqrt(sv2)*2**beta
if __name__=='__main__':
  bounds=[(.001,1.999),(.001,2*np.pi-.001),(.001,2*np.pi-.001),(.001,2*np.pi-.001),(0,10),(0,10)]
  for seed in range(4):
    r=differential_evolution(measure,bounds,popsize=14,maxiter=200,tol=1e-10,seed=seed,polish=True);print(seed,r.fun,r.x,flush=True)
