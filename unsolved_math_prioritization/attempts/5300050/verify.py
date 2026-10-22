#!/usr/bin/env python3
"""Exact algebraic controls; entropy limits are proved in PARTIAL.md."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
N=0

def check(b):
 global N
 assert b
 N+=1

def add(z,w): return z[0]+w[0],z[1]+w[1]
def sub(z,w): return z[0]-w[0],z[1]-w[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm(z): return z[0]**2+z[1]**2
def div(z,w):
 t=norm(w)
 return (z[0]*w[0]+z[1]*w[1])/t,(z[1]*w[0]-z[0]*w[1])/t
one=(Q(1),Q(0))
def scale(a,z): return a*z[0],a*z[1]
def B(a,z): return div(mul(z,sub(z,(a,0))),sub(one,scale(a,z)))
def deriv(a,z):
 # Quotient-rule derivative, evaluated independently of angular formula.
 num=mul(z,sub(z,(a,0))); den=sub(one,scale(a,z))
 return div(add(mul(sub(scale(2,z),(a,0)),den),scale(a,num)),mul(den,den))
parameters=[Q(1,3),Q(1,2),Q(2,3),Q(1,4),Q(3,4),Q(2,5),Q(3,5),Q(4,5)]
for t in parameters:
 a=2*t/(1+t*t); b=(1-t*t)/(1+t*t); A=1+b
 check(a*a+b*b==1 and 0<a<1 and 0<t<1)
 check(A*(1+t*t)==2 and A*t==a)
 check(1<A<2) # strict harmonic/topological entropy gap
 check(deriv(a,(t,0))==(0,0) and deriv(a,(1/t,0))==(0,0))
 check(B(a,(t,0))==(-t*t,0))
 check(deriv(a,(0,0))==(-a,0))
 for k in range(-20,21):
  r=Q(k,7); z=((1-r*r)/(1+r*r),2*r/(1+r*r))
  check(norm(z)==1)
  v=B(a,z); check(norm(v)==1)
  angular=div(mul(z,deriv(a,z)),v)
  D=1+(1-a*a)/(1-2*a*z[0]+a*a)
  check(angular==(D,0))
  check(Q(2)/(1+a)<=D<=Q(2)/(1-a))
  check(D==A*norm(sub(one,scale(t,z)))/norm(sub(one,scale(a,z))))
 for i in range(-4,5):
  for j in range(-4,5):
   z=Q(i,5),Q(j,5)
   if 0<norm(z)<1:
    check(norm(B(a,z))<norm(z))
    w=Q(i,5),Q(j,5)
    # Reflection controls rationally sample the outside dynamics as well.
    zinv=div(one,(w[0],-w[1]))
    if norm(B(a,w))==0:
     check(sub(one,scale(a,zinv))==(0,0)) # image is infinity on the sphere
    else:
     check(B(a,zinv)==div(one,(B(a,w)[0],-B(a,w)[1])))
     check(norm(B(a,zinv))>1)
a=Q(3,5)
check(Q(2)/(1+a)==Q(5,4) and Q(2)/(1-a)==5)
check(1+Q(4,5)==Q(9,5) and 1+Q(4,5)<2)
# The full shift/doubling comparator: exact inverse images and itineraries.
for n in range(1,9):
 den=2**n
 pre=[Q(2*j+1,2*den) for j in range(den)]
 words=set()
 for x in pre:
  y=x; word=[]
  for k in range(n):
   digit=int(2*y);word.append(digit);y=2*y-digit
  check(y==Q(1,2))
  check(all(d in (0,1) for d in word))
  words.add(tuple(word))
 check(len(words)==den)
# Explicit formula for non-uniform expansion degenerating only at a=1.
for n in range(2,31):
 t=Q(n-1,n); a=2*t/(1+t*t); b=(1-t*t)/(1+t*t)
 check(1<1+b<2 and Q(2)/(1+a)>1)
root=Path(__file__).resolve().parent
result={'status':'PASS','assertions':N,'method':'standard-library exact rational complex arithmetic; no entropy limit inferred from finite tests','families':{'blaschke_parameters':len(parameters),'circle_points_per_parameter':41,'doubling_depths':8},'artifact_sha256':hashlib.sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':['The general basin-boundary entropy question remains unresolved.','Measure entropy and topological entropy are justified analytically in the accompanying proof, not estimated numerically.']}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
