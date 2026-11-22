#!/usr/bin/env python3
"""Independent exact check of the SOS / Gram certificate (Claim 3).

Written from the formulas in the manuscript only.  Parses G from appendices.tex.
"""
import re, sys, itertools, json
from fractions import Fraction as Fr
import numpy as np

TEX = sys.argv[1]
src = open(TEX).read()

# ---------------------------------------------------------------- parse G
m = re.search(r"G=\\left\(\\begin\{array\}\{\*\{12\}\{r\}\}(.*?)\\end\{array\}", src, re.S)
assert m, "matrix not found"
rows = [r.strip() for r in m.group(1).split("\\\\") if r.strip()]
G = [[int(tok.strip()) for tok in r.split("&")] for r in rows]
assert len(G) == 12 and all(len(r) == 12 for r in G), (len(G), [len(r) for r in G])
print("parsed G: 12x12 integer matrix")

out = {}
# ---------------------------------------------------------------- symmetry
sym = all(G[i][j] == G[j][i] for i in range(12) for j in range(12))
print("symmetric:", sym)
out["symmetric"] = sym

# ---------------------------------------------------------------- minors (exact, two methods)
def det_bareiss(M):
    n = len(M)
    A = [row[:] for row in M]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = None
            for i in range(k + 1, n):
                if A[i][k] != 0:
                    sw = i; break
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]

def det_fraction(M):
    n = len(M)
    A = [[Fr(x) for x in row] for row in M]
    d = Fr(1)
    for k in range(n):
        piv = None
        for i in range(k, n):
            if A[i][k] != 0:
                piv = i; break
        if piv is None:
            return Fr(0)
        if piv != k:
            A[k], A[piv] = A[piv], A[k]; d = -d
        d *= A[k][k]
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return d

minors = []
for k in range(1, 13):
    sub = [row[:k] for row in G[:k]]
    d1 = det_bareiss(sub)
    d2 = det_fraction(sub)
    assert d2.denominator == 1 and d1 == d2.numerator, (k, d1, d2)
    minors.append(d1)
print("leading principal minors:")
for k, d in enumerate(minors, 1):
    print(f"  Delta_{k} = {d}")
allpos = all(d > 0 for d in minors)
print("all leading minors positive:", allpos)
out["minors"] = [str(d) for d in minors]
out["all_minors_positive"] = allpos

floors = []
prev = 1
for d in minors:
    floors.append((10 * d) // prev)
    prev = d
printed = [51270, 16698, 17179, 269, 8, 10, 4199, 5263, 242, 252, 5, 11]
print("floor(10*Delta_k/Delta_{k-1}) =", floors)
print("matches printed values:", floors == printed)
out["floors"] = floors
out["floors_match"] = floors == printed

# independent PD check: exact LDL^T with Fractions (pivots = Delta_k/Delta_{k-1})
A = [[Fr(x) for x in row] for row in G]
piv = []
for k in range(12):
    piv.append(A[k][k])
    for i in range(k + 1, 12):
        f = A[i][k] / A[k][k]
        for j in range(k, 12):
            A[i][j] -= f * A[k][j]
print("LDL pivots (float):", [float(p) for p in piv])
assert all(p > 0 for p in piv)
ev = np.linalg.eigvalsh(np.array(G, dtype=float))
print("float eigenvalues of G: min %.6f max %.3f" % (ev[0], ev[-1]))
out["min_eig_float"] = float(ev[0])

tr = sum(G[i][i] for i in range(12))
print("Tr G =", tr, " Tr/600 =", Fr(tr, 600), " 289/10-7/20 =", Fr(289, 10) - Fr(7, 20),
      " equal:", Fr(tr, 600) == Fr(289, 10) - Fr(7, 20))
out["trace"] = tr
out["trace_ok"] = Fr(tr, 600) == Fr(289, 10) - Fr(7, 20)

# ---------------------------------------------------------------- free algebra
# A monomial is a pair (wa, wb) of reduced words (tuples) in the alphabets
# {A0,A1,A2} and {B0,B1}.  Relations: X^2 = 1, [A_x, B_y] = 0.  NO relation
# between different A's or between different B's.

def red(word):
    st = []
    for s in word:
        if st and st[-1] == s:
            st.pop()
        else:
            st.append(s)
    return tuple(st)

class Poly:
    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v != 0}
    @staticmethod
    def mono(wa=(), wb=(), c=1):
        return Poly({(red(wa), red(wb)): Fr(c)})
    def __add__(self, o):
        d = dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return Poly(d)
    def __sub__(self, o):
        return self + o * Fr(-1)
    def __mul__(self, o):
        if isinstance(o, (int, Fr)):
            return Poly({k: v * o for k, v in self.d.items()})
        d = {}
        for (wa1, wb1), v1 in self.d.items():
            for (wa2, wb2), v2 in o.d.items():
                k = (red(wa1 + wa2), red(wb1 + wb2))
                d[k] = d.get(k, 0) + v1 * v2
        return Poly(d)
    __rmul__ = __mul__
    def dagger(self):
        return Poly({(tuple(reversed(wa)), tuple(reversed(wb))): v for (wa, wb), v in self.d.items()})
    def iszero(self):
        return len(self.d) == 0
    def subs(self, mapA, mapB):
        """substitute generators: mapA[x] = (sign, newindex)"""
        d = {}
        for (wa, wb), v in self.d.items():
            s = 1
            na = []
            for x in wa:
                sg, nx = mapA[x]; s *= sg; na.append(nx)
            nb = []
            for y in wb:
                sg, ny = mapB[y]; s *= sg; nb.append(ny)
            k = (red(tuple(na)), red(tuple(nb)))
            d[k] = d.get(k, 0) + s * v
        return Poly(d)
    def __repr__(self):
        def nm(k):
            wa, wb = k
            s = "".join(f"A{x}" for x in wa) + "".join(f"B{y}" for y in wb)
            return s or "1"
        return " + ".join(f"({v})*{nm(k)}" for k, v in sorted(self.d.items()))

