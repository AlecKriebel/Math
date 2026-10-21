#!/usr/bin/env python3
"""Independent finite algebra controls; no finite check certifies the PDE/statistical proof."""
import sympy as s,json
n=0
for d in range(2,7):
 x=s.symbols('x:'+str(d)); m=d*(d+1)//2+d
 polys=[t*t/2 for t in x]+[x[i]*x[j]/2 for i in range(d) for j in range(i+1,d)]+list(x)
 def jet(f):return [s.diff(f,t,2) for t in x]+[2*s.diff(f,x[i],x[j]) for i in range(d) for j in range(i+1,d)]+[s.diff(f,t) for t in x]
 M=s.Matrix([jet(f) for f in polys]).subs(dict.fromkeys(x,0));assert M==s.eye(m);n+=m*m
# Exact repeated eigenvalue rotations preserve normal equations.
for a in range(1,20):
 for b in range(1,12):
  co=s.Rational(a*a-b*b,a*a+b*b);si=s.Rational(2*a*b,a*a+b*b)
  U=s.Matrix([[co,-si],[si,co]])
  B=s.Matrix([[1,a],[b,2],[a-b,3]])
  e=s.Matrix([[a+b,1]])
  assert (B*U)*(B*U).T==B*B.T
  assert (B*U)*(e*U).T==B*e.T;n+=2
# Solve extension equations independently, rather than insert author weights.
for k in range(1,9):
 V=s.Matrix([[(-j)**i for j in range(1,k+2)] for i in range(k+1)])
 al=V.inv()*s.ones(k+1,1)
 assert V*al==s.ones(k+1,1);n+=k+1
 if k==6:assert list(al)==[28,-112,210,-224,140,-48,7];n+=1
# Exact covariance identity on a stationary reversible three-state chain.
P=s.Matrix([[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)],[s.Rational(1,3),s.Rational(1,2),s.Rational(1,6)],[s.Rational(1,6),s.Rational(1,6),s.Rational(2,3)]])
F=s.Matrix([[1,3,-2],[4,0,1],[-1,2,5]])
mean=sum(P[i,j]*F[i,j]/3 for i in range(3) for j in range(3));Z=F-s.ones(3)*mean
r=s.Matrix([sum(P[i,j]*Z[i,j] for i in range(3)) for j in range(3)])
t=s.Matrix([sum(P[i,j]*Z[i,j] for j in range(3)) for i in range(3)])
for lag in range(1,12):
 Q=P**(lag-1)
 direct=sum(P[i,j]*Q[j,k]*P[k,l]*Z[i,j]*Z[k,l]/3 for i in range(3) for j in range(3) for k in range(3) for l in range(3))
 assert direct==(r.T*Q*t)[0]/3;n+=1
print(json.dumps({'status':'PASS','independent_exact_assertions':n,'scope':'Jet spanning in dimensions2–6, degenerate-eigenspace basis invariance, finite-order extension weights and stationary pair-covariance identity; no analytic or empirical consistency inferred from these finite controls.'},indent=2))
