#!/usr/bin/env python3
"""Independent bounded checks. No imports from the author package; Python >=3.8.

All test conditions use explicit exceptions, so optimized Python is also safe.
The geometric conclusions still require the audited proofs, not these counts.
"""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def binary_span(vectors):
    values = {0}
    for v in vectors:
        values |= {x ^ v for x in values}
    return frozenset(values)


@lru_cache(None)
def binary_subspaces(n):
    """Generate actual vector sets by adjoining vectors, never RREF matrices."""
    levels = [{frozenset({0})}]
    for dimension in range(n):
        next_level = set()
        for space in levels[-1]:
            for v in range(1, 1 << n):
                if v not in space:
                    next_level.add(space | frozenset(x ^ v for x in space))
        levels.append(next_level)
    return tuple(tuple(sorted(level, key=lambda s: tuple(sorted(s)))) for level in levels)


def gaussian_binary(n, r):
    if not 0 <= r <= n:
        return 0
    value = 1
    denominator = 1
    for i in range(r):
        value *= (1 << (n-i)) - 1
        denominator *= (1 << (r-i)) - 1
    return value // denominator


def exponents(n, degree):
    return [e for e in product(range(degree+1), repeat=n) if sum(e) == degree]


def exponent_add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def multiply_binary(vector, basis, variable, target):
    out = 0
    for j, monomial in enumerate(basis):
        if vector & (1 << j):
            out ^= 1 << target.index(exponent_add(monomial, variable))
    return out


def weight_two():
    rows = []
    for weights in ((1,1,1), (1,1,2), (2,2,3)):
        n = len(weights)
        units = [tuple(int(i == j) for i in range(n)) for j in range(n)]
        linear = [v for v, w in zip(units, weights) if w == 1]
        quadratic = [e for e in product(range(3), repeat=n)
                     if sum(a*w for a,w in zip(e,weights)) == 2]
        for r in range(len(linear)+1):
            m, N = len(linear), len(quadratic)
            E = weights.count(2) + r*(r+1)//2
            total = Counter()
            for kernel in binary_subspaces(m)[m-r]:
                forced = binary_span(multiply_binary(v,linear,x,quadratic)
                                     for v in kernel for x in linear)
                require(len(forced) == 1 << (N-E), 'weight-two relation rank')
                for s in range(N+1):
                    count = sum(forced <= K for K in binary_subspaces(N)[N-s])
                    require(count == gaussian_binary(E,s), 'weight-two fiber count')
                    total[s] += count
            for s in range(N+1):
                expected = gaussian_binary(m,r)*gaussian_binary(E,s)
                require(total[s] == expected, 'weight-two total count')
            rows.append({'weights':weights,'r':r,'bundle_rank':E,
                         'counts_by_s':dict(sorted(total.items()))})
    # An explicitly torsion-valued grading: x0,x1=(1,0), y=(1,1), z=(2,0)
    # in Z x Z/2. Squares of either linear degree collide in degree (2,0).
    linear0 = [(1,0,0,0),(0,1,0,0)]
    linear1 = [(0,0,1,0)]
    b0 = [(0,0,0,1),(2,0,0,0),(1,1,0,0),(0,2,0,0),(0,0,2,0)]
    b1 = [(1,0,1,0),(0,1,1,0)]
    torsion = []
    for r0 in range(3):
        for r1 in range(2):
            E0 = 1+r0*(r0+1)//2+r1*(r1+1)//2
            E1 = r0*r1
            fibers = 0
            for K0 in binary_subspaces(2)[2-r0]:
                for K1 in binary_subspaces(1)[1-r1]:
                    forced0 = binary_span(
                        [multiply_binary(v,linear0,x,b0) for v in K0 for x in linear0]
                        + [multiply_binary(v,linear1,x,b0) for v in K1 for x in linear1])
                    forced1 = binary_span(
                        [multiply_binary(v,linear0,x,b1) for v in K0 for x in linear1]
                        + [multiply_binary(v,linear1,x,b1) for v in K1 for x in linear0])
                    for E,basis,forced in ((E0,b0,forced0),(E1,b1,forced1)):
                        require(len(forced)==1 << (len(basis)-E), 'torsion block rank')
                        for s in range(len(basis)+1):
                            actual=sum(forced <= K for K in binary_subspaces(len(basis))[len(basis)-s])
                            require(actual == gaussian_binary(E,s), 'torsion fiber count')
                    fibers += 1
            torsion.append({'r0':r0,'r1':r1,'degree20_rank':E0,'degree21_rank':E1,
                            'degree_one_choices':fibers})
    return {'ordinary_weights':rows,'torsion_degree_collision':torsion}


def field_span(vectors, p):
    n = len(vectors[0])
    values = {tuple(0 for _ in range(n))}
    for v in vectors:
        values = {tuple((x+a*y)%p for x,y in zip(w,v))
                  for w in values for a in range(p)}
    return values


