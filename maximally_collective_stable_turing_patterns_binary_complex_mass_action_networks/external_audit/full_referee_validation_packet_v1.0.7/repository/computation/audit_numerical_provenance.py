#!/usr/bin/env python3
"""Audit that all finite displayed and simulated values use the current profile."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
import sympy as sp

if not __debug__:
    raise SystemExit(
        "audit_numerical_provenance.py requires assertions; "
        "unset PYTHONOPTIMIZE and do not use python -O"
    )

ROOT=Path(__file__).resolve().parents[1]
REFINEMENT_RELATIVE_DIFFERENCE_LIMIT = 2e-8
exact=json.loads((ROOT/'data'/'current_profile_exact.json').read_text())
rows={int(r['m']):r for r in exact['rows']}
assert rows[3]['ell_dot_r']=='-7451873/924210'
assert rows[3]['ell_dot_Dr']=='-71818/462105'
assert rows[3]['eta']['exact']=='143636/7451873'

# The generated table is the sole claim-facing finite table.
table=(ROOT/'data'/'contrast_table.tex').read_text()
for m in range(3,11):
    r=rows[m]
    for field in ('eta','cubic','amplitude_coefficient'):
        val=float(sp.N(sp.sympify(r[field]['exact'].replace('sqrt','sqrt')))) if field!='amplitude_coefficient' else float(sp.N(sp.sympify(r['amplitude_squared']['exact'])**sp.Rational(1,2)))
        assert f'{val:.6g}' in table or f'{val:.7g}' in table
for stale in ('0.1054','1.306','1.311','57/56','227m-451'):
    assert stale not in table, stale

# All simulation metadata must cite and agree with the exact source.
sim=ROOT/'data'/'simulations'
for p in sim.glob('parameters_*.json'):
    z=json.loads(p.read_text()); m=int(z['config']['m']); row=rows[m]
    eta=float(sp.N(sp.sympify(row['eta']['exact'])))
    cubic=float(sp.N(sp.sympify(row['cubic']['exact'])))
    pred=math.sqrt(-eta*float(z['config']['mu'])/cubic)
    assert z['exact_source']=='data/current_profile_exact.json'
    assert abs(z['eta']-eta)<1e-14
    assert abs(z['cubic']-cubic)<1e-14
    assert abs(z['predicted_amplitude']-pred)<1e-13

# Ratios must approach one as mu decreases for each displayed dimension.
with open(ROOT/'data'/'branch_amplitudes.csv',newline='') as f:
    data=list(csv.DictReader(f))
for m in (3,5,8):
    base=sorted((x for x in data if int(x['m'])==m and int(x['modes'])==16 and x['precision']=='base'), key=lambda x:float(x['mu']), reverse=True)
    errs=[float(x['relative_error']) for x in base]
    assert all(errs[i]>errs[i+1] for i in range(len(errs)-1)), (m,errs)

with open(ROOT/'data'/'refinement_checks.csv',newline='') as f:
    refinement_differences = [
        float(z['relative_difference']) for z in csv.DictReader(f)
    ]
assert refinement_differences
max_refinement_difference = max(refinement_differences)
print(f'MAX_REFINEMENT_RELATIVE_DIFFERENCE={max_refinement_difference:.17g}')
assert max_refinement_difference < REFINEMENT_RELATIVE_DIFFERENCE_LIMIT, (
    max_refinement_difference,
    REFINEMENT_RELATIVE_DIFFERENCE_LIMIT,
)
print('NUMERICAL_PROVENANCE_PASS')
