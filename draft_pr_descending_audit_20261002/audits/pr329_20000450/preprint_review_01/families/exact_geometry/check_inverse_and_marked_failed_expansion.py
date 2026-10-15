#!/usr/bin/env python3
import sys
import sympy as S
X,Y,L,r,x,xi,eta,delta,t,z=S.symbols('X Y L r x xi eta delta t z')
phi=(1+r)/2;c=(11+5*r)/2;d=5+2*r;m=5-2*r
alpha=1-r/5;gamma=2*r/5
a=40+20*r+8*L;b=a+5;h=4*X*X+2*X-1
a0=m;a1=(-26+10*r)*L-20*r
a2=(42-86*r/5)*L**2+(-100+100*r)*L+500+200*r
a3=(-112+48*r)*L**2*(L+5*r)/5
def red(p):return S.Poly(S.expand(p),r).rem(S.Poly(r*r-5,r)).as_expr().expand()
def re(p):
    q=S.Poly(S.expand(p),delta).rem(S.Poly(delta*delta-d,delta)).as_expr()
    return red(q)
tests=[]
def check(name,p,reducer=red,want=True):
    result=reducer(S.together(p).as_numer_denom()[0])==0
    tests.append(result==want)
    print(('PASS ' if result==want else 'FAIL ')+name+'; vanishes='+str(result),flush=True)
    if result!=want: print(reducer(S.together(p).as_numer_denom()[0]),flush=True)
P=red(2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X*X+Y*Y)**2-5*phi**3*(X*X+Y*Y)+c)
G=P+L*(X*X+Y*Y-1)**2
A=red(S.Poly(G,Y).coeff_monomial(Y**4));B=red(S.Poly(G,Y).coeff_monomial(Y**2));C=red(S.Poly(G,Y).coeff_monomial(1))
f=xi**3+a2*xi*xi+a1*a3*xi+a0*a3*a3
zI=a3/xi-alpha*L;tI=zI-d
XI=(b-tI*tI)/(a+4*r*tI)
YI=eta*zI/(20*xi*(zI+gamma*L))
# Modulo eta²=f, the inverse sends the cubic identically to the entire affine quintic.
YI2=f*zI*zI/(400*xi*xi*(zI+gamma*L)**2)
check('inverse cubic goes to quintic',A.subs(X,XI)*YI2*YI2+B.subs(X,XI)*YI2+C.subs(X,XI))
V_back=(2*A.subs(X,XI)*YI2+B.subs(X,XI))/h.subs(X,XI)
check('inverse chooses the original conic branch',V_back-2*r*XI-tI)
check('inverse recovers xi',a3/(V_back-2*r*XI+d+alpha*L)-xi)
check('inverse recovers eta literally',xi*20*YI*(zI+gamma*L)/zI-eta)
beta=(11-5*r)*L/(2*(L+5*r));k=4*(L+5*r)/r;q=d*k*k
Xi=q*(x-beta)
Eta=(k*delta)**3*(S.symbols('y')+((1-beta)*x-beta)/2)
ratio=5*xi*(b-t*t)/(r*eta*z)
for xx,yy,label in [(0,0,'P0'),(0,beta,'minus P0')]:
    ee=Eta.subs({x:xx,S.symbols('y'):yy})
    pp=ratio.subs({xi:Xi.subs(x,xx),eta:ee,z:-gamma*L,t:-gamma*L-d})
    for target,label2 in [(delta,'delta'),(r/delta,'r/delta'),(-delta,'minus delta'),(-r/delta,'minus r/delta')]:
        print('MARKED '+label+' slope comparison '+label2+' '+str(re(S.together(pp-target).as_numer_denom()[0])==0),flush=True)
    check(label+' is infinity slope of sqrt(m)',pp*pp-m,re)
for yy,label in [(0,'minus 2P0'),(beta*beta,'2P0')]:
    ee=Eta.subs({x:beta,S.symbols('y'):yy})
    pp=-5*a3/(r*ee)
    for target,label2 in [(delta,'delta'),(r/delta,'r/delta'),(-delta,'minus delta'),(-r/delta,'minus r/delta')]:
        print('MARKED '+label+' slope comparison '+label2+' '+str(re(S.together(pp-target).as_numer_denom()[0])==0),flush=True)
    check(label+' is infinity slope of sqrt(d)',pp*pp-d,re)
print('RESULTS',len(tests),'unexpected',sum(not a for a in tests),flush=True)
sys.exit(any(not a for a in tests))
