#!/usr/bin/env python3
"""Claim 2: heavy global search over qubit PVM strategies for the 3x2 functional, and the POVM positive control.
usage: claim2_search.py seed out.json [scale]
"""
import sys, json, time, itertools
import numpy as np
from scipy.optimize import minimize
import bell_lib as bl
import claim1_lib as cl

seed = int(sys.argv[1]); outp = sys.argv[2]; scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
rng = np.random.default_rng(seed)
t00 = time.time()

# ---------------------------------------------------------------- the functional (eq:bell-functional)
alpha = np.array([1.0, -1.0, 1.0]); beta = np.array([1.0, -1.0])
C = [[None, None] for _ in range(3)]
for x in range(2):
    for y in range(2):
        s = -1.0 if (x, y) == (1, 1) else 1.0
        C[x][y] = 10 * s * np.outer(alpha, beta)
C[2][0] = np.zeros((3, 2)); C[2][0][0, 0] = 0.6; C[2][0][1, 1] = 0.6
C[2][1] = np.zeros((3, 2)); C[2][1][2, 0] = 0.8
outsA = (3, 3, 3); outsB = (2, 2)
L0 = 20 * np.sqrt(2) + 16 / 25; L1 = (16 + 8 * np.sqrt(7813)) / 25; RB = 28.9
print(f"targets: L0={L0:.12f}  L1={L1:.12f}  rational PVM bound 289/10; 20sqrt2+3/5 = {20*np.sqrt(2)+0.6:.12f}")
out = dict(L0=L0, L1=L1)

def batch_c(N):
    return [[np.broadcast_to(C[x][y], (N, 3, 2)).copy() for y in range(2)] for x in range(3)]

# ---------------------------------------------------------------- sanity: evaluate the paper's strategies numerically
def val_of(MA, MB, psi):
    cb = batch_c(1)
    return bl.value(cb, [m[None] for m in MA], [m[None] for m in MB], psi[None])[0]
I2 = np.eye(2, dtype=complex); X = bl.SX; Z = bl.SZ
def pe(A):
    return np.array([(I2 + A) / 2, (I2 - A) / 2, np.zeros((2, 2))])
phi = np.array([[1, 0], [0, 1]], dtype=complex) / np.sqrt(2)
MA = [pe((Z + X) / np.sqrt(2)), pe((Z - X) / np.sqrt(2)), np.array([(17 * I2 - 8 * X + 15 * Z) / 50, (17 * I2 - 8 * X - 15 * Z) / 50, (16 * I2 + 16 * X) / 50])]
MB = [np.array([(I2 + Z) / 2, (I2 - Z) / 2]), np.array([(I2 + X) / 2, (I2 - X) / 2])]
print("numeric value of the simple strategy:", val_of(MA, MB, phi), " (L0)")
q = np.sqrt(7813); eta = 1 / q; k = 0.6 * np.sqrt((q - 1) / (q + 1)); s6 = 6 * np.sqrt(217)
psi_eta = np.array([[np.sqrt((1 + eta) / 2), 0], [0, np.sqrt((1 - eta) / 2)]], dtype=complex)
MA1 = [pe((s6 * X + q * Z) / 125), pe((s6 * X - q * Z) / 125),
       np.array([[[k * k, k], [k, 1]], [[k * k, -k], [-k, 1]], [[2 * (1 - k * k), 0], [0, 0]]], dtype=complex) / 2]
MB1 = [np.array([(I2 + X) / 2, (I2 - X) / 2]), np.array([(I2 + Z) / 2, (I2 - Z) / 2])]
print("numeric value of the strengthened strategy:", val_of(MA1, MB1, psi_eta), " (L1)")
out['numeric_L0'] = float(val_of(MA, MB, phi)); out['numeric_L1'] = float(val_of(MA1, MB1, psi_eta))

