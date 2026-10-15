#!/usr/bin/env python3
"""Independent exact alpha=16 algebra/analysis audit.
No submission modules, certificates, or review artifacts are loaded.
Eighth roots use binary integer power comparisons, not iterated isqrt.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

CHECKS=0
def require(ok, label):
    global CHECKS
    if not ok: raise AssertionError(label)
    CHECKS+=1

def box(a,b=None):
    a=Q(a); b=a if b is None else Q(b)
    require(a<=b,'interval order')
    return a,b

def add(a,b): return a[0]+b[0], a[1]+b[1]
def neg(a): return -a[1],-a[0]
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    corners=[x*y for x in a for y in b]
    return min(corners),max(corners)
def scale(a,r): return mul(a,box(r))
def sq(a):
    return (0 if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def div(a,b):
    require(not b[0]<=0<=b[1],'nonzero interval denominator')
    return mul(a,(1/b[1],1/b[0]))
def power_nonnegative(a,n):
    require(a[0]>=0,'nonnegative power input')
    return a[0]**n,a[1]**n

def root8_exact(q,places=36):
    """Return neighboring decimal-grid rationals enclosing positive eighth root."""
    q=Q(q); require(q>=0,'root domain')
    if q==0: return box(0)
    den=10**places
    target=(q.numerator*den**8)//q.denominator
    lo=0;hi=1 << ((target.bit_length()+7)//8)
    require(hi**8>target,'initial integer upper bound')
    while hi-lo>1:
        mid=(hi+lo)//2
        if mid**8<=target: lo=mid
        else: hi=mid
    require(lo**8<=target<hi**8,'integer eighth power enclosure')
    lower,upper=Q(lo,den),Q(hi,den)
    require(lower**8<=q<=upper**8,'rational eighth power enclosure')
    return lower,upper

def root8(a): return root8_exact(a[0])[0],root8_exact(a[1])[1]
def sumsq(p): return add(sq(p[0]),sq(p[1]))
def psub(p,q): return sub(p[0],q[0]),sub(p[1],q[1])
def det(p,q): return sub(mul(p[0],q[1]),mul(p[1],q[0]))
def dist16(p,q): return power_nonnegative(sumsq(psub(p,q)),8)
def separated(p,q): return any(a[1]<b[0] or b[1]<a[0] for a,b in zip(p,q))
def sign(a): return 1 if a[0]>0 else -1 if a[1]<0 else 0

def serial(a):return [str(a[0]),str(a[1])]
def decimal_enclosure(a,places=12):
    den=10**places
    lo=(a[0].numerator*den)//a[0].denominator
    hi=-((-a[1].numerator*den)//a[1].denominator)
    return [str(Q(lo,den)),str(Q(hi,den))]
def entry(a):return {'rational':serial(a),'decimal_grid_enclosure':decimal_enclosure(a)}

b=Q(2073,10000);c=Q(4719,10000);d=Q(64,10000);lam=Q(27,1250)

def outgoing(s):
    u=root8(s);v=root8(add(s,box(lam)));w=root8(add(s,box(1)))
    x=scale(sub(add(box(b*b),u),v),1/(2*b))
    y=scale(sub(sub(add(box(c*c+d*d),u),w),scale(x,2*c)),1/(2*d))
    return (x,y),sub(sumsq((x,y)),u)

signs=[]
for s,lower,upper in [(Q(9,10000),Q(38,100),Q(39,100)),
                       (Q(11,10000),Q(-28,100),Q(-27,100)),
                       (Q(13,10000),Q(51,100),Q(52,100)),
                       (Q(1,2),Q(-91,100),Q(-90,100)),
                       (Q(1),Q(9),Q(10))]:
    _,res=outgoing(box(s))
    require(lower<res[0]<=res[1]<upper,'outgoing coarse strict enclosure')
    signs.append({'s':str(s),'G':entry(res)})

# Independent analytic endpoint: s=10^16 has exact u=100.
# Concavity f(t)=t^(1/8) gives f(s+a)-f(s)<=a/(8s^(7/8)).
x0=b/2;y0=(c*c+d*d-b*c)/(2*d)
dvmax=lam/Q(8*10**14);dwmax=Q(1,8*10**14)
xlast=box(x0-dvmax/(2*b),x0)
ylast=box(y0-dwmax/(2*d),y0+(c/b)*dvmax/(2*d))
glast=sub(sumsq((xlast,ylast)),box(100))
require(glast[1]<Q(-47,10),'analytic negative endpoint margin')
signs.append({'s':str(10**16),'G':entry(glast),'mechanism':'concavity bound; exact u=100'})

# Isolate boundary parameters with exact rational polynomial comparisons.
def t_polynomial(qx,qy,h,level,t):
    n=qx*qx+qy*qy
    return n**8*(((t-1)**2+h*h)**8-(t*t+h*h)**8)-level

def boundary(qx,qy,h,level,base):
    lo=Q(-8);hi=Q(8)
    require(t_polynomial(qx,qy,h,level,lo)>0,'boundary lower sign')
    require(t_polynomial(qx,qy,h,level,hi)<0,'boundary upper sign')
    for _ in range(128):
        middle=(lo+hi)/2
        if t_polynomial(qx,qy,h,level,middle)>0:lo=middle
        else:hi=middle
    require(t_polynomial(qx,qy,h,level,lo)>0,'isolated boundary lower sign')
    require(t_polynomial(qx,qy,h,level,hi)<0,'isolated boundary upper sign')
    t=box(lo,hi)
    p=(add(box(base[0]-h*qy),scale(t,qx)),add(box(base[1]+h*qx),scale(t,qy)))
    return p,{'q':[str(qx),str(qy)],'h':str(h),'level':str(level),'t':serial(t),'point':[entry(a) for a in p]}

A1,t1=boundary(c,d,Q(10),Q(1),(Q(0),Q(0)))
A3,t3=boundary(b,Q(0),Q(1),lam,(Q(0),Q(0)))
A5,t5=boundary(c-b,d,Q(-10),1-lam,(b,Q(0)))
A2=(box(0),box(0));A4=(box(b),box(0));A6=(box(c),box(d))
P=[A1,A2,A3,A4,A5,A6]
for a,z in combinations(P,2):require(separated(a,z),'distinct boundary points')
even=det(psub(A4,A2),psub(A6,A2));odd=det(psub(A3,A1),psub(A5,A1))
require(even==box(Q(2073*64,10**8)),'exact even determinant')
require(Q(637,100)<odd[0]<=odd[1]<Q(639,100),'odd determinant range')
for a,z,r in combinations(P,3):require(sign(det(psub(z,a),psub(r,a)))!=0,'noncollinear boundary triple')

# All common-focus centers have x<b/2 by positive lambda.
require(A1[0][0]>b/2 and A5[0][0]>b/2,'odd boundary focus-side exclusions')
not_A3=sub(sub(dist16(A3,A6),dist16(A3,A2)),box(1))
require(Q(98,100)<not_A3[0]<=not_A3[1]<Q(99,100),'A3 exclusion margin')
require(b**16!=lam,'A2 exclusion')
require(lam>0 and 1>0,'A4 A6 exclusions')

# Direct incoming certificate, algebraic boundary data as rigorously enclosed constants.
L=sub(dist16(A4,A5),dist16(A4,A3))
M=sub(dist16(A2,A1),dist16(A2,A3))
require(L[0]>0 and M[0]>0,'positive incoming levels')
B=psub(A5,A3);C=psub(A1,A3);D=det(B,C)
require(sign(D)!=0,'invertible incoming linear map')

def incoming(s):
    u=root8(s);v=root8(add(s,L));w=root8(add(s,M))
    r1=sub(add(sumsq(B),u),v);r2=sub(add(sumsq(C),u),w)
    x=div(sub(mul(r1,C[1]),mul(r2,B[1])),scale(D,2))
    y=div(sub(mul(B[0],r2),mul(C[0],r1)),scale(D,2))
    return (add(A3[0],x),add(A3[1],y)),sub(sumsq((x,y)),u)

incoming_checks=[]
for s,lower,upper in [(Q(1,100),Q(37,100000),Q(38,100000)),
                       (Q(11,1000),Q(-81,100000),Q(-80,100000))]:
    _,res=incoming(box(s))
    require(lower<res[0]<=res[1]<upper,'incoming strict coarse margin')
    incoming_checks.append({'s':str(s),'H':entry(res)})
Z,_=incoming(box(Q(1,100),Q(11,1000)))
for a in P:require(separated(Z,a),'incoming distinct from boundary')
for a,z in combinations(P,2):require(sign(det(psub(Z,a),psub(z,a)))!=0,'incoming no boundary-pair collinearity')

# Root enclosures for explicit outgoing center separation and nondegeneracy.
cut=[Q(9,10000),Q(11,10000),Q(13,10000),Q(1,2),Q(1),Q(10**16)]
roots=[]
for index,(lo,hi) in enumerate(zip(cut[:-1],cut[1:])):
    leftsign=1 if index%2==0 else -1
    for _ in range(100):
        mid=(lo+hi)/2;sg=sign(outgoing(box(mid))[1])
        require(sg!=0,'strict midpoint sign')
        if sg==leftsign:lo=mid
        else:hi=mid
    require(sign(outgoing(box(lo))[1])==leftsign,'refined lower sign')
    require(sign(outgoing(box(hi))[1])==-leftsign,'refined upper sign')
    X,_=outgoing(box(lo,hi))
    for a in P:require(separated(X,a),'outgoing distinct from boundary')
    for a,z in combinations(P,2):require(sign(det(psub(X,a),psub(z,a)))!=0,'outgoing no boundary-pair collinearity')
    roots.append({'s':serial(box(lo,hi)),'X':[entry(a) for a in X]})

out={'status':'independently verified at least five alpha16 outgoing centers plus incoming center',
     'arithmetic':'fractions; integer binary-power eighth roots; exact rational interval operations',
     'precision_decimal_places':36,'boundary_bisections':128,'checks':CHECKS,
     'outgoing_endpoint_signs':signs,'independent_analytic_endpoint':{'circumcenter':[str(x0),str(y0)],'norm2':str(x0*x0+y0*y0),'delta_v_upper':str(dvmax),'delta_w_upper':str(dwmax)},
     'boundary':[t1,t3,t5],'odd_determinant':entry(odd),'even_determinant':entry(even),
     'A3_exclusion':entry(not_A3),'incoming_levels':[entry(L),entry(M)],
     'incoming_endpoints':incoming_checks,'incoming_whole_interval_box':[entry(a) for a in Z],
     'outgoing_root_boxes':roots}
path=Path(__file__).with_name('independent_certificate.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('Exact checks:',CHECKS)
print('G endpoint enclosures:',[(a['s'],a['G']['decimal_grid_enclosure']) for a in signs])
print('H endpoint enclosures:',[(a['s'],a['H']['decimal_grid_enclosure']) for a in incoming_checks])
print('Odd determinant:',decimal_enclosure(odd))
print('Boundary parameter boxes:',[decimal_enclosure(tuple(map(Q,x['t']))) for x in (t1,t3,t5)])
print('Incoming Z:',[decimal_enclosure(a) for a in Z])
print('Outgoing X:',[[a['decimal_grid_enclosure'] for a in root['X']] for root in roots])
