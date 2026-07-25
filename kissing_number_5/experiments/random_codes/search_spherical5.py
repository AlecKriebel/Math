#!/usr/bin/env python3
"""Deterministic numerical construction search for one-sided spherical codes.

Discovery code only: floating point output is not a certificate.
"""
import argparse
import json
import math
import os
import time

import numpy as np
from scipy.optimize import minimize

EVIDENCE_STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"

def normalize(y):
    y = y.reshape((-1, 5))
    n = np.linalg.norm(y, axis=1, keepdims=True)
    return y / n


def pairs(n):
    return np.triu_indices(n, 1)


def smoothmax_fun_grad(yflat, n, beta):
    y = yflat.reshape((n, 5))
    norms = np.linalg.norm(y, axis=1)
    x = y / norms[:, None]
    ii, jj = pairs(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    z = beta * s
    zmax = np.max(z)
    ez = np.exp(z - zmax)
    weights = ez / np.sum(ez)
    f = (zmax + math.log(np.sum(ez))) / beta
    gx = np.zeros_like(x)
    np.add.at(gx, ii, weights[:, None] * x[jj])
    np.add.at(gx, jj, weights[:, None] * x[ii])
    radial = np.sum(gx * x, axis=1)
    gy = (gx - radial[:, None] * x) / norms[:, None]
    return f, gy.ravel()


def softplus_hinge_fun_grad(yflat, n, threshold, beta):
    """Mean squared softplus(beta*(dot-threshold))/beta."""
    y = yflat.reshape((n, 5))
    norms = np.linalg.norm(y, axis=1)
    x = y / norms[:, None]
    ii, jj = pairs(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    z = beta * (s - threshold)
    # Stable softplus and sigmoid.
    sp = np.maximum(z, 0.0) + np.log1p(np.exp(-np.abs(z)))
    sig = np.empty_like(z)
    pos = z >= 0
    sig[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    sig[~pos] = ez / (1.0 + ez)
    vals = sp / beta
    f = np.mean(vals * vals)
    ds = (2.0 / len(s)) * vals * sig
    gx = np.zeros_like(x)
    np.add.at(gx, ii, ds[:, None] * x[jj])
    np.add.at(gx, jj, ds[:, None] * x[ii])
    radial = np.sum(gx * x, axis=1)
    gy = (gx - radial[:, None] * x) / norms[:, None]
    return f, gy.ravel()


def exact_hinge_fun_grad(yflat, n, threshold):
    """Mean squared positive-part violation: nonsmooth only at threshold."""
    y = yflat.reshape((n, 5))
    norms = np.linalg.norm(y, axis=1)
    x = y / norms[:, None]
    ii, jj = pairs(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    v = np.maximum(s-threshold, 0.0)
    f = np.mean(v*v)
    ds = 2.0*v/len(s)
    gx = np.zeros_like(x)
    np.add.at(gx, ii, ds[:, None]*x[jj])
    np.add.at(gx, jj, ds[:, None]*x[ii])
    radial = np.sum(gx*x, axis=1)
    gy = (gx-radial[:,None]*x)/norms[:,None]
    return f, gy.ravel()


def power_energy_fun_grad(yflat, n, power):
    """Riesz-like energy sum (1-dot)^(-power), logarithmically scaled."""
    y = yflat.reshape((n, 5))
    norms = np.linalg.norm(y, axis=1)
    x = y / norms[:, None]
    ii, jj = pairs(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    d = np.maximum(1.0 - s, 1e-14)
    logs = -power * np.log(d)
    lm = np.max(logs)
    a = np.exp(logs - lm)
    asum = np.sum(a)
    f = (lm + np.log(asum)) / power
    # f is log(sum d^-p)/p, derivative weights / d.
    ds = (a / asum) / d
    gx = np.zeros_like(x)
    np.add.at(gx, ii, ds[:, None] * x[jj])
    np.add.at(gx, jj, ds[:, None] * x[ii])
    radial = np.sum(gx * x, axis=1)
    gy = (gx - radial[:, None] * x) / norms[:, None]
    return f, gy.ravel()


def d5():
    out = []
    for i in range(5):
        for j in range(i + 1, 5):
            for a in (-1.0, 1.0):
                for b in (-1.0, 1.0):
                    v = np.zeros(5)
                    v[i] = a / math.sqrt(2)
                    v[j] = b / math.sqrt(2)
                    out.append(v)
    return np.array(out)


def initial(n, seed, kind):
    rng = np.random.default_rng(seed)
    if kind == "random":
        return normalize(rng.normal(size=(n, 5)))
    if kind == "d5plus":
        base = d5()
        if n <= 40:
            return base[:n].copy()
        extra = normalize(rng.normal(size=(n - 40, 5)))
        # Break symmetry throughout, but only slightly.
        return normalize(np.vstack((base, extra)) + 0.03 * rng.normal(size=(n, 5)))
    if kind == "d5surgery":
        base = d5()
        # Excise a seed-dependent patch and replace it by one extra point beyond
        # the number excised (or N-40 extras generally), explicitly breaking D5.
        k = 1 + (seed % 12)
        keep = np.ones(40, dtype=bool)
        keep[rng.choice(40, size=k, replace=False)] = False
        extra = normalize(rng.normal(size=(n-(40-k), 5)))
        scale = (0.01, 0.04, 0.10)[seed % 3]
        return normalize(np.vstack((base[keep], extra)) +
                         scale*rng.normal(size=(n,5)))
    if kind == "delete":
        # Optimize a somewhat larger random cloud softly, then delete worst points.
        m = n + 5
        y = normalize(rng.normal(size=(m, 5)))
        for p in (1.0, 2.0, 4.0, 8.0):
            res = minimize(
                power_energy_fun_grad, y.ravel(), args=(m, p), jac=True,
                method="L-BFGS-B", options={"maxiter": 300, "ftol": 1e-12,
                                            "gtol": 1e-8, "maxls": 30})
            y = normalize(res.x)
        while len(y) > n:
            g = y @ y.T
            np.fill_diagonal(g, -np.inf)
            # Delete the point with greatest exponential local crowding.
            beta = 30.0
            crowd = np.sum(np.exp(beta * (g - np.max(g))), axis=1)
            y = np.delete(y, int(np.argmax(crowd)), axis=0)
        return y
    raise ValueError(kind)


def optimize_one(n, seed, kind, mode):
    y = initial(n, seed, kind)
    history = []
    if mode == "exacthinge":
        for threshold in (.70,.64,.59,.55,.525,.510,.500):
            # Repetition matters because the active set changes discontinuously.
            for repeat in range(3):
                res = minimize(
                    exact_hinge_fun_grad, y.ravel(), args=(n,threshold), jac=True,
                    method="L-BFGS-B",
                    options={"maxiter":1600,"ftol":1e-16,"gtol":1e-11,
                             "maxls":80,"maxcor":40})
                y=normalize(res.x)
                history.append(["exacthinge",[threshold,repeat],
                    float(np.max((y@y.T)[pairs(n)])),int(res.nit),bool(res.success)])
        for beta in (40.,120.,400.,1200.,4000.):
            res=minimize(smoothmax_fun_grad,y.ravel(),args=(n,beta),jac=True,
                method="L-BFGS-B",options={"maxiter":1600,"ftol":2e-16,
                "gtol":3e-10,"maxls":60,"maxcor":30})
            y=normalize(res.x)
            history.append(["smoothmax",beta,
                float(np.max((y@y.T)[pairs(n)])),int(res.nit),bool(res.success)])
    if mode in ("power", "hybrid"):
        for power in (2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
            res = minimize(
                power_energy_fun_grad, y.ravel(), args=(n, power), jac=True,
                method="L-BFGS-B",
                options={"maxiter": 600, "ftol": 2e-15, "gtol": 2e-9, "maxls": 40})
            y = normalize(res.x)
            history.append(["power", power, float(np.max((y @ y.T)[pairs(n)])),
                            int(res.nit), bool(res.success)])
    if mode in ("hinge", "hybrid"):
        # The threshold continuation keeps pressure on all near-worst pairs.
        current = float(np.max((y @ y.T)[pairs(n)]))
        thresholds = [current - q for q in (0.03, 0.02, 0.012, 0.007, 0.004)]
        thresholds += [0.505, 0.500]
        for threshold in thresholds:
            for beta in (30.0, 80.0, 200.0):
                res = minimize(
                    softplus_hinge_fun_grad, y.ravel(),
                    args=(n, threshold, beta), jac=True, method="L-BFGS-B",
                    options={"maxiter": 700, "ftol": 1e-16, "gtol": 1e-10, "maxls": 50})
                y = normalize(res.x)
                history.append(["hinge", [threshold, beta],
                                float(np.max((y @ y.T)[pairs(n)])),
                                int(res.nit), bool(res.success)])
    if mode in ("smoothmax", "hybrid"):
        for beta in (20.0, 50.0, 120.0, 300.0, 800.0, 2000.0):
            res = minimize(
                smoothmax_fun_grad, y.ravel(), args=(n, beta), jac=True,
                method="L-BFGS-B",
                options={"maxiter": 1200, "ftol": 2e-16, "gtol": 3e-10, "maxls": 60,
                         "maxcor": 30})
            y = normalize(res.x)
            history.append(["smoothmax", beta, float(np.max((y @ y.T)[pairs(n)])),
                            int(res.nit), bool(res.success)])
    gram = y @ y.T
    maxip = float(np.max(gram[pairs(n)]))
    return {"n": n, "seed": seed, "kind": kind, "mode": mode,
            "maxip": maxip, "x": y, "history": history}


def analyze(result):
    x = result["x"]
    n = len(x)
    g = x @ x.T
    vals = np.linalg.eigvalsh(g)
    off = g[pairs(n)]
    mu = np.max(off)
    # Counts are intentionally at several numerical tolerances.
    counts = {str(tol): int(np.sum(off >= mu - tol))
              for tol in (1e-3, 1e-4, 1e-5, 1e-6)}
    degs = {}
    for tol in (1e-4, 1e-5):
        adj = (g >= mu - tol)
        np.fill_diagonal(adj, False)
        d = np.sum(adj, axis=1).astype(int)
        degs[str(tol)] = d.tolist()
    return {
        "maxip": float(mu),
        "top_inner_products": np.sort(off)[-30:][::-1].tolist(),
        "gram_eigenvalues": vals.tolist(),
        "near_contact_counts": counts,
        "near_contact_degrees": degs,
        "norm_errors_max": float(np.max(np.abs(np.sum(x*x, axis=1)-1))),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seeds", type=int, nargs="+", required=True)
    ap.add_argument("--kinds", nargs="+", default=["random"])
    ap.add_argument("--mode", choices=["power", "hinge", "smoothmax", "hybrid",
                                      "exacthinge"],
                    default="hybrid")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    best = None
    summaries = []
    start = time.time()
    for kind in args.kinds:
        for seed in args.seeds:
            r = optimize_one(args.n, seed, kind, args.mode)
            summaries.append({k: r[k] for k in ("n", "seed", "kind", "mode", "maxip")})
            print(json.dumps(summaries[-1]), flush=True)
            if best is None or r["maxip"] < best["maxip"]:
                best = r
                np.savez(args.out + ".npz", x=best["x"])
                with open(args.out + ".json", "w") as f:
                    json.dump({
                        "evidence_status": EVIDENCE_STATUS,
                        "metadata": {k: best[k] for k in ("n", "seed", "kind", "mode", "maxip")},
                        "analysis": analyze(best), "history": best["history"],
                        "all_runs": summaries, "elapsed_seconds": time.time()-start,
                    }, f, indent=2)
    # Rewrite once at completion so all non-winning runs are also retained.
    with open(args.out + ".json", "w") as f:
        json.dump({
            "evidence_status": EVIDENCE_STATUS,
            "metadata": {k: best[k] for k in ("n", "seed", "kind", "mode", "maxip")},
            "analysis": analyze(best), "history": best["history"],
            "all_runs": summaries, "elapsed_seconds": time.time()-start,
        }, f, indent=2)
    print("BEST", json.dumps({k: best[k] for k in ("n", "seed", "kind", "mode", "maxip")}))
    print(json.dumps(analyze(best), indent=2))


if __name__ == "__main__":
    main()
