#!/usr/bin/env python3
"""Separate review controls; imports no author code. Prints reproducible JSON.
Exact controls are algebra tests, not a proof of billiard dynamics or root existence.
Actual Jacobi billiards and area limits are explicitly numerical diagnostics.
Dependencies: Python standard library, installed SymPy and mpmath.
"""
from fractions import Fraction as F
from math import gcd
import json
import sympy as S
import mpmath as mp
count=0
def check(v):
    global count
    assert v
    count+=1
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def wedge(a,b): return a[0]*b[1]-a[1]*b[0]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def meet(l,m):
    h=cross(l,m); check(h[2]!=0); return (h[0]/h[2],h[1]/h[2])
def totals(q):
    n=len(q); z=[wedge(q[i],q[(i+1)%n]) for i in range(n)]
    return sum(z)/2,tuple(sum(z[i]*(q[i][j]+q[(i+1)%n][j]) for i in range(n)) for j in range(2))
def check_center(q):
    area,mom=totals(q)
    check(tuple(map(sum,zip(*q)))==(0,0));check(mom==(0,0))
    if area: check(tuple(x/(6*area) for x in mom)==(0,0))
    c=(F(7,3),F(-4,5));translated=[(x+c[0],y+c[1]) for x,y in q]
    area2,mom2=totals(translated);check(area2==area);check(mom2==tuple(6*area*x for x in c))
    return area
cases=0;negative=0
for half in range(2,13):
    first=[]
    for j in range(half):
        t=F(2*j-half+1,2*half+3)
        x,y=(1-t*t)/(1+t*t),2*t/(1+t*t)
        first.append(((3*x-4*y)/5,(4*x+3*y)/5))
    points=first+[(-x,-y) for x,y in first];n=2*half
    for tau in range(1,half):
        if gcd(tau,n)>1:continue
        check(tau%2==1);check(tau*half%n==half)
        for a,b in [(F(5,2),F(3,2)),(F(7),F(1)),(F(1),F(1)),(F(20),F(1,3))]:
            p=[(a*points[(i*tau)%n][0],b*points[(i*tau)%n][1]) for i in range(n)]
            tangent=[(x/a**2,y/b**2,F(-1)) for x,y in p]
            r=[meet(tangent[i],tangent[(i+1)%n]) for i in range(n)]
            lines=[(x,y,-x*x-y*y) for x,y in r]
            q=[meet(lines[i],lines[(i+1)%n]) for i in range(n)]
            for i in range(n):
                check(wedge(p[i],p[(i+1)%n])>0)
                check(wedge(r[i],r[(i+1)%n])>0)
                check(q[(i+half)%n]==tuple(-v for v in q[i]))
                check(dot(lines[i],(*q[i],F(1)))==0)
                check(dot(lines[(i+1)%n],(*q[i],F(1)))==0)
            area=check_center(q);negative+=int(area<0)
            check(totals(list(reversed(q)))[0]==-area)
            check_center(list(reversed(q)));check_center(q+q+q)
            cases+=1
zero=[tuple(map(F,q)) for q in [(1,0),(0,1),(2,1),(-1,0),(0,-1),(-2,-1)]]
check(check_center(zero)==0)  # Moment zero does not license division by zero.
# Symbolic independent Fourier calculation, in eccentric rather than polar angle.
a,b=S.symbols('a b',positive=True);c,s=S.symbols('c s',real=True);d=a*a-b*b
qx=a*c+d*c*s*s/a;qy=b*s-d*s*c*c/b
# Reduce identities modulo c²+s²=1 by eliminating c².
reduce=lambda x:S.factor(S.rem(S.Poly(S.together(x).as_numer_denom()[0],c),S.Poly(c*c+s*s-1,c)).as_expr())
check(reduce(a*c*qx+b*s*qy-(a*a*c*c+b*b*s*s))==0)
check(reduce(-a*s*qx+b*c*qy-2*(b*b-a*a)*s*c)==0)
a1=a+d/(4*a);a3=-d/(4*a);b1=b-d/(4*b);b3=-d/(4*b)
check(reduce(qx-a1*c-a3*(4*c**3-3*c))==0)
check(reduce(qy-b1*s-b3*(3*s-4*s**3))==0)
area_over_pi=S.factor(a1*b1+3*a3*b3)
check(S.factor(area_over_pi-(a*b-d*d/(8*a*b)))==0)
check(area_over_pi.subs({a:1,b:S.Rational(1,4)})==-S.Rational(97,512))
check(area_over_pi.subs({a:1,b:1})==1)
exact=count
# Independently constructed direct geometry diagnostics.
mp.mp.dps=65;num=0;maxerr=mp.mpf(0)
def near(x,scale=1):
    global num,maxerr
    err=abs(x)/(1+abs(scale));assert err<mp.mpf('1e-48');num+=1;maxerr=max(maxerr,err)
