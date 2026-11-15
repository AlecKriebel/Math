"""Small root algebra checks, independent of deposited or peer programs."""
import sympy as s
import json
count=0
def eq(a,b,label):
    global count
    count+=1
    if s.simplify(a-b)!=0:raise RuntimeError(label)
def ne(a,b,label):
    global count
    count+=1
    if s.simplify(a-b)==0:raise RuntimeError(label)
u,v=s.symbols('u v',nonnegative=True)
p,x=s.symbols('p x',nonnegative=True)
t=s.symbols('t',nonnegative=True)
e=s.Rational(1,96);d=s.Rational(1,4)
pp=u/(1+u);xx=v/(1+v)
phi=2*s.log(1+u)+(2-e)/(1+u)+2*s.log(1+v)+d*pp*xx**2
sub={u:p/(1-p),v:x/(1-x)}
A=s.cancel(((1+u)**2*s.diff(u*s.diff(phi,u),u)).subs(sub))
B=s.cancel(((1+v)**2*s.diff(v*s.diff(phi,v),v)).subs(sub))
Q=s.cancel(((1+u)**2*(1+v)**2*u*v*s.diff(phi,u,v)**2).subs(sub))
eq(A,4*p+(e+d*x*x)*(1-2*p),'global A')
eq(B,2+2*d*p*x*(2-3*x),'global B')
eq(Q,4*d*d*p*(1-p)*x**3*(1-x),'global mixed square')
A0=e+s.Rational(167,48)*p;B0=s.Rational(3,2);Q0=p/4
eq(A-A0,d*x*x+2*d*p*(1-x*x),'A nonnegative decomposition')
eq(B-B0,2*d*((1-p)+p*(1-x)*(1+3*x)),'B nonnegative decomposition')
eq(Q0-Q,4*d*d*p*(1-(1-p)*x**3*(1-x)),'Q nonnegative decomposition')
eq(A0*B0-Q0,s.Rational(1,64)+s.Rational(159,32)*p,'strict determinant lower bound')
P1=2*x-1;P2=6*x*x-6*x+1
lap=lambda f:s.expand((x*(1-x)*s.diff(f,x,2)+(1-2*x)*s.diff(f,x))/2)
eq(s.integrate(P1,(x,0,1)),0,'first mean')
eq(s.integrate(P2,(x,0,1)),0,'second mean')
eq(lap(P1),-P1,'first eigenvalue')
eq(lap(P2),-3*P2,'second eigenvalue')
eq(x*x,s.Rational(1,3)+P1/2+P2/6,'initial spectral decomposition')
w=e+d/3+d*P1/2+d*s.exp(-2*t)*P2/6
mean=s.integrate(w,(x,0,1))
eq(w.subs(t,0),e+d*x*x,'actual jet initial data')
eq(s.diff(w,t),lap(w)+w-mean,'exact normalized jet residual')
eq(mean,s.Rational(3,32),'time independent probability mean')
at=w.subs(x,0)
eq(at,e-(1-s.exp(-2*t))/24,'horizontal coefficient')
eq(at.subs(t,s.log(2)/2),-e,'strict finite-time negative coefficient')
eq(at.subs(t,s.log(s.Rational(4,3))/2),0,'first zero')
eq(s.diff(at,t).subs(t,0),-s.Rational(1,12),'initial decreasing direction')
eq(s.limit(at,t,s.oo),-s.Rational(1,32),'negative asymptotic jet coefficient only')
ne(s.diff(w,t),lap(w)+w,'omitted normalization must fail')
wrong=w.subs(s.exp(-2*t),s.exp(-t))
ne(s.diff(wrong,t),lap(wrong)+wrong-s.integrate(wrong,(x,0,1)),'wrong decay must fail')
ne(2*2-2,0,'literal same-weight rank-two reaction calibration must fail')
eq(1*2-2,0,'defining-flow stationary product calibration')
print(json.dumps({'status':'PASS_ROOT117_EXACT_ALGEBRA_AND_CONVENTION_CONTROLS','explicit_guards':count,'negative_curvature':'-1/96','finite_time':'log(2)/2','continuum_inequality_proof':'Nonnegative decompositions on the entire closed unit square; guarded equalities supplement the written proof','classical_PDE_existence_proved_by_algebra':False},sort_keys=True))
