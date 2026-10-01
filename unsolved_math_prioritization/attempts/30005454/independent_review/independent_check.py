#!/usr/bin/env python3
"""Independent exact local/finite controls; no infinite stochastic theorem by simulation."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import json
counts={}
def ck(k,v):
 assert bool(v),k
 counts[k]=counts.get(k,0)+1
for n,a,b in product(range(1,11),range(1,5),range(1,5)):
 rate=F(n,n+a)+F(n,n+b)
 ck('harmonic_jump_drift',rate/n==F(1,n+a)+F(1,n+b))
 ck('harmonic_quadratic_jump',F(1,n)**2==F(1,n*n))
for length,values in [(4,range(1,5)),(6,range(1,3)),(8,range(1,3))]:
 for raw in product(values,repeat=length):
  mean=F(sum(raw),length);z=[F(v)/mean for v in raw];T=[z[i]+z[(i+1)%length] for i in range(length)]
  inv=[1/x for x in T];rate=[z[i]*(inv[i-1]+inv[i]) for i in range(length)];g=[inv[i-1]+inv[i]-1 for i in range(length)]
  ck('rate_mean',sum(rate)==length);ck('pair_mean',sum(T)==2*length)
  lhs=sum((rate[i]+rate[(i+1)%length])/T[i] for i in range(length))-length
  rhs=sum(z[i]*g[i]*g[i] for i in range(length));ck('log_pair_energy',lhs==rhs)
  ck('pair_harmonic_entropy',sum((t-2)**2/(2*t) for t in T)==2*sum(inv)-length)
  u=[(-1)**i*(z[i]-1) for i in range(length)];flux=[(-1)**i*(inv[i]-F(1,2)) for i in range(length)]
  for i in range(length):
   drift=sum(z[i]*(u[j]-u[i])/(2*(z[i]+z[j])) for j in [(i-1)%length,(i+1)%length])
   ck('staggered_diffusion',drift==(-1)**i*z[i]*g[i]);ck('log_flux',flux[i]-flux[i-1]==(-1)**i*g[i])
# Finite block telescoping, without a periodic identification at its ends.
for L in range(2,82,2):
 coeff=[0]*(L+1)
 for i in range(L):coeff[i]+=(-1)**i;coeff[i+1]+=(-1)**i
 ck('two_boundary_terms_only',coeff==[1]+[0]*(L-1)+[-1])
# Formal Taylor coefficients of the exact Poisson reciprocal expression.
for n in range(101):
 ck('poisson_reciprocal_coefficients',F(1,(n+1)*factorial(n))-F(1,factorial(n+2))==F(1,(n+2)*factorial(n)))
# Deterministic recurrence phase error for arbitrary finite adjacent-pair errors.
for errors in product([F(-1,8),F(0),F(1,8)],repeat=5):
 z=[F(4,5)]
 for error in errors:z.append(2+error-z[-1])
 total=F(0)
 for i in range(1,len(z)):
  total+=abs(errors[i-1]);ideal=z[0] if i%2==0 else 2-z[0]
  ck('growing_window_telescope',abs(z[i]-ideal)<=total)
# Exact selected-time exponents and ceiling estimates; tau=q^2 makes sqrt exact.
for n in range(2,51):
 for q in [n,n*n,n**3+1]:
  tau=q*q;L=n**3*q;L+=L%2
  ck('even_ceiling',L%2==0 and n**3*q<=L<n**3*q+2)
  ck('variance_summable',F(1,L)<=F(1,n**4))
  ck('boundary_summable',F(q,L)<=F(1,n**3))
  ck('phase_error_summable',F(2*L,n**8*q)<=F(2,n**5)+F(4,n**9))
# A vertex ring contributes once to its own incident pair and at most once to each other pair.
for vertex in range(-4,5):
 for edge in [vertex-1,vertex]:
  ck('own_pair_increment',edge in [vertex-1,vertex])
  for i in range(-5,5):
   increment=int(edge in [i,i+1]);ck('three_clock_support',not increment or vertex in [i,i+1,i+2])
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'floating_point_used':False,'stochastic_simulation_used':False,'scope':'supporting finite identities only; the separate review checks the infinite-volume probability proof'},indent=2))
