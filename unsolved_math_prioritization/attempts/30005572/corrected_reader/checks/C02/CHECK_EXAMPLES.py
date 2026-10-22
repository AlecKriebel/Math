"""Exact arithmetic checks for the residue-module examples. No external data."""
from math import gcd, isqrt
import json

def prime_to(n, primes):
    for p in primes:
        while n % p == 0:
            n //= p
    return n

def reduced_forms(D):
    assert D < 0 and D % 4 in (0, 1)
    out = []
    for a in range(1, isqrt(abs(D)//3) + 2):
        for b in range(-a, a+1):
            if (b*b-D) % (4*a):
                continue
            c = (b*b-D)//(4*a)
            if a > c or gcd(gcd(a, abs(b)), c) != 1:
                continue
            if (abs(b) == a or a == c) and b < 0:
                continue
            out.append((a, b, c))
    return out

forms = reduced_forms(-23)
assert forms == [(1,1,6), (2,-1,3), (2,1,3)]
assert 2**2 + 2*(-1) + 6*(-1)**2 == 8
assert pow(2,3,7) == 1 and 2 % 7 != 1 and pow(2,2,7) != 1
assert [x for x in range(1,7) if pow(x,3,7) == 1] == [1,2,4]
examples = []
for name,Q,f in [("Gaussian norm 29",29,1), ("Gaussian norm 13",13,1),
                 ("Gaussian inert 11",121,1), ("Nonprincipal q over 2 in D=-23",2,3)]:
    m = Q**f-1
    examples.append({"example":name,"Q":Q,"f":f,"residue_exponent":m,
                     "over_Z_1_6":prime_to(m,(2,3)),"over_Z_1_30":prime_to(m,(2,3,5))})
assert [(e["over_Z_1_6"],e["over_Z_1_30"]) for e in examples] == [(7,7),(1,1),(5,1),(7,7)]
# Abstract C_7 example checks that the residual 7-group action need not vanish.
# This is a module check, not a claim about a specified imaginary quadratic field.
assert (29**7-1) % 49 == 0 and (29**7-1) % 343 != 0
assert 29 % 49 != 1 and pow(29,7,49) == 1
print(json.dumps({"status":"PASS","reduced_forms_D_minus_23":forms,"examples":examples,
 "abstract_p_group_action":{"C":"C_7","Q":29,"p":7,"p_primary_exponent":49,
 "Frobenius_multiplier":29,"Frobenius_nontrivial":True,"Frobenius_order":7}},indent=2))
