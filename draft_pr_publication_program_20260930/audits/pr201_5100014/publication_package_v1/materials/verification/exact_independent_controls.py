"""Independent direct line/foot constructions; no candidate imports or formulas."""
import sys, json
from pathlib import Path
import sympy as s

def need(condition, message):
    if condition is not True:
        raise RuntimeError(message)

def area(points):
    return s.simplify(sum(points[i][0]*points[(i+1)%len(points)][1]-points[i][1]*points[(i+1)%len(points)][0] for i in range(len(points)))/2)

def cross(p,q):
    return s.det(s.Matrix([list(p),list(q)]))

def direct(P, M):
    lines=[(x/4,y,s.Integer(1)) for x,y in P]
    out=[]; feet=[]
    for i,(nx,ny,h) in enumerate(lines):
        ax,ay,ah=lines[(i+1)%len(lines)]
        det=s.simplify(nx*ay-ny*ax)
        need(det != 0,'parallel consecutive outer tangents')
        out.append(((h*ay-ny*ah)/det,(nx*ah-h*ax)/det))
        k=s.simplify((h-nx*M[0]-ny*M[1])/(nx*nx+ny*ny))
        f=(s.simplify(M[0]+k*nx),s.simplify(M[1]+k*ny))
        need(s.simplify(nx*f[0]+ny*f[1]-h)==0,'foot off line')
        need(s.simplify(cross((f[0]-M[0],f[1]-M[1]),(nx,ny)))==0,'foot displacement not normal')
        feet.append(f)
    return area(out),area(feet),out,feet

def main():
    m,n=s.symbols('m n',real=True)
    R=s.Rational
    p0=[(2,0),(R(4,3),s.sqrt(5)/3),(-R(4,3),s.sqrt(5)/3),(-2,0),(-R(4,3),-s.sqrt(5)/3),(R(4,3),-s.sqrt(5)/3)]
    p1=[(0,1),(-4*s.sqrt(2)/3,R(1,3)),(-4*s.sqrt(2)/3,-R(1,3)),(0,-1),(4*s.sqrt(2)/3,-R(1,3)),(4*s.sqrt(2)/3,R(1,3))]
    records=[]
    for index,P in enumerate((p0,p1)):
        P=[tuple(map(s.sympify,p)) for p in P]
        for j,(x,y) in enumerate(P):
            need(s.simplify(x*x/4+y*y-1)==0,'boundary vertex not on ellipse')
            X,Y=P[(j+1)%6]
            nx,ny,h=y-Y,X-x,y*X-x*Y
            need(s.simplify(R(32,9)*nx*nx+R(5,9)*ny*ny-h*h)==0,'chord not tangent to confocal caustic')
        ap,am,outer,feet=direct(P,(m,n))
        product=s.factor(ap*am)
        need(s.simplify(product.subs({m:0,n:0})-40)==0,'origin product not 40')
        if records:
            need(s.simplify(product-s.sympify(records[0]['product'],locals={'m':m,'n':n}))==0,'two independent phase products disagree')
        rap,ram,_,_=direct(list(reversed(P)),(m,n))
        need(s.simplify(rap+ap)==0 and s.simplify(ram+am)==0,'signed reversal failed')
        tap,tam,_,_=direct(P*3,(m,n))
        need(s.simplify(tap-3*ap)==0 and s.simplify(tam-3*am)==0,'tripled traversal area failed')
        records.append({'phase':index,'outer_area':str(ap),'pedal_area':str(s.factor(am)),'product':str(product),'outer_vertices':[list(map(str,p)) for p in outer]})
    print(json.dumps({'status':'PASS','checks_enforced_with_explicit_exceptions':True,'optimization':sys.flags.optimize,'sympy_version':s.__version__,'records':records},indent=2))

if __name__=='__main__':
    main()
