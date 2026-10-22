#!/usr/bin/env python3
"""Exact rational checks for 30005717. Python 3 + SymPy; no network or data files.
This tests finite examples and a derivative criterion, not the full conjecture.
"""
import itertools as it
import json
from math import comb
from pathlib import Path
import sympy as s


def exponents(n, k):
    if n == 0:
        return [()] if k == 0 else []
    if n == 1:
        return [(k,)]
    return [(i,) + a for i in range(k + 1) for a in exponents(n - 1, k - i)]


def facets_exact(points):
    n, d = len(points), len(points[0])
    r = s.Matrix([[1] + list(p) for p in points])
    assert r.rank() == d + 1
    out = []
    for f in it.combinations(range(n), d):
        null = r[list(f), :].nullspace()
        if len(null) != 1:
            continue
        sides = list(r * null[0])
        if all(x >= 0 for x in sides) or all(x <= 0 for x in sides):
            zero = frozenset(i for i, x in enumerate(sides) if x == 0)
            assert len(zero) == d, 'Non-simplicial facet in test input'
            out.append(zero)
    return sorted(set(out), key=lambda a: tuple(sorted(a)))


def face_data(points):
    n, d = len(points), len(points[0])
    facets = facets_exact(points)
    faces = {frozenset()}
    for f in facets:
        for j in range(1, d + 1):
            faces.update(map(frozenset, it.combinations(f, j)))
    missing = []
    for j in range(2, min(n, d + 1) + 1):
        for a in it.combinations(range(n), j):
            a = frozenset(a)
            if a not in faces and all(a - {v} in faces for v in a):
                missing.append(a)
    fvec = [sum(len(f) == j for f in faces) for j in range(d + 1)]
    hvec = [sum((-1)**(j-i)*comb(d-i,d-j)*fvec[i] for i in range(j+1)) for j in range(d+1)]
    assert hvec == list(reversed(hvec))
    return facets, faces, missing, hvec


def stress_basis(points, faces, degree):
    """Return homogeneous stress polynomials in exact Gale coordinates.
    All polynomials killed by the augmented coordinate rows are Sym^degree(ker R).
    The remaining equations set every non-face-supported coefficient to zero.
    """
    n, d = len(points), len(points[0])
    r = s.Matrix([[1]*n] + [[p[j] for p in points] for j in range(d)])
    gale = r.nullspace()
    m = len(gale)
    z = s.symbols('z:'+str(m))
    x = s.symbols('x:'+str(n))
    ze = exponents(m, degree)
    if not ze:
        return z, [], []
    ell = [sum(gale[j][i]*x[i] for i in range(n)) for j in range(m)]
    columns = [s.Poly(s.prod(ell[j]**a[j] for j in range(m)), *x).as_dict() for a in ze]
    bad = [a for a in exponents(n, degree) if frozenset(j for j,e in enumerate(a) if e) not in faces]
    matrix = s.Matrix([[col.get(a,0) for col in columns] for a in bad]) if bad else s.zeros(0,len(ze))
    coeffs = matrix.nullspace()
    basis = [s.Poly(sum(c[i]*s.prod(z[j]**a[j] for j in range(m)) for i,a in enumerate(ze)),*z) for c in coeffs]
    # Independently verify support and all augmented-row differential equations.
    for c in coeffs:
        pol = s.Poly(sum(c[i]*s.prod(ell[j]**a[j] for j in range(m)) for i,a in enumerate(ze)),*x)
        assert all(frozenset(j for j,e in enumerate(a) if e) in faces for a,v in pol.terms() if v)
        for row in r.tolist():
            assert sum(row[i]*pol.diff(x[i]).as_expr() for i in range(n)).expand() == 0
    return z, basis, [list(v) for v in gale]


def derivative_rank(basis, z, order):
    if not basis:
        return 0
    degree = basis[0].total_degree() - order
    target = exponents(len(z), degree)
    rows = []
    for p in basis:
        for a in exponents(len(z), order):
            q = p
            for j,e in enumerate(a):
                for unused in range(e):
                    q = q.diff(z[j])
            q = q.as_dict()
            rows.append([q.get(b,0) for b in target])
    return s.Matrix(rows).rank()


def simplex(d):
    return [[int(i==j) for j in range(d)] for i in range(d)] + [[-1]*d]


def cross(d):
    return [[sign*int(i==j) for j in range(d)] for i in range(d) for sign in [-1,1]]


def direct_sum(*polytopes):
    dims = [len(p[0]) for p in polytopes]
    total = sum(dims)
    ans, offset = [], 0
    for p,d in zip(polytopes,dims):
        ans += [[0]*offset + list(v) + [0]*(total-offset-d) for v in p]
        offset += d
    return ans


