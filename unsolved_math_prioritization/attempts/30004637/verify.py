#!/usr/bin/env python3
"""Deterministic, small regression checks; not an interval or continuum proof.

Run: python3 verify.py --output checks.json
Dependencies: numpy and sympy. No network, downloads, or external source files.
"""
import argparse
import json
import math
import platform
from pathlib import Path

import numpy as np
import sympy as sp


def H(c, nu, lam):
    return nu * lam * (math.cosh(c / nu) - 1)


def Hp(c, nu, lam):
    return lam * math.sinh(c / nu)


def psi(r, nu, lam):
    return nu * (r * math.asinh(r / lam) - math.hypot(lam, r) + lam)


def inner_prox(c, tau, nu, lam):
    lo, hi = min(0.0, c), max(0.0, c)
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid + tau * Hp(mid, nu, lam) > c:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def project_K(a, b, c, nu, lam):
    b = np.asarray(b, dtype=float)
    h0 = a + float(b @ b) / 2 + H(c, nu, lam)
    if h0 <= 0:
        return np.r_[a, b, c], 0.0
    lo, hi = 0.0, h0
    for _ in range(80):
        tau = (lo + hi) / 2
        cc = inner_prox(c, tau, nu, lam)
        h = a - tau + float(b @ b) / (2 * (1 + tau)**2) + H(cc, nu, lam)
        if h > 0:
            lo = tau
        else:
            hi = tau
    tau = (lo + hi) / 2
    return np.r_[a - tau, b / (1 + tau), inner_prox(c, tau, nu, lam)], tau


def derivatives_check():
    r, nu, lam = sp.symbols('r nu lam', real=True, positive=True)
    P = nu * (r * sp.asinh(r / lam) - sp.sqrt(lam**2 + r**2) + lam)
    assert sp.simplify(sp.diff(P, r) - nu * sp.asinh(r / lam)) == 0
    assert sp.simplify(sp.diff(P, r, 2) - nu / sp.sqrt(lam**2 + r**2)) == 0
    rho, m, z = sp.symbols('rho m z', real=True, positive=True)
    # Positive symbols suffice for the algebraic identity; numerical checks include negative m,z.
    f = m*m/(2*rho) + rho * P.subs(r, z/rho)
    v, rr = m/rho, z/rho
    v1, v2 = sp.Matrix([-v, 1, 0]), sp.Matrix([-rr, 0, 1])
    target = (v1*v1.T + nu/sp.sqrt(lam**2 + rr**2)*(v2*v2.T))/rho
    err = sp.hessian(f, (rho,m,z))-target
    assert all(sp.simplify(x)==0 for x in err)
    s,q = sp.symbols('s q')
    G=q*s/(1-(1-q)*s)
    assert sp.simplify(sp.diff(G,s,2)-2*q*(1-q)/(1-(1-q)*s)**3)==0
    return {'legendre_derivatives':'exact symbolic identity',
            'perspective_hessian':'exact symbolic identity',
            'yule_second_derivative':'exact symbolic identity'}


def local_checks(rng):
    records=[]
    max_boundary=max_stationarity=max_moreau=0.0
    outside=inside=0
    for nu,lam in [(0.5,0.3),(1.0,1.0),(2.0,3.0)]:
        for d in [1,2,4]:
            cases=[(-5.0,np.zeros(d),0.0),(0.0,np.zeros(d),0.0),
                   (1.0,np.zeros(d),0.0),(0.1,np.ones(d),-1.2)]
            for _ in range(12):
                cases.append((float(rng.uniform(-3,3)),rng.uniform(-2,2,d),
                              float(rng.uniform(-2,2))))
            for a,b,c in cases:
                x=np.r_[a,b,c]
                p,tau=project_K(a,b,c,nu,lam)
                g=p[0]+float(p[1:-1]@p[1:-1])/2+H(p[-1],nu,lam)
                if tau==0:
                    inside+=1
                    assert np.array_equal(x,p) and g<=1e-14
                    continue
                outside+=1
                normal=np.r_[1.0,p[1:-1],Hp(p[-1],nu,lam)]
                stationary=np.linalg.norm(x-p-tau*normal)
                max_boundary=max(max_boundary,abs(g))
                max_stationarity=max(max_stationarity,float(stationary))
                u=x-p  # gamma=1 Moreau identity; rho=tau>0
                rho=u[0]; v=u[1:-1]/rho; rr=u[-1]/rho
                grad=np.r_[-float(v@v)/2+psi(rr,nu,lam)-rr*nu*math.asinh(rr/lam),
                            v,nu*math.asinh(rr/lam)]
                moreau=np.linalg.norm(grad-p)/(1+np.linalg.norm(p))
                max_moreau=max(max_moreau,float(moreau))
                assert abs(g)<2e-11 and stationary<2e-11 and moreau<2e-10
    return {'cases':inside+outside,'inside':inside,'outside':outside,
            'max_abs_boundary_residual':max_boundary,
            'max_KKT_stationarity_residual':max_stationarity,
            'max_relative_Moreau_gradient_residual':max_moreau}


def difference(N):
    D=np.zeros((N,N))
    for j in range(N):
        D[j,j]+=N
        D[j,(j-1)%N]-=N
    return D


def unpack(u,T,N):
    n=(T-1)*N
    return u[:n].reshape(T-1,N),u[n:n+T*N].reshape(T,N),u[n+T*N:].reshape(T,N)


