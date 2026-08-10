#!/usr/bin/env python3
"""Exact arithmetic interfaces for the terminal Green contradiction."""
from __future__ import annotations
from fractions import Fraction

def endpoint_balance(counts,increments):
    """Return normalized physical endpoint displacement."""
    if len(counts)!=len(increments):raise ValueError
    total=sum(map(Fraction,counts))
    if total<=0:raise ValueError
    d=len(increments[0]);q=[Fraction(0)]*d
    for c,z in zip(counts,increments):
        for i in range(d):q[i]+=Fraction(c)*z[i]/total
    return tuple(q)

def workload_flux(counts,increments,h):
    q=endpoint_balance(counts,increments)
    return sum(Fraction(a)*b for a,b in zip(h,q))

def upward_rate_linear_bound(channels):
    """Return coefficients C0,C1 with upward total rate <= C0+C1|x|.

    `channels` is an iterable `(source_molecularity, rate, positive_delta)`.
    """
    C0=Fraction(0);C1=Fraction(0)
    for degree,rate,up in channels:
        if not up:continue
        r=Fraction(rate)
        if degree==0:C0+=r
        elif degree==1:C1+=r
        else:raise AssertionError("bimolecular upward channel has degree two")
    return C0,C1

def self_test():
    q=endpoint_balance((2,1),((1,0,0),(-1,1,0)))
    assert q==(Fraction(1,3),Fraction(1,3),0)
    assert workload_flux((2,1),((1,0,0),(-1,1,0)),(1,1,0))==Fraction(2,3)
    assert upward_rate_linear_bound(((0,2,True),(1,3,True),(2,5,False)))==(2,3)
if __name__=="__main__":
    self_test();print("global_green_closure.py self-test: OK")