I = Poly.mono()
A = [Poly.mono(wa=(x,)) for x in range(3)]
B = [Poly.mono(wb=(y,)) for y in range(2)]
W = [I, A[0], A[1], A[2], B[0], B[1], A[0] * B[0], A[0] * B[1], A[1] * B[0], A[1] * B[1], A[2] * B[0], A[2] * B[1]]

# sanity checks of the algebra implementation
assert (A[0] * A[0] - I).iszero() and (B[1] * B[1] - I).iszero()
assert (A[0] * B[1] - B[1] * A[0]).iszero()
assert not (A[0] * A[1] - A[1] * A[0]).iszero()
assert not (B[0] * B[1] - B[1] * B[0]).iszero()

# Bell operator on support {0,2} as printed in the paper
S = A[0] * (B[0] + B[1]) + A[1] * (B[0] - B[1])
B02_paper = (S * 10 + I * Fr(7, 20) + B[0] * Fr(3, 20) + B[1] * Fr(1, 5) - A[2] * Fr(1, 20)
             + A[2] * B[0] * Fr(3, 20) - A[2] * B[1] * Fr(1, 5))

# derive B02 from the functional itself (eq:bell-functional)
# alpha = (1,-1,1) on Alice labels, beta = (1,-1) on Bob labels.
# x=0,1: signed observable A_x = M^x_0 - M^x_1 + M^x_2 ; Bob N^y_0=(1+B_y)/2, N^y_1=(1-B_y)/2
half = Fr(1, 2)
N = [[(I + B[y]) * half, (I - B[y]) * half] for y in range(2)]
def bell_operator(M2):
    """M2 = [M_0, M_1, M_2] effects of Alice's third input as polynomials."""
    op = S * 10
    op = op + M2[0] * N[0][0] * Fr(3, 5) + M2[1] * N[0][1] * Fr(3, 5) + M2[2] * N[1][0] * Fr(4, 5)
    return op
ZERO = Poly()
B02_derived = bell_operator([(I + A[2]) * half, ZERO, (I - A[2]) * half])
print("\nderived B_02 from functional:", B02_derived)
ok_exp = (B02_derived - B02_paper).iszero()
print("paper's expansion of B_02 confirmed:", ok_exp)
out["B02_expansion_ok"] = ok_exp

