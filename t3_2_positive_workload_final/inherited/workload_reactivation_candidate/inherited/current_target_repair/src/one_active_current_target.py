#!/usr/bin/env python3
"""Exact creator-service paths for the one-active-coordinate reduction."""
from __future__ import annotations
from collections import defaultdict,deque
from dataclasses import dataclass
from typing import Iterable,Sequence
try:
    from .model import Channel,Complex
except ImportError:
    from model import Channel,Complex

@dataclass(frozen=True,slots=True)
class CreatorService:
    birth_channel:int
    path:tuple[int,...]
    death_channel:int


def qA(y:Complex,active:int=0)->int:return y[active]


def linkage_paths(channels:Sequence[Channel],active:int=0)->tuple[CreatorService,...]:
    """For every qA=0 -> qA=1 birth find its creator-linkage q1 prefix death.

    Assumes no complex has two active particles.  Strong connectivity of each
    linkage supplies a path back to the birth source.  Truncating at the first
    q1->q0 edge yields the required service prefix.
    """
    by_link:dict[int,list[int]]=defaultdict(list)
    for i,e in enumerate(channels):by_link[e.linkage].append(i)
    out=[]
    for bi,b in enumerate(channels):
        if qA(b.source,active)!=0 or qA(b.target,active)!=1:continue
        inds=by_link[b.linkage];adj:dict[Complex,list[tuple[int,Complex]]]=defaultdict(list)
        for i in inds:adj[channels[i].source].append((i,channels[i].target))
        start=b.target;goal=b.source;q=deque([start]);parent={start:None};found=None
        while q:
            u=q.popleft()
            for i,v in adj[u]:
                if qA(u,active)==1 and qA(v,active)==0:
                    # first service crossing; no need to continue to the exact
                    # birth source.
                    parent[v]=(u,i);found=v;q.clear();break
                if qA(v,active)==1 and v not in parent:
                    parent[v]=(u,i);q.append(v)
            if found is not None:break
        if found is None:raise ValueError(f'no q1-to-q0 service path for {b.name}')
        rev=[];v=found
        while parent[v] is not None:
            u,i=parent[v];rev.append(i);v=u
        path=tuple(reversed(rev));death=path[-1]
        if any(qA(channels[i].source,active)!=1 for i in path):raise AssertionError(path)
        if channels[death].displacement[active]!=-1:raise AssertionError(channels[death])
        out.append(CreatorService(bi,path,death))
    return tuple(out)


def service_token_invariant(complexes:Iterable[Complex],active:int=0):
    C=tuple(complexes);d=len(C[0]);q1=[y for y in C if y[active]==1];q0=[y for y in C if y[active]==0]
    if any(sum(y)==1 for y in q1):return None
    K=set()
    for y in q1:
        outside=[i for i in range(d) if i!=active and y[i]]
        if len(outside)!=1 or y[outside[0]]!=1:return None
        K.add(outside[0])
    if any(any(y[j] for j in K) for y in q0):return None
    w=[0]*d;w[active]=1
    for j in K:w[j]-=1
    vals={sum(w[i]*y[i] for i in range(d)) for y in C}
    if vals!={0}:raise AssertionError((C,w,vals))
    return tuple(w)


def self_test()->None:
    ch=(
      Channel('birth',(0,0),(1,1),linkage=0),
      Channel('neutral',(1,1),(1,0),linkage=0),
      Channel('death',(1,0),(0,0),linkage=0),
    )
    p=linkage_paths(ch);assert len(p)==1 and p[0].path==(1,2)
    inv=service_token_invariant(((0,0),(1,1)),0);assert inv==(1,-1)
    assert service_token_invariant(((0,0),(1,0)),0) is None

if __name__=='__main__':self_test();print('one_active_current_target.py self-test: OK')
