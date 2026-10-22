#!/usr/bin/env python3
"""Finite equivalence comparisons; Luo-Zha parameters remain unknown."""
from collections import Counter
from fractions import Fraction as F
import json
def require(value,message):
    if not value: raise RuntimeError(message)
def dual(m): return [(-b,-a) for a,b in m]
def canonical(m):
    c=min(a for a,b in m)
    return sorted((a-c,b-c) for a,b in m)
def invariant(m):
    lengths=[b-a+1 for a,b in m]
    require(all(x.denominator==1 and x>0 for x in lengths),'invalid length')
    return {'degree':int(sum(lengths)),'lengths':sorted(map(int,lengths)),
            'canonical':[[str(a),str(b)] for a,b in canonical(m)],
            'occurrence_multiplicities':sorted(Counter(m).values())}
M=[(F(a),F(b)) for a,b in [(4,6),(2,5),(3,3),(1,4),(0,2)]]
EXAMPLES={
 'OWR_Minguez':[(F(1),F(2)),(F(-1),F(1)),(F(0),F(0))],
 'LM_Leclerc':[(F(3),F(4)),(F(1),F(3)),(F(2),F(2)),(F(0),F(1))],
 'MOS_Langlands':[(F(4),F(4)),(F(3),F(3)),(F(3),F(3)),(F(2),F(2)),(F(1),F(2)),(F(0),F(1))],
 'MOS_Zelevinsky_dual':[(F(2),F(3)),(F(1),F(4)),(F(0),F(1))],
 'GMM':[(F(1,2),F(3,2)),(F(-1,2),F(7,2)),(F(-3,2),F(-1,2)),(F(-5,2),F(5,2)),(F(-7,2),F(1,2))],
 'Sharma':[(F(0),F(0)),(F(0),F(1)),(F(0),F(1)),(F(1),F(1)),(F(1),F(2))]}
rows=[]
for name,n in EXAMPLES.items():
    equiv=canonical(M) in (canonical(n),canonical(dual(n)))
    require(not equiv,'inspected earlier construction equivalent')
    rows.append({'example':name,'invariant':invariant(n),'translation_dual_reordering_equivalent':equiv})
require(sorted((a+6,b+6) for a,b in dual(M))==sorted(M),'candidate dual identity')
print(json.dumps({'status':'PASS','candidate':invariant(M),'examples':rows,
 'Luo_Zha':{'parameters':'UNKNOWN','mechanism_overlap':'UNKNOWN','period_consequences':'UNKNOWN'},
 'novelty_certified':False},indent=2,sort_keys=True))
