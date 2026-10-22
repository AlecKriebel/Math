#!/usr/bin/env python3
"""Fresh exact scalar/reference reconstruction; no source-author imports.
Uses only our independent arithmetic in check_certificate.py.
Analytic comparison inequalities are stated external premises, not proved here.
"""
import check_certificate as c
from fractions import Fraction as F
from functools import lru_cache
import math,json,sys,pathlib
I=c.I;S=c.S;need=c.need;pos=c.pos;neg=c.neg
def atan(x):
    x=F(x);v=sum(((-1)**j*x**(2*j+1)/ (2*j+1) for j in range(120)),F(0));e=x**241/241
    return I(v-e,v+e)
PI=16*atan(F(1,5))-4*atan(F(1,239))
def trigpoint(x,cos=False):
    # Proposal only. The entire remainder and exact PI interval are retained.
    k=round(float(F(x.l+x.h,2*S))/(2*math.pi));v=x-2*k*PI
    need(v.l>=-4*S and v.h<=4*S,'trig reduction')
    term=I(1) if cos else v;z=term
    for j in range(1,37):
        den=(2*j-1)*(2*j) if cos else (2*j)*(2*j+1)
        term=-term*v*v/den;z=z+term
    # cos degree72; sin degree73, next nonzero remainder as in manuscript.
    n=74 if cos else 75;e=I(F(4**n,math.factorial(n)))
    return z+I(-e.h,e.h,True)
def sinbox(x):
    need(x.l>0 and x.h<PI.l,'sine chart')
    a=trigpoint(I(x.l,x.l,True));b=trigpoint(I(x.h,x.h,True));lo=min(a.l,b.l);hi=max(a.h,b.h)
    if x.l<=(PI/2).h and x.h>=(PI/2).l:hi=max(hi,S)
    return I(lo,hi,True)
def cosbox(x):
    need(x.l>0 and x.h<PI.l,'cosine chart')
    a=trigpoint(I(x.l,x.l,True),True);b=trigpoint(I(x.h,x.h,True),True)
    return I(b.l,a.h,True)
def sinc(x):return sinbox(x)/x
def sincprime(x):return (x*cosbox(x)-sinbox(x))/(x*x)
@lru_cache(maxsize=10000)
def hpoint(n):
    X=I(n,n,True);need(X.l>0 and X.h<PI.l,'h chart');z=I(0)
    for j in range(1,81):z=z+(trigpoint(j*X)**2)/(j**3*X*X)
    tail=1/(12800*X*X)
    return -z-(X/PI).log()+I(-tail.h,0,True)
def hcap(x):return hpoint(x.h)
def aparam(k,kind):return I(F(1153,500))-k/4 if kind=='affine' else I(F(9,5))
def external(k,x,kind):
    a=aparam(k,kind);cc=(a+2)/2;rr=(2-a)/2;K=((a-x)*(2-x)).sqrt();rho0=(I(2).sqrt()-a.sqrt())/(I(2).sqrt()+a.sqrt());rhox=rr/(cc-x+K)
    need(pos(a-x) and (pos(x) or neg(x)),'external domain')
    xx=x if pos(x) else -x
    W=k*xx.log()+((cc-x+K)/2).log()-2*k*(1-rho0*rhox).log()
    Wx=k/x-1/K+2*k*rho0*rhox/(K*(1-rho0*rhox))
    return W,Wx,K,rhox,rho0
def floatroots(k,kind):
    a=2.306-k/4 if kind=='affine' else 1.8;cc=(a+2)/2;rr=(2-a)/2;r0=(math.sqrt(2)-math.sqrt(a))/(math.sqrt(2)+math.sqrt(a))
    def w(x):
        K=math.sqrt((a-x)*(2-x));rx=rr/(cc-x+K)
        return k*math.log(abs(x))+math.log((cc-x+K)/2)-2*k*math.log1p(-r0*rx)
    xc=k/(k+1)*math.sqrt(2*a)
    need(w(-2)>0 and w(-1e-8)<0 and w(1e-8)<0 and w(xc)>0,'float proposal bounds')
    def bis(l,h,minus):
        for _ in range(65):
            m=(l+h)/2
            if (w(m)>0)==minus:l=m
            else:h=m
        return (l+h)/2
    return bis(-2,-1e-8,True),bis(1e-8,xc,False)
