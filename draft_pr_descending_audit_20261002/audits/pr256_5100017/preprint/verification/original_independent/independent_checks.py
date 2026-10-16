#!/usr/bin/env python3
"""Independent exact support/moment algebra and a rational reconstruction of the8/3 orbit.
No author code is imported. Requires SymPy for formal Laurent identities only.
"""
from fractions import Fraction as Q
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(x,key):
    assert bool(x),key;C[key]+=1

def ident(x,key):ck(s.cancel(s.together(x))==0,key)
# Independent extraction from the full antipodal edge moment.
x,y,h,g,t,tc,D,H,E=s.symbols('x y h g t tc D H E',nonzero=True)
def edge_moment(h,g):
    p=h*x-t*x*x;q=g*y-t*y*y
    pc=h/x-tc/(x*x);qc=g/y-tc/(y*y)
    return s.expand((pc*q-p*qc)*(p+q))
paired=s.expand((edge_moment(h,g)+edge_moment(-h,-g))/2)
lin_t=paired.coeff(t,1).coeff(tc,0);lin_tc=paired.coeff(tc,1).coeff(t,0)
h2=H+E*(x*x+x**-2)/2;g2=H+E*(y*y+y**-2)/2;hg=D*(x/y+y/x)/2+E*(x*y+1/(x*y))/2
sub=lambda v:s.expand(v).subs(h*h,h2).subs(g*g,g2).subs(h*g,hg)
R=x*x/(y*y)-y*y/(x*x);U=x**4/(y*y)-y**4/(x*x)
ident(sub(lin_t)-D*U-s.Rational(3,2)*E*R-(H+D)*(x*x-y*y)-E*(x**4-y**4),'linear_t_coboundary')
ident(sub(lin_tc)-(H+D/2)*R-E*U/2-E*(x*x-y*y)/2-E*(y**-2-x**-2),'linear_conjugate_coboundary')
ident(paired-t*lin_t-tc*lin_tc+t*t*tc*(y*y/(x*x)-x*x/(y*y))*(x*x+y*y),'full_cubic_remainder')
# Unit-circle identity without selecting any numerical angles.
ident((y/x-x/y)*(x+y)/(2*s.I)+s.I*(1+(y/x+x/y)/2)*(y-x),'unit_circle_moment_telescope')
A,B,L=s.symbols('A B L',positive=True);HH=(A+B)/2;EE=(A-B)/2;dd=1-L*(1/A+1/B);FF=HH*dd+2*L
ident(FF+EE*dd-A+L*(A/B-1),'first_positive_factor')
ident(FF-EE*dd-B-L*(1-B/A),'second_positive_factor')
ident(2*EE*(HH-FF/dd)/((FF/dd)**2-EE**2)+4*EE*L*dd/(FF**2-EE**2*dd**2),'v_parameter_conversion')
# Coefficient relation obtained by squaring the adjacent-normal bilinear form.
cos=(y/x+x/y)/2;co=(x*y+1/(x*y))/2
ident(h2*g2-hg**2-(H*H-E*E-(D*D-E*E)*cos*cos+2*E*(H-D)*co*cos),'doubled_normal_identity')
# Rational scaled coordinates: physical point=(sqrt(A2)u,sqrt(B2)v).
A2=Q(221,96);B2=Q(27625,20736);lam=Q(125,96);ca=A2-lam;cb=B2-lam
ps=[(Q(0),Q(1)),(Q(-12,13),Q(-5,13)),(Q(1),Q(0)),(Q(-12,13),Q(5,13)),(Q(0),Q(-1)),(Q(12,13),Q(5,13)),(Q(-1),Q(0)),(Q(12,13),Q(-5,13))]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def subvec(p,q):return(p[0]-q[0],p[1]-q[1])
def am(points):
    cs=[cross(points[j],points[(j+1)%len(points)]) for j in range(len(points))]
    ar=sum(cs,Q(0))/2
    mt=tuple(sum((cs[j]*(points[j][i]+points[(j+1)%len(points)][i]) for j in range(len(points))),Q(0)) for i in (0,1))
    return ar,mt
