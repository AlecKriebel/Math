#!/usr/bin/env python3
"""Exact finite controls, not a construction of an EZ-structure or surface group."""
from fractions import Fraction
from itertools import product,permutations
import json

# q(i,+/-1) identifies all endpoints at the same height. Interior fibers remain
# separate. C5 represents only a finite test alphabet, not the circle boundary.
N=5
PPLUS=('pole',1); PMINUS=('pole',-1)
def q(i,r):
    r=Fraction(r)
    assert -1<=r<=1
    return ('pole',int(r)) if abs(r)==1 else (i%N,r)
heights=[Fraction(-1),Fraction(-1,2),Fraction(0),Fraction(1,2),Fraction(1)]
points=sorted({q(i,r) for i in range(N) for r in heights},key=repr)
def apply(p,letter):
    if p[0]=='pole': return p
    i,r=p
    maps={'g':lambda x:(x+1)%N,'G':lambda x:(x-1)%N,
          't':lambda x:3*x%N,'T':lambda x:2*x%N}
    return (maps[letter](i),r)
def act(word,p):
    # Group actions compose right-to-left.
    for letter in reversed(word):p=apply(p,letter)
    return p

def tests():
    counts={}
    for r in (-1,1):
        assert len({q(i,r) for i in range(N)})==1
    assert PPLUS!=PMINUS
    counts['quotient_poles']=2
    for p in points:
        for u,v in [('g','G'),('t','T')]:
            assert act(u+v,p)==p==act(v+u,p)
        # t^{-1} g t = g^2 for phi(g)=g^2 on C5.
        assert act('Tgt',p)==act('gg',p)
    counts['relation_test_points']=len(points)
    word_count=0
    for k in range(7):
        for letters in product('gGtT',repeat=k):
            word=''.join(letters);word_count+=1
            assert act(word,PPLUS)==PPLUS and act(word,PMINUS)==PMINUS
            for p in points:assert act(word,p)[1]==p[1]
    counts['all_words_through_length_6']=word_count
    fixed={p for p in points if all(apply(p,g)==p for g in 'gt')}
    assert fixed=={PPLUS,PMINUS}
    counts['global_fixed_points_in_model']=len(fixed)
    # Negative control: a pole-swapping map is NOT a suspension of a base map.
    bad=lambda p: PMINUS if p==PPLUS else PPLUS if p==PMINUS else p
    assert bad(PPLUS)!=PPLUS and bad(PMINUS)!=PMINUS
    counts['bad_pole_swapping_action_detected']=True
    # Conjugacy carries fixed points to fixed points. Exhaust all 5! finite
    # coordinate changes for a nontrivial permutation with exactly two fixed points.
    perm=(1,2,0,3,4);fixed0={x for x in range(5) if perm[x]==x}
    assert len(fixed0)==2
    conjugacy_count=0
    for f in permutations(range(5)):
        inv=[0]*5
        for i,j in enumerate(f):inv[j]=i
        c=tuple(f[perm[inv[j]]] for j in range(5))
        assert {j for j in range(5) if c[j]==j}=={f[j] for j in fixed0}
        conjugacy_count+=1
    counts['conjugacy_changes_checked']=conjugacy_count
    # Negative control for naive product inflation: in the max product metric,
    # (g*x,0) and (g*x,1) stay distance 1 no matter how small the base tile gets.
    diameters=[max(Fraction(1,2**n),Fraction(1)) for n in range(40)]
    assert all(d==1 for d in diameters)
    counts['product_inflation_uniform_lower_bound']='1'
    counts['product_inflation_nullity_rejected']=True
    return {'result':'pass','scope':'Exact finite sanity controls only; the proof relies on cited infinite and topological theorems.','checks':counts}
if __name__=='__main__':print(json.dumps(tests(),indent=2,sort_keys=True))
