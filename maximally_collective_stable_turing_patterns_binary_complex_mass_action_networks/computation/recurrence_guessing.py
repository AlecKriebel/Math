#!/usr/bin/env python3
"""Reproduce the exact recurrences used after symbolic discovery."""
from __future__ import annotations
import argparse
import sympy as sp
from closed_form import L,Tfactor
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('m',type=int);a=p.parse_args();m=a.m
 for i in range(3,m):
  lhs=sp.factor(Tfactor(m,i)/Tfactor(m,i-1))
  rhs=sp.factor(L(m,i)/L(m,i-4))
  assert lhs==rhs;print(f'T_{i}/T_{i-1} =',lhs)
 print('telescoping recurrence verified')
