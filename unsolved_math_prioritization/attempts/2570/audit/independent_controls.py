#!/usr/bin/env python3
"""Independent bounded controls for KOU-21.61; no author helper imports."""
import hashlib, json, math, sys
from pathlib import Path
from itertools import product
if len(sys.argv) != 2:
    raise SystemExit('Usage: python independent_controls.py PATH_TO_FROZEN_PAYLOAD')
ROOT = Path(sys.argv[1])
EXPECTED = '0ec82991eabebee6e9366a9795ea75beb2806962b458f9b288ad3688c444db5b'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(ROOT/'AUTHOR_MANIFEST.json') == EXPECTED
manifest = json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
assert len(manifest['files']) == 8
assert {p.name for p in ROOT.iterdir()} == {f['path'] for f in manifest['files']} | {'AUTHOR_MANIFEST.json'}
for record in manifest['files']:
    p = ROOT/record['path']
    assert p.is_file() and not p.is_symlink()
    assert p.stat().st_size == record['bytes'] and digest(p) == record['sha256']
def red(w):
    ans=[]
    for x in w:
        if ans and ans[-1]==-x: ans.pop()
        else: ans.append(x)
    return tuple(ans)
def inv(w): return tuple(-x for x in reversed(w))
def mul(*words): return red(x for w in words for x in w)
def power(w,k): return mul(*([w if k>=0 else inv(w)]*abs(k)))
def sub(w,images): return mul(*(images[x] if x>0 else inv(images[-x]) for x in w))
a,b=(1,),(2,)
# A non-inner periodic-outer automorphism: phi = inn(a) composed with a/b swap.
phi={1:mul(a,b,inv(a)),2:a}
phi_inv={1:b,2:mul(inv(b),a,b)}
for x in (a,b):
    assert sub(sub(x,phi),phi_inv)==x and sub(sub(x,phi_inv),phi)==x
c=mul(a,b)
for x in (a,b): assert sub(sub(x,phi),phi)==mul(c,x,inv(c))
def phipow(w,k):
    for _ in range(abs(k)): w=sub(w,phi if k>=0 else phi_inv)
    return w
def gmul(x,y): return mul(x[0],phipow(y[0],x[1])), x[1]+y[1]
def ginv(x): return phipow(inv(x[0]),-x[1]),-x[1]
def gpow(x,k):
    if k<0: x=ginv(x)
    ans=((),0)
    for _ in range(abs(k)): ans=gmul(ans,x)
    return ans
z=(inv(c),2)
for x in (a,b): assert gmul(gmul(z,(x,0)),ginv(z))==(x,0)
coordinate_cases=0
words=[(),a,b,mul(a,b,inv(a)),mul(inv(b),a)]
for f in words:
    for ell in range(-7,8):
        assert gmul((mul(f,power(c,ell)),0),gpow(z,ell))==(f,2*ell)
        coordinate_cases+=1
# Finite quotient arithmetic, including trivial image and non-surjective image.
quotient_cases=0
for m in range(1,13):
    for heights in product(range(-3,4),repeat=3):
        D={0}
        while True:
            enlarged=D|{(r+k)%m for r in D for k in heights}
            if enlarged==D: break
            D=enlarged
        g=math.gcd(m,*heights)
        assert len(D)==m//g and D==set(range(0,m,g))
        q=len(D)
        assert (q*g)%m==0
        assert all((j*g)%m != 0 for j in range(1,q))
        quotient_cases+=1
# Count actual graph components rather than assuming the claimed rank formula.
plateau_cases=0
for M in range(1,65):
    for N in range(0,M+4):
        I=set(range(N+1))|set(range(M,M+N+1))
        J=set(range(N))|set(range(M,M+N))
        parent={i:i for i in I}
        def find(i):
            while parent[i]!=i:
                parent[i]=parent[parent[i]]; i=parent[i]
            return i
        for i in J:
            assert i in I and i+1 in I
            parent[find(i)]=find(i+1)
        comps={find(i) for i in I}
        assert len(comps)==(2 if N<M else 1)
        assert len(J)==len(I)-len(comps) # no hidden cycles
        # In the pre-merger eliminated basis s=1,x0=2,xM=3, test missing relator.
        if N<M:
            witness=(-3,)+(1,)*M+(2,)+(-1,)*M
            assert red(witness)==witness and len(witness)==2*M+2
            ambient={1:a,2:b,3:mul(power(a,M),b,power(a,-M))}
            assert sub(witness,ambient)==()
        plateau_cases+=1
# Independently check the automorphism and distortion recurrence of Proposition 7.
psi={1:(1,2),2:(1,)}
psi_inv={1:(2,),2:(-2,1)}
for x in (a,b): assert sub(sub(x,psi),psi_inv)==x and sub(sub(x,psi_inv),psi)==x
w=a; Fprev,Fcur=1,1
lengths=[]
for k in range(19):
    expected=Fcur
    assert len(w)==expected and all(x>0 for x in w)
    lengths.append([k,len(w),2*k+1])
    w=sub(w,psi); Fprev,Fcur=Fcur,Fprev+Fcur
# A^m is never identity in this tested range; general proof uses positive growth.
A=((1,1),(1,0)); P=((1,0),(0,1))
for m in range(1,65):
    P=tuple(tuple(sum(P[i][k]*A[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    assert P[0][1]>0
result={
    'author_manifest_sha256':EXPECTED,'payload_records_bound':8,
    'periodic_outer_coordinate_cases':coordinate_cases,
    'finite_quotient_cases':quotient_cases,
    'plateau_cases':plateau_cases,
    'fibonacci_controls':lengths,
    'status':'all independent bounded assertions passed',
    'limits':'Finite controls support the written audit; they do not prove general effective coherence or implement every scoped algorithm.'
}
print(json.dumps(result,indent=2))
