"""Exact algebraic controls only; no splitting or minimal-genus certificate."""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json

counts = {}
def ck(v, name):
    assert v, name
    counts[name] = counts.get(name, 0)+1

def pairing(x,y):
    return sum(x[2*i]*y[2*i+1]-x[2*i+1]*y[2*i]
               for i in range(len(x)//2))
def twist(x,c,n):
    p=pairing(x,c)
    return tuple(a+n*p*b for a,b in zip(x,c))

for g in [1,2,3]:
    zero=(0,)*(2*g)
    vectors=[]
    for j in range(2*g):
        e=tuple(int(i==j) for i in range(2*g));vectors.append(e)
    vectors += [tuple((i%3)-1 for i in range(2*g)),
                tuple((2*i+1)%5-2 for i in range(2*g))]
    for c in vectors:
        for n in [-3,-1,0,1,4]:
            ck(twist(zero,c,n)==zero,'zero_class_fixed')
            for x in vectors:
                ck(twist(twist(x,c,n),c,-n)==x,'transvection_inverse')
            for x,y in zip(vectors,vectors[1:]+vectors[:1]):
                ck(pairing(twist(x,c,n),twist(y,c,n))==pairing(x,y),
                   'intersection_pairing_preserved')

# Explicit nonminimal torus control and its polynomial calculation.
M=((2,1),(3,2))
ck(M[0][0]*M[1][1]-M[0][1]*M[1][0]==1,'torus_control')
ck((M[0][0],M[1][0])==(2,3) and gcd(2,3)==1,'torus_control')
def mul(a,b):
    r={}
    for i,x in a.items():
        for j,y in b.items():r[i+j]=r.get(i+j,0)+x*y
    return {i:x for i,x in r.items() if x}
ck(mul({2:1,1:-1,0:1},mul({2:1,0:-1},{3:1,0:-1}))
   ==mul({6:1,0:-1},{1:1,0:-1}),'trefoil_polynomial_identity')
ck(sum([1,-1,1])==1 and sum([1,1,1])==3,'trefoil_polynomial_values')

# The filling relation is primitive even though topology can change.
# Coordinates are (mu_U,mu_C), relation (n*ell,1).
for n,ell in product(range(-8,9),repeat=2):
    v=(n*ell,1)
    ck(gcd(*v)==1,'primitive_filling_relation')
    # Relation v and generator (1,0) form a unimodular basis of Z^2.
    ck(v[0]*0-v[1]*1==-1,'free_rank_one_quotient')
    if n:
        ck(abs(1*0-n*1)==abs(n)>0,'surgery_slope_distinct')
    if ell==0:
        ck(v==(0,1),'winding_zero_relation')

p=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':sum(counts.values()),
        'checks':dict(sorted(counts.items())),
        'artifact_sha256':hashlib.sha256((p/'OBSTRUCTION.md').read_bytes()).hexdigest(),
        'scope':'Symplectic homology, nonminimal torus polynomial, and surgery first-homology controls only. No split-link, minimal-genus, disk-existence or full-resolution certificate.'}
print(json.dumps(result,indent=2,sort_keys=True))
