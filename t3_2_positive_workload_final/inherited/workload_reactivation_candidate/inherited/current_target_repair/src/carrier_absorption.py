#!/usr/bin/env python3
"""Exact finite carrier absorption and interruption bounds."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict
from typing import Sequence
try:
    from .current_target_bellman import solve
except ImportError:
    from current_target_bellman import solve

@dataclass(frozen=True,slots=True)
class AbsorptionCertificate:
    mean_steps:tuple[Fraction,...]
    service_probabilities:tuple[Fraction,...]
    max_mean_steps:Fraction


def closed_nonservice_scc(P:Sequence[Sequence[Fraction]],service:Sequence[Fraction])->tuple[int,...]|None:
    n=len(P);adj={i:[j for j,p in enumerate(P[i]) if p] for i in range(n)}
    # Tarjan
    idx=0;stack=[];on=set();ind={};low={};comps=[]
    def visit(v):
        nonlocal idx
        ind[v]=low[v]=idx;idx+=1;stack.append(v);on.add(v)
        for w in adj[v]:
            if w not in ind:visit(w);low[v]=min(low[v],low[w])
            elif w in on:low[v]=min(low[v],ind[w])
        if low[v]==ind[v]:
            c=[]
            while True:
                w=stack.pop();on.remove(w);c.append(w)
                if w==v:break
            comps.append(tuple(sorted(c)))
    for v in range(n):
        if v not in ind:visit(v)
    for c in comps:
        C=set(c)
        if all(service[i]==0 and sum(P[i][j] for j in C)==1 for i in c):return c
    return None


def certify(P:Sequence[Sequence[Fraction]],service:Sequence[Fraction])->AbsorptionCertificate:
    """P is the transient carrier-step kernel; service is one-step absorption.

    Rows satisfy sum(P_i)+service_i=1.  Failure exits are omitted only when
    their probability is zero; otherwise they should be included as another
    absorbing outcome in the calling theorem.
    """
    n=len(P)
    for i in range(n):
        if sum(P[i],Fraction(0))+service[i]!=1:raise ValueError('row not stochastic')
    bad=closed_nonservice_scc(P,service)
    if bad is not None:raise ValueError(f'closed nonservice class {bad}')
    A=[[(Fraction(1) if i==j else 0)-P[i][j] for j in range(n)] for i in range(n)]
    t=tuple(solve(A,[Fraction(1)]*n))
    q=tuple(solve(A,list(service)))
    if any(x!=1 for x in q):raise AssertionError(q)
    if any(x<=0 for x in t):raise AssertionError(t)
    return AbsorptionCertificate(t,q,max(t))


def interruption_bound(expected_carrier_steps:Fraction,slow_to_carrier_ratio:Fraction)->Fraction:
    if expected_carrier_steps<0 or slow_to_carrier_ratio<0:raise ValueError
    # Union/compensator bound; may exceed one, so cap.
    return min(Fraction(1),expected_carrier_steps*slow_to_carrier_ratio)


def self_test():
    P=((Fraction(0),Fraction(1,2)),(Fraction(1,3),Fraction(0)))
    s=(Fraction(1,2),Fraction(2,3))
    c=certify(P,s);assert c.service_probabilities==(1,1)
    assert c.max_mean_steps==Fraction(9,5)
    assert interruption_bound(c.max_mean_steps,Fraction(1,100))==Fraction(9,500)

if __name__=='__main__':self_test();print('carrier_absorption.py self-test: OK')
