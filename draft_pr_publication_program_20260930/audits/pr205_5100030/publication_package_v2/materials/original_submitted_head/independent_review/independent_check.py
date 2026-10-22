"""Independent controls for k601. Exact identities and numerical diagnostics are separate."""
import math,json
from collections import Counter
import sympy as s
import mpmath as mp
exact=Counter();numeric=Counter();mp.mp.dps=75;worst=mp.mpf(0)
def eq(x,group):
    assert s.factor(x)==0,group
    exact[group]+=1
def near(x,y,group):
    global worst
    r=abs(x-y)/(1+abs(x)+abs(y));worst=max(worst,r)
    assert r<mp.mpf('1e-60'),(group,str(r))
    numeric[group]+=1

# Independently invert the cn/dn difference-addition linear system.
m,S,ca,da=s.symbols('m S ca da')
D=da-m*ca*S;C=ca-da*S
eq(D+m*S*C-da*(1-m*S*S),'difference_system')
eq(C+S*D-ca*(1-m*S*S),'difference_system')
eq(D-m*C-(da-m*ca+m*(da-ca)*S),'cross_correlation')
z=s.symbols('z')
eq((1-m*z*z)-m*(1-z*z)-(1-m),'diagonal_identity')
eq((1-m)*z*z+(1-z*z)-(1-m*z*z),'line_normal')
eq((1+s.sqrt(m)*z)*(1-s.sqrt(m)*z)-(1-m*z*z),'pointwise_distance_product')
for N in range(3,102,2):
    for r in range(1,N):
        assert (2*r)%N!=0
        exact['odd_denominator_guard']+=1
    for t in range(1,N//2+1):
        if math.gcd(t,N)==1:
            assert sorted((t*i)%N for i in range(N))==list(range(N))
            exact['primitive_winding_permutation']+=1

# Direct distances to chord lines, not to formula-generated pedal points.
families=0
for k in map(mp.mpf,['0.2','0.65','0.95']):
    par=k*k;K=mp.ellipk(par);beta=mp.sqrt(1-par)
    def sn(x):return mp.ellipfun('sn',x,par)
    def cn(x):return mp.ellipfun('cn',x,par)
    def dn(x):return mp.ellipfun('dn',x,par)
    for N in [3,5,7,9,13]:
        predicted=beta**2*sum(1/dn(4*K*i/N) for i in range(N))**2
        for winding in range(1,(N+1)//2):
            if math.gcd(N,winding)!=1:continue
            h=2*winding*K/N;a=dn(h)/cn(h);b=beta/cn(h)
            near(a*a-b*b,k*k,'confocal_axes');families+=1
            for phase in [mp.mpf('0.07'),mp.mpf('0.37'),mp.mpf('0.91')]:
                u=phase*K
                P=[(-a*sn(u+2*i*h),b*cn(u+2*i*h)) for i in range(N)]
                plus=[];minus=[]
                for i,((x,y),(xx,yy)) in enumerate(zip(P,P[1:]+P[:1])):
                    nx,ny=y-yy,xx-x;constant=nx*x+ny*y;norm=mp.sqrt(nx*nx+ny*ny)
                    qp=abs(constant-nx*k)/norm;qm=abs(constant+nx*k)/norm
                    v=u+(2*i+1)*h
                    near(qp,beta*(1+k*sn(v))/dn(v),'direct_positive_plus')
                    near(qm,beta*(1-k*sn(v))/dn(v),'direct_positive_minus')
                    assert qp>0 and qm>0;numeric['positive_distances']+=1
                    near(qp*qm,beta*beta,'pointwise_product')
                    near(x*x/(a*a)+y*y/(b*b),1,'outer_incidence')
                    # Tangency condition for an arbitrary normalized chord normal.
                    near(nx*nx+beta*beta*ny*ny,constant*constant,'caustic_tangency')
                    plus.append(qp);minus.append(qm)
                near(sum(plus)*sum(minus),predicted,'family_constant')

                args=[u+K+4*K*i/N for i in range(N)]
                Dsum=sum(dn(t) for t in args);Csum=sum(cn(t) for t in args)
                near(Dsum*Dsum-par*Csum*Csum,predicted,'quarter_period_bridge')
                # A direct check of all cyclic sn correlations against a second phase.
                for r in range(1,N):
                    shift=4*K*r/N
                    lhs=sum(sn(t)*sn(t+shift) for t in args)
                    rhs=sum(sn(t+K/11)*sn(t+K/11+shift) for t in args)
                    near(lhs,rhs,'cyclic_correlation')

# Even-length negative control: no claim of the same invariant is made there.
k=mp.mpf('0.7');par=k*k;K=mp.ellipk(par)
def value(t):
    D=sum(mp.ellipfun('dn',t+K*i,par) for i in range(4))
    C=sum(mp.ellipfun('cn',t+K*i,par) for i in range(4))
    return D*D-par*C*C
gap=abs(value(K/10)-value(K/3));assert gap>mp.mpf('1e-10');numeric['even_negative_control']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(exact.values()),'exact_counts':dict(exact),'numerical_diagnostics':sum(numeric.values()),'numerical_counts':dict(numeric),'families':families,'decimal_precision':mp.mp.dps,'max_scaled_residual':str(worst),'even_negative_gap':str(gap),'limits':'Numerical diagnostics are not interval certificates. The exact general proof is the audited finite telescoping argument.'},indent=2))
