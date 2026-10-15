#!/usr/bin/env python3
"""Independent exact kernel checks, using incremental constraint intersection.

This does not import or execute the candidate checker. It builds kernels by
intersecting the current basis with each force-balance hyperplane. No assert
statement is used; all checks survive Python optimization.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
import os
import sys

class AuditFailure(Exception):
    pass

def demand(test, message):
    if not test:
        raise AuditFailure(message)

def sign(x):
    return (x > 0) - (x < 0)

def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), Q(0))

def kernel(equations, width):
    # Start with the ambient coordinate basis. Each equation eliminates one
    # current basis vector, keeping an explicit basis for the intersection.
    basis = [tuple(Q(i == j) for i in range(width)) for j in range(width)]
    for equation in equations:
        values = [dot(equation, b) for b in basis]
        if not any(values):
            continue
        pivot = max(j for j,c in enumerate(values) if c)
        b = basis[pivot]
        basis = [tuple(x-values[j]/values[pivot]*y for x,y in zip(v,b))
                 for j,v in enumerate(basis) if j != pivot]
    demand(all(dot(r,b)==0 for r in equations for b in basis), 'kernel residual')
    return basis

def points(n, d, e, t):
    demand(n >= 1 and d >= 1, 'positive n,d required')
    demand(e[0] < e[1] and e[0]>=0 and e[1]<n, 'bad distinguished edge')
    demand(Q(-1,2) <= t <= Q(1,2), 'path interval')
    scalars = [Q(10+3*k) for k in range(n)]
    scalars[e[0]], scalars[e[1]] = t,Q(0)
    direction = [Q(2*k+1) * (-1 if k%2 else 1) for k in range(d)]
    return [tuple(s*a for a in direction) for s in scalars]

def equations(edges, p):
    # Vertex-first construction, independently of the candidate column fill.
    d = len(p[0])
    return [tuple(p[v][r]-p[i][r] if i==u else
                  p[u][r]-p[i][r] if i==v else Q(0)
                  for u,v in edges)
            for i in range(len(p)) for r in range(d)]

def factors(edges, p, q):
    return tuple((p[v][0]-p[u][0])/(q[v][0]-q[u][0]) for u,v in edges)

def transport_check(edges, p, q, diagonal):
    demand(len(diagonal)==len(edges), 'diagonal shape')
    demand(all(c>0 for c in diagonal), 'sign-preserving invertibility')
    a,b=equations(edges,p),equations(edges,q)
    k,l=kernel(a,len(edges)),kernel(b,len(edges))
    demand(len(k)==len(l), 'kernel dimensions differ')
    for basis, target, scale in ((k,b,diagonal),(l,a,tuple(1/x for x in diagonal))):
        for v in basis:
            image=tuple(c*x for c,x in zip(scale,v))
            demand(tuple(map(sign,v))==tuple(map(sign,image)), 'coordinate sign including zero')
            demand(all(dot(row,image)==0 for row in target), 'transported vector not equilibrium')
    return len(k)

def single_support_check(edges,p,q,e):
    j=edges.index(e)
    unit=tuple(Q(k==j) for k in range(len(edges)))
    demand(all(dot(r,unit)==0 for r in equations(edges,p)), 'collision singleton missing')
    demand(any(dot(r,unit)!=0 for r in equations(edges,q)), 'separated singleton retained')

def validate_signs(v,w):
    demand(tuple(map(sign,v))==tuple(map(sign,w)), 'zero and nonzero signs must match')

def graphs(n):
    es=tuple(combinations(range(n),2))
    for mask in range(1<<len(es)):
        yield tuple(e for k,e in enumerate(es) if mask>>k&1)

def components(n,edges):
    visited=set()
    count=0
    for i in range(n):
        if i in visited: continue
        count+=1
        todo=[i]
        while todo:
            u=todo.pop()
            if u in visited: continue
            visited.add(u)
            for a,b in edges:
                if a==u and b not in visited: todo.append(b)
                if b==u and a not in visited: todo.append(a)
    return count

def rejected(label,fn):
    try:
        fn()
    except AuditFailure as ex:
        return {'mutant':label,'rejected':True,'reason':str(ex)}
    raise AuditFailure('accepted semantic mutant: '+label)

def main():
    demand(len(sys.argv)==1,'no arguments supported')
    counts={};pair_counts={};samples=(Q(-1,3),Q(1,7),Q(2,5))
    small_checks=0; pair_checks=0; nullities=set()
    for n in range(1,5):
        universe=tuple(combinations(range(n),2)); allg=list(graphs(n)); count=0
        for h in allg:
            for e in universe:
                if e in h: continue
                count+=1
                g=tuple(sorted(h+(e,)))
                for d in (1,2,4):
                    p=points(n,d,e,Q(0))
                    for t in samples:
                        q=points(n,d,e,t)
                        k=transport_check(h,p,q,factors(h,p,q))
                        # With every graph edge noncollapsed on a line, the
                        # independent graph-incidence nullity formula applies.
                        demand(k==len(h)-n+components(n,h),'cycle-space nullity')
                        single_support_check(g,p,q,e)
                        nullities.add(k);small_checks+=1
        counts[str(n)]=count
        pc=0
        for g,h in combinations(allg,2):
            difference=set(g)^set(h)
            demand(bool(difference),'distinct pair difference')
            e=min(difference)
            containing,omitting=(g,h) if e in g else (h,g)
            p=points(n,2,e,Q(0)); q=points(n,2,e,Q(1,7))
            single_support_check(containing,p,q,e)
            transport_check(omitting,p,q,factors(omitting,p,q))
            pc+=1;pair_checks+=1
        pair_counts[str(n)]=pc
    large=[]
    for n in (5,7,10):
        complete=tuple(combinations(range(n),2))
        for e in ((0,1),(0,n-1),(n-2,n-1)):
            families={
                'dense':tuple(x for x in complete if x!=e),
                'disconnected':tuple(x for x in complete if x!=e and x[0]//3==x[1]//3),
                'forest':tuple(x for x in complete if x!=e and x[1]==x[0]+1),
                'empty':(),
            }
            for name,h in families.items():
                for d in (1,3,5):
                    p=points(n,d,e,Q(0));q=points(n,d,e,Q(-1,3))
                    k=transport_check(h,p,q,factors(h,p,q))
                    demand(k==len(h)-n+components(n,h),'large cycle-space nullity')
                    single_support_check(tuple(sorted(h+(e,))),p,q,e)
                    large.append({'n':n,'d':d,'edge':list(e),'family':name,'nullity':k})
    # A nontrivial cyclic omitting graph makes ratio errors observable on kernels.
    h=((0,2),(0,3),(2,3));e=(0,1)
    p=points(4,2,e,Q(0));q=points(4,2,e,Q(1,7));diag=factors(h,p,q)
    triangle=((0,1),(0,2),(1,2))
    a=points(3,1,(0,1),Q(0));b=points(3,1,(0,1),Q(1,7))
    ka,kb=kernel(equations(triangle,a),3),kernel(equations(triangle,b),3)
    demand(len(ka)==len(kb)==1,'same-nullity triangle')
    demand(tuple(map(sign,ka[0])) != tuple(map(sign,kb[0])),'triangle sign support')
    mutants=[
        rejected('invert length ratio',lambda:transport_check(h,p,q,tuple(1/x for x in diag))),
        rejected('omit length ratio',lambda:transport_check(h,p,q,(Q(1),)*3)),
        rejected('negate diagonal (kernel map, wrong signs)',lambda:transport_check(h,p,q,tuple(-x for x in diag))),
        rejected('singular diagonal',lambda:transport_check(h,p,q,(Q(0),)*3)),
        rejected('allow zero-to-positive coordinate',lambda:validate_signs((Q(1),Q(0)),(Q(1),Q(1)))),
        rejected('replace sign equivalence by dimension',lambda:demand(tuple(map(sign,ka[0]))==tuple(map(sign,kb[0])),'equal dimensions do not give equal sign supports')),
        rejected('claim pair-collision K3 nullity two',lambda:demand(len(ka)==2,'actual pair-collision nullity is one')),
        rejected('permit zero ambient dimension',lambda:points(2,0,(0,1),Q(0))),
        rejected('use separated realization as collision',lambda:single_support_check(((0,1),),points(2,1,(0,1),Q(1,7)),points(2,1,(0,1),Q(2,7)),(0,1))),
    ]
    # Connected-component warning: for one edge on the real line, noncollapsed
    # configurations at t<0,t>0 have identical zero fibers but lie in different
    # components (a path would cross the equality hyperplane). This is not a
    # counterexample to the candidate: its H-path never collapses an H-edge.
    one=((0,1),)
    demand(not kernel(equations(one,points(2,1,(0,1),Q(-1,3))),1),'negative one-edge kernel')
    demand(not kernel(equations(one,points(2,1,(0,1),Q(1,3))),1),'positive one-edge kernel')
    return {'status':'PASS','uid':os.getuid(),'optimization':sys.flags.optimize,
            'independence':'incremental kernel intersection; no candidate import',
            'arithmetic':'exact fractions.Fraction','nonedge_instances':counts,
            'nonedge_transport_checks':small_checks,'distinct_graph_pairs':pair_counts,
            'pair_kernel_checks':pair_checks,'parameters':[str(x) for x in samples],
            'small_dimensions':[1,2,4],'larger_checks':large,
            'triangle_nullities':[len(ka),len(kb)],
            'triangle_basis_at_collision':[[str(x) for x in v] for v in ka],
            'triangle_basis_separated':[[str(x) for x in v] for v in kb],
            'semantic_mutants':mutants,
            'connected_component_warning_checked':True,
            'limits':['finite regression only','no source-intent decision','no novelty certification']}

if __name__=='__main__':
    try:
        print(json.dumps(main(),indent=2,sort_keys=True))
    except AuditFailure as ex:
        print(json.dumps({'status':'FAIL','reason':str(ex)},sort_keys=True))
        sys.exit(1)
