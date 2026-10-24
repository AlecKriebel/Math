#!/usr/bin/env python3
"""Census check using the independently verified complete flat lattice only.
For a rank-two normal flat N, hyperplanes restricted to N^perp are in
bijection with rank-three normal flats containing N. This checks the separate
boundary-profile output without importing any producer or its verifier.
"""
from pathlib import Path
from collections import Counter
from math import comb
import hashlib,json
p=Path(__file__).resolve().parent.parent
ambient=json.loads((p/'arrangement_certificate.json').read_text())['types']
claimed=json.loads((p/'rank2_boundary_profiles.json').read_text())
out=[]
for a,c in zip(ambient,claimed):
 assert a['type']==c['type']
 f2=[frozenset(x['members']) for x in a['rank2_flats']]
 f3=[frozenset(x['members']) for x in a['rank3_flats']]
 pairs=Counter((len(t),sum(t <= s for s in f3)) for t in f2)
 actual=[{'normal_mirrors':m,'restricted_lines':l,'flat_count':n} for (m,l),n in sorted(pairs.items())]
 assert actual==c['profiles']
 # A stronger independent triple tally per rank-three flat.
 assert sum(comb(len(s),3)-sum(comb(len(t),3) for t in f2 if t<=s) for s in f3)==comb(len(a['hyperplanes']),3)-sum(comb(len(t),3) for t in f2)
 out.append({'type':a['type'],'profiles':actual,'rank_two_completeness_precondition':'fresh reproduction.json verifies complete pair partition','rank_three_completeness_precondition':'fresh reproduction.json verifies independent-triple partition'})
r={'status':'PASS','method':'normal flat incidence; restricted lines correspond to containing rank-three normal flats','types':out,'input_sha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['arrangement_certificate.json','rank2_boundary_profiles.json']}}
Path(__file__).with_name('boundary_profiles_verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
