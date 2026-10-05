#!/usr/bin/env python3
"""Exact rational controls. Python 3 standard library only; no network."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parent

def cf(x):
    assert 0 < x <= 1
    out=[]
    while x:
        a=x.denominator//x.numerator
        out.append(a)
        x=1/x-a
    return out

def question(x):
    if x==0:return F(0)
    assert 0 < x <= 1
    s=0; y=F(0)
    for i,a in enumerate(cf(x)):
        s+=a
        y+=F((-1)**i,1<<(s-1))
    return y

def pair(x):return [x.numerator,x.denominator]
def encode_interval(a,b,qa,qb,depth,reason):
    return {'a':pair(a),'b':pair(b),'qa':pair(qa),'qb':pair(qb),'depth':depth,'reason':reason}

def exhaust(depth):
    stack=[(F(2,5),F(3,7),F(3,8),F(7,16),0)]
    leaves=[]; visited=0
    while stack:
        a,b,qa,qb,d=stack.pop();visited+=1
        assert b.numerator*a.denominator-a.numerator*b.denominator==1
        assert question(a)==qa and question(b)==qb
        if qb<a: reason='negative'
        elif qa>b: reason='positive'
        elif d==depth:reason='retained'
        else:
            m=F(a.numerator+b.numerator,a.denominator+b.denominator)
            qm=(qa+qb)/2
            assert question(m)==qm
            stack.append((m,b,qm,qb,d+1));stack.append((a,m,qa,qm,d+1));continue
        leaves.append(encode_interval(a,b,qa,qb,d,reason))
    leaves.sort(key=lambda z:F(*z['a']))
    assert F(*leaves[0]['a'])==F(2,5) and F(*leaves[-1]['b'])==F(3,7)
    assert all(F(*x['b'])==F(*y['a']) for x,y in zip(leaves,leaves[1:]))
    live=[z for z in leaves if z['reason']=='retained']
    lo=min(F(*z['a']) for z in live); hi=max(F(*z['b']) for z in live)
    # The hull brackets at least one root, in addition to containing every root.
    assert question(lo)<lo and question(hi)>hi
    digits=42037233942322307564099300664622187394918986
    assert (lo*10**44)//1==digits and (hi*10**44)//1==digits
    return {'depth':depth,'visited':visited,'leaf_count':len(leaves),'retained_count':len(live),'hull':[pair(lo),pair(hi)],'width':pair(hi-lo),'leaves':leaves}

def bisect(n):
    a,b=F(2,5),F(3,7)
    for _ in range(n):
        m=(a+b)/2; d=question(m)-m
        assert d!=0
        if d<0:a=m
        else:b=m
    assert question(a)<a and question(b)>b
    assert b-a==F(1,35*(1<<n))
    return {'steps':n,'a':pair(a),'b':pair(b),'width':pair(b-a)}

def rational_spacing(maxq):
    failed_half=[];failed_one=[];tested=0;min_ratio=None;argmin=None
    for q in range(3,maxq+1):
        for p in range(1,(q+1)//2):
            if gcd(p,q)!=1:continue
            x=F(p,q); y=question(x);d=abs(y-x);r=d*q*q;tested+=1
            assert d>0
            s=sum(cf(x));den=1<<(s-1)
            assert y.denominator==den
            assert d>=F(gcd(q,den),q*den)
            if min_ratio is None or r<min_ratio:min_ratio=r;argmin=x
            if r<=F(1,2):failed_half.append({'x':pair(x),'q2_displacement':pair(r)})
            if r<F(1):failed_one.append({'x':pair(x),'q2_displacement':pair(r)})
    return {'max_denominator':maxq,'tested':tested,'at_most_half':failed_half,'less_than_one':failed_one,'minimum_ratio':pair(min_ratio),'argmin':pair(argmin)}

def controls():
    vals={F(0):F(0),F(1,2):F(1,2),F(1):F(1),F(1,3):F(1,4),F(3,8):F(5,16),F(2,5):F(3,8),F(3,7):F(7,16),F(7,16):F(29,64),F(4,9):F(15,32)}
    for x,y in vals.items():assert question(x)==y
    for q in range(2,151):
        for p in range(1,q):
            if gcd(p,q)!=1:continue
            x=F(p,q)
            assert question(1-x)==1-question(x)
            assert question(x/(1+x))==question(x)/2
            assert (question(x)==x)==(x==F(1,2))
    # Same-sign endpoints do not certify absence of a fixed point.
    a,b=F(2,5),F(4,7)
    assert question(a)-a<0 and question(b)-b<0
    assert a<F(1,2)<b and question(F(1,2))==F(1,2)
    # Rational spacing conjecture fails at these small denominators.
    assert abs(question(F(3,7))-F(3,7))*49==F(7,16)
    assert abs(question(F(8,19))-F(8,19))*361==F(19,64)
    # F=Q-id is not increasing even inside the candidate interval.
    a,b=F(5,12),F(53,127)
    assert F(2,5)<a<b<F(3,7)
    assert question(b)-b < question(a)-a
    # A Q-fixed t in (0,1) cannot have L(t) fixed: symbolic correction is negative.
    for t in [F(1,4),F(2,5),F(3,7),F(1,2),F(3,4)]:
        lhs=question(t/(1+t))-t/(1+t)
        rhs=(question(t)-t)/2+t*(t-1)/(2*(1+t))
        assert lhs==rhs
    return {'base_values':len(vals),'symmetry_and_left_equation_maxq':150,'negative_controls':'passed'}

def main():
    results={'controls':controls(),'cylinder_exhaustion':exhaust(128),'bisection':bisect(160),'rational_spacing':rational_spacing(1500)}
    out=ROOT/'EXACT_RESULTS.json';data=(json.dumps(results,indent=2,sort_keys=True)+'\n').encode()
    if '--check' in __import__('sys').argv:
        assert out.read_bytes()==data,'Exact results differ'
        print('PASS: exact results reproduced byte-for-byte')
    else:out.write_bytes(data)
    for k,v in results.items():
        if k=='cylinder_exhaustion':v={a:b for a,b in v.items() if a!='leaves'}
        print(k,json.dumps(v,sort_keys=True))
    print('result_bytes',len(data),'sha256',hashlib.sha256(data).hexdigest())
if __name__=='__main__':main()
