#!/usr/bin/env python3
"""Small exact checks for polygonalization-counting obstructions.

Standard library only. No files written, network used, or assertions relied on.
This is factorial/exponential verification, not a polynomial-time count algorithm.
"""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial
import json
import os
import sys

MAX_N = 9
MAX_BITS = 64
MAX_IE_EVENTS = 18
MAX_EDGE_SUBSET_N = 6


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(points, general=False):
    require(isinstance(points, (list, tuple)), 'points must be a list or tuple')
    require(len(points) <= MAX_N, 'point-count guard exceeded')
    for p in points:
        require(isinstance(p, (list, tuple)) and len(p) == 2,
                'each point must have two coordinates')
        for x in p:
            require(type(x) in (int, Fraction), 'coordinates must be exact integers or Fractions')
            z = Fraction(x)
            require(z.numerator.bit_length() <= MAX_BITS and z.denominator.bit_length() <= MAX_BITS,
                    'coordinate-bit guard exceeded')
    points = tuple(tuple(Fraction(x) for x in p) for p in points)
    require(len(set(points)) == len(points), 'duplicate points rejected')
    if general:
        require(len(points) >= 3, 'general-position routines require at least three points')
        require(all(orient(points[a], points[b], points[c]) != 0
                    for a, b, c in combinations(range(len(points)), 3)),
                'general-position routine rejects collinearity')
    return points


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def on_segment(a, b, c):
    return orient(a,b,c) == 0 and all(min(a[i],b[i]) <= c[i] <= max(a[i],b[i]) for i in (0,1))


def intersects(a,b,c,d):
    x,y,z,w = orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    if x*y < 0 and z*w < 0:
        return True
    return (x == 0 and on_segment(a,b,c)) or (y == 0 and on_segment(a,b,d)) or \
           (z == 0 and on_segment(c,d,a)) or (w == 0 and on_segment(c,d,b))


def path_edges(order, closed=False):
    result = list(zip(order, order[1:]))
    if closed:
        result.append((order[-1],order[0]))
    return result


def simple(points, order, closed=False):
    if len(set(order)) != len(order) or any(type(v) is not int or not 0 <= v < len(points) for v in order):
        return False
    if closed and len(order) < 3:
        return False
    edges = path_edges(order,closed)
    # An edge may not go through any other used vertex, including at 180-degree reversals.
    for a,b in edges:
        if any(v not in (a,b) and on_segment(points[a],points[b],points[v]) for v in order):
            return False
    for (a,b),(c,d) in combinations(edges,2):
        if len({a,b,c,d}) == 4 and intersects(points[a],points[b],points[c],points[d]):
            return False
    return True


def canonical_cycles(n):
    if n < 3:
        return
    for tail in permutations(range(1,n)):
        if tail[0] < tail[-1]:
            yield (0,) + tail


def polygons(points):
    points = validate(points)
    return [c for c in canonical_cycles(len(points)) if simple(points,c,True)]


def edge_set(order):
    return frozenset(tuple(sorted(e)) for e in path_edges(order,True))


def hull(points):
    order = sorted(range(len(points)),key=lambda i:points[i])
    if len(order) <= 1:
        return order
    def chain(seq):
        out=[]
        for p in seq:
            while len(out)>1 and orient(points[out[-2]],points[out[-1]],points[p]) <= 0:
                out.pop()
            out.append(p)
        return out
    return chain(order)[:-1]+chain(order[::-1])[:-1]


def allowed_edges(points):
    return [e for e in combinations(range(len(points)),2)
            if not any(v not in e and on_segment(points[e[0]],points[e[1]],points[v])
                       for v in range(len(points)))]


def is_plane(points, edges):
    return all(len(set(a+b)) < 4 or not intersects(points[a[0]],points[a[1]],points[b[0]],points[b[1]])
               for a,b in combinations(edges,2))


def connected(n, edges):
    adj=[[] for _ in range(n)]
    for a,b in edges:
        adj[a].append(b);adj[b].append(a)
    seen={0};stack=[0]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v);stack.append(v)
    return len(seen)==n


def count_edge_subsets(points):
    points=validate(points)
    n=len(points)
    require(n <= MAX_EDGE_SUBSET_N,'edge-subset point-count guard exceeded')
    if n<3:
        return 0
    total=0
    for es in combinations(allowed_edges(points),n):
        deg=[0]*n
        for a,b in es:deg[a]+=1;deg[b]+=1
        if all(d==2 for d in deg) and connected(n,es) and is_plane(points,es):
            total+=1
    return total


