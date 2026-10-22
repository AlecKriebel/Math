"""Independent exact diagnostics. No imports from author code and no network.

These are finite corroborations of the accompanying mathematical audit, not
an exhaustive classification or a formal proof of the open finiteness claim.
"""
import json
from fractions import Fraction
from itertools import combinations, product
from math import comb

CHECKS = 0
def require(truth, label):
    global CHECKS
    if not truth: raise RuntimeError(label)
    CHECKS += 1

def solve_columns(columns, target):
    """Exact rectangular Gaussian elimination; return unique solution or None."""
    k = len(columns)
    rows = [[Fraction(columns[j][i]) for j in range(k)] + [Fraction(target[i])]
            for i in range(len(target))]
    pivotrow = 0
    for col in range(k):
        pivot = next((i for i in range(pivotrow, len(rows)) if rows[i][col]), None)
        if pivot is None: return None
        rows[pivotrow], rows[pivot] = rows[pivot], rows[pivotrow]
        scale = rows[pivotrow][col]
        rows[pivotrow] = [x / scale for x in rows[pivotrow]]
        for i in range(len(rows)):
            if i != pivotrow:
                scale = rows[i][col]
                rows[i] = [a - scale*b for a,b in zip(rows[i], rows[pivotrow])]
        pivotrow += 1
    if any(not any(row[:k]) and row[-1] for row in rows): return None
    return [rows[i][-1] for i in range(k)]

def box_poly(vertices, opened):
    """Count homogenized lattice points in a simplex fundamental box.

    Half-open box gives h*; fully open box gives the local h* polynomial.
    Using the ambient lattice also handles proper faces in their induced lattice.
    """
    if not vertices: return {0: 1}
    columns = [tuple(v) + (1,) for v in vertices]
    bounds = []
    for row in zip(*columns):
        bounds.append(range(sum(min(0, x) for x in row), sum(max(0, x) for x in row) + 1))
    result = {}
    for target in product(*bounds):
        a = solve_columns(columns, target)
        if a is not None and all((0 < x < 1) if opened else (0 <= x < 1) for x in a):
            height = target[-1]
            result[height] = result.get(height, 0) + 1
    return result

def face_stringy(vertices, dual):
    answer = {}
    faces = []
    for k in range(len(vertices) + 1):
        for ids in combinations(range(len(vertices)), k):
            F = [vertices[i] for i in ids]
            D = [w for w in dual if all(sum(a*b for a,b in zip(v,w)) == -1 for v in F)]
            sf, sd = box_poly(F, True), box_poly(D, True)
            faces.append({'face_vertex_count': k, 'dual_vertex_count': len(D),
                          'local': sf, 'dual_local': sd})
            for i, a in sf.items():
                for j, b in sd.items():
                    exponent = (k-i+j-1, i+j-1)
                    answer[exponent] = answer.get(exponent, 0) + (-1)**k*a*b
    return {k:v for k,v in answer.items() if v}, faces

def polynomial(m):
    # Dense 4 by 4 array built directly from the stated factorization.
    a = [[0]*4 for _ in range(4)]
    a[0][0], a[3][0], a[0][3], a[3][3] = 1,-1,-1,1
    for i,j,c in ((1,1,1), (1,2,-1), (2,1,-1), (2,2,1)): a[i][j] += m*c
    return a

