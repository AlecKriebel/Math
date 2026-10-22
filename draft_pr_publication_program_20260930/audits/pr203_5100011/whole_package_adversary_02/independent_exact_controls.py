from pathlib import Path
from datetime import datetime,timezone
import json,sys
import sympy as s
O=Path(__file__).resolve().parent
checks=[]
def req(x,n):
 if x is not True and x is not s.true:raise RuntimeError(n+': '+str(x))
 checks.append(n)
def zero(x,n):req(s.simplify(x)==0,n)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return s.simplify(sum(det(x,y) for x,y in zip(p,p[1:]+p[:1]))/2)
def foot(p,q,M):
 d=q-p;return s.simplify(p+d*((M-p).dot(d))/d.dot(d))
def pedals(p,M):return [foot(x,y,M) for x,y in zip(p,p[1:]+p[:1])]
a,b,l,u,v,w,e=s.symbols('a b l u v w eta',nonzero=True,real=True)
H=a*a*u*u+b*b*v*v;D=u*u+v*v
X=-a*a*u*w-v*e;Y=-b*b*v*w+u*e
zero(u*X+v*Y+w*H,'generic endpoint incidence')
expr=s.expand(b*b*X*X+a*a*Y*Y-a*a*b*b*H*H)
expr=expr.subs(e*e,a*a*b*b*l*D).subs(w*w,H-l*D)
zero(expr,'generic endpoint conic on discriminant cover')
z=s.symbols('z',real=True)
normal=a*a*(a*a-l)*z+b*b*(b*b-l)*(1-z)-(a*a-b*b)**2*z*(1-z)
zero(normal-(a*a*z+b*b*(1-z))*(a*a*z+b*b*(1-z)-l),'normal-incidence factorization')
v0=2*s.I;w0=s.sqrt(s.Rational(12,5));y0=(4-w0*w0)/(2*w0*v0);x0=-w0-v0*y0
zero(x0*x0/4+y0*y0-1,'H0 finite endpoint lies on ellipse')
zero(x0+v0*y0+w0,'H0 finite endpoint incidence')
req(2*w0*v0/4!=0,'H0 direct equation has nonzero linear coefficient')
req(s.simplify(2*w0*v0/4)!=0,'H0 infinity root is simple')
t=s.symbols('t');vv=s.I*s.sqrt(1-5*t*t/16);ww=s.sqrt(3+t*t/16);dd=5*t*t/16
for M,tag,special in [(s.Matrix([1,2]),'generic',False),(s.Matrix([-s.sqrt(3),0]),'focal',True)]:
 Q=M-(M[0]+vv*M[1]+ww)/dd*s.Matrix([1,vv])
 for k,c in enumerate(Q):
  zero(s.simplify(c.subs(t,-t)-c),tag+' foot even '+str(k))
  lead=s.limit(t*t*c,t,0)
  if special:zero(lead,tag+' canceled double pole '+str(k));req(s.limit(c,t,0).is_finite is True,tag+' regular '+str(k))
  else:req(lead!=0,tag+' actual double pole '+str(k))
M=s.Matrix(s.symbols('Mx My',real=True));raw=[(s.Matrix([1,2]),s.Rational(3,2)),(s.Matrix([-2,5]),s.Rational(-4,3)),(s.Matrix([3,-1]),s.Rational(7,5)),(s.Matrix([-4,-3]),s.Rational(2,7)),(s.Matrix([5,1]),s.Rational(-9,2)),(s.Matrix([2,-7]),s.Rational(5,3))]
def line_area(lines,M):return area([M+(h-n.dot(M))*n/n.dot(n) for n,h in lines])
B=line_area(raw,M);poly=s.Poly(B,*M)
zero(poly.coeff_monomial(M[0]*M[1]),'six arbitrary lines no mixed quadratic')
zero(poly.coeff_monomial(M[0]**2)-poly.coeff_monomial(M[1]**2),'six arbitrary lines equal radial coefficients')
C=sum(det(n,m)*n.dot(m)/(n.dot(n)*m.dot(m)) for (n,h),(m,k) in zip(raw,raw[1:]+raw[:1]))/4
zero(poly.coeff_monomial(M[0]**2)-C,'six arbitrary lines independent quadratic coefficient')
zero(line_area([(n*(-1 if j%2 else 1),h*(-1 if j%2 else 1)) for j,(n,h) in enumerate(raw)],M)-B,'line normal signs immaterial')
a0=4*s.sqrt(2);b0=3*s.sqrt(3)
W=[s.Matrix(p) for p in [(a0,0),(4*a0/5,3*b0/5),(0,b0),(-4*a0/5,3*b0/5),(-a0,0),(-4*a0/5,-3*b0/5),(0,-b0),(4*a0/5,-3*b0/5)]]
P=[W[3*j%8] for j in range(8)];Ap=area(P);Bp=area(pedals(P,M))
zero(Ap-168*s.sqrt(6)/5,'star A')
zero(Bp-96*s.sqrt(6)/245*(13-M.dot(M)),'star all-M pedal polynomial')
zero(Ap*Bp-s.Rational(13824,175)*(13-M.dot(M)),'star all-M product')
feet=pedals(P,s.Matrix([s.sqrt(13),0]));zero(area(feet),'star zero pedal')
req(s.simplify(det(feet[1]-feet[0],feet[2]-feet[0]))!=0,'zero pedal feet not collinear')
req(Bp.subs({M[0]:4,M[1]:0}).is_negative is True,'star negative pedal')
zero(area(P[::-1])+Ap,'star reversed A')
zero(area(pedals(P[::-1],M))+Bp,'star reversed B all-M')
R=s.Rational
H6=[s.Matrix(p) for p in [(2,0),(R(4,3),s.sqrt(5)/3),(-R(4,3),s.sqrt(5)/3),(-2,0),(-R(4,3),-s.sqrt(5)/3),(R(4,3),-s.sqrt(5)/3)]]
J6=[s.Matrix(p) for p in [(0,1),(-4*s.sqrt(2)/3,R(1,3)),(-4*s.sqrt(2)/3,-R(1,3)),(0,-1),(4*s.sqrt(2)/3,-R(1,3)),(4*s.sqrt(2)/3,R(1,3))]]
vals=[]
for P,want,tag in [(H6,R(14000,729),'H'),(J6,R(14336,729),'J')]:
 val=area(P)*area(pedals(P,s.zeros(2,1)));zero(val-want,tag+' N6 exact product');vals.append(val)
 zero(area(P*2)*area(pedals(P*2,s.zeros(2,1)))-4*val,tag+' doubled list scales product by four')
zero(4*(vals[1]-vals[0])-R(448,243),'nominal12 products have exact nonzero difference')
U=s.Matrix([3,1]);V=s.Matrix([-1,2]);P=[U,V,-U,-V]
expected=8*det(U,V)**4/((V-U).dot(V-U)*(V+U).dot(V+U))
zero(area(P)*area(pedals(P,M))-expected,'rational parallelogram all-M distance product formula')
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','optimization':sys.flags.optimize,'check_count':len(checks),'passed':checks,'limitations':'Focused exact symbolic controls, not a universal proof or finite-sweep replacement.'}
(O/('INDEPENDENT_EXACT_OPT.json' if sys.flags.optimize else 'INDEPENDENT_EXACT.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