# also confirm that the CHSH part 10*(E00+E01+E10-E11) written with effects equals 10*S
# when M^x = {(1+A_x)/2 on label 0 or 2, (1-A_x)/2 on label 1}
chk = Poly()
alpha = [1, -1, 1]; beta = [1, -1]
for x in range(2):
    Mx = [(I + A[x]) * half, (I - A[x]) * half, ZERO]  # label 0: +, label 1: -, label 2 unused
    for y in range(2):
        sgn = 1 if (x, y) != (1, 1) else -1
        for a in range(3):
            for b in range(2):
                chk = chk + Mx[a] * N[y][b] * (alpha[a] * beta[b] * sgn * 10)
print("CHSH term from effects equals 10*S:", (chk - S * 10).iszero())
out["chsh_term_ok"] = (chk - S * 10).iszero()

# ---- the SOS identity
rhs = Poly()
for i in range(12):
    for j in range(12):
        if G[i][j]:
            rhs = rhs + W[i].dagger() * W[j] * Fr(G[i][j], 600)
lhs = I * Fr(289, 10) - B02_paper
diff = lhs - rhs
print("\nSOS identity (289/10) - B_02 == (1/600) sum G_ij W_i^dag W_j  [exact, free algebra]:", diff.iszero())
if not diff.iszero():
    print("  residual:", diff)
out["sos_identity_exact"] = diff.iszero()
print("  number of distinct normal-form words appearing in sum before cancellation:",
      len({(red(tuple(reversed(wa1)) + wa2), red(tuple(reversed(wb1)) + wb2))
           for i in range(12) for j in range(12)
           for (wa1, wb1) in W[i].d for (wa2, wb2) in W[j].d}))
print("  words surviving in RHS:", sorted(rhs.d.keys()))

# sensitivity test: perturbing any single symmetric pair of G by +-1 must break the identity
broken = 0; total = 0
for i in range(12):
    for j in range(i, 12):
        total += 1
        d = W[i].dagger() * W[j] + (W[j].dagger() * W[i] if i != j else Poly())
        if not d.iszero():
            broken += 1
print(f"  sensitivity: {broken}/{total} single-entry perturbations of G change the polynomial")
out["sensitivity"] = [broken, total]

# ---- support {1,2}: substitution rule
B12_derived = bell_operator([ZERO, (I + A[2]) * half, (I - A[2]) * half])
mapA = {0: (-1, 1), 1: (-1, 0), 2: (1, 2)}
mapB = {0: (-1, 0), 1: (1, 1)}
B12_sub = B02_paper.subs(mapA, mapB)
S_sub = S.subs(mapA, mapB)
print("\nsupport {1,2}: derived operator:", B12_derived)
print("substitution (A0,A1,A2,B0,B1)->(-A1,-A0,A2,-B0,B1) preserves S:", (S_sub - S).iszero())
print("substitution maps B_02 to the derived B_12:", (B12_sub - B12_derived).iszero())
out["subst_preserves_S"] = (S_sub - S).iszero()
out["subst_gives_B12"] = (B12_sub - B12_derived).iszero()
# the substituted generators are still involutions commuting across parties, so the SOS
# identity transports: check directly as well
rhs12 = rhs.subs(mapA, mapB)
print("transported SOS identity for {1,2}: (289/10)-B_12 == substituted SOS:",
      (I * Fr(289, 10) - B12_derived - rhs12).iszero())
out["sos_identity_12"] = (I * Fr(289, 10) - B12_derived - rhs12).iszero()

# deterministic third measurement are special cases A2 = +-1 (label 0, label 2, label 1)
# label 0 only: M0 = 1  <=> A2 = +1 in {0,2} support
B_det0 = bell_operator([I, ZERO, ZERO]); B_det2 = bell_operator([ZERO, ZERO, I]); B_det1 = bell_operator([ZERO, I, ZERO])
def subsA2(p, sign):
    d = {}
    for (wa, wb), v in p.d.items():
        s = 1; na = []
        for x in wa:
            if x == 2: s *= sign
            else: na.append(x)
        k = (red(tuple(na)), wb); d[k] = d.get(k, 0) + s * v
    return Poly(d)
print("deterministic label 0 == B_02|A2=+1:", (subsA2(B02_paper, 1) - B_det0).iszero(),
      "; label 2 == B_02|A2=-1:", (subsA2(B02_paper, -1) - B_det2).iszero(),
      "; label 1 == B_12|A2=+1:", (subsA2(B12_derived, 1) - B_det1).iszero())
