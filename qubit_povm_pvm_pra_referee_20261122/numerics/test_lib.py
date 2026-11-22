#!/usr/bin/env python3
"""Self-tests of bell_lib building blocks against independent brute-force optimisers."""
import time, sys
import numpy as np
from scipy.optimize import minimize
import bell_lib as bl

rng = np.random.default_rng(7)

# ---------------- 1. exact POVM step vs generic smooth optimiser
def povm_from_params(p, n):
    A = (p[: n * 4] + 1j * p[n * 4:]).reshape(n, 2, 2)
    M = A.conj().transpose(0, 2, 1) @ A
    S = M.sum(0)
    es, U = np.linalg.eigh(S)
    Sih = (U / np.sqrt(es)) @ U.conj().T
    return Sih @ M @ Sih

def brute(K, n, starts=12):
    best = -np.inf
    def f(p):
        M = povm_from_params(p, n)
        return -np.einsum('aij,aji->', K, M).real
    for s in range(starts):
        r = minimize(f, rng.normal(size=8 * n), method='BFGS', options=dict(gtol=1e-10, maxiter=2000))
        best = max(best, -r.fun)
    return best

print("== test 1: exact qubit POVM step ==")
worst = 0; worst_under = 0; nf = 0; tot = 0
for n in (2, 3, 4, 5):
    N = 40
    H = rng.normal(size=(N, n, 2, 2)) + 1j * rng.normal(size=(N, n, 2, 2))
    K = H + H.conj().transpose(0, 1, 3, 2)
    # make some instances special: identical operators, commuting operators, one dominant
    K[0, 1] = K[0, 0]
    K[1] = np.array([np.diag(rng.normal(size=2)) for _ in range(n)])
    K[2, 0] += 10 * np.eye(2)
    k, kap = bl.to_bloch(K)
    w, v, val, found = bl.solve_povm_batch(k, kap)
    M = bl.from_bloch(w, v)
    mineig, nerr = bl.povm_validity(M)
    prim = np.einsum('naij,naji->n', K, M).real
    nf += (~found).sum(); tot += N
    for i in range(N):
        if not found[i]:
            print("   not found: n=%d instance %d" % (n, i)); continue
        b = brute(K[i], n)
        worst = max(worst, b - val[i]); worst_under = max(worst_under, val[i] - b)
        assert abs(prim[i] - val[i]) < 1e-8, (prim[i], val[i])
        assert mineig[i] > -1e-9 and nerr[i] < 1e-8, (mineig[i], nerr[i])
    print(f"  n={n}: found {found.sum()}/{N}; max (brute - exact) so far {worst:.2e}; max (exact - brute) {worst_under:.2e}; "
          f"min eig {mineig[found].min():.1e}, norm err {nerr[found].max():.1e}")
print(f"  not-found total {nf}/{tot}.  Exact value must be >= brute (brute is a lower bound): worst brute-exact = {worst:.2e}")

# large random batch: duality gap check only
for n in (3, 4, 6):
    N = 20000
    H = rng.normal(size=(N, n, 2, 2)) + 1j * rng.normal(size=(N, n, 2, 2))
    K = H + H.conj().transpose(0, 1, 3, 2)
    k, kap = bl.to_bloch(K)
    t0 = time.time()
    w, v, val, found = bl.solve_povm_batch(k, kap)
    dt = time.time() - t0
    M = bl.from_bloch(w, v)
    mineig, nerr = bl.povm_validity(M)
    prim = np.einsum('naij,naji->n', K, M).real
    nz = (w > 1e-9).sum(1)
    print(f"  n={n}, N={N}: found {found.mean()*100:.3f}%  max|primal-dual| {np.abs(prim-val)[found].max():.2e}  min eig {mineig[found].min():.1e} "
          f"norm err {nerr[found].max():.1e}  time {dt:.2f}s; #nonzero-effects histogram {np.bincount(nz, minlength=5)[:6].tolist()}")

