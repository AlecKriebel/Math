#!/usr/bin/env python3
"""Exact arithmetic checks, conditional on standard character formulas in notes.

This does not compute character tables from representations, or settle21.135.
It checks hook-length dimensions, field-parameter orbits, central-block subset
obstructions, and a finite affine action used to falsify an overstrong lemma.
"""
from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import product
from math import factorial, gcd, lcm
import json


def partitions(n, ceiling=None):
    if n == 0:
        yield ()
        return
    for first in range(min(n, ceiling or n), 0, -1):
        for rest in partitions(n-first, first):
            yield (first,) + rest


def transpose(part):
    return tuple(sum(row >= j for row in part) for j in range(1, part[0]+1))


def symmetric_degree(part):
    trans = transpose(part)
    hooks = 1
    for i, row in enumerate(part):
        for j in range(row):
            hooks *= row-j + trans[j]-i-1
    return factorial(sum(part)) // hooks


def alternating_degrees(n):
    result = Counter()
    for part in partitions(n):
        trans = transpose(part)
        if part > trans:
            continue
        d = symmetric_degree(part)
        if part == trans:
            assert d % 2 == 0
            result[d//2] += 2
        else:
            result[d] += 1
    assert sum(m*d*d for d,m in result.items()) == factorial(n)//2
    return result


def invariant(degrees):
    n = sum(m*d*d for d,m in degrees.items())
    ell = lcm(*degrees)
    assert n % ell == 0
    assert all(n % d == 0 for d in degrees)
    return {'order': n, 'degree_lcm': ell, 'delta': n//ell,
            'linear_count': degrees[1],
            'multiplicity_gcd': reduce(gcd, degrees.values()),
            'spectrum': {str(d):degrees[d] for d in sorted(degrees)}}


def prime_factors(n):
    result = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] = result.get(p,0)+1
            n //= p
        p += 1
    if n > 1:
        result[n] = result.get(n,0)+1
    return result


def pprime_mass(degrees, p):
    return sum(m*d*d for d,m in degrees.items() if d % p)


def perfect_small_action_certificate(degrees):
    inv = invariant(degrees)
    if inv['linear_count'] != 1:
        return {'passes': False, 'reason': 'not perfect'}
    tests = []
    for p,a in prime_factors(inv['delta']).items():
        soluble = a <= 1 or (p in (2,3) and a <= 2)
        mass = pprime_mass(degrees,p)
        central_excluded = mass > inv['order']//p
        tests.append({'prime':p,'maximum_rank':a,
                      'all_allowable_GL_solvable':soluble,
                      'pprime_mass':mass,'quotient_order':inv['order']//p,
                      'central_excluded_by_mass':central_excluded})
    return {'passes':all(t['all_allowable_GL_solvable'] and
                         t['central_excluded_by_mass'] for t in tests),
            'tests':tests}


def product_degrees(a,b):
    result=Counter()
    for d,m in a.items():
        for e,n in b.items():
            result[d*e] += m*n
    return result


