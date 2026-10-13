#!/usr/bin/env python3
"""Fresh symbolic/local/lattice controls, not a substitute for the written proof."""
from collections import Counter
from fractions import Fraction
from math import gcd
import json
import sympy as s
C=Counter()
def check(expr,label):
    assert bool(expr), label
    C[label]+=1

def dot(p,q):return sum(p[i]*q[i] for i in range(2))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def meet(p,q):
    hp,hq=dot(p,p),dot(q,q);d=det(p,q)
    return s.Matrix([(hp*q[1]-hq*p[1])/d,(p[0]*hq-q[0]*hp)/d])
x,y,u,v,z,t=s.symbols('x y u v z t')
P=s.Matrix([x,y]);Q=s.Matrix([u,v]);R=s.Matrix([z,t])
h=dot(P,P);hq=dot(Q,Q);hr=dot(R,R)
left=meet(R,P);right=meet(P,Q)
check(s.factor(dot(P,left)-h)==0,'incoming_support_line')
check(s.factor(dot(P,right)-h)==0,'outgoing_support_line')
local=h*((hq-dot(P,Q))/det(P,Q)+(hr-dot(R,P))/det(R,P))/2
check(s.factor(det(left,right)/2-local)==0,'one_vertex_shoelace_decomposition')
edge=h*(hq-dot(P,Q))/(2*det(P,Q))+hq*(h-dot(P,Q))/(2*det(P,Q))
F=(h*hq-(h+hq)*dot(P,Q)/2)/det(P,Q)
check(s.factor(edge-F)==0,'edge_assembly')
check(s.factor(h*hq-(h+hq)*dot(P,Q)/2-((h+hq)*dot(P-Q,P-Q)-(h-hq)**2)/4)==0,'coincident_endpoint_second_order')
# A distinct ideal reduction of full rational Jacobi chord/tangent identities.
ss,cc,dd,S,Cc,D,k,alpha,beta=s.symbols('s c d S C D k alpha beta')
gb=s.groebner([cc**2+ss**2-1,dd**2+k**2*ss**2-1,Cc**2+S**2-1,D**2+k**2*S**2-1],cc,dd,Cc,D,ss,S,k)
red=lambda f:gb.reduce(s.expand(f))[1]
den=1-k**2*ss**2*S**2
pm=s.Matrix([-(S*cc*dd-ss*Cc*D),Cc*cc+S*ss*D*dd])
pp=s.Matrix([-(S*cc*dd+ss*Cc*D),Cc*cc-S*ss*D*dd])
check(red(det(pm,pp)-2*ss*cc*D*den)==0,'complete_chord_determinant_addition')
for sign in (-1,1):
    p=s.Matrix([-(S*cc*dd+sign*ss*Cc*D),Cc*cc-sign*S*ss*D*dd])
    check(red(-S*p[0]*dd+Cc*p[1]-cc*den)==0,'chord_tangent_substitution')
# Pole chart, B=2absc*dn(u)/(1-k²s²sn²u).
a,b,sv,cv,dv=s.symbols('a b sv cv dv',nonzero=True)
zs,zc,zd=s.symbols('zs zc zd')
pchart=-2*s.I*a*b*sv*cv*zc*zs/(zs**2-sv**2)
check(s.simplify(pchart/(2*a*b*sv*cv)-(-s.I*zc/zs)/(1-sv**2/zs**2))==0,'midpoint_common_pole_chart')
# At p±v the denominator derivative is ±2cd/s; nonzero for strict real v.
for sign in (-1,1):
    Su=sign/(k*sv);Cu=-sign*s.I*dv/(k*sv);Du=-sign*s.I*cv/sv
    check(s.simplify(-2*k**2*sv**2*Su*Cu*Du-sign*2*cv*dv/sv)==0,'D_root_simple_derivative')
    residue=2*a*b*sv*cv*Du/(sign*2*cv*dv/sv)
    check(s.simplify(residue+s.I*a*b*sv*cv/dv)==0,'B_endpoint_pole_residue')
# Linear zeros at opposite/coincident midpoint types, explicitly nonzero.
zz=s.symbols('zz')
check(s.limit(pchart.subs({zs:zz,zc:1})/zz,zz,0)==2*s.I*a*b*cv/sv,'B_opposite_zero_linear_coefficient')
check(s.simplify((2*a*b*sv*cv*s.I*s.sqrt(1-k**2)/(1-sv**2)).subs(sv**2,1-cv**2)-2*s.I*a*b*sv*s.sqrt(1-k**2)/cv)==0,'B_coincident_zero_linear_coefficient')
# Explicit leading vertex-edge double pole, as an independent order check.
Sd,Cd,Dd=s.symbols('Sd Cd Dd',nonzero=True)
Rp=s.Matrix([-a/k,-s.I*b/k]);Q0=s.Matrix([-a/(k*Sd),-s.I*b*Dd/(k*Sd)])
lead=-dot(Rp,Rp)*dot(Rp,Q0)/(2*det(Rp,Q0))
check(s.factor(lead+(a*a-b*b)*(a*a-b*b*Dd)/(2*s.I*a*b*k*k*(Dd-1)))==0,'individual_F_double_pole_coefficient')
coeffs=s.symbols('c_2 c_1 c0 c1 c2 c3')
G=coeffs[0]/zz**2+coeffs[1]/zz+coeffs[2]+coeffs[3]*zz+coeffs[4]*zz**2+coeffs[5]*zz**3
check(s.expand(G-G.subs(zz,-zz))==2*coeffs[1]/zz+2*coeffs[3]*zz+2*coeffs[5]*zz**3,'incident_double_pole_removed')
# Pedal local chart from DLMF quarter shifts: Q(r+z)=(alpha dn z,i beta/k') cn z/(k sn²z).
kp=s.symbols('kp',nonzero=True)
# sn(r+z)=dnz/(k cnz); cn(r+z)=-i kp/(k cnz); dn(r+z)=i kp snz/cnz.
Snr=zd/(k*zc);Cnr=-s.I*kp/(k*zc);Dnr=s.I*kp*zs/zc
Qr=s.Matrix([-alpha*kp**2*Snr/Dnr**2,beta*Cnr/Dnr**2])
qchart=s.Matrix([alpha*zd*zc/(k*zs**2),s.I*beta*zc/(k*kp*zs**2)])
check(all(s.simplify(v)==0 for v in Qr-qchart),'pedal_quarter_shift_chart')
check(all(s.simplify(v)==0 for v in qchart.subs(zs,-zs)-qchart),'pedal_pole_chart_even')
# Universal arithmetic explained in the report; these are finite exact controls.
families=0
for n in range(3,204,2):
    ell=Fraction(2,n)
    for tau in range(1,(n+1)//2):
        if gcd(n,tau)!=1:continue
        v=2*Fraction(tau,n);delta=2*v
        check(gcd(2*tau,n)==1,'primitive_odd_multiplication_invertible')
        check({j*delta%2 for j in range(n)}=={j*ell for j in range(n)},'full_real_quotient_lattice')
        check(v/ell==tau,'opposite_midpoint_classes_collapse')
        check((1+v)%ell==ell/2,'origin_pedal_half_trace_shift')
        idx=[j for j in range(n) if (v+j*delta)%2==0]
        check(idx==[(n-1)//2],'opposite_edge_exact_index')
        check((delta%2)!=0,'incident_neighbors_regular')
        families+=1
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'families':dict(C),'primitive_odd_lattice_families':families,'sympy_version':s.__version__,'scope':'Finite exact algebra and arithmetic controls only; universal proof is reconstructed independently in INDEPENDENT_DERIVATION.md.'},indent=2))
