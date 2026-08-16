#!/usr/bin/env python3
"""Exact normal-form computation for the rational seed."""
from __future__ import annotations
import argparse
import sympy as sp
from reconstruct_family import jacobian_factor, conservation_vector, hessian_bilinear_from_reactions


def seed_data(m: int):
    if m < 3:
        raise ValueError
    A = jacobian_factor(m, sp.Integer(1), sp.Integer(1))
    u=sp.Rational(7,3); v=sp.Rational(1,32); p=sp.Rational(11,16); q=sp.Rational(1,40)
    r=[sp.Integer(1)]
    for i in range(2,m):
        r.append(-(u+v*sp.Rational(m-1-i,m-2)))
    r.extend([-p,q])
    r=sp.Matrix(r)
    d=[sp.Rational(257,240)]
    d.append(sp.Rational(m+1,227*m-457))
    for i in range(3,m):
        d.append(sp.Rational(3,227*m-451-3*i))
    d.extend([sp.Rational(43,165),sp.Integer(21)])
    D=sp.diag(*d)
    # left vector from exact nullspace, normalized ell_Z=1
    ell=A.T-D
    ns=ell.nullspace()
    if len(ns)!=1:
        raise RuntimeError(f"left nullity {len(ns)}")
    ell=sp.simplify(ns[0]/ns[0][-1])
    c=conservation_vector(m)
    return A,D,r,ell,c


def solve_w0(A: sp.Matrix, rhs: sp.Matrix, c: sp.Matrix):
    n=A.rows
    aug=A.row_join(c)
    bottom=c.T.row_join(sp.zeros(1,1))
    K=aug.col_join(bottom)
    sol=K.inv()*rhs.col_join(sp.Matrix([0]))
    return sp.simplify(sol[:n,0])


def normal_form(m: int):
    A,D,r,ell,c=seed_data(m)
    Brr=hessian_bilinear_from_reactions(m,r,r)
    rhs=-sp.Rational(1,4)*Brr
    w0=solve_w0(A,rhs,c)
    w2=sp.simplify((A-4*D).inv()*rhs)
    eta=sp.factor((ell.T*D*r)[0]/(ell.T*r)[0])
    cubic_vec=hessian_bilinear_from_reactions(m,r,w0)+sp.Rational(1,2)*hessian_bilinear_from_reactions(m,r,w2)
    cubic=sp.factor((ell.T*cubic_vec)[0]/(ell.T*r)[0])
    checks={
        "critical": sp.simplify((A-D)*r)==sp.zeros(m+1,1),
        "left": sp.simplify((A-D).T*ell)==sp.zeros(m+1,1),
        "compat": sp.simplify((c.T*Brr)[0])==0,
        "w0": sp.simplify(A*w0-rhs)==sp.zeros(m+1,1) and sp.simplify((c.T*w0)[0])==0,
        "w2": sp.simplify((A-4*D)*w2-rhs)==sp.zeros(m+1,1),
    }
    return dict(A=A,D=D,r=r,ell=ell,c=c,Brr=Brr,w0=w0,w2=w2,eta=eta,cubic=cubic,checks=checks)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('m',type=int)
    ap.add_argument('--vectors',action='store_true')
    args=ap.parse_args()
    out=normal_form(args.m)
    print('checks',out['checks'])
    print('eta =',out['eta'])
    print('c =',out['cubic'])
    print('eta decimal',sp.N(out['eta'],16),'c decimal',sp.N(out['cubic'],16))
    if args.vectors:
        for key in ['r','ell','Brr','w0','w2']:
            print(key,'=',out[key].T)

if __name__=='__main__':
    main()
