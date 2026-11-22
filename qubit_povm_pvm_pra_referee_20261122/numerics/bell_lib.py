"""Independent numerical toolkit for qubit Bell optimisation (POVM vs PVM).

Conventions
-----------
A Bell functional is c[x][y] = real array of shape (..., a_x, b_y) (leading batch axis N).
Alice's measurement at input x: MA[x] of shape (N, a_x, 2, 2); Bob: MB[y] of shape (N, b_y, 2, 2).
State psi of shape (N, 2, 2) (first index Alice, second Bob).
value = sum_{x,y,a,b} c[x][y][a,b] <psi| MA[x][a] (x) MB[y][b] |psi>.

Single-measurement POVM optimisation (exact, no SDP solver):
   max sum_a Tr(K_a M_a),  M_a >= 0, sum_a M_a = 1 on C^2.
With K_a = k_a 1 + kappa_a.sigma and M_a = w_a 1 + v_a.sigma the dual is
   min_gamma 2 max_a (k_a + |gamma - kappa_a|)
(smallest ball enclosing balls).  The optimum is determined by an active set of at most 4 labels
with affinely independent centres; we enumerate all subsets of size <= 4, solve the resulting
quadratic, and accept a candidate iff it is dual feasible AND admits nonnegative primal weights
(complementary slackness) -- such a candidate is provably optimal (zero duality gap).
"""
import itertools
import numpy as np

I2 = np.eye(2)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]])
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


# ----------------------------------------------------------------------------- Bloch helpers
def to_bloch(K):
    k = 0.5 * (K[..., 0, 0].real + K[..., 1, 1].real)
    kx = 0.5 * (K[..., 0, 1] + K[..., 1, 0]).real
    ky = 0.5 * (1j * (K[..., 0, 1] - K[..., 1, 0])).real
    kz = 0.5 * (K[..., 0, 0] - K[..., 1, 1]).real
    return k, np.stack([kx, ky, kz], -1)


def from_bloch(w, v):
    M = np.empty(w.shape + (2, 2), dtype=complex)
    M[..., 0, 0] = w + v[..., 2]
    M[..., 1, 1] = w - v[..., 2]
    M[..., 0, 1] = v[..., 0] - 1j * v[..., 1]
    M[..., 1, 0] = v[..., 0] + 1j * v[..., 1]
    return M


