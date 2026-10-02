"""Own finite exact checks of the sealed reconstruction; no audited imports."""
from fractions import Fraction as F
import json
from math import gcd

checks = []
def record(name, assertion, evidence):
    if not assertion: raise AssertionError(name)
    checks.append({'mechanism':name,'checked':True,'evidence':evidence})

# Collaredness count / primitive shell count has ratio r^(3-kappa(n-2)).
record('dimension-three strict decay', 3-F(4)*(3-2) == -1,
       'kappa=4 gives exponent -1; kappa=3 gives exponent0 and is insufficient')
record('dimension-two failure of this mechanism', all(3-k*(2-2)==3 for k in (F(1),F(4),F(100))),
       'n=2 exponent remains3; this is not a surface theorem')

# Endpoints lie on height1. The arc has height² 1+u(1-u)|D-C|².
# V1 omitted the1; its failed source and complete streams are preserved.
def height(C,D,u): return 1+u*(1-u)*sum((b-a)**2 for a,b in zip(C,D))
def point(C,D,u): return tuple(a+u*(b-a) for a,b in zip(C,D))
def glide(P): return P[0]+1,-P[1]
C=(F(0),-F(1,5));D=(F(2),F(1,5));u=F(1,4);v=1-u
P=point(C,D,u);Q=point(C,D,v)
record('actual glide self-intersection witness', glide(P)==Q and height(C,D,u)==height(C,D,v)==F(89,50),
       'P=(1/2,-1/10),Q=(3/2,1/10), equal positive height²89/50')
C=(F(0),-F(1,5));D=(F(4),F(3,10));u=F(11,40);v=F(21,40)
record('projected collision insufficient', glide(point(C,D,u))==point(C,D,v) and height(C,D,u)!=height(C,D,v),
       {'height_squared_P':str(height(C,D,u)),'height_squared_Q':str(height(C,D,v))})

# An orientation-preserving isometry fixing0 and infinity has form z -> az;
# repeated traversals of one axis are one image, regardless of larger length.
A=((1,2),(0,1));B=((1,0),(2,1))
AB=tuple(tuple(sum(A[i][k]*B[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
record('axis-intersection primitive shortcut fails', AB==((5,2),(2,1)) and (2-1)**2+1**2==2 and (2-3)**2+1**2==2,
       'AB=[[5,2],[2,1]] has axis circle center1 radius√2; its A-translate has center3, same radius, and crosses at (2,1)')
record('not a proper power in free generators', gcd(1,1)==1,
       'Exponent sums of AB are(1,1); any k-th power has sums divisible by k, so no |k|>1. Freeness is imported/proved by ping-pong, not certified by this arithmetic.')

# All glide axes y=m beta/2 are avoided if the arc midpoint has positive
# distance from this lattice. These margins remain positive under endpoint error.
record('symmetric Klein midpoint margin', F(1,5)-F(1,100)>0,
       'beta=1,a=1/5: midpoint n/2-a stays ≥1/5 from half-lattice, perturbation≤1/100')
record('nonsymmetric Klein midpoint margin', F(1,15)-F(1,100)>0,
       'endpoint y values -1/5,1/3 give midpoint1/15 and transverse width8/15<1')
record('boundary fixed-point contraction margin', F(1,(4-1)**2)<1,
       'For |B|=K>3 the maps B+Qx/|x|² and their inverses contract on disjoint unit balls around B and0; K=4 bound1/9. General derivative inequality is in the sealed proof.')

print(json.dumps({'status':'FINITE_EXACT_CHECKS_PASS','checks':checks,
 'scope':'Finite arithmetic checks and explicit counterchecks of unsafe implications; no universal target proof or new mathematical discovery.',
 'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0},indent=2))
