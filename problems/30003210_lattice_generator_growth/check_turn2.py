import itertools,json
checks=0
def test(x):
 global checks
 assert x;checks+=1
# Exact finite-group analogues of index decreasing under a quotient.
for n in range(1,151):
 for a in range(1,n+1):
  if n%a:continue
  # H=aZ/nZ, kernel=bZ/nZ. [image(G):image(H)]=gcd(a,b).
  for b in range(1,n+1):
   if n%b:continue
   import math
   image_index=math.gcd(a,b)
   test(image_index<=a)
   test(a%image_index==0)
# Local-degree and representation bounds, including nonconstant dimensions.
for D in range(1,20):
 for d in range(1,D+1):
  for N in range(1,8):
   for n in range(1,N+1):test(3**(d*n*n)<=3**(D*N*N))
print(json.dumps({'assertions':checks,'scope':'index and uniform-bound controls; compactness and arithmetic scope require the written proof'},indent=2))
