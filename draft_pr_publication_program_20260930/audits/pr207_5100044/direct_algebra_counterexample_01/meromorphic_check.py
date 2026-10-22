"""Independent nonreal substitutions and supplemental controls, all diagnostics."""
from pathlib import Path
from datetime import datetime, timezone
import json
import mpmath as mp
from euclidean_check import geometry,orbit,area,focal_area,family,serialize,ssum
mp.mp.dps=100
maxima={key:mp.mpf(0) for key in ['Eq4','Eq9_cn','Eq9_dn','Eq10','Eq11','Eq12','Eq14','Eq17','Eq18','Eq19']}
count=0

def err(a,b): return abs(a-b)/max(1,abs(a),abs(b))
for ks,N,tau in [('0.2',4,1),('0.8',8,3),('0.999',12,5),('0.99',20,3),('0.999999',32,15)]:
    k=mp.mpf(ks); g=geometry(k,N,tau); p=k*k; K=g['K']; Kp=mp.ellipk(1-p); v=g['v']; h=g['snv']; t=h*h; q=g['cnv']**2
    a,b=g['a'],g['b']; U=1-2*p*t+p*t*t; V=1-2*t+p*t*t; W=1-p*t*t; C=b*h*g['dnv']*q*q
    sn=lambda x:mp.ellipfun('sn',x,p)
    cn=lambda x:mp.ellipfun('cn',x,p)
    dn=lambda x:mp.ellipfun('dn',x,p)
    P=lambda x:(-a*sn(x),b*cn(x))
    I=lambda x:((P(x)[0]-k)/(a+k*sn(x))**2,P(x)[1]/(a+k*sn(x))**2)
    cross=lambda x,y:x[0]*y[1]-x[1]*y[0]
    E=lambda u:C*dn(u)*(1-p*t*sn(u)**2)/((1+k*sn(u))*(U+k*V*sn(u))**2)
    B=lambda u:2*C*(1-p*t*sn(u)**2)*(U*U+p*V*(V+2*U)*sn(u)**2)/(dn(u)*(U*U-p*V*V*sn(u)**2)**2)
    r=K+1j*Kp
    phases=[K*mp.mpf('.137')+1j*Kp*mp.mpf('.231'),K*mp.mpf('.813')+1j*Kp*mp.mpf('.719'),r+2*v+mp.mpc('.000031','.000027'),1j*Kp+mp.mpc('.000021','.000013')]
    for u in phases:
        du=dn(u); D=1-p*t*sn(u)**2
        maxima['Eq4']=max(maxima['Eq4'],err(cross(P(u-v),P(u+v)),2*a*b*h*g['cnv']*du/D))
        maxima['Eq9_cn']=max(maxima['Eq9_cn'],err(cn(2*v),V/W))
        maxima['Eq9_dn']=max(maxima['Eq9_dn'],err(dn(2*v),U/W))
        maxima['Eq10']=max(maxima['Eq10'],err(cross(I(u-v),I(u+v))/2,E(u)))
        maxima['Eq11']=max(maxima['Eq11'],err((a+k*sn(u-v))*(a+k*sn(u+v)),(1+k*sn(u))*(U+k*V*sn(u))/(q*D)))
        pm=P(u-v); pp=P(u+v)
        maxima['Eq12']=max(maxima['Eq12'],err(cross((pm[0]-k,pm[1]),(pp[0]-k,pp[1])),2*b*h*g['dnv']*du*(1+k*sn(u))/D))
        maxima['Eq14']=max(maxima['Eq14'],err(E(u)+E(u+2*K),B(u)))
        maxima['Eq17']=max(maxima['Eq17'],err(sn(u+K+1j*Kp),dn(u)/(k*cn(u))))
        maxima['Eq18']=max(maxima['Eq18'],err(B(2*r-u),-B(u)))
        if N==4: maxima['Eq19']=max(maxima['Eq19'],err(B(u),2*C/U**2*(q/dn(u)+t*dn(u))))
        count+=1

# Circular endpoint, inverse-area scaling, and false period labels.
mp.mp.dps=100
supplement=[]
for N,tau in [(4,1),(8,3),(12,5),(16,7),(7,3)]:
    products=[]
    R=mp.mpf('2.37')
    for theta in [mp.mpf('.13'),mp.mpf('.777')]:
        pts=[(R*mp.cos(theta+2*mp.pi*tau*j/N),R*mp.sin(theta+2*mp.pi*tau*j/N)) for j in range(N)]
        products.append(area(pts)*focal_area(pts,0))
    expected=(mp.mpf(N)/2*mp.sin(2*mp.pi*tau/N))**2
    supplement.append({'type':'circle','N':N,'tau':tau,'error':max(abs(x-expected) for x in products)})
g=geometry(mp.mpf('.8'),12,5); pts,_=orbit(g,mp.mpf('.137')*mp.pi); prod=area(pts)*focal_area(pts,g['k'])
for scale in ['0.00000001','0.237','7.43','100000000']:
    f=mp.mpf(scale); scaled=[(x*f,y*f) for x,y in pts]
    supplement.append({'type':'physical_scale','factor':scale,'product_error':err(prod,area(scaled)*focal_area(scaled,g['k']*f))})
repeats=[]
for N,tau,least in [(12,2,6),(12,4,3),(24,2,12),(24,6,4)]:
    summary=family(mp.mpf('.8'),N,tau,['0','0.137','0.333','0.5','0.731'],formula=False)
    summary['actual_least_period']=least; repeats.append(summary)
    assert summary['minimum_earlier_return']<mp.mpf('1e-80')
assert repeats[0]['relative_product_spread']>mp.mpf('.001')
assert repeats[1]['relative_product_spread']>mp.mpf('.1')
assert repeats[2]['relative_product_spread']<mp.mpf('1e-80')
assert repeats[3]['relative_product_spread']<mp.mpf('1e-80')

# Recompute hardest case with 50 extra digits to check precision sensitivity.
mp.mp.dps=140
refinements=[]
for ks,N,tau in [('0.999999999999999999999999',8,1),('0.999999999999999999999999',12,5)]:
    refinements.append(family(mp.mpf(ks),N,tau,['0','0.137','0.333'],formula=True))
output={'created_utc':datetime.now(timezone.utc).isoformat(),'meromorphic_substitution_dps':100,'complex_point_count':count,'max_scaled_errors':maxima,'supplemental_controls':supplement,'repeated_orbit_controls':repeats,'precision_refinement_dps':140,'precision_refinements':refinements,'limits':'Diagnostic floating-point checks; algebraic reductions in algebra_check.py supply exact real/rational identities.'}
Path(__file__).with_name('supplemental_results.json').write_text(json.dumps(serialize(output),indent=2)+'\n')
print(json.dumps(serialize(output),indent=2))
assert max(maxima.values())<mp.mpf('1e-60')
