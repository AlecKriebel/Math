#!/usr/bin/env python3
"""Post-exposure checks using independent tangent/normal intersections.

This script follows reading PROOF.md. It is not early independent discovery.
It imports only this family's pre-freeze Cartesian implementation, never the
submitted author or reviewer helpers. Complex dot products are bilinear.
"""
import hashlib
import json
import platform
import sys
from datetime import datetime,timezone
from pathlib import Path
import mpmath as mp
import direct_controls as direct

HERE=Path(__file__).resolve().parent


def size(x):
    return max(abs(t) for t in x)


def ser(x):
    if isinstance(x,mp.mpf):
        return mp.nstr(x,mp.mp.dps)
    if isinstance(x,mp.mpc):
        return {'real':mp.nstr(x.real,mp.mp.dps),'imag':mp.nstr(x.imag,mp.mp.dps)}
    if isinstance(x,dict):
        return {k:ser(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [ser(v) for v in x]
    return x


def family(ktext,n,tau):
    k=mp.mpf(ktext)
    kp=mp.sqrt(1-k*k)
    K=mp.ellipk(k*k)
    p=mp.j*mp.ellipk(kp*kp)
    v=2*K*tau/n
    sn=lambda w:mp.ellipfun('sn',w,k*k)
    cn=lambda w:mp.ellipfun('cn',w,k*k)
    dn=lambda w:mp.ellipfun('dn',w,k*k)
    sv,cv,dv=sn(v),cn(v),dn(v)
    a,b=dv/cv,kp/cv
    A,B=dv*dv/(cv*cv),kp/(cv*cv)
    lam=a*a-1
    P=lambda w:(-a*sn(w),b*cn(w))
    def outer(w):
        pts=P(w-v),P(w+v)
        normals=[(q[0]/(a*a),q[1]/(b*b)) for q in pts]
        return direct.solve2(normals[0],normals[1],1,1)[0]
    def anti(r,q):
        mr,mq=(r[0]-k,r[1]),(q[0]-k,q[1])
        return direct.solve2(mr,mq,direct.dot(mr,r),direct.dot(mq,q))[0]
    def U(u):
        return anti(outer(u-v),outer(u+v))
    def total(w):
        rs=[outer(w+2*j*v) for j in range(n)]
        us=[anti(rs[j],rs[(j+1)%n]) for j in range(n)]
        return tuple(mp.fsum(u[i] for u in us)/n for i in (0,1))
    real_ref=total(mp.mpf(0))
    # Canonical dimensions are a stimulus; the physical tracer re-solves its
    # caustic independently by closure and propagates reflected rays.
    independently_closed_lam=direct.periodic_lambda(a,b,n,tau)
    physical=[]
    for theta in (mp.mpf(0),mp.mpf(1)/7,mp.mpf('1.123456789')):
        verts,angle,residuals=direct.shoot(a,b,independently_closed_lam,theta,n,True)
        mean,_,_,_,_=direct.construct(a,b,verts)
        canonical_start=mp.ellipf(theta-mp.pi/2,k*k)
        canonical=[P(canonical_start+2*j*v) for j in range(n)]
        physical.append({'theta':theta,'mean':mean,
                         'max_physical_vs_canonical_vertex_error_over_a':max(size(direct.sub(x,y)) for x,y in zip(verts,canonical))/a,
                         'mean_vs_complex_real_reference':size(direct.sub(mean,real_ref))/(1+size(real_ref)),
                         'physical_residuals':residuals})
    sample=mp.mpf('.237')*K+mp.mpf('.218')*p
    r=outer(sample)
    formula_r=(-A*sn(sample),B*cn(sample))
    qminus,qplus=outer(sample-v),outer(sample+v)
    qm,qp=(qminus[0]-k,qminus[1]),(qplus[0]-k,qplus[1])
    determinant=qm[0]*qp[1]-qm[1]*qp[0]
    expected=2*B*sv*dv*dn(sample)*(a+k*sn(sample))/(1-k*k*sv*sv*sn(sample)**2)
    shifts={'sn_2K':abs(sn(sample+2*K)+sn(sample)),
            'cn_2K':abs(cn(sample+2*K)+cn(sample)),
            'dn_2K':abs(dn(sample+2*K)-dn(sample)),
            'sn_2p':abs(sn(sample+2*p)-sn(sample)),
            'cn_2p':abs(cn(sample+2*p)+cn(sample)),
            'dn_2p':abs(dn(sample+2*p)+dn(sample))}
    local,complete=[],[]
    if n>=6:
        h=mp.ellipf(mp.asin(1/a),k*k)
        centers={'dn_zero':K+p,'midpoint_Jacobi_pole':p,
                 'focal_root_1':p-h,'focal_root_2':p+2*K+h}
        for exponent in (12,24,36):
            eps=mp.power(10,-exponent)
            for name,u in centers.items():
                left,right=U(u-eps),U(u+eps)
                local.append({'kind':name,'eps':eps,
                              'two_sided_difference_normalized':size(direct.sub(left,right))/(1+size(left)+size(right)),
                              'max_value_size':max(size(left),size(right))})
            endpoint=U(p+v+eps)
            local.append({'kind':'endpoint_pole','eps':eps,'scaled_U_eps':tuple(eps*x for x in endpoint),
                          'max_value_size':size(endpoint)})
            for shift in (mp.mpf(0),2*p):
                mean=total(p+shift+eps)
                complete.append({'pole_translate':shift,'eps':eps,
                                 'mean_residual_normalized':size(direct.sub(mean,real_ref))/(1+size(real_ref)),
                                 'mean':mean})
    return {'k':k,'N':n,'tau':tau,'a':a,'b':b,'caustic_lambda':lam,
            'physical_reclosed_lambda_difference_over_b_squared':abs(lam-independently_closed_lam)/(b*b),
            'real_reference_mean':real_ref,'physical':physical,
            'actual_outer_vs_formula_normalized':size(direct.sub(r,formula_r))/(1+size(r)),
            'actual_complex_normal_determinant_vs_formula':abs(determinant-expected)/(1+abs(expected)),
            'shift_identity_residuals':shifts,'local_singularities':local,'complete_pole_neighborhoods':complete}


def main():
    mp.mp.dps=120
    stimuli=[('.63',8,3),('.2',6,1),('.7',10,3),('.98',12,5),('.63',4,1)]
    cases,failures=[],[]
    for stimulus in stimuli:
        try:
            cases.append(family(*stimulus))
        except Exception as ex:
            failures.append({'stimulus':stimulus,'error':repr(ex)})
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.executable,
             'python_version':platform.python_version(),'mpmath_version':mp.__version__,'dps':mp.mp.dps,
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'exposure':'After reading submitted PROOF.md and author scripts; root suggested .63,N8,tau3 sign adversary.',
             'code_imports':'Only own direct_controls.py; never submitted helpers.',
             'validation_class':'High-precision corroboration; universal argument requires exact analytic audit.'}
    (HERE/'post_freeze_geometry_audit.json').write_text(json.dumps(ser({'receipt':receipt,'cases':cases,'failures':failures}),indent=2)+'\n')
    print('Cases:',len(cases),'failures:',failures)
    if cases:
        print('k=.63,N8,tau3 independently ray-traced means:',[mp.nstr(x['mean'][0],40) for x in cases[0]['physical']])
        print('largest complete pole cancellation residual:',max(row['mean_residual_normalized'] for case in cases for row in case['complete_pole_neighborhoods']))


if __name__=='__main__':
    main()
