#!/usr/bin/env python3
"""Exact finite controls only; the universal theorem is in PROOF.md."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json

counts={}
def check(ok,group):
    counts[group]=counts.get(group,0)+1
    if not ok: raise AssertionError((group,counts[group]))

def maximal_exponent(w):
    """For each factor start and period, extend to the first failed equality."""
    best=F(1) if w else F(0)
    N=len(w)
    for i in range(N):
        for d in range(1,N-i):
            j=i+d
            while j<N and w[j]==w[j-d]: j+=1
            best=max(best,F(j-i,d))
    return best

def brute_exponent(w):
    best=F(1) if w else F(0)
    for i in range(len(w)):
        for j in range(i+1,len(w)+1):
            z=w[i:j]
            for d in range(1,len(z)+1):
                if all(z[t]==z[t+d] for t in range(len(z)-d)):
                    best=max(best,F(len(z),d))
    return best

def morph(w,images): return tuple(c for x in w for c in images[x])

def matches(p,w):
    """Match whole w with nonempty images; different variables may agree."""
    def rec(k,j,images):
        if k==len(p): return j==len(w)
        a=p[k]
        if a in images:
            t=images[a]
            return w[j:j+len(t)]==t and rec(k+1,j+len(t),images)
        for end in range(j+1,len(w)+1):
            images[a]=w[j:end]
            if rec(k+1,end,images):
                del images[a]
                return True
        images.pop(a,None)
        return False
    return rec(0,0,{})

@lru_cache(None)
def contains(p,w):
    return any(matches(p,w[i:j]) for i in range(len(w)) for j in range(i+1,len(w)+1))

# Independent direct-period oracle for the optimized maximal-exponent routine.
for k,maxlen in [(2,7),(3,5)]:
    for l in range(maxlen+1):
        for w in product(range(k),repeat=l):
            check(maximal_exponent(w)==brute_exponent(w),'period_oracle')

# All nonempty proper truncations, with factors starting anywhere.
for s in range(2,12):
    for n in range(1,5):
        for r in range(1,s):
            w=tuple(range(s))*n+tuple(range(r))
            check(maximal_exponent(w)==F(n)+F(r,s),'distinct_cycle_formula')

examples=[]
for den in range(2,15):
    for num in range(1,den):
        delta=F(num,den)
        q=(den+(den-num)-1)//(den-num)
        r=q-1
        D=(r*den)//num+1
        check(q>=2 and 0<r<q<D,'construction_parameters')
        check(F(r,q)>=delta>F(r,D),'strict_threshold_crossing')
        for n in range(1,5):
            w=tuple(range(q))*n+tuple(range(r))
            images={i:(i,) for i in range(D)}
            images[q-1]=tuple(range(q-1,D))
            v=morph(w,images)
            check(all(images.values()) and all(c<D for z in images.values() for c in z),'same_alphabet_non_erasing')
            check(v==tuple(range(D))*n+tuple(range(r)),'exact_morphism_image')
            check(maximal_exponent(w)==F(n)+F(r,q),'input_all_factor_exponents')
            check(maximal_exponent(v)==F(n)+F(r,D),'output_all_factor_exponents')
            check(maximal_exponent(w)>=F(n)+delta>maximal_exponent(v),'bad_to_good')
            if n==1 and den in (2,3,10) and num in (1,den-1):
                examples.append(dict(alpha=str(F(n)+delta),q=q,r=r,D=D,input_exponent=str(F(n)+F(r,q)),output_exponent=str(F(n)+F(r,D))))

# Very small delta and delta close to one: exact integer arithmetic, not floats.
for den in [10,100,1000,10**12]:
    for num in [1,den-1]:
        q=(den+(den-num)-1)//(den-num);r=q-1;D=r*den//num+1
        check(F(r,q)>=F(num,den)>F(r,D) and D>q,'endpoint_parameter_arithmetic')

# Irrational examples are certified by rational brackets; no floats used.
# 7/5 < sqrt(2) < 3/2, so q=2,r=1,D=3 straddles it between4/3 and3/2.
check(F(4,3)**2<2<F(3,2)**2,'irrational_bracket')
# 11/5 < sqrt(5) < 9/4: q=2,r=1,D=5 crosses it between11/5 and5/2.
check(F(11,5)**2<5<F(5,2)**2,'irrational_bracket')

# Actual nonerasing substitutions preserve actual detected pattern factors.
patterns=[(0,0),(0,1,0),(0,1,0,1,0),(0,1,2)]
images_list=[(0,),(1,),(0,1),(1,0),(0,0),(1,1)]
for p in patterns:
    for l in range(1,6):
        for w in product(range(2),repeat=l):
            if contains(p,w):
                for a,b in product(images_list,repeat=2):
                    check(contains(p,morph(w,{0:a,1:b})),'pattern_occurrence_closure')

for l in range(9):
    for w in product(range(2),repeat=l):
        characterized=contains((0,0),w) or contains((0,1,2),w)
        for alpha in [F(101,100),F(4,3),F(3,2)]:
            check(characterized==(maximal_exponent(w)>=alpha),'binary_exception')
        for k in [2,3,4]:
            check(contains((0,)*k,w)==(maximal_exponent(w)>=k),'integer_boundary')
for den in range(2,10):
    for num in range(den+1,5*den):
        alpha=F(num,den);ceil_alpha=(num+den-1)//den
        for l in range(7):
            w=(0,)*l
            check(contains((0,)*ceil_alpha,w)==(maximal_exponent(w)>=alpha),'unary_exception')

check(maximal_exponent(tuple('ababa'))==F(5,2),'named_example')
check(maximal_exponent(tuple('abcabca'))==F(7,3),'named_example')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':counts,'sample_witnesses':examples,'floating_point_used':False,'scope':'Finite controls only; universal real-threshold proof in PROOF.md'},indent=2,sort_keys=True))
