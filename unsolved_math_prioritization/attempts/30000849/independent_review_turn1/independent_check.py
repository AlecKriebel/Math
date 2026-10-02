#!/usr/bin/env python3
"""Independent finite algebra controls; no claim to compute infinite ODEs."""
from fractions import Fraction as F
from collections import defaultdict,Counter
from itertools import product
import json
counts=Counter()
def ck(x,k):
 counts[k]+=1
 if not x:raise AssertionError((k,counts[k]))

def moment_coefficients(n,k):
 # Construct the entire vector field as formal monomer/cluster products.
 # Keys are (rate,cluster index) multiplying c1*c_index.
 rows=[defaultdict(int) for _ in range(n)]
 rows[0][('unit',1)]-=1
 for i in range(1,n+1):rows[0][('a',i)]-=1
 for j in range(2,n+1):
  rows[j-1][('b',j)] +=1  # birth multiplies c1*c_(j-1)
  rows[j-1][('a',j)] -=1
 result=defaultdict(int)
 for j,row in enumerate(rows,1):
  for (rate,index),v in row.items():
   cluster=index-1 if rate=='b' else index
   result[(rate,index,cluster)]+=j**k*v
 return {z:v for z,v in result.items() if v}

def replace_standard(coeff):
 result=defaultdict(int)
 for (rate,index,cluster),v in coeff.items():
  if rate=='b':rate,index='a',index-1
  if rate=='a' and index==1:rate='unit'
  result[(rate,index,cluster)]+=v
 return {z:v for z,v in result.items() if v}

for n in range(2,101):
 for k in (1,2,3):
  coeff=moment_coefficients(n,k)
  expected={('unit',1,1):-1,('a',1,1):-1}
  for i in range(2,n+1):expected[('a',i,i)]=-(1+i**k)
  for j in range(2,n+1):expected[('b',j,j-1)]=j**k
  ck(coeff==expected,'full_polynomial_moment_identity')
  physical=replace_standard(coeff)
  exp={('unit',1,1):2**k-2,('a',n,n):-(1+n**k)}
  if exp[('unit',1,1)]==0:del exp[('unit',1,1)]
  for i in range(2,n):
   c=(i+1)**k-i**k-1
   if c:exp[('a',i,i)]=c
  ck(physical==exp,'standard_stoichiometric_cancellation')
  if k==1:ck(physical=={('a',n,n):-(n+1)},'first_moment_boundary_flux')
  if k==2:
   ck(physical.get(('unit',1,1))==2,'second_moment_dimer_term')
   ck(physical[('a',n,n)]==-(n*n+1),'second_moment_boundary_flux')
 # Direct evaluation at arbitrary rational coefficients/concentrations.
 rates=[F(1)]+[F(i+3,i+1) for i in range(2,n+1)]
 births={j:F(j+2,2*j+1) for j in range(2,n+1)}
 c=[F(j+1,3*j+2) for j in range(1,n+1)]
 rhs=[F(1)-c[0]**2-c[0]*sum(a*x for a,x in zip(rates,c))]
 rhs += [births[j]*c[0]*c[j-2]-rates[j-1]*c[0]*c[j-1] for j in range(2,n+1)]
 direct=sum(j*rhs[j-1] for j in range(1,n+1))
 telescoped=1+(2*births[2]-2)*c[0]**2+c[0]*sum(((i+1)*births[i+1]-(i+1)*rates[i-1])*c[i-1] for i in range(2,n))-(n+1)*rates[n-1]*c[0]*c[n-1]
 ck(direct==telescoped,'rational_direct_vector_field')

# Irrational p=1/4 coefficients are compared by positive fourth powers.
for j in range(2,1001):
 ck(j < j**4*(j-1),'printed_birth_below_standard')
 ck(j < j**4*(j-1),'printed_mass_coefficient_negative')
 ck((j+1)**4<=16*j**4,'boundary_factor_two')
 ck(j<=j**4,'rate_below_mass_weight')
 ck(j**5<=j**8,'second_moment_rate_bound')
for L in range(1,33):
 for j in range(L+1,4*L+2):
  ck((L+1)**3<=j**3,'monomer_tail_power_bound')
  ck(L+1<=j,'mass_tail_second_moment_bound')

p=F(1,4);w=F(0);r=(1-w*(1-p))/((2+w)*(1-p));s=(2+w)/(3-2*p)
ck((r,s)==(F(2,3),F(4,5)),'source_exponents')
ck(r+p==F(11,12)<3,'zero_data_admissible_decay')
q=1-r+1/s
ck(q==F(19,12),'individual_integral_exponent')
ck(q+1==F(31,12),'band_integral_exponent')
ck(2/s==F(30,12),'mass_budget_exponent')
ck(q+1-2/s==F(1,12)>0,'strict_exponent_contradiction')
ck(s*(2-r)==F(16,15)>1,'equivalent_mass_condition')
ck(2-1/s==F(3,4),'scope_boundary_not_convergence_claim')
# The chain-rule exponents in t_j' and the rescaled concentration.
for invs in [F(1,2),F(3,4),F(5,4),F(2),F(7,3)]:
 for rr in [F(-2),F(0),F(2,3),F(3,4),F(4)]:
  for beta in [F(0),F(1),F(3,2),F(4)]:
   lower=2-rr+invs;upper=(beta+1)*invs
   ck((lower>upper)==((2-rr)/invs>beta),'Fatou_exponent_equivalence')
# Exact common-window bounds using s=4/5: compare fourth powers of times.
for K in [F(1,3),F(1),F(7,2)]:
 a,b=F(1,4),F(1,2)
 for n in range(1,21):
  lower=(F(n)/(K*b))**5;upper=(F(2*n)/(K*a))**5
  for j in range(n,2*n):
   start=(F(j)/(K*b))**5;end=(F(j)/(K*a))**5
   ck(lower<=start<=end<=upper,'common_time_window')
# Finite band lower bound for rational powers with denominators<=5.
for num in range(-8,9):
 for den in range(1,6):
  for n in range(1,13):
   # Raise every positive comparison to den, avoiding algebraic floats.
   for j in range(n,2*n):
    left=F(j,n)**num;right=F(1) if num>=0 else F(2)**num
    ck(left>=right,'real_exponent_band_bound')

print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'floating_point_used':False,'scope':'Independent finite moment identities, exact coefficient inequalities and change-of-variable exponent controls. Infinite-system existence and Fatou/source scope are separately audited in the written report.'},indent=2,sort_keys=True))