def cubic_check():
    q, c, units = exponents(3,2), exponents(3,3), exponents(3,1)
    index = {e:i for i,e in enumerate(c)}
    by_rank = Counter()
    incidence = Counter()
    for functional in range(1,1 << len(c)):
        rows = [sum(((functional >> index[exponent_add(x,y)]) & 1) << j
                    for j,y in enumerate(q)) for x in units]
        image = binary_span(rows)
        rank = len(image).bit_length()-1
        require(rank >= 1, 'nonzero cubic has nonzero contraction')
        by_rank[rank] += 1
        for s in range(7):
            incidence[s] += sum(image <= U for U in binary_subspaces(6)[s])
    require(dict(by_rank)=={1:7,2:84,3:932}, 'binary rank distribution')
    require(incidence[2]==301, 'direct binary h1321 count')
    rank3 = Counter()
    for first in range(10):
        for tail in product(range(3),repeat=9-first):
            F = (0,)*first+(1,)+tail
            rows = [tuple(F[index[exponent_add(x,y)]] for y in q) for x in units]
            size = len(field_span(rows,3))
            require(size in (3,9,27), 'ternary contraction image size')
            rank3[{3:1,9:2,27:3}[size]] += 1
    require(dict(rank3)=={1:13,2:468,3:29043}, 'ternary rank distribution')
    # The incorrect ordinary-derivative replacement fails in both small primes.
    failures = []
    for p, monomial in ((2,(2,1,0)), (3,(3,0,0))):
        contraction = [tuple(int(exponent_add(x,y)==monomial) for y in q) for x in units]
        derivative = []
        for i in range(3):
            e = list(monomial)
            coefficient = e[i] % p
            e[i] -= 1
            derivative.append(tuple(coefficient if tuple(e)==y else 0 for y in q))
        a,b = len(field_span(contraction,p)),len(field_span(derivative,p))
        require(a != b, 'naive derivative mutation must be rejected')
        failures.append({'prime':p,'monomial':monomial,'contraction_image_size':a,
                         'ordinary_derivative_image_size':b})
    return {'F2_rank_counts':dict(by_rank),'F2_direct_incidence_counts':dict(incidence),
            'F3_rank_counts':dict(rank3),'naive_derivative_negative_controls':failures}


def dual_add(a,b,p):
    return ((a[0]+b[0])%p,(a[1]+b[1])%p)


def dual_mul(a,b,p):
    return (a[0]*b[0]%p,(a[0]*b[1]+a[1]*b[0])%p)


def dual_span(rows,p):
    zero = ((0,0),)*len(rows[0])
    values = {zero}
    ring = tuple(product(range(p),repeat=2))
    for row in rows:
        values = {tuple(dual_add(x,dual_mul(a,y,p),p) for x,y in zip(v,row))
                  for v in values for a in ring}
    return values


def dual_number_controls():
    result=[]
    for p in (2,3):
        ring=list(product(range(p),repeat=2)); one=(1,0); eps=(0,1); zero=(0,0)
        minus_eps=(0,p-1)
        # Degree-two relation vectors in basis x^2,xy,y^2,z after y=eps*x.
        for t in ring:
            negative_t=((-t[0])%p,(-t[1])%p)
            relations=[(minus_eps,one,zero,zero),(zero,zero,one,zero),
                       (negative_t,zero,zero,one)]
            generated=dual_span(relations,p)
            kernel=set()
            for v in product(ring,repeat=4):
                value=zero
                for a,b in zip(v,(one,eps,zero,t)):
                    value=dual_add(value,dual_mul(a,b,p),p)
                if value==zero:
                    kernel.add(v)
            require(generated==kernel, 'symmetric quotient over dual numbers')
            require(len(kernel)==p**6, 'dual-number degree-two freeness')
        flat=nonflat=0
        for a,b in product(ring,repeat=2):
            # In the chart a0=b0=1, degree-(2,2) relations are
            # xyz-b*y^2 and a*xyz, giving quotient R/(a*b).
            relations=[(one,((-b[0])%p,(-b[1])%p)),(a,zero)]
            generated=dual_span(relations,p)
            quotient_size=p**4//len(generated)
            equation=dual_mul(a,b,p)==zero
            require((quotient_size==p**2)==equation, 'nilpotent Haiman incidence')
            flat+=equation; nonflat+=not equation
        require(dual_mul(eps,eps,p)==zero and dual_mul(eps,one,p)!=zero,
                'nilpotent incidence negative control')
        result.append({'prime':p,'weight_two_parameter_values':len(ring),
                       'haiman_flat_affine_chart_pairs':flat,'haiman_nonflat_pairs':nonflat})
    return result


