from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
n=0
def check(t):
 global n
 assert t;n+=1
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def sub(a,b):return add(a,scale(-1,b))
def cube(a):return scale(dot(a,a),a)
v=tuple(map(F,(1,2,3,4,5,6,7,8)))
def Q(a):return sub(a,scale(2*dot(a,v)/dot(v,v),v))
points=[tuple(map(F,p))+tuple(F(0) for _ in range(5)) for p in product(range(-2,3),repeat=3)]
for x in points:
 check(dot(Q(x),Q(x))==dot(x,x));check(Q(Q(x))==x)
 check(cube(Q(x))==Q(cube(x)))
 if dot(x,x):
  def D(h):return add(scale(dot(x,x),h),scale(2*dot(x,h),x))
  check(D(x)==scale(3*dot(x,x),x))
  e=tuple(F(i==0) for i in range(8));h=sub(scale(dot(x,x),e),scale(x[0],x))
  check(dot(x,h)==0);check(D(h)==scale(dot(x,x),h))
for x in points:
 for y in points:
  check(dot(sub(Q(x),Q(y)),sub(Q(x),Q(y)))==dot(sub(x,y),sub(x,y)))
  check(dot(sub(cube(Q(x)),cube(Q(y))),sub(cube(Q(x)),cube(Q(y))))==dot(sub(cube(x),cube(y)),sub(cube(x),cube(y))))
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':n,'rational_points':len(points),'scope':'Finite radial-cubic and orthogonal-coordinate algebra only; no computational certification of the imported Euclidean theorem or original general implication.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
