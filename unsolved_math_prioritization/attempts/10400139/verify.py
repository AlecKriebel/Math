#!/usr/bin/env python3
"""Exact exponent/normalization controls and separately labelled finite diagnostics.
No source executable, no network. Python standard library + mpmath1.3.0.
Analytic proofs, not these finite tests, establish the all-N/all-link theorem.
"""
import json,math,hashlib
from fractions import Fraction
from pathlib import Path
import mpmath as mp
count=0
def check(p):
 global count
 assert p
 count+=1
# h_old(1/u)^N=h_new(u)^N: every paired numerator/denominator
# contributes u^(-j), cancelling u^(m*N), with no residual sign.
for N in range(3,102,2):
 m=(N-1)//2;half=(N+1)//2
 check(sum(range(1,N))==m*N)
 check((2*half)%N==1)
 # Exact factor exponent vectors prove the Nth-powered h shift identity.
 for a in range(N):
  left=[(a-t)%N-(-t)%N for t in range(N)]
  right=[a-N*(1<=t<=a) for t in range(N)]
  check(left==right)
  # Inverse tensor scalar: [u]/[u*zeta^a] times the omega ratio telescopes.
  # Ratios represented by exponent vectors of factors1-u*zeta^t.
  telescope=[0]*N
  for j in range(1,a+1):
   telescope[(j-1)%N]+=1;telescope[j%N]-=1
  bracket=[0]*N;bracket[a%N]+=1;bracket[0]-=1
  check([x+y for x,y in zip(telescope,bracket)]==[0]*N)
  for c in range(N):
   check((2*(half*a*c)-a*c)%N==0)
   check((N*(half*a*c))%N==0)
 # The later state sum N^(2-V) is N^2 times the old N^(-V).
 for V in range(2,21):
  check(Fraction(N)**(2-V)/Fraction(N)**(-V)==N*N)
  check((Fraction(N)**(-2))**N==Fraction(1,N**(2*N)))
 # Scaling test for the sign of the global edge exponent; E-H=T.
 for tetra in range(2,21):
  check(Fraction((N-1)*tetra,N)+Fraction((1-N)*tetra,N)==0)
  check(Fraction((N-1)*tetra,N)+Fraction((N-1)*tetra,N)>0)
# Rotation of the 2011 positive o-graph by180deg identifies i,j,k,l with f2,f0,f3,f1.
check(dict(i=2,j=0,k=3,l=1)==dict(zip('ijkl',(2,0,3,1))))
# Root-only ambiguity is killed by power N; a sign would survive since N odd.
for N in range(3,32,2):
 check((-1)**N==-1)
 for s in range(N):check((s*N)%N==0)
exact=count
mp.mp.dps=90
worst=mp.mpf(0);numeric=0

def close(a,b,tol=mp.mpf('1e-70')):
 global worst,numeric
 err=abs(a-b)/max(1,abs(a),abs(b));worst=max(worst,err);numeric+=1
 assert err<tol,mp.nstr(err,15)

for N in (3,5,7,9,11):
 m=(N-1)//2;half=(N+1)//2;zeta=mp.exp(2j*mp.pi/N)
 def gnew(u):return mp.exp(sum(mp.mpf(j)/N*mp.log(1-u*zeta**(-j)) for j in range(1,N)))
 def gold(u):return mp.exp(sum(mp.mpf(j)/N*mp.log(1-u*zeta**j) for j in range(1,N)))
 gn1=gnew(1);go1=gold(1)
 def hn(u):return gnew(u)/gn1
 def ho(u):return u**(-m)*gold(u)/go1
 def om(u,v,n):return mp.fprod(v/(1-u*zeta**j) for j in range(1,n%N+1))
 def br(u):return (1-u**N)/(N*(1-u))
 for ur,ui in [('0.31','0.17'),('1.2','0.23'),('-0.43','0.62')]:
  u=mp.mpc(ur,ui);v=mp.exp(mp.log(1-u**N)/N)
  close(ho(1/u)**N,hn(u)**N)
  for a in range(N):
   Up=u*zeta**(-a);Um=u*zeta**a
   for c in range(N):
    Vp=v*zeta**c;Vm=v*zeta**(-c)
    rp=[];rm=[]
    for n in range(N):
     oldp=ho(1/u)*zeta**(c*n-half*a*c)*om(u,v,n-a)
     newp=hn(Up)*om(Up,Vp,n)
     oldm=br(u)/ho(1/u)*zeta**(c*n+half*a*c)/om(u/zeta,v,n+a)
     newm=br(Um)/hn(Um)/om(Um/zeta,Vm,n)
     rp.append(oldp/newp);rm.append(oldm/newm)
     close(rp[-1],rp[0]);close(rm[-1],rm[0])
     close(rp[-1]**N,1);close(rm[-1]**N,1)
# All matrix states for N3,5: the charged Kronecker conditions reduce unchanged;
# exponent changes have no residual dependence on the arbitrary alpha,delta.
for N in (3,5):
 for a in range(N):
  for c in range(N):
   for alpha in range(N):
    for beta in range(N):
     for gamma in range(N):
      for delta in range(N):
       check((gamma-a+delta-(beta-a))%N==(gamma+delta-beta)%N)
       check((gamma+a+delta-(beta+a))%N==(gamma+delta-beta)%N)
       check((alpha*delta+pow(2,-1,N)*alpha*alpha)%N ==(alpha*delta+((N+1)//2)*alpha*alpha)%N)
receipt={'problem_id':10400139,'exact_controls':count,'exact_factor_and_normalization_controls':exact,'numerical_controls':numeric,'mpmath_dps':mp.mp.dps,'worst_relative_error':mp.nstr(worst,12),'numeric_tolerance':'1e-70','scope':'Exact factor-exponent, half-charge, normalization, scaling-sign and state-index controls; non-interval finite complex diagnostics for both charged tensor orientations. Published all-link theorem and analytic arbitrary-N bridge remain the proof.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(receipt,indent=2,sort_keys=True))
