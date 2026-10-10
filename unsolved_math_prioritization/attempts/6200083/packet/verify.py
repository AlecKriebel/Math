#!/usr/bin/env python3
"""Exact finite controls; not a decision procedure for boundary topology."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def run():
    assertions = 0
    def check(condition):
        nonlocal assertions
        assertions += 1
        assert condition

    # Exact algebraic upper bounds on parabolic displacement/word length.
    previous = None
    parabolic = []
    for k in range(1, 81):
        n = 2 ** k
        bound = F(2 * (k + 1), n)
        check(F(1) + F(n*n, 2) > 1)
        if previous is not None:
            check(bound < previous)
        previous = bound
        if k in (1, 4, 16, 40, 80):
            parabolic.append({'k': k, 'ratio_upper_bound': str(bound)})
    check(previous < F(1, 10**20))

    def graph(N, horizontal_top=False):
        xs = sorted({F(0)} | {F(1,n) for n in range(1,N+1)})
        ys = [F(0),F(1,4),F(1,2),F(1)]
        vertices = {(x,y) for x in xs for y in ys}
        edges = set()
        for x in xs:
            for y,z in zip(ys,ys[1:]):
                edges.add(frozenset(((x,y),(x,z))))
        for x,z in zip(xs,xs[1:]):
            edges.add(frozenset(((x,F(0)),(z,F(0)))))
            if horizontal_top:
                edges.add(frozenset(((x,F(1,2)),(z,F(1,2)))))
        return vertices, edges

    def components(vertices, edges):
        adj = {v:set() for v in vertices}
        for edge in edges:
            if edge <= vertices:
                a,b = tuple(edge)
                adj[a].add(b)
                adj[b].add(a)
        unseen = set(vertices)
        result = []
        while unseen:
            todo = [unseen.pop()]
            component = set(todo)
            while todo:
                v = todo.pop()
                for w in adj[v] & unseen:
                    unseen.remove(w)
                    component.add(w)
                    todo.append(w)
            result.append(component)
        return result

    combs = []
    for N in (2,3,5,8,13,21,34,55,89):
        vertices,edges = graph(N)
        check(len(components(vertices,edges)) == 1)
        upper = {v for v in vertices if v[1] > F(1,4)}
        cc = components(upper,edges)
        check(len(cc) == N+1)
        p,q = (F(0),F(1,2)), (F(1,N),F(1,2))
        check(not any(p in c and q in c for c in cc))
        check(abs(p[0]-q[0]) == F(1,N))
        # Adding horizontal edges at y=1/2 is a positive control.
        rv,re = graph(N,True)
        check(len(components({v for v in rv if v[1]>F(1,4)},re)) == 1)
        for n in range(N+1,10*N+1):
            # Every point on an omitted tooth is within this bound of x=0.
            check(F(1,n) <= F(1,N+1))
        combs.append({'N':N,'upper_components':len(cc),
                      'nearby_pair_distance':str(F(1,N)),
                      'continuum_diameter_lower_bound':'1/2',
                      'hausdorff_upper_bound':str(F(1,N+1))})

    # exp(rho) in a cone normalized to boundary diameter 1.
    def exp_rho(d,u,v):
        return (d+max(u,v))**2/(u*v)

    cone_cases = 0
    for k in range(0,16):
        u=F(1,2**k)
        for n in range(1,33):
            d=F(1,n)
            v=F(1,2**(k//2))
            check(exp_rho(d,u,u) <= (1+1/u)**2)
            check(exp_rho(d,u/2,u/2) > exp_rho(d,u,u))
            check(exp_rho(0,u,u) == 1)
            check(exp_rho(0,u,v) == max(u/v,v/u))
            check(exp_rho(d,u,v) == exp_rho(d,v,u))
            # Exponential form of the displayed Gromov product at a base z.
            # Any metric x-distance data satisfying the triangle inequalities.
            a,b=F(1,2),F(1,2)
            check(abs(a-b) <= d <= a+b)
            direct=((1+a)**2/u)*((1+b)**2/v)/exp_rho(d,u,v)
            formula=((1+a)*(1+b)/(d+max(u,v)))**2
            check(direct == formula)
            cone_cases += 1

    return {'all_passed':True,'assertions':assertions,
            'parabolic_bound_samples':parabolic,'comb_cases':combs,
            'cone_cases':cone_cases,
            'scope':'Exact finite graph and rational metric controls only. '
                    'Infinite topology and cited theorem applications require '
                    'the written proofs and source inspection.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true',
                        help='write controls.json during author preparation')
    parser.add_argument('--source-dir',type=Path,
                        help='optionally check independently retrieved source PDF bytes')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    result=run()
    if args.write:
        (root/'controls.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        expected=json.loads((root/'controls.json').read_text())
        assert result==expected, 'control result mismatch'
    if args.source_dir:
        meta=json.loads((root/'verification_metadata.json').read_text())
        for item in meta['sources']:
            if not item.get('pdf'):
                continue
            path=args.source_dir/(item['id']+'.pdf')
            data=path.read_bytes()
            assert len(data)==item['bytes'], item['id']+' byte count'
            assert hashlib.sha256(data).hexdigest()==item['sha256'], item['id']+' hash'
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