def apply_A(u,T,N,nu):
    rho,m,z=unpack(u,T,N)
    D=difference(N); E=T*np.eye(N)+(nu/2)*(D@D.T)
    out=m@D.T-z
    if T>1:
        out[:-1]+=rho@E.T
        out[1:]-=T*rho
    return out


def apply_At(y,T,N,nu):
    D=difference(N); E=T*np.eye(N)+(nu/2)*(D@D.T)
    rho=y[:-1]@E-T*y[1:]
    return np.r_[rho.ravel(),(y@D).ravel(),(-y).ravel()]


def tridiagonal(diag,off,rhs):
    a=np.array(diag,dtype=float,copy=True)
    b=np.array(rhs,dtype=complex,copy=True)
    n=len(a)
    for j in range(1,n):
        assert a[j-1]>0
        factor=off[j-1]/a[j-1]
        a[j]-=factor*off[j-1]
        b[j]-=factor*b[j-1]
    assert np.all(a>0)
    out=np.empty(n,dtype=complex)
    out[-1]=b[-1]/a[-1]
    for j in range(n-2,-1,-1):
        out[j]=(b[j]-off[j]*out[j+1])/a[j]
    return out


def solve_AAt(rhs,T,N,nu):
    transformed=np.fft.fft(rhs,axis=1)
    sol=np.empty_like(transformed)
    for k in range(N):
        ell=4*N*N*math.sin(math.pi*k/N)**2
        e=T+nu*ell/2
        diag=np.full(T,1+ell,dtype=float)
        if T>1:
            diag[:-1]+=e*e
            diag[1:]+=T*T
        off=np.full(T-1,-T*e,dtype=float)
        sol[:,k]=tridiagonal(diag,off,transformed[:,k])
    out=np.fft.ifft(sol,axis=1)
    assert np.max(np.abs(out.imag))<1e-10
    return out.real


def grid_checks(rng):
    maximum={'relative_dense_projection_error':0.,'relative_feasibility_error':0.,
             'relative_idempotence_error':0.,'relative_symbol_solve_error':0.}
    cases=0
    for T in [1,2,3,5]:
        for N in [1,2,3,5,8]:
            for nu in [0.,0.2,1.5]:
                cases+=1
                dim=(3*T-1)*N
                basis=np.eye(dim)
                A=np.column_stack([apply_A(basis[j],T,N,nu).ravel() for j in range(dim)])
                G=A@A.T
                assert np.min(np.linalg.eigvalsh(G))>1-2e-10
                x=rng.standard_normal(dim)
                rho0=rng.uniform(.2,2,N); rhoT=rng.uniform(.2,2,N)
                D=difference(N); E=T*np.eye(N)+(nu/2)*(D@D.T)
                b=np.zeros((T,N)); b[0]+=T*rho0; b[-1]-=E@rhoT
                rhs=apply_A(x,T,N,nu)-b
                y=solve_AAt(rhs,T,N,nu)
                proj=x-apply_At(y,T,N,nu)
                dense=x-A.T@np.linalg.solve(G,rhs.ravel())
                feas=apply_A(proj,T,N,nu)-b
                proj_again=proj-apply_At(solve_AAt(feas,T,N,nu),T,N,nu)
                vals={'relative_dense_projection_error':np.linalg.norm(proj-dense)/(1+np.linalg.norm(dense)),
                      'relative_feasibility_error':np.linalg.norm(feas)/(1+np.linalg.norm(b)),
                      'relative_idempotence_error':np.linalg.norm(proj_again-proj)/(1+np.linalg.norm(proj)),
                      'relative_symbol_solve_error':np.linalg.norm(G@y.ravel()-rhs.ravel())/(1+np.linalg.norm(rhs))}
                for k,v in vals.items():
                    maximum[k]=max(maximum[k],float(v)); assert v<2e-10,(T,N,nu,k,v)
    return {'cases':cases,**maximum,
            'boundary_cases':['T=1','N=1','nu=0'],
            'note':'No positivity assertion for the affine projection.'}


def surrogate_checks():
    max_bound_ratio=0.0
    for nu,lam in [(0.5,0.3),(1.,1.),(2.,3.)]:
        for r in [-100.,-10.,-3.,-1.,-.1,0.,.1,1.,3.,10.,100.]:
            Q=nu*r*r/(2*lam); gap=Q-psi(r,nu,lam); upper=nu*r**4/(24*lam**3)
            assert gap>=-1e-12 and gap<=upper+1e-11
            if upper: max_bound_ratio=max(max_bound_ratio,gap/upper)
    ratios={str(r):psi(r,1,1)/(r*r/2) for r in [1,10,100,1000,10000]}
    assert all(a>b for a,b in zip(ratios.values(),list(ratios.values())[1:]))
    return {'cases':33,'max_gap_to_quartic_bound_ratio':max_bound_ratio,
            'psi_over_quadratic_nu_lambda_one':ratios,
            'note':'Finite checks support, but do not prove, the analytic bound or limit.'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rng=np.random.default_rng(30004637)
    result={'problem_id':30004637,'seed':30004637,'result':'PASS',
            'scope':'Symbolic identities and finite floating-point regression checks only; no full solver or interval proof.',
            'versions':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__},
            'symbolic':derivatives_check(),'local_proximal':local_checks(rng),
            'affine_projection':grid_checks(rng),'quadratic_surrogate':surrogate_checks()}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')


if __name__=='__main__': main()
