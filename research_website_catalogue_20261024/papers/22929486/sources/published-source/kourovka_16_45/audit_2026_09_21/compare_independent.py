#!/usr/bin/env python3
"""Compare independent audit certificate against archived and fresh certificates."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
ind=json.loads((root/'audit_2026_09_21/independent_subgroups.json').read_text())
ind={frozenset(tuple(m) for m in subgroup) for subgroup in ind}
assert len(ind)==76
for name in ['data/certified/finite_certificate.json','build/certified/finite_certificate.json']:
    c=json.loads((root/name).read_text())
    matrices=[tuple(m) for m in c['matrices']]
    actual={frozenset(matrices[i] for i in s['elements']) for s in c['subgroups']}
    assert actual==ind, name
    print(f'PASS: all 76 actual matrix subgroups match {name}')
for name in ['data/certified/subgroups_cpp.txt','build/certified/subgroups_cpp.txt']:
    lines=(root/name).read_text().splitlines()
    def decode(n):
        digits=[]
        for i in range(4): n,d=divmod(n,29); digits.insert(0,d)
        assert n==0
        return tuple(digits)
    actual={frozenset(decode(int(x)) for x in line.split()) for line in lines[1:]}
    assert int(lines[0])==76 and actual==ind, name
    print(f'PASS: all 76 actual matrix subgroups match {name}')
