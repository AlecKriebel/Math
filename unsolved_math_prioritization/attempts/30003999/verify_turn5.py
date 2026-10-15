"""Exact sparse carry controls. No external implementation is imported."""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
from math import gcd
import heapq,json

def normal(p,q,terms):
    data={}
    for e,a in terms:
        assert a>=0
        if a:data[e]=data.get(e,0)+a
    A=sum(data.values());heap=[-e for e in data];heapq.heapify(heap)
    queued=set(data);out={};steps=0;maxbit=0
    while heap:
        r=-heapq.heappop(heap);queued.remove(r);a=data.pop(r,0)
        if not a:continue
        steps+=1;maxbit=max(maxbit,a.bit_length())
        c,d=divmod(a,q)
        if d:out[r]=d
        if c:
            nxt=r-1;data[nxt]=data.get(nxt,0)+p*c
            if nxt not in queued:heapq.heappush(heap,-nxt);queued.add(nxt)
        assert all(a<=A for a in data.values())
    return sorted(out.items()),steps,maxbit

def value(p,q,ts):return sum((a*F(p,q)**e for e,a in ts),F(0))
count=0;maxsteps=0
for p,q in ((1,2),(2,3),(2,5),(3,5),(4,5)):
    for m in range(0,6):
        for exps in combinations_with_replacement(range(-2,7),m):
            ts=[(e,1) for e in exps]
            out,steps,mb=normal(p,q,ts)
            assert value(p,q,out)==value(p,q,ts);count+=1
            assert all(0<a<q for e,a in out);count+=1
            assert normal(p,q,out)[0]==out;count+=1
            maxsteps=max(maxsteps,steps)
# Uniqueness on a finite exact universe of already-normal digit strings.
for p,q in ((1,2),(2,3),(2,5),(3,5)):
    seen={}
    for digits in product(range(q),repeat=5):
        ts=tuple((e-2,a) for e,a in enumerate(digits) if a)
        v=value(p,q,ts)
        assert v not in seen or seen[v]==ts;count+=1
        seen[v]=ts
# Binary coefficient heights, including huge index gaps handled without expansion.
large=[]
E=10**100
for p,q in ((2,3),(3,5),(4,5)):
    a=2**1000+17
    base,steps,mb=normal(p,q,[(0,a)])
    shifted,steps2,mb2=normal(p,q,[(E,a)])
    assert shifted==[(e+E,d) for e,d in base];count+=1
    assert value(p,q,base)==a;count+=1
    both,steps3,mb3=normal(p,q,[(E,a),(0,a)])
    assert both==sorted(base+shifted);count+=1
    assert steps3==steps+steps2;count+=1
    large.append({'p':p,'q':q,'coefficient_bitlength':a.bit_length(),'input_exponent_decimal_digits':101,'output_nonzero_digits':len(both),'processed_positions':steps3,'maximum_intermediate_coefficient_bits':mb3})
# General explicit order/certificate obstruction, checking its exact parameters.
for q in range(3,50):
    for p in range(2,q):
        if gcd(p,q)!=1:continue
        d=(q+p-1)//p;t=d*p-q
        assert 1<=d<=q-1 and 1<=t<p;count+=1
        assert 0<F(t,q)<1 and F(d*p,q)-1==F(t,q);count+=1
        for R in range(1,10):assert (t*pow(q,R-1,p))%p!=0;count+=1
print(json.dumps({'status':'PASS','exact_assertions':count,'finite_unit_input_max_processed_positions':maxsteps,'large_binary_input_cases':large,'specific_order_failure':'2*(2/3)=4/3>1 despite its smaller leading place','nonnegative_integer_certificate_failure':'2*(2/3)-1=1/3 has no finite nonnegative-integer power-sum representation','limitations':'Canonical equality normalization and specific order-certificate obstructions only; not a general order algorithm or complexity lower bound.'},indent=2))