def billiard(n,tau,k,phase):
    m=k*k;K=mp.ellipk(m);v=2*K*tau/n
    sn=lambda u:mp.ellipfun('sn',u,m)
    cn=lambda u:mp.ellipfun('cn',u,m)
    dn=lambda u:mp.ellipfun('dn',u,m)
    a=dn(v)/cn(v);b=mp.sqrt(1-m)/cn(v)
    p=[(-a*sn(K*phase+2*i*v),b*cn(K*phase+2*i*v)) for i in range(n)]
    r=[]
    for i in range(n):
        x,y=p[i];z,w=p[(i+1)%n];den=1+x*z/a**2+y*w/b**2
        r.append(((x+z)/den,(y+w)/den))
    q=[]
    for i in range(n):
        x,y=r[i];z,w=r[(i+1)%n];den=x*w-y*z;assert den>0
        s=((z*z+w*w)-(z*x+w*y))/den
        q.append((x-s*y,y+s*x))
    scale=max(1,max(abs(x)+abs(y) for x,y in q));area,mom=totals(q)
    for i in range(n):
        near(q[i][0]+q[(i+n//2)%n][0],scale);near(q[i][1]+q[(i+n//2)%n][1],scale)
        # Verify both anti-pedal lines and both original ellipse tangencies.
        for j in (i,(i+1)%n):
            near(dot(r[j],q[i])-dot(r[j],r[j]),scale**2)
        x,y=r[i]
        for j in (i,(i+1)%n):near(x*p[j][0]/a**2+y*p[j][1]/b**2-1,scale)
        # Exact caustic chord discriminant relation, evaluated numerically.
        dx=p[(i+1)%n][0]-p[i][0];dy=p[(i+1)%n][1]-p[i][1]
        h=-dy*p[i][0]+dx*p[i][1]
        near(h*h-dy*dy-(1-m)*dx*dx,h*h)
    near(mom[0],n*scale**3);near(mom[1],n*scale**3)
    return area
families=0
for n,tau in [(4,1),(6,1),(8,1),(8,3),(10,3),(12,5),(14,3),(16,7),(22,9),(26,11),(30,7)]:
    for k in map(mp.mpf,['0','0.4','0.85','0.97']):
        for phase in map(mp.mpf,['0.231','1.149']):
            billiard(n,tau,k,phase);families+=1
limit=-97*mp.pi/512;sequence=[]
for n in [32,64,128,256,512]:
    area=billiard(n,1,mp.sqrt(15)/4,mp.mpf('0.231'))
    sequence.append({'N':n,'area':mp.nstr(area,22),'error_from_limit':mp.nstr(area-limit,12)})
assert mp.mpf(sequence[-1]['area'])<0
# Circle area is positive also for primitive stars; no floating root certificate.
for n,tau in [(4,1),(10,3),(16,7),(30,7)]:
    got=billiard(n,tau,mp.mpf(0),mp.mpf('0.231'))
    v=mp.pi*tau/n;want=n*mp.sin(2*v)/(2*mp.cos(v)**6)
    near(got-want,want);assert got>0
print(json.dumps({'status':'PASS','exact_assertions':exact,'exact_rational_ellipse_polygon_cases':cases,'negative_area_exact_nonbilliard_cases':negative,'zero_area_general_symmetry_control':True,'independent_envelope_area_over_pi':str(area_over_pi),'actual_billiard_families':families,'additional_limit_and_circle_cases':9,'numerical_diagnostic_assertions':num,'decimal_precision':65,'relative_threshold':'1e-48','maximum_relative_residual':mp.nstr(maxerr,8),'limit_diagnostics_not_proof':sequence,'scope':'Exact finite algebra controls, symbolic Fourier identity, and separate numerical diagnostics. Analytic universal and zero-area existence claims are audited in FINAL_REVIEW.md; no numerical zero is certified.'},sort_keys=True,indent=2))