def run_case(name, points, degree=None, expected_valid=True):
    n,d=len(points),len(points[0])
    degree = degree or d//2
    facets, faces, missing, h = face_data(points)
    valid = all(len(a)-1 < d-degree+1 for a in missing)
    assert valid == expected_valid
    z, basis, gale = stress_basis(points,faces,degree)
    _, lower, _ = stress_basis(points,faces,degree-1)
    assert len(basis) == h[degree]-h[degree-1]
    assert len(lower) == h[degree-1]-h[degree-2] if degree>1 else True
    linear_rank = derivative_rank(basis,z,degree-1)
    immediate_rank = derivative_rank(basis,z,1)
    result = dict(name=name,dimension=d,vertices=n,stress_degree=degree,
                  facets=len(facets),missing_dimensions=sorted(len(a)-1 for a in missing),
                  satisfies_missing_face_bound=valid,h_vector=h,
                  affine_dependency_dimension=len(z),stress_dimension=len(basis),
                  previous_stress_dimension=len(lower),first_derivative_rank=immediate_rank,
                  socle_previous_degree=len(lower)-immediate_rank,
                  degree_one_derivative_rank=linear_rank,
                  reconstructs_affine_type_by_derivatives=linear_rank==len(z))
    if valid:
        assert linear_rank == len(z)
    if name == 'three_triangles_6d':
        assert (len(basis),len(lower),immediate_rank,linear_rank)==(1,3,2,2)
        result['gale_basis']=[[str(a) for a in v] for v in gale]
        result['top_stress_gale_polynomials']=[str(p.as_expr()) for p in basis]
        # Explicit natural-coordinate certificate for the credited 2026 family.
        x=s.symbols('x:9')
        a,b,c=(sum(x[3*j:3*j+3]) for j in range(3))
        cubic=s.Poly((a-c)*(b-c)*(a-b),*x)
        inactive=[]
        for f in faces:
            if len(f)==3:
                mon=s.prod(x[j] for j in f)
                if cubic.coeff_monomial(mon)==0:
                    inactive.append(f)
        assert len(inactive)==27
        assert all(len(f & frozenset(range(3*j,3*j+3)))==1 for f in inactive for j in range(3))
        result['triangular_faces']=sum(len(f)==3 for f in faces)
        result['faces_absent_from_all_top_stresses']=27
    if name == 'stacked_simplex_negative_control':
        assert (len(basis),linear_rank,len(z)) == (0,0,1)
    return result


def algebra_checks():
    u,v=s.symbols('u v')
    ideal=s.groebner([u**3,v**3,(u+v)**3],u,v)
    socle=u*u+u*v+v*v
    assert ideal.reduce(socle)[1] != 0
    assert ideal.reduce(u*socle)[1] == ideal.reduce(v*socle)[1] == 0
    cubic=s.Poly(u*u*v-u*v*v,u,v)
    assert derivative_rank([cubic],(u,v),1)==2
    assert derivative_rank([cubic],(u,v),2)==2
    assert cubic.diff(u).diff(u).diff(u).is_zero
    assert cubic.diff(v).diff(v).diff(v).is_zero
    assert sum(comb(3,i)*s.diff(cubic.as_expr(),u,i,v,3-i) for i in range(4)) == 0
    # A deliberately non-polytopal inverse-system control: top Y^2 loses X.
    assert derivative_rank([s.Poly(v*v,u,v)],(u,v),1)==1
    return dict(three_triangle_quotient_groebner=[str(p.as_expr()) for p in ideal.polys],
                nonzero_degree_two_socle=str(socle),top_inverse_polynomial=str(cubic.as_expr()),
                abstract_bad_example='Q[u,v]/(u^2,u*v,v^3): top inverse polynomial v^2 has derivative rank 1 < 2',
                suspension_cross4={'base_h':[1,4,6,4,1],'bipyramid_h':[1,5,10,10,5,1],
                                   'base_S2_dimension':2,'bipyramid_S2_dimension':5,'extra_dimension':3})


def main():
    tri=simplex(2)
    square=cross(2)
    pent=[[-1,-1],[1,-1],[2,0],[1,1],[-1,1]]
    pert=[[s.Rational(100)*a+s.Rational(((i+2)*(j+3))%7-3,10) for j,a in enumerate(p)] for i,p in enumerate(cross(4))]
    cases=[('cross_4d',cross(4),None,True),('perturbed_cross_4d',pert,None,True),
           ('cyclic_4d_6',[[t**j for j in range(1,5)] for t in range(1,7)],None,True),
           ('cyclic_4d_8',[[t**j for j in range(1,5)] for t in range(1,9)],None,True),
           ('triangle_square_4d',direct_sum(tri,square),None,True),
           ('triangle_pentagon_4d',direct_sum(tri,pent),None,True),
           ('three_triangles_6d',direct_sum(tri,tri,tri),None,True),
           ('cyclic_6d_8',[[t**j for j in range(1,7)] for t in range(1,9)],None,True),
           ('cyclic_6d_9',[[t**j for j in range(1,7)] for t in range(1,10)],None,True),
           ('cross_6d',cross(6),None,True),
           ('bipyramid_cross4',cross(5),2,True),
           ('stacked_simplex_negative_control',[[0]*4]+[[int(i==j) for j in range(4)] for i in range(4)]+[[s.Rational(3,10)]*4],None,False)]
    results=[]
    for name,p,k,valid in cases:
        results.append(run_case(name,p,k,valid))
        print(name, 'ok', flush=True)
    out={'arithmetic':'exact SymPy rationals; exhaustive supporting-facet enumeration',
         'sympy_version':s.__version__,'cases':results,'algebra':algebra_checks(),
         'conclusion':'All ten even-dimensional target examples and the odd-dimensional control recover degree one. The three-triangle example fails full lower-degree generation. The unrestricted negative control fails recovery. No general proof or counterexample is established.'}
    dest=Path(__file__).with_name('exact_results.json')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS:',dest.name)

if __name__=='__main__':
    main()
