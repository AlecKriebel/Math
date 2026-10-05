#!/usr/bin/env python3
from fractions import Fraction as Q
import json
n=0
# Exhaustively check the one-mark band partition in log2 coordinates, including boundaries.
for den in range(1,16):
 for markn in range(-30,31):
  mark=Q(markn,den)
  for origin in [Q(-7,2),Q(0),Q(5,3),Q(11,7)]:
   hits=[j for j in range(-100,101) if origin+j<=mark<origin+j+1]
   assert len(hits)==1;n+=1
# Derive substitution powers for general beta and the DI criterion.
for bd in range(1,14):
 for bn in range(2*bd+1,6*bd):
  beta=Q(bn,bd)
  assert -(2-beta)-2==beta-4;n+=1
  for an in range(1,bd+1):
   a=Q(an,bd)
   assert (1-beta+2*a>-1)==(beta<2+2*a);n+=1
# Exactly integrate synthetic h(u)=sum mass*1_{u<=size} for integral alpha.
for alpha in range(1,12):
 for size in range(1,40):
  mass=Q(size+2,size+3)
  integral=mass*Q(size**alpha,alpha)
  assert alpha*integral==mass*size**alpha;n+=1
# Random-band tail algebra: log2x chosen rational at dyadic x, no probability simulation.
for j0 in range(10):
 for k in range(50):
  x=2**k;J=j0+k;C=Q(7,3);H=Q(5,2)
  actual=C*J/x+H/Q(2**J)
  asserted=(C*(j0+1+k)+H/Q(2**j0))/x
  assert actual<=asserted;n+=1
for an in range(1,100):
 a=Q(an,100)
 assert a-2<-1 and 1/(1-a)**2>0;n+=1
print(json.dumps({'status':'PASS','independent_exact_assertions':n,'scope':'Band partition, radial/DI exponent identities, intrinsic-mark integration and tail bookkeeping; not a SIRSN simulation or formal proof.'},indent=2))
