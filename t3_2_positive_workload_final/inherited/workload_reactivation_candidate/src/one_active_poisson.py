#!/usr/bin/env python3
"""Exact finite-phase stationary distribution and Poisson corrector."""
from __future__ import annotations
from fractions import Fraction
from typing import Sequence

def solve_linear(A,b):
    A=[list(map(Fraction,row))+[Fraction(v)] for row,v in zip(A,b)]
    n=len(A);m=len(A[0])-1;row=0;piv=[]
    for col in range(m):
        p=next((i for i in range(row,n) if A[i][col]),None)
        if p is None:continue
        A[row],A[p]=A[p],A[row]
        z=A[row][col];A[row]=[v/z for v in A[row]]
        for i in range(n):
            if i!=row and A[i][col]:
                z=A[i][col];A[i]=[A[i][j]-z*A[row][j] for j in range(m+1)]
        piv.append(col);row+=1
    for i in range(row,n):
        if all(A[i][j]==0 for j in range(m)) and A[i][m]:raise ValueError("inconsistent")
    x=[Fraction(0)]*m
    for i,c in enumerate(piv):x[c]=A[i][m]
    return tuple(x)

def stationary(P:Sequence[Sequence[Fraction]]):
    n=len(P)
    A=[[Fraction(P[j][i])-(1 if i==j else 0) for j in range(n)] for i in range(n)]
    A[-1]=[Fraction(1)]*n
    b=[Fraction(0)]*(n-1)+[Fraction(1)]
    pi=solve_linear(A,b)
    if any(v<0 for v in pi) or sum(pi)!=1:raise ValueError
    return pi

def poisson(P,reward):
    n=len(P);pi=stationary(P)
    mean=sum(pi[i]*Fraction(reward[i]) for i in range(n))
    A=[[(1 if i==j else 0)-Fraction(P[i][j]) for j in range(n)] for i in range(n)]
    b=[Fraction(reward[i])-mean for i in range(n)]
    A[-1]=[Fraction(0)]*n;A[-1][0]=1;b[-1]=0
    h=solve_linear(A,b)
    for i in range(n):
        lhs=sum(((1 if i==j else 0)-Fraction(P[i][j]))*h[j] for j in range(n))
        if i!=n-1 and lhs!=Fraction(reward[i])-mean:raise AssertionError
    return pi,mean,h

def corrected_variance(P,edge_reward,h):
    pi=stationary(P);n=len(P);v=Fraction(0)
    for i in range(n):
        for j in range(n):
            inc=Fraction(edge_reward[i][j])+h[j]-h[i]
            v+=pi[i]*Fraction(P[i][j])*inc*inc
    return v

def self_test():
    P=((Fraction(1,2),Fraction(1,2)),(Fraction(1,3),Fraction(2,3)))
    pi,mean,h=poisson(P,(Fraction(-1),Fraction(0)))
    assert pi==(Fraction(2,5),Fraction(3,5)) and mean==Fraction(-2,5)
    # A zero-mean nonzero-variance chain is not an invariant.
    Q=((Fraction(0),Fraction(1)),(Fraction(1),Fraction(0)))
    edge=((0,1),(-1,0))
    h0=(Fraction(0),Fraction(0))
    assert corrected_variance(Q,edge,h0)==1
if __name__=="__main__":
    self_test();print("one_active_poisson.py self-test: OK")
