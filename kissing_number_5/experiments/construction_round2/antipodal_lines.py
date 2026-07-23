#!/usr/bin/env python3
"""Numerical search for 21 or 22 unoriented lines in R^5 of coherence <= 1/2.

If successful, adjoining both signs would give 42 or 44 kissing points.
This is discovery code only; ordinary floating-point output is not a proof.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize


def normalize(y):
    y = y.reshape((-1, 5))
    return y/np.linalg.norm(y, axis=1)[:, None]


def pairs(n):
    return np.triu_indices(n, 1)


def abs_smoothmax_fg(flat, n, beta):
    y = flat.reshape(n, 5)
    norms = np.linalg.norm(y, axis=1)
    x = y/norms[:, None]
    ii, jj = pairs(n)
    d = np.sum(x[ii]*x[jj], axis=1)
    vals = np.r_[d, -d]
    z = beta*vals
    zm = np.max(z)
    e = np.exp(z-zm)
    w = e/np.sum(e)
    coeff = w[:len(d)]-w[len(d):]
    gx = np.zeros_like(x)
    np.add.at(gx, ii, coeff[:, None]*x[jj])
    np.add.at(gx, jj, coeff[:, None]*x[ii])
    radial = np.sum(gx*x,axis=1)
    gy=(gx-radial[:,None]*x)/norms[:,None]
    return float((zm+np.log(np.sum(e)))/beta),gy.ravel()


def projective_energy_fg(flat,n,power):
    y=flat.reshape(n,5); norms=np.linalg.norm(y,axis=1);x=y/norms[:,None]
    ii,jj=pairs(n);d=np.sum(x[ii]*x[jj],axis=1)
    gap=np.maximum(1-d*d,1e-14)
    logs=-power*np.log(gap); lm=np.max(logs);a=np.exp(logs-lm);w=a/a.sum()
    # derivative of log sum(gap^-p)/p = 2d/gap times softmax weights
    coeff=w*2*d/gap
    gx=np.zeros_like(x);np.add.at(gx,ii,coeff[:,None]*x[jj]);np.add.at(gx,jj,coeff[:,None]*x[ii])
    radial=np.sum(gx*x,axis=1);gy=(gx-radial[:,None]*x)/norms[:,None]
    return float((lm+np.log(a.sum()))/power),gy.ravel()


def sqp_refine(x):
    x=normalize(x);n=len(x);ii,jj=pairs(n);mu=float(np.max(np.abs((x@x.T)[ii,jj])))
    z=np.r_[x.ravel(),mu+1e-9]
    def obj(q):
        g=np.zeros_like(q);g[-1]=1;return float(q[-1]),g
    def eq(q):
        y=q[:-1].reshape(n,5);v=np.sum(y*y,axis=1)-1
        jac=np.zeros((n,len(q)))
        for i in range(n):jac[i,5*i:5*i+5]=2*y[i]
        return v,jac
    def iq(q):
        y=q[:-1].reshape(n,5);t=q[-1];d=np.sum(y[ii]*y[jj],axis=1)
        v=np.r_[t-d,t+d];jac=np.zeros((2*len(ii),len(q)));rows=np.arange(len(ii))
        for k in range(5):
            jac[rows,5*ii+k]=-y[jj,k];jac[rows,5*jj+k]=-y[ii,k]
            jac[len(ii)+rows,5*ii+k]=y[jj,k];jac[len(ii)+rows,5*jj+k]=y[ii,k]
        jac[:,-1]=1
        return v,jac
    cons=({'type':'eq','fun':lambda q:eq(q)[0],'jac':lambda q:eq(q)[1]},
          {'type':'ineq','fun':lambda q:iq(q)[0],'jac':lambda q:iq(q)[1]})
    r=minimize(obj,z,jac=True,method='SLSQP',constraints=cons,
               options={'maxiter':2500,'ftol':5e-14,'disp':False})
    xx=normalize(r.x[:-1]);mup=float(np.max(np.abs((xx@xx.T)[ii,jj])))
    return xx,{'mu':mup,'nit':int(r.nit),'success':bool(r.success),'message':str(r.message)}


def d5_lines():
    out=[]
    for i in range(5):
        for j in range(i+1,5):
            for b in (-1.,1.):
                v=np.zeros(5);v[i]=1/math.sqrt(2);v[j]=b/math.sqrt(2);out.append(v)
    return np.asarray(out)


def initial(n,seed,kind):
    rng=np.random.default_rng(seed)
    if kind=='random':
        return normalize(rng.normal(size=(n,5)))
    if kind=='d5plus':
        base=d5_lines()
        x=np.vstack((base,normalize(rng.normal(size=(n-20,5)))))
        scale=(0.,1e-4,.003,.03,.12)[seed%5]
        return normalize(x+scale*rng.normal(size=x.shape))
    if kind=='d5surgery':
        base=d5_lines(); k=1+seed%8
        keep=np.ones(20,dtype=bool);keep[rng.choice(20,k,replace=False)]=False
        x=np.vstack((base[keep],normalize(rng.normal(size=(n-20+k,5)))))
        scale=(.001,.01,.05,.2)[seed%4]
        return normalize(x+scale*rng.normal(size=x.shape))
    raise ValueError(kind)


def one(n,seed,kind):
    x=initial(n,seed,kind);hist=[]
    for p in (1.,2.,4.,8.,16.,32.,64.,128.):
        r=minimize(projective_energy_fg,x.ravel(),args=(n,p),jac=True,method='L-BFGS-B',
                   options={'maxiter':1000,'ftol':3e-16,'gtol':2e-10,'maxls':60,'maxcor':35})
        x=normalize(r.x); hist.append(['energy',p,float(np.max(np.abs((x@x.T)[pairs(n)]))),int(r.nit)])
    for beta in (80.,240.,720.,2160.,6480.,19440.):
        r=minimize(abs_smoothmax_fg,x.ravel(),args=(n,beta),jac=True,method='L-BFGS-B',
                   options={'maxiter':1600,'ftol':3e-16,'gtol':2e-10,'maxls':70,'maxcor':40})
        x=normalize(r.x);hist.append(['smooth',beta,float(np.max(np.abs((x@x.T)[pairs(n)]))),int(r.nit)])
    x,sq=sqp_refine(x);g=x@x.T;ii,jj=pairs(n);d=np.abs(g[ii,jj]);mu=float(d.max())
    active=np.abs(d-mu)<1e-7
    deg=np.zeros(n,dtype=int)
    np.add.at(deg,ii[active],1);np.add.at(deg,jj[active],1)
    ev=np.linalg.eigvalsh(g)
    return {'line_count':n,'point_count':2*n,'seed':seed,'kind':kind,'mu':mu,'gap':mu-.5,
            'sqp':sq,'history':hist,'active_pairs_1e-7':int(active.sum()),
            'degree_histogram':{str(int(v)):int(np.sum(deg==v)) for v in np.unique(deg)},
            'frame_eigenvalues':ev[-5:].tolist(),'coordinates':x.tolist()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--line-count',type=int,nargs='+',default=[21,22])
    ap.add_argument('--seeds',type=int,nargs='+',required=True)
    ap.add_argument('--kinds',nargs='+',default=['random'])
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();runs=[]
    for n in a.line_count:
        for kind in a.kinds:
          for seed in a.seeds:
            r=one(n,seed,kind);runs.append(r);print(n,kind,seed,r['mu'],flush=True)
    a.out.write_text(json.dumps({'status':'NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE','runs':runs},indent=2)+'\n')

if __name__=='__main__':main()
