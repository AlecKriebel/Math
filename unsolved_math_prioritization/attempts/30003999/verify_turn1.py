"""Independent implementation of the turn-1 elementary reductions.
Finite exact tests only. No external source program is used.
"""
from fractions import Fraction
from itertools import combinations,combinations_with_replacement,product
from math import gcd
import json

def zero_test(p,q,terms):
    d={}
    for e,a in terms:d[e]=d.get(e,0)+a
    ts=sorted((e,a) for e,a in d.items() if a)
    if not ts:return True
    c=ts[0][1];last=ts[0][0]
    A=sum(abs(a) for _,a in ts)
    for e,a in ts[1:]:
        gap=e-last
        if c:
            if gap>abs(c).bit_length():return False
            divisor=p**gap
            if c%divisor:return False
            c=(c//divisor)*q**gap+a
        else:c=a
        assert abs(c)<=A
        last=e
    return c==0

def positive_compare(rs):
    n=len(rs)
    if n==0:return -1,0
    if min(rs)<0:return 1,0
    if min(rs)==0:return (0 if n==1 else 1),0
    if n==1:return -1,0
    k=(n-1).bit_length();R=0;num=0;den=1;expanded=0
    for e in sorted(rs):
        if e>=3*(R+k):return -1,expanded
        num=num*3**(e-R)+2**e;den=3**e;R=e;expanded+=1
        assert 2*R<3*k*(3**expanded-1)
        assert num%2==0 and den%2==1 and num!=den
        if num>den:return 1,expanded
    return -1,expanded

def sgn(x):return (x>0)-(x<0)
zero_cases=0;positive_cases=0;max_expanded=0
for p,q in ((2,1),(3,2),(5,3),(7,6),(9,4)):
    assert gcd(p,q)==1
    base=Fraction(p,q)
    for size in range(1,5):
        for exps in combinations(range(6),size):
            for coeff in product((-2,-1,1,2),repeat=size):
                val=sum(a*base**e for a,e in zip(coeff,exps))
                assert zero_test(p,q,list(zip(exps,coeff)))==(val==0)
                zero_cases+=1
# Explicit large-exponent exact cancellations: never expand the gap.
E=10**100
for p,q in ((3,2),(5,3),(9,4)):
    cases=[([(0,-p),(1,q),(E,-p),(E+1,q)],True),([(0,-p),(1,q),(E,1)],False),([(0,1),(E,-1)],False)]
    for terms,wanted in cases:
        assert zero_test(p,q,terms)==wanted;zero_cases+=1
for n in range(0,7):
    for rs in combinations_with_replacement(range(-2,11),n):
        expected=sgn(sum((Fraction(2,3)**r for r in rs),Fraction(0))-1)
        got,expanded=positive_compare(rs)
        assert got==expected,(rs,got,expected)
        positive_cases+=1;max_expanded=max(max_expanded,expanded)
# Large binary exponents are rejected without expanding enormous powers.
for rs,wanted in (([E],-1),([1,E],-1),([1,2,E],1),([E,E,E],-1),([0,E],1)):
    got,_=positive_compare(rs);assert got==wanted;positive_cases+=1
# Tetranomial precision example: structural cancellation, not a hardness result.
precision_cases=0
for N in range(3,101):
    x=Fraction(2,3)
    assert 9*x*x-12*x+4-x**N==-x**N;precision_cases+=1
print(json.dumps({'status':'PASS','zero_test_exact_cases':zero_cases,'positive_comparison_exact_cases':positive_cases,'precision_identity_exact_cases':precision_cases,'max_terms_expanded_in_finite_tests':max_expanded,'large_exponent_decimal_digits':101,'limitations':'Finite exact checks of the stated algorithms, not evidence for a general polynomial-time sign algorithm or a complexity lower bound.'},indent=2))
