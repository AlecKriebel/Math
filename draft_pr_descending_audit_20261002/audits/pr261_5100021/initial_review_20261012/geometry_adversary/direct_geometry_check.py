"""Independent conic-tangency checks; written before submitted proof exposure."""
import sys, json, math, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'_python'))
import mpmath as mp
mp.mp.dps=85

def vadd(p,q):return p[0]+q[0],p[1]+q[1]
def vsub(p,q):return p[0]-q[0],p[1]-q[1]
def vmul(s,p):return s*p[0],s*p[1]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return mp.sqrt(dot(p,p))
def pedal_anti(poly,focus):
    rel=[vsub(p,focus) for p in poly]
    feet=[];anti=[];mins=[]
    for p,q in zip(rel,rel[1:]+rel[:1]):
        d=vsub(q,p);k=det(p,q);d2=dot(d,d)
        feet.append((k*d[1]/d2,-k*d[0]/d2))
        pp=dot(p,p);qq=dot(q,q)
        anti.append(((pp*q[1]-qq*p[1])/k,(p[0]*qq-q[0]*pp)/k))
        mins.append(abs(k)/(norm(p)*norm(q)))
    return feet,anti,min(mins)
def area(poly):return sum(det(p,q) for p,q in zip(poly,poly[1:]+poly[:1]))/2

def step(p,a,b,lam):
    ac=mp.sqrt(a*a-lam);bc=mp.sqrt(b*b-lam)
    w=(p[0]/ac,p[1]/bc);s=dot(w,w);r=mp.sqrt(s-1)
    candidates=[]
    for sign in (1,-1):
        t=(ac*(w[0]-sign*r*w[1])/s,bc*(w[1]+sign*r*w[0])/s)
        d=vsub(t,p)
        z=-2*(p[0]*d[0]/(a*a)+p[1]*d[1]/(b*b))/(d[0]*d[0]/(a*a)+d[1]*d[1]/(b*b))
        q=vadd(p,vmul(z,d))
        if det(p,q)>0:candidates.append(q)
    if len(candidates)!=1:raise ValueError(('bad orientation branch',p,a,b,lam,len(candidates)))
    return candidates[0]
def orbit(a,b,lam,n,t):
    p=(a*mp.cos(t),b*mp.sin(t));poly=[];turn=mp.mpf(0)
    for _ in range(n):
        poly.append(p);q=step(p,a,b,lam)
        ps=(p[0]/a,p[1]/b);qs=(q[0]/a,q[1]/b)
        turn+=mp.atan2(det(ps,qs),dot(ps,qs));p=q
    return poly,p,turn

def caustic(a,b,n,m):
    if n==4 and m==1:return a*a*b*b/(a*a+b*b)
    lo=b*b*mp.mpf('1e-70');hi=b*b*(1-mp.mpf('1e-70'))
    target=2*mp.pi*m
    for _ in range(270):
        mid=(lo+hi)/2
        advance=orbit(a,b,mid,n,mp.mpf(0))[2]
        if advance<target:lo=mid
        else:hi=mid
    return (lo+hi)/2

def strnum(x):return mp.nstr(x,35)
def resid(poly,a,b,lam):
    outer=mp.mpf(0);tang=mp.mpf(0);reflection=mp.mpf(0)
    for i,p in enumerate(poly):
        prev=poly[(i-1)%len(poly)];q=poly[(i+1)%len(poly)]
        outer=max(outer,abs(p[0]*p[0]/(a*a)+p[1]*p[1]/(b*b)-1))
        d=vsub(q,p);normal=(d[1],-d[0]);h=dot(normal,p)
        tang=max(tang,abs(h*h-(a*a-lam)*normal[0]**2-(b*b-lam)*normal[1]**2)/(a*a*dot(normal,normal)))
        incoming=vsub(p,prev);incoming=vmul(1/norm(incoming),incoming)
        outgoing=vsub(q,p);outgoing=vmul(1/norm(outgoing),outgoing)
        en=(p[0]/(a*a),p[1]/(b*b));ref=vsub(incoming,vmul(2*dot(incoming,en)/dot(en,en),en))
        reflection=max(reflection,norm(vsub(ref,outgoing)))
    return outer,tang,reflection

