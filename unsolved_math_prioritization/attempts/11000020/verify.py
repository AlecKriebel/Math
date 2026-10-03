#!/usr/bin/env python3
"""Exact arithmetic controls, not a reconstruction of the MSSV classification."""
from fractions import Fraction as F
import json
from pathlib import Path

count = 0
def check(test):
    global count
    count += 1
    assert test, count

def deficit(t):
    return F(1) - sum((F(1, n) for n in t), F(0))

# Analytic proof in RESULT.md gives a<=3, b<=5 and c<=23 when 0<D<1/8.
found = {
    (a,b,c)
    for a in range(2, 25)
    for b in range(a, 25)
    for c in range(b, 100)
    if F(0) < deficit((a,b,c)) < F(1,8)
}
expected = {(2,3,c) for c in range(7,24)} | {
    (2,4,5), (2,4,6), (2,4,7), (2,5,5), (3,3,4)
}
check(found == expected)
check(len(found) == 22)

def is_power(n, p):
    while n > 1 and n % p == 0:
        n //= p
    return n == 1

for a,b,c in sorted(found):
    check(F(0) < deficit((a,b,c)) < F(1,8))
    if (a,b) == (2,3):
        check(c != 6) # coprime commuting factors force product order 6
    elif (a,b) == (2,4):
        check(not is_power(c,2)) # product remains in Sylow 2-subgroup
    elif (a,b) == (2,5):
        check(c != 10) # coprime commuting factors force product order 10
    elif (a,b) == (3,3):
        check(not is_power(c,3)) # product remains in Sylow 3-subgroup
    else:
        raise AssertionError('unhandled signature')

check(F(1)-3*F(1,4) >= F(1,8))
check(F(1)-F(1,3)-2*F(1,4) >= F(1,8))
check(F(1)-F(1,2)-2*F(1,6) >= F(1,8))
check(-2 + 3*F(1,2) + F(2,3) == F(1,6))
check(-2 + 5*F(1,2) == F(1,2))

rows = [
    {'row':5,'group_id':[128,138]},
    {'row':6,'group_id':[128,136]},
    {'row':7,'group_id':[128,134]},
    {'row':8,'group_id':[128,75]},
]
check(len({tuple(r['group_id']) for r in rows}) == 4)
for r in rows:
    order, index = r['group_id']
    check(order == 2**7)
    check(is_power(order,2))
    check(order == 16*(9-1))
    check(order*deficit((2,4,8)) == 2*9-2)
check(deficit((2,4,8)) == F(1,8))

out = {
    'status':'PASS',
    'assertions':count,
    'small_deficit_signatures':len(found),
    'credited_genus':9,
    'nilpotent_maximum_order':128,
    'source_group_ids':[r['group_id'] for r in rows],
    'classification_reproduced':False,
    'scope':'Exact arithmetic and finite signature controls supplement RESULT.md; published full-group existence is an explicit dependency.'
}
print(json.dumps(out, indent=2, sort_keys=True))
