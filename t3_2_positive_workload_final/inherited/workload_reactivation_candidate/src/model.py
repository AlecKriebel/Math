#!/usr/bin/env python3
"""Exact finite stochastic mass-action model for the T3-2 repair."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import factorial
from typing import Iterable, Sequence

Complex = tuple[int, ...]
State = tuple[int, ...]

def falling(n:int,k:int)->int:
    if k<0: raise ValueError
    if n<k:return 0
    out=1
    for j in range(k):out*=n-j
    return out

def source_factor(x:Sequence[int],y:Sequence[int])->int:
    if len(x)!=len(y):raise ValueError
    out=1
    for a,b in zip(x,y):
        out*=falling(a,b)
        if not out:return 0
    return out

@dataclass(frozen=True,slots=True)
class Channel:
    source:Complex
    target:Complex
    rate:Fraction=Fraction(1)
    name:str=""
    linkage:int=0
    def __post_init__(self):
        if len(self.source)!=len(self.target):raise ValueError
        if self.rate<=0:raise ValueError
        if sum(self.source)>2 or sum(self.target)>2:raise ValueError("not bimolecular")
    @property
    def vector(self)->Complex:
        return tuple(b-a for a,b in zip(self.source,self.target))
    @property
    def delta_molecularity(self)->int:
        return sum(self.target)-sum(self.source)
    def enabled(self,x:Sequence[int])->bool:
        return all(a>=b for a,b in zip(x,self.source))
    def propensity(self,x:Sequence[int])->Fraction:
        return self.rate*source_factor(x,self.source)
    def fire(self,x:Sequence[int])->State:
        if not self.enabled(x):raise ValueError
        return tuple(a+v for a,v in zip(x,self.vector))

def dot(h:Sequence[int|Fraction],x:Sequence[int])->Fraction:
    return sum((Fraction(a)*b for a,b in zip(h,x)),Fraction(0))

def complexes(channels:Iterable[Channel])->tuple[Complex,...]:
    c={r.source for r in channels}|{r.target for r in channels}
    return tuple(sorted(c))

def is_weakly_reversible(channels:Iterable[Channel])->bool:
    rs=tuple(channels)
    C=complexes(rs)
    adj={c:set() for c in C}
    radj={c:set() for c in C}
    for r in rs:
        adj[r.source].add(r.target)
        radj[r.target].add(r.source)
    for link in {r.linkage for r in rs}:
        nodes={r.source for r in rs if r.linkage==link}|{r.target for r in rs if r.linkage==link}
        if not nodes:continue
        root=next(iter(nodes))
        for graph in (adj,radj):
            seen={root};stack=[root]
            while stack:
                v=stack.pop()
                for w in graph[v]:
                    if w in nodes and w not in seen:
                        seen.add(w);stack.append(w)
            if seen!=nodes:return False
    return True

def exact_total_rate(x:State,channels:Iterable[Channel])->Fraction:
    return sum((r.propensity(x) for r in channels),Fraction(0))

def factorial_weight(x:State)->Fraction:
    den=1
    for v in x:den*=factorial(v)
    return Fraction(1,den)

def self_test():
    assert falling(5,2)==20 and falling(1,2)==0
    r=Channel((1,0,0),(1,1,0),Fraction(3,2),"r",0)
    assert r.propensity((4,7,0))==6
    assert r.fire((4,7,0))==(4,8,0)
    cyc=(Channel((0,),(1,),linkage=0),Channel((1,),(0,),linkage=0))
    assert is_weakly_reversible(cyc)
if __name__=="__main__":
    self_test();print("model.py self-test: OK")
