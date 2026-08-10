#!/usr/bin/env python3
"""Exact workload-return-prefix regressions for failed activation examples."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
try:
    from .model import Channel
    from .source_layer_trace import Edge,return_prefix,first_changing_sign
except ImportError:
    from model import Channel
    from source_layer_trace import Edge,return_prefix,first_changing_sign


def workload(y,h):return sum(Fraction(a)*b for a,b in zip(h,y))

def as_priority_edges(channels,h):
    # Clear denominators in workload values.
    vals=[workload(e.source,h) for e in channels]+[workload(e.target,h) for e in channels]
    den=1
    from math import gcd
    for v in vals:den=den*v.denominator//gcd(den,v.denominator)
    return tuple(Edge(e.source,e.target,int(den*workload(e.source,h)),int(den*workload(e.target,h)-den*workload(e.source,h)),e.name) for e in channels)


def regression_one_linkage():
    ch=(Channel('0_2A',(0,),(2,)),Channel('2A_A',(2,),(1,)),Channel('A_0',(1,),(0,)))
    E=as_priority_edges(ch,(1,))
    p=return_prefix(E,0)
    alpha,top=first_changing_sign(E)
    return p,alpha,top


def regression_two_linkage():
    ch=(
      Channel('A_2A',(1,0),(2,0),linkage=0),Channel('2A_A',(2,0),(1,0),linkage=0),
      Channel('0_AB',(0,0),(1,1),linkage=1),Channel('AB_B',(1,1),(0,1),linkage=1),Channel('B_0',(0,1),(0,0),linkage=1),
    )
    E=as_priority_edges(ch,(1,0))
    pos=[i for i,e in enumerate(E) if e.workload_change>0]
    pref=tuple(return_prefix(E,i) for i in pos)
    alpha,top=first_changing_sign(E)
    return pos,pref,alpha,top


def self_test():
    p,a,t=regression_one_linkage();assert p.total_reward==0 and a==2
    pos,pref,a,t=regression_two_linkage();assert len(pos)==2 and all(p.total_reward==0 for p in pref)
    assert a==2 and any(i for i in t if True)

if __name__=='__main__':self_test();print('priority_regressions.py self-test: OK')
