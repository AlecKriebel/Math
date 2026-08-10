#!/usr/bin/env python3
"""Exact stationary vectors and Poisson correctors for finite generators."""
from __future__ import annotations
from fractions import Fraction
from typing import Sequence

Matrix=list[list[Fraction]]


def solve_linear(a:Matrix,b:Sequence[Fraction])->list[Fraction]:
    n=len(a);aug=[a[i][:]+[b[i]] for i in range(n)]
    row=0;piv=[]
    for c in range(n):
        p=next((i for i in range(row,n) if aug[i][c]),None)
        if p is None:continue
        aug[row],aug[p]=aug[p],aug[row]
        z=aug[row][c];aug[row]=[v/z for v in aug[row]]
        for i in range(n):
            if i!=row and aug[i][c]:
                z=aug[i][c];aug[i]=[aug[i][j]-z*aug[row][j] for j in range(n+1)]
        piv.append(c);row+=1
    if row<n:raise ValueError('singular')
    return [aug[i][-1] for i in range(n)]


def stationary(q:Matrix)->tuple[Fraction,...]:
    n=len(q)
    # pi Q=0, replace last equation by normalization.
    a=[[q[j][i] for j in range(n)] for i in range(n)]
    a[-1]=[Fraction(1)]*n
    b=[Fraction(0)]*(n-1)+[Fraction(1)]
    return tuple(solve_linear(a,b))


def poisson_corrector(q:Matrix,reward:Sequence[Fraction])->tuple[Fraction,tuple[Fraction,...]]:
    n=len(q);pi=stationary(q)
    mean=sum((pi[i]*reward[i] for i in range(n)),Fraction(0))
    # Q h = mean - reward, h_0=0.
    a=[row[:] for row in q];b=[mean-reward[i] for i in range(n)]
    a[0]=[Fraction(0)]*n;a[0][0]=Fraction(1);b[0]=Fraction(0)
    h=tuple(solve_linear(a,b))
    for i in range(n):
        lhs=sum((q[i][j]*h[j] for j in range(n)),Fraction(0))
        assert lhs==mean-reward[i]
    return mean,h


def corrected_variance(p:Matrix,reward_edge:Sequence[Sequence[Fraction]],h:Sequence[Fraction])->Fraction:
    pi=stationary([[p[i][j]-(Fraction(1) if i==j else Fraction(0)) for j in range(len(p))] for i in range(len(p))])
    return sum((pi[i]*p[i][j]*(reward_edge[i][j]+h[j]-h[i])**2
                for i in range(len(p)) for j in range(len(p))),Fraction(0))


def self_test()->None:
    q=[[Fraction(-1),Fraction(1)],[Fraction(2),Fraction(-2)]]
    pi=stationary(q);assert pi==(Fraction(2,3),Fraction(1,3))
    mean,h=poisson_corrector(q,(Fraction(0),Fraction(-1)))
    assert mean==Fraction(-1,3)

if __name__=='__main__':self_test();print('one_active_poisson.py self-test: OK')
