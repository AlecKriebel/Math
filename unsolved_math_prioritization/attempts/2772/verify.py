"""Exact arithmetic checks for the restricted Chern-number obstruction.

This verifies intersection-ring expansions only, not existence/nonexistence
of arbitrary Kodaira surfaces.
"""
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib,json

checks=Counter()
def test(label,condition):
    assert condition,label
    checks[label]+=1
def add(a,b):
    r=dict(a)
    for m,v in b.items():r[m]=r.get(m,0)+v
    return r
def mul(a,b):
    r={}
    for m,v in a.items():
        for n,w in b.items():
            if m&n:continue
            r[m|n]=r.get(m|n,0)+v*w
    return r
def integral(a):return a.get(7,0)
def obstruction(D,K,j,k):return integral(mul(mul(D,add(D,K[j])),add(D,K[k])) )

for a,b,c in product(range(1,6),repeat=3):
    coefficients=[a,b,c];D={1:a,2:b,4:c}
    for degrees in product((2,4,6,8),repeat=3):
        K=[{1<<i:degrees[i]} for i in range(3)]
        for i in range(3):
            j,k=[x for x in range(3) if x!=i]
            expected=coefficients[i]*(6*coefficients[j]*coefficients[k]+2*coefficients[k]*degrees[j]+2*coefficients[j]*degrees[k]+degrees[j]*degrees[k])
            got=obstruction(D,K,j,k)
            test('exact_expansion',got==expected)
            test('positive_ample_product_class',got>0)
test('small_example',obstruction({1:1,2:1,4:1},[{1:2},{2:2},{4:2}],1,2)==18)
test('nonample_boundary_not_excluded',obstruction({1:1},[{1:2},{2:2},{4:2}],0,2)==0)

root=Path(__file__).resolve().parent
out={'artifact_sha256':hashlib.sha256((root/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),
     'assertions_passed':sum(checks.values()),'by_category':dict(checks),
     'scope':'exact finite intersection-ring expansion checks; no universal surface search or proof of the original target'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
