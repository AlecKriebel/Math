#!/usr/bin/env python3
"""Deterministic cosine-Galerkin illustrations for the all-spectrum family.

The simulations are not used in any proof.  Because the reaction field is
quadratic, mode products are evaluated by the exact cosine convolution and
then truncated at the chosen Galerkin order.
"""
from __future__ import annotations
import argparse, json, sys, shutil
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'independent_verifier'))
from core import d_seed, r_seed, ell_seed, Hsum, ell_Dr_formula, ell_r_formula, cubic_num_formula

@dataclass(frozen=True)
class Config:
    m:int
    mu:float
    modes:int
    tfinal:float
    precision:str='base'
    rtol:float=2e-8
    atol:float=2e-10
    initial_fraction:float=.85
    samples:int=181

def cosine_product(a:np.ndarray,b:np.ndarray)->np.ndarray:
    """Coefficients of the Galerkin projection of two cosine series."""
    K=len(a)-1
    out=.5*np.convolve(a,b)[:K+1]
    diff=np.empty(K+1,dtype=float)
    diff[0]=np.dot(a,b)
    for k in range(1,K+1):
        diff[k]=np.dot(a[k:],b[:-k])+np.dot(a[:-k],b[k:])
    return out+.5*diff

def reaction_coefficients(m:int,C:np.ndarray)->np.ndarray:
    out=np.zeros_like(C); x1=C[0]; xm=C[m-1]; z=C[m]
    one=np.zeros(C.shape[1]); one[0]=1.
    out[0]=one-cosine_product(x1,C[m-2])+cosine_product(z,z)-cosine_product(x1,xm)
    out[1]=-cosine_product(x1,C[1])+cosine_product(xm,xm)
    for i in range(2,m-1):
        out[i]=cosine_product(x1,C[i-1])-cosine_product(x1,C[i])
    out[m-1]=2*cosine_product(x1,C[m-2])-2*cosine_product(xm,xm)+cosine_product(z,z)-cosine_product(x1,xm)
    out[m]=-2*cosine_product(z,z)+2*cosine_product(x1,xm)
    return out

def coefficients(m:int):
    h=Hsum(m); er=ell_r_formula(m,h); ed=ell_Dr_formula(m,h)
    return float(ed/er),float(cubic_num_formula(m,h)/er)

def evaluate(C:np.ndarray,grid:np.ndarray)->np.ndarray:
    return C@np.cos(np.outer(np.arange(C.shape[1]),grid))

