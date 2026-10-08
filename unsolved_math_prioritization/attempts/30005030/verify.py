#!/usr/bin/env python3
"""Exact arithmetic checks of the authored implication, not the cited theorem."""
from fractions import Fraction as F
import hashlib, json
from pathlib import Path


def check(H, q):
    iq = F(0) if q is None else 1/q
    A = 1-1/(2*H)
    S = 1-1/H+iq/H
    assert A-S == (F(1,2)-iq)/H
    alpha=(max(F(0),S)+A)/2
    assert F(0)<alpha<A<F(1,2)
    assert alpha>S
    assert 1-H-iq+H*alpha>0
    return alpha

n=0
for den in range(3,61):
    for num in range(den//2+1,den):
        H=F(num,den)
        for q in [F(201,100),F(21,10),F(5,2),F(3),F(4),F(10),F(1000),None]:
            check(H,q); n+=1
H,q,alpha=F(3,4),F(4),F(1,6)
assert 1-1/H+1/(H*q)==0
assert 1-1/(2*H)==F(1,3)
assert 1-H-1/q+H*alpha==F(1,8)
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
source_dir=root.parent/'private_sources'
verified=[]
for s in manifest['downloaded_sources']:
    p=source_dir/s['local_basename']
    if p.exists():
        data=p.read_bytes()
        assert len(data)==s['bytes']
        assert hashlib.sha256(data).hexdigest()==s['sha256']
        verified.append(s['id'])
print(json.dumps({'status':'PASS','rational_parameter_tests':n,
 'explicit_witness':{'H':'3/4','q':'4','alpha':'1/6','scaling_boundary':'0',
 'old_boundary':'1/3','scaling_exponent':'1/8'},
 'local_source_hashes_verified':verified,
 'scope':'Exact arithmetic and provenance only; no formal verification of the preprint theorem.'},indent=2))