# ----------------------------------------------------------------------------- exact POVM step
def solve_povm_batch(k, kap, tol=1e-9):
    """Exact optimum of max sum_a Tr(K_a M_a) over qubit POVMs, batched.

    k: (N, n), kap: (N, n, 3).  Returns w (N,n), v (N,n,3), val (N,), found (N,) bool.
    """
    N, n = k.shape
    scale = 1.0 + np.abs(k).max(1) + np.linalg.norm(kap, axis=-1).max(1)
    ftol = tol * scale
    found = np.zeros(N, dtype=bool)
    w_out = np.zeros((N, n))
    v_out = np.zeros((N, n, 3))
    val = np.full(N, -np.inf)
    ar = np.arange(N)

    def consider(S, gam, t, valid):
        nonlocal found
        m = len(S)
        todo = valid & ~found
        if not todo.any():
            return
        dist = np.linalg.norm(gam[:, None, :] - kap, axis=-1)  # (N, n)
        slack = t[:, None] - k - dist
        feas = todo & np.isfinite(t) & (slack.min(1) >= -ftol)
        if not feas.any():
            return
        if m == 1:
            ok = feas
            wS = np.ones((N, 1))
            nv = np.zeros((N, 1, 3))
        else:
            dS = dist[:, S]
            act = np.abs(slack[:, S]).max(1) <= 10 * ftol
            good = dS.min(1) > 1e-12 * scale
            nv = (kap[:, S, :] - gam[:, None, :]) / np.where(dS > 0, dS, 1.0)[..., None]
            if m == 2:
                wS = np.full((N, 2), 0.5)
                okw = (nv[:, 0] * nv[:, 1]).sum(-1) < -1 + 1e-7
            elif m == 3:
                c0 = np.cross(nv[:, 1], nv[:, 2]); c1 = np.cross(nv[:, 2], nv[:, 0]); c2 = np.cross(nv[:, 0], nv[:, 1])
                s = c0 + c1 + c2
                ss = (s * s).sum(-1)
                ssafe = np.where(ss > 1e-18, ss, 1.0)
                wS = np.stack([(c0 * s).sum(-1), (c1 * s).sum(-1), (c2 * s).sum(-1)], -1) / ssafe[:, None]
                okw = ss > 1e-18
            else:
                def det3(a, b, c):
                    return (a * np.cross(b, c)).sum(-1)
                d0 = det3(nv[:, 1], nv[:, 2], nv[:, 3]); d1 = -det3(nv[:, 0], nv[:, 2], nv[:, 3])
                d2 = det3(nv[:, 0], nv[:, 1], nv[:, 3]); d3 = -det3(nv[:, 0], nv[:, 1], nv[:, 2])
                sm = d0 + d1 + d2 + d3
                smsafe = np.where(np.abs(sm) > 1e-12, sm, 1.0)
                wS = np.stack([d0, d1, d2, d3], -1) / smsafe[:, None]
                okw = np.abs(sm) > 1e-12
            res = np.linalg.norm((wS[..., None] * nv).sum(1), axis=-1)
            okw = okw & (wS.min(1) >= -1e-9) & (res <= 1e-8) & (np.abs(wS.sum(1) - 1) <= 1e-8)
            ok = feas & act & good & okw
        if not ok.any():
            return
        idx = ar[ok]
        wS_ok = np.clip(wS[ok], 0, None)
        for j, a in enumerate(S):
            w_out[idx, a] = wS_ok[:, j]
            v_out[idx, a, :] = wS_ok[:, j, None] * nv[ok, j, :]
        val[idx] = 2 * t[ok]
        found[idx] = True

    for m in range(1, min(n, 4) + 1):
        for S in itertools.combinations(range(n), m):
            S = list(S)
            k0 = k[:, S[0]]
            c0 = kap[:, S[0], :]
            if m == 1:
                consider(S, c0, k0, np.ones(N, dtype=bool))
                continue
            E = kap[:, S[1:], :] - c0[:, None, :]  # (N, m-1, 3)
            Gm = E @ E.transpose(0, 2, 1)
            p = k[:, S[1:]] - k0[:, None]
            q = 0.5 * ((E * E).sum(-1) - k[:, S[1:]] ** 2 + k0[:, None] ** 2)
            det = np.linalg.det(Gm)
            tr = np.trace(Gm, axis1=1, axis2=2) / (m - 1)
            nons = np.abs(det) > 1e-13 * np.maximum(tr, 1e-300) ** (m - 1)
            Gs = np.where(nons[:, None, None], Gm, np.eye(m - 1)[None])
            c1 = np.linalg.solve(Gs, p[..., None])[..., 0]
            c0v = np.linalg.solve(Gs, q[..., None])[..., 0]
            a2 = np.einsum('ni,nij,nj->n', c1, Gs, c1) - 1.0
            a1 = 2 * np.einsum('ni,nij,nj->n', c1, Gs, c0v) + 2 * k0
            a0 = np.einsum('ni,nij,nj->n', c0v, Gs, c0v) - k0 ** 2
            disc = a1 * a1 - 4 * a2 * a0
            okd = nons & (disc >= -1e-9 * (1 + a1 * a1))
            sq = np.sqrt(np.clip(disc, 0, None))
            sg = np.where(a1 >= 0, 1.0, -1.0)
            qq = -0.5 * (a1 + sg * sq)
            with np.errstate(divide='ignore', invalid='ignore'):
                t1 = np.where(a2 != 0, qq / np.where(a2 != 0, a2, 1.0), np.inf)
                t2 = np.where(qq != 0, a0 / np.where(qq != 0, qq, 1.0), np.inf)
            for t in (t1, t2):
                tt = np.where(np.isfinite(t), t, 0.0)
                cc = tt[:, None] * c1 + c0v
                gam = c0 + np.einsum('ni,nij->nj', cc, E)
                consider(S, gam, t, okd & np.isfinite(t))
            if found.all():
                break
        if found.all():
            break
    return w_out, v_out, val, found


