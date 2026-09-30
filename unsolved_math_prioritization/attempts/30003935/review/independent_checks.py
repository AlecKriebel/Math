#!/usr/bin/env python3
"""Independent exact controls, with no stochastic simulation or asymptotic inference."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
Cts={}
def ck(v,k):
 assert v,k
 Cts[k]=Cts.get(k,0)+1

def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def mv(A,v):return tuple(sum((x*y for x,y in zip(row,v)),F(0)) for row in A)
def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(a,A):return [[a*x for x in r] for r in A]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def inv2(A):
 a,b=A[0];c,d=A[1];det=a*d-b*c
 assert det
 return [[d/det,-b/det],[-c/det,a/det]]
def n2(v):return sum((x*x for x in v),F(0))
def hs2(A):return sum((n2(row) for row in A),F(0))
def psd2(A):return A==tr(A) and A[0][0]>=0 and A[1][1]>=0 and A[0][0]*A[1][1]-A[0][1]*A[1][0]>=0

def cov(U,V):
 J=len(U);p=len(U[0]);k=len(V[0]);um=[sum(u[a] for u in U)/J for a in range(p)];vm=[sum(v[a] for v in V)/J for a in range(k)]
 C=[[sum((u[a]-um[a])*(v[b]-vm[b]) for u,v in zip(U,V))/J for b in range(k)] for a in range(p)]
 S=[[sum((v[a]-vm[a])*(v[b]-vm[b]) for v in V)/J for b in range(k)] for a in range(k)]
 return C,S

def H(u):return (u[0]/(1+u[0]**2),(u[1]+u[2])/(1+(u[1]+u[2])**2))
L=[[F(2),F(1)],[F(1),F(3)]];Gamma=mm(L,L);Li=inv2(L);z=(F(2,3),F(-1,5));M2=F(1,2)
ensembles=0
for J in (2,3,4,5):
 for seed in range(15):
  U=[tuple(F(((seed+2)*(j+1)+a*a)%9-4,2) for a in range(3)) for j in range(J)]
  V=[H(u) for u in U];C,S=cov(U,V);ensembles+=1;U2=sum((n2(u) for u in U),F(0))
  ck(all(n2(v)<=M2 for v in V),'bounded_nonlinear_forward')
  ck(hs2(C)<=M2*U2/J,'covariance_growth')
  ck(psd2(S) and psd2(add(scale(M2,eye(2)),scale(-1,S))),'covariance_psd_bound')
  rawV=[mv(L,v) for v in V];Cup,Cpp=cov(U,rawV)
  ck(mm(Cup,Li)==C and mm(mm(Li,Cpp),Li)==S,'whitened_covariances')
  for h in (F(1,20),F(1,7),F(1,2),F(1)):
   R=inv2(add(eye(2),scale(h,S)));K=mm(C,R)
   ck(mm(mm(Cup,inv2(add(Gamma,scale(h,Cpp)))),L)==K,'noncommuting_gain_whitening')
   ck(psd2(add(eye(2),scale(-1,mm(R,R)))),'resolvent_contraction')
   ck(add(R,scale(h,mm(S,R)))==eye(2),'resolvent_consistency')
   ck(J*hs2(K)<=M2*U2,'stacked_diffusion_growth')
   dif=add(K,scale(-1,C));ck(J*hs2(dif)<=h*h*M2**3*U2,'stacked_diffusion_consistency')
   f=[mv(K,tuple(a-b for a,b in zip(z,v))) for v in V]
   bound=2*M2*(n2(z)+M2)*U2
   ck(sum((n2(a) for a in f),F(0))<=bound,'stacked_drift_growth')
   df=[mv(dif,tuple(a-b for a,b in zip(z,v))) for v in V]
   ck(sum((n2(a) for a in df),F(0))<=h*h*M2*M2*bound,'stacked_drift_consistency')
  # Resolvent difference formula on two genuinely different covariance matrices.
  V2=[H(tuple(a+F(j+1,7) for a in u)) for j,u in enumerate(U)]
  _,S2=cov(U,V2);h=F(1,3);R1=inv2(add(eye(2),scale(h,S)));R2=inv2(add(eye(2),scale(h,S2)))
  ck(add(R1,scale(-1,R2))==scale(h,mm(mm(R1,add(S2,scale(-1,S))),R2)),'local_resolvent_identity')
  for flag in (0,1):
   Uflag=[tuple(flag*a for a in u) for u in U];Cf,Sf=cov(Uflag,[H(u) for u in Uflag])
   ck(Cf==scale(flag,C),'initial_event_pasting')

# Finite and endpoint-moment controls: qth moment exists without any higher one.
# The infinite law has masses 2^(-q k)/(k(k+1)), k>=1, and remaining mass at 0.
for q in (2,3,4):
 for K in range(1,65):
  mass=sum((F(1,2**(q*k)*k*(k+1)) for k in range(1,K+1)),F(0))
  moment=sum((F(1,k*(k+1)) for k in range(1,K+1)),F(0))
  ck(mass<1,'heavy_initial_probability')
  ck(moment==F(K,K+1),'endpoint_moment_truncation')
  ck(1-moment==F(1,K+1),'endpoint_moment_tail')

# Independent scalar Gaussian calculation from empirical covariances.
energy_cases=0
for R in range(1,25):
 for a in (F(7,2),F(4),F(5),F(8)):
  U=[(F(R),),(-a*R,)];V=[(F(R),),(F(0),)];C,S=cov(U,V);c=C[0][0];s=S[0][0]
  ck(c==(1+a)*R*R/4 and s==F(R*R,4),'ramp_covariance')
  LV=-2*R*R*c+2*c*c
  ck(LV==(1+a)*(a-3)*R**4/8,'generator_quartic')
  for h in (F(1,11),F(1,3),F(1,R**4)):
   gain=c/(1+h*s);means=(R-h*gain*R,-a*R);variance=h*gain*gain
   direct=sum(x*x for x in means)+2*variance-(1+a*a)*R*R
   claimed=h*R**4*((1+a)*(a-3)/8+h*R*R*(1+a)*(a-1)/16)/(1+h*R*R/4)**2
   ck(direct==claimed and direct>0,'exact_gaussian_energy');energy_cases+=1
# Closed-form growth ratio for a=5,h=R^-4 after dividing by R^2.
for R in range(1,65):
 h=F(1,R**4);delta=F(3,2)*(1+F(1,R*R))/(1+F(1,4*R*R))**2
 normalized=delta/(h*(1+26*R*R)*R*R)
 target=F(3,2)*(1+F(1,R*R))/((1+F(1,4*R*R))**2*(26+F(1,R*R)))
 ck(normalized==target,'one_step_bound_obstruction')

C,S=cov([(F(0),),(F(1,2),)],[(F(1),),(F(0),)])
ck(C==[[-F(1,8)]] and S==[[F(1,4)]],'compact_support_diagnostic')
for k in range(1,50):
 h=F(1,k);gain=C[0][0]/(1+h*S[0][0]);mu=-h*gain;var=h*gain*gain
 ck(mu==h/(8*(1+h/4)) and var==h/(64*(1+h/4)**2)>0,'nondegenerate_gaussian_step')

root=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(Cts.values()),'categories':Cts,'bounded_forward_ensembles':ensembles,'scalar_energy_cases':energy_cases,'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact covariance/gain/moment algebra and initial-tail controls only. Stochastic strong convergence is audited analytically; no finite experiment establishes it or disproves general nonlinear convergence.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
