#!/usr/bin/env python3
"""Independent finite exact controls; Python stdlib only.
Effects: reads no external inputs, opens no network/process; writes one sibling JSON.
Arithmetic is Q(sqrt(5),sqrt(21)), with exact ordering and inversion.
These finite checks supplement, and do not replace, UNIVERSAL_RECONSTRUCTION.md.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd
import json

class F:
    def __init__(self, x=0):
        self.c = x.c if isinstance(x,F) else tuple(map(Q,x)) if isinstance(x,(tuple,list)) else (Q(x),Q(0),Q(0),Q(0))
        assert len(self.c)==4
    def __add__(self,y):
        y=F(y);return F(tuple(a+b for a,b in zip(self.c,y.c)))
    __radd__=__add__
    def __neg__(self):return F(tuple(-a for a in self.c))
    def __sub__(self,y):return self+-F(y)
    def __rsub__(self,y):return F(y)+-self
    def __mul__(self,y):
        y=F(y);z=[Q(0)]*4
        for i,a in enumerate(self.c):
            for j,b in enumerate(y.c):
                z[i^j]+=a*b*(5 if i&j&1 else 1)*(21 if i&j&2 else 1)
        return F(z)
    __rmul__=__mul__
    def conjugate(self,mask):
        return F(tuple((-1 if (i&mask).bit_count()%2 else 1)*a for i,a in enumerate(self.c)))
    def inverse(self):
        n=self.conjugate(1)*self.conjugate(2)*self.conjugate(3);d=self*n
        assert d.c[1:]==(0,0,0) and d.c[0]
        return F(tuple(a/d.c[0] for a in n.c))
    def __truediv__(self,y):return self*F(y).inverse()
    def __rtruediv__(self,y):return F(y)*self.inverse()
    def __pow__(self,n):
        assert n>=0
        r=F(1)
        for _ in range(n):r=r*self
        return r
    def __eq__(self,y):return self.c==F(y).c
    def sign(self):
        def sqsign(a,b):
            sa=(a>0)-(a<0);sb=(b>0)-(b<0)
            if not sb:return sa
            if not sa:return sb
            if sa==sb:return sa
            d=a*a-5*b*b
            return sa*((d>0)-(d<0))
        a,b,c,d=self.c;su=sqsign(a,b);sv=sqsign(c,d)
        if not sv:return su
        if not su:return sv
        if su==sv:return su
        u2minus21v2=(a*a+5*b*b-21*(c*c+5*d*d),2*a*b-42*c*d)
        return su*sqsign(*u2minus21v2)
    def __repr__(self):
        names=['1','sqrt(5)','sqrt(21)','sqrt(105)']
        return ' + '.join(str(c)+'*'+n for c,n in zip(self.c,names) if c) or '0'

s5=F((0,1,0,0));s21=F((0,0,1,0));zero=F(0)
checks=[];positives=[]
def eq(label,x,y=0):
    assert x==y,(label,str(x),str(y));checks.append(label)
def pos(label,x):
    assert x.sign()>0,(label,str(x));positives.append(label)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,t):return tuple(a*t for a in x)
def dot(x,y):return sum((a*b for a,b in zip(x,y)),zero)
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(p):return sum((det(x,p[(j+1)%len(p)]) for j,x in enumerate(p)),zero)/2
def linefoot(f,p,q):
    d=sub(q,p);return add(p,scale(d,dot(sub(f,p),d)/dot(d,d)))
def crossline(n,m):
    h=det(n,m);return ((m[1]-n[1])/h,(n[0]-m[0])/h)
def projective(p,A,c):return (A*(p[0]+c)/(A+c*p[0]),A*p[1]/(A+c*p[0]))

def case(name,P,A,B,lam,c):
    n=len(P);N=[(p[0]/A,p[1]/B) for p in P]
    V=[crossline(N[j],N[(j+1)%n]) for j in range(n)]
    for j,p in enumerate(P):
        eq(name+':boundary:'+str(j),p[0]**2/A+p[1]**2/B,1)
        e=sub(P[(j+1)%n],p);u=sub(p,P[j-1]);normal=N[j]
        reflected=sub(u,scale(normal,2*dot(u,normal)/dot(normal,normal)))
        eq(name+':reflection-parallel:'+str(j),det(reflected,e))
        pos(name+':reflection-forward:'+str(j),dot(reflected,e))
        aq=e[0]**2/(A-lam)+e[1]**2/(B-lam)
        bq=2*(p[0]*e[0]/(A-lam)+p[1]*e[1]/(B-lam))
        cq=p[0]**2/(A-lam)+p[1]**2/(B-lam)-1
        eq(name+':caustic-discriminant:'+str(j),bq*bq-4*aq*cq)
        eq(name+':outer-tangent-start:'+str(j),dot(N[j],V[j-1]),1)
        eq(name+':outer-tangent-end:'+str(j),dot(N[j],V[j]),1)
    target={};chord={};inverse={}
    for sign in [1,-1]:
        f=(sign*c,zero)
        feet=[linefoot(f,V[j-1],V[j]) for j in range(n)]
        for j,q in enumerate(feet):
            eq(name+':actual-side-incidence:'+str(sign)+':'+str(j),det(sub(q,V[j-1]),sub(V[j],V[j-1])))
            eq(name+':actual-side-perpendicular:'+str(sign)+':'+str(j),dot(sub(q,f),sub(V[j],V[j-1])))
            eq(name+':auxiliary-circle:'+str(sign)+':'+str(j),dot(q,q),A)
            formula=projective(P[j],A,sign*c)
            for k in [0,1]:eq(name+':closed-foot:'+str(sign)+':'+str(j)+':'+str(k),q[k],formula[k])
        target[sign]=area(feet)
        chord[sign]=area([linefoot(f,P[j],P[(j+1)%n]) for j in range(n)])
        inv=[add(f,scale(sub(p,f),1/dot(sub(p,f),sub(p,f)))) for p in P]
        inverse[sign]=area(inv)
        eq(name+':reversal:'+str(sign),area(list(reversed(feet))),-target[sign])
        eq(name+':fixed-repeat:'+str(sign),area(feet*2),2*target[sign])
        eq(name+':cyclic-cut:'+str(sign),area(feet[-1:]+feet[:-1]),target[sign])
    if A==21:
        R=[projective(v,A,c) for v in V]
        d=-c*lam/(B-lam);radius=F(Q(15,4))*s21
        for j,r in enumerate(R):
            eq(name+':bicentric-circle:'+str(j),(r[0]-d)**2+r[1]**2,radius**2)
            eq(name+':bicentric-contact:'+str(j),dot(projective(P[j],A,c),r),A)
        eq(name+':contact-area-ratio',target[1]/area(R),F(Q(2,15)))
        for sign in [1,-1]:eq(name+':opposite-focus-inverse:'+str(sign),target[sign],F(Q(2016,5))*inverse[-sign])
    return {'outer_plus':str(target[1]),'outer_minus':str(target[-1]),'outer_product':str(target[1]*target[-1]),'chord_product':str(chord[1]*chord[-1]),'unit_inverse_product':str(inverse[1]*inverse[-1])},target,chord,inverse

# Sanity checks for field ordering/inverse before geometric controls.
eq('field:sqrt5-square',s5*s5,5);eq('field:sqrt21-square',s21*s21,21)
for x in [s21+s5,3-s5,s5*s21-10,1-s21+s5]:
    eq('field:inverse:'+str(x),x*x.inverse(),1)
pos('field:ordering',s21-s5)
H=[(s21,zero),(-3*s21/5,F(Q(16,5))),(-3*s21/5,F(Q(-16,5)))]
V=[(zero,F(4)),(F(Q(-21,5)),F(Q(-8,5))),(F(Q(21,5)),F(Q(-8,5)))]
D=[(F(2),zero),(zero,F(1)),(F(-2),zero),(zero,F(-1))]
C=[(4*s5/5,s5/5),(-4*s5/5,s5/5),(-4*s5/5,-s5/5),(4*s5/5,-s5/5)]
results={}
for name,P,A,B,lam,c in [('H',H,F(21),F(16),F(Q(336,25)),s5),('V',V,F(21),F(16),F(Q(336,25)),s5)]:
    r,t,h,i=case(name,P,A,B,lam,c);results[name]=r
    eq(name+':expected-outer-product',t[1]*t[-1],F(Q(12544,25)))
    eq(name+':expected-chord-product',h[1]*h[-1],F(Q(7225344,390625)))
    eq(name+':expected-inverse-product',i[1]*i[-1],F(Q(1,324)))
    if name=='H':
        eq('H:plus',t[1],(49*s21+7*s5)/10);eq('H:minus',t[-1],(49*s21-7*s5)/10)
    else:eq('V:both',t[1],F(Q(112,5)));eq('V:minus',t[-1],F(Q(112,5)))

# For central-symmetric four-periodics the tangent-foot area is independent
# of focus sign and expressible without adjoining sqrt(3): symmetrize algebra.
# Represent focus f symbolically as a vector coefficient and use quadratic
# area polynomial: B(f)=B(0)+f B1+f^2 B2; f^2=3. Geometry checks at f=0
# establish actual sides; construction is affine in f for any line.
for name,P,expected in [('D',D,4),('C',C,5)]:
    A=F(4);B=F(1);lam=F(Q(4,5));n=len(P);N=[(p[0]/A,p[1]/B) for p in P];Vs=[crossline(N[j],N[(j+1)%n]) for j in range(n)]
    for j,p in enumerate(P):
        eq(name+':boundary:'+str(j),p[0]**2/A+p[1]**2/B,1)
        e=sub(P[(j+1)%n],p);u=sub(p,P[j-1]);nn=N[j]
        reflected=sub(u,scale(nn,2*dot(u,nn)/dot(nn,nn)))
        eq(name+':reflection:'+str(j),det(reflected,e));pos(name+':forward:'+str(j),dot(reflected,e))
        aq=e[0]**2/(A-lam)+e[1]**2/(B-lam);bq=2*(p[0]*e[0]/(A-lam)+p[1]*e[1]/(B-lam));cq=p[0]**2/(A-lam)+p[1]**2/(B-lam)-1
        eq(name+':caustic:'+str(j),bq*bq-4*aq*cq)
    q0=[linefoot((zero,zero),Vs[j-1],Vs[j]) for j in range(n)]
    q1=[sub(linefoot((F(1),zero),Vs[j-1],Vs[j]),q0[j]) for j in range(n)]
    B0=area(q0);B2=area(q1);B1=area([add(x,y) for x,y in zip(q0,q1)])-B0-B2
    eq(name+':linear-focus-coefficient',B1);eq(name+':area-at-sqrt3',B0+3*B2,expected)
    results[name]={'B0':str(B0),'B1':str(B1),'B2':str(B2),'both_focal_areas':str(B0+3*B2),'outer_product':str((B0+3*B2)**2)}

# Detect the cited source's printed incorrect rectangle: (±2/sqrt5,±2/sqrt5).
bad=(2*s5/5,2*s5/5)
eq('wrong-rectangle:boundary-residual',bad[0]**2/4+bad[1]**2-1,0)
bad_normal=(bad[0]/4,bad[1]);bad_in=(4*s5/5,zero);bad_out=(zero,-4*s5/5)
bad_ref=sub(bad_in,scale(bad_normal,2*dot(bad_in,bad_normal)/dot(bad_normal,bad_normal)))
assert det(bad_ref,bad_out)!=0
results['wrong_printed_rectangle']={'reflection_cross_residual':str(det(bad_ref,bad_out)),'fails':True}

lattice_cases=0
for n in range(3,40):
    for tau in range(1,(n+1)//2):
        if gcd(n,tau)!=1:continue
        step=Q(tau,n);roots={Q(0),step}
        for j in range(n):
            w=(-j*step)%1
            singular=[h for h in range(n) if (w+h*step)%1 in roots]
            assert set(singular)=={j,(j+1)%n}
            lattice_cases+=1

report={'arithmetic':'exact Q(sqrt(5),sqrt(21)); no floating equality checks','equality_checks':len(checks),'strict_positive_checks':len(positives),'lattice_singular_phase_checks':lattice_cases,'lattice_n_range':[3,39],'fixtures':results,'passed':True,'scope':'finite checks; universal proof in separate reconstruction','effects':'one sibling output JSON only; no input source/review imported'}
Path(__file__).with_name('INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
