import json, hashlib
from pathlib import Path

def rank(vectors):
    basis={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p in basis: v^=basis[p]
            else:
                basis[p]=v; break
    return len(basis)

def apply(rows,v):
    return sum(((row&v).bit_count()%2)<<i for i,row in enumerate(rows))

def check(rows):
    n=len(rows)
    columns=[apply(rows,1<<i) for i in range(n)]
    r1=rank(columns); r2=rank([apply(rows,c) for c in columns])
    e=n-2*r1+r2
    kernel=[v for v in range(1<<n) if apply(rows,v)==0]
    dualker=[v for v in range(1<<n) if all((v&c).bit_count()%2==0 for c in columns)]
    dimker=rank(kernel)
    # dim(K intersect I) = dim K + dim I - dim(K+I)
    intersection=dimker+r1-rank(kernel+columns)
    assert e==dimker-intersection
    pairingrows=[sum(((v&w).bit_count()%2)<<i for i,w in enumerate(dualker)) for v in kernel]
    assert rank(pairingrows)==e
    assert e>=0
    return e

counts=0
for n in range(7):
    positions=[(i,j) for i in range(n) for j in range(i+1,n)]
    for mask in range(1<<len(positions)):
        rows=[0]*n
        for k,(i,j) in enumerate(positions):
            if (mask>>k)&1: rows[i]|=1<<j
        check(rows); counts+=1
assert check([0])==1
assert check([2,0])==0
assert check([2,0,0])==1
assert check([0,0])==2
p=Path(__file__).parent
receipt={'status':'PASS','matrices':counts,'assertions':3*counts+16,'control_cases':4,'scope':'strictly upper triangular binary matrices, dimensions 0 through 6; no Floer realization claim','artifact_sha256':hashlib.sha256((p/'PARTIAL_RESULT.md').read_bytes()).hexdigest()}
(p/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
