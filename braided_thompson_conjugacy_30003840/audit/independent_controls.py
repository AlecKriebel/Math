#!/usr/bin/env python3
"""Independent audit controls. No original checker imported; not a solver."""
import itertools as it
import json
import math
import random
from functools import lru_cache


def invword(w): return tuple(-x for x in reversed(w))

def reduced(w):
    out = []
    for x in w:
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return tuple(out)

def subst(w, aut):
    return reduced(x for a in w for x in (aut[a-1] if a > 0 else invword(aut[-a-1])))

def artin(n, w):
    a = tuple((i+1,) for i in range(n))
    for letter in w:
        i = abs(letter)
        g = list((j+1,) for j in range(n))
        if letter > 0: g[i-1],g[i]=(i,i+1,-i),(i,)
        else: g[i-1],g[i]=(i+1,), (-(i+1),i,i+1)
        a = tuple(subst(v,a) for v in g)
    return a

def tracks(n,w):
    labels=list(range(n)); cross=[[0]*n for _ in range(n)]
    for letter in w:
        i=abs(letter)-1; a,b=labels[i:i+2]
        cross[a][b] += 1 if letter>0 else -1
        cross[b][a] = cross[a][b]
        labels[i],labels[i+1]=b,a
    return tuple(labels), tuple(map(tuple,cross))

