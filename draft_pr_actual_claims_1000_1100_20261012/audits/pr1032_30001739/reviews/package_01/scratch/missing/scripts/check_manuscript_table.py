#!/usr/bin/env python3
"""Check the actual TeX Hall/Y table against complete finite LC graphs."""
from pathlib import Path
import importlib.util
import json
import re
p=Path(__file__).resolve()
spec=importlib.util.spec_from_file_location('table_lc',p.with_name('independent_lc.py'))
lc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)
text=(p.parents[1]/'paper.tex').read_text()
rows=[]
for line in text.splitlines():
    if not re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line): continue
    parts=line.split(' & ')
    partition=re.findall(r'[ABCDT]+',parts[0])
    direction=re.findall(r'[ABCDT]+',parts[1])
    m,n=[x.replace('T','E') for x in direction]
    witness=re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[2])[0]
    witness=tuple(x.replace('T','E') for x in witness)
    wanted=[tuple(x.replace('T','E') for x in pair) for pair in re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[3])]
    X,Y,edges=lc.graph(tuple(m),tuple(n))
    actual=[(m[i],n[j]) for i,j in Y]
    x=(m.index(witness[0]),n.index(witness[1]))
    lc.require(x in X and not edges[x],'paper isolated vertex invalid')
    lc.require(sorted(wanted)==sorted(actual),'paper entire Y mismatch')
    lc.require(set(m)|set(n)==set('ABCDE') and not set(m)&set(n),'paper partition invalid')
    lc.require(sorted([set(z.replace('T','E')) for z in partition],key=lambda s:sorted(s))==sorted([set(m),set(n)],key=lambda s:sorted(s)),'paper direction differs from partition')
    rows.append({'partition':partition,'direction':[m,n],'witness':witness,'entire_Y':actual})
lc.require(len(rows)==15,'paper must display fifteen rows')
keys={frozenset(frozenset(z.replace('T','E')) for z in r['partition']) for r in rows}
lc.require(len(keys)==15,'paper repeated partition')
print(json.dumps({'status':'PASS','manuscript_Hall_rows':rows,'computes_Hom_space':False},indent=2,sort_keys=True))
