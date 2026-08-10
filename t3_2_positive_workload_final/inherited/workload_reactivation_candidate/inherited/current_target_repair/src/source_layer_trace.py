#!/usr/bin/env python3
"""Exact finite-priority return-prefix and carrier-clearing certificates.

The module verifies finite algebra used by the source-layer theorem.  It does
not infer stochastic recurrence from enumeration.  Priorities are integers:
larger source priority means asymptotically faster physical propensity.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict, deque
from typing import Hashable, Iterable, Mapping, Sequence

Node=Hashable

@dataclass(frozen=True,slots=True)
class Edge:
    source:Node
    target:Node
    source_priority:int
    workload_change:int
    label:str=''

@dataclass(frozen=True,slots=True)
class ReturnPrefix:
    activation:int
    path:tuple[int,...]
    endpoint:Node
    total_reward:int
    minimum_source_priority:int


def adjacency(edges:Sequence[Edge])->dict[Node,list[tuple[int,Node]]]:
    out:dict[Node,list[tuple[int,Node]]]=defaultdict(list)
    for i,e in enumerate(edges):out[e.source].append((i,e.target))
    return out


def return_prefix(edges:Sequence[Edge],activation:int)->ReturnPrefix:
    """Find a path from the positive edge's target back to its source.

    The graph must be strongly connected and source priorities must be the
    workload values of source nodes (up to an order-preserving scalarization).
    We stop at the first node whose priority is no larger than the activation
    source priority.  Every prefix source is then strictly faster.
    """
    e=edges[activation]
    if e.workload_change<=0:raise ValueError('activation must have positive reward')
    alpha=e.source_priority
    adj=adjacency(edges)
    # BFS in the induced set of nodes with priority > alpha, allowing the
    # terminal source as the final endpoint.
    q=deque([e.target]);parent:dict[Node,tuple[Node,int]|None]={e.target:None};end=None
    while q:
        u=q.popleft()
        # A target at/below alpha completes the credit.  The initial target is
        # strictly above alpha because reward is positive.
        if node_priority(u,edges)<=alpha:
            end=u;break
        for idx,v in adj.get(u,[]):
            if v not in parent:
                parent[v]=(u,idx);q.append(v)
    if end is None:raise ValueError('no return prefix found')
    rev=[];v=end
    while parent[v] is not None:
        u,idx=parent[v];rev.append(idx);v=u
    path=tuple(reversed(rev))
    if not path:raise AssertionError('positive edge target cannot already be at/below source')
    total=e.workload_change+sum(edges[i].workload_change for i in path)
    mins=min(edges[i].source_priority for i in path)
    if mins<=alpha:
        # The final edge source is still above alpha; only its target may fall.
        raise AssertionError((alpha,mins,path))
    if total>0:raise AssertionError((total,path))
    return ReturnPrefix(activation,path,end,total,mins)


def node_priority(node:Node,edges:Sequence[Edge])->int:
    vals={e.source_priority for e in edges if e.source==node}
    if not vals:
        # A weakly reversible complex is a source.  Isolated test nodes are
        # rejected rather than assigned an artificial priority.
        raise ValueError(f'node {node!r} has no outgoing edge')
    if len(vals)!=1:raise ValueError('source priority must be node-defined')
    return next(iter(vals))


def strongly_connected(nodes:Iterable[Node],edges:Sequence[Edge])->bool:
    nodes=tuple(nodes);adj=adjacency(edges);radj=adjacency(tuple(Edge(e.target,e.source,node_priority(e.target,edges),-e.workload_change,e.label) for e in edges))
    def reach(A,start):
        seen={start};st=[start]
        while st:
            u=st.pop()
            for _,v in A.get(u,[]):
                if v not in seen:seen.add(v);st.append(v)
        return seen
    return bool(nodes) and len(reach(adj,nodes[0]))==len(nodes) and len(reach(radj,nodes[0]))==len(nodes)


def first_changing_sign(edges:Sequence[Edge])->tuple[int,tuple[int,...]]:
    changing=[(i,e) for i,e in enumerate(edges) if e.workload_change]
    if not changing:raise ValueError('no changing edge')
    alpha=max(e.source_priority for _,e in changing)
    top=tuple(i for i,e in changing if e.source_priority==alpha)
    if any(edges[i].workload_change>0 for i in top):
        raise AssertionError('a positive top changing edge contradicts its return prefix')
    if not any(edges[i].workload_change<0 for i in top):raise AssertionError('no strict edge')
    return alpha,top

@dataclass(frozen=True,slots=True)
class CreditDriftBound:
    success_probability:Fraction
    service_amount:Fraction
    maximum_failure_arrival:Fraction
    expected_credit_change:Fraction


def credit_drift_bound(success_probability:Fraction,service_amount:Fraction,maximum_failure_arrival:Fraction)->CreditDriftBound:
    """One-trial workload-credit drift.

    Success removes at least ``service_amount``.  Failure leaves the old
    credit and adds at most ``maximum_failure_arrival``; relative to the
    pre-trial credit the increment is therefore bounded by that arrival.
    """
    if not (0<success_probability<=1):raise ValueError('bad probability')
    if service_amount<=0 or maximum_failure_arrival<0:raise ValueError('bad amounts')
    drift=-success_probability*service_amount+(1-success_probability)*maximum_failure_arrival
    return CreditDriftBound(success_probability,service_amount,maximum_failure_arrival,drift)


def trials_to_clear_bound(initial_credit:Fraction,bound:CreditDriftBound)->Fraction:
    if initial_credit<0:raise ValueError('negative credit')
    if bound.expected_credit_change>=0:raise ValueError('no negative drift')
    return initial_credit/(-bound.expected_credit_change)


def sccs(nodes:Iterable[Node],edges:Sequence[Edge])->list[set[Node]]:
    nodes=tuple(nodes);adj=adjacency(edges);index=0;stack=[];on=set();ind={};low={};out=[]
    def visit(v):
        nonlocal index
        ind[v]=low[v]=index;index+=1;stack.append(v);on.add(v)
        for _,w in adj.get(v,[]):
            if w not in ind:visit(w);low[v]=min(low[v],low[w])
            elif w in on:low[v]=min(low[v],ind[w])
        if low[v]==ind[v]:
            c=set()
            while True:
                w=stack.pop();on.remove(w);c.add(w)
                if w==v:break
            out.append(c)
    for v in nodes:
        if v not in ind:visit(v)
    return out


def zero_sccs(nodes:Iterable[Node],edges:Sequence[Edge])->tuple[frozenset[Node],...]:
    out=[]
    for c in sccs(nodes,edges):
        internal=[e for e in edges if e.source in c and e.target in c]
        if internal and all(e.workload_change==0 for e in internal):out.append(frozenset(c))
    return tuple(out)


def self_test()->None:
    # Positive lower edge 0->2, faster return 2->1->0.
    E=(Edge(0,2,0,2,'birth'),Edge(2,1,2,-1,'service1'),Edge(1,0,1,-1,'service2'))
    assert strongly_connected((0,1,2),E)
    p=return_prefix(E,0)
    assert p.path==(1,2) and p.total_reward==0 and p.minimum_source_priority==1
    alpha,top=first_changing_sign(E)
    assert alpha==2 and top==(1,)
    b=credit_drift_bound(Fraction(99,100),Fraction(1),Fraction(2))
    assert b.expected_credit_change==Fraction(-97,100)
    assert trials_to_clear_bound(Fraction(5),b)==Fraction(500,97)

if __name__=='__main__':self_test();print('source_layer_trace.py self-test: OK')
