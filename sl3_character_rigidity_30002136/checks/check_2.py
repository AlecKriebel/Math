#!/usr/bin/env python3
"""Exact sanity checks for the low-minority-letter lemma, not its proof.
No sampling or probabilistic identity tests. Only Python stdlib is required.
"""
from itertools import product
from collections import Counter
from fractions import Fraction
import json

# Laurent polynomials: exponent tuple -> integer coefficient.
def add(p,q):
    r=p.copy()
    for k,v in q.items():
        r[k]=r.get(k,0)+v
        if not r[k]: del r[k]
    return r

def mul(p,q):
    r={}
    for e,c in p.items():
        for f,d in q.items():
            k=tuple(a+b for a,b in zip(e,f));r[k]=r.get(k,0)+c*d
    return {k:v for k,v in r.items() if v}

def mm(A,B):
    n=len(A)
    return [[sum_polys(mul(A[i][k],B[k][j]) for k in range(n)) for j in range(n)] for i in range(n)]

def sum_polys(it):
    p={}
    for q in it:p=add(p,q)
    return p

def ident(n,d):return [[{(0,)*d:1} if i==j else {} for j in range(n)] for i in range(n)]
def trace(M):return sum_polys(M[i][i] for i in range(len(M)))
def const_mat(A,d):return [[{(0,)*d:x} if x else {} for x in row] for row in A]
def diag_mons(es):return [[{e:1} if i==j else {} for j in range(len(es))] for i,e in enumerate(es)]
def canon(p):return min(p[i:]+p[:i] for i in range(len(p))) if p else p

C=const_mat([[2,1],[1,1]],1)
Ci=const_mat([[1,-1],[-1,2]],1)
D=diag_mons([(1,),(-1,)])
Di=diag_mons([(-1,),(1,)])
mapping={'a':C,'A':Ci,'b':D,'B':Di}
inverse={'a':'A','A':'a','b':'B','B':'b'}
count_checks=0
for n in range(1,8):
    for w in product('aAbB',repeat=n):
        if any(inverse[w[i]]==w[(i+1)%n] for i in range(n)):continue
        for swap in (False,True):
            M=ident(2,1)
            for c in w:
                if swap:c={'a':'b','A':'B','b':'a','B':'A'}[c]
                M=mm(M,mapping[c])
            p=add(trace(M),{(0,):1}) # Embed in SL3.
            wanted=sum(c in ('aA' if swap else 'bB') for c in w)
            assert max(e[0] for e in p)==wanted,(w,swap,p,wanted)
            count_checks+=1

P3=const_mat([[0,1,0],[0,0,1],[1,0,0]],2)
P2=const_mat([[0,1,0],[1,0,0],[0,0,-1]],2)
gap_checks={}
for k,P in ((2,P2),(3,P3)):
    signatures={};checked=0
    for gaps in product(range(-3,4),repeat=k):
        M=ident(3,2)
        for p in gaps:M=mm(mm(M,diag_mons([(p,0),(0,p),(-p,-p)])),P)
        got=trace(M)
        if k==2:
            p,q=gaps;expected=sum_polys([{(p,q):1},{(q,p):1},{(-p-q,-p-q):1}])
        else:
            p,q,r=gaps;expected=sum_polys([{(p-r,q-r):1},{(r-q,p-q):1},{(q-p,r-p):1}])
        assert got==expected,(gaps,got,expected)
        sig=(sum(gaps),tuple(sorted(got.items())))
        if sig in signatures: assert canon(gaps)==signatures[sig],gaps
        signatures[sig]=canon(gaps);checked+=1
    gap_checks[str(k)]=checked

# Optional k=4 reconstruction lemma; all equality patterns are covered by four symbols.
bigram={};bigram_checks=0
for p in product(range(4),repeat=4):
    sig=tuple(sorted(Counter((p[i],p[(i+1)%4]) for i in range(4)).items()))
    if sig in bigram: assert canon(p)==bigram[sig],(p,bigram[sig])
    bigram[sig]=canon(p);bigram_checks+=1

# A sample actual SL3 separation, including a negative a exponent and a zero gap.
x,y=Fraction(2),Fraction(3)
def value(gaps):
    p,q,r=gaps
    return x**(p-r)*y**(q-r)+x**(r-q)*y**(p-q)+x**(q-p)*y**(r-p)
p=(-2,0,3);q=tuple(reversed(p))
assert value(p)!=value(q)
report={'status':'all exact assertions passed',
        'unsigned_count_checks_on_all_cyclically_reduced_words_lengths_1_through_7_and_both_generators':count_checks,
        'gap_matrix_formula_and_orbit_signature_checks':gap_checks,
        'optional_length4_bigram_reconstruction_checks':bigram_checks,
        'example':{'gaps_u':p,'gaps_v':q,'A_diagonal':['2','3','1/6'],'B':'[[0,1,0],[0,0,1],[1,0,0]]','trace_u':str(value(p)),'trace_v':str(value(q))},
        'scope':'Finite sanity checks of the accompanying general proof; not an exhaustive solution of the open question.'}
print(json.dumps(report,indent=2))