def forced_cycle_count(n, edges):
    """Number of undirected Hamilton cycles of complete K_n containing edges."""
    require(type(n) is int and 3 <= n <= MAX_N,'invalid forced-cycle n')
    es=set()
    for e in edges:
        require(len(e)==2 and all(type(v) is int and 0<=v<n for v in e) and e[0]!=e[1],
                'invalid forced edge')
        es.add(tuple(sorted(e)))
    adj=[set() for _ in range(n)]
    for a,b in es:adj[a].add(b);adj[b].add(a)
    if any(len(a)>2 for a in adj):return 0
    seen=set();nontrivial_paths=0
    for v in range(n):
        if v in seen:continue
        todo=[v];component=set()
        while todo:
            x=todo.pop()
            if x in component:continue
            component.add(x);seen.add(x);todo.extend(adj[x]-component)
        edge_count=sum(len(adj[x]) for x in component)//2
        if edge_count==len(component):
            return int(len(component)==n)
        if edge_count:nontrivial_paths+=1
    components=n-len(es)
    return (2**nontrivial_paths * factorial(components-1))//2


def crossing_events(points):
    points=validate(points,general=True)
    edges=list(combinations(range(len(points)),2))
    return [(a,b) for a,b in combinations(edges,2) if len(set(a+b))==4
            and intersects(points[a[0]],points[a[1]],points[b[0]],points[b[1]])]


def inclusion_exclusion(points):
    points=validate(points,general=True)
    events=crossing_events(points)
    require(len(events)<=MAX_IE_EVENTS,'crossing-event guard exceeded')
    terms_by_size=[0]*(len(events)+1)
    for mask in range(1<<len(events)):
        used=set();size=mask.bit_count()
        for i,event in enumerate(events):
            if mask>>i&1:used.update(event)
        terms_by_size[size]+=forced_cycle_count(len(points),used)
    total=sum((-1)**i*x for i,x in enumerate(terms_by_size))
    return total, terms_by_size


def triangulations(points):
    points=validate(points,general=True)
    n=len(points)
    require(n<=MAX_EDGE_SUBSET_N,'triangulation point-count guard exceeded')
    hs=hull(points);boundary=edge_set(tuple(hs))
    candidates=[e for e in combinations(range(n),2) if e not in boundary]
    required=3*n-len(hs)-3-len(boundary)
    return [frozenset(boundary.union(extra)) for extra in combinations(candidates,required)
            if is_plane(points,list(boundary)+list(extra))]


def weak_compositions(k,h):
    if h==1:
        yield (k,);return
    for a in range(k+1):
        for rest in weak_compositions(k-a,h-1):yield (a,)+rest


def hull_gap_count(points):
    points=validate(points,general=True)
    hs=hull(points);interior=sorted(set(range(len(points)))-set(hs))
    tried=0;total=0
    for perm in permutations(interior):
        for lengths in weak_compositions(len(interior),len(hs)):
            order=[];offset=0
            for v,k in zip(hs,lengths):
                order.append(v);order.extend(perm[offset:offset+k]);offset+=k
            tried+=1
            total+=simple(points,order,True)
    require(tried==factorial(len(interior))*comb(len(points)-1,len(interior)),
            'hull-gap candidate total mismatch')
    return total,tried


def continuation_count(points,path):
    remain=sorted(set(range(len(points)))-set(path))
    return sum(simple(points,tuple(path)+tail,True) for tail in permutations(remain))


def obstruction(points):
    points=validate(points,general=True)
    n=len(points)
    for length in range(4,n):
        for subset in combinations(range(1,n),length-1):
            states={}
            for middle in permutations(subset):
                path=(0,)+middle
                if not simple(points,path):continue
                value=continuation_count(points,path)
                old=states.get(path[-1])
                if old and old[1]!=value:
                    return {'path_a':old[0],'completions_a':old[1],
                            'path_b':path,'completions_b':value,'subset':(0,)+subset}
                states[path[-1]]=(path,value)
    return None


def check(condition,message):
    if not condition:raise RuntimeError(message)


def expect_rejected(fn,message):
    try:fn()
    except ValueError:return
    raise RuntimeError('guard failed: '+message)


