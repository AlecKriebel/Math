#!/usr/bin/env python3
"""Exact integer reward-cycle classification and coboundary certificates."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Iterable, Sequence

Vertex = Hashable


@dataclass(frozen=True, slots=True)
class RewardEdge:
    source: Vertex
    target: Vertex
    reward: int
    label: str = ""


@dataclass(frozen=True, slots=True)
class CoboundaryCertificate:
    potential: tuple[tuple[Vertex, int], ...]


@dataclass(frozen=True, slots=True)
class NonzeroCycleCertificate:
    edges: tuple[int, ...]
    total_reward: int


def _simple_cycles(vertices: Sequence[Vertex], edges: Sequence[RewardEdge]):
    """Deterministic DFS enumeration; intended for modest certificate graphs."""
    adj={v:[] for v in vertices}
    order={v:i for i,v in enumerate(vertices)}
    for idx,e in enumerate(edges): adj[e.source].append((e.target,idx))
    for v in adj: adj[v].sort(key=lambda p:(order[p[0]],p[1]))
    for root in vertices:
        path=[root]; used={root}; edge_path=[]
        def dfs(v):
            for w,idx in adj[v]:
                if order[w] < order[root]: continue
                if w==root:
                    yield tuple(edge_path+[idx])
                elif w not in used:
                    used.add(w);path.append(w);edge_path.append(idx)
                    yield from dfs(w)
                    edge_path.pop();path.pop();used.remove(w)
        yield from dfs(root)


def classify_reward_cycles(vertices: Iterable[Vertex], edges: Sequence[RewardEdge]):
    vertices=tuple(vertices)
    for cyc in _simple_cycles(vertices,edges):
        r=sum(edges[i].reward for i in cyc)
        if r!=0:
            return NonzeroCycleCertificate(cyc,r)
    # All directed cycles have zero reward.  On each weakly reachable component,
    # path sums are independent and yield reward = h(target)-h(source).
    adj={v:[] for v in vertices}
    for idx,e in enumerate(edges):
        adj[e.source].append((e.target,e.reward))
        adj[e.target].append((e.source,-e.reward))
    h={}
    for root in vertices:
        if root in h: continue
        h[root]=0; stack=[root]
        while stack:
            v=stack.pop()
            for w,r in adj[v]:
                val=h[v]+r
                if w in h:
                    if h[w]!=val: raise AssertionError("cycle enumeration missed nonzero cycle")
                else:
                    h[w]=val;stack.append(w)
    cert=CoboundaryCertificate(tuple((v,h[v]) for v in vertices))
    verify_coboundary(edges,cert)
    return cert


def verify_coboundary(edges: Sequence[RewardEdge], cert: CoboundaryCertificate) -> None:
    h=dict(cert.potential)
    for e in edges:
        if e.reward != h[e.target]-h[e.source]:
            raise AssertionError("invalid coboundary potential")


def self_test() -> None:
    vs=(0,1,2)
    es=(RewardEdge(0,1,1),RewardEdge(1,2,-1),RewardEdge(2,0,0))
    c=classify_reward_cycles(vs,es)
    assert isinstance(c,CoboundaryCertificate)
    es2=es+(RewardEdge(0,2,1),)
    c2=classify_reward_cycles(vs,es2)
    assert isinstance(c2,NonzeroCycleCertificate) and c2.total_reward!=0


if __name__=="__main__":
    self_test();print("reward_cycle.py self-test: OK")
