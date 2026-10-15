#!/usr/bin/env python3
"""Exact controls of the restricted multipartite profile; standard library."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json
C={}
def ck(x,s):
 assert x,s
 C[s]=C.get(s,0)+1

def parts(n,lo=1):
 if n==0:yield ()
 for i in range(lo,n+1):
  for z in parts(n-i,i):yield(i,)+z

def data(q):
 r=1//q
 d=((r+1)*q-1)/r
 A=(1+6*r*d+r*(r*r-r+1)*d*d)/(r+1)**3
 B=4*r*(r-1)*d/(r+1)**3
 return r,d,A,B

def plus(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y,d):return (x[0]*y[0]+x[1]*y[1]*d,x[0]*y[1]+x[1]*y[0])
def scale(x,c):return(x[0]*c,x[1]*c)
def power(x,n,d):
 a=(Q(1),Q(0))
 for _ in range(n):a=mul(a,x,d)
 return a

for r in range(1,41):
 for j in range(1,10):
  q=Q(1,r+1)+(Q(1,r)-Q(1,r+1))*Q(j,10)
  rr,d,A,B=data(q);ck(rr==r,'interval_index')
  a=(Q(1,r+1),Q(1,r+1));b=(Q(1,r+1),Q(-r,r+1))
  ck(plus(scale(a,r),b)==(1,0),'first_moment')
  ck(plus(scale(power(a,2,d),r),power(b,2,d))==(q,0),'second_moment')
  ck(plus(scale(power(a,4,d),r),power(b,4,d))==(A,-B),'fourth_moment_radical')
  ck(0<d<Q(1,r*r),'positive_part_domain')
for a in range(1,16):
 for b in range(a+1,20):
  t,u=Q(a,23),Q(b,23)
  lam2=4*(t*t+t*u+u*u)
  ck(2*(12*t*t-lam2)==8*(t-u)*(2*t+u)<0,'constrained_hessian')
for r in range(1,41):
 q=Q(1,r);rr,d,A,B=data(q)
 ck(rr==r and d==Q(1,r*r),'reciprocal_endpoint')
 ck(A-B/r==q**3,'endpoint_value')
 ck(3*(q*q-q**3)==Q(3*(r-1),r**3),'credited_endpoint_density')

partition_count=direct_graphs=0
for n in range(1,25):
 for p in parts(n):
  x=[Q(z,n) for z in p]
  q=sum(z*z for z in x);p3=sum(z**3 for z in x);p4=sum(z**4 for z in x)
  r,d,A,B=data(q)
  ck(p4>=A or B*B*d>=(A-p4)**2,'partition_moment_bound')
  N=sum(comb(a,2)*comb(b,2) for a,b in combinations(p,2))
  ck(Q(24*N,n**4)==3*(q*q-p4)+Q(6,n)*(p3-q)+Q(3,n*n)*(1-q),'finite_count_identity')
  ck(abs(Q(24*N,n**4)-3*(q*q-p4))<=Q(6,n)+Q(3,n*n),'uniform_count_error')
  ck(3*(q*q-p4)==6*sum(a*a*b*b for a,b in combinations(x,2)),'weighted_c4_formula')
  if n>=2:
   e=sum(a*b for a,b in combinations(p,2))
   ck(Q(e,comb(n,2))==Q(n,n-1)*(1-q),'edge_normalization')
  if 4<=n<=8:
   labels=[i for i,z in enumerate(p) for _ in range(z)]
   direct=0
   for S in combinations(range(n),4):
    deg=[sum(labels[v]!=labels[w] for w in S if w!=v) for v in S]
    direct+=all(d==2 for d in deg)
   ck(direct==N,'direct_induced_vertex_sets');direct_graphs+=1
  partition_count+=1
print(json.dumps({'assertions':sum(C.values()),'by_scope':C,
 'arithmetic':'exact integers and fractions; quadratic-radical comparisons by certified squaring',
 'integer_partitions':partition_count,'partition_max_order':24,
 'direct_graphs':direct_graphs,'direct_max_order':8,
 'scope':'Restricted multipartite controls only; no arbitrary-graph extremal assertion.'},indent=2)+'\n',end='')
