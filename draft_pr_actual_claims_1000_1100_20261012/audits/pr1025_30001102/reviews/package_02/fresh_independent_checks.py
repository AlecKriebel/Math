#!/usr/bin/env python3
"""New exact review controls; standard library, deliberately finite enumeration."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import ceil, floor, lcm
import json
import sys


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def layers(d, negative=True, strict=False, subunit=True):
    ans = []
    for sign in (1, -1) if negative else (1,):
        old = Q(0)
        for t in sorted({sign*x for x in d if sign*x > 0}):
            r = tuple(sign*int(sign*x > t if strict else sign*x >= t) for x in d)
            weight = t-old
            if subunit or weight >= 1:
                ans.append((weight, r))
            old = t
    return ans


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def solve(rows, rhs, n):
    m = [list(map(Q, row))+[Q(v)] for row, v in zip(rows, rhs)]
    rank = 0
    for col in range(n):
        pivot = next((j for j in range(rank, len(m)) if m[j][col]), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        q = m[rank][col]
        m[rank] = [v/q for v in m[rank]]
        for j in range(len(m)):
            if j != rank and m[j][col]:
                q = m[j][col]
                m[j] = [v-q*w for v, w in zip(m[j], m[rank])]
        rank += 1
    if rank != n or any(all(not v for v in row[:-1]) and row[-1] for row in m):
        return None
    return tuple(m[j][-1] for j in range(n))


def unit(i, n):
    return tuple(int(i == j) for j in range(n))


def components(n, edges):
    unused = set(range(n))
    result = []
    while unused:
        found = {min(unused)}
        while True:
            nxt = found | {j for u, v in edges for i, j in ((u, v), (v, u)) if i in found}
            if nxt == found:
                break
            found = nxt
        result.append(found)
        unused -= found
    return result


def lp(n, edges, demands, cost, fixed):
    eq = [(unit(i, n), Q(p)) for i, p in fixed.items()]
    for comp in components(n, edges):
        if not comp.intersection(fixed):
            need(sum(cost[i] for i in comp) == 0, 'anchor objective invariance')
            eq.append((unit(min(comp), n), Q(0)))
    ir = [(tuple(int(j == u)-int(j == v) for j in range(n)), b)
          for (u, v), b in zip(edges, demands)]
    candidates = []
    for active in combinations(ir, n-len(eq)):
        rows = eq+list(active)
        y = solve([r for r, _ in rows], [b for _, b in rows], n)
        if y is not None and all(dot(r, y) >= b for r, b in ir):
            candidates.append(y)
    need(candidates, 'slice has anchored vertex')
    y = min(candidates, key=lambda y: (dot(cost, y), y))
    return dot(cost, y), y


def domain_encoding(lows, highs, edges, demands, omit_base=False):
    nodes = {(i, t) for i in range(len(lows)) for t in range(lows[i]+1, highs[i]+1)}
    arcs = {( (i, t), (i, t-1)) for i, t in nodes if t > lows[i]+1}
    forced, forbidden = set(), set()
    empty = False
    for (u, v), b in zip(edges, demands):
        d = ceil(b)
        t0 = lows[v]+d
        if not omit_base and t0 > lows[u]:
            if t0 > highs[u]:
                empty = True
            else:
                forced.add((u, t0))
        for t in range(lows[v]+1, highs[v]+1):
            target = t+d
            if target > highs[u]:
                forbidden.add((v, t))
            elif target > lows[u]:
                arcs.add(((v, t), (u, target)))
    def closure(seed):
        result = set(seed)|forced
        while True:
            nxt = result | {v for u, v in arcs if u in result}
            if nxt == result:
                return None if empty or result & forbidden else result
            result = nxt
    return nodes, arcs, forced, forbidden, empty, closure


def check_thresholds():
    count = removals = 0
    vals = (Q(-7, 3), Q(-1), Q(-1, 5), Q(0), Q(2, 7), Q(1), Q(9, 4))
    for n in range(1, 5):
        for d in product(vals, repeat=n):
            ls = layers(d)
            need(len(ls) <= n, 'layer count')
            need(tuple(sum((w*r[i] for w, r in ls), Q(0)) for i in range(n)) == d,
                 'layer reconstruction')
            for w, r in ls:
                for i in range(n):
                    need(min(0, d[i]) <= w*r[i] <= max(0, d[i]), 'coordinate conformity')
                    for j in range(n):
                        diff = d[i]-d[j]
                        need(min(0, diff) <= w*(r[i]-r[j]) <= max(0, diff),
                             'all-pair difference conformity')
                if w >= 1:
                    need(sum(abs(d[i]-r[i]) for i in range(n)) < sum(map(abs, d)),
                         'removal strictly reduces distance')
                    removals += 1
            count += 1
    controls = []
    for label, d, options in (
            ('negative-layer omission', (Q(-1), Q(0)), {'negative':False}),
            ('strict-threshold replacement', (Q(1), Q(0)), {'strict':True}),
            ('subunit-layer omission', (Q(1,2), Q(0)), {'subunit':False})):
        ls = layers(d, **options)
        reconstructed = tuple(sum((w*r[i] for w,r in ls),Q(0)) for i in range(len(d)))
        need(reconstructed != d, 'control failed to expose wrong threshold decomposition')
        controls.append({'fault':label, 'witness':list(map(str,d)), 'reconstruction':list(map(str,reconstructed))})
    # Unit removal is illegal at subunit weight: distance can grow.
    d = (Q(1,5),)
    need(abs(d[0]-1) > abs(d[0]), 'illegal small-layer removal control')
    controls.append({'fault':'removing a positive subunit layer', 'witness':['1/5'], 'before_l1':'1/5','after_l1':'4/5'})
    return {'vectors':count, 'removable_layers':removals, 'fresh_wrong_rule_controls':controls}


def check_rings():
    count = assignments = minima = 0
    edges = ((0,1),(0,2))
    for lows in ((-3,0,2),(0,0,0),(2,-2,1)):
        for widths in product(range(3), repeat=3):
            highs = tuple(l+w for l,w in zip(lows,widths))
            for ds in product(range(-3,4), repeat=2):
                nodes,arcs,forced,forbidden,empty,close = domain_encoding(lows,highs,edges,ds)
                feasible = []
                for p in product(*(range(l,h+1) for l,h in zip(lows,highs))):
                    A = {(i,t) for i,t in nodes if t <= p[i]}
                    actual = all(p[u]-p[v] >= b for (u,v),b in zip(edges,ds))
                    encoded = not empty and forced <= A and not A & forbidden and all(u not in A or v in A for u,v in arcs)
                    need(actual == encoded, 'domain exact base/arcs/forbid equivalence')
                    if actual:
                        feasible.append(A)
                    assignments += 1
                if feasible:
                    need(close(set()) == set.intersection(*feasible), 'smallest ring member')
                    for node in nodes:
                        selected = [A for A in feasible if node in A]
                        need(close({node}) == (set.intersection(*selected) if selected else None),
                             'smallest ring member containing node')
                        minima += 1
                else:
                    need(close(set()) is None, 'ring infeasibility reachability')
                count += 1
    _,_,_,_,_,bad_close = domain_encoding((0,0),(1,0),((0,1),),(Q(1),),omit_base=True)
    need(bad_close(set()) == set(), 'omitted-base diagnostic construction')
    need(0-0 < 1, 'omitted-base diagnostic failure')
    return {'families':count, 'assignments':assignments, 'containing_min_checks':minima,
            'fresh_fault_control':{'fault':'omitted base condition','lows':[0,0],'highs':[1,0],'demand':'1','false_assignment':[0,0]}}


def check_lp_values():
    models = slices = pairs = removal_checks = 0
    cases = []
    for edges in ((),((0,1),),((0,1),(0,2))):
        for pattern in ((Q(-2,3),Q(7,5)),(Q(1,2),Q(-11,7))):
            ds = pattern[:len(edges)]
            for weights in ((Q(0),Q(0)),(Q(2,3),Q(7,5))):
                cost = [Q(0)]*3
                for (u,v),w in zip(edges,weights):
                    cost[u] += w
                    cost[v] -= w
                for mask in range(8):
                    cases.append((3,edges,ds,tuple(cost),tuple(i for i in range(3) if mask>>i & 1)))
    # Connected four-variable cycle and disconnected edge+isolates, selected mixed masks.
    for edges in (((0,2),(0,3),(1,2),(1,3)),((0,2),)):
        ds = tuple((Q(-13,11),Q(17,19),Q(3,5),Q(-2,7))[i] for i in range(len(edges)))
        cost = [Q(0)]*4
        for i,(u,v) in enumerate(edges):
            w = Q(i+1,7)
            cost[u] += w; cost[v] -= w
        for ints in ((),(0,),(2,),(0,3),(1,2)):
            cases.append((4,edges,ds,tuple(cost),ints))
    for n,edges,ds,cost,ints in cases:
        _,ys = lp(n,edges,ds,cost,{})
        k = lcm(*(b.denominator for b in ds)) if ds else 1
        q = lcm(*(a.denominator for a in cost))
        B = max([1]+[ceil(abs(b)) for b in ds])
        A0 = max([1]+[ceil(abs(a)) for a in cost])
        Hstar = ceil(max(map(abs,ys)))+n
        # A bounded smaller sublattice gives many nontrivial submodular comparisons.
        ranges = [range(floor(ys[i])-1,floor(ys[i])+2) for i in ints]
        values = {}
        for labels in product(*ranges):
            fixed = dict(zip(ints,labels))
            if any(u in fixed and v in fixed and fixed[u]-fixed[v] < ceil(b) for (u,v),b in zip(edges,ds)):
                continue
            val,y = lp(n,edges,ds,cost,fixed)
            need(all(k % x.denominator == 0 for x in y), 'tight-forest coordinate denominator')
            need(k*q % val.denominator == 0, 'value denominator divides kq')
            need(abs(val) <= n*A0*(Hstar+n*B), 'uniform value magnitude')
            need(max(map(abs,y)) <= Hstar+n*B, 'forest magnitude')
            values[labels] = val
            slices += 1
        for p,pv in values.items():
            for z,zv in values.items():
                meet = tuple(map(min,p,z)); join = tuple(map(max,p,z))
                need(meet in values and join in values, 'partial domain minmax closure')
                need(pv+zv >= values[meet]+values[join], 'partial LP submodularity')
                pairs += 1
        # Construct a mixed feasible point using original positive coordinates.
        common = max([0]+[ceil(b) for b in ds])+5
        y = tuple(Q(common+i) if any(u==i for u,v in edges) or i==0 else Q(-common-i)
                  for i in range(n))
        need(all(y[u]-y[v] >= b for (u,v),b in zip(edges,ds)), 'constructed cover feasibility')
        d = tuple(x-z for x,z in zip(y,ys))
        for w,r in layers(d):
            need(all((ys[u]+w*r[u])-(ys[v]+w*r[v]) >= b for (u,v),b in zip(edges,ds)),
                 'one layer remains LP feasible')
            need(dot(cost,r) >= 0, 'LP layer objective direction')
            if w >= 1:
                yz = tuple(v-ri for v,ri in zip(y,r))
                need(all(yz[u]-yz[v] >= b for (u,v),b in zip(edges,ds)), 'mixed removal row feasibility')
                need(all(yz[i].denominator==1 for i in ints), 'mixed removal selected integrality')
                need(dot(cost,yz) <= dot(cost,y), 'mixed removal objective')
                removal_checks += 1
        models += 1
    # Large binary demands/objectives, with distinct denominator factors.
    big = Q(2**211+19,2**127-1)
    edges = ((0,1),(0,2)); ds = (big,-Q(2**193+7,2**89-1)); cost=(Q(5,2**107-1),-Q(5,2**107-1),Q(0))
    val,y = lp(3,edges,ds,cost,{0:ceil(big)+3})
    k=lcm(*(b.denominator for b in ds)); q=lcm(*(a.denominator for a in cost))
    need(k*q % val.denominator == 0,'large input value denominator')
    # Min/max in original cover coordinates must fail; this guards against wrong model transfer.
    p=(Q(1),Q(0)); z=(Q(0),Q(1)); meet=tuple(map(min,p,z))
    need(sum(p)>=1 and sum(z)>=1 and sum(meet)<1,'original-variable minmax counterexample')
    return {'models':models,'slice_lps':slices,'submodular_pairs':pairs,'removal_checks':removal_checks,
            'large_binary_input':{'demand_numerator_bits':big.numerator.bit_length(),'k_bits':k.bit_length(),'q_bits':q.bit_length(),'value_denominator_bits':val.denominator.bit_length()},
            'original_cover_meet_counterexample':{'p':['1','0'],'q':['0','1'],'infeasible_meet':['0','0'],'demand':'1'}}


def check_actual_hull_boundaries():
    # One all-integer edge: actual hull y0-y1 >= ceil(b), versus its weaker LP.
    b=Q(4,3); boundary=(Q(5,2),Q(1,2)); outside=(Q(23,10),Q(1,2))
    need(boundary[0]-boundary[1]==ceil(b),'integer hull boundary')
    need(outside[0]-outside[1]>=b and outside[0]-outside[1]<ceil(b),'LP feasible hull outside')
    # Boundary is midpoint of actual mixed points; a rational recession shift is finite interpolation.
    endpoints=((Q(2),Q(0)),(Q(3),Q(1)))
    need(tuple((x+y)/2 for x,y in zip(*endpoints))==boundary,'boundary actual convex combination')
    d=(Q(-1),Q(-1)); t=Q(17,5); m=floor(t); alpha=t-m
    shifted=tuple(x+t*ri for x,ri in zip(boundary,d))
    step_lo=tuple(x+m*ri for x,ri in zip(boundary,d));step_hi=tuple(x+(m+1)*ri for x,ri in zip(boundary,d))
    need(tuple((1-alpha)*x+alpha*y for x,y in zip(step_lo,step_hi))==shifted,'lineality interpolation')
    # I empty and empty E are not excluded by definitions; B=1 and no facets in R^n.
    need(max([1]+[])==1,'empty-edge B convention')
    return {'boundary':['5/2','1/2'],'outside_lp_feasible':['23/10','1/2'],
            'hull_separator':'y0-y1 >= 2','negative_lineality_step':'17/5',
            'empty_edge_B':1,'zero_dimension':'immediate singleton in R^0'}


def check_completion_and_unbounded():
    # Rounding a row with one continuous coordinate would change the exact value.
    v,y=lp(2,((0,1),),(Q(4,3),),(Q(1),Q(-1)),{0:0})
    bad,_=lp(2,((0,1),),(Q(2),),(Q(1),Q(-1)),{0:0})
    need(v==Q(4,3) and y==(Q(0),Q(-4,3)) and bad==2,'continuous-row rounding diagnostic')
    # Huge rational recession certificate; clearing coordinate denominators has additive bit length.
    p=2**107-1;q=2**89-1;r=(Q(-1,p),Q(-1,q));cost=(Q(p),Q(0))
    need(r[0]-r[1]>=0 and dot(cost,r)<=-1,'rational improving ray')
    multiplier=lcm(*(x.denominator for x in r));integer=tuple(multiplier*x for x in r)
    need(all(x.denominator==1 for x in integer),'cleared ray integral')
    need(dot(cost,integer)<-1,'strict GLS ray normalization')
    z=(Q(2),Q(-2))
    for m in (0,1,2,10**20):
        step=tuple(x+m*d for x,d in zip(z,integer))
        need(step[0]-step[1]>=Q(4,3) and all(x.denominator==1 for x in step),'integer ray steps feasible')
    need(multiplier.bit_length()<=p.bit_length()+q.bit_length(),'ray bit bound')
    return {'continuous_integer_row_unrounded_optimum':'4/3','wrong_all_row_rounding_optimum':'2',
            'rational_ray_denominator_bits':[p.bit_length(),q.bit_length()],
            'clearing_multiplier_bits':multiplier.bit_length(),'integer_steps_checked':[0,1,2,10**20]}


def main():
    report={'status':'PASS','optimization_mode':sys.flags.optimize,
            'thresholds':check_thresholds(),'rings':check_rings(),
            'lp_values':check_lp_values(),'hull_boundaries':check_actual_hull_boundaries(),
            'completion_unbounded':check_completion_and_unbounded(),
            'limitation':'Finite exact adversarial diagnostics, not an implementation of polynomial LP/SFM/GLS or a universal proof.'}
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
