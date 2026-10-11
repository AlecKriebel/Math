#!/usr/bin/env python3
"""Independent pair-accumulation reproduction of PR42's scoped finite claims."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
import json
import os

checks = 0
events = []

def demand(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)

def d2(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2

def inspect(points):
    points = tuple((F(x),F(y)) for x,y in points)
    demand(bool(points), "empty configuration")
    demand(len(set(points)) == len(points), "duplicate coordinates")
    local = [set() for _ in points]
    incidence = {}
    for i,j in combinations(range(len(points)),2):
        d = d2(points[i],points[j])
        demand(d>0,"positive pair distance")
        local[i].add(d); local[j].add(d)
        incidence.setdefault(d,set()).update((i,j))
    counts = [len(s) for s in local]
    deficits = {len(points)-1-r for r in counts}
    demand(len(deficits)==len(set(counts)),"affine deficit spectrum cardinality")
    demand(sum(counts)==sum(map(len,incidence.values())),"incidence double count")
    for i,j in combinations(range(len(points)),2):
        demand(len(points)-2<=2*counts[i]*counts[j],"two-pin product inequality")
    h=len(points)-len(set(counts))
    if len(points)>1:
        demand(min(counts)>=1 and max(counts)<=len(points)-1,"count range")
        demand(len(points)-2<=2*h*(h+1),"classical spectrum deficit inequality")
    return counts,deficits

def generic(blocks, external_internal_check=True):
    flat = sum(blocks,[])
    if len(set(flat))!=len(flat):return False
    for i,block in enumerate(blocks):
        ext=sum((other for j,other in enumerate(blocks) if j!=i),[])
        for p in block:
            ds=[d2(p,q) for q in ext]
            if len(set(ds))!=len(ds):return False
            if external_internal_check and set(ds)&{d2(p,q) for q in block if q!=p}:return False
    return True

def layout(seeds):
    for base in range(7,80):
        blocks=[[(F(x)+base**(2*i+1),F(y)+base**(2*i+2)) for x,y in seed]
                for i,seed in enumerate(seeds)]
        if generic(blocks):return blocks,base
    raise AssertionError("private deterministic witness search exhausted")

def glued(seeds,label):
    blocks,base=layout(seeds)
    flat=sum(blocks,[])
    actual,D=inspect(flat)
    expected=[];expected_D=set()
    for seed in seeds:
        local,di=inspect(seed)
        expected.extend([len(flat)-len(seed)+r for r in local])
        expected_D|=di
    demand(actual==expected,"generic union full count vector")
    demand(D==expected_D,"generic deficit spectrum union")
    maximum=max(map(len,seeds))
    demand(len(D)<=max(1,maximum-1),"largest seed bound")
    events.append({"family":label,"n":len(flat),"blocks":len(seeds),"base":base,
                   "actual_counts":actual,"deficits":sorted(D),"M":len(D)})
    return flat,D

def rejected(label,fn):
    try:fn()
    except AssertionError as e:
        return {"mutation":label,"rejected":True,"rejection":str(e)}
    raise AssertionError("mutation accepted: "+label)

single=[(0,0)]
pair=[(0,0),(1,0)]
square=[(0,0),(1,0),(0,1),(1,1)]
axis4=[(0,0),(1,0),(0,1),(0,-1)]
line7=[(i,0) for i in range(7)]
powers6=[(2**i,0) for i in range(6)]
parabola5=[(i,i*i) for i in range(5)]
seed_types=[single,pair,square,axis4,line7,powers6,parabola5]
for ia,ib in product(range(7),repeat=2):
    glued([seed_types[ia],seed_types[ib]],f"seed pair {ia},{ib}")
for seed in seed_types:
    _,original_D=inspect(seed)
    for k in (1,2,3,7,13):
        _,D=glued([seed]*k,"repeated fixed seed")
        demand(D==original_D,"copies preserve spectrum rather than multiply it")
    for k in (1,2,5,11):
        _,D=glued([seed]+[single]*k,"singleton padding")
        demand(D==original_D|{0},"padding union zero deficit")
leaves=[[square,axis4],[pair,line7],[single,powers6,parabola5]]
lower=[glued(group,"lower hierarchy")[0] for group in leaves]
_,hier_D=glued(lower,"upper hierarchy")
leaf_D=set()
for group in leaves:
    for leaf in group:leaf_D |= inspect(leaf)[1]
demand(hier_D==leaf_D,"hierarchical leaf spectrum identity")

# All nontrivial subsets of nine integer collinear points.
line_subsets=0
for n in range(2,10):
    for xs in combinations(range(9),n):
        counts,D=inspect([(x,0) for x in xs])
        demand(len(D)<=(n+1)//2,"line support bound")
        demand(min(counts)>=(n//2),"line min pinned count")
        line_subsets+=1

# Rational equal-angle arcs: multiplication by a unit complex fraction.
circle_controls=0;support_controls=0
for n in range(2,49):
    tangent=F(1,5*n)
    c=(1-tangent*tangent)/(1+tangent*tangent);s=2*tangent/(1+tangent*tangent)
    points=[];x,y=F(1),F(0)
    for _ in range(n):
        points.append((x,y));x,y=c*x-s*y,s*x+c*y
    demand(all(x*x+y*y==1 for x,y in points),"exact positive-radius circle")
    counts,D=inspect(points)
    expected=[max(i,n-1-i) for i in range(n)]
    demand(counts==expected,"small-angle circle full count vector")
    demand(len(D)==(n+1)//2,"sharp circle bound")
    events.append({"family":"sharp rational arc","n":n,"counts":counts,"M":len(D)})
    circle_controls+=1
    for support in (points,[(j,0) for j in range(n)]):
        for t in (0,1,2,5):
            extras=([(F(0),F(0))] if support is points and t else [])
            remaining=t-len(extras)
            extras.extend([(F(10+j),F(21+j*j)) for j in range(remaining)])
            combined=support+extras
            vals,dd=inspect(combined);N=len(combined);a=n//2
            bound=min(N-1,N+t-a)
            demand(len(dd)<=bound,"support with exceptions bound")
            demand(all(v>=a for v in vals[:n]),"supported pins remain bounded below")
            if support is points and t:
                demand(vals[n]<=t,"circle center is exceptional")
            support_controls+=1

# Independent product-bound verification on every nonempty 3x3 grid subset.
grid=[(i,j) for i in range(3) for j in range(3)]
grid_subsets=0
for n in range(1,10):
    for subset in combinations(grid,n):inspect(subset);grid_subsets+=1

square_blocks=[pair,[(0,1),(1,1)]]
square_D=inspect(sum(square_blocks,[]))[1]
demand(not generic(square_blocks),"nongeneric square rejected")
demand(square_D=={1} and inspect(pair)[1]=={0},"nongeneric square deficit differs")
demand(generic(square_blocks,False),"weak predicate counterexample actually exists")
mutations=[
    rejected("drop external/internal equality check",lambda:demand(not generic(square_blocks,False),"weak predicate wrongly accepted square")),
    rejected("apply generic deficit identity to square",lambda:demand(square_D=={0},"square cross collisions change deficits")),
    rejected("multiply spectrum by copies",lambda:demand(glued([axis4]*3,"mutation witness")[1]==set(range(9)),"repetition cannot multiply deficits")),
    rejected("padding always creates a new spectrum value",lambda:demand(len(glued([pair,single,single],"padding mutation witness")[1])==2,"seed already contains zero deficit")),
    rejected("add overlapping point cardinalities",lambda:inspect([(0,0),(1,0),(1,0),(2,0)])),
    rejected("count degree in square",lambda:demand(inspect(square)[0]==[3]*4,"distinct distances are not degrees")),
    rejected("full circle has arithmetic progression counts",lambda:demand(inspect(square)[0]==[3,2,2,3],"folded circle counts differ")),
    rejected("center pin obeys supported circle minimum",lambda:demand(inspect([(0,0),(1,0),(0,1),(-1,0),(0,-1)])[0][0]>=2,"center lies outside positive-radius supporting circle")),
]
print(json.dumps({"pid":os.getpid(),"claims_checked":"Scoped PR42 lemmas only; finite controls supplement separately assessed proofs",
    "implementation":"pairwise accumulation; integer/Fraction squared distances; deterministic translations",
    "assertions":checks,"line_subsets":line_subsets,"sharp_circle_sizes":[2,48],
    "circle_controls":circle_controls,"support_exception_controls":support_controls,
    "nonempty_grid_subsets":grid_subsets,"mutations":mutations,"events":events},indent=2))
