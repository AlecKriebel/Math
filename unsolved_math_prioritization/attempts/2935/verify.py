from math import gcd
from pathlib import Path
import json,hashlib
p,q,r=231,53,86
units=[u for u in range(p) if gcd(u,p)==1]
roots=[u for u in units if (r*u*u-q)%p==0]
assert roots==[10,32,67,109,122,164,199,221]
assert sorted({q,-q%p,pow(q,-1,p),-pow(q,-1,p)%p})==[53,61,170,178]
assert r not in {q,-q%p,pow(q,-1,p),-pow(q,-1,p)%p}
assert r*100-q==37*p
checks=4
for u in roots:
    assert len({u*x%p for x in range(p)})==p;checks+=1
    for x in range(p):
        for y in range(p):
            assert (q*x*y-r*(u*x%p)*(u*y%p))%p==0; checks+=1
# For u=10 compute orthogonal complement directly, not from its predicted size.
orth=[(a,b) for a in range(p) for b in range(p) if (q*a-r*10*b)%p==0]
graph={(x,10*x%p) for x in range(p)}
assert set(orth)==graph;checks+=1
for b1 in range(100):
    b2,b3=2*b1,b1+1
    assert 1-b1+b2-b3==0;checks+=1
out={'status':'PASS','assertions':checks,'roots':roots,'unoriented_homeomorphism_orbit':[53,61,170,178],'metabolizer_size':len(graph),'scope':'exact modular linking-form and integer-cover identities only; no cobordism construction','artifact_sha256':hashlib.sha256((Path(__file__).parent/'PARTIAL_RESULT.md').read_bytes()).hexdigest()}
(Path(__file__).parent/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
