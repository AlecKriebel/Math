"""Independent exact PR117 LP audit; explicit guards survive python -O.

Construction precedes reading the original checker. No third-party dependencies.
Finite vertex enumeration is a cross-check; universal face/fiber proof is in REPORT.md.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import sys

CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


VARIABLES = ("x1", "x2", "x3", "y1", "y2", "y3")
TERMS = ((('x1', 'y2'), ('x2', 'y1')),
         (('x2', 'y3'), ('x3', 'y2')),
         (('x3', 'y1'), ('x1', 'y3')))


def exponent(term, variables=VARIABLES):
    return tuple(Q(term.count(v)) for v in variables)


def augmented(terms=TERMS, variables=VARIABLES):
    r = len(terms)
    columns = [exponent(pair[0], variables) for pair in terms]
    columns += [exponent(pair[1], variables) for pair in terms]
    top = tuple(tuple(columns[j][i] for j in range(2*r))
                for i in range(len(variables)))
    bottom = tuple(tuple(Q(j % r == i) for j in range(2*r))
                   for i in range(r))
    return top + bottom


def rref(rows, width=None):
    mat = [list(map(Q, row)) for row in rows]
    n = len(mat[0]) if width is None else width
    pivots = []
    active = 0
    for col in range(n):
        pivot = next((i for i in range(active, len(mat)) if mat[i][col]), None)
        if pivot is None:
            continue
        mat[active], mat[pivot] = mat[pivot], mat[active]
        divisor = mat[active][col]
        mat[active] = [x / divisor for x in mat[active]]
        for i in range(len(mat)):
            if i != active and mat[i][col]:
                factor = mat[i][col]
                mat[i] = [x - factor*y for x, y in zip(mat[i], mat[active])]
        pivots.append(col)
        active += 1
        if active == len(mat):
            break
    return mat, tuple(pivots)


def kernel(rows):
    mat, pivots = rref(rows)
    n = len(rows[0])
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        vector = [Q(0)] * n
        vector[f] = Q(1)
        for i, p in enumerate(pivots):
            vector[p] = -mat[i][f]
        basis.append(tuple(vector))
    return tuple(basis)


def matvec(rows, point):
    return tuple(sum(a*x for a, x in zip(row, point)) for row in rows)


def vertex_enumeration(rows):
    n = len(rows[0])
    inequalities = list(rows)
    rhs = [Q(1)] * len(rows)
    for j in range(n):
        inequalities.append(tuple(Q(-1 if j == k else 0) for k in range(n)))
        rhs.append(Q(0))
    vertices = set()
    bases = 0
    nonsingular = 0
    for active in combinations(range(len(inequalities)), n):
        bases += 1
        matrix = [list(inequalities[i]) + [rhs[i]] for i in active]
        reduced, pivots = rref(matrix, width=n)
        if len(pivots) != n:
            continue
        nonsingular += 1
        point = tuple(reduced[j][-1] for j in range(n))
        if all(value <= bound for value, bound in zip(matvec(inequalities, point), rhs)):
            vertices.add(point)
    return tuple(sorted(vertices)), bases, nonsingular


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    return value


def point(t):
    return (Q(t),)*3 + (Q(1)-Q(t),)*3


def validate_target_matrix(matrix):
    if len(matrix) != 9 or any(len(row) != 6 for row in matrix):
        raise ValueError("Target must retain all six exponent and three augmentation rows")
    if tuple(tuple(map(Q, row)) for row in matrix) != augmented():
        raise ValueError("Matrix differs from the exact exponent/lower-identity prescription")


def polynomial_multiply(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            monomial = tuple(x+y for x, y in zip(a, b))
            result[monomial] = result.get(monomial, Q(0)) + ca*cb
    return {a: c for a, c in result.items() if c}


def polynomial_sum(*polynomials):
    result = {}
    for poly in polynomials:
        for a, c in poly.items():
            result[a] = result.get(a, Q(0)) + c
    return {a: c for a, c in result.items() if c}


def main():
    A = augmented()
    require(A == ((1,0,0,0,0,1), (0,1,0,1,0,0), (0,0,1,0,1,0),
                  (0,0,1,1,0,0), (1,0,0,0,1,0), (0,1,0,0,0,1),
                  (1,0,0,1,0,0), (0,1,0,0,1,0), (0,0,1,0,0,1)),
            "Nine rows independently derived from terms disagree")
    validate_target_matrix(A)
    cross_rows = {tuple(Q(j == i or j == 3+k) for j in range(6))
                  for i in range(3) for k in range(3)}
    require(set(A) == cross_rows and len(set(A)) == 9,
            "All nine rows must be exactly all cross-part pair bounds")
    reduced, pivots = rref(A)
    require(len(pivots) == 5, "Augmented rank must be five")
    K = kernel(A)
    require(K == ((-1,-1,-1,1,1,1),), "Exact nullspace is not the proposed cyclic line")
    require(matvec(A, (1,1,1,-1,-1,-1)) == (Q(0),)*9, "Kernel direction failed")
    for t in (Q(0), Q(1), Q(1,2), Q(1,997), Q(996,997)):
        z = point(t)
        require(all(x >= 0 for x in z), "Primal certificate nonnegativity")
        require(matvec(A, z) == (Q(1),)*9, "Primal image exact equality")
        require(sum(z) == 3, "Primal value three")
        partner = point(0 if t else 1)
        require(partner != z and matvec(A, partner) == matvec(A, z), "Fiber witness")

    dual = (Q(0),)*6 + (Q(1),)*3
    transpose_dual = tuple(sum(dual[i]*A[i][j] for i in range(9)) for j in range(6))
    require(all(d >= 0 for d in dual), "Dual nonnegative")
    require(transpose_dual == (Q(1),)*6, "Dual equals objective on every column")
    require(sum(dual) == 3, "Dual objective three")

    vertices, bases, nonsingular = vertex_enumeration(A)
    optimal_vertices = tuple(v for v in vertices if sum(v) == max(map(sum, vertices)))
    require(bases == 5005, "Incorrect complete active-basis count")
    require(optimal_vertices == tuple(sorted((point(0), point(1)))), "Additional optimal vertex")
    require(max(map(sum, vertices)) == 3, "Vertex optimum mismatch")
    require(all(matvec(A,v) == (Q(1),)*9 for v in optimal_vertices), "Endpoint images")

    # Column relabeling for all generator orders/orientations is exact, not numerical.
    transformations = 0
    for order in permutations(range(3)):
        for flips in product((False, True), repeat=3):
            changed = tuple(TERMS[i][::-1] if flips[j] else TERMS[i]
                            for j, i in enumerate(order))
            B = augmented(changed)
            colmap = tuple(order[j] + (3 if flips[j] else 0) for j in range(3))
            colmap += tuple(order[j] + (0 if flips[j] else 3) for j in range(3))
            require(all(B[i][j] == A[i][colmap[j]] for i in range(6) for j in range(6)),
                    "Term flip/order top-row mapping")
            require(all(B[6+i][j] == A[6+order[i]][colmap[j]]
                        for i in range(3) for j in range(6)), "Augmentation relabeling")
            require(len(rref(B)[1]) == 5 and len(kernel(B)) == 1, "Relabeled kernel")
            for endpoint in (point(0), point(1)):
                mapped = tuple(endpoint[k] for k in colmap)
                require(matvec(B, mapped) == (Q(1),)*9, "Relabeled endpoint")
            transformations += 1
    require(transformations == 48, "Missing order/orientation cases")
    row_permutations = 0
    for variables in permutations(VARIABLES):
        B = augmented(variables=variables)
        require(all(B[i] == A[VARIABLES.index(variables[i])] for i in range(6)),
                "Variable renaming must only permute exponent rows")
        require(B[6:] == A[6:], "Variable renaming changed augmentation")
        row_permutations += 1
    require(row_permutations == 720, "Missing variable-order cases")

    # Structural mutants detect silent alteration of the exact source LP. Some preserve
    # this particular optimal face; rejection concerns correct target authentication.
    mutant_matrices = {
        "augmentation_omitted": A[:6],
        "one_augmentation_row_omitted": A[:8],
        "lower_right_identity_omitted": A[:6] + tuple(row[:3]+(Q(0),)*3 for row in A[6:]),
        "one_exponent_mutated": ((2,0,0,0,0,1),) + A[1:],
        "columns_ordered_as_pairs_without_relabeling": tuple(tuple(row[j] for j in (0,3,1,4,2,5)) for row in A),
    }
    rejected = []
    for label, matrix in mutant_matrices.items():
        try:
            validate_target_matrix(matrix)
        except ValueError:
            rejected.append(label)
        else:
            raise RuntimeError("Undetected exact-target mutation: " + label)
    require(len(rejected) == 5, "Mutation coverage")

    # Dropping one genuine generator gives a different minimal system with injective
    # A and multiple optimal points: nonuniqueness alone is no counterexample.
    A2 = augmented(TERMS[:2])
    require(len(rref(A2)[1]) == 4 and kernel(A2) == (), "Two-generator map must be injective")
    v2, b2, ns2 = vertex_enumeration(A2)
    opt2 = tuple(v for v in v2 if sum(v) == max(map(sum,v2)))
    require(max(map(sum,v2)) == 2 and len(opt2) > 1, "Quantifier control needs multiple optimizers")
    require(len({matvec(A2,v) for v in opt2}) == len(opt2), "Injective control images distinct")

    # Strict inequalities destroy attainment, though scaled feasible points approach3.
    require(not all(a < 1 for a in matvec(A, point(0))), "Nonstrict boundary is essential")
    for epsilon in (Q(1,2), Q(1,10), Q(1,1000)):
        z = tuple((1-epsilon)*x for x in point(Q(1,2)))
        require(all(a < 1 for a in matvec(A,z)) and sum(z) == 3*(1-epsilon),
                "Strict-LP limiting control")

    # Minimality mutation: a duplicate fourth binomial has dependent degree-two class.
    monomials = tuple(exponent(term) for pair in TERMS for term in pair)
    require(len(set(monomials)) == 6, "Original six degree-two monomials must be distinct")
    coefficient_rows = []
    for a,b in TERMS + (TERMS[0],):
        coefficient_rows.append(tuple(Q((m == exponent(a)) - (m == exponent(b))) for m in monomials))
    require(len(rref(coefficient_rows)[1]) == 3 < 4, "Redundant fourth generator mutation")

    # Compatible variable rescalings preserve exponents/hypotheses. Arbitrary binomial
    # coefficients need not: gamma-product !=1 explicitly puts a monomial in the ideal.
    scales = dict(zip(VARIABLES, (Q(2),Q(3),Q(5),Q(7),Q(11),Q(13))))
    scalar_of = lambda term: scales[term[0]]*scales[term[1]]
    gammas = tuple(scalar_of(b)/scalar_of(a) for a,b in TERMS)
    require(gammas[0]*gammas[1]*gammas[2] == 1, "Variable scaling compatibility")
    evaluation = {v: 1/scales[v] for v in VARIABLES}
    for i,(a,b) in enumerate(TERMS):
        require(evaluation[a[0]]*evaluation[a[1]] == gammas[i]*evaluation[b[0]]*evaluation[b[1]],
                "Nonzero point after invertible variable scaling")
    u = [{exponent(a):Q(1)} for a,b in TERMS]
    v = [{exponent(b):Q(1)} for a,b in TERMS]
    bad = (Q(2),Q(1),Q(1))
    f = [polynomial_sum(u[i], {m:-bad[i]*c for m,c in v[i].items()}) for i in range(3)]
    p1 = polynomial_multiply(polynomial_multiply(f[0],u[1]),u[2])
    p2 = {m:bad[0]*c for m,c in polynomial_multiply(polynomial_multiply(v[0],f[1]),u[2]).items()}
    p3 = {m:bad[0]*bad[1]*c for m,c in polynomial_multiply(polynomial_multiply(v[0],v[1]),f[2]).items()}
    certificate = polynomial_sum(p1,p2,p3)
    require(certificate == {(Q(1),)*6:Q(-1)}, "Incompatible-coefficient monomial certificate")

    result = {
        "status":"PASS", "explicit_guards":CHECKS,
        "optimizations_disabled":bool(sys.flags.optimize),
        "matrix":A, "rank":len(pivots), "kernel_basis":K,
        "dual_certificate":dual, "optimum":Q(3),
        "all_vertices":vertices, "vertex_count":len(vertices),
        "active_bases_checked":bases, "nonsingular_bases":nonsingular,
        "optimal_vertices":optimal_vertices,
        "universal_face":"z(t)=(t,t,t,1-t,1-t,1-t), t rational in [0,1]; see unrestricted proof",
        "universal_image":"ones(9)",
        "independent_polytope_identity":"conv(([0,1]^3 x {0}) union ({0} x [0,1]^3))",
        "generator_order_orientation_cases":transformations,
        "variable_order_cases":row_permutations,
        "exact_target_mutants_rejected":rejected,
        "quantifier_control":{"generator_count":2,"rank":4,"optimum":Q(2),"optimal_vertex_count":len(opt2),
                              "condition_holds_despite_nonunique_optimizer":True},
        "coefficient_control":{"compatible_rescaling_gammas":gammas,
                               "incompatible_gammas":bad,"ideal_contains_negative_full_product":True},
        "mathematics_only":True, "novelty_clearance":False,
    }
    print(json.dumps(encode(result), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
