"""Exact arithmetic controls for the proved rectangular-modulus scaling formula."""
from fractions import Fraction as F
from itertools import product
import json,math
count=0
for n in range(2,6):
  for sizes in product(range(1,4),repeat=n):
    volume=math.prod(sizes)
    for p in range(1,7):
      value=F(volume,sizes[-1]**p)
      for s in (F(1,2),F(2,3),F(3,2)):
        scaled_volume=s**n*volume
        scaled_value=scaled_volume/(s*sizes[-1])**p
        assert scaled_value==s**(n-p)*value
        if p==n: assert scaled_value==value
        count+=1+(p==n)
print(json.dumps({'assertions':count,'scope':'finite exact formula/scaling arithmetic; not a numerical proof of modulus bounds'},sort_keys=True))
