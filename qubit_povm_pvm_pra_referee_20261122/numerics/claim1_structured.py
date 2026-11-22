#!/usr/bin/env python3
"""Claim 1: structured functionals (CGLMP-3, trine / tetrahedral POVM targets, squeezed CHSH+discrimination).
usage: claim1_structured.py seed out.json
"""
import sys, json, time, itertools
import numpy as np
import bell_lib as bl
import claim1_lib as cl

seed = int(sys.argv[1]); outp = sys.argv[2]
rng = np.random.default_rng(seed)
t00 = time.time()
I2 = np.eye(2, dtype=complex)

def stack(clist):
    """list of c (c[x][y] (a,b)) -> batched cs"""
    return [[np.array([c[x][y] for c in clist]) for y in range(2)] for x in range(2)]

def rank1_povm(dirs, weights=None):
    dirs = np.asarray(dirs, dtype=float)
    n = len(dirs)
    w = np.full(n, 1.0 / n) if weights is None else np.asarray(weights)
    return bl.from_bloch(w, w[:, None] * dirs)

def pvm_labels(direction, n, la=0, lb=1):
    w = np.zeros(n); v = np.zeros((n, 3))
    w[la] += 0.5; w[lb] += 0.5; v[la] += 0.5 * np.asarray(direction); v[lb] -= 0.5 * np.asarray(direction)
    return bl.from_bloch(w, v)

def rot_y(dirs, ang):
    c, s = np.cos(ang), np.sin(ang)
    Rm = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.asarray(dirs) @ Rm.T

def rand_rot(rng):
    Q, R_ = np.linalg.qr(rng.normal(size=(3, 3)))
    Q = Q * np.sign(np.diag(R_))
    if np.linalg.det(Q) < 0: Q[:, 0] *= -1
    return Q

trine = np.array([[np.sin(2 * np.pi * i / 3), 0, np.cos(2 * np.pi * i / 3)] for i in range(3)])
tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
assert np.allclose(trine.sum(0), 0) and np.allclose(tet.sum(0), 0)

def state(theta):
    psi = np.zeros((2, 2), dtype=complex); psi[0, 0] = np.cos(theta); psi[1, 1] = np.sin(theta); return psi
singlet = np.array([[0, 1], [-1, 0]], dtype=complex) / np.sqrt(2)

def behav(MA, MB, psi):
    q = bl.behavior([m[None] for m in MA], [m[None] for m in MB], psi[None])
    return [[q[x][y][0] for y in range(2)] for x in range(2)]

def functionals_from_target(q, tag, MA=None, MB=None):
    """several functionals designed to reward the target behaviour q"""
    outs = []
    c_q = [[q[x][y] * 5 for y in range(2)] for x in range(2)]
    conn = [[(q[x][y] - q[x][y].sum(1, keepdims=True) * q[x][y].sum(0, keepdims=True)) * 10 for y in range(2)] for x in range(2)]
    lr = [[np.log(np.clip(q[x][y], 1e-4, None) / np.clip(q[x][y].sum(1, keepdims=True) * q[x][y].sum(0, keepdims=True), 1e-4, None)) for y in range(2)] for x in range(2)]
    outs += [(tag + ':c=q', c_q), (tag + ':connected', conn), (tag + ':loglik', lr)]
    # nearest-local-point witness (if the target is nonlocal)
    outsA = (q[0][0].shape[0], q[1][0].shape[0]); outsB = (q[0][0].shape[1], q[0][1].shape[1])
    V = cl.det_vertices(outsA, outsB)
    qf = np.concatenate([q[x][y].ravel() for x in range(2) for y in range(2)])
    lam, _ = cl.nnls(np.vstack([V.T, 1e3 * np.ones((1, V.shape[0]))]), np.concatenate([qf, [1e3]]), maxiter=50000)
    d = qf - V.T @ lam
    if np.linalg.norm(d) > 1e-4:
        cs = cl.unflat((d / np.linalg.norm(d) * 5)[None], outsA, outsB)
        outs.append((tag + ':nearest-local-witness', [[cs[x][y][0] for y in range(2)] for x in range(2)]))
    return outs, float(np.linalg.norm(d))