def roots(k,kind):
    aa=float(F(k.l,S));bb=float(F(k.h,S));vs=[floatroots(t,kind) for t in [aa,(aa+bb)/2,bb]];zs=[]
    for j in [0,1]:
        vals=[v[j] for v in vs];pad=max(1e-9,8*(bb-aa));z=I(F.from_float(min(vals)-pad),F.from_float(max(vals)+pad))
        lo=external(k,I(z.l,z.l,True),kind)[0];hi=external(k,I(z.h,z.h,True),kind)[0];der=external(k,z,kind)[1]
        need((neg(der) and pos(lo) and neg(hi)) if j==0 else (pos(der) and neg(lo) and pos(hi)),'uniform physical roots')
        for _ in range(4):
            m=I((z.l+z.h)//2,(z.l+z.h)//2,True);z=z.intersect(m-external(k,m,kind)[0]/external(k,z,kind)[1])
        zs.append(z)
    return zs
T=I('1.83443047576266171109075363512901884952989750747')
def finite(a,b,kind,out,depth=0):
    try:
        k=I(a,b);ap=aparam(k,kind);need(ap.l>=S and ap.h<2*S and pos(k+1-k*(2/ap).sqrt()),'density positivity');H=(2-ap)/4
        xm,xp=roots(k,kind);need(neg(xm) and pos(xp),'physical sides');_,sm,Km,rm,r0=external(k,xm,kind);_,sp,Kp,rp,_=external(k,xp,kind);sm=-1/sm;sp=1/sp
        need(all(pos(t) and pos(1-t) for t in [rm,rp,r0]),'Poisson ranges')
        api=1+2*k*r0/(1+r0);bpi=4*sm*rm/(1-rm*rm)+4*sp*rp/(1-rp*rp);R0=2*sm*rm/(1-rm)+2*sp*rp/(1-rp)
        Q=PI/api;R=PI*R0/bpi;C=H.log()+k*((ap+2+2*(2*ap).sqrt())/4).log();Ce=C+(T-(xp-xm))/R0
        need(pos(R0) and pos(bpi) and pos(R) and pos(Q-R) and pos(PI-Q) and neg(Ce),'reference caps and target')
        B=(2*H/(api*bpi)).log()+hcap(Q)+hcap(R);P=-PI*Ce/api
        margins=[B+P/Q]
        if kind=='affine':
            margins=[B+P/R,B+P/Q+(sinc(Q)-sinc(R))**2]
            for j in range(32):
                U=I(F(j,32),F(j+1,32));X=R+U*(Q-R)
                need(neg(-P/(X*X)+2*(sinc(X)-sinc(R))*sincprime(X)),'affine monotonicity')
        need(all(pos(v) for v in margins),'finite strict surplus')
        out.append(dict(a=str(a),b=str(b),what=kind,margin=[min(v.l for v in margins),min(v.h for v in margins)],scale=S));return
    except ValueError:
        if depth>=17:raise
        m=(a+b)/2;finite(a,m,kind,out,depth+1);finite(m,b,kind,out,depth+1)
def terminal(a,b,refined,out,depth=0):
    try:
        r=I(a,b);q,_,_,d,*_=c.pars(r);A=1-r*d;p=c.rootbox(r,False);m=c.rootbox(r,True)
        def raw(z):return 1-A*(1-q*q)*z/((1-z)*(z-q*q))
        need(neg(raw(p)) and pos(raw(m)),'terminal raw');wp=-1/raw(p);wm=1/raw(m);P0=r*d+2*q*A/(1+q);D=2*P0*(wp+wm)
        k=A/(r*d);need(pos(1-2*k*q/(1-q)) and pos(D),'terminal density')
        v=-D.log()
        if refined:
            Q=PI*r*d/P0;R=PI*((1+q/p)*wp+(1+q/m)*wm)/(2*(wp+wm))
            need(pos(Q) and pos(R) and pos(PI-Q) and pos(PI-R),'terminal caps');v=v+hcap(Q)+hcap(R)
        need(pos(v),'terminal strict surplus');out.append(dict(a=str(a),b=str(b),what='refined' if refined else 'simple',margin=[v.l,v.h],scale=S));return
    except ValueError:
        if depth>=17:raise
        mid=(a+b)/2;terminal(a,mid,refined,out,depth+1);terminal(mid,b,refined,out,depth+1)
def main():
    out=[];s=-1/I(F(26631,10**6)).log();cap=-1/I(F(41542,10**6)).log()
    witness=c.isolation();need(F(witness['width'][1])<F(T.l,S),'exact L<T linkage')
    q=I(F(41542,10**6));d=c.LN2-2*(1+q).log();g=(1+q)*d+2*q*q.log();k=1/((-1/q.log())*d)-1
    need(pos(g-I('.372861191115')) and neg(k-I(F(21,5))),'terminal cap coverage')
    if '--replay' in sys.argv:
        old=json.loads(pathlib.Path(sys.argv[sys.argv.index('--replay')+1]).read_text())
        for row in old['records']:
            a,b=F(row['a']),F(row['b']);n=len(out)
            if row['what'] in ['affine','constant']:finite(a,b,row['what'],out)
            elif row['what'] in ['simple','refined']:terminal(a,b,row['what']=='refined',out)
            else:raise ValueError('unrecognized reference regime')
            need(len(out)==n+1 and out[-1]==row,'exact slab replay')
        for kind,a,b in [('affine',F(36,25),F(21,10)),('constant',F(21,10),F(21,5)),('simple',F(1,50),F(s.h,S)),('refined',F(s.l,S),F(cap.h,S))]:c.cover(out,kind,a,b)
    elif '--full' in sys.argv:
        finite(F(36,25),F(21,10),'affine',out);finite(F(21,10),F(21,5),'constant',out)
        terminal(F(1,50),F(s.h,S),False,out);terminal(F(s.l,S),F(cap.h,S),True,out)
        for kind,a,b in [('affine',F(36,25),F(21,10)),('constant',F(21,10),F(21,5)),('simple',F(1,50),F(s.h,S)),('refined',F(s.l,S),F(cap.h,S))]:c.cover(out,kind,a,b)
    else:
        for x,kind in [(F(29,20),'affine'),(F(21,10),'affine'),(F(21,10),'constant'),(F(21,5),'constant')]:finite(x,x,kind,out)
        for x,ref in [(F(1,50),False),(F(s.l,S),False),(F(s.h,S),True),(F(cap.h,S),True)]:terminal(x,x,ref,out)
    print(json.dumps({'schema':'ep1038-independent-block-scalar/v1','cap_g':g.out(),'cap_k':k.out(),'records':out,'guards':c.GATES},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
