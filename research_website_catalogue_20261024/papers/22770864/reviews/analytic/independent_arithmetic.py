"""Fresh analytic-review checks; never import the published verification code."""
from collections import Counter
from itertools import combinations
from math import factorial, comb, isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / 'sources/published-source/kourovka_16_63'
P = 1009
assert all(P % d for d in range(2, isqrt(P) + 1))
N = 31
zero = lambda: [0] * N
def basis(i):
    v = zero(); v[i] = 1; return v
C = [[zero() for _ in range(N)] for _ in range(N)]
def put(i, j, k, v):
    assert not C[i][j][k] or C[i][j][k] == v
    C[i][j][k] = v
    C[j][i][k] = -v
put(0, 1, 1, 2); put(0, 2, 2, -2); put(1, 2, 0, 1)
modules = {'U': (3, 6), 'V': (10, 4), 'W': (15, 6),
           'T': (22, 2), 'R': (25, 4), 'Z': (30, 0)}
for start, degree in modules.values():
    for i in range(degree + 1):
        put(0, start + i, start + i, degree - 2 * i)
        if i: put(1, start + i, start + i - 1, i)
        if i < degree: put(2, start + i, start + i + 1, degree - i)
def derivative_coefficient(x, y, dx, dy):
    if x < dx or y < dy: return 0
    return factorial(x) // factorial(x-dx) * (factorial(y) // factorial(y-dy))
for a, b, target, order in [('U','U','W',3), ('U','V','T',4),
                           ('U','W','T',5), ('U','R','T',4),
                           ('V','V','T',3), ('V','R','Z',4),
                           ('R','R','T',3)]:
    starta, m = modules[a]; startb, n = modules[b]; startc, degree = modules[target]
    for i in range(m+1):
        for j in range(n+1):
            if a == b and i >= j: continue
            coefficient = sum((-1)**k * comb(order,k)
                              * derivative_coefficient(m-i,i,order-k,k)
                              * derivative_coefficient(n-j,j,k,order-k)
                              for k in range(order+1))
            if coefficient:
                assert 0 <= i+j-order <= degree
                put(starta+i,startb+j,startc+i+j-order,coefficient)
def bracket(v,w):
    result=zero()
    for i,a in enumerate(v):
        if not a: continue
        for j,b in enumerate(w):
            if b:
                for k,c in enumerate(C[i][j]):
                    result[k] += a*b*c
    return result
def add(*vs): return [sum(row) for row in zip(*vs)]
units = [basis(i) for i in range(N)]
checks = 0
for i,j,k in combinations(range(N),3):
    assert add(bracket(units[i],C[j][k]), bracket(units[j],C[k][i]),
               bracket(units[k],C[i][j])) == zero()
    checks += 1
# Reconstruct the adapted basis and its inverse directly from x,y,t definitions.
b = [units[0], add(*(units[i] for i in [1,2,4,10,27])), units[3]]
tail = [i for i in range(N) if i not in (0,1,3)]
b += [units[i] for i in tail]
def adapted(v):
    return [v[0],v[1],v[3]] + [v[i]-v[1]*(i in (2,4,10,27)) for i in tail]
weights=[0,0,1]+[2]*28
terms=[]
for i,j in combinations(range(N),2):
    for k,c in enumerate(adapted(bracket(b[i],b[j]))):
        if c: terms.append([i,j,k,c*P**(2+weights[i]+weights[j]-weights[k])])
presentation=json.loads((SOURCE/'data/group_lie_presentation.json').read_text())
assert terms == presentation['bracket_terms_i_lt_j']
# Exterior-cube character decomposition independently checks the Jacobi argument.
weights6=list(range(-6,7,2))
character=Counter(sum(t) for t in combinations(weights6,3))
decomposition=[]
while any(character.values()):
    highest=max(k for k,v in character.items() if v)
    decomposition.append(highest)
    for w in range(-highest,highest+1,2):
        character[w]-=1; assert character[w]>=0
assert decomposition==[12,8,6,4,0]
assert sum([87,55,758,6,25]) == 931
assert sum(v*m for v,m in enumerate([87,55,758,6,25])) == 1689
assert 31*1689 == 30*1689+1689 == 52359
assert 2*847 >= 1689+4 and 846 < P
# Exact divisibility bounds for initial large-denominator degrees; subsequent
# degrees are covered analytically by v_p(n!) <= n/(p-1).
def factorial_valuation(n):
    total=0
    while n: n//=P; total+=n
    return total
for r in range(P-1,200000):
    assert r-6-factorial_valuation(r+1) > 0
    if r>=P: assert r-5-factorial_valuation(r)>0
result={'integer_jacobi_triples':checks, 'exported_presentation_terms_match':len(terms),
        'exterior_cube_V6_highest_weights':decomposition,
        'arithmetic_and_denominator_bound_checks':'passed',
        'source_code_imports':False}
(HERE/'independent_arithmetic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
