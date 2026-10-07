from fractions import Fraction
from math import prod
cases=0
for q in (3,5,7,11):
 for r in (1,2,3,4):
  for a in range(1,13):
   if a%q==0: continue
   N=q**r*a; m=1+(q-1)*r
   W=[-N,N]+[0]*(q-2)
   def divide(w):
    # w_i=v_i-v_{i-1}, with degree zero determining the additive constant
    accum=[0]
    for wi in w[1:]: accum.append(accum[-1]+wi)
    avg=Fraction(sum(accum),q)
    return [Fraction(v)-avg for v in accum]
   for t in range(1,m):
    W=divide(W)
    assert all(v.denominator==1 for v in W)
    assert sum(W)==0
   nxt=divide(W)
   assert not all(v.denominator==1 for v in nxt)
   cases+=1
print('Infinity-lattice divisions integral through m, obstructed at m+1:',cases,'cases passed')
