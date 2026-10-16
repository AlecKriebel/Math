#!/usr/bin/env python3
"""Independent high precision pole/zero diagnostics; not validated numerics or proof."""
from collections import Counter
from math import gcd
import json
import mpmath as m
m.mp.dps=220
counts=Counter();worst=m.mpf(0)
TOL=m.mpf('1e-80')
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(ps):return sum(det(ps[i],ps[(i+1)%len(ps)]) for i in range(len(ps)))/2
def err(x,y,label):
    global worst
    e=abs(x-y)/max(1,abs(x),abs(y));worst=max(worst,e)
    assert e<TOL,(label,m.nstr(e,12))
    counts[label]+=1

def meet(p,q):
    h,g=dot(p,p),dot(q,q);c=det(p,q)
    return m.matrix([(h*q[1]-g*p[1])/c,(p[0]*g-q[0]*h)/c])
def F(p,q):
    h,g=dot(p,p),dot(q,q)
    return (h*g-(h+g)*dot(p,q)/2)/det(p,q)
rows=[]
configs=[]
for kval in ('0.02','0.7','0.98'):
    for n,tau in ((3,1),(5,2),(9,4),(21,2),(31,15)):
        configs.append((kval,n,tau))
for kval in ('1e-20','0.9999999999999999999999999'):
    configs.extend((kval,n,tau) for n,tau in ((3,1),(9,4)))
for kval,n,tau in configs:
    assert gcd(n,tau)==1 and n%2==1
    k=m.mpf(kval);kp=m.sqrt(1-k*k);K=m.ellipk(k*k);ip=m.j*m.ellipk(1-k*k)
    sn=lambda z:m.ellipfun('sn',z,k*k)
    cn=lambda z:m.ellipfun('cn',z,k*k)
    dn=lambda z:m.ellipfun('dn',z,k*k)
    v=2*K*tau/n;delta=2*v;ell=2*K/n
    a=dn(v)/cn(v);b=kp/cn(v)
    P=lambda z:m.matrix([-a*sn(z),b*cn(z)])
    Q=lambda z:m.matrix([-kp*kp*sn(z)/dn(z)**2,kp*cn(z)/dn(z)**2])
    trace=lambda z:sum(dn(z+j*delta) for j in range(n))
    def evaluate(w,verifyfeet=False):
        ps=[P(w+j*delta) for j in range(n)]
        rs=[meet(ps[j],ps[(j+1)%n]) for j in range(n)]
        qs=[Q(w+v+j*delta) for j in range(n)]
        U=area(rs);Ap=area(qs)
        err(U,sum(F(ps[j],ps[(j+1)%n]) for j in range(n)),'actual_antipedal_vs_edge_function')
        if verifyfeet:
            for j,p in enumerate(ps):
                q=ps[(j+1)%n];side=q-p
                foot=p-dot(p,side)/dot(side,side)*side
                for d in range(2):err(foot[d],qs[j][d],'origin_foot_actual_original_line')
                err(dot(ps[j],rs[j]),dot(ps[j],ps[j]),'antipedal_first_named_line')
                err(dot(ps[(j+1)%n],rs[j]),dot(ps[(j+1)%n],ps[(j+1)%n]),'antipedal_second_named_line')
        Sw=trace(w);Sv=trace(w+v+K)
        return U/Sw,Ap/Sv,U*Ap,Sw*trace(w+ell/2)
    base=evaluate(K*m.mpf('0.217'),True)
    points=[K*m.mpf('0.819'),K*(m.mpf('0.113')+m.j*m.mpf('0.097'))]
    for w in points:
        vals=evaluate(w,True)
        for i,label in enumerate(('antipedal_trace_ratio','origin_pedal_trace_ratio','source_product','trace_half_period_product')):err(vals[i],base[i],label)
    # Both limiting phase types: U pole / pedal zero, and U zero / pedal pole.
    for exponent in (10,22):
        z=K*m.power(10,-exponent)*(1+m.j*m.mpf('0.371'))
        for center,label in ((ip,'vertex_and_opposite_collision'),(K+ip-v,'coincident_midpoint_and_pedal_collision')):
            vals=evaluate(center+z)
            for i,name in enumerate(('antipedal_trace_ratio','origin_pedal_trace_ratio','source_product','trace_half_period_product')):err(vals[i],base[i],label+'_'+name)
        # A local exact cancellation identity evaluated separately, with no quotient by total area.
        G=lambda zz:F(P(ip+zz),P(ip+delta+zz))
        left=F(P(ip-delta+z),P(ip+z));right=G(z)
        err(left+right,G(z)-G(-z),'incident_F_odd_Laurent_identity')
        # Coincident numerator vanishes to second order; chart denominator to first order.
        mid=K+ip+z;pp=P(mid-v);qq=P(mid+v)
        h,g=dot(pp,pp),dot(qq,qq)
        numerator=h*g-(h+g)*dot(pp,qq)/2
        other=((h+g)*dot(pp-qq,pp-qq)-(h-g)**2)/4
        err(numerator,other,'coincident_numerator_factorization_complex')
    # Forced trace zeros measured without evaluating a derived polygon at its singular complex phase.
    err(trace(ip+ell/2),0,'trace_forced_zero')
    # Anti-period and correct real lattice, at nonsingular complex phase.
    w=K*m.mpf('0.271')+m.j*K*m.mpf('0.039')
    err(trace(w+ell),trace(w),'trace_real_lattice')
    err(trace(w+2*ip),-trace(w),'trace_imaginary_antiperiod')
    rows.append({'k':kval,'N':n,'tau':tau,'source_product':m.nstr(base[2],30),'near_pole_exponents':[10,22]})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','decimal_digits':m.mp.dps,'max_scaled_residual':m.nstr(worst,12),'tolerance':str(TOL),'billiard_families':len(rows),'assertions':sum(counts.values()),'families':dict(counts),'rows':rows,'scope':'Unvalidated finite high precision diagnostics. Universal claims are proved in INDEPENDENT_DERIVATION.md.'},indent=2))
