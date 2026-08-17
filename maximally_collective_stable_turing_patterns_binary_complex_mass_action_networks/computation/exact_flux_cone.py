#!/usr/bin/env python3
"""Exact positive steady-flux cone reconstruction."""
from __future__ import annotations
import argparse
import sympy as sp
from reconstruct_family import matrices


def verify(m:int)->None:
    G,_=matrices(m)
    e=sp.Matrix([1]*m+[0,0]);p=sp.Matrix([0]*m+[1,1])
    E=sp.Matrix.hstack(e,p)
    assert G.rank()==m and len(G.nullspace())==2
    assert G*E==sp.zeros(m+1,2)
    assert all(E.gauss_jordan_solve(v)[1].rows==0 for v in G.nullspace())
    print(f'ker Gamma_{m}=span{{(1_m,0,0),(0_m,1,1)}}; positive cone=(a1_m,b,b)')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('m',type=int);a=p.parse_args();verify(a.m)
