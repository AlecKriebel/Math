#!/usr/bin/env python3
"""Mandatory exact/analytic regressions for forbidden activation conditioning."""
from __future__ import annotations
from fractions import Fraction
from math import factorial,log

def source_factor(x,y):
    out=1
    for a,b in zip(x,y):
        if a<b:return 0
        for j in range(b):out*=a-j
    return out

def probabilities(x,channels):
    rates=[source_factor(x,s)*float(k) for s,t,k in channels]
    z=sum(rates)
    return [a/z for a in rates]

def fire(x,s,t):return tuple(a-u+v for a,u,v in zip(x,s,t))
def V(x,target):return sum(log(factorial(a-b)) for a,b in zip(x,target))

def episode(x,target,channels,path):
    """Expected V increment; stop on deviation, final ordinary jump after path."""
    initial=V(x,target)
    def final_value(y,t):
        p=probabilities(y,channels)
        return sum(p[i]*V(fire(y,*channels[i][:2]),channels[i][1])
                   for i in range(len(channels)) if p[i])
    def rec(y,t,k):
        p=probabilities(y,channels)
        if k==len(path):return final_value(y,t)
        d=path[k]
        out=0.0
        for i,ch in enumerate(channels):
            if not p[i]:
                continue
            yp=fire(y,*ch[:2])
            if i==d:out+=p[i]*rec(yp,ch[1],k+1)
            else:out+=p[i]*V(yp,ch[1])
        return out
    return rec(x,target,0)-initial

ONE=(
 ((0,),(2,),1.0),((2,),(1,),1.0),((1,),(0,),1.0),
)
TWO=(
 ((1,0),(2,0),1.0),((2,0),(1,0),1.0),
 ((0,0),(1,1),1.0),((1,1),(0,1),1.0),((0,1),(0,0),1.0),
)

def one_linkage_conditioned(n):
    pre=V((n,),(0,))
    y=(n+2,)
    return V(y,(2,))-pre + episode(y,(2,),ONE,(1,2))

def two_linkage_conditioned(n):
    x=(n,0);target=(2,0);birth=TWO[2]
    activation=V(fire(x,*birth[:2]),birth[1])-V(x,target)
    y=fire(x,*birth[:2])
    return activation+episode(y,(1,1),TWO,(3,4))

def honest_two_linkage(n):
    return episode((n,0),(2,0),TWO,(1,))

def exact_one_coefficients(n):
    N=n;d0=N*N+1;d1=N*N+2*N+2;d2=N*N+4*N+5;D=d0*d1*d2
    return {
      2:Fraction(-N*N*(N+1)**2*(N+2),D),
      3:Fraction(N**5+6*N**4+13*N**3+18*N**2+16*N+10,D),
      4:Fraction(2*(N**4+3*N**3+5*N**2+5*N+3),D),
      5:Fraction(2*N*N+5*N+4,d1*d2),
      6:Fraction(1,d2),
    }

def exact_one_value(n):return sum(float(c)*log(n+j) for j,c in exact_one_coefficients(n).items())

def self_test():
    for n in (100,1000,10000):
        assert exact_one_value(n)>0
        assert two_linkage_conditioned(n)>0
        assert honest_two_linkage(n)<0
    assert 5 < 100000**2*exact_one_value(100000)/log(100000) < 8
    assert Fraction(4,5)<Fraction.from_float(two_linkage_conditioned(10000)/log(10000))<Fraction(6,5)
if __name__=="__main__":
    self_test();print("current_target_regressions.py self-test: OK")
