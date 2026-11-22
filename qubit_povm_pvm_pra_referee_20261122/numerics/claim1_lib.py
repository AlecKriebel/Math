"""Claim 1 attack driver: POVM see-saw / joint optimisation vs two-angle PVM bound."""
import itertools, json, time
import numpy as np
from scipy.optimize import minimize
import os
import bell_lib as bl
TWO_ANGLE = os.environ.get("TWO_ANGLE", "v1")


# ----------------------------------------------------------------------------- helpers
def local_bound(c, outsA, outsB):
    """max over local deterministic strategies; c[x][y] (a,b)"""
    best = -np.inf
    for a0 in range(outsA[0]):
        for a1 in range(outsA[1]):
            # Bob optimises each input independently
            v = 0
            for y in range(2):
                v += (c[0][y][a0, :] + c[1][y][a1, :]).max()
            best = max(best, v)
    return best


def seesaw_adaptive(c, MA, MB, mode='povm', chunk=25, max_iters=1500, conv=1e-13):
    """run see-saw, dropping converged instances from the active batch."""
    N = MA[0].shape[0]
    MA = [m.copy() for m in MA]; MB = [m.copy() for m in MB]
    active = np.arange(N)
    nfail = 0; it = 0
    val = np.zeros(N)
    while len(active) and it < max_iters:
        ca = [[c[x][y][active] for y in range(len(MB))] for x in range(len(MA))]
        a_MA, a_MB, psi, v, nf, hist = bl.seesaw(ca, [m[active] for m in MA], [m[active] for m in MB],
                                                 iters=chunk, mode=mode, stop=conv, return_hist=True)
        nfail += nf; it += len(hist) - 1
        for x in range(len(MA)): MA[x][active] = a_MA[x]
        for y in range(len(MB)): MB[y][active] = a_MB[y]
        val[active] = v
        if len(hist) >= 3:
            sc = 1 + np.abs(hist[-1])
            done = (np.abs(hist[-1] - hist[-2]) < conv * sc) & (np.abs(hist[-2] - hist[-3]) < conv * sc)
        else:
            done = np.zeros(len(active), dtype=bool)
        active = active[~done]
    return MA, MB, val, nfail, it, len(active)


def rep(cs, R):
    return [[np.repeat(cs[x][y], R, axis=0) for y in range(len(cs[0]))] for x in range(len(cs))]


def single(cs, f):
    return [[cs[x][y][f] for y in range(len(cs[0]))] for x in range(len(cs))]


# ----------------------------------------------------------------------------- joint optimisation
def joint_value(params, c1, outsA, outsB):
    """params (P, D) -> lambda_max (P,).  Each effect M_a = S^-1/2 A_a^dag A_a S^-1/2, A_a 2x2 complex."""
    P = params.shape[0]
    pos = 0
    Ms = []
    for n in list(outsA) + list(outsB):
        blk = params[:, pos: pos + 8 * n]; pos += 8 * n
        A = (blk[:, : 4 * n] + 1j * blk[:, 4 * n:]).reshape(P, n, 2, 2)
        M = A.conj().transpose(0, 1, 3, 2) @ A
        S = M.sum(1)
        es, U = np.linalg.eigh(S)
        Sih = np.einsum('nij,nj,nkj->nik', U, 1 / np.sqrt(es), U.conj())
        Ms.append(np.einsum('nij,najk,nkl->nail', Sih, M, Sih))
    MA = Ms[:len(outsA)]; MB = Ms[len(outsA):]
    cb = [[np.broadcast_to(c1[x][y], (P,) + c1[x][y].shape) for y in range(len(outsB))] for x in range(len(outsA))]
    B = bl.bell_operator(cb, MA, MB)
    B = 0.5 * (B + B.conj().transpose(0, 2, 1))
    return np.linalg.eigvalsh(B)[:, -1], MA, MB


