#!/usr/bin/env python3
"""Own exact finite checks; no imported author verifier or simulation."""
from fractions import Fraction as Q
from pathlib import Path
import json
import math
import datetime

q = Q(3, 4)
p = ((q, 1-q), (1-q, q))
mu = (Q(1,2), Q(1,2))

def word(j):
    return tuple(int(math.isqrt(r)**2 == r and r >= 4) for r in range(1,j*j))

def probability(w):
    if not w:
        return Q(1)
    answer = mu[w[0]]
    for a,b in zip(w,w[1:]):
        answer *= p[a][b]
    return answer

def cylinder(w):
    left, length = Q(0), Q(1)
    for index,digit in enumerate(w):
        probs = mu if index == 0 else p[w[index-1]]
        if digit:
            left += length * probs[0]
        length *= probs[digit]
    return left,left+length

def profile_eventual(prefix,digit):
    # Includes the empty prefix and all prefixes through the finite prefix.
    value = sum((probability(prefix[:r]) for r in range(len(prefix)+1)),Q(0))
    last = prefix[-1]
    value += probability(prefix)*p[last][digit]/(1-p[digit][digit])
    return value

def ceil_q(x):
    return (x.numerator+x.denominator-1)//x.denominator

assert all(sum(row) == 1 for row in p)
assert all(sum(mu[i]*p[i][j] for i in range(2)) == mu[j] for j in range(2))
assert p[0] != p[1]
records=[]
series=Q(0)
for j in range(2,31):
    W=word(j)
    P=probability(W)
    formula=Q(1,2)*Q(1,4)**(2*j-4)*q**(j*j-2*j+2)
    assert P==formula and W[-1]==0
    assert sum(a != b for a,b in zip(W,W[1:]))==2*j-4
    series += q*P
    tau=cylinder(W+(1,))[0]
    assert tau==series==cylinder(W+(0,))[1]
    A=profile_eventual(W+(0,),1)
    B=profile_eventual(W+(1,),0)
    C=sum((probability(W[:r]) for r in range(len(W)+1)),Q(0))
    assert A==C+Q(3,2)*P and B==C+Q(1,2)*P and A-B==P
    right_long=cylinder(W+(1,)+(0,)*(2*j))
    assert right_long[0]==tau and right_long[1]-tau==P*q**(2*j)/12
    K=j//2
    left_near=cylinder(W+(0,)+(1,)*K)
    right_near=cylinder(W+(1,)+(0,)*K)
    assert left_near[1]==tau and right_near[0]==tau
    assert tau-left_near[0]==P*q**K/4
    assert right_near[1]-tau==P*q**K/12
    width=P*q**j
    n=ceil_q(1/width**2)
    assert n*width**2>=1 and n*width**2<1+width**2
    assert n*P**2>=q**(-2*j)
    records.append({'j':j,'P':str(P),'tau':str(tau),'jump':str(A-B),'window_contained':width < right_near[1]-tau,'ceil_n_digits':len(str(n))})

# Independent rigorous enclosure of the infinite rank.
# Consecutive P ratios equal q^(2j-1)/16, always below 1/16.
t_lower=series
P_next=Q(1,2)*Q(1,4)**(2*31-4)*q**(31*31-2*31+2)
t_upper=series+Q(16,15)*q*P_next
assert Q(0)<t_lower<t_upper<Q(1,2)

large=[]
for j in (20,40,80,120,160,200):
    P=Q(1,2)*Q(1,4)**(2*j-4)*q**(j*j-2*j+2)
    width=P*q**j
    n=ceil_q(1/width**2)
    # Use logarithms of exact big integers; no conversion of huge n to float.
    L=math.log(n)
    H=math.ceil(5*L/math.log(4/3))+1
    sqrt_n_P=math.exp(0.5*L+math.log(P.numerator)-math.log(P.denominator))
    leading_R_ratio=2*H*math.sqrt(2*L)/sqrt_n_P
    profile_ratio=float(q**(j//2))
    large.append({'j':j,'log_n':L,'sqrt_n_P':sqrt_n_P,'profile_error_over_P':profile_ratio,'leading_R_over_nP':leading_R_ratio,'combined_leading_band_error_over_P':leading_R_ratio+profile_ratio,'right_window_length_over_width':float(q**(j//2-j)/12),'rank_boundary_distance_over_width_upper':float(q**j/12)})

output={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'method':'Own exact fractions for finite identities; logarithmic diagnostics for asymptotic sizes; no asymptotic claim rests on finite numerics.',
 'finite_identities_all_pass':True,
 'j_values':list(range(2,31)),
 'stationary_source_pass':True,
 't_enclosure':{'lower':str(t_lower),'upper':str(t_upper),'approximate':float(t_lower),'width':str(t_upper-t_lower)},
 'exact_records':records,
 'large_size_diagnostics':large,
 'CLT_status':'Analytical binomial triangular CLT, not verified by finite computation.',
}
Path('CHECK_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ('exact_records','t_enclosure')},indent=2))
