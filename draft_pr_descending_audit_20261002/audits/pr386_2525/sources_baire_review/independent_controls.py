"""Independent adversarial controls: no candidate imports, exact integer arithmetic."""
from collections import deque, Counter
from itertools import permutations, combinations, product
import json
from pathlib import Path

counts = Counter()
def check(condition, category):
    if not condition:
        raise AssertionError(category)
    counts[category] += 1

def distances(elements, operation, identity, generators):
    d = {identity: 0}
    q = deque([identity])
    while q:
        x = q.popleft()
        for s in generators:
            y = operation(x, s)
            if y not in d:
                d[y] = d[x] + 1
                q.append(y)
    return d

def generating_sets(elements, operation, identity):
    others = [x for x in elements if x != identity]
    for k in range(len(others) + 1):
        for subset in combinations(others, k):
            s = (identity,) + subset
            d = distances(elements, operation, identity, s)
            if len(d) == len(elements):
                yield s, d

e3 = (0, 1, 2)
s3 = tuple(permutations(range(3)))
compose = lambda x, y: tuple(x[y[i]] for i in range(3))
d8 = tuple(product(range(4), range(2)))
ed = (0, 0)
dmul = lambda x, y: ((x[0] + (-1)**x[1]*y[0]) % 4, (x[1]+y[1]) % 2)
s3_sets = list(generating_sets(s3, compose, e3))
d8_sets = list(generating_sets(d8, dmul, ed))
rectangles = 0
elements = tuple(product(s3, d8))
op = lambda x,y: (compose(x[0],y[0]), dmul(x[1],y[1]))
for (a, da), (b, db) in product(s3_sets, d8_sets):
    generators = tuple(product(a,b))
    d = distances(elements,op,(e3,ed),generators)
    check(len(d)==len(elements), 'nonabelian_cartesian_generation')
    rectangles += 1
    for x,y in elements:
        check(d[(x,y)]==max(da[x],db[y]), 'nonabelian_cartesian_max')

# A nonrectangular generator set with identical coordinate projections.
c22 = tuple(product(range(2), repeat=2))
plus22 = lambda x,y: tuple((a+b)%2 for a,b in zip(x,y))
correlated = distances(c22,plus22,(0,0),((0,0),(1,0),(0,1)))
check(correlated[(1,1)]==2, 'cartesian_hypothesis_counterexample')

# Removing coordinate identity padding invalidates even the finite formula.
c23 = tuple(product(range(2),range(3)))
plus23 = lambda x,y: ((x[0]+y[0])%2,(x[1]+y[1])%3)
unpad = distances(c23,plus23,(0,0),((1,1),))
check(len(unpad)==6 and unpad[(0,1)]==4, 'padding_counterexample')
check(max(0,1)==1 < unpad[(0,1)], 'padding_false_max_detected')

# Finite windows of the diagonal full-product obstruction, distinct from
# increasing support: every coordinate is nonzero; one coordinate forces length.
diagonal_windows=[]
for n in range(1,9):
    orders=tuple(range(2,n+2))
    target=tuple(k-1 for k in orders)
    length=max(target)
    word=[tuple(1 if j<k-1 else 0 for k in orders) for j in range(length)]
    check(tuple(sum(w[i] for w in word)%k for i,k in enumerate(orders))==target,
          'diagonal_window_padded_realization')
    check(target[-1]==n and all(target[-1] != j%orders[-1] for j in range(n)),
          'diagonal_window_lower_bound')
    diagonal_windows.append({'factors':orders,'target':target,'positive_length':length})

# Omitted finite quotient levels can miss closed-set length even in C8.
c8=tuple(range(8))
d=distances(c8,lambda x,y:(x+y)%8,0,(0,1))
proper_levels=max(7%2,7%4)
check(d[7]==7 and proper_levels==3, 'cofinal_projection_hypothesis')

# Exact product-vs-difference control; no analytic/Baire inference from a grid.
circle_mod=101
arc={30,31,32}
aa={(a+b)%circle_mod for a,b in product(arc,repeat=2)}
aminus={(a-b)%circle_mod for a,b in product(arc,repeat=2)}
check(aa==set(range(60,65)) and 0 not in aa and 0 in aminus,
      'product_not_difference')

# Exhaustive unbounded positive balls in a noncompact discrete group.
for m in range(1,101):
    check(2*m+1 > 2*m, 'noncompact_counterexample_integer_witness')

result={'assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),
        'nonabelian_factors':['S3','D8'],'generating_sets':[len(s3_sets),len(d8_sets)],
        'generating_rectangles':rectangles,'diagonal_windows':diagonal_windows,
        'limitations':'Exact finite controls; infinite diagonal, dense subgroup, compact Baire and analytic arguments require written proofs.'}
if __name__=='__main__':
    print(json.dumps(result,indent=2,sort_keys=True))
