#!/usr/bin/env python3
"""Independent exact identities and finite controls; no PDE/probability certification.

Read-only, no network, explicit failures survive optimized Python.
"""
import argparse
import itertools
import json
from fractions import Fraction as F
import sympy as s


def require(ok, label):
    if not ok:
        raise ValueError(label)


def eq(left, right, label):
    residual = s.factor(s.together(left - right))
    require(residual == 0, f"{label}: residual {residual}")


def main(mutation):
    checks = []
    r, u, c = s.symbols("r u c", real=True)
    a, b, p, q, ap, bp, app, bpp = s.symbols("a b p q ap bp app bpp", real=True)
    nu, M = s.symbols("nu M", positive=True)
    # Compute equilibrium bond currents directly from each allowed jump.
    prob = {-1:(1-r+u)/2, 0:r, 1:(1-r-u)/2}
    jumps = [(1,0,1),(0,-1,1),(1,-1,2)]
    rho_current = sum(prob[x]*prob[y]*v*(y*y-x*x) for x,y,v in jumps)
    signed_current = sum(prob[x]*prob[y]*v*(y-x) for x,y,v in jumps)
    eq(rho_current,r*u,"hole current")
    eq(signed_current,r+u*u-1,"signed current")
    for x,y in itertools.product([-1,0,1],repeat=2):
        eq(prob[x]*prob[y]-prob[y]*prob[x],0,"stirring cancellation")
    checks.append("equilibrium_currents_from_three_transitions")

    U=s.Matrix([-a*b,a+b]); T=U.jacobian([a,b]); d=a-b
    flux=s.Matrix([U[0]*U[1],U[0]+U[1]**2])
    diag=T.inv()*flux.jacobian([a,b])
    for i,j in itertools.product(range(2),repeat=2):
        eq(diag[i,j],([2*a+b,a+2*b][i] if i==j else 0),"diagonalization")
    eq(1-U[0]-U[1],(1-a)*(1-b),"positive-u triangle side")
    eq(1-U[0]+U[1],(1+a)*(1+b),"negative-u triangle side")
    eq(d*d,U[1]**2+4*U[0],"discriminant")
    eq(s.diff(2*a+b,a),2,"a-family orientation")
    eq(s.diff(a+2*b,b),2,"b-family orientation")
    checks.append("global_coordinate_polynomial_certificates")

    Sc=r+c*u-c*c; Fc=(u+c)*Sc
    J=s.Matrix([[u,r],[1,2*u]])
    for z,expected in zip([r,u],(s.Matrix([[1,c]])*J)):
        eq(s.diff(Fc,z),expected,"affine entropy compatibility")
    eq(Sc.subs({r:-a*b,u:a+b}), (a-c)*(c-b),"entropy factorization")
    # Convexity of |S_c| is analytic; compatibility holds on both affine branches.
    for sign in [-1,1]:
        for z,expected in zip([r,u],(s.Matrix([[sign,sign*c]])*J)):
            eq(s.diff(sign*Fc,z),expected,"absolute entropy branch")
    k=s.symbols("k",real=True)
    for face,cv,scale,beta in [(0,k,k,0),(1+u,k+1,k+2,1),(1-u,k-1,k-2,-1)]:
        eq(Sc.subs({r:face,c:cv},simultaneous=True),scale*(u-k),"face entropy")
        actual_beta=0 if mutation=="wrong_face_flux" and beta==1 else beta
        eq((u+cv)*(u-k),u*u+actual_beta*u-k*k-actual_beta*k,"face flux")
    # A uniform quantitative k -> 0 control, sampled only as a sanity check.
    for uu,kk in itertools.product([F(j,8) for j in range(-8,9)],[F(-1,100),F(1,100)]):
        require(abs(abs(uu-kk)-abs(uu))<=abs(kk),"zero entropy limit")
        require(abs((uu+kk)*abs(uu-kk)-uu*abs(uu))<=2*abs(uu)*abs(kk)+kk*kk,"zero entropy flux limit")
    checks.append("full_entropy_branches_scalar_faces_and_zero_limit")

    # All four violation signs, checked independently over an exact rational grid.
    thresholds=[F(1,4),F(3,4),F(-3,4),F(-1,4)]
    for aa,bb in itertools.product([F(j,8) for j in range(9)],[F(j,8) for j in range(-8,1)]):
        vals=[(aa-cc)*(cc-bb) for cc in thresholds]
        equivalences=[(vals[0]>=0,aa>=thresholds[0]),(vals[1]<=0,aa<=thresholds[1]),
                      (vals[2]<=0,bb>=thresholds[2]),(vals[3]>=0,bb<=thresholds[3])]
        require(all(left==right for left,right in equivalences),"rectangle entropy signs")
    # For decreasing cutoff g, psi_s=2g' and |psi_x|=-g'.
    gp=F(-1); ps=2*gp if mutation!="reverse_cone" else -2*gp
    for v in [F(j,4) for j in range(-8,9)]:
        for direction in [-1,1]:
            require(ps+v*gp*direction<=0,"backward cone sign")
    checks.append("rectangle_signs_and_cone_orientation")

    # Independent physical-variable reconstruction of viscous equations.
    jets=[a,b,p,q,ap,bp]; nxt=[p,q,ap,bp,app,bpp]
    dx=lambda expr:sum(s.diff(expr,z)*zz for z,zz in zip(jets,nxt))
    Ux=T*s.Matrix([p,q]); Uxx=Ux.applyfunc(dx)
    time=T.inv()*(-flux.applyfunc(dx)+nu*Uxx)
    at,bt=[s.factor(v) for v in time]
    eq(at,-(2*a+b)*p+nu*(ap-2*p*q/d),"physical a viscosity")
    eq(bt,-(a+2*b)*q+nu*(bp+2*p*q/d),"physical b viscosity")
    P=p/d; Q=q/d
    dt=lambda expr:s.diff(expr,a)*at+s.diff(expr,b)*bt+s.diff(expr,p)*dx(at)+s.diff(expr,q)*dx(bt)
    plus=s.factor(dt(P)+(2*a+b)*dx(P))
    minus=s.factor(dt(Q)+(a+2*b)*dx(Q))
    eq(plus.subs(nu,0),-2*d*P*P,"inviscid a Riccati")
    eq(minus.subs(nu,0),-2*d*Q*Q,"inviscid b Riccati")
    cross=0 if mutation=="drop_viscous_cross" else -2*P*dx(Q)
    expected=-2*d*P*P+nu*(dx(dx(P))+2*(P-2*Q)*dx(P)+cross+2*P*Q*(P+Q))
    eq(plus,expected,"weighted physical viscosity")
    av=M if mutation=="wrong_third_jet" else M+1
    jet={a:s.Rational(1,2),b:-s.Rational(1,2),p:1,q:0,ap:1,bp:-M,app:av,bpp:0}
    eq(dx(P).subs(jet),0,"jet first derivative")
    eq(dx(dx(P)).subs(jet),0,"jet second derivative")
    eq(dx(Q).subs(jet),-M,"jet mixed derivative")
    eq(plus.subs(jet),-2+2*nu*M,"jet production")
    strict=dict(jet);strict[app]=M+s.Rational(1,2)
    eq(dx(dx(P)).subs(strict),-s.Rational(1,2),"strict maximum jet")
    require(plus.subs(strict).subs({nu:s.Rational(1,4),M:8})>0,"strict maximum positive production")
    checks.append("independent_physical_viscosity_Riccati_and_strict_jet")

    # Verify increasing cylinder obstruction for several ring lengths explicitly.
    for n in [3,4,5,7]:
        lo=[-1]*n;hi=[-1]*n;lo[0]=hi[0]=1;hi[1]=0
        sig=F(7,3)
        def generator(z):
            total=F(0)
            for i in range(n):
                j=(i+1)%n;v=sig+dict(((x,y),rt) for x,y,rt in jumps).get((z[i],z[j]),0)
                zz=z.copy();zz[i],zz[j]=zz[j],zz[i]
                total+=v*(int(zz[1]==1)-int(z[1]==1))
            return total
        require(generator(lo)==sig+2 and generator(hi)==sig+1,"non-attractive generator")
    checks.append("non_attractiveness_rings")

    # Explicit admissible source kernel, C2 after extension by zero.
    x=s.symbols("x",real=True); ell=s.symbols("ell",integer=True,positive=True); j=s.symbols("j",integer=True)
    K=s.Rational(35,32)*(1-x*x)**3
    eq(s.integrate(K,(x,-1,1)),1,"kernel integral")
    for degree in range(3):
        for endpoint in [-1,1]:eq(s.diff(K,x,degree).subs(x,endpoint),0,"kernel C2 boundary")
    W=s.factor(s.summation(K.subs(x,j/ell),(j,-ell,ell))/ell)
    expected_W=1 if mutation=="assume_kernel_exact" else 1+s.Rational(7,48)/ell**4-s.Rational(5,96)/ell**6
    eq(W,expected_W,"discrete kernel mass")
    eq(W.subs(ell,2),s.Rational(2065,2048),"explicit kernel mass")
    variation=2*K.subs(x,0)
    for ll in [1,2,3,7,20]:
        for shift in [s.Rational(0),s.Rational(1,7),s.Rational(1,2)]:
            ws=sum(K.subs(x,(shift-jj)/ll)/ll for jj in range(-ll-1,ll+2) if abs((shift-jj)/ll)<=1)
            require(abs(ws-1)<=variation/ll,"translated quadrature bound finite controls")
    checks.append("source_kernel_nonunit_mass_and_uniform_bound_controls")

    # Invariant upper bounds under positive part and negative part.
    for left,right in itertools.product([F(j,8) for j in range(-8,9)],repeat=2):
        for trunc in [lambda v:max(v,0),lambda v:min(v,0)]:
            require(trunc(right)-trunc(left)<=max(right-left,0),"one-sided truncation")
    # The cost comparison identity forces minimizer order when x2>x1.
    x1,x2,y1,y2,t=s.symbols("x1 x2 y1 y2 t",real=True)
    cross_cost=((x1-y2)**2+(x2-y1)**2-(x1-y1)**2-(x2-y2)**2)/(2*t)
    eq(cross_cost,(x2-x1)*(y2-y1)/t,"Hopf-Lax minimizer ordering")
    for beta in [-1,0,1]:
        fan=(x/t-beta)/2
        eq(s.diff(fan,x),1/(2*t),"sharp rarefaction slope")
    checks.append("Hopf_Lax_order_truncations_and_sharp_fan_slope")
    return {"status":"passed","checks":checks,"count":len(checks),"mutation":mutation,
            "limitations":"Symbolic identities and finite witnesses only; analytic and probabilistic proofs are audited in INDEPENDENT_AUDIT.md."}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--mutation",choices=["none","wrong_face_flux","reverse_cone","drop_viscous_cross","wrong_third_jet","assume_kernel_exact"],default="none")
    print(json.dumps(main(p.parse_args().mutation),sort_keys=True))
