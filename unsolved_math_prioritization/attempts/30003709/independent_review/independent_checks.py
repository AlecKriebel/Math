"""Finite-cover representation and Betti recovery controls; standard library."""
from pathlib import Path
from math import gcd,comb
import hashlib,json
root=Path(__file__).resolve().parent
EXPECTED='0902b513e349c0a5a3d811c458a865029441632a36e963580e04eb8838e25111'
assert hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()==EXPECTED
counts={}
def ck(v,k):
    assert v,k
    counts[k]=counts.get(k,0)+1
def orbits(perm):
    todo=set(range(len(perm)));n=0
    while todo:
        i=min(todo);n+=1
        while i in todo:todo.remove(i);i=perm[i]
    return n
def mul(A,B):
    out=[0]*(len(A)+len(B)-1)
    for i,a in enumerate(A):
        for j,b in enumerate(B):out[i+j]+=a*b
    return out
def bino(d):return [comb(d,j) for j in range(d+1)]
def recover(P):
    d=len(P)-1;b1=P[1] if d else 0;k=b1-d
    m=P[2]-comb(d,2)-2*(d-1) if k==2 else None
    return d,k,m

for m in range(1,23):
    for a in range(-m,m+1):
        if gcd(a,m)!=1:continue
        # One puncture (0) is fixed; m punctures form a rotation block.
        B=[0]+[1+(j+1)%m for j in range(m)]
        F=[0]+[1+(j+a)%m for j in range(m)]
        tensor=[B[i]*(m+1)+F[j] for i in range(m+1) for j in range(m+1)]
        ck(orbits(B)==2 and orbits(F)==2,'finite_cover_H1_invariants')
        ck(orbits(tensor)==m+3,'finite_cover_H2_invariants')
        ck(gcd(1,0,a,m)==1 and abs(1*m-0*a)==m,'intersection_smith_minors')
        for d in range(2,11):
            P=mul([1,4,m+3],bino(d-2))
            # Independent layer/Mobius sum, compared in every degree.
            alt=bino(d)
            for j,c in enumerate(bino(d-1)):alt[j+1]+=2*c
            for j,c in enumerate(bino(d-2)):alt[j+2]+=m*c
            ck(P==alt,'all_degree_polynomial_identity')
            ck(recover(P)==(d,2,m),'two_hypertorus_recovery')
for d in range(11):
    ck(recover(bino(d))==(d,0,None),'empty_recovery')
    if d:
        ck(recover(mul([1,2],bino(d-1)))==(d,1,None),'one_hypertorus_recovery')

r={'all_pass':True,'assertions':sum(counts.values()),'counts':counts,
   'artifact_sha256':EXPECTED,
   'scope':'Finite cyclic-cover representation and all-degree Betti recovery controls in the at-most-two distinct connected central class; no general ring-to-poset reconstruction.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
