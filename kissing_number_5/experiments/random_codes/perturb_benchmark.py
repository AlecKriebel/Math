#!/usr/bin/env python3
"""Basin-hopping perturbations around a supplied spherical-code benchmark."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parent))
import search_spherical5 as sc
from analyze_refine_coordinates import read_coordinate_text

EVIDENCE_STATUS="NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
def relax(x,method):
    n=len(x)
    if method=="hinge":
        for t in (.54,.52,.51,.50):
            for rep in range(2):
                r=minimize(sc.exact_hinge_fun_grad,x.ravel(),args=(n,t),jac=True,
                  method="L-BFGS-B",options={"maxiter":1200,"ftol":1e-16,
                  "gtol":1e-11,"maxls":70,"maxcor":40})
                x=sc.normalize(r.x)
    elif method=="power":
        for p in (8.,24.,64.):
            r=minimize(sc.power_energy_fun_grad,x.ravel(),args=(n,p),jac=True,
              method="L-BFGS-B",options={"maxiter":1000,"ftol":2e-15,
              "gtol":2e-9,"maxls":60,"maxcor":35})
            x=sc.normalize(r.x)
    for beta in (80.,250.,800.,2500.,6000.):
        r=minimize(sc.smoothmax_fun_grad,x.ravel(),args=(n,beta),jac=True,
          method="L-BFGS-B",options={"maxiter":1800,"ftol":2e-16,
          "gtol":3e-10,"maxls":70,"maxcor":40})
        x=sc.normalize(r.x)
    return x

ap=argparse.ArgumentParser()
ap.add_argument("--input",required=True)
ap.add_argument("--seeds",type=int,nargs="+",required=True)
ap.add_argument("--out",required=True)
args=ap.parse_args()
input_path=Path(args.input)
x0=(np.load(input_path)["x"] if input_path.suffix==".npz"
    else read_coordinate_text(input_path)[0])
n=len(x0);g=x0@x0.T
ii,jj=sc.pairs(n);mu=np.max(g[ii,jj]);A=g>=mu-1e-7;np.fill_diagonal(A,False)
core=A.sum(1)>0
scales=(1e-5,1e-4,1e-3,.004,.012,.035,.10,.25)
runs=[];best=None
for seed in args.seeds:
    rng=np.random.default_rng(seed)
    scale=scales[seed%len(scales)]
    mode=("all","core","rattlers")[seed%3]
    method=("smooth","hinge","power")[seed%3]
    mask=np.ones(n,dtype=bool) if mode=="all" else (core if mode=="core" else ~core)
    noise=rng.normal(size=(n,5));noise-=np.sum(noise*x0,axis=1)[:,None]*x0
    noise[~mask]=0
    x=sc.normalize(x0+scale*noise)
    # On larger rattler perturbations, replace them altogether.
    if mode=="rattlers" and scale>=.10:
        x[~core]=sc.normalize(rng.normal(size=((~core).sum(),5)))
    x=relax(x,method)
    mip=float(np.max((x@x.T)[sc.pairs(n)]))
    rec={"seed":seed,"scale":scale,"mode":mode,"method":method,"maxip":mip}
    runs.append(rec);print(rec,flush=True)
    if best is None or mip<best[0]:
        best=(mip,seed,x.copy());np.savez(args.out+".npz",x=x)
with open(args.out+".json","w") as f:
    json.dump({"evidence_status":EVIDENCE_STATUS,
               "n":n,"original_mu":float(mu),"core_size":int(core.sum()),
               "best_maxip":best[0],"best_seed":best[1],"runs":runs},f,indent=2)
print("BEST",best[0],best[1])
