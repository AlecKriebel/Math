#!/usr/bin/env python3
"""Exact turn4 controls and complete finite coefficient certificate."""
from itertools import product
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json,hashlib
checks=0

def ck(v):
 global checks
 assert v;checks+=1

def upsets(n):
 if not n:return [0,1]
 old=upsets(n-1)
 return [a|(b<<(1<<(n-1))) for a in old for b in old if a&b==a]

# Certify the Boolean event classification used in the universal 3-variable lemma.
U=upsets(3);ck(len(U)==20);top=1<<7;ALL=255
singles=[sum(1<<s for s in range(8) if s>>i&1) for i in range(3)]
pairs=[sum(1<<s for s in range(8) if s&m==m) for m in (3,5,6)]
forks=[singles[i]& (singles[(i+1)%3]|singles[(i+2)%3]) for i in range(3)]
majority=sum(1<<s for s in range(8) if s.bit_count()>=2)
def forced(e):return any(e&~a==0 for a in singles)
def dual(e):return sum((not(e>>(7^s)&1))<<s for s in range(8))
cases=Counter()
def certificate(e,f,can_dual=True):
 if not e or not f or e==ALL or f==ALL or e&f in (e,f):return 'nested-or-constant'
 if e in singles or f in singles:return 'singleton-regression'
 if e in pairs or f in pairs:
  if f in pairs:e,f=f,e
  support=next(m for m in (3,5,6) if e==sum(1<<s for s in range(8) if s&m==m));k=next(i for i in range(3) if not support>>i&1)
  ck(f&~singles[k]==0);ck(e&f==top);return 'pair-versus-missing-coordinate'
 if e in forks or f in forks:
  if f in forks:e,f=f,e
  ck(forced(f));ck(f in forks);i=forks.index(e);j=forks.index(f);ck(i!=j);ck(e&f==singles[i]&singles[j]);return 'two-forks-via-pair-correlation'
 ck(e==majority or not forced(e));ck(f==majority or not forced(f));ck(can_dual)
 de,df=dual(e),dual(f);ck(forced(de) or forced(df));certificate(de,df,False);return 'dual-forced-case'
for e in U:
 for f in U:cases[certificate(e,f)]+=1

# Direct three-side coloring counts versus the symbolic parameter weights.
three_cases=0
for q in range(3,8):
 a=q-2;r=q-1;R=F(a+1,a)
 for m12,m13,m23,m in product(range(3),range(3),range(3),range(4)):
  nb=[3]*m12+[5]*m13+[6]*m23+[7]*m;w=[0]*8
  for colors in product(range(q),repeat=3):
   ways=1
   for N in nb:ways*=q-len({colors[i] for i in range(3) if N>>i&1})
   w[sum((colors[i]==0)<<i for i in range(3))]+=ways
  x,y,z=R**m12,R**m13,R**m23;t=R**m;u=F(a-1,a)**m;M=x*y*z*t;scale=a**len(nb)
  expected=[r*(M+a*(x+y+z)+a*(a-1)*u),r*(z+a*u),r*(y+a*u),r*x,r*(x+a*u),r*y,r*z,M]
  ck(w==[scale*v for v in expected])
  for S in range(8):
   for T in range(8):ck(w[S&T]*w[S|T]>=w[S]*w[T])
  ck(t*(1+a*u)>=a+1);three_cases+=1
# Sharp side-four family, with m repeated triple-neighborhood vertices and t=2^m.
u=[0]*16;v=[0]*16
for c in product(range(3),repeat=4):
 used=len({c[i] for i in (1,2,3)})
 if used==3:continue
 ways=1
 for N in (9,12,10,5,6):ways*=3-len({c[i] for i in range(4) if N>>i&1})
 (v if used==1 else u)[sum((c[i]==0)<<i for i in range(4))]+=ways
ck(u==[52,12,20,4,12,8,12,8,12,8,12,8,8,16,0,0]);ck(v==[80,16,0,0,0,0,0,0,0,0,0,0,0,0,16,32])
# The local lattice gap has coefficients (0,0,-32) in t.
ck(v[0]*v[3]-v[1]*v[2]==0)
ck(u[0]*v[3]+v[0]*u[3]-u[1]*v[2]-v[1]*u[2]==0)
ck(u[0]*u[3]-u[1]*u[2]==-32)
U4=upsets(4);ck(len(U4)==168);Z0=sum(u);Z1=sum(v)
def mass(e):return(sum(u[s] for s in range(16) if e>>s&1),sum(v[s] for s in range(16) if e>>s&1))
M={e:mass(e) for e in U4};spectrum=Counter();pairs_checked=0
for i,e in enumerate(U4):
 for f in U4[i:]:
  a,b=M[e];c,d=M[f];h,j=mass(e&f)
  A=j*Z1-b*d;B=h*Z1+j*Z0-a*d-b*c;C=h*Z0-a*c
  coeff=(A,4*A+B,4*A+2*B+C) # t=2+z, descending coefficients z²,z,1
  ck(min(coeff)>=0);spectrum[coeff]+=1;pairs_checked+=1
certificate_data=[list(c)+[mult] for c,mult in sorted(spectrum.items())]
blob=(json.dumps(certificate_data,separators=(',',':'))+'\n').encode()
(Path(__file__).parent/'TURN_4_COEFFICIENT_CERTIFICATE.json').write_bytes(blob)
print(json.dumps({'status':'PASS','exact_assertions':checks,'boolean3_upset_pairs':400,'boolean3_proof_cases':dict(sorted(cases.items())),'three_side_graph_q_cases':three_cases,'four_side_family_weight_vectors':[u,v],'four_side_family_lattice_gap':'-32 for every t>=2','complete_upset_pairs_for_parameter_family':pairs_checked,'distinct_coefficient_triples':len(spectrum),'all_t_minus_2_coefficients_nonnegative':True,'coefficient_certificate_sha256':hashlib.sha256(blob).hexdigest(),'scope':'Universal lemmas have written proofs; the 4-coordinate parameter-family association uses a complete exact finite coefficient certificate. The negative lattice gap is not a source counterexample.'},indent=2))