out["deterministic_cases_ok"] = bool((subsA2(B02_paper, 1) - B_det0).iszero() and (subsA2(B02_paper, -1) - B_det2).iszero()
                                     and (subsA2(B12_derived, 1) - B_det1).iszero())

# ---- support {0,1}
# aux operator = 3/5 (M0 N^0_0 + M1 N^0_1), M0 + M1 = 1 -> <= 3/5 ; and 20 sqrt2 + 3/5 < 289/10 ?
# exact: 20 sqrt2 < 289/10 - 3/5 = 283/10  <=>  800 < (283/10)^2 = 80089/100
lhs2 = Fr(800); rhs2 = Fr(283, 10) ** 2
print("\nsupport {0,1}: 20*sqrt2 + 3/5 < 289/10  <=>  800 < 80089/100 :", lhs2 < rhs2, f"({float(rhs2)})")
out["support01_bound_ok"] = lhs2 < rhs2
B01 = bell_operator([(I + A[2]) * half, (I - A[2]) * half, ZERO])
# aux part: 3/5*( (1+A2)/2 (1+B0)/2 + (1-A2)/2 (1-B0)/2 ) = 3/10 (1 + A2 B0)  <= 3/5
aux01 = B01 - S * 10
print("aux operator on support {0,1}:", aux01, " (= 3/10 (1 + A2 B0) <= 3/5)")
out["aux01"] = repr(aux01)

# ---------------------------------------------------------------- numerical check
rng = np.random.default_rng(20261122)
def rand_involution(d, rng, allow_trivial=True):
    # random Hermitian involution: U diag(+-1) U^dag with random signature
    X = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    Q, _ = np.linalg.qr(X)
    lo = 0 if allow_trivial else 1
    k = rng.integers(lo, d + 1 - lo) if d > 1 else rng.integers(0, 2)
    s = np.array([1] * k + [-1] * (d - k))
    return (Q * s) @ Q.conj().T

Gf = np.array(G, dtype=float)
maxres = 0.0; minlam = np.inf; cnt = 0
for d in (2, 3, 4):
    for trial in range(400):
        Am = [np.kron(rand_involution(d, rng), np.eye(d)) for _ in range(3)]
        Bm = [np.kron(np.eye(d), rand_involution(d, rng)) for _ in range(2)]
        Id = np.eye(d * d)
        Wm = [Id, Am[0], Am[1], Am[2], Bm[0], Bm[1], Am[0] @ Bm[0], Am[0] @ Bm[1], Am[1] @ Bm[0], Am[1] @ Bm[1],
              Am[2] @ Bm[0], Am[2] @ Bm[1]]
        Sm = Am[0] @ (Bm[0] + Bm[1]) + Am[1] @ (Bm[0] - Bm[1])
        B02m = 10 * Sm + 0.35 * Id + 0.15 * Bm[0] + 0.2 * Bm[1] - 0.05 * Am[2] + 0.15 * Am[2] @ Bm[0] - 0.2 * Am[2] @ Bm[1]
        R = sum(Gf[i, j] * Wm[i].conj().T @ Wm[j] for i in range(12) for j in range(12)) / 600
        L = 28.9 * Id - B02m
        maxres = max(maxres, np.abs(L - R).max())
        minlam = min(minlam, np.linalg.eigvalsh((L + L.conj().T) / 2)[0])
        cnt += 1
print(f"\nnumerical check, {cnt} random involution tuples in local dims 2,3,4:")
print(f"  max |LHS-RHS| entry = {maxres:.3e};  min eigenvalue of 28.9-B_02 over samples = {minlam:.6f}")
out["numeric_max_residual"] = maxres
out["numeric_min_gap_eig_random"] = minlam

json.dump(out, open(sys.argv[2], "w"), indent=1)
print("\nALL CLAIM-3 CHECKS PASS:", all([out["symmetric"], out["all_minors_positive"], out["floors_match"], out["trace_ok"],
      out["B02_expansion_ok"], out["sos_identity_exact"], out["subst_preserves_S"], out["subst_gives_B12"],
      out["sos_identity_12"], out["support01_bound_ok"], out["deterministic_cases_ok"], maxres < 1e-9]))
