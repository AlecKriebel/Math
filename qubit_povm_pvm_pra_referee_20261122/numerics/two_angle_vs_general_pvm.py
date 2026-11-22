#!/usr/bin/env python3
"""Final check of the two-angle corollary's parametrisation: uncapped two-angle maximisation (provable shortlist)
versus a general PVM see-saw with arbitrary (complex, 3D) Bloch directions and free label choice.
usage: two_angle_vs_general_pvm.py seed F family a0,a1 b0,b1"""
import sys, json, numpy as np, time, bell_lib as bl, claim1_lib as cl
seed = int(sys.argv[1]); F = int(sys.argv[2]); fam = sys.argv[3]
outsA = tuple(int(v) for v in sys.argv[4].split(',')); outsB = tuple(int(v) for v in sys.argv[5].split(','))
rng = np.random.default_rng(seed)
cs = cl.FAMILIES[fam](rng, F, outsA, outsB)
F = cs[0][0].shape[0]
Rp = 150; cb = cl.rep(cs, Rp); N = F * Rp
MA = [bl.random_povm(rng, N, outsA[x], 'pvm') for x in range(2)]; MB = [bl.random_povm(rng, N, outsB[y], 'pvm') for y in range(2)]
MA, MB, val, nf, its, left = cl.seesaw_adaptive(cb, MA, MB, mode='pvm')
cv, MAs, MBs, psis = bl.certified_value(cb, MA, MB)
pvmss = cv.reshape(F, Rp).max(1)
t0 = time.time()
r2 = [bl.pvm_two_angle_v2(cl.single(cs, f), outsA, outsB, cap=10 ** 7, keep2=5000) for f in range(F)]
v2 = np.array([r['value'] for r in r2])
print(f"{outsA};{outsB} seed {seed} {fam}: F={F}, uncapped two-angle time {time.time()-t0:.0f}s; "
      f"#(general PVM see-saw > two-angle + 1e-9) = {(pvmss > v2 + 1e-9).sum()}; max(see-saw - two-angle) = {np.max(pvmss - v2):+.2e}; "
      f"#(|diff| < 1e-9) = {(np.abs(pvmss - v2) < 1e-9).sum()}; #(two-angle > see-saw + 1e-9) = {(v2 > pvmss + 1e-9).sum()} (max {np.max(v2 - pvmss):+.2e}); "
      f"max #starts {max(r['nstarts'] for r in r2)}")
