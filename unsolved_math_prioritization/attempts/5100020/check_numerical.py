#!/usr/bin/env python3
"""High-precision diagnostics, explicitly not exact certificates or proofs.
Uses direct original-side projections and antipedal line intersections.
"""
import mpmath as m
from math import gcd
import json
from collections import Counter
m.mp.dps=95;C=Counter();worst=m.mpf(0)
def ckerr(e,label,scale=1):
    global worst
    e=abs(e)/max(1,abs(scale));worst=max(worst,e)
    assert e<m.mpf('1e-70'),(label,m.nstr(e,10))
    C[label]+=1

def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def area(ps):return sum(cross(ps[i-1],ps[i]) for i in range(len(ps)))/2
def meet(p,q):
    hp,hq=dot(p,p),dot(q,q);d=cross(p,q)
    return m.matrix([(hp*q[1]-hq*p[1])/d,(p[0]*hq-q[0]*hp)/d])
def edge(p,q):
    hp,hq=dot(p,p),dot(q,q)
    return (hp*hq-(hp+hq)*dot(p,q)/2)/cross(p,q)
rows=[]
for kval in ('.2','.6','.9'):
    k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);ip=m.j*m.ellipk(1-k*k)
    sn=lambda z:m.ellipfun('sn',z,k*k);cn=lambda z:m.ellipfun('cn',z,k*k);dn=lambda z:m.ellipfun('dn',z,k*k)
    for N in (3,5,7,9,11,13,15):
        for tau in range(1,N//2+1):
            if gcd(tau,N)!=1:continue
            v=2*K*tau/N;delta=2*v;a=dn(v)/cn(v);b=kp/cn(v);ell=2*K/N
            P=lambda w:m.matrix([-a*sn(w),b*cn(w)])
            Ssum=lambda w:sum(dn(w+j*delta) for j in range(N))
            vals=[]
            for phase in ('.137','.439','.813'):
                w=K*m.mpf(phase);ps=[P(w+j*delta) for j in range(N)]
                rs=[meet(ps[j],ps[(j+1)%N]) for j in range(N)];qs=[]
                for j,p in enumerate(ps):
                    q=ps[(j+1)%N];side=q-p;foot=p-dot(p,side)/dot(side,side)*side;qs.append(foot)
                    ckerr(dot(foot,side),'direct_perpendicular_foot')
                    ckerr(cross(foot-p,side),'named_side_collinearity')
                    ckerr(dot(p,rs[j])-dot(p,p),'first_antipedal_line',dot(p,p))
                    ckerr(dot(q,rs[j])-dot(q,q),'second_antipedal_line',dot(q,q))
                    assert cross(p,q)>0;C['real_intersection_finite']+=1
                    u=w+(j+m.mpf('.5'))*delta
                    n=m.matrix([-sn(u),cn(u)/kp])
                    ckerr(dot(n,p)-1,'caustic_chord_first');ckerr(dot(n,q)-1,'caustic_chord_second')
                    explicit=m.matrix([-kp*kp*sn(u)/dn(u)**2,kp*cn(u)/dn(u)**2])
                    ckerr(m.norm(foot-explicit),'pedal_formula_vs_direct',m.norm(explicit))
                U=area(rs);T=area(qs)
                ckerr(U-sum(edge(ps[j-1],ps[j]) for j in range(N)),'area_identity_vs_intersections',U)
                vals.append((U/Ssum(w),T/Ssum(w+v+K),U*T,Ssum(w)*Ssum(w+ell/2)))
            for row in vals[1:]:
                for j,label in enumerate(('antipedal_two_pole_ratio','pedal_two_pole_ratio','source_product','dn_half_period_product')):ckerr(row[j]-vals[0][j],label,vals[0][j])
            # Meromorphic pole symmetry diagnostics at generic nonsingular complex points.
            z=m.mpf('.037')+m.j*m.mpf('.021')
            ckerr(m.norm(P(ip+z)+P(ip-z)),'vertex_odd_reflection')
            ckerr(m.norm(P(ip+v)+P(ip-v)),'opposite_endpoint_type')
            ckerr(m.norm(P(K+ip+v)-P(K+ip-v)),'coincident_endpoint_type')
            rows.append({'k':kval,'N':N,'tau':tau,'area_product_display':m.nstr(vals[0][2],25)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','assertions':sum(C.values()),'families':dict(C),'billiard_families':len(rows),'decimal_digits':m.mp.dps,'max_scaled_residual':m.nstr(worst,8),'rows':rows,'scope':'Finite high-precision observations only; not interval certificates or a proof of invariant identities.'},indent=2))
