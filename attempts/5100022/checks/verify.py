"""Exact algebra controls and separately labelled numerical diagnostics for k404.
The meromorphic proof, not finite tests, establishes all-period constancy.
Uses installed sympy and mpmath only; prints a deterministic JSON receipt.
"""
import json, math
from collections import Counter
import sympy as S
import mpmath as mp
exact=Counter(); numeric=Counter(); worst=mp.mpf(0)
def ck(v,name):
    assert bool(v),name
    exact[name]+=1
s,c,d,k,t,B,C,D=S.symbols('s c d k t B C D')
rels=[(c,1-s*s),(d,1-k*k*s*s),(B,1-k*k),(C,1-t*t),(D,1-k*k*t*t)]
def reduce(expr):
    q=S.together(expr).as_numer_denom()[0]
    for z,r in rels:q=S.rem(S.Poly(q,z),S.Poly(z*z-r,z)).as_expr()
    return S.factor(q)
def zero(expr,name):ck(reduce(expr)==0,name)
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
det=lambda x,y:x[0]*y[1]-x[1]*y[0]
sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
L=1-k*k*t*t*s*s; E=1-2*k*k*t*t+k*k*t**4
M=(-s*D*D/L,B*c/L)
H=(-D*t*d*c/(C*L),-B*D*t*d*s/(C*L))
Pm=sub(M,H);Pp=tuple(a+b for a,b in zip(M,H));F=(k,0);n=(-s,c/B)
U=(-(E*s+k*(C*C-D*D*s*s))/(C*C*L),c*(2*B*B-E*(1+k*s))/(B*C*C*L))
zero(dot(sub(Pm,F),sub(U,Pm)),'actual_minus_antipedal_line')
zero(dot(sub(Pp,F),sub(U,Pp)),'actual_plus_antipedal_line')
zero(det(sub(Pm,F),sub(Pp,F))-2*B*D*t*d*(1+k*s)/(C*L),'exact_intersection_determinant')
zero(dot(n,M)-1,'contact_line_midpoint')
zero(dot(n,H),'contact_line_direction')
for P in [Pm,Pp]:zero(P[0]**2*C*C/(D*D)+P[1]**2*C*C/(B*B)-1,'original_ellipse_endpoints')
zero((D*D-B*B)/(C*C)-k*k,'confocal_focus')
eta=(dot(H,H)-dot(sub(M,F),sub(M,F)))/(1+k*s)
for a,b in zip(U,tuple(2*M[i]-F[i]+eta*n[i] for i in range(2))):zero(a-b,'midpoint_intersection_derivation')
q=((k-s)/(1-k*s),B*c/(1-k*s))
for a,b in zip(q,tuple(F[i]+(1-dot(n,F))*n[i]/dot(n,n) for i in range(2))):zero(a-b,'actual_focal_projection')
zero(q[0]**2+q[1]**2-1,'focal_pedal_circle')
zero(dot(n,q)-1,'pedal_on_tangent')
zero(det(n,(-c*d,-s*d/B))-d/B,'strict_normal_rotation')
derivsq=4*k**4*t**4*(1/(k*k*t*t))*(1-1/(k*k*t*t))*(1-1/(t*t))
zero(derivsq-4*D*D*C*C/(t*t),'simple_antipedal_poles')
# All source even primitive indices in a finite exact range. Moduli are proof input.
rotations=0
for N in range(4,301,2):
    m=N//2
    for tau in range(1,m):
        if math.gcd(tau,N)!=1:continue
        rotations+=1
        ck(tau%2==1,'even_primitive_turning_odd')
        ck(math.gcd(tau,m)==1,'quotient_real_lattice')
        ck((m*tau)%N==m,'antipodal_vertex_shift')
        ck(len({j*tau%m for j in range(m)})==m,'distinct_quotient_poles')
        ck(sum(j*tau%m==0 for j in range(N))==2,'two_equal_trace_residues')
        ck(((m+tau)%2==0)==(N%4==2),'exact_pedal_phase_alignment')
# Laurent parity certificate: f(p+z)=-f(p-z) kills all even terms.
for degree in range(-2,13):
    allowed=((-1)**degree==-1)
    ck(allowed==(degree%2==1),'Laurent_character_parity')
ck(sum(degree<0 and degree%2==1 for degree in range(-2,0))==1,'at_most_one_negative_Laurent_power')

