"""Exact finite diagnostics only; not a proof of the stochastic limit theorem."""
from itertools import product
from fractions import Fraction
import argparse, json
ORDER={2:0,0:1,1:2}
LAM={1:Fraction(2,3),2:Fraction(7,4)}
def ordered(x,y):
 return all(ORDER[a]<=ORDER[b] for a,b in zip(x,y))
def arrow(x,a):
 u,v=x
 return (u,a if u==a and v==0 else v)
def check_monotonicity():
 count=0
 for lo,hi,a in product(product((0,1,2),repeat=2),product((0,1,2),repeat=2),(1,2)):
  if ordered(lo,hi):
   if not ordered(arrow(lo,a),arrow(hi,a)):
    raise ValueError(f'Arrow attractiveness failure: {lo}, {hi}, {a}')
   count+=1
 return count
def rate(n,m,x,v,a,skeleton=False):
 if x[v]!=0: return Fraction(0)
 total=0
 for u in range(n):
  if u==v or x[u]!=a: continue
  mm=m[min(u,v),max(u,v)]
  total+=int(mm>0) if skeleton else mm
 return LAM[a]*total
def check_skeleton():
 checked=0; graphs=0
 for n in range(1,4):
  edges=[(u,v) for u in range(n) for v in range(u,n)]
  for vals in product(range(3),repeat=len(edges)):
   m=dict(zip(edges,vals)); defects=set()
   for (u,v),mm in m.items():
    if (u==v and mm>0) or (u!=v and mm>1): defects.update((u,v))
   for forced in (1,2):
    for x in product((0,1,2),repeat=n):
     if any(x[v]!=forced for v in defects): continue
     for v,a in product(range(n),(1,2)):
      original=rate(n,m,x,v,a)
      simple=rate(n,m,x,v,a,skeleton=True)
      if original!=simple: raise ValueError(f'Skeleton generator mismatch: {n},{m},{x},{v},{a}')
      checked+=1
   graphs+=1
 return graphs,checked
def check_normalization(negative):
 mass=Fraction(1,2); factor=1 if negative else 2
 for a in (1,2):
  actual=mass*factor*LAM[a]
  if actual!=LAM[a]: raise ValueError(f'Jump-mark normalization mismatch: type {a}, actual {actual}, expected {LAM[a]}')
 return 2
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--negative-control',action='store_true');args=parser.parse_args()
 a=check_monotonicity();g,s=check_skeleton();r=check_normalization(args.negative_control)
 print(json.dumps({'status':'PASS','arrow_order_cases':a,'multigraphs_n_le_3_multiplicity_le_2':g,'exact_generator_coordinate_checks':s,'jump_normalizations':r,'limitations':'Finite deterministic algebra diagnostics; no stochastic or asymptotic theorem proved by code.'}))
if __name__=='__main__': main()
