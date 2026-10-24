#!/usr/bin/env python3
"""Exact independent certificate: exterior square of the 5D standard A6 module."""
from itertools import permutations
from collections import Counter
import json

def even(p):
    return sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2==0

def standard_character(p):
    return sum(i==p[i] for i in range(6))-1

hist=Counter()
norm_numerator=0
for p in permutations(range(6)):
    if not even(p):
        continue
    chi=standard_character(p)
    square=tuple(p[p[i]] for i in range(6))
    numerator=chi*chi-standard_character(square)
    assert numerator%2==0
    wedge2=numerator//2
    norm_numerator+=wedge2*wedge2
    hist[wedge2]+=1
assert sum(hist.values())==360
assert norm_numerator==360
assert ((5*5-5)//2)==10
print(json.dumps({"group":"A6","order":360,"construction":"exterior square of permutation-standard degree5 representation","dimension":10,"character_value_multiplicities":dict(sorted(hist.items())),"norm_numerator":norm_numerator,"norm_denominator":360,"inner_product":1,"conclusion":"irreducible complex degree10 representation; inflates to 3.A6"},indent=2))