def lk(n,w):
    p,c=tracks(n,w)
    assert p==tuple(range(n))
    assert all(v%2==0 for row in c for v in row)
    return tuple(tuple(v//2 for v in row) for row in c)

def cable(n,w,source_index):
    # Cable the original source strand. For pure braids this is also the
    # same-index bottom strand in Zaremsky's convention. The two copies
    # never cross each other: crossings are rectangular block crossings.
    blocks=[(i, 2 if i==source_index else 1) for i in range(n)]
    out=[]
    for letter in w:
        i=abs(letter)-1; a,b=blocks[i:i+2]
        start=sum(s for _,s in blocks[:i]); s,t=a[1],b[1]
        sign=1 if letter>0 else -1
        for j in range(t):
            out.extend(sign*(k+1) for k in range(start+s+j-1,start+j-1,-1))
        blocks[i],blocks[i+1]=b,a
    return tuple(out)

def dupmat(m,k):
    inds=list(range(len(m))); inds.insert(k+1,k)
    return tuple(tuple(m[i][j] for j in inds) for i in inds)

def permprod(a,b): return tuple(a[b[i]] for i in range(len(a)))
def perminv(a): return tuple(a.index(i) for i in range(len(a)))
def conj(a,b): return permprod(permprod(a,b),perminv(a))

def semiprod(x,y):
    a,f=x; b,g=y
    return permprod(a,conj(f,b)),permprod(f,g)
def semiinv(x):
    a,f=x
    return conj(perminv(f),perminv(a)),perminv(f)

@lru_cache(None)
def trees(n):
    if n==1: return (("",),)
    return tuple(tuple('0'+s for s in a)+tuple('1'+s for s in b)
                 for k in range(1,n) for a in trees(k) for b in trees(n-k))

def common(*parts):
    words=set(w for p in parts for w in p)
    return tuple(sorted(w for w in words if not any(v!=w and v.startswith(w) for v in words)))

def compose_tables(a,b):
    # a after b, all entries are (domain prefix, range prefix).
    out=[]
    for d,t in b:
        for e,u in a:
            if e.startswith(t): out.append((d+e[len(t):],u))
            elif t.startswith(e): out.append((d,u+t[len(e):]))
    return tuple(sorted(set(out)))

def image_word(w,tab):
    matches=[t+w[len(d):] for d,t in tab if w.startswith(d)]
    assert len(matches)==1, (w,tab)
    return matches[0]

def invariant_partition(tab,m,start):
    powers=[(("",""),)]
    for _ in range(1,m): powers.append(compose_tables(tab,powers[-1]))
    assert all(d==t for d,t in compose_tables(tab,powers[-1]))
    base=common(start,*(tuple(d for d,t in f) for f in powers))
    orbit_parts=[tuple(sorted(image_word(w,f) for w in base)) for f in powers]
    p=common(*orbit_parts)
    assert tuple(sorted(image_word(w,tab) for w in p))==p
    assert all(any(w.startswith(d) for d in start) for w in p)
    # The induced leaf permutation must be cyclic in T.
    image=[p.index(image_word(w,tab)) for w in p]
    assert len({(j-i)%len(p) for i,j in enumerate(image)})==1
    return p



def submat(m,inds): return tuple(tuple(m[i][j] for j in inds) for i in inds)
def cyclic_key(m):
    n=len(m)
    return min(submat(m,tuple(range(k,n))+tuple(range(k))) for k in range(n))
def reduced_key(m,circular):
    reps=[i for i in range(len(m)) if i==0 or m[i]!=m[i-1]]
    if circular and len(reps)>1 and m[reps[0]]==m[reps[-1]]: reps.pop()
    r=submat(m,reps)
    return cyclic_key(r) if circular else r
@lru_cache(None)
def compositions(total,parts):
    if parts==1: return ((total,),) if total>=1 else ()
    return tuple((x,)+r for x in range(1,total-parts+2) for r in compositions(total-x,parts-1))
def twin_controls():
    matrices=[]
    for n in range(1,5):
        edges=list(it.combinations(range(n),2))
        for bits in it.product((0,1),repeat=len(edges)):
            m=[[0]*n for _ in range(n)]
            for (i,j),v in zip(edges,bits): m[i][j]=m[j][i]=v
            matrices.append(tuple(map(tuple,m)))
    counts={}
    for circular in (False,True):
        witness=set()
        for total in range(1,8):
            expanded={}
            for owner,m in enumerate(matrices):
                if len(m)>total: continue
                for c in compositions(total,len(m)):
                    inds=tuple(i for i,k in enumerate(c) for _ in range(k))
                    key=submat(m,inds)
                    if circular: key=cyclic_key(key)
                    expanded.setdefault(key,set()).add(owner)
            for owners in expanded.values(): witness.update(it.product(owners,repeat=2))
        keys=[reduced_key(m,circular) for m in matrices]
        for i,j in it.product(range(len(matrices)),repeat=2):
            assert ((i,j) in witness)==(keys[i]==keys[j])
        counts['cyclic' if circular else 'linear']=len(matrices)**2
    return counts

def run():
    counts={}
    # Relation checks in faithful Artin action, including cabled words.
    ncheck=0
    for n in range(3,6):
        rels=[]
        for i in range(1,n-1): rels.append(((i,i+1,i),(i+1,i,i+1)))
        for i in range(1,n):
            for j in range(i+2,n): rels.append(((i,j),(j,i)))
        for a,b in rels:
            for sign in (1,-1):
                aa,bb=(a,b) if sign==1 else (invword(a),invword(b))
                assert artin(n,aa)==artin(n,bb)
                for k in range(n):
                    assert artin(n+1,cable(n,aa,k))==artin(n+1,cable(n,bb,k))
                    ncheck+=1
    counts['cabled_relation_checks']=ncheck
    rng=random.Random(30003840+999)
    equiv=clones=hom=0
    for n in range(2,6):
        for _ in range(24):
            v=tuple(rng.choice((-1,1))*rng.randrange(1,n) for _ in range(4))
            i=rng.randrange(1,n); p=v+(i,i)+invword(v)
            h=tuple(rng.choice((-1,1))*rng.randrange(1,n) for _ in range(5))
            hp=tracks(n,h)[0]; pi=perminv(hp)
            m=lk(n,p); q=lk(n,h+p+invword(h))
            assert q==tuple(tuple(m[pi[i]][pi[j]] for j in range(n)) for i in range(n))
            equiv+=1
            for k in range(n):
                cp=cable(n,p,k)
                assert lk(n+1,cp)==dupmat(m,k)
                assert artin(n+1,cable(n,p+invword(p),k))==artin(n+1,())
                clones+=1
                # Restriction to pure braids really is a homomorphism.
                q0=(rng.randrange(1,n),)*2
                assert artin(n+1,cable(n,p+q0,k))==artin(n+1,cp+cable(n,q0,k))
                hom+=1
    counts.update(linking_equivariance=equiv,source_strand_cloning=clones,pure_cloning_homomorphism=hom)
    # Source-vs-bottom convention: nonpure cloning is NOT a homomorphism.
    assert artin(3,cable(2,(1,1),0)) != artin(3,cable(2,(1,),0)*2)
    assert artin(3,(1,2)*3)==artin(3,(2,1)*3)
    assert artin(3,(1,)+(2,1)+(-1,))==artin(3,(1,2))
    assert artin(3,(1,1,2,2,-1,-1,-2,-2))!=artin(3,())
    counts['faithful_braid_witnesses']=3
    counts['exhaustive_binary_matrix_pairs']=twin_controls()
    group=tuple(it.permutations(range(3))); identity=tuple(range(3)); ns=nc=0
    for a,f,k,z in it.product(group,repeat=4):
        actual=semiprod(semiprod((k,z),(a,f)),semiinv((k,z)))
        zfz=conj(z,f)
        expected=(permprod(permprod(k,conj(z,a)),conj(zfz,perminv(k))),zfz)
        assert actual==expected; ns+=1
        if zfz==f:
            norm=permprod(permprod(k,conj(z,a)),conj(f,perminv(k)))
            assert actual==(norm,f); nc+=1
    counts.update(nonabelian_semidirect_conjugation=ns,normalized_centralizer_equation=nc)
    np=0; maxp=0
    starts=tuple(t for n in range(1,6) for t in trees(n))
    for n in range(2,6):
        for tr in trees(n):
            for shift in range(1,n):
                tab=tuple((tr[i],tr[(i+shift)%n]) for i in range(n))
                # Non-symmetric expansion: source and target trees differ.
                d,t=tab[0]; tab=tuple(sorted(tab[1:]+((d+'0',t+'0'),(d+'1',t+'1'))))
                order=n//math.gcd(n,shift)
                for start in starts:
                    base=common(start,tuple(d for d,t in tab),tuple(t for d,t in tab))
                    p=invariant_partition(tab,order,base)
                    np+=1; maxp=max(maxp,len(p))
    counts.update(finite_order_invariant_partitions=np,largest_partition_leaves=maxp)
    return {'status':'PASS','scope':'Independent finite controls; proofs and global termination reviewed separately',
            'counts':counts,'solves_original_problem':False}

if __name__=='__main__': print(json.dumps(run(),indent=2))
