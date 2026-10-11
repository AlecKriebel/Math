#!/usr/bin/env python3
"""Reconstruct the author's finite test scope without importing their code."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json

def run():
    c=Counter()
    def test(v,name):
        if not v: raise AssertionError(name)
        c[name]+=1
    weights=[F(4,k*(k+1)*(k+2)) for k in range(1,502)]
    for n in range(1,501):
        test(weights[n-1]==F(2,n*(n+1))-F(2,(n+1)*(n+2)),'weight_difference')
        test(sum(weights[:n])==1-F(2,(n+1)*(n+2)),'normalization')
        test(sum((k+1)*weights[k] for k in range(n))==2-F(4,n+2),'first_moment')
        test(weights[n-1]*2>weights[n],'atom_order')
    for M in list(range(1,1001))+[2**k+j for k in range(11,41) for j in (-1,0,1)]:
        K=1
        while 2**K<2*M: K+=1
        test(2**K>=2*M,'threshold')
        # Closed-form omitted mass, rather than iterative greedy selection.
        n=(M+2).bit_length()-2
        residual=M-(2**(n+1)-2)
        missed=F(2,(n+1)*(n+2))-residual*F(4,(n+1)*(n+2)*(n+3)*2**(n+1))
        test(missed>=F(1,K*(K+1)),'missed_mass')
    for dimension in (1,2,3):
        for r in (0,1,2,3):
            vertices=tuple(product(range(-r,r+1),repeat=dimension))
            test(len(vertices)==(2*r+1)**dimension,'cube_size')
            for v,w in product(vertices,repeat=2):
                test(all(-2*r<=v[i]+w[i]<=2*r for i in range(dimension)),'minkowski_containment')
    for dimension,r,b in product(range(1,4),range(4),range(1,5)):
        M=pow(b,pow(2*r+1,dimension))
        K=M.bit_length()+(M.bit_count()!=1)
        test(2**K>=2*M,'source_word_threshold')
        test(K*(K+1)>0,'positive_denominator')
    return {'status':'PASS','assertions':sum(c.values()),'families':dict(c),
            'matches_author_claimed_count':sum(c.values())==141484,
            'implementation':'Independent reconstruction; no author-code imports',
            'not_an_infinite_process_proof':True}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
