#!/usr/bin/env python3
"""Independent finite probability, CDF-flat and moving-cut controls."""
from fractions import Fraction as Q
from pathlib import Path
from math import tanh,sqrt
import datetime,json,random
O=Path(__file__).resolve().parent
def inverse(z,r):return (2*z-r-1)/(r+4-2*r*z)
def solve(z,weights,A,B):
 lo,hi=-A,A
 for _ in range(90):
  r=(lo+hi)/2
  residual=r-A*tanh((B/A)*sum(w*inverse(value,r) for w,value in zip(weights,z)))
  if residual>0:hi=r
  else:lo=r
 r=(lo+hi)/2
 x=[inverse(v,r) for v in z]
 return x,r,r-A*tanh((B/A)*sum(w*v for w,v in zip(weights,x)))
rng=random.Random(23129302)
worst=0;max_residual=0;cases=0;cut_checks=0
for A in [0.4,0.001,1e-12]:
 for B in [6.0000000001,16.0]:
  for count in [1,2,7,23]:
   for trial in range(12):
    raw=[1+rng.randrange(19) for _ in range(count)];weights=[v/sum(raw) for v in raw]
    labels=[rng.randrange(2) for _ in range(count)]
    # Both later coordinates are correlated with the same old branch labels.
    later=[(.49 if label else -.49) if trial%2 else rng.uniform(-.499,.499) for label in labels]
    later2=[rng.uniform(-.499,.499) for _ in labels]
    z=[v+label for v,label in zip(later,labels)]
    zz=[v+label for v,label in zip(later2,labels)]
    x,r,residual=solve(z,weights,A,B);xx,rr,residual2=solve(zz,weights,A,B)
    den=sum(w*(v-vv)**2 for w,v,vv in zip(weights,z,zz))
    ratio=sum(w*(v-vv)**2 for w,v,vv in zip(weights,x,xx))/den
    assert ratio<=0.7+1e-12
    assert max(abs(residual),abs(residual2))<2e-12
    for v,label in zip(x,labels):
     assert -.5-1e-14<=v<=.5+1e-14
     assert (v<-r/4 if label==0 else v>-r/4)
     cut_checks+=1
    max_residual=max(max_residual,abs(residual),abs(residual2));worst=max(worst,ratio);cases+=1

# Reject exogenous zero feedback for a clearly nonzero-mean lifted input.
z=[.8,1.1];weights=[.25,.75];A=.4;B=16
wrong_x=[inverse(v,0) for v in z]
wrong_residual=-A*tanh(B/A*sum(w*v for w,v in zip(weights,wrong_x)))
assert abs(wrong_residual)>.1

# Exact PIT interval masses with flats on several source cells. Input law is
# normalized histogram; source CDF image interval has length equal to cell mass.
histograms=[[Q(0),Q(1),Q(0),Q(3)],[Q(5),Q(0),Q(0),Q(0)],[Q(1),Q(1),Q(1),Q(1)],[Q(0),Q(0),Q(2),Q(0),Q(5)]]
cdf_cases=0
for raw in histograms:
 mass=[v/sum(raw) for v in raw];start=Q(0);images=[]
 for v in mass:images.append((start,start+v));start+=v
 assert start==1
 for i in range(13):
  for j in range(i+1,14):
   left,right=Q(i,13),Q(j,13)
   result=sum(max(Q(0),min(right,hi)-max(left,lo)) for lo,hi in images)
   assert result==right-left
   cdf_cases+=1

# Terminal CDF transport of a symmetric zero-containing histogram is uniform;
# its one-step backward correction can be checked exactly for r=rho=0.
# In t=x+1/2 coordinates T0 is doubling mod1, and H0(t) is
# H1(2t)/2 on the left, (H1(2t-1)+1)/2 on the right.
heights=[Q(2),Q(0),Q(0),Q(2)]
def H1(t):
 total=Q(0)
 for k,h in enumerate(heights):total+=h*max(Q(0),min(t,Q(k+1,4))-Q(k,4))
 return total
def H0(t):return H1(2*t)/2 if t<=Q(1,2) else (H1(2*t-1)+1)/2
assert H0(0)==0 and H0(1)==1 and H0(Q(1,2))==Q(1,2)
assert all(H0(Q(i,80))<=H0(Q(i+1,80)) for i in range(80))
for i in range(1,80):
 t=Q(i,80)
 # Choose non-boundary points of output doubling to avoid arbitrary cut values.
 if t!=Q(1,2) and H0(t)!=Q(1,2):
  old=2*t if t<Q(1,2) else 2*t-1
  new=2*H0(t) if H0(t)<Q(1,2) else 2*H0(t)-1
  assert new==H1(old)
result={'record_id':'23129302','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'finite_exact_controls_and_float_corroboration','numerical_probability_cases':cases,'moving_cut_checks':cut_checks,'maximum_observed_squared_contraction_ratio':worst,'maximum_feedback_residual':max_residual,'selfconsistency_negative_control_rejected':True,'wrong_exogenous_feedback_residual':wrong_residual,'exact_CDF_interval_cases':cdf_cases,'flat_monotone_transport_control':True,'universal_proof_claimed_from_numerics':False,'source_helpers_executed':False}
(O/'probability-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
