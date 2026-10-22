"""Independent geometric and complex elliptic audit. No inherited program is run.
Run: /opt/homebrew/bin/python3.11 -E -S -B -P audit_checks.py
Writes only the adjacent CHECK_RESULTS.json.
"""
import sys
sys.path.insert(0, '/Users/alec/Library/Python/3.11/lib/python/site-packages')
import mpmath as mp
import sympy as sp
from pathlib import Path
from datetime import datetime, timezone
import json, math, hashlib
mp.mp.dps=90
HERE=Path(__file__).resolve().parent
checks=[]
def s(x): return mp.nstr(x,28)
def require(label,error,tol=mp.mpf('1e-70')):
    error=abs(error)
    if not error<tol: raise RuntimeError(label+': '+s(error)+' >= '+s(tol))
    checks.append((label,s(error)))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(poly):return mp.fsum(det(poly[j],poly[(j+1)%len(poly)]) for j in range(len(poly)))/2
def rel(x,y):return abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
def sn(z,m):return mp.ellipfun('sn',z,m)
def cn(z,m):return mp.ellipfun('cn',z,m)
def dn(z,m):return mp.ellipfun('dn',z,m)
def geometric_case(N,tau,kstr,scale='1'):
    k=mp.mpf(kstr);m=k*k;kp=mp.sqrt(1-m);K=mp.ellipk(m)
    v=2*K*tau/N;b=mp.mpf(scale);a=b*dn(v,m)/kp
    al=a*cn(v,m)/dn(v,m);be=b*cn(v,m);lam=b*b*sn(v,m)**2
    f=lambda t:sn(t,m)*cn(t,m)/dn(t,m)
    P=lambda u:(-a*sn(u,m),b*cn(u,m))
    T=lambda u:mp.fsum(dn(u+2*j*v,m) for j in range(N))
    q=N//math.gcd(N,2);r=N//q
    phase_results=[]
    for phase in ('0','.137','.371','.823'):
        u=mp.mpf(phase)*K
        points=[P(u+2*j*v) for j in range(N)]
        normals=[(x/(a*a),y/(b*b)) for x,y in points]
        R=[];Q=[]
        for j,n in enumerate(normals):
            nx=normals[(j+1)%N];d=det(n,nx)
            R.append(((nx[1]-n[1])/d,(n[0]-nx[0])/d))
            ss=n[0]**2+n[1]**2;Q.append((n[0]/ss,n[1]/ss))
        ar=area(R);aq=area(Q)
        for j in range(N):
            z=u+2*j*v
            rex=(-a*dn(v,m)/cn(v,m)*sn(z+v,m),b/cn(v,m)*cn(z+v,m))
            require('R intersection formula',max(rel(R[j][c],rex[c]) for c in range(2)))
            w=K-v;pm=P(z+K-v);pp=P(z+K+v)
            qex=(b/a*(pm[0]-pp[0])/(2*cn(w,m)),(pm[1]-pp[1])/(2*cn(w,m)))
            require('Q foot vs edge identity',max(rel(Q[j][c],qex[c]) for c in range(2)))
            prev=points[j-1];nxt=points[(j+1)%N];cur=points[j]
            inc=(cur[0]-prev[0],cur[1]-prev[1]);out=(nxt[0]-cur[0],nxt[1]-cur[1])
            ni=mp.sqrt(inc[0]**2+inc[1]**2);no=mp.sqrt(out[0]**2+out[1]**2)
            inc=tuple(x/ni for x in inc);out=tuple(x/no for x in out)
            normal=normals[j];nd=normal[0]**2+normal[1]**2
            dot=inc[0]*normal[0]+inc[1]*normal[1]
            ref=tuple(inc[c]-2*dot*normal[c]/nd for c in range(2))
            require('actual reflection',max(abs(ref[c]-out[c]) for c in range(2)))
            # Chord tangent discriminant: support of C equals line offset.
            dxy=(nxt[0]-cur[0],nxt[1]-cur[1]);ln=(-dxy[1],dxy[0]);offset=ln[0]*cur[0]+ln[1]*cur[1]
            require('same-caustic tangent',rel(al*al*ln[0]**2+be*be*ln[1]**2,offset**2))
        ar_ex=a*a*b*b/(al*be)*f(v)*T(u+v)
        aq_ex=b*b/(4*cn(K-v,m)**2)*(2*f(v)-f(2*v))*T(u+K-v)
        require('R signed area trace',rel(ar,ar_ex))
        require('Q signed area trace',rel(aq,aq_ex))
        require('inner signed area trace',rel(area(points),a*b*f(v)*T(u)))
        require('closure',max(rel(P(u+2*N*v)[c],points[0][c]) for c in range(2)))
        require('confocality',rel(a*a-al*al,b*b-be*be))
        if not 0<lam<b*b or not a>b>0:raise RuntimeError('Improper geometry')
        if N%4:
            C=mp.fprod((cn(2*K*j/q,m)/sn(2*K*j/q,m))**2 for j in range(1,(q+1)//2))
            value=a*a*b**4*f(v)*(2*f(v)-f(2*v))/(4*al*be*cn(K-v,m)**2)*r*r*kp**q/(C*C)
            require('explicit product value',rel(ar*aq,value))
        require('reversal product',rel(area(list(reversed(R)))*area(list(reversed(Q))),ar*aq))
        require('three-repeat square scaling',rel(area(R*3)*area(Q*3),9*ar*aq))
        phase_results.append(dict(phase=phase,outer=s(ar),pedal=s(aq),product=s(ar*aq)))
    spread=max(mp.mpf(row['product']) for row in phase_results)-min(mp.mpf(row['product']) for row in phase_results)
    # Detailed values are rounded for output only; the full-precision explicit tests above decide PASS.
    return dict(N=N,tau=tau,k=kstr,scale=scale,a=s(a),b=s(b),lambda_=s(lam),phases=phase_results,rounded_product_spread=s(spread))
geometry=[]
for N,tau,k in ((3,1,'.7'),(5,1,'.9'),(5,2,'.6'),(6,1,'.8'),(7,3,'.98'),(10,3,'.999'),(11,4,'.1'),(14,5,'.999999'),(18,7,'.5'),(21,10,'.95')):
    geometry.append(geometric_case(N,tau,k))
geometry.append(geometric_case(5,2,'.6','7.25'))
# Direct scale check uses identical shape/phase but a different unit length.
for r1,r2 in zip(geometry[2]['phases'],geometry[-1]['phases']):
    require('length-four scaling',rel(mp.mpf(r2['product']),mp.mpf(r1['product'])*mp.mpf('7.25')**4),mp.mpf('1e-26'))
trace=[]
for kstr in ('.01','.7','.9999'):
    k=mp.mpf(kstr);m=k*k;K=mp.ellipk(m);Ki=mp.ellipk(1-m);kp=mp.sqrt(1-m)
    for q in (1,3,5,7,15,31):
        U=lambda z:mp.fsum(dn(z+2*K*j/q,m) for j in range(q))
        V=lambda z:mp.fprod(dn(z+2*K*j/q,m) for j in range(q))
        C=mp.fprod((cn(2*K*j/q,m)/sn(2*K*j/q,m))**2 for j in range(1,(q+1)//2))
        val=kp**q/(C*C)
        maxprod=mp.mpf(0);maxsum=mp.mpf(0)
        for z in (mp.mpf('.173')*K,mp.mpc('.217','.193')*K,mp.mpf('.17')*K+mp.j*Ki*mp.mpf('.73')):
            maxprod=max(maxprod,rel(U(z)*U(z+K),val))
            maxsum=max(maxsum,rel(V(z),C*U(z)))
            require('complex odd trace product',rel(U(z)*U(z+K),val),mp.mpf('1e-65'))
            require('complex product-to-sum normalization',rel(V(z),C*U(z)),mp.mpf('1e-65'))
        # Principal part and simultaneous shifted zero, with no literal evaluation at a pole.
        for shift in (0,2*K/q):
            p=mp.j*Ki-shift;h=mp.mpf('1e-22')
            require('trace simple pole residue',abs(h*U(p+h)+mp.j),mp.mpf('1e-19'))
            require('trace product near complex pole',rel(U(p+h)*U(p+h+K),val),mp.mpf('1e-40'))
            require('shifted trace zero slope',rel(U(p+h+K)/h,mp.j*val),mp.mpf('1e-19'))
        trace.append(dict(k=kstr,q=q,product=s(val),max_product_relative_error=s(maxprod),max_product_to_sum_relative_error=s(maxsum)))
even=[]
for q in (2,4,6,8):
    m=mp.mpf('.49');K=mp.ellipk(m);Ki=mp.ellipk(1-m)
    U=lambda z:mp.fsum(dn(z+2*K*j/q,m) for j in range(q))
    p=mp.j*Ki;h=mp.mpf('1e-20')
    require('even subgroup K period',rel(U(mp.mpf('.137')) , U(mp.mpf('.137')+K)))
    require('even trace product has double pole',rel(h*h*U(p+h)*U(p+h+K),-1),mp.mpf('1e-18'))
    diff=abs(U(0)**2-U(K/q)**2)
    if not diff>mp.mpf('1e-12'):raise RuntimeError('Even parity negative control failed')
    even.append(dict(q=q,real_product_difference=s(diff),scaled_double_pole=s(h*h*U(p+h)*U(p+h+K))))
# Exact rational period-four common-caustic examples from direct Cartesian geometry.
def exact_product(points):
    aa=sp.Integer(4);bb=sp.Integer(1)
    normals=[(x/aa,y/bb) for x,y in points];rr=[];qq=[]
    for j,n in enumerate(normals):
        nn=normals[(j+1)%len(points)];dd=det(n,nn)
        rr.append(((nn[1]-n[1])/dd,(n[0]-nn[0])/dd))
        ss=n[0]**2+n[1]**2;qq.append((n[0]/ss,n[1]/ss))
    def a2(poly):return sp.simplify(sum(det(poly[j],poly[(j+1)%len(poly)]) for j in range(len(poly)))/2)
    return a2(rr),a2(qq)
sq=sp.sqrt(5)
exact4_points=[[(sp.Integer(2),sp.Integer(0)),(sp.Integer(0),sp.Integer(1)),(-sp.Integer(2),sp.Integer(0)),(sp.Integer(0),-sp.Integer(1))],[(4/sq,1/sq),(-4/sq,1/sq),(-4/sq,-1/sq),(4/sq,-1/sq)]]
exact_geometry_count=0
for points in exact4_points:
    for j,cur in enumerate(points):
        prev=points[j-1];nxt=points[(j+1)%4]
        if sp.simplify(cur[0]**2/4+cur[1]**2-1)!=0:raise RuntimeError('Exact boundary incidence')
        exact_geometry_count+=1
        inc=sp.Matrix([cur[c]-prev[c] for c in range(2)]);out=sp.Matrix([nxt[c]-cur[c] for c in range(2)])
        inc=inc/sp.sqrt(inc.dot(inc));out=out/sp.sqrt(out.dot(out));normal=sp.Matrix([cur[0]/4,cur[1]])
        ref=inc-2*inc.dot(normal)/normal.dot(normal)*normal
        if any(sp.simplify(ref[c]-out[c])!=0 for c in range(2)):raise RuntimeError('Exact reflection')
        exact_geometry_count+=2
        delta=sp.Matrix([nxt[c]-cur[c] for c in range(2)]);ln=sp.Matrix([-delta[1],delta[0]]);off=ln.dot(sp.Matrix(cur))
        if sp.simplify(sp.Rational(16,5)*ln[0]**2+sp.Rational(1,5)*ln[1]**2-off**2)!=0:raise RuntimeError('Exact common caustic')
        exact_geometry_count+=1
exact4=[exact_product(points) for points in exact4_points]
if exact4 != [(sp.Integer(8),sp.Integer(4)),(sp.Integer(10),sp.Integer(5))]:raise RuntimeError(str(exact4))
# Circle coefficient identity in the k=0 limit.
x=sp.symbols('x', real=True)
f=sp.sin(x)*sp.cos(x)
coef=sp.trigsimp(f*(2*f-sp.sin(2*x)*sp.cos(2*x))/(4*sp.cos(x)**2*sp.sin(x)**2)-sp.sin(x)**2)
if coef != 0:raise RuntimeError('Circle limit '+str(coef))
result=dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),python=sys.version,mpmath=mp.__version__,sympy=sp.__version__,decimal_precision=mp.mp.dps,numerical_assertions=len(checks),geometry=geometry,odd_trace=trace,even_trace_negative_controls=even,exact_period_four_areas=[[str(x) for x in pair] for pair in exact4],exact_boundary_assertions=exact_geometry_count+2,exact_circle_coefficient='sin(v)^2',maximum_numerical_assertion_error=s(max(mp.mpf(e) for _,e in checks)),limits='Independent exact and arbitrary-precision controls. Not interval-certified; universal coverage is supplied by written analytic proof, not samples.')
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],numerical_assertions=len(checks),geometry_cases=len(geometry),odd_trace_cases=len(trace),even_negative_controls=len(even),maximum_error=result['maximum_numerical_assertion_error']),indent=2))
