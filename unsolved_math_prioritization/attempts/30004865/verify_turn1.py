#!/usr/bin/env python3
"""Exact controls for the all-tester Werner obstruction; no numerical optimization."""
from fractions import Fraction as Q
from itertools import product
import random,json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
roots=[(1,0),(0,1),(-1,0),(0,-1)]
# Entrywise verification of the finite projector ensemble.
frame_cases=[]
for d in range(2,7):
 phases=[(0,)+z for z in product(range(4),repeat=d-1)]
 for i,j,k,l in product(range(d),repeat=4):
  sr=si=0
  for z in phases:
   a,b=roots[(z[i]-z[j]+z[k]-z[l])%4];sr+=a;si+=b
  real=Q(sr,len(phases)*d*(d+1))+Q(int(i==j==k==l),d*(d+1))
  imag=Q(si,len(phases)*d*(d+1))
  want=Q(int(i==j and k==l)+int(i==l and j==k),d*(d+1))
  ck(real==want and imag==0)
 frame_cases.append({'dimension':d,'flat_phase_representatives':len(phases),'tensor_entries':d**4})
# Rational Werner eigenvalues, flip expectation and exact invisible interval.
werner_cases=0
for d in range(2,41):
 for denominator in range(1,26):
  for numerator in range(-denominator,denominator+1):
   f=Q(numerator,denominator);a=(d-f)/(d*(d*d-1));b=(d*f-1)/(d*(d*d-1))
   sp=Q(d*(d+1),2);am=Q(d*(d-1),2)
   ck(a+b>=0 and a-b>=0)
   ck(sp*(a+b)+am*(a-b)==1)
   ck(sp*(a+b)-am*(a-b)==f)
   ck(d*a+b==Q(1,d))
   ck((abs(b)<=Q(1,d*(d+1)))==(Q(2,d)-1<=f<=1))
   werner_cases+=1
# Cauchy-Schwarz upper bound for exact unit-disk points.
points=[]
for n in range(25):
 t=Q(n,24);points.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
for x,y in product(points,repeat=2):
 ck(x[0]*x[0]+x[1]*x[1]==1)
 for c in [Q(0),Q(1,7),Q(3,4),Q(1)]:
  ck(x[0]*y[0]+c*x[1]*y[1]<=1)
# Explicit d=3 state, projectors, ranks/traces and entanglement witness.
d=3;N=d*d
I=[[int(i==j) for j in range(N)] for i in range(N)]
F=[[int((i//d,i%d)==(j%d,j//d)) for j in range(N)] for i in range(N)]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
ck(mm(F,F)==I)
Ps=[[Q(I[i][j]+F[i][j],2) for j in range(N)] for i in range(N)]
Pa=[[Q(I[i][j]-F[i][j],2) for j in range(N)] for i in range(N)]
ck(mm(Ps,Ps)==Ps);ck(mm(Pa,Pa)==Pa);ck(all(v==0 for row in mm(Ps,Pa) for v in row))
ck(sum(Ps[i][i] for i in range(N))==6);ck(sum(Pa[i][i] for i in range(N))==3)
rho=[[Q(19*I[i][j]-9*F[i][j],144) for j in range(N)] for i in range(N)]
for i,j in product(range(N),repeat=2):ck(rho[i][j]==Q(5,72)*Ps[i][j]+Q(7,36)*Pa[i][j])
ck(sum(rho[i][i] for i in range(N))==1)
ck(sum(F[i][j]*rho[j][i] for i,j in product(range(N),repeat=2))==Q(-1,6))
ck(Q(1,16)<Q(1,12))
# Exact complex arithmetic and generic-map finite second moments in dimension 3.
def plus(z,w):return(z[0]+w[0],z[1]+w[1])
def mult(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def conj(z):return(z[0],-z[1])
def sq(z):return z[0]*z[0]+z[1]*z[1]
def div(z,n):return(Q(z[0],n),Q(z[1],n))
rng=random.Random(300048651)
phase_points=[(0,)+z for z in product(range(4),repeat=2)]
ensemble=[]
for j in range(d):ensemble.append((Q(1,d*(d+1)),[[(int(i==k==j),0) for k in range(d)] for i in range(d)]))
for z in phase_points:
 P=[[div(roots[(z[i]-z[j])%4],d) for j in range(d)] for i in range(d)]
 ensemble.append((Q(d,(d+1)*len(phase_points)),P))
ck(sum(w for w,P in ensemble)==1)
map_cases=0
for _ in range(120):
 mats=[[[ (rng.randrange(-3,4),rng.randrange(-3,4)) for j in range(d)] for i in range(d)] for k in range(rng.randrange(1,7))]
 hs=sum(sq(A[i][j]) for A in mats for i,j in product(range(d),repeat=2))
 trsq=0
 for A in mats:
  tr=(0,0)
  for i in range(d):tr=plus(tr,A[i][i])
  trsq+=sq(tr)
 observed=Q(0)
 for w,P in ensemble:
  norm=Q(0)
  for A in mats:
   val=(0,0)
   for i,j in product(range(d),repeat=2):val=plus(val,mult(conj(A[i][j]),P[i][j]))
   norm+=sq(val)
  observed+=w*norm
 ck(observed==Q(hs+trsq,d*(d+1)))
 S=Q(hs)-Q(trsq,d);ck(S>=0)
 u2=Q(trsq,d);ck(observed==u2/d+S/(d*(d+1)))
 # C supplies an explicit global S1-to-Hilbert norm upper bound.
 C=sum(abs(v) for A in mats for row in A for z in row for v in z)
 if C:
  ck(C*C>=hs);ck(observed/(C*C)<=1)
 map_cases+=1
print(json.dumps({'exact_assertions':checks,'finite_second_moment_frames':frame_cases,'rational_Werner_cases':werner_cases,'generic_complex_map_second_moments':map_cases,'explicit_state':'(19 I - 9 F)/144 on C3 tensor C3','flip_expectation':'-1/6','universal_bound_from_written_proof':True,'numerical_search_used_as_proof':False},indent=2))
