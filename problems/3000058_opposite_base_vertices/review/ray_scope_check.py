from fractions import Fraction as F
import json
checks=0
# None denotes +infinity; operations and ordering remain extended-valued.
b=[0,1,None,0]
def add(a,c):return None if a is None or c is None else a+c
def ge(a,c):return a is None or (c is not None and a>=c)
def ck(v):
 global checks
 assert v
 checks+=1
for s in range(4):
 for t in range(4):ck(ge(add(b[s],b[t]),add(b[s&t],b[s|t])))
def point(t):return (t,-t)
def feasible(v):return sum(v)==0 and v[0]<=1
for t in [F(-2),F(-1),F(0),F(1)]:ck(feasible(point(t)))
ck(point(F(1))==(1,-1))
ck(tuple(-x for x in point(F(1)))==point(F(-1)))
ck(tuple((a+b)/2 for a,b in zip(point(F(-2)),point(F(0))))==point(F(-1)))
ck(tuple((a+b)/2 for a,b in zip(point(F(-1)),point(F(1))))==point(F(0)))
ck(any(abs(x)>1 for x in point(F(-2))))
# The active endpoint normals (1,1),(1,0) have determinant -1.
ck(1*0-1*1==-1)
print(json.dumps({'status':'PASS','assertions':checks,'scope':'Literal current linked extended-valued definition; unique-vertex proof is the affine-ray argument, not finite testing','bounded_conjecture':'unresolved, no resolution claimed'},indent=2))
