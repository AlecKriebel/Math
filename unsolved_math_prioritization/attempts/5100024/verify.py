#!/usr/bin/env python3
"""Author finite controls. Exact identities and separately labeled diagnostics.
Does not prove billiard parametrization or certify a numerical zero-area root.
Uses only Python standard library and installed SymPy/mpmath.
"""
from fractions import Fraction as F
from math import gcd
import json
import sympy as s
import mpmath as mp
checks = 0
def ck(x):
    global checks
    assert x
    checks += 1
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def neg(x): return (-x[0],-x[1])
def solve(n,h,m,j):
    d=det(n,m)
    return ((h*m[1]-n[1]*j)/d,(n[0]*j-h*m[0])/d)
def derived(P,a,b):
    n=len(P); normals=[(x/a**2,y/b**2) for x,y in P]
    R=[solve(normals[i],1,normals[(i+1)%n],1) for i in range(n)]
    Q=[solve(R[i],dot(R[i],R[i]),R[(i+1)%n],dot(R[(i+1)%n],R[(i+1)%n])) for i in range(n)]
    D=[det(Q[i],Q[(i+1)%n]) for i in range(n)]
    area=sum(D)/2
    moment=tuple(sum(D[i]*(Q[i][j]+Q[(i+1)%n][j]) for i in range(n)) for j in range(2))
    return R,Q,area,moment
rotations=0
for N in range(4,202,2):
    for tau in range(1,N//2):
        if gcd(N,tau)!=1: continue
        rotations+=1
        ck(tau%2==1)
        ck((N//2*tau)%N==N//2)
        ck(len({i*tau%N for i in range(N)})==N)
        ck(2*tau<N)
exact_cases=0
for m in range(2,15):
    H=[]
    for j in range(m):
        t=F(j,m-j)
        H.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
    # t=j/(m-j) does not cover the entire semicircle as j -> m-1
    # but the endpoint gap to the antipode stays < pi; append antipodes.
    C=H+[neg(x) for x in H]
    for tau in range(1,m):
        if gcd(2*m,tau)!=1: continue
        for a,b in [(F(2),F(1)),(F(4),F(1)),(F(7,3),F(5,4))]:
            P=[(a*C[i*tau%(2*m)][0],b*C[i*tau%(2*m)][1]) for i in range(2*m)]
            R,Q,area,moment=derived(P,a,b)
            for i in range(2*m):
                ck(P[(i+m)%(2*m)]==neg(P[i]))
                ck(R[(i+m)%(2*m)]==neg(R[i]))
                ck(Q[(i+m)%(2*m)]==neg(Q[i]))
                ck(det(R[i],R[(i+1)%(2*m)])>0)
                ck(dot(R[i],Q[i])==dot(R[i],R[i]))
                ck(dot(R[(i+1)%(2*m)],Q[i])==dot(R[(i+1)%(2*m)],R[(i+1)%(2*m)]))
            ck(sum(x for x,y in Q)==0)
            ck(sum(y for x,y in Q)==0)
            ck(moment==(0,0))
            if area: ck(tuple(z/(6*area) for z in moment)==(0,0))
            exact_cases+=1
t=s.symbols('t',positive=True)
ck(s.integrate(t*t/(1+t*t)**3,(t,0,s.oo))==s.pi/16)
A,B=s.symbols('A B',positive=True)
expr=s.pi*A*B-s.pi*(A*A-B*B)**2/(8*A*B)
ck(expr.subs({A:1,B:1})==s.pi)
ck(expr.subs({A:4,B:1})==-97*s.pi/32)
ck(s.simplify(expr.subs({A:1,B:s.Rational(1,4)}))==-97*s.pi/512)
exact_checks=checks
# Actual confocal billiards: numerical diagnostics, not proof certificates.
mp.mp.dps=80
num_checks=0
max_relative=mp.mpf(0)
num_cases=0
def near(x,scale=1):
    global num_checks,max_relative
    r=abs(x)/(1+abs(scale));max_relative=max(max_relative,r)
    assert r<mp.mpf('1e-60')
    num_checks+=1
def billiard(k,N,tau,phase):
    K=mp.ellipk(k*k);v=2*K*tau/N;step=2*v
    sn=lambda u:mp.ellipfun('sn',u,k*k)
    cn=lambda u:mp.ellipfun('cn',u,k*k)
    dn=lambda u:mp.ellipfun('dn',u,k*k)
    a=dn(v)/cn(v);b=mp.sqrt(1-k*k)/cn(v)
    P=[(-a*sn(phase*K+j*step),b*cn(phase*K+j*step)) for j in range(N)]
    R,Q,area,moment=derived(P,a,b)
    scale=max(1,max(abs(x)+abs(y) for x,y in Q))
    for i in range(N):
        near(P[i][0]**2/a**2+P[i][1]**2/b**2-1)
        # Unit velocity reflection: incoming-outgoing difference is normal.
        prev=P[(i-1)%N];cur=P[i];nxt=P[(i+1)%N]
        v1=(cur[0]-prev[0],cur[1]-prev[1]);v2=(nxt[0]-cur[0],nxt[1]-cur[1])
        l1=mp.sqrt(dot(v1,v1));l2=mp.sqrt(dot(v2,v2))
        diff=(v1[0]/l1-v2[0]/l2,v1[1]/l1-v2[1]/l2)
        normal=(cur[0]/a**2,cur[1]/b**2)
        near(det(diff,normal),mp.sqrt(dot(normal,normal)))
        # A chord nx x+ny y=h is tangent to caustic axes 1,sqrt(1-k²).
        chord=(-v2[1],v2[0]);h=dot(chord,cur)
        near(h*h-chord[0]**2-(1-k*k)*chord[1]**2,h*h)
        near(Q[i][0]+Q[(i+N//2)%N][0],scale)
        near(Q[i][1]+Q[(i+N//2)%N][1],scale)
    near(sum(x for x,y in Q),N*scale)
    near(sum(y for x,y in Q),N*scale)
    near(moment[0],N*scale**3);near(moment[1],N*scale**3)
    return area/(a*b)
for N in range(4,22,2):
    for tau in range(1,N//2):
        if gcd(N,tau)!=1:continue
        for k in map(mp.mpf,['0.2','0.7','0.98']):
            for ph in map(mp.mpf,['0.123','0.571']):
                billiard(k,N,tau,ph);num_cases+=1
sign_diagnostics=[]
for k in map(mp.mpf,['0.95','0.99']):
    val=billiard(k,14,1,mp.mpf('0.123'))
    sign_diagnostics.append({'N':14,'tau':1,'k':str(k),'phase_over_K':'0.123','area_over_ab':mp.nstr(val,25)})
# Opposite signs are diagnostics only; the written proof uses a continuum limit.
assert mp.mpf(sign_diagnostics[0]['area_over_ab'])>0
assert mp.mpf(sign_diagnostics[1]['area_over_ab'])<0
print(json.dumps({'status':'PASS','exact_assertions':exact_checks,'primitive_even_rotations':rotations,'rational_polygon_cases':exact_cases,'actual_billiard_diagnostic_cases':num_cases+2,'numerical_diagnostic_assertions':num_checks,'decimal_precision':80,'relative_residual_threshold':'1e-60','maximum_relative_residual':mp.nstr(max_relative,8),'area_sign_diagnostics_not_certificates':sign_diagnostics,'scope':'Finite exact algebra controls and independent high-precision geometric diagnostics; universal claims rely on PROOF.md, not sampling.'},indent=2,sort_keys=True))
