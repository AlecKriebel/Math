#!/usr/bin/env python3
"""Literal-data generator. Type checking and the equality theorem remain Lean's job."""
import argparse,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--check-only',action='store_true');args=p.parse_args()
terms=json.loads((root/'data/lie31_brackets.json').read_text())['terms']
assert all(0<=i<j<31 and 0<=k<31 and c!=0 for i,j,k,c in terms)
out=['/- UNCOMPILED literal data generated from the byte-frozen integer table. -/',
     'import Mathlib.Data.Int.Basic','','namespace Kourovka','',
     'def exportedTerms : List (Nat × Nat × Nat × Int) :=','  [']
for q,(i,j,k,c) in enumerate(terms):
    out.append(f'    ({i}, {j}, {k}, {c})'+(',' if q+1<len(terms) else ''))
out+=['  ]','','end Kourovka','']
text='\n'.join(out); dest=root/'Kourovka/ExportedData.lean'
if args.check_only:
    assert dest.read_text()==text, 'Lean literal differs from deterministic export'
else: dest.write_text(text)
print('Literal export matches frozen data; this is not Lean proof checking.')
