#!/usr/bin/env python3
"""Exact algebra/clock controls; no simulated proof of profile convergence."""
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
C=Counter()
def ck(k,b):
 if not b:raise AssertionError(k)
 C[k]+=1
def add(A,B):return [(A[i] if i<len(A) else 0)+(B[i] if i<len(B) else 0) for i in range(max(len(A),len(B)))]
def mean(poly,a):return sum(v*F(factorial(a)*factorial(i),factorial(a+i)) for i,v in enumerate(poly))
def generator(poly,a,beta):
 c=1-beta
 # Discounted first-moment equation u'_f=-c(1-f)u_f+beta f E_mu[u_f].
 out=add([-c*v for v in poly],[F(0)]+[c*v for v in poly]);out[1]+=beta*mean(poly,a);return out
cases=0
for a in range(2,9):
 I=F(a,a-1)
 for denominator in range(3,15):
  for numerator in range(1,denominator):
   beta=F(numerator,denominator);rho=1-beta*I;c=1-beta
   if rho<=0:continue
   ka=I/c;kk=beta*(I-1)/c
   ck('renewal_defect',1-kk==rho/c and kk<1)
   ck('renewal_integral',ka/(1-kk)==I/rho)
   ck('uniform_growth_constant',1+beta*I/rho==1/rho)
   # Derivatives at zero from two separately computed formulas.
   direct=[];poly=[F(1)]
   for n in range(11):direct.append(mean(poly,a));poly=generator(poly,a,beta)
   forcing=[];kernel=[];renew=[]
   for n in range(11):
    forcing.append((-c)**n*F(a,a+n))
    kernel.append(beta*(-c)**n*F(a,(a+n)*(a+n+1)))
    renew.append(forcing[n]+sum(kernel[j]*renew[n-1-j] for j in range(n)))
   ck('renewal_vs_generator_series',direct==renew)
   for q in (F(3,2),F(2),F(3)):
    for x in (F(1,3),F(1),F(2)):
     t=F(20);eps=x/(q*t);tail=eps**a
     ck('tail_integrability_bound',tail/eps<=F(a,a-1)*eps**(a-1))
     ck('late_mutation_power',t*tail==x**a/(q**a*t**(a-1)))
     ck('tail_decay_ratio',(2*t)*(x/(q*2*t))**a/(t*tail)==F(1,2)**(a-1))
   cases+=1
# Gamma antiderivative and shape/rate consistency.
for k in range(1,9):
 for lam in (F(1,3),F(3,4),F(1),F(2)):
  P=[lam**j/F(factorial(j)) for j in range(k)]
  derivative=[(j+1)*P[j+1] for j in range(k-1)]+[F(0)]
  ck('gamma_cdf_derivative',[lam*P[j]-derivative[j] for j in range(k)]==[F(0)]*(k-1)+[lam**k/F(factorial(k-1))])
  for c in (F(1,4),F(1,2),F(3,4),F(1)):
   for q in (F(3,2),F(2),F(3)):
    eta=lam+c*(q-1);small=q**(-k);large=(lam/eta)**k
    ck('ratio_limits_force_clock',(small==large)==(lam==c))
    ck('density_exponent',(lam-eta/q)==(lam-c)*(q-1)/q)
    if lam==c:ck('corrected_growth_ratio',large==q**(-k))
for n in range(1,30):
 for den in range(2,21):
  for j in range(1,den):
   p=F(j,den);u=p*F(2,3)
   normalized_variance=n*(u/p)**2*(1-p)/n**2
   ck('old_clone_variance',normalized_variance<=F(1,n))
# Exact advertised example and its two incompatible ratio limits.
beta=F(1,4);I=F(2);rho=1-beta*I;c=1-beta;q=F(2);lam=F(1);k=2
ck('counterexample_parameters',(rho,c)==(F(1,2),F(3,4)))
ck('counterexample_ratio_constants',(q**(-k),(lam/(lam+c*(q-1)))**k)==(F(1,4),F(16,49)))
ck('counterexample_density_exponent',(lam-c)*(q-1)/q==F(1,8))
ck('counterexample_unequal_limits',F(1,4)!=F(16,49))
root=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((root/'CLOCK_OBSTRUCTION.md').read_bytes()).hexdigest(),'exact_assertions':sum(C.values()),'categories':dict(C),'renewal_parameter_cases':cases,'scope':'Exact renewal/generator Taylor identities, integral constants, Yule variance bounds, mutation-tail exponents and Gamma rate identities. No numerical fits or proof of corrected-profile existence.'}
print(json.dumps(out,indent=2))
