#!/usr/bin/env python3
"""Exact direct-geometric controls, no assertions stripped by optimization."""
import sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'pr200_5100007/math_algebra_family_01/runtime_packages'))
import sympy as S

def need(c,msg):
    if c is not True:
        raise RuntimeError(msg)
def simp(x):return S.simplify(x)
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def area(p):return simp(sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2)
def quantities(a2,b2,p,m):
    a2,b2=S.sympify(a2),S.sympify(b2)
    p=[tuple(map(S.sympify,q)) for q in p];m=tuple(map(S.sympify,m))
    ns=[(x/a2,y/b2) for x,y in p]; feet=[]; outer=[]
    for i,n in enumerate(ns):
        v=ns[(i+1)%len(ns)]; d=simp(cross(n,v)); need(d!=0,'parallel tangents')
        outer.append(tuple(simp(x/d) for x in (v[1]-n[1],n[0]-v[0])))
        h=simp((1-dot(n,m))/dot(n,n));feet.append(tuple(simp(m[j]+h*n[j]) for j in range(2)))
    answer=(area(outer),area(feet))
    for z in answer:need(len(z.atoms(S.Float))==0,'unexpected floating point in exact geometry')
    return answer

def caustic_checks(a2,b2,lam,p):
    a2,b2,lam=map(S.sympify,(a2,b2,lam))
    p=[tuple(map(S.sympify,q)) for q in p]
    for i,(x,y) in enumerate(p):
        need(simp(x*x/a2+y*y/b2-1)==0,'boundary')
        q=p[(i+1)%len(p)];n=(q[1]-y,x-q[0]);h=simp(dot(n,(x,y)))
        need(simp((a2-lam)*n[0]**2+(b2-lam)*n[1]**2-h*h)==0,'caustic tangency')
    # Equal-J signed normal component, hence specular reflection.
    js=[]
    for i,(x,y) in enumerate(p):
        q=p[(i+1)%len(p)];v=(q[0]-x,q[1]-y);le=S.sqrt(dot(v,v));js.append(simp(-(x*v[0]/a2+y*v[1]/b2)/le))
    for j in js:need(simp(j-S.sqrt(lam/(a2*b2)))==0,'equal Joachimsthal value')
    for i,point in enumerate(p):
        prev=p[(i-1)%len(p)];nxt=p[(i+1)%len(p)]
        incoming=tuple(simp(point[j]-prev[j]) for j in range(2));outgoing=tuple(simp(nxt[j]-point[j]) for j in range(2))
        lin,lout=S.sqrt(dot(incoming,incoming)),S.sqrt(dot(outgoing,outgoing))
        incoming=tuple(simp(z/lin) for z in incoming);outgoing=tuple(simp(z/lout) for z in outgoing)
        nn=(point[0]/a2,point[1]/b2);factor=simp(2*dot(incoming,nn)/dot(nn,nn))
        for j in range(2):need(simp(incoming[j]-factor*nn[j]-outgoing[j])==0,'direct specular reflection')

def run():
    a,b=S.sqrt(15),S.sqrt(7);lam=S.Rational(105,16)
    pH=[(a,0),(-3*a/4,S.Rational(7,4)),(-3*a/4,-S.Rational(7,4))]
    pV=[(0,b),(-S.Rational(15,4),-b/4),(S.Rational(15,4),-b/4)]
    m=(S.Integer(1),S.Integer(0));out=[]
    for name,p in [('horizontal',pH),('vertical',pV)]:
        caustic_checks(15,7,lam,p)
        aa,bb=quantities(15,7,p,m);aa6,bb6=quantities(15,7,p+p,m)
        need(simp(aa6-2*aa)==0,'repeat outer area scaling');need(simp(bb6-2*bb)==0,'repeat pedal area scaling')
        out.append(dict(case=name,lambda_=str(lam),primitive_period=3,listed_period=6,M=['1','0'],A_outer=str(aa),A_pedal=str(bb),primitive_product=str(simp(aa*bb)),repeated_product=str(simp(aa6*bb6))))
    need(simp(S.sympify(out[0]['repeated_product'])-S.sympify(out[1]['repeated_product']))!=0,'expected repeated-odd-period obstruction disappeared')
    # Strict nesting alone is insufficient: affine-regular hexagons on a
    # nonconfocal homothetic pair provide exact unequal products.
    nonconfocal=[]
    for phase in (S.Integer(0),S.pi/6):
        p=[(2*S.cos(phase+i*S.pi/3),S.sin(phase+i*S.pi/3)) for i in range(6)]
        for i,(x,y) in enumerate(p):
            q=p[(i+1)%6];nn=(q[1]-y,x-q[0]);hh=dot(nn,(x,y))
            need(simp(3*nn[0]**2+S.Rational(3,4)*nn[1]**2-hh**2)==0,'homothetic caustic tangency')
        aa,bb=quantities(4,1,p,(0,0));nonconfocal.append(simp(aa*bb))
    need(simp(nonconfocal[0]-nonconfocal[1])!=0,'nonconfocal obstruction disappeared')
    out.append(dict(case='nonconfocal affine-regular hexagons',outer_squared_axes=['4','1'],inner_squared_axes=['3','3/4'],products=[str(z) for z in nonconfocal]))
    # Exact N6 axis orbit and its complete arbitrary-M pedal polynomial.
    a2,b2=4,1;root=S.sqrt(5);p=[(S.Integer(2),0),(S.Rational(4,3),root/3),(-S.Rational(4,3),root/3),(-S.Integer(2),0),(-S.Rational(4,3),-root/3),(S.Rational(4,3),-root/3)]
    caustic_checks(a2,b2,S.Rational(4,9),p)
    u,v=S.symbols('u v',real=True);aa,bb=quantities(a2,b2,p,(u,v));prod=simp(aa*bb)
    need(simp(prod-S.Rational(40,9)*(u*u+v*v+9))==0,'N6 exact axis polynomial')
    out.append(dict(case='N6 axis',A_outer=str(aa),A_pedal=str(bb),product=str(prod)))
    # Universal conic invariant-density algebra, independent of candidate pole proof.
    aa,bb,ll=S.symbols('aa bb ll');PP=aa*bb;cc=aa-bb
    al,be,ga=PP-ll*cc,PP+ll*cc,PP-ll*(aa+bb)
    need(S.expand(al*al-ga*ga-4*ll*PP*(bb-ll))==0,'invariant density cosine coefficient')
    need(S.expand(be*be-ga*ga-4*ll*PP*(aa-ll))==0,'invariant density sine coefficient')
    # Exact symbolic coefficient of general pedal quadratic from angle variables.
    x,y=S.symbols('x y', real=True)
    identity=simp(S.cos(x)*S.cos(y)*S.sin(y-x)-(S.sin(2*(y-x))+S.sin(2*y)-S.sin(2*x))/4)
    need(S.trigsimp(identity)==0,'quadratic telescoping trig identity')
    return out

if __name__=='__main__':print(json.dumps({'label':'exact symbolic controls; finite cases do not prove phase invariance','checks':run()},indent=2))
