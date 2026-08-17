#!/usr/bin/env python3
"""Derive the vector field and unit-equilibrium Jacobian from reactions."""
from __future__ import annotations
import argparse
from reconstruct_family import vector_field,jacobian_factor
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('m',type=int);a=p.parse_args()
 x,f=vector_field(a.m);print('variables=',x);print('f=');print(f);print('A=');print(jacobian_factor(a.m))
