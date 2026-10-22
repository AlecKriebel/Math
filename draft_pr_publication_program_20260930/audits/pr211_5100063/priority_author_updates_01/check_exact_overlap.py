#!/usr/bin/env python3
"""Fresh Cartesian comparison; standard library only; no source-copied checker.
The input triangles are the explicitly credited datum in Ferudun 23096994 pp5-6
and the accepted PR211 note. This program independently constructs all objects.
It is a finite overlap/definition control, never an all-period proof.
"""
from fractions import Fraction as F
from pathlib import Path
import datetime, json, argparse

class BQ:
    """Q(sqrt(5),sqrt(21)), basis 1,sqrt5,sqrt21,sqrt105."""
    def __init__(self, x=0):
        self.v = tuple(F(t) for t in x) if isinstance(x,(tuple,list)) else (F(x),F(0),F(0),F(0))
    def __add__(self,y):
        y=asq(y);return BQ(tuple(a+b for a,b in zip(self.v,y.v)))
    __radd__=__add__
    def __neg__(self):return BQ(tuple(-a for a in self.v))
    def __sub__(self,y):return self+-asq(y)
    def __rsub__(self,y):return asq(y)+-self
    def __mul__(self,y):
        y=asq(y);v=[F(0)]*4
        for i,a in enumerate(self.v):
            for j,b in enumerate(y.v):v[i^j]+=a*b*(5 if i&j&1 else 1)*(21 if i&j&2 else 1)
        return BQ(v)
    __rmul__=__mul__
    def conj(self,m):return BQ(tuple(-a if ((i&m).bit_count()%2) else a for i,a in enumerate(self.v)))
    def inv(self):
        num=self.conj(1)*self.conj(2)*self.conj(3);den=self*num
        assert all(x==0 for x in den.v[1:]) and den.v[0]!=0
        return BQ(tuple(x/den.v[0] for x in num.v))
    def __truediv__(self,y):return self*asq(y).inv()
    def __rtruediv__(self,y):return asq(y)*self.inv()
    def __eq__(self,y):return self.v==asq(y).v
    def out(self):return [str(x) for x in self.v]

def asq(x):return x if isinstance(x,BQ) else BQ(x)
def point(x,y):return (asq(x),asq(y))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def mul(t,x):return tuple(t*a for a in x)
def dot(x,y):return sum((a*b for a,b in zip(x,y)),BQ())
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
def area(p):return sum((cross(x,p[(i+1)%len(p)]) for i,x in enumerate(p)),BQ())/2

def outer(p):
    result=[]
    for i,x in enumerate(p):
        y=p[(i+1)%len(p)];n=point(x[0]/21,x[1]/16);m=point(y[0]/21,y[1]/16);d=cross(n,m)
        z=point((m[1]-n[1])/d,(n[0]-m[0])/d)
        assert dot(n,z)==dot(m,z)==1
        result.append(z)
    return result

def inverse(p,f):
    # F + (...) may be omitted by area translation invariance; retain full map.
    return [add(f,mul(1/dot(sub(x,f),sub(x,f)),sub(x,f))) for x in p]

def outer_pedal(p,f):
    # Outer side at original vertex x lies on (x0/21,x1/16).X=1.
    result=[]
    for x in p:
        n=point(x[0]/21,x[1]/16);z=add(f,mul((1-dot(n,f))/dot(n,n),n))
        assert dot(n,z)==1 and cross(sub(z,f),n)==0
        result.append(z)
    return result

def check_orbit(p,lengths):
    lam=F(336,25)
    for i,x in enumerate(p):
        prev=p[i-1];nxt=p[(i+1)%3]
        assert x[0]*x[0]/21+x[1]*x[1]/16==1
        v=sub(nxt,x);assert dot(v,v)==lengths[i]**2
        # exact dual tangency to the same strictly nested confocal ellipse
        normal=point(-v[1],v[0]);w=dot(normal,x)
        assert w*w==(21-lam)*normal[0]*normal[0]+(16-lam)*normal[1]*normal[1]
        uin=mul(1/lengths[i-1],sub(x,prev));uout=mul(1/lengths[i],v)
        bn=point(x[0]/21,x[1]/16)
        assert dot(uin,uin)==dot(uout,uout)==1
        assert cross(sub(uin,uout),bn)==0 and dot(uin,bn)==-dot(uout,bn)
    assert all(p[i]!=p[j] for i in range(3) for j in range(i))

s5=BQ((0,1,0,0));s21=BQ((0,0,1,0))
phases={'H':[point(s21,0),point(-3*s21/5,F(16,5)),point(-3*s21/5,F(-16,5))],
        'V':[point(0,4),point(F(-21,5),F(-8,5)),point(F(21,5),F(-8,5))]}
lengths={'H':[F(8),F(32,5),F(8)],'V':[F(7),F(42,5),F(7)]}
results=[]
for name,p in phases.items():
    check_orbit(p,lengths[name]);q=outer(p);orig=[];out=[];ped=[]
    ell_inv=[mul(1/(x[0]*x[0]/21+x[1]*x[1]/16),x) for x in q]
    mids=[mul(F(1,2),add(x,p[(i+1)%3])) for i,x in enumerate(p)]
    assert ell_inv==mids and area(ell_inv)==area(p)/4
    assert area(q)/area(ell_inv)==F(50,3)
    for sign in [1,-1]:
        f=point(sign*s5,0);a=area(inverse(p,f));b=area(inverse(q,f));c=area(outer_pedal(p,f))
        assert b==F(3,10)*a
        assert inverse(q,f)!=ell_inv
        assert area(inverse(q[::-1],f))==-b
        assert area(inverse(q[1:]+q[:1],f))==b
        assert area(inverse(q*3,f))==3*b
        orig.append(a);out.append(b);ped.append(c)
    assert orig[0]*orig[1]==F(1,324)
    assert out[0]*out[1]==F(1,3600)
    assert orig[0]*orig[1]!=out[0]*out[1]
    results.append({'phase':name,'original_inverse_areas_basis': [x.out() for x in orig],
      'outer_inverse_areas_basis':[x.out() for x in out],
      'original_product':(orig[0]*orig[1]).out(),'outer_product':(out[0]*out[1]).out(),
      'outer_pedal_product':(ped[0]*ped[1]).out(),'outer_over_original_each_focus':'3/10','central_ellipse_inverse_area_basis':area(ell_inv).out(),
      'outer_over_central_ellipse_inverse_area':'50/3'})
result={'schema':'pr211-fresh-exact-overlap-control-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'input_credit':'Ferudun DOI10.5281/zenodo.23096994 pp5-6 and accepted PR211 exact datum; construction/checker freshly authored',
 'field_basis':['1','sqrt5','sqrt21','sqrt105'],'a_squared':'21','b_squared':'16','lambda':'336/25',
 'checks':['boundary incidence','same strict confocal caustic via dual tangency','unit-velocity specular reflection',
 'three distinct vertices','outer intersections satisfy both original tangent equations','actual unit focal inversion',
 'signed shoelace','Theorem A ratio3/10 both phases and foci','original1/324 versus outer1/3600',
 'reversal sign','cyclic relabeling','triple traversal area scaling',
 'central ellipse inverse equals original side midpoint polygon','central ellipse inverse differs from unit focal inverse',
 'midpoint-area and k810 finite triangular ratio50/3'],
 'status':'all assertions passed','limitation':'finite Cartesian definition/overlap control, not a universal proof','results':results}
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('EXACT_OVERLAP_RESULTS.json'))
args=parser.parse_args()
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
