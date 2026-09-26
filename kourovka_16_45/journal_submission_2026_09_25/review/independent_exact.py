#!/usr/bin/env python3
"""Independent exact audit written from the displayed manuscript specification.

Python standard library only. No input files, tables, or supplied verifiers are
read. Run with python3 review/independent_exact.py from the submission directory.
All mathematical checks use integer arithmetic. Wall-clock metadata is excluded
from the stable JSON certificate printed on standard output.
"""

from collections import Counter, deque
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def matrix_system(p):
    identity = (1, 0, 0, 1)

    def mul(a, b):
        return ((a[0]*b[0] + a[1]*b[2]) % p,
                (a[0]*b[1] + a[1]*b[3]) % p,
                (a[2]*b[0] + a[3]*b[2]) % p,
                (a[2]*b[1] + a[3]*b[3]) % p)

    return identity, mul


def closure(generators, identity, mul):
    generators = tuple(generators)
    found = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in generators:
            y = mul(x, g)
            if y not in found:
                found.add(y)
                queue.append(y)
    return frozenset(found)


def power(x, n, identity, mul):
    result = identity
    for _ in range(n):
        result = mul(result, x)
    return result


def order(x, identity, mul):
    y = x
    n = 1
    while y != identity:
        y = mul(y, x)
        n += 1
        require(n < 1000000, "Order bound exceeded")
    return n


def enumerate_subgroups(elements, identity, mul):
    # Every subgroup has a finite generating sequence. Each generator in any
    # such sequence is among the extensions visited here, proving coverage.
    records = {frozenset([identity]): ()}
    queue = deque(records)
    while queue:
        subgroup = queue.popleft()
        gens = records[subgroup]
        for x in elements:
            if x not in subgroup:
                newgens = gens + (x,)
                generated = closure(newgens, identity, mul)
                if generated not in records:
                    records[generated] = newgens
                    queue.append(generated)
    return records


def rank_checks(subgroups, elements, identity, max_rank):
    positions = {x: i for i, x in enumerate(elements)}
    full = (1 << len(elements)) - 1
    identity_mask = 1 << positions[identity]
    masks = sorted(sum(1 << positions[x] for x in K)
                   for K in subgroups if len(K) != len(elements))
    rank_counts = {}
    faithful_counts = {}
    for rank in range(1, max_rank + 1):
        irredundant = faithful = 0
        for family in combinations(masks, rank):
            bottom = full
            for mask in family:
                bottom &= mask
            essential = True
            for omitted in range(rank):
                deleted = full
                for j, mask in enumerate(family):
                    if j != omitted:
                        deleted &= mask
                if deleted == bottom:
                    essential = False
                    break
            if essential:
                irredundant += 1
                faithful += bottom == identity_mask
        rank_counts[str(rank)] = irredundant
        faithful_counts[str(rank)] = faithful
    return rank_counts, faithful_counts


def affine_system(p):
    I, mm = matrix_system(p)
    identity = (0, 0, I)

    def mul(a, b):
        x, y, h = a
        u, v, k = b
        return ((x+h[0]*u+h[1]*v) % p,
                (y+h[2]*u+h[3]*v) % p, mm(h, k))

    return identity, mul


def meet(family):
    require(len(family) > 0, "Nonempty family required")
    answer = set(family[0])
    for K in family[1:]:
        answer.intersection_update(K)
    return frozenset(answer)


def deletion_orders(family):
    return [len(meet(family[:i] + family[i+1:])) for i in range(len(family))]


