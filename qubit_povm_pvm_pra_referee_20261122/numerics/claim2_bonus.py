#!/usr/bin/env python3
"""Bonus random tests of intermediate inequalities of the 'alternative analytic projective bound' (not formalised in Lean):
   S <= 2sqrt2 - eta^2/sqrt2,  S <= 2sqrt2 - u^2/(2sqrt2),  T_PVM <= 3/5 + (2/5)(eta+u),  and Bell_PVM <= U.
Also the ideal-point discrimination values (PVM 3/5, POVM 16/25)."""
import numpy as np, bell_lib as bl
rng = np.random.default_rng(99)
N = 400000
eta = rng.uniform(0, 1, N); eta[: N // 4] = rng.uniform(0, 0.05, N // 4)
def rd(n):
    v = rng.normal(size=(n, 3)); return v / np.linalg.norm(v, axis=1, keepdims=True)
b0 = rd(N); b1 = rd(N)
# also near-orthogonal / near-parallel pairs
t = rng.uniform(0, 0.1, N // 4); b1[: N // 4] = np.cos(np.pi / 2 + t)[:, None] * b0[: N // 4] + np.sin(np.pi / 2 + t)[:, None] * np.cross(b0[: N // 4], rd(N // 4))
b1 /= np.linalg.norm(b1, axis=1, keepdims=True)
u = np.abs((b0 * b1).sum(1))
psi = np.zeros((N, 2, 2), dtype=complex); psi[:, 0, 0] = np.sqrt((1 + eta) / 2); psi[:, 1, 1] = np.sqrt((1 - eta) / 2)
def proj(n):  # (N,3)->(N,2,2,2) effects +,-
    w = np.full((n.shape[0], 2), 0.5); v = np.stack([0.5 * n, -0.5 * n], 1); return bl.from_bloch(w, v)
MB = [proj(b0), proj(b1)]
# CHSH: optimal Alice observables for given state and Bob: S = sum over x of |kappa-type vector|
cc = [[np.broadcast_to(np.array([[1., -1], [-1, 1]]), (N, 2, 2)), np.broadcast_to(np.array([[1., -1], [-1, 1]]), (N, 2, 2))],
      [np.broadcast_to(np.array([[1., -1], [-1, 1]]), (N, 2, 2)), np.broadcast_to(-np.array([[1., -1], [-1, 1]]), (N, 2, 2))]]
S = 0
for x in range(2):
    k, kap = bl.to_bloch(bl.alice_scores(cc, MB, psi, x))
    w, v, val = bl.solve_pvm_batch(k, kap)   # best labelled PVM (includes deterministic)
    S = S + val
d1 = S - (2 * np.sqrt(2) - eta ** 2 / np.sqrt(2)); d2 = S - (2 * np.sqrt(2) - u ** 2 / (2 * np.sqrt(2)))
print(f"N={N} random (eta, b0, b1): max[S - (2sqrt2 - eta^2/sqrt2)] = {d1.max():+.3e}; max[S - (2sqrt2 - u^2/(2sqrt2))] = {d2.max():+.3e}  (both must be <= 0)")
# T term: Alice x=2 best PVM
cT = [[np.zeros((N, 3, 2)), np.zeros((N, 3, 2))]]
cT[0][0][:, 0, 0] = 0.6; cT[0][0][:, 1, 1] = 0.6; cT[0][1][:, 2, 0] = 0.8
k, kap = bl.to_bloch(bl.alice_scores(cT, MB, psi, 0))
w, v, Tpvm = bl.solve_pvm_batch(k, kap)
w2, v2, Tpovm, found = bl.solve_povm_batch(k, kap)
d3 = Tpvm - (0.6 + 0.4 * (eta + u))
print(f"   max[T_PVM - (3/5 + 2(eta+u)/5)] = {d3.max():+.3e} (must be <= 0); min slack at small eta+u: {(-d3)[(eta+u)<0.05].min() if ((eta+u)<0.05).any() else float('nan'):.3e}")
delta = 2 * np.sqrt(2) - S
kappa = 0.4 * (2 ** 0.25 + 2 ** 0.75)
U = 20 * np.sqrt(2) + 0.6 + (4 + 3 * np.sqrt(2)) / 250
tot = 10 * S + Tpvm
print(f"   max[10 S + T_PVM] over samples = {tot.max():.6f} <= U = {U:.6f}: {bool(tot.max() <= U)};  max[T_PVM - (3/5 + kappa sqrt(delta))] = {(Tpvm - 0.6 - kappa*np.sqrt(np.clip(delta,0,None))).max():+.3e}")
print(f"   (for reference: max T_POVM - T_PVM over samples = {(Tpovm-Tpvm)[found].max():.5f})")
# ideal point
W = np.array([0.15 * (np.eye(2) + bl.SZ), 0.15 * (np.eye(2) - bl.SZ), 0.2 * (np.eye(2) + bl.SX)])[None]
k, kap = bl.to_bloch(W)
print("ideal-point discrimination: best PVM score", bl.solve_pvm_batch(k, kap)[2][0], "(paper 3/5); best POVM score", bl.solve_povm_batch(k, kap)[2][0], "(paper 16/25)")
