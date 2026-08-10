#!/usr/bin/env python3
"""Exact finite source-layer elimination and zero-class cohomology."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict,deque
from typing import Hashable,Sequence

Phase=Hashable

@dataclass(frozen=True,slots=True)
class EffectiveEdge:
    source:Phase
    target:Phase|None
    reward:Fraction
    layer:int
    label:str=""

@dataclass(frozen=True,slots=True)
class LayerClass:
    phases:tuple[Phase,...]
    layer:int
    kind:str       # strict, zero, or exit
    mean_upper:Fraction
    potential:tuple[tuple[Phase,Fraction],...]

def _scc(phases,edges):
    adj={p:[] for p in phases};radj={p:[] for p in phases}
    for e in edges:
        if e.target is not None:
            adj[e.source].append(e.target);radj[e.target].append(e.source)
    seen=set();order=[]
    def f(v):
        seen.add(v)
        for w in adj[v]:
            if w not in seen:f(w)
        order.append(v)
    for p in phases:
        if p not in seen:f(p)
    seen.clear();out=[]
    def g(v,c):
        seen.add(v);c.add(v)
        for w in radj[v]:
            if w not in seen:g(w,c)
    for p in reversed(order):
        if p not in seen:
            c=set();g(p,c);out.append(c)
    return out

def zero_coboundary(phases,edges)->tuple[tuple[Phase,Fraction],...]:
    """For zero cycle sums, find psi with reward+psi(t)-psi(s)=0."""
    und=defaultdict(list)
    for e in edges:
        if e.target is None:continue
        und[e.source].append((e.target,-e.reward))
        und[e.target].append((e.source,e.reward))
    psi={}
    for root in phases:
        if root in psi:continue
        psi[root]=Fraction(0);stack=[root]
        while stack:
            u=stack.pop()
            for v,d in und[u]:
                cand=psi[u]+d
                if v in psi:
                    if psi[v]!=cand:raise ValueError("nonzero reward cycle")
                else:
                    psi[v]=cand;stack.append(v)
    return tuple((p,psi[p]) for p in phases)

def classify_layer(phases:Sequence[Phase],edges:Sequence[EffectiveEdge],layer:int)->tuple[LayerClass,...]:
    current=[e for e in edges if e.layer==layer]
    comps=_scc(phases,current)
    out=[]
    for c in comps:
        internal=[e for e in current if e.source in c and e.target in c]
        outgoing=[e for e in current if e.source in c and (e.target is None or e.target not in c)]
        if outgoing:
            out.append(LayerClass(tuple(sorted(c,key=repr)),layer,"exit",Fraction(0),()))
            continue
        if any(e.reward>0 for e in internal):
            raise ValueError("positive effective edge: faster clearing was incomplete")
        if any(e.reward<0 for e in internal):
            # All rewards are nonpositive; any finite irreducible stationary
            # distribution gives strict negative mean. This exact upper bound
            # records only the sign; compact rate cells provide the margin.
            out.append(LayerClass(tuple(sorted(c,key=repr)),layer,"strict",Fraction(-1),()))
        else:
            pot=zero_coboundary(tuple(c),internal)
            out.append(LayerClass(tuple(sorted(c,key=repr)),layer,"zero",Fraction(0),pot))
    return tuple(out)

def terminate_hierarchy(phases,edges,max_layer):
    trace=[]
    active=set(phases)
    for layer in range(max_layer+1):
        cls=classify_layer(tuple(active),tuple(e for e in edges if e.source in active),layer)
        trace.extend(cls)
        # A strict class closes the current branch; a zero class is carried to
        # the next physical layer. Exits leave the chart.
        next_active=set()
        for c in cls:
            if c.kind=="zero":next_active.update(c.phases)
        active=next_active
        if not active:break
    if active:
        raise ValueError("source hierarchy did not terminate")
    return tuple(trace)

def self_test():
    E=(
        EffectiveEdge(0,1,Fraction(0),0,"fast neutral"),
        EffectiveEdge(1,0,Fraction(0),0,"fast neutral"),
        EffectiveEdge(0,0,Fraction(-1),1,"slow service"),
        EffectiveEdge(1,1,Fraction(-2),1,"slow service"),
    )
    out=terminate_hierarchy((0,1),E,1)
    assert any(c.kind=="zero" and c.layer==0 for c in out)
    assert any(c.kind=="strict" and c.layer==1 for c in out)
    try:
        classify_layer((0,), (EffectiveEdge(0,0,Fraction(1),0),),0)
    except ValueError:
        pass
    else:raise AssertionError
if __name__=="__main__":
    self_test();print("source_layer_hierarchy.py self-test: OK")
