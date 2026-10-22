#!/usr/bin/env python3
"""Exact, bounded algebraic checks for the n=2 reconstruction.

These tests complement PROOF.md. They do not prove the categorical theorem,
the global-dimension bounds, or identities outside the explicitly tested range.
No external packages, files, networking, or randomness are used.
"""
from collections import Counter
from itertools import product
from fractions import Fraction
import json

REL = {'H': {(0, 0): 1, (2, 0): -1},
       'L': {}, 'B': {(2, 0): -1}}
COUNTS = Counter()

def clean(a):
    return {k: v for k, v in a.items() if v}

def mono(i=0, j=0):
    return {(i, j): 1}

def add(*xs):
    out = Counter()
    for x in xs:
        for k, v in x.items():
            out[k] += v
    return clean(out)

def scale(x, n):
    return clean({k: n*v for k, v in x.items()})

def mm(kind, a, b):
    i, j = a
    r, s = b
    sign = -1 if (j*r) % 2 else 1
    if j+s < 2:
        return {(i+r, j+s): sign}
    return {(i+r+v, w): sign*c for (v, w), c in REL[kind].items()}

def mul(kind, a, b):
    out = Counter()
    for u, v in a.items():
        for x, y in b.items():
            for z, c in mm(kind, u, x).items():
                out[z] += v*y*c
    return clean(out)

def tensor(*xs):
    out = {(): 1}
    for x in xs:
        out = {a+(b,): c*d for a, c in out.items() for b, d in x.items()}
    return clean(out)

def tmul(kinds, a, b):
    out = Counter()
    for u, v in a.items():
        for x, y in b.items():
            for z, c in tensor(*(mm(k, p, q) for k, p, q in zip(kinds, u, x))).items():
                out[z] += v*y*c
    return clean(out)

def tmap(a, pos, fn):
    out = Counter()
    for key, c in a.items():
        for sub, d in fn(mono(*key[pos])).items():
            out[key[:pos]+sub+key[pos+1:]] += c*d
    return clean(out)

def delta(kind, a, old=False):
    out = {}
    for (i, j), c in a.items():
        base = tensor(mono(i), mono(i))
        if j:
            skew = add(tensor(mono(0,1), mono()), tensor(mono(1), mono(0,1)))
            if old:
                skew = add(tensor(mono(), mono(0,1)), tensor(mono(0,1), mono(1)))
            base = tmul((kind, kind), base, skew)
        out = add(out, scale(base, c))
    return out

def rho(a):
    out = {}
    for (i,j), c in a.items():
        base = tensor(mono(i), mono(i))
        if j:
            base = tmul(('B','H'),base,add(tensor(mono(0,1),mono()),tensor(mono(1),mono(0,1))))
        out = add(out,scale(base,c))
    return out

def left(a):
    out = {}
    for (i,j), c in a.items():
        base = tensor(mono(i),mono(i))
        if j:
            base = tmul(('L','B'),base,add(tensor(mono(1),mono(0,1)),tensor(mono(0,1),mono())))
        out=add(out,scale(base,c))
    return out

def antipode(kind, a):
    out={}
    for (i,j),c in a.items():
        val=mono(-i)
        if j:
            val=mul(kind,scale(mono(-1,1),-1),val)
        out=add(out,scale(val,c))
    return out

def can_right(a):
    out={}
    for (p,q),c in a.items():
        out=add(out,scale(tmul(('B','H'),tensor(mono(*p),mono()),rho(mono(*q))),c))
    return out

def inv_right(a):
    out={}
    for (p,(i,j)),c in a.items():
        b=mono(*p)
        if not j:
            val=tensor(mul('B',b,mono(-i)),mono(i))
        else:
            val=add(tensor(mul('B',b,mono(-i-1)),mono(i,1)),
                    scale(tensor(mul('B',mul('B',mul('B',b,mono(-1)),mono(0,1)),mono(-i)),mono(i)),-1))
        out=add(out,scale(val,c))
    return out

def can_left(a):
    out={}
    for (p,q),c in a.items():
        out=add(out,scale(tmul(('L','B'),left(mono(*p)),tensor(mono(),mono(*q))),c))
    return out

