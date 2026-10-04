#!/usr/bin/env python3
"""Supplementary exact algebraic controls, not a full RUOT solver.

Run with sympy 1.14.0:
    python3 independent_checks.py --output independent_results.json
This program does not read source documents or use the network.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def difference(n):
    d = s.zeros(n)
    for j in range(n):
        d[j,j] += n
        d[j,(j-1)%n] -= n
    return d


def matrix(t,n,nu):
    d=difference(n); e=t*s.eye(n)+nu*d*d.T/2
    a=s.zeros(t*n,(3*t-1)*n)
    for j in range(t):
        if j < t-1:
            a[j*n:(j+1)*n,j*n:(j+1)*n] = e
        if j > 0:
            a[j*n:(j+1)*n,(j-1)*n:j*n] = -t*s.eye(n)
        a[j*n:(j+1)*n,(t-1+j)*n:(t+j)*n] = d
        a[j*n:(j+1)*n,(2*t-1+j)*n:(2*t+j)*n] = -s.eye(n)
    return a,d,e


def controls():
    count=0
    for t in [1,2,4]:
        for n in [1,2,3]:
            for nu in [s.Integer(0),s.Rational(1,3)]:
                a,d,e=matrix(t,n,nu)
                g=a*a.T
                expected=s.zeros(t*n)
                for j in range(t):
                    diag=s.eye(n)+d*d.T
                    if j<t-1: diag += e*e
                    if j>0: diag += t*t*s.eye(n)
                    expected[j*n:(j+1)*n,j*n:(j+1)*n] = diag
                    if j<t-1:
                        expected[j*n:(j+1)*n,(j+1)*n:(j+2)*n] = -t*e
                        expected[(j+1)*n:(j+2)*n,j*n:(j+1)*n] = -t*e
                assert g==expected
                assert a[:,(2*t-1)*n:]==-s.eye(t*n)
                assert s.ones(1,n)*d==s.zeros(1,n)
                assert s.ones(1,n)*e==t*s.ones(1,n)
                # Exact Gram identity proves positive definiteness without an eigenvalue tolerance.
                rest=a[:,:((2*t-1)*n)]
                assert g-s.eye(t*n)==rest*rest.T
                count += 1

    # Affine feasibility does not preserve positivity, even with positive endpoints.
    a,_,_=matrix(2,1,s.Integer(1))
    x=s.Matrix([-10,0,0,0,0]); rhs=s.Matrix([2,-2])
    projected=x-a.T*(a*a.T).inv()*(a*x-rhs)
    assert a*projected==rhs
    assert projected[0]==-s.Rational(2,9)
    assert projected==s.Matrix([-s.Rational(2,9),0,0,-s.Rational(22,9),s.Rational(22,9)])

    # Exact Hessian/radial degeneracy for the binary perspective.
    rho,nu,lam=s.symbols('rho nu lam',positive=True)
    m,z=s.symbols('m z',real=True)
    psi=lambda r: nu*(r*s.asinh(r/lam)-s.sqrt(lam**2+r**2)+lam)
    f=m*m/(2*rho)+rho*psi(z/rho)
    h=s.hessian(f,(rho,m,z))
    radial=s.Matrix([rho,m,z])
    assert all(s.simplify(v)==0 for v in h*radial)

    # The local projection derivative needs a square, even for negative inputs.
    tau=s.symbols('tau',nonnegative=True)
    c=s.symbols('c',real=True)
    q=s.Function('q')(tau)
    hp=lam*s.sinh(q/nu); hpp=lam*s.cosh(q/nu)/nu
    qprime=-hp/(1+tau*hpp)
    chain=s.diff(nu*lam*(s.cosh(q/nu)-1),tau).subs(s.diff(q,tau),qprime)
    assert s.simplify(chain+hp**2/(1+tau*hpp))==0

    # Nontrivial exact tight dual witness for one weighted cell and B=I.
    weight=s.Integer(3)
    u=s.Matrix([1,2,1])
    y=weight*s.Matrix([-1-s.sqrt(2),2,s.asinh(1)])
    kval=s.simplify((y[0]/weight+(y[1]/weight)**2/2+s.cosh(y[2]/weight)-1).rewrite(s.exp))
    value=weight*(s.Integer(2)+s.asinh(1)-s.sqrt(2)+1)
    assert kval==0
    assert s.simplify(value-(u.T*y)[0])==0

    # Exact small-growth coefficient confirms the quartic constant is sharp at zero.
    r=s.symbols('r',real=True)
    gap=nu*r*r/(2*lam)-psi(r)
    coefficient=s.simplify(s.diff(gap,r,4).subs(r,0)/s.factorial(4))
    assert coefficient==nu/(24*lam**3)

    return {
        'result':'PASS',
        'sympy_version':s.__version__,
        'exact_grid_cases':count,
        'exact_grid_controls':['temporal boundary blocks','free-source full row rank',
                               'mass telescoping','Gram lower bound by identity'],
        'negative_density_projection':{'T':2,'N':1,'endpoints':[1,1],
                                       'input_density':-10,'projected_density':str(projected[0]),
                                       'exactly_affine_feasible':True},
        'binary_hessian_scaling_null_direction':'exact identity',
        'corrected_H_of_prox_derivative':'exact identity',
        'weighted_nonzero_tight_dual_witness':'exact identity',
        'quartic_surrogate_leading_coefficient':str(coefficient),
        'scope':'Finite exact algebraic controls only. They do not establish continuum convergence, a general algorithm, or floating-point certification.'
    }

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path); args=p.parse_args()
    result=json.dumps(controls(),indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(result)
    print(result,end='')
