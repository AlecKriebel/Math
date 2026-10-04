#!/usr/bin/env python3
"""Independent reconstruction of the candidate geometry. No candidate imports."""
import hashlib
import pathlib
import sys
import sympy as S

X,Y,T,L,r,z,s,t,x,u,v = S.symbols('X Y T L r z s t x u v')
phi=(1+r)/2
c=(11+5*r)/2
d=5+2*r
m=5-2*r
alpha=1-r/5
gamma=2*r/5
def red(p):
    return S.Poly(S.expand(p),r).rem(S.Poly(r*r-5,r)).as_expr().expand()
def eqzero(p):
    return red(S.together(p).as_numer_denom()[0]) == 0
checks=[]
def check(label,p,expected=True):
    result=eqzero(p)
    checks.append((label,result,expected))
    print(('PASS ' if result==expected else 'FAIL ')+label+'; vanishes='+str(result), flush=True)
    if result!=expected:
        print('NONZERO NUMERATOR '+str(red(S.together(p).as_numer_denom()[0])), flush=True)
P=red(2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X**2+Y**2)**2*T-5*phi**3*(X**2+Y**2)*T**3+c*T**5)
Q=X**2+Y**2-T**2
G=red((P+L*T*Q**2).subs(T,1))
A=S.Poly(G,Y).coeff_monomial(Y**4)
B=S.Poly(G,Y).coeff_monomial(Y**2)
C=S.Poly(G,Y).coeff_monomial(1)
print('RECONSTRUCTED A,B,C',A,B,C,flush=True)
h=4*X**2+2*X-1
a=40+20*r+8*L
b=a+5
D=red(B**2-4*A*C)
check('quartic discriminant factorization',D-h**2*(20*X**2-a*X+b))
check('negative control changed conic constant',D-h**2*(20*X**2-a*X+b+1),False)
check('conic discriminant',a**2-80*b-64*L*(L+5*r))
t_forward=(2*A*Y**2+B)/h-2*r*X
check('forward recovery X identity',b-t_forward**2-X*(a+4*r*t_forward)+4*A*G/h**2)
x_of_t=(b-t*t)/(a+4*r*t)
check('conic parameterization',(t+2*r*x_of_t)**2-(20*x_of_t*x_of_t-a*x_of_t+b))
F=z**3-((3+r)*L+40+20*r)*z**2+((60+36*r)*L+900+400*r)*z+(48+16*r)*L**2+(500+220*r)*L
Y2=(h*(t+2*r*X)-B)/(2*A)
Y2z=Y2.subs(X,x_of_t).subs(t,z-d)
target_Y2=m*z*z*F/(400*(z+gamma*L)**2*(z+alpha*L))
check('rational second square root',Y2z-target_Y2)
check('negative control removed z square',Y2z-m*z*F/(400*(z+gamma*L)**2*(z+alpha*L)),False)
derived_coeffs=[red(S.Poly(red(m*F.subs(z,s-alpha*L)),s).coeff_monomial(s**j)) for j in [3,2,1,0]]
a0=m
a1=(-26+10*r)*L-20*r
a2=(42-86*r/5)*L**2+(-100+100*r)*L+500+200*r
a3=(-112+48*r)*L**2*(L+5*r)/5
for j,(got,want) in enumerate(zip(derived_coeffs,[a0,a1,a2,a3])):
    check('independently expanded coefficient a'+str(j),got-want)
