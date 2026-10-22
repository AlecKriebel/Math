#!/usr/bin/env python3
"""Finite exact controls. These do not prove analytic estimates or global rigidity."""
import json
from collections import defaultdict
from fractions import Fraction
import sympy as s

counts = defaultdict(int)
def ck(group, proposition):
    assert bool(proposition), (group, proposition)
    counts[group] += 1

def zero(group, expression):
    ck(group, s.simplify(expression) == 0)

a,b,c,t,R=s.symbols('a b c t R', positive=True)
q=s.sqrt(a*a+b*b)
w=a*(a*a+2*b*b-a*c)/q**3
zero('weight_algebra', a/q-(s.diff(b/q,a)*b+s.diff(b/q,b)*c)-w)
zero('weight_algebra', w.subs({a:t*a,b:t*b,c:t*c}, simultaneous=True)-w)
zero('weight_algebra', w.subs({a:R,b:0,c:0})-1)
zero('weight_algebra', s.diff(q,a).subs({a:R,b:0})-1)
zero('weight_algebra', s.diff(q,b).subs({a:R,b:0}))
zero('weight_algebra', s.diff(q,a,a).subs({a:R,b:0}))
zero('weight_algebra', s.diff(q,a,b).subs({a:R,b:0}))
zero('weight_algebra', s.diff(q,b,b).subs({a:R,b:0})-1/R)
j=s.symbols('j', integer=True, positive=True)
zero('funk_binomial_bounds',(2*j+1)**2-4*j*(j+1)-1)
zero('funk_binomial_bounds',4*(j+1)**3-(2*j+1)**2*(j+2)-(3*j+2))
zero('convexity_reciprocal',(-c/a**2+2*b*b/a**3)+1/a-(a*a+2*b*b-a*c)/a**3)
for j in range(41):
    expected=(-1)**j*s.binomial(2*j,j)/4**j
    zero('funk_spectrum', s.legendre(2*j,0)-expected)
    ck('funk_spectrum', expected != 0)
for j in range(21):
    zero('funk_spectrum', s.legendre(2*j+1,0))
for m in range(21):
    ck('band_dimensions', sum(4*j+1 for j in range(m+1))==(m+1)*(2*m+1))

A11,A22,A33,A12,A13,A23=s.symbols('A11 A22 A33 A12 A13 A23', real=True)
A=s.Matrix([[A11,A12,A13],[A12,A22,A23],[A13,A23,A33]])
vs=[s.eye(3).col(i) for i in range(3)]
vs += [(vs[i]+vs[j])/s.sqrt(2) for i,j in [(0,1),(0,2),(1,2)]]
p=[s.trace(A)-(v.T*A*v)[0] for v in vs] # values divided by pi
inv=[(p[1]+p[2]-p[0])/2,(p[0]+p[2]-p[1])/2,(p[0]+p[1]-p[2])/2,
     (p[0]+p[1])/2-p[3],(p[0]+p[2])/2-p[4],(p[1]+p[2])/2-p[5]]
for got,expected in zip(inv,[A11,A22,A33,A12,A13,A23]):
    zero('six_plane_inverse',got-expected)
linear=s.Matrix([[s.diff(p_i,z) for z in [A11,A22,A33,A12,A13,A23]] for p_i in p])
ck('six_plane_inverse', linear.det()!=0)
ck('six_plane_constants',3*Fraction(3,2)**2+6*2**2==Fraction(123,4))
ck('six_plane_constants',123<12**2)
ck('six_plane_constants',Fraction(24,9801)+Fraction(48,99)==Fraction(4776,9801))
ck('six_plane_constants',Fraction(4776,9801)<Fraction(1,2))
ck('six_plane_constants',Fraction(99,100)>Fraction(4,100))