# ---------------------------------------------------------------- positive control: POVM see-saw
t0 = time.time()
N = int(3000 * scale)
cb = batch_c(N)
def mixed(n):
    kk = ['full', 'rank1', 'pvm']
    parts = [bl.random_povm(rng, N // 3 + (1 if i < N % 3 else 0), n, kk[i]) for i in range(3)]
    return np.concatenate(parts)[rng.permutation(N)]
MAr = [mixed(3) for _ in range(3)]; MBr = [mixed(2) for _ in range(2)]
MAr, MBr, val, nf, its, left = cl.seesaw_adaptive(cb, MAr, MBr, mode='povm', max_iters=1000)
cv, MAc, MBc, psic = bl.certified_value(cb, MAr, MBr)
ib = int(cv.argmax())
mineigA = min(bl.povm_validity(m)[0].min() for m in MAc); nerrA = max(bl.povm_validity(m)[1].max() for m in MAc + MBc)
print(f"\nPOVM see-saw: {N} random restarts, {its} iterations (unconverged {left}), {time.time()-t0:.0f}s")
print(f"   best POVM value found = {cv.max():.12f}   (-28.9 = {cv.max()-RB:+.6f};  -L1 = {cv.max()-L1:+.3e})")
print(f"   fraction of restarts > 28.9: {(cv > RB + 1e-9).mean():.3f};  POVM validity: min eig {mineigA:.1e}, normalisation err {nerrA:.1e}")
vals_sorted = np.sort(cv)[::-1]
print("   top distinct converged values:", np.unique(np.round(vals_sorted[:400], 7))[::-1][:8].tolist())
# start the see-saw from the paper's two strategies as well
for nm, (a, b) in dict(simple=(MA, MB), strengthened=(MA1, MB1)).items():
    c1 = batch_c(1)
    a2, b2, v2, _, it2, _ = cl.seesaw_adaptive(c1, [m[None].copy() for m in a], [m[None].copy() for m in b], mode='povm', max_iters=1000)
    cv2, _, _, _ = bl.certified_value(c1, a2, b2)
    print(f"   POVM see-saw started at the paper's {nm} strategy converges to {cv2[0]:.12f} ({it2} its)")
    out[f'povm_from_{nm}'] = float(cv2[0])
out['povm_best'] = float(cv.max()); out['povm_frac_above_289_10'] = float((cv > RB + 1e-9).mean())
best_povm = dict(MA=[m[ib] for m in MAc], MB=[m[ib] for m in MBc], psi=psic[ib])
third = best_povm['MA'][2]
print("   best POVM strategy: Alice x=2 effect traces", np.round([np.trace(e).real for e in third], 6).tolist(),
      "dets", np.round([np.linalg.det(e).real for e in third], 9).tolist(),
      "; Schmidt coefficients", np.round(np.linalg.svd(best_povm['psi'], compute_uv=False), 6).tolist())
out['povm_best_strategy'] = dict(MA_re=[m.real.tolist() for m in best_povm['MA']], MA_im=[m.imag.tolist() for m in best_povm['MA']],
                                 MB_re=[m.real.tolist() for m in best_povm['MB']], MB_im=[m.imag.tolist() for m in best_povm['MB']],
                                 psi_re=best_povm['psi'].real.tolist(), psi_im=best_povm['psi'].imag.tolist())

# ---------------------------------------------------------------- PVM search (a): free-pattern PVM see-saw
t0 = time.time()
N = int(40000 * scale)
cb = batch_c(N)
MAp = [np.concatenate([bl.random_povm(rng, N // 2, 3, 'pvm'), bl.random_povm(rng, N - N // 2, 3, 'full')]) for _ in range(3)]
MBp = [np.concatenate([bl.random_povm(rng, N // 2, 2, 'pvm'), bl.random_povm(rng, N - N // 2, 2, 'full')]) for _ in range(2)]
MAp, MBp, val, nf, its, left = cl.seesaw_adaptive(cb, MAp, MBp, mode='pvm', max_iters=1000)
cvp, MApc, MBpc, psip = bl.certified_value(cb, MAp, MBp)
projA = np.all([bl.is_projective(m) for m in MApc + MBpc], axis=0)
print(f"\nPVM see-saw (labels + arbitrary Bloch directions chosen optimally each step): {N} restarts, {its} its (unconverged {left}), {time.time()-t0:.0f}s")
print(f"   all final strategies projective: {projA.all()};  best PVM value = {cvp[projA].max():.12f}  (28.9 - best = {RB-cvp[projA].max():.6f})")
print("   top distinct converged values:", np.unique(np.round(np.sort(cvp)[::-1][:2000], 7))[::-1][:8].tolist())
out['pvm_seesaw_best'] = float(cvp[projA].max()); out['pvm_seesaw_restarts'] = N
ibp = int(np.where(projA, cvp, -np.inf).argmax())
best_pvm = dict(val=float(cvp[ibp]), MA=[m[ibp] for m in MApc], MB=[m[ibp] for m in MBpc], psi=psip[ibp], src='free see-saw')

# ---------------------------------------------------------------- PVM search (b): exhaustive pattern enumeration
# pattern per input: (a, a') ; a == a' means identity on label a; a != a' means rank-one projector P -> a, 1-P -> a'
# (unordered pairs suffice because the direction ranges over the whole sphere).
patA = [(a, a) for a in range(3)] + [(0, 1), (0, 2), (1, 2)]
patB = [(0, 0), (1, 1), (0, 1)]
patterns = [(p0, p1, p2, q0, q1) for p0 in patA for p1 in patA for p2 in patA for q0 in patB for q1 in patB]
P = len(patterns)
Rpat = max(4, int(24 * scale))
N = P * Rpat
print(f"\npattern-constrained PVM see-saw: {P} labelled rank patterns x {Rpat} restarts = {N} runs", flush=True)
pat = np.repeat(np.array(patterns), Rpat, axis=0)  # (N, 5, 2)

def build(pats, dirs, n):
    """pats (N,2) labels, dirs (N,3) unit -> effects (N,n,2,2)"""
    Nn = pats.shape[0]; ar = np.arange(Nn)
    w = np.zeros((Nn, n)); v = np.zeros((Nn, n, 3))
    np.add.at(w, (ar, pats[:, 0]), 0.5); np.add.at(w, (ar, pats[:, 1]), 0.5)
    np.add.at(v, (ar, pats[:, 0]), 0.5 * dirs); np.add.at(v, (ar, pats[:, 1]), -0.5 * dirs)
    return bl.from_bloch(w, v)

def rand_dirs(Nn):
    d = rng.normal(size=(Nn, 3)); return d / np.linalg.norm(d, axis=-1, keepdims=True)

def constrained_chunk(cb, pat, dA, dB, iters):
    Nn = pat.shape[0]; ar = np.arange(Nn)
    MA = [build(pat[:, x], dA[x], 3) for x in range(3)]; MB = [build(pat[:, 3 + y], dB[y], 2) for y in range(2)]
    psi, val = bl.top_state(cb, MA, MB)
    prev = val.copy(); prev2 = val.copy()
    for it in range(iters):
        for x in range(3):
            k, kap = bl.to_bloch(bl.alice_scores(cb, MB, psi, x))
            d = kap[ar, pat[:, x, 0]] - kap[ar, pat[:, x, 1]]
            nd = np.linalg.norm(d, axis=-1)
            dA[x] = np.where((nd > 1e-14)[:, None], d / np.where(nd > 0, nd, 1)[:, None], dA[x])
            MA[x] = build(pat[:, x], dA[x], 3)
        psi, _ = bl.top_state(cb, MA, MB)
        for y in range(2):
            k, kap = bl.to_bloch(bl.bob_scores(cb, MA, psi, y))
            d = kap[ar, pat[:, 3 + y, 0]] - kap[ar, pat[:, 3 + y, 1]]
            nd = np.linalg.norm(d, axis=-1)
            dB[y] = np.where((nd > 1e-14)[:, None], d / np.where(nd > 0, nd, 1)[:, None], dB[y])
            MB[y] = build(pat[:, 3 + y], dB[y], 2)
        psi, val = bl.top_state(cb, MA, MB)
        prev2 = prev; prev = val.copy() if it < iters - 1 else prev
        if it == iters - 2:
            last = val.copy()
    done = np.abs(val - last) < 3e-12
    return dA, dB, MA, MB, psi, val, done


def constrained_seesaw(cb_unused, pat, dA, dB, iters=400, chunk=20):
    """pattern-constrained see-saw with an active set (converged runs are dropped)."""
    Nn = pat.shape[0]
    active = np.arange(Nn)
    val = np.zeros(Nn); psi = np.zeros((Nn, 2, 2), dtype=complex)
    MA = [np.zeros((Nn, 3, 2, 2), dtype=complex) for _ in range(3)]; MB = [np.zeros((Nn, 2, 2, 2), dtype=complex) for _ in range(2)]
    it = 0
    while len(active) and it < iters:
        cba = batch_c(len(active))
        a_dA = [d[active] for d in dA]; a_dB = [d[active] for d in dB]
        a_dA, a_dB, a_MA, a_MB, a_psi, a_val, done = constrained_chunk(cba, pat[active], a_dA, a_dB, chunk)
        for x in range(3): dA[x][active] = a_dA[x]; MA[x][active] = a_MA[x]
        for y in range(2): dB[y][active] = a_dB[y]; MB[y][active] = a_MB[y]
        psi[active] = a_psi; val[active] = a_val
        active = active[~done]; it += chunk
    return dA, dB, MA, MB, psi, val, it, len(active)

t0 = time.time()
dA = [rand_dirs(N) for _ in range(3)]; dB = [rand_dirs(N) for _ in range(2)]
dA, dB, MAq, MBq, psiq, valq, itq, leftq = constrained_seesaw(None, pat, dA, dB, iters=600)
vq = valq.reshape(P, Rpat).max(1)
print(f"   done in {time.time()-t0:.0f}s, {itq} iterations (unconverged {leftq}); overall best = {valq.max():.12f}  (28.9 - best = {RB-valq.max():.6f})")
order = np.argsort(vq)[::-1]
print("   best value per pattern (top 12):   [pattern = Alice x0,x1,x2 label pairs | Bob y0,y1 label pairs]")
for o in order[:12]:
    print(f"     {vq[o]:.10f}   A:{patterns[o][:3]}  B:{patterns[o][3:]}")
# group by x=2 support
by_support = {}
for o in range(P):
    key = patterns[o][2]
    by_support[key] = max(by_support.get(key, -np.inf), vq[o])
print("   best value by Alice's x=2 label pattern:", {str(k_): round(float(v_), 10) for k_, v_ in by_support.items()})
out['pattern_best_by_x2'] = {str(k_): float(v_) for k_, v_ in by_support.items()}
# fully degenerate classes
deg = [o for o in range(P) if any(p[0] == p[1] for p in patterns[o][:2]) or any(p[0] == p[1] for p in patterns[o][3:])]
print(f"   best over patterns with a deterministic CHSH measurement ({len(deg)} patterns): {max(vq[o] for o in deg):.10f}  (<= 20+7/5 expected)")
out['pattern_enum_best'] = float(valq.max()); out['pattern_enum_runs'] = N; out['n_patterns'] = P
out['degenerate_chsh_best'] = float(max(vq[o] for o in deg))
iq = int(valq.argmax())
if valq[iq] > best_pvm['val']:
    best_pvm = dict(val=float(valq[iq]), MA=[m[iq] for m in MAq], MB=[m[iq] for m in MBq], psi=psiq[iq], src='pattern see-saw',
                    pattern=[list(map(int, p)) for p in pat[iq]])

# ---------------------------------------------------------------- PVM search (c): direct optimisation over Bloch angles
def dirs_from_angles(a):
    th, ph = a[..., 0], a[..., 1]
    return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], -1)

def lam_from_angles(X, patt):
    """X (Pn, 10) angles for 5 directions; patt (5,2)"""
    Pn = X.shape[0]
    d = dirs_from_angles(X.reshape(Pn, 5, 2))
    pt = np.broadcast_to(np.array(patt)[None], (Pn, 5, 2))
    MA = [build(pt[:, x], d[:, x], 3) for x in range(3)]; MB = [build(pt[:, 3 + y], d[:, 3 + y], 2) for y in range(2)]
    cb = batch_c(Pn)
    B = bl.bell_operator(cb, MA, MB)
    return np.linalg.eigvalsh(0.5 * (B + B.conj().transpose(0, 2, 1)))[:, -1]

def direct_opt(patt, x0, h=1e-6):
    eye = np.eye(10)
    f = lambda x: -lam_from_angles(x[None], patt)[0]
    def g(x):
        v = lam_from_angles(np.concatenate([x[None] + h * eye, x[None] - h * eye]), patt)
        return -(v[:10] - v[10:]) / (2 * h)
    r = minimize(f, x0, jac=g, method='BFGS', options=dict(gtol=1e-9, maxiter=300))
    r2 = minimize(f, r.x, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-14, maxiter=1200))
    return (r2.x, -r2.fun) if -r2.fun > -r.fun else (r.x, -r.fun)

t0 = time.time()
main_pats = [((0, 1), (0, 1), p2, (0, 1), (0, 1)) for p2 in patA]   # CHSH part nondegenerate (labels 0/2 equivalent for x=0,1)
nstart = max(3, int(15 * scale))
direct_best = {}
for patt in main_pats:
    bv = -np.inf
    for s in range(nstart):
        x0 = np.stack([np.arccos(rng.uniform(-1, 1, size=5)), rng.uniform(0, 2 * np.pi, size=5)], -1).ravel()
        xo, v = direct_opt(patt, x0)
        bv = max(bv, v)
    direct_best[str(patt[2])] = bv
print(f"\ndirect BFGS+Nelder-Mead over 10 Bloch angles, {nstart} random starts per x=2 pattern ({time.time()-t0:.0f}s):")
print("   best by x=2 pattern:", {k_: round(float(v_), 10) for k_, v_ in direct_best.items()})
out['direct_best_by_x2'] = {k_: float(v_) for k_, v_ in direct_best.items()}
out['direct_best'] = float(max(direct_best.values()))

# ---------------------------------------------------------------- summary of PVM side
pvm_best_all = max(best_pvm['val'], out['direct_best'])
print(f"\nBEST QUBIT PVM VALUE FOUND = {pvm_best_all:.12f}   (289/10 - best = {RB - pvm_best_all:.9f};  best - (20sqrt2+3/5) = {pvm_best_all-(20*np.sqrt(2)+0.6):+.9f})")
print("   exceeds 289/10:", bool(pvm_best_all > RB + 1e-9))
out['pvm_best'] = float(pvm_best_all); out['pvm_exceeds_bound'] = bool(pvm_best_all > RB + 1e-9)
# describe the best PVM strategy
MAb, MBb, psib = best_pvm['MA'], best_pvm['MB'], best_pvm['psi']
print("   source:", best_pvm['src'], " value re-evaluated:", val_of(MAb, MBb, psib))
for x in range(3):
    kx, kapx = bl.to_bloch(MAb[x])
    print(f"   Alice x={x}: effect (trace/2, Bloch vector) per label:", [(round(float(kx[a]), 6), np.round(2 * kapx[a], 6).tolist()) for a in range(3)])
for y in range(2):
    ky, kapy = bl.to_bloch(MBb[y])
    print(f"   Bob   y={y}: effect (trace/2, Bloch vector) per label:", [(round(float(ky[b]), 6), np.round(2 * kapy[b], 6).tolist()) for b in range(2)])
sv = np.linalg.svd(psib, compute_uv=False)
print("   state Schmidt coefficients:", np.round(sv, 8).tolist(), " (eta = %.6f)" % (sv[0] ** 2 - sv[1] ** 2))
out['pvm_best_strategy'] = dict(MA_re=[m.real.tolist() for m in MAb], MA_im=[m.imag.tolist() for m in MAb],
                                MB_re=[m.real.tolist() for m in MBb], MB_im=[m.imag.tolist() for m in MBb],
                                psi_re=psib.real.tolist(), psi_im=psib.imag.tolist(), schmidt=sv.tolist(), source=best_pvm['src'])
out['wall_seconds'] = time.time() - t00
json.dump(out, open(outp, 'w'), indent=1)
print(f"\nwall {time.time()-t00:.0f}s")