def solve_pvm_batch(k, kap):
    """Exact optimum over labelled qubit PVMs (identity on one label, or two orthogonal rank-one
    projectors on an ordered pair of labels).  Returns w, v, val."""
    N, n = k.shape
    ar = np.arange(N)
    best = 2 * k.max(1)
    arg = k.argmax(1)
    w_out = np.zeros((N, n)); v_out = np.zeros((N, n, 3))
    w_out[ar, arg] = 1.0
    for a in range(n):
        for b in range(a + 1, n):
            d = kap[:, a] - kap[:, b]
            nd = np.linalg.norm(d, axis=-1)
            v = k[:, a] + k[:, b] + nd
            upd = v > best + 1e-15
            if upd.any():
                best = np.where(upd, v, best)
                idx = ar[upd]
                w_out[idx] = 0; v_out[idx] = 0
                nn = d[upd] / np.where(nd[upd] > 0, nd[upd], 1.0)[:, None]
                w_out[idx, a] = 0.5; w_out[idx, b] = 0.5
                v_out[idx, a] = 0.5 * nn; v_out[idx, b] = -0.5 * nn
    return w_out, v_out, best


# ----------------------------------------------------------------------------- Bell operator etc.
def bell_operator(c, MA, MB):
    N = MA[0].shape[0]
    B = np.zeros((N, 2, 2, 2, 2), dtype=complex)
    for y in range(len(MB)):
        for x in range(len(MA)):
            cN = np.einsum('nab,nbkl->nakl', c[x][y], MB[y])
            B += np.einsum('naij,nakl->nikjl', MA[x], cN)
    return B.reshape(N, 4, 4)


def top_state(c, MA, MB):
    B = bell_operator(c, MA, MB)
    B = 0.5 * (B + B.conj().transpose(0, 2, 1))
    ev, evec = np.linalg.eigh(B)
    psi = evec[:, :, -1].reshape(-1, 2, 2)
    return psi, ev[:, -1]


def value(c, MA, MB, psi):
    B = bell_operator(c, MA, MB)
    p = psi.reshape(-1, 4)
    return np.einsum('ni,nij,nj->n', p.conj(), B, p).real


def behavior(MA, MB, psi):
    """p[x][y] of shape (N, a, b)"""
    out = []
    for x in range(len(MA)):
        row = []
        for y in range(len(MB)):
            row.append(np.einsum('nik,naij,nbkl,njl->nab', psi.conj(), MA[x], MB[y], psi).real)
        out.append(row)
    return out


def alice_scores(c, MB, psi, x):
    """K[n,a] 2x2 with value contribution of input x = sum_a Tr(K_a M_a)."""
    K = 0
    for y in range(len(MB)):
        R = np.einsum('nik,nbkl,njl->nbji', psi.conj(), MB[y], psi)
        K = K + np.einsum('nab,nbji->naji', c[x][y], R)
    return K


def bob_scores(c, MA, psi, y):
    K = 0
    for x in range(len(MA)):
        Q = np.einsum('nik,naij,njl->nalk', psi.conj(), MA[x], psi)
        K = K + np.einsum('nab,nalk->nblk', c[x][y], Q)
    return K


def sanitize(M):
    """Project to an exactly valid POVM: clip negative eigenvalues, renormalise by S^{-1/2}."""
    M = 0.5 * (M + M.conj().transpose(0, 1, 3, 2))
    ev, U = np.linalg.eigh(M)
    ev = np.clip(ev, 0, None)
    M = np.einsum('naij,naj,nakj->naik', U, ev, U.conj())
    S = M.sum(1)
    es, Us = np.linalg.eigh(S)
    Sih = np.einsum('nij,nj,nkj->nik', Us, 1 / np.sqrt(es), Us.conj())
    M = np.einsum('nij,najk,nkl->nail', Sih, M, Sih)
    return M


