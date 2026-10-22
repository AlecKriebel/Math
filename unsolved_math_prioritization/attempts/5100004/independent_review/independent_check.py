"""Independent exact controls, standard library only; no theorem inferred from samples."""
from fractions import Fraction as F
from collections import Counter
import json

counts = Counter()
def check(ok, group):
    assert ok, group
    counts[group] += 1
def area(p):
    return sum(x*v-u*y for (x,y),(u,v) in zip(p,p[1:]+p[:1]))/2
def outer(p,a2,b2):
    out=[]
    for (x,y),(u,v) in zip(p,p[1:]+p[:1]):
        det=x*v-u*y
        out.append((a2*(v-y)/det,b2*(x-u)/det))
    return out
def geometry(p,a2,b2,al2,be2):
    t=outer(p,a2,b2)
    s=[(al2*x/a2,be2*y/b2) for x,y in t]
    for i,((x,y),(u,v)) in enumerate(zip(p,p[1:]+p[:1])):
        tx,ty=t[i];sx,sy=s[i]
        check(x*x/a2+y*y/b2==1,'true_orbit_geometry')
        check(x*tx/a2+y*ty/b2==1,'true_orbit_geometry')
        check(u*tx/a2+v*ty/b2==1,'true_orbit_geometry')
        check(sx*sx/al2+sy*sy/be2==1,'true_orbit_geometry')
        check(x*sx/al2+y*sy/be2==1,'true_orbit_geometry')
        check(u*sx/al2+v*sy/be2==1,'true_orbit_geometry')
    A,Ap,App=area(p),area(t),area(s)
    check(App==al2*be2/(a2*b2)*Ap,'signed_area_transfer')
    check(area(list(reversed(s)))==-App,'orientation')
    return A,Ap,App

four=[]
for m in range(2,10):
    for n in range(1,m):
        a,b=sorted((F(m*m-n*n),F(2*m*n)),reverse=True)
        h=F(m*m+n*n);a2=a*a;b2=b*b;al2=a2*a2/(h*h);be2=b2*b2/(h*h)
        diamond=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
        rectangle=[(a2/h,b2/h),(-a2/h,b2/h),(-a2/h,-b2/h),(a2/h,-b2/h)]
        d=geometry(diamond,a2,b2,al2,be2);r=geometry(rectangle,a2,b2,al2,be2)
        K=8*a2*a2*b2*b2/(h**4)
        check(d[0]*d[2]==K==r[0]*r[2],'four_period_product')
        check(K!=2*a2*a2*b2*b2/(h**4),'printed_coefficient_negative_control')
        check(d[1]*d[2]!=r[1]*r[2],'product_not_ratio_negative_control')
        four.append({'a':str(a),'b':str(b),'AA_inner':str(K)})

# General-position identities, evaluated independently without square roots.
for a in range(2,10):
    for b in range(1,a):
        a2,b2=F(a*a),F(b*b);c2=a2-b2
        for fraction in [F(1,5),F(1,2),F(4,5)]:
            lam=b2*fraction;al2=a2-lam;be2=b2-lam
            X=a2*al2/c2;Y=-b2*be2/c2
            d=1/(a2*be2)-1/(b2*al2)
            check(X/a2+Y/b2==1,'complex_intersections')
            check(X/al2+Y/be2==1,'complex_intersections')
            check(d==lam*c2/(a2*b2*al2*be2)>0,'transversality')
            check(X!=0 and Y!=0,'transversality')

# Signed shoelace covariance for crossing, zero-area and ordinary traversals.
# These are arbitrary polygons, not claimed to be billiard trajectories.
base=[(F(0),F(0)),(F(3),F(1)),(F(1),F(4)),(F(-2),F(1)),(F(1),F(-2))]
for order in [[0,1,2,3,4],[0,2,4,1,3],[4,3,2,1,0],[0,1,0,1]]:
    p=[base[i] for i in order]
    for u in [F(1,3),F(2),F(7,5)]:
        for v in [F(1,4),F(3),F(9,7)]:
            q=[(u*x,v*y) for x,y in p]
            check(area(q)==u*v*area(p),'arbitrary_signed_covariance')

# A separate exact quadratic-field implementation checks the two six-period controls.
class Quad:
    D=F(5)
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    @staticmethod
    def cast(x): return x if isinstance(x,Quad) else Quad(x)
    def __add__(self,o):
        o=self.cast(o);return Quad(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Quad(-self.a,-self.b)
    def __sub__(self,o): return self+-self.cast(o)
    def __rsub__(self,o): return self.cast(o)+-self
    def __mul__(self,o):
        o=self.cast(o);return Quad(self.a*o.a+self.D*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.cast(o);z=o.a*o.a-self.D*o.b*o.b;return self*Quad(o.a/z,-o.b/z)
    def __rtruediv__(self,o): return self.cast(o)/self
    def __eq__(self,o):
        o=self.cast(o);return self.a==o.a and self.b==o.b
    def __str__(self): return str(self.a)+' + '+str(self.b)+' sqrt('+str(self.D)+')'
six=[]
for D,coordinates,expected in [
    (5,[(2,0,0,0),(F(4,3),0,0,F(1,3)),(-F(4,3),0,0,F(1,3)),(-2,0,0,0),(-F(4,3),0,0,-F(1,3)),(F(4,3),0,0,-F(1,3))],[F(20,9),F(16,5),F(128,81)]),
    (2,[(0,0,1,0),(0,-F(4,3),F(1,3),0),(0,-F(4,3),-F(1,3),0),(0,0,-1,0),(0,F(4,3),-F(1,3),0),(0,F(4,3),F(1,3),0)],[F(32,9),F(5),F(200,81)])]:
    Quad.D=F(D);p=[(Quad(a,b),Quad(c,d)) for a,b,c,d in coordinates]
    values=geometry(p,F(4),F(1),F(32,9),F(5,9))
    for val,coef in zip(values,expected):check(val==Quad(0,coef),'six_period_areas')
    product=values[0]*values[2]
    check(product==F(12800,729),'six_period_product')
    six.append({'D':D,'areas':list(map(str,values)),'product':str(product)})

print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'counts':dict(counts),'four_period_cases':len(four),'six_period_cases':six,'limits':'Finite implementation controls only. The general result uses the published theorem and analytic polarity proof; arbitrary signed polygons are not billiard orbits.'},indent=2))
