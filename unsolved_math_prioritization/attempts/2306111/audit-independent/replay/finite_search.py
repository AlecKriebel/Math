"""Finite floating-point experiments only; not a proof or an exhaustive search."""
import json, platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import differential_evolution
from numpy.polynomial.legendre import leggauss

def sigma(d,q):
    a=abs(d)**2;b=4*abs(q)**2;c=2*(d*np.conj(q)).imag
    # Stable smaller Gram eigenvalue: determinant divided by larger eigenvalue.
    det=4*(d*np.conj(q)).real**2
    return np.sqrt(max(0,2*det/(a+b+np.hypot(a-b,2*c))))

def evaluate(b,beta,x,order=128):
    ang=np.array(x[:3]); raw=np.array([x[3],x[4],1.]);w=raw/sum(raw);u=np.exp(1j*ang)
    X,W=QUADS[order]
    d=np.exp(-beta*np.sum(w*np.log(1-b*u)))
    q=np.sum(W*np.exp(-beta*np.sum(w*np.log(1-b*X[:,None]*u),axis=1)))
    return float(sigma(d,q)*(1+b)**beta)
QUADS={}
for order in [128,256]:
    X,W=leggauss(order);QUADS[order]=((X+1)/2,W/2)
bounds=[(.001,2*np.pi-.001)]*3+[(0,10)]*2
rows=[]
for b in [.94,.97,1.]:
 for beta in [.1,.5,1.,1.5,1.9]:
    seed=2306111+len(rows)
    obj=lambda x:evaluate(b,beta,x)
    r=differential_evolution(obj,bounds,popsize=10,maxiter=160,tol=1e-9,seed=seed,polish=True,workers=1)
    row={'b':b,'B':-b,'A':b*(beta-1),'beta':beta,'seed':seed,'nfev':r.nfev,'optimizer_success':bool(r.success),'minimum_ratio_128':float(r.fun),'recheck_ratio_256':evaluate(b,beta,r.x,256),'parameters':r.x.tolist()}
    rows.append(row);print(json.dumps(row),flush=True)
result={'purpose':'Seek strict counterexamples within a restricted three-atom family at z=1; no certificate or global optimization claim.','versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'limits':{'b_values':3,'beta_values':5,'atoms':3,'angle_interval':[.001,2*np.pi-.001],'raw_weight_bounds':[0,10],'third_raw_weight':1,'quadrature_order':128,'recheck_order':256,'optimizer':'scipy differential_evolution','population_multiplier':10,'maxiter':160,'tol':1e-9,'polish':True,'workers':1,'interval_arithmetic':False},'rows':rows,'strict_counterexamples_below_1_minus_1e_7':sum(r['recheck_ratio_256']<1-1e-7 for r in rows)}
Path(__file__).with_name('FINITE_SEARCH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
