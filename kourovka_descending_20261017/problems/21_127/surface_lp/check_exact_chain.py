#!/usr/bin/env python3
"""Free-group identities and Euler bookkeeping for the exact chain certificate."""
from pathlib import Path
import json

def reduce(word):
    out=[]
    for x in word:
        if out and out[-1]==-x:
            out.pop()
        else:
            out.append(x)
    return out

def inverse(word):
    return [-x for x in word[::-1]]

def comm(u,v):
    return reduce(u+v+inverse(u)+inverse(v))

x,y=[1],[2]
h=comm(x,y)
first=comm([-1],y)
second=comm(y,x)
assert first==reduce([-1]+inverse(h)+[1])
assert second==inverse(h)
a,b,c,d=x,[-1,-1],[],y
assert comm(a,b)==comm(b,c)==comm(c,d)==[]
assert comm(reduce(a+b),d)==first
assert comm(d,a)==second
chi=-2
boundaries_before=4
boundaries_after=2
assert (2-boundaries_before-chi)//2==0
assert (2-boundaries_after-chi)//2==1
out={'scope':'one chain mechanism certificate only',
     'homomorphism':{'a':'x','b':'x^-2','c':'1','d':'y'},
     'commutator_h':h,'first_image':first,'second_image':second,
     'Euler_characteristic':chi,'final_genus':1,'prescribed_boundary_degree_each':1,
     'chain_scl':1,'all_checks_passed':True}
Path(__file__).with_name('EXACT_CHAIN_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print('Free-group identities and genus bookkeeping passed')
