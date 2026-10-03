#!/usr/bin/env python3
"""Independent exact finite geometric/expectation controls; not a SIRSN simulation."""
from bisect import bisect_left
from collections import deque
from fractions import Fraction as F
from itertools import combinations
import json

checks = 0
def require(test):
    global checks
    assert test
    checks += 1

def path(adj,a,b):
    parent={a:None}; todo=deque([a])
    while b not in parent:
        z=todo.popleft()
        for y in adj[z]:
            if y not in parent: parent[y]=z;todo.append(y)
    out=[b]
    while out[-1]!=a: out.append(parent[out[-1]])
    return out[::-1]

# Disjoint narrow rectangles abutting a straight trunk. Each hair is a finite
# serpentine with increasing row levels, arbitrarily large length, tiny diameter.
N=7
root=(F(0),F(0)); far=(F(3,4),F(0))
hairs=[];rectangles=[]
for n in range(1,N+1):
    x=F(1,2**n); w=F(1,2**(n+2)); rows=n*2**(n+2)
    ys=[F(j,rows)*w for j in range(1,rows+1)]
    points=[(x,F(0))]; current_x=x
    for y in ys:
        points.append((current_x,y))
        current_x=x+w if current_x==x else x
        points.append((current_x,y))
    rectangles.append((x,x+w,F(0),w))
    require(rows*w==n)
    require(all(a<b for a,b in zip(ys,ys[1:])))
    require(all(a*a+b*b<1 for a,b in points))
    require(len(set(points))==len(points))
    length=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(points,points[1:]))
    require(length==F(n)+w)
    # Every vertical segment spans adjacent row levels: it meets horizontal
    # rows only at those levels, which are its consecutive path endpoints.
    for a,b in zip(points,points[1:]):
        require((a[0]==b[0]) != (a[1]==b[1]))
        if a[0]==b[0]:
            require(a[1]<b[1])
            lower=bisect_left(ys,a[1]);upper=bisect_left(ys,b[1])
            require(upper-lower<=1)
        else:
            require({a[0],b[0]}=={x,x+w})
    hairs.append(points)
for ra,rb in combinations(rectangles,2):
    require(ra[1]<rb[0] or rb[1]<ra[0])

# All-pair route compatibility on the explicitly embedded finite tree.
adj={}
def add_edge(a,b):
    adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
trunk=[root]+sorted([hair[0] for hair in hairs])+[far]
for a,b in zip(trunk,trunk[1:]):add_edge(a,b)
for hair in hairs:
    for a,b in zip(hair,hair[1:]):add_edge(a,b)
require(sum(map(len,adj.values()))//2==len(adj)-1)
endpoints=[root,far]+[h[-1] for h in hairs]
routes=[path(adj,a,b) for a,b in combinations(endpoints,2)]
for first,second in combinations(routes,2):
    second_set=set(second);meet=[x for x in first if x in second_set]
    if len(meet)<2:continue
    a,b=meet[0],meet[-1]
    f=first[first.index(a):first.index(b)+1]
    ia,ib=second.index(a),second.index(b)
    s=second[min(ia,ib):max(ia,ib)+1]
    require(f==s or f==s[::-1])

root_lengths=[]
for n,hair in enumerate(hairs,1):
    r=path(adj,root,hair[-1])
    length=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(r,r[1:]))
    require(length>=n)
    root_lengths.append(str(length))

# Fixed-radius deletion removes every sufficiently small hair, regardless of
# its very long arclength. This check considers Euclidean distance, not cost.
trimmed_hairs=0
for radius in [F(1,4),F(1,8),F(1,16),F(1,32)]:
    for hair,rect in zip(hairs,rectangles):
        w=rect[1]-rect[0]
        if 2*w*w<radius*radius:
            tip=hair[-1]
            require(all((z[0]-tip[0])**2+(z[1]-tip[1])**2<radius*radius for z in hair))
            trimmed_hairs+=1

# Deterministic-shell length coefficients, disc-annulus coefficients, and
# finite circle-pair count. These are algebraic controls only.
for level in range(1,61):
    shell=(F(1,4**level)-F(1,4**(level+1)))*2**(level+1)
    require(shell==F(3,2)*F(1,2**level))
    require(sum(F(3,2)*F(1,2**j) for j in range(level))==3*(1-F(1,2**level)))
    require(sum(F(1,2**j) for j in range(level))==2*(1-F(1,2**level)))
for k in range(61):require(len(list(combinations(range(k),2)))==k*(k-1)//2)
require(4*F(3)*F(1)==12)
require(4*F(2)*F(2)==16)

# Correlated capture radius: P(A=2^k)=3*4^-k, finite E A, but captured
# local length 4^k/k has harmonic divergent mean. Fixed windows see only
# finitely many such locations. The infinite conclusion is the exact series.
harmonic=F(0)
for truncation in range(1,101):
    harmonic += F(1,truncation)
    mass=sum(3*F(1,4**k) for k in range(1,truncation+1))
    radius_mean=sum(3*F(1,4**k)*2**k for k in range(1,truncation+1))
    captured_mean=sum(3*F(1,4**k)*F(4**k,k) for k in range(1,truncation+1))
    require(mass==1-F(1,4**truncation))
    require(radius_mean==3*(1-F(1,2**truncation)))
    require(captured_mean==3*harmonic)

print(json.dumps({'status':'PASS','exact_assertions':checks,
      'planar_hairs':N,'embedded_tree_vertices':len(adj),'all_pair_routes':len(routes),
      'root_route_lengths':root_lengths,'entire_hair_trimming_controls':trimmed_hairs,
      'random_radius_truncations':100,
      'mathematical_extension':'n-th compact terminal hair has length n+2^(-n-2); sup is infinite although all paths lie in the unit disc. The infinite tree is a non-SIRSN logical control. Correlated captured mean is 3*sum(1/k), while E radius=3.',
      'scope':'Exact finite embedding, pairwise subroute compatibility, terminal Euclidean trimming and localization constants; not an infinite SIRSN proof or counterexample.'},indent=2,sort_keys=True))
