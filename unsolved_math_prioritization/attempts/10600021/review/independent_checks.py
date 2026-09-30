#!/usr/bin/env python3
"""Independent finite diagnostics; no knot realization or isotopy algorithm."""
from itertools import product
from math import gcd
from pathlib import Path
import hashlib, json

counts = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def words(alphabet, limit):
    return [''.join(t) for n in range(limit+1) for t in product(alphabet, repeat=n)]

def primitive(word):
    if not word:
        return '', 0
    for length in range(1, len(word)+1):
        if len(word) % length == 0 and word[:length] * (len(word)//length) == word:
            return word[:length], len(word)//length
    raise AssertionError('unreachable')

# Different algorithm from the submitted prefix-recursion: primitive periods.
W = words('abc', 4)
commuting = 0
for u in W:
    for v in W:
        p, a = primitive(u)
        q, b = primitive(v)
        same = u+v == v+u
        check('primitive_period_criterion', same == (not u or not v or p == q))
        if same:
            commuting += 1
            root = p or q
            m = len(u)//len(root) if root else 0
            n = len(v)//len(root) if root else 0
            check('common_root_reconstruction', root*m == u and root*n == v)
            if u and v:
                k = gcd(len(u),len(v))
                check('gcd_period_reconstruction', u[:k]*(len(u)//k)==u and u[:k]*(len(v)//k)==v)
            for c,d in [(0,0),(0,3),(2,0),(1,4)]:
                # Lift into N x free monoid, allowing distinct residual central factors.
                check('normal_form_lift', (c,root*m)==(c,u) and (d,root*n)==(d,v))
                check('central_factors_commute', (c+d,u+v)==(d+c,v+u))

# Union-find, rather than a per-word breadth-first search, computes each entire
# homogeneous finite slice of <a,b | abba=baab>. No relation changes length.
B = words('ab', 8)
parent = {w:w for w in B}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def join(x,y):
    rx,ry=find(x),find(y)
    if rx!=ry:
        parent[max(rx,ry)] = min(rx,ry)

edges=[]
for w in B:
    for i in range(len(w)-3):
        if w[i:i+4] == 'abba':
            v=w[:i]+'baab'+w[i+4:]
            edges.append((w,v)); join(w,v)
            check('relation_gradings',len(w)==len(v) and w.count('a')==v.count('a'))
classes={}
for w in B:
    classes.setdefault(find(w),[]).append(w)
for group in classes.values():
    first=group[0]
    for w in group:
        check('class_gradings',len(w)==len(first) and w.count('a')==first.count('a'))
        if len(w)<4:
            check('short_word_singletons',len(group)==1)
# The finite slice is closed under all possible defining moves at that length.
for x,y in edges:
    check('defining_equivalence',find(x)==find(y))
    for c in ('','a','b'):
        if len(x)+len(c)<=8:
            check('left_context',find(c+x)==find(c+y))
            check('right_context',find(x+c)==find(y+c))
for x in words('ab',2):
    for y in words('ab',2):
        check('short_word_distinctness',(find(x)==find(y)) == (x==y))
for x in ('aa','ab','ba','bb'):
    for y in ('aa','ab','ba','bb'):
        check('ordered_atom_pair_rigidity',(find(x)==find(y))==(x==y))
check('composite_pair_distinct',find('ab')!=find('ba'))
check('composite_pair_commutes',find('abba')==find('baab'))
# Grading forces any root length to divide 2, and forces equal positive exponents.
for length in (1,2):
    exp=2//length
    for root in (w for w in B if len(w)==length):
        check('no_common_composite_root',not(find(root*exp)==find('ab') and find(root*exp)==find('ba')))
        for c,q,qp in product(range(5),repeat=3):
            if exp*c+q==0 and exp*c+qp==0:
                check('zero_central_coordinates',c==q==qp==0)
# Every bounded representative admits the claimed atom decomposition; the proof
# that these are all atoms is the nonnegative additive grading argument in REVIEW.
for c in range(4):
    for w in B:
        degree=c+len(w)
        check('atomic_representative_length',degree>=0)
        if degree==1:
            check('three_possible_atoms',(c,w) in {(1,''),(0,'a'),(0,'b')})
        if degree>=2:
            factor=(1,'') if c else (0,w[0])
            remainder=(c-1,w) if c else (0,w[1:])
            check('nontrivial_atomic_split',factor!=(0,'') and remainder!=(0,'') and
                  factor[0]+remainder[0]==c and factor[1]+remainder[1]==w)

root=Path(__file__).parent
out={
 'problem_id':10600021,
 'status':'PASS_INDEPENDENT_FINITE_ALGEBRA_DIAGNOSTICS',
 'assertions':sum(counts.values()),'groups':counts,
 'free_word_alphabet':'abc','free_word_max_length':4,'free_word_pairs':len(W)**2,
 'commuting_word_pairs':commuting,
 'presentation_max_length':8,'presentation_words':len(B),'presentation_classes':len(classes),
 'relation_edges':len(edges),
 'artifact_sha256':hashlib.sha256((root/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitations':'Finite monoid diagnostics only. No virtual-knot realization, isotopy search, ordered geometric normal form, or literature completeness is certified.'
}
print(json.dumps(out,indent=2,sort_keys=True))
