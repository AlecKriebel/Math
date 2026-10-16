#!/usr/bin/env python3
"""Fresh geometry and complete-class local tests; no submitted helpers."""
from pathlib import Path
import sys,math,json
from datetime import datetime,timezone
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor');sys.path.insert(0,str(V))
import mpmath as mp
mp.mp.dps=85
O=Path(__file__).resolve().parent
fmt=lambda x:mp.nstr(x,40)
def encode(v):
    if isinstance(v,(mp.mpc,complex)):return {'re':fmt(mp.re(v)),'im':fmt(mp.im(v))}
    return fmt(v)
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def solve(rows,rhs):
    d=det(*rows);return [(rhs[0]*rows[1][1]-rows[0][1]*rhs[1])/d,(rows[0][0]*rhs[1]-rhs[0]*rows[1][0])/d]
def I(X,Y,M):
    Q=[X[t]-M[t] for t in (0,1)];T=[Y[t]-M[t] for t in (0,1)]
    return solve([Q,T],[dot(Q,X),dot(T,Y)])
def model(k,N,tau):
    K=mp.ellipk(k*k);kp=mp.sqrt(1-k*k);p=mp.j*mp.ellipk(kp*kp);v=2*K*tau/N;delta=2*v
    sn=lambda z:mp.ellipfun('sn',z,k*k);cn=lambda z:mp.ellipfun('cn',z,k*k);dn=lambda z:mp.ellipfun('dn',z,k*k)
    s,c,d=sn(v),cn(v),dn(v);a=d/c;b=kp/c;A=d*d/(c*c);B=kp/(c*c)
    def P(z):return [-a*sn(z),b*cn(z)]
    def Rt(z):
        x,y=P(z-v),P(z+v)
        return solve([[x[0]/(a*a),x[1]/(b*b)],[y[0]/(a*a),y[1]/(b*b)]],[1,1])
    def R(z):return [-A*sn(z),B*cn(z)]
    return K,p,v,delta,a,b,s,c,d,P,Rt,R,sn,cn,dn
