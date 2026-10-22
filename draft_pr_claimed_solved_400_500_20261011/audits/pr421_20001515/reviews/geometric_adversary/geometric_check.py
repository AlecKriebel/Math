#!/usr/bin/env python3
"""Independent finite cubical incidence audit; standard library only.

No source verifier is imported or executed.  Edges are signed tuples; links
retain source incidences before identifying their vertex-name sets.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
import json


def inv(h):
    return h[0], -h[1]


def negword(w):
    return [inv(h) for h in reversed(w)]


def rotations(w):
    return [w[k:] + w[:k] for k in range(len(w))]


def equivalent(w, v):
    return w in rotations(v) + rotations(negword(v))


def germ(h):
    return h[0] + ('+' if h[1] == 1 else '-')


def named(simplex):
    return tuple(sorted(simplex))


def corner_pairs(w):
    return [(inv(w[k - 1]), w[k]) for k in range(len(w))]


def lam(h):
    e, s = h
    return ({'x': 'y', 'y': 'x', 'b': 'b'}[e], -s if e == 'b' else s)


BASE = [ [('x', 1), ('y', 1), ('x', -1), ('y', -1)],
         [('b', 1), ('x', 1), ('b', -1), ('y', -1)] ]
MODEL = {
    'vertices': ['A', 'B', 'C', 'D'],
    'edges': {
        'p': ('B', 'A', ('x', 1)), 'q': ('A', 'C', ('y', 1)),
        'r': ('D', 'C', ('x', 1)), 's': ('B', 'D', ('y', 1)),
        'd': ('A', 'B', ('b', 1)), 'e': ('C', 'A', ('b', 1))},
    'squares': [[('p', 1), ('q', 1), ('r', -1), ('s', -1)],
                [('d', 1), ('p', 1), ('e', -1), ('q', -1)]],
    'cube_indices': [0, 1], 'merge_vertical': {}}


def orientation(data, h):
    a, b, ell = data['edges'][h[0]]
    return (a, b, ell) if h[1] == 1 else (b, a, inv(ell))


def link_audit(vertices, edge_inc, triangle_inc=()):
    errors = []
    ec = Counter(named(pair) for pair, _ in edge_inc)
    tc = Counter(named(tri) for tri, _ in triangle_inc)
    if any(len(set(e)) != 2 for e in ec): errors.append('collapsed_link_edge')
    if any(n != 1 for n in ec.values()): errors.append('duplicate_link_edge')
    if any(len(set(t)) != 3 for t in tc): errors.append('collapsed_link_triangle')
    if any(n != 1 for n in tc.values()): errors.append('duplicate_link_triangle')
    for t in tc:
        if any(named(p) not in ec for p in combinations(t, 2)):
            errors.append('triangle_boundary_missing')
    missing = []
    cliques = defaultdict(list)
    vv = sorted(vertices)
    for k in range(3, len(vv) + 1):
        found = []
        for c in combinations(vv, k):
            if all(named(p) in ec for p in combinations(c, 2)):
                found.append(c)
                if k != 3 or named(c) not in tc: missing.append(c)
        if not found: break
        cliques[k] = found
    if missing: errors.append('nonflag_link')
    return {'errors': sorted(set(errors)), 'vertices': vv,
            'edge_incidence_count': len(edge_inc), 'edge_count': len(ec),
            'triangle_incidence_count': len(triangle_inc), 'triangle_count': len(tc),
            'edges': [list(e) for e in sorted(ec)],
            'triangles': [list(t) for t in sorted(tc)],
            'duplicate_edges': {str(e): n for e,n in ec.items() if n != 1},
            'duplicate_triangles': {str(t):n for t,n in tc.items() if n != 1},
            'clique_counts': {str(k):len(v) for k,v in cliques.items()},
            'missing_simplices': [list(c) for c in missing]}


def audit(data):
    errors = []
    kv = {germ((e,s)) for e in ('x','y','b') for s in (-1,1)}
    ke = [(tuple(germ(h) for h in c), f'K{s}:{k}')
          for s,w in enumerate(BASE) for k,c in enumerate(corner_pairs(w))]
    ka = link_audit(kv,ke)
    errors.extend('K:'+e for e in ka['errors'])
    kel = {named(e) for e,_ in ke}
    if not all(lam(lam((e,s))) == (e,s)
               for e in ('x','y','b') for s in (-1,1)):
        errors.append('lambda_not_involution')
    for si,w in enumerate(BASE):
        if not equivalent([lam(h) for h in w],w):
            errors.append(f'lambda_square_mismatch:{si}')

    qv = defaultdict(set)
    qe = defaultdict(list)
    qcorners = []
    for e,(a,b,ell) in data['edges'].items():
        qv[a].add((e,1)); qv[b].add((e,-1))
    for si,w in enumerate(data['squares']):
        ow = [orientation(data,h) for h in w]
        if any(ow[k][1] != ow[(k+1)%4][0] for k in range(4)):
            errors.append(f'Q_square_not_closed:{si}')
        image = [a[2] for a in ow]
        if not any(equivalent(image,bw) for bw in BASE):
            errors.append(f'Q_square_image_not_a_K_face:{si}')
        corners = []
        for k,(left,right) in enumerate(corner_pairs(w)):
            v = ow[k][0]
            pair = (left,right)
            qe[v].append((pair,f'Q{si}:{k}'))
            corners.append((v,pair))
        qcorners.append(corners)
    qlinks = {}
    for v in data['vertices']:
        image = {h:germ(orientation(data,h)[2]) for h in qv[v]}
        induced = {e for e in kel if set(e) <= set(image.values())}
        if any(h not in qv[v] for pair,_ in qe[v] for h in pair):
            errors.append(f'Q_corner_endpoint_mismatch:{v}')
        mapped = [named(germ(orientation(data,h)[2]) for h in pair)
                  for pair,_ in qe[v]]
        if len(set(image.values())) != len(image):
            errors.append(f'Q_link_map_not_vertex_injective:{v}')
        if len(set(mapped)) != len(mapped):
            errors.append(f'Q_link_map_not_edge_injective:{v}')
        if set(mapped) != induced:
            errors.append(f'Q_link_map_not_full:{v}')
        if any(len(set(e)) != 2 for e in mapped):
            errors.append(f'Q_link_collapsed_corner:{v}')
        qlinks[v] = {'source_germs': [germ(h) for h in sorted(qv[v])],
                     'image_germs': sorted(image.values()),
                     'image_edges': [list(e) for e in sorted(mapped)],
                     'induced_edges': [list(e) for e in sorted(induced)]}

    def vertical(v,s=1):
        return 'z_'+data['merge_vertical'].get(v,v),s

    products = {}
    for e,(a,b,ell) in data['edges'].items():
        products[e] = [ell, vertical(b), inv(lam(ell)), inv(vertical(a))]
    ze = list(ke)
    square_corners = []
    for e,w in products.items():
        for k,c in enumerate(corner_pairs(w)):
            pair = tuple(germ(h) for h in c)
            ze.append((pair,f'product_{e}:{k}'))
            square_corners.append({'square':e,'corner':k,'directions':pair})
    triangles = []
    cube_faces = []
    for si in data['cube_indices']:
        w = data['squares'][si]
        ow = [orientation(data,h) for h in w]
        bword = [a[2] for a in ow]
        tword = [lam(h) for h in bword]
        bm = [i for i,b in enumerate(BASE) if equivalent(bword,b)]
        tm = [i for i,b in enumerate(BASE) if equivalent(tword,b)]
        if len(bm) != 1 or len(tm) != 1:
            errors.append(f'cube_horizontal_face_mismatch:{si}')
        sides = []
        for k,h in enumerate(w):
            a,b,ell = ow[k]
            side = [ell,vertical(b),inv(lam(ell)),inv(vertical(a))]
            if not equivalent(side,products[h[0]]):
                errors.append(f'cube_side_face_mismatch:{si}:{k}')
            sides.append({'Q_edge':germ(h),'product_face':h[0],
                          'boundary':[germ(x) for x in side]})
        cube_faces.append({'cube':si,'bottom_base_face':bm,'top_base_face':tm,
                           'Q_vertex_cycle':[a[0] for a in ow],'side_faces':sides})
        for layer in (0,1):
            for k,(v,pair) in enumerate(qcorners[si]):
                hp = [orientation(data,h)[2] for h in pair]
                if layer == 1: hp = [lam(h) for h in hp]
                tri = tuple([germ(h) for h in hp]+[germ(vertical(v,1 if layer==0 else -1))])
                triangles.append((tri,f'cube_{si}:{layer}:{k}'))
    zv = kv | {germ(vertical(v,s)) for v in data['vertices'] for s in (-1,1)}
    za = link_audit(zv,ze,triangles)
    errors.extend('Z:'+e for e in za['errors'])
    return {'accepted':not errors,'errors':sorted(set(errors)),
            'K_link':ka,'Q_links':qlinks,'Z_link':za,
            'cell_counts': {'vertices':1,'edges':3+len(set(vertical(v)[0] for v in data['vertices'])),
                            'squares':2+len(products),'cubes':len(data['cube_indices'])},
            'product_square_boundaries': {e:[germ(h) for h in w] for e,w in products.items()},
            'product_square_corner_records':square_corners,
            'cube_face_records':cube_faces,
            'cube_corner_records':[{'directions':list(t),'provenance':p} for t,p in triangles]}


def main():
    baseline = audit(deepcopy(MODEL))
    assert baseline['accepted'],baseline['errors']
    assert baseline['cell_counts'] == {'vertices':1,'edges':7,'squares':8,'cubes':2}
    assert baseline['Z_link']['edge_count'] == 32
    assert baseline['Z_link']['triangle_count'] == 16
    assert baseline['Z_link']['clique_counts'] == {'3':16}
    controls = []
    def check_control(name, data, expected):
        result = audit(data)
        assert not result['accepted'],name
        assert expected in result['errors'],(name,expected,result['errors'])
        controls.append({'name':name,'expected_defect':expected,
                         'rejected':True,'detected_errors':result['errors'],
                         'missing_simplices':result['Z_link']['missing_simplices'],
                         'duplicate_edges':result['Z_link']['duplicate_edges']})
    d=deepcopy(MODEL); d['squares']=d['squares'][1:]; d['cube_indices']=[0]
    check_control('omit_first_Q_square',d,'Q_link_map_not_full:A')
    d=deepcopy(MODEL); d['cube_indices']=[1]
    check_control('omit_first_product_cube_keep_all_side_squares',d,'Z:nonflag_link')
    d=deepcopy(MODEL); d['merge_vertical']={'B':'A'}
    check_control('merge_vertical_A_and_B',d,'Z:duplicate_link_edge')
    d=deepcopy(MODEL); d['edges']['r']=('D','C',('y',1))
    check_control('change_r_label_x_to_y',d,'Q_square_image_not_a_K_face:0')
    d=deepcopy(MODEL); d['edges']['r']=('B','C',('x',1))
    check_control('change_r_initial_vertex_D_to_B',d,'Q_square_not_closed:0')
    d=deepcopy(MODEL)
    d['squares']=[negword(w) for w in d['squares']]
    reverse = audit(d)
    assert reverse['accepted']
    assert reverse['Z_link']['edges'] == baseline['Z_link']['edges']
    assert reverse['Z_link']['triangles'] == baseline['Z_link']['triangles']
    print(json.dumps({'generated_at_utc':datetime.now(timezone.utc).isoformat(),
                      'baseline':baseline,'negative_controls':controls,
                      'orientation_reversal_invariance':True,
                      'all_assertions_passed':True},indent=2))


if __name__ == '__main__':
    main()
