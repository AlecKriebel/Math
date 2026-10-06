#!/usr/bin/env python3
"""Exact finite checks supporting, not replacing, the accompanying proofs."""
import itertools
import json
import math


def require(condition, message):
    if not condition:
        raise ValueError(message)


def h_from_f(f):
    # f includes the empty face in position zero.
    n = len(f) - 1
    return [sum((-1) ** (k-j) * math.comb(n-j, n-k) * f[j]
                for j in range(k+1)) for k in range(n+1)]


def hdouble(d, h):
    out = [1]
    for k in range(1, d+1):
        correction = math.comb(d+1, k) * sum(
            (-1) ** (k-1-j) * math.comb(d, j) for j in range(1, k))
        out.append(h[k] - correction)
    out.append(1)
    return out


def norm(vertices, q):
    vertices = tuple(sorted(vertices))
    first = vertices[0]
    return (sum(first) % q,
            tuple(tuple(x-y for x, y in zip(v, first)) for v in vertices))


def vertices(key):
    residue, offsets = key
    return tuple((v[0]+residue,) + v[1:] for v in offsets)


def regularity(key, q):
    vs = vertices(key)
    require(len({sum(v) % q for v in vs}) == len(vs),
            'Closed simplex has identified vertices')


def face_keys(key, q, size):
    return tuple(norm(vs, q) for vs in itertools.combinations(vertices(key), size))


def rank_f2(columns):
    pivots = {}
    for col in columns:
        while col:
            pivot = col.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = col
                break
            col ^= pivots[pivot]
    return len(pivots)


def quotient(d, q):
    cells = [set() for _ in range(d+1)]
    for residue in range(q):
        for perm in itertools.permutations(range(d)):
            p = [residue]+[0]*(d-1)
            vs = [tuple(p)]
            for axis in perm:
                p[axis] += 1
                vs.append(tuple(p))
            key = norm(vs, q)
            regularity(key, q)
            for size in range(1, d+2):
                cells[size-1].update(face_keys(key, q, size))
    cells = [sorted(level) for level in cells]
    lower_intervals = 0
    for k, level in enumerate(cells):
        for cell in level:
            regularity(cell, q)
            below = []
            for size in range(1, k+2):
                keys = face_keys(cell, q, size)
                require(len(set(keys)) == math.comb(k+1, size), 'Boolean face count')
                require(set(keys) <= set(cells[size-1]), 'Face missing from quotient')
                below.extend((size, key) for key in keys)
            require(len(set(below))+1 == 2**(k+1), 'Boolean lower interval')
            lower_intervals += 1
    indices = [{cell:i for i,cell in enumerate(level)} for level in cells]
    boundaries = [[]]
    for k in range(1, d+1):
        columns = []
        for cell in cells[k]:
            value = 0
            for face in face_keys(cell, q, k):
                value ^= 1 << indices[k-1][face]
            columns.append(value)
        boundaries.append(columns)
    for k in range(2, d+1):
        for col in boundaries[k]:
            boundary2 = 0
            while col:
                bit = col & -col
                boundary2 ^= boundaries[k-1][bit.bit_length()-1]
                col ^= bit
            require(boundary2 == 0, 'Boundary squared is nonzero')
    incidences = [0]*len(cells[d-1])
    for col in boundaries[d]:
        while col:
            bit = col & -col
            incidences[bit.bit_length()-1] += 1
            col ^= bit
    require(set(incidences) == {2}, 'Ridge incidence is not two')
    f = [len(level) for level in cells]
    require(f[0] == q, 'Vertex count')
    require(f[-1] == q*math.factorial(d), 'Lattice volume facet count')
    require(sum((-1)**k*v for k,v in enumerate(f)) == 0, 'Euler characteristic')
    h = h_from_f([1]+f)
    hd = hdouble(d, h)
    require(hd == hd[::-1] and min(hd) >= 0, 'Torus h-double-prime conditions')
    require(f[-1] == math.comb(2*d,d)+sum(hd[1:-1]), 'Facet identity')
    result = {'dimension':d, 'lattice_index':q, 'f_vector':f,
              'h_double_prime':hd, 'verified_boolean_intervals':lower_intervals,
              'boundary_squared_zero':True, 'ridge_incidence_two':True}
    if d <= 4:
        ranks = [0]+[rank_f2(columns) for columns in boundaries[1:]]+[0]
        betti = [f[k]-ranks[k]-ranks[k+1] for k in range(d+1)]
        require(betti == [math.comb(d,k) for k in range(d+1)], 'Torus Betti numbers')
        result['betti_mod_2'] = betti
    return result


def run():
    identities = 0
    for d in range(1,101):
        for k in range(1,d+1):
            lhs = sum((-1)**(k-1-j)*math.comb(d,j) for j in range(1,k))
            rhs = math.comb(d-1,k-1)-(-1)**(k-1)
            require(lhs == rhs, 'Alternating Betti identity')
            identities += 1
        vand = sum(math.comb(d+1,k)*math.comb(d-1,k-1) for k in range(1,d+1))
        alt = sum(math.comb(d+1,k)*(-1)**(k-1) for k in range(1,d+1))
        require(vand == math.comb(2*d,d), 'Vandermonde identity')
        require(alt == 1+(-1)**(d+1), 'Endpoint cancellation')
        identities += 2
    candidates = []
    # Four-vertex decompositions are excluded by the cited Basak-Datta theorem,
    # not by this numerical enumeration. This is not a gluing enumeration.
    for v in range(5,25):
        for middle in range(24):
            F = 20+2*(v-4)+middle
            if F < 24:
                f = [v, v+F, 2*F, F]
                h = h_from_f([1]+f)
                hd = hdouble(3,h)
                require(hd == [1,v-4,middle,v-4,1], 'Candidate transform')
                candidates.append({'f_vector':f, 'h_double_prime':hd})
    require([x['f_vector'] for x in candidates] == [[5,27,44,22],[5,28,46,23]],
            'Unexpected numerical obstruction list')
    # The top-cycle equations of boundary(Delta^4) on tetrahedron types.
    parity_cycles = []
    for parities in itertools.product(range(2), repeat=5):
        if all(parities[i] == parities[j] for i,j in itertools.combinations(range(5),2)):
            parity_cycles.append(list(parities))
    require(parity_cycles == [[0]*5,[1]*5], 'Facet-type parity equations')
    products = 0
    for p in range(1,21):
        for q in range(1,21):
            value = math.comb(p+q,p)*math.factorial(p+1)*math.factorial(q+1)
            target = math.factorial(p+q+1)
            require(value-target == math.factorial(p+q)*p*q, 'Product gap')
            products += 1
    examples = [quotient(d,d+1) for d in range(1,6)]
    # An explicitly inadmissible quotient must be rejected, rather than counted
    # as a smaller regular-cell torus.
    rejected = []
    for d in range(2,6):
        try:
            quotient(d,d)
        except ValueError as error:
            require(str(error) == 'Closed simplex has identified vertices', 'Wrong rejection')
            rejected.append(d)
        else:
            raise ValueError('Nonregular quotient escaped rejection')
    return {'problem_id':30001702, 'status':'PARTIAL_UNRESOLVED',
            'universal_factorial_bound_proved':False,
            'identity_checks':identities, 'product_gap_checks':products,
            'three_dimensional_candidates':candidates,
            'facet_type_parity_cycles':parity_cycles,
            'actual_regular_quotient_examples':examples,
            'nonregular_quotient_dimensions_rejected':rejected,
            'scope':'Arithmetic and explicit regular quotients only; no exhaustive torus search.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
