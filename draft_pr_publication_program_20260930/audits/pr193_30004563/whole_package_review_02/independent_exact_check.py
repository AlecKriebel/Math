#!/usr/bin/env python3
"""Independent exact check: triple integer square roots, 45-place radicals,
150 boundary isolations, and absolute-coordinate incoming reconstruction.
All validity predicates explicitly raise; no imported author verifier/certificate.
"""
from fractions import Fraction as F
from math import isqrt
from itertools import combinations
import json
from pathlib import Path

class I:
    def __init__(self,a,b=None):
        if isinstance(a,I): self.a,self.b=a.a,a.b; return
        self.a=F(a); self.b=F(a if b is None else b)
        if self.a>self.b: raise ValueError('unordered')
    def __add__(a,b):
        b=I(b);return I(a.a+b.a,a.b+b.b)
    __radd__=__add__
    def __neg__(a):return I(-a.b,-a.a)
    def __sub__(a,b):return a+-I(b)
    def __rsub__(a,b):return I(b)+-a
    def __mul__(a,b):
        b=I(b);v=[x*y for x in [a.a,a.b] for y in [b.a,b.b]];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(a,b):
        b=I(b)
        if b.a<=0<=b.b:raise ValueError('zero divisor')
        return a*I(1/b.b,1/b.a)
    def sq(a):return I(0 if a.a<=0<=a.b else min(a.a*a.a,a.b*a.b),max(a.a*a.a,a.b*a.b))
    def eighth(a):
        if a.a<0:raise ValueError('negative power')
        return I(a.a**8,a.b**8)
    def sign(a):return 1 if a.a>0 else -1 if a.b<0 else 0
    def data(a):return {'exact':[str(a.a),str(a.b)],'display':[float(a.a),float(a.b)]}
    def root(a):
        def grid(q):
            if q<0:raise ValueError('negative root')
            D=10**45; target=q.numerator*D**8//q.denominator
            k=isqrt(isqrt(isqrt(target)))
            lower,upper=F(k,D),F(k+1,D)
            if not lower**8<=q<upper**8:raise ArithmeticError('root error')
            return lower,upper
        return I(grid(a.a)[0],grid(a.b)[1])

def vec(x,y):return I(x),I(y)
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def norm(p):return p[0].sq()+p[1].sq()
def determinant(p,q):return p[0]*q[1]-p[1]*q[0]
def d16(p,q):return norm(sub(p,q)).eighth()
def test(ok,label):
    if not ok:raise AssertionError(label)
def exclude(p,q):return any(a.b<b.a or b.b<a.a for a,b in zip(p,q))
def pdata(p):return [a.data() for a in p]
b,c,d,lam=map(F,['2073/10000','4719/10000','64/10000','27/1250'])
A=vec(0,0);B=vec(b,0);C=vec(c,d)

def outgoing(s):
    u=I(s).root();v=(I(s)+lam).root();w=(I(s)+1).root()
    # Independent direct elimination, y solved after eliminating x.
    x=(b*b+u-v)/(2*b)
    y=(b*(c*c+d*d+u-w)-c*(b*b+u-v))/(2*b*d)
    X=x,y
    return X,norm(X)-u

cut=list(map(F,['9/10000','11/10000','13/10000','1/2','1','10000000000000000']))
G=[outgoing(s)[1] for s in cut]
test([r.sign() for r in G]==[1,-1,1,-1,1,-1],'six endpoint signs')
coarse=[('0.38','0.39'),('-.28','-.27'),('.51','.52'),('-.91','-.90'),('9','10'),('-4.766','-4.765')]
for g,(lo,hi) in zip(G,coarse):test(F(lo)<g.a<=g.b<F(hi),'table G')
x0,y0=b/2,(c*c+d*d-b*c)/(2*d)
test(x0==F(2073,20000) and y0==F(1249057,128000),'analytic circumcenter')
xbox=I(x0-lam/(16*b*10**14),x0);ybox=I(y0-1/(16*d*10**14),y0+(c/b)*lam/(16*d*10**14))
glast=norm((xbox,ybox))-100
test(F('-4.766')<glast.a<=glast.b<F('-4.765'),'analytic G bound')
test(x0*x0+y0*y0==F(39007985196121,409600000000),'circumcenter norm')

def isolate(q,h,lev,base):
    qx,qy=q; n=qx*qx+qy*qy
    def poly(t):return n**8*(((t-1)**2+h*h)**8-(t*t+h*h)**8)-lev
    lo,hi=F(-16),F(16)
    test(poly(lo)>0 and poly(hi)<0,'boundary initial signs')
    for _ in range(150):
        m=(lo+hi)/2
        if poly(m)>0:lo=m
        else:hi=m
    test(poly(lo)>0>poly(hi),'boundary isolated signs')
    T=I(lo,hi)
    p=(I(base[0])+T*qx-h*qy,I(base[1])+T*qy+h*qx)
    return p,{'t':T.data(),'point':pdata(p)}
