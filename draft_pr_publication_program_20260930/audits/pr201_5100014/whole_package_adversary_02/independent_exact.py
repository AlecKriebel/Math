"""Fresh algebra checks from definitions; explicit exceptions survive -O."""
import sympy as s,json,sys
from datetime import datetime,timezone
false='--false-identity' in sys.argv
checks=[]
def need(c,m):
    if c is not True:raise RuntimeError(m)
    checks.append(m)
def eq(x,y,m):need(s.simplify(x-y)==0,m)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return s.simplify(sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2)
def geom(p,M):
    ns=[(x/4,y) for x,y in p];V=[];Q=[]
    for i,n in enumerate(ns):
        v=ns[(i+1)%len(p)];d=det(n,v)
        need(s.simplify(d)!=0,'outer tangent intersection finite')
        V.append(((v[1]-n[1])/d,(n[0]-v[0])/d))
        f=tuple(s.simplify(M[j]+(1-dot(n,M))*n[j]/dot(n,n)) for j in range(2))
        eq(dot(n,f),1,'foot incidence');eq(det(tuple(f[j]-M[j] for j in range(2)),n),0,'perpendicular foot')
        Q.append(f)
    return area(p),area(V),area(Q)
a,b,l=s.symbols('a b l',positive=True);c=a*a-b*b
x2=a**4/c;y2=-b**4/c
expr=x2/(a*a-l)+y2/(b*b-l)-1
eq(expr,-l*l/((a*a-l)*(b*b-l)),'contact is not branch point')
eq((a*a-l)/a**2-(b*b-l)/b**2,l*(1/b**2-1/a**2),'infinity not common tangent')
eq(-(a*a-l)/a**2+(b*b-l)/b**2,l*(1/a**2-1/b**2),'origin tangent transverse E intersection')
# Complete modular classification and boundary m=3; symbolic proof in derivation.
for m in range(3,100,2):
    N=2*m
    need({j for j in range(N) if 2*j%N==0}=={0,m},'exhaustive sigma fixed shifts')
    need(not any(2*j%N==1 for j in range(N)),'no mixed involution fixed orbit')
    need({i for i in (0,1,m,m+1) if (i+1)%N in {0,1,m,m+1}}=={0,m},'all adjacent singular pairs')
    need(2*((1-m)//2)%N==(1-m)%N,'pedal orbit infinity shift')
    need(2*((m-1)//2)%N==(m-1)%N and 2*((m+1)//2)%N==(m+1)%N,'both AA-prime palindrome shifts')
for m in range(2,100,2):need(not any((2*k-1+m)%(2*m)==0 for k in range(2*m)),'excluded even-half-period congruence fails')
# Same contact means no double pole without assuming residue equality.
r1,r2,nx,ny=s.symbols('r1 r2 nx ny');eq(det((r1*nx,r1*ny),(r2*nx,r2*ny)),0,'arbitrary parallel residues cancel')
u,v=s.symbols('u v',real=True);r=s.sqrt(5);R=s.Rational
H=[(s.Integer(2),s.Integer(0)),(R(4,3),r/3),(-R(4,3),r/3),(-s.Integer(2),s.Integer(0)),(-R(4,3),-r/3),(R(4,3),-r/3)]
A,Ap,B=geom(H,(u,v));target=(s.Integer(41) if false else s.Integer(40))*(1+(u*u+v*v)/9)
eq(Ap*B,target,'N6 target product identity (deliberately false 41 when requested)')
rA,rAp,rB=geom(H[::-1],(u,v));eq(A+rA,0,'original reversal');eq(Ap+rAp,0,'outer reversal');eq(B+rB,0,'pedal reversal')
# Displayed repeated-triangle control: independently test unit reflection and strict contact.
d=s.sqrt(13);alpha=2*(d-1)/3;beta=(4-d)/3;gamma=s.sqrt(2*d-5);lam=4*(2*d-5)/9
tris=[[(s.Integer(2),s.Integer(0)),(-alpha,gamma/3),(-alpha,-gamma/3)],[(s.Integer(0),s.Integer(1)),(-4*gamma/3,-beta),(4*gamma/3,-beta)]]
products=[]
for P in tris:
    for i,p in enumerate(P):
        q=P[(i+1)%3];prev=P[i-1]
        eq(p[0]**2/4+p[1]**2,1,'triangle boundary')
        n=(p[1]-q[1],q[0]-p[0]);h=dot(n,p)
        eq((4-lam)*n[0]**2+(1-lam)*n[1]**2,h*h,'triangle confocal tangency')
        ca=(s.simplify((4-lam)*n[0]/h),s.simplify((1-lam)*n[1]/h))
        direction=tuple(q[j]-p[j] for j in range(2));t=s.simplify(dot(tuple(ca[j]-p[j] for j in range(2)),direction)/dot(direction,direction))
        need(t.is_positive is True and s.simplify(1-t).is_positive is True,'strict caustic contact in chord')
        inc=tuple(s.simplify(p[j]-prev[j]) for j in range(2));out=direction
        ni=s.sqrt(dot(inc,inc));no=s.sqrt(dot(out,out));inc=tuple(s.simplify(z/ni) for z in inc);out=tuple(s.simplify(z/no) for z in out);normal=(p[0]/4,p[1])
        reflected=tuple(s.simplify(inc[j]-2*dot(inc,normal)*normal[j]/dot(normal,normal)) for j in range(2))
        for j in range(2):eq(reflected[j],out[j],'triangle direct specular reflection')
    _,ap,bm=geom(P*2,(s.Integer(1),s.Integer(0)));products.append(s.simplify(ap*bm))
eq(products[0],(1166+322*d)/9,'horizontal repeated triangle printed constant')
eq(products[1],(956+244*d)/9,'vertical repeated triangle printed constant')
need(s.simplify(products[0]-products[1]).is_positive is True,'excluded repeated triangle products differ')
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','optimization':sys.flags.optimize,'checks':len(checks),'independent_hexagon_product':str(s.factor(Ap*B)),'repeated_triangle_products':list(map(str,products)),'scope':'Exact finite geometry/algebra controls; written derivation handles universal claim.'},indent=2))
