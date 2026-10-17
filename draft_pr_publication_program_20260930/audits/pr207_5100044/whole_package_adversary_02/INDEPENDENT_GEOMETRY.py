#!/usr/bin/env python3
"""Reviewer 02: Poncelet tangent-neighbor propagation and complex diagnostics.
No package code/results imported. Finite samples, not interval or universal proof.
"""
import math,json,hashlib
from pathlib import Path
import mpmath as mp
mp.mp.dps=100
TOL=mp.mpf('1e-70')
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def unit(p):
    h=mp.sqrt(dot(p,p));return (p[0]/h,p[1]/h)
def dist(p,q): return mp.sqrt(dot(sub(p,q),sub(p,q)))
def area(ps):return mp.fsum(cross(ps[i],ps[(i+1)%len(ps)]) for i in range(len(ps)))/2
def inverse(ps,f):
    out=[]
    for p in ps:
        z=(p[0]-f,p[1]);d=dot(z,z)
        if not d>0:raise RuntimeError('invalid inverse denominator')
        out.append((z[0]/d,z[1]/d))
    return out
def small(v,label):
    if not mp.isfinite(v) or abs(v)>TOL:raise RuntimeError(label+': '+mp.nstr(v,12))
    return abs(v)

def next_circle(z,ax,by):
    # caustic is diag(ax,by) times unit circle, outer boundary is unit circle.
    L=(z[0]/ax,z[1]/by);L2=dot(L,L)
    if not L2>1: raise RuntimeError('not exterior to nested caustic')
    h=mp.sqrt(L2-1)
    candidates=[]
    for sign in [-1,1]:
        u=((L[0]-sign*h*L[1])/L2,(L[1]+sign*h*L[0])/L2)
        contact=(ax*u[0],by*u[1]);d=sub(contact,z)
        lam=-2*dot(z,d)/dot(d,d)
        q=(z[0]+lam*d[0],z[1]+lam*d[1])
        if cross(z,q)>0:candidates.append((q,contact,lam))
    if len(candidates)!=1:raise RuntimeError('orientation ambiguous')
    return candidates[0]

