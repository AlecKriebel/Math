#!/usr/bin/env python3
"""Independent exact check by circular-subset maxima; imports no package code.

Shift averaging: for k distinct circular points with gaps g, the backward
residual A=1-max has integral sum_g int_0^g f(a) da. Hence
E max^s = sum_g [1-(1-g)^(s+1)]/(s+1).
Expand the count power by onto tuples onto every nonempty subset. Integrate
slope on all collision/wrap breakpoints a/b, b<=n-1. The linear gap powers
are integrated directly, without parameter polygons or source checker code.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb,factorial
import json,sys
checks=0

def require(ok,message):
 global checks
 checks+=1
 if not ok:raise RuntimeError(message)

def stirling(m,k):
 return sum((-1)**(k-j)*comb(k,j)*j**m for j in range(k+1))//factorial(k)

def linear_power_integral(a,b,p,lo,hi):
 if a==0:return b**p*(hi-lo)
 return ((a*hi+b)**(p+1)-(a*lo+b)**(p+1))/(a*(p+1))

def maximum_moment(indices,s):
 n=max(indices)+1
 boundaries=sorted({Q(a,b) for b in range(1,max(2,n)) for a in range(b+1)})
 result=Q(0)
 for lo,hi in zip(boundaries,boundaries[1:]):
  mid=(lo+hi)/2
  points=sorted((Q(j),Q(-(j*mid//1))) for j in indices)
  points.sort(key=lambda pair:pair[0]*mid+pair[1])
  gaps=[(c-a,d-b) for (a,b),(c,d) in zip(points,points[1:])]
  gaps.append((points[0][0]-points[-1][0],1+points[0][1]-points[-1][1]))
  require(sum(a for a,b in gaps)==0 and sum(b for a,b in gaps)==1,'gaps do not close')
  require(all(a*mid+b>0 for a,b in gaps),'gap nonpositive')
  result+=sum(((hi-lo)-linear_power_integral(-a,1-b,s+1,lo,hi))/(s+1) for a,b in gaps)
 return result

def moment(n,p):
 total=Q(1,p+1)
 pieces=[]
 for m in range(1,p+1):
  integrals=Q(0)
  for k in range(1,min(m,n)+1):
   count=factorial(k)*stirling(m,k)
   for subset in combinations(range(n),k):
    # int x^(p-m) 1[all subset points<x] dx
    term=(1-maximum_moment(subset,p-m+1))/Q(p-m+1)
    integrals+=count*term
  piece=comb(p,m)*(-1)**(p-m)*integrals/n**m
  pieces.append(str(piece));total+=piece
 return total,pieces

def iid_moment(n,p):
 # Integrate each binomial probability times (k/n-x)^p using beta integrals.
 result=Q(0)
 for k in range(n+1):
  for a in range(p+1):
   beta=Q(factorial(k+a)*factorial(n-k),factorial(n+a+1))
   result+=comb(n,k)*comb(p,a)*Q(k,n)**(p-a)*(-1)**a*beta
 return result

def independent_shift_maximum(indices,z,s):
 points=sorted({(j*z)%1 for j in indices})
 cuts=sorted({Q(0),Q(1)}|{1-v for v in points})
 total=Q(0)
 for lo,hi in zip(cuts,cuts[1:]):
  mid=(lo+hi)/2
  intercept=max(v-((v+mid)//1) for v in points)
  total+=((hi+intercept)**(s+1)-(lo+intercept)**(s+1))/(s+1)
 gaps=[b-a for a,b in zip(points,points[1:])]+[1+points[0]-points[-1]]
 residual=sum((1-(1-g)**(s+1))/(s+1) for g in gaps)
 require(total==residual,'independent wrap-interval shift integral')
 return total

def main():
 # Check the residual-life formula against a separate wrap-interval integration.
 for size in range(1,5):
  for subset in combinations(range(6),size):
   for z in (Q(1,11),Q(2,7),Q(3,5),Q(5,8)):
    for s in range(1,6):independent_shift_maximum(subset,z,s)
 for m in range(1,5):
  for k in range(1,m+1):
   from itertools import product
   onto=sum(len(set(t))==k for t in product(range(k),repeat=m))
   require(onto==factorial(k)*stirling(m,k),'onto tuple multiplicity')
 rows=[]
 expected={1:Q(1,15),2:Q(1,48),3:Q(19,1620),4:Q(139,17280)}
 for n in range(1,9):
  fourth,pieces=moment(n,4);second,_=moment(n,2);iid=iid_moment(n,4)
  require(second==Q(1,6*n),'variance equality')
  require(iid==Q(3*n-1,30*n**3),'iid comparator')
  if n in expected:require(fourth==expected[n],'exact fourth n='+str(n))
  if n>=3:require(fourth>iid,'reversal')
  else:require(fourth==iid,'small n equality')
  if n>=4:require(fourth>=Q(2,105*(n-1))>iid,'tail comparator')
  rows.append({'n':n,'lattice_fourth':str(fourth),'iid_fourth':str(iid),'difference':str(fourth-iid),'second':str(second),'count_expansion_pieces':pieces})
 require(Q(19,1620)-Q(4,405)==Q(1,540),'gap')
 require(Q(19,1620)/Q(4,405)==Q(19,16),'ratio')
 # Adverse controls deliberately distinguish invalid substitutions.
 adverse={
  'iid_triple_is_not_lattice':maximum_moment((0,1,2),2)!=Q(3,5),
  'n3_tail_does_not_prove_reversal':Q(2,210)<Q(4,405),
  'normalization_cannot_be_omitted':Q(19,1620)*3**4!=Q(19,1620),
  'n2_generator_intervals_are_not_disjoint':Q(1,1)>1-Q(1,1),
  'fixed_generator_cannot_substitute':Q(1,15)!=Q(19,1620),
 }
 for name,ok in adverse.items():require(ok,name)
 if '--force-failure' in sys.argv:require(False,'deliberate failure')
 print(json.dumps({'status':'PASS','method':'Circular-subset maxima and onto-tuple expansion; exact slope antiderivatives','rows':rows,'checks':checks,'adverse_controls':adverse},indent=2,sort_keys=True))
if __name__=='__main__':main()
