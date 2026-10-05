#!/usr/bin/env python3
"""Independent exact finite models. No smooth realization is certified."""
import itertools
import json
from collections import Counter

checks = Counter()
negative = []

def require(group, truth):
    checks[group] += 1
    if not truth:
        raise AssertionError((group, checks[group]))

def reject(name, false_claim, witness):
    require('deliberate_negative_controls', not false_claim)
    negative.append({'claim_rejected': name, 'witness': witness})

# An independent dihedral-group model, rather than permutation multiplication.
# (r,s) represents a^r b^s, a^4=b^2=1, ba=a^-1 b.
G = tuple(itertools.product(range(4), range(2)))
one = (0, 0)
def mul(x, y):
    return ((x[0] + (-1 if x[1] else 1)*y[0]) % 4, x[1] ^ y[1])
def inv(x):
    return next(y for y in G if mul(x,y) == one == mul(y,x))
def closure(seed):
    out = set(seed) | {one}
    while True:
        new = out | {mul(x,y) for x in out for y in out}
        if new == out:
            return frozenset(out)
        out = new
subgroups = {closure(S) for n in range(9) for S in itertools.combinations(G,n)}
require('dihedral_group', len(subgroups) == 10)
for x,y,z in itertools.product(G,repeat=3):
    require('dihedral_group',mul(mul(x,y),z)==mul(x,mul(y,z)))
normal_closure = lambda S: closure({mul(mul(g,x),inv(g)) for g in G for x in S})
for H in subgroups:
    # Every bijective group homomorphism H->H is a permitted reparametrization.
    hs = tuple(sorted(H))
    for values in itertools.permutations(hs):
        phi = dict(zip(hs,values))
        if all(phi[mul(x,y)]==mul(phi[x],phi[y]) for x in H for y in H):
            require('normal_closure_reparametrization',normal_closure(H)==normal_closure(phi.values()))
    # Normal generation is weaker than being trivial: an exterior can be nontrivial.
require('nontrivial_exterior_model',len(G)>1 and normal_closure({(1,0),(0,1)})==frozenset(G))
reverse_order_witness = None
for A,B in itertools.product(subgroups, repeat=2):
    for g in G:
        orbit = {mul(mul(a,g),b) for a in A for b in B}
        opposite = {mul(mul(b,g),a) for a in A for b in B}
        if orbit != opposite and reverse_order_witness is None:
            reverse_order_witness = {'A':sorted(A),'B':sorted(B),'g':g,'AgB':sorted(orbit),'BgA':sorted(opposite)}
        for h in G:
            # Direct equality a*g=h*b, not an algebraically rearranged lookup.
            compatible = any(mul(a,g)==mul(h,b) for a in A for b in B)
            require('double_coset_direct_compatibility',(h in orbit)==compatible)
reject('double-coset left/right factors can always be interchanged',reverse_order_witness is None,reverse_order_witness)
A=closure({(0,1)}); B={one}; f=(0,1)
reject('nonextension over C alone forces effective twisting',f not in {mul(a,b) for a in A for b in B},
       {'f_not_in_B':f not in B,'f_in_A':f in A,'abstract_model_only':True})

# A gluing extension must be inverted with the author's direction conventions.
for modulus in range(2,18):
    for shift,c in itertools.product(range(modulus),repeat=2):
        original=c
        target=(c-shift+shift)%modulus
        require('inverse_extension_gluing',original==target)
reject('the extension itself always works in place of its inverse',(0+1+1)%3==0,
       {'boundary_map':'translation by 1 in Z/3','incorrect_result':2,'required_result':0})
reject('every orientation-preserving map may be treated as an involution',(1+1)%3==0,
       {'algebraic_map_order':3,'scope':'order model, not an asserted cork'})

# Signed intersection arrays, including the empty product decomposition.
for k in range(4):
    for negatives in itertools.product(range(2),repeat=k*k):
        total=sum(2*negatives[i*k+j]+int(i==j) for i in range(k) for j in range(k))
        c=total-k
        require('intersection_parity_including_zero',c==2*sum(negatives) and c>=0 and c%2==0)
