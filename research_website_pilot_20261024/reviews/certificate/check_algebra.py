#!/usr/bin/env python3
"""Exact Q(sqrt(2)) checks of displayed algebra, plus labeled decimal diagnostics."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
import json

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y): return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sc(a,x): return (a*x[0],a*x[1])

def run():
    one=(F(1),F(0));k=(F(0),F(1,2));A=(F(1),F(1));C=add(one,k)
    rt=(F(-2,7),F(3,7));rg=(F(6,7),F(-2,7));degree=(F(24,7),F(-1,7))
    checks={
     'branch_fixed_point':mul(k,add(sc(2,one),sc(2,k)))==add(one,sc(2,k)),
     'A_identity':A==add(one,sc(2,k)),
     'A_upper_fixed_point':mul(A,add(one,A))==add(mul(C,add(one,A)),A),
     'R_tree':mul(rt,add(one,sc(3,k)))==one,
     'R_grandparent':mul(rg,add(sc(3,one),sc(2,k)))==sc(2,one),
     'degree_sum':add(sc(3,rt),sc(5,rg))==degree,
    }
    if not all(checks.values()): raise RuntimeError(checks)
    with localcontext() as c:
        c.prec=65
        g=(Decimal(24)-Decimal(2).sqrt())/Decimal(7)
        h=Decimal(3208526010913748780)/Decimal(10**18)
        return {'status':'PASS','exact_Q_sqrt2_equation_checks':checks,
                'decimal_diagnostics_only':{'G_expected_degree':str(g),'H_certified_upper_bound':str(h),
                'degree_gap_lower_bound':str(g-h),'bF_gap_lower_bound':str((g-h)/2)}}
if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