results = {}
def run_group(label, items, outsA, outsB, R=150, joint_n=6):
    names = [n for n, _ in items]
    cs = stack([c for _, c in items])
    res = cl.evaluate(cs, outsA, outsB, rng, R=R, Rp=60, Rseed=6, joint_n=min(joint_n, len(items)), joint_starts=4, names=names,
                      ngrid=12, ntop=120)
    print(cl.summarize(res, label), flush=True)
    pb = np.maximum(res['pvm2'], res['pvmss'])
    for i, n in enumerate(names):
        if len(names) <= 40 or abs(res['gap'][i]) > 1e-7:
            print(f"      {n:58s} local {res['local'][i]:.6f}  PVM {pb[i]:.10f}  POVM-best {max(res['povmss'][i], res['povmseed'][i], res['joint'][i]):.10f}  gap {res['gap'][i]:+.2e}")
    r = cl.to_jsonable(res); r['names'] = names
    results[label] = r
    json.dump(results, open(outp, 'w'))
    return res

# =============================================================== (3,3;3,3)
items = []
d = lambda cond: np.array([[1.0 if cond(a, b) else 0.0 for b in range(3)] for a in range(3)])
# CGLMP-3 (Collins-Gisin-Linden-Massar-Popescu), inputs A1,A2 = x 0,1 ; B1,B2 = y 0,1
cg = [[None, None], [None, None]]
cg[0][0] = d(lambda a, b: a == b) - d(lambda a, b: a == (b - 1) % 3)
cg[1][0] = d(lambda a, b: b == (a + 1) % 3) - d(lambda a, b: b == a)
cg[1][1] = d(lambda a, b: a == b) - d(lambda a, b: a == (b - 1) % 3)
cg[0][1] = d(lambda a, b: b == a) - d(lambda a, b: b == (a - 1) % 3)
items.append(('CGLMP-3', cg))
items.append(('-CGLMP-3', [[-cg[x][y] for y in range(2)] for x in range(2)]))
for sgm in (0.05, 0.2):
    for i in range(10):
        items.append((f'CGLMP-3+{sgm}*gauss#{i}', [[cg[x][y] + sgm * rng.normal(size=(3, 3)) for y in range(2)] for x in range(2)]))
# anti-correlation functional rewarding the trine table (zero diagonal)
anti = [[-np.eye(3) for y in range(2)] for x in range(2)]
items.append(('trine:anti-diagonal(all pairs)', anti))
# trine-based targets
targets = []
T0 = rank1_povm(trine)
for ang in (np.pi / 6, np.pi / 3, np.pi / 2):
    targets.append((f'singlet,trine+trine_rot{ang:.2f} both', [T0, rank1_povm(rot_y(trine, ang))], [T0, rank1_povm(rot_y(trine, ang))], singlet))
targets.append(('singlet,A:trine/trine_rot90,B:trine_rot45/rot135', [T0, rank1_povm(rot_y(trine, np.pi / 2))],
                [rank1_povm(rot_y(trine, np.pi / 4)), rank1_povm(rot_y(trine, 3 * np.pi / 4))], singlet))
targets.append(('singlet,same trine both inputs (remark)', [T0, T0], [T0, T0], singlet))
for th in (0.3, 0.6):
    targets.append((f'psi({th}),trines', [T0, rank1_povm(rot_y(trine, np.pi / 2))], [rank1_povm(rot_y(trine, np.pi / 4)), rank1_povm(rot_y(trine, 3 * np.pi / 4))], state(th)))