def main():
    check(os.getuid()==1000,'verification requires UID 1000')
    fixtures={
      'triangle':[(0,0),(4,0),(0,4)],
      'convex4':[(0,0),(4,0),(4,4),(0,4)],
      'triangle_plus_one':[(0,0),(10,0),(0,10),(2,3)],
      'hull4_plus_one':[(0,0),(10,0),(9,9),(0,8),(3,2)],
      'two_interior':[(0,0),(12,0),(0,13),(2,3),(5,2)],
      'six_mixed':[(0,0),(12,0),(13,10),(0,13),(2,3),(7,5)],
      'convex5':[(i,i*i) for i in range(5)],
      'convex6':[(i,i*i) for i in range(6)],
      'convex7':[(i,i*i) for i in range(7)],
      'collinear4':[(0,0),(1,0),(2,0),(3,0)],
      'boundary_straight':[(0,0),(1,0),(2,0),(2,2),(0,2)],
      'boundary_inward':[(0,0),(100,1),(200,0),(200,200),(0,200)],
    }
    out={'uid':os.getuid(),'warning':'Finite exact checks only; no general complexity conclusion.','fixtures':{}}
    for name,raw in fixtures.items():
        p=validate(raw);cycles=polygons(p);row={'points':raw,'count':len(cycles)}
        if len(p)<=MAX_EDGE_SUBSET_N:
            row['edge_subset_count']=count_edge_subsets(p)
            check(row['edge_subset_count']==len(cycles),'edge-subset mismatch '+name)
        gp=all(orient(p[a],p[b],p[c]) for a,b,c in combinations(range(len(p)),3))
        if gp:
            count,tried=hull_gap_count(p);row.update(hull_gap_count=count,hull_gap_candidates=tried,hull_size=len(hull(p)))
            check(count==len(cycles),'hull-gap mismatch '+name)
            if len(crossing_events(p))<=MAX_IE_EVENTS:
                count,terms=inclusion_exclusion(p);row.update(inclusion_exclusion_count=count,ie_terms_by_size=terms)
                check(count==len(cycles),'inclusion-exclusion mismatch '+name)
        out['fixtures'][name]=row
    check(out['fixtures']['triangle']['count']==1,'triangle count')
    check(out['fixtures']['convex6']['count']==1,'convex count')
    check(out['fixtures']['triangle_plus_one']['count']==3,'single interior count')
    check(out['fixtures']['hull4_plus_one']['count']==4,'single interior count')
    check(out['fixtures']['collinear4']['count']==0,'collinear convention')
    # Exhaustive combinatorial validation of the forced-edge formula for n=3,4,5.
    checked=0
    for n in (3,4,5):
        es=list(combinations(range(n),2));cycles=[edge_set(c) for c in canonical_cycles(n)]
        for mask in range(1<<len(es)):
            forced={e for i,e in enumerate(es) if mask>>i&1}
            actual=sum(forced<=c for c in cycles)
            check(forced_cycle_count(n,forced)==actual,'forced-edge formula mismatch')
            checked+=1
    out['forced_edge_subsets_checked']=checked
    p=validate(fixtures['six_mixed'],general=True)
    witness=obstruction(p)
    check(witness is not None,'missing endpoint-state witness')
    out['endpoint_state_obstruction']=witness
    p=validate(fixtures['two_interior'],general=True)
    ts=triangulations(p);cycles=polygons(p)
    multiplicities=[sum(edge_set(c)<=t for t in ts) for c in cycles]
    check(min(multiplicities)>0,'polygon failed to extend to triangulation')
    out['triangulation_incidence']={'points':fixtures['two_interior'],'triangulations':len(ts),
       'polygons':len(cycles),'sum_hamilton_cycles':sum(multiplicities),
       'cycles_and_extensions':list(zip(cycles,multiplicities))}
    require(len(set(multiplicities))>1,'fixture must show unequal extension counts')
    cp=validate(fixtures['convex5'],general=True)
    check(len(triangulations(cp))==5 and len(polygons(cp))==1,'convex-five divisor comparison')
    out['convex5_triangulations']=5
    expect_rejected(lambda:validate([(0,0),(0,0)]),'duplicates')
    expect_rejected(lambda:validate([(0.1,0)]),'float input')
    expect_rejected(lambda:validate([(True,0)]),'Boolean coordinate')
    expect_rejected(lambda:validate([(1<<65,0)]),'bit cap')
    expect_rejected(lambda:validate([(i,i*i) for i in range(MAX_N+1)]),'point cap')
    expect_rejected(lambda:inclusion_exclusion(fixtures['collinear4']),'IE degeneracy')
    expect_rejected(lambda:inclusion_exclusion(fixtures['convex7']),'IE event cap')
    expect_rejected(lambda:count_edge_subsets(fixtures['convex7']),'edge-subset cap')
    check(polygons([])==[] and polygons([(0,0)])==[],'small-set convention')
    # Affine changes and relabeling preserve the count; test independently chosen transformations.
    base=validate(fixtures['six_mixed'])
    affine=tuple((3*x+2*y+5,x+y-7) for x,y in base)
    rational=tuple((x/Fraction(7),y/Fraction(11)) for x,y in base)
    reordered=tuple(base[i] for i in [4,2,5,1,3,0])
    for transformed in (affine,rational,reordered):
        check(len(polygons(transformed))==13,'affine/rational/relabeling mismatch')
    check(out['fixtures']['boundary_inward']['count']==4,'perturbation does not preserve count')
    out['metamorphic_tests_passed']=3
    out['guard_tests_passed']=8
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
