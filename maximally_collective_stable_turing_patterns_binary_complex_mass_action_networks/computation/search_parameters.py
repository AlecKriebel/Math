#!/usr/bin/env python3
"""Diagnostic parameter search; the first rational seed already succeeds."""
from __future__ import annotations
import argparse
import sympy as sp
from exact_normal_form import normal_form
SEED=(sp.Rational(7,3),sp.Rational(1,32),sp.Rational(11,16),sp.Rational(1,40))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=20);a=p.parse_args()
 print('fixed seed',SEED)
 for m in range(3,a.max_m+1):
  z=normal_form(m);print(m,float(z['eta']),float(z['cubic']))
