#!/usr/bin/env python3
"""Independent bounded PR205 diagnostics; finite noninterval evidence only.

Run with Python 3.10+ and mpmath==1.3.0 installed, or add
--runtime /path/to/external/site-packages. No package-specific/private import.
The construction intersects caustic tangent lines; it never calls verify.py.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--runtime', type=Path)
args = p.parse_args()
if args.runtime:
    sys.path.insert(0, str(args.runtime.resolve()))
import mpmath as mp
if mp.__version__ != '1.3.0':
    raise RuntimeError('mpmath 1.3.0 required')
mp.mp.dps = 100
tol = mp.mpf('1e-75')
worst = {}
checks = 0

def valid(x):
    x = mp.mpf(x)
    if not mp.isfinite(x):
        raise RuntimeError('nonfinite diagnostic')
    return x

def check(label, x, y=0, scale=1):
    global checks
    e = valid(abs(valid(x)-valid(y))/max(valid(scale), 1))
    worst[label] = max(worst.get(label, 0), e)
    checks += 1
    if e >= tol:
        raise RuntimeError(label+': '+str(e))

def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def norm(x): return mp.sqrt(dot(x,x))
def unit(x):
    r=norm(x)
    if not r>0: raise RuntimeError('zero vector')
    return (x[0]/r,x[1]/r)
def intersect(n,r):
    d=cross(n,r)
    if d==0: raise RuntimeError('parallel tangent lines')
    return ((r[1]-n[1])/d,(n[0]-r[0])/d)

rows=[]
specs=[('1e-12',3,1),('.3',5,2),('.73',9,1),('.73',9,2),('.73',9,4),
       ('.999999',15,1),('.999999',15,2),('.999999',15,4),('.999999',15,7),
       ('.98',21,8),('.2',25,1),('.2',25,12)]
for mtext,N,w in specs:
    if math.gcd(N,w)!=1 or N%2!=1: raise RuntimeError('bad test specification')
    m=mp.mpf(mtext); k=mp.sqrt(m); kp=mp.sqrt(1-m)
    alpha=mp.mpf('2.7');beta=alpha*kp;c=alpha*k;K=mp.ellipk(m)
    f=lambda name,t: mp.ellipfun(name,t,m)
    h=2*K*w/N
    a=alpha*f('dn',h)/f('cn',h);b=beta/f('cn',h)
    check('confocal',a*a-b*b,c*c,a*a)
    q=mp.exp(-mp.pi*mp.ellipk(1-m)/K);Q=q**N
    M=(mp.jtheta(2,0,Q)/mp.jtheta(3,0,Q))**4
    KM=mp.ellipk(M);gamma=K/(N*KM)
    if not 0<M<1 or not gamma>0:raise RuntimeError('invalid transformed parameter')
    check('transformed_nome',mp.exp(-mp.pi*mp.ellipk(1-M)/KM),Q)
    ref=alpha**2*(1-M)/gamma**2
    reciprocal=beta**2*mp.fsum(1/f('dn',4*K*j/N) for j in range(N))**2
    check('normalization',ref,reciprocal,ref)
    check('gamma',gamma,1/mp.fsum(f('dn',2*K*j/N) for j in range(N)))
    values=[];segment_values=[]
    for phase in [mp.mpf('.017')*K,mp.mpf('.431')*K,mp.mpf('1.173')*K]:
        grid=[phase+4*K*j/N for j in range(N)]
        D=mp.fsum(f('dn',z) for z in grid);H=mp.fsum(f('cn',z) for z in grid)
        check('dn_trace',D,mp.ellipfun('dn',phase/gamma,M)/gamma,N)
        check('cn_trace',H,mp.sqrt(M/m)*mp.ellipfun('cn',phase/gamma,M)/gamma,N)
        check('lorentz',D*D-m*H*H,(1-M)/gamma**2,N*N)
        for direction in [1,-1]:
            # Independent contact-line construction: consecutive line intersection.
            contacts=[phase+direction*2*h*i for i in range(N)]
            normals=[(-f('sn',v)/alpha,f('cn',v)/beta) for v in contacts]
            vertices=[intersect(normals[i-1],normals[i]) for i in range(N)]
            plus=[];minus=[];sp=[];sm=[]
            for i,P in enumerate(vertices):
                R=vertices[(i+1)%N];before=vertices[i-1]
                check('outer_boundary',P[0]**2/a**2+P[1]**2/b**2,1)
                v=unit(sub(R,P));normal=unit((P[0]/a**2,P[1]/b**2))
                incoming=unit(sub(P,before));reflected=tuple(incoming[j]-2*dot(incoming,normal)*normal[j] for j in [0,1])
                check('reflection',norm(sub(reflected,v)))
                nn=(-v[1],v[0]);support=dot(nn,P)
                check('caustic_tangent',support**2,alpha**2*nn[0]**2+beta**2*nn[1]**2,alpha**2)
                ds=[];segments=[]
                for F in [(c,0),(-c,0)]:
                    ds.append(abs(cross(v,sub(F,P))))
                    t=dot(sub(F,P),sub(R,P))/dot(sub(R,P),sub(R,P))
                    clipped=max(0,min(1,t));foot=tuple(P[j]+clipped*(R[j]-P[j]) for j in [0,1])
                    segments.append(norm(sub(F,foot)))
                check('focal_pointwise',ds[0]*ds[1],beta**2,beta**2)
                plus.append(ds[0]);minus.append(ds[1]);sp.append(segments[0]);sm.append(segments[1])
                for j in range(i):
                    if norm(sub(P,vertices[j]))/a<mp.mpf('1e-30'): raise RuntimeError('nonprimitive test orbit')
            I=mp.fsum(plus)*mp.fsum(minus);values.append(I)
            segment_values.append(mp.fsum(sp)*mp.fsum(sm))
            check('physical_value',I,ref,ref)
    rows.append({'m':mtext,'N':N,'winding':w,'physical_traversals':6,
                 'value':mp.nstr(ref,35),'relative_phase_spread':mp.nstr((max(values)-min(values))/ref,8),
                 'max_segment_relative_difference':mp.nstr(max(abs(x-ref)/ref for x in segment_values),12)})

# Exact algebraic N4 is proved separately in the report; here directly measure
# its two lists and verify tangency/reflection/boundary without Jacobi input.
a=mp.sqrt(mp.mpf(3)/2);b=mp.sqrt(3)/2;c=b;alpha=mp.mpf(1);beta=mp.mpf('.5')
four=[]
for expected,P in [(8,[(0,b),(-a,0),(0,-b),(a,0)]),(9,[(1,beta),(-1,beta),(-1,-beta),(1,-beta)])]:
    sums=[[],[]]
    for i,x in enumerate(P):
        y=P[(i+1)%4];v=unit(sub(y,x));incoming=unit(sub(x,P[i-1]));n=unit((x[0]/a**2,x[1]/b**2))
        check('N4_boundary',x[0]**2/a**2+x[1]**2/b**2,1)
        check('N4_reflection',norm(sub(tuple(incoming[j]-2*dot(incoming,n)*n[j] for j in [0,1]),v)))
        nn=(-v[1],v[0]);check('N4_tangent',dot(nn,x)**2,nn[0]**2+beta**2*nn[1]**2)
        for z,F in enumerate([(c,0),(-c,0)]):sums[z].append(abs(cross(v,sub(F,x))))
    I=mp.fsum(sums[0])*mp.fsum(sums[1]);check('N4_value',I,expected);four.append(mp.nstr(I,30))

print(json.dumps({'status':'PASS','scope':'finite noninterval independent diagnostics; universal proof is separate',
 'python':sys.version.split()[0],'mpmath':mp.__version__,'working_digits':mp.mp.dps,'tolerance':str(tol),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'checks':checks,'physical_traversals':len(rows)*6,'configurations':rows,
 'worst_scaled_residuals':{k:mp.nstr(v,12) for k,v in worst.items()},'N4_values':four},indent=2,allow_nan=False))