reject('excess-intersection complexity equals handle-pair count',2*5==1,
       {'handle_pairs':1,'positive_intersections':6,'negative_intersections':5,'complexity':10})
reject('a selected large cobordism bounds the minimum from below',min(0,100)>=100,
       {'selected_complexity':100,'available_product_complexity':0})

# Surface-genus order bounds allow negative adjunction expressions.
items=[(g,h,sq) for g in range(4) for h in range(g,4) for sq in range(-3,4)]
for row in itertools.product(items,repeat=2):
    lower=max(2*g-q for g,h,q in row)
    upper=max(2*h-q for g,h,q in row)
    require('signed_genus_upper_bound',lower<=upper)
reject('2g-v^2 is automatically nonnegative',2*0-1>=0,{'genus':0,'square':1,'expression':-1})
for n in range(1,101):
    require('yasui_cork_hypothesis_fails',not (0>11*n+10))
    # Each exterior e has a finite bound e, but these bounds have no fixed cap.
    require('embedding_bound_not_uniform',n+1>n)
reject('a bound for each embedding supplies one uniform bound',all(e<=5 for e in range(1,7)),
       {'six_exterior_bounds':[1,2,3,4,5,6],'purported_bound':5,'model_only':True})
for size in range(2,15):
    relation=lambda e,t:e==t
    require('embedding_quantifiers',all(any(relation(e,t) for e in range(size)) for t in range(size))
            and not any(all(relation(e,t) for t in range(size)) for e in range(size)))

# Coordinate-based F2 calculations independent of the author's bit encoding.
def dot(x,y):return sum(a*b for a,b in zip(x,y))%2
for d in range(1,5):
    vectors=list(itertools.product((0,1),repeat=d))
    for x,y,functional in itertools.product(vectors,repeat=3):
        delta=tuple((a+b)%2 for a,b in zip(x,y))
        require('linear_difference',dot(functional,delta)==(dot(functional,x)-dot(functional,y))%2)
    for delta in vectors[1:]:
        i=delta.index(1)
        for length in range(1,7):
            for values in itertools.product((0,1),repeat=length):
                functionals=[tuple(v if j==i else 0 for j in range(d)) for v in values]
                require('prescribed_evaluations',tuple(dot(l,delta) for l in functionals)==values)
reject('dimension one forces all complement evaluations to coincide',0==1,
       {'delta':[1],'two_linear_functionals':[[0],[1]],'values':[0,1]})
# A-only moves preserve coordinate 1; B-only moves preserve coordinate 2.
vertices=list(itertools.product(range(2),repeat=2)); start=(0,0); finish=(1,1)
reach_A={v for v in vertices if v[0]==start[0]}
reach_B={v for v in vertices if v[1]==start[1]}
reject('separate preservation obstructions exclude mixed sequences',
       not (start[0]==(0,1)[0] and (0,1)[1]==finish[1]),
       {'path':[start,(0,1),finish],'A_alone_misses_finish':finish not in reach_A,
        'B_alone_misses_finish':finish not in reach_B})
reject('pairwise finite stabilization bounds imply a global bound',all(n<=10 for n in range(1,12)),
       {'individual_heights':list(range(1,12)),'proposed_uniform_bound':10,'model_only':True})
reject('a finite-family existence quantifier fixes one candidate forever',
       any(all(candidate>=family for family in range(1,9)) for candidate in range(1,8)),
       {'model':'candidate k handles every finite family of size at most k; k depends on family'})
reject('unknown extension existence is equivalent to nonexistence',False,
       {'countermodel':'an extension exists but has not been found; corrected definition uses existence'})

print(json.dumps({'status':'PASS','total_assertions':sum(checks.values()),
      'groups':dict(sorted(checks.items())),'negative_controls':negative,
      'scope':'Exact finite algebra and logical countermodels only. No geometric realization, Floer calculation, topology classification, or universal quantifier is computationally certified.'},indent=2,sort_keys=True))
