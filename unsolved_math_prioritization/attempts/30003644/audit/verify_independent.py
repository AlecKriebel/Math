#!/usr/bin/env python3
"""Independent fixed-point rational audit. Python standard library only.

No floating-point/transcendental library enters the proof arithmetic.
All intervals have integer endpoints divided by 2**160. Multiplication and
rational scaling round outward by Python integer floor/ceiling division.
Logarithms use the positive atanh series with a geometric tail bound; pi
uses Machin's formula and alternating arctangent remainder. Sine/cosine
use Taylor's theorem after rigorous period reduction, and full intervals
include every possible critical point. Exponential uses Taylor's theorem.
See AUDIT.md for the mathematical specification and limits.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import hashlib, json, sys
S=1<<160

def ceildiv(a,b):
    assert b>0
    return -((-a)//b)

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=lo;self.hi=lo if hi is None else hi
        assert self.lo<=self.hi
    @classmethod
    def q(cls,x):
        x=Q(x);return cls((x.numerator*S)//x.denominator,ceildiv(x.numerator*S,x.denominator))
    def __add__(a,b):
        if not isinstance(b,I):b=I.q(b)
        return I(a.lo+b.lo,a.hi+b.hi)
    __radd__=__add__
    def __neg__(a):return I(-a.hi,-a.lo)
    def __sub__(a,b):return a+-as_i(b)
    def __rsub__(a,b):return as_i(b)+-a
    def __mul__(a,b):
        if not isinstance(b,I):b=I.q(b)
        p=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]
        return I(min(p)//S,ceildiv(max(p),S))
    __rmul__=__mul__
    def scale(a,q):
        q=Q(q);n,d=q.numerator,q.denominator
        p=[a.lo*n,a.hi*n]
        return I(min(p)//d,ceildiv(max(p),d))
    def recip(a):
        assert not a.lo<=0<=a.hi
        if a.hi<0:return -(-a).recip()
        return I(S*S//a.hi,ceildiv(S*S,a.lo))
    def __truediv__(a,b):
        return a*b.recip() if isinstance(b,I) else a.scale(1/Q(b))
    def excludes(a):return a.lo>0 or a.hi<0
    def abs_upper(a):return max(abs(a.lo),abs(a.hi))
    def exact(a):return {'denominator':str(S),'lower_numerator':str(a.lo),'upper_numerator':str(a.hi)}

def as_i(x):return x if isinstance(x,I) else I.q(x)
def hull(a,b):return I(min(a.lo,b.lo),max(a.hi,b.hi))
def bounds(lo,hi):return I(I.q(lo).lo,I.q(hi).hi)

def log_int(p):
    z=Q(p-1,p+1);N=180
    s=2*sum((z**(2*k+1)/(2*k+1) for k in range(N)),Q())
    tail=2*z**(2*N+1)/((2*N+1)*(1-z*z))
    return bounds(s,s+tail)

def atan(q):
    N=120;s=sum(((-1)**k*q**(2*k+1)/(2*k+1) for k in range(N)),Q())
    nextterm=(-1)**N*q**(2*N+1)/(2*N+1)
    return bounds(min(s,s+nextterm),max(s,s+nextterm))
PI=16*atan(Q(1,5))-4*atan(Q(1,239))
LOG={p:log_int(p) for p in (2,3,5)}
TRIG_ERR=I.q(Q(4**100,factorial(100))).hi
EXP_ERR=I.q(Q(81*4**181,factorial(181))).hi

def point_trig(x):
    # k is any integer; the following subtraction is valid regardless of
    # its selection. The exact rational check |reduced x| <= 4 supplies the
    # only hypothesis needed for the Taylor remainder.
    k=(x.lo+x.hi+2*PI.lo)//(4*PI.lo)
    y=x-(2*k)*PI
    assert y.abs_upper()<=4*S
    yy=y*y
    sin,cos=y,I.q(1);st,ct=y,I.q(1)
    # Recurrences avoid the interval blow-up from quantizing tiny Horner
    # coefficients. Degree 99/98 are both degree-99 Taylor polynomials.
    for j in range(1,50):
        st=-(st*yy)/((2*j)*(2*j+1));ct=-(ct*yy)/((2*j-1)*(2*j))
        sin=sin+st;cos=cos+ct
    return I(max(-S,cos.lo-TRIG_ERR),min(S,cos.hi+TRIG_ERR)),I(max(-S,sin.lo-TRIG_ERR),min(S,sin.hi+TRIG_ERR))

def trig(x):
    if x.hi-x.lo>=2*PI.lo:return I(-S,S),I(-S,S)
    ca,sa=point_trig(I(x.lo));cb,sb=point_trig(I(x.hi))
    c,s=hull(ca,cb),hull(sa,sb)
    q=x/(PI/2)
    # The exact quotient is enclosed, so every possible critical point
    # k*pi/2 in x is considered. False-positive inclusion only widens.
    for k in range(q.lo//S-1,ceildiv(q.hi,S)+2):
        t=(PI/2)*k
        if t.lo<=x.hi and t.hi>=x.lo:
            if k%4==0:c=hull(c,I(S))
            if k%4==2:c=hull(c,I(-S))
            if k%4==1:s=hull(s,I(S))
            if k%4==3:s=hull(s,I(-S))
    return c,s

def exp(x):
    assert x.abs_upper()<=4*S
    acc=I.q(1);term=I.q(1)
    for j in range(1,181):
        term=(term*x)/j;acc=acc+term
    return I(acc.lo-EXP_ERR,acc.hi+EXP_ERR)

def hexq(s):
    # Parse Python hex float syntax as an exact rational, without floats.
    m,e=s.split('p');e=int(e);sign=-1 if m.startswith('-') else 1
    m=m.lstrip('+-');assert m.startswith('0x');a,b=m[2:].split('.')
    q=Q(sign*int(a+b,16),16**len(b))
    return q*2**e if e>=0 else q/2**(-e)

def rawq(raw):
    sign,m,e,bits=raw
    assert m>=0 and m.bit_length()==bits
    return (-1 if sign else 1)*Q(m)*(2**e if e>=0 else Q(1,2**(-e)))

def box(lo,hi,co):
    t=bounds(lo,hi);re,im=I.q(1),I.q(0)
    for p,a in zip((2,3,5),co):
        if not a:continue
        c,s=trig(t*LOG[p]);re=re+c.scale(Q(a,p));im=im-s.scale(Q(a,p))
    return re,im

def scan(path,height,co):
    rows=[json.loads(s) for s in path.read_text().splitlines()]
    last=Q(0);accepted=0;unknown=[];mind=None;digest=hashlib.sha256();raw_exclusion=0
    hist={};cert_digest=hashlib.sha256();containment=0
    for row in rows:
        lo,hi=hexq(row['lo_hex']),hexq(row['hi_hex']);d=row['depth']
        assert lo==last and lo<hi and hi<=height
        assert hi-lo==Q(height,2**d)
        assert (lo/Q(height,2**d)).denominator==1
        last=hi
        r,i=box(lo,hi,co)
        safe=r.excludes() or i.excludes()
        if row['accepted']:
            assert safe,(row,r.exact(),i.exact())
            accepted+=1;hist[d]=hist.get(d,0)+1
            digest.update(f"{row['lo_hex']}:{row['hi_hex']}:{d}\n".encode())
            gaps=[v.lo if v.lo>0 else -v.hi for v in (r,i) if v.excludes()]
            gap=max(gaps);mind=gap if mind is None else min(mind,gap)
            rr=[rawq(v) for v in row['original_re_raw']]
            ii=[rawq(v) for v in row['original_im_raw']]
            assert rr[0]<=rr[1] and ii[0]<=ii[1]
            assert rr[0]>0 or rr[1]<0 or ii[0]>0 or ii[1]<0
            raw_exclusion+=1
            if rr[0]<=Q(r.lo,S)<=Q(r.hi,S)<=rr[1] and ii[0]<=Q(i.lo,S)<=Q(i.hi,S)<=ii[1]:
                containment+=1
        else:
            assert not safe
            unknown.append([str(lo),str(hi)])
        cert_digest.update(json.dumps([str(lo),str(hi),r.exact(),i.exact()],sort_keys=True,separators=(',',':')).encode()+b'\n')
    assert last==height
    return {'complete_exact_cover':True,'total_leaves':len(rows),'accepted':accepted,'depth_histogram':hist,'unresolved':unknown,'original_raw_exclusions_rechecked':raw_exclusion,'original_boxes_containing_independent_boxes':containment,'accepted_endpoint_sha256':digest.hexdigest(),'independent_boxes_sha256':cert_digest.hexdigest(),'minimum_component_gap':str(Q(mind,S))}

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    target=scan(root/'target_leaves.jsonl',10000,(1,1,1))
    assert target['accepted']==4782 and not target['unresolved']
    assert target['original_boxes_containing_independent_boxes']==4782
    assert target['accepted_endpoint_sha256']=='642d2bed994405c2f3fbe99b182d4158f493c4b1346acbe62124992cf96b2618'
    negative=scan(root/'negative_leaves.jsonl',8,(2,0,0))
    assert len(negative['unresolved'])==1
    rt=PI/LOG[2];lo,hi=map(Q,negative['unresolved'][0])
    assert Q(rt.lo,S)>lo and Q(rt.hi,S)<hi
    # Original JSON prints round-trip decimal floats. Even reading these as
    # exact decimal rationals preserves this negative root containment.
    assert Q('4.532360076904297')<Q(rt.lo,S) and Q(rt.hi,S)<Q('4.53236198425293')
    sigma=I.q('1.006705654528482647538233912439');t=I.q('185.725918497342080628141229326837');radius=I.q('1e-20')
    re,im,dr,b2=I.q(1),I.q(0),I.q(0),I.q(0)
    for p in (2,3,5):
        log=LOG[p];am=exp(-sigma*log);c,s=trig(t*log)
        re=re+am*c;im=im-am*s;dr=dr-log*am*c
        b2=b2+log*log*exp(-(sigma-radius)*log)
    residual=Q(re.abs_upper()+im.abs_upper(),S)
    assert residual<Q('1e-27') and Q(dr.lo,S)>Q('.9') and b2.hi<2*S
    assert Q('1e-27')+Q('1e-20')**2<Q('.9')*Q('1e-20')
    assert (sigma-radius).lo>S
    L=sum((LOG[p]/p for p in (2,3,5)),I.q(0))-LOG[5]/30
    assert Q(L.lo,S)>Q('.98')
    hs=[]
    for q in ('1.032','1.033'):
        h=sum((exp(-I.q(q)*LOG[p]) for p in (2,3,5)),I.q(0))-1
        hs.append(h)
    assert hs[0].lo>0 and hs[1].hi<0
    # A broad interval with actual zero must remain inconclusive. Endpoint
    # exclusion alone would fail this control (both endpoint real parts >0).
    nr,ni=box(Q(0),Q(8),(2,0,0));assert not nr.excludes() and not ni.excludes()
    print(json.dumps({'arithmetic':'Python integer/rational fixed-point directed intervals, 160 binary fractional bits; no mpmath','target':target,'negative':negative,'known_negative_root':rt.exact(),'right_halfplane_rouche':{'passes':True,'residual_l1_upper':str(residual),'derivative_real':dr.exact(),'second_derivative_upper':str(Q(b2.hi,S)),'radius':'1e-20'},'sigma_star_bracket':[h.exact() for h in hs],'hypothetical_zero_derivative_lower':str(Q(L.lo,S)),'constants':{'pi':PI.exact(),'logs':{p:LOG[p].exact() for p in (2,3,5)}},'scope':'Only |t| <= 10000; unique zero strictly to the right of Re(s)=1; no all-height conclusion.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
