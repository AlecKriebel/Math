"""Exact rational-tangle slope normalization only, not an equivariant surgery search."""
import math,json
from collections import Counter
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
def bezout(a,b):
 if b==0:return (abs(a),1 if a>=0 else -1,0)
 g,x,y=bezout(b,a%b);return(g,y,x-(a//b)*y)
vs=[(a,b) for a in range(-9,10) for b in range(-9,10) if math.gcd(a,b)==1]
for a,b in vs:
 g,u,v=bezout(a,b);ck(g==1 and u*a+v*b==1,'primitive_meridian_Bezout')
 for c,d in vs:
  det=a*d-b*c
  if abs(det)!=2:continue
  # Matrix [[u,v],[-b,a]] has determinant1 and fixes the chosen meridian as infinity.
  p=u*c+v*d;q=-b*c+a*d
  if q<0:p,q=-p,-q
  ck(q==2 and p%2==1,'distance_two_odd_numerator')
  k=(1-p)//2;ck(p+2*k==1,'meridian_preserving_shear')
  ck((a%2,b%2)==(c%2,d%2),'same_endpoint_connectivity_mod2')
# [[0,-1],[1,-1]] maps the two crossing slopes to infinity and1/2 up to sign.
ck((0*1-1*1,1*1-1*1)==(-1,0),'standard_positive_crossing_to_infinity')
ck((0*(-1)-1*1,1*(-1)-1*1)==(-1,-2),'standard_negative_crossing_to_half')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'limitations':'Finite arithmetic support for the distance-two rational-tangle equivalence. No knot unknotting number, surgery-link existence or mutation counterexample is computed.'},indent=2))
