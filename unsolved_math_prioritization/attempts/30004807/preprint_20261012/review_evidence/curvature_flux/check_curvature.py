#!/usr/bin/env python3
"""Exact independent local metric-derivative checks; no author imports.

This is finite supporting evidence, not a replacement for the analytic proof.
All checks are explicit exceptions and remain active under python -O.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

CHECKS = 0

def same(actual, expected, label):
    global CHECKS
    CHECKS += 1
    if actual != expected:
        raise ValueError(f'{label}: got {actual!r}, expected {expected!r}')


def local_curvature(a, rho, A, B):
    # Independent full-coordinate Christoffel / Ricci / Riemann computation
    # at theta=pi/2 from exact zeroth, first, and second metric derivatives.
    phi = 1 - a/rho
    phip = a/rho**2
    phipp = -2*a/rho**3
    q = (rho+a)/(rho-a)
    N = A+B*q
    Np = -2*a*B/(rho-a)**2
    Npp = 4*a*B/(rho-a)**3
    H = phi**4
    Hp = 4*phi**3*phip
    Hpp = 12*phi**2*phip**2+4*phi**3*phipp
    metric = [-N**2, H, H*rho**2, H*rho**2]
    d = [[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    dd = [[[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    radial_d = [-2*N*Np, Hp, Hp*rho**2+2*H*rho, Hp*rho**2+2*H*rho]
    radial_dd = [-2*(Np**2+N*Npp), Hpp, Hpp*rho**2+4*Hp*rho+2*H, Hpp*rho**2+4*Hp*rho+2*H]
    for i in range(4):
        d[i][i][1] = radial_d[i]
        dd[i][i][1][1] = radial_dd[i]
    # The theta derivative of sin^2(theta) is zero at pi/2;
    # its SECOND derivative -2 is essential, and is retained.
    dd[3][3][2][2] = -2*H*rho**2
    inv = [1/x for x in metric]
    def C(k,i,j):
        return d[j][k][i]+d[i][k][j]-d[i][j][k]
    gamma = [[[Q(1,2)*inv[k]*C(k,i,j) for j in range(4)] for i in range(4)] for k in range(4)]
    dg = [[[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k in range(4):
        for i in range(4):
            for j in range(4):
                for m in range(4):
                    dinv = -d[k][k][m]*inv[k]**2
                    dC = dd[j][k][i][m]+dd[i][k][j][m]-dd[i][j][k][m]
                    dg[k][i][j][m] = Q(1,2)*(dinv*C(k,i,j)+inv[k]*dC)
    ric = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            ric[i][j] = sum(dg[k][i][j][k]-dg[k][i][k][j] for k in range(4))
            ric[i][j] += sum(gamma[k][i][j]*gamma[l][k][l]-gamma[l][i][k]*gamma[k][j][l]
                             for k in range(4) for l in range(4))
    scalar = sum(inv[i]*ric[i][i] for i in range(4))
    mixed = [[inv[i]*ric[i][j]-(Q(1,2)*scalar if i==j else 0)
              for j in range(4)] for i in range(4)]
    rr = rho*phi**2
    coeff = (A/N)*a/rr**3
    target = [0, 4*coeff, -2*coeff, -2*coeff]
    same(scalar, 0, 'scalar curvature')
    for i in range(4):
        for j in range(4):
            same(mixed[i][j], target[i] if i==j else 0, f'mixed Einstein {i},{j}')
    ric_squared = sum(inv[i]*inv[j]*ric[i][j]**2 for i in range(4) for j in range(4))
    same(ric_squared, 24*a**2*(A/N)**2/rr**6, 'Ricci squared')
    kretschmann = Q(0)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    upper = dg[i][l][j][k]-dg[i][k][j][l]
                    upper += sum(gamma[i][k][e]*gamma[e][l][j]-gamma[i][l][e]*gamma[e][k][j] for e in range(4))
                    lower = metric[i]*upper
                    kretschmann += inv[i]*inv[j]*inv[k]*inv[l]*lower**2
    same(kretschmann, 96*a**2*(1+(B*q/N)**2)/rr**6, 'Kretschmann')
    # Densitized radial and angular mixed eigenvalues are independent of B.
    same(N*phi**6*mixed[1][1], 4*A*a/rho**3, 'radial density')
    same(N*phi**6*mixed[2][2], -2*A*a/rho**3, 'angular density')


def cartesian_check(a, x, rho, A):
    same(sum(z*z for z in x), rho*rho, 'Cartesian radius')
    if not rho>a:
        raise ValueError('Expected an interior Cartesian point')
    phi = 1-a/rho
    n = [z/rho for z in x]
    p = [a/rho**2*z for z in n]
    D = [[A*a/rho**3*(6*n[i]*n[j]-2*(i==j)) for j in range(3)] for i in range(3)]
    same(sum(D[i][i] for i in range(3)), 0, 'density trace')
    for k in range(3):
        contraction = sum(D[i][j]*(Q(2)/phi)*((1 if j==i else 0)*p[k]+(1 if j==k else 0)*p[i]-(1 if i==k else 0)*p[j]) for i in range(3) for j in range(3))
        same(contraction, 0, 'complete Cartesian connection contraction')
    # Differentiate the Cartesian expression D^i_j = Aa(6 x_i x_j/rho^5 - 2 delta_ij/rho^3).
    for j in range(3):
        div = sum(A*a*(6*((x[j]+(x[i] if i==j else 0))/rho**5-5*x[i]**2*x[j]/rho**7)
                       +6*(x[i] if i==j else 0)/rho**5) for i in range(3))
        same(div, 0, 'Cartesian density divergence')
    # Exact spatial flux at the inner sphere per unit Euclidean area.
    for j in range(3):
        inner_flux = -sum(n[i]*D[i][j] for i in range(3))
        same(inner_flux, -4*A*a/rho**3*n[j], 'outward-normal sign')


def run():
    metric_cases = 0
    for a in [Q(1,3),Q(1),Q(5,2)]:
        for gap in [Q(1,7),Q(1,2),Q(2),Q(11)]:
            for A,B in [(Q(0),Q(1)),(Q(1),Q(0)),(Q(1,2),Q(1,2)),(Q(1,3),Q(2,5)),(Q(2),Q(5))]:
                local_curvature(a,a+gap,A,B)
                metric_cases += 1
    cartesian_cases = 0
    for a in [Q(1,3),Q(1),Q(5,2)]:
        for x,rho in [([Q(1),Q(2),Q(2)],Q(3)),([Q(3),Q(4),Q(12)],Q(13)),([Q(0),Q(0),Q(7)],Q(7))]:
            for A in [Q(0),Q(1,2),Q(2)]:
                cartesian_check(a,x,rho,A)
                cartesian_cases += 1
    return {'status':'PASS','metric_cases':metric_cases,'cartesian_cases':cartesian_cases,
            'exact_equalities':CHECKS,'arithmetic':'fractions.Fraction',
            'scope':'Finite independent supporting checks, not a universal proof.',
            'imports_author_code':False,'all_checks_active_under_optimization':True}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
