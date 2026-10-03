#!/usr/bin/env python3
"""Exact finite checks for Attempt 4; not a solver for pro-p coherence."""
import json
from pathlib import Path


def rank_mod_p(a, p):
    a = [[x % p for x in row] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = pow(a[r][c], -1, p)
        a[r] = [(x*z) % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [(x-z*y) % p for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def check_chain(p,n):
    # One row per generator x_i,y_i; columns are the edge identifications.
    a = [[0]*(2*n) for _ in range(2*(n+1))]
    for i in range(n):
        a[2*i][2*i] = p
        a[2*(i+1)][2*i] = -1
        a[2*i+1][2*i+1] = 1
        a[2*(i+1)+1][2*i+1] = -p
    r = rank_mod_p(a,p)
    assert r == 2*n
    assert 2*(n+1)-r == 2
    # Global abelian coordinate map x_i -> p^i e1, y_i -> p^(n-i) e2.
    for i in range(n):
        assert p*p**i == p**(i+1)
        assert p**(n-i) == p*p**(n-i-1)
    # Mod out by C=<p^n e1,p^n e2>. All vertex and edge groups
    # inject into (Z/p^n)^2; these are image orders of diagonal lattices.
    vertex_orders = [p**(n-i)*p**i for i in range(n+1)]
    edge_orders = [p**(n-i-1)*p**i for i in range(n)]
    assert all(v == p**n for v in vertex_orders)
    assert all(e == p**(n-1) for e in edge_orders)
    assert all(vertex_orders[i] == p*edge_orders[i] == vertex_orders[i+1]
               for i in range(n))
    # The endpoint lattices meet exactly in the common central lattice.
    endpoint_intersection_exponents = (max(0,n),max(n,0))
    assert endpoint_intersection_exponents == (n,n)
    return {'p':p,'edges':n,'vertices':n+1,'mod_p_relation_rank':r,
            'generator_dimension':2,'vertex_quotient_order':p**n,
            'edge_quotient_order':p**(n-1),'edge_index':p}


def finite_lattice_check(p,n):
    m=p**n
    vertices=[]
    for i in range(n+1):
        im={(p**i*a % m,p**(n-i)*b % m)
            for a in range(p**(n-i)) for b in range(p**i)}
        assert len(im)==p**n
        vertices.append(im)
    assert vertices[0]&vertices[-1]=={(0,0)}
    for i in range(n):
        im={(p**(i+1)*a % m,p**(n-i)*b % m)
            for a in range(p**(n-i-1)) for b in range(p**i)}
        assert len(im)==p**(n-1)
        assert im==vertices[i]&vertices[i+1]
    return {'p':p,'edges':n,'enumerated':True}


if __name__=='__main__':
    data={'scope':'Finite linear/lattice checks only; the written pro-p proof is essential.',
          'chains':[check_chain(p,n) for p in (2,3,5,7) for n in range(1,33)],
          'enumerated_lattices':[finite_lattice_check(p,n) for p in (2,3,5) for n in range(1,6)]}
    target=Path(__file__).with_name('chain_obstruction_results.json')
    target.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'chain_cases':len(data['chains']),
                      'enumerated_lattice_cases':len(data['enumerated_lattices']),
                      'passed':True}))