# PVM on input 0, trine on input 1 (nonlocal candidates): CHSH-like geometry
z = np.array([0, 0, 1.0]); xx = np.array([1.0, 0, 0])
for ang in (0.0, np.pi / 4, np.pi / 2):
    bz = rot_y([z], np.pi / 4)[0]
    targets.append((f'phi+,A:PVM_Z/trine_rot{ang:.2f},B:PVM_45/trine', [pvm_labels(z, 3), rank1_povm(rot_y(trine, ang))],
                    [pvm_labels(bz, 3), rank1_povm(rot_y(trine, np.pi / 4 + ang))], state(np.pi / 4)))
    targets.append((f'phi+,A:PVM_Z/trine_rot{ang:.2f},B:PVM_45/PVM_-45', [pvm_labels(z, 3), rank1_povm(rot_y(trine, ang))],
                    [pvm_labels(bz, 3), pvm_labels(rot_y([z], -np.pi / 4)[0], 3)], state(np.pi / 4)))
# non-planar trines and unequal-weight 3-outcome POVM
tr_yz = trine[:, [1, 0, 2]]
tr_xy = trine[:, [0, 2, 1]]
uw = np.array([0.5, 0.3, 0.2]); ud = np.array([[0, 0, 1.0], [np.sin(2.0), 0, np.cos(2.0)], [0, 0, 0]])
ud[2] = -(uw[0] * ud[0] + uw[1] * ud[1]) / uw[2]
if abs(np.linalg.norm(ud[2]) - 1) > 1e-9:
    # choose angle so that the third vector is unit: solve numerically
    from scipy.optimize import brentq
    fz = lambda t: np.linalg.norm((uw[0] * np.array([0, 0, 1.0]) + uw[1] * np.array([np.sin(t), 0, np.cos(t)])) / uw[2]) - 1
    t = brentq(fz, 0.1, np.pi - 1e-6) if fz(0.1) * fz(np.pi - 1e-6) < 0 else None
    if t is not None:
        ud[1] = [np.sin(t), 0, np.cos(t)]; ud[2] = -(uw[0] * ud[0] + uw[1] * ud[1]) / uw[2]
unequal = bl.from_bloch(uw, uw[:, None] * ud)
print("unequal-weight POVM valid:", bl.povm_validity(unequal[None]))
targets.append(('phi+,nonplanar trines + unequal POVM', [T0, rank1_povm(tr_yz)], [rank1_povm(tr_xy), unequal], state(np.pi / 4)))
for i in range(6):
    Ra, Rb, Rc, Rd = (rand_rot(rng) for _ in range(4))
    targets.append((f'random-rotated trines #{i}', [rank1_povm(trine @ Ra.T), rank1_povm(trine @ Rb.T)],
                    [rank1_povm(trine @ Rc.T), rank1_povm(trine @ Rd.T)], state(rng.uniform(0.3, np.pi / 4))))
tinfo = {}
for tag, MA, MB, psi in targets:
    q = behav(MA, MB, psi)
    fs, dloc = functionals_from_target(q, tag)
    tinfo[tag] = dloc
    items += fs
print("distance of each target behaviour from the local polytope:", {k: round(v, 5) for k, v in tinfo.items()})
run_group('(3,3;3,3) structured: CGLMP-3, trine targets', items, (3, 3), (3, 3))

# =============================================================== squeezed CHSH + discrimination, Bob with 2 or 3 labels
def squeezed(outsB, mu, signA1, wts, both_inputs=False, bob_term=False, x_disc=1):
    """c = mu*CHSH(coarse-grained) + T,  T = w0 p(0,0|x_disc,0) + w1 p(1,1|x_disc,0) + w2 p(2,0|x_disc,1)."""
    alphaA = [np.array([1.0, -1.0, 1.0]), np.array(signA1, dtype=float)]
    betaB = [np.array([1.0, -1.0, 1.0][:outsB[y]]) for y in range(2)]
    c = [[None, None], [None, None]]
    for x in range(2):
        for y in range(2):
            s = -1.0 if (x, y) == (1, 1) else 1.0
            c[x][y] = mu * s * np.outer(alphaA[x], betaB[y])
    xs = [0, 1] if both_inputs else [x_disc]
    for x_ in xs:
        c[x_][0][0, 0] += wts[0]; c[x_][0][1, 1] += wts[1]; c[x_][1][2, 0] += wts[2]
    if bob_term:
        # mirrored discrimination term on Bob's 3-outcome input y=1 (requires 3 labels there)
        c[0][1][0, 0] += wts[0]; c[0][1][1, 1] += wts[1]; c[1][1][0, 2] += wts[2]
    return c

