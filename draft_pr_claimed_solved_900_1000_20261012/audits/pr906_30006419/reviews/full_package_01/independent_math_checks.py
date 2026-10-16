#!/usr/bin/env python3
"""New exact diagnostic controls; written analysis supplies universal claims."""
from pathlib import Path
import json
import sympy as s
R=Path(__file__).resolve().parent
x,y,e,theta=s.symbols('x y e theta',real=True);receipts=[]
def eq(name,left,right):
 z=s.simplify(left-right)
 if z!=0:raise RuntimeError(name+': '+str(z))
 receipts.append({'name':name,'passed':True,'exact':str(left)})
def integ(f):return s.integrate(s.expand(f),(x,-1,1),(y,-1,1))
bubble=(1-x*x)**2*(1-y*y)**2
f=y+e*bubble*(1+x-y)
energy=integ(s.diff(f,x)**2+s.diff(f,y)**2)
extra=integ(s.diff(f-y,x)**2+s.diff(f-y,y)**2)
eq('same-trace scalar energy on new rectangle',energy,4+extra)
F=x+bubble/s.Integer(11);G=y-bubble*(1+x)/s.Integer(7)
jac=s.diff(F,x)*s.diff(G,y)-s.diff(F,y)*s.diff(G,x)
eq('new nonlinear exact primitive boundary identity',integ((G+F**2)*jac),integ(y+x*x))
# A variable source differential is essential to the domain variation formula.
V=bubble*(1+x)
direct=integ(36*x**3*V+18*x**4*s.diff(V,x))
stress=integ((9*x**4-1)*s.diff(V,x))
eq('cubic variable-field domain variation',direct,stress)
if not direct<0:raise RuntimeError('new variation sign')
receipts.append({'name':'new KS sign','passed':True,'exact':str(direct)})
wrong=integ(18*x**4*s.diff(V,x))
if wrong==stress:raise RuntimeError('missing spatial composition mutant undetected')
receipts.append({'name':'missing composition mutant rejected','passed':True,'incorrect':str(wrong),'correct':str(stress)})
D=s.Matrix([[s.Rational(2,3),s.Rational(-1,4)],[s.Rational(4,7),s.Rational(-2,5)]]);A=s.eye(2)+e*D
w=s.Matrix([s.cos(theta),s.sin(theta)])
q=(A.inv()*w).dot(A.inv()*w)
weight=A.det()**-2*q**-2
kernel=4*(w.T*D*w)[0]-2*s.trace(D)
eq('angular weight arbitrary-matrix derivative',s.trigsimp(s.diff(weight,e).subs(e,0)),kernel)
G0=s.Matrix([[s.Rational(7,3),s.Rational(2,5)],[s.Rational(2,5),s.Rational(1,7)]])
T=s.simplify(s.integrate((w.T*G0*w)[0]*(4*w*w.T-2*s.eye(2)),(theta,0,2*s.pi))/s.pi)
for i in range(2):
 for j in range(2):eq('quadratic stress entry '+str((i,j)),T[i,j],(2*G0-s.trace(G0)*s.eye(2))[i,j])
rot=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
T2=rot.T*T*rot
q0=T[0,0]-s.I*T[0,1];q2=T2[0,0]-s.I*T2[0,1]
eq('holomorphic-coordinate complex-square sign',q2,(s.Rational(3,5)+s.I*s.Rational(4,5))**2*q0)
m=s.sqrt(17)-4
eq('positive degeneracy-root equation',m*m+8*m,1)
eq('stretch-ratio reciprocal',1/m,4+s.sqrt(17))
# Half-area strict cutoff requirement is mathematically essential, not just a model specification.
for mass in [s.Rational(1,5),s.Rational(2,5)]:
 b=mass/(1-mass);eq('global zero period '+str(mass),(1+b)*mass-b,0)
 if not 0<b<1:raise RuntimeError('comass bound')
if not s.Rational(3,5)/(1-s.Rational(3,5))>1:raise RuntimeError('large cutoff mutant')
receipts.append({'name':'large-cutoff comass mutant rejected','passed':True})
result={'status':'PASS','sympy_version':s.__version__,'exact_check_count':len(receipts),'checks':receipts,'imports_candidate_code':False,'scope':'Finite symbolic controls and sensitivity tests; no numerical quadrature and no formal Sobolev certification.'}
(R/'MATH_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','exact_check_count':len(receipts)},indent=2))
