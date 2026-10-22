#!/usr/bin/env python3
"""Fresh exact protocol enumeration and polynomial drift check, no package imports."""
from itertools import product
from collections import defaultdict
from fractions import Fraction as F
import json,math,datetime

def common_chunk_first_and_exit(z,x,y):
 # Individually labelled peers: 0 empty, 1 chunk X, 2 chunk Y, 3 seed.
 peers=[0]*z+[1]*x+[2]*y+[3];S=len(peers);p=F(1,S**3)
 first=[F(0),F(0)];exit=[F(0),F(0)]
 for sample in product(peers,repeat=3):
  seen=[sum(bool(mask & bit) for mask in sample) for bit in [1,2]]
  rare=[i for i,n in enumerate(seen) if n==1]
  for i in rare:first[i]+=z*p/len(rare)
  if seen[0]>=2 and seen[1]>=1:exit[0]+=x*p
  if seen[1]>=2 and seen[0]>=1:exit[1]+=y*p
 return first,exit
p=common_chunk_first_and_exit(0,1,0)[1][0]
assert p==F(7,8) and p!=F(1,2)
f=sum(common_chunk_first_and_exit(1,0,0)[0]);assert f==F(3,8)
assert p/F(1,2)!=f/F(1)
empty=[]
for M in range(1,13):
 cc=sum(common_chunk_first_and_exit(M,0,0)[0]);assert cc==F(3*M**3,(M+1)**3)<3
 empty.append({'M':M,'Common_Chunk_first':str(cc),'DFC_first':M})
# Build LG as an exact polynomial in r, by independently generating all actual moves.
def field(s):
 a,b,x,y=s;S=sum(s)+1;out=defaultdict(F)
 for k in [x+1,y+1,a+b]:out[k]+=S
 return out

def drift_poly(M):
 s=(1,0,M,1);a,b,x,y=s;D=x+y+1
 events=[((2,0,M,1),F(1,2)),((1,1,M,1),F(1,2)),((0,0,M+1,1),F(M+1,M+2)),((1,0,M-1,1),F(2*M,M+2)),((1,0,M,0),F(M+1,M+2))]
 old=field(s);out=defaultdict(F)
 for t,rate in events:
  new=field(t)
  for e in set(new)|set(old):out[e]+=rate*(new[e]-old[e])
 return dict(sorted(out.items()))
rows=[]
for M in [100,10000,1000000]:
 poly=drift_poly(M);r=math.exp(-1);C=864*math.e
 # These floats are only an illustration of the separately justified symbolic limit.
 qW=-2+F(6,M+2)
 qG=math.fsum(float(c)*r**k for k,c in poly.items())
 drift=float(C*qW)+qG
 assert drift>0 if M>=10000 else True
 assert F(M+1,M+2)>F(12,(M+3)**2)
 rows.append({'M':M,'LG_low_degree_coefficients_divided_by_M':{str(k):str(v/M) for k,v in poly.items() if k<=2},'remaining_exponents':[k for k in poly if k>2],'QW':str(qW),'L_drift':drift,'L_drift_over_M':drift/M,'rare_departure_DFC':str(F(M+1,M+2)),'CC_retention_bound':str(F(12,(M+3)**2))})
rare_rows=[]
for M in [1,2,10,1000]:
 # The 2011 two-chunk rare-rule function, after mapping profile counts.
 lam=F(1);LW=2*lam-M-F(M,M+1)
 Lsquare=M*(2*M+1)+F(M,M+1)*(-2*M+1)
 actual=2*LW+Lsquare
 assert actual>0
 rare_rows.append({'state':[M,0,M,0],'lambda':'1','DFC_drift_of_2011_rare_rule_function':str(actual)})
print(json.dumps({'status' :'PASS_INDEPENDENT_PRIORITY_CONTROLS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'single_peer_departure':{'CC':str(p),'DFC':'1/2'},'single_empty_first':{'CC':str(f),'DFC':'1'},'empty_plane':empty,'transfer_rows':rows,'2011_rare_rule_function_fails_on_DFC':rare_rows,'analytic_limit':'Q_DFC(CW+G)(1,0,M,1)/M -> 1-exp(-1)>0 for every fixed finite C','scope':'Model and direct-theorem-transfer exclusions only. No worldwide absence claim and no universal recurrence proof by these controls.'},indent=2))
