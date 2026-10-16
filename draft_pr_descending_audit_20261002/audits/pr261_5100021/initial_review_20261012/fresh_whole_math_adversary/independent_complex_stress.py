"""Non-interval falsification diagnostics with direct constructions only."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'dependencies'))
import mpmath as mp
mp.mp.dps=115

def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def det(u,v): return u[0]*v[1]-u[1]*v[0]
def minus(u,v): return u[0]-v[0],u[1]-v[1]
def area(v): return sum(det(v[j],v[(j+1)%len(v)]) for j in range(len(v)))/2
def close(u,v): return abs(u-v)/(1+abs(u)+abs(v))

receipts=[]
worst=mp.mpf(0)
for N,tau,ks in [(4,1,'.001'),(4,1,'.9999'),(8,3,'.63'),(12,5,'.91'),(16,7,'.91'),(20,9,'.63'),(28,13,'.63'),(44,19,'.98')]:
    k=mp.mpf(ks); kp=mp.sqrt(1-k*k)
    K=mp.ellipk(k*k); Ki=mp.ellipk(kp*kp)
    v=2*K*tau/N; delta=2*v; h=4*K/N
    sn=lambda u:mp.ellipfun('sn',u,k*k)
    cn=lambda u:mp.ellipfun('cn',u,k*k)
    dn=lambda u:mp.ellipfun('dn',u,k*k)
    a=dn(v)/cn(v); b=kp/cn(v)
    def direct(w,sign=1):
        f=(sign*k,mp.mpf(0))
        P=[(-a*sn(w+j*delta),b*cn(w+j*delta)) for j in range(N)]
        feet=[]; anti=[]
        for j,p in enumerate(P):
            q=P[(j+1)%N]; e=minus(q,p)
            t=dot(minus(f,p),e)/dot(e,e)
            feet.append((p[0]+t*e[0],p[1]+t*e[1]))
            u,t=minus(p,f),minus(q,f)
            D=det(u,t); hu=dot(u,p); ht=dot(t,q)
            anti.append(((hu*t[1]-ht*u[1])/D,(u[0]*ht-t[0]*hu)/D))
        return area(feet),area(anti)
    def trace(w): return sum(dn(w+j*delta) for j in range(N))
    P0,B0=direct(mp.mpf('.371')*K)
    ref=P0*B0
    case={'N':N,'winding':tau,'modulus':ks,'reference_product':mp.nstr(ref,30)}
    errors={}
    for label,w in [('real_phase',mp.mpf('.839')*K),('complex_regular',mp.mpf('.234')*K+mp.mpf('.413')*1j*Ki),('antipedal_pole',1j*Ki+mp.mpf('1e-14')),('pedal_pole',K+1j*Ki-v+mp.mpf('1e-14'))]:
        P,B=direct(w)
        err=close(P*B,ref)
        assert err<mp.mpf('1e-65'),(N,tau,label,err)
        errors[label]=mp.nstr(err,8); worst=max(worst,err)
    w=mp.mpf('.247')*K+mp.mpf('.319')*1j*Ki
    P,B=direct(w); Pm,Bm=direct(w,-1)
    for label,err in [('focus_pedal_equality',close(P,Pm)),('focus_antipedal_equality',close(B,Bm)),('antipedal_evenness',close(B,direct(-w)[1])),('antipedal_imaginary_antiperiod',close(B,-direct(w+2j*Ki)[1])),('trace_complement_product',close(trace(w)*trace(w+h/2),trace(0)*trace(h/2)))]:
        assert err<mp.mpf('1e-65'),(label,err)
        errors[label]=mp.nstr(err,8); worst=max(worst,err)
    germ=[]
    for epss in ['1e-8','1e-16']:
        eps=mp.mpf(epss)
        Pp,Bp=direct(1j*Ki+eps); Pn,Bn=direct(1j*Ki-eps)
        odd_error=close(Bp,-Bn)
        assert odd_error<mp.mpf('1e-65')
        germ.append({'epsilon':epss,'antipedal_zB':mp.nstr(eps*Bp,25),'antipedal_z2B':mp.nstr(eps*eps*Bp,25),'odd_germ_error':mp.nstr(odd_error,8)})
    case['scaled_errors']=errors
    case['local_antipedal_germ']=germ
    receipts.append(case)
print(json.dumps({'status':'PASS','decimal_precision':mp.mp.dps,'cases':receipts,'maximum_scaled_error':mp.nstr(worst,10),'scope':'Non-interval diagnostics; these can falsify the theorem but do not prove all periods, divisor completeness, or cancellation.'},indent=2))
