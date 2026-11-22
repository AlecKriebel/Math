#!/usr/bin/env python3
"""Claim 2: exact Born-rule recomputation of the two POVM strategies for the 3x2 functional."""
import json, sys
import sympy as sp
from sympy import Rational as R, sqrt, Matrix, eye, zeros, simplify, nsimplify, radsimp
from fractions import Fraction as Fr

out = {}
X = Matrix([[0, 1], [1, 0]]); Z = Matrix([[1, 0], [0, -1]]); I2 = eye(2)
kron = sp.kronecker_product

# ---------------- functional as a coefficient table c[(a,b,x,y)]
alpha = [1, -1, 1]; beta = [1, -1]
c = {}
for x in range(2):
    for y in range(2):
        sgn = -1 if (x, y) == (1, 1) else 1
        for a in range(3):
            for b in range(2):
                c[(a, b, x, y)] = c.get((a, b, x, y), 0) + 10 * sgn * alpha[a] * beta[b]
c[(0, 0, 2, 0)] = c.get((0, 0, 2, 0), 0) + R(3, 5)
c[(1, 1, 2, 0)] = c.get((1, 1, 2, 0), 0) + R(3, 5)
c[(2, 0, 2, 1)] = c.get((2, 0, 2, 1), 0) + R(4, 5)

def is_psd_2x2(M):
    """exact PSD test for a Hermitian 2x2 sympy matrix: trace >= 0 and det >= 0"""
    M = sp.Matrix(M)
    assert sp.simplify(M - M.H) == zeros(2, 2), "not Hermitian"
    tr = sp.simplify(M.trace()); dt = sp.simplify(M.det())
    return bool(tr >= 0) and bool(sp.simplify(dt) >= 0), tr, dt

def bell_value(psi, MA, NB):
    """psi: 4x1 column, MA[x][a], NB[y][b] 2x2 matrices. Exact Born rule."""
    val = 0
    probs = {}
    for (a, b, x, y), coef in c.items():
        p = (psi.H * kron(MA[x][a], NB[y][b]) * psi)[0, 0]
        probs[(a, b, x, y)] = p
        val += coef * p
    return sp.simplify(val), probs

def check_povm(effects, name):
    ok = True
    s = zeros(2, 2)
    for a, M in enumerate(effects):
        psd, tr, dt = is_psd_2x2(M)
        ok = ok and psd
        s += M
    norm = sp.simplify(s - I2) == zeros(2, 2)
    print(f"  {name}: all effects PSD: {ok}; sums to identity: {norm}")
    return ok and norm

def proj_effects(Aobs):
    """binary observable -> effects on labels (0: +, 1: -, 2: zero)"""
    return [(I2 + Aobs) / 2, (I2 - Aobs) / 2, zeros(2, 2)]

# ================= simple strategy
print("== simple strategy (main text) ==")
phi = Matrix([1, 0, 0, 1]) / sqrt(2)
B0, B1 = Z, X
A0 = (Z + X) / sqrt(2); A1 = (Z - X) / sqrt(2)
M2 = [(17 * I2 - 8 * X + 15 * Z) / 50, (17 * I2 - 8 * X - 15 * Z) / 50, (16 * I2 + 16 * X) / 50]
MA = [proj_effects(A0), proj_effects(A1), M2]
NB = [[(I2 + B0) / 2, (I2 - B0) / 2], [(I2 + B1) / 2, (I2 - B1) / 2]]
ok = True
for x in range(3):
    ok &= check_povm(MA[x], f"Alice x={x}")
for y in range(2):
    ok &= check_povm(NB[y], f"Bob y={y}")
print("  A0^2=I:", sp.simplify(A0 * A0 - I2) == zeros(2, 2), " A1^2=I:", sp.simplify(A1 * A1 - I2) == zeros(2, 2))
# rank-one factorizations as printed
f0 = Matrix([4, -1]) * Matrix([[4, -1]]) / 25
f1 = Matrix([1, -4]) * Matrix([[1, -4]]) / 25
f2 = R(8, 25) * Matrix([1, 1]) * Matrix([[1, 1]])
print("  printed rank-one factorizations match M_0,M_1,M_2:", [sp.simplify(f0 - M2[0]) == zeros(2, 2),
      sp.simplify(f1 - M2[1]) == zeros(2, 2), sp.simplify(f2 - M2[2]) == zeros(2, 2)])
