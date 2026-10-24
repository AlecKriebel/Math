#!/usr/bin/env python3
"""Independent exact grid-interpolation audit of selected fixed-zero coefficients.

Evaluates Q=V(vertices)*product(nonadjacent edge-sum differences), including
its actual integer Vandermonde. It uses the original binomial grid weights,
not the simplified signed-permutation/factorial formula being audited.
"""
import argparse
from functools import reduce
from itertools import permutations
from math import comb, factorial, gcd, prod
from time import perf_counter


def audit_exponent_vectors(exponent_vectors):
    n=len(exponent_vectors[0])
    assert all(len(t)==n and sum(t)==n*(n-2) for t in exponent_vectors)
    assert all(all(0<=a<n for a in t) for t in exponent_vectors)
    nonadjacent = [(i,j) for i in range(n) for j in range(i+1,n)
                   if j-i not in (1,n-1)]
    numerators = [0]*len(exponent_vectors)
    nonzero_values = 0
    for first in range(max(t[0] for t in exponent_vectors)+1):
      for tail in permutations(a for a in range(n) if a!=first):
        point=(first,)+tail
        sums=[point[i]+point[(i+1)%n] for i in range(n)]
        color_factor=1
        for i,j in nonadjacent:
            difference=sums[j]-sums[i]
            if difference==0:
                color_factor=0
                break
            color_factor*=difference
        if not color_factor:
            continue
        nonzero_values+=1
        vertex_factor=prod(point[j]-point[i]
                           for i in range(n) for j in range(i+1,n))
        q_value=vertex_factor*color_factor
        for witness_index, exponent in enumerate(exponent_vectors):
            weight=1
            for a,t in zip(point,exponent):
                if a>t:
                    weight=0
                    break
                weight*=(-1)**(t-a)*comb(t,a)
            numerators[witness_index]+=weight*q_value
    result=[]
    for exponent,numerator in zip(exponent_vectors,numerators):
        denominator=prod(factorial(t) for t in exponent)
        coefficient,remainder=divmod(numerator,denominator)
        assert remainder==0
        result.append((exponent,coefficient))
    return result,nonzero_values


def audit_coefficients(n,positions):
    vectors=[tuple(0 if i==0 else n-2 if i==j else n-1 for i in range(n)) for j in positions]
    return audit_exponent_vectors(vectors)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,default=11)
    parser.add_argument('--positions',type=int,nargs='+',default=[1,2])
    parser.add_argument('--n10-combined',action='store_true')
    args=parser.parse_args()
    start=perf_counter()
    if args.n10_combined:
        args.n=10
        result,nonzero_values=audit_exponent_vectors([(0,8,9,9,9,9,9,9,9,9),(1,9,8,8,9,9,9,9,9,9)])
    else:
        result,nonzero_values=audit_coefficients(args.n,args.positions)
    for exponent,coefficient in result:
        print('n=',args.n,'exponents=',exponent,'coefficient=',coefficient,flush=True)
    print('witness_gcd=',reduce(gcd,(abs(c) for _,c in result),0),
          'nonzero_Q_values=',nonzero_values,'seconds=',perf_counter()-start,flush=True)
    if args.n10_combined:
        assert [c for _,c in result]==[-30955393332,-125404419790]
    if args.n==11 and args.positions==[1,2]:
        assert [c for _,c in result]==[11098103614834,189427196282499]
