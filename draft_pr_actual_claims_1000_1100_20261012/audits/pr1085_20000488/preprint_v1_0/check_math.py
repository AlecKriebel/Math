#!/usr/bin/env python3
"""Exact finite diagnostics, not continuum proof or numerical spectral evidence."""
import argparse
from fractions import Fraction as F
from kit_common import require, emit, safe_output
from verify_package import verify

def run(mutation=None):
    theta = F(1, 4)
    denominator = 1 - (4 if mutation == "preprint_theta" else 2) * theta
    require(denominator > 0, "published HHRV theta range; older preprint differs")
    factor = theta**2 / denominator**2
    require(factor == F(1, 4), "journal HHRV factor")
    defect = F(1, 5000) * F(25, 24) * 10
    c = F(1250, 2501)
    require(defect == F(1, 480) and c-defect == F(597499, 1200480), "Hardy bump margin")
    v = F(1, 5000) * F(25, 24) / c
    require(v == F(2501, 6000000) and 16*v < F(1, 100), "prior theorem bump margin")
    require(F(201, 10000) < F(1, 40) and F(1, 240) < 1, "integer count certificate")
    # All-function square coercivity; finite diagnostics of the universal proof.
    probes = 0
    grid = [F(-2), F(-1, 2), F(0), F(1, 3), F(3)]
    g = [F(1, 3), F(-2, 3), F(2, 3)]
    for a0 in grid:
        for a1 in grid:
            for b in grid:
                a = [a0, a1, F(2, 5)]
                left = sum(z*z for z in a) + b*b
                right = 4*(sum((z-t*b)**2 for z,t in zip(a,g)) + b*b)
                require(left <= right, "pointwise metric coercivity")
                probes += 1
    minors = 0
    for r in [F(0), F(1,2500), F(1,10), F(1), F(100)]:
        for s in [F(0), r/2, r]:
            det=(1+2*r)*(2*(1+r)*(1+s)-1)-4*(1+r)**2*s
            require(det == (1+2*r)**2-2*(1+r)*s and det >= 1+2*r+2*r*r > 0,
                    "coercivity principal minor")
            minors += 1
    boundary = (1 - F(-4,5) if mutation == "normal_sign" else 1 + F(-4,5))
    surface = 1 if mutation == "lost_jacobian" else F(5,4)
    require(boundary*surface == F(1,4), "normal defect with surface Jacobian")
    require(1 + F(-1) == 0, "flat cancellation")
    hardy = 0
    for m in [3,4,5,10,100]:
        a0=F(m-2,2)
        require(a0*(m-2-a0)==a0*a0 and a0*m > 0, "regularized Hardy coefficients")
        hardy += 1
    require(F(2-2,2)==0 and F(1-2,2)<0, "critical dimension exclusion")
    trace = 0
    for x in [F(0), F(1,3), F(1), F(100)]:
        for y in [F(0), F(1,5), F(1), F(10)]:
            lhs=10*(x*x+y*y); rhs=8*x*x+4*x*y
            require(lhs-rhs == 8*y*y+2*(x-y)**2 >= 0, "weighted trace absorption")
            trace += 1
    vertical = 0
    for beta in [F(1,10),F(1),F(10)]:
        for kappa in [F(0),F(1,10),F(1),F(10)]:
            L=1/(2*(beta+kappa))
            require(2*beta*L+2*kappa*L==1, "vertical integration trace identity")
            vertical += 1
    require(F(2,200)/2-F(1,100)<0 and F(44,2800)/2-F(1,100)<0,
            "linear and logarithmic null-sequence sign diagnostics")
    square = 0
    for beta,p,rho in [(F(3),F(4),F(5)),(F(5),F(12),F(13)),
                       (F(1),F(0),F(1)),(F(3,5),F(4,5),F(1))]:
        require(rho*rho==p*p+beta*beta, "mass relation")
        for A in [F(-2),F(0),F(1),F(3,2)]:
            for B in [F(-1),F(0),F(2)]:
                for r,s in [(F(1),F(2)),(F(3,2),F(5,2)),(rho,rho+1)]:
                    u2=A*A/(2*r)+2*A*B/(r+s)+B*B/(2*s)
                    dt2=A*A*r/2+2*A*B*r*s/(r+s)+B*B*s/2
                    boundary_beta = -beta if mutation=="fourier_boundary_sign" else beta
                    energy=dt2+(p*p+beta*beta)*u2-boundary_beta*(A+B)**2
                    completed=((rho-r)*A)**2/(2*r)+2*(rho-r)*(rho-s)*A*B/(r+s)+((rho-s)*B)**2/(2*s)
                    require(energy==completed+(rho-beta)*(A+B)**2 and completed>=0,
                            "Fourier trace square identity")
                    square += 1
    scaling = 0
    for beta in [F(1,20),F(1,3),F(1),F(7)]:
        for C in [F(1,100),F(1,2),F(3)]:
            require((16*beta*C*(16*beta*C+2*beta))**2==
                    beta**4*(16*C*(16*C+2))**2, "boundary dimension4 mass scaling")
            scaling += 1
    return {"passed":True,"coercivity_probes":probes,"coercivity_minors":minors,
            "Hardy_coefficient_guards":hardy,"trace_guards":trace,"vertical_guards":vertical,
            "Fourier_square_guards":square,"mass_scaling_guards":scaling,
            "Hardy_margin":"597499/1200480","v_upper":"2501/6000000","N_coarse_upper":"1/240",
            "scope":"Finite rational diagnostics supplement the universal proofs; no discretized PDE, source theorem reproof, historical executable replay or formal proof certificate."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output")
    p.add_argument("--mutation",choices=["normal_sign","lost_jacobian","preprint_theta","fourier_boundary_sign"])
    args=p.parse_args()
    if args.output: safe_output(args.output)
    package=verify()
    result=run(args.mutation)
    result["package"]=package
    emit(result,args.output)
if __name__=="__main__":
    main()