def case(a0,b0,n,m):
    a=mp.mpf(a0);b=mp.mpf(b0);c=mp.sqrt(a*a-b*b);lam=caustic(a,b,n,m)
    phases=[mp.mpf(t) for t in ('0','.173','.61','1.17','2.013')]
    products=[];ap=[];aa=[];closures=[];circles=[];minangles=[];reflections=[];outer=[];tangent=[];sym=[];focusdiff=[];reversal=[];cyclic=[];scaling=[];primitive=[]
    for t in phases:
        poly,end,advance=orbit(a,b,lam,n,t)
        closures.append(norm(vsub(end,poly[0]))/a)
        op,tr,rr=resid(poly,a,b,lam);outer.append(op);tangent.append(tr);reflections.append(rr)
        p1,a1,k=pedal_anti(poly,(c,mp.mpf(0)));x=area(p1);y=area(a1);products.append(x*y);ap.append(x);aa.append(y);minangles.append(k)
        circles.append(max(abs(dot(vadd(q,(c,mp.mpf(0))),vadd(q,(c,mp.mpf(0))))-(a*a-lam)) for q in p1)/(a*a))
        p2,a2,_=pedal_anti(poly,(-c,mp.mpf(0)));focusdiff.append(abs(area(p2)*area(a2)-x*y)/max(1,abs(x*y)))
        prev,arev,_=pedal_anti(poly[::-1],(c,mp.mpf(0)));reversal.append(max(abs(area(prev)+x),abs(area(arev)+y))/max(1,abs(x),abs(y)))
        pc,ac,_=pedal_anti(poly[1:]+poly[:1],(c,mp.mpf(0)));cyclic.append(abs(area(pc)*area(ac)-x*y)/max(1,abs(x*y)))
        factor=mp.mpf('2.7');ps,ass,_=pedal_anti([vmul(factor,q) for q in poly],(factor*c,mp.mpf(0)));scaling.append(abs(area(ps)*area(ass)-factor**4*x*y)/max(1,abs(factor**4*x*y)))
        if n%2==0:sym.append(max(norm(vadd(poly[i],poly[i+n//2]))/a for i in range(n//2)))
        primitive.append(min(norm(vsub(poly[d],poly[0]))/a for d in range(1,n) if n%d==0))
    scale=max(1,max(abs(p) for p in products));span=max(products)-min(products)
    return {'a':a0,'b':b0,'N':n,'winding':m,'gcd':math.gcd(n,m),'lambda':strnum(lam),'lambda_fraction_of_b2':strnum(lam/(b*b)),'phases':[strnum(t) for t in phases],'products':[strnum(p) for p in products],'pedal_areas':[strnum(p) for p in ap],'antipedal_areas':[strnum(p) for p in aa],'relative_product_span':strnum(span/scale),'max_closure':strnum(max(closures)),'max_outer_residual':strnum(max(outer)),'max_tangency_residual':strnum(max(tangent)),'max_reflection_residual':strnum(max(reflections)),'max_pedal_circle_residual':strnum(max(circles)),'minimum_antipedal_angle_sine':strnum(min(minangles)),'minimum_proper_divisor_return_distance':strnum(min(primitive)),'max_central_symmetry_residual':strnum(max(sym)) if sym else None,'max_other_focus_product_difference':strnum(max(focusdiff)),'max_reversal_area_residual':strnum(max(reversal)),'max_cyclic_product_residual':strnum(max(cyclic)),'max_scaling_degree4_residual':strnum(max(scaling))}

def exact_axial():
    from fractions import Fraction as F
    poly=[(F(5),F(0)),(F(0),F(3)),(-F(5),F(0)),(F(0),-F(3))]
    rel=[vsub(p,(F(4),F(0))) for p in poly]
    pp=[];aa=[]
    for p,q in zip(rel,rel[1:]+rel[:1]):
        d=vsub(q,p);k=det(p,q);dd=dot(d,d);p2=dot(p,p);q2=dot(q,q)
        pp.append((k*d[1]/dd,-k*d[0]/dd))
        aa.append(((p2*q[1]-q2*p[1])/k,(p[0]*q2-q[0]*p2)/k))
    # Area calculations keep rational values despite norm used only for conditioning.
    x=area(pp);y=area(aa)
    assert x==F(3375,289) and y==60 and x*y==F(202500,289)
    return {'pedal_vertices':[[str(x) for x in p] for p in pp],'antipedal_vertices':[[str(x) for x in p] for p in aa],'pedal_area':str(x),'antipedal_area':str(y),'product':str(x*y)}

if __name__=='__main__':
    cases=[]
    for a,b,pairs in [('5','3',[(4,1),(8,1),(8,3),(12,1),(12,5),(16,1),(16,3),(16,5),(16,7),(20,1),(20,9)]),('1.0001','1',[(4,1),(8,3),(12,5)]),('10','1',[(4,1),(8,1),(8,3),(12,5)])]:
        for n,m in pairs:
            r=case(a,b,n,m);cases.append(r)
            print('case',a,b,n,m,'product_span',r['relative_product_span'],'closure',r['max_closure'],flush=True)
    controls=[case('5','3',6,1),case('5','3',10,3)]
    result={'provenance':'Written and run before PROOF.md or author/prior-review checkers read; only mpmath arithmetic, direct conic tangency, reflection, linear algebra, and shoelace.','digits':mp.mp.dps,'exact_four_period_axial':exact_axial(),'target_cases':cases,'outside_target_controls':controls}
    Path('PRE_EXPOSURE_NUMERIC.json').write_text(json.dumps(result,indent=2)+'\n')
