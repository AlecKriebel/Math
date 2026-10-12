from itertools import product
from fractions import Fraction as F
import json
nu=(1,2)
T=((F(7,8),F(1,8)),(F(1,16),F(15,16)))
assert all(sum(row)==1 for row in T)
assert all(sum(nu[i]*T[i][j] for i in range(2))==nu[j] for j in range(2))
alloc=[]
for tau in product(range(2),repeat=2):
 if all(sum(nu[i] for i in range(2) if tau[i]==j)==nu[j] for j in range(2)):alloc.append(tau)
assert alloc==[(0,1)]
assert T[0][1]>0 and T[1][0]>0
print(json.dumps({'status':'PASS','counting_multiplicities':nu,'T':[[str(x) for x in row] for row in T],'all_preserving_allocations':alloc,'claim':'This preserving Markov kernel, from the observable denominator family with C containing both points, is not a mixture of preserving allocations. This is a transport-class separation, not a law counterexample.'},sort_keys=True,indent=2))
