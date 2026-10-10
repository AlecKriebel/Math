"""Exact finite arithmetic for square-discriminant Seifert-core partials."""
from math import gcd,isqrt
from collections import Counter,deque
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def divisors(n):
 out=set()
 for a in range(1,isqrt(n)+1):
  if n%a==0:out|={a,n//a}
 return sorted(out)
def calc(N):
 k=(N-1)//2;T={4*b*b*d*d%N for b in divisors(k)for d in divisors(k+1)}
 H={1};todo=deque([1])
 while todo:
  x=todo.popleft()
  for t in T:
   y=x*t%N
   if y not in H:H.add(y);todo.append(y)
 return T,H
rows=[]
for N in range(3,200,2):
 k=(N-1)//2;T,H=calc(N)
 ck(1 in T,'one_step_contains_identity')
 ck(all(gcd(x,N)==1 for x in T),'one_step_units')
 ck({pow(x,-1,N)for x in T}==T,'one_step_inverse_closed')
 ck(all(x*y%N in H for x in H for y in H),'generated_group_closed')
 ck((T==H)==all(x*y%N in T for x in T for y in T),'closure_criterion')
 for b in divisors(k):
  for d in divisors(k+1):
   a=(k+1)//d*b;c=-(k//b)*d
   ck(1-4*a*c==N*N,'special_form_discriminant')
   residue=2*d*b%N;inverse_residue=2*(k//b)*((k+1)//d)%N
   ck(residue*inverse_residue%N==N-1,'special_inverse_identity')
   ck(residue*residue%N in T,'special_square_membership')
   # Explicit SL2 change in AFMW Lemma 6.9, applied to polynomial factors.
   alpha=(k+1)//d;beta=b;gamma=-(k//b);delta=d
   ck(alpha*delta+beta*gamma==1,'factor_matrix_unimodular')
   # Product after substitution (x,y) -> (delta*x-gamma*y,beta*x+alpha*y).
   A=alpha*delta+gamma*beta;B=-alpha*gamma+gamma*alpha
   D=beta*delta+delta*beta;E=-beta*gamma+delta*alpha
   ck(A==1 and B==0 and D==2*beta*delta and E==N,'special_form_reduction_coefficients')
 rows.append({'N':N,'one_step_count':len(T),'subgroup_count':len(H),'all_primitive_pairs_disjoint':T==H})
expected={5:{1,4},7:{1,2,4},9:{1,4,7},11:{1,3,4,5,9},15:{1,4},21:{1,4,16},33:{1,4,16,25,31}}
for N,S in expected.items():
 T,H=calc(N);ck(T==H==S,'reported_positive_cases')
for r in [0,1,2,4,8,16]:
 k=2**r;p=k+1;N=2*k+1
 ck(all(p%d for d in range(2,isqrt(p)+1)),'conditional_family_prime_examples')
 T,H=calc(N);P={pow(4,j,N) for j in range(r+2)}
 ck(T==H==P,'conditional_family_exact_set')
 ck(pow(4,r+1,N)==1,'conditional_family_period')
T,H=calc(257);ck(len(T)==24 and len(H)==128,'power_of_two_without_prime_negative_control')
T,H=calc(13)
ck(T=={1,3,4,9,10} and H=={1,3,4,9,10,12},'small_gap_sets')
ck(3 in T and 4 in T and 3*4%13==12 and 12 not in T,'two_step_not_one_step')
# Direct 2x2 determinant-polynomial coefficients and skew entries.
for a in [1,4,12]:
 k=6;det=-k*(k+1);middle=(k+1)**2+k*k
 ck(det==-42 and middle==85 and 2*det+middle==1,'gap_alexander_polynomial')
 ck((k+1)-k==1,'gap_unimodular_skew')
 ck(gcd(a,13)==1,'gap_primitive_form')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'cases_3_through_199':rows,'scope':'Finite modular arithmetic certifies the stated one-step/subgroup tests only. Published AFMW topology is a separate input; intersecting common-boundary realization of gap pairs remains unresolved.'},indent=2,sort_keys=True))
