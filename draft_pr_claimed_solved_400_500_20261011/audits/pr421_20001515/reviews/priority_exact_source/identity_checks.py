"""Priority identity checks, exact integer arithmetic; no proof search."""
import json
from functools import reduce
from math import gcd
from itertools import combinations

def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def monodromy_power(p, k):
    m = [[1,p,0],[0,1,2],[0,0,1]]
    out = [[1,0,0],[0,1,0],[0,0,1]]
    for _ in range(k):
        out = multiply(out, m)
    return [[out[i][j] - int(i == j) for j in range(3)] for i in range(3)]

def rank_two_smith(a):
    d1 = reduce(gcd, (abs(v) for row in a for v in row), 0)
    minors = []
    for i,j in combinations(range(3), 2):
        for k,l in combinations(range(3), 2):
            minors.append(abs(a[i][k]*a[j][l]-a[i][l]*a[j][k]))
    d12 = reduce(gcd, minors, 0)
    if d12 == 0:
        raise ValueError("Expected rank two")
    return [d1,d12//d1,0]

rows = []
for p in (1,2):
    for k in range(1,21):
        a = monodromy_power(p,k)
        expected = [[0,p*k,p*k*(k-1)],[0,0,2*k],[0,0,0]]
        if a != expected:
            raise RuntimeError("Power formula failed")
        snf = rank_two_smith(a)
        desired = [k,2*k,0] if p == 1 else [2*k,2*k,0]
        if snf != desired:
            raise RuntimeError("Smith formula failed")
        rows.append({"b_prefix_exponent":p,"time_cover_degree":k,"smith":snf,
                     "H1_free_rank":2,"H1_torsion_order":snf[0]*snf[1]})
print(json.dumps({"status":"PASS","checked_power_values":40,
 "general_formula_proof":"DEDUCTIONS.md","rows":rows}, indent=2))