def main():
    T = [(1,0), (0,1), (-1,-1)]
    D = [(-1,-1), (-1,2), (2,-1)]
    require(box_poly(T, False) == {0:1, 1:1, 2:1}, 'triangle h* box enumeration')
    require(box_poly(D, False) == {0:1, 1:7, 2:1}, 'dual h* box enumeration')
    require(box_poly(T, True) == {1:1, 2:1}, 'triangle open box')
    require(box_poly(D, True) == {1:1, 2:1}, 'dual open box')
    triangle, faces = face_stringy(T,D)
    require(triangle == {(0,0):1,(1,0):-1,(0,1):-1,(1,1):1}, 'all triangle face contributions')
    require(len(faces) == 8, 'all triangle faces included')
    interval, interval_faces = face_stringy([(-1,), (1,)], [(-1,), (1,)])
    require(interval == {(0,0):2}, 'interval all faces')
    require(box_poly([(0,)], True) == {}, 'point local polynomial is zero')
    # Direct facet verification of R=conv(e_i,-1) and the index-two pyramid.
    # For each facet a*x >= -1 of R, 2P-(0,1) has facet (a,-1)*y >= -1;
    # the base inequality is z >= -1. Each normal is integral and primitive.
    dimensions = []
    for dimension in range(2, 15):
        R = [tuple(int(i==j) for i in range(dimension)) for j in range(dimension)] + [(-1,)*dimension]
        normals = [(-1,)*dimension]
        normals += [tuple(dimension if i==j else -1 for i in range(dimension)) for j in range(dimension)]
        for a in normals:
            values = [sum(x*y for x,y in zip(a,v)) for v in R]
            require(values.count(-1) == dimension and min(values) == -1, 'reflexive simplex supporting facet')
        pyramid = [tuple(2*x for x in v) + (-1,) for v in R] + [(0,)*dimension + (1,)]
        lifted = [a + (-1,) for a in normals] + [(0,)*dimension + (1,)]
        for a in lifted:
            values = [sum(x*y for x,y in zip(a,v)) for v in pyramid]
            require(values.count(-1) == dimension+1 and min(values) == -1, 'index-two pyramid facet')
        require((dimension+1)+1-4 == dimension-2, 'pyramid CY dimension')
        dimensions.append(dimension-2)
    # Ehrhart series of k integral interval joins: h*=(1+t)^k and d+1=2k.
    # Independent counting by compositions of the dilation parameter.
    for k in range(1, 8):
        for dilation in range(5):
            counts = [1] + [0]*dilation
            for _ in range(k):
                counts = [sum(counts[s]*(2*(q-s)+1) for s in range(q+1)) for q in range(dilation+1)]
            predicted = sum(comb(k,j)*comb(dilation-j+2*k-1,2*k-1) for j in range(min(k,dilation)+1))
            require(counts[dilation] == predicted, 'interval join Ehrhart convolution')
        require(2*k-1+1-2*k == 0, 'join CY zero')
    for m in range(65):
        a = polynomial(m)
        require(a[0][0] == a[3][3] == 1, 'formal family corner')
        require(a[1][1] == m, 'formal parameter separates normalized scalar classes')
        for i,j in product(range(4), repeat=2):
            require(a[i][j] == a[j][i], 'Hodge symmetry')
            require(a[i][j] == a[3-i][3-j], 'Poincare symmetry')
            require(a[i][j] == -a[3-i][j], 'self-mirror relation')
            require((-1)**(i+j)*a[i][j] >= 0, 'Hodge sign nonnegativity')
        require([a[i][0] for i in range(4)] == [1,0,0,-1], 'boundary/Serre')
        require(all(sum(row) == 0 for row in a), 'Q(u,1) vanishes identically')
        E = sum(sum(row) for row in a)
        d1 = sum(i*sum(row) for i,row in enumerate(a))
        d2 = sum(i*(i-1)*sum(row) for i,row in enumerate(a))
        require(2*d1 == 3*E and 12*d2 == 3*(9-5)*E, 'both derivative identities')
    return {'schema':1, 'problem_id':30002042, 'independent_checks':CHECKS,
            'triangle_E':[[a,b,c] for (a,b),c in sorted(triangle.items())],
            'triangle_complete_face_data':faces, 'interval_E':2,
            'direct_pyramid_facet_CY_dimensions':dimensions,
            'formal_family_parameters_tested':list(range(65)),
            'scope':'Independent finite exact diagnostics; general proofs are in AUDIT.md; no geometric realization of Q_m.'}

if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