print("  nonzero eigenvalues (traces of rank-one effects):", [M.trace() for M in M2], " -> not a PVM")
print("  state normalized:", sp.simplify((phi.H * phi)[0, 0]) == 1)
val0, probs = bell_value(phi, MA, NB)
L0 = 20 * sqrt(2) + R(16, 25)
print("  p(0,0|2,0), p(1,1|2,0), p(2,0|2,1) =", probs[(0, 0, 2, 0)], probs[(1, 1, 2, 0)], probs[(2, 0, 2, 1)])
print("  Bell value =", val0, "  equals 20*sqrt2+16/25:", sp.simplify(val0 - L0) == 0, f" (~{float(val0):.10f})")
out["simple_value_ok"] = bool(sp.simplify(val0 - L0) == 0) and bool(ok)
# dual certificate for discrimination problem
W0 = R(3, 20) * (I2 + Z); W1 = R(3, 20) * (I2 - Z); W2 = R(1, 5) * (I2 + X)
Gam = R(8, 25) * I2 + R(2, 25) * X
dual_ok = True
for Wk, Mk in zip([W0, W1, W2], M2):
    psd, tr, dt = is_psd_2x2(Gam - Wk)
    cs = sp.simplify((Gam - Wk) * Mk) == zeros(2, 2)
    dual_ok &= psd and cs
print("  dual operator Gamma >= W_i and (Gamma-W_i)M_i=0:", dual_ok, "; Tr Gamma =", Gam.trace())
out["simple_dual_ok"] = bool(dual_ok)

# ================= strengthened strategy
print("== strengthened strategy (Appendix B) ==")
q = sqrt(7813); eta = 1 / q
s = sqrt(1 - eta ** 2)
print("  s == 6*sqrt(217)/q:", sp.simplify(s - 6 * sqrt(217) / q) == 0, "; 36*217+7813 == 125^2:", 36 * 217 + 7813 == 125 ** 2)
psi = Matrix([sqrt((1 + eta) / 2), 0, 0, sqrt((1 - eta) / 2)])
B0, B1 = X, Z
A0 = (6 * sqrt(217) * X + q * Z) / 125
A1 = (6 * sqrt(217) * X - q * Z) / 125
k = R(3, 5) * sqrt((q - 1) / (q + 1))
M2 = [Matrix([[k ** 2, k], [k, 1]]) / 2, Matrix([[k ** 2, -k], [-k, 1]]) / 2, Matrix([[1 - k ** 2, 0], [0, 0]])]
MA = [proj_effects(A0), proj_effects(A1), M2]
NB = [[(I2 + B0) / 2, (I2 - B0) / 2], [(I2 + B1) / 2, (I2 - B1) / 2]]
ok = True
for x in range(3):
    ok &= check_povm(MA[x], f"Alice x={x}")
for y in range(2):
    ok &= check_povm(NB[y], f"Bob y={y}")
print("  A0^2=I:", sp.simplify(A0 * A0 - I2) == zeros(2, 2), " A1^2=I:", sp.simplify(A1 * A1 - I2) == zeros(2, 2))
print("  k^2 =", sp.nsimplify(sp.simplify(k ** 2)), "~", float(k ** 2), " (<1 so M_2>=0)")
print("  dets of M_0,M_1,M_2 (rank one):", [sp.simplify(M.det()) for M in M2])
print("  state normalized:", sp.simplify((psi.H * psi)[0, 0]) == 1)
val1, probs = bell_value(psi, MA, NB)
L1 = (16 + 8 * q) / 25
d1 = sp.simplify(sp.radsimp(sp.simplify(val1 - L1)))
num_d1 = sp.N(val1 - L1, 60)
print("  Bell value ~", sp.N(val1, 30), "; L1 ~", sp.N(L1, 30))
print("  exact difference simplifies to:", d1, " (60-digit numeric:", num_d1, ")")
# CHSH part and T part separately
Sval = 0; Tval = 0
for (a, b, x, y), coef in c.items():
    if x < 2: Sval += coef * probs[(a, b, x, y)]
    else: Tval += coef * probs[(a, b, x, y)]
print("  10*S == 2500/q:", sp.simplify(Sval - 2500 / q) == 0, "; T == (16+4*eta)/25:", sp.simplify(sp.radsimp(sp.simplify(Tval - (16 + 4 * eta) / 25))) == 0,
      " numeric T diff:", sp.N(Tval - (16 + 4 * eta) / 25, 50))
# robust exact check of val1 == L1 via minimal polynomial / algebraic equality
eq = sp.simplify(val1 - L1)
is_zero = eq == 0 or sp.minimal_polynomial(eq, sp.Symbol('t')) == sp.Symbol('t')
print("  exact equality val == (16+8*sqrt(7813))/25:", bool(is_zero))
out["strengthened_value_ok"] = bool(is_zero) and bool(ok)

