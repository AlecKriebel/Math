#!/usr/bin/env python3
"""Independent, bounded audit of the frozen polygonalization checker.
Standard library only; writes no files; exact rational arithmetic; no assertions.
Pass the frozen public directory as the sole argument. No complexity conclusion.
"""
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import io
import json
import os
import random
import sys
import types

FROZEN_CHECKER_SHA256 = 'c3598583dacd2695b4a245fafb23c9b253c31262c95e6f7a8fe8236b514eae33'
FROZEN_EXPECTED_SHA256 = 'bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def load_checker(source):
    module = types.ModuleType('frozen_counting')
    exec(compile(source, 'frozen_check_counting.py', 'exec'), module.__dict__)
    return module


def point_on_segment(a, b, p):
    """Solve p=a+t(b-a), component by component, without orientation signs."""
    a, b, p = (tuple(map(Q, x)) for x in (a, b, p))
    u = tuple(y-x for x,y in zip(a,b))
    if u == (0,0):
        return p == a
    axis = 0 if u[0] else 1
    t = (p[axis]-a[axis])/u[axis]
    return 0 <= t <= 1 and all(a[j]+t*u[j] == p[j] for j in (0,1))


def intersection(a, b, c, d):
    """Return (empty|point|overlap, point-or-None) by linear elimination.

    For nonparallel lines solve a+t(b-a)=c+s(d-c). For coincident
    lines intersect one-dimensional parameter intervals. No call to any
    author's geometric primitive and no orientation-product crossing test.
    """
    a,b,c,d = (tuple(map(Q, x)) for x in (a,b,c,d))
    u = tuple(y-x for x,y in zip(a,b))
    v = tuple(y-x for x,y in zip(c,d))
    w = tuple(y-x for x,y in zip(a,c))
    if u == (0,0):
        return ('point',a) if point_on_segment(c,d,a) else ('empty',None)
    if v == (0,0):
        return ('point',c) if point_on_segment(a,b,c) else ('empty',None)
    i = 0 if u[0] else 1
    j = 1-i
    coefficient = u[j]*v[i]/u[i]-v[j]
    rhs = w[j]-u[j]*w[i]/u[i]
    if coefficient:
        s = rhs/coefficient
        t = (w[i]+v[i]*s)/u[i]
        if 0 <= s <= 1 and 0 <= t <= 1:
            return ('point',tuple(a[k]+t*u[k] for k in (0,1)))
        return ('empty',None)
    if rhs:
        return ('empty',None)
    tc,td = w[i]/u[i],(d[i]-a[i])/u[i]
    lo,hi = max(Q(0),min(tc,td)),min(Q(1),max(tc,td))
    if lo > hi:
        return ('empty',None)
    if lo == hi:
        return ('point',tuple(a[k]+lo*u[k] for k in (0,1)))
    return ('overlap',None)


def edge_pairs(order, closed):
    edges = list(zip(order,order[1:]))
    if closed:
        edges.append((order[-1],order[0]))
    return edges


def independent_simple(points, order, closed=False, cache=None):
    if any(type(v) is not int or not 0 <= v < len(points) for v in order):
        return False
    if len(set(order)) != len(order) or (closed and len(order)<3):
        return False
    for e,f in combinations(edge_pairs(order,closed),2):
        key = tuple(sorted((tuple(sorted(e)),tuple(sorted(f)))))
        result = cache[key] if cache is not None else intersection(points[e[0]],points[e[1]],points[f[0]],points[f[1]])
        shared = set(e)&set(f)
        if shared:
            shared_point = tuple(points[next(iter(shared))])
            if result != ('point',shared_point):
                return False
        elif result[0] != 'empty':
            return False
    return True


def geometry_cache(points):
    edges = list(combinations(range(len(points)),2))
    return {tuple(sorted((e,f))):intersection(points[e[0]],points[e[1]],points[f[0]],points[f[1]])
            for e,f in combinations(edges,2)}


