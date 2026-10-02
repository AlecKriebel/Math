#!/usr/bin/env python3
"""Standalone exact certificate verification; does not call the search code."""
from itertools import combinations,permutations
from pathlib import Path
import json
E=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)]
E=list(map(lambda e:tuple(sorted(e)),E));counts={}
def ck(x,k):
 assert x,k;counts[k]=counts.get(k,0)+1

def image(mask,p):
 return sum(1<<E.index(tuple(sorted((p[a],p[b])))) for i,(a,b) in enumerate(E) if mask>>i&1)
def trianglefree(mask):
 edges={e for i,e in enumerate(E) if mask>>i&1}
 return not any(all(tuple(e) in edges for e in combinations(T,2)) for T in combinations(range(6),3))
def colors_ok(mask,C):
 for S in C:ck(len(S)==3 and len(set(S))==3 and set(S)<=set(range(1,9)),'palette_triples')
 for i,(a,b) in enumerate(E):
  t=len(set(C[a])&set(C[b]));ck(t==0 if mask>>i&1 else t in (1,2),'edge_type_overlaps')
D=json.loads((Path(__file__).parent/'prism_certificates.json').read_text())
autos=[p for p in permutations(range(6)) if {tuple(sorted((p[a],p[b]))) for a,b in E}==set(E)]
ck(len(autos)==12,'automorphism_count')
valid=[m for m in range(512) if trianglefree(m)];ck(len(valid)==392,'labeled_valid_count')
canonical={m:min(image(m,p) for p in autos) for m in valid};ck(len(set(canonical.values()))==54,'orbit_count')
cert={c['mask']:c['triples'] for c in D['certificates']};ck(len(cert)==54 and set(cert)==set(canonical.values()),'complete_orbit_certificate')
for m,C in cert.items():colors_ok(m,C)
for m in valid:
 rep=canonical[m];p=next(p for p in autos if image(rep,p)==m);C=[None]*6
 for i,S in enumerate(cert[rep]):C[p[i]]=S
 colors_ok(m,C);ck(image(rep,p)==m,'orbit_transport')
print(json.dumps({'status':'pass','assertions':sum(counts.values()),'breakdown':counts,'all_trianglefree_core_patterns':392,'automorphisms':12,'certified_orbits':54,'scope':'Complete finite proof certificate for branch color constraints; arbitrary subdivision lengths use the written integer path-extension theorem.'},indent=2,sort_keys=True))
