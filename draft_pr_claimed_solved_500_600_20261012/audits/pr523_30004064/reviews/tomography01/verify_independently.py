#!/usr/bin/env python3
"""Independent bitset enumeration, ray geometry, and exact determinant audit.

No candidate/audit import, subprocess replay, optimization library, network,
or floating point. All explicit checks survive Python optimized execution.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


checks = 0


def require(condition, description):
    global checks
    checks += 1
    if not condition:
        raise ArithmeticError(description)


def inner(a, b):
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    return sum(x*y for x, y in zip(a, b))


def apply(matrix, v):
    return tuple(inner(row, v) for row in matrix)


def backproject(matrix, u):
    return tuple(sum(matrix[i][j]*u[i] for i in range(len(matrix)))
                 for j in range(len(matrix[0])))


def ray_matrix(k, redundant=False, side=F(1)):
    # Cell (r,c) is [c*h,(c+1)*h] x [r*h,(r+1)*h].
    # Rays pass through cell centers, avoiding all grid-boundary ambiguities.
    cells = [(c*side, (c+1)*side, r*side, (r+1)*side)
             for r in range(k) for c in range(k)]
    rays = [('horizontal', (F(r)+F(1,2))*side) for r in range(k)]
    rays += [('vertical', (F(c)+F(1,2))*side)
             for c in range(k if redundant else k-1)]
    matrix = []
    for direction, coordinate in rays:
        row = []
        for left, right, bottom, top in cells:
            if direction == 'horizontal':
                length = right-left if bottom < coordinate < top else F(0)
            else:
                length = top-bottom if left < coordinate < right else F(0)
            row.append(length)
        matrix.append(tuple(row))
    return tuple(matrix)


def bareiss_determinant(matrix):
    # Fraction-free elimination on an integer Gram matrix, with exact divisions.
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    previous, parity = 1, 1
    for col in range(n-1):
        p = next((r for r in range(col, n) if a[r][col]), None)
        if p is None:
            return 0
        if p != col:
            a[p], a[col] = a[col], a[p]
            parity *= -1
        pivot = a[col][col]
        for i in range(col+1, n):
            for j in range(col+1, n):
                numerator = a[i][j]*pivot-a[i][col]*a[col][j]
                quotient, remainder = divmod(numerator, previous)
                require(remainder == 0, "Bareiss division is exact")
                a[i][j] = quotient
            a[i][col] = 0
        previous = pivot
    return parity*a[-1][-1]


def gram(matrix):
    return tuple(tuple(int(inner(r, s)) for s in matrix) for r in matrix)


def masks_for_margins(k):
    # Bit positions encode +1 pixels. This enumeration uses row/column counts,
    # independently of the ray-matrix multiplication code.
    return tuple(sum(1 << (r*k+c) for c in range(k)) for r in range(k)) + tuple(
        sum(1 << (r*k+c) for r in range(k)) for c in range(k-1))


def margins(bitset, k, masks):
    return tuple(2*(bitset & mask).bit_count()-k for mask in masks)


def image(bitset, k):
    return tuple(1 if bitset & (1 << p) else -1 for p in range(k*k))


def common_bitset(fiber, k):
    all_one = (1 << (k*k))-1
    any_one = 0
    for v in fiber:
        all_one &= v
        any_one |= v
    return tuple(1 if all_one & (1 << p) else
                 (-1 if not(any_one & (1 << p)) else 0)
                 for p in range(k*k))


def checkerboards(k):
    pair = []
    for a in (-1, 1):
        values = [1]*(k*k)
        for r, c, v in ((k-2,k-2,a), (k-2,k-1,-a),
                        (k-1,k-2,-a), (k-1,k-1,a)):
            values[r*k+c] = v
        pair.append(tuple(values))
    return pair


def objective(matrix, data, u):
    residual = tuple(x-y for x,y in zip(u,data))
    return inner(residual,residual)/F(2)+sum(abs(x) for x in backproject(matrix,u))


def projected(matrix, data, u, projection):
    residual = apply(projection,tuple(x-y for x,y in zip(u,data)))
    return inner(residual,residual)/F(2)+sum(abs(x) for x in backproject(matrix,u))


def main():
    require((F(1,2)+F(1,2)) == 1, "exact arithmetic sanity")
    matrix = ray_matrix(3)
    displayed = (
        (1,1,1,0,0,0,0,0,0), (0,0,0,1,1,1,0,0,0),
        (0,0,0,0,0,0,1,1,1), (1,0,0,1,0,0,1,0,0),
        (0,1,0,0,1,0,0,1,0))
    require(matrix == displayed, "physical rays reproduce displayed matrix")
    determinant3 = bareiss_determinant(gram(matrix))
    require(determinant3 == 81, "3x3 Gram determinant establishes full row rank")

    all_fibers, summaries = {}, []
    enumerated = 0
    for k in (2,3,4):
        masks = masks_for_margins(k)
        fibers = {}
        for binary in range(1 << (k*k)):
            data = margins(binary,k,masks)
            fibers.setdefault(data,[]).append(binary)
            enumerated += 1
        no_common = sum(all(v==0 for v in common_bitset(f,k)) for f in fibers.values())
        summaries.append({'k':k,'images':1 << (k*k),'fibers':len(fibers),
                          'singleton_fibers':sum(len(f)==1 for f in fibers.values()),
                          'fibers_with_no_common_pixels':no_common,
                          'fibers_where_exact_rule_fails_common_recovery':len(fibers)-no_common})
        all_fibers[k] = fibers
        for fiber in fibers.values():
            c = common_bitset(fiber,k)
            for coordinate,value in enumerate(c):
                require((value != 0) ==
                        all(image(b,k)[coordinate] == image(fiber[0],k)[coordinate]
                            for b in fiber), "common coordinate bitset agrees with definition")

    data = (3,1,1,3,1)
    fiber = all_fibers[3][data]
    actual_solutions = sorted(image(v,3) for v in fiber)
    require(actual_solutions == sorted(checkerboards(3)), "exactly the two claimed solutions")
    c = common_bitset(fiber,3)
    require(c == (1,1,1,1,0,0,1,0,0), "five fixed positive pixels")
    require(len(all_fibers[3][(3,3,3,3,3)]) == 1, "all-positive datum is uniquely binary")
    complemented = tuple(-t for t in data)
    require(common_bitset(all_fibers[3][complemented],3) == tuple(-t for t in c),
            "five fixed negative pixels")
    mixed_data = (3,-1,-1,-1,1)
    mixed_c = common_bitset(all_fibers[3][mixed_data],3)
    require(len(all_fibers[3][mixed_data]) == 2, "mixed-sign fiber has two solutions")
    require(mixed_c == (1,1,1,-1,0,0,-1,0,0), "mixed-sign common pixels")

    physical = tuple((v+1)//2 for v in actual_solutions[0])
    physical_data = apply(matrix,physical)
    require(physical_data == (3,2,2,3,2), "0/1 recoding yields nonnegative line integrals")
    require(physical_data == tuple((y+z)/F(2) for y,z in zip(data,apply(matrix,(1,)*9))),
            "recoding datum has exact baseline shift")

    family_results = []
    for k in tuple(range(2,17))+(31,):
        a = ray_matrix(k)
        det = bareiss_determinant(gram(a))
        require(det == k**(2*k-2), "all-size Gram determinant formula")
        family_data = (k,)*(k-2)+(k-2,k-2)+(k,)*(k-2)+(k-2,)
        for s in checkerboards(k):
            require(apply(a,s) == family_data, "family reduced data formula")
            full_data = apply(ray_matrix(k,True),s)
            require(full_data == (k,)*(k-2)+(k-2,k-2)+(k,)*(k-2)+(k-2,k-2),
                    "family full data formula")
        require(sum(t==u for t,u in zip(*checkerboards(k))) == k*k-4,
                "family common-pixel count")
        if k in all_fibers:
            require(len(all_fibers[k][family_data]) == 2, "small family is exhaustive")
        family_results.append({'k':k,'rows':2*k-1,'pixels':k*k,'rank':2*k-1,
                               'Gram_determinant':str(det),
                               'common_pixels':k*k-4,
                               'measurement_ratio':str(F(2*k-1,k*k))})

    box_identity_count = 0
    matrices = (((1,),), ((0,),), ((-3,2),), ((1,2),(2,4)),
                ((1,0),(0,1)), ((1,-1,2),(0,2,-1)))
    grid = (F(-1),F(-2,3),F(0),F(2,3),F(1))
    multiplier_grid = (F(-2),F(-1,3),F(0),F(1,3),F(2))
    for a in matrices:
        for s in product(grid,repeat=len(a[0])):
            y = apply(a,s)
            zero = (F(0),)*len(a)
            for u in product(multiplier_grid,repeat=len(a)):
                bp = backproject(a,u)
                slack = sum(abs(t)-s_j*t for s_j,t in zip(s,bp))
                gap = objective(a,y,u)-objective(a,y,zero)
                require(gap == inner(u,u)/F(2)+slack, "unprojected identity")
                require(gap >= inner(u,u)/F(2), "box-feasible lower bound")
                require((gap == 0) == (u == zero), "unique zero on finite grid")
                box_identity_count += 1

    b = ray_matrix(3,True)
    dependency = (1,1,1,-1,-1,-1)
    require(backproject(b,dependency) == (0,)*9, "full data redundancy")
    require(bareiss_determinant(gram(b)) == 0, "full Gram matrix is singular")
    p = tuple(tuple(F(i==j)-F(dependency[i]*dependency[j],6)
                    for j in range(6)) for i in range(6))
    require(tuple(zip(*p)) == p, "projector is symmetric")
    for basis in range(6):
        e = tuple(F(j==basis) for j in range(6))
        require(apply(p,apply(p,e)) == apply(p,e), "projector is idempotent")
    for column in zip(*b):
        require(apply(p,column) == column, "projector preserves measurement range")
    require(apply(p,dependency) == (0,)*6, "projector removes exact kernel")
    projected_count = 0
    s = checkerboards(3)[0]
    y = apply(b,s)
    require(y == (3,1,1,3,1,1), "full consistent datum")
    require(apply(p,y) == y, "noiseless datum lies in measurement range")
    for u in product((F(-1),F(0),F(1)),repeat=6):
        bp = backproject(b,u)
        gap = projected(b,y,u,p)-projected(b,y,(0,)*6,p)
        pu = apply(p,u)
        expected = inner(pu,pu)/F(2)+sum(abs(v)-t*v for t,v in zip(s,bp))
        require(gap == expected, "projected exact identity")
        require((gap == 0) == (pu == (0,)*6), "projected minimizers are precisely kernel")
        if gap == 0:
            require(bp == (0,)*9, "every projected minimizer has zero backprojection")
        projected_count += 1
    for scale in (F(-3),F(-1,2),F(0),F(2,3),F(7)):
        u = tuple(scale*t for t in dependency)
        require(projected(b,y,u,p) == projected(b,y,(0,)*6,p), "nonzero kernel minimizers")

    # Controls preventing extension of the theorem beyond its hypotheses.
    scalar = ((1,),)
    require(objective(scalar,(2,),(1,)) < objective(scalar,(2,),(0,)),
            "outside-box scalar datum refutes unconditional zero claim")
    require(objective(scalar,(F(1,2),),(0,)) < objective(scalar,(F(1,2),),(F(1,2),)),
            "box-feasible but binary-infeasible scalar datum is zero-minimized")
    epsilons = (F(1,2),F(1,10),F(1,1000))
    for epsilon in epsilons:
        f0 = objective(scalar,(1,),(0,))
        require(objective(scalar,(1,),(epsilon,))-f0 == epsilon**2/F(2),
                "positive approach to optimizer")
        require(objective(scalar,(1,),(-epsilon,))-f0 == 2*epsilon+epsilon**2/F(2),
                "negative approach to same optimizer")
    require(common_bitset(all_fibers[2][(0,0,0)],2) == (0,)*4,
            "zero-common-coordinate control does satisfy exact common rule")
    mixed_unique = (1,1,-1,-1)
    d2 = apply(ray_matrix(2),mixed_unique)
    require(len(all_fibers[2][d2]) == 1, "mixed-sign unique image control")
    require(mixed_unique != (1,)*4 and mixed_unique != (-1,)*4,
            "fixed alternative sign(0) cannot recover mixed-sign unique image")
    permutation_data = (-1,)*5
    perm_fiber = all_fibers[3][permutation_data]
    require(len(perm_fiber) == 6, "permutation fiber has six binary solutions")
    require(common_bitset(perm_fiber,3) == (0,)*9, "permutation fiber has no common pixels")
    require(apply(matrix,(0,)*9) != permutation_data,
            "common vector need not be box-feasible")
    z = (F(-1,3),)*9
    require(apply(matrix,z) == permutation_data, "valid auxiliary box variable")
    require(apply(matrix,(-1,)*9) != permutation_data,
            "sign of a valid auxiliary variable need not solve tomography")
    y_orthogonal_noise = tuple(v+w for v,w in zip(y,dependency))
    require(apply(p,y_orthogonal_noise) == y and y_orthogonal_noise != y,
            "projected formulation ignores noise in orthogonal data direction")
    for side in (F(1,2),F(2)):
        scaled_a = ray_matrix(3,side=side)
        require(apply(scaled_a,s) == tuple(side*v for v in data),
                "length scaling retains genuine data")
        u = (F(1,3),)*5
        require(objective(scaled_a,apply(scaled_a,s),u) >
                objective(scaled_a,apply(scaled_a,s),(0,)*5),
                "geometric length scaling does not evade zero obstruction")

    return {'status':'all independent exact checks passed',
            'arithmetic':'integers and fractions.Fraction; no floating point',
            'candidate_modules_imported_or_replayed':False,
            'binary_images_enumerated':enumerated,
            'fiber_summaries':summaries,
            '3x3_matrix':[list(map(int,row)) for row in matrix],
            '3x3_Gram_determinant':determinant3,
            '3x3_solutions':[list(s) for s in actual_solutions],
            '3x3_common_vector':list(c),
            '3x3_nonnegative_0_1_datum':list(map(int,physical_data)),
            'all_size_family_finite_checks':family_results,
            'box_objective_identities':box_identity_count,
            'projected_objective_identities':projected_count,
            'explicit_require_calls':checks,
            'universal_proof_scope':'Finite checks supplement the separately written algebraic and all-k proofs.'}


if __name__ == '__main__':
    result = main()
    print(json.dumps(result,indent=2,sort_keys=True))
