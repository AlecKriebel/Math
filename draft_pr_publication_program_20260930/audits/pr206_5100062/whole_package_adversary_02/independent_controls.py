"""Independent exact controls: squarefree-radicand dictionaries and linear solve.
No package import. Different division mechanism from published conjugation.
"""
from fractions import Fraction as F
from math import gcd,isqrt
from functools import lru_cache
import json,hashlib,sys
from pathlib import Path
RAD=(1,2,3,5,6,10,13,15,26,30,39,65,78,130,195,390)
class R:
    def __init__(self,x=0):self.d={1:F(x)} if not isinstance(x,dict) else {r:F(c) for r,c in x.items() if c}
    def __add__(self,y):
        y=co(y);d=dict(self.d)
        for r,c in y.d.items():d[r]=d.get(r,F(0))+c
        return R(d)
    __radd__=__add__
    def __neg__(self):return R({r:-c for r,c in self.d.items()})
    def __sub__(self,y):return self+-co(y)
    def __rsub__(self,y):return co(y)+-self
    def __mul__(self,y):
        d={};y=co(y)
        for r,a in self.d.items():
            for s,b in y.d.items():
                g=gcd(r,s);k=(r//g)*(s//g);d[k]=d.get(k,F(0))+g*a*b
        return R(d)
    __rmul__=__mul__
    def __truediv__(self,y):return self*inverse(tuple(co(y).d.get(r,F(0)) for r in RAD))
    def __rtruediv__(self,y):return co(y)/self
    def __eq__(self,y):return not (self-co(y)).d
    def sign(self):
        if not self.d:return 0
        scale=2**256;lo=hi=F(0)
        for r,c in self.d.items():
            k=isqrt(r*scale*scale);l=F(k,scale);h=l if k*k==r*scale*scale else F(k+1,scale)
            lo+=c*(l if c>0 else h);hi+=c*(h if c>0 else l)
        if lo>0:return 1
        if hi<0:return -1
        raise RuntimeError('unresolved sign')
    def rational(self):
        if any(r!=1 for r in self.d):raise RuntimeError('not rational')
        return self.d.get(1,F(0))
    def data(self):return {str(r):str(c) for r,c in sorted(self.d.items())}
def co(x):return x if isinstance(x,R) else R(x)
def root(n):return R({n:1})
@lru_cache(None)
def inverse(t):
    # Multiplication matrix in the squarefree basis, solved over Q.
    y=R({r:c for r,c in zip(RAD,t) if c})
    a=[[((y*root(s)).d.get(r,F(0))) for s in RAD]+[F(r==1)] for r in RAD]
    n=len(RAD)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ZeroDivisionError('singular multiplication matrix')
        a[j],a[pivot]=a[pivot],a[j];v=a[j][j];a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                v=a[i][j];a[i]=[x-v*z for x,z in zip(a[i],a[j])]
    ans=R({r:a[j][-1] for j,r in enumerate(RAD) if a[j][-1]})
    if y*ans!=1:raise RuntimeError('linear inverse check')
    return ans
def sqrtq(x):
    q=co(x).rational();v=q.numerator*q.denominator
    if v<=0:raise RuntimeError('nonpositive square')
    out=1;rad=1;p=2
    while p*p<=v:
        k=0
        while v%p==0:v//=p;k+=1
        out*=p**(k//2)
        if k%2:rad*=p
        p+=1
    rad*=v
    if rad not in RAD:raise RuntimeError('unsupported root')
    return root(rad)*F(out,q.denominator)
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return sum((det(x,p[(j+1)%len(p)]) for j,x in enumerate(p)),R())/2
def invert(p,f,r=1):
    ans=[]
    for x,y in p:
        d=(x-f)*(x-f)+y*y
        if d.sign()!=1:raise RuntimeError('bad focal denominator')
        ans.append((f+r*r*(x-f)/d,r*r*y/d))
    return ans
CHECKS={}
def check(group,condition):
    if not condition:raise RuntimeError('independent check failed: '+group)
    CHECKS[group]=CHECKS.get(group,0)+1
s2,s3,s5,s13=[root(i) for i in (2,3,5,13)]
CASES=[('H',F(40,9),[(2*s2,R()),(-4*s2/3,R(F(5,3))),(-4*s2/3,R(-F(5,3)))],[s2/10-s3/80,s2/10+s3/80],F(5,256)),('V',F(40,9),[(R(),s5),(R(-F(8,3)),-s5/3),(R(F(8,3)),-s5/3)],[s5/16,s5/16],F(5,256)),('diamond',F(40,13),[(2*s2,R()),(R(),s5),(-2*s2,R()),(R(),-s5)],[s2*s5/10,s2*s5/10],F(1,10)),('rectangle',F(40,13),[(8*s13/13,5*s13/13),(-8*s13/13,5*s13/13),(-8*s13/13,-5*s13/13),(8*s13/13,-5*s13/13)],[R(F(13,40)),R(F(13,40))],F(169,1600))]
RESULTS=[]
for name,lam,p,expected,prod in CASES:
    for j,x in enumerate(p):
        q=p[(j+1)%len(p)];prev=p[j-1];e=sub(q,x);di=sub(x,prev)
        check('outer_incidence',x[0]*x[0]/8+x[1]*x[1]/5==1)
        k=det(x,q);u=(q[1]-x[1])/k;v=(x[0]-q[0])/k
        check('caustic_tangency',(8-lam)*u*u+(5-lam)*v*v==1)
        ct=((8-lam)*u,(5-lam)*v);fraction=dot(sub(ct,x),e)/dot(e,e)
        check('segment_contact',fraction.sign()>0 and (1-fraction).sign()>0)
        ni=sqrtq(dot(di,di));no=sqrtq(dot(e,e));din=(di[0]/ni,di[1]/ni);dout=(e[0]/no,e[1]/no);n=(x[0]/8,x[1]/5);k=2*dot(din,n)/dot(n,n)
        check('reflection',all(din[h]-k*n[h]==dout[h] for h in (0,1)))
        check('positive_focal_edge',all(det(sub(x,(f,R())),sub(q,(f,R()))).sign()>0 for f in (s3,-s3)))
    a=[]
    for f,target in zip((s3,-s3),expected):
        image=invert(p,f);value=area(image);a.append(value)
        check('exact_area',value==target)
        check('reversal',area(invert(list(reversed(p)),f))==-value)
        for r in (1,2,3,7):check('indexed_repetition',area(image*r)==r*value)
        check('radius_scaling',area(invert(p,f,2))==16*value)
        sp=[(F(3,2)*x,F(3,2)*y) for x,y in p]
        check('physical_scaling',area(invert(sp,F(3,2)*f))==F(4,9)*value)
    check('product',a[0]*a[1]==prod)
    RESULTS.append({'name':name,'areas':[x.data() for x in a],'product':(a[0]*a[1]).data()})
check('even_difference',R(F(169,1600))-F(1,10)==F(9,1600))
print(json.dumps({'status':'PASS','method':'squarefree-radicand dictionaries; independent rational multiplication-matrix division','runtime':sys.version,'flags':repr(sys.flags),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':CHECKS,'total':sum(CHECKS.values()),'controls':RESULTS},indent=2))