def joint_opt(c1, outsA, outsB, rng, x0=None, maxiter=400, h=1e-6):
    D = 8 * (sum(outsA) + sum(outsB))
    if x0 is None:
        x0 = rng.normal(size=D)
    eye = np.eye(D)

    def f(x):
        return -joint_value(x[None], c1, outsA, outsB)[0][0]

    def g(x):
        X = np.concatenate([x[None] + h * eye, x[None] - h * eye], 0)
        v = joint_value(X, c1, outsA, outsB)[0]
        return -(v[:D] - v[D:]) / (2 * h)

    r = minimize(f, x0, jac=g, method='L-BFGS-B', options=dict(maxiter=maxiter, gtol=1e-9, ftol=1e-15))
    v, MA, MB = joint_value(r.x[None], c1, outsA, outsB)
    return float(v[0]), MA, MB


# ----------------------------------------------------------------------------- main evaluation
def evaluate(cs, outsA, outsB, rng, R=40, Rp=20, Rseed=3, joint_n=0, joint_starts=3, names=None, verbose=True,
             ngrid=6, ntop=60):
    """cs[x][y]: (F, a, b).  Returns dict of arrays + list of flagged cases."""
    F = cs[0][0].shape[0]
    t0 = time.time()
    # 1. two-angle PVM bound
    pvm2 = np.zeros(F); strat = []
    for f in range(F):
        r = (bl.pvm_two_angle_v2(single(cs, f), outsA, outsB, ngrid=(12 if max(outsA + outsB) <= 3 else 8)) if TWO_ANGLE == 'v2'
             else bl.pvm_two_angle(single(cs, f), outsA, outsB, ngrid=ngrid, ntop=ntop))
        pvm2[f] = r['value']; strat.append(r)
    t1 = time.time()
    loc = np.array([local_bound(single(cs, f), outsA, outsB) for f in range(F)])
    # 2. PVM see-saw (arbitrary complex Bloch directions, labels chosen optimally at each step)
    N = F * Rp
    cb = rep(cs, Rp)
    kinds = ['pvm', 'full']
    MA = [np.concatenate([bl.random_povm(rng, N // 2, outsA[x], kinds[0]), bl.random_povm(rng, N - N // 2, outsA[x], kinds[1])]) for x in range(2)]
    MB = [np.concatenate([bl.random_povm(rng, N // 2, outsB[y], kinds[0]), bl.random_povm(rng, N - N // 2, outsB[y], kinds[1])]) for y in range(2)]
    perm = rng.permutation(N)  # mix the kinds across functionals
    MA = [m[perm] for m in MA]; MB = [m[perm] for m in MB]
    MA, MB, val, nf, its, left = seesaw_adaptive(cb, MA, MB, mode='pvm')
    cv, MAs, MBs, _ = bl.certified_value(cb, MA, MB)
    proj_ok = all(bl.is_projective(m).all() for m in MAs + MBs)
    pvmss = cv.reshape(F, Rp).max(1)
    t2 = time.time()
    # 3. POVM see-saw, random inits
    N = F * R
    cb = rep(cs, R)
    kk = ['full', 'rank1', 'pvm']
    def mixed(n):
        parts = [bl.random_povm(rng, N // 3 + (1 if i < N % 3 else 0), n, kk[i]) for i in range(3)]
        return np.concatenate(parts)[rng.permutation(N)]
    MA = [mixed(outsA[x]) for x in range(2)]; MB = [mixed(outsB[y]) for y in range(2)]
    MA, MB, val, nf_povm, its_povm, left_povm = seesaw_adaptive(cb, MA, MB, mode='povm')
    cv, MAr, MBr, psir = bl.certified_value(cb, MA, MB)
    cvr = cv.reshape(F, R)
    povmss = cvr.max(1); arg_r = cvr.argmax(1)
    t3 = time.time()
    # 4. POVM see-saw seeded at the two-angle PVM optimiser (exact + perturbed)
    eps = [0.0] + [e for e in (1e-3, 1e-2, 0.1, 0.3) for _ in range(Rseed)]
    Rs = len(eps)
    N = F * Rs
    cb = rep(cs, Rs)
    SA = [np.zeros((N, outsA[x], 2, 2), dtype=complex) for x in range(2)]
    SB = [np.zeros((N, outsB[y], 2, 2), dtype=complex) for y in range(2)]
    for f in range(F):
        mA, mB = bl.two_angle_strategy(strat[f], outsA, outsB)
        for x in range(2): SA[x][f * Rs:(f + 1) * Rs] = mA[x]
        for y in range(2): SB[y][f * Rs:(f + 1) * Rs] = mB[y]
    ee = np.tile(np.array(eps), F)[:, None, None, None]
    SA = [bl.sanitize((1 - ee) * SA[x] + ee * bl.random_povm(rng, N, outsA[x], 'full')) for x in range(2)]
    SB = [bl.sanitize((1 - ee) * SB[y] + ee * bl.random_povm(rng, N, outsB[y], 'full')) for y in range(2)]
    _, start_val = bl.top_state(cb, SA, SB)
    start_exact = start_val.reshape(F, Rs)[:, 0]
    SA, SB, val, nf_seed, its_seed, left_seed = seesaw_adaptive(cb, SA, SB, mode='povm')
    cvs, SAs, SBs, psis = bl.certified_value(cb, SA, SB)
    cvs = cvs.reshape(F, Rs)
    seed_exact = cvs[:, 0]
    povmseed = cvs.max(1); arg_s = cvs.argmax(1)
    t4 = time.time()
    # 5. joint optimisation on a subset
    joint = np.full(F, -np.inf)
    for f in range(min(joint_n, F)):
        c1 = single(cs, f)
        for s in range(joint_starts):
            v, mA, mB = joint_opt(c1, outsA, outsB, rng)
            # polish with POVM see-saw
            c1b = [[c1[x][y][None] for y in range(2)] for x in range(2)]
            mA, mB, vv, _, _, _ = seesaw_adaptive(c1b, mA, mB, mode='povm')
            cvj, _, _, _ = bl.certified_value(c1b, mA, mB)
            joint[f] = max(joint[f], v, cvj[0])
    t5 = time.time()
    pvm_best = np.maximum(pvm2, pvmss)
    povm_best = np.maximum(np.maximum(povmss, povmseed), joint)
    gap = povm_best - pvm_best
    flagged = []
    for f in np.where(gap > 1e-7 * (1 + np.abs(pvm_best)))[0]:
        f = int(f)
        if povmss[f] >= povmseed[f]:
            i = f * R + int(arg_r[f]); mA = [m[i] for m in MAr]; mB = [m[i] for m in MBr]; ps = psir[i]
        else:
            i = f * Rs + int(arg_s[f]); mA = [m[i] for m in SAs]; mB = [m[i] for m in SBs]; ps = psis[i]
        flagged.append(dict(index=f, name=(names[f] if names else None), gap=float(gap[f]), povm=float(povm_best[f]),
                            pvm_two_angle=float(pvm2[f]), pvm_seesaw=float(pvmss[f]),
                            c=[[cs[x][y][f].tolist() for y in range(2)] for x in range(2)],
                            MA_re=[m.real.tolist() for m in mA], MA_im=[m.imag.tolist() for m in mA],
                            MB_re=[m.real.tolist() for m in mB], MB_im=[m.imag.tolist() for m in mB],
                            psi_re=ps.real.tolist(), psi_im=ps.imag.tolist()))
    out = dict(F=F, R=R, Rp=Rp, Rs=Rs, pvm2=pvm2, pvmss=pvmss, povmss=povmss, povmseed=povmseed, seed_exact=seed_exact,
               start_exact=start_exact, joint=joint, local=loc, gap=gap, flagged=flagged, pvm_seesaw_projective=bool(proj_ok),
               nfail=dict(povm=int(nf_povm), seed=int(nf_seed)), iters=dict(povm=int(its_povm), seed=int(its_seed)),
               unconverged=dict(povm=int(left_povm), seed=int(left_seed)),
               frac_restarts_at_opt=float((cvr >= pvm_best[:, None] - 1e-6 * (1 + np.abs(pvm_best[:, None]))).mean()),
               times=dict(two_angle=t1 - t0, pvm_ss=t2 - t1, povm_ss=t3 - t2, seed=t4 - t3, joint=t5 - t4))
    if verbose:
        print(f"   F={F}: time two-angle {t1-t0:.1f}s, PVM-ss {t2-t1:.1f}s, POVM-ss {t3-t2:.1f}s ({its_povm} its, unconverged {left_povm}), "
              f"seeded {t4-t3:.1f}s, joint {t5-t4:.1f}s", flush=True)
    return out


def summarize(res, label):
    gap = res['gap']; pb = np.maximum(res['pvm2'], res['pvmss'])
    q = (pb > res['local'] + 1e-7)
    lines = []
    lines.append(f"[{label}] F={res['F']}  restarts: POVM random {res['R']}, POVM seeded-at-PVM {res['Rs']}, PVM see-saw {res['Rp']}")
    lines.append(f"   functionals with qubit value > local bound: {int(q.sum())}/{res['F']}")
    lines.append(f"   max (POVM - PVM) gap = {gap.max():+.3e}   min gap = {gap.min():+.3e}   #gap>1e-7: {int((gap > 1e-7).sum())}   #|gap|<=1e-7: {int((np.abs(gap) <= 1e-7).sum())}")
    lines.append(f"   POVM random-restart see-saw alone reached PVM bound (within 1e-6) for {int((res['povmss'] >= pb - 1e-6*(1+np.abs(pb))).sum())}/{res['F']} functionals; "
                 f"fraction of all restarts at optimum {res['frac_restarts_at_opt']:.3f}")
    lines.append(f"   PVM see-saw (general Bloch dirs) - two-angle bound: max {np.max(res['pvmss'] - res['pvm2']):+.3e} (must be <= 0), "
                 f"#equal within 1e-7: {int((np.abs(res['pvmss'] - res['pvm2']) < 1e-7).sum())}")
    lines.append(f"   sanity: POVM see-saw started at PVM optimiser minus PVM bound: min {np.min(res['seed_exact'] - res['pvm2']):+.3e}, max {np.max(res['seed_exact'] - res['pvm2']):+.3e}; "
                 f"start value - two-angle value max abs {np.max(np.abs(res['start_exact'] - res['pvm2'])):.2e}")
    lines.append(f"   seeded (perturbed PVM optimum) best - PVM bound: max {np.max(res['povmseed'] - pb):+.3e}")
    if np.isfinite(res['joint']).any():
        jm = np.isfinite(res['joint'])
        lines.append(f"   joint L-BFGS optimisation ({int(jm.sum())} functionals): max (joint - PVM) = {np.max(res['joint'][jm] - pb[jm]):+.3e}, "
                     f"#reaching PVM bound within 1e-6: {int((res['joint'][jm] >= pb[jm] - 1e-6*(1+np.abs(pb[jm]))).sum())}")
    lines.append(f"   see-saw POVM-step fallbacks (degenerate instances): {res['nfail']}, unconverged runs: {res['unconverged']}")
    return "\n".join(lines)


def to_jsonable(res):
    out = {}
    for k, v in res.items():
        out[k] = v.tolist() if isinstance(v, np.ndarray) else v
    return out


# ----------------------------------------------------------------------------- functional families
def fam_gaussian(rng, F, outsA, outsB):
    return [[rng.normal(size=(F, outsA[x], outsB[y])) for y in range(2)] for x in range(2)]


def fam_integer(rng, F, outsA, outsB):
    return [[rng.integers(-2, 3, size=(F, outsA[x], outsB[y])).astype(float) for y in range(2)] for x in range(2)]


def random_sign_map(rng, n):
    while True:
        s = rng.choice([-1.0, 1.0], size=n)
        if n == 1 or (s.min() < 0 < s.max()):
            return s


def fam_chsh_embed(rng, F, outsA, outsB):
    """CHSH on random +-1 coarse-grainings plus gaussian noise of random strength"""
    cs = [[np.zeros((F, outsA[x], outsB[y])) for y in range(2)] for x in range(2)]
    for f in range(F):
        sig = rng.choice([0.0, 0.02, 0.1, 0.3, 0.6])
        fa = [random_sign_map(rng, outsA[x]) for x in range(2)]; gb = [random_sign_map(rng, outsB[y]) for y in range(2)]
        for x in range(2):
            for y in range(2):
                s = -1.0 if (x, y) == (1, 1) else 1.0
                cs[x][y][f] = s * np.outer(fa[x], gb[y]) + sig * rng.normal(size=(outsA[x], outsB[y]))
    return cs


def random_strategy(rng, N, outsA, outsB, kind='rank1', maxent=None):
    MA = [bl.random_povm(rng, N, n, kind) for n in outsA]; MB = [bl.random_povm(rng, N, n, kind) for n in outsB]
    th = rng.uniform(0, np.pi / 4, size=N) if maxent is None else np.full(N, np.pi / 4 if maxent else 0.3)
    psi = np.zeros((N, 2, 2), dtype=complex)
    psi[:, 0, 0] = np.cos(th); psi[:, 1, 1] = np.sin(th)
    # random local unitaries are irrelevant since POVMs are Haar-random
    return MA, MB, psi


def fam_povm_target(rng, F, outsA, outsB):
    """functionals built from the behaviour q of a random genuinely-POVM strategy:
       c = q - qA*qB (connected part), or q itself, or sign pattern, randomly chosen."""
    MA, MB, psi = random_strategy(rng, F, outsA, outsB, 'rank1')
    psi[: F // 2, 0, 0] = psi[: F // 2, 1, 1] = np.sqrt(0.5)  # half maximally entangled
    q = bl.behavior(MA, MB, psi)
    cs = [[None, None], [None, None]]
    mode = rng.integers(0, 4, size=F)
    for x in range(2):
        for y in range(2):
            qa = q[x][y].sum(2, keepdims=True); qb = q[x][y].sum(1, keepdims=True)
            conn = q[x][y] - qa * qb
            with np.errstate(divide='ignore', invalid='ignore'):
                lr = np.log(np.clip(q[x][y], 1e-6, None) / np.clip(qa * qb, 1e-6, None))
            alt = [conn * 10, q[x][y] * 5, lr, conn * 10 + 0.3 * rng.normal(size=conn.shape)]
            cs[x][y] = np.where((mode == 0)[:, None, None], alt[0], np.where((mode == 1)[:, None, None], alt[1],
                               np.where((mode == 2)[:, None, None], alt[2], alt[3])))
    return cs


def fam_discrimination(rng, F, outsA, outsB):
    """CHSH on coarse-grainings (weight mu) + state-discrimination style terms on the multi-outcome inputs,
    mimicking the paper's 3x2 construction but with only two inputs per party."""
    cs = [[np.zeros((F, outsA[x], outsB[y])) for y in range(2)] for x in range(2)]
    for f in range(F):
        mu = rng.choice([0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0])
        fa = [random_sign_map(rng, outsA[x]) for x in range(2)]; gb = [random_sign_map(rng, outsB[y]) for y in range(2)]
        for x in range(2):
            for y in range(2):
                s = -1.0 if (x, y) == (1, 1) else 1.0
                cs[x][y][f] = mu * s * np.outer(fa[x], gb[y])
        # Alice's input xs: each label a rewarded jointly with a random Bob event (y_a, b_a)
        for (party, outs) in (('A', outsA), ('B', outsB)):
            if party == 'B' and rng.random() < 0.5:
                continue
            xs = int(np.argmax(outs)) if outs[0] != outs[1] else int(rng.integers(0, 2))
            for a in range(outs[xs]):
                wgt = rng.choice([0.6, 0.8, 1.0, rng.uniform(0.3, 1.0)])
                yo = int(rng.integers(0, 2))
                other = outsB if party == 'A' else outsA
                bo = int(rng.integers(0, other[yo]))
                if party == 'A':
                    cs[xs][yo][f][a, bo] += wgt
                else:
                    cs[yo][xs][f][bo, a] += wgt
    return cs


FAMILIES = dict(gaussian=fam_gaussian, integer=fam_integer, chsh_embed=fam_chsh_embed, povm_target=fam_povm_target,
                discrimination=fam_discrimination)


# ----------------------------------------------------------------------------- nonlocal-filtered families
def filter_nonlocal(gen, rng, F, outsA, outsB, oversample=25, max_rounds=4, Rf=6):
    """rejection-sample functionals whose qubit (PVM see-saw) value strictly exceeds the local bound."""
    keep = [[[] for _ in range(2)] for _ in range(2)]
    got = 0
    for rnd in range(max_rounds):
        G = oversample * F
        cs = gen(rng, G, outsA, outsB)
        loc = np.array([local_bound(single(cs, f), outsA, outsB) for f in range(G)])
        cb = rep(cs, Rf)
        N = G * Rf
        MA = [bl.random_povm(rng, N, outsA[x], 'pvm') for x in range(2)]
        MB = [bl.random_povm(rng, N, outsB[y], 'pvm') for y in range(2)]
        MA, MB, val, nf, its, left = seesaw_adaptive(cb, MA, MB, mode='pvm', max_iters=200)
        best = val.reshape(G, Rf).max(1)
        nl = np.where(best > loc + 1e-3 * (1 + np.abs(loc)))[0]
        for x in range(2):
            for y in range(2):
                keep[x][y].append(cs[x][y][nl])
        got += len(nl)
        if got >= F:
            break
    out = [[np.concatenate(keep[x][y])[:F] for y in range(2)] for x in range(2)]
    return out


def fam_gaussian_nl(rng, F, outsA, outsB):
    return filter_nonlocal(fam_gaussian, rng, F, outsA, outsB)


def fam_integer_nl(rng, F, outsA, outsB):
    return filter_nonlocal(fam_integer, rng, F, outsA, outsB)


def fam_povm_target_nl(rng, F, outsA, outsB):
    return filter_nonlocal(fam_povm_target, rng, F, outsA, outsB)


def fam_discrimination_nl(rng, F, outsA, outsB):
    return filter_nonlocal(fam_discrimination, rng, F, outsA, outsB, oversample=6)


FAMILIES = dict(gaussian=fam_gaussian, gaussian_nonlocal=fam_gaussian_nl, integer_nonlocal=fam_integer_nl,
                chsh_embed=fam_chsh_embed, povm_target=fam_povm_target, povm_target_nonlocal=fam_povm_target_nl,
                discrimination=fam_discrimination, discrimination_nonlocal=fam_discrimination_nl)


# ----------------------------------------------------------------------------- witness families (LP / nearest local point)
from scipy.optimize import linprog, nnls


def det_vertices(outsA, outsB):
    """all local deterministic behaviours flattened in the order (x,y,a,b)"""
    V = []
    for a0 in range(outsA[0]):
        for a1 in range(outsA[1]):
            for b0 in range(outsB[0]):
                for b1 in range(outsB[1]):
                    a = (a0, a1); b = (b0, b1)
                    vec = []
                    for x in range(2):
                        for y in range(2):
                            m = np.zeros((outsA[x], outsB[y])); m[a[x], b[y]] = 1
                            vec.append(m.ravel())
                    V.append(np.concatenate(vec))
    return np.array(V)


def flat(q, f):
    return np.concatenate([q[x][y][f].ravel() for x in range(2) for y in range(2)])


def unflat(vecs, outsA, outsB):
    """vecs (F, D) -> cs[x][y] (F,a,b)"""
    cs = [[None, None], [None, None]]; pos = 0
    for x in range(2):
        for y in range(2):
            n = outsA[x] * outsB[y]
            cs[x][y] = vecs[:, pos:pos + n].reshape(-1, outsA[x], outsB[y]).copy(); pos += n
    return cs


def mixed_strategy_behaviors(rng, G, outsA, outsB):
    """behaviours of random qubit strategies with a random mix of PVM / rank-one POVM measurements"""
    def meas(n):
        kinds = rng.integers(0, 2, size=G)
        Mp = bl.random_povm(rng, G, n, 'pvm'); Mr = bl.random_povm(rng, G, n, 'rank1')
        return np.where((kinds == 0)[:, None, None, None], Mp, Mr)
    MA = [meas(n) for n in outsA]; MB = [meas(n) for n in outsB]
    th = rng.uniform(np.pi / 8, np.pi / 4, size=G)
    th[: G // 2] = np.pi / 4
    psi = np.zeros((G, 2, 2), dtype=complex); psi[:, 0, 0] = np.cos(th); psi[:, 1, 1] = np.sin(th)
    return bl.behavior(MA, MB, psi), MA, MB, psi


def fam_witness(rng, F, outsA, outsB, kind='lp', oversample=30, max_rounds=6):
    V = det_vertices(outsA, outsB)
    D = V.shape[1]
    out = []
    for rnd in range(max_rounds):
        G = oversample * F
        q, MA, MB, psi = mixed_strategy_behaviors(rng, G, outsA, outsB)
        for f in range(G):
            qf = flat(q, f)
            if kind == 'lp':
                # maximise <c,q> - t  s.t. <c,d> <= t for all deterministic d, -1 <= c <= 1
                cost = np.concatenate([-qf, [1.0]])
                A_ub = np.hstack([V, -np.ones((V.shape[0], 1))])
                r = linprog(cost, A_ub=A_ub, b_ub=np.zeros(V.shape[0]), bounds=[(-1, 1)] * D + [(None, None)], method='highs')
                if r.status == 0 and -r.fun > 1e-4:
                    out.append(r.x[:D])
            else:
                # nearest point of the local polytope (NNLS with heavily weighted normalisation row)
                Wt = 1e3
                Amat = np.vstack([V.T, Wt * np.ones((1, V.shape[0]))])
                lam, _ = nnls(Amat, np.concatenate([qf, [Wt]]), maxiter=20000)
                d = qf - V.T @ lam
                nd = np.linalg.norm(d)
                if nd > 1e-3 and (d @ qf - (V @ d).max()) > 1e-6:
                    out.append(d / nd * 5)
            if len(out) >= F:
                break
        if len(out) >= F:
            break
    if not out:
        return unflat(np.zeros((0, D)), outsA, outsB)
    return unflat(np.array(out[:F]), outsA, outsB)


def fam_lp_witness(rng, F, outsA, outsB):
    return fam_witness(rng, F, outsA, outsB, 'lp')


def fam_nearest_witness(rng, F, outsA, outsB):
    return fam_witness(rng, F, outsA, outsB, 'nearest')


FAMILIES = dict(gaussian=fam_gaussian, integer=fam_integer, chsh_embed=fam_chsh_embed, povm_target=fam_povm_target,
                discrimination=fam_discrimination, discrimination_nonlocal=fam_discrimination_nl,
                lp_witness=fam_lp_witness, nearest_local_witness=fam_nearest_witness)