rows=[];maxdev=mp.mpf(0);minreal=mp.inf;maxcaustic=mp.mpf(0);maxouter=mp.mpf(0)
for kk in ('0.15','0.63','0.97'):
    k=mp.mpf(kk)
    for N in (4,6,8,10,12,14,18):
        for tau in range(1,N//2):
            if math.gcd(tau,N)!=1:continue
            K,p,v,delta,a,b,s,c,d,P,Rt,R,sn,cn,dn=model(k,N,tau)
            Cs=[]
            for phase in (mp.mpf(0),K/17,K*mp.mpf('0.71'),K*mp.mpf('1.93')):
                # Rt midpoint phase is original phase plus v; the outer construction is raw tangent solving.
                Ps=[P(phase+i*delta) for i in range(N)]
                Rs=[Rt(phase+v+i*delta) for i in range(N)]
                for i in range(N):
                    maxouter=max(maxouter,*(abs(Rs[i][t]-R(phase+v+i*delta)[t]) for t in (0,1)))
                    X,Y=Ps[i],Ps[(i+1)%N];normal=[Y[1]-X[1],X[0]-Y[0]];offset=dot(normal,X)
                    # Segment tangent to caustic x²+y²/kp²=1 (canonical scale).
                    maxcaustic=max(maxcaustic,abs(offset*offset-normal[0]**2-(1-k*k)*normal[1]**2))
                for sig in (-1,1):
                    M=[sig*k,mp.mpf(0)];Us=[I(Rs[i],Rs[(i+1)%N],M) for i in range(N)]
                    C=[sum(U[t] for U in Us)/N for t in (0,1)]
                    Cs.append((sig,C))
                    for i in range(N):minreal=min(minreal,abs(det([Rs[i][t]-M[t] for t in (0,1)],[Rs[(i+1)%N][t]-M[t] for t in (0,1)])))
            plus=[C for sig,C in Cs if sig==1];minus=[C for sig,C in Cs if sig==-1]
            dev=max(abs(C[t]-plus[0][t]) for C in plus for t in (0,1));dev=max(dev,max(abs(C[t]-minus[0][t]) for C in minus for t in (0,1)))
            axis=max(abs(C[1]) for sig,C in Cs);focusneg=max(abs(plus[j][t]+minus[j][t]) for j in range(4) for t in (0,1))
            maxdev=max(maxdev,dev,axis,focusneg)
            rows.append({'k':kk,'N':N,'tau':tau,'phase_and_symmetry_max_error':fmt(max(dev,axis,focusneg)),'centroid_plus':list(map(fmt,plus[0]))})
assert maxdev<mp.mpf('1e-65'),maxdev
assert maxouter<mp.mpf('1e-65'),maxouter
assert maxcaustic<mp.mpf('1e-60'),maxcaustic
# All classes on common torus; independently use explicit focal-root representatives.
k=mp.mpf('0.63');N=10;tau=3
K,p,v,delta,a,b,s,c,d,P,Rt,R,sn,cn,dn=model(k,N,tau);M=[k,0]
local=[]
centers={'dn_zero':[K+p+2*m*K+2*n*p for m in (0,1) for n in (0,1)],'unshifted_jacobi_pole':[p+2*m*K+2*n*p for m in (0,1) for n in (0,1)],'focal_isotropic_root':[-K+p+sgn*v+2*n*p for sgn in (-1,1) for n in (0,1)],'endpoint_pole':[p+sgn*v+2*m*K+2*n*p for sgn in (-1,1) for m in (0,1) for n in (0,1)]}
for name,pts in centers.items():
    for center in pts:
        values=[]
        for exponent in (12,20,28):
            eps=mp.mpf(10)**(-exponent);U=I(R(center+eps-v),R(center+eps+v),M)
            values.append({'eps':fmt(eps),'U':list(map(encode,U)),'eps_U_max':fmt(max(abs(eps*x) for x in U)),'eps2_U_max':fmt(max(abs(eps*eps*x) for x in U))})
        if name!='endpoint_pole':assert mp.mpf(values[-1]['eps_U_max'])<mp.mpf('1e-23'),(name,values)
        else:assert mp.mpf(values[-1]['eps2_U_max'])<mp.mpf('1e-23'),(name,values)
        focal_res=abs(a+k*sn(center)) if name=='focal_isotropic_root' else None
        local.append({'class':name,'center':encode(center),'values':values,'focal_root_error':fmt(focal_res) if focal_res is not None else None})
# Actual four incident edge residues at every pole translate, not a generic algebra surrogate.
actual=[]
for center in centers['unshifted_jacobi_pole']:
    eps=mp.mpf('1e-28');Rs=[R(center+eps+i*delta) for i in range(N)]
    edges=[N-1,0,N//2-1,N//2];res=[]
    for i in edges:res.append([eps*x for x in I(Rs[i],Rs[(i+1)%N],M)])
    total=[sum(x[t] for x in res) for t in (0,1)]
    assert max(map(abs,total))<mp.mpf('1e-22'),total
    actual.append({'pole_center':encode(center),'edge_indices':edges,'scaled_actual_edge_intersections':[[encode(y) for y in x] for x in res],'sum_scaled':list(map(encode,total))})
# Wide-reading raw geometry counterexample independent of the exact script.
q=(4-mp.sqrt(13))/3;x=2*mp.sqrt(1-q*q);orig=[[0,mp.mpf(1)],[x,-q],[-x,-q]];M=[mp.sqrt(3),0]
outer=[]
for i in range(3):outer.append(solve([[orig[i][0]/4,orig[i][1]],[orig[(i+1)%3][0]/4,orig[(i+1)%3][1]]],[1,1]))
odd=[]
for sig in (-1,1):
    Rs=[[X[0],sig*X[1]] for X in outer];Rs+=Rs
    Us=[I(Rs[i],Rs[(i+1)%6],M) for i in range(6)]
    C=[sum(U[t] for U in Us)/6 for t in (0,1)];odd.append({'vertical_sign':sig,'centroid':list(map(fmt,C))})
output={'utc':datetime.now(timezone.utc).isoformat(),'runtime':{'python':sys.version,'mpmath':mp.__version__,'dps':mp.mp.dps,'vendor':str(V)},'primitive_even_cases':rows,'max_phase_and_symmetry_error':fmt(maxdev),'min_actual_real_antipedal_determinant':fmt(minreal),'max_raw_tangent_vs_closed_outer_error':fmt(maxouter),'max_confocal_segment_tangency_residual':fmt(maxcaustic),'all_class_local_probes':local,'all_translate_actual_four_edge_residues':actual,'raw_geometry_double_odd_counterexample':odd,'limitation':'finite high-precision samples corroborate exact derivations; not interval proofs or all-period proofs'}
(O/'INDEPENDENT_NUMERIC.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ('utc','max_phase_and_symmetry_error','min_actual_real_antipedal_determinant','max_raw_tangent_vs_closed_outer_error','max_confocal_segment_tangency_residual','raw_geometry_double_odd_counterexample')},indent=2))