def povm_validity(M):
    ev = np.linalg.eigvalsh(0.5 * (M + M.conj().transpose(0, 1, 3, 2)))
    S = M.sum(1)
    return ev.min(axis=(1, 2)), np.abs(S - np.eye(2)[None]).max(axis=(1, 2))


def is_projective(M, tol=1e-8):
    """each effect a projector (M^2 = M)"""
    return np.abs(M @ M - M).max(axis=(1, 2, 3)) < tol


def seesaw(c, MA, MB, iters=300, mode='povm', stop=1e-13, return_hist=False, verbose=False):
    """Alternating optimisation.  mode in {'povm','pvm'}.  Returns MA, MB, psi, val, nfail."""
    MA = [m.copy() for m in MA]; MB = [m.copy() for m in MB]
    nfail = 0
    psi, val = top_state(c, MA, MB)
    hist = [val.copy()]

    def step(K, Mold):
        nonlocal nfail
        k, kap = to_bloch(K)
        if mode == 'povm':
            w, v, vv, found = solve_povm_batch(k, kap)
            Mnew = from_bloch(w, v)
            nf = (~found).sum()
            if nf:
                # borderline/degenerate instance: fall back to the better of (old POVM, exact PVM step)
                nfail += int(nf)
                nfi = np.where(~found)[0]
                w2, v2, v2val = solve_pvm_batch(k[nfi], kap[nfi])
                oldval = np.einsum('naij,naji->n', K[nfi], Mold[nfi]).real
                Mp = from_bloch(w2, v2)
                use = v2val > oldval
                Mnew[nfi] = np.where(use[:, None, None, None], Mp, Mold[nfi])
            return Mnew
        else:
            w, v, vv = solve_pvm_batch(k, kap)
            return from_bloch(w, v)

    for it in range(iters):
        for x in range(len(MA)):
            MA[x] = step(alice_scores(c, MB, psi, x), MA[x])
        psi, _ = top_state(c, MA, MB)
        for y in range(len(MB)):
            MB[y] = step(bob_scores(c, MA, psi, y), MB[y])
        psi, val = top_state(c, MA, MB)
        hist.append(val.copy())
        if it >= 3 and np.abs(hist[-1] - hist[-2]).max() < stop and np.abs(hist[-2] - hist[-3]).max() < stop:
            break
        if verbose and it % 50 == 0:
            print('  it', it, 'max', val.max(), 'max inc', np.abs(hist[-1] - hist[-2]).max(), flush=True)
    if return_hist:
        return MA, MB, psi, val, nfail, np.array(hist)
    return MA, MB, psi, val, nfail


def certified_value(c, MA, MB):
    """Sanitise POVMs to exactly valid ones and return lambda_max of the Bell operator."""
    MA = [sanitize(m) for m in MA]; MB = [sanitize(m) for m in MB]
    psi, val = top_state(c, MA, MB)
    return val, MA, MB, psi


# ----------------------------------------------------------------------------- random initialisations
def random_povm(rng, N, n, kind='full'):
    """random POVM with n effects. kind: 'full' (rank-2 effects), 'rank1', 'pvm'"""
    if kind == 'pvm':
        # random labelled PVM
        v = rng.normal(size=(N, 3)); v /= np.linalg.norm(v, axis=-1, keepdims=True)
        w = np.zeros((N, n)); vv = np.zeros((N, n, 3))
        a = rng.integers(0, n, size=N); b = rng.integers(0, n, size=N)
        ar = np.arange(N)
        np.add.at(w, (ar, a), 0.5); np.add.at(w, (ar, b), 0.5)
        np.add.at(vv, (ar, a), 0.5 * v); np.add.at(vv, (ar, b), -0.5 * v)
        return from_bloch(w, vv)
    if kind == 'rank1':
        A = rng.normal(size=(N, n, 1, 2)) + 1j * rng.normal(size=(N, n, 1, 2))
    else:
        A = rng.normal(size=(N, n, 2, 2)) + 1j * rng.normal(size=(N, n, 2, 2))
    M = A.conj().transpose(0, 1, 3, 2) @ A
    return sanitize(M)


