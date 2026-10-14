#!/usr/bin/env python3
"""Finite supporting checks; these do not evaluate an arithmetic cocycle."""
import json
from math import ceil

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def v5(n):
    if n == 0:
        return 1000
    r = 0
    while n % 5 == 0:
        n //= 5
        r += 1
    return r

local = []
for n in range(9):
    # In Z_5[sqrt(-5)], p^(2k)=(5^k),
    # p^(2k+1)=(5^(k+1),5^k sqrt(-5)).
    vals = []
    if n == 0:
        points = [(a,b) for a in range(1,26) if a % 5 for b in range(25)]
    else:
        astep = 5 ** ((n+1)//2)
        bstep = 5 ** (n//2)
        points = [(1+astep*a, bstep*b) for a in range(5) for b in range(5)]
    for a,b in points:
        norm = a*a + 5*b*b
        vals.append(v5(norm*norm-1))
    expected = max(1,ceil(n/2))
    need(min(vals)==expected, f"bad local minimum n={n}")
    local.append({"p_level_exponent":n,"a":expected,"sample_minimum":min(vals)})

# The three ray-degree examples for discriminant -20 and h=2.
ray=[]
for l, expected_degree, expected_split in [(3,4,True),(13,168,False),(11,120,False)]:
    split = any((x*x+5)%l==0 for x in range(l))
    phi = (l-1)**2 if split else l*l-1
    degree = 2*phi//2  # units +/-1 inject at these levels
    need(split==expected_split and degree==expected_degree, f"ray check {l}")
    ray.append({"rational_level":l,"split":split,"ray_degree":degree,
                "passes_no_tame_five_inertia":degree%5!=0})

# An elementary model tests both stages and the exponent bound.
# It is deliberately not identified with any actual arithmetic module.
mod=25
s=[5,10]
compatible=[]
solutions=0
first_obstructions=0
second_obstructions=0
for a0 in range(mod):
    for a1 in range(mod):
        if (s[1]*a0-s[0]*a1)%mod:
            continue
        pair=(a0,a1)
        compatible.append(pair)
        actual=[u for u in range(mod) if all((t*u-a)%mod==0 for t,a in zip(s,pair))]
        roots=[u for u in range(mod) if (5*u-a0)%mod==0]
        if not roots:
            first_obstructions+=1
            need(not actual,"first obstruction incorrectly obstructs")
        else:
            u=roots[0]
            residue=[(a-t*u)%mod for t,a in zip(s,pair)]
            need(all(5*r%mod==0 for r in residue),"residue not in M[5]")
            corrections=[v for v in range(mod) if 5*v%mod==0 and all((t*v-r)%mod==0 for t,r in zip(s,residue))]
            need(bool(corrections)==bool(actual),"two-stage criterion mismatch")
            if not corrections:
                second_obstructions+=1
        if actual:
            solutions+=1
        need(all((t*a0-5*a)%mod==0 for t,a in zip(s,pair)),"5E not in delta(M)")
need((0,5) in compatible,"secondary example missing")
need(not any(all((t*u-a)%mod==0 for t,a in zip(s,(0,5))) for u in range(mod)),"secondary example soluble")
need(pow(6,5,25)==1 and 6%25!=1,"deep cyclotomic action check")
print(json.dumps({"local_depth_checks":local,"ray_degree_checks":ray,
                  "formal_module_only":{"compatible_families":len(compatible),"soluble_families":solutions,
                                        "first_stage_failures":first_obstructions,"second_stage_failures":second_obstructions},
                  "deep_twist":{"modulus":25,"C5_generator_image":6},
                  "actual_auxiliary_obstruction_evaluated":False},indent=2))
