#!/usr/bin/env python3
"""Finite SCC classification of Q2 and Q1 one-active layers."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from .one_active_generator import OneActiveGenerator,Phase

@dataclass(frozen=True,slots=True)
class LayerClass:
    phases: tuple[Phase,...]
    recurrent: bool
    has_negative_reward: bool
    has_positive_reward: bool


def scc(nodes,edges):
    adj={v:[] for v in nodes}
    for a,b in edges:
        if b is not None:adj[a].append(b)
    idx=0;st=[];on=set();ind={};low={};out=[]
    def visit(v):
        nonlocal idx
        ind[v]=low[v]=idx;idx+=1;st.append(v);on.add(v)
        for w in adj[v]:
            if w not in ind:visit(w);low[v]=min(low[v],low[w])
            elif w in on:low[v]=min(low[v],ind[w])
        if low[v]==ind[v]:
            c=[]
            while True:
                w=st.pop();on.remove(w);c.append(w)
                if w==v:break
            out.append(tuple(sorted(c)))
    for v in nodes:
        if v not in ind:visit(v)
    return out


def classify_layer(g:OneActiveGenerator,degree:int)->tuple[LayerClass,...]:
    es=[t for t in g.transitions if t.degree==degree and t.coefficient>0]
    comps=scc(g.phases,[(t.source_phase,t.target_phase) for t in es])
    cid={p:i for i,c in enumerate(comps) for p in c}
    classes=[]
    for i,c in enumerate(comps):
        outgoing=any(t.target_phase is None or cid.get(t.target_phase)!=i for t in es if t.source_phase in c)
        rewards=[t.level_jump for t in es if t.source_phase in c and t.target_phase in c]
        classes.append(LayerClass(c,not outgoing,any(r<0 for r in rewards),any(r>0 for r in rewards)))
    return tuple(classes)


def verify_bimolecular_sign(g:OneActiveGenerator)->None:
    for t in g.transitions:
        if t.degree==2 and t.level_jump>=0:
            raise AssertionError('genuine 2A edge is not strictly negative')
        if t.degree==1 and t.level_jump>0:
            raise AssertionError('linear source increases A although 2A is absent/removed')


def self_test()->None:
    from .model import Channel
    from .one_active_generator import build
    ch=(Channel('birth',(0,0,0),(1,1,0)),Channel('death',(1,1,0),(0,1,0)))
    g=build(ch,1,0)
    verify_bimolecular_sign(g)
    cls=classify_layer(g,1)
    assert any(c.has_negative_reward for c in cls)

if __name__=='__main__':self_test();print('one_active_phase_classifier.py self-test: OK')


def service_token_alternative(complexes, active_index: int = 0):
    """Structural one-active strict-service/global-invariant dichotomy.

    Assumes every complex has active count 0 or 1 (the 2A branch is handled
    separately).  Returns ('strict', witness) or ('invariant', vector).
    """
    d=len(complexes[0])
    q1=[y for y in complexes if y[active_index]==1]
    q0=[y for y in complexes if y[active_index]==0]
    if any(sum(y)==1 for y in q1):
        return ('strict', ('unary', next(y for y in q1 if sum(y)==1)))
    service=set()
    for y in q1:
        outside=[i for i in range(d) if i!=active_index and y[i]]
        if len(outside)!=1 or y[outside[0]]!=1:
            raise ValueError('q1 complex is not unary or A+D')
        service.add(outside[0])
    for y in q0:
        for j in service:
            if y[j]:
                # The corresponding A+D source is enabled over this lower
                # terminal after target following.
                top=next(z for z in q1 if z[j])
                return ('strict', ('service', top, y))
    w=[0]*d;w[active_index]=1
    for j in service:w[j]-=1
    for y in complexes:
        if sum(w[i]*y[i] for i in range(d))!=0:
            raise AssertionError('claimed service-token invariant fails')
    return ('invariant',tuple(w))
