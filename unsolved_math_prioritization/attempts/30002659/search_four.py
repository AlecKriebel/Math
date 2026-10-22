"""Exploratory floating-point search; no exact feasibility or lower-bound certificate."""
import json
import numpy as np
import scipy
from scipy.optimize import minimize
from pathlib import Path


def vertices(z):
    a,b,c,d,e,f=z
    return np.array([[0.,0.,0.],[a,0.,0.],[b,c,0.],[d,e,f]])


def geometry(z):
    x=vertices(z)
    edge=np.roll(x,-1,axis=0)-x
    lengths=np.linalg.norm(edge,axis=1)
    u=edge/np.maximum(lengths[:,None],1e-14)
    v=np.roll(u,1,axis=0)-u
    nv=np.linalg.norm(v,axis=1)
    n=v/np.maximum(nv[:,None],1e-14)
    S=np.concatenate((x,x-n),axis=0)
    return x,S,lengths,nv


def constraints(z):
    x,S,l,nv=geometry(z)
    c=[1-np.dot(S[i]-S[j],S[i]-S[j]) for i in range(8) for j in range(i) if i!=j+4]
    return np.r_[c,l-1e-5,nv-1e-5]


def main():
    rng=np.random.default_rng(30002659)
    runs=[]
    for k in range(80):
        z=np.array([.6,.3,.5,.3,.15,.4]) if k==0 else np.r_[rng.uniform(.1,1),rng.uniform(-.5,.8),rng.uniform(.02,.7),rng.uniform(-.5,.8),rng.uniform(-.5,.8),rng.uniform(.02,.7)]
        r=minimize(lambda t:float(geometry(t)[2].sum()),z,method='SLSQP',bounds=[(1e-5,2),(-2,2),(1e-5,2),(-2,2),(-2,2),(1e-5,2)],constraints=[{'type':'ineq','fun':constraints}],options={'maxiter':600,'ftol':1e-11})
        x,S,l,nv=geometry(r.x)
        rec={'run':k,'success':bool(r.success),'message':str(r.message),'length':float(l.sum()),'minimum_constraint_slack':float(constraints(r.x).min()),'tetrahedron_six_volume':float(np.linalg.det(x[1:])),'coordinates':x.tolist()}
        runs.append(rec)
        if k%10==0: print(k,rec['length'],rec['minimum_constraint_slack'],flush=True)
    out={'description':'80 seeded SLSQP searches, floating point only. Edge lengths, normal differences, first in-plane altitude and out-of-plane height are bounded away from zero by 1e-5; these search restrictions are not theorem assumptions.','seed':30002659,'numpy':np.__version__,'scipy':scipy.__version__,'runs':runs}
    p=Path(__file__).with_name('search_four_results.json');p.write_text(json.dumps(out,indent=2)+'\n')
    feasible=[r for r in runs if r['minimum_constraint_slack']>=-1e-7]
    print(json.dumps({'feasible_diagnostics':len(feasible),'best':min(feasible,key=lambda r:r['length']) if feasible else None},indent=2))
if __name__=='__main__': main()
