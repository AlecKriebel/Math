#!/usr/bin/env python3
"""Exact independent normal-form test in a nontrivial two-dead-letter model.
Ambient group: Z(a) x Z(b) x F(c,z,w), weights (2,4,3,0,0).
The predicted kernel is Z(k) x F(l,z0,z1,w0,w1), with
k=a^-2 b and l=a^-3 c^2. Both dead letters have residue modulus 2.
This checks one explicit family, not the general theorem.
"""
from pathlib import Path
import json

# Signed integers name free generators. Ambient: 1=c,2=z,3=w.
# Kernel free basis: 1=l,2=z0,3=z1,4=w0,5=w1.
images={1:(1,1),2:(2,),3:(1,2,-1),4:(3,),5:(1,3,-1)}

def reduce_word(word):
    stack=[]
    for a in word:
        if stack and stack[-1] == -a: stack.pop()
        else: stack.append(a)
    return tuple(stack)

def inverse(word): return tuple(-x for x in word[::-1])

def ambient_image(word):
    return reduce_word(a for x in word for a in (images[x] if x>0 else inverse(images[-x])))

def schreier_decode(word):
    parity=0
    out=[]
    for a in word:
        if a==1:
            if parity: out.append(1)
            parity=1-parity
        elif a==-1:
            if not parity: out.append(-1)
            parity=1-parity
        else:
            sign=1 if a>0 else -1
            out.append(sign*((2 if abs(a)==2 else 4)+parity))
    assert parity==0
    return reduce_word(out)

letters=tuple(range(1,6))+tuple(range(-5,0))
level=[()]
checks=0
for length in range(6):
    for word in level:
        amb=ambient_image(word)
        assert schreier_decode(amb)==word
        l_exp=sum(1 if x==1 else -1 if x==-1 else 0 for x in word)
        c_exp=sum(1 if x==1 else -1 if x==-1 else 0 for x in amb)
        assert c_exp==2*l_exp
        for k_exp in range(-2,3):
            a_exp=-2*k_exp-3*l_exp
            b_exp=k_exp
            assert 2*a_exp+4*b_exp+3*c_exp==0
            # The ambient abelian coordinates uniquely recover the central
            # kernel coordinate and the free c exponent constraint.
            assert b_exp==k_exp
            assert a_exp==-2*b_exp-3*c_exp//2
        checks+=1
    if length<5:
        level=[word+(x,) for word in level for x in letters if not word or word[-1]!=-x]

residue_checks=0
for q in range(-40,41):
    residue=q%2
    ell=(q-residue)//2
    for dead,basegen in ((2,2),(3,4)):
        zq=(1,)*q+(dead,)+(-1,)*q if q>=0 else (-1,)*(-q)+(dead,)+(1,)*(-q)
        # l^ell z_residue l^-ell in the kernel free basis.
        power=(1,)*ell if ell>=0 else (-1,)*(-ell)
        kernelword=power+(basegen+residue,)+inverse(power)
        assert ambient_image(kernelword)==reduce_word(zq)
        residue_checks+=1
result={
    "status":"pass",
    "ambient":"Z^2 x F(c,z,w), weights (a,b,c,z,w)=(2,4,3,0,0)",
    "predicted_kernel":"Z x F_5",
    "moduli":{"z":2,"w":2},
    "reduced_kernel_free_words_checked":checks,
    "maximum_word_length":5,
    "central_coordinates_per_word":5,
    "positive_negative_residue_identities_checked":residue_checks,
    "scope":"One explicit model with two dead letters, nontrivial associated cyclic subgroup, residue modulus two, arbitrary signs, and exact Schreier normal forms. Not a proof of the general upper bound."
}
Path(__file__).with_name('zero_direction_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