P1,t1=isolate((c,d),F(10),F(1),(0,0))
P3,t3=isolate((b,F(0)),F(1),lam,(0,0))
P5,t5=isolate((c-b,d),F(-10),1-lam,(b,0))
P=[P1,A,P3,B,P5,C]
for p,q in combinations(P,2):test(exclude(p,q),'six distinct points')
triangles=[determinant(sub(q,p),sub(r,p)) for p,q,r in combinations(P,3)]
for v in triangles:test(v.sign()!=0,'boundary triple')
odd=determinant(sub(P3,P1),sub(P5,P1))
test(F('6.37')<odd.a<=odd.b<F('6.39'),'odd determinant')
cross=[determinant(sub(A,P1),sub(P3,P1)),determinant(sub(A,P1),sub(B,P1)),determinant(sub(B,P3),sub(P1,P3)),determinant(sub(B,P3),sub(A,P3))]
test([x.sign() for x in cross]==[-1,1,1,-1],'strict crossing')
L=d16(B,P5)-d16(B,P3); M=d16(A,P1)-d16(A,P3)
test(L.a>0 and M.a>0,'incoming levels positive')
Q0,R0=sub(P5,P3),sub(P1,P3)
D=determinant(Q0,R0)

def incoming(s):
    u=I(s).root();v=(I(s)+L).root();w=(I(s)+M).root()
    # Solve directly for absolute Z rather than translated Y.
    rhsq=norm(P5)-norm(P3)+u-v
    rhsr=norm(P1)-norm(P3)+u-w
    z=((rhsq*R0[1]-rhsr*Q0[1])/(2*D),(Q0[0]*rhsr-R0[0]*rhsq)/(2*D))
    return z,norm(sub(z,P3))-u
H=[incoming(F(s))[1] for s in ['1/100','11/1000']]
for h,(lo,hi) in zip(H,[('.00037','.00038'),('-.00081','-.00080')]):test(F(lo)<h.a<=h.b<F(hi),'incoming table')
Z=incoming(I('1/100','11/1000'))[0]
for z,(lo,hi) in zip(Z,[('.1677','.1717'),('-.0036','-.0026')]):test(F(lo)<z.a<=z.b<F(hi),'incoming whole box')
for p in P:test(exclude(Z,p),'Z nonboundary')
for p,q in combinations(P,2):test(determinant(sub(Z,p),sub(q,p)).sign()!=0,'Z pair collinearity')
roots=[]
for lo,hi in zip(cut[:-1],cut[1:]):
    ls=outgoing(lo)[1].sign()
    for _ in range(100):
        mid=(lo+hi)/2;sg=outgoing(mid)[1].sign()
        test(sg!=0,'midpoint nonzero')
        if sg==ls:lo=mid
        else:hi=mid
    test(outgoing(lo)[1].sign()==ls and outgoing(hi)[1].sign()==-ls,'retained sign change')
    X=outgoing(I(lo,hi))[0]
    for p in P:test(exclude(X,p),'X nonboundary')
    for p,q in combinations(P,2):test(determinant(sub(X,p),sub(q,p)).sign()!=0,'X pair collinearity')
    roots.append({'s':I(lo,hi).data(),'X':pdata(X)})
for r,s in combinations(roots,2):test(F(r['s']['exact'][1])<F(s['s']['exact'][0]),'five disjoint retained intervals')
# A sparse linear-form calculation checks all six quad identities from the
# defining distance differences, using independent symbolic coefficient vectors.
# Coordinates in basis [a,f,g,lambda,1,r3,qA].
a,f,g,l,one,r,q=[tuple(int(i==j) for i in range(7)) for j in range(7)]
def plus(*v):return tuple(sum(c) for c in zip(*v))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))
r1=plus(r,minus(a,f));r5=plus(r,minus(g,plus(f,l)));qB=plus(q,l);qC=plus(q,one)
identities=[minus(plus(a,r),plus(r1,f)),minus(plus(f,l,r5),plus(r,g)),minus(plus(g,one,tuple(-x for x in l),r1),plus(r5,a,one)),minus(plus(f,qB),plus(q,f,l)),minus(plus(g,qC),plus(qB,g,one,tuple(-x for x in l))),minus(plus(a,one,q),plus(qC,a))]
for v in identities:test(not any(v),'symbolic six-face residual')
result={'status':'PASS_INDEPENDENT_SOURCE_MATCHED_FIXED_BOUNDARY_FIVE_OUTGOING_PLUS_INCOMING','arithmetic':'Fraction intervals; eighth roots via three math.isqrt calls on scaled integers; 45 places; 150 boundary bisections; 100 outgoing refinements','G':[x.data() for x in G],'analytic_G_10^16':glast.data(),'boundary_parameters':[t1,t3,t5],'odd_determinant':odd.data(),'boundary_triple_signs':[x.sign() for x in triangles],'crossing_signs':[x.sign() for x in cross],'incoming_levels':[L.data(),M.data()],'H':[x.data() for x in H],'Z_whole':pdata(Z),'roots':roots,'symbolic_face_residuals':[list(v) for v in identities]}
Path(__file__).with_name('independent_exact_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status']);print('G', [r['display'] for r in result['G']]);print('H',[r['display'] for r in result['H']]);print('Odd',odd.data()['display']); print('Z',[x.data()['display'] for x in Z])
