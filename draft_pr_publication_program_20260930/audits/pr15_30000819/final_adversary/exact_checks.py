#!/usr/bin/env python3
"""Fresh exact falsifiers; only this directory's receipt may be regenerated.

No candidate or sibling mathematical code is imported. General proof is in
INDEPENDENT_FIRST_PASS.md and REPORT.md. The triangle certificate bounds every
degree by explicit saturation-module conductors. The BDGM family uses a directly
derived integer-fiber description rather than an unexplained cutoff.
"""
from pathlib import Path
from itertools import combinations, product
from math import gcd, comb
from functools import reduce
import json

assertions = 0


def check(condition):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(f"exact assertion {assertions} failed")


def sum_layers(a, last):
    d = len(a[0])
    layers = [{(0,) * d}]
    for _ in range(last):
        layers.append({tuple(x[j] + v[j] for j in range(d))
                       for x in layers[-1] for v in a})
    return layers


def det3(columns):
    a, b, c = columns
    return (a[0] * (b[1] * c[2] - c[1] * b[2])
            - b[0] * (a[1] * c[2] - c[1] * a[2])
            + c[0] * (a[1] * b[2] - b[1] * a[2]))


def primitive(u):
    g = reduce(gcd, (abs(t) for t in u))
    return tuple(t // g for t in u) if g else None


def triangle_circuits(a, volume):
    cols = tuple(v + (1,) for v in a)
    circuits = []
    for ids in combinations(range(len(a)), 3):
        sub = tuple(cols[i] for i in ids)
        if det3(sub):
            continue
        rows = tuple(tuple(v[j] for v in sub) for j in range(3))
        u = None
        for r, s in combinations(rows, 2):
            u = primitive((r[1] * s[2] - r[2] * s[1],
                           r[2] * s[0] - r[0] * s[2],
                           r[0] * s[1] - r[1] * s[0]))
            if u:
                break
        check(u is not None and all(u))
        circuits.append((ids, u))
    for ids in combinations(range(len(a)), 4):
        sub = tuple(cols[i] for i in ids)
        minors = tuple((-1) ** i * det3(sub[:i] + sub[i+1:])
                       for i in range(4))
        if all(minors):
            circuits.append((ids, primitive(minors)))
    index_values = set()
    for ids, u in circuits:
        check(all(sum(cols[i][j] * t for i, t in zip(ids, u)) == 0
                  for j in range(3)))
        degree = sum(t for t in u if t > 0)
        check(degree <= volume)
        check(len(ids) <= 2 * degree)
        extended = ids
        if len(ids) == 3:
            extended = ids + (next(i for i in range(len(a)) if i not in ids
                                  and det3((cols[ids[0]], cols[ids[1]], cols[i]))),)
        sub = tuple(cols[i] for i in extended)
        signed = tuple((-1) ** i * det3(sub[:i] + sub[i+1:])
                       for i in range(4))
        index = reduce(gcd, (abs(t) for t in signed))
        index_values.add(index)
        check(index >= 1)
        check(sum(max(t, 0) for t in signed) == index * degree)
        check(index * degree <= volume)
    # An explicit rational-kernel basis, each with its own nonzero last entry.
    basis = []
    for i, (x, y) in enumerate(a[3:], 3):
        u = [x+y-1, -x, -y] + [0] * (len(a)-3)
        u[i] = 1
        check(all(sum(cols[t][j] * u[t] for t in range(len(a))) == 0
                  for j in range(3)))
        basis.append(u)
    check(all(any(u[i] for u in basis) for i in range(len(a))))
    check(len(a) <= 2 * volume * len(basis))
    check(len(basis) <= volume-1)
    return {'circuits': len(circuits), 'complement_indices': sorted(index_values)}


def triangle_family(m):
    a = ((0, 0), (1, 0), (0, 1), (m, 0), (m-1, 0),
         (m-1, 1), (0, m), (0, m-1), (1, m-1))
    check(len(set(a)) == 9)
    # The first three selected points certify the full generated lattice.
    check(det3(tuple(v + (1,) for v in a[:3])) == 1)
    residues = []
    cutoff = 0
    for x, y in product(range(m), repeat=2):
        k = (x+y+m-1) // m
        bounds = (max(0, x+y-k), max(0, (m-1)*k-x),
                  max(0, (m-1)*k-y))
        # Explicit S-representations of b+N_i a_i at each vertex:
        witness0 = [(0, 0)] * (k+bounds[0]-x-y) + [(1, 0)]*x + [(0, 1)]*y
        deficiency1 = m*k-x
        witness1 = [(m, 0)] * (k+bounds[1]-deficiency1) + [(m-1, 1)]*y + [(m-1, 0)]*(deficiency1-y)
        deficiency2 = m*k-y
        witness2 = [(0, m)] * (k+bounds[2]-deficiency2) + [(1, m-1)]*x + [(0, m-1)]*(deficiency2-x)
        for i, w in enumerate((witness0, witness1, witness2)):
            target = ((x, y), (x+m*bounds[1], y), (x, y+m*bounds[2]))[i]
            check(len(w) == k+bounds[i])
            check(tuple(sum(v[j] for v in w) for j in range(2)) == target)
            check(all(v in a for v in w))
        residues.append((x, y, k, bounds))
        if all(bounds):
            cutoff = max(cutoff, k+sum(t-1 for t in bounds))
    layers = sum_layers(a, cutoff+3)
    residue_holes = set()
    for x, y, k, bounds in residues:
        for t0, t1, t2 in product(*(range(t) for t in bounds)):
            degree = k+t0+t1+t2
            p = (x+m*t1, y+m*t2)
            if p not in layers[degree]:
                residue_holes.add(p + (degree,))
    direct_holes = set()
    counts = []
    for k, layer in enumerate(layers):
        saturation = {(x, y) for x in range(m*k+1)
                      for y in range(m*k+1-x)}
        check(layer <= saturation)
        holes = saturation - layer
        counts.append(len(holes))
        direct_holes.update(p + (k,) for p in holes)
        if k > cutoff:
            check(not holes)
    check(direct_holes == residue_holes)
    h = max((p[-1] for p in residue_holes), default=-1)
    check(bool(residue_holes))
    check(h <= 2*(m*m)**2*(m*m-1)**2-2)
    return {'m': m, 'dimension': 2, 'n': 9, 'intrinsic_volume': m*m,
            'residues': m*m, 'all_degree_certificate_cutoff': cutoff,
            'highest_hole': h, 'total_holes': len(residue_holes),
            'degree_hole_counts': counts,
            'circuit_checks': triangle_circuits(a, m*m)}


def bdgm_family(m):
    a = ((0,0,0), (0,0,1), (1,0,0), (1,0,1),
         (0,1,0), (0,1,1), (1,1,m), (1,1,m+1))
    # Unit differences certify generated lattice Z^3; no saturation-index guess.
    check(set(a) >= {(0,0,0), (1,0,0), (0,1,0), (0,0,1)})
    layers = sum_layers(a, m+2)
    counts = []
    witnesses = []
    for k, layer in enumerate(layers):
        saturation = set()
        predicted_sums = set()
        gap_intervals = 0
        for x, y in product(range(k+1), repeat=2):
            low, high = max(0, x+y-k), min(x, y)
            saturation.update((x, y, z) for z in range(m*low, m*high+k+1))
            predicted_sums.update((x, y, m*j+t) for j in range(low, high+1)
                                  for t in range(k+1))
            gap_intervals += high-low
        check(layer == predicted_sums)
        check(layer <= saturation)
        check(gap_intervals == comb(k+1, 3))
        holes = saturation-layer
        expected = comb(k+1,3)*max(0,m-k-1)
        check(len(holes) == expected)
        counts.append(len(holes))
        if holes:
            witnesses.append({'degree': k, 'example': min(holes)})
        if k >= m-1:
            check(not holes)
    check(counts[1] == 0 and counts[2] == m-3)
    check(max(w['degree'] for w in witnesses) == m-2)
    # u is a degree-two normalization generator which cannot be a product of
    # normalized degree-one monomials, because their set is precisely a.
    u = (1,1,3)
    check(u not in layers[2])
    check(0 <= u[2] <= m+2)
    check(all(v in layers[1] for v in a) and len(layers[1]) == 8)
    # m*u is in S: 3 D0, m-3 B0, m-3 C0 and 3 A0 give degree 2m.
    power_witness = [(1,1,m)]*3 + [(1,0,0)]*(m-3) + [(0,1,0)]*(m-3) + [(0,0,0)]*3
    check(len(power_witness) == 2*m)
    check(tuple(sum(v[j] for v in power_witness) for j in range(3)) == tuple(m*t for t in u))
    return {'m':m, 'dimension':3, 'n':8, 'intrinsic_volume':m+6,
            'highest_hole':m-2, 'degree_hole_counts':counts,
            'normalization_not_degree_one_generated':True,
            'degree_two_witness':u, 'positive_power_in_original_ring':m,
            'sample_holes':witnesses}


def mutation_falsifiers():
    rejected = []
    def reject(name, predicate, witness):
        check(not predicate())
        rejected.append({'mutation':name, 'witness':witness, 'rejected':True})
    reject('extend nonempty-hole quartic formula to empty V=1 with h=-1',
           lambda: -1 <= 2*1**2*(1-1)**2-2, {'h':-1,'V':1,'rhs':-2})
    reject('replace chosen degree-one generators by all lattice points',
           lambda: set(sum_layers(((0,), (1,), (3,), (4,)),1)[1]) == {(i,) for i in range(5)},
           {'configuration':[0,1,3,4], 'missing_height_one_point':2})
    # A hypersurface/free index-two segment is intrinsically normal but has
    # ambient odd holes in every positive degree.
    reject('finite ambient holes allow a proper generated-group index',
           lambda: (1,) in sum_layers(((0,), (2,)),5)[5],
           {'configuration':[0,2], 'generated_slice':'2Z', 'ambient_point':1, 'degree':5})
    reject('normalization of an eligible finite-hole ring is generated in degree one',
           lambda: (1,1,3) in sum_layers(((0,0,0),(0,0,1),(1,0,0),(1,0,1),(0,1,0),(0,1,1),(1,1,4),(1,1,5)),2)[2],
           {'BDGM_m':4,'normalized_degree_two_point':[1,1,3],'all_degree_one_points_selected':True})
    reject('homogeneous circuit degree bound applies without primitive normalization',
           lambda: sum(max(t,0) for t in (3,-3,-3,3)) <= 2,
           {'square_volume':2,'nonprimitive_relation':[3,-3,-3,3],'degree':6})
    # A4 has C concentrated in degree 1; normalization is the fourth Veronese
    # of C[s,t], whose reg is 1. Hence reg R=2 and reg I=3 by local cohomology.
    reject('replace subtract-two by subtract-three',
           lambda: 1 <= 3-3, {'A4_h':1,'reg_I_by_written_cohomology_derivation':3})
    reject('interval coverage iff k>=m-2 includes k=0',
           lambda: ({0} == {0}) == (0 >= 4-2), {'m':4,'k':0,'coverage':True})
    # A4 plus 20 independent apex coordinates has n=24,c=2,V=4, and infinite
    # holes: (2,e_last*(k-1),k) always forces one missing base generator.
    reject('drop finite nonempty holes from generator count bound',
           lambda: 24 <= 2*4*2,
           {'twenty_fold_pyramid_over_A4':True,'n':24,'c':2,'V':4,'holes':'infinite'})
    return rejected


def main():
    triangles = [triangle_family(m) for m in range(3,10)]
    bdgm = [bdgm_family(m) for m in range(4,10)]
    mutants = mutation_falsifiers()
    # The printed BDGM m>=3 highest-gap sentence has an empty-case boundary:
    # for m=3 the gaps have length max(0,3-k-1), while the number of gaps is
    # binomial(k+1,3); these never are positive at the same k. Thus no holes.
    for k in range(12):
        check(comb(k+1,3)*max(0,3-k-1) == 0)
    result = {'passed':True,'arithmetic':'exact Python integers and sets; determinant minors',
              'independent_of_candidate_and_family_code':True,
              'assertions':assertions,'triangle_families':triangles,
              'BDGM_m3_empty_boundary':'No holes in any degree by the written fiber argument; no highest-hole height assigned.',
              'bdgm_normalization_families':bdgm,'mutation_falsifiers':mutants,
              'scope':'All-degree certificates for these families supplement the separately checked general proof; computed tests do not prove the theorem.'}
    Path(__file__).with_name('exact_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'assertions':assertions,
                      'triangle_families':len(triangles),'bdgm_families':len(bdgm),
                      'circuits':sum(t['circuit_checks']['circuits'] for t in triangles),
                      'mutations_rejected':len(mutants)},indent=2))


if __name__ == '__main__':
    main()
