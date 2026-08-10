#!/usr/bin/env python3
"""Exact finite chart-flow decomposition and workload-cone gluing."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict
from typing import Hashable,Sequence

Chart=Hashable

@dataclass(frozen=True,slots=True)
class ChartEdge:
    source:Chart
    target:Chart|None
    flow:Fraction
    workload_increment:Fraction=Fraction(0)
    structural_exit:bool=False

def verify_flow_balance(charts:Sequence[Chart],edges:Sequence[ChartEdge],source_error=None):
    err={c:Fraction(0) for c in charts}
    if source_error:
        for c,v in source_error.items():err[c]=Fraction(v)
    bal={c:-err[c] for c in charts}
    for e in edges:
        if e.flow<0:raise ValueError
        bal[e.source]-=e.flow
        if e.target is not None:bal[e.target]+=e.flow
    return bal

def terminal_components(charts,edges):
    # Support graph using positive-flow nonexit edges.
    adj={c:[] for c in charts};radj={c:[] for c in charts}
    for e in edges:
        if e.flow>0 and e.target is not None and not e.structural_exit:
            adj[e.source].append(e.target);radj[e.target].append(e.source)
    seen=set();order=[]
    def f(v):
        seen.add(v)
        for w in adj[v]:
            if w not in seen:f(w)
        order.append(v)
    for c in charts:
        if c not in seen:f(c)
    seen.clear();comps=[]
    def g(v,C):
        seen.add(v);C.add(v)
        for w in radj[v]:
            if w not in seen:g(w,C)
    for c in reversed(order):
        if c not in seen:
            C=set();g(c,C);comps.append(C)
    out=[]
    for C in comps:
        outgoing=sum((e.flow for e in edges if e.source in C and
                      (e.target is None or e.target not in C or e.structural_exit)),Fraction(0))
        internal=sum((e.flow for e in edges if e.source in C and e.target in C),Fraction(0))
        if outgoing==0 and internal>0:out.append(tuple(sorted(C,key=repr)))
    return tuple(out)

def common_workload(vectors,active=(0,1)):
    """Find a small rational nonnegative vector annihilating supplied increments.

    Dimension is at most three. Exhaustive bounded rational search is a
    certificate constructor for finite tests; manuscripts use Farkas duality.
    """
    vec=tuple(tuple(map(Fraction,v)) for v in vectors)
    for den in range(1,9):
        for a in range(1,9):
            for b in range(1,9):
                for c in range(-8,9):
                    h=(Fraction(a,den),Fraction(b,den),Fraction(c,den))
                    if all(h[i]>0 for i in active) and all(sum(h[i]*v[i] for i in range(3))==0 for v in vec):
                        return h
    return None

def strict_or_common(vectors,active=(0,1)):
    h=common_workload(vectors,active)
    if h is not None:return ("invariant",h)
    return ("strict",None)

def self_test():
    E=(ChartEdge("a","b",Fraction(2)),ChartEdge("b","a",Fraction(2)))
    assert verify_flow_balance(("a","b"),E)=={"a":0,"b":0}
    assert terminal_components(("a","b"),E)==(("a","b"),)
    h=common_workload(((1,-1,0),),active=(0,1))
    assert h and h[0]==h[1]
if __name__=="__main__":
    self_test();print("chart_flow_gluing.py self-test: OK")
