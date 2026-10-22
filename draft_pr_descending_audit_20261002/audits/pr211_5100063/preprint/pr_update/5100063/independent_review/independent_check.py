#!/usr/bin/env python3
"""Independent exact algebra/finite lattice controls and direct-geometry diagnostics.
The universal proof is reviewed in INDEPENDENT_REVIEW.md; numerical tests are not certificates.
Run in this directory; only INDEPENDENT_CHECKS.json is written.
"""
import json, hashlib, math
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sympy as S
import mpmath as mp
counts=Counter(); nums=Counter(); maxerr=mp.mpf(0)
def ck(name,v):
    assert bool(v),name
    counts[name]+=1
k,h,s,C,d,c,n,b=S.symbols('k h s C d c n b')
rels=[(c,1-s*s),(n,1-k*k*s*s),(C,1-h*h),(d,1-k*k*h*h),(b,1-k*k)]
def reduce(p):
    p=S.expand(p)
    for var,value in rels:
        p=S.rem(p,var*var-value,var)
    return S.expand(p)
def eq(name,left,right):
    ck(name,reduce(S.together(left-right).as_numer_denom()[0])==0)
D=1-k*k*h*h*s*s
sm=(s*C*d-h*c*n)/D; sp=(s*C*d+h*c*n)/D
cm=(c*C+s*n*h*d)/D; cp=(c*C-s*n*h*d)/D
# Outer axes for alpha=1, expressed separately from ordinary billiard axes.
Ao=d*d/(C*C);Bo=b/(C*C)
U=1-2*k*k*h*h+k*k*h**4;V=1-2*h*h+k*k*h**4;W=1-k*k*h**4
L0=(U*U-k*k*V*V*h*h)/d;L1=(V*V-U*U*h*h)/C
Z=W*W-4*k*k*h**4*C*C*d*d
# These checks start with tangent-line and Euclidean inverse-vertex formulas.
eq('two_tangent_equations_minus', d*s*sm/C+c*cm/C,1)
eq('two_tangent_equations_plus', d*s*sp/C+c*cp/C,1)
eq('outer_squared_distance',(-Ao*s-k)**2+Bo**2*c*c,(1+k*s)*(U+k*V*s)/C**4)
eq('first_distance_factor_pair',(1+k*sm)*(1+k*sp),(d+k*C*s)**2/D)
eq('second_distance_factor_pair',(U+k*V*sm)*(U+k*V*sp),(d+k*C*s)*(L0+k*L1*s)/D)
cross=((-Ao*sm-k)*Bo*cp-Bo*cm*(-Ao*sp-k))/2
eq('translated_outer_cross_product',cross,Bo*h*d*n*(d+k*C*s)/(C*D))
# Independent assembly of the normalization from numerator and two distances.
Ncross=Bo*h*d*n*(d+k*C*s)/(C*D)
Ndist=(d+k*C*s)**3*(L0+k*L1*s)/(D*D*C**8)
formula=Bo*h*d*C**8*n*D/(C*(d+k*C*s)**2*(L0+k*L1*s))
eq('inverse_edge_normalization',Ncross/Ndist,formula)
# Triple-angle identities derived from sn(2v), cn(2v), dn(2v).
s2=2*h*C*d/W;c2=V/W;d2=U/W
sn3=(s2*C*d+h*c2*d2)/(1-k*k*s2*s2*h*h)
cn3=(c2*C-s2*d2*h*d)/(1-k*k*s2*s2*h*h)
dn3=(d2*d-k*k*s2*c2*h*C)/(1-k*k*s2*s2*h*h)
eq('triple_dn_factor',L0,Z*dn3)
eq('triple_cn_factor',L1,Z*cn3)
eq('strict_second_denominator_square_gap',L0**2-k*k*L1**2,(1-k*k)*Z**2)
eq('strict_first_denominator_square_gap',d*d-k*k*C*C,1-k*k)
# Local N=3 critical zero order: sn=1/k,dn=0, cn^2=1-1/k^2.
ck('N3_second_derivative_nonzero_polynomial',S.simplify(k*(1/k)*(k*k*(1-1/k**2))-(k*k-1))==0)
ck('N3_dn_derivative_square_nonzero_polynomial',S.simplify(k**4*(1/k**2)*(1-1/k**2)-(k*k-1))==0)
rot=0
for N in range(3,102,2):
    for tau in range(1,N//2+1):
        if math.gcd(N,tau)>1:continue
        rot+=1; delta=F(tau,N); v=delta/2; L=F(1,N)
        poles={v%1,(-v)%1}; simple={(3*v)%1,(-3*v)%1}
        ck('odd_group_order',len({j*delta%1 for j in range(N)})==N)
        ck('quadratic_poles_distinct',len(poles)==2)
        ck('different_denominator_fibers_disjoint',not poles.intersection(simple))
        ck('critical_fiber_only_primitive_N3',(len(simple)==1)==(N==3))
        ck('second_factor_not_constant',3*v!=F(1,4))
        ck('one_pole_class_in_real_quotient',all(((p-v)/L).denominator==1 for p in poles|simple))
        signed=Counter()
        for j in range(N): signed[(v-j*delta)%1]+=1;signed[(-v-j*delta)%1]-=1
        ck('all_double_coefficients_cancel',all(x==0 for x in signed.values()))
        ck('opposite_focus_is_halfperiod',F(1,2)%L==L/2)
# Direct high-precision geometry, using no author's code or stored numerical data.
mp.mp.dps=90
threshold=mp.mpf('1e-65')
def nc(name,x,scale=1):
    global maxerr
    err=abs(x)/max(1,abs(scale));assert err<threshold,(name,mp.nstr(err,10))
    nums[name]+=1;maxerr=max(maxerr,err)
def area(p):return sum(p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0] for i in range(len(p)))/2
families=0
for kval in ['0.07','0.61','0.96']:
    k=mp.mpf(kval);m=k*k;K=mp.ellipk(m);Kp=mp.ellipk(1-m);kp=mp.sqrt(1-m)
    sn=lambda z:mp.ellipfun('sn',z,m)
    cn=lambda z:mp.ellipfun('cn',z,m)
    dn=lambda z:mp.ellipfun('dn',z,m)
    for N in [3,5,7,9,11,15]:
      for tau in range(1,(N+1)//2):
        if math.gcd(N,tau)>1:continue
        families+=1;v=2*K*tau/N;delta=2*v;L=4*K/N
        h=sn(v);C=cn(v);d=dn(v);q=C*C;t=h*h
        alpha=mp.mpf('1.37');b=alpha*kp/C;a=alpha*d/C;focus=alpha*k
        Ao=a*d/C;Bo=b/C;U=1-2*m*t+m*t*t;V=1-2*t+m*t*t
        l0=(U*U-m*V*V*t)/d;l1=(V*V-U*U*t)/C
        coef=Bo*h*d*q**4/(alpha**3*C)
        E=lambda z:coef*dn(z)*(1-m*t*sn(z)**2)/((d+k*C*sn(z))**2*(l0+k*l1*sn(z)))
        cyc=lambda z:sum(E(z+j*delta) for j in range(N))
        def outer(z):
            # Solve the two tangent lines directly, not from the proposed outer ellipse.
            a1=-sn(z-v)/a;b1=cn(z-v)/b;a2=-sn(z+v)/a;b2=cn(z+v)/b
            determinant=a1*b2-a2*b1
            return ((b2-b1)/determinant,(a1-a2)/determinant)
        def inverse(p,f):
            x,y=p;norm=(x-f)**2+y*y;return ((x-f)/norm,y/norm)
        def get(z):
            vertices=[outer(z+j*delta) for j in range(N)]
            for j,p in enumerate(vertices):
                zz=z+j*delta
                nc('direct_tangent_intersection_x',p[0]+Ao*sn(zz),Ao)
                nc('direct_tangent_intersection_y',p[1]-Bo*cn(zz),Bo)
            plus=area([inverse(p,focus) for p in vertices]);minus=area([inverse(p,-focus) for p in vertices])
            nc('direct_inverse_area_equals_edge_sum',plus-cyc(z+v),plus)
            nc('opposite_focus_equals_phase_shift',minus-cyc(z+v+2*K),minus)
            nc('orientation_reversal',area(list(reversed([inverse(p,focus) for p in vertices])))+plus,plus)
            assert plus>0 and minus>0
            return plus*minus
        reference=get(mp.mpf('.123')*K)
        for phase in ['.419','1.073','1.881']:
            nc('real_product_constancy',get(mp.mpf(phase)*K)/reference-1)
        # Independently compare a complex inverse edge with the reduced expression.
        zz=mp.mpf('.37')*K+mp.mpf('.19')*1j*Kp
        p=inverse(outer(zz-v),focus);r=inverse(outer(zz+v),focus)
        direct=(p[0]*r[1]-p[1]*r[0])/2
        nc('complex_direct_edge_normalization',direct-E(zz),E(zz))
        nc('complex_product_constancy',cyc(zz)*cyc(zz+L/2)/reference-1)
        r0=3*K+1j*Kp;R=r0+v
        nc('edge_reflection',E(2*r0-zz)+E(zz),E(zz))
        nc('cyclic_reflection',cyc(2*R-zz)+cyc(zz),cyc(zz))
        nc('imaginary_antiperiod',cyc(zz+2j*Kp)+cyc(zz),cyc(zz))
        nc('first_quotient_zero',cyc(R+L/2),cyc(zz))
        nc('second_quotient_zero',cyc(R+L/2+2j*Kp),cyc(zz))
# Exact even N=4 diagnostic: a diamond and an axis rectangle in the same (4,3) ellipse,
# caustic (16/5,9/5), invert actual outer tangent vertices at the original foci sqrt(7).
# Even products need not be constant; this is a scope calibration, not a needed premise.
f=S.sqrt(7)
def inv(p):
    x,y=p;dd=(x-f)**2+y*y;return ((x-f)/dd,y/dd)
diamond_outer=[(4,3),(-4,3),(-4,-3),(4,-3)]
rectangle_outer=[(S.Integer(5),0),(0,S.Integer(5)),(-S.Integer(5),0),(0,-S.Integer(5))]
ev=[S.simplify(area([inv(p) for p in poly])**2) for poly in [diamond_outer,rectangle_outer]]
ck('even_scope_control_is_not_constant',ev[0]!=ev[1])
result={'status':'PASS','exact_assertions':sum(counts.values()),'exact_categories':dict(counts),'primitive_rotations_exact':rot,'numerical_diagnostics':sum(nums.values()),'numerical_categories':dict(nums),'families':families,'precision_digits':90,'maximum_scaled_error':mp.nstr(maxerr,12),'even_N4_product_control':[str(x) for x in ev],'limits':'Finite exact identities and lattice controls plus uncertified high-precision diagnostics. The universal mathematical argument is independently audited in the report.'}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
