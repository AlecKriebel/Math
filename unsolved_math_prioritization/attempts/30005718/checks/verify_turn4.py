#!/usr/bin/env python3
"""Exact bounded controls for the analytic endpoint argument.
No finite control certifies an unspecified analytic threshold.
"""
from fractions import Fraction as F
from math import factorial
from collections import Counter
import json
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
B=69
def plus(*ps):
 out=[F(0)]*max(map(len,ps))
 for p in ps:
  for i,c in enumerate(p):out[i]+=c
 return out
def times(p,q,limit=B):
 out=[F(0)]*min(len(p)+len(q)-1,limit+1)
 for i,a in enumerate(p):
  for j,b in enumerate(q[:max(0,limit+1-i)]):out[i+j]+=a*b
 return out
def invert(p,limit=B):
 out=[1/p[0]]
 for k in range(1,limit+1):out.append(-sum(p[i]*out[k-i] for i in range(1,min(len(p),k+1)))/p[0])
 return out
def scale(p,a):return [a*x for x in p]
def coef(p,k):return p[k] if 0<=k<len(p) else 0
# All coefficients are rational in x=sqrt(w).
sqrt=[F(0)]*(B+1);q=F(1)
for j in range(B//2+1):
 sqrt[2*j]=q*F(5,4)**j
 q=q*(F(1,2)-j)/(j+1)
ck(times(sqrt,sqrt)==[F(1),0,F(5,4)]+[F(0)]*(B-2),'square_root_identity')
L=plus(sqrt,[0,F(3,2),0,1]);kap=times(L,L)
E=plus([0,2,0,2],scale(times([1,0,6,0,6],invert(sqrt)),F(1,2)))
O=times(E,L)
ck(kap[0]==1 and kap[1]==3 and E[0]==O[0]==F(1,2),'upper_analytic_hypotheses')
# Direct original three-state recurrence, independent of the parity formula.
def zshift(p,k):return [0]*k+p
def addpoly(*ps):
 z=[0]*max(map(len,ps))
 for p in ps:
  for i,c in enumerate(p):z[i]+=c
 while len(z)>1 and z[-1]==0:z.pop()
 return z
T=[0,0,0,2,1];Q=[0,0,0,0,1];S=[0,0,0,2,2];rows={}
for n in range(4,166):
 rows[n]=addpoly(T,Q,S)
 T,Q,S=addpoly(zshift(T,1),Q,zshift(Q,1),S,zshift(S,1)),addpoly(Q,zshift(Q,1),zshift(S,1)),addpoly(zshift(T,1),zshift(T,2),S,zshift(S,1))
power=[F(1)]
for r in range(81):
 pe=times(E,power);po=times(O,power)
 for delta,series,n in [(1,pe,2*r+4),(0,po,2*r+5)]:
  row=rows[n];degree=len(row)-1
  for h in range(17):
   ck(2*coef(series,2*h+delta)==coef(row,degree-h),'exact_upper_parity_coefficients')
  if r<=9:
   for h in range(degree+3):
    if 2*h+delta<=B:ck(2*coef(series,2*h+delta)==coef(row,degree-h),'full_small_parity_rows_including_zeros')
 power=times(power,kap)
# Reproduce the upper fixed-h leading coefficient through the linear-power term.
for h in range(16):
 ck(2*E[0]*3**(2*h+1)/factorial(2*h+1)==F(3**(2*h+1),factorial(2*h+1)),'even_leading_tail_constant')
 ck(2*O[0]*3**(2*h)/factorial(2*h)==F(3**(2*h),factorial(2*h)),'odd_leading_tail_constant')
# Exact quadratic field arithmetic for the lower inverse-variance limit.
def qa(a,b=(0,0)):return (a[0]+b[0],a[1]+b[1])
def qm(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def qi(a):
 n=a[0]**2-5*a[1]**2
 return a[0]/n,-a[1]/n
def qs(a,b):return qa(a,(-b[0],-b[1]))
def qd(a,b):return qm(a,qi(b))
A=(F(3,2),F(1,2));rt=(F(0),F(1));D=qs((F(1,3),F(0)),qd((F(2),F(0)),qm(rt,qm(A,A))))
ck(D==qd((F(3),F(7)),(F(45),F(21))),'lower_gap_limit_identity')
ck(all(x>0 for x in [F(3),F(7),F(45),F(21)]),'lower_gap_limit_positive_certificate')
# Construct the first TWO saddle corrections directly by formal exponential
# multiplication. Powers of i are restored after integration of each even monomial.
def bmul(a,b):
 out=Counter()
 for (e,y),x in a.items():
  for (f,z),v in b.items():
   if e+f<=4:out[e+f,y+z]+=x*v
 return dict(out)
def correction(nu,hs,cs):
 phase={(l-2,l):cs[l]/factorial(l) for l in range(3,7)}
 ex={(0,0):F(1)};pow={(0,0):F(1)}
 for n in range(1,5):
  pow=bmul(pow,phase)
  for key,v in pow.items():ex[key]=ex.get(key,F(0))+v/factorial(n)
 amp={(l,l):hs[l]/factorial(l) for l in range(5)};out=Counter()
 for (eps,y),v in bmul(amp,ex).items():
  if y%2:continue
  moment=F(1)
  for k in range(1,y,2):moment*=k/nu
  out[eps]+=(-1)**(y//2)*v*moment
 return out
cases=0
for nu,h1,h2,c3,c4 in __import__('itertools').product([F(1,2),F(1),F(3,2)], [F(-2),F(0),F(3)], [F(-1),F(2)], [F(-2),F(1),F(4)], [F(-3),F(1)]):
 hs={0:F(1),1:h1,2:h2,3:F(2,3),4:F(-7,5)};cs={3:c3,4:c4,5:F(-3,2),6:F(5,3)}
 out=correction(nu,hs,cs)
 formula=-h2/(2*nu)+h1*c3/(2*nu**2)+c4/(8*nu**2)-5*c3*c3/(24*nu**3)
 ck(out[2]==formula,'first_gaussian_correction_formula')
 ck(out[0]==1 and out[1]==out[3]==0,'odd_gaussian_orders_cancel')
 cases+=1
out=correction(F(1),{0:F(1),1:F(0),2:F(0),3:F(0),4:F(0)},{l:F(1) for l in range(3,7)})
ck(out[2]==F(-1,12),'poisson_first_correction')
ck(out[4]==F(1,288),'poisson_second_correction')
# Binomial normalization shift is log(1+4t)-log(1+3t).
ck(F(4-3)==1 and -F(4**2-3**2,2)==-F(7,2),'lower_shift_seven_halves')
ck(-F(1,2)+F(7,2)==3,'lower_normalized_margin_three')
for h in range(5,10001):
 for delta in [0,1]:ck(F(4)/(F(6,5)*(2*h+delta))>=F(3,2*h),'uniform_upper_curvature_constant')
 ck(F(1,h)+F(1,11*h)==F(12,11*h),'upper_binomial_curvature_constant')
ck(F(7,5)-F(12,11)==F(17,55)>0,'strict_upper_margin_constant')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact parity/endpoint/Gaussian algebra controls only; the uniform analytic estimates are proved in TURN_4 and no effective global threshold is inferred.'},indent=2,sort_keys=True))
