#!/usr/bin/env python3
"""Uniform exact 1/n expansions of rational finite kernels."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import sympy as sp

@dataclass(frozen=True,slots=True)
class KernelExpansion:
    variable: sp.Symbol
    coefficients: tuple[sp.Matrix,...]
    remainder_orders: tuple[tuple[int,...],...]


def expand_at_infinity(matrix: Sequence[Sequence[sp.Expr]], n: sp.Symbol, order:int=2)->KernelExpansion:
    if order<0:raise ValueError('order must be nonnegative')
    M=sp.Matrix(matrix); coeff=[sp.zeros(*M.shape) for _ in range(order+1)]
    rem=[]
    t=sp.symbols('_t', positive=True)
    for i in range(M.rows):
      rr=[]
      for j in range(M.cols):
        expr=sp.cancel(M[i,j].subs(n,1/t))
        ser=sp.series(expr,t,0,order+1).removeO().expand()
        for k in range(order+1):coeff[k][i,j]=sp.factor(ser.coeff(t,k))
        rr.append(order+1)
      rem.append(tuple(rr))
    # Independent row-sum checks for stochastic kernels.
    if all(sp.simplify(sum(M[i,j] for j in range(M.cols))-1)==0 for i in range(M.rows)):
      if any(sp.simplify(sum(coeff[0][i,j] for j in range(M.cols))-1)!=0 for i in range(M.rows)):
        raise AssertionError('P0 row sums failed')
      for k in range(1,order+1):
        if any(sp.simplify(sum(coeff[k][i,j] for j in range(M.cols)))!=0 for i in range(M.rows)):
          raise AssertionError(f'P{k} row sums failed')
    return KernelExpansion(n,tuple(coeff),tuple(rem))


def self_test()->None:
    n=sp.symbols('n',positive=True)
    P=[[n/(n+1),1/(n+1)],[2/(n+2),n/(n+2)]]
    e=expand_at_infinity(P,n,2)
    assert e.coefficients[0]==sp.eye(2)
    assert e.coefficients[1]==sp.Matrix([[-1,1],[2,-2]])

if __name__=='__main__':self_test();print('kernel_expansion.py self-test: OK')