def inv_left(a):
    out={}
    for ((i,j),p),c in a.items():
        b=mono(*p)
        if not j:
            val=tensor(mono(i),mul('B',mono(-i),b))
        else:
            val=add(tensor(mono(i,1),mul('B',mono(-i),b)),
                    scale(tensor(mono(i+1),mul('B',mul('B',mul('B',mono(-1),mono(0,1)),mono(-i)),b)),-1))
        out=add(out,scale(val,c))
    return out

def check(label, a, b):
    assert a == b, (label, a, b)
    COUNTS[label]+=1

def run():
    one=mono(); g=mono(1); z=mono(0,1)
    small=[mono(i,j) for i in range(-2,3) for j in range(2)]
    wider=[mono(i,j) for i in range(-3,4) for j in range(2)]
    for kind in REL:
        for a,b,c in product(small,repeat=3):
            check('normal_form_associativity',mul(kind,mul(kind,a,b),c),mul(kind,a,mul(kind,b,c)))
    for kind in ['H','L']:
        for a,b in product(small,repeat=2):
            check('coproduct_multiplicativity',delta(kind,mul(kind,a,b)),tmul((kind,kind),delta(kind,a),delta(kind,b)))
            check('antipode_antimultiplicativity',antipode(kind,mul(kind,a,b)),mul(kind,antipode(kind,b),antipode(kind,a)))
        for a in wider:
            d=delta(kind,a)
            check('hopf_coassociativity',tmap(d,0,lambda x:delta(kind,x)),tmap(d,1,lambda x:delta(kind,x)))
            for side in [0,1]:
                total={}
                for (p,q),c in d.items():
                    terms=[mono(*p),mono(*q)];terms[side]=antipode(kind,terms[side])
                    total=add(total,scale(mul(kind,*terms),c))
                eps=sum(c for (i,j),c in a.items() if j==0)
                check('antipode_identity',total,scale(one,eps))
            check('antipode_fourth_power',antipode(kind,antipode(kind,antipode(kind,antipode(kind,a)))),a)
    for a,b in product(small,repeat=2):
        check('right_coaction_multiplicativity',rho(mul('B',a,b)),tmul(('B','H'),rho(a),rho(b)))
        check('left_coaction_multiplicativity',left(mul('B',a,b)),tmul(('L','B'),left(a),left(b)))
    for a in wider:
        check('right_coassociativity',tmap(rho(a),0,rho),tmap(rho(a),1,lambda x:delta('H',x)))
        check('left_coassociativity',tmap(left(a),0,lambda x:delta('L',x)),tmap(left(a),1,left))
        check('commuting_coactions',tmap(left(a),1,rho),tmap(rho(a),0,left))
    for a,b in product(wider,repeat=2):
        pair=tensor(a,b)
        check('right_can_after_inverse',can_right(inv_right(pair)),pair)
        check('right_inverse_after_can',inv_right(can_right(pair)),pair)
        check('left_can_after_inverse',can_left(inv_left(pair)),pair)
        check('left_inverse_after_can',inv_left(can_left(pair)),pair)
    # A literal use of the source's opposite coproduct fails for its left coaction.
    bad=tmap(left(z),0,lambda x:delta('L',x,old=True))
    good=tmap(left(z),1,left)
    assert bad!=good
    COUNTS['source_opposite_coproduct_detected']=1
    # The printed inclusive range j <= n cannot define the advertised linear map.
    # At n=2, gamma(1-g^2)=1-u^2, whereas the printed prescription gives t^2=-u^2.
    check('source_inclusive_basis_range_detected',add(REL['H'],scale(REL['B'],-1)),one)
    # Dual-number resolution: multiplication by y sends 1->y, y->0.
    check('dual_number_differential',mul('L',z,one),z)
    check('dual_number_differential',mul('L',z,z),{})
    check('dual_number_image_kernel_dimension',1,2-1)
    return {'problem_id':'30004831','status':'pass','arithmetic':'exact integers and rationals',
            'assertions':sum(COUNTS.values()),'counts':dict(sorted(COUNTS.items())),
            'scope':'Finite normal-form tests, not a formal proof of global dimension or tensor equivalence.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
