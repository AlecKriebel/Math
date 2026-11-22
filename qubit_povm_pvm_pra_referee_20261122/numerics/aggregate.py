#!/usr/bin/env python3
"""Aggregate all Claim-1 result JSON files into a summary table."""
import json, glob, sys
import numpy as np

rows = []
tot = dict(F=0, nl=0, maxgap=-np.inf, flagged=0, joint=0, runs=0, reach=0)

def one(label, fam, r):
    pvm2 = np.array(r['pvm2']); pvmss = np.array(r['pvmss']); povmss = np.array(r['povmss']); seed = np.array(r['povmseed'])
    joint = np.array([v if v is not None else -np.inf for v in r['joint']], dtype=float)
    loc = np.array(r['local']); gap = np.array(r['gap']); se = np.array(r['seed_exact'])
    pb = np.maximum(pvm2, pvmss)
    nl = int((pb > loc + 1e-7).sum())
    jm = np.isfinite(joint)
    reach = int((povmss >= pb - 1e-6 * (1 + np.abs(pb))).sum())
    rel = gap / (1 + np.abs(pb))
    rows.append((label, fam, r['F'], nl, gap.max(), rel.max(), gap.min(), reach, float(np.max(pvmss - pvm2)), float(np.min(se - pvm2)),
                 int(jm.sum()), (float(np.max(joint[jm] - pb[jm])) if jm.any() else float('nan')),
                 (int((joint[jm] >= pb[jm] - 1e-6 * (1 + np.abs(pb[jm]))).sum()) if jm.any() else 0), len(r['flagged'])))
    tot['F'] += r['F']; tot['nl'] += nl; tot['maxgap'] = max(tot['maxgap'], gap.max()); tot['flagged'] += len(r['flagged'])
    tot['joint'] += int(jm.sum()); tot['runs'] += r['F'] * (r['R'] + r['Rs']); tot['reach'] += reach

for fn in sorted(glob.glob('claim1_random_*.json')):
    d = json.load(open(fn))
    for fam, r in d['results'].items():
        one(d['scenario'], fam, r)
try:
    d = json.load(open('claim1_structured.json'))
    for lab, r in d.items():
        one('structured', lab[:60], r)
except FileNotFoundError:
    pass

print(f"{'scenario':12s} {'family':62s} {'F':>4s} {'>loc':>4s} {'max gap':>10s} {'max rel':>9s} {'min gap':>10s} {'ss@opt':>6s} {'PVMss-2ang':>10s} {'seed-PVM':>10s} {'nJ':>3s} {'J-PVM max':>10s} {'J@opt':>5s} {'flag':>4s}")
for r in rows:
    print(f"{r[0]:12s} {r[1]:62s} {r[2]:4d} {r[3]:4d} {r[4]:+10.2e} {r[5]:+9.1e} {r[6]:+10.2e} {r[7]:6d} {r[8]:+10.2e} {r[9]:+10.2e} {r[10]:3d} {r[11]:+10.2e} {r[12]:5d} {r[13]:4d}")
print()
# per scenario totals
sc = {}
for r in rows:
    s = sc.setdefault(r[0], dict(F=0, nl=0, mg=-np.inf, reach=0, nj=0, jo=0))
    s['F'] += r[2]; s['nl'] += r[3]; s['mg'] = max(s['mg'], r[4]); s['reach'] += r[7]; s['nj'] += r[10]; s['jo'] += r[12]
for k, s in sc.items():
    print(f"  {k:12s}: {s['F']:5d} functionals ({s['nl']} with qubit value > local bound); max POVM-PVM gap {s['mg']:+.2e}; "
          f"random-restart POVM see-saw reached the PVM bound for {s['reach']}/{s['F']}; joint optimiser reached it for {s['jo']}/{s['nj']}")
print(f"\nTOTAL: {tot['F']} functionals, {tot['nl']} nonlocal, {tot['runs']} POVM see-saw runs, {tot['joint']} functionals with joint optimisation, "
      f"max gap {tot['maxgap']:+.3e}, flagged (gap > 1e-7 rel) {tot['flagged']}")
