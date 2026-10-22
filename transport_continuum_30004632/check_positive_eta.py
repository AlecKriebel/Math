import numpy as np
from math import tanh, ceil
def require(ok, message):
    if not ok: raise RuntimeError('MATHEMATICAL CHECK: '+message)
for eta in [0.1,0.5,1.,2.,5.]:
    r=1/tanh(1/eta);T=1/tanh(1/(2*eta))
    for n in [64,256,1024]:
        u=np.zeros(n);u[:n//2]=1.
        for k in range(ceil(T*n)):
            a=u[k%2:n-1:2];b=u[k%2+1:n:2]
            p=(a+b)/2
            # Stable equivalent of (r-sqrt(r*r-4*p*(1-p)))/2.
            f=2*p*(1-p)/(r+np.sqrt(r*r-4*p*(1-p)))
            a[:]=p-f;b[:]=p+f
            require(np.all(u>=-1e-12) and np.all(u<=1+1e-12), 'pair feasibility')
            require(abs(float(np.sum(u))/n-.5)<1e-10, 'mass conservation')
        U=np.concatenate(([0.],np.cumsum(u)/n));x=np.arange(n+1)/n
        require(np.max(np.abs(U-np.maximum(0,x-.5)))<.1, 'finite primitive residual sanity bound')
        print('eta',eta,'n',n,'T',T,'primitive_error',max(abs(U-np.maximum(0,x-.5))),'mass_error',abs(U[-1]-.5),flush=True)
