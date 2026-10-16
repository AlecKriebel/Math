"""Independent physical-variable identities and exact Euclidean 4/8 certificates.
No assertions, elliptic functions, author imports, or numerical fits. All orbit
arithmetic is over QQ or a real quadratic field. Ordinary products are positive.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"runtime_packages"))
import sympy as s
import json
ROOT=Path(__file__).resolve().parent
checks=[]
def check(label,test):
    if not test: raise RuntimeError("exact check failed: "+label)
    checks.append(label)
A,B,L,S=s.symbols("A B L S")
C=A-B;U=A**2/(A-L);V=B**2/(B-L)
H=(V+C+(U-V)*S)**2-4*C*U*S
fact=(1-C*S/(A-L))*((V+C)**2-(A-L)*(U-V)**2*S/C)
check("physical paired focal-distance factorization",s.cancel(H-fact)==0)
check("outer locus axes difference",s.cancel(U-V-C*(A*B-L*(A+B))/((A-L)*(B-L)))==0)
check("N4 circle locus",s.simplify((U-V).subs(L,A*B/(A+B)))==0)
check("N4 radius squared",s.simplify(U.subs(L,A*B/(A+B))-(A+B))==0)
ss,zz,hh,cv,dv,du,kap=s.symbols("ss zz hh cv dv du kap")
den=1-kap*ss*ss*hh*hh
sp=(ss*cv*dv+hh*zz*du)/den
sm=(ss*cv*dv-hh*zz*du)/den
cp=(zz*cv-ss*hh*du*dv)/den
cm=(zz*cv+ss*hh*du*dv)/den
def addreduce(expression):
    return s.cancel(s.expand(expression).subs(dv**2,1-kap*hh**2).subs(zz**2,1-ss**2))
check("independent canonical chord plus endpoint",addreduce((dv*ss*sp+zz*cp-cv)*den)==0)
check("independent canonical chord minus endpoint",addreduce((dv*ss*sm+zz*cm-cv)*den)==0)
check("independent canonical orientation determinant",addreduce((sp*cm-sm*cp-2*hh*cv*du/den)*den**2)==0)
check("independent canonical caustic coefficient",s.cancel((A-L)*(1-(A-B)*L/(B*(A-L)))/A-(B-L)/B)==0)
x,y,r=s.symbols("x y r")
D=B*x*x+A*y*y
def reduce_n4(poly):
    result=s.rem(s.expand(poly),r*r-A*A*y*y-B*B*x*x,r)
    return s.rem(s.expand(result),x*x+y*y-1,x)
q0x=B*x-r*y;q0y=r*x+A*y
q1x=-B*x-r*y;q1y=r*x-A*y
check("universal N4 outer circle by coefficient reduction",
      reduce_n4(A*q0x*q0x+B*q0y*q0y-(A+B)*D*D)==0)
dx=-A*y-r*x;dy=B*x-r*y
check("universal N4 chord tangency by coefficient reduction",
      reduce_n4(B*dy*dy+A*dx*dx-(A+B)*(x*dx+y*dy)**2)==0)
check("universal N4 ordinary product square by coefficient reduction",
      reduce_n4((A*D*D-C*q0x*q0x)*(A*D*D-C*q1x*q1x)-B*B*D**4)==0)

def exact_orbit(A0,B0,L0,p0,V0,period,name):
    """Normalized p=(x/a,y/b), d=(dx/a,dy/b), Euclidean reflection."""
    extensions=[r for r in V0.atoms(s.Pow) if r.exp==s.Rational(1,2)]
    K=s.QQ.algebraic_field(*extensions) if extensions else s.QQ
    cv=lambda x:K.from_sympy(s.sympify(x))
    out=lambda x:s.sstr(K.to_sympy(x))
    aa,bb,ll=cv(A0),cv(B0),cv(L0)
    p=(cv(p0[0]),cv(p0[1]));d=(cv(-1),cv(V0))
    z=K.zero;one=K.one
    def dot(x,y):return x[0]*y[0]+x[1]*y[1]
    def reflect(d,p):
        f=2*dot(d,p)/(p[0]*p[0]/aa+p[1]*p[1]/bb)
        return (d[0]-f*p[0]/aa,d[1]-f*p[1]/bb)
    points=[p]
    for j in range(period):
        t=-2*dot(p,d)/dot(d,d)
        q=(p[0]+t*d[0],p[1]+t*d[1])
        check(name+":outer:"+str(j),dot(q,q)==one)
        check(name+":tangency:"+str(j),aa*bb*dot(p,d)**2==ll*(bb*d[1]**2+aa*d[0]**2))
        check(name+":positive hit:"+str(j),s.sign(K.to_sympy(t))==1)
        points.append(q);d=reflect(d,q);p=q
    check(name+":closure",points[-1]==points[0])
    check(name+":primitive",len(set(points[:-1]))==period)
    outer=[]
    for j in range(period):
        p,q=points[j],points[j+1];det=p[0]*q[1]-p[1]*q[0]
        check(name+":finite outer:"+str(j),det!=z)
        w=((q[1]-p[1])/det,(p[0]-q[0])/det)
        check(name+":tangent 1:"+str(j),dot(w,p)==one)
        check(name+":tangent 2:"+str(j),dot(w,q)==one)
        check(name+":locus:"+str(j),(aa-ll)*w[0]**2/aa+(bb-ll)*w[1]**2/bb==one)
        outer.append(w)
    product_square=one
    for j in range(period//2):
        x,y=outer[j]
        check(name+":antipodal:"+str(j),outer[j+period//2]==(-x,-y))
        product_square*=((aa*x*x+bb*y*y+aa-bb)**2-4*(aa-bb)*aa*x*x)
    expected=s.Rational(3200,3)**2 if period==8 else (4*A0*B0)**2
    check(name+":ordinary focal product square",product_square==cv(expected))
    return {"name":name,"A":str(A0),"B":str(B0),"lambda":str(L0),
            "normalized_start":[str(v) for v in p0],"normalized_initial_direction":["-1",str(V0)],
            "number_field":str(K),"period":period,
            "normalized_vertices":[[out(v) for v in p] for p in points],
            "normalized_outer_vertices":[[out(v) for v in p] for p in outer],
            "exact_product_square":out(product_square),
            "ordinary_positive_product":str(s.sqrt(expected))}

def initial_slope(A0,B0,L0,x,y):
    v=s.symbols("v")
    f=s.expand(L0*(B0*v*v+A0)-A0*B0*(-x+y*v)**2)
    roots=s.solve(f,v)
    chosen=[r for r in roots if s.sign(-x+y*r)==-1 and s.sign(x*r+y)==1]
    check("unique inward counterclockwise tangent at "+str((A0,B0,L0,x,y)),len(chosen)==1)
    return chosen[0]
records=[]
for A0,B0,L0,N,phase,name in [
    (s.Rational(8),s.Rational(3),s.Rational(24,35),8,(s.Rational(1),s.Rational(0)),"N8_axis"),
    (s.Rational(8),s.Rational(3),s.Rational(24,35),8,(s.Rational(3,5),s.Rational(4,5)),"N8_generic"),
    (s.Rational(9),s.Rational(4),s.Rational(36,13),4,(s.Rational(1),s.Rational(0)),"N4_axis"),
    (s.Rational(9),s.Rational(4),s.Rational(36,13),4,(s.Rational(3,5),s.Rational(4,5)),"N4_generic")]:
    slope=initial_slope(A0,B0,L0,*phase)
    records.append(exact_orbit(A0,B0,L0,phase,slope,N,name))
summary={"status":"PASS","mechanism":"Exact normalized Euclidean reflection and line tangency, not Jacobi parametrization",
         "checks":len(checks),"labels":checks,
         "physical_factorization":"H=(1-(A-B)S/(A-lambda))*((V+A-B)^2-(A-lambda)(U-V)^2*S/(A-B)), U=A^2/(A-lambda), V=B^2/(B-lambda)",
         "records":records}
(ROOT/"exact_certificates.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
