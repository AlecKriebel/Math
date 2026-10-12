"""Independent controls; does not import submitted or prior checker code."""
from pathlib import Path
from datetime import datetime,timezone
import math,json,hashlib
import sympy as sy
import mpmath as mp
OUT=Path(__file__).resolve().parent
k,s,S,C,D,c,d,t=sy.symbols('k s S C D c d t')
L=1-k*k*s*s*S*S; H=1-2*k*k*s*s+k*k*s**4
# Rationalize k'=t; impose t^2=1-k^2 only after clearing denominators.
R=sy.Matrix([-(H*S+k*(c*c-d*d*S*S))/(c*c*L), C*(2*t*t-H*(1+k*S))/(t*c*c*L)])
minus=sy.Matrix([-d/c*(S*c*d-s*C*D)/L,t/c*(C*c+S*s*D*d)/L])
plus=sy.Matrix([-d/c*(S*c*d+s*C*D)/L,t/c*(C*c-S*s*D*d)/L])
F=sy.Matrix([k,0])
G=sy.groebner([C*C-(1-S*S),D*D-(1-k*k*S*S),c*c-(1-s*s),d*d-(1-k*k*s*s),t*t-(1-k*k)], C,D,c,d,t,S,s,k)
def rem(expr):
    num=sy.fraction(sy.cancel(expr))[0]
    return str(sy.expand(G.reduce(sy.expand(num))[1]))
inc=[rem((P-F).dot(R-P)) for P in (minus,plus)]
det=sy.det(sy.Matrix.hstack(minus-F,plus-F))
det_rem=rem(det-2*t*s*d*D*(1+k*S)/(c*L))
normal=sy.Matrix([-S,C/t])
q=F+(1-normal.dot(F))/normal.dot(normal)*normal
qexpected=sy.Matrix([(k-S)/(1-k*S),t*C/(1-k*S)])
q_rem=[rem(q[j]-qexpected[j]) for j in (0,1)]
assert inc==['0','0'] and det_rem=='0' and q_rem==['0','0']
mp.mp.dps=70
jac=mp.ellipfun
numeric=[]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def area(ps):return sum(cross(ps[i],ps[(i+1)%len(ps)]) for i in range(len(ps)))/2
def calc(kk,N,tau,w,focus_sign=1):
    K=mp.ellipk(kk**2);v=2*K*tau/N;delta=2*v
    sn=lambda x:jac('sn',x,kk**2);cn=lambda x:jac('cn',x,kk**2);dn=lambda x:jac('dn',x,kk**2)
    a=dn(v)/cn(v);b=mp.sqrt(1-kk**2)/cn(v);f=(focus_sign*kk,mp.mpf(0))
    ps=[(-a*sn(w+i*delta),b*cn(w+i*delta)) for i in range(N)]
    qs=[];rs=[];detmin=mp.inf
    for i in range(N):
        P,Q=ps[i],ps[(i+1)%N];u=(Q[0]-P[0],Q[1]-P[1]);u2=u[0]**2+u[1]**2
        tt=((f[0]-P[0])*u[0]+(f[1]-P[1])*u[1])/u2
        qs.append((P[0]+tt*u[0],P[1]+tt*u[1]))
        n1=(P[0]-f[0],P[1]-f[1]);n2=(Q[0]-f[0],Q[1]-f[1]);D0=cross(n1,n2)
        r1=n1[0]*P[0]+n1[1]*P[1];r2=n2[0]*Q[0]+n2[1]*Q[1]
        rs.append(((r1*n2[1]-n1[1]*r2)/D0,(n1[0]*r2-r1*n2[0])/D0));detmin=min(detmin,abs(D0))
    A=area(qs);B=area(rs);T=sum(dn(w+j*delta) for j in range(N));shift=K+v
    Tq=sum(dn(w+shift+j*delta) for j in range(N))
    return A,B,A*B,T,Tq,detmin
for N in (4,8,12,20):
    for tau in range(1,N//2):
        if math.gcd(tau,N)!=1:continue
        for ks in ('0.05','0.4','0.85','0.99'):
            kk=mp.mpf(ks);K=mp.ellipk(kk*kk);phases=[mp.mpf(z)*K for z in ('0.013','0.19','0.63','1.27')]
            values=[calc(kk,N,tau,w) for w in phases];base=values[0]
            rel=lambda x,y:abs(x-y)/(1+abs(x)+abs(y))
            err=max(rel(z[2],base[2]) for z in values)
            erra=max(rel(z[0]/z[4],base[0]/base[4]) for z in values)
            errb=max(rel(z[1]/z[3],base[1]/base[3]) for z in values)
            twin=calc(kk,N,tau,phases[1],-1);errfocus=max(rel(twin[i],values[1][i]) for i in range(3))
            assert err<mp.mpf('1e-55') and erra<mp.mpf('1e-55') and errb<mp.mpf('1e-55') and errfocus<mp.mpf('1e-55')
            assert all(z[0]>0 and z[5]>0 for z in values)
            numeric.append({'N':N,'tau':tau,'k':ks,'product_relative_error':str(err),'pedal_trace_error':str(erra),'antipedal_trace_error':str(errb),'two_focus_error':str(errfocus),'B_sign':int(mp.sign(base[1])),'minimum_real_normal_determinant':str(min(z[5] for z in values))})
# Explicit repeated traversal control: exact domain excludes it, but shoelace scaling is N^2.
kk=mp.mpf('.4');primitive=calc(kk,4,1,mp.mpf('.27'));repeat=calc(kk,8,2,mp.mpf('.27'))
repeaterr=max(abs(repeat[i]-2*primitive[i]) for i in (0,1))
assert abs(repeat[2]-4*primitive[2])<mp.mpf('1e-55')
# Non-even least period traces not being claimed; output three phase-varying products as a guard.
oddvals=[calc(mp.mpf('.6'),3,1,mp.mpf(w))[2] for w in ('.1','.3','.8')]
result={'created_utc':datetime.now(timezone.utc).isoformat(),'symbolic':{'antipedal_original_line_incidence_remainders':inc,'determinant_remainder':det_rem,'pedal_projection_remainders':q_rem},'numeric_domain_cases':numeric,'numeric_case_count':len(numeric),'repeat_4_twice_vs_4_area_error':str(repeaterr),'repeat_product_scaling':4,'outside_domain_3_period_products':[str(z) for z in oddvals],'limitations':'Finite diagnostics support but do not prove all-period meromorphic reasoning; nonprimitive and non-0-mod-4 cases are not promoted.'}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'symbolic':result['symbolic'],'numeric_cases':len(numeric),'max_product_error':str(max(mp.mpf(x['product_relative_error']) for x in numeric)),'outside_domain_3_period_products':result['outside_domain_3_period_products']},indent=2))