def main(subgroups_output=None):
    output = {"arithmetic": "exact Python integers; no external inputs"}
    p = 29
    I, mm = matrix_system(p)
    minus = (28, 0, 0, 28)
    A, B = (0, 28, 1, 0), (2, 7, 12, 28)
    H = closure([A, B], I, mm)
    require(len(H) == 120, "Complement order")
    require(all((a*d-b*c) % p == 1 for a,b,c,d in H), "Determinants")
    require(power(A,2,I,mm) == power(B,3,I,mm)
            == power(mm(A,B),5,I,mm) == minus, "Triangle relations")

    # Generate the graph of the proposed isomorphism, then verify all products.
    I5, mul5 = matrix_system(5)
    A5, B5 = (0,4,1,0), (0,4,1,1)
    graph = closure([(A5,A),(B5,B)], (I5,I),
                    lambda x,y:(mul5(x[0],y[0]),mm(x[1],y[1])))
    sl5 = {(a,b,c,d) for a,b,c,d in product(range(5), repeat=4)
           if (a*d-b*c) % 5 == 1}
    iso = dict(graph)
    require(len(graph) == len(iso) == len(sl5) == 120
            and set(iso) == sl5 and set(iso.values()) == set(H), "SL2(5) bijection")
    require(all(iso[mul5(x,y)] == mm(iso[x],iso[y]) for x in sl5 for y in sl5),
            "SL2(5) homomorphism all products")

    perm_id = tuple(range(5))
    pm = lambda s,t: tuple(s[t[i]] for i in range(5))
    perm_a, perm_b = (1,0,3,2,4), (2,1,4,3,0)
    quotient_graph = closure([(A,perm_a),(B,perm_b)], (I,perm_id),
                             lambda x,y:(mm(x[0],y[0]),pm(x[1],y[1])))
    quotient = dict(quotient_graph)
    alternating = {s for s in product(range(5),repeat=5)
                   if len(set(s)) == 5 and
                   sum(s[i] > s[j] for i in range(5) for j in range(i+1,5)) % 2 == 0}
    require(len(quotient_graph) == len(quotient) == 120
            and set(quotient.values()) == alternating
            and {h for h in H if quotient[h] == perm_id} == {I,minus},
            "A5 quotient")
    require(all(quotient[mm(x,y)] == pm(quotient[x],quotient[y]) for x in H for y in H),
            "A5 quotient all products")
    require({h for h in H if order(h,I,mm) == 2} == {minus}, "Unique involution")

    R = [A, (12,24,0,17), (25,3,4,4)]
    require(R[1] == mm(mm(B,A),power(B,2,I,mm))
            and R[2] == mm(mm(A,R[1]),power(mm(A,B),2,I,mm)), "Witness words")
    require(all(r in H and mm(r,r) == minus for r in R), "Witness squares")
    pairs = [closure(R[:i]+R[i+1:],I,mm) for i in range(3)]
    require([len(K) for K in pairs] == [8,12,20], "Pair subgroup orders")
    require([order(mm(R[1],R[2]),I,mm),order(mm(R[0],R[2]),I,mm),
             order(mm(R[0],R[1]),I,mm)] == [4,3,10], "Product orders")
    require(closure(R,I,mm) == H and all(R[i] not in pairs[i] for i in range(3)),
            "Independent generating triple")
    require(meet(pairs) == {I,minus}, "Pair subgroup common intersection")

    H_sorted = sorted(H)
    subgroups = enumerate_subgroups(H_sorted,I,mm)
    if subgroups_output is not None:
        Path(subgroups_output).write_text(json.dumps(sorted(sorted(K) for K in subgroups),
                                                     indent=2) + '\n')
    ranks, faithful = rank_checks(subgroups,H_sorted,I,4)
    require(len(subgroups) == 76 and ranks['4'] == 0 and ranks['3'] > 0
            and faithful['3'] == 0 and faithful['2'] > 0, "Complement ranks")
    inverses = {h: power(h,order(h,I,mm)-1,I,mm) for h in H}
    cores = [frozenset(x for x in K if all(mm(mm(h,x),inverses[h]) in K for h in H))
             for K in pairs]
    require(all(core == {I,minus} for core in cores), "Pair subgroup cores")
    normal_subgroups = [K for K in subgroups
                        if all(mm(mm(h,x),inverses[h]) in K for h in (A,B) for x in K)]
    require(sorted(map(len,normal_subgroups)) == [1,2,120], "Normal subgroups H")
    output['complement'] = {
        "order": len(H), "SL2_5_all_products_verified":120**2,
        "A5_all_products_verified":120**2,
        "subgroup_count":len(subgroups),
        "subgroup_order_distribution":dict(sorted(Counter(map(len,subgroups)).items())),
        "irredundant_family_counts":ranks, "faithful_family_counts":faithful,
        "normal_subgroup_orders":sorted(map(len,normal_subgroups)),
        "pair_orders":[len(K) for K in pairs], "pair_core_orders":list(map(len,cores)),
    }

    lines = [(1,t) for t in range(p)] + [(0,1)]
    stabilizer_orders = []
    for x,y in lines:
        stabilizer = {h for h in H
                      if ((h[0]*x+h[1]*y)*y-(h[2]*x+h[3]*y)*x) % p == 0}
        require(len(stabilizer) == 4 and any(order(h,I,mm) == 4 for h in stabilizer),
                "Line stabilizer cyclic order four")
        stabilizer_orders.append(len(stabilizer))
    require([h for h in H if (h[0],h[2]) == (1,0) and (h[1],h[3]) == (0,1)] == [I],
            "Faithful action / translation centralizer")
    output['line_stabilizers'] = {"count":len(lines),"orders":stabilizer_orders}

    # Independently enumerate the largest scalar group from the line lemma.
    scalar = next(x for x in range(2,p) if pow(x,4,p) == 1 and pow(x,2,p) != 1)
    scalar_mul = lambda a,b: ((a[0]+a[1]*b[0]) % p, a[1]*b[1] % p)
    scalar_identity = (0,1)
    scalar_group = closure([(1,1),(0,scalar)],scalar_identity,scalar_mul)
    scalar_subgroups = enumerate_subgroups(sorted(scalar_group),scalar_identity,scalar_mul)
    scalar_ranks, scalar_faithful = rank_checks(scalar_subgroups,sorted(scalar_group),scalar_identity,3)
    require(len(scalar_group) == 116 and scalar_ranks['3'] == 0 and scalar_ranks['2'] > 0,
            "Scalar lemma finite case")
    output['scalar_line_case'] = {"order":len(scalar_group), "subgroups":len(scalar_subgroups),
                                 "irredundant_family_counts":scalar_ranks}

    one, am = affine_system(p)
    S = [(1,0,I)] + [(0,0,r) for r in R]
    G = closure(S,one,am)
    omissions = [closure(S[:i]+S[i+1:],one,am) for i in range(4)]
    require(len(G) == 100920 and [len(K) for K in omissions] == [120,6728,10092,16820],
            "Affine group and omission orders")
    require(all(S[i] not in omissions[i] for i in range(4)), "Affine independent set")
    Z0 = frozenset([one,(0,0,minus)])
    require(meet(omissions) == Z0, "Four-way affine intersection")
    conjugate = am(am((1,0,I),(0,0,minus)),(28,0,I))
    require(conjugate == (2,0,minus) and conjugate not in Z0, "Nonnormal bottom")
    L = [closure([(1,0,I),(0,0,minus)],one,am),
         closure([(0,1,I),(0,0,minus)],one,am),
         closure([(1,1,I),(2,0,minus)],one,am)]
    require([len(K) for K in L] == [58,58,58], "Faithful base subgroup orders")
    require(L[0]&L[1] == {one,(0,0,minus)}
            and L[0]&L[2] == {one,(2,0,minus)}
            and L[1]&L[2] == {one,(0,27,minus)}
            and meet(L) == {one}, "Faithful base exact intersections")
    require(deletion_orders(L) == [2,2,2], "Faithful family essentiality")
    # Conjugation by these generators suffices for normality; the core of H is
    # trivial also follows directly from the intersection with one conjugate,
    # because this representation is fixed-point-free on nonzero vectors.
    complement = omissions[0]
    translated = {am(am((1,0,I),h),(28,0,I)) for h in complement}
    require(complement & translated == {one}, "Complement core trivial")
    VZ = {(x,y,h) for x in range(p) for y in range(p) for h in (I,minus)}
    inverse_affine = [(28,0,I)] + [(0,0,inverses[r]) for r in R]
    require(all(am(am(s,z),inv) in VZ for s,inv in zip(S,inverse_affine) for z in VZ),
            "VZ normality by generators")
    output['affine'] = {
        "order":len(G), "omission_orders":list(map(len,omissions)),
        "omission_deletion_orders":deletion_orders(omissions),
        "omission_intersection":sorted(Z0), "nonnormality_conjugate":conjugate,
        "faithful_base_subgroup_orders":list(map(len,L)),
        "faithful_base_deletion_orders":deletion_orders(L), "coset_degree":3*len(G)//58,
        "complement_intersection_with_translation_conjugate":1,
        "VZ_normal_order":len(VZ),
        "elements_sha256":hashlib.sha256(json.dumps(sorted((x,y,*h) for x,y,h in G),
                                                       separators=(',',':')).encode()).hexdigest(),
    }

    p = 11
    I11, mm11 = matrix_system(p)
    A11,B11,C = (0,10,1,0),(0,2,5,1),(6,10,0,2)
    H11 = closure([A11,B11],I11,mm11)
    require(len(H11) == 120 and C in H11 and order(C,I11,mm11) == 10,
            "Characteristic 11 complement and C")
    one11, am11 = affine_system(p)
    C2,C5 = power(C,2,I11,mm11),power(C,5,I11,mm11)
    Q = [closure([(1,0,I11),(0,0,C)],one11,am11),
         closure([(1,4,I11),(0,0,C)],one11,am11),
         closure([(1,0,I11),(0,1,I11),(0,0,C5)],one11,am11),
         closure([(1,0,I11),(0,1,I11),(0,0,C2)],one11,am11)]
    require(meet(Q) == {one11} and deletion_orders(Q) == [11,11,5,2],
            "Characteristic 11 faithful rank-four witness")
    output['characteristic_11'] = {"complement_order":len(H11),"C_order":10,
                                    "subgroup_orders":list(map(len,Q)),
                                    "deletion_orders":deletion_orders(Q),
                                    "total_intersection_order":len(meet(Q))}
    output['status'] = "PASS: every assertion verified"
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subgroups-output', help='Optional path for exact matrix subgroup sets')
    main(parser.parse_args().subgroups_output)
