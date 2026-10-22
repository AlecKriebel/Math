#!/usr/bin/env python3
"""Exact Newton-basis certificates for fixed-index ULC bands, for ALL row sizes.
Analytic degree bounds are proved in TURN_5. No all-index claim is made.
Run with --dump FILE to save all 200 coefficient vectors as a separate JSON file.
"""
from fractions import Fraction as F
from collections import Counter
from math import comb
import hashlib,json,sys
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
def add(*ps):
 a=[0]*max(map(len,ps))
 for p in ps:
  for j,c in enumerate(p):a[j]+=c
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def shift(p,k):return [0]*k+p
# Original three-state source matrix, not the two-state or reverse reductions.
T=[0,0,0,2,1];Q=[0,0,0,0,1];S=[0,0,0,2,2];rows={}
for n in range(4,501):
 rows[n]=add(T,Q,S)
 ck(len(rows[n])-1==(3*(n-1))//2,'source_degree_formula')
 T,Q,S=add(shift(T,1),Q,shift(Q,1),S,shift(S,1)),add(Q,shift(Q,1),shift(S,1)),add(shift(T,1),shift(T,2),S,shift(S,1))
def at(p,k):return p[k] if 0<=k<len(p) else 0
def margin(r,par,index,side):
 row=rows[2*r+4+par];d=len(row)-1;k=index+3 if side=='lower' else d-index
 return k*(d-k)*at(row,k)**2-(k+1)*(d-k+1)*at(row,k-1)*at(row,k+1)
def forward(v):
 out=[]
 while v:out.append(v[0]);v=[b-a for a,b in zip(v,v[1:])]
 return out
cert=[];nonzero=0
for side,cutoff in [('lower',60),('upper',40)]:
 for index in range(1,cutoff+1):
  for par in [0,1]:
   degree=2*index+1 if side=='lower' else 4*index+3-2*par
   coefficients=forward([margin(r,par,index,side) for r in range(degree+1)])
   for a in coefficients:ck(a>=0,'nonnegative_Newton_coefficient')
   ck(coefficients[-1]>0,'top_Newton_coefficient_positive')
   first=next(i for i,x in enumerate(coefficients) if x)
   r_min=max(0,(index-2*par+2)//3) if side=='lower' else max(0,(index-1-2*par+2)//3)
   ck(first==r_min,'first_nonzero_matches_first_positive_interior')
   for r in [degree+1,degree+2,degree+7,degree+11]:
    value=sum(a*comb(r,i) for i,a in enumerate(coefficients))
    ck(value==margin(r,par,index,side),'additional_exact_polynomial_identity_control')
   nonzero+=sum(a>0 for a in coefficients)
   cert.append({'side':side,'index':index,'parity':par,'degree_bound':degree,'first_nonzero':first,'coefficients':coefficients})
# A strict Newton-positivity criterion is only sufficient, not necessary.
ck(forward([5,2,1])==[5,-3,2],'positive_polynomial_negative_Newton_control')
# Exact rational Sturm computation for the rejected real-rootedness shortcut.
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def rem(a,b):
 a=list(map(F,a));b=list(map(F,b))
 while a!=[0] and len(a)>=len(b):
  c=a[-1]/b[-1];d=len(a)-len(b)
  for j,x in enumerate(b):a[j+d]-=c*x
  trim(a)
 return a
p=list(map(F,rows[7][3:]));sturm=[p,[i*p[i] for i in range(1,len(p))]]
while len(sturm[-1])>1:sturm.append([-x for x in rem(sturm[-2],sturm[-1])])
sign=lambda x:1 if x>0 else -1 if x<0 else 0
var=lambda v:sum(a!=b for a,b in zip([x for x in v if x],[x for x in v if x][1:]))
minus=[sign(a[-1])*(-1)**(len(a)-1) for a in sturm];zero=[sign(a[0]) for a in sturm];plus=[sign(a[-1]) for a in sturm]
ck(p==list(map(F,[4,40,132,195,129,32,1])),'degree_six_source_row')
ck([len(a)-1 for a in sturm]==[6,5,4,3,2,1,0],'Sturm_degrees')
ck(plus==zero==[1,1,1,1,1,1,-1],'Sturm_endpoint_signs')
ck(var(minus)==5 and var(zero)==1 and var(plus)==1,'Sturm_four_negative_real_roots')
ck(sturm[-1][0]!=0,'Sturm_no_repeated_roots')
canonical=json.dumps(cert,separators=(',',':'),sort_keys=True).encode()
if len(sys.argv)==3 and sys.argv[1]=='--dump':
 from pathlib import Path
 Path(sys.argv[2]).write_bytes(canonical+b'\n')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'certificate_polynomials':len(cert),'certificate_coefficients':sum(len(x['coefficients']) for x in cert),'strictly_positive_certificate_coefficients':nonzero,'canonical_certificate_sha256':hashlib.sha256(canonical).hexdigest(),'lower_index_j_cutoff':60,'upper_distance_h_cutoff':40,'row_parameter_evaluation_max':max(x['degree_bound']+11 for x in cert),'scope':'With the proved polynomial degree bounds, nonnegative exact Newton coefficients certify these fixed bands for all nonnegative integer row parameters. The rest of the all-index family is unproved; Sturm counts only reject a real-rootedness shortcut.'},indent=2,sort_keys=True))
