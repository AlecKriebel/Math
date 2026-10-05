#!/usr/bin/env python3
"""Independent exact controls; standard library only; no author-code imports."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, product
from fractions import Fraction as Q
from math import comb, prod, gcd
import json, random

# A root-block / interval construction, distinct from the author's Bell-partition filter.
@lru_cache(None)
def nc(n):
    if n == 0:
        return ((),)
    answer = []
    for size in range(n):
        for tail in combinations(range(1,n),size):
            root = (0,) + tail
            stops = root[1:] + (n,)
            gaps = [(a+1,b) for a,b in zip(root,stops)]
            for parts in product(*(nc(b-a) for a,b in gaps)):
                blocks = [root]
                for ((start,_),p) in zip(gaps,parts):
                    blocks.extend(tuple(x+start for x in block) for block in p)
                answer.append(tuple(sorted(blocks)))
    return tuple(answer)

def noncrossing_arcs(p):
    arcs = [(b[i], b[i+1]) for b in p for i in range(len(b)-1)]
    return not any(a<c<b<d or c<a<d<b for (a,b),(c,d) in combinations(arcs,2))

@lru_cache(None)
def complement(p):
    n = sum(map(len,p))
    predecessor = {}
    for block in p:
        predecessor.update((block[j],block[j-1]) for j in range(len(block)))
    # Compose the cyclic successor with the block predecessor.
    k = {i:predecessor[(i+1)%n] for i in range(n)}
    unseen = set(range(n)); blocks=[]
    while unseen:
        start = min(unseen); block=[]; x=start
        while x in unseen:
            unseen.remove(x); block.append(x); x=k[x]
        blocks.append(tuple(sorted(block)))
    return tuple(sorted(blocks))

@lru_cache(None)
def geometric_complement(p):
    n = sum(map(len,p))
    doubled = tuple(tuple(2*x for x in block) for block in p)
    possibilities = [q for q in nc(n) if noncrossing_arcs(doubled + tuple(tuple(2*x+1 for x in block) for block in q))]
    least = min(map(len,possibilities))
    coarsest = [q for q in possibilities if len(q)==least]
    assert len(coarsest)==1
    return coarsest[0]

@lru_cache(None)
def words(s,N):
    return tuple(w for n in range(1,N+1) for w in product(range(s),repeat=n))

def at_partition(f,w,p):
    return prod(f.get(tuple(w[i] for i in b),0) for b in p)

def box(f,g,s,N,m=None):
    out={}
    for w in words(s,N):
        x=sum(at_partition(f,w,p)*at_partition(g,w,complement(p)) for p in nc(len(w)))
        out[w] = x%m if m else x
    return out

def identity(s,N):
    return {w:int(len(w)==1) for w in words(s,N)}

def reciprocal(x,m=None):
    return pow(x,-1,m) if m else Q(1,x)

def inv(f,s,N,m=None,left=False):
    r={}
    for w in words(s,N):
        if len(w)==1:
            r[w]=reciprocal(f[w],m); continue
        total=0
        for p in nc(len(w)):
            if (len(p)==1 if left else len(p)==len(w)):
                continue
            total += at_partition(r,w,p)*at_partition(f,w,complement(p)) if left else at_partition(f,w,p)*at_partition(r,w,complement(p))
        x=-total*reciprocal(prod(f[(i,)] for i in w),m)
        r[w]=x%m if m else x
    return r

# Polynomial monomials are sorted tuples of word-valued generator labels.
def mono(ws):
    return tuple(sorted(ws))

def pmul(a,b):
    out=Counter()
    for x,v in a.items():
        for y,w in b.items():
            out[mono(x+y)] += v*w
    return {x:v for x,v in out.items() if v}

@lru_cache(None)
def delta_generator(w,normalized=True):
    out=Counter()
    for p in nc(len(w)):
        factors=[]
        for q in (p,complement(p)):
            factors.append(mono(tuple(w[i] for i in b) for b in q if not normalized or len(b)>1))
        out[tuple(factors)] += 1
    return dict(out)

@lru_cache(None)
def delta_monomial(a,normalized=True):
    out={((),()):1}
    for w in a:
        nxt=Counter()
        for (l,r),v in out.items():
            for (ll,rr),vv in delta_generator(w,normalized).items():
                nxt[(mono(l+ll),mono(r+rr))] += v*vv
        out=dict(nxt)
    return out

def coassociativity(w,normalized):
    lhs=Counter();rhs=Counter()
    for (a,b),c in delta_generator(w,normalized).items():
        for (x,y),v in delta_monomial(a,normalized).items():
            lhs[(x,y,b)] += c*v
        for (x,y),v in delta_monomial(b,normalized).items():
            rhs[(a,x,y)] += c*v
    return lhs,rhs

def basis(s,d):
    gens=[w for w in words(s,d+1) if len(w)>1]
    layers={0:{()}}
    for weight in range(1,d+1):
        layer=set()
        for w in gens:
            k=len(w)-1
            for a in layers.get(weight-k,set()):
                layer.add(mono(a+(w,)))
        layers[weight]=layer
    return sorted(set.union(*layers.values()),key=lambda a:(sum(len(w)-1 for w in a),a))

def matrix(u,s,d):
    bs=basis(s,d); index={a:i for i,a in enumerate(bs)}; out={}
    for j,a in enumerate(bs):
        for (b,c),v in delta_monomial(a).items():
            value=v*prod(u[w] for w in c)
            if value:
                out[(index[b],j)]=out.get((index[b],j),0)+value
    return bs,{k:v for k,v in out.items() if v}

def matmul(a,b):
    byrow=defaultdict(list); out=Counter()
    for (i,j),x in b.items():byrow[i].append((j,x))
    for (i,k),x in a.items():
        for j,y in byrow[k]:out[(i,j)]+=x*y
    return {k:v for k,v in out.items() if v}

def scalar_multiply(a,b,N):
    return [sum(a[j]*b[n-j] for j in range(n+1)) for n in range(N+1)]

def scalar_compose(f,g,N):
    ans=[Q(0)]*(N+1); power=[Q(1)]+[Q(0)]*N
    for n in range(N+1):
        for j in range(N+1):ans[j]+=f[n]*power[j]
        power=scalar_multiply(power,g,N)
    return ans

def classical_transform(f,N):
    seq=[Q(0)]+[Q(f[(0,)*n]) for n in range(1,N+1)]
    inverse=[Q(0)]*(N+1)
    for n in range(1,N+1):
        inverse[n] = ((1 if n==1 else 0)-scalar_compose(seq,inverse,N)[n])/seq[1]
    return inverse[1:]

def run():
    counts=Counter(); details={};rng=random.Random(64120002720)
    def check(label,condition):
        assert condition,label
        counts[label]+=1
    for n in range(1,8):
        check('catalan_root_block_enumeration',len(nc(n))==comb(2*n,n)//(n+1))
        for p in nc(n):
            check('kreweras_rotation',complement(complement(p))==tuple(sorted(tuple(sorted((i-1)%n for i in b)) for b in p)))
            if n<=6:
                check('geometric_right_complement',complement(p)==geometric_complement(p))
    symbol_sizes={}
    for normalized in (False,True):
        for n in range(1,7):
            left,right=coassociativity(tuple(range(n)),normalized)
            check('universal_integer_coassociativity',left==right)
            symbol_sizes[f'{"normalized" if normalized else "full"}_degree_{n}']=len(left)
    details['distinct_label_symbolic_terms']=symbol_sizes
    for m in (None,2,3,4,6,8,9,12):
        s,N=2,4;e=identity(s,N)
        for trial in range(3):
            fs=[]
            for _ in range(3):
                f={w:rng.randrange(m) if m else Q(rng.randrange(-4,5)) for w in words(s,N)}
                us=[a for a in range(m) if gcd(a,m)==1] if m else [Q(-3),Q(-1),Q(2),Q(4)]
                for i in range(s):f[(i,)]=rng.choice(us)
                fs.append(f)
            f,g,h=fs
            right,left=inv(f,s,N,m),inv(f,s,N,m,True)
            check('separate_left_right_inverse_recursions',left==right)
            check('two_sided_inverse',box(f,right,s,N,m)==e==box(left,f,s,N,m))
            check('associativity_rings',box(box(f,g,s,N,m),h,s,N,m)==box(f,box(g,h,s,N,m),s,N,m))
            def normalize(v):
                return {w:(v[w]*prod(reciprocal(v[(i,)],m) for i in w))%m if m else v[w]*prod(reciprocal(v[(i,)]) for i in w) for w in words(s,N)}
            t={w:f[w] if len(w)==1 else 0 for w in words(s,N)}
            check('central_torus_nonuniform_units',box(t,g,s,N,m)==box(g,t,s,N,m))
            check('normalization_recovery',box(t,normalize(f),s,N,m)==f)
            check('normalization_homomorphism',normalize(box(f,g,s,N,m))==box(normalize(f),normalize(g),s,N,m))
            if trial==0:
                def full_matrix(v):
                    _,a=matrix(normalize(v),s,2)
                    out={(i,i):v[(i,)] for i in range(s)}
                    out.update({(i+s,j+s):x for (i,j),x in a.items()})
                    return {k:x%m for k,x in out.items() if x%m} if m else out
                actual=matmul(full_matrix(f),full_matrix(g))
                if m:actual={k:x%m for k,x in actual.items() if x%m}
                check('full_group_block_representation',actual==full_matrix(box(f,g,s,N,m)))
            radial_coeff={n:rng.randrange(5) for n in range(1,N+1)}
            radial={w:radial_coeff[len(w)]%(m or 10**9) for w in words(s,N)}
            check('radial_semigroup_centrality',box(radial,g,s,N,m)==box(g,radial,s,N,m))
            comm=box(box(box(f,g,s,N,m),right,s,N,m),inv(g,s,N,m),s,N,m)
            check('commutator_pure_word_obstruction',all(comm[(i,)*n]==int(n==1) for i in range(s) for n in range(1,N+1)))
    # Nonzero is not enough over a ring: 2 in Z/4Z cannot have a reciprocal.
    check('nonunit_mean_obstruction',all((2*x)%4!=1 for x in range(4)))
    s,N=2,4;e=identity(s,N);f=e.copy();g=e.copy();f[(0,0)]=1;g[(0,1)]=1
    fg=box(f,g,s,N);gf=box(g,f,s,N)
    check('order_sensitive_word',fg[(0,1,0)]==1 and gf[(0,1,0)]==0)
    sizes={}
    for d in (1,2,3):
        bs,a=matrix(f,s,d);_,b=matrix(g,s,d);_,ab=matrix(fg,s,d);_,ba=matrix(gf,s,d)
        check('right_translation_multiplication_order',matmul(a,b)==ab)
        check('right_translation_opposite_order',matmul(b,a)==ba)
        check('upper_unitriangular',all(a.get((j,j))==1 for j in range(len(bs))) and all(i<=j for i,j in a))
        check('coefficient_recovery',all(a.get((0,bs.index((w,))),0)==f[w] for w in words(s,d+1) if len(w)>1))
        if d>=2:
            j=bs.index(((0,1,0),))
            check('wrong_order_is_detected',ab.get((0,j),0)==1 and ba.get((0,j),0)==0)
        if d>1:
            prior_bs,prior=matrix(f,s,d-1)
            check('compatible_restrictions',{k:v for k,v in a.items() if k[1]<len(prior_bs)}==prior)
        sizes[d]=len(bs)
    details['matrix_dimensions']=sizes
    # Faithfulness detects a single arbitrary top-degree coefficient, unlike the prior quotient.
    for s,N in ((1,5),(2,4),(3,3)):
        e=identity(s,N);h=e.copy();w=tuple(i%s for i in range(N));h[w]=7
        _,low=matrix(h,s,N-2);_,low_e=matrix(e,s,N-2)
        bs,high=matrix(h,s,N-1);_,high_e=matrix(e,s,N-1)
        check('sharp_degree_detection',low==low_e and high!=high_e and high[(0,bs.index((w,))) ]==7)
    # Classical transform: literal scalar compatibility is a separate encoding, not equality of matrices.
    for _ in range(5):
        N=6
        f={(0,)*n:Q(rng.randrange(-3,4)) for n in range(1,N+1)}
        g={(0,)*n:Q(rng.randrange(-3,4)) for n in range(1,N+1)}
        f[(0,)]=Q(2);g[(0,)]=Q(-3)
        sf,sg=classical_transform(f,N),classical_transform(g,N)
        check('classical_scalar_transform',classical_transform(box(f,g,1,N),N)==scalar_multiply(sf,sg,N-1))
    # A degree-three pure coefficient distinguishes F^3 from the derived subgroup.
    z=identity(2,3);z[(0,0,0)]=1
    check('additional_source_derived_subgroup_counterexample',all(z[w]==0 for w in words(2,2) if len(w)==2) and z[(0,0,0)]!=0)
    details['additional_source_correction']='Example 6.1 of arXiv:1309.6194v1 claims [U_2,U_2]=F^3. Pure-variable projection disproves this.'
    return {'passed':True,'assertions':sum(counts.values()),'seed':64120002720,'assertion_groups':dict(counts),'details':details,'limits':'Finite exact controls supplement the independent mathematical audit. They do not establish all-degree results or historical priority.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
