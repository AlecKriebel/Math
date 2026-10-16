#!/usr/bin/env python3
"""R2 supplementary high-precision attacks, independent of bundled code.

Uses scratch-installed mpmath 1.3.0 with parameter m=k**2. These residuals
are unvalidated diagnostics; the review's universal conclusion is analytic.
"""
from pathlib import Path
import sys, math, json, datetime
sys.path.insert(0, str(Path(__file__).parent/'scratch/python_dependencies'))
import mpmath as mp
mp.mp.dps = 100

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def sub(x,y): return [a-b for a,b in zip(x,y)]
def unit(x):
    r=mp.sqrt(dot(x,x))
    return [t/r for t in x]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def fmt(x):return mp.nstr(x,15)

def case(k,n,tau):
    m=k*k; K=mp.ellipk(m); Kp=mp.ellipk(1-m)
    v=2*K*tau/n; delta=2*v
    sn=lambda u:mp.ellipfun('sn',u,m)
    cn=lambda u:mp.ellipfun('cn',u,m)
    dn=lambda u:mp.ellipfun('dn',u,m)
    A=mp.mpf(1); B=mp.sqrt(1-m); c=k
    a=dn(v)/cn(v); b=B/cn(v)
    P=lambda u:[-a*sn(u),b*cn(u)]
    maxima={s:mp.mpf(0) for s in ['confocal','tangency','reflection','distance','closure','orientation','focal_equality','zero','simple_zero_derivative_min']}
    maxima['simple_zero_derivative_min']=mp.inf
    vals=[]
    for frac in [mp.mpf('0.0'),mp.mpf('0.173'),mp.mpf('0.317'),mp.mpf('0.887')]:
        u=frac*K; p=P(u)
        maxima['confocal']=max(maxima['confocal'],abs(a*a-b*b-c*c))
        for sign in [-1,1]:
            U=u+sign*v;q=[-A*sn(U),B*cn(U)];other=P(u+sign*delta)
            for pt in [p,other]:
                maxima['tangency']=max(maxima['tangency'],abs(-pt[0]*sn(U)/A+pt[1]*cn(U)/B-1))
            # Strictly interior contact and forward tangent chord are physical.
            assert q[0]**2/a**2+q[1]**2/b**2<1
            assert dot(sub(q,p),sub(q,other))<0
        ray1=unit(sub(P(u-delta),p));ray2=unit(sub(P(u+delta),p))
        normal=[p[0]/a**2,p[1]/b**2]
        maxima['reflection']=max(maxima['reflection'],abs(cross([ray1[i]+ray2[i] for i in range(2)],normal)))
        products=[]
        for sign in [1,-1]:
            factors=[]
            for j in range(n):
                q=P(u+j*delta);actual=mp.sqrt((q[0]-sign*c)**2+q[1]**2);factor=a+sign*c*sn(u+j*delta)
                assert factor>0
                maxima['distance']=max(maxima['distance'],abs(actual-factor))
                factors.append(factor/a)
            products.append(mp.fprod(factors))
            reverse=mp.fprod(1+sign*(c/a)*sn(u-j*delta) for j in range(n))
            maxima['orientation']=max(maxima['orientation'],abs(reverse-products[-1]))
        if n%2==0:maxima['focal_equality']=max(maxima['focal_equality'],abs(products[0]-products[1]))
        vals.append(products)
        maxima['closure']=max(maxima['closure'],max(abs(x-y) for x,y in zip(P(u+n*delta),p)))
    pole=1j*Kp
    for sign in [-1,1]:
        q=pole-K+sign*v
        maxima['zero']=max(maxima['zero'],abs(a+c*sn(q)))
        maxima['simple_zero_derivative_min']=min(maxima['simple_zero_derivative_min'],abs(c*cn(q)*dn(q)))
    for name,error in maxima.items():
        if name!='simple_zero_derivative_min':assert error<mp.mpf('1e-75'),(name,error,k,n,tau)
    assert maxima['simple_zero_derivative_min']>0
    spread=max(x[0] for x in vals)-min(x[0] for x in vals)
    if n%4==2:assert spread<mp.mpf('1e-75')
    return {'k':fmt(k),'least_period':n,'tau':tau,'normalized_plus_spread':fmt(spread),'residuals':{s:fmt(v) for s,v in maxima.items()}}

def main():
    rows=[]
    for k in [mp.mpf('0.01'),mp.mpf('0.7'),mp.mpf('0.999999')]:
        for n in range(3,19):
            for tau in range(1,(n+1)//2):
                if math.gcd(n,tau)==1:
                    rows.append(case(k,n,tau))
    assert any(mp.mpf(x['normalized_plus_spread'])>mp.mpf('1e-3') for x in rows if x['least_period']%2)
    assert any(mp.mpf(x['normalized_plus_spread'])>mp.mpf('1e-3') for x in rows if x['least_period']%4==0)
    result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS supplementary unvalidated diagnostics','mpmath':mp.__version__,'decimal_precision':mp.mp.dps,'cases':rows,'limit':'These are observed high-precision residuals, not rigorous numerical bounds. No universal conclusion is inferred from the finite test.'}
    Path(__file__).with_name('independent_geometry_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(rows),'precision':mp.mp.dps},indent=2))

if __name__=='__main__':main()
