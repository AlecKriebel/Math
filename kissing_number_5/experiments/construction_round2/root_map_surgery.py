#!/usr/bin/env python3
"""Low-rank map surgery on D6 and E6 roots (floating-point discovery only)."""
from __future__ import annotations
import argparse,json,math,importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

SPEC=importlib.util.spec_from_file_location('round2',Path(__file__).with_name('search_round2.py'))
R2=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(R2)


def mapped_fg(flat, roots, beta, squared=False):
    m=roots.shape[1];b=flat.reshape(m,5);raw=roots@b
    norms=np.linalg.norm(raw,axis=1);x=raw/norms[:,None]
    ii,jj=np.triu_indices(len(x),1);d=np.sum(x[ii]*x[jj],axis=1)
    if squared:
        # Projective-style energy is useful early even for a one-sided code:
        # it avoids collapsing antipodal source pairs under a rank drop.
        gap=np.maximum(1-d*d,1e-14);logs=-beta*np.log(gap)
        lm=np.max(logs);a=np.exp(logs-lm);w=a/a.sum()
        coeff=w*2*d/gap
        f=(lm+np.log(a.sum()))/beta
    else:
        z=beta*d;zm=np.max(z);a=np.exp(z-zm);w=a/a.sum();coeff=w
        f=(zm+np.log(a.sum()))/beta
    gx=np.zeros_like(x);np.add.at(gx,ii,coeff[:,None]*x[jj]);np.add.at(gx,jj,coeff[:,None]*x[ii])
    radial=np.sum(gx*x,axis=1);graw=(gx-radial[:,None]*x)/norms[:,None]
    gb=roots.T@graw
    return float(f),gb.ravel()


def optimize_map(roots,b0):
    b=b0.copy();hist=[]
    for p in (2.,4.,8.,16.,32.):
        r=minimize(mapped_fg,b.ravel(),args=(roots,p,True),jac=True,method='L-BFGS-B',
                   options={'maxiter':800,'ftol':3e-15,'gtol':3e-9,'maxls':50,'maxcor':30})
        b=r.x.reshape(b.shape);x=R2.unit_rows(roots@b)
        hist.append(['projective_energy',p,R2.max_ip(x),int(r.nit),bool(r.success)])
    for beta in (40.,120.,360.,1080.,3240.,9720.):
        r=minimize(mapped_fg,b.ravel(),args=(roots,beta,False),jac=True,method='L-BFGS-B',
                   options={'maxiter':1400,'ftol':3e-16,'gtol':2e-10,'maxls':70,'maxcor':35})
        b=r.x.reshape(b.shape);x=R2.unit_rows(roots@b)
        hist.append(['one_sided_smoothmax',beta,R2.max_ip(x),int(r.nit),bool(r.success)])
    return b,R2.unit_rows(roots@b),hist


def root_family(name):
    if name=='D6':
        x=R2.d_roots(6)
    elif name=='E6':
        x=R2.e6_roots()
    else:raise ValueError(name)
    base=np.flatnonzero(np.abs(x[:,5])<1e-13)
    extra=np.flatnonzero(np.abs(x[:,5])>=1e-13)
    assert len(base)==40
    return x,base,extra


def one(name,n,seed):
    allr,base,extra=root_family(name);rng=np.random.default_rng(seed)
    k=1+seed%min(15,len(extra)-(n-40))
    kept=np.delete(base,rng.choice(len(base),k,replace=False))
    add=rng.choice(extra,n-40+k,replace=False)
    ids=np.r_[kept,add];roots=allr[ids]
    b=np.zeros((6,5));b[:5]=np.eye(5)
    b += (.002,.02,.08,.25)[seed%4]*rng.normal(size=b.shape)
    b,x,hist=optimize_map(roots,b)
    # Deliberately release the common-map constraint at the end.
    xf,fullhist=R2.refine_full(x,betas=(300.,1200.,4800.,19200.,76800.))
    # Graph-targeted realization is applied independently and retained only
    # when the true recomputed maximum improves.
    xg,gh=R2.graph_realize(xf,target_degree=7+seed%5,outer=3)
    if R2.max_ip(xg)<R2.max_ip(xf):out=xg;chosen='graph'
    else:out=xf;chosen='full_minimax'
    out,sqp=R2.epigraph_slsqp(out)
    return {'family':name,'n':n,'seed':seed,'removed_base':int(k),
            'root_indices':ids.tolist(),'map':b.tolist(),'map_history':hist,
            'full_history':fullhist,'graph_history':gh,'chosen':chosen,
            'final_epigraph_slsqp':sqp,
            'diagnostics':R2.diagnostics(out),'coordinates':out.tolist()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--family',nargs='+',default=['D6','E6'])
    ap.add_argument('--n',nargs='+',type=int,default=[41,42,43,44]);ap.add_argument('--seeds',nargs='+',type=int,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();runs=[]
    for fam in a.family:
      for n in a.n:
       for seed in a.seeds:
        r=one(fam,n,seed);runs.append(r);print(fam,n,seed,r['removed_base'],r['diagnostics']['maxip'],flush=True)
    a.out.write_text(json.dumps({'status':'NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE','runs':runs},indent=2)+'\n')
if __name__=='__main__':main()