def independent_cycles(n):
    """Canonicalize by the complete undirected edge set, not label inequality."""
    found = {}
    if n < 3:
        return []
    for tail in permutations(range(1,n)):
        order=(0,)+tail
        key=frozenset(frozenset(e) for e in edge_pairs(order,True))
        found.setdefault(key,order)
    return sorted(found.values())


def independent_count(points):
    cache=geometry_cache(points)
    return sum(independent_simple(points,c,True,cache) for c in independent_cycles(len(points)))


def expect_value_error(fn, label):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError('missing ValueError: '+label)


def check_guards(m):
    tests = [
      ('point_container',lambda:m.validate(None)),
      ('point_count',lambda:m.validate([(i,i*i) for i in range(10)])),
      ('point_shape_short',lambda:m.validate([(0,)])),
      ('point_shape_long',lambda:m.validate([(0,0,0)])),
      ('point_type',lambda:m.validate([0])),
      ('float',lambda:m.validate([(0.0,0)])),
      ('boolean',lambda:m.validate([(True,0)])),
      ('coordinate_string',lambda:m.validate([('1',0)])),
      ('numerator_bits',lambda:m.validate([(1<<64,0)])),
      ('denominator_bits',lambda:m.validate([(Q(1,1<<64),0)])),
      ('duplicates',lambda:m.validate([(0,0),(Q(0),Q(0))])),
      ('general_too_small',lambda:m.validate([(0,0),(1,0)],general=True)),
      ('general_collinear',lambda:m.validate([(0,0),(1,0),(2,0)],general=True)),
      ('edge_subset_n7',lambda:m.count_edge_subsets([(i,i*i) for i in range(7)])),
      ('triangulation_n7',lambda:m.triangulations([(i,i*i) for i in range(7)])),
      ('forced_n_bool',lambda:m.forced_cycle_count(True,[])),
      ('forced_n_low',lambda:m.forced_cycle_count(2,[])),
      ('forced_n_high',lambda:m.forced_cycle_count(10,[])),
      ('forced_bad_length',lambda:m.forced_cycle_count(3,[(0,1,2)])),
      ('forced_bool_vertex',lambda:m.forced_cycle_count(3,[(False,1)])),
      ('forced_negative',lambda:m.forced_cycle_count(3,[(-1,1)])),
      ('forced_out_of_range',lambda:m.forced_cycle_count(3,[(0,3)])),
      ('forced_loop',lambda:m.forced_cycle_count(3,[(1,1)])),
      ('IE_collinear',lambda:m.inclusion_exclusion([(0,0),(1,0),(2,0)])),
      ('IE_event_count',lambda:m.inclusion_exclusion([(i,i*i) for i in range(7)])),
      ('hull_gap_collinear',lambda:m.hull_gap_count([(0,0),(1,0),(2,0)])),
      ('triangulation_collinear',lambda:m.triangulations([(0,0),(1,0),(2,0)])),
      ('obstruction_collinear',lambda:m.obstruction([(0,0),(1,0),(2,0)])),
    ]
    for label,fn in tests:
        expect_value_error(fn,label)
    need(len(m.validate([(i,i*i) for i in range(9)]))==9,'MAX_N inclusive')
    need(m.validate([((1<<64)-1,Q(1,(1<<64)-1))]),'MAX_BITS inclusive')
    need(m.polygons([(0,0),(1,0)])==[],'two-point convention')
    need(m.forced_cycle_count(3,[(0,1),(1,0),(0,1)])==1,'duplicate forced-edge normalization')
    need(not m.simple([(0,0),(1,0),(0,1)],(0,0,1),True),'duplicate cycle label')
    need(not m.simple([(0,0),(1,0),(0,1)],(0,1,3),True),'out-of-range cycle label')
    need(not m.simple([(0,0),(1,0),(0,1)],(False,1,2),True),'boolean cycle label')
    old=m.os.getuid
    try:
        m.os.getuid=lambda:999
        try:
            m.main()
        except RuntimeError as e:
            need('UID 1000' in str(e),'wrong UID guard exception')
        else:
            raise RuntimeError('missing UID guard')
    finally:
        m.os.getuid=old
    return {'rejections':len(tests),'rejection_labels':[a for a,_ in tests],
            'acceptance_boundary_checks':7,'UID_guard_simulation_passed':True}


