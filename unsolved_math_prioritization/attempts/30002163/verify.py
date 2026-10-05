"""Self-authored exact controls and optional high-precision diagnostics.
The proof is in PROOF.md. Finite bounds do not replace its uniform argument.
"""
from fractions import Fraction as F
from math import isqrt
import json
checks=0
sections={}
def ck(x):
 global checks
 assert x
 checks+=1

def mark(name,before): sections[name]=checks-before
fib=[0,1]
for n in range(2,33): fib.append(fib[-1]+fib[-2])
start=checks
for n in range(3,33):
 q,p=fib[n],fib[n-1]
 ck(p*p+p*q-q*q==(-1)**n)
 ck(p*p%q==((-1)**n)%q)
 for m in range(1,isqrt(q)+1):
  if m*m>=q: continue
  rem=m*p%q;s=rem if 2*rem<=q else rem-q;r=abs(s);ell=(m*p-s)//q
  B=ell*ell+ell*m-m*m
  ck(r>0)
  ck(B!=0)
  ck(q*q*B==(-1)**n*m*m-(2*p+q)*m*s+s*s)
  ck(q*q<=m*m+(2*p+q)*m*r+r*r)
  if q>=8 and 4*r<q:
   ck(4*m*r>q)
   ck(q+F(13,16)*q*q<q*q)
mark('Cassini_and_dangerous_residue_controls',start)
start=checks
# Rational latitude algebra, including both pole endpoints.
for q in range(2,42):
 for i in range(q):
  for j in range(i+1,q+1):
   a,b=F(i,q),F(j,q);d=b-a;U=1+d*d-(1-a-b)**2
   ck(U==2*(a+b-2*a*b))
   ck(U-2*d==4*a*(1-b))
   ck(U>=2*d)
   ck(U*U-4*d*d==16*a*(1-a)*b*(1-b))
# Rational parametrization of the relevant hyperbola gives exact square identity.
for m in range(1,10):
 d=F(m,10)
 for u in range(1,25):
  t=F(u,3)+1;U=d*(t+1/t);V=d*(t-1/t)
  for v in range(11):
   c=F(v,10)
   ck(U-c*V>=0)
   ck((U-c*V)**2-4*d*d*(1-c*c)==(V-c*U)**2)
mark('geometric_identities_and_positive_square_roots',start)
start=checks
allpairs=0;cases={'vertical':0,'nonpositive_cosine':0,'positive_cosine':0}
# Every pair for all nontrivial Fibonacci sizes through 610.
for n in range(3,16):
 q,p=fib[n],fib[n-1]
 for i in range(q):
  for j in range(i+1,q):
   m=j-i;r=min(m*p%q,(-m*p)%q)
   if m*m>=q:
    bound=F(4*m*m,q*q);cases['vertical']+=1
   elif 4*r>=q:
    bound=F(4*m,q);cases['nonpositive_cosine']+=1
   else:
    bound=F(16*m*r,q*q);cases['positive_cosine']+=1
   ck(bound>=F(4,q));allpairs+=1
 # Exact north-pole attainment and alternative south-pole attainment.
 ck(4*F(1,q)*(1-F(1,q))+F(4,q*q)==F(4,q))
mark('all_pair_lower_certificates_and_attainment',start)
start=checks
for n in range(3,20):
 q,p=fib[n],fib[n-1]
 for k in range(q):
  # Swapped lattice reindexing and the possible longitude reflection.
  j=k*p%q
  ck(((-1)**n*j*p)%q==k)
  ck(F(k,q)*(1-F(k,q))==F(q-k,q)*(1-F(q-k,q)))
  ck(1-F(2*(q-k),q)==-(1-F(2*k,q)))
mark('endpoint_and_companion_reindexing',start)
print(json.dumps({'status':'PASS','exact_assertions':checks,'section_assertions':sections,
 'all_pair_certificates':allpairs,'all_pair_case_counts':cases,
 'max_all_pair_size':610,'largest_Cassini_size':fib[32],
 'scope':'Exact rational geometry, integer-residue identities and proof-derived finite all-pair lower certificates. Uniform proof and elementary sine/sign facts are in PROOF.md; no floating-point value is used as a certificate.'},indent=2,sort_keys=True))
