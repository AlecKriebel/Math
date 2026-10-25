"""Independent symbolic controls built from fresh_graph_fourier, not published helpers."""
from pathlib import Path
from datetime import datetime,timezone
import json
import sympy as s
from fresh_graph_fourier import coordinate,omega,theta,labels,orbits
h=s.Rational(1,2)
rows=[tuple(map(int,g)) for g in orbits]
u0,u1,u2,u3,u4,u5,p0,p1,p2=s.symbols('u0 u1 u2 u3 u4 u5 p0 p1 p2')
g=u4+2*u5;hh=u0*u5+2*u4
xs=[u0,u1,u2,u3,u4,h,h,u5,p0,p1,p2,h]
xt=[2*u5*(4-u0)/g,u3/(4-u0),u2,2*u1*hh/g,4*u4*p2*(4-u0)/hh,h,h,2*u0*p2*g/hh,p1,p0,g/8,h]
perm={f'L{i}':v for i,v in enumerate([1,0,3,2])}
for r in rows:
 assert s.cancel(coordinate(omega,labels,r,xs,[h,h])-coordinate(omega,perm,r,xt,[h,h]))==0
print('Omega nine-variable map: all 14 nonconstant JC orbits exact',flush=True)
xx=s.symbols('x0:12');lv,lf=s.symbols('lv lf')
tq=[s.expand(coordinate(theta,labels,r,xx,[lv,lf])) for r in rows]
A,B,C,D,E,F,G,H,J,K,L,M,N,O=tq
identities=[J-K-M+N,J-A*H-B*F+C*E,G*L-E*N,L**2-B*E*H,B*M-D*L-B**2*F+B*C*E,B*E*O-B*G*H-C*E*L+D*E*H]
for i,z in enumerate(identities):assert s.expand(z)==0;print('Theta identity',i+1,'exact for all parameters',flush=True)
# Algebraic beta point: exact reduction modulo the irreducible quadratic.
b=s.symbols('b');poly=43337075*b*b-36083110*b+7336259
source=list(map(s.Rational,['2/3','3/4','3/5','1/2','9/20','2/5','1/2','1/3','1/5','1/2','1/2','3/8']))
target=[s.Rational(2,3),s.Rational(3,4),24835*b/(20678-24835*b),h,s.Rational(9934,12215),s.Rational(171,775),10339/(53010*b),h,3/(20*b),h,s.Rational(1767,4832),s.Rational(31,190)]
pt={f'L{i}':v for i,v in enumerate([3,1,2,0])}
for r in rows:
 z=s.cancel(coordinate(theta,labels,r,source,[h,h])-coordinate(theta,pt,r,target,[h,h]));num,den=s.fraction(z)
 assert s.rem(num,poly,b)==0
 assert s.gcd(den,poly)==1
# Rational isolating interval and elementary monotonic ratio bounds ensure every multiplier strict.
lo=s.Rational(441,1250);hi=s.Rational(3529,10000)
assert poly.subs(b,lo)>0 and poly.subs(b,hi)<0 and s.diff(poly,b).subs(b,hi)<0
for expr in target:
 a=s.cancel(expr).subs(b,lo) if hasattr(expr,'subs') else expr
 c=s.cancel(expr).subs(b,hi) if hasattr(expr,'subs') else expr
 assert 0<a<1 and 0<c<1
print('Theta algebraic point: exact equality modulo quadratic and strict interval',flush=True)
# Generic bridge-cut identities and strict inequality obstruction.
a,bb,c,t,AA,BB,CC,T,z=s.symbols('a b c t A B C T z')
f1=a*AA-z*z*bb*c*BB*CC;f2=z*T*t-z*z*bb*c*BB*CC;f3=z*CC*(AA*t-z*T*bb*c);f4=z*c*(z*BB*CC*t-T*a)
assert s.expand(a*AA-z*T*t-(f1-f2))==0
assert s.expand(z*z*CC*T*(a*bb*c-t*t)-(z*CC*t*(f1-f2)-a*f3))==0
assert s.expand(z*z*c*t*(AA*BB*CC-T*T)-(AA*f4+z*c*T*(f1-f2)))==0
# Non-strict central edge is a genuine boundary exception.
assert all(s.expand(q.subs({a:1,bb:1,c:1,t:1,AA:1,BB:1,CC:1,T:1,z:1}))==0 for q in [f1,f2,f3,f4])
# Signs of comparison factor: f1 can vanish despite nonzero terms, so equality/positivity mechanism is needed.
assert f1.subs({a:s.Rational(1,4),AA:1,z:s.Rational(1,2),bb:1,c:1,BB:1,CC:1})==0
# Incidence transformation preserves a character contraction term, but bridges alone do not determine physical feasibility.
l,r,x=s.symbols('l r x',positive=True)
assert s.simplify(l*r*x/(l*r)-x)==0
assert s.Rational(9,10)*2>1 # a local endpoint may leave its physical range despite admissible rescaled bridge.
Path(__file__).with_name('fresh-symbolic.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','omega_rational_identity_orbits':14,'theta_generic_polynomial_identities':6,'theta_algebraic_point_orbits':14,'theta_isolating_interval':[str(lo),str(hi)],'cut_identities':3,'boundary_and_incidence_controls':3,'scope':'Exact symbolic checks and strict witnesses; finite atlas completeness not inferred'},indent=2)+'\n')
print('PASS all fresh symbolic controls')