x,y,z=s.symbols('x y z', real=True)
u=s.Matrix([x,y,z])
ns=[s.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(s.Rational(3,5),s.Rational(4,5),0),(0,s.Rational(3,5),s.Rational(4,5)),(s.Rational(4,5),0,s.Rational(3,5))]]
h=s.prod((u.dot(n))**2 for n in ns)
for n in ns:
    zero('finite_plane_invisibility',n.dot(n)-1)
    i=next(i for i in range(3) if n[i]!=0)
    coords=[x,y,z]
    substitution={coords[i]:-sum(n[j]*coords[j] for j in range(3) if j!=i)/n[i]}
    zero('finite_plane_invisibility',h.subs(substitution))
    grad=s.Matrix([s.diff(h,v) for v in coords])
    zero('finite_plane_invisibility',(grad.dot(n.cross(u))).subs(substitution))
zero('finite_plane_invisibility',h.subs({x:-x,y:-y,z:-z},simultaneous=True)-h)
zero('finite_plane_invisibility',sum(u[i]*s.diff(h,u[i]) for i in range(3))-12*h)
ck('finite_plane_invisibility',h.subs({x:1,y:1,z:1})>0)

x1,x2,y1,y2=s.symbols('x1 x2 y1 y2', real=True)
dot=x1*y1+x2*y2; det=x1*y2-x2*y1
zero('midpoint_defect',(x1*x1+x2*x2)*(y1*y1+y2*y2)-dot*dot-det*det)
# Pythagorean input vectors and sum vectors make the rationalization checks exact.
for X in [(3,4),(4,3),(5,12),(12,5),(8,15),(15,8)]:
    for Y in [(3,-4),(4,-3),(5,-12),(12,-5)]:
        AA=s.sqrt(sum(s.Integer(v)**2 for v in X));BB=s.sqrt(sum(s.Integer(v)**2 for v in Y))
        CC=s.sqrt(sum(s.Integer(X[i]+Y[i])**2 for i in range(2)))
        dd=X[0]*Y[1]-X[1]*Y[0];pp=X[0]*Y[0]+X[1]*Y[1]
        zero('midpoint_defect',(AA+BB-CC)*(AA+BB+CC)*(AA*BB+pp)-2*dd*dd)
# Incidence constant integral on one unit tangent circle.
ang=s.symbols('ang', real=True)
zero('incidence_constant',s.integrate(s.cos(ang)**2,(ang,0,2*s.pi))-s.pi)
zero('incidence_constant',s.integrate(s.sin(ang)*s.cos(ang),(ang,0,2*s.pi)))

c0=s.Rational(99,100)
ck('cap_switch_geometry',2*c0*c0-1>s.Rational(96,100))
ck('cap_switch_geometry',s.Rational(9,14)<s.Rational(81,100)**2)
centers=[s.eye(3).col(i) for i in range(3)]+[s.Matrix([1,2,3])/s.sqrt(14)]
centers += [-v for v in centers]
for i in range(len(centers)):
    for j in range(i):
        ck('cap_switch_geometry',centers[i].dot(centers[j])<2*c0*c0-1)
q00,q01,q02,q10,q11,q12,q20,q21,q22=s.symbols('q00 q01 q02 q10 q11 q12 q20 q21 q22')
Q=s.Matrix([[q00,q01,q02],[q10,q11,q12],[q20,q21,q22]])
solution=s.solve(list(Q-s.eye(3)),list(Q),dict=True)
ck('cap_switch_geometry',len(solution)==1)
ck('cap_switch_geometry',Q.subs(solution[0])==s.eye(3))
ck('cap_switch_geometry',centers[3]!=-centers[3])

print(json.dumps({
    'status':'PASS', 'exact_assertions':sum(counts.values()),
    'groups':dict(sorted(counts.items())),
    'requirements':'Python 3 and SymPy',
    'sympy_version':s.__version__,
    'limits':'Finite algebraic controls only. No numerical search, no proof of functional-analytic convergence by computation, no global resolution or formal-verification claim.'
},indent=2,sort_keys=True))
