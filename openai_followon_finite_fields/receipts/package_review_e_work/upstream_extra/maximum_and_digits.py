from itertools import product
from math import gcd
counts={}
for q in (3,5,7):
 c=0
 for e in product(range(-2,3),repeat=q):
  if sum(e): continue
  # sigma sends coefficient at index i-1 to index i
  sig=lambda d: (d[-1],)+d[:-1]
  sums=[(0,)*q]; cur=(0,)*q; turn=e
  for j in range(1,q):
   cur=tuple(a+b for a,b in zip(cur,turn));sums.append(cur);turn=sig(turn)
  V=tuple(max(s[i] for s in sums) for i in range(q))
  assert tuple(a-b for a,b in zip(V,sig(V)))==e
  c+=1
 counts[q]=c
print('Cyclic coefficientwise maximum identity, exhaustive sums-zero vectors:',counts)
count=0
for q in (3,5,7):
 for s in (1,2,3,4):
  mod=q**s
  for exponent in range(mod):
   known=0
   for j in range(s):
    residue=((exponent-known)*q**(s-j-1))%mod
    digits=[c for c in range(q) if (c*q**(s-1))%mod==residue]
    assert len(digits)==1
    known+=digits[0]*q**j
   assert known==exponent
   if exponent%q==0: assert (q*(known//q))%mod==exponent
   count+=1
print('Primary-digit recovery exhaustive exponent cases:',count)
