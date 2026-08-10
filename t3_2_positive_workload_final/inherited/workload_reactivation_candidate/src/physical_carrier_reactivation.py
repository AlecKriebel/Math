#!/usr/bin/env python3
"""Finite physical phase classification and service reactivation."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict,deque
from typing import Hashable,Iterable,Sequence

Phase=Hashable

@dataclass(frozen=True,slots=True)
class PhaseEdge:
    source:Phase
    target:Phase|None   # None is a declared structural exit
    workload:int
    label:str=""

@dataclass(frozen=True,slots=True)
class ReturnCertificate:
    positive_edge:int
    path:tuple[int,...]

@dataclass(frozen=True,slots=True)
class ComponentCertificate:
    phases:tuple[Phase,...]
    kind:str            # strict, zero, or exit
    negative_edges:tuple[int,...]
    outgoing_exits:tuple[int,...]

def _scc(phases:Sequence[Phase],edges:Sequence[PhaseEdge])->list[set[Phase]]:
    adj={p:[] for p in phases}
    radj={p:[] for p in phases}
    for e in edges:
        if e.target is not None:
            adj[e.source].append(e.target);radj[e.target].append(e.source)
    seen=set();order=[]
    def dfs(v):
        seen.add(v)
        for w in adj[v]:
            if w not in seen:dfs(w)
        order.append(v)
    for v in phases:
        if v not in seen:dfs(v)
    out=[];seen.clear()
    def dfs2(v,c):
        seen.add(v);c.add(v)
        for w in radj[v]:
            if w not in seen:dfs2(w,c)
    for v in reversed(order):
        if v not in seen:
            c=set();dfs2(v,c);out.append(c)
    return out

def verify_return_certificates(edges:Sequence[PhaseEdge],certs:Sequence[ReturnCertificate])->None:
    by={c.positive_edge:c for c in certs}
    for idx,e in enumerate(edges):
        if e.workload<=0:continue
        if idx not in by:raise AssertionError(f"positive edge {idx} lacks return certificate")
        c=by[idx]
        phase=e.target
        if phase is None:continue
        total=e.workload
        for j in c.path:
            f=edges[j]
            if f.source!=phase:raise AssertionError("return path is not composable")
            total+=f.workload
            phase=f.target
            if phase is None:break
        if phase is not None and total>0:
            raise AssertionError("return prefix does not cancel positive workload")

def classify(phases:Sequence[Phase],edges:Sequence[PhaseEdge],
             certs:Sequence[ReturnCertificate])->tuple[ComponentCertificate,...]:
    verify_return_certificates(edges,certs)
    comps=_scc(phases,edges)
    cid={p:i for i,c in enumerate(comps) for p in c}
    answer=[]
    for i,c in enumerate(comps):
        internal=[];outgoing=[]
        for j,e in enumerate(edges):
            if e.source not in c:continue
            if e.target is None or e.target not in c:outgoing.append(j)
            else:internal.append(j)
        neg=tuple(j for j in internal if edges[j].workload<0)
        pos=tuple(j for j in internal if edges[j].workload>0)
        if outgoing:
            kind="exit"
        elif neg:
            kind="strict"
        else:
            # A closed component without a negative edge cannot contain a
            # positive edge: the positive edge's certified return path remains
            # in the closed component and must contain a negative increment.
            if pos:
                raise AssertionError("closed positive/no-service component")
            kind="zero"
        answer.append(ComponentCertificate(tuple(sorted(c,key=repr)),kind,neg,tuple(outgoing)))
    return tuple(answer)

def service_minorization(*,phase_count:int,path_length:int,
                         minimum_edge_probability:Fraction)->Fraction:
    q=Fraction(minimum_edge_probability)
    if phase_count<1 or path_length<1 or not (0<q<=1):raise ValueError
    # At most phase_count SCC transitions and path_length physical edges per attempt.
    return q**(phase_count*path_length)

def reactivation_alternative(component:ComponentCertificate)->str:
    if component.kind=="strict":return "service"
    if component.kind=="exit":return "structural_exit"
    return "zero_layer"

def self_test():
    # Positive activation, neutral transfer, strict return.
    E=(
        PhaseEdge("idle","high",1,"arrival"),
        PhaseEdge("high","high2",0,"neutral"),
        PhaseEdge("high2","idle",-1,"service"),
    )
    C=(ReturnCertificate(0,(1,2)),)
    out=classify(("idle","high","high2"),E,C)
    assert out[0].kind=="strict"
    # Pure cancellation is zero only after replacing the complete excursion by
    # its effective edge; it is not falsely called strict.
    Z=(PhaseEdge("z","z",0,"cancelled excursion"),)
    assert classify(("z",),Z,())[0].kind=="zero"
    # A positive closed loop without a certified negative return is rejected.
    try:
        classify(("x",),(PhaseEdge("x","x",1),),(ReturnCertificate(0,()),))
    except AssertionError:
        pass
    else:
        raise AssertionError("invalid positive/no-service class accepted")
if __name__=="__main__":
    self_test();print("physical_carrier_reactivation.py self-test: OK")
