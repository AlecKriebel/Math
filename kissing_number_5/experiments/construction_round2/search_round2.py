#!/usr/bin/env python3
"""Independent numerical construction search for spherical (5,N,1/2) codes.

Discovery only.  Every coordinate and solver result is floating point.

This program explores three mechanisms deliberately different from a plain
random soft-max sweep:

1. rank-five projections of D6/E6/E7 roots, alternating a discrete
   maximum-compatible-subset problem with continuous kernel optimization;
2. latitude-layer seeds based on D4 roots/cross-polytopes/simplexes, followed
   by both layer-constrained and fully symmetry-broken minimax refinement;
3. graph-targeted low-rank realization, in which a proposed contact graph is
   held close to inner product 1/2 while nonedges are penalized only when they
   violate the desired threshold.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp, minimize
from scipy.sparse import coo_matrix


def unit_rows(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x, axis=1)
    if np.min(n) < 1e-12:
        raise ValueError("zero row")
    return x / n[:, None]


def offdiag(x: np.ndarray) -> np.ndarray:
    return (x @ x.T)[np.triu_indices(len(x), 1)]


def max_ip(x: np.ndarray) -> float:
    return float(np.max(offdiag(unit_rows(x))))


def d_roots(d: int) -> np.ndarray:
    out = []
    for i in range(d):
        for j in range(i + 1, d):
            for a in (-1.0, 1.0):
                for b in (-1.0, 1.0):
                    v = np.zeros(d)
                    v[i] = a
                    v[j] = b
                    out.append(v / math.sqrt(2.0))
    return np.asarray(out)


def e6_roots() -> np.ndarray:
    # Forty D5 roots in the first five coordinates.
    out = []
    for r in d_roots(5):
        out.append(np.r_[r, 0.0])
    # Thirty-two half-roots.  In unnormalised root coordinates these are
    # (eps_1,...,eps_5,sqrt(3)eps_6)/2 with product eps_i = +1.
    for mask in range(1 << 5):
        eps = np.asarray([1.0 if (mask >> i) & 1 else -1.0 for i in range(5)])
        eps6 = float(np.prod(eps))
        r = np.r_[eps / 2.0, eps6 * math.sqrt(3.0) / 2.0]
        out.append(r / math.sqrt(2.0))
    x = np.asarray(out)
    assert x.shape == (72, 6)
    assert np.max(offdiag(x)) < 0.500000000001
    return x


def e8_roots() -> np.ndarray:
    out = []
    for i in range(8):
        for j in range(i + 1, 8):
            for a in (-1.0, 1.0):
                for b in (-1.0, 1.0):
                    v = np.zeros(8)
                    v[i], v[j] = a, b
                    out.append(v / math.sqrt(2.0))
    for mask in range(1 << 8):
        # Standard E8 convention: even number of minus signs.
        eps = np.asarray([1.0 if (mask >> i) & 1 else -1.0 for i in range(8)])
        if np.prod(eps) > 0:
            out.append(eps / math.sqrt(8.0))
    x = np.asarray(out)
    assert x.shape == (240, 8)
    return x


def e7_roots() -> np.ndarray:
    # E7 is the E8 subsystem perpendicular to e_1+e_2.  Compress that
    # seven-dimensional hyperplane using an orthonormal basis.
    x = e8_roots()
    keep = np.abs(x[:, 0] + x[:, 1]) < 1e-12
    x = x[keep]
    normal = np.asarray([1.0, 1.0, 0, 0, 0, 0, 0, 0]) / math.sqrt(2)
    q, _ = np.linalg.qr(np.column_stack([normal, np.eye(8)[:, 2:]]))
    # QR's first vector spans normal; use an SVD nullspace to avoid depending
    # on a particular QR completion.
    _, _, vh = np.linalg.svd(normal.reshape(1, 8))
    basis = vh[1:].T
    y = x @ basis
    assert y.shape == (126, 7)
    assert np.max(np.abs(np.sum(y * y, axis=1) - 1)) < 1e-12
    assert np.max(offdiag(y)) < 0.500000000001
    return y


def projection_from_kernel(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    q, _ = np.linalg.qr(kernel)
    residual = x - (x @ q) @ q.T
    return unit_rows(residual)


def max_compatible_subset(y: np.ndarray, threshold: float = 0.5,
                          time_limit: float = 20.0) -> dict:
    """Solve maximum compatible subset as a 0-1 MILP.

    A violating pair supplies x_i+x_j <= 1.  HiGHS reports a rigorous
    combinatorial optimum only relative to the binary64 graph supplied to it;
    this remains discovery evidence because graph construction uses floats.
    """
    g = y @ y.T
    ii, jj = np.where(np.triu(g > threshold + 2e-12, 1))
    m, n = len(ii), len(y)
    rows = np.repeat(np.arange(m), 2)
    cols = np.column_stack((ii, jj)).ravel()
    data = np.ones(2 * m)
    a = coo_matrix((data, (rows, cols)), shape=(m, n)).tocsr()
    c = -np.ones(n)
    res = milp(c, integrality=np.ones(n),
               bounds=Bounds(np.zeros(n), np.ones(n)),
               constraints=LinearConstraint(a, -np.inf, np.ones(m)),
               options={"time_limit": time_limit, "mip_rel_gap": 0.0})
    if res.x is None:
        return {"size": 0, "indices": [], "status": int(res.status),
                "gap": None, "violations": m}
    chosen = np.flatnonzero(res.x > 0.5)
    return {"size": int(len(chosen)), "indices": chosen.tolist(),
            "status": int(res.status),
            "gap": float(getattr(res, "mip_gap", math.nan)),
            "violations": int(m)}


def projected_softmax_kernel(root_x: np.ndarray, chosen: np.ndarray,
                             kernel0: np.ndarray,
                             betas=(100.0, 400.0, 1600.0, 6400.0)):
    """Optimize a kernel subspace for a fixed subset."""
    m = root_x.shape[1]
    k = kernel0.shape[1]
    sel = root_x[chosen]
    tri = np.triu_indices(len(sel), 1)

    def fg(z, beta):
        # Finite differences are intentional here: dimensions are only 6 or
        # 14 and QR makes a clean analytic derivative cumbersome.
        ker = z.reshape(m, k)
        y = projection_from_kernel(sel, ker)
        s = (y @ y.T)[tri]
        zeta = beta * s
        zmax = np.max(zeta)
        f = (zmax + np.log(np.sum(np.exp(zeta - zmax)))) / beta
        return float(f)

    z = kernel0.ravel().copy()
    hist = []
    for beta in betas:
        res = minimize(fg, z, args=(beta,), method="Nelder-Mead",
                       options={"maxiter": 1800, "xatol": 2e-10,
                                "fatol": 2e-12, "adaptive": True})
        z = res.x
        ker = z.reshape(m, k)
        y = projection_from_kernel(sel, ker)
        hist.append({"beta": beta, "maxip": max_ip(y),
                     "nit": int(res.nit), "success": bool(res.success)})
    return z.reshape(m, k), y, hist


def root_projection_search(family: str, seeds: list[int],
                           rounds: int = 2) -> list[dict]:
    roots = {"D6": d_roots(6), "E6": e6_roots(), "E7": e7_roots()}[family]
    k = roots.shape[1] - 5
    results = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        ker = rng.normal(size=(roots.shape[1], k))
        trial = {"family": family, "seed": seed, "alternations": []}
        for rep in range(rounds):
            yall = projection_from_kernel(roots, ker)
            clique = max_compatible_subset(yall, time_limit=15.0)
            entry = {"round": rep, "subset": clique}
            if clique["size"] < 6:
                trial["alternations"].append(entry)
                break
            chosen = np.asarray(clique["indices"], dtype=int)
            # If more than 44 survive, retain 44 points having least local
            # crowding, then optimize that fixed set.
            if len(chosen) > 44:
                g = yall[chosen] @ yall[chosen].T
                np.fill_diagonal(g, -np.inf)
                crowd = np.sort(g, axis=1)[:, -8:].sum(axis=1)
                chosen = chosen[np.argsort(crowd)[:44]]
            ker, y, hist = projected_softmax_kernel(roots, chosen, ker)
            entry["optimized_size"] = int(len(chosen))
            entry["optimized_maxip"] = max_ip(y)
            entry["history"] = hist
            entry["indices_optimized"] = chosen.tolist()
            trial["alternations"].append(entry)
        # Final graph after continuous adjustment.
        yall = projection_from_kernel(roots, ker)
        final = max_compatible_subset(yall, time_limit=30.0)
        trial["final_subset"] = final
        trial["kernel"] = ker.tolist()
        trial["final_all_maxip"] = max_ip(yall)
        results.append(trial)
    return results


def d4_roots() -> np.ndarray:
    return d_roots(4)


def cross4() -> np.ndarray:
    return np.vstack((np.eye(4), -np.eye(4)))


def simplex4() -> np.ndarray:
    # Five vertices in the four-dimensional sum-zero hyperplane, expressed in
    # an arbitrary orthonormal basis.
    a = np.eye(5) - np.ones((5, 5)) / 5
    _, _, vh = np.linalg.svd(np.ones((1, 5)) / math.sqrt(5))
    b = vh[1:].T
    return unit_rows(a @ b)


def random_so4(rng: np.random.Generator) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(4, 4)))
    q *= np.sign(np.diag(r))[None, :]
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def layer_seed(pattern: tuple[int, ...], seed: int) -> tuple[np.ndarray, dict]:
    """Build latitude layers using structured S^3 seeds.

    Supported layer sizes select deterministic subsets of D4 roots, a cross
    polytope, repeated simplex blocks, or a one-point pole.  Heights are
    spread and every block receives an independent SO(4) rotation.
    """
    rng = np.random.default_rng(seed)
    blocks = []
    meta = []
    levels = np.linspace(-0.72, 0.72, len(pattern))
    for li, (count, z) in enumerate(zip(pattern, levels)):
        if count == 1:
            base = np.zeros((1, 4))
            z = -1.0 if li == 0 else 1.0
        elif count <= 5:
            base = simplex4()[:count]
        elif count <= 8:
            base = cross4()[:count]
        elif count <= 24:
            # Seed-dependent, deliberately asymmetric subset ordering.
            dr = d4_roots()
            order = rng.permutation(len(dr))
            base = dr[order[:count]]
        else:
            raise ValueError(count)
        if count == 1:
            x = np.c_[base, np.full(count, z)]
        else:
            rot = random_so4(rng)
            base = base @ rot
            x = np.c_[math.sqrt(max(0.0, 1-z*z)) * base,
                      np.full(count, z)]
        blocks.append(x)
        meta.append({"count": count, "initial_height": float(z)})
    x = unit_rows(np.vstack(blocks))
    # Break all residual exact orbit symmetry before unrestricted refinement.
    x = unit_rows(x + 0.012 * rng.normal(size=x.shape))
    return x, {"pattern": list(pattern), "layers": meta}


def smoothmax_fg(flat: np.ndarray, n: int, beta: float):
    y = flat.reshape(n, 5)
    norms = np.linalg.norm(y, axis=1)
    x = y / norms[:, None]
    ii, jj = np.triu_indices(n, 1)
    s = np.sum(x[ii] * x[jj], axis=1)
    z = beta * s
    zm = float(np.max(z))
    w = np.exp(z - zm)
    w /= np.sum(w)
    f = (zm + math.log(np.sum(np.exp(z-zm)))) / beta
    gx = np.zeros_like(x)
    np.add.at(gx, ii, w[:, None] * x[jj])
    np.add.at(gx, jj, w[:, None] * x[ii])
    radial = np.sum(gx*x, axis=1)
    gy = (gx-radial[:, None]*x)/norms[:, None]
    return float(f), gy.ravel()


def refine_full(x0: np.ndarray,
                betas=(80., 240., 720., 2160., 6480., 19440.)):
    x = unit_rows(x0)
    hist = []
    for beta in betas:
        res = minimize(smoothmax_fg, x.ravel(), args=(len(x), beta), jac=True,
                       method="L-BFGS-B",
                       options={"maxiter": 1400, "ftol": 5e-16,
                                "gtol": 2e-10, "maxls": 70, "maxcor": 35})
        x = unit_rows(res.x.reshape(-1, 5))
        hist.append({"beta": beta, "maxip": max_ip(x), "nit": int(res.nit),
                     "success": bool(res.success)})
    return x, hist


def epigraph_slsqp(x0: np.ndarray, maxiter: int = 4000):
    """Direct minimax refinement with exact unit equalities (binary64 SQP)."""
    x = unit_rows(x0)
    n = len(x)
    ii, jj = np.triu_indices(n, 1)
    mu = float(np.max((x @ x.T)[ii, jj]))
    q0 = np.r_[x.ravel(), mu + 1e-9]

    def objective(q):
        gradient = np.zeros_like(q)
        gradient[-1] = 1.0
        return float(q[-1]), gradient

    def equalities(q):
        y = q[:-1].reshape(n, 5)
        values = np.sum(y*y, axis=1)-1.0
        jacobian = np.zeros((n, len(q)))
        for i in range(n):
            jacobian[i, 5*i:5*i+5] = 2*y[i]
        return values, jacobian

    def inequalities(q):
        y = q[:-1].reshape(n, 5)
        values = q[-1]-np.sum(y[ii]*y[jj], axis=1)
        jacobian = np.zeros((len(ii), len(q)))
        rows = np.arange(len(ii))
        for coordinate in range(5):
            jacobian[rows, 5*ii+coordinate] = -y[jj, coordinate]
            jacobian[rows, 5*jj+coordinate] = -y[ii, coordinate]
        jacobian[:, -1] = 1.0
        return values, jacobian

    constraints = (
        {"type": "eq", "fun": lambda q: equalities(q)[0],
         "jac": lambda q: equalities(q)[1]},
        {"type": "ineq", "fun": lambda q: inequalities(q)[0],
         "jac": lambda q: inequalities(q)[1]},
    )
    result = minimize(
        objective, q0, jac=True, method="SLSQP", constraints=constraints,
        options={"maxiter": maxiter, "ftol": 5e-14, "disp": False},
    )
    y = unit_rows(result.x[:-1].reshape(n, 5))
    return y, {
        "maxip": max_ip(y),
        "epigraph_value": float(result.fun),
        "nit": int(result.nit),
        "success": bool(result.success),
        "message": str(result.message),
    }


def graph_realize(x0: np.ndarray, target_degree: int = 8,
                  outer: int = 6) -> tuple[np.ndarray, list[dict]]:
    """Alternate graph selection and fixed-graph realization at t=1/2.

    The graph is selected from the `target_degree` nearest angular neighbours.
    Its edges are attracted to exactly 1/2; all pair violations are penalized.
    Then a short high-beta minimax stage rebalances the active set.
    """
    x = unit_rows(x0)
    n = len(x)
    ii, jj = np.triu_indices(n, 1)
    hist = []
    for rep in range(outer):
        g = x @ x.T
        np.fill_diagonal(g, -np.inf)
        edge = np.zeros((n, n), dtype=bool)
        for i in range(n):
            near = np.argpartition(g[i], -target_degree)[-target_degree:]
            edge[i, near] = True
        edge |= edge.T
        eij = edge[ii, jj]

        def fg(flat):
            y = flat.reshape(n, 5)
            norms = np.linalg.norm(y, axis=1)
            z = y/norms[:, None]
            dots = np.sum(z[ii]*z[jj], axis=1)
            # Equality penalty on proposed contacts plus a substantially
            # stronger positive-part penalty on every violation.
            de = dots[eij]-0.5
            viol = np.maximum(dots-0.5, 0)
            weights = np.zeros_like(dots)
            weights[eij] += 2.0*de/max(1, np.sum(eij))
            weights += 40.0*2.0*viol/len(dots)
            f = (np.mean(de*de) if len(de) else 0.0) + \
                40.0*np.mean(viol*viol)
            gz = np.zeros_like(z)
            np.add.at(gz, ii, weights[:, None]*z[jj])
            np.add.at(gz, jj, weights[:, None]*z[ii])
            radial = np.sum(gz*z, axis=1)
            gy = (gz-radial[:, None]*z)/norms[:, None]
            return float(f), gy.ravel()

        res = minimize(fg, x.ravel(), jac=True, method="L-BFGS-B",
                       options={"maxiter": 1800, "ftol": 1e-16,
                                "gtol": 1e-11, "maxls": 80, "maxcor": 40})
        x = unit_rows(res.x.reshape(n, 5))
        x, short = refine_full(x, betas=(1200., 4800., 19200.))
        hist.append({"round": rep, "graph_edges": int(np.sum(eij)),
                     "post_realize_maxip": max_ip(x),
                     "realize_nit": int(res.nit), "minimax": short})
    return x, hist


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    n = len(x)
    g = x @ x.T
    ii, jj = np.triu_indices(n, 1)
    s = g[ii, jj]
    mu = float(np.max(s))
    ev = np.linalg.eigvalsh(g)
    ans = {
        "n": n,
        "maxip": mu,
        "gap_above_half": mu-0.5,
        "norm_error": float(np.max(np.abs(np.sum(x*x, axis=1)-1))),
        "gram_eigenvalues_top5": ev[-5:].tolist(),
        "gram_eigenvalue_abs_below_top5": float(np.max(np.abs(ev[:-5]))),
        "coordinate_sha256": hashlib.sha256(
            np.asarray(x, dtype="<f8").tobytes()).hexdigest(),
        "thresholds": {},
    }
    for tol in (1e-4, 1e-6, 1e-8):
        adj = g >= mu-tol
        np.fill_diagonal(adj, False)
        deg = np.sum(adj, axis=1).astype(int)
        unique, counts = np.unique(deg, return_counts=True)
        # components
        unseen = set(range(n))
        comps = []
        while unseen:
            stack = [unseen.pop()]
            size = 0
            while stack:
                i = stack.pop()
                size += 1
                nbr = set(np.flatnonzero(adj[i])) & unseen
                unseen -= nbr
                stack.extend(nbr)
            comps.append(size)
        ans["thresholds"][str(tol)] = {
            "pairs": int(np.sum(adj)//2),
            "degree_histogram": {str(int(a)): int(b)
                                 for a, b in zip(unique, counts)},
            "components": sorted(comps, reverse=True),
        }
    ans["top_inner_products"] = np.sort(s)[-25:][::-1].tolist()
    return ans


def layer_search(ns: list[int], seeds: list[int]) -> list[dict]:
    patterns = {
        41: [(24, 9, 8), (8, 8, 8, 8, 8, 1),
             (5, 5, 5, 5, 5, 5, 5, 5, 1), (16, 8, 8, 8, 1)],
        42: [(24, 9, 9), (8, 8, 8, 8, 8, 1, 1),
             (5, 5, 5, 5, 5, 5, 5, 5, 1, 1), (16, 9, 8, 8, 1)],
        43: [(24, 10, 9), (8, 8, 8, 8, 8, 3),
             (5, 5, 5, 5, 5, 5, 5, 5, 3), (16, 9, 9, 8, 1)],
        44: [(24, 10, 10), (8, 8, 8, 8, 8, 4),
             (5, 5, 5, 5, 5, 5, 5, 5, 4), (16, 10, 9, 8, 1)],
    }
    out = []
    for n in ns:
        for pi, pat in enumerate(patterns[n]):
            for seed in seeds:
                x0, meta = layer_seed(pat, seed+100003*pi+1009*n)
                x, hist = refine_full(x0)
                # Only graph-refine the best-looking mechanism from each
                # pattern/seed; graph realization is materially more costly.
                xg, gh = graph_realize(x, target_degree=8+(seed % 3), outer=3)
                if max_ip(xg) < max_ip(x):
                    x, chosen = xg, "graph"
                else:
                    chosen = "minimax"
                x, final_sqp = epigraph_slsqp(x)
                out.append({"n": n, "pattern_index": pi, "seed": seed,
                            "meta": meta, "minimax_history": hist,
                            "graph_history": gh, "chosen": chosen,
                            "final_epigraph_slsqp": final_sqp,
                            "diagnostics": diagnostics(x),
                            "coordinates": x.tolist()})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("roots", "layers"), required=True)
    ap.add_argument("--families", nargs="*", default=["D6", "E6", "E7"])
    ap.add_argument("--n", type=int, nargs="*", default=[41, 42, 43, 44])
    ap.add_argument("--seeds", type=int, nargs="+", required=True)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.mode == "roots":
        data = {fam: root_projection_search(fam, args.seeds, args.rounds)
                for fam in args.families}
    else:
        data = {"layer_runs": layer_search(args.n, args.seeds)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(args.output)


if __name__ == "__main__":
    main()
