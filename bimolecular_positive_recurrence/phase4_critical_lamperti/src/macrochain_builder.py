#!/usr/bin/env python3
"""Exact finite-phase level generators for declared defect shells.

The builder is intentionally explicit.  A model declares a finite list of
complex nodes, the defect phase occupied by each node, and the exact
falling-factorial multiplier left after the level variable n is separated.
It then constructs the CTMC phase generator and the first two level reward
rates over Q(n).  This is the representation used by the exact shell audits.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence
import sympy as sp

@dataclass(frozen=True,slots=True)
class ShellNode:
    name:str
    phase:int
    q:int
    defect_factor:int=1

@dataclass(frozen=True,slots=True)
class ShellEdge:
    source:int
    target:int
    rate:Fraction=Fraction(1)

@dataclass(frozen=True,slots=True)
class MacroGenerator:
    n:sp.Symbol
    Q:sp.Matrix
    first_reward_rate:sp.Matrix
    second_reward_rate:sp.Matrix


def build_shell_generator(nodes:Sequence[ShellNode],edges:Sequence[ShellEdge],phase_count:int,n:sp.Symbol|None=None)->MacroGenerator:
    n=n or sp.symbols('n',positive=True,integer=True)
    Q=sp.zeros(phase_count);d=sp.zeros(phase_count,1);v=sp.zeros(phase_count,1)
    for e in edges:
      s=nodes[e.source];t=nodes[e.target]
      if s.q not in (0,1):raise ValueError('safe shell q must be 0 or 1')
      rr=sp.Rational(e.rate.numerator,e.rate.denominator)*s.defect_factor*(n if s.q else 1)
      r=t.q-s.q
      d[s.phase]+=rr*r;v[s.phase]+=rr*r*r
      if s.phase!=t.phase:Q[s.phase,t.phase]+=rr
    for i in range(phase_count):Q[i,i]=-sum(Q[i,j] for j in range(phase_count) if j!=i)
    return MacroGenerator(n,Q,d,v)


def stationary_ctmc(Q:sp.Matrix)->tuple[sp.Expr,...]:
    m=Q.rows
    A=Q.T.copy();A[m-1,:]=sp.ones(1,m)
    b=sp.zeros(m,1);b[m-1]=1
    sol=A.inv()*b
    vals=tuple(sp.factor(sol[i]) for i in range(m))
    if any(sp.simplify(sum(vals[i]*Q[i,j] for i in range(m)))!=0 for j in range(m)):raise AssertionError('stationary check')
    return vals


def stationary_reward(model:MacroGenerator)->tuple[sp.Expr,sp.Expr]:
    pi=stationary_ctmc(model.Q)
    d=sp.factor(sum(pi[i]*model.first_reward_rate[i] for i in range(len(pi))))
    v=sp.factor(sum(pi[i]*model.second_reward_rate[i] for i in range(len(pi))))
    return d,v


def self_test()->None:
    # Two phases: q0 C births q1 A+D, q1 returns q0.  Reward average is zero.
    nodes=[ShellNode('C',0,0),ShellNode('AD',1,1)]
    edges=[ShellEdge(0,1,Fraction(2)),ShellEdge(1,0,Fraction(3))]
    g=build_shell_generator(nodes,edges,2)
    d,v=stationary_reward(g)
    assert sp.simplify(d)==0 and v>0

if __name__=='__main__':self_test();print('macrochain_builder.py self-test: OK')
