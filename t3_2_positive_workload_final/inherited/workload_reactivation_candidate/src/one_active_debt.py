#!/usr/bin/env python3
"""Exact one-active polynomial-rate interfaces."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Hashable,Sequence

Phase=Hashable

@dataclass(frozen=True,slots=True)
class PolynomialEdge:
    source_phase:Phase
    target_phase:Phase|None
    level_increment:int
    c2:Fraction=Fraction(0)
    c1:Fraction=Fraction(0)
    c0:Fraction=Fraction(0)
    label:str=""
    def __post_init__(self):
        if min(self.c2,self.c1,self.c0)<0:raise ValueError
        if abs(self.level_increment)>2:raise ValueError
    def rate(self,n:int)->Fraction:
        if n<0:raise ValueError
        return self.c2*n*(n-1)+self.c1*n+self.c0

def coefficients_for_channel(source:tuple[int,int,int],rate:Fraction,b:int,c:int):
    """Exact A-polynomial propensity at fixed bounded B,C."""
    a=source[0]
    f=Fraction(rate)
    # bounded source factor
    def fall(n,k):
        if n<k:return 0
        out=1
        for j in range(k):out*=n-j
        return out
    f*=fall(b,source[1])*fall(c,source[2])
    if a==2:return (f,Fraction(0),Fraction(0))
    if a==1:return (Fraction(0),f,Fraction(0))
    if a==0:return (Fraction(0),Fraction(0),f)
    raise ValueError

def verify_bimolecular_sign(source:tuple[int,int,int],target:tuple[int,int,int],two_a_present:bool):
    if sum(source)>2 or sum(target)>2:raise ValueError
    k=target[0]-source[0]
    if source==(2,0,0):
        if k>=0:raise AssertionError("genuine 2A reaction must lower A")
    if not two_a_present and source[0]==1 and k>0:
        raise AssertionError("without 2A, a degree-one source cannot increase A")
    if source[0]==0 and k>1:
        raise AssertionError("bounded source creates at most one A")
    return k

def quadratic_drift_bound(edges:Sequence[PolynomialEdge]):
    c2=sum((-e.level_increment)*e.c2 for e in edges if e.level_increment<0)
    up1=sum(e.level_increment*e.c1 for e in edges if e.level_increment>0)
    up0=sum(e.level_increment*e.c0 for e in edges if e.level_increment>0)
    if c2<=0:raise ValueError("no quadratic descent")
    return c2,up1,up0

def q1_reward_sign(edges:Sequence[PolynomialEdge]):
    for e in edges:
        if e.c1 and e.level_increment>0:
            raise AssertionError("positive degree-one reward")
    return True

def service_token_vector(complexes:Sequence[tuple[int,int,int]]):
    """q_A in {0,1}: return strict or the exact A-service-token invariant."""
    q1=[y for y in complexes if y[0]==1]
    if any(sum(y)==1 for y in q1):
        return ("strict",None)
    K={j for y in q1 for j in (1,2) if y[j]}
    if any(y[0]==0 and any(y[j] for j in K) for y in complexes):
        return ("strict",None)
    w=[1,0,0]
    for j in K:w[j]-=1
    for y in complexes:
        if y[0] not in (0,1):raise ValueError("safe one-active reduction required")
        if y[0]==1 and sum(y[j] for j in K)!=1:raise AssertionError
        if y[0]==0 and sum(y[j] for j in K)!=0:raise AssertionError
    return ("invariant",tuple(w))

def self_test():
    assert coefficients_for_channel((1,1,0),Fraction(3),2,7)==(0,6,0)
    assert coefficients_for_channel((0,1,1),Fraction(2),2,3)==(0,0,12)
    verify_bimolecular_sign((2,0,0),(1,0,1),True)
    verify_bimolecular_sign((1,1,0),(0,1,0),False)
    e=(PolynomialEdge(0,0,-1,Fraction(2)),PolynomialEdge(0,0,1,c1=Fraction(3),c0=Fraction(4)))
    assert quadratic_drift_bound(e)==(Fraction(2),Fraction(3),Fraction(4))
    q1_reward_sign((PolynomialEdge(0,0,-1,c1=1),PolynomialEdge(0,0,0,c1=2)))
    kind,w=service_token_vector(((0,0,0),(1,1,0)))
    assert kind=="invariant" and w==(1,-1,0)
if __name__=="__main__":
    self_test();print("one_active_debt.py self-test: OK")