mus = [0.0, 0.03, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
signs = [(1, -1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 0), (1, 0, -1)]
wlist = [(0.6, 0.6, 0.8), (1.0, 1.0, 1.0), (0.5, 0.5, 1.0), (0.6, 0.8, 0.8)]
for outsB in [(2, 2), (2, 3), (3, 3)]:
    items = []
    for mu in mus:
        for sg in signs:
            for wt in wlist[:2] if outsB != (2, 2) else wlist:
                items.append((f'squeezed mu={mu} signA1={sg} w={wt}', squeezed(outsB, mu, sg, wt)))
                if mu in (1.0, 10.0):
                    items.append((f'squeezed mu={mu} signA1={sg} w={wt} both-inputs', squeezed(outsB, mu, sg, wt, both_inputs=True)))
                    items.append((f'squeezed mu={mu} signA1={sg} w={wt} disc-on-x0', squeezed(outsB, mu, sg, wt, x_disc=0)))
                if outsB[1] == 3 and mu in (0.3, 1.0, 5.0, 10.0):
                    items.append((f'squeezed mu={mu} signA1={sg} w={wt} +Bob-term', squeezed(outsB, mu, sg, wt, bob_term=True)))
    res = run_group(f'(3,3;{outsB[0]},{outsB[1]}) squeezed CHSH+discrimination ({len(items)} functionals)', items, (3, 3), outsB, R=100, joint_n=6)

# =============================================================== (4,4;4,4): tetrahedral targets
items = []
S0 = rank1_povm(tet)
targets = [('singlet,A:tet/-tet,B:tet/-tet', [S0, rank1_povm(-tet)], [S0, rank1_povm(-tet)], singlet)]
for i in range(5):
    Ra, Rb, Rc, Rd = (rand_rot(rng) for _ in range(4))
    targets.append((f'random-rotated tetrahedra #{i}', [rank1_povm(tet @ Ra.T), rank1_povm(tet @ Rb.T)],
                    [rank1_povm(tet @ Rc.T), rank1_povm(tet @ Rd.T)], state(rng.uniform(0.3, np.pi / 4)) if i % 2 else singlet))
    targets.append((f'PVM+tetra mix #{i}', [pvm_labels(z, 4), rank1_povm(tet @ Ra.T)],
                    [pvm_labels(rot_y([z], np.pi / 4)[0], 4), rank1_povm(tet @ Rc.T)], state(np.pi / 4)))
for tag, MA, MB, psi in targets:
    q = behav(MA, MB, psi)
    fs, dloc = functionals_from_target(q, tag)
    items += fs
# elegant-style correlation functionals  c[a,b] = -t_a . t'_b
items.append(('tetra elegant: -t_a.t_b all pairs', [[-(tet @ tet.T) * 3 for y in range(2)] for x in range(2)]))
items.append(('tetra elegant: signs (+,+,+,-)', [[(-1 if (x, y) == (1, 1) else 1) * (-(tet @ tet.T) * 3) for y in range(2)] for x in range(2)]))
items.append(('tetra anti-diagonal', [[-np.eye(4) for y in range(2)] for x in range(2)]))
run_group('(4,4;4,4) structured: tetrahedral targets', items, (4, 4), (4, 4), R=100, joint_n=4)
print(f"wall {time.time()-t00:.0f}s")
