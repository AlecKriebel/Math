#!/usr/bin/env python3
"""Independent review checks. Does not import or run the author's verifier.

Young branching replaces hook lengths; union-find replaces orbit iteration;
explicit matrix groups corroborate the group examples. Character-degree
classification and Clifford theory remain mathematical dependencies.
"""
from collections import Counter, deque
from functools import cache, reduce
from itertools import product
from math import factorial, gcd, lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1] / 'arithmetic'


@cache
def young_dimension(shape):
    if not shape:
        return 1
    total = 0
    for i, row in enumerate(shape):
        if i + 1 == len(shape) or row > shape[i + 1]:
            child = list(shape)
            child[i] -= 1
            total += young_dimension(tuple(x for x in child if x))
    return total


def partitions_by_growth(n):
    shapes = {()}
    for _ in range(n):
        next_shapes = set()
        for shape in shapes:
            for i in range(len(shape) + 1):
                if i == len(shape):
                    next_shapes.add(shape + (1,))
                elif i == 0 or shape[i] < shape[i - 1]:
                    child = list(shape)
                    child[i] += 1
                    next_shapes.add(tuple(child))
        shapes = next_shapes
    return shapes


def alternating(n):
    result = Counter()
    for shape in partitions_by_growth(n):
        trans = tuple(sum(x >= j for x in shape)
                      for j in range(1, shape[0] + 1))
        if shape < trans:
            result[young_dimension(shape)] += 1
        elif shape == trans:
            assert young_dimension(shape) % 2 == 0
            result[young_dimension(shape) // 2] += 2
    assert sum(d*d*m for d, m in result.items()) == factorial(n)//2
    return result


def invariants(spec):
    n = sum(d*d*m for d, m in spec.items())
    ell = lcm(*spec)
    return dict(order=n, degree_lcm=ell, delta=n//ell,
                linear_count=spec[1],
                multiplicity_gcd=reduce(gcd, spec.values()),
                spectrum={str(d): spec[d] for d in sorted(spec)})


def factors(n):
    p, result = 2, {}
    while p <= n:
        if n % p == 0:
            a = 0
            while n % p == 0:
                a += 1
                n //= p
            result[p] = a
        p += 1
    return result


def mass(spec, p):
    return sum(d*d*m for d, m in spec.items() if d % p)


def certificate(spec):
    inv = invariants(spec)
    tests = []
    for p, a in factors(inv['delta']).items():
        tests.append(dict(prime=p, maximum_rank=a,
                          all_allowable_GL_solvable=(a == 1 or
                                                   (p in (2, 3) and a <= 2)),
                          pprime_mass=mass(spec, p),
                          quotient_order=inv['order']//p,
                          central_excluded_by_mass=mass(spec,p)*p > inv['order']))
    return dict(passes=spec[1] == 1 and all(
        t['all_allowable_GL_solvable'] and t['central_excluded_by_mass']
        for t in tests), tests=tests)


def even_psl(q):
    return Counter({1: 1, q: 1, q-1: q//2, q+1: (q-2)//2})


def product_spec(a, b):
    out = Counter()
    for x, m in a.items():
        for y, k in b.items():
            out[x*y] += m*k
    return out


def sign_orbits_union_find(modulus, multiplier):
    parents = list(range(modulus))
    def root(a):
        while parents[a] != a:
            parents[a] = parents[parents[a]]
            a = parents[a]
        return a
    def union(a,b):
        parents[root(a)] = root(b)
    for a in range(1, modulus):
        union(a, (-a) % modulus)
        union(a, multiplier*a % modulus)
    sizes = Counter(root(a) for a in range(1, modulus))
    assert all(s % 2 == 0 for s in sizes.values())
    return Counter(s//2 for s in sizes.values())


def extension_even(q, multiplier, index):
    spec = Counter({1:index, q:index})
    orbits = {}
    for modulus, degree in ((q-1,q+1),(q+1,q-1)):
        counts = sign_orbits_union_find(modulus,multiplier)
        assert set(counts) <= {1,index}
        orbits[str(degree)] = {str(k):v for k,v in sorted(counts.items())}
        for orbit_length, multiplicity in counts.items():
            spec[degree*orbit_length] += multiplicity*index//orbit_length
    return spec, orbits


def field_data(q, polynomial):
    def mul(a,b):
        out = 0
        while b:
            if b % 2:
                out ^= a
            b //= 2
            a *= 2
            if a >= q:
                a ^= polynomial
        return out
    table = [[mul(a,b) for b in range(q)] for a in range(q)]
    for a in range(1,q):
        assert sum(table[a][b] == 1 for b in range(1,q)) == 1
    def mm(x,y):
        a,b,c,d=x
        e,f,g,h=y
        return (table[a][e]^table[b][g], table[a][f]^table[b][h],
                table[c][e]^table[d][g], table[c][f]^table[d][h])
    def act(g,v):
        a,b,c,d=g
        x,y=v
        return (table[a][x]^table[b][y],table[c][x]^table[d][y])
    group = [g for g in product(range(q),repeat=4)
             if table[g[0]][g[3]]^table[g[1]][g[2]] == 1]
    return table,mm,act,group


def conjugacy_components(elements, transformations):
    remaining=set(elements)
    sizes=[]
    while remaining:
        initial=next(iter(remaining))
        found={initial}
        todo=deque([initial])
        while todo:
            x=todo.popleft()
            for transform in transformations:
                y=transform(x)
                if y not in found:
                    found.add(y)
                    todo.append(y)
        assert found <= remaining
        remaining -= found
        sizes.append(len(found))
    return sorted(sizes)


def matrix_group_checks():
    # F16 = F2[t]/(t^4+t+1); construct all matrices, not parameter packets.
    t,mm,act,sl = field_data(16,19)
    identity=(1,0,0,1)
    assert len(sl)==4080
    sigma=lambda g: tuple(t[t[x][x]][t[x][x]] for x in g)
    assert all(sigma(sigma(g))==g for g in sl)
    assert any(sigma(g)!=g for g in sl)
    basis=(1,2,4,8)
    generators=[(1,a,0,1) for a in basis]+[(1,0,a,1) for a in basis]
    generated={identity}
    todo=deque([identity])
    while todo:
        g=todo.popleft()
        for h in generators:
            k=mm(g,h)
            if k not in generated:
                generated.add(k)
                todo.append(k)
    assert generated==set(sl)
    # Reject every possible inner implementer, using the generating matrices.
    inner_implementers=[]
    for h in sl:
        inverse_h=(h[3],h[1],h[2],h[0])
        if all(mm(mm(inverse_h,g),h)==sigma(g) for g in generators):
            inner_implementers.append(h)
    assert not inner_implementers
    transforms=[]
    for h in generators:
        # All chosen unipotents are involutions.
        transforms.append(lambda x,h=h: (mm(mm(h,x[0]),
                                               sigma(h) if x[1] else h),x[1]))
    transforms.append(lambda x:(sigma(x[0]),x[1]))
    classes=conjugacy_components(((g,e) for g in sl for e in (0,1)),transforms)
    assert len(classes)==16 and sum(classes)==8160

    # F4 affine example, independently as explicit affine maps.
    t4,mm4,act4,sl4=field_data(4,7)
    assert len(sl4)==60
    generators4=((1,1,0,1),(1,2,0,1),(1,0,1,1),(1,0,2,1))
    generated4={identity}
    todo4=[identity]
    while todo4:
        g=todo4.pop()
        for h in generators4:
            k=mm4(g,h)
            if k not in generated4:
                generated4.add(k)
                todo4.append(k)
    assert generated4==set(sl4)
    vectors=list(product(range(4),repeat=2))
    basis4=((1,0),(2,0),(0,1),(0,2))
    encode=lambda v: v[0]+4*v[1]
    pair=lambda mask,v: (mask & encode(v)).bit_count()%2
    duals={tuple(pair(1,act4(g,v)) for v in basis4) for g in sl4}
    assert len(duals)==15
    stabilizer=[g for g in sl4
                if all(pair(1,act4(g,v))==pair(1,v) for v in basis4)]
    assert len(stabilizer)==4
    assert all(mm4(g,g)==identity for g in stabilizer)
    assert all(mm4(g,h)==mm4(h,g) for g in stabilizer for h in stabilizer)
    differences={encode((v[0]^act4(g,v)[0],v[1]^act4(g,v)[1]))
                 for v in vectors for g in sl4}
    # In fact every vector occurs as a commutator with the natural module.
    assert differences==set(range(16))
    transforms4=[]
    for u in basis4:
        transforms4.append(lambda x,u=u:((x[0][0]^u[0]^act4(x[1],u)[0],
                                           x[0][1]^u[1]^act4(x[1],u)[1]),x[1]))
    for h in generators4:
        transforms4.append(lambda x,h=h:(act4(h,x[0]),mm4(mm4(h,x[1]),h)))
    affine_classes=conjugacy_components(((v,g) for v in vectors for g in sl4),
                                       transforms4)
    assert len(affine_classes)==9 and sum(affine_classes)==960
    return dict(PSL2_16_field_C2=dict(
        matrix_socle_order=4080, semidirect_order=8160,
        defining_polynomial='t^4+t+1', field_automorphism='entrywise fourth power',
        generators_generate_socle=True, automorphism_exact_order=2,
        possible_inner_implementers=0,
        conjugacy_class_sizes=classes, character_count=16),
        affine_F4=dict(linear_group_order=60, affine_group_order=960,
        defining_polynomial='t^2+t+1', dual_nonzero_orbit_size=15,
        generators_generate_linear_group=True,
        dual_stabilizer_order=4, stabilizer_element_orders_divide=2,
        module_commutator_set_size=16, conjugacy_class_sizes=affine_classes,
        character_count=9))


def gl2_derived_checks(p):
    ident=(1,0,0,1)
    def mul(x,y):
        a,b,c,d=x
        e,f,g,h=y
        return ((a*e+b*g)%p,(a*f+b*h)%p,
                (c*e+d*g)%p,(c*f+d*h)%p)
    def inverse(g):
        a,b,c,d=g
        k=pow((a*d-b*c)%p,-1,p)
        return (d*k%p,-b*k%p,-c*k%p,a*k%p)
    group={g for g in product(range(p),repeat=4)
           if (g[0]*g[3]-g[1]*g[2])%p}
    orders=[]
    while len(group)>1:
        orders.append(len(group))
        commutators={mul(mul(mul(inverse(x),inverse(y)),x),y)
                     for x in group for y in group}
        generated={ident}
        todo=[ident]
        while todo:
            x=todo.pop()
            for y in commutators:
                z=mul(x,y)
                if z not in generated:
                    generated.add(z)
                    todo.append(z)
        assert generated < group
        group=generated
    return orders+[1]


def quotient_filter_by_divisors():
    """Use bounded-sum dynamic programming, independently of nested choices."""
    spec={1:1,16:1,17:3,30:2,34:1}
    total=sum(d*d*m for d,m in spec.items())
    packets={1: [(1,)]}
    for d,m in spec.items():
        if d==1:
            continue
        next_packets={}
        for weight, supports in packets.items():
            for used in range(m+1):
                target=weight+used*d*d
                for support in supports:
                    next_packets.setdefault(target,[]).append(
                        support+((d,) if used else ()))
        packets=next_packets
    survivors=[]
    for candidate in range(1,total+1):
        if total%candidate:
            continue
        if any(candidate%lcm(*support)==0
               for support in packets.get(candidate,[])):
            survivors.append(candidate)
    assert survivors==[1,4080]
    expected=json.loads((PACKAGE/'spectrum_quotients_results.json').read_text())
    assert survivors==[x['order'] for x in expected['necessary_quotient_candidates']]
    return dict(distinct_sums=len(packets), packets_checked=sum(map(len,packets.values())),
                surviving_quotient_orders=survivors,
                conditional_conclusion='Any actual group realizing D0 must be simple.',
                no_realizing_group_constructed=True)


def main():
    expected=json.loads((PACKAGE/'exact_results.json').read_text())
    a7=alternating(7)
    assert invariants(a7)==expected['A7']['invariants']
    assert certificate(a7)==expected['A7']['certificate']
    altern=[]
    for e in expected['alternating_filter_examples']:
        spec=alternating(e['n'])
        actual=dict(n=e['n'],delta=invariants(spec)['delta'],
                    certificate=certificate(spec))
        assert actual==e
        altern.append(actual)
    family=[]
    for f in range(2,11):
        q=2**f
        spec=product_spec(a7,even_psl(q))
        item=dict(q=q,order=invariants(spec)['order'],certificate=certificate(spec))
        assert item==expected['A7_times_PSL2_even_examples'][f-2]
        family.append(item)
    semidirects={}
    for q,mult,index,key in ((16,4,2,'PSL2_16_field_C2'),
                             (512,8,3,'PSL2_512_field_C3')):
        spec,orbits=extension_even(q,mult,index)
        assert invariants(spec)==expected[key]['invariants']
        assert orbits==expected[key]['parameter_orbits']
        semidirects[key]=dict(invariants=invariants(spec),parameter_orbits=orbits)
    solutions=[(a,b,c) for a in range(3) for b in range(5) for c in range(3)
               if 64*a+225*b+289*c==586]
    assert not solutions
    s5_solutions=[(a,b) for a in range(3) for b in range(2)
                  if 16*a+36*b==8]
    assert not s5_solutions
    affine_spec=alternating(5)
    affine_spec[15]+=4
    assert invariants(affine_spec)==expected['affine_counterexample_to_mass_only']['affine_spectrum']
    assert mass(affine_spec,2)==944
    odd=[]
    for p in (5,7,11,13,17):
        q=p**p
        half=(q+(1 if q%4==1 else -1))//2
        spec=Counter({1:1,q:1,half:2})
        spec[q+1]+=(q-5)//4 if q%4==1 else (q-3)//4
        spec[q-1]+=(q-1)//4 if q%4==1 else (q-3)//4
        spec=+spec
        assert invariants(spec)['order']==q*(q*q-1)//2
        assert invariants(spec)['delta']==1
        assert [d for d in spec if d%p==0]==[q]
        odd.append(dict(p=p,q=q,base_delta=1,
                        unique_p_divisible_base_degree=q,
                        base_order_p_valuation=p,
                        semidirect_order_p_valuation=p+1,
                        largest_extension_degree_p_valuation=p,
                        conditional_semidirect_delta=p))
    hashes={name:hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()
            for name in ('research_notes.md','verify_arithmetic.py','exact_results.json',
                         'sources/manifest.json','followup_20261024.md',
                         'spectrum_quotients.py','spectrum_quotients_results.json')}
    source_checks=[]
    for source in json.loads((PACKAGE/'sources/manifest.json').read_text()):
        path=PACKAGE/'sources'/(source['name']+'.pdf')
        actual_hash=hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual_hash==source['sha256']
        assert path.stat().st_size==source['bytes']
        source_checks.append(dict(name=source['name'],sha256=actual_hash,
                                  bytes=path.stat().st_size,checked=True))
    output=dict(scope='Independent arithmetic and explicit group checks; no proof '
                      'of character classification, no full 21.135 solution.',
                input_sha256=hashes, alternating_branching_checks=altern,
                A7_product_checks=family, semidirect_parameter_checks=semidirects,
                central_block_equation_solutions=solutions,
                S5_central_block_equation_solutions=s5_solutions,
                affine_character_arithmetic=dict(invariants=invariants(affine_spec),
                                                 M2=mass(affine_spec,2)),
                explicit_matrix_groups=matrix_group_checks(),
                GL2_derived_series_orders={str(p):gl2_derived_checks(p) for p in (2,3)},
                odd_prime_symbolic_specializations=odd,
                quotient_filter=quotient_filter_by_divisors(),
                source_file_checks=source_checks)
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
