#!/usr/bin/env python3
"""Exact algebra and a covering-interval certificate for TURN_3.md.
This is not a numerical simulation of the infinite-dimensional theorem.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import csv,io,json,itertools
import sympy as s
checks=0

def ck(v):
 global checks
 assert v
 checks+=1

r,x,z,y=s.symbols('r x z y')
f=lambda x,r:((r+4)*x+r+1)/(2*r*x+2)
b=lambda z,r:(2*z-r-1)/(r+4-2*r*z)
fr=(4-r*r)/(2*(1+r*x)**2)
for e in [f(b(z,r),r)-z,b(f(x,r),r)-x,s.diff(f(x,r),x)-fr,s.diff(b(z,r),r)+(1-4*b(z,r)**2)/(4-r*r),b(s.Rational(1,2),r)+r/4,b(-s.Rational(1,2),r)+s.Rational(1,2),b(s.Rational(3,2),r)-s.Rational(1,2)]:ck(s.factor(e)==0)
# Parameter rectangle, rank-one extremum and distortion constants.
t=s.symbols('t',nonnegative=True)
beta=(16-100*t*t)/(4-t*t)
ck(s.factor(s.diff(beta,t)+768*t/(4-t*t)**2)==0)
ck(s.Rational(9,16)**2/s.Integer(3)<s.Rational(1,3)**2)
q=s.symbols('q',nonnegative=True)
ck(s.diff(q/(1+q*q)**2,q).subs(q,1/s.sqrt(3))==0)
ck(s.simplify((q/(1+q*q)**2).subs(q,1/s.sqrt(3))-9/(16*s.sqrt(3)))==0)
ck(F(16)*F(24,25)/(1-F(24,25))==384)
ck(3+F(25,24)*384==403)
ck(1+F(25,96)*384==101)
ck(403+F(35,24)*384==963)
ck(F(2)*F(2,5)/(1-F(2,5)/2)==1)
ck(F(2)*F(2,5)/(4-F(2,5)**2)+1/(1-F(2,5)/2)==F(35,24))
algebra_checks=checks
# Rational interval certificate: all points are covered by the 40 intervals.
rows=[]; worst=F(0)
for j in range(40):
 lo=F(j,100);hi=F(j+1,100)
 bet=(16-100*lo*lo)/(4-lo*lo)
 den=1000;kk=isqrt(bet.numerator*den*den//bet.denominator)
 if F(kk*kk,den*den)<bet:kk+=1
 ck(F(kk*kk,den*den)>=bet)
 ck(kk==0 or F((kk-1)**2,den*den)<bet)
 bound=(2+hi)**2/(4*(2-hi)**2)*(1+F(kk,3000)+bet/4)
 ck(bound<=F(91,100))
 ck(bound<F(24,25)**2)
 worst=max(worst,bound)
 rows.append([j,str(lo),str(hi),str(bet),kk,str(bound)])
ck(F(91,100)<F(24,25)**2)
stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n')
w.writerow(['interval','lower','upper','beta_upper','sqrt_upper_times_1000','norm_squared_upper']);w.writerows(rows)
certificate=stream.getvalue()
p=Path(__file__).with_name('TURN_3_CONTRACTION.csv')
if p.exists():ck(p.read_bytes()==certificate.encode())
else:p.write_bytes(certificate.encode());ck(True)
interval_checks=checks-algebra_checks
# Herglotz branch transport identity, including branch normalization.
wy=lambda x,y:(1-y*y/4)/(1-x*y)**2
sig=2*(y+r)/((r+1)*y+r+4)
tau=2*(y+r)/((r-1)*y-r+4)
for branch,target in [(0,sig),(1,tau)]:
 inv=b(x+branch,r)
 transported=s.factor(wy(inv,y)*s.diff(inv,x))
 mass=s.factor(transported/wy(x,target))
 ck(s.factor(s.diff(mass,x))==0)
 ck(s.factor(s.diff(target,y)-2*(4-r*r)/s.denom(target)**2)==0)
 ck(s.factor(s.diff(target,r)-2*(4-y*y)/s.denom(target)**2)==0)
 for rr,yy in itertools.product([s.Rational(-2,5),s.Rational(2,5)],[s.Rational(-2,3),s.Rational(2,3)]):
  val=target.subs({r:rr,y:yy});ma=mass.subs({r:rr,y:yy})
  ck(-s.Rational(2,3)<=val<=s.Rational(2,3));ck(0<ma<1)
# Exact finite-dimensional random-variable inverse differentials with
# nonuniform probabilities, so the calculation is not limited to equal weights.
finite_cases=0
for B in [F(7),F(10),F(16)]:
 for vals in itertools.product([F(-1,2),F(0),F(1,2)],repeat=3):
  # r=0 is a permissible feedback point only when mean is 0.
  weights=[F(1,6),F(1,3),F(1,2)]
  if sum(a*v for a,v in zip(weights,vals))!=0:continue
  qv=s.Matrix([s.Rational(1-4*v*v) for v in vals]);E=s.Matrix([[s.Rational(a) for a in weights]])
  be=s.Rational(B/4);m=(E*qv)[0]
  Inv=s.eye(3)-be/(1+be*m)*qv*E
  ck(Inv*(s.eye(3)+be*qv*E)==s.eye(3));finite_cases+=1
# The cut-matching identity used to glue monotone maps.
ck(s.factor(b(s.Rational(1,2),r)+r/4)==0)
print(json.dumps({'status':'PASS','exact_assertions':checks,'algebra_assertions':algebra_checks,'covering_interval_assertions':interval_checks,'covering_intervals':40,'maximum_certified_squared_bound':str(worst),'chosen_contraction':'24/25','unequal_weight_inverse_cases':finite_cases,'limitations':'Finite controls certify the displayed identities and the full parameter bound; the probability, transport and boundary proofs remain analytic arguments in TURN_3.md.'},indent=2,sort_keys=True))
