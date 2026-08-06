#!/usr/bin/env python3
"""Exact stationary distributions and Poisson correctors for finite chains."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence
import sympy as sp


def _M(a: Sequence[Sequence[object]] | sp.MatrixBase) -> sp.Matrix:
    if isinstance(a, sp.MatrixBase):
        return sp.Matrix(a)
    return sp.Matrix([[sp.Rational(x) for x in row] for row in a])


@dataclass(frozen=True, slots=True)
class PoissonCertificate:
    stationary: tuple[sp.Rational, ...]
    mean_reward: sp.Rational
    corrector: tuple[sp.Rational, ...]


def stationary_distribution(P: Sequence[Sequence[object]]) -> tuple[sp.Rational, ...]:
    M=_M(P); n=M.rows
    if M.cols!=n: raise ValueError('P must be square')
    if any(sp.simplify(sum(M[i,j] for j in range(n))-1)!=0 for i in range(n)):
        raise ValueError('rows of P must sum to one')
    A=(M.T-sp.eye(n)); A[n-1,:]=sp.ones(1,n)
    b=sp.zeros(n,1); b[n-1]=1
    sol=A.inv()*b if A.det()!=0 else sp.linsolve((A,b))
    if isinstance(sol,sp.MatrixBase): vals=tuple(sp.factor(sol[i]) for i in range(n))
    else:
        S=list(sol)
        if len(S)!=1: raise ValueError('stationary distribution not unique')
        tup=S[0]
        free=sorted(set().union(*(x.free_symbols for x in tup)),key=str)
        if free: raise ValueError('stationary distribution not unique')
        vals=tuple(sp.factor(x) for x in tup)
    if any(v<0 for v in vals): raise ValueError('negative stationary entry')
    if any(sp.simplify(sum(vals[i]*M[i,j] for i in range(n))-vals[j])!=0 for j in range(n)):
        raise AssertionError('stationary verification failed')
    return vals


def solve_poisson(
    P: Sequence[Sequence[object]],
    conditional_reward: Sequence[object],
    normalization_state: int=0,
) -> PoissonCertificate:
    M=_M(P); n=M.rows
    d=sp.Matrix([sp.Rational(x) for x in conditional_reward])
    if d.rows!=n: raise ValueError('reward dimension mismatch')
    pi=stationary_distribution(P)
    b=sp.factor(sum(pi[i]*d[i] for i in range(n)))
    # (I-P)h=d-b, h[normalization_state]=0.
    A=sp.eye(n)-M; rhs=d-sp.ones(n,1)*b
    A[normalization_state,:]=sp.zeros(1,n); A[normalization_state,normalization_state]=1
    rhs[normalization_state]=0
    h=A.inv()*rhs if A.det()!=0 else None
    if h is None: raise ValueError('Poisson system singular after normalization')
    vals=tuple(sp.factor(h[i]) for i in range(n))
    for i in range(n):
        lhs=vals[i]-sum(M[i,j]*vals[j] for j in range(n))
        if sp.simplify(lhs-(d[i]-b))!=0:
            raise AssertionError('Poisson equation verification failed')
    return PoissonCertificate(pi,sp.Rational(b),vals)


def self_test()->None:
    P=[[Fraction(1,2),Fraction(1,2)],[Fraction(1,3),Fraction(2,3)]]
    d=[1,-1]
    c=solve_poisson(P,d)
    assert c.stationary==(sp.Rational(2,5),sp.Rational(3,5))
    assert c.mean_reward==sp.Rational(-1,5)

if __name__=='__main__':
    self_test(); print('poisson_corrector.py self-test: OK')
