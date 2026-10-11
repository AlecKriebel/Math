#!/usr/bin/env python3
"""Exact finite controls for Turn1. No claim to verify geometric realizations computationally."""
from itertools import product,combinations,permutations
from collections import Counter
import json

counts=Counter()
def check(condition,group):
    assert condition,group
    counts[group]+=1

def expand(word,degree=3,distinct=False):
    out={():1}
    for letter in word:
        label=abs(letter);sign=1 if letter>0 else -1
        if sign==1:factor={():1,(label,):1}
        else:factor={tuple([label]*j):(-1)**j for j in range(degree+1)}
        new=Counter()
        for a,c in out.items():
            for b,d in factor.items():
                w=a+b
                if len(w)<=degree and (not distinct or len(set(w))==len(w)):
                    new[w]+=c*d
        out={w:c for w,c in new.items() if c}
    return out

def ordered(word,I):
    ans=0
    for pos in combinations(range(len(word)),len(I)):
        if tuple(abs(word[p]) for p in pos)==I:
            v=1
            for p in pos:v*=1 if word[p]>0 else -1
            ans+=v
    return ans

def reduce_word(word):
    stack=[]
    for x in word:
        if stack and stack[-1]==-x:stack.pop()
        else:stack.append(x)
    return tuple(stack)

total_words=0
for length in range(8):
    for w in product((1,-1,2,-2),repeat=length):
        total_words+=1
        E=expand(w,degree=2)
        a=E.get((1,),0);b=E.get((2,),0)
        c=E.get((1,2),0);d=E.get((2,1),0)
        check(c+d==a*b,'integer_shuffle')
        check(c==ordered(w,(1,2)),'ordered_pairs')
        check(d==ordered(w,(2,1)),'ordered_pairs')
        check(E==expand(reduce_word(w),degree=2),'free_reduction')
        sw=tuple((2 if x>0 else -2) if abs(x)==1 else (1 if x>0 else -1) for x in w)
        F=expand(sw,degree=2)
        check(F.get((1,2),0)==d and F.get((2,1),0)==c,'label_exchange')

# A separate direct subsequence count checks the distinct-index expansion,
# including negative letters and the third degree.
triple_words=0
Ilist=[I for k in range(1,4) for I in permutations((1,2,3),k)]
for length in range(5):
    for w in product((1,-1,2,-2,3,-3),repeat=length):
        triple_words+=1
        E=expand(w,degree=3,distinct=True)
        for I in Ilist:
            check(E.get(I,0)==ordered(w,I),'distinct_ordered_tuples')
        for x in (1,-2,3):
            where=len(w)//2
            inserted=w[:where]+(x,-x)+w[where:]
            check(expand(inserted,degree=3,distinct=True)==E,'cut_tangency_cancellation')

for r in range(2,8):
    w=tuple(range(1,r+1));E=expand(w,degree=r,distinct=True)
    swapped=(2,1)+w[2:]
    check(E.get(w,0)==1,'point_push_examples')
    check(E.get(swapped,0)==0,'point_push_examples')
    check(all(E.get((i,),0)==1 for i in range(1,r+1)),'point_push_examples')

for a in range(-8,9):
    for b in range(-8,9):
        w=tuple(([1 if a>=0 else -1]*abs(a))+([2 if b>=0 else -2]*abs(b)))
        E=expand(w,degree=2)
        check(E.get((1,2),0)==a*b and E.get((2,1),0)==0,'power_family')

w=(1,2);v=(2,1)
check(reduce_word((-1,)+w+(1,))==v,'conjugate_closure_control')
check(expand(w,2).get((1,2),0)==1 and expand(v,2).get((1,2),0)==0,'conjugate_closure_control')
C=expand((1,2,-1,-2),2)
check(C.get((1,),0)==C.get((2,),0)==0,'vanishing_lower_control')
check(C.get((1,2),0)==1 and C.get((2,1),0)==-1,'vanishing_lower_control')
for integer_c in range(-128,129):
    check(2*integer_c!=1,'symmetric_integral_correction_obstruction')

print(json.dumps({'status':'PASS','arithmetic':'exact integer arithmetic only','assertions':sum(counts.values()),'groups':dict(sorted(counts.items())),'exhaustive_two_letter_words':total_words,'exhaustive_three_letter_words':triple_words,'scope':'Finite Magnus/ordered-intersection/shuffle identities and examples. Smooth point-pushing realization, conjugate braid closure isotopy, and surface-orientation arguments are written topology, not computationally certified. No full-target resolution is claimed.'},indent=2,sort_keys=True))
