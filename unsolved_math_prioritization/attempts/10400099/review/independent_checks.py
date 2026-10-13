#!/usr/bin/env python3
"""Exact independent finite-quandle and braid controls; no floating logarithms."""
from collections import Counter
from itertools import product
from math import gcd,comb
import json
checks=Counter()
def ok(v,k):
    assert v,k
    checks[k]+=1

def braid(colors,word,q,t):
    c=list(colors);inv=pow(t,-1,q) if q>1 else 0
    for letter in word:
        i=abs(letter)-1;a,b=c[i:i+2]
        if letter>0:c[i:i+2]=[b,(t*a+(1-t)*b)%q]
        else:c[i:i+2]=[(inv*b+(1-inv)*a)%q,a]
    return tuple(c)

def count(q,t,n,word):
    return sum(braid(c,word,q,t)==c for c in product(range(q),repeat=n))

# Dihedral and non-involutory connected Alexander examples, plus a singleton.
models=[(1,0),(3,2),(5,4),(7,6),(5,2),(7,2),(7,3)]
for q,t in models:
    op=lambda a,b:(t*a+(1-t)*b)%q
    for a in range(q):ok(op(a,a)==a,'idempotent_constant_colors')
    for b in range(q):ok(len({op(a,b) for a in range(q)})==q,'right_translations_bijective')
    for a,b,c in product(range(q),repeat=3):
        ok(op(op(a,b),c)==op(op(a,c),op(b,c)),'quandle_self_distributivity')
    if q>1:
        ok(gcd(1-t,q)==1,'connected_Alexander_parameter')
        if t*t%q!=1:ok(any(op(op(a,b),b)!=a for a,b in product(range(q),repeat=2)),'non_involutory_negative_crossing_control')
    for c in product(range(q),repeat=3):
        for i in (1,2):
            ok(braid(c,[i,-i],q,t)==c and braid(c,[-i,i],q,t)==c,'positive_negative_inverse_propagation')
        ok(braid(c,[1,2,1],q,t)==braid(c,[2,1,2],q,t),'braid_relation')
    for c in range(q):
        ok(braid((c,c,c),[1,-2,1,2,-1],q,t)==(c,c,c),'constant_colors_survive_mixed_braid')
    ok(count(q,t,1,[])==q,'unknot_count')
    for word in ([1],[1,1,1],[-1,-1,-1],[1,-2,1,-2],[1,2],[1,2]*4,[1,-2,2,-1]):
        n=2 if max(map(abs,word))==1 else 3
        h=count(q,t,n,word)
        ok(q<=h<=q**n,'closure_color_bound')

for q in range(2,10):
    for m in range(-15,16):
        word=[1 if m>=0 else -1]*abs(m)
        h=count(q,q-1,2,word)
        ok(h==q*gcd(q,m),'dihedral_two_braid_count_all_signs')

# Finite differences are additive, also for a real scalar times these sequences.
for degree in range(9):
    for z in range(-5,6):
        s=sum((-1)**(degree+1-j)*comb(degree+1,j)*(z+j)**degree for j in range(degree+2))
        ok(s==0,'polynomial_finite_difference')
# For R3 on T(2,2z+1), log(count)/log(3) is the nonconstant period-three sequence.
a=[1+int((2*z+1)%3==0) for z in range(3)]
for r in range(1,16):
    a=[a[(i+1)%3]-a[i] for i in range(3)]
    ok(any(a),'nonconstant_periodic_log_sequence_difference')
# Normalization by q subtracts a constant, which has zero positive differences.
for r in range(1,10):
    ok(sum((-1)**(r-j)*comb(r,j) for j in range(r+1))==0,'constant_log_normalization_shift')

print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'Alexander_quandles':[{'q':q,'t':t} for q,t in models],
 'scope':'Finite exact quandle, inverse-braid and finite-difference controls. The all-knot conclusion uses the written universal bound and Eisermann\'s published theorem.'},indent=2,sort_keys=True))
