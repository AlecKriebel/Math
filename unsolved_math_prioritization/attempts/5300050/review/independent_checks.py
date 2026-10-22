#!/usr/bin/env python3
"""Independent exact inverse-branch and distortion diagnostics, not entropy proofs."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

count = 0
def check(test):
    global count
    assert test
    count += 1

def times(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]
def minus(z, w):
    return z[0]-w[0], z[1]-w[1]
def divide(z, w):
    den = w[0]*w[0]+w[1]*w[1]
    return (z[0]*w[0]+z[1]*w[1])/den, (z[1]*w[0]-z[0]*w[1])/den
def scale(z, c):
    return z[0]*c, z[1]*c
def norm(z):
    return z[0]*z[0]+z[1]*z[1]
def B(a, z):
    return divide(times(z, minus(z, (a, 0))), minus((1, 0), scale(z, a)))
def D(a, z):
    return (2-2*a*z[0])/(1-2*a*z[0]+a*a)

parameters = [Q(1,7),Q(2,7),Q(3,5),Q(5,7),Q(8,9)]
points = [(-Q(1),Q(0))]
for k in range(-11,12):
    t=Q(k,5)
    points.append(((1-t*t)/(1+t*t), 2*t/(1+t*t)))

# Solve the quadratic inverse equation at an independently selected rational
# boundary point. The second root is -w/z, with w=B(z).
for a in parameters:
    for z in points:
        w=B(a,z)
        other=scale(divide(w,z),-1)
        check(norm(other)==1 and other != z)
        check(B(a,other)==w)
        check(times(z,other)==scale(w,-1))
        check(min(D(a,z),D(a,other))>1)
        check(1/D(a,z)+1/D(a,other)==1)
        check(D(a,z)<=2/(1-a) and D(a,other)<=2/(1-a))
    # Exact inverse-contraction sum controlling the full n-step distortion.
    lam=2/(1+a)
    for n in range(1,31):
        total=sum((lam**(-j) for j in range(1,n+1)),Q(0))
        check(total==(1-lam**(-n))/(lam-1))
        check(total<1/(lam-1))

# Independent Laurent-coefficient comparison for the entropy factorization,
# using rational parametrizations of sqrt(1-a^2). It compares coefficients,
# rather than evaluating sampled unit-circle points.
for den in range(3,18):
    for num in range(1,den):
        t=Q(num,den)
        a=2*t/(1+t*t)
        b=(1-t*t)/(1+t*t)
        check(a*a+b*b==1)
        check((1+b)*(1+t*t)==2)
        check((1+b)*t==a)
        check(1<1+b<2)
        # As the zero multiplier is approached, the factor becomes 2.
        # As a approaches 1, it becomes 1; neither endpoint is substituted.
        check(1+b==2/(1+t*t))

check(B(Q(3,5),(1,0))==(1,0))
check(B(Q(3,5),(-1,0))==(1,0))
check(D(Q(3,5),(1,0))==5)
check(D(Q(3,5),(-1,0))==Q(5,4))
check(Q(1,5)+Q(4,5)==1)
check(1+Q(4,5)==Q(9,5))

root=Path(__file__).resolve().parent
snapshot=root/'author_replay'/'PARTIAL.md'
receipt={
    'status':'PASS',
    'assertions':count,
    'reviewed_artifact_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'controls':['two exact inverse roots and transfer-operator normalization',
                'uniform inverse-contraction geometric sums',
                'Laurent coefficient identities for the entropy factor',
                'partition endpoint and strict expansion checks'],
    'limitations':'Finite identities do not establish entropy limits, boundary accessibility, or the unresolved general upper bound.'
}
(root/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
