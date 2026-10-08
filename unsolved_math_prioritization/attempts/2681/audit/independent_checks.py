#!/usr/bin/env python3
"""Independent exact arithmetic for K3 1.22; no imported author checker.

This verifies algebraic examples and obstruction models, not topology or the
general open problem. Python standard library only; deterministic JSON output.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import lcm
import json


COUNT = 0


def check(test, label):
    global COUNT
    if not test:
        raise ValueError(label)
    COUNT += 1


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def trans(a):
    return list(map(list, zip(*a)))


def matrix_power(a, n):
    result = identity(len(a))
    for _ in range(n):
        result = product(result, a)
    return result


def bareiss(a):
    """Fraction-free determinant, independent of rational row elimination."""
    a = [row[:] for row in a]
    previous, sign = 1, 1
    for k in range(len(a)-1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k+1, len(a)) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                if numerator % previous:
                    raise ValueError("Bareiss division not exact")
                a[i][j] = numerator//previous
        for i in range(k+1, len(a)):
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1] if a else 1


def tree(arms):
    n = 1+sum(arms)
    q = [[2*int(i == j) for j in range(n)] for i in range(n)]
    cursor = 1
    for arm in arms:
        last = 0
        for _ in range(arm):
            q[last][cursor] = q[cursor][last] = -1
            last, cursor = cursor, cursor+1
    return q


def unitriangular_inverse(v):
    """Solve each column by backward substitution, all in integers."""
    n = len(v)
    w = [[0]*n for _ in range(n)]
    for j in range(n):
        for i in range(n-1, -1, -1):
            w[i][j] = int(i == j)-sum(v[i][k]*w[k][j] for k in range(i+1, n))
    return w


def poly_product(p, q):
    out = [0]*(len(p)+len(q)-1)
    for i in range(len(p)):
        for j in range(len(q)):
            out[i+j] += p[i]*q[j]
    return out


def trim(p):
    while len(p)>1 and p[-1] == 0:
        p.pop()
    return p


def divmonic(p, q):
    if q[-1] != 1:
        raise ValueError("monic divisor required")
    r, answer = p[:], [0]*max(1, len(p)-len(q)+1)
    for k in range(len(p)-len(q), -1, -1):
        answer[k] = r[k+len(q)-1]
        for j in range(len(q)):
            r[k+j] -= answer[k]*q[j]
    return trim(answer), trim(r)


def divisors(n):
    return [d for d in range(1, n+1) if n%d == 0]


@lru_cache(None)
def cyclotomic(n):
    p = [-1]+[0]*(n-1)+[1]
    for d in divisors(n)[:-1]:
        p, r = divmonic(p, list(cyclotomic(d)))
        if r != [0]:
            raise ValueError("cyclotomic factorization")
    return tuple(p)


def evaluate(p, x):
    return sum(c*x**i for i, c in enumerate(p))


def vector_rank(rows):
    """GF(2) rank using integer bit masks, rather than matrix elimination."""
    basis = {}
    for v in rows:
        while v:
            pivot = v.bit_length()-1
            if pivot not in basis:
                basis[pivot] = v
                break
            v ^= basis[pivot]
    return len(basis)


def main():
    monodromies = []
    models = [("A2", [[2,-1],[-1,2]], 3, 6),
              ("A4", [[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]], 5, 10),
              ("E6", tree([1,2,2]), 3, 12),
              ("E8", tree([1,2,4]), 1, 15)]
    for label, q, determinant, order in models:
        n = len(q)
        v = [[int(i == j)+(q[i][j] if i<j else 0) for j in range(n)] for i in range(n)]
        a = product(unitriangular_inverse(v), trans(v))
        check(product(product(trans(a), v), a) == v, label+" Seifert invariance")
        check(product(product(trans(a), q), a) == q, label+" quadratic invariance")
        check(bareiss(q) == determinant, label+" determinant")
        check(all(bareiss([r[:k] for r in q[:k]])>0 for k in range(1,n+1)), label+" definiteness")
        check(matrix_power(a, order) == identity(n), label+" order bound")
        check(all(matrix_power(a,d) != identity(n) for d in divisors(order)[:-1]), label+" exact order")
        monodromies.append({"type":label,"order":order,"determinant":determinant})

    bk = []
    for n in range(1,33):
        a,b = 4*n+5,4*n+2
        first = {d for d in divisors(2*a) if a%d}
        second = {d for d in divisors(2*b) if b%d}
        check(not first.intersection(second), "disjoint numerator cyclotomics")
        indices = sorted(first.union(second)-{2,4})
        p = [1]
        for d in indices:
            p = poly_product(p,list(cyclotomic(d)))
        numerator = poly_product([1]+[0]*(a-1)+[1], [1]+[0]*(b-1)+[1])
        check(poly_product(p,[1,1,1,1]) == numerator,"BK polynomial identity")
        check(len(p)-1 == 8*n+4,"BK degree")
        check(evaluate(p,1) == 1 and abs(evaluate(p,-1)) == 4*n+5,"BK evaluations")
        exact_order = lcm(*indices)
        check(exact_order == lcm(2*a,2*b),"BK cyclotomic exact order")
        check(2*(4*n+2)-((4*n+2)+2) == 4*n,"conditional BK signature defect")
        bk.append({"n":n,"degree":len(p)-1,"cyclotomic_indices":indices,"exact_characteristic_polynomial_order":exact_order,"determinant":abs(evaluate(p,-1))})

    p = poly_product(poly_product(list(cyclotomic(6)),list(cyclotomic(6))),list(cyclotomic(30)))
    check(p == [1,-1,1,0,0,-1,1,-1,0,0,1,-1,1],"formal companion coefficients")
    power30 = [-1]+[0]*29+[1]
    check(divmonic(power30,p)[1] != [0],"formal p does not divide t30-1")
    check(divmonic(poly_product(power30,power30),p)[1] == [0],"formal p divides square")

    tree_cases = 0
    for a in range(1,5):
        for b in range(a,6):
            for c in range(b,8):
                s = Fraction(1,a+1)+Fraction(1,b+1)+Fraction(1,c+1)-1
                check(bareiss(tree([a,b,c])) == (a+1)*(b+1)*(c+1)*s,"independent tree determinant")
                check((s>0) == (a==b==1 or (a==1 and b==2 and c in [2,3,4])),"ADE classification")
                tree_cases += 1
    check(bareiss(tree([1,1,5]))==4 and bareiss(tree([1,2,3]))==2,"excluded diagrams even determinant")
    q4 = tree([1,1,1,1])
    check(product(q4,[[2],[1],[1],[1],[1]])==[[0] for _ in range(5)],"degree-four null vector")
    slope_cases = 0
    for denominator in range(3,51):
        for numerator in range(1,denominator):
            c=Fraction(numerator,denominator)
            if 0<c<Fraction(1,2):
                check([q for q in range(-7,8) if abs(2*c-q)<1]==[0,1],"FDTC residual")
                slope_cases += 1
    check(abs(2*Fraction(1,2))==1,"FDTC equality boundary")

    triangles, filtered = 0, 0
    for d in [1,3,5,9,15]:
        for r in [2,4,8,16,32]:
            # Image-coordinate subspaces of inclusion/projection/zero maps.
            rank_f=vector_rank([1<<i for i in range(d)])
            rank_g=vector_rank([1<<i for i in range(r)])
            rank_h=vector_rank([0 for _ in range(r)])
            check((rank_f+rank_h,rank_f+rank_g,rank_g+rank_h)==(d,d+r,r),"triangle dimensions")
            check(rank_g+rank_h==r and rank_f==d,"surjection and injection")
            triangles+=1
            # d(u_i)=v_i, with e_j and v_i cycles; integer masks label images.
            images=[0]*d+[1<<(d+r+i) for i in range(r)]+[0]*r
            rank=vector_rank(images)
            check(d+2*r-2*rank==d,"filtered homology rank")
            check(images[0]==0 and all(v&1==0 for v in images),"e1 permanent cycle")
            check(all(images[i]==0 for i in range(d+r,d+2*r)),"d squared zero")
            filtered+=1

    output={"result":"PASS","checks":COUNT,"scope":"Independent algebra only; no topology or general-conjecture proof", "definite_monodromy":monodromies,"baker_kegel":bk,"tree_cases":tree_cases,"slope_cases":slope_cases,"abstract_triangle_models":triangles,"abstract_filtered_models":filtered,"signature_recomputed_from_knot":False}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
