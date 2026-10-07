#!/usr/bin/env python3
"""Exact finite checks in the family-197 torsion-free proof.

This checks finite arithmetic/type identities only. It does not execute the
asymptotic random construction or certify the topology of a selected group.
No third-party code is executed. Python standard library only.
"""
from fractions import Fraction as Q
from math import factorial
import hashlib
import json
from pathlib import Path

q = 128
v = q*q+q+1
p = Q(q+1, v)
alphabet_size = v+7
ordinary = list(range(v))
extra = list(range(v, v+7))
bar = {i:v+i for i in range(7)} | {v+i:i for i in range(7)}
for i in range(7, v, 2):
    bar[i], bar[i+1] = i+1, i
assert len(bar) == alphabet_size
assert all(bar[bar[t]] == t and bar[t] != t for t in bar)

def f(t):
    return 4 if bar[t] in extra else 1

def w(t, u):
    if u == bar[t]:
        return Q(0)
    if bar[t] in ordinary and u in ordinary:
        return Q(1,q+1)
    if bar[t] in extra and u in extra:
        return Q(1,2)
    return p

# One representative of each possible row category: bar(t) extra,
# bar(t) ordinary paired with extra, and bar(t) ordinary paired with ordinary.
rows = {t:sum(w(t,u)**2*f(u) for u in range(alphabet_size))/f(t)
        for t in (0,v,7)}
lambda1 = Q(q,q+1)+7*p*p+Q(21,(q+1)**2)
lambda2 = (Q(6,4)+(v+21)*p*p)/4
assert rows[0] == lambda2
assert rows[7] == lambda1
assert rows[v] == lambda1-Q(3,(q+1)**2)
lambda_bound = Q(199,200)
assert all(x < lambda_bound for x in rows.values())

# Fano lines are nonzero kernels of nonzero linear functionals on F_2^3.
points = range(1,8)
def dot_mod2(a,b):
    return (a & b).bit_count() % 2
lines = [frozenset(b for b in points if dot_mod2(a,b)==0) for a in points]
complements = [frozenset(points)-line for line in lines]
assert len(set(lines))==7
assert all(len(line)==3 for line in lines)
assert all(len(d)==4 for d in complements)
assert all(len(d&e)==2 for i,d in enumerate(complements) for e in complements[i+1:])
assert all(sum(x in d for d in complements)==4 for x in points)
assert all(sum(x in d and y in d for d in complements)==2
           for x in points for y in points if x!=y)
parts = [frozenset(),*complements,frozenset(points)]
assert all(len(a&b)%2 == (i==len(parts)-1 and j==len(parts)-1)
           for i,a in enumerate(parts) for j,b in enumerate(parts))
for m in (1,5,9,101,1001):
    a_m = Q((q+1)*m-1,4)
    b_m = Q((q+1)*(m-1),4)
    assert a_m.denominator == b_m.denominator == 1
    assert 4*a_m+1 == (q+1)*m
    assert 4*b_m == (q+1)*(m-1)

# Rational Taylor lower bounds for e^16, e^5, and e^12 prove the
# logarithmic comparisons used for c0=1/100 and explicit word-decay constants.
def exp_lower(x,k):
    return sum(Q(x)**i/factorial(i) for i in range(k+1))
assert exp_lower(16,16) > 2*alphabet_size/p
assert exp_lower(5,9) > 136
assert exp_lower(12,11) > 4*alphabet_size/lambda_bound
c0 = Q(1,100)
assert c0*16 < 1 and 2*c0*5 < 1
# Mf<=lambda_bound*f implies sum_W P(W)^2<=4|T|lambda_bound^(h-1).
# log(lambda_bound)<=-(1-lambda_bound)=-1/200. The e^12 check gives
# log(4|T|/lambda_bound)<12, so delta=1/1000 works for every h>=4000.
delta = Q(1,1000)
assert 12-Q(4000,200) <= -2*delta*4000
# All positive turn weights >=1/129 and log(129)<5; full blocks have
# h<=s+1, so d=floor(-log P(W))<=5s. We use the looser a0=6.
a0 = Q(6)
epsilon = min(Q(1,4),delta/(16*(1+a0)))
assert epsilon == Q(1,112000)

out = {
    'check_kind':'exact finite arithmetic; no asymptotic graph or topology certificate',
    'q':q,'v':v,'p':str(p),'alphabet_size':alphabet_size,
    'Mf_over_f_representative_rows':{str(k):str(x) for k,x in rows.items()},
    'lambda1':str(lambda1),'lambda2':str(lambda2),
    'lambda_bound':str(lambda_bound),'delta':str(delta),
    'word_decay_valid_for_h_at_least':4000,
    'c0':str(c0),'a0':str(a0),'epsilon':str(epsilon),
    'fano_lines':[sorted(x) for x in lines],
    'fano_complements':[sorted(x) for x in complements],
    'status':'all checks passed',
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(out,indent=2,sort_keys=True))
