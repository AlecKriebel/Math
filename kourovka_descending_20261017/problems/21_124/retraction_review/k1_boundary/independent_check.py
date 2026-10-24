#!/usr/bin/env python3
"""Independent exact affine-model check for the k=1 boundary only."""
import datetime
import hashlib
import json
from pathlib import Path

N=4
A=(1,0,-1,0)
T=(0,0,1,1)
ZERO=(0,)*N

def shift(v, j):
    return tuple(v[(i+j)%N] for i in range(N))

def mul(x,y):
    v,j=x;w,k=y
    return (tuple(a+b for a,b in zip(v,shift(w,j))), (j+k)%N)

def inv(x):
    v,j=x
    return (tuple(-a for a in shift(v,-j)), (-j)%N)

images={'a':(A,0),'b':(ZERO,1),'c':(ZERO,2),'t':(T,0)}

def evaluate(word):
    result=(ZERO,0)
    for ch in word:
        x=images[ch.lower()]
        result=mul(result, x if ch.islower() else inv(x))
    return result

# Uppercase denotes inverse. Every relation is checked directly.
relations={'tat^-1=a':'taTA', 'tbt^-1=ba':'tbTAB',
           'tct^-1=caba^-1b^-1':'tcTbaBAC'}
checked={name:evaluate(word) for name,word in relations.items()}
assert all(x==(ZERO,0) for x in checked.values())
assert evaluate('a')[0][0]==1
# Directly evaluate all boundary words of length <=5. For each pair
# in the quotient kernel, check the character product formula.
from itertools import product
kernel=[]
for length in range(6):
    for letters in product('abctABCT',repeat=length):
        word=''.join(letters)
        v,j=evaluate(word)
        if j==0:
            kernel.append((word,v))
# Pair every kernel word with every kernel word of length at most one.
small=[x for x in kernel if len(x[0])<=1]
pairs=0
for w,v in kernel:
    for z,u in small:
        image=evaluate(w+z)
        assert image[1]==0 and image[0][0]==v[0]+u[0]
        pairs+=1
for n in range(-100,101):
    word='a'*n if n>=0 else 'A'*(-n)
    v,j=evaluate(word)
    assert j==0 and v[0]==n
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'scope':'k=1 only; exact index-four virtual retraction onto <a>',
     'status':'PASS', 'linear_convention':'P(v)_i=v_(i+1 mod4)',
     'images':images,'relator_images':checked,
     'kernel_words_checked':len(kernel),'character_product_checks':pairs,
     'a_power_checks':201,
     'note':'Finite checks supplement the complete affine equations and kernel argument in AUDIT.md.'}
print(json.dumps(out,indent=2))
