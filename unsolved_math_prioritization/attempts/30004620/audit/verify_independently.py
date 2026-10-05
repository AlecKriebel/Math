#!/usr/bin/env python3
"""Independent rational audit. No imports from the author package; no network."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, gcd, lcm
import json

if not __debug__:
    raise SystemExit('Run without -O.')

counts = Counter()
def require(value, label):
    if not value:
        raise AssertionError(label)
    counts[label] += 1

def dot(a, b):
    return sum((F(x)*y for x, y in zip(a, b)), F(0))

def det(m):
    n = len(m)
    answer = F(0)
    for p in permutations(range(n)):
        parity = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = F((-1)**parity)
        for i in range(n):
            term *= m[i][p[i]]
        answer += term
    return answer

def minor(m, i, j):
    return [row[:j]+row[j+1:] for k, row in enumerate(m) if k != i]

# Transcribed directly from the five rows of GH v2 (22), including stack factors.
primary_rows = [
    [F(1,1152),0,0,F(1,16)],
    [0,F(1,96),0,F(-1,8)],
    [0,F(1,48),F(1,24),F(-1,8)],
    [0,0,F(1,48),F(-1,16)],
    [0,0,F(1,4),F(1,4)],
]
rays = [tuple(F(scale)*v for v in row) for row, scale in zip(primary_rows,[1152,96,48,48,4])]
normals = [(1,0,0,0),(0,1,0,0),(-72,12,3,1),(72,-8,1,-1),(72,-12,3,-1)]

# Adjugate/Cramer's rule, independent of the author's elimination-based solver.
bases = []
for ids in combinations(range(5),4):
    m = [[rays[j][i] for j in ids] for i in range(4)]
    d = det(m)
    if d:
        inverse = [[(-1)**(i+j)*det(minor(m,j,i))/d for j in range(4)] for i in range(4)]
        bases.append((ids,inverse))
require(len(bases)==4, 'independent bases')

def basis_member(v):
    return any(all(dot(row,v)>=0 for row in inverse) for _,inverse in bases)

def interval_member(v):
    # Solve all five ray coefficients, leaving the T coefficient as a free variable.
    x,y,z,w = map(F,v)
    k0 = (w-72*x+12*y+3*z)/4
    lower = max(F(0),k0-z)
    upper = min(y,k0/3)
    return x>=0 and lower<=upper

def facets(v):
    return [dot(n,v) for n in normals]

def author_coefficients(v):
    x,y,z,w = map(F,v)
    p,q = facets(v)[2:4]
    t = max(F(0),y-q/4)
    return [x,y-t,t,t+q/4-y,p/4-3*t]

def reconstruct(coefficients):
    return tuple(sum(coefficients[j]*rays[j][i] for j in range(5)) for i in range(4))

found = set()
for ids in combinations(range(5),3):
    m = [list(rays[i]) for i in ids]
    n = [(-1)**j*det([row[:j]+row[j+1:] for row in m]) for j in range(4)]
    if not any(n):
        continue
    vals = [dot(n,r) for r in rays]
    if all(v<=0 for v in vals):
        n = [-v for v in n]
        vals = [-v for v in vals]
    if any(v<0 for v in vals):
        continue
    denominator = lcm(*(v.denominator for v in n))
    integers = [int(v*denominator) for v in n]
    common = gcd(*integers)
    found.add(tuple(v//common for v in integers))
require(found==set(normals), 'complete facet enumeration')
incidence = [facets(r) for r in rays]
require(incidence==[[1,0,0,0,0],[0,1,0,4,0],[0,1,12,0,0],[0,0,0,4,6],[0,0,4,0,2]], 'facet incidence')
require(tuple(rays[1][i]+3*rays[4][i] for i in range(4))==tuple(rays[2][i]+rays[3][i] for i in range(4)), 'ray circuit')

grid_points = grid_inside = 0
for x,y,z,r in product(range(3),range(5),range(7),range(-30,31)):
    v = (x,y,z,72*x-12*y+r)
    present = interval_member(v)
    require(present==basis_member(v), '6405 interval versus bases')
    require(present==(min(facets(v))>=0), '6405 interval versus facets')
    if present:
        coefficients = author_coefficients(v)
        require(min(coefficients)>=0 and reconstruct(coefficients)==v, 'grid constructive certificate')
        grid_inside += 1
    grid_points += 1

for v in product(range(-2,3),range(-2,3),range(-2,3),range(-3,4)):
    require(interval_member(v)==basis_member(v)==(min(facets(v))>=0), 'signed grid')

# Exact polynomial multiplication in L,D, instead of the author's binomial summation.
def multiply(a,b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out

d_degrees = list(map(F,['1/181440','0','0','1/720','0','-203/240','-4103/144']))
beta_degrees = list(map(F,['0','0','0','-11/48','-445/48']))
polynomial = [F(1)]
t, beta = [], []
for j in range(7):
    t.append(dot(polynomial,d_degrees))
    if j<=4:
        beta.append(dot(polynomial,beta_degrees))
    polynomial = multiply(polynomial,[12,-1])
require(t==list(map(F,['1/181440','1/15120','1/1260','41/5040','1/21','73/336','871/1008'])), 'corrected divisor degrees')
require(beta==list(map(F,['0','0','0','11/48','83/48'])), 'corrected beta degrees')
monomials = [(t[j],t[j+1],t[j+2],beta[j]) for j in range(5)]
expected_pqg = [list(map(F,row)) for row in [
    ['1/360','1/1512','1/504'],['7/240','11/1680','11/560'],
    ['11/60','5/126','43/420'],['13/15','27/140','367/840'],
    ['7/2','52/63','283/168'],
]]
for j,v in enumerate(monomials):
    require(facets(v)[2:]==expected_pqg[j], 'displayed monomial facets')
    require(min(facets(v))>0 and basis_member(v), 'strict monomial interior')
    require(reconstruct(author_coefficients(v))==v and min(author_coefficients(v))>=0, 'monomial decomposition')

def mixed(factors):
    p = [F(1)]
    for a,b in factors:
        p = multiply(p,[F(a),F(b)])
    v = tuple(sum(p[j]*monomials[j][i] for j in range(5)) for i in range(4))
    return p,v

original_trials = 0
for factors in product([(0,1),(1,0),(1,1),(1,2)],repeat=4):
    p,v = mixed(factors)
    require(min(facets(v))>0 and basis_member(v), '256 mixed divisor controls')
    original_trials += 1

# A numerical zero factor is the only degenerate product. Boundary nef divisors
# L and M, irrational coefficients in the proof, and vanishing factors are allowed.
extended_trials = zero_trials = 0
choices = [(0,0),(1,0),(0,1),(F(1,2),0),(0,F(2,3)),(1,1),(F(1,2),F(2,3))]
for factors in product(choices,repeat=4):
    p,v = mixed(factors)
    zero = any(a==b==0 for a,b in factors)
    require((not any(v))==zero, 'zero factor equivalence')
    require(min(facets(v))>=0 and (zero or min(facets(v))>0), 'degenerate interior qualification')
    extended_trials += 1
    zero_trials += zero

u = (0,1,0,-10)
printed = normals[:2]+[(0,0,1,0)]+normals[2:4]
require([dot(n,u) for n in printed]==[0,1,0,2,2], 'v2 printed tests witness')
require(dot(normals[4],u)==-2 and not interval_member(u), 'v2 missing facet witness')
require(tuple(F(a+b,6) for a,b in zip(normals[2],normals[4]))==(0,0,1,0), 'M squared redundant')
require(tuple(normals[3][i]+(0,-4,2,0)[i] for i in range(4))==normals[4], 'localization identity')
for y in range(8):
    for z in range(24):
        if 3*z>=8*y:
            require(2*z-4*y>=F(4,3)*y>=0, 'localization bound')

limit = (0,0,1,2)
require(tuple(F(4,5)*limit[i]+F(1,5)*rays[3][i] for i in range(4))==rays[4], 'closure loss of extremality')
for n in range(6,70):
    v = (F(1,n*n),F(1,n),F(1),F(2))
    require(v[0]>0 and v[1]>0 and v[1]**2==v[0]*v[2], 'closure model Hodge test')
    require(facets(v)[3]<0 and not interval_member(v), 'closure model outside cone')
    require((v[2]-v[3])/4<0<(3*v[2]+v[3])/4, 'closure face obstruction')

candidates = [(1,3,9,0),(1,4,16,57)]
for v,wanted in zip(candidates,[[-9,57,63],[81,-1,15]]):
    x,y,z,w = v
    tests = [x,y,z,w,12*x-y,12*y-z,y-3*x,z-3*y,3*y-8*x,3*z-8*y,y*y-x*z]
    require(min(tests)>=0 and facets(v)[2:]==wanted and not basis_member(v), 'unrealized numerical candidates')
    for r in rays:
        require((r[0]==0<x) or (r[1]==r[2]==0 and y>0), 'old-ray decompositions exclude candidate')

def rational_json(v):
    if isinstance(v,F):
        return str(v)
    if isinstance(v,(tuple,list)):
        return [rational_json(x) for x in v]
    if isinstance(v,dict):
        return {k:rational_json(x) for k,x in v.items()}
    return v

result = {
    'status':'PASS','problem_id':30004620,'disposition':'UNSOLVED 5/5',
    'independent_assertions':sum(counts.values()),'checks_by_label':dict(sorted(counts.items())),
    'author_grid_rebuilt':grid_points,'author_grid_inside':grid_inside,
    'signed_grid_points':875,'original_mixed_trials_rebuilt':original_trials,
    'extended_mixed_trials':extended_trials,'zero_factor_trials':zero_trials,
    'rays':rays,'facets':normals,'monomials':[{'j':j,'coordinates':v,'facets':facets(v),'coefficients':author_coefficients(v)} for j,v in enumerate(monomials)],
    'limitations':'Finite exact controls supplement universal written arguments. No geometric counterexample, global nefness proof, or original-problem solution is certified.'
}
print(json.dumps(rational_json(result),indent=2,sort_keys=True))
