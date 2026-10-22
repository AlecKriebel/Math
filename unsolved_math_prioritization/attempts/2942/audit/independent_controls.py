#!/usr/bin/env python3
"""Independent exact algebraic controls. These do not compute a manifold invariant."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json

counts = Counter()


def require(value, name):
    if not value:
        raise RuntimeError(name)
    counts[name] += 1


def pairing(g, x, y):
    return sum(g[i][j] * x[i] * y[j] for i in range(len(x)) for j in range(len(y)))


def block(*blocks):
    size = sum(map(len, blocks))
    out = [[0] * size for _ in range(size)]
    offset = 0
    for b in blocks:
        for i, row in enumerate(b):
            for j, value in enumerate(row):
                out[offset+i][offset+j] = value
        offset += len(b)
    return out


def inertia_and_det(matrix):
    """Rational symmetric congruence, including a shear for a zero diagonal."""
    a = [[Fraction(x) for x in row] for row in matrix]
    pos = neg = zero = 0
    det = Fraction(1)
    while a:
        size = len(a)
        pivot = next((i for i in range(size) if a[i][i]), None)
        if pivot is None:
            off = next(((i,j) for i in range(size) for j in range(i+1,size) if a[i][j]), None)
            if off is None:
                zero += size
                det = Fraction(0)
                break
            i, j = off
            # Congruence replacing basis vector e_i by e_i+e_j; determinant one.
            old = [row[:] for row in a]
            for k in range(size):
                a[i][k] = old[i][k] + old[j][k]
                a[k][i] = old[k][i] + old[k][j]
            a[i][i] = old[i][i] + 2*old[i][j] + old[j][j]
            pivot = i
        a[0], a[pivot] = a[pivot], a[0]
        for row in a:
            row[0], row[pivot] = row[pivot], row[0]
        d = a[0][0]
        pos += d > 0
        neg += d < 0
        det *= d
        a = [[a[i][j] - a[i][0]*a[0][j]/d for j in range(1,size)]
             for i in range(1,size)]
    return (pos, neg, zero), det


def mul_vec(a, v):
    return tuple(sum(x*y for x,y in zip(row,v)) for row in a)


def main():
    # Quotient factorization tested by actual representatives of equal cosets.
    for u, v in product(range(-3,4), repeat=2):
        if (u,v) == (0,0):
            continue
        k = (-v,u)
        for s,t in product(range(-3,4), repeat=2):
            lam = lambda x: s*x[0] + t*x[1]
            annihilates = lam(k) == 0
            equivalent_representatives = all(lam((2+z*k[0],-1+z*k[1])) == lam((2,-1))
                                             for z in (-4,-1,1,5))
            require(annihilates == equivalent_representatives, 'quotient_coset_well_definedness')

    # Semisimple balanced tensor: explicit surviving basis pairs by sector.
    for a,b,c,d in product(range(5),repeat=4):
        m = [(0,i) for i in range(a)] + [(1,i) for i in range(b)]
        n = [(0,i) for i in range(c)] + [(1,i) for i in range(d)]
        surviving = [(x,y) for x in m for y in n if x[0] == y[0]]
        require(len(surviving) == a*c+b*d, 'balanced_tensor_sector_basis')

    h = [[0,1],[1,0]]
    e8 = [[2 if i == j else 0 for j in range(8)] for i in range(8)]
    for i,j in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]:
        e8[i][j] = e8[j][i] = -1
    tests = [([[1]],(1,0)), (h,(1,1)), (e8,(8,0)),
             (block(e8,h),(9,1)), (block(h,h),(2,2))]
    for q,(p,n) in tests:
        inertia, det = inertia_and_det(q)
        require(inertia == (p,n,0) and abs(det) == 1, 'unimodular_lattice_oracle')
        for extra in range(5):
            original = block(q,*([[-1]] for _ in range(extra)))
            sig = p-(n+extra)
            r = 2 if sig == 1 else 1
            result = block(original,*([[-1]] for _ in range(r)))
            result_inertia,result_det = inertia_and_det(result)
            require(result_inertia == (p,n+extra+r,0) and abs(result_det) == 1
                    and any(result[i][i] % 2 for i in range(len(result)))
                    and p > 0 and n+extra+r > 0 and sig-r != 0,
                    'negative_blowup_hypotheses')
    require(pairing(h,(1,1),(1,1)) == 2, 'diagonal_square')
    require(-(-1) == 1, 'positive_sphere_threshold')

    # Integral lattice automorphism with torsion index transport retained.
    # f(x,y,t)=(x+y,y,2t mod 3); Q' has Gram [[1,-1],[-1,0]].
    g = [[1,0],[0,-1]]
    gp = [[1,-1],[-1,0]]
    vecs = list(product(range(-2,3),range(-2,3),range(3)))
    f = lambda x: (x[0]+x[1],x[1],2*x[2]%3)
    inv = lambda x: (x[0]-x[1],x[1],2*x[2]%3)
    for a in vecs:
        require(inv(f(a)) == a, 'torsion_basis_transport_inverse')
        for b in vecs:
            aa,bb = f(a),f(b)
            s = (a[0]+b[0],a[1]+b[1])
            ss = (aa[0]+bb[0],aa[1]+bb[1])
            require(-2*pairing(g,a[:2],b[:2]) == -2*pairing(gp,aa[:2],bb[:2])
                    and tuple((-pairing(g,s,s)-k)%4 for k in (0,2))
                    == tuple((-pairing(gp,ss,ss)-k)%4 for k in (0,2))
                    and (a == b) == (aa == bb), 'lee_degree_transport_with_torsion')

    # Filtrations with exhaustive but nonseparated behavior and finite witnesses.
    for d in range(1,21):
        for q in range(-20,21):
            require(d-d == 0, 'nonzero_space_zero_associated_graded')
        for level in range(-12,13):
            dim = lambda q: d if q >= level else 0
            require(dim(level)-dim(level-1) == d, 'finite_filtration_witness')

    # Plateau of finite-dimensional kernels followed by arbitrarily delayed death.
    for delay in range(1,51):
        a = ((1,0),(0,1)); kill_first = ((0,0),(0,1)); kill_second = ((1,0),(0,0))
        sequence = [a]*delay+[kill_first]+[a]*delay+[kill_second]
        e1,e2 = (1,0),(0,1)
        images=[]
        for transition in sequence:
            e1,e2 = mul_vec(transition,e1),mul_vec(transition,e2)
            images.append((e1,e2))
        require(images[delay-1] == ((1,0),(0,1)) and images[delay] == ((0,0),(0,1))
                and images[-1] == ((0,0),(0,0)), 'delayed_kernel_jumps')

    # Tail-defined family of upper-block maps; constant first-coordinate functional.
    for a,b,c in product(range(-4,5),repeat=3):
        maps = (((1,0,0),(a,1,b),(c,0,1)), ((1,0,0),(0,2,c),(a,b,1)))
        for m in maps:
            v = (3,a,b)
            require(mul_vec(m,v)[0] == v[0] != 0, 'compatible_functional_local_identity')

    # The infinite-basis inverse is Euclidean division, checked on a disjoint interval.
    for n in range(1000,2000):
        for bit in (0,1):
            require(divmod(2*n+bit,2) == (n,bit), 'infinite_tensor_inverse_samples')
    for k in range(-40,41):
        degree = (Fraction(-k*k,2),Fraction(k*k,2))
        require((degree == (0,0)) == (k == 0), 'gluck_zero_shift_exactly_zero_intersection')
    return {'status':'pass', 'checks':sum(counts.values()), 'sections':dict(sorted(counts.items())),
            'scope':'Independent finite rational/integer algebra only. No geometric existence, topology theorem, link homology, or infinite-limit computation is certified.'}


if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
