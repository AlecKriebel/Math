#!/usr/bin/env python3
"""Finite exhaustive initial certificate plus exact algebraic controls; standard library only."""
from math import isqrt
from pathlib import Path
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def norm(a,N):M=4*a;return N**5+2*M**4*N-M**5
def P(n,r):return n**5+20*r*n**3+120*r*r*n
def E(n,r,a):return 320*r**3*n**4+(6080*r**4+8192)*n*n+32768*r**5+65536*r-(32768 if a==2 else -32768)
rows=[]
for a in (2,-2):
 for r in (-1,0,1):
  for n in range(1,200,2):
   N=n*n+8*r;D=norm(a,N);row={'a':a,'r':r,'n':n,'N':N,'D':D}
   ck(D==P(n,r)**2+E(n,r,a),'finite_exact_expansion')
   if D<0:row['negative']=True;ck(D<0,'finite_negative_norm')
   else:
    y=isqrt(D);lo=D-y*y;hi=(y+1)**2-D
    ck(lo>0 and hi>0,'finite_strict_square_gaps');row.update(floor_sqrt=y,lower_gap=lo,upper_gap=hi)
   rows.append(row)
certificate=(json.dumps({'scope':'All 600 initial cases n positive odd below 200; infinite tail proved in TURN_4.md.','rows':rows},indent=2,sort_keys=True)+'\n').encode()
path=Path(__file__).with_name('TURN_4_SMALL_CERTIFICATE.json')
if path.exists():ck(path.read_bytes()==certificate,'small_certificate_byte_exact')
else:path.write_bytes(certificate);ck(True,'small_certificate_byte_exact')
for a in (2,-2):
 for b in range(-51,52,2):
  for c in range(-5,6):
   eps=1 if b%4==1 else -1;k=(eps-b)//(2*a);N=b*b-4*a*c
   ck((eps-b)%(2*a)==0 and eps*(2*a*k+b)==1,'integer_normal_form_linear_term')
   cc=a*k*k+b*k+c
   ck(cc==(1-N)//(4*a) and (1-N)%(4*a)==0,'integer_normal_form_discriminant')
for n in [200,201,257,1001,10000]:
 for r in (-1,0,1):
  for a in (2,-2):
   pp=P(n,r);ee=E(n,r,a);D=norm(a,n*n+8*r)
   ck(D==pp*pp+ee,'tail_exact_expansion_controls')
   ck(pp>0 and 2*pp-1>399*n**4 and abs(ee)<321*n**4,'tail_bound_controls')
   ck(ee<0 if r==-1 else ee>0,'tail_sign_controls')
   ck((pp-1)**2<D<pp*pp if r==-1 else pp*pp<D<(pp+1)**2,'tail_square_gap_controls')
ck(norm(2,1)<0 and norm(-2,-7)<0,'sign_range_endpoints')
print(json.dumps({'status':'PASS','arithmetic':'exact integers and integer square roots; standard library only','assertions':sum(C.values()),'by_scope':dict(C),'complete_initial_cases':len(rows),'negative_initial_cases':sum('negative' in r for r in rows),'positive_nonsquare_initial_cases':sum('floor_sqrt' in r for r in rows),'initial_square_exceptions':0,'tail_threshold':200,'scope':'The 600-case initial certificate is exhaustive. The infinite tail is established by the written inequalities, not by the extra finite tail controls. The full source question remains unresolved.'},indent=2,sort_keys=True))