def check_mutations(source,expected):
    changes = [
      ('omit_proper_crossings','if x*y < 0 and z*w < 0:','if False:'),
      ('omit_contact_membership','return orient(a,b,c) == 0 and all(', 'return False and all('),
      ('omit_closing_edge','edges = path_edges(order,closed)','edges = path_edges(order,False)'),
      ('omit_reversal_quotient','if tail[0] < tail[-1]:','if True:'),
      ('omit_connectivity','and connected(n,es) and is_plane','and True and is_plane'),
      ('omit_path_orientations','2**nontrivial_paths * factorial','1 * factorial'),
      ('omit_forced_reversal_quotient','factorial(components-1))//2','factorial(components-1))'),
      ('accept_nonspanning_cycles','return int(len(component)==n)','return 1'),
      ('drop_final_composition','for a in range(k+1):','for a in range(k):'),
      ('weaken_bit_guard','<= MAX_BITS','<= MAX_BITS+2'),
      ('skip_general_position_guard','if general:','if False:'),
      ('erase_require_guard','if not condition:\n        raise ValueError(message)','if False:\n        raise ValueError(message)'),
    ]
    records=[]
    for label,old,new in changes:
        need(old in source,'mutation does not match: '+label)
        mutated=source.replace(old,new)
        m=load_checker(mutated)
        failure=None
        try:
            stream=io.StringIO()
            with redirect_stdout(stream):
                m.main()
            if stream.getvalue().encode() != expected:
                failure='full-output mismatch'
            if failure is None:
                check_guards(m)
        except (ValueError,RuntimeError) as e:
            failure=type(e).__name__+': '+str(e)
        need(failure is not None,'surviving semantic mutation: '+label)
        records.append({'mutation':label,'rejected_by':failure,
                        'mutated_sha256':hashlib.sha256(mutated.encode()).hexdigest()})
    return records