print('DERIVED COEFFICIENTS',derived_coeffs,flush=True)
check('F value at s=0',F.subs(z,-alpha*L)-(-S.Rational(16,5)+16*r/25)*L**2*(L+5*r))
discF=red(S.discriminant(F,z))
check('F discriminant',discF-(24064+10752*r)*L*(L+5*r)**3*(L+c))
xi=S.symbols('xi')
W=xi**3+a2*xi**2+a1*a3*xi+a0*a3*a3
discW=red(16*S.discriminant(W,xi))
check('Weierstrass discriminant',discW-2**24*(161-72*r)*L**5*(L+5*r)**5*(L+c))
X0=-(5*phi+L)/10
check('vertical B at A root',B.subs(X,X0)-L*(L+5*r)*(L+5*(phi+1))/25)
check('vertical exceptional X=1/2',X0.subs(L,-5*(phi+1))-S.Rational(1,2))
check('vertical exceptional C=-1',C.subs({L:-5*(phi+1),X:S.Rational(1,2)})+1)
Fm=red(F.subs({z:s-alpha*L,L:-c}))
Fm=red(F.subs(z,s-alpha*L).subs(L,-c))
Fmrad=Fm.subs(r,S.sqrt(5))
gcdF=S.gcd(S.Poly(Fmrad,s,extension=S.sqrt(5)),S.Poly(S.diff(Fmrad,s),s,extension=S.sqrt(5))).monic().as_expr()
check('excluded minus-c gcd',gcdF-(s-1-3*S.sqrt(5)/5))
print('EXCLUDED -c F(s)',S.factor(Fmrad,extension=S.sqrt(5)),flush=True)
print('EXCLUDED -c branch pole numerator',red(Fm.subs(s,0)),flush=True)
print('EXCLUDED -c conic discriminant',red((a*a-80*b).subs(L,-c)),flush=True)
Pconj=red(2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*(1-r)/2*(X**2+Y**2)**2*T-5*((1-r)/2)**3*(X**2+Y**2)*T**3+((1-r)/2)**5*T**5)
check('minus-5r conjugate side product',P-5*r*T*Q**2-Pconj)
local=red(G.subs({X:1+u,Y:v}))
local2=red(sum(term for term in S.Add.make_args(local) if S.Poly(term,u,v).total_degree()==2))
# Extract homogeneous local jets without assuming any coordinates simplify.
scale=S.symbols('scale')
localjet=S.Poly(local.subs({u:scale*u,v:scale*v}),scale)
local2=red(localjet.coeff_monomial(scale**2))
local3=red(localjet.coeff_monomial(scale**3))
Lc=-(25+10*r)/4
print('VERTEX QUADRATIC JET',local2,flush=True)
print('CUSP QUADRATIC JET',red(local2.subs(L,Lc)),flush=True)
print('CUSP CUBIC JET',red(local3.subs(L,Lc)),flush=True)
print('CUSP TANGENT cubic restriction v=0',red(local3.subs({L:Lc,v:0})),flush=True)
print('CUSP W discriminant',red(discW.subs(L,Lc)),flush=True)
check('vertex quadratic coefficient u^2 degenerates only Lc',S.Poly(local2,u,v).coeff_monomial(u*u)-(4*L+25+10*r))
check('cusp has nonzero tangent cubic',local3.subs({L:Lc,v:0}),False)
check('origin plane derivative',S.diff(P+L*T*Q**2,X).subs({X:0,Y:1,T:0})-10)
check('origin limiting X',((b-t*t)/(a+4*r*t)).subs(t,-alpha*L-d)-X0)
check('origin limiting denominator',(a+4*r*t).subs(t,-alpha*L-d)-4*(3-r)*L)
beta=(11-5*r)*L/(2*(L+5*r))
k=4*(L+5*r)/r
q=d*k*k
Tbeta=4*x**3+(beta*beta-6*beta+1)*x*x+2*(beta*beta-beta)*x+beta*beta
check('Tate square-completion and exact twist',W.subs(xi,q*(x-beta))-q**3*Tbeta/4)
check('negative control reverse twist sign',W.subs(xi,q*(x-beta))+q**3*Tbeta/4,False)
z_from_x=a3/(q*(x-beta))-alpha*L
check('nonmarked inverse chart denominator',z_from_x+gamma*L-(gamma-alpha)*L*x/(x-beta))
check('conic inverse denominator equals 4r chart factor',(a+4*r*(z-d))-4*r*(z+gamma*L))
print('INFINITY FORM',red(P.subs(T,0)),flush=True)
rho=S.symbols('rho')
Ipoly=red(P.subs({X:rho,Y:1,T:0}))
check('infinity slopes factorization',Ipoly-2*rho*(rho*rho-d)*(rho*rho-m))
check('infinity square classes dm=5',d*m-5)
check('negative control changed infinity square product',d*m+5,False)
source=pathlib.Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_01/evidence/candidate_stage1/inputs/manuscript.tex')
pdf=pathlib.Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_01/evidence/source/qptsurface2.pdf')
print('INPUT_SHA256 manuscript',hashlib.sha256(source.read_bytes()).hexdigest(),flush=True)
print('INPUT_SHA256 AIM_PDF',hashlib.sha256(pdf.read_bytes()).hexdigest(),flush=True)
print('SYMPY',S.__version__,flush=True)
bad=[q for q in checks if q[1]!=q[2]]
print('SUMMARY total',len(checks),'unexpected',len(bad),flush=True)
sys.exit(bool(bad))
