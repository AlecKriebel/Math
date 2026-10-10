from fractions import Fraction as F
import json
checks=0
def test(c):
 global checks
 assert c;checks+=1
for d in range(2,41):
 for n in range(1,151):
  for v in (F(1,3),F(7,5),F(100)):
   upper=1+n*(d-1)
   test(F(upper-1)/(n*v)==F(d-1)/v)
for k in range(1,1000):
 chain=0;n=1
 while 2*n<=k:n*=2;chain+=1
 test(chain==k.bit_length()-1)
print(json.dumps({'assertions':checks,'scope':'Schreier-volume cancellation and ascending-chain arithmetic; Wang and FMW remain cited theorem inputs'},indent=2))
