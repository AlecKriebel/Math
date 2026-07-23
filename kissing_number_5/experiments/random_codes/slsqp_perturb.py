#!/usr/bin/env python3
"""Direct epigraph SQP from tangent perturbations, without smooth continuation."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parent))
import search_spherical5 as sc
import refine_spherical5 as rf
from analyze_refine_coordinates import read_coordinate_text

EVIDENCE_STATUS="NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
ap=argparse.ArgumentParser()
ap.add_argument("--input",required=True)
ap.add_argument("--seeds",type=int,nargs="+",required=True)
ap.add_argument("--out",required=True)
args=ap.parse_args()
input_path=Path(args.input)
x0=(np.load(input_path)["x"] if input_path.suffix==".npz"
    else read_coordinate_text(input_path)[0])
n=len(x0);g=x0@x0.T;ii,jj=sc.pairs(n)
mu0=float(np.max(g[ii,jj]));A=g>=mu0-1e-7;np.fill_diagonal(A,False);core=A.sum(1)>0
scales=(1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,.005,.02)
eq={"type":"eq","fun":lambda q:rf.sphere_equalities(q,n)[0],
    "jac":lambda q:rf.sphere_equalities(q,n)[1]}
iq={"type":"ineq","fun":lambda q:rf.pair_inequalities(q,n)[0],
    "jac":lambda q:rf.pair_inequalities(q,n)[1]}
runs=[];best=None
for seed in args.seeds:
    rng=np.random.default_rng(seed);scale=scales[seed%len(scales)]
    mode=("all","core")[seed%2];mask=np.ones(n,dtype=bool) if mode=="all" else core
    noise=rng.normal(size=(n,5));noise-=np.sum(noise*x0,1)[:,None]*x0;noise[~mask]=0
    x=sc.normalize(x0+scale*noise);mu=float(np.max((x@x.T)[ii,jj]))
    z=np.r_[x.ravel(),mu+1e-10]
    r=minimize(rf.epigraph_objective,z,args=(n,),jac=True,method="SLSQP",
      constraints=(eq,iq),options={"maxiter":1200,"ftol":1e-13,"disp":False})
    x=sc.normalize(r.x[:-1].reshape((n,5)));mu=float(np.max((x@x.T)[ii,jj]))
    rec={"seed":seed,"scale":scale,"mode":mode,"mu":mu,
         "nit":int(r.nit),"success":bool(r.success),"msg":str(r.message)}
    runs.append(rec);print(rec,flush=True)
    if best is None or mu<best[0]:
      best=(mu,seed,x.copy());np.savez(args.out+".npz",x=x)
with open(args.out+".json","w") as f:
 json.dump({"evidence_status":EVIDENCE_STATUS,
            "n":n,"mu0":mu0,"core_size":int(core.sum()),
            "best_mu":best[0],"best_seed":best[1],"runs":runs},f,indent=2)
print("BEST",best[0],best[1])
