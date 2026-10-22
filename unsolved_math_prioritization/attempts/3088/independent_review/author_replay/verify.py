import itertools,math,json,hashlib
from pathlib import Path
P=Path(__file__).parent
r=json.loads((P/'finite_coloring.json').read_text());V=[tuple(v) for v in r['vectors']];C=r['colors']
expected=sorted({tuple((-x if next(t for t in v if t)<0 else x) for x in v) for v in itertools.product(range(-3,4),repeat=3) if any(v) and math.gcd(*v)==1})
assert V==expected and len(V)==145
assert len(C)==len(V) and set(C)<=set(range(4))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
checks=2;bad=0
for i,j,k in itertools.combinations(range(len(V)),3):
    prod=dot(V[i],V[j])*dot(V[i],V[k])*dot(V[j],V[k]);bad+=prod<0
    assert C[i]!=C[j] or C[j]!=C[k] or prod>=0;checks+=1
for v in [(1,1,0),(1,-1,0),(1,0,1),(1,0,-1)]:
    assert C[V.index(v)]==0;checks+=1
assert bad==125614;checks+=1
A=[(1,1,0),(1,-1,0),(1,0,1),(1,0,-1)]
for a,b,c in itertools.combinations(A,3):
    assert dot(a,b)*dot(a,c)*dot(b,c)>=0;checks+=1
out={'status':'PASS','assertions':checks,'directions':len(V),'triples':math.comb(len(V),3),'negative_product_triples':bad,'scope':'finite grid certificate only; no global coloring or full conjecture claim','artifact_sha256':hashlib.sha256((P/'PARTIAL_RESULT.md').read_bytes()).hexdigest()}
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
