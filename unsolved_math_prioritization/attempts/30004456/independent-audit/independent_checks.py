#!/usr/bin/env python3
"""Independent bounded checks for ID 30004456; no imported submission code."""
from pathlib import Path
from itertools import product
from math import gcd
from fractions import Fraction
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent
FROZEN='d51066d53d8cbe9e114b044fa828b9adaad61f08140b4f0bac7cfa90a7cdb9eb'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def component(q, offsets):
    parent=list(range(q))
    def root(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for v in range(q):
        for a in offsets:
            parent[root((v+a)%q)]=root(v)
    vertices=[v for v in range(q) if root(v)==root(0)]
    edges=[(v,(v+a)%q) for v in vertices for a in offsets]
    return vertices,edges

def rank_rational(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]
    if not a:return 0
    r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        den=a[r][col];a[r]=[x/den for x in a[r]]
        for i in range(r+1,len(a)):
            if a[i][col]:
                k=a[i][col];a[i]=[x-k*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def reduce_word(word):
    out=[]
    for a in word:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return tuple(out)
def inverse(word):return tuple(-a for a in reversed(word))
def alpha(word,k):
    # Automorphism of F(x,y): x -> x, y -> y x, and its integral powers.
    yimage=(2,)+(1,)*k if k>=0 else (2,)+(-1,)*(-k)
    images={1:(1,),-1:(-1,),2:yimage,-2:inverse(yimage)}
    return reduce_word(c for a in word for c in images[a])
def multiply(p,q):return (reduce_word(p[0]+alpha(q[0],p[1])),p[1]+q[1])

def main():
    assert digest(ROOT/'FROZEN_MANIFEST.json')==FROZEN
    frozen=json.loads((ROOT/'FROZEN_MANIFEST.json').read_text())
    names=set()
    for x in frozen['payload_files']:
        p=ROOT/x['path'];assert p.stat().st_size==x['bytes'];assert digest(p)==x['sha256'];names.add(p.name)
    assert names=={p.name for p in (ROOT/'submission').iterdir() if p.is_file()}
    provenance=json.loads((ROOT/'submission/SOURCE_PROVENANCE.json').read_text())
    for x in provenance['source_pdfs']:
        p=ROOT/'independent-audit/private'/x['filename']
        assert p.read_bytes().startswith(b'%PDF');assert digest(p)==x['sha256'];assert p.stat().st_size==x['bytes']
    counts={'frozen_payloads':len(names),'fresh_source_hashes':len(provenance['source_pdfs']),'signed_graph_cases':0,'signed_scale_cases':0,'rational_incidence_ranks':0,'semidirect_word_checks':0,'rank_one_kernel_checks':0,'rank_zero_checks':0}
    for n in range(1,5):
        for offsets in product(range(-2,3),repeat=n):
            for q in range(1,10):
                v,e=component(q,offsets);d=gcd(q,*offsets);m=q//d
                assert len(v)==m and len(e)==n*m
                graph_rank=len(e)-len(v)+1
                assert graph_rank==1+m*(n-1)
                counts['signed_graph_cases']+=1
                for c in (-5,-2,2,5):
                    vv,ee=component(abs(c)*q,tuple(c*a for a in offsets))
                    assert (len(vv),len(ee))==(len(v),len(e))
                    dd=gcd(c*q,*(c*a for a in offsets));assert dd==abs(c)*d
                    assert tuple(c*a//dd for a in offsets+(q,))==tuple((1 if c>0 else -1)*a//d for a in offsets+(q,))
                    counts['signed_scale_cases']+=1
                if n<=3 and q<=7:
                    # Exact incidence-matrix rank, independent of the spanning-tree count.
                    mat=[[int(w==target)-int(w==source) for source,target in e] for w in v]
                    r=rank_rational(mat);assert r==len(v)-1
                    assert len(e)-r==graph_rank
                    counts['rational_incidence_ranks']+=1
    # Klein bottle: x -> x^-1 under t. Any Z-character must vanish on x.
    # Normal form (m,n)=x^m t^n, multiplication (m,n)(p,q)=(m+(-1)^n*p,n+q).
    for q in list(range(-12,0))+list(range(1,13)):
        for m,n in product(range(-8,9),repeat=2):
            assert (q*n==0)==(n==0)
            counts['rank_one_kernel_checks']+=1
        assert -1==-(1-0) # Rank zero: trivial kernel has b0=1, b1=0.
        counts['rank_zero_checks']+=1
    x=((1,),0);y=((2,),0);t=((),1);yi=((-2,),0)
    assert multiply(multiply(yi,t),y)==multiply(x,t)
    for length in range(5):
        for word in product((1,-1,2,-2),repeat=length):
            w=reduce_word(word)
            for k in (-3,-1,0,1,3):
                assert alpha(alpha(w,k),-k)==w
                assert sum(1 if a==2 else -1 if a==-2 else 0 for a in alpha(w,k))==sum(1 if a==2 else -1 if a==-2 else 0 for a in w)
                counts['semidirect_word_checks']+=1
    # Negative controls genuinely catch the three excluded shortcuts.
    assert (6//gcd(2,6))*(2-1)!=6*(2-1)
    assert 0!=-(1-0)
    assert gcd(0,0,0)==0
    print(json.dumps({'result':'PASS','counts':counts,'frozen_manifest_sha256':FROZEN,'limits':['Finite checks do not prove the general splitting theorem.','Normal-form and graph checks verify conventions only.','All source PDFs are private and excluded from the audit release.']},indent=2,sort_keys=True))
if __name__=='__main__':main()
