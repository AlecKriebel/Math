#!/usr/bin/env python3
"""Independent chain-level controls. Standard library; finite F2 tests only."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
counts=Counter()
def ck(x,label):
    assert x,label
    counts[label]+=1

def xor(vs):
    r=0
    for v in vs:r^=v
    return r

def bitlist(v):return [i for i in range(v.bit_length()) if v>>i&1]

# Actual algebra: (corner, exponents) ordered f,x,y,xy,e,m,xm.
B=[('A',0,0),('A',1,0),('A',0,1),('A',1,1),('K',0,0),('M',0,0),('M',1,0)]
def atom_mul(i,j):
    c,a,b=B[i];d,s,t=B[j]
    if (c,d)==('A','A'):z=('A',a+s,b+t)
    elif (c,d)==('A','M'):z=('M',a+s,b)
    elif (c,d)==('M','K'):z=B[i]
    elif (c,d)==('K','K'):z=B[i]
    else:return 0
    if z not in B:return 0
    return 1<<B.index(z)
def mul(v,w):return xor(atom_mul(i,j) for i in bitlist(v) for j in bitlist(w))
def words(n):
    if n==0:return [()]
    return list(product((1,2,3),repeat=n))+[w+(m,) for w in product((1,2,3),repeat=n-1) for m in (5,6)]
def evalf(f,w):return f.get(w,0)
def db(f,n,w):
    ans=mul(1<<w[0],evalf(f,w[1:]))^mul(evalf(f,w[:-1]),1<<w[-1])
    for q in range(n):
        for t in bitlist(atom_mul(w[q],w[q+1])):
            ans^=evalf(f,w[:q]+(t,)+w[q+2:])
    return ans

def solve(columns,target):
    piv={}
    for i,v in enumerate(columns):
        t=1<<i
        while v:
            p=v.bit_length()-1
            if p not in piv:piv[p]=(v,t);break
            z,s=piv[p];v^=z;t^=s
    ans=0
    while target:
        p=target.bit_length()-1
        if p not in piv:return None
        z,s=piv[p];target^=z;ans^=s
    return ans

# Build mixed corrections rather than assuming the ambient cocycle extends.
def monomial_cochain(m):
    a,b,i,j=m;n=i+j
    coeff=1<<(a+2*b);f={}
    for w in product((1,2,3),repeat=n):
        z=coeff
        for pos,t in enumerate(w):
            _,ax,ay=B[t]
            if pos<i:
                d=0 if ax==0 else 1<<(2*ay)
            else:d=0 if ay==0 else 1<<ax
            z=mul(z,d)
        if z:f[w]=z
    return f

def image_on_shuffle(f,n):
    out=set()
    for i in range(n+1):
        val=xor(evalf(f,tuple(1 if t in where else 2 for t in range(n))) for where in map(set,combinations(range(n),i)))
        for c in bitlist(val):
            ck(c<4,'shuffle output corner')
            out.add((c%2,c//2,i,n-i))
    return out

lifts={}
for m,value in [((0,0,0,0),(1<<0)|(1<<4)),((0,1,0,0),1<<2),((1,1,0,0),1<<3)]:
    f={():value};lifts[m]=f
    for w in words(1):ck(db(f,0,w)==0,'degree-zero centrality')
for n in range(1,4):
    mixed=[w for w in words(n) if w[-1]>=5]
    mixednext=[w for w in words(n+1) if w[-1]>=5]
    coordinates=[(w,t) for w in mixed for t in (5,6)]
    def encode_delta(f):
        return xor((db(f,n,w)>>(5+t)&1)<<(2*r+t) for r,w in enumerate(mixednext) for t in range(2))
    columns=[encode_delta({w:1<<t}) for w,t in coordinates]
    for i in range(n+1):
        for a,b in product(range(2),repeat=2):
            if not(i or b):continue
            m=(a,b,i,n-i);f=monomial_cochain(m)
            correction=solve(columns,encode_delta(f))
            ck(correction is not None,'actual mixed correction exists')
            for t in bitlist(correction):
                w,o=coordinates[t];f[w]=f.get(w,0)^(1<<o)
            for w in words(n+1):ck(db(f,n,w)==0,'actual lifted cocycle')
            ck(image_on_shuffle(f,n)=={m},'cup-coordinate normalization')
            lifts[m]=f

# Full relative insertions, including zero-arity input and idempotent normalization.
radmask=sum(1<<i for i in (1,2,3,5,6))
def insert(f,p,g,q,w):
    result=0
    for s in range(p):
        val=evalf(g,w[s:s+q])&radmask
        for t in bitlist(val):result^=evalf(f,w[:s]+(t,)+w[s+q:])
    return result

def predicted(m,n):
    out=set()
    for s,t in ((0,2),(2,0),(1,3),(3,1)):
        if m[s]%2==0 or n[t]%2==0:continue
        z=[m[a]+n[a] for a in range(4)];z[s]-=1;z[t]-=1
        if z[0]>=2 or z[1]>=2:continue
        z=tuple(z)
        if z in out:out.remove(z)
        else:out.add(z)
    return out
bracket_pairs=0
# Both higher-input-degree and degree-zero cases, total input degrees <=5.
for m,f in lifts.items():
    p=m[2]+m[3]
    for n,g in lifts.items():
        q=n[2]+n[3];d=p+q-1
        if d<0 or p+q>5:continue
        h={w:insert(f,p,g,q,w)^insert(g,q,f,p,w) for w in words(d)}
        ck(image_on_shuffle(h,d)==predicted(m,n),'actual relative higher bracket')
        for w in words(d+1):ck(db(h,d,w)==0,'bracket cocycle')
        bracket_pairs+=1

# Shuffle chain-map identity in normalized bar chains, with outer monomials.
def symdiff_terms(terms):
    out=set()
    for t in terms:
        if t in out:out.remove(t)
        else:out.add(t)
    return out

def shuffle(i,j):
    n=i+j
    return {tuple(1 if p in S else 2 for p in range(n)) for S in map(set,combinations(range(n),i))}
def bar_boundary(w):
    ts=[(w[0],w[1:],0),(0,w[:-1],w[-1])]
    for s in range(len(w)-1):
        z=atom_mul(w[s],w[s+1])
        for t in bitlist(z):ts.append((0,w[:s]+(t,)+w[s+2:],0))
    return ts
for n in range(1,11):
    for i in range(n+1):
        j=n-i
        left=symdiff_terms(t for w in shuffle(i,j) for t in bar_boundary(w))
        right=[]
        if i:
            for w in shuffle(i-1,j):right.extend([(1,w,0),(0,w,1)])
        if j:
            for w in shuffle(i,j-1):right.extend([(2,w,0),(0,w,2)])
        ck(left==symdiff_terms(right),'shuffle chain map')

# A^e resolution ranks, tensor-with-M ranks, and Q comparison through degree 12.
def rank(cols):
    piv={}
    for v in cols:
        while v:
            p=v.bit_length()-1
            if p not in piv:piv[p]=v;break
            v^=piv[p]
    return len(piv)
def dP(n,tensor=False):
    # basis (i,a,b,c,d): x/y degrees i,n-i; outer xL,yL,xR,yR
    outer=list(product(range(2),repeat=3 if tensor else 4))
    now=[(i,)+z for i in range(n+1) for z in outer]
    prev=[(i,)+z for i in range(n) for z in outer];idx={z:j for j,z in enumerate(prev)}
    cols=[]
    for z in now:
        i,*ex=z;j=n-i;dest=[]
        for typ,positions,ni in [('x',(0,2),i-1),('y',(1,) if tensor else (1,3),i)]:
            if (typ=='x' and not i) or (typ=='y' and not j):continue
            for pos in positions:
                if ex[pos]==0:
                    e=ex.copy();e[pos]=1;dest.append(1<<idx[(ni,)+tuple(e)])
        cols.append(xor(dest))
    return now,prev,cols
for tensor in (False,True):
    last=None
    for n in range(1,13):
        now,prev,cols=dP(n,tensor)
        ck(rank(cols)==((4*n+2) if tensor else (8*n+4)),'resolution ranks')
        if last is not None:
            for v in cols:ck(xor(last[i] for i in bitlist(v))==0,'resolution differential square')
        last=cols
        if tensor:
            index={z:i for i,z in enumerate(now)};previndex={z:i for i,z in enumerate(prev)}
            for a,b in product(range(2),repeat=2):
                # j_n sends a monomial in A to its left multiple of e_(0,n) tensor 1.
                out=cols[index[(0,a,b,0)]]
                expect=0 if b else 1<<previndex[(0,a,1,0)]
                ck(out==expect,'all-degree Q comparison diagnostics')

here=Path(__file__).resolve().parent
result={'problem_id':30002879,'assertions':sum(counts.values()),'sections':dict(counts),
 'actual_relative_bracket_pairs':bracket_pairs,'lifted_basis_classes':len(lifts),
 'shuffle_max_degree':10,'resolution_max_degree':12,
 'artifact_sha256':sha256((here/'author_replay/PROOF.md').read_bytes()).hexdigest(),
 'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Independent finite F2 chain, cocycle, and actual relative-bar insertion controls. The all-degree and all-characteristic-two-field conclusions rely on the audited mathematical proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
