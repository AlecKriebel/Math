"""New exact finite diagnostics; these are illustrations, not an infinite PDE proof."""
from fractions import Fraction as F
from itertools import product
import json
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return list(map(list,zip(*a)))
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def diag(xs):return [[F(x) if i==j else F(0) for j in range(len(xs))] for i,x in enumerate(xs)]
u=[[F(7,25),-F(24,25)],[F(24,25),F(7,25)]]
old=diag([1,0]);branch=mul(mul(u,old),tr(u));difference=sub(branch,old)
assert mul(tr(u),u)==diag([1,1])
assert mul(difference,difference)==diag([F(24,25)**2]*2)
assert mul(mul(u,diag([1,1])),tr(u))==diag([1,1])
geometry=[]
for d in (2,3,5):
    a,b,p,delta=F(3,2),F(13,4),F(3),F(2,7)
    center1=p-a;center2=p+b;count=0
    for offset in product([F(-2,3),F(0),F(2,3)],repeat=d):
        y=[p+delta*offset[0],*[delta*t for t in offset[1:]]]
        inold=(abs(y[0]-center1)<a and all(abs(t)<a for t in y[1:])) or (abs(y[0]-center2)<b and all(abs(t)<b for t in y[1:]))
        assert inold==(offset[0]!=0);count+=1
    geometry.append({'d':d,'exact_grid_points':count})
# Resonance is avoidable for a finite protected set, but fixed width can fail.
assert F(3,4)==F(12,16) # d=3, halfwidth1/m=(1,1,1), halfwidth2/m=(2,2,2)
width=F(19,7);protected=[3,6,11,17];forbidden=set()
for q in protected:
    for m in product(range(1,14),repeat=3):
        a2=F(sum(x*x for x in m),q)
        if 4<a2<9:forbidden.add(a2)
assert 2<width<3 and width**2 not in forbidden
# Exact epsilon-tail and birth-plus-tail diagonal error for late births.
tails=[]
for n in range(1,101):
    finite=sum(F(1,2**(j+2)) for j in range(n,n+200))
    infinite=F(1,2**(n+1));remainder=F(1,2**(n+201))
    assert finite+remainder==infinite
    assert F(1,2**n)+infinite==F(3,2**(n+1))
    tails.append({'n':n,'tail':str(infinite)})
print(json.dumps({'status':'PASS_DIAGNOSTICS_ONLY','geometry':geometry,
    'branch_distance':'24/25','whole_cluster_distance':'0','nonresonant_width':'19/7',
    'forbidden_squared_width_count':len(forbidden),'exact_tail_cases':len(tails),
    'limits':'No finite test certifies capacity, PDE limits, usable apertures or completeness.'},indent=2))
