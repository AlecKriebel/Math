"""Exact Heisenberg quotient controls for the relative disk obstruction."""
import json
from itertools import product
checks=0
E=(0,0,0);X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
def mul(a,b):
 x,y,z=a;u,v,w=b
 return x+u,y+v,z+w+x*v
def inv(a):
 x,y,z=a
 return -x,-y,-z+x*y
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def power(a,n):
 if n<0:return power(inv(a),-n)
 r=E
 for _ in range(n):r=mul(r,a)
 return r
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
eq(comm(X,Y),Z);eq(comm(Y,X),inv(Z))
eq(mul(comm(X,Y),comm(Y,X)),E)
for g in (X,Y,Y,X):
 for sign in (-1,1):eq(mul(mul(power(Z,sign),g),power(Z,-sign)),g)
for q in product(range(-3,4),repeat=3):
 eq(mul(q,inv(q)),E)
 for m in range(-4,5):eq(mul(mul(q,power(Z,m)),inv(q)),power(Z,m))
eq(power(Z,2),(0,0,2))
assert power(Z,2) not in (E,Z);checks+=1
# Quotient distinguishes all m from the two permitted smooth local exponents.
for m in range(-20,21):
 eq(power(Z,m) in (E,Z),m in (0,1))
print(json.dumps({'status':'PASS','exact_assertions':checks,'surface_relation_image':E,'vanishing_cycle_image':Z,'obstructed_boundary_image':power(Z,2),'permitted_smooth_images':[E,Z],'limitations':'Finite controls of an explicitly proved integral group quotient; no closed positive relation counterexample is claimed.'},indent=2))