def simulate(cfg:Config,outdir:Path):
    n=cfg.m+1; K=cfg.modes
    D=np.array([float(x) for x in d_seed(cfg.m)])
    r=np.array([float(x) for x in r_seed(cfg.m)]).ravel()
    ell=np.array([float(x) for x in ell_seed(cfg.m)]).ravel()
    eta,cubic=coefficients(cfg.m); pred=np.sqrt(-eta*cfg.mu/cubic)
    C0=np.zeros((n,K+1)); C0[:,0]=1.; C0[:,1]=cfg.initial_fraction*pred*r
    k2=np.arange(K+1,dtype=float)**2
    diff=(1-cfg.mu)*D
    def rhs(t,y):
        C=y.reshape(n,K+1)
        return (reaction_coefficients(cfg.m,C)-diff[:,None]*k2[None,:]*C).ravel()
    sol=solve_ivp(rhs,(0,cfg.tfinal),C0.ravel(),method='BDF',
                  t_eval=np.linspace(0,cfg.tfinal,cfg.samples),rtol=cfg.rtol,atol=cfg.atol)
    if not sol.success: raise RuntimeError(sol.message)
    grid=np.linspace(0,np.pi,257)
    amps=[]; mins=[]
    for col in range(sol.y.shape[1]):
        C=sol.y[:,col].reshape(n,K+1)
        amps.append(float(ell@C[:,1]/(ell@r)))
        mins.append(float(evaluate(C,grid).min()))
    C=sol.y[:,-1].reshape(n,K+1); X=evaluate(C,grid); meas=amps[-1]
    outdir.mkdir(parents=True,exist_ok=True)
    mutag=str(cfg.mu).replace('.','p')
    tag=f'm{cfg.m}_mu{mutag}_K{K}_{cfg.precision}'
    pd.DataFrame({'time':sol.t,'amplitude':amps,'minimum_concentration':mins}).to_csv(outdir/f'amplitude_{tag}.csv',index=False)
    prof={'x':grid}
    for i in range(cfg.m): prof[f'X{i+1}']=X[i]
    prof['Z']=X[-1]; pd.DataFrame(prof).to_csv(outdir/f'profile_{tag}.csv',index=False)
    meta={'method':'cosine Galerkin method of lines','config':asdict(cfg),
          'predicted_amplitude':float(pred),'measured_amplitude':float(meas),
          'relative_error':float(abs(abs(meas)-pred)/pred),
          'minimum_concentration':float(X.min()),'eta':eta,'cubic':cubic,
          'diffusion':diff.tolist(),'nfev':sol.nfev,'message':sol.message,
          'max_omitted_mode_proxy':float(np.max(np.abs(C[:,-2:]))) if K>=2 else 0.}
    (outdir/f'parameters_{tag}.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta

def _simulate_pair(item):
    cfg,outdir=item
    return simulate(cfg,outdir)

def configs_full():
    out=[]
    for m,times in [(3,(6000,4200,2800)),(5,(8000,5200,3400))]:
        out += [
          Config(m,.0025,16,times[0]),
          Config(m,.005,16,times[1]),
          Config(m,.005,32,times[1],precision='spatial-fine'),
          Config(m,.005,16,times[1],precision='time-tight',rtol=5e-10,atol=5e-12),
          Config(m,.01,16,times[2]),
        ]
    out.append(Config(8,.005,16,6800))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--outdir',type=Path,default=ROOT/'data'/'simulations')
    ap.add_argument('--quick',action='store_true')
    ap.add_argument('--jobs',type=int,default=1)
    args=ap.parse_args()
    configs=[Config(3,.005,8,900,rtol=1e-6,atol=1e-8,samples=31)] if args.quick else configs_full()
    if args.jobs>1 and len(configs)>1:
        with ProcessPoolExecutor(max_workers=args.jobs) as ex:
            results=list(ex.map(_simulate_pair,[(c,args.outdir) for c in configs]))
    else:
        results=[simulate(c,args.outdir) for c in configs]
    (args.outdir/'simulation_summary.json').write_text(json.dumps(results,indent=2)+'\n')
    rows=[]
    for r in results:
        c=r['config']; rows.append({'m':c['m'],'mu':c['mu'],'modes':c['modes'],'precision':c['precision'],
          'predicted_amplitude':r['predicted_amplitude'],'measured_amplitude':abs(r['measured_amplitude']),
          'relative_error':r['relative_error'],'minimum_concentration':r['minimum_concentration']})
    df=pd.DataFrame(rows); df.to_csv(ROOT/'data'/'branch_amplitudes.csv',index=False)
    if not args.quick:
        for m in (3,5):
            tag=f'm{m}_mu0p005_K32_spatial-fine'
            shutil.copyfile(args.outdir/f'profile_{tag}.csv',args.outdir/f'profile_m{m}_modes32.csv')
        refs=[]
        for m in (3,5):
            base=df[(df.m==m)&(df.mu==.005)&(df.modes==16)&(df.precision=='base')].iloc[0]
            spatial=df[(df.m==m)&(df.mu==.005)&(df.modes==32)].iloc[0]
            temporal=df[(df.m==m)&(df.mu==.005)&(df.precision=='time-tight')].iloc[0]
            refs.append({'m':m,'mu':.005,'comparison':'spatial','base_modes':16,'refined_modes':32,
              'base_amplitude':base.measured_amplitude,'refined_amplitude':spatial.measured_amplitude,
              'relative_difference':abs(base.measured_amplitude-spatial.measured_amplitude)/abs(spatial.measured_amplitude)})
            refs.append({'m':m,'mu':.005,'comparison':'temporal_tolerance','base_rtol':2e-8,'refined_rtol':5e-10,
              'base_amplitude':base.measured_amplitude,'refined_amplitude':temporal.measured_amplitude,
              'relative_difference':abs(base.measured_amplitude-temporal.measured_amplitude)/abs(temporal.measured_amplitude)})
        pd.DataFrame(refs).to_csv(ROOT/'data'/'refinement_checks.csv',index=False)
        (ROOT/'data'/'simulation_parameters.json').write_text(json.dumps([asdict(c) for c in configs],indent=2)+'\n')
    print('SIMULATIONS_PASS')
    for r in results:
        c=r['config']; print(c['m'],c['mu'],c['modes'],c['precision'],r['relative_error'])
if __name__=='__main__': main()