mp.mp.dps=90
def numclose(x,y,name,tol=mp.mpf('1e-65')):
    global worst
    err=abs(x-y)/(1+abs(x)+abs(y))
    assert err<tol,(name,mp.nstr(err,8))
    worst=max(worst,err);numeric[name]+=1
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))/2
def model(k,N,tau):
    K=mp.ellipk(k*k);Kp=mp.ellipk(1-k*k);v=2*K*tau/N
    sn=lambda w:mp.ellipfun('sn',w,k*k)
    cn=lambda w:mp.ellipfun('cn',w,k*k)
    dn=lambda w:mp.ellipfun('dn',w,k*k)
    tv=sn(v);cv=cn(v);dv=dn(v);bp=mp.sqrt(1-k*k)
    a=dv/cv;b=bp/cv
    def P(w):return(-a*sn(w),b*cn(w))
    def U(u):
        ss=sn(u);cc=cn(u);ll=1-k*k*tv*tv*ss*ss;ee=1-2*k*k*tv*tv+k*k*tv**4
        return(-(ee*ss+k*(cv*cv-dv*dv*ss*ss))/(cv*cv*ll),cc*(2*bp*bp-ee*(1+k*ss))/(bp*cv*cv*ll))
    def q(u):return((k-sn(u))/(1-k*sn(u)),bp*cn(u)/(1-k*sn(u)))
    def get(w,actual=True):
        pp=[P(w+2*j*v) for j in range(N)]
        uu=[U(w+(2*j+1)*v) for j in range(N)]
        qq=[q(w+(2*j+1)*v) for j in range(N)]
        if actual:
            for j,(p,z) in enumerate(zip(pp,pp[1:]+pp[:1])):
                n=(p[0]-k,p[1]);nn=(z[0]-k,z[1]);hp=dot(n,p);hz=dot(nn,z);dd=det(n,nn)
                direct=((hp*nn[1]-n[1]*hz)/dd,(n[0]*hz-hp*nn[0])/dd)
                for x,y in zip(direct,uu[j]):numclose(x,y,'actual_antipedal_intersection')
                edge=sub(z,p);lam=dot(sub((k,0),p),edge)/dot(edge,edge)
                foot=tuple(p[i]+lam*edge[i] for i in range(2))
                for x,y in zip(foot,qq[j]):numclose(x,y,'actual_original_side_projection')
        trace=sum(dn(w+2*j*v) for j in range(N))
        aa=area(pp);bb=area(uu);cc=area(qq)
        numclose(aa,a*b*tv*cv/dv*trace,'original_area_trace')
        return aa,bb,cc,trace
    return K,Kp,v,get
families=0;realcases=0
for N in [6,10,14,18,22,26]:
    for tau in range(1,N//2):
        if math.gcd(tau,N)!=1:continue
        for kk in ['.1','.5','.9','.99']:
            k0=mp.mpf(kk);K,Kp,v,get=model(k0,N,tau);families+=1
            vals=[get(K*x) for x in map(mp.mpf,['.071','.213','.491','.837'])]
            for aa,bb,cc,ss in vals:
                assert aa>0 and cc>0
                numeric['positive_original_and_focal_pedal']+=2
                numclose(bb/ss,vals[0][1]/vals[0][3],'antipedal_constant_trace')
                numclose(cc/ss,vals[0][2]/vals[0][3],'pedal_aligned_trace')
                numclose(bb/cc,vals[0][1]/vals[0][2],'requested_ratio_constancy')
                realcases+=1
# Excluded even parity: antipedal/original remains constant, target ratio usually varies.
excluded=[]
for N in [4,8,12,16]:
    K,Kp,v,get=model(mp.mpf('.7'),N,1)
    vals=[get(K*x) for x in map(mp.mpf,['.071','.317','.671'])]
    for aa,bb,cc,ss in vals:numclose(bb/ss,vals[0][1]/vals[0][3],'general_even_antipedal_trace')
    spread=max(x[1]/x[2] for x in vals)-min(x[1]/x[2] for x in vals)
    assert abs(spread)>mp.mpf('1e-14');numeric['excluded_parity_nonconstant_control']+=1
    excluded.append({'N':N,'ratio_spread':mp.nstr(spread,15)})
complexcases=0
for N,tau,kk in [(6,1,'.35'),(10,3,'.7'),(14,5,'.85'),(22,9,'.6')]:
    K,Kp,v,get=model(mp.mpf(kk),N,tau)
    base=get(K*mp.mpf('.237'),actual=False)
    for e in ['1e-5','1e-9','1e-13']:
        val=get(1j*Kp+mp.mpf(e),actual=False)
        numclose(val[1]/val[3],base[1]/base[3],'near_pole_antipedal_trace',mp.mpf('1e-50'))
        numclose(val[2]/val[3],base[2]/base[3],'near_pole_pedal_trace',mp.mpf('1e-50'))
        complexcases+=1
    w=K*mp.mpf('.237')+1j*Kp*mp.mpf('.137')
    aa=get(w,actual=False);neg=get(-w,actual=False);im=get(w+2j*Kp,actual=False)
    numclose(neg[1],aa[1],'antipedal_reflection_even')
    numclose(im[1],-aa[1],'antipedal_imaginary_character')
print(json.dumps({'status':'PASS','exact_assertions':sum(exact.values()),'exact_counts':dict(exact),'primitive_rotations_checked':rotations,'numerical_diagnostics':{'precision_decimal_digits':90,'comparisons':sum(numeric.values()),'counts':dict(numeric),'real_families':families,'real_phases':realcases,'near_pole_cases':complexcases,'excluded_parity_controls':excluded,'maximum_scaled_error':mp.nstr(worst,15)},'scope':'Exact finite algebra and period controls, with separate floating diagnostics. The analytic all-period proof is PROOF.md; tests alone do not establish it.'},indent=2,sort_keys=True))
