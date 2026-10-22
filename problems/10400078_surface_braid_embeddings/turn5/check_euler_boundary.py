#!/usr/bin/env python3
import itertools,json
from fractions import Fraction
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def mul(a,b,N):
 c=[Fraction(0)]*(N+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<=N:c[i+j]+=x*y
 return c
def inv(a,N):
 b=[Fraction(0)]*(N+1);b[0]=1/a[0]
 for k in range(1,N+1):b[k]=-sum(a[j]*b[k-j] for j in range(1,k+1))/a[0]
 return b
def power(a,e,N):
 if e<0:a=inv(a,N);e=-e
 z=[Fraction(1)]+[Fraction(0)]*N
 for _ in range(e):z=mul(z,a,N)
 return z
for g,d,c in itertools.product(range(2,11),range(1,9),(-3,-2,-1,1,2,3)):
 a=[Fraction(1)]+[Fraction(0)]*d;a[d]=c;e=2-2*g
 z=power(a,e,d);ck(z[d]==e*c);ck(z[d]!=0)
# Ordered Laurent supports: independent extrema confirm no inverse in a finite box
# for a small sample of genuine two-term elements. This is only a commutative control.
for a,b in itertools.combinations(range(-3,4),2):
 for c,d in itertools.combinations(range(-3,4),2):ck((a+c,b+d)[0]<(a+c,b+d)[1])
print(json.dumps({'assertions':checks,'Euler_leading_term_cases':9*8*6,'scope':'Scalar leading-power and ordered-support controls only; surface-group orderability, centralizers, circle Euler class and the finite-orbit lemma are proved or cited analytically.'},indent=2))