for j,(u,v) in enumerate(ps):
    q=ps[(j+1)%8];prev=ps[j-1];du,dv=subvec(q,(u,v));iu,iv=subvec((u,v),prev)
    ck(u*u+v*v==1,'star_ellipse')
    ck((-dv*u+du*v)**2==ca*dv*dv/A2+cb*du*du/B2,'star_caustic_dual')
    ck(cross((u,v),q)>0,'star_positive_chord')
    n2=u*u/A2+v*v/B2;ip=iu*u+iv*v
    refl=(iu-2*ip*u/(A2*n2),iv-2*ip*v/(B2*n2))
    ck(cross(refl,(du,dv))==0,'star_reflection_direction')
    ck(A2*refl[0]*du+B2*refl[1]*dv>0,'star_reflection_sign')
ck(len(set(ps))==8,'star_primitive_eight')
ck(sum(p[1]<=0<ps[(j+1)%8][1] for j,p in enumerate(ps))==3,'star_winding_three')
H0=(A2+B2)/2;e0=(A2-B2)/2;d0=1-lam*(1/A2+1/B2);F0=H0*d0+2*lam;v0=-4*e0*lam*d0/(F0*F0-e0*e0*d0*d0);rho2=-2*F0/d0
ck((d0,F0,v0,rho2)==(Q(-120,221),Q(2795,1728),Q(7,13),Q(123539,20736)),'exact_star_constants')
ck(rho2==Q(13*13*731,144*144),'named_zero_point')
def projected(mx,my):
    out=[]
    for u,v in ps:
        n2=u*u/A2+v*v/B2;fac=(1-u*mx-v*my)/n2
        q=(mx+fac*u/A2,my+fac*v/B2)
        ck(u*q[0]+v*q[1]==1,'named_outer_tangent')
        # Difference is parallel to the tangent's normal in physical coordinates.
        ck((q[0]-mx)*A2*v-(q[1]-my)*B2*u==0,'perpendicular_projection')
        out.append(q)
    return out
S0,_=am(projected(Q(0),Q(0)));ck(S0>0,'origin_positive_area')
valid=0
for i in range(-8,9):
    for j in range(-6,7):
        mx,my=Q(i,3),Q(j,4);r2=A2*mx*mx+B2*my*my;G=2*F0+d0*r2
        ar,mt=am(projected(mx,my));ck(ar==S0*G/(2*F0),'all_M_area_formula')
        if G==0:continue
        caa=F0+2*H0*d0+e0*v0*d0;cbb=2*F0*v0+3*e0*d0+v0*d0*r2/2
        pred=(mx/2-mx*(caa+cbb)/(3*G),my/2-my*(caa-cbb)/(3*G))
        for axis in (0,1):ck(mt[axis]==6*ar*pred[axis],'direct_signed_first_moment')
        valid+=1
# Reconstruct the zero circle without radicals: S(t,0) is a quadratic polynomial.
Sp,_=am(projected(Q(1),Q(0)));Sm,_=am(projected(Q(-1),Q(0)))
lin=(Sp-Sm)/2;quad=(Sp+Sm-2*S0)/2
ck(lin==0 and S0+quad*(rho2/A2)==0,'exact_zero_circle_polynomial')
# Rectangle case in arbitrary M by a separate rational-grid shoelace.
for a in (Q(1),Q(3,2),Q(7,3)):
    for b in (Q(1,2),Q(2),Q(5,3)):
        for mx,my in ((Q(0),Q(0)),(Q(5),Q(-3)),(Q(2,7),Q(11,5))):
            ar,mt=am([(a,my),(mx,b),(-a,my),(mx,-b)])
            ck(ar==2*a*b,'rectangle_area')
            ck(mt==(2*ar*mx,2*ar*my),'rectangle_area_centroid')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'families':dict(C),'rational_star_M_queries':valid,'sympy_version':s.__version__,'scope':'Exact support/moment algebra and rational physical star controls. Source, all-period and domain claims are audited separately in the review.'},indent=2))
