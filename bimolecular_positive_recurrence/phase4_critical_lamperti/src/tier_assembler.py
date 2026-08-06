#!/usr/bin/env python3
"""Exact Bellman patching for a finite hierarchy of regime certificates."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

@dataclass(frozen=True,slots=True)
class RegimeEdge:
    source:int
    target:int
    reward_upper:Fraction

@dataclass(frozen=True,slots=True)
class BellmanPatch:
    offsets:tuple[Fraction,...]
    margin:Fraction


def bellman_patch(vertex_count:int,edges:Sequence[RegimeEdge],margin:Fraction=Fraction(1))->BellmanPatch:
    """Solve h(v)-h(u) >= reward(u,v)+margin by longest paths.

    Feasible exactly when the edge weights reward+margin have no nonnegative
    directed cycle.  Bellman-Ford on negated weights is implemented with
    Fractions, and the returned offsets are independently checked.
    """
    if vertex_count<=0:raise ValueError('positive vertex count')
    h=[Fraction(0)]*vertex_count
    w=[e.reward_upper+margin for e in edges]
    # Longest-path relaxation. A positive cycle causes an update on pass n.
    for it in range(vertex_count):
      changed=False
      for e,ww in zip(edges,w):
        if h[e.target]<h[e.source]+ww:
          h[e.target]=h[e.source]+ww;changed=True
      if not changed:break
      if it==vertex_count-1:raise ValueError('nonnegative/positive reward cycle prevents Bellman patch')
    # Our desired inequality can be written h[target]-h[source]>=w.
    for e,ww in zip(edges,w):
      if h[e.target]-h[e.source]<ww:raise AssertionError('Bellman verification failed')
    mn=min(h);h=[x-mn for x in h]
    return BellmanPatch(tuple(h),margin)


def hierarchy_exponent(reaction_count:int,species_count:int)->int:
    """A conservative explicit exponent bound for finite priority assembly."""
    if reaction_count<1 or species_count<1:raise ValueError('positive sizes')
    depth=2*reaction_count+species_count+2
    return 4*depth+4


def self_test()->None:
    # Acyclic exits are patchable.
    p=bellman_patch(3,[RegimeEdge(0,1,Fraction(0)),RegimeEdge(1,2,Fraction(-3))])
    assert len(p.offsets)==3
    # Zero reward cycle cannot carry a positive margin.
    try:bellman_patch(2,[RegimeEdge(0,1,Fraction(0)),RegimeEdge(1,0,Fraction(0))])
    except ValueError:pass
    else:raise AssertionError('cycle should fail')

if __name__=='__main__':self_test();print('tier_assembler.py self-test: OK')
