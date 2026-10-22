from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import sympy as S

def vsub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(c,a): return tuple(c*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def clip(x): return min(F(1),max(F(0),x))
def segdist2(a,b,c,d):
    u,v,w=vsub(b,a),vsub(d,c),vsub(a,c)
    aa,bb,cc,dd,ee=dot(u,u),dot(u,v),dot(v,v),dot(u,w),dot(v,w)
    candidates=[(F(0),clip(ee/cc)),(F(1),clip((ee+bb)/cc)),(clip(-dd/aa),F(0)),(clip((bb-dd)/aa),F(1))]
    den=aa*cc-bb*bb
    if den:
        ss=(bb*ee-cc*dd)/den; tt=(aa*ee-bb*dd)/den
        if 0<=ss<=1 and 0<=tt<=1: candidates.append((ss,tt))
    return min(dot(z,z) for s,t in candidates for z in [vsub(add(w,mul(s,u)),mul(t,v))])
p5=[(0,-1,0),(0,0,0),(1,0,0),(F(2,5),F(4,5),0),(F(-1,5),0,0),(F(-6,5),0,0)]
p6=[(0,-1,0),(0,0,0),(F(24,25),0,F(-7,25)),(F(48,125),F(96,125),F(-14,25)),(F(-24,125),0,F(-21,25)),(F(-24,125),0,F(4,25)),(F(-149,125),0,F(4,25))]
for label,pts in [('five',p5),('six',p6)]:
    pts=[tuple(map(F,p)) for p in pts]
    es=[vsub(b,a) for a,b in zip(pts,pts[1:])]
    assert [dot(e,e) for e in es]==[F(1)]*len(es)
    projected=[(p[0]-p[2]/10,p[1]) for p in pts]
    distances=[(i+1,j+1,segdist2(projected[i],projected[i+1],projected[j],projected[j+1])) for i,j in combinations(range(len(es)),2) if j>i+1]
    assert all(dd>0 for i,j,dd in distances)
    print(label,'projected exact squared separations',distances)
    weights=([6,5,5] if label=='five' else [150,125,125,112])
    assert tuple(sum(w*es[i+1][k] for i,w in enumerate(weights)) for k in range(3))==(0,0,0)
    if label=='six':
        # Affine simplex determinant, not only linear independence.
        tetra=S.Matrix.hstack(*(S.Matrix(vsub(es[i],es[4])) for i in [1,2,3]))
        print('six affine determinant',tetra.det(),'barycentric weights',[F(w,sum(weights)) for w in weights])

# Independent symbolic circle identity. Q=A+alpha*D-beta*JD.
l,r=S.symbols('l r',positive=True)
a=(r-1+l)/(2*l); b2=r/l-a*a
assert S.factor((a*a+b2)*l-r)==0
assert S.factor(((a-1)**2+b2)*l-1)==0
print('Both two-circle squared-length identities are exact.')
# Every regular-pentagon chord used in the packet has length one.
w=S.sqrt(5); R2=(5+w)/10
assert S.simplify(2*R2*(1-(w-1)/4))==1
assert S.simplify(R2+S.Rational(1,16))<1
print('Regular pentagon edge and ball-radius identities are exact.')
# Noncoincident ring endpoints at t=99/100.
print('Ring endpoint separation squared',S.simplify((R2+S.Rational(1,16))/10000))

# Independent dyadic interval implementation; compares every published decimal-floor bound.
from math import isqrt
import json
ONE=(F(1),F(1))
def point(x): return (F(x),F(x))
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def minus(a,b): return (a[0]-b[1],a[1]-b[0])
def times(a,b):
    z=[x*y for x in a for y in b]; return min(z),max(z)
def divide(a,b):
    assert b[0]>0 or b[1]<0
    return times(a,(1/b[1],1/b[0]))
def square(a): return ((F(0) if a[0]<=0<=a[1] else min(x*x for x in a)), max(x*x for x in a))
def radical(a):
    assert a[0]>=0
    base=2**160
    lows=isqrt(a[0].numerator*base**2//a[0].denominator)
    highs=isqrt(a[1].numerator*base**2//a[1].denominator)+1
    assert F(lows,base)**2<=a[0] and F(highs,base)**2>=a[1]
    return F(lows,base),F(highs,base)
def vs(a,b): return tuple(minus(x,y) for x,y in zip(a,b))
def va(a,b): return tuple(plus(x,y) for x,y in zip(a,b))
def vm(k,a): return tuple(times(k,x) for x in a)
def vnorm2(a):
    ans=point(0)
    for x in a: ans=plus(ans,square(x))
    return ans
def cr(a,b): return minus(times(a[0],b[1]),times(a[1],b[0]))
w=radical(point(5)); r2=divide(plus(point(5),w),point(10)); rr=radical(r2)
co72=divide(minus(w,point(1)),point(4)); sn72=divide(radical(plus(point(10),times(point(2),w))),point(4))
co144=divide(minus(point(-1),w),point(4)); sn144=divide(radical(minus(point(10),times(point(2),w))),point(4))
h=point(F(1,4)); tt=point(F(99,100)); zz=point(0)
q0=(rr,zz,h); q1=(times(rr,co72),times(rr,sn72),h); q2=(times(rr,co144),times(rr,sn144),h); q3=(q2[0],minus(zz,q2[1]),h); q5=vm(tt,q0)
a=q3[:2]; b=q5[:2]; dv=vs(b,a); ell2=vnorm2(dv); circle_r2=minus(ONE,times(square(h),square(minus(ONE,tt))))
alpha=divide(plus(minus(circle_r2,ONE),ell2),times(point(2),ell2)); beta2=minus(divide(circle_r2,ell2),square(alpha)); beta=radical(beta2)
q4=(*vs(va(a,vm(alpha,dv)),vm(beta,(minus(zz,dv[1]),dv[0]))),times(tt,h))
ring=[q0,q1,q2,q3,q4,q5]; rho2=plus(r2,square(h)); cx=divide(rho2,times(point(2),rr)); sy=radical(minus(ONE,square(cx)))
m={'circle_center_distance_squared':ell2,'circle_height_squared':circle_r2,'circle_intersection_radicand':beta2,'stem_x':cx,'stem_y':sy,'ring_plane_gap':minus(h,times(tt,h)),'negative_q3_y':minus(zz,q3[1]),'negative_q4_y':minus(zz,q4[1])}
for i,q in enumerate(ring): m['unit_ball_slack_'+str(i)]=minus(ONE,vnorm2(q)); m['positive_height_'+str(i)]=q[2]
polygon=[(divide(q[0],q[2]),divide(q[1],q[2])) for q in ring[:5]]
for i in range(5):
    j=(i+1)%5;m['origin_left_of_edge_'+str(i)]=cr(polygon[i],polygon[j])
    for k in range(5):
        if k!=i and k!=j: m[f'vertex_{k}_left_of_edge_{i}']=cr(vs(polygon[j],polygon[i]),vs(polygon[k],polygon[i]))
published=json.load(open(Path(__file__).resolve().parents[1] / 'checks.json'))['eight_bar_fixed_tail_barrier']['geometry_margins']
assert m.keys()==published.keys()
for name,interval in m.items():
    assert interval[0]>0 and interval[0]>=F(published[name]),name
print('All',len(m),'eight-bar strict bounds independently certified using 160-bit dyadic outward intervals; every published rational lower bound is valid.')
print('eight-bar independent minimal ball slack >', float(min(m['unit_ball_slack_'+str(i)][0] for i in range(6))))