# ----------------------------------------------------------------------------- two-angle PVM bound
PPLUS = np.array([[1.0, 0], [0, 0]]); PMINUS = np.array([[0, 0], [0, 1.0]])
ZR = np.array([[1.0, 0], [0, -1]]); XR = np.array([[0, 1.0], [1, 0]])


def party_assignments(n0, n1, ordered_first=False):
    out = []
    for p in range(n0):
        for pp in (range(n0) if ordered_first else range(p, n0)):
            for r in range(n1):
                for rr in range(n1):
                    out.append((p, pp, r, rr))
    return out


def party_effects(assign, theta, n0, n1):
    """assign: (K,4) int array, theta: (K,) -> E0 (K,n0,2,2), E1 (K,n1,2,2) real."""
    assign = np.asarray(assign); K = assign.shape[0]
    ar = np.arange(K)
    E0 = np.zeros((K, n0, 2, 2)); E1 = np.zeros((K, n1, 2, 2))
    np.add.at(E0, (ar, assign[:, 0]), PPLUS[None]); np.add.at(E0, (ar, assign[:, 1]), PMINUS[None])
    Pi = 0.5 * (I2[None] + np.cos(theta)[:, None, None] * ZR[None] + np.sin(theta)[:, None, None] * XR[None])
    np.add.at(E1, (ar, assign[:, 2]), Pi); np.add.at(E1, (ar, assign[:, 3]), I2[None] - Pi)
    return E0, E1


def lam_pairs(c, EA, EB):
    """c[x][y] (a,b); EA=[E0,E1] with (K,a,2,2); EB similarly (K,...) -> lambda_max (K,) elementwise."""
    K = EA[0].shape[0]
    B = np.zeros((K, 2, 2, 2, 2))
    for x in range(2):
        for y in range(2):
            T = np.einsum('ab,kbrs->kars', c[x][y], EB[y])
            B += np.einsum('kapq,kars->kprqs', EA[x], T)
    return np.linalg.eigvalsh(B.reshape(K, 4, 4))[:, -1]


def lam_outer(c, EA, EB):
    """all pairs of configs: (CA, CB)"""
    CA = EA[0].shape[0]; CB = EB[0].shape[0]
    B = np.zeros((CA, CB, 2, 2, 2, 2))
    for x in range(2):
        for y in range(2):
            T = np.einsum('ab,jbrs->jars', c[x][y], EB[y])
            B += np.einsum('iapq,jars->ijprqs', EA[x], T, optimize=True)
    return np.linalg.eigvalsh(B.reshape(CA * CB, 4, 4))[:, -1].reshape(CA, CB)


