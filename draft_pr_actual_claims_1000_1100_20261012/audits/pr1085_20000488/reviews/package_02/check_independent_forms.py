#!/usr/bin/env python3
"""New exact diagnostics for review 02; not continuum proof or source reproof."""
import argparse, json, math
from fractions import Fraction as F

def need(ok, message):
    if not ok:
        raise ValueError(message)

def plus(a,b):
    n=max(len(a),len(b)); return [(a[j] if j<len(a) else 0)+(b[j] if j<len(b) else 0) for j in range(n)]

def scale(a,s): return [s*x for x in a]
def derivative(a): return [(j+1)*a[j+1] for j in range(len(a)-1)]
def inner(a,b,r):
    return sum(x*y*F(math.factorial(i+j),(2*r)**(i+j+1)) for i,x in enumerate(a) for j,y in enumerate(b))

def run(fault=None):
    counts={"complex_shear":0,"regularized_Hardy":0,"polynomial_Fourier_fibers":0,"weighted_trace_polynomials":0,"mass_scaling":0,"normal_area":0}
    grid=[F(-7,3),F(-1,4),F(0),F(2,5),F(9,2)]
    # Complex vectors are represented as pairs of rational real vectors.
    for G in [F(0),F(1,9),F(1),F(8)]:
        g=[G*F(3,5),G*F(4,5)]
        for x in grid:
            for y in grid:
                for b in grid:
                    a=[x,y]; imag=[y,-x]; bi=b/3
                    source=sum(z*z for z in a+imag)+b*b+bi*bi
                    shifted=sum((a[j]-g[j]*b)**2+(imag[j]-g[j]*bi)**2 for j in range(2))+b*b+bi*bi
                    need(source<=2*(1+G*G)*shifted,"complex shear lower bound")
                    counts["complex_shear"]+=1
    for m in [3,4,7,19]:
        a=F(m-2,2)
        for s in [F(0),F(1,17),F(1),F(99)]:
            for d in [F(1,100),F(1),F(23)]:
                lhs=a*((m-2)*s+m*d)/(s+d)**2-a*a*s/(s+d)**2
                rhs=(a*a*s+a*m*d)/(s+d)**2
                need(lhs==rhs and rhs>=a*a*s/(s+d)**2,"regularized Hardy divergence square")
                counts["regularized_Hardy"]+=1
    for beta,rho in [(F(1,3),F(5,3)),(F(2),F(7,2)),(F(7,5),F(7,5))]:
        p2=rho*rho-beta*beta
        for r in [F(1,7),F(2),F(11,3)]:
            for x in grid:
                for y in grid:
                    for imag in [False,True]:
                        poly=[x,y,F(3,7)] if not imag else [y,-x,F(-2,9)]
                        dt=plus(derivative(poly),scale(poly,-r))
                        energy=inner(dt,dt,r)+rho*rho*inner(poly,poly,r)-beta*poly[0]**2
                        square=plus(dt,scale(poly,rho))
                        sign=-1 if fault=="Fourier_trace_sign" else 1
                        completed=inner(square,square,r)+sign*(rho-beta)*poly[0]**2
                        need(energy==completed and inner(square,square,r)>=0,"polynomial Fourier completion")
                        counts["polynomial_Fourier_fibers"]+=1
    for beta in [F(1,10),F(3,2),F(10)]:
        for r in [F(1,7),F(3),F(13)]:
            for x in grid:
                poly=[x,F(3,4),F(-1,6)]; deriv=plus(derivative(poly),scale(poly,-r))
                rate=beta+r
                local=inner(poly,poly,rate)
                cross=inner(poly,deriv,rate)
                # w=poly*exp(-rt), with additional weight exp(-2 beta t).
                need(2*beta*local-2*cross==poly[0]**2,"weighted polynomial vertical endpoint")
                counts["weighted_trace_polynomials"]+=1
    for m in [4,6,10]:
        for beta in [F(1,100),F(2,7),F(1),F(11)]:
            for C in [F(1,200),F(3,5),F(12)]:
                exponent=m//2 if fault=="mass_exponent" else m
                need((16*beta*C*(16*beta*C+2*beta))**(m//2)==beta**exponent*(16*C*(16*C+2))**(m//2),"mass is beta, not fixed one")
                counts["mass_scaling"]+=1
    for den,num in [(5,3),(13,5),(17,8),(25,7)]:
        # Rational unit normal from a Pythagorean triple, downward component.
        tangent=F(num,den); vertical2=1-tangent*tangent
        # The listed triples have rational downward normal.
        root=math.isqrt(vertical2.numerator); rootd=math.isqrt(vertical2.denominator)
        need(root*root==vertical2.numerator and rootd*rootd==vertical2.denominator,"test triple")
        down=F(root,rootd); surface=1/down
        nuy=down if fault=="normal_sign" else -down
        area=1 if fault=="area_lost" else surface
        need((1+nuy)*area==surface-1,"normal defect includes area")
        counts["normal_area"]+=1
    theta=F(1,4); denominator=1-(4 if fault=="old_theta" else 2)*theta
    need(denominator>0 and theta*theta/denominator**2==F(1,4),"published version theta")
    m=2 if fault=="Hardy_m2" else 3
    need(m>2 and F(m-2,2)>0,"homogeneous Hardy dimension")
    flat_boundary=1 if fault=="flat_sign" else -1
    need(F(1,2)+F(1,2)+flat_boundary==0,"flat decaying mode threshold")
    need(F(1250,2501)-F(1,480)==F(597499,1200480)>0,"exact bump margin")
    need(F(2501,6000000)*16<F(1,100) and F(201,10000)<F(1,40),"prior count certificate")
    return {"passed":True,"counts":counts,"hardy_margin":"597499/1200480","source_count_coarse":"1/240","scope":"New finite exact diagnostics; analytic universal arguments and source applicability independently read, not proved by samples."}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--fault",choices=["Fourier_trace_sign","mass_exponent","normal_sign","area_lost","old_theta","Hardy_m2","flat_sign"]);a=p.parse_args()
    print(json.dumps(run(a.fault),indent=2,sort_keys=True))