families=[]
for N in [4,8,12,16,20,28]:
 for tau in range(1,N//2):
  if math.gcd(N,tau)!=1:continue
  for k in [mp.mpf('0.37'),mp.mpf('0.91')]:
   kp=mp.sqrt(1-k*k);K=mp.ellipk(k*k);v=2*K*tau/N
   cv=mp.ellipfun('cn',v,k*k);dv=mp.ellipfun('dn',v,k*k)
   a,b=dv/cv,kp/cv
   values=[];maxres=mp.mpf(0)
   for phase in [mp.mpf('0.029'),mp.mpf('0.271'),mp.mpf('0.819')]:
    start=(mp.cos(phase*mp.pi),mp.sin(phase*mp.pi));z=start;ps=[];turn=mp.mpf(0);early=mp.inf
    for j in range(N):
     ps.append((a*z[0],b*z[1]));q,contact,lam=next_circle(z,1/a,kp/b)
     maxres=max(maxres,small(dot(q,q)-1,'circle'),small(contact[0]**2*a*a+contact[1]**2*b*b/(kp*kp)-1,'contact'))
     turn+=mp.atan2(cross(z,q),dot(z,q))
     if j+1<N:early=min(early,dist(q,start))
     if not lam>1:raise RuntimeError('contact not internal')
     z=q
    maxres=max(maxres,small(dist(z,start),'closure'),small(turn/(2*mp.pi)-tau,'winding'))
    if not early>mp.mpf('1e-20'):raise RuntimeError('earlier return')
    for j,p in enumerate(ps):
     vi=unit(sub(p,ps[j-1]));vo=unit(sub(ps[(j+1)%N],p));ne=(p[0]/(a*a),p[1]/(b*b))
     ref=(vi[0]-2*dot(vi,ne)/dot(ne,ne)*ne[0],vi[1]-2*dot(vi,ne)/dot(ne,ne)*ne[1])
     maxres=max(maxres,small(dist(ref,vo),'reflection'))
    A=area(ps);I=area(inverse(ps,k));Im=area(inverse(ps,-k));val=A*I
    if not A>0 or not I>0:raise RuntimeError('area sign')
    maxres=max(maxres,small(I-Im,'focus'))
    if N==4: maxres=max(maxres,small(val-4,'N4'))
    # Compute classical half-grid constant directly in theta variables.
    h=mp.ellipfun('sn',v,k*k);t=h*h;q=cv*cv
    U=1-2*k*k*t+k*k*t*t;W=1-k*k*t*t
    Lam=U*(k**4*(t**3+t*t)-5*k*k*t+k*k+2)/(2*kp**4*W**3)
    CA=a*b*h*cv/dv;C0=b*h*dv*cv**4
    nome=mp.exp(-mp.pi*mp.ellipk(kp*kp)/K)**(N//2)
    expected=4*CA*C0*Lam/kp*(N//2*mp.pi/(2*K))**2*mp.jtheta(3,0,nome)**2*mp.jtheta(4,0,nome)**2
    maxres=max(maxres,small(val-expected,'explicit_constant'))
    values.append(val)
   maxres=max(maxres,small(max(values)-min(values),'family spread'))
   families.append({'N':N,'tau':tau,'k':str(k),'phase_count':3,'maximum_absolute_residual':mp.nstr(maxres,12),'product':mp.nstr(values[0],24)})

# Direct samples of complex identities used by retained torus proof.
complex_checks=[]
for N,tau in [(4,1),(8,1),(8,3),(12,5),(20,3)]:
 k=mp.mpf('0.73');m=N//2;K=mp.ellipk(k*k);Kp=mp.ellipk(1-k*k);kp=mp.sqrt(1-k*k);delta=4*K*tau/N;v=delta/2
 sn=lambda z:mp.ellipfun('sn',z,k*k)
 cn=lambda z:mp.ellipfun('cn',z,k*k)
 dn=lambda z:mp.ellipfun('dn',z,k*k)
 h=sn(v);t=h*h;U=1-2*k*k*t+k*k*t*t;V=1-2*t+k*k*t*t;ell=2*K/m;r=K+1j*Kp
 def B(z):
  x=sn(z)**2
  return 2*(1-k*k*t*x)*(U*U+k*k*V*(V+2*U)*x)/(dn(z)*(U*U-k*k*V*V*x)**2)
 def R(z):return mp.fsum(B(z+j*delta) for j in range(m))
 def S(z):return mp.fsum(dn(z+j*delta) for j in range(m))
 worst=mp.mpf(0)
 for u in [K*mp.mpf('0.17')+1j*Kp*mp.mpf('0.23'),K*mp.mpf('0.77')+1j*Kp*mp.mpf('0.41')]:
  for val,label in [(sn(2*r-u)-sn(u),'sn reflection'),(dn(2*r-u)+dn(u),'dn reflection'),(B(2*r-u)+B(u),'paired oddness'),(R(u+ell)-R(u),'reduced period'),(R(u+2j*Kp)+R(u),'anti-period'),(S(u)*S(u+ell/2)-S(0)*S(ell/2),'complex half-grid product')]:
   worst=max(worst,small(val,label))
 complex_checks.append({'N':N,'tau':tau,'maximum_absolute_residual':mp.nstr(worst,12)})
result={'schema':'pr207-reviewer02-independent-geometry-v1','status':'PASS','mpmath':mp.__version__,'precision_dps':mp.mp.dps,'tolerance':str(TOL),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'target_family_count':len(families),'target_phase_count':3*len(families),'families':families,'complex_identity_samples':complex_checks,'scope':'Finite tangent-neighbor and complex-function samples only. Geometry is propagated by tangency at every step and checked against Euclidean reflection. No package program, stored PASS oracle, interval bounds or universal certification.'}
print(json.dumps(result,indent=2,allow_nan=False))
