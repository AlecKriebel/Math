"""Exact controls for the pentagonal-pencil calculation; no numeric inference."""
import sympy as S,json
checks=0
r=S.sqrt(5);l,X,Y,T,z,t,u,x,b,Z,W,v=S.symbols('l X Y T z t u x b Z W v')
phi=(1+r)/2;d=5+2*r;m=5-2*r;c=(11+5*r)/2

def ck(test):
 global checks
 assert test
 checks+=1

def equal(a,b=0):
 q=S.cancel(a-b,extension=r)
 ck(q==0)

def coeffzero(q,*vars):
 q=S.Poly(S.expand(q),*vars)
 for a in q.coeffs():equal(a)

# Independent multiplication of the five line equations over the cyclotomic field.
cyc=1+v+v**2+v**3+v**4;phiv=1+v+v**4
prod=S.prod(Z+v**(2*j+1)*W-(1+v)*v**j*T for j in range(5))
expected=Z**5+W**5+5*phiv*Z**2*W**2*T-5*phiv**3*Z*W*T**3+phiv**5*T**5
for a in S.Poly(S.expand(prod-expected),Z,W,T).coeffs():ck(S.rem(a,cyc,v)==0)

P=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X*X+Y*Y)**2*T-5*phi**3*(X*X+Y*Y)*T**3+phi**5*T**5
Q=X*X+Y*Y-T*T;G=P+l*T*Q**2
A=10*X+5*phi+l;B=-20*X**3+2*(5*phi+l)*X**2-5*phi**3-2*l
C=2*X**5+(5*phi+l)*X**4-(5*phi**3+2*l)*X**2+phi**5+l;h=4*X*X+2*X-1
coeffzero(G.subs(T,1)-(A*Y**4+B*Y*Y+C),X,Y,l)
a=40+20*r+8*l;bb=a+5
coeffzero(B*B-4*A*C-h*h*(20*X*X-a*X+bb),X,l)
equal(a*a-80*bb,64*l*(l+5*r))
xt=(bb-t*t)/(a+4*r*t);vt=2*r*xt+t
equal(vt*vt-(20*xt*xt-a*xt+bb))
alpha=1-r/5;gamma=2*r/5
F=z**3-((3+r)*l+40+20*r)*z*z+((60+36*r)*l+900+400*r)*z+(48+16*r)*l*l+(500+220*r)*l
Ut=m*z*z*F/(400*(z+gamma*l)**2*(z+alpha*l))
equal((h.subs(X,xt)*vt-B.subs(X,xt))/(2*A.subs(X,xt)),Ut.subs(z,t+5+2*r))
a0=m;a1=(-26+10*r)*l-20*r
a2=(42-86*r/5)*l*l+(-100+100*r)*l+500+200*r
a3=(-112+48*r)*l*l*(l+5*r)/5
coeffzero(m*F.subs(z,u-alpha*l)-(a0*u**3+a1*u*u+a2*u+a3),u,l)
equal(F.subs(z,-alpha*l),(-S.Rational(16,5)+16*r/25)*l*l*(l+5*r))
equal(S.discriminant(F,z),(24064+10752*r)*l*(l+5*r)**3*(l+c))
wa4=a1*a3;wa6=a0*a3*a3
b2=4*a2;b4=2*wa4;b6=4*wa6;b8=4*a2*wa6-wa4*wa4
Delta=-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
equal(Delta,2**24*(161-72*r)*l**5*(l+5*r)**5*(l+c))
# Origin and singular-fiber controls.
equal(S.diff(G,X).subs({X:0,Y:1,T:0}),10)
tO=-alpha*l-5-2*r
equal(xt.subs(t,tO),-(5*phi+l)/10)
conj=(1-r)/2
Pc=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*conj*(X*X+Y*Y)**2*T-5*conj**3*(X*X+Y*Y)*T**3+conj**5*T**5
coeffzero(G.subs(l,-5*r)-Pc,X,Y,T)
Fbad=S.Poly(S.expand(F.subs(l,-c)),z,extension=r)
ck(S.degree(S.gcd(Fbad,Fbad.diff()),z)==1)
nodeparam=-(25+10*r)/4
equal(S.diff(G.subs(T,1),X,2).subs({X:1,Y:0,l:nodeparam}),0)
equal(S.diff(G.subs(T,1),Y,2).subs({X:1,Y:0}),-50)
equal(S.diff(G.subs(T,1),X,3).subs({X:1,Y:0,l:nodeparam}),30)
ck(S.simplify(Delta.subs(l,nodeparam))!=0)
# An actual Tate isomorphism, rather than a j-only comparison.
beta=(11-5*r)*l/(2*(l+5*r));k=4*(l+5*r)/r;q=d*k*k
Tb=4*x**3+(b*b-6*b+1)*x*x+2*(b*b-b)*x+b*b
xi=q*(x-beta)
equal(xi**3+a2*xi*xi+wa4*xi+wa6-q**3*Tb.subs(b,beta)/4)
equal(a2,q*(beta*beta+6*beta+1)/4)
# Fifth-division polynomial and the two explicit quintic factors.
b2=b*b-6*b+1;b4=b*b-b;b6=b*b;b8=-b**3
p3=3*x**4+b2*x**3+3*b4*x*x+3*b6*x+b8
H6=2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x*x+(b2*b8-b4*b6)*x+b4*b8-b6*b6
co=[5,5*(b*b-5*b+1),b**4-7*b**3+44*b*b-38*b+1,b*(b**4+3*b**3-26*b*b+127*b-9),b*b*(b**4+3*b**3+19*b*b-248*b+36),b**3*(b**4+3*b**3-71*b*b+322*b-84),b**4*(b**4-12*b**3+94*b*b-293*b+126),5*b**5*(b**3-10*b*b+36*b-25),5*b**6*(2*b*b-13*b+16),10*b**7*(b-3),5*b**8]
R=sum(co[i]*x**(10-i) for i in range(11))
coeffzero(Tb*Tb*H6-p3**3-x*(x-b)*R,x,b)
Rp=x**5+((b*b-5*b+1)/2+r*(-b*b+11*b+1)/10)*x**4+(4*b*b-2*b+r*(b**3-11*b*b-b)/5)*x**3+((b**4-7*b**3+7*b*b)/2+r*(-b**4+11*b**3+b*b)/10)*x*x+(b**4-3*b**3)*x+b**4
Rm=Rp.xreplace({r:-r})
coeffzero(5*Rp*Rm-R,x,b)
# Direct modular cover identity and specialization to the plane parameter.
f=t**4+3*t**3+4*t*t+2*t+1;g=t**4-2*t**3+4*t*t-3*t+1
iota=lambda s:(c*s+1)/(s-c)
eps=lambda s:(phi*s+1)/(s-phi)
equal(iota(iota(t)),t);equal(eps(eps(t)),t)
equal(iota(eps(t)**5),t*f/g)
equal(iota(beta),-1/(l+c))
equal(d*(5-2*r),5)
# Exact finite-field falsification controls, separate from universal proof.
field_cases=point_cases=full_five_cases=cyclic_cases=plane_checks=0
for prime in [41,61,101]:
 inv=lambda a:pow(int(a)%prime,-1,prime)
 roots={}
 for yy in range(prime):roots.setdefault(yy*yy%prime,[]).append(yy)
 for rr in range(prime):
  if rr*rr%prime!=5:continue
  dd=(5+2*rr)%prime
  if dd not in roots:continue
  delta=roots[dd][0];ph=(1+rr)*inv(2)%prime;cc=pow(ph,5,prime)
  for ll in range(prime):
   if ll in [0,(-5*rr)%prime,(-cc)%prime]:continue
   be=(11-5*rr)*ll*inv(2*(ll+5*rr))%prime
   aa=(be*be-6*be+1)*inv(4)%prime;ab=(be*be-be)*inv(2)%prime;ac=be*be*inv(4)%prime
   kval=4*(ll+5*rr)*inv(rr)%prime;qval=dd*kval*kval%prime
   a0v=(5-2*rr)%prime;a1v=((-26+10*rr)*ll-20*rr)%prime
   a2v=((42-86*rr*inv(5))*ll*ll+(-100+100*rr)*ll+500+200*rr)%prime
   a3v=(-112+48*rr)*ll*ll*(ll+5*rr)*inv(5)%prime
   al=(1-rr*inv(5))%prime;gam=2*rr*inv(5)%prime
   def add(P,Q):
    if P is None:return Q
    if Q is None:return P
    x1,y1=P;x2,y2=Q
    if x1==x2 and (y1+y2)%prime==0:return None
    slope=((3*x1*x1+2*aa*x1+ab)*inv(2*y1) if P==Q else (y2-y1)*inv(x2-x1))%prime
    x3=(slope*slope-aa-x1-x2)%prime;y3=(-y1+slope*(x1-x3))%prime
    return x3,y3
   def mul5(P):return add(add(add(P,P),add(P,P)),P)
   n5=1
   Rfunc=S.Poly(R,x,b)
   def evalR(xx):
    val=0
    for (ix,ib),vv in Rfunc.terms():val+=int(vv)*pow(xx,ix,prime)*pow(be,ib,prime)
    return val%prime
   for xx in range(prime):
    rhs=(xx**3+aa*xx*xx+ab*xx+ac)%prime
    for yy in roots.get(rhs,[]):
     Pp=(xx,yy);is5=mul5(Pp) is None
     ck(is5==(xx*(xx-be)*evalR(xx)%prime==0));point_cases+=1
     if is5:n5+=1
     xiv=qval*(xx-be)%prime;etav=pow(kval*delta,3,prime)*yy%prime
     ck((etav*etav-xiv**3-a2v*xiv*xiv-a1v*a3v*xiv-a0v*a3v*a3v)%prime==0)
     if xiv==0:continue
     sv=a3v*inv(xiv)%prime;zv=(sv-al*ll)%prime;tv=(zv-5-2*rr)%prime
     av=(40+20*rr+8*ll)%prime;bv=(av+5)%prime
     den=(av+4*rr*tv)%prime;denY=20*xiv*(zv+gam*ll)%prime
     if not den or not denY:continue
     xp=(bv-tv*tv)*inv(den)%prime;yp=etav*zv*inv(denY)%prime
     rho=(xp*xp+yp*yp)%prime
     poly=2*(xp**5-10*xp**3*yp*yp+5*xp*yp**4)+5*ph*rho*rho-5*pow(ph,3,prime)*rho+pow(ph,5,prime)+ll*(rho-1)**2
     ck(poly%prime==0);plane_checks+=1
   fifth=pow((ll+cc)%prime,(prime-1)//5,prime)==1
   ck(n5==(25 if fifth else 5));field_cases+=1
   if fifth:full_five_cases+=1
   else:cyclic_cases+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_field_fibers':field_cases,'enumerated_affine_points':point_cases,'inverse_plane_checks':plane_checks,'full_5_torsion_fibers':full_five_cases,'cyclic_5_torsion_fibers':cyclic_cases,'scope':'Symbolic polynomial identities and finite-field controls supplement the universal proof and credited full-level modular input; they are not a standalone proof of the number-field assertion.'},indent=2))
