#!/usr/bin/env python3
"""High-beta and epigraph-SLSQP refinements of discovered spherical codes."""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import search_spherical5 as sc

EVIDENCE_STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"

def epigraph_objective(z, n):
    f = z[-1]
    grad = np.zeros_like(z)
    grad[-1] = 1.0
    return f, grad


def sphere_equalities(z, n):
    x = z[:-1].reshape((n, 5))
    vals = np.sum(x*x, axis=1) - 1.0
    jac = np.zeros((n, len(z)))
    for i in range(n):
        jac[i, 5*i:5*i+5] = 2*x[i]
    return vals, jac


def pair_inequalities(z, n):
    x = z[:-1].reshape((n, 5))
    t = z[-1]
    ii, jj = sc.pairs(n)
    vals = t - np.sum(x[ii]*x[jj], axis=1)
    jac = np.zeros((len(ii), len(z)))
    rows = np.arange(len(ii))
    for k in range(5):
        jac[rows, 5*ii+k] = -x[jj, k]
        jac[rows, 5*jj+k] = -x[ii, k]
    jac[:, -1] = 1.0
    return vals, jac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--slsqp", action="store_true")
    args = ap.parse_args()
    x = np.load(args.input)["x"]
    n = len(x)
    hist = []
    for beta in (4000., 8000., 16000., 32000., 64000., 128000.):
        res = minimize(sc.smoothmax_fun_grad, x.ravel(), args=(n,beta), jac=True,
                       method="L-BFGS-B",
                       options={"maxiter": 3000, "maxfun": 30000, "ftol": 1e-16,
                                "gtol": 2e-11, "maxls": 80, "maxcor": 50})
        x = sc.normalize(res.x)
        mu = float(np.max((x@x.T)[sc.pairs(n)]))
        hist.append(["smooth", beta, mu, int(res.nit), str(res.message)])
        print(hist[-1], flush=True)
    if args.slsqp:
        mu = float(np.max((x@x.T)[sc.pairs(n)]))
        z = np.r_[x.ravel(), mu + 1e-10]
        eq = {"type":"eq", "fun":lambda q: sphere_equalities(q,n)[0],
              "jac":lambda q: sphere_equalities(q,n)[1]}
        iq = {"type":"ineq", "fun":lambda q: pair_inequalities(q,n)[0],
              "jac":lambda q: pair_inequalities(q,n)[1]}
        res = minimize(epigraph_objective, z, args=(n,), jac=True,
                       method="SLSQP", constraints=(eq,iq),
                       options={"maxiter":3000, "ftol":1e-13,"disp":True})
        x = sc.normalize(res.x[:-1].reshape((n,5)))
        mu = float(np.max((x@x.T)[sc.pairs(n)]))
        hist.append(["slsqp", float(res.fun), mu, int(res.nit), str(res.message)])
        print(hist[-1], flush=True)
    result={"n":n,"seed":-1,"kind":"loaded","mode":"refine","maxip":
            float(np.max((x@x.T)[sc.pairs(n)])),"x":x,"history":hist}
    np.savez(args.out+".npz", x=x)
    with open(args.out+".json","w") as f:
        json.dump({"evidence_status":EVIDENCE_STATUS,
                   "metadata":{k:result[k] for k in ("n","maxip")},
                   "analysis":sc.analyze(result),"history":hist},f,indent=2)
    print(json.dumps(sc.analyze(result),indent=2))


if __name__=="__main__":
    main()
