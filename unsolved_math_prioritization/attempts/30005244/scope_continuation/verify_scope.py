"""Exact finite controls for the analytic compact-support counterexample."""
import sympy as s
import json
from fractions import Fraction as Q
checks=0
z=s.symbols('z');i=s.I
f=s.exp(i*z)*(1-i*z-z*z)-1
g=s.exp(i*z)*(z*z+3*i*z-3)+3
for n in range(2,13):
 assert s.expand(s.series(f,z,0,n+1).removeO()).coeff(z,n)==i**n*(n-1)**2/s.factorial(n);checks+=1
 assert s.expand(s.series(g,z,0,n+1).removeO()).coeff(z,n)==-i**n*(n-1)*(n-3)/s.factorial(n);checks+=1
for n in range(4,100):
 assert (n-1)**2<=n*n;checks+=1
 assert abs((n-1)*(n-3))<=n*n;checks+=1
# Bound e via terms 0..4 plus a geometric upper bound for its tail.
e_upper=sum((Q(1,s.factorial(n)) for n in range(5)),Q(0))+Q(1,100)
assert e_upper<Q(11,4);checks+=1
assert 2*e_upper-Q(9,2)<1;checks+=1
for ell in range(1,101):
 a=Q(1,2*ell+1)
 assert ell*a-(-(ell+1)*a)==1;checks+=1
 lam=Q(ell,2*ell+1)-Q(1,3)
 if ell==1:assert lam==0
 else:assert lam>=Q(1,15)
 checks+=1
k=Q(1,10000)
assert 2*k*k<Q(1,60);checks+=1
assert 120*k*k<Q(1,2);checks+=1
assert 1446*k<Q(2,3);checks+=1
assert Q(3,4)*2*Q(4,3)==2;checks+=1
assert Q(6,64)*Q(32,3)==1;checks+=1
assert Q(3)*Q(4,3)/6==Q(2,3);checks+=1
for j in range(1,31):
 ratio=Q(1,7*2**(3*j+12))
 assert 0<ratio<1;checks+=1
 assert ratio/8==Q(1,7*2**(3*(j+1)+12));checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'frequency':'1/10000','trace_imaginary_upper_bound':str(-Q(2,3)*k**3+Q(1446)*k**4),'e_upper_bound':str(e_upper),'geometric_removed_volume_ratio':'2^(-3j-12)/7','limits':'Exact algebra and inequalities only. The Hilbert-space spectral and compact-mask arguments require the written proof; no numerical eigenvalue is used.'},indent=2))
