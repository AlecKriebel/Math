#!/usr/bin/env python3
"""Exact finite controls of the credited all-degree, all-period construction."""
from pathlib import Path
import json,itertools
import sympy as s
z=s.symbols("z")
checks={}
def ck(name,x):
 assert bool(x),name
 checks[name]="PASS"
def iterate(P,Q,p,q,d):
 return (s.Poly(sum(p.nth(j)*P.as_expr()**j*Q.as_expr()**(d-j) for j in range(d+1)),z),
         s.Poly(sum(q.nth(j)*P.as_expr()**j*Q.as_expr()**(d-j) for j in range(d+1)),z))
case_count=0;iterates=0;directions=0
for d in (2,3):
 p0=s.Poly(s.prod(z+(2*j-1) for j in range(1,d+1)),z)
 q0=s.Poly(s.prod(z+2*j for j in range(1,d+1)),z)
 cases=[("base",p0,q0)]
 eps=s.Rational(1,10000)
 # Every coefficient-chart direction, including numerator leading coefficient;
 # denominator leading coefficient is the chart normalization.
 for which,j in [("p",j) for j in range(d+1)]+[("q",j) for j in range(d)]:
  for sign in (-1,1):
   p=p0+s.Poly(sign*eps*z**j,z) if which=="p" else p0
   q=q0+s.Poly(sign*eps*z**j,z) if which=="q" else q0
   cases.append((f"{which}{j}_{sign}",p,q));directions+=1
 # Also vary all chart coordinates simultaneously.
 for sign in (-1,1):
  p=p0+s.Poly(sign*eps*sum((j+1)*z**j for j in range(d+1)),z)
  q=q0+s.Poly(sign*eps*sum((j+1)*z**j for j in range(d)),z)
  cases.append((f"mixed_{sign}",p,q))
 for label,p,q in cases:
  tag=f"d{d}_{label}";case_count+=1
  ck(tag+"_chart_dimension",len(p.all_coeffs())+len(q.all_coeffs())-1==2*d+1)
  ck(tag+"_positive_coefficients",all(c>0 for c in p.all_coeffs()+q.all_coeffs()))
  ck(tag+"_coprime",s.gcd(p,q).degree()==0)
  # Disjoint quarter-radius intervals certify the complete negative strict
  # interlacing order, without floating-point root approximations.
  for poly,parity in [(p,1),(q,0)]:
   for j in range(1,d+1):
    center=-(2*j-parity)
    a=center-s.Rational(1,4);b=center+s.Rational(1,4)
    ck(tag+f"_root_{parity}_{j}",poly.count_roots(a,b)==1)
  P,Q=p,q
  for k in range(1,3):
   e=d**k;it=tag+f"_iterate{k}";iterates+=1
   ck(it+"_degrees",P.degree()==Q.degree()==e)
   ck(it+"_positive",all(c>0 for c in P.all_coeffs()+Q.all_coeffs()))
   ck(it+"_no_cancellation",s.gcd(P,Q).degree()==0)
   ck(it+"_real_simple_negative_poles",Q.count_roots(-s.oo,0)==e and s.gcd(Q,Q.diff()).degree()==0)
   F=P-s.Poly(z,z)*Q
   ck(it+"_fixed_degree",F.degree()==e+1)
   ck(it+"_fixed_all_real",F.count_roots(-s.oo,s.oo)==e+1)
   ck(it+"_positive_fixed_point",F.count_roots(0,s.oo)>=1)
   wronskian=P.diff()*Q-P*Q.diff()
   ck(it+"_no_finite_real_critical_point",wronskian.count_roots(-s.oo,s.oo)==0)
   c_infty=(P.nth(e-1)*Q.nth(e)-P.nth(e)*Q.nth(e-1))/Q.nth(e)**2
   ck(it+"_unramified_infinity",c_infty!=0)
   ck(it+"_infinity_not_fixed",P.LC()>0 and Q.LC()>0)
   if k==1:P,Q=iterate(P,Q,p,q,d)
# One higher period beyond the author's second-iterate checks.
p=s.Poly((z+1)*(z+3),z);q=s.Poly((z+2)*(z+4),z);P,Q=p,q
for k in range(2,4):P,Q=iterate(P,Q,p,q,2)
F=P-s.Poly(z,z)*Q
ck("period3_degree",F.degree()==9)
ck("period3_real_simple_roots",F.count_roots(-s.oo,s.oo)==9 and s.gcd(F,F.diff()).degree()==0)
# Negative control: real-fibered alone does not imply all periodic points real.
# (z²-1)/(2z) is conjugate to z² via a real-circle/complex-circle Mobius map.
p=s.Poly(z*z-1,z);q=s.Poly(2*z,z);F=p-s.Poly(z,z)*q
ck("real_fibered_not_sufficient_nonreal_fixed",s.factor(F.as_expr())==-(z*z+1))
ck("negative_control_finite_fixed_nonreal",F.count_roots(-s.oo,s.oo)==0)
out={"passed":len(checks),"failed":0,"sympy_version":s.__version__,
 "base_and_perturbed_maps":case_count,"individual_chart_directions_tested":directions,
 "iterated_map_cases":iterates,"checks":checks,
 "scope":"Exact finite perturbation and iteration controls. Ambient openness and all periods are justified by the written proof, not by this finite sample."}
Path(__file__).with_name("independent_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="checks"},indent=2))
