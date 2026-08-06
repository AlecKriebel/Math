#!/usr/bin/env python3
"""Exact absorption probabilities, rewards, and durations for finite CTMCs."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable,Sequence
import sympy as sp

@dataclass(frozen=True,slots=True)
class AbsorptionCertificate:
    transient: tuple[int,...]
    absorbing: tuple[int,...]
    probabilities: sp.Matrix
    expected_time: tuple[sp.Expr,...]
    expected_reward: tuple[sp.Expr,...]


def ctmc_absorption(Q:Sequence[Sequence[object]], absorbing:Iterable[int], reward_rate:Sequence[object]|None=None)->AbsorptionCertificate:
    M=sp.Matrix(Q); n=M.rows
    if M.cols!=n:raise ValueError('Q square')
    if any(sp.simplify(sum(M[i,j] for j in range(n)))!=0 for i in range(n)):raise ValueError('Q rows')
    A=tuple(sorted(set(absorbing)));T=tuple(i for i in range(n) if i not in A)
    QT=M.extract(T,T); QR=M.extract(T,A)
    if QT.det()==0:raise ValueError('transient block singular')
    N=-QT.inv(); B=sp.simplify(N*QR); times=N*sp.ones(len(T),1)
    rr=sp.zeros(len(T),1) if reward_rate is None else sp.Matrix([sp.sympify(reward_rate[i]) for i in T])
    rewards=N*rr
    if any(sp.simplify(sum(B[i,j] for j in range(len(A)))-1)!=0 for i in range(len(T))):
      raise AssertionError('absorption probabilities do not sum to one')
    return AbsorptionCertificate(T,A,B,tuple(sp.factor(x) for x in times),tuple(sp.factor(x) for x in rewards))


def self_test()->None:
    Q=[[-2,1,1],[0,-3,3],[0,0,0]]
    c=ctmc_absorption(Q,{2})
    assert c.probabilities==sp.ones(2,1)
    assert c.expected_time==(sp.Rational(2,3),sp.Rational(1,3))

if __name__=='__main__':self_test();print('exact_absorption.py self-test: OK')
