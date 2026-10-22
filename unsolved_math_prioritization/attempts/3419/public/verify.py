#!/usr/bin/env python3
"""Exact finite consistency checks. These do not resolve OPG-37237."""
import itertools as it
import json
import random
from collections import Counter
from fractions import Fraction

checks = Counter()
def check(name, value):
    assert value, name
    checks[name] += 1

def rank(rows):
    if not rows:
        return 0
    a = [list(map(Fraction, row)) for row in rows]
    r = 0
    for c in range(len(a[0])):
        p = next((j for j in range(r, len(a)) if a[j][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for j in range(len(a)):
            if j != r:
                v = a[j][c]
                a[j] = [x-v*y for x,y in zip(a[j],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def det(rows):
    if not rows:
        return Fraction(1)
    a = [list(map(Fraction, row)) for row in rows]
    out = Fraction(1)
    for c in range(len(a)):
        p = next((j for j in range(c, len(a)) if a[j][c]), None)
        if p is None:
            return Fraction(0)
        if p != c:
            a[p],a[c] = a[c],a[p]
            out *= -1
        v=a[c][c]
        out *= v
        for j in range(c+1,len(a)):
            ratio=a[j][c]/v
            for k in range(c,len(a)):
                a[j][k] -= ratio*a[c][k]
    return out

# General-purpose exact linear algebra is only checking displayed maps.
check('universal_construction_matrix', det([[1,1],[-1,0]]) == 1)
for x,y in it.product(range(-12,13),repeat=2):
    a,b=-y,x+y
    check('universal_construction_inverse', (a+b,-a)==(x,y))
check('gamma1_matrix_rank',rank([[3,0,3,0],[0,-3,0,-3]])==2)
check('single_s_matrix_rank',rank([[3,0],[0,-3]])==2)
gamma1_b2=4-2
gamma2_b2_lower=gamma1_b2+(5-2)
gamma3_b2_lower=gamma2_b2_lower+2
gamma4_b2_lower=gamma3_b2_lower
edge_a_b2=0+1+2
edge_c_b2=2
gamma5_b2_lower=gamma4_b2_lower-edge_a_b2
gamma6_b2_lower=gamma5_b2_lower-edge_c_b2
check('homology_lower_bound', [gamma1_b2,gamma2_b2_lower,gamma3_b2_lower,gamma4_b2_lower,gamma5_b2_lower,gamma6_b2_lower]==[2,5,7,7,4,2])

# Every labelled tree on <=6 vertices, via Pruefer codes; labels in this
# enumeration mean vertex names, not the arbitrary conjugating words.
def tree(n,code):
    if n == 1:
        return []
    degrees=[1]*n
    for v in code: degrees[v]+=1
    edges=[]
    for v in code:
        u=next(i for i,d in enumerate(degrees) if d==1)
        edges.append((u,v))
        degrees[u]-=1;degrees[v]-=1
    u,v=[i for i,d in enumerate(degrees) if d==1]
    return edges+[(u,v)]

trees=0
for n in range(1,7):
    for code in it.product(range(n),repeat=max(n-2,0)):
        edges=tree(n,code)
        mat=[[int(j==v)-int(j==u) for u,v in edges] for j in range(n)]
        check('tree_incidence_rank',rank(mat)==n-1)
        for root in range(n):
            check('tree_incidence_unimodular_minor',abs(det([row for j,row in enumerate(mat) if j!=root]))==1)
        trees+=1

# Proposition 4 base group: (r,n) encodes b^r a^n.
def mul(g,h):
    r,n=g;s,m=h
    return ((r+(1 if n%2==0 else -1)*s)%3,n+m)
def inv(g):
    r,n=g
    return ((-(1 if n%2==0 else -1)*r)%3,-n)
I=(0,0)
base=list(it.product(range(3),range(-3,4)))
for g in base:
    check('base_inverse',mul(g,inv(g))==I==mul(inv(g),g))
for g,h,k in it.product(base,repeat=3):
    check('base_associativity',mul(mul(g,h),k)==mul(g,mul(h,k)))

def wp(word):
    """Britton pinch reduction; a,A,b,B,t,T are generators/inverses."""
    blocks=[I];stable=[]
    atom={'a':(0,1),'A':(0,-1),'b':(1,0),'B':(2,0)}
    for x in word:
        if x in atom:
            blocks[-1]=mul(blocks[-1],atom[x])
        else:
            assert x in 'tT'
            stable.append(1 if x=='t' else -1)
            blocks.append(I)
    while True:
        found=False
        for j in range(len(stable)-1):
            r,n=blocks[j+1]
            if r or stable[j+1]!=-stable[j]:
                continue
            if stable[j]==1:
                replacement=(0,2*n)
            elif n%2==0:
                replacement=(0,n//2)
            else:
                continue
            merged=mul(mul(blocks[j],replacement),blocks[j+2])
            blocks[j:j+3]=[merged]
            stable[j:j+2]=[]
            found=True
            break
        if not found:
            return not stable and blocks[0]==I

def inverse_word(w):
    return w.swapcase()[::-1]
# aba^-1=b^-1 is a b A b.
relators=['taTAA','abAb','bbb']
for rel in relators:
    check('hnn_relators',wp(rel))
for w in ['', 'aA','bB','tT','Tt','tbaABT','Taa t'.replace(' ', '')+'A']:
    check('hnn_inverse_controls',wp(w+inverse_word(w)))
for w in ['a','b','t','T','tbT','Tbt','T a t'.replace(' ', '')]:
    check('hnn_nontrivial_controls',not wp(w))
for r,n in it.product(range(3),range(-30,31)):
    w='b'*r+('a'*n if n>=0 else 'A'*(-n))
    check('hnn_base_agreement',wp(w)==((r,n)==I))

rng=random.Random(3419)
alphabet='aAbBtT'
for _ in range(5000):
    w=''.join(rng.choice(alphabet) for __ in range(rng.randrange(15)))
    v=''.join(rng.choice(alphabet) for __ in range(rng.randrange(8)))
    r=rng.choice(relators)
    insertion=v+r+inverse_word(v)
    pos=rng.randrange(len(w)+1)
    check('hnn_relator_insertion',wp(w)==wp(w[:pos]+insertion+w[pos:]))
    check('hnn_inverse_random',wp(w+inverse_word(w)))
    check('hnn_inversion_invariance',wp(w)==wp(inverse_word(w)))

# Finite permutation controls: enumerate representations into S_n, n<=5.
def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
reps={}
for n in range(1,6):
    ps=list(it.permutations(range(n)));identity=tuple(range(n));count=0
    invs={p:pinv(p) for p in ps}
    bs=[p for p in ps if compose(compose(p,p),p)==identity]
    for a in ps:
        a2=compose(a,a)
        valid_b=[b for b in bs if compose(compose(a,b),invs[a])==invs[b]]
        for t in ps:
            if compose(compose(t,a),invs[t])!=a2: continue
            for b in valid_b:
                check('finite_quotients_kill_b',b==identity)
                count+=1
    reps[str(n)]=count

out={
 'target':'3419 / OPG-37237',
 'result':'UNRESOLVED',
 'checks':dict(sorted(checks.items())),
 'total_assertions':sum(checks.values()),
 'labelled_trees_checked':trees,
 'permutation_representations_checked':reps,
 'gamma6_rational_h2_lower_bound':gamma6_b2_lower,
 'scope':'Finite consistency checks only. No target solution or mechanized topology claim.'
}
print(json.dumps(out,indent=2,sort_keys=True))
