#!/usr/bin/env python3
"""Independent bounded EP1038 reconstruction. Stdlib only; no author imports.

Exact fixed-point intervals include every primitive rounding and series tail.
Float roots propose boxes only; every accepted box has uniform exact signs.
This program does not assert the analytic reduction to all polynomials.
"""
from fractions import Fraction as F
from functools import lru_cache
import math, json, sys

S=1<<240
GATES=0
def need(p,m):
    global GATES
    GATES+=1
    if not p: raise ValueError(m)
def ceildiv(a,b): return -((-a)//b)
class I:
    __slots__=('l','h')
    def __init__(self,x=0,y=None,raw=False):
        if raw:
            need(type(x) is int and type(y) is int and x<=y,'raw interval')
            self.l,self.h=x,y
        else:
            need(not isinstance(x,float) and not isinstance(y,float),'float construction')
            a=F(x); b=a if y is None else F(y)
            need(a<=b,'reversed interval')
            self.l=a.numerator*S//a.denominator
            self.h=ceildiv(b.numerator*S,b.denominator)
    def __add__(a,b):
        b=iv(b);return I(a.l+b.l,a.h+b.h,True)
    __radd__=__add__
    def __neg__(a):return I(-a.h,-a.l,True)
    def __sub__(a,b):return a+-iv(b)
    def __rsub__(a,b):return iv(b)+-a
    def __mul__(a,b):
        b=iv(b); v=[a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h]
        return I(min(v)//S,ceildiv(max(v),S),True)
    __rmul__=__mul__
    def inv(a):
        need(a.l>0 or a.h<0,'zero inverse')
        return I(S*S//a.h,ceildiv(S*S,a.l),True)
    def __truediv__(a,b):return a*iv(b).inv()
    def __rtruediv__(a,b):return iv(b)*a.inv()
    def __pow__(a,n):
        need(type(n) is int and n>=0,'power')
        if n==0:return I(1)
        if n==2:
            v=[a.l*a.l,a.h*a.h]
            return I(0 if a.l<=0<=a.h else min(v)//S,ceildiv(max(v),S),True)
        z=I(1)
        while n:
            if n&1:z=z*a
            a=a*a;n//=2
        return z
    def intersect(a,b):
        return I(max(a.l,b.l),min(a.h,b.h),True)
    def log(a):
        need(a.l>0,'positive log')
        return I(logpt(a.l).l,logpt(a.h).h,True)
    def exp(a):return I(exppt(a.l).l,exppt(a.h).h,True)
    def sqrt(a):
        need(a.l>=0,'nonnegative sqrt');l=math.isqrt(a.l*S);h=math.isqrt(a.h*S)
        return I(l,h+(h*h!=a.h*S),True)
    def out(a):return [str(F(a.l,S)),str(F(a.h,S))]
    def display(a):return [float(F(a.l,S)),float(F(a.h,S))]
def iv(a):return a if isinstance(a,I) else I(a)
def pos(a):return iv(a).l>0
def neg(a):return iv(a).h<0
def logseries(y):
    need(y.l>=S and y.h<=2*S,'log chart')
    t=(y-1)/(y+1); p=t; z=I(0)
    for j in range(96):z=z+p/(2*j+1);p=p*t*t
    tail=2*p/(193*(1-t*t))
    return 2*z+I(0,tail.h,True)
LN2=logseries(I(2))
@lru_cache(maxsize=4096)
def logpt(n):
    need(n>0,'log endpoint');k=n.bit_length()-1-240
    y=I(n<<(-k),n<<(-k),True) if k<0 else I(n//(1<<k),ceildiv(n,1<<k),True)
    return logseries(y)+k*LN2
@lru_cache(maxsize=4096)
def exppt(n):
    if n<0:return exppt(-n).inv()
    k=0
    while n> (S>>3)*(1<<k):k+=1
    v=I(n//(1<<k),ceildiv(n,1<<k),True);t=I(1);z=I(1)
    for j in range(1,61):t=t*v/j;z=z+t
    tail=t*v/61/(1-v/62);z=z+I(0,tail.h,True)
    for _ in range(k):z=z*z
    return z
class J:
    __slots__=('v','d','dd')
    def __init__(self,v,d=0,dd=0):self.v,self.d,self.dd=iv(v),iv(d),iv(dd)
    def __add__(a,b):
        b=jet(b);return J(a.v+b.v,a.d+b.d,a.dd+b.dd)
    __radd__=__add__
    def __neg__(a):return J(-a.v,-a.d,-a.dd)
    def __sub__(a,b):return a+-jet(b)
    def __rsub__(a,b):return jet(b)+-a
    def __mul__(a,b):
        b=jet(b);return J(a.v*b.v,a.d*b.v+a.v*b.d,a.dd*b.v+2*a.d*b.d+a.v*b.dd)
    __rmul__=__mul__
    def inv(a):return J(1/a.v,-a.d/(a.v**2),2*a.d*a.d/(a.v**3)-a.dd/(a.v**2))
    def __truediv__(a,b):return a*jet(b).inv()
    def __rtruediv__(a,b):return jet(b)*a.inv()
    def __pow__(a,n):
        z=J(1)
        for _ in range(n):z=z*a
        return z
def jet(a):return a if isinstance(a,J) else J(a)
def glog(a):
    a=jet(a);return J(a.v.log(),a.d/a.v,a.dd/a.v-(a.d/a.v)**2)
def series(a,kind):
    a=jet(a);need(a.v.l>=0,'positive series');K=33;z=J(0)
    for m in reversed(range(K)):
        den=math.factorial(2*m+(kind=='S')) if kind!='T' else 2*m+1
        z=z*a+F(1,den)
    Y=I(a.v.h,a.v.h,True)
    den=math.factorial(2*K+(kind=='S')) if kind!='T' else 2*K+1
    R=Y/((2*K+(kind=='S')+2)*(2*K+(kind=='S')+1)) if kind!='T' else Y
    need(pos(1-R) and pos(1-F(K+1,K)*R),'series tail ratio')
    v=(Y**K)/(den*(1-R));der=K*(Y**(K-1))/(den*(1-F(K+1,K)*R))
    return J(z.v+I(0,v.h,True),z.d+I(0,der.h,True)*a.d,0)
def pars(r):
    q=(-1/r).exp();qr=q/(r**2);qrr=q*(1-2*r)/(r**4)
    d=LN2-2*(1+q).log();dr=-2*qr/(1+q);drr=-2*(qrr/(1+q)-qr*qr/((1+q)**2))
    return q,qr,qrr,d,dr,drr,1-r*d,-d-r*dr,-2*dr-r*drr
def gv(r,z,minus):
    q,qr,qrr,d,dr,drr,A,Ar,Arr=pars(r)
    den=z-1 if minus else 1-z;W=(z-q*q).log()-den.log()
    Wz=1/(z-q*q)+1/(1-z);Wzz=-1/((z-q*q)**2)+1/((1-z)**2)
    Wr=-2*q*qr/(z-q*q);Wrz=2*q*qr/((z-q*q)**2)
    Wrr=-2*(qr*qr+q*qrr)/(z-q*q)-(2*q*qr)**2/((z-q*q)**2)
    return A*W-z.log()-d,A*Wz-1/z,Ar*W+A*Wr-dr,Arr*W+2*Ar*Wr+A*Wrr-drr,Ar*Wz+A*Wrz,A*Wzz+1/(z*z)
def floatroots(r):
    q=math.exp(-1/r);d=math.log(2)-2*math.log1p(q);A=1-r*d
    def g(z,minus):return A*math.log((z-q*q)/(z-1 if minus else 1-z))-math.log(z)-d
    B=1+q*q-A*(1-q*q);crit=(B+math.sqrt(max(0,B*B-4*q*q)))/2
    def bis(l,h,minus):
        for _ in range(65):
            m=(l+h)/2
            if (g(m,minus)>0)==minus:l=m
            else:h=m
        return (l+h)/2
    return bis(max(q*1.000001,crit),1-1e-13,False),bis(1+1e-13,4,True)
def rootbox(r,minus):
    aa=float(F(r.l,S));bb=float(F(r.h,S));v=[floatroots(x)[int(minus)] for x in [aa,(aa+bb)/2,bb]]
    pad=max(1e-9,4*(bb-aa),(max(v)-min(v))*.5)
    z=I(F.from_float(min(v)-pad),F.from_float(max(v)+pad));q=pars(r)[0]
    need(z.l>q.h and (z.l>S if minus else z.h<S),'branch box')
    lo=gv(r,I(z.l,z.l,True),minus)[0];hi=gv(r,I(z.h,z.h,True),minus)[0];slope=gv(r,z,minus)[1]
    need((pos(lo) and neg(hi) and neg(slope)) if minus else (neg(lo) and pos(hi) and pos(slope)),'uniform root bracket')
    for _ in range(5):
        m=I((z.l+z.h)//2,(z.l+z.h)//2,True);z=z.intersect(m-gv(r,m,minus)[0]/gv(r,z,minus)[1])
    return z
def width(r,zp,zm):
    q,qr,qrr,*_=pars(r);qj=J(q,qr,qrr);zs=[]
    for z,minus in [(zp,False),(zm,True)]:
        _,gz,gr,grr,grz,gzz=gv(r,z,minus);zr=-gr/gz;zrr=-(grr+2*grz*zr+gzz*zr*zr)/gz;zs.append(J(z,zr,zrr))
    p,m=zs;return 2*(m-p)/((1+qj)**2)+2*qj*qj*(1/m-1/p)/((1+qj)**2)
def bulk(a,b,what,records,depth=0):
    r=I(a,b)
    try:
        p=rootbox(r,False);m=rootbox(r,True);v=width(r,p,m);val=v.dd if what=='convex' else v.d
        need(pos(val) if what in ['positive','convex'] else neg(val),'derivative sign')
        records.append(dict(a=str(a),b=str(b),what=what,bound=val.out()));return
    except ValueError:
        if depth>=17:raise
        c=(a+b)/2;bulk(a,c,what,records,depth+1);bulk(c,b,what,records,depth+1)
def softD(q,y):
    q=jet(q);y=jet(y);A=glog(2*q/((1+q)**2))/glog(q);C=series(y,'C');SS=series(y,'S');b=q*SS/(1-q*C);w=y*b*b
    need(pos(1-q*C.v) if isinstance(q,I) else pos((1-q*C).v),'soft denominator')
    need(w.v.l>=0 and w.v.h<I('0.03').l,'soft branch')
    return A-1+2*A*b*series(w,'T')
def soft(a,b,last,records,depth=0):
    q=I(a,b);r=-1/q.log()
    try:
        # Soft proposals are derived from the regular plus root at endpoints.
        ys=[]
        for x in [a,b]:
            xf=float(x)
            if xf>=.123630684649383:ys.append(0.0)
            else:ys.append(math.log(floatroots(-1/math.log(xf))[0]/xf)**2)
        pad=max(1e-7,500*float(b-a),.5*(max(ys)-min(ys)))
        y=I(0 if last else F.from_float(max(0,min(ys)-pad)),F.from_float(max(ys)+pad))
        lo=softD(q,I(y.l,y.l,True)).v;hi=softD(q,I(y.h,y.h,True)).v;dy=softD(q,J(y,1)).d
        need((last or neg(lo)) and pos(hi) and pos(dy),'soft bracket')
        # Last slab lower sign is analytic only on q<=q_s, as in report.
        yq=-softD(J(q,1),y).d/dy
        m=rootbox(r,True);_,gz,gr,*_=gv(r,m,True);mq=(-gr/gz)/(pars(r)[0]/(r*r))
        qj=J(q,1);yj=J(y,yq);mj=J(m,mq)
        val=(2*mj/((1+qj)**2)+2*qj*qj/(((1+qj)**2)*mj)-4*qj/((1+qj)**2)*series(yj,'C')).d
        need(pos(val),'soft positive derivative');records.append(dict(a=str(a),b=str(b),what='soft_last' if last else 'soft',bound=val.out()));return
    except ValueError:
        if depth>=15:raise
        c=(a+b)/2;soft(a,c,False,records,depth+1);soft(c,b,last,records,depth+1)
def tails():
    r=I(0,F(1,50));E=I(-50).exp();q=I(0,E.h,True);qr=I(0,(2500*E).h,True);d=LN2-2*(1+q).log();dr=-2*qr/(1+q);A=1-r*d;Ar=-d-r*dr
    zp=I(F(499,1000),F(501,1000));zm=I(F(149,100),F(15001,10000));js=[];ws=[]
    for z,minus in [(zp,False),(zm,True)]:
        def simple(zz):return A*((zz-q*q).log()-(zz-1 if minus else 1-zz).log())-zz.log()-d
        gz=A*(1/(z-q*q)+1/(1-z))-1/z
        need((pos(simple(I(z.l,z.l,True))) and neg(simple(I(z.h,z.h,True))) and neg(gz)) if minus else (neg(simple(I(z.l,z.l,True))) and pos(simple(I(z.h,z.h,True))) and pos(gz)),'tail root')
        gr=Ar*((z-q*q).log()-(z-1 if minus else 1-z).log())-2*A*q*qr/(z-q*q)-dr
        js.append(J(z,-gr/gz));raw=1-A*(1-q*q)*z/((1-z)*(z-q*q));need(pos(raw) if minus else neg(raw),'tail raw');ws.append(1/raw if minus else -1/raw)
    p,m=js;qj=J(q,qr);v=(2*(m-p)/((1+qj)**2)+2*qj*qj*(1/m-1/p)/((1+qj)**2)).d
    need(neg(v) and v.l>I('-.788').h and v.h<I('-.737').l,'tail width derivative')
    wp,wm=ws;P0=r*d+2*q*A/(1+q);D=2*P0*(wp+wm)
    need(D.l>=0 and D.h<I('.038237980791').l,'terminal tail D')
    need(pos(1-2*50*I(0,F(1,1<<72))/(d*(1-q))),'tail density')
    return dict(derivative=v.out(),terminal_D=D.out())
def isolation():
    qslo=I('0.123630684649383');qshi=I('0.123630684649384')
    def g(q):return (1+q)*(LN2-2*(1+q).log())+2*q*q.log()
    need(pos(g(qslo)) and neg(g(qshi)),'q_s signs')
    qc=I('0.02571553686652745032257637166391965344');rc=-1/qc.log();eps=I('1e-30');rlo=I((rc-eps).l,(rc-eps).l,True);rhi=I((rc+eps).h,(rc+eps).h,True)
    vals=[]
    for r in [rlo,rhi]:
        p=rootbox(r,False);m=rootbox(r,True);vals.append(width(r,p,m).d)
    need(neg(vals[0]) and pos(vals[1]),'stationary signs')
    r=I(rlo.l,rhi.h,True);p=rootbox(r,False);m=rootbox(r,True);v=width(r,p,m);q=(-1/r).exp()
    need(pos(v.dd),'local convexity');need(v.v.l>I('1.834430475762661').h and v.v.h<I('1.834430475762662').l,'L digits')
    need(q.l>I('.025715536866527').h and q.h<I('.025715536866528').l,'q digits')
    need(pos(I(F(-200,87)).exp()-I('.1')) and pos(qslo-I(F(-200,87)).exp()),'chart overlap')
    return dict(r=r.out(),q=q.out(),width=v.v.out(),derivatives=[x.out() for x in vals])
def controls():
    n=0
    for f in [lambda:I(.1),lambda:I(2,1),lambda:1/I(-1,1),lambda:I(-1).log(),lambda:I(-1).sqrt(),lambda:I(0).inv(),lambda:I(0,1,True).intersect(I(2,3,True))]:
        try:f()
        except ValueError:n+=1
        else:raise ValueError('negative control escaped')
    need(n==7,'controls');return n
def cover(rows,kind,start,end):
    rs=[v for v in rows if v['what']==kind];need(bool(rs),'empty cover')
    need(F(rs[0]['a'])==start and F(rs[-1]['b'])==end,'cover endpoints')
    for j,v in enumerate(rs):
        need(F(v['a'])<=F(v['b']),'reversed slab')
        if j:need(F(rs[j-1]['b'])==F(v['a']),'cover gap or overlap')
        if 'bound' in v:
            z=[F(t) for t in v['bound']];need(z[0]<=z[1],'bound order')
            need(z[1]<0 if kind=='negative' else z[0]>0,'signed certificate')
        if 'margin' in v:need(0<v['margin'][0]<=v['margin'][1] and v['scale']==S,'strict surplus record')
def main():
    rows=[];result={'schema':'ep1038-independent-bounded-reconstruction/v1','negative_controls':controls(),'tail':tails(),'isolation':isolation()}
    if '--global-family' in sys.argv:
        bulk(F(1,50),F(27,100),'negative',rows);bulk(F(27,100),F(28,100),'convex',rows);bulk(F(28,100),F(87,200),'positive',rows)
        soft(F(1,10),F(6181,50000),False,rows);soft(F(6181,50000),F('0.123630684649384'),True,rows)
        for kind,a,b in [('negative',F(1,50),F(27,100)),('convex',F(27,100),F(28,100)),('positive',F(28,100),F(87,200)),('soft',F(1,10),F(6181,50000)),('soft_last',F(6181,50000),F('0.123630684649384'))]:cover(rows,kind,a,b)
        result['family_cover']=rows
    result['guards']=GATES;print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