def rank_one_toric():
    chains=0
    for ell in ((2,-2,0),(2,1,-2),(2,2,-2),(1,-1,0)):
        positive=tuple(max(x,0) for x in ell)
        negative=tuple(max(-x,0) for x in ell)
        for origin in product(range(4),repeat=3):
            lower=max(-origin[i]//ell[i] + int((-origin[i])%ell[i]!=0)
                      for i in range(3) if ell[i]>0)
            upper=min(origin[i]//(-ell[i]) for i in range(3) if ell[i]<0)
            fiber=[tuple(origin[i]+t*ell[i] for i in range(3))
                   for t in range(lower,upper+1)]
            require(fiber and all(min(m)>=0 for m in fiber), 'complete positive fiber')
            for left,right in zip(fiber,fiber[1:]):
                common=tuple(min(x,y) for x,y in zip(left,right))
                require(exponent_add(common,negative)==left and
                        exponent_add(common,positive)==right, 'adjacent binomial multiples')
            chains+=1
    # Arbitrary nilpotent chart coefficients, including both boundary charts.
    p=2; ring=list(product(range(p),repeat=2)); zero=(0,0); one=(1,0)
    flat_chains=0
    for length in range(1,6):
        for t in ring:
            for reverse in (False,True):
                relation=[]
                for j in range(length-1):
                    row=[zero]*length; row[j]=one; row[j+1]=t
                    if reverse: row.reverse()
                    relation.append(tuple(row))
                span=dual_span(relation,p) if relation else {((0,0),)*length}
                require(len(span)==len(ring)**(length-1), 'rank-one chart free quotient')
                flat_chains+=1
    return {'lattice_generators':[[2,-2,0],[2,1,-2],[2,2,-2],[1,-1,0]],
            'complete_degree_fibers_checked':chains,'nilpotent_chart_chains_checked':flat_chains}


def choose2_nonnegative(n):
    return comb(n,2) if n>=2 else 0


def cid_controls():
    checked=0
    for a in range(2,8):
        for u in range(2*a+3):
            for v in range(2*a+3):
                count1=count2=0
                for x0 in range(u+1):
                    for x1 in range(u-x0+1):
                        for y0 in range(v+1):
                            count1 += x0==0 and not (x1>=a and y0>=2*a)
                            count2 += x0<2*a and not (x0>=1 and y0>=1) and not (x1>=a and y0>=1)
                form1=(u+1)*(v+1)-max(u-a+1,0)*max(v-2*a+1,0)
                form2=v*min(u+1,a)+comb(u+2,2)-choose2_nonnegative(u-2*a+2)
                require((count1,count2)==(form1,form2), 'Cid-Ruiz exact piecewise counts')
                if (u,v)==(1,0):
                    require((count1,count2)==(2,3), 'distinct original low-degree functions')
                if u>=2*a-1 and v>=2*a-1:
                    p=2*a*u+a*v+3*a-2*a*a
                    require(count1==count2==p, 'stable polynomial')
                checked+=1
        dehom1=sum(x0==0 and not (x1>=a and y0>=2*a)
                   for x0,x1,y0 in ((1,0,0),(0,1,0)))
        dehom2=sum(x0<2*a and not (x0>=1 and y0>=1) and not (x1>=a and y0>=1)
                   for x0,x1,y0 in ((1,0,0),(0,1,0)))
        require((dehom1,dehom2)==(1,2), 'distinct dehomogenized low-degree functions')
    # A bounded direct check of the intersection by ideal membership.
    memberships=0
    for a in range(2,8):
        for x0,x1,y0 in product(range(2*a+2),repeat=3):
            J=(x0>=1 or x1>=a)
            K=(x0>=2*a or y0>=1)
            I=(x0>=2*a or (x0>=1 and y0>=1) or (x1>=a and y0>=1))
            require(I==(J and K), 'monomial intersection membership')
            memberships+=1
    # Product ranks are independently represented as exponent sets.
    units=exponents(3,1)
    kernels=(((2,0,0),(0,2,0),(0,0,2)),((2,0,0),(1,1,0),(1,0,1)))
    ranks=[len({exponent_add(x,y) for x in K for y in units}) for K in kernels]
    require(ranks==[9,6], 'multiplication rank jump')
    return {'bidegrees_checked':checked,'intersection_memberships_checked':memberships,
            'parameters_a':[2,3,4,5,6,7],'stable_rectangle_for_these_two_ideals':'u,v >= 2a-1',
            'rank_jump':ranks,'original_h10':[2,3],'dehomogenized_h10':[1,2],
            'not_a_uniform_regularity_bound_for_the_entire_parameter_scheme':True}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    for n in range(7):
        for r,spaces in enumerate(binary_subspaces(n)):
            require(len(spaces)==gaussian_binary(n,r), 'independent vector-set enumeration')
    out={'status':'PASS','scope':'independent bounded exact controls, not a proof of the general target',
         'weight_two':weight_two(),'cubic':cubic_check(),
         'nonreduced_bases':dual_number_controls(),'rank_one_toric':rank_one_toric(),
         'monomial_controls':cid_controls()}
    encoded=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded,end='')


if __name__=='__main__':
    main()