# PVM step vs brute force over labelled PVMs
print("== test 1b: PVM step ==")
n = 3; N = 2000
H = rng.normal(size=(N, n, 2, 2)) + 1j * rng.normal(size=(N, n, 2, 2)); K = H + H.conj().transpose(0, 1, 3, 2)
k, kap = bl.to_bloch(K)
w, v, val = bl.solve_pvm_batch(k, kap)
M = bl.from_bloch(w, v)
prim = np.einsum('naij,naji->n', K, M).real
wp, vp, valp, f = bl.solve_povm_batch(k, kap)
print("  primal==reported:", np.abs(prim - val).max(), " projective:", bl.is_projective(M).all(), " PVM<=POVM:", (val <= valp + 1e-9).all(),
      " fraction with POVM>PVM:", (valp > val + 1e-9).mean())

# ---------------- 2. two-angle bound: CHSH and reduction check
print("== test 2: two-angle PVM bound ==")
chsh = [[np.array([[1., -1], [-1, 1]]), np.array([[1., -1], [-1, 1]])], [np.array([[1., -1], [-1, 1]]), -np.array([[1., -1], [-1, 1]])]]
r = bl.pvm_two_angle(chsh, (2, 2), (2, 2))
print("  CHSH:", r['value'], "vs 2*sqrt2 =", 2 * np.sqrt(2), " assign", r['assignA'], r['assignB'], r['thetaA'], r['thetaB'])
mx = 0
for trial in range(6):
    outsA = (3, 3); outsB = (3, 2) if trial % 2 else (3, 3)
    c = [[rng.normal(size=(outsA[x], outsB[y])) for y in range(2)] for x in range(2)]
    t0 = time.time(); r1 = bl.pvm_two_angle(c, outsA, outsB); t1 = time.time() - t0
    t0 = time.time(); r2 = bl.pvm_two_angle(c, outsA, outsB, ordered_first=True, ngrid=24, ntop=200); t2 = time.time() - t0
    mx = max(mx, abs(r1['value'] - r2['value']))
    print(f"  trial {trial}: reduced {r1['value']:.12f} ({t1:.2f}s, {r1['nconfigs']} cfgs)  literal-ordered fine-grid {r2['value']:.12f} ({t2:.2f}s, {r2['nconfigs']} cfgs)  diff {r1['value']-r2['value']:+.2e}")
print("  max |reduced - literal| =", mx)

# ---------------- 3. see-saw timing & PVM see-saw vs two-angle
print("== test 3: see-saw ==")
outsA = (3, 3); outsB = (3, 3); F = 20; R = 50
cs = [[rng.normal(size=(F, outsA[x], outsB[y])) for y in range(2)] for x in range(2)]
cb = [[np.repeat(cs[x][y], R, axis=0) for y in range(2)] for x in range(2)]
N = F * R
for mode in ('pvm', 'povm'):
    MA = [bl.random_povm(rng, N, outsA[x]) for x in range(2)]; MB = [bl.random_povm(rng, N, outsB[y]) for y in range(2)]
    t0 = time.time()
    MA, MB, psi, val, nfail, hist = bl.seesaw(cb, MA, MB, iters=300, mode=mode, return_hist=True)
    dt = time.time() - t0
    cv, MAs, MBs, psis = bl.certified_value(cb, MA, MB)
    print(f"  mode={mode}: {len(hist)-1} iters, {dt:.1f}s, nfail={nfail}, monotone violations (max decrease) {np.min(np.diff(hist, axis=0)):.2e}, "
          f"|certified - seesaw| max {np.abs(cv-val).max():.2e}")
    best = cv.reshape(F, R).max(1)
    if mode == 'pvm':
        pvmss = best
        print("   all projective:", all(bl.is_projective(m).all() for m in MAs + MBs))
    else:
        povmss = best
ta = np.array([bl.pvm_two_angle([[cs[x][y][f] for y in range(2)] for x in range(2)], outsA, outsB)['value'] for f in range(F)])
print("  two-angle PVM bound - PVM see-saw best (>=0 expected):", np.round(ta - pvmss, 10).tolist())
print("  POVM see-saw best - two-angle PVM bound (<=0 expected by theorem):", np.round(povmss - ta, 10).tolist())