def main():
    need(os.getuid()==1000,'audit requires actual UID 1000')
    need(len(sys.argv)==2,'usage: audit_counting.py FROZEN_PUBLIC_DIRECTORY')
    directory=Path(sys.argv[1])
    code=(directory/'check_counting.py').read_bytes()
    expected=(directory/'EXPECTED_RESULTS.json').read_bytes()
    need(hashlib.sha256(code).hexdigest()==FROZEN_CHECKER_SHA256,'frozen checker identity')
    need(hashlib.sha256(expected).hexdigest()==FROZEN_EXPECTED_SHA256,'frozen output identity')
    m=load_checker(code.decode())
    original=io.StringIO()
    with redirect_stdout(original):
        m.main()
    need(original.getvalue().encode()==expected,'full author stdout mismatch')
    out={'uid':os.getuid(),'scope':'Finite independent audit; no general complexity or novelty conclusion.',
         'frozen_full_output_equal':True,'guards':check_guards(m)}
    grid=list(product(range(3),repeat=2))
    relations=Counter()
    for a,b,c,d in product(grid,repeat=4):
        relation=intersection(a,b,c,d)
        need(m.intersects(a,b,c,d)==(relation[0]!='empty'),'segment predicate disagreement')
        relations[relation[0]]+=1
    for a,b,p in product(grid,repeat=3):
        need(m.on_segment(a,b,p)==point_on_segment(a,b,p),'point membership disagreement')
    out['geometry_predicates']={'all_grid_quadruples':9**4,'all_grid_triples':9**3,
                                'intersection_histogram':dict(sorted(relations.items()))}
    fixture_counts={}
    for name,row in json.loads(expected)['fixtures'].items():
        actual=independent_count(row['points'])
        need(actual==row['count'],'independent fixture count: '+name)
        fixture_counts[name]=actual
    out['independent_author_fixtures']=fixture_counts
    grid_rows=[];cycles_checked=0
    for n in range(3,7):
        histogram=Counter();pointsets=0
        orders=independent_cycles(n)
        for points in combinations(grid,n):
            cache=geometry_cache(points)
            total=0
            for order in orders:
                actual=independent_simple(points,order,True,cache)
                need(actual==m.simple(points,order,True),'grid cycle geometry disagreement')
                total+=actual;cycles_checked+=1
            histogram[total]+=1;pointsets+=1
        grid_rows.append({'n':n,'pointsets':pointsets,'count_histogram':dict(sorted(histogram.items()))})
    out['exhaustive_grid']={'rows':grid_rows,'cycles_compared':cycles_checked}
    rng=random.Random(5500016)
    gp_rows=[]
    for trial in range(30):
        n=6 if trial<20 else 7
        points=[]
        while len(points)<n:
            p=(rng.randrange(-50,51),rng.randrange(-50,51))
            if p in points:
                continue
            # Collinearity via parameter membership on the infinite line.
            if any((p[0]-a[0])*(b[1]-a[1])==(p[1]-a[1])*(b[0]-a[0]) for a,b in combinations(points,2)):
                continue
            points.append(p)
        count=independent_count(points)
        need(count==len(m.polygons(points)),'seeded canonical mismatch')
        gap,candidates=m.hull_gap_count(points)
        need(gap==count,'seeded hull-gap mismatch')
        hs=m.hull(points)
        need(candidates==__import__('math').factorial(n-1)//__import__('math').factorial(len(hs)-1),'candidate formula')
        events=len(m.crossing_events(points))
        ie=None
        if events<=12:
            ie=m.inclusion_exclusion(points)[0]
            need(ie==count,'seeded IE mismatch')
        gp_rows.append({'points':points,'count':count,'hull_size':len(hs),'candidates':candidates,'crossing_events':events,'IE_count':ie})
    out['seeded_general_position']=gp_rows
    event17=[(-5,10),(45,-49),(50,19),(-17,23),(12,18),(11,-34),(23,-15)]
    event19=[(-24,0),(-25,0),(-25,37),(25,-27),(36,7),(50,39),(-2,-8)]
    need(len(m.crossing_events(event17))==17 and len(m.crossing_events(event19))==19,'near-cap event counts')
    accepted17=m.inclusion_exclusion(event17)[0]
    need(accepted17==independent_count(event17)==40,'17-event inclusive check')
    expect_value_error(lambda:m.inclusion_exclusion(event19),'19-event near-cap rejection')
    out['IE_near_cap']={'accepted_events':17,'accepted_count':accepted17,'rejected_events':19,'rejected_direct_count':independent_count(event19)}
    base=[(0,0),(12,0),(13,10),(0,13),(2,3),(7,5)]
    changes=[[(3*x+2*y+5,x+y-7) for x,y in base],
             [(Q(x,7),Q(y,11)) for x,y in base],
             [base[i] for i in [4,2,5,1,3,0]],
             [(-x,y) for x,y in base],
             [(Q(x,(1<<64)-1),Q(y,(1<<63)-1)) for x,y in base]]
    for points in changes:
        need(independent_count(points)==len(m.polygons(points))==13,'independent metamorphic check')
    out['independent_metamorphic_counts']=[13]*len(changes)
    geometry_boundaries=[
      ('straight_boundary',[(0,0),(1,0),(2,0),(2,2),(0,2)],(0,1,2,3,4),True,True),
      ('adjacent_backtracking',[(0,0),(2,0),(1,0)],(0,1,2),False,False),
      ('nonadjacent_touch',[(0,0),(4,0),(4,2),(2,0)],(0,1,2,3),False,False),
      ('collinear_overlap',[(0,0),(4,0),(4,2),(1,0),(3,0)],(0,1,2,3,4),False,False),
      ('closing_edge_bowtie',[(0,0),(2,0),(2,2),(0,2)],(0,1,3,2),True,False),
      ('open_bowtie_prefix',[(0,0),(2,0),(2,2),(0,2)],(0,1,3,2),False,True)]
    out['geometry_boundaries']=[]
    for label,points,order,closed,wanted in geometry_boundaries:
        need(independent_simple(points,order,closed)==m.simple(points,order,closed)==wanted,label)
        out['geometry_boundaries'].append({'label':label,'points':points,'order':order,'closed':closed,'simple':wanted})
    forced=[]
    for n in range(3,7):
        edges=list(combinations(range(n),2))
        index={e:i for i,e in enumerate(edges)}
        masks=set()
        for tail in permutations(range(1,n)):
            order=(0,)+tail
            masks.add(sum(1<<index[tuple(sorted(e))] for e in edge_pairs(order,True)))
        histogram=Counter()
        for bits in range(1<<len(edges)):
            truth=sum(bits&cycle==bits for cycle in masks)
            es=[e for i,e in enumerate(edges) if bits>>i&1]
            need(m.forced_cycle_count(n,es)==truth,'forced graph mismatch')
            histogram[truth]+=1
        forced.append({'n':n,'subsets':1<<len(edges),'abstract_cycles':len(masks),'count_histogram':dict(sorted(histogram.items()))})
    out['forced_graphs']=forced
    boundaries=[('m1_spanning_path',5,[(0,1),(1,2),(2,3),(3,4)],1),
                ('m2_path_plus_singleton',5,[(0,1),(1,2),(2,3)],1),
                ('m2_two_paths',5,[(0,1),(1,2),(3,4)],2),
                ('proper_cycle',5,[(0,1),(1,2),(2,0)],0),
                ('spanning_cycle',3,[(0,1),(1,2),(2,0)],1),
                ('degree_three',4,[(0,1),(0,2),(0,3)],0)]
    out['forced_boundaries']=[]
    for label,n,edges,value in boundaries:
        need(m.forced_cycle_count(n,edges)==value,label)
        out['forced_boundaries'].append({'label':label,'n':n,'edges':edges,'count':value})
    six=[(0,0),(12,0),(13,10),(0,13),(2,3),(7,5)]
    completions=[]
    for path in ((0,1,4,2),(0,4,1,2)):
        need(independent_simple(six,path),'prefix is simple')
        rows=[]
        for tail in permutations((3,5)):
            order=path+tail
            rows.append({'order':order,'simple':independent_simple(six,order,True)})
        completions.append(rows)
    need([sum(x['simple'] for x in r) for r in completions]==[0,1],'continuation certificate')
    out['continuations']=completions
    determinants=[]
    for a,b,c,d in ((4,2,3,5),(4,1,5,0)):
        determinants.append([int(m.orient(six[x],six[y],six[z])) for x,y,z in ((a,b,c),(a,b,d),(c,d,a),(c,d,b))])
    need(determinants==[[124,-13,-54,83],[35,-36,-11,60]],'determinant certificates')
    out['determinants']=determinants
    five=[(0,0),(12,0),(0,13),(2,3),(5,2)]
    events=[]
    for e,f in combinations(list(combinations(range(5),2)),2):
        if not(set(e)&set(f)) and intersection(five[e[0]],five[e[1]],five[f[0]],five[f[1]])[0]!='empty':
            events.append([e,f])
    need(events==[[(1,3),(2,4)]],'unique crossing fixture')
    all_edges=frozenset(combinations(range(5),2))
    ts=[all_edges-{(2,4)},all_edges-{(1,3)}]
    incidence=[]
    for cycle in independent_cycles(5):
        if independent_simple(five,cycle,True):
            es=frozenset(tuple(sorted(e)) for e in edge_pairs(cycle,True))
            incidence.append({'cycle':cycle,'extensions':sum(es<=t for t in ts)})
    need(Counter(x['extensions'] for x in incidence)=={1:4,2:4},'independent incidence')
    out['independent_incidence']={'crossing_events':events,'polygons':len(incidence),
        'incidences':sum(x['extensions'] for x in incidence),'cycles':incidence}
    out['semantic_mutations']=check_mutations(code.decode(),expected)
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
