#!/usr/bin/env python3
"""Exact dyadic algebra controls and an independent finite-field certificate; stdlib only."""
from itertools import product
from collections import Counter
from fractions import Fraction
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def mul(a,b,mod=None):
 c=[0]*9
 for i in range(5):
  for j in range(5):c[i+j]+=a[i]*b[j]
 for k in range(8,4,-1):c[k-5]-=c[k];c[k-4]-=2*c[k]
 return tuple(x%mod if mod else x for x in c[:5])
def val(n):
 if not n:return 10**9
 n=abs(n);t=0
 while n%2==0:n//=2;t+=1
 return t
def criterion(M,N):
 if not N:return False
 v=val(N)
 return v%2==0 and val(M)>=v+3 and (N//2**v)%8==1
linear_primitive=0
for a in product(range(8),repeat=5):
 q=mul(a,a,8)
 if any(x%2 for x in a):
  ck(any(x%2 for x in q),'reduced_mod2_no_square_nilpotents')
  if q[2:]==(0,0,0):
   ck(q[:2]==(1,0),'primitive_linear_square_mod8');linear_primitive+=1
 # Exact theta-square coefficient, independent of generic multiplication reduction.
 exact=mul(a,a)
 formula=2*a[0]*a[2]+a[1]**2-4*a[2]*a[4]-2*a[3]**2-2*a[3]*a[4]
 ck(exact[2]==formula,'coefficient_theta2_identity')
# F16 = F2[X]/(X^4+X^3+X^2+X+1).
def fm(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&16:a^=31
 return c
def tr(a):
 z=a;t=0
 for _ in range(4):t^=z;z=fm(z,z)
 return t
ck(tr(2)==1 and tr(1)==0,'trace_of_theta_and_one')
for a in range(16):ck(tr(fm(a,a)^a)==0,'artin_schreier_trace_zero')
# Fixed precision root construction for primitive admissible linear elements.
P=24;mod=2**P;root_cases=0
for M,N in product(range(-24,25,8),range(-15,18,8)):
 ck(criterion(M,N),'admissible_linear_unit')
 h=((N-1)//8,M//8,0,0,0);u=(0,)*5
 for _ in range(P):
  z=mul(u,u,mod);u=tuple((h[i]-2*z[i])%mod for i in range(5))
 beta=tuple(((1 if i==0 else 0)+4*u[i])%mod for i in range(5))
 ck(mul(beta,beta,mod)==(N%mod,M%mod,0,0,0),'contractive_root_mod_2power');root_cases+=1
quadratics=0;obstructed=0
for a,b,c in product(range(-16,17),range(-16,17),range(-3,4)):
 if not a:continue
 M=4*a;N=b*b-4*a*c
 yes=b!=0 and val(a)>2*val(b)
 ck(criterion(M,N)==yes,'integer_quadratic_exact_valuation_equivalence')
 quadratics+=1;obstructed+=not yes
# Mod-11 irreducibility certificate with independent polynomial arithmetic.
p=11
def trim(a):
 a=list(a)
 while a and not a[-1]:a.pop()
 return a
def rem(a,b):
 a=trim([x%p for x in a]);b=trim(b);iv=pow(b[-1],-1,p)
 while len(a)>=len(b):
  k=len(a)-len(b);r=a[-1]*iv%p
  for i in range(len(b)):a[k+i]=(a[k+i]-r*b[i])%p
  a=trim(a)
 return a
def pm(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return trim(c)
def power(a,n,F):
 r=[1]
 while n:
  if n&1:r=rem(pm(r,a),F)
  n//=2;a=rem(pm(a,a),F)
 return r
def gcd(a,b):
 while b:a,b=b,rem(a,b)
 return [(x*pow(a[-1],-1,p))%p for x in a]
h=[1,2,4,0,0,1,10,40,80,80,32];F=[x%p for x in h];iv=pow(F[-1],-1,p);F=[x*iv%p for x in F]
residues={};z=[0,1]
for n in range(1,11):
 z=power(z,11,F)
 if n in (2,5,10):residues[n]=z
ck(residues[10]==[0,1],'rabin_full_power_degree10')
for n in (2,5):
 v=residues[n]+[0]*(max(2,len(residues[n]))-len(residues[n]));v[1]=(v[1]-1)%p
 ck(gcd(F,trim(v))==[1],'rabin_prime_divisor_gcd')
# Independently compose integer polynomial to check displayed example.
def im(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
q=[1]
for _ in range(5):q=im(q,[0,1,2])
q[0]+=1;q[1]+=2;q[2]+=4
ck(q==h,'exact_integer_composition')
print(json.dumps({'status':'PASS','arithmetic':'exact integers, finite rings and finite fields; standard library only','assertions':sum(C.values()),'by_scope':dict(C),'A_mod8_vectors':8**5,'primitive_linear_square_vectors':linear_primitive,'contractive_root_cases':root_cases,'root_precision_bits':P,'integer_quadratics':quadratics,'dyadically_obstructed_quadratics':obstructed,'mod11_example':{'integer_coefficients_low_to_high':h,'monic_mod11':F,'frobenius_residues':residues},'scope':'Exact finite controls support the written theorem. The complementary dyadically split class remains globally unresolved, and no full degree-five solution is claimed.'},indent=2,sort_keys=True))
