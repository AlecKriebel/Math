import numpy as np, sys, time
src=open('equality_probe.py').read().split("rng=np.random.default_rng")[0]
exec(src)
from scipy.optimize import minimize
rng=np.random.default_rng(int(sys.argv[1]))
alpha=np.array([1,-1,1.]); 
for t in range(int(sys.argv[2])):
    c=np.zeros((3,3,2,2))
    betaB=np.array([1,-1,1.]) if t%2==0 else np.array([1,-1,-1.])
    for (x,y,s) in [(0,0,1),(0,1,1),(1,0,1),(1,1,-1)]:
        c[:,:,x,y]+=10*s*np.outer(alpha,betaB)
    c+=rng.normal(size=c.shape)*(1.0 if t<3 else 0.3)
    pb=pvm_bound(c)
    best=-1e9
    for rst in range(30):
        p0=rng.normal(size=2*nA*8+2*nB*8)
        r=minimize(lambda p:-povm_val(p,c),p0,method='BFGS',options={'gtol':1e-10,'maxiter':800})
        best=max(best,-r.fun)
    print(f"chsh-like test {t}: PVM bound {pb:.9f}  POVM search {best:.9f}  diff {best-pb:+.2e}",flush=True)
