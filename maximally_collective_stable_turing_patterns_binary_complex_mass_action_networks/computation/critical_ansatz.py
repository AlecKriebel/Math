#!/usr/bin/env python3
"""Derive diffusion entries from the affine-chain critical-vector ansatz."""
from __future__ import annotations
import argparse
import sympy as sp
from reconstruct_family import jacobian_factor


def ansatz(m,u,v,p,q):
 r=[1]+[-(u+v*sp.Rational(m-1-i,m-2)) for i in range(2,m)]+[-p,q]
 r=sp.Matrix(r);A=jacobian_factor(m,1,1)
 d=[sp.factor((A*r)[i]/r[i]) for i in range(m+1)]
 expected=[-2+u+p+2*q,
   sp.factor((1+2*p-u-v*sp.Rational(m-3,m-2))/(u+v*sp.Rational(m-3,m-2)))]
 expected += [sp.factor(v/((m-2)*u+v*(m-1-i))) for i in range(3,m)]
 expected += [sp.factor((2*u-5*p-2*q-1)/p),sp.factor((2-2*p-4*q)/q)]
 assert all(sp.factor(x-y)==0 for x,y in zip(d,expected))
 return r,d
if __name__=='__main__':
 p0=argparse.ArgumentParser();p0.add_argument('m',type=int);a=p0.parse_args()
 vals=(sp.Rational(7,3),sp.Rational(1,32),sp.Rational(11,16),sp.Rational(1,40))
 r,d=ansatz(a.m,*vals);print('r=',r.T);print('D=',d)
