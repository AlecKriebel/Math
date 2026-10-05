#!/usr/bin/env python3
"""Exact controls for a constructive proof in order two and scaling distinctions."""
from fractions import Fraction as F
import json


def need(x,why):
    if not x:
        raise ValueError(why)


def factor2(a,b,c):
    """Return (integer multiplicity, nonnegative integer vector) pairs.

    Expanding each multiplicity into that many identical columns gives an
    ordinary unweighted nonnegative integral Gram factor. This is an existence
    algorithm, with no minimal-width or complexity claim.
    """
    need(all(isinstance(x,int) and x>=0 for x in (a,b,c)) and a*c>=b*b,'not an integral doubly nonnegative matrix')
    P=[[1,0],[0,1]]; steps=0
    while a<b or c<b:
        previous=a+c
        if a<b:
            b,c=b-a,c+a-2*b
            P=[[r[0]+r[1],r[1]] for r in P]
        else:
            a,b=a+c-2*b,b-c
            P=[[r[0],r[0]+r[1]] for r in P]
        steps+=1
        need(a>=0 and b>=0 and c>=0 and a*c>=b*b,'congruence invariant')
        need(a+c<previous,'trace descent')
    terms=[]
    for n,w in ((a-b,(1,0)),(b,(1,1)),(c-b,(0,1))):
        if n:
            terms.append((n,[sum(x*y for x,y in zip(row,w)) for row in P]))
    return terms,steps


def gram(terms,n=2):
    return [[sum(weight*v[i]*v[j] for weight,v in terms) for j in range(n)] for i in range(n)]


def main():
    checked=0;max_steps=0
    for a in range(61):
        for b in range(61):
            for c in range(61):
                if a*c<b*b:
                    continue
                terms,steps=factor2(a,b,c)
                need(gram(terms)==[[a,b],[b,c]],'factor mismatch')
                need(all(weight>0 and all(isinstance(x,int) and x>=0 for x in v) for weight,v in terms),'invalid integral column')
                checked+=1;max_steps=max(max_steps,steps)
    for triple in ((0,1,0),(1,2,1),(-1,0,0),(F(1,2),0,1)):
        try:
            factor2(*triple)
        except ValueError:
            pass
        else:
            raise RuntimeError('invalid input accepted')
    M=[[2,3,1],[3,5,3],[1,3,5]]
    columns=[[F(2,2),F(3,2),F(1,2)]]*2+[[0,F(1,2),F(3,2)]]*2
    need(gram([(1,v) for v in columns],3)==M,'rational three-order witness')
    # Integral impossibility follows from the first row having exactly two
    # unit entries, hence row two has 1 and 2 there and nothing elsewhere.
    # The third row sums to 1 on those entries and cannot have dot product 3.
    admissible=[]
    for x in range(4):
        for y in range(4):
            if x+y==3 and x*x+y*y<=5:
                admissible.append((x,y))
                need(x*x+y*y==5,'unexpected row-two residual')
                need(max(x,y)<3,'integer dot-product obstruction failed')
    need(admissible==[(1,2),(2,1)],'row-two exhaustion')
    # A positive rational weight is a finite sum of rational squares without
    # invoking four squares: p/q = p*q copies of (1/q)^2.
    for p in range(1,20):
        for q in range(1,20):
            need(p*q*F(1,q)**2==F(p,q),'rational coefficient expansion')
    return {'status':'PASS','all_entries_0_through':60,'integral_psd_triples_checked':checked,
            'maximum_trace_descent_steps':max_steps,'invalid_input_controls':4,
            'three_order_rational_gram_identity':True,'three_order_integral_obstruction_cases':2,
            'rational_weight_expansion_controls':361,
            'scope':'Finite controls corroborate the separate all-input proof; no numerical tolerance or minimum-width claim.'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
