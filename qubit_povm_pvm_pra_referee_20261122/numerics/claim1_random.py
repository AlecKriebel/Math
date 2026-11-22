#!/usr/bin/env python3
"""Claim 1: random functional families in a given two-input scenario.
usage: claim1_random.py a0,a1 b0,b1 F_per_family R seed out.json [joint_n]
"""
import sys, json, time
import numpy as np
import bell_lib as bl
import claim1_lib as cl

outsA = tuple(int(v) for v in sys.argv[1].split(','))
outsB = tuple(int(v) for v in sys.argv[2].split(','))
Ff = int(sys.argv[3]); R = int(sys.argv[4]); seed = int(sys.argv[5]); outp = sys.argv[6]
joint_n = int(sys.argv[7]) if len(sys.argv) > 7 else 0
rng = np.random.default_rng(seed)
label = f"({outsA[0]},{outsA[1]};{outsB[0]},{outsB[1]})"
t0 = time.time()
allres = {}
print(f"=== scenario {label}  F/family={Ff} R={R} seed={seed} ===", flush=True)
tot_max = -np.inf; nF = 0
for fam, gen in cl.FAMILIES.items():
    cs = gen(rng, Ff, outsA, outsB)
    if cs[0][0].shape[0] == 0:
        print(f"[{label} {fam}] no functionals generated (filter found none)", flush=True); continue
    res = cl.evaluate(cs, outsA, outsB, rng, R=R, Rp=max(10, R // 2), joint_n=joint_n)
    print(cl.summarize(res, f"{label} {fam}"), flush=True)
    allres[fam] = cl.to_jsonable(res)
    tot_max = max(tot_max, res['gap'].max()); nF += res['F']
    json.dump(dict(scenario=label, seed=seed, results=allres), open(outp, 'w'))
print(f"=== {label}: {nF} functionals, overall max POVM-PVM gap {tot_max:+.3e}, wall {time.time()-t0:.0f}s ===", flush=True)
