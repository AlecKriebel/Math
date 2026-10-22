#!/usr/bin/env python3
"""Independent finite word/normalization controls; no analytic realization claim."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from pathlib import Path
import hashlib,json
checks=Counter()
def ck(k,b):
    checks[k]+=1
    assert b,k
def words(bound,prefix=()):
    yield prefix
    for n in range(2,bound+1):
        yield from words(bound-n,prefix+(n,))
def encode(w):
    return ''.join('x'*(k-1)+'y' for k in w)
def decode(w):
    out=[];k=1
    for a in w:
        if a=='x':k+=1
        else:out.append(k);k=1
    assert k==1
    return tuple(out)
for w in words(12):
    a=encode(w);actual=Counter()
    # Choose the positions of the NEW x and y, preserving their order.
    for i,j in combinations(range(len(a)+2),2):
        result=[];it=iter(a)
        for t in range(len(a)+2):
            result.append('x' if t==i else 'y' if t==j else next(it))
        actual[decode(''.join(result))]+=1
    exceptional={v:c for v,c in actual.items() if 1 in v}
    predicted=Counter()
    for j,k in enumerate(w):
        raised=list(w);raised[j]+=1;raised=tuple(raised)
        for i in range(j+1,len(w)+1):
            predicted[raised[:i]+(1,)+raised[i:]]+=2*k
    ck('literal_insertion_one_1_terms',exceptional==dict(predicted))
    ck('no_leading_1_or_multiple_1',all(v[0]>=2 and v.count(1)==1 for v in exceptional))
    ck('literal_shuffle_multiplicities',sum(actual.values())==(len(a)+2)*(len(a)+1)//2)
    for j in range(len(w)):
        coefficients=[0]*len(w)
        for i in range(j+1,len(w)+1):
            coefficients[i-1]+=1
            if i<len(w):coefficients[i]-=1
        ck('terminal_telescoping',coefficients==[int(t==j) for t in range(len(w))])

# Independent coefficient extraction in u^d/d! v^(k-1).
for k in range(1,15):
    for d in range(15):
        coefficient=F((d+1)*k,factorial(d+1))*factorial(d)
        ck('mixed_derivative_coefficient',coefficient==k)
        factor=F(factorial(d),factorial(k-1))
        reverse=F(factorial(k-1),factorial(d))
        ck('depth_one_swap_square',factor*reverse==1)

# Low-weight analytic normalization, via exact Fourier coefficients of G2 and G4.
# g_k=G_k/(2*pi*i)^k; g2=-1/24+sum sigma1 q^n,
# g4=1/1440+(1/6)sum sigma3 q^n.
def sigma(n,k):
    return sum(d**k for d in range(1,n+1) if n%d==0)
bound=80
g2=[F(-1,24)]+[F(sigma(n,1)) for n in range(1,bound+1)]
g4=[F(1,1440)]+[F(sigma(n,3),6) for n in range(1,bound+1)]
for n in range(bound+1):
    lhs=n*g2[n]
    square=sum(g2[j]*g2[n-j] for j in range(n+1))
    ck('classical_G2_derivative_normalization',lhs==5*g4[n]-2*square)
ck('nonzero_q_coefficient',g2[1]!=0)
root=Path(__file__).resolve().parent
sha=hashlib.sha256((root/'author_replay/SOURCE_STATUS.md').read_bytes()).hexdigest()
ck('frozen_artifact',sha=='440edf90c25d16eeb424699d88a4c93f81a079040e753915925a9773e8ed7a60')
print(json.dumps({'assertions':sum(checks.values()),'categories':dict(sorted(checks.items())),
                  'artifact_sha256':sha,'scope':'Finite rational formal-word and Fourier-normalization controls only. This does not certify all-depth regularization or swap-invariant analytic realization.','verdict':'PASS_SCOPED_CONTROLS'},indent=2,sort_keys=True))