def psl2_even_degrees(f):
    q=2**f
    assert f>=2
    return Counter({1:1,q:1,q-1:q//2,q+1:(q-2)//2})


def parameter_orbits(modulus, multiplier):
    """Nonzero Z/modulus indices identified under j~-j."""
    canonical=lambda j:min(j % modulus, (-j) % modulus)
    todo=set(range(1,(modulus-1)//2+1))
    lengths=Counter()
    while todo:
        start=min(todo)
        orbit=set()
        x=start
        while x not in orbit:
            orbit.add(x)
            x=canonical(multiplier*x)
        assert x==start
        assert orbit <= todo
        todo -= orbit
        lengths[len(orbit)] += 1
    return lengths


def prime_field_extension(f, extension_prime):
    assert f % extension_prime == 0
    q=2**f
    r=2**(f//extension_prime)
    result=Counter({1:extension_prime,q:extension_prime})
    orbit_data={}
    for modulus, base_degree in ((q-1,q+1),(q+1,q-1)):
        lengths=parameter_orbits(modulus,r)
        assert set(lengths) <= {1,extension_prime}
        orbit_data[str(base_degree)]={str(k):v for k,v in sorted(lengths.items())}
        for length,count in lengths.items():
            # An invariant character has p extensions; a p-orbit induces once.
            result[base_degree*length] += count*extension_prime//length
    result=+result
    assert invariant(result)['order']==extension_prime*q*(q*q-1)
    return result,orbit_data


def central_derived_quotient_remainders(degrees,p):
    n=invariant(degrees)['order']
    target=n//p-pprime_mass(degrees,p)
    terms=[(d,m) for d,m in sorted(degrees.items()) if d % p==0]
    witnesses=[]
    if target>=0:
        for counts in product(*(range(m+1) for d,m in terms)):
            if sum(c*d*d for c,(d,m) in zip(counts,terms)) == target:
                witnesses.append({str(d):c for c,(d,m) in zip(counts,terms) if c})
    return {'prime':p,'target':target,'terms':terms,'witnesses':witnesses,
            'excluded':not witnesses}


def f4_multiply(a,b):
    value=0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7  # X^2+X+1
    return value


def matrix_multiply(x,y):
    a,b,c,d=x
    e,f,g,h=y
    return (f4_multiply(a,e)^f4_multiply(b,g),
            f4_multiply(a,f)^f4_multiply(b,h),
            f4_multiply(c,e)^f4_multiply(d,g),
            f4_multiply(c,f)^f4_multiply(d,h))


def matrix_act(mat,vector):
    a,b,c,d=mat
    x,y=vector
    return (f4_multiply(a,x)^f4_multiply(b,y),
            f4_multiply(c,x)^f4_multiply(d,y))


def binary_pair(mask,vector):
    encoding=vector[0] | (vector[1]<<2)
    return (mask & encoding).bit_count() % 2


def dual_act(mat,mask):
    basis=((1,0),(2,0),(0,1),(0,2))
    return sum(binary_pair(mask,matrix_act(mat,v))<<j for j,v in enumerate(basis))


def affine_action_check():
    identity=(1,0,0,1)
    group=[g for g in product(range(4),repeat=4)
           if f4_multiply(g[0],g[3])^f4_multiply(g[1],g[2])==1]
    assert len(group)==60
    orbit={matrix_act(g,(1,0)) for g in group}
    dual_orbit={dual_act(g,1) for g in group}
    stabilizer=[g for g in group if dual_act(g,1)==1]
    assert len(orbit)==len(dual_orbit)==15
    assert len(stabilizer)==4
    assert all(matrix_multiply(g,g)==identity for g in stabilizer)
    assert all(matrix_multiply(g,h)==matrix_multiply(h,g)
               for g,h in product(stabilizer,repeat=2))
    degrees=psl2_even_degrees(2)
    degrees[15]+=4
    inv=invariant(degrees)
    assert inv['order']==960 and inv['delta']==16
    return {'linear_group_order':60,'natural_orbit':15,'dual_orbit':15,
            'dual_stabilizer_order':4,'dual_stabilizer_exponent':2,
            'affine_spectrum':inv,'M2':pprime_mass(degrees,2)}


def main():
    a7=alternating_degrees(7)
    assert a7==Counter({1:1,6:1,10:2,14:2,15:1,21:1,35:1})
    g16,orbits16=prime_field_extension(4,2)
    assert g16==Counter({1:2,16:2,17:6,30:4,34:2})
    normalized=Counter({d:m//2 for d,m in g16.items()})
    assert all(m % 2==0 for m in g16.values())
    g512,orbits512=prime_field_extension(9,3)
    assert g512==Counter({1:3,512:3,511:12,513:9,1533:84,1539:84})
    families=[]
    for f in range(2,11):
        q=2**f
        s=psl2_even_degrees(f)
        assert invariant(s)['delta']==1
        pair=product_degrees(a7,s)
        certificate=perfect_small_action_certificate(pair)
        assert certificate['passes']
        assert Fraction(pprime_mass(s,2),invariant(s)['order'])>=Fraction(11,15)
        assert Fraction(pprime_mass(s,3),invariant(s)['order'])>Fraction(1,2)
        families.append({'q':q,'order':invariant(pair)['order'],
                         'certificate':certificate})
    alternating=[]
    for n in range(5,33):
        degrees=alternating_degrees(n)
        inv=invariant(degrees)
        alternating.append({'n':n,'delta':inv['delta'],
                            'certificate':perfect_small_action_certificate(degrees)})
    s5=Counter({1:2,4:2,5:2,6:1})
    report={
        'scope':'Exact checks of stated restricted lemmas; no solution of21.135.',
        'A7':{'invariants':invariant(a7),
              'certificate':perfect_small_action_certificate(a7)},
        'S5_central_C2':central_derived_quotient_remainders(s5,2),
        'PSL2_16_field_C2':{'invariants':invariant(g16),'parameter_orbits':orbits16,
            'central_derived_C2':central_derived_quotient_remainders(g16,2),
            'normalized_candidate':invariant(normalized),
            'normalized_realizability':'Not established by this computation.'},
        'PSL2_512_field_C3':{'invariants':invariant(g512),'parameter_orbits':orbits512,
            'normalized_degree_divisibility_obstruction':[
                d for d in g512 if (invariant(g512)['order']//3) % d]},
        'affine_counterexample_to_mass_only':affine_action_check(),
        'A7_times_PSL2_even_examples':families,
        'alternating_filter_examples':alternating,
    }
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
