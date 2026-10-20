from itertools import product
import json
N=[{(i+d)%20 for d in range(7,14)} for i in range(20)]
def extend(a):
 L=[N[t] for t in a]
 for x in L[0]:
  for y in L[1]&N[x]:
   for z in L[2]&N[y]:
    if L[3]&N[z]&N[x]:return True
 return False
r={}
for pairs in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,1)],[(0,1),(1,2)]]:
 count=0;fail=None
 for b,c,d in product(range(20),repeat=3):
  a=[0,b,c,d]
  if not all(a[j] in N[a[i]] for i,j in pairs):continue
  count+=1
  if not extend(a):fail=a;break
 r[str(pairs)]={'checked':count,'failure':fail}
print(json.dumps(r,indent=2))
