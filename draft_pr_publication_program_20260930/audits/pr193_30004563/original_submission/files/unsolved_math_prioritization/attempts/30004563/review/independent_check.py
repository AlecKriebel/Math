#!/usr/bin/env python3
"""Independent exact certificate for the alpha=16 five-center example.

Tuple intervals and binary integer eighth-root search, separate from the author's
class implementation and triple-isqrt roots. Inputs are rational constants in the
statement, not the author's computed signs. All validity decisions are exact.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json

COUNT = 0
ROOTS = 0
SCALE = 1 << 256

def check(test, label):
    global COUNT
    COUNT += 1
    if not test:
        raise AssertionError(label)

def interval(a, b=None):
    a = F(a)
    b = a if b is None else F(b)
    if a > b:
        raise ValueError('Reversed interval')
    return (a,b)

def add(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[1],-a[0])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    values = [x*y for x in a for y in b]
    return (min(values),max(values))
def inv(a):
    check(a[1]<0 or a[0]>0,'division interval excludes zero')
    return (1/a[1],1/a[0])
def div(a,b): return mul(a,inv(b))
def sq(a):
    return (F(0) if a[0]<=0<=a[1] else min(x*x for x in a), max(x*x for x in a))
def positive_power(a,n):
    check(a[0]>=0 and n>0,'positive power domain')
    return (a[0]**n,a[1]**n)
def scalar(a):return interval(a)
def sign(a): return 1 if a[0]>0 else -1 if a[1]<0 else 0

def root_bound(q):
    """Binary search the integer floor of SCALE times the positive eighth root."""
    global ROOTS
    q=F(q)
    check(q>=0,'eighth root domain')
    ROOTS+=1
    if q==0:return interval(0)
    target=(q.numerator*(SCALE**8))//q.denominator
    left=0
    right=1<<((target.bit_length()+7)//8)
    # right**8 > target: follows from bit_length and rounding up.
    check(left**8<=target<right**8,'binary root initial bracket')
    while right-left>1:
        mid=(left+right)//2
        if mid**8<=target:left=mid
        else:right=mid
    lower,upper=F(left,SCALE),F(right,SCALE)
    check(lower**8<=q<upper**8,'binary root exact powers')
    return (lower,upper)

def root(a):return (root_bound(a[0])[0],root_bound(a[1])[1])
def p(x,y):return (scalar(x),scalar(y))
def psub(a,b):return (sub(a[0],b[0]),sub(a[1],b[1]))
def padd(a,b):return (add(a[0],b[0]),add(a[1],b[1]))
def det(a,b):return sub(mul(a[0],b[1]),mul(a[1],b[0]))
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def norm2(a):return add(sq(a[0]),sq(a[1]))
def norm16(a):return positive_power(norm2(a),8)
def distance16(a,b):return norm16(psub(a,b))
def disjoint(a,b):return any(a[k][1]<b[k][0] or b[k][1]<a[k][0] for k in [0,1])
def contains_strict(a,lo,hi):return F(lo)<a[0]<=a[1]<F(hi)
def encode(a):return {'lower':str(a[0]),'upper':str(a[1])}
def ep(a):return [encode(z) for z in a]

A=p(0,0); B=p(F(2073,10000),0); C=p(F(4719,10000),F(64,10000))
LAM=F(27,1250); MU=F(1)

def radical_point(base,focus1,focus2,level1,level2,s):
    # Subtract squared-distance equations; solve the affine linear system.
    e=psub(focus1,base); f=psub(focus2,base)
    U=root(s); V=root(add(s,level1)); W=root(add(s,level2))
    a=div(add(norm2(e),sub(U,V)),scalar(2))
    b=div(add(norm2(f),sub(U,W)),scalar(2))
    determinant=det(e,f)
    x=div(sub(mul(a,f[1]),mul(b,e[1])),determinant)
    y=div(sub(mul(e[0],b),mul(f[0],a)),determinant)
    return padd(base,(x,y)),sub(add(sq(x),sq(y)),U)

def outgoing(s):return radical_point(A,B,C,scalar(LAM),scalar(MU),s)

cuts=list(map(F,['9/10000','11/10000','13/10000','1/2','1','100000000000000000']))
bounds=[('38/100','39/100'),('-28/100','-27/100'),('51/100','52/100'),('-91/100','-90/100'),('9','10'),('-39','-38')]
signs=[1,-1,1,-1,1,-1]
samples=[]
for s,(lo,hi),sg in zip(cuts,bounds,signs):
    val=outgoing(scalar(s))[1]
    check(sign(val)==sg,'outgoing sample strict sign')
    check(contains_strict(val,lo,hi),'outgoing sample published coarse bound')
    samples.append({'s':str(s),'residual':encode(val)})

# Independently isolate boundary parameters using 180 rational bisections.
def boundary_parameter(q,h,level):
    qx,qy=q
    n=qx*qx+qy*qy
    def poly(t):return n**8*(((t-1)**2+h*h)**8-(t*t+h*h)**8)-level
    lo,hi=F(-8),F(8)
    check(poly(lo)>0>poly(hi),'independent boundary initial bracket')
    for _ in range(180):
        mid=(lo+hi)/2
        val=poly(mid)
        check(val!=0,'boundary midpoint not exact root')
        if val>0:lo=mid
        else:hi=mid
    check(poly(lo)>0>poly(hi),'boundary final exact polynomial signs')
    return interval(lo,hi)

def offset_point(base,q,h,t):
    x=add(base[0],sub(mul(scalar(q[0]),t),scalar(h*q[1])))
    y=add(base[1],add(mul(scalar(q[1]),t),scalar(h*q[0])))
    return (x,y)

b=F(2073,10000); c=F(4719,10000); d=F(64,10000)
t1=boundary_parameter((c,d),F(10),MU)
t3=boundary_parameter((b,F(0)),F(1),LAM)
t5=boundary_parameter((c-b,d),F(-10),MU-LAM)
A1=offset_point(A,(c,d),F(10),t1)
A3=offset_point(A,(b,F(0)),F(1),t3)
A5=offset_point(B,(c-b,d),F(-10),t5)
vertices=[A1,A,A3,B,A5,C]
for point,boxes in [(A1,[('0.17194','0.17196'),('4.72219','4.72221')]),(A3,[('-0.55229','-0.55227'),None]),(A5,[('0.40359','0.40361'),('-2.64281','-2.64279')])]:
    for k,coarse in enumerate(boxes):
        if coarse:check(contains_strict(point[k],*coarse),'boundary stated coordinate bound')
check(A3[1]==scalar(b),'A3 y equals b exactly')
for v,w in combinations(vertices,2):check(disjoint(v,w),'boundary vertices pairwise distinct')
triple_dets=[]
for i,j,k in combinations(range(6),3):
    z=det(psub(vertices[j],vertices[i]),psub(vertices[k],vertices[i]))
    check(sign(z)!=0,'all twenty boundary triples noncollinear')
    triple_dets.append({'indices':[i+1,j+1,k+1],'determinant':encode(z)})
check(det(psub(B,A),psub(C,A))==scalar(F('0.00132672')),'even determinant exact')
odd=det(psub(A3,A1),psub(A5,A1))
check(contains_strict(odd,'6.37','6.39'),'odd determinant coarse interval')
check(A1[0][0]>b/2 and A5[0][0]>b/2,'two odd vertices excluded by x bound')
a3bad=sub(sub(distance16(A3,C),distance16(A3,A)),scalar(MU))
check(contains_strict(a3bad,'.98','.99'),'A3 C equation fails')
check(LAM>0 and MU>0 and b**16!=LAM,'foci cannot be centers')

center_certificates=[]
center_boxes=[]
for index in range(5):
    lo,hi=cuts[index:index+2]
    leftsign=signs[index]
    # Independently generated 110-step brackets, rather than relying on receipt.
    for step in range(110):
        mid=(lo+hi)/2
        sm=sign(outgoing(scalar(mid))[1])
        check(sm!=0,'outgoing independent bisection sign separated')
        if sm==leftsign:lo=mid
        else:hi=mid
    left=outgoing(scalar(lo))[1]; right=outgoing(scalar(hi))[1]
    check(sign(left)==leftsign and sign(right)==-leftsign,'retained interval has IVT root')
    check(cuts[index]<=lo<hi<=cuts[index+1],'root bracket within original gap')
    X=outgoing(interval(lo,hi))[0]
    for v in vertices:check(disjoint(X,v),'outgoing center disjoint from each boundary vertex')
    for v,w in combinations(vertices,2):check(sign(det(psub(X,v),psub(w,v)))!=0,'outgoing center off all boundary pair lines')
    for Y in center_boxes:check(disjoint(X,Y),'outgoing centers pairwise distinct')
    center_boxes.append(X)
    center_certificates.append({'s_interval':[str(lo),str(hi)],'G_left':encode(left),'G_right':encode(right),'point_box':ep(X)})

# Algebraic actual boundaries remain in the enclosing intervals throughout.
L=sub(distance16(B,A5),distance16(B,A3))
M=sub(distance16(A,A1),distance16(A,A3))
check(L[0]>0 and M[0]>0,'incoming levels positive')
check(sign(det(psub(A5,A3),psub(A1,A3)))!=0,'incoming affine system invertible')
def incoming(s):return radical_point(A3,A5,A1,L,M,s)
H0=incoming(scalar(F(1,100)))[1]
H1=incoming(scalar(F(11,1000)))[1]
check(contains_strict(H0,'.00037','.00038'),'incoming left residual coarse positive bound')
check(contains_strict(H1,'-.00081','-.00080'),'incoming right residual coarse negative bound')
Z=incoming(interval(F(1,100),F(11,1000)))[0]
check(contains_strict(Z[0],'.1677','.1717'),'incoming x box')
check(contains_strict(Z[1],'-.0036','-.0026'),'incoming y box')
for v in vertices:check(disjoint(Z,v),'incoming distinct from boundary')
for v,w in combinations(vertices,2):check(sign(det(psub(Z,v),psub(w,v)))!=0,'incoming off all boundary pair lines')
for X in center_boxes:check(disjoint(Z,X),'incoming distinct from five outgoing centers')

# Direct formal linear identity checks for quad equations. Coordinates ordered
# as E12,E23,E34,E45,E56,E61,lambda,mu; these are coefficient vectors.
def vec(**kw):
    keys=['E12','E23','E34','E45','E56','E61','lam','mu']
    return tuple(F(kw.get(k,0)) for k in keys)
def vsum(*items):return tuple(sum(values) for values in zip(*items))
def vneg(v):return tuple(-x for x in v)
r1=vec(E61=1,E12=-1,mu=-1)
r3=vec(E34=1,E23=-1,lam=-1)
r5=vec(E56=1,E45=-1,mu=-1,lam=1)
balance=vec(E12=1,E34=1,E56=1,E23=-1,E45=-1,E61=-1)
check(vsum(vneg(r1),r3,r5)==balance,'boundary balance from the three exact defining identities')
# M-L-(E61-E56)=E12-E23-E45+E34-E61+E56.
check(vec(E12=1,E23=-1,E45=-1,E34=1,E61=-1,E56=1)==balance,'third old quad follows by balance')
# Outgoing equations have exact constants lambda,mu and mu-lambda, matching
# E34-E23, E61-E12 and E56-E45 respectively.
check(vsum(r1,vneg(r3))==vec(E61=1,E12=-1,E34=-1,E23=1,mu=-1,lam=1),'difference of outgoing levels consistent')

result={'status':'PASS_INDEPENDENT_EXACT_FIVE_CENTER_CERTIFICATE','checks':COUNT,'certified_eighth_root_evaluations':ROOTS,'root_arithmetic':'256-bit-scale binary integer search; exact power inequalities','boundary_bisection_steps':180,'outgoing_bisection_steps':110,'samples':samples,'boundary_parameter_intervals':{'t1':encode(t1),'t3':encode(t3),'t5':encode(t5)},'boundary_boxes':[ep(v) for v in vertices],'all_twenty_boundary_determinants':triple_dets,'odd_determinant':encode(odd),'A3_exclusion_residual':encode(a3bad),'outgoing_centers':center_certificates,'incoming':{'L':encode(L),'M':encode(M),'H_left':encode(H0),'H_right':encode(H1),'point_box':ep(Z)},'limitations':'At least five allowed outgoing centers for a certified incoming realization; no maximality, uniqueness or novelty assertion'}
output=Path(__file__).with_name('INDEPENDENT_CERTIFICATE.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],COUNT,'checks,',ROOTS,'exact eighth-root evaluations')
print('Receipt SHA256',hashlib.sha256(output.read_bytes()).hexdigest())
