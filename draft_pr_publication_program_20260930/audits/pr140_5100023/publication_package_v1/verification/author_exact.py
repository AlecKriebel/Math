#!/usr/bin/env python3
"""Exact chord identities; no numerical billiard orbits are used as proof."""
from fractions import Fraction as F
from math import gcd
from verification_support import options, emit
args=options(__doc__, ["false-guard"])
checks=0; chords=0; rotation_cases=0

def ck(p):
 global checks
 if not p:raise RuntimeError("Exact verification check failed")
 checks+=1

if args.negative_control == "false-guard":
 ck(False)

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def q(A,B,M):
 r=sub(A,M);s=sub(B,M)
 # q is in absolute coordinates: (Q-M).r=|r|².
 det=r[0]*s[1]-r[1]*s[0]
 ck(det!=0)
 z=((dot(r,r)*s[1]-dot(s,s)*r[1])/det,(r[0]*dot(s,s)-s[0]*dot(r,r))/det)
 Q=tuple(z[j]+M[j] for j in range(2))
 ck(dot(sub(Q,M),r)==dot(r,r));ck(dot(sub(Q,M),s)==dot(s,s))
 return Q

def unit(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))
angles=sorted(set(F(k,d) for d in range(1,9) for k in range(-10,11)))
halves=sorted(set(F(k,d) for d in range(2,14) for k in range(1,d)))
for aa,bb,cc in [(5,3,4),(5,4,3),(13,5,12),(13,12,5),(17,8,15)]:
 a,b,c=F(aa),F(bb),F(cc)
 for t in angles:
  C,S=unit(t)
  for u in halves:
   U,V=unit(u)
   D2=C*C/(a*a)+S*S/(b*b)
   lam=V*V/D2
   if not 0<lam<b*b:continue
   chords+=1
   K=a*a*b*b-lam*c*c
   A=(a*(C*U+S*V),b*(S*U-C*V))
   B=(a*(C*U-S*V),b*(S*U+C*V))
   ck(A[0]**2/a**2+A[1]**2/b**2==1)
   ck(B[0]**2/a**2+B[1]**2/b**2==1)
   ck(A[0]*B[1]-A[1]*B[0]>0)
   ck(U*U==1-lam*D2)
   ck(U*U-c*c*C*C/(a*a)==(b*b-lam)*D2)
   ck(dot(sub(B,A),sub(B,A))==4*a*a*b*b*lam*D2*D2)
   # Derivative of squared chord length when both eccentric angles shift.
   Adot=(-a*(S*U-C*V),b*(C*U+S*V))
   Bdot=(-a*(S*U+C*V),b*(C*U-S*V))
   dl2=2*dot(sub(B,A),sub(Bdot,Adot))
   ck(dl2==8*V*V*c*c*S*C)
   ck(dl2==8*lam*D2*c*c*S*C)
   for sig in [-1,1]:
    h=sig*c;M=(h,F(0))
    Q=q(A,B,M);R=q(neg(A),neg(B),M)
    ck(U>h*C/a)
    ck(Q[0]+R[0]==-2*h+2*h*K*C*C/(a*a*(b*b-lam)))
    ck(Q[1]+R[1]==2*h*K*S*C/(a*b*(b*b-lam)))
    ck(Q[0]+R[0]==2*h*b*b*(C*C-U*U)/(b*b-lam))
   Q=q(A,B,(F(0),F(0)));R=q(neg(A),neg(B),(F(0),F(0)))
   ck(Q==neg(R))
# In the invariant circular coordinate of the written finite-action argument,
# every reduced even-order rotation has odd numerator and half-turn power.
for n in range(4,102,2):
 for m in range(1,n):
  if gcd(m,n)!=1:continue
  rotation_cases+=1
  ck(m%2==1);ck((F(m,n)*(n//2))%1==F(1,2))
# Exact axis-vertex four-periods, independently solving the antipedal systems.
for aa,bb,cc in [(5,3,4),(5,4,3),(13,5,12),(13,12,5),(17,8,15)]:
 a,b,c=map(F,(aa,bb,cc));lam=a*a*b*b/(a*a+b*b)
 P=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
 K=a*a*b*b-lam*c*c
 H=F(1,2)
 ck(-1+K*H/(a*a*(b*b-lam))==0)
 for M in [(F(0),F(0)),(c,F(0)),(-c,F(0))]:
  Q=[q(P[i],P[(i+1)%4],M) for i in range(4)]
  ck(sum(x[0] for x in Q)==0);ck(sum(x[1] for x in Q)==0)
receipt={'assertions':checks,'exact_chords':chords,'reduced_even_rotation_cases':rotation_cases,'method':'Exact rational 2x2 systems and independent chord-length differentiation; finite checks supplement the written all-period proof','status':'PASS'}
emit(receipt,args,__file__)