def pvm_two_angle(c, outsA, outsB, ngrid=6, ntop=60, nzoom=34, ordered_first=False, return_all=False):
    """PVM bound by the two-angle formula.  c[x][y]: (a_x, b_y) real arrays.
    Setting 0 of each party: Z, spectral projectors -> unordered label pair (by the Z->-Z symmetry;
    ordered_first=True enumerates all ordered pairs literally).  Setting 1: cos(t) Z + sin(t) X,
    spectral projectors -> ordered label pair, t in [0, pi].
    """
    grid = np.linspace(0, np.pi, ngrid + 1)
    cfg = []
    for outs in (outsA, outsB):
        asg = party_assignments(outs[0], outs[1], ordered_first)
        A = []; TH = []
        for a in asg:
            if a[0] != a[1] and a[2] != a[3]:
                for t in grid:
                    A.append(a); TH.append(t)
            else:
                A.append(a); TH.append(np.pi / 2)
        cfg.append((np.array(A), np.array(TH)))
    (aA, tA), (aB, tB) = cfg
    EA = party_effects(aA, tA, *outsA); EB = party_effects(aB, tB, *outsB)
    lam = lam_outer(c, EA, EB)
    # shortlist: best config pair for each distinct (assignA, assignB)
    order = np.argsort(lam, axis=None)[::-1]
    seen = set(); sel = []
    for o in order[: 40 * ntop]:
        i, j = divmod(int(o), lam.shape[1])
        key = (tuple(aA[i]), tuple(aB[j]))
        if key in seen:
            continue
        seen.add(key); sel.append((i, j))
        if len(sel) >= ntop:
            break
    si = np.array([s[0] for s in sel]); sj = np.array([s[1] for s in sel])
    sa = aA[si]; sb = aB[sj]; ta = tA[si].copy(); tb = tB[sj].copy()
    freeA = (sa[:, 0] != sa[:, 1]) & (sa[:, 2] != sa[:, 3]); freeB = (sb[:, 0] != sb[:, 1]) & (sb[:, 2] != sb[:, 3])
    h = np.pi / ngrid
    K = len(sel)
    offs = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    oa, ob = np.meshgrid(offs, offs, indexing='ij'); oa = oa.ravel(); ob = ob.ravel()
    best = lam[si, sj].copy()
    for z in range(nzoom):
        TA = np.clip(ta[:, None] + h * oa[None, :] * freeA[:, None], 0, np.pi)
        TB = np.clip(tb[:, None] + h * ob[None, :] * freeB[:, None], 0, np.pi)
        EAz = party_effects(np.repeat(sa, 25, axis=0), TA.ravel(), *outsA)
        EBz = party_effects(np.repeat(sb, 25, axis=0), TB.ravel(), *outsB)
        L = lam_pairs(c, EAz, EBz).reshape(K, 25)
        am = L.argmax(1)
        ar = np.arange(K)
        ta = TA[ar, am]; tb = TB[ar, am]; best = L[ar, am]
        h *= 0.5
    b = int(best.argmax())
    res = dict(value=float(best[b]), assignA=tuple(int(v) for v in sa[b]), assignB=tuple(int(v) for v in sb[b]),
               thetaA=float(ta[b]), thetaB=float(tb[b]), grid_best=float(lam.max()),
               nconfigs=int(lam.size), top_values=np.sort(best)[::-1][:5].tolist())
    if return_all:
        res['all'] = (sa, sb, ta, tb, best)
    return res


def two_angle_strategy(res, outsA, outsB):
    """explicit MA, MB (batch size 1, complex) for a pvm_two_angle result"""
    EA = party_effects(np.array([res['assignA']]), np.array([res['thetaA']]), *outsA)
    EB = party_effects(np.array([res['assignB']]), np.array([res['thetaB']]), *outsB)
    return [e.astype(complex) for e in EA], [e.astype(complex) for e in EB]