# dual-slack statements of Appendix B: K_j = steered score operators (weights 3/5,3/5,4/5)
# K_j defined by T = sum_j Tr(K_j M_j):  K_j = coef * Tr_B[(1 (x) N) |psi><psi|]^T-convention; compute directly
rho = psi * psi.H
def steer(Nop, coef):
    # K with Tr(K M) = coef * <psi| M (x) Nop |psi>
    K = zeros(2, 2)
    for i in range(2):
        for j in range(2):
            E = zeros(2, 2); E[i, j] = 1  # M = |i><j|
            K[j, i] = coef * (psi.H * kron(E, Nop) * psi)[0, 0]
    return K
K = [steer(NB[0][0], R(3, 5)), steer(NB[0][1], R(3, 5)), steer(NB[1][0], R(4, 5))]
Gam = sp.diag(R(2, 5) * (1 + eta), R(6, 25) * (1 - eta))
vm = Matrix([1, -k]); vp = Matrix([1, k])
slk = [(1 + eta) / 4 * vm * vm.T, (1 + eta) / 4 * vp * vp.T, R(6, 25) * (1 - eta) * Matrix([[0, 0], [0, 1]])]
def exact_zero(e):
    e = sp.simplify(e)
    if e == 0:
        return True
    t = sp.Symbol('t')
    try:
        return sp.minimal_polynomial(e, t) == t
    except Exception:
        return False
sl_ok = all(exact_zero(e) for j in range(3) for e in (Gam - K[j] - slk[j]))
cs_ok = all(exact_zero(e) for j in range(3) for e in (slk[j] * M2[j]))
print("  K_j (float):", [[[float(sp.N(e)) for e in K[j].row(r)] for r in range(2)] for j in range(3)])
print("  dual slacks Gamma-K_j equal printed rank-one forms:", sl_ok, "; slack*M_j = 0:", cs_ok,
      "; Tr Gamma - (16+4 eta)/25 =", sp.simplify(Gam.trace() - (16 + 4 * eta) / 25))
out["strengthened_dual_ok"] = bool(sl_ok and cs_ok)

# ================= numeric comparisons done exactly
print("== exact comparisons ==")
# (16 sqrt(7813) - 1413)/50 > 0.02517  <=> 16 sqrt(7813) > 1413 + 50*0.02517 = 1414.2585
thr = Fr(1413) + 50 * Fr(2517, 100000)
lhs_sq = Fr(256 * 7813); rhs_sq = thr * thr
print("  (16*sqrt(7813)-1413)/50 > 0.02517  <=> 256*7813 > (1414.2585)^2:", lhs_sq > rhs_sq,
      f" [{lhs_sq} vs {float(rhs_sq):.6f}]  value ~ {float((16*sp.sqrt(7813)-1413)/50):.9f}")
out["gap_gt_0.02517"] = bool(lhs_sq > rhs_sq)
print("  L1 - 289/10 == (16 sqrt(7813)-1413)/50:", sp.simplify(L1 - R(289, 10) - (16 * q - 1413) / 50) == 0)
# L0 > 289/10 ?  20 sqrt2 > 28.9 - 0.64 = 28.26  <=> 800 > 28.26^2 = 798.6276
print("  L0 > 289/10  <=> 800 >", float(Fr(2826, 100) ** 2), ":", Fr(800) > Fr(2826, 100) ** 2, f"  L0-28.9 ~ {float(L0)-28.9:.9f}")
out["L0_gt_289_10"] = bool(Fr(800) > Fr(2826, 100) ** 2)
U = 20 * sqrt(2) + R(3, 5) + (4 + 3 * sqrt(2)) / 250
print("  U ~", float(U), "; L0-U == 3(2-sqrt2)/250:", sp.simplify(L0 - U - 3 * (2 - sqrt(2)) / 250) == 0, "; L1 > U:", bool(L1 > U), "; 289/10 < U:", bool(R(289, 10) < U))
print("  (6+80 sqrt7813)^2 - 2*5003^2 == -56782+960 sqrt7813:", sp.expand((6 + 80 * q) ** 2 - 2 * 5003 ** 2 - (-56782 + 960 * q)) == 0,
      "; 960^2*7813-56782^2 =", 960 ** 2 * 7813 - 56782 ** 2)
out["L0"] = float(L0); out["L1"] = float(L1); out["U"] = float(U); out["gap_L1"] = float(L1) - 28.9
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(out)
