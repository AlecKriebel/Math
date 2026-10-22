"""Independent checks. Python -B; uses existing mpmath without installation."""
import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from math import gcd
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'pr200_5100007/math_algebra_family_01/runtime_packages'))
import mpmath as mp
mp.mp.dps = 65

def det(x,y): return x[0]*y[1]-x[1]*y[0]
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def area(v): return sum(det(v[i],v[(i+1)%len(v)]) for i in range(len(v)))/2
def funcs(k):
    m=k*k
    return lambda u: tuple(mp.ellipfun(t,u,m) for t in ('sn','cn','dn'))
def setup(k,N,tau):
    f=funcs(k); K=mp.ellipk(k*k); Kp=mp.ellipk(1-k*k)
    h=2*K*tau/N; p,q,r=f(h); alpha=mp.mpf(2); beta=alpha*mp.sqrt(1-k*k)
    return f,K,Kp,h,alpha,beta,alpha*r/q,beta/q
def orbit(data,N,u,M=(0,0)):
    f,K,Kp,h,al,be,a,b=data; ps=[]; bs=[]; qs=[]; ns=[]
    for i in range(N):
        s,c,d=f(u+2*i*h); ps.append((-a*s,b*c))
        s,c,d=f(u+(2*i+1)*h); bs.append((-al*s,be*c)); n=(-s/al,c/be)
        z=(1-dot(n,M))/dot(n,n); qs.append(tuple(M[j]+z*n[j] for j in range(2))); ns.append(n)
    C=sum(det(ns[i],ns[(i+1)%N])*dot(ns[i],ns[(i+1)%N])/(dot(ns[i],ns[i])*dot(ns[(i+1)%N],ns[(i+1)%N])) for i in range(N))/4
    return area(ps),area(bs),area(qs),C,ps,bs,qs,ns
def out(x): return mp.nstr(x,12)
def relspread(v): return max(abs(x-v[0]) for x in v)/(1+abs(v[0]))

errors={'product':mp.mpf(0),'pedal_contact_ratio':mp.mpf(0),'radial':mp.mpf(0),'line_incidence':mp.mpf(0),'reversal':mp.mpf(0),'area_sum':mp.mpf(0)}
cases=0
for ks in ('0.15','0.6','0.92','0.999'):
    k=mp.mpf(ks)
    for N in (4,8,12,16,20):
        for tau in range(1,N//2):
            if gcd(tau,N)!=1: continue
            data=setup(k,N,tau); f,K,Kp,h,al,be,a,b=data
            vals={M:[] for M in ((0,0),(mp.mpf('.3'),mp.mpf('-.7')),(mp.mpf('20'),mp.mpf('31')))}
            ratios={M:[] for M in vals}
            for u in (K*mp.mpf('.071'),K*mp.mpf('.237'),K*mp.mpf('.584')):
                A,I,B0,C,ps,bs,qs,ns=orbit(data,N,u)
                S=sum(f(u+2*i*h)[2] for i in range(N)); p,q,r=f(h)
                errors['area_sum']=max(errors['area_sum'],abs(A-a*b*p*q/r*S)/(1+abs(A)))
                for i in range(N):
                    errors['line_incidence']=max(errors['line_incidence'],abs(dot(ns[i],ps[i])-1),abs(dot(ns[i],ps[(i+1)%N])-1))
                for M in vals:
                    Ap,Ip,B,Cp,psp,bsp,qsp,nsp=orbit(data,N,u,M)
                    vals[M].append(Ap*B); ratios[M].append(B/Ip)
                    errors['radial']=max(errors['radial'],abs(B-B0-dot(M,M)*C)/(1+abs(B)))
                    errors['reversal']=max(errors['reversal'],abs(area(list(reversed(psp)))*area(list(reversed(qsp)))-Ap*B)/(1+abs(Ap*B)))
                cases+=1
            for M in vals:
                errors['product']=max(errors['product'],relspread(vals[M]))
                errors['pedal_contact_ratio']=max(errors['pedal_contact_ratio'],relspread(ratios[M]))

data=setup(mp.mpf('.6'),8,3); f,K,Kp,h,al,be,a,b=data
A,I,B,C,*_=orbit(data,8,K*mp.mpf('.17'))
radius=mp.sqrt(-B/C)
sign_cases=[]
for factor in (0,1,2):
    M=(radius*factor,0)
    values=[orbit(data,8,K*u,M)[2] for u in (mp.mpf('.11'),mp.mpf('.36'),mp.mpf('.73'))]
    sign_cases.append({'radius_factor':factor,'pedal_areas':[out(x) for x in values]})

pole_checks=[]
for N,tau in ((4,1),(8,3),(12,5)):
    data=setup(mp.mpf('.6'),N,tau); f,K,Kp,h,al,be,a,b=data; T=4*K/N; d=2*h
    analytic=2j*a*b*(f(d)[2]-1)/(mp.mpf('.36')*f(d)[0])
    e=mp.mpf('1e-18')
    A,I,B,C,*_=orbit(data,N,1j*Kp+e,(mp.mpf('.3'),mp.mpf('.4')))
    A2,I2,B2,C2,*_=orbit(data,N,T/2+1j*Kp+e,(mp.mpf('.3'),mp.mpf('.4')))
    pole_checks.append({'N':N,'tau':tau,'A_residue_relative_error':out(abs(e*A-analytic)/(1+abs(analytic))),
        'B_at_A_pole_over_e':out(B/e),'A_at_B_pole_over_e':out(A2/e),'B_residue':out(e*B2)})

data=setup(mp.mpf('.6'),6,1); f,K,*_=data
repeated=[]
for u in (K*mp.mpf('.07'),K*mp.mpf('.31')):
    A,I,B,C,ps,bs,qs,ns=orbit(data,6,u,(mp.mpf('.3'),mp.mpf('.4')))
    repeated.append(out(area(ps+ps)*area(qs+qs)))

result={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version.split()[0],'mpmath':mp.__version__,'digits':mp.mp.dps,
        'phase_cases':cases,'max_errors':{k:out(v) for k,v in errors.items()},'signed_zero_negative_cases':sign_cases,
        'zero_radius':out(radius),'complex_pole_checks':pole_checks,'nonprimitive_6_repeated_twice_product':repeated,
        'note':'Finite checks support, but do not replace, the analytic proof. The repeated-list example refutes a literal displayed-list-length interpretation.'}
Path(__file__).with_name('reproduction_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