# ----------------------------------------------------------------------------- two-angle PVM bound, robust version
def pvm_two_angle_v2(c, outsA, outsB, ngrid=12, nzoom=30, cap=3000, keep2=300):
    """Two-angle PVM bound with a provable shortlist.

    For an assignment pair the Bell operator is B(tA,tB); for the optimal eigenvector the expectation is a
    degree-(1,1) trigonometric polynomial, hence the true maximum of the pair exceeds the value at the nearest
    grid point by at most  margin = (1-cos(h/2)) (L_A + L_B) + G11 (h/2)^2  with
      L_A = 1/2 sum_y max_b |c[1][y][r,b]-c[1][y][r',b]|,  L_B = 1/2 sum_x max_a |c[x][1][a,s]-c[x][1][a,s']|,
      G11 = 1/4 |c11[r,s]-c11[r,s']-c11[r',s]+c11[r',s']|   (zero for parties without a free angle).
    Every grid point with lam + margin >= best grid value is used as a start for local zoom refinement.
    """
    grid = np.linspace(0, np.pi, ngrid + 1); h = np.pi / ngrid
    asg = [party_assignments(*outsA), party_assignments(*outsB)]
    cfg = []
    for pa in asg:
        A = []; TH = []; IDX = []
        for i, a in enumerate(pa):
            if a[0] != a[1] and a[2] != a[3]:
                for t in grid:
                    A.append(a); TH.append(t); IDX.append(i)
            else:
                A.append(a); TH.append(np.pi / 2); IDX.append(i)
        cfg.append((np.array(A), np.array(TH), np.array(IDX)))
    (aA, tA, iA), (aB, tB, iB) = cfg
    EA = party_effects(aA, tA, *outsA); EB = party_effects(aB, tB, *outsB)
    lam = lam_outer(c, EA, EB)
    # margins
    pA = np.array(asg[0]); pB = np.array(asg[1])
    freeA = (pA[:, 0] != pA[:, 1]) & (pA[:, 2] != pA[:, 3]); freeB = (pB[:, 0] != pB[:, 1]) & (pB[:, 2] != pB[:, 3])
    LA = 0.5 * sum(np.abs(c[1][y][pA[:, 2], :] - c[1][y][pA[:, 3], :]).max(1) for y in range(2)) * freeA
    LB = 0.5 * sum(np.abs(c[x][1][:, pB[:, 2]] - c[x][1][:, pB[:, 3]]).max(0) for x in range(2)) * freeB
    c11 = c[1][1]
    G = 0.25 * np.abs(c11[np.ix_(pA[:, 2], pB[:, 2])] - c11[np.ix_(pA[:, 2], pB[:, 3])]
                      - c11[np.ix_(pA[:, 3], pB[:, 2])] + c11[np.ix_(pA[:, 3], pB[:, 3])]) * np.outer(freeA, freeB)
    oc = 1 - np.cos(h / 2)
    marg_pair = oc * (LA[:, None] + LB[None, :]) + G * (h / 2) ** 2
    marg = marg_pair[np.ix_(iA, iB)]
    best_grid = lam.max()
    score = lam + marg
    si, sj = np.where(score >= best_grid - 1e-12)
    capped = False
    if len(si) > cap:
        o = np.argsort(score[si, sj])[::-1][:cap]
        si, sj = si[o], sj[o]; capped = True
    nstarts = len(si)
    sa = aA[si]; sb = aB[sj]; ta = tA[si].copy(); tb = tB[sj].copy(); mg = marg[si, sj]
    fA = freeA[iA[si]]; fB = freeB[iB[sj]]
    offs = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
    oa, ob = np.meshgrid(offs, offs, indexing='ij'); oa = oa.ravel(); ob = ob.ravel()
    best = lam[si, sj].copy()
    hh = h

    def zoom(levels, sa, sb, ta, tb, fA, fB, best, hh):
        for z in range(levels):
            Kk = len(ta)
            TA = np.clip(ta[:, None] + hh * oa[None, :] * fA[:, None], 0, np.pi)
            TB = np.clip(tb[:, None] + hh * ob[None, :] * fB[:, None], 0, np.pi)
            EAz = party_effects(np.repeat(sa, 25, axis=0), TA.ravel(), *outsA)
            EBz = party_effects(np.repeat(sb, 25, axis=0), TB.ravel(), *outsB)
            L = lam_pairs(c, EAz, EBz).reshape(Kk, 25)
            am = L.argmax(1); ar = np.arange(Kk)
            ta = TA[ar, am]; tb = TB[ar, am]; best = L[ar, am]
            hh = hh * 0.5
        return ta, tb, best, hh

    ta, tb, best, hh = zoom(3, sa, sb, ta, tb, fA, fB, best, hh)
    keep = best >= best.max() - mg / 16 - 1e-9
    if keep.sum() > keep2:
        o = np.argsort(np.where(keep, best, -np.inf))[::-1][:keep2]
        k2 = np.zeros_like(keep); k2[o] = True; keep = k2
    sa, sb, ta, tb, fA, fB, best = sa[keep], sb[keep], ta[keep], tb[keep], fA[keep], fB[keep], best[keep]
    ta, tb, best, hh = zoom(nzoom - 3, sa, sb, ta, tb, fA, fB, best, hh)
    b = int(best.argmax())
    return dict(value=float(best[b]), assignA=tuple(int(v) for v in sa[b]), assignB=tuple(int(v) for v in sb[b]),
                thetaA=float(ta[b]), thetaB=float(tb[b]), grid_best=float(best_grid), nconfigs=int(lam.size),
                nstarts=int(nstarts), capped=bool(capped), max_margin=float(mg.max()) if len(mg) else 0.0)
