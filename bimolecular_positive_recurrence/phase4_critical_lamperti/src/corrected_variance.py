#!/usr/bin/env python3
"""Exact corrected increment moments and Lamperti coefficient Xi."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import sympy as sp
from .poisson_corrector import stationary_distribution, solve_poisson


def _matrix(a): return sp.Matrix([[sp.Rational(x) for x in row] for row in a])

@dataclass(frozen=True, slots=True)
class CorrectedMomentCertificate:
    stationary: tuple[sp.Rational,...]
    leading_mean: sp.Rational
    corrector: tuple[sp.Rational,...]
    a_by_state: tuple[sp.Expr,...]
    v_by_state: tuple[sp.Expr,...]
    a: sp.Expr
    v: sp.Expr
    xi: sp.Expr


def corrected_moments(
    P0: Sequence[Sequence[object]],
    P1: Sequence[Sequence[object]],
    reward0: Sequence[Sequence[object]],
    reward1: Sequence[Sequence[object]]|None=None,
)->CorrectedMomentCertificate:
    """Compute a,v,Xi for P_n=P0+P1/n+O(n^-2).

    reward0[i][j] is the O(1) level increment conditional on i->j and
    reward1 the coefficient of 1/n.  Entries with P0=P1=0 may be arbitrary.
    The critical formula is intended when the leading stationary mean is zero,
    but the routine reports it in all cases.
    """
    P=_matrix(P0); Q=_matrix(P1); R=_matrix(reward0)
    S=sp.zeros(*R.shape) if reward1 is None else _matrix(reward1)
    n=P.rows
    if P.cols!=n or Q.shape!=(n,n) or R.shape!=(n,n) or S.shape!=(n,n):
        raise ValueError('dimension mismatch')
    d0=[sp.factor(sum(P[i,j]*R[i,j] for j in range(n))) for i in range(n)]
    pc=solve_poisson(P,d0)
    h=pc.corrector; pi=pc.stationary
    z=[[sp.factor(R[i,j]+h[j]-h[i]) for j in range(n)] for i in range(n)]
    # First correction to corrected mean.  Q row sums must be zero.
    if any(sp.simplify(sum(Q[i,j] for j in range(n)))!=0 for i in range(n)):
        raise ValueError('rows of P1 must sum to zero')
    a_i=[];v_i=[]
    for i in range(n):
        a_i.append(sp.factor(sum(Q[i,j]*z[i][j]+P[i,j]*S[i,j] for j in range(n))))
        v_i.append(sp.factor(sum(P[i,j]*z[i][j]**2 for j in range(n))))
    a=sp.factor(sum(pi[i]*a_i[i] for i in range(n)))
    v=sp.factor(sum(pi[i]*v_i[i] for i in range(n)))
    xi=sp.factor(2*a+v)
    return CorrectedMomentCertificate(pi,pc.mean_reward,h,tuple(a_i),tuple(v_i),a,v,xi)


def self_test()->None:
    # Symmetric +/-1 phase-independent walk: a=0,v=1,Xi=1.
    P0=[[sp.Rational(1,2),sp.Rational(1,2)],[sp.Rational(1,2),sp.Rational(1,2)]]
    P1=[[0,0],[0,0]]
    R=[[-1,1],[-1,1]]
    c=corrected_moments(P0,P1,R)
    assert c.leading_mean==0 and c.v==1 and c.xi==1

if __name__=='__main__':
    self_test();print('corrected_variance.py self-test: OK')
