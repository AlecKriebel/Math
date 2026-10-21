"""Numeric diagnostics for the independently derived telescoping/Fourier route."""
from pathlib import Path
from datetime import datetime, timezone
import json
import mpmath as mp
from euclidean_check import geometry,orbit,area,focal_area,ssum,serialize
mp.mp.dps=120
cases=[]
for ks,N,tau in [('0.2',4,1),('0.8',8,3),('0.999',12,5),('0.99',20,3),('0.999999',32,15),('0.8',1024,1),('0.999999999999999999999999',12,5)]:
    k=mp.mpf(ks); g=geometry(k,N,tau); p=k*k; kp=g['beta']; K=g['K']; v=g['v']; delta=2*v; m=N//2
    h=g['snv']; cv=g['cnv']; dv=g['dnv']; t=h*h; q=cv*cv
    U=1-2*p*t+p*t*t; V=1-2*t+p*t*t; W=1-p*t*t
    C=g['b']*h*dv*q*q; ca=g['a']*g['b']*h*cv/dv
    a0=q/(U-V)**2
    Lam=U*(p*p*t**3+p*p*t*t-5*p*t+p+2)/(2*kp**4*W**3)
    a1=(Lam-a0)/2
    a2=(V*V-U*U*t)/(4*h*cv*dv*(U*U-p*V*V)*(U-V))
    sn=lambda z:mp.ellipfun('sn',z,p)
    cn=lambda z:mp.ellipfun('cn',z,p)
    dn=lambda z:mp.ellipfun('dn',z,p)
    F=lambda z:1/dn(z)
    Fprime=lambda z:p*sn(z)*cn(z)/dn(z)**2
    B=lambda z:2*C*(1-p*t*sn(z)**2)*(U*U+p*V*(V+2*U)*sn(z)**2)/(dn(z)*(U*U-p*V*V*sn(z)**2)**2)
    max_identity=mp.mpf(0)
    for u in [K*mp.mpf('.137'),K*mp.mpf('.713')+mp.mpc('.031','.097')]:
        rhs=2*C*(a0*F(u)+a1*(F(u+delta)+F(u-delta))+a2*(Fprime(u+delta)-Fprime(u-delta)))
        max_identity=max(max_identity,abs(rhs-B(u))/max(1,abs(rhs),abs(B(u))))
    nome=mp.exp(-mp.pi*mp.ellipk(1-p)/K); nome_new=nome**m
    th2=mp.jtheta(2,0,nome_new); th3=mp.jtheta(3,0,nome_new); th4=mp.jtheta(4,0,nome_new)
    mod_new=(th2/th3)**2; kp_new=(th4/th3)**2; K_new=mp.pi*th3**2/2; lam=m*K_new/K
    cyclic_constant=lam*lam*kp_new
    predicted_product=2*ca*(2*C*Lam/kp)*cyclic_constant
    products=[]; max_fourier=mp.mpf(0); max_half=mp.mpf(0); max_ratio=mp.mpf(0)
    for phase in ['0','0.137','0.333']:
        theta=mp.pi*mp.mpf(phase); w=mp.ellipf(theta-mp.pi/2,p); pts,_=orbit(g,theta)
        A=area(pts); inv=focal_area(pts,k); products.append(A*inv)
        S=ssum(g,w)
        reduced=lam*mp.ellipfun('dn',lam*w,mod_new**2)
        max_fourier=max(max_fourier,abs(S-reduced)/max(1,abs(S)))
        max_half=max(max_half,abs(S*ssum(g,w+K/m)-cyclic_constant)/max(1,abs(cyclic_constant)))
        max_ratio=max(max_ratio,abs(inv-(2*C*Lam/kp)*ssum(g,w+K+v))/max(1,abs(inv)))
    product_error=max(abs(x-predicted_product)/max(1,abs(predicted_product)) for x in products)
    cases.append({'k_input':ks,'N':N,'tau':tau,'telescoping_identity_error':max_identity,'cyclic_reduction_error':max_ratio,'fourier_multiplication_error':max_fourier,'half_shift_constant_error':max_half,'predicted_product_error':product_error,'predicted_product':predicted_product,'Lambda':Lam})
result={'created_utc':datetime.now(timezone.utc).isoformat(),'precision_dps':120,'cases':cases,'limits':'Diagnostic substitutions; universal derivation is in DIRECT_TELESCOPING_PROOF.md and exact rational certificate in telescoping_certificate.py. No novelty claim.'}
Path(__file__).with_name('telescoping_numeric.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
print(json.dumps(serialize(result),indent=2))
assert max(c[key] for c in cases for key in ['telescoping_identity_error','cyclic_reduction_error','fourier_multiplication_error','half_shift_constant_error','predicted_product_error'])<mp.mpf('1e-75')
