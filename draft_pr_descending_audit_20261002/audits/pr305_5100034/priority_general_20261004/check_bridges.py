#!/usr/bin/env python3
import sympy as s
x,y=s.symbols('x y',real=True)
a=s.sqrt(21);c=s.sqrt(5)
V=[s.Matrix([a,0]),s.Matrix([-3*a/5,s.Rational(16,5)]),s.Matrix([-3*a/5,-s.Rational(16,5)])]
M=s.Matrix([x,y])
def area(W):return s.simplify(sum(s.det(s.Matrix.hstack(W[i],W[(i+1)%len(W)])) for i in range(len(W)))/2)
def line(A,B):
 d=B-A;n=s.Matrix([d[1],-d[0]]);return n,s.simplify(n.dot(A))
def foot(n,h):return s.simplify(M+(h-n.dot(M))*n/n.dot(n))
lines=[line(V[i],V[(i+1)%3]) for i in range(3)]
D=area([foot(n,h) for n,h in lines]);O=s.Matrix([1/a,0]);R2=s.Rational(400,21);T=area(V)
classic=s.expand(T*(R2-(M-O).dot(M-O))/(4*R2));assert s.simplify(D-classic)==0
Aplus=s.simplify(D.subs({x:c,y:0}));Aminus=s.simplify(D.subs({x:-c,y:0}));assert s.simplify(Aplus-84*(7*a+c)/625)==0;assert s.simplify(Aminus-84*(7*a-c)/625)==0
R=s.simplify(Aplus/Aminus);assert s.simplify(R-(7*a+c)/(7*a-c))==0;assert R>1
assert s.simplify((D.subs({x:-c,y:0})/D.subs({x:c,y:0}))*R)==1
outerlines=[(s.Matrix([p[0]/21,p[1]/16]),s.Integer(1)) for p in V]
B=area([foot(n,h) for n,h in outerlines]);Bplus=s.simplify(B.subs({x:c,y:0}));Bminus=s.simplify(B.subs({x:-c,y:0}));assert s.simplify(Bplus/Aplus-s.Rational(125,24))==0;assert s.simplify(Bminus/Aminus-s.Rational(125,24))==0
print('SymPy version:',s.__version__)
print('Triangle area:',T)
print('Circumcenter:',list(O),'circumradius squared:',R2)
print('Original pedal polynomial:',s.factor(D))
print('Classical signed formula identity: exact zero residual')
print('Aplus:',Aplus,'Aminus:',Aminus)
print('Original focal ratio:',R,'> 1; inverted phase ratio exactly reciprocal')
print('Outer pedal polynomial:',s.factor(B))
print('Both phase-specific outer/original multipliers:',s.Rational(125,24))
print('SCOPE: exact consistency check of old formula and one candidate phase; no new all-N or historical-firstness inference.')
