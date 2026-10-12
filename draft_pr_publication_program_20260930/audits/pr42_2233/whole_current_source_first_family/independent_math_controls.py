"""Independently authored exact diagnostics. Imports no candidate code."""
from fractions import Fraction as F
from itertools import combinations, product
import json

checks = 0
def demand(value, name):
    global checks
    checks += 1
    if not value:
        raise AssertionError(name)
def lengths(P):
    demand(len(P) == len(set(P)), 'distinct coordinates')
    distance_sets = [set() for _ in P]
    for i, j in combinations(range(len(P)), 2):
        d = sum((P[i][k]-P[j][k])**2 for k in (0,1))
        distance_sets[i].add(d); distance_sets[j].add(d)
    return [len(s) for s in distance_sets]
def ds(P):
    return {len(P)-1-r for r in lengths(P)}
def bounds(P):
    r = lengths(P); n = len(P)
    if n < 2: return
    for i,j in combinations(range(n),2):
        demand(n-2 <= 2*r[i]*r[j], 'two circles per pair of radii')
    h=n-len(set(r))
    demand(n-2 <= 2*h*(h+1), 'quadratic defect, including sigma one')
def allowed(blocks):
    P=sum(blocks,[])
    if len(P)!=len(set(P)): return False
    for i,B in enumerate(blocks):
        O=sum([C for j,C in enumerate(blocks) if j!=i],[])
        for p in B:
            inside={sum((p[k]-q[k])**2 for k in (0,1)) for q in B if p!=q}
            outside=[sum((p[k]-q[k])**2 for k in (0,1)) for q in O]
            if len(outside)!=len(set(outside)) or inside & set(outside):return False
    return True

grid=list(product(range(-1,2),repeat=2)); grid_count=0
for n in range(2,10):
    for P in combinations(grid,n): bounds(P);grid_count+=1

line_count=0
for n in range(2,10):
    for S in combinations(range(9),n):
        P=[(i,0) for i in S]
        demand(len(set(lengths(P))) <= (n+1)//2, 'line bound')
        line_count+=1
for n in range(2,61):
    demand(lengths([(i,0) for i in range(n)])==[max(i,n-1-i) for i in range(n)], 'AP exact count vector')

# Exact rotations provide equal-angle unit-circle arcs, with span < 2/7 < pi.
circle_count=0; exception_count=0
for n in range(2,36):
    t=F(1,7*n); c=(1-t*t)/(1+t*t); s=2*t/(1+t*t)
    P=[];x,y=F(1),F(0)
    for i in range(n):
        P.append((x,y));x,y=c*x-s*y,s*x+c*y
    demand(all(x*x+y*y==1 for x,y in P), 'unit support')
    demand(lengths(P)==[max(i,n-1-i) for i in range(n)], 'short arc exact sharpness')
    circle_count+=1
    for support in (P, [(i,0) for i in range(n)]):
        for extra in ([],[(F(0),F(0))] if support==P else [(0,1)],[(F(0),F(0)),(3,5)] if support==P else [(0,1),(3,5)]):
            Q=support+extra;N=len(Q);t_exc=len(extra)
            demand(len(set(lengths(Q)))<=min(N-1,N+t_exc-(n//2)), 'exception interval bound')
            bounds(Q);exception_count+=1

seeds=[[(0,0)],[(0,0),(1,0)],[(0,0),(1,0),(2,0)],[(0,0),(1,0),(0,1)]]
generic_count=0;nongeneric_count=0
for A,B in product(seeds,repeat=2):
    for u,v in product(range(8,16),range(7,12)):
        C=[(x+u,y+v) for x,y in B]
        if allowed([A,C]):
            Q=A+C
            demand(ds(Q)==ds(A)|ds(B),'exact deficit union')
            demand(len(ds(Q))<=max(1,max(len(A),len(B))-1),'singleton-safe maximum seed bound')
            generic_count+=1
        else:nongeneric_count+=1
square=[[(0,0),(1,0)],[(0,1),(1,1)]]
demand(not allowed(square),'square rejects admissibility')
demand(ds(sum(square,[]))=={1} and ds(square[0])|ds(square[1])=={0},'nongeneric square disproves universal identity')
demand(ds([(0,0)])=={0},'singleton convention')
demand(len(ds([(0,0),(1,0)]))==1,'two point boundary')

mutations=[]
for name, claimed in [
    ('all singleton bound falsely zero',len(ds([(0,0),(10,3)]))<=0),
    ('nongeneric gluing identity',ds(sum(square,[]))==ds(square[0])|ds(square[1])),
    ('all circular arrangements have AP counts',lengths(sum(square,[]))==[3,2,2,3]),
    ('circle center inherits supported lower bound', lengths([(1,0),(0,1),(-1,0),(0,-1),(0,0)])[-1]>=2)
]:
    demand(not claimed, 'rejected mutated demand '+name);mutations.append(name)
print(json.dumps({'status':'PASS_OWN_EXACT_FINITE_CONTROLS','checks':checks,'grid_subsets':grid_count,'line_subsets':line_count,'sharp_short_arcs':circle_count,'exception_examples':exception_count,'generic_placements':generic_count,'rejected_placements':nongeneric_count,'rejected_mutated_demands':mutations,'arithmetic':'integers/Fraction squared distances','scope':'finite diagnostics supplement analytic proof; no original-helper execution or unrestricted asymptotic solution'},indent=2))
