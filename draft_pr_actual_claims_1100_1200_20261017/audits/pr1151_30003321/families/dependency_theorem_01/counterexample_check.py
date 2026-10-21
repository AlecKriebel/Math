"""Finite sign-prefix checks for the infinite examples proved in REPORT.md.

No external dependencies. Finite checks illustrate, rather than prove, the
quantified infinite statements. Fractions avoid floating-point comparisons.
"""
from fractions import Fraction

N = 16
q = ['+' + '-' * n for n in range(N)]
p = [s + '+' for s in q]
E = {''} | set(q) | set(p)

def lex(a, b):
    for i in range(max(len(a), len(b))):
        x = {'-': -1, '+': 1}.get(a[i] if i < len(a) else '', 0)
        y = {'-': -1, '+': 1}.get(b[i] if i < len(b) else '', 0)
        if x != y:
            return -1 if x < y else 1
    return 0

for s in E:
    assert all(s[:i] in E for i in range(len(s)))
for n in range(N - 1):
    assert lex(p[n], p[n + 1]) == 1
for a in E:
    for i in range(len(a)):
        r = a[:i]
        if lex(r, a) > 0:
            assert r in q
assert all(not any(t != s and t.startswith(s) for t in E) for s in p)
assert Fraction(1, 2).denominator != 1
print(f'PASS: prefix closure, descending p support, right-predecessor coefficient assignment, leaf property for {N} levels; dyadic 1/2 is not integral.')
print('Infinite support and all-level assertions are proved in REPORT.md, not inferred from this bounded computation.')
