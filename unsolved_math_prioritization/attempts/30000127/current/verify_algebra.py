#!/usr/bin/env python3
"""Read-only exact algebra checks for the authored Leroux partial report.

Requires Python 3 and SymPy. Does not read source corpora, write files, access the
network, or claim to verify analytic compactness, stochastic convergence, or
PDE uniqueness. All validation uses explicit exceptions and survives -O/-OO.
"""
import argparse
import json
from fractions import Fraction as F
import sympy as s


def require(condition, label):
    if not condition:
        raise ValueError(label)


def zero(expr, label):
    if s.factor(s.cancel(expr)) != 0:
        raise ValueError(f"{label}: nonzero residual {s.factor(expr)}")


def check(mutation):
    checks = []
    rho, u, a, b, c, sigma, nu = s.symbols("rho u a b c sigma nu", real=True)
    probs = {0: rho, 1: (1-rho-u)/2, -1: (1-rho+u)/2}
    collision_rate = 1 if mutation == "alter_collision_rate" else 2
    rates = {(1, 0): 1, (0, -1): 1, (1, -1): collision_rate}
    def rate(x, y):
        return sigma + rates.get((x, y), 0)
    flux_rho = sum(probs[x]*probs[y]*rate(x,y)*((1-x*x)-(1-y*y)) for x in probs for y in probs)
    flux_u = sum(probs[x]*probs[y]*rate(x,y)*(-x+y) for x in probs for y in probs)
    zero(flux_rho-rho*u, "microscopic hole flux")
    zero(flux_u-(rho+u*u-1), "microscopic signed-spin flux")
    checks.append("microscopic_expected_fluxes")

    U = s.Matrix([-a*b, a+b])
    J = s.Matrix([[u,rho],[1,2*u]]).subs({rho:-a*b,u:a+b}, simultaneous=True)
    for variable, speed in [(a,2*a+b),(b,a+2*b)]:
        vector = U.diff(variable)
        for residual in J*vector-speed*vector:
            zero(residual,"eigenvector and speed")
    zero(U.jacobian([a,b]).det()-(a-b),"coordinate Jacobian")
    for ai in [F(0),F(1,4),F(1,2),F(1)]:
        for bi in [F(-1),F(-1,2),F(-1,4),F(0)]:
            rh, uu = -ai*bi, ai+bi
            require(rh>=0 and rh+abs(uu)<=1,"physical rectangle maps to triangle")
            require((ai-bi)**2==uu*uu+4*rh,"discriminant identity")
    checks.append("coordinates_speeds_and_boundary_grid")

    Sc = rho+c*u-c*c
    Fc = (u-c if mutation == "reverse_entropy_flux" else u+c)*Sc
    f1, f2 = rho*u, rho+u*u
    zero(Fc-(f1+c*f2-c**3),"affine entropy flux")
    zero(Sc.subs({rho:-a*b,u:a+b})-(a-c)*(c-b),"affine entropy factorization")
    for rv, k, cv, scale, beta in [
        (0,c,c,c,0),
        (1+u,c-1,c,1+c,1),
        (1-u,c+1,c,c-1,-1),
    ]:
        zero(Sc.subs(rho,rv)-scale*(u-k),"face affine entropy")
        zero((u+cv)*(u-k)-((u*u+beta*u)-(k*k+beta*k)),"face entropy flux")
    checks.append("affine_entropies_and_scalar_face_reductions")

    # Necessary monotonicity of the generator on comparable states with F equal.
    lower, upper = (1,-1,-1), (1,0,-1)
    require(all(x<=y for x,y in zip(lower,upper)),"ordered generator witness")
    def observable(z): return int(z[1]==1)
    def generator(z):
        out = 0
        for i in range(3):
            j=(i+1)%3
            zz=list(z); zz[i],zz[j]=zz[j],zz[i]
            out += rate(z[i],z[j])*(observable(zz)-observable(z))
        return s.expand(out)
    zero(generator(lower)-(sigma+2),"lower generator")
    zero(generator(upper)-(sigma+1),"upper generator")
    zero(generator(lower)-generator(upper)-1,"generator monotonicity obstruction")
    checks.append("natural_order_non_attractiveness_witness")

    # Radius3 triangular block, with exact weights. Build a legal stirring path.
    initial=[0,1,-1]*5
    def profile(z,center):
        weights=[1,2,3,2,1]
        rh=sum(F(w,9)*(1-z[(center+j-2)%len(z)]**2) for j,w in enumerate(weights))
        uu=sum(F(w,9)*(-z[(center+j-2)%len(z)]) for j,w in enumerate(weights))
        return rh,uu
    require(all(profile(initial,i)==(F(1,3),F(0)) for i in range(15)),"initial block rectangle")
    target=[0]*5+[1]*5+[-1]*5
    z=initial.copy(); path=[]
    for i,wanted in enumerate(target):
        j=z.index(wanted,i)
        while j>i:
            old=z.copy(); z[j-1],z[j]=z[j],z[j-1]
            require(sorted(old)==sorted(z),"stirring preserves species counts")
            require(old[j-1]!=old[j],"effective adjacent exchange")
            path.append((j-1,j)); j-=1
    require(z==target,"reachable target")
    require(profile(z,2)==(F(1),F(0)),"block exits interior rectangle")
    checks.append("reachable_block_rectangle_obstruction")

    p,q,ap,bp,app,bpp=s.symbols("p q ap bp app bpp",real=True)
    def Dx(expr):
        return sum(s.diff(expr,x)*y for x,y in [(a,p),(b,q),(p,ap),(q,bp),(ap,app),(bp,bpp)])
    d=a-b; lp=2*a+b; lm=a+2*b
    at=-lp*p; bt=-lm*q
    def Dt(expr,at,bt):
        return s.diff(expr,a)*at+s.diff(expr,b)*bt+s.diff(expr,p)*Dx(at)+s.diff(expr,q)*Dx(bt)
    P=p/d; Q=q/d
    zero(Dt(P,at,bt)+lp*Dx(P)+2*d*P**2,"inviscid weighted a cancellation")
    zero(Dt(Q,at,bt)+lm*Dx(Q)+2*d*Q**2,"inviscid weighted b cancellation")
    checks.append("inviscid_weighted_Riccati_identities")

    atv=at+nu*(ap-2*p*q/d); btv=bt+nu*(bp+2*p*q/d)
    # Reconstruct the physical conserved-variable viscous equation.
    ut=U.diff(a)*atv+U.diff(b)*btv
    ux=U.diff(a)*p+U.diff(b)*q
    uxx=ux.applyfunc(Dx)
    for residual in ut+J*ux-nu*uxx:
        zero(residual,"physical isotropic viscosity transform")
    cross=0 if mutation=="omit_mixed_derivative" else -2*P*Dx(Q)
    expected=-2*d*P**2+nu*(Dx(Dx(P))+2*(P-2*Q)*Dx(P)+cross+2*P*Q*(P+Q))
    zero(Dt(P,atv,btv)+lp*Dx(P)-expected,"viscous weighted derivative equation")
    M=s.symbols("M",positive=True)
    jets={a:s.Rational(1,2),b:-s.Rational(1,2),p:1,q:0,ap:1,bp:-M,app:M+1,bpp:0}
    zero(P.subs(jets)-1,"jet P")
    zero(Q.subs(jets),"jet Q")
    zero(Dx(P).subs(jets),"jet P_x")
    zero(Dx(Dx(P)).subs(jets),"jet P_xx")
    zero(Dx(Q).subs(jets)+M,"jet Q_x")
    zero((Dt(P,atv,btv)+lp*Dx(P)).subs(jets)-(-2+2*nu*M),"jet positive production")
    require((-2+2*nu*M).subs({nu:s.Rational(1,4),M:8})>0,"positive jet production witness")
    checks.append("viscous_cross_term_and_positive_maximum_jet")

    for aa,bb in [(F(3,4),F(-1,4)),(F(0),F(-1)),(F(1),F(0))]:
        rh,uu=-aa*bb,aa+bb
        require(rh+abs(uu)<=1,"face normal controls")
    A=(F(0),F(1)); B=(F(0),F(-1)); threshold=F(1,2)
    def ent(V): return abs(V[0]+threshold*V[1]-threshold**2)
    require((ent(A)+ent(B))/2==F(1,2),"weak initial entropy average")
    require(ent((F(0),F(0)))==F(1,4),"weak initial entropy of average")
    checks.append("initial_entropy_non_continuity_witness")
    return {"status":"passed","checks":checks,"count":len(checks),"stirring_path_length":len(path),"mutation":mutation}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutation",choices=["none","alter_collision_rate","reverse_entropy_flux","omit_mixed_derivative"],default="none")
    args=parser.parse_args()
    print(json.dumps(check(args.mutation),sort_keys=True))


if __name__=="__main__":
    main()
