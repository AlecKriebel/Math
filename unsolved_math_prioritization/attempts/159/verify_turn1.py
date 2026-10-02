"""Exact finite controls for all-degree written arithmetic reductions."""
from itertools import product
import json
N=0
def ck(b):
 global N
 N+=1
 assert b
def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def main():
 candidates=accepted=prefixes=fracprefixes=0
 for m in range(1,6):
  for n in range(1,6):
   for mid_a in product(range(3),repeat=m-1):
    a=(2,)+mid_a+(2,)
    for mid_b in product(range(3),repeat=n-1):
     b=(2,)+mid_b+(2,);c=conv(a,b);candidates+=1
     if all(x in (0,4) for x in c):
      accepted+=1;ck(all(x in (0,2) for x in a+b));ck(m!=n)
      ck(a[0]==a[-1]==b[0]==b[-1]==2)
 for h in range(1,5):
  for mid_a in product(range(5),repeat=h):
   a=(4,)+mid_a
   for mid_b in product(range(5),repeat=h):
    b=(4,)+mid_b;c=conv(a,b)
    if all(x in (0,16) for x in c[:h+1]):
     prefixes+=1
     frac=[k for k in range(1,h+1) if a[k] not in (0,4) or b[k] not in (0,4)]
     if frac:
      fracprefixes+=1;k=min(frac)
      ck(0<a[k]<4 and 0<b[k]<4);ck(a[k]+b[k]==4)
      ck(sum(a[i]*b[k-i] for i in range(1,k))==0);ck(c[k]==16)
 ck(accepted>0);ck(fracprefixes>0)
 print(json.dumps({'problem_id':159,'turn':1,'status':'PASS','exact_assertions':N,'rational_factor_pairs_examined':candidates,'Boolean_products_accepted':accepted,'admissible_prefix_pairs':prefixes,'fractional_prefix_pairs':fracprefixes,'scope':'Finite rational grids and incomplete prefixes only. The written proof, not the scan, establishes all-degree rational and conjugate-positive cases.'},indent=2))
if __name__=='__main__':main()
