#!/usr/bin/env python3
"""Deterministic, non-certified Rayleigh--Ritz counterexample search.

NumPy/SciPy, FFT trapezoidal quadrature. Values are NOT rigorous enclosures.
Actual continuous integrals would give variational upper bounds, not lower bounds.
"""
import json, math, os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from scipy.linalg import eigvalsh
from scipy.optimize import minimize
from pathlib import Path

class Ritz:
    def __init__(self,a,b,N=3,G=96):
        self.a,self.b,self.N,self.G=a,b,N,G
        self.k=np.array([(m,n) for m in range(-N,N+1) for n in range(-N,N+1) if m or n])
        self.dm=(self.k[:,None,0]-self.k[None,:,0])%G
        self.dn=(self.k[:,None,1]-self.k[None,:,1])%G
        self.q=self.k[:,0]+1j*(self.k[:,1]-a*self.k[:,0])/b
        u,v=np.meshgrid(np.arange(G)/G,np.arange(G)/G,indexing='ij')
        self.u,self.v=u,v
        self.modes=np.array([np.cos(2*np.pi*u),np.cos(2*np.pi*v),np.cos(2*np.pi*(u+v)),np.cos(2*np.pi*(u-v)),np.cos(4*np.pi*v),np.sin(2*np.pi*(u+v))])
    def value_f(self,f):
        f=f/math.sqrt(np.mean(f*f))
        F=np.fft.fft2(f)/(self.G*self.G)
        R=np.fft.fft2(1/f)/(self.G*self.G)
        A=(2*np.pi)**2*np.conj(self.q[:,None])*self.q[None,:]*R[self.dm,self.dn]
        z=F[self.k[:,0]%self.G,self.k[:,1]%self.G]
        B=F[self.dm,self.dn]-np.outer(z,z.conj())/F[0,0]
        A=(A+A.conj().T)/2;B=(B+B.conj().T)/2
        lam2=float(eigvalsh(A,B,subset_by_index=[0,0],check_finite=False)[0])
        return math.sqrt(max(lam2,0)*self.b)
    def value(self,c):
        return self.value_f(np.exp(np.tensordot(c,self.modes,axes=1)))

def main():
    controls=[]
    for a,b in [(0,1),(0.5,math.sqrt(3)/2),(0.4,2),(0.2,math.pi),(0,4),(0.5,7)]:
        r=Ritz(a,b);v=r.value(np.zeros(6));exact=2*np.pi/math.sqrt(b)
        if abs(v-exact)>1e-10: raise RuntimeError('flat formula failed')
        controls.append({'a':a,'b':b,'computed':v,'exact':exact})
    # Analytic one-dimensional family from Approach 3; truncation N=10.
    oned=[]
    for a,b,e in [(0,2,0.3),(0.4,3.2,0.7),(0.5,4,0.8)]:
        r=Ritz(a,b,N=8,G=192)
        val=r.value_f(1+e*np.cos(2*np.pi*r.v))
        exact=2*np.pi/math.sqrt(b)*math.sqrt(1+e*e/2)
        if val < exact-1e-9 or abs(val-exact)>2e-7:raise RuntimeError('one-dimensional control failed')
        oned.append({'a':a,'b':b,'epsilon':e,'ritz':val,'exact':exact})
    rng=np.random.default_rng(30005600)
    results=[]
    for a,b in [(0,1),(0.5,math.sqrt(3)/2),(0.25,2),(0,math.pi),(0.5,math.pi),(0.25,4),(0,6)]:
        r=Ritz(a,b)
        trials=[(r.value(np.zeros(6)),np.zeros(6),'flat')]
        for amplitude in [0.25,0.75,1.5]:
            for j in range(12):
                c=rng.normal(size=6);c*=amplitude/np.linalg.norm(c)
                trials.append((r.value(c),c,f'random_{amplitude}_{j}'))
        for amp in [0.5,1,2,3]:
            c=np.array([amp,amp,0,0,0,0],float)
            trials.append((r.value(c),c,f'bump_{amp}'))
        nonflat=sorted(trials[1:],key=lambda x:x[0])
        opt=[]
        for st in nonflat[:2]:
            z=minimize(r.value,st[1],method='L-BFGS-B',bounds=[(-3,3)]*6,
                       options={'maxiter':70,'ftol':1e-11,'gtol':2e-6})
            opt.append({'value':float(z.fun),'c':z.x.tolist(),'success':bool(z.success),'nfev':int(z.nfev)})
        candidates=[{'value':t[0],'c':t[1].tolist(),'kind':t[2]} for t in trials]+opt
        best=min(candidates,key=lambda x:x['value'])
        # Record the best genuinely nonflat sample independently of flat convergence.
        bn=nonflat[0]
        refined=[]
        for N,G in [(4,128),(6,192)]:
            rr=Ritz(a,b,N=N,G=G)
            refined.append({'N':N,'G':G,'value':rr.value(np.array(best['c'])),'nonflat_value':rr.value(bn[1])})
        results.append({'a':a,'b':b,'target':min(2*np.pi/math.sqrt(b),2*math.sqrt(np.pi)),
                        'samples':len(trials),'best':best,'best_nonflat_sample':{'value':bn[0],'c':bn[1].tolist(),'kind':bn[2]},
                        'optimization':opt,'refinement':refined})
        print(json.dumps(results[-1]),flush=True)
    out={'status':'numerical evidence only; no interval certification','seed':30005600,
         'basis_N':3,'quadrature_G':96,'flat_controls':controls,'one_dimensional_controls':oned,'search':results}
    dest=Path(__file__).with_name('SEARCH_RESULTS.json');dest.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
