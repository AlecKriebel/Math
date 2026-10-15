#!/usr/bin/env python3
"""Fresh finite permutation controls; universal proof is in REPORT.md.

No candidate implementation is imported. Standard library only. This exercises
the law beyond the torus-bundle model and rejects falsely universal laws.
"""
from itertools import permutations, product
from fractions import Fraction
import json


def inverse_word(w):
    return w.swapcase()[::-1]


def freely_reduce(w):
    # Delete the first adjacent inverse pair and restart, independently of the
    # author's stack algorithm and the old auditor's whole-string replacement.
    while True:
        for i in range(len(w)-1):
            if w[i] == w[i+1].swapcase():
                w = w[:i] + w[i+2:]
                break
        else:
            return w


def bracket(a, b):
    return a+b+inverse_word(a)+inverse_word(b)


c = bracket('x', 'y')
d = 'x'+c+'X'
w = freely_reduce(bracket(c, d))
assert w == 'xyXYxxyXYXyxxYXX'
assert freely_reduce(w+inverse_word(w)) == ''
assert freely_reduce(bracket('x', 'x')) == ''
assert len(w) == 16


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    return tuple(p.index(i) for i in range(len(p)))


def evaluate(word, x, y):
    images = {'x': x, 'X': inverse(x), 'y': y, 'Y': inverse(y)}
    value = tuple(range(len(x)))
    for letter in word:
        value = compose(value, images[letter])
    return value


def even(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p))) % 2 == 0


models = {
    'S3': list(permutations(range(3))),
    'A4': [p for p in permutations(range(4)) if even(p)],
    'D8': sorted({tuple((s*i+k) % 4 for i in range(4)) for s in (-1,1) for k in range(4)}),
}
results = []
for name, elements in models.items():
    identity = tuple(range(len(elements[0])))
    assert all(compose(p,inverse(p)) == identity == compose(inverse(p),p) for p in elements)
    assert all(compose(p,q) in elements for p,q in product(elements,repeat=2))
    assert all(evaluate(w,p,q) == identity for p,q in product(elements,repeat=2))
    noncommuting = sum(compose(p,q) != compose(q,p) for p,q in product(elements,repeat=2))
    assert noncommuting > 0
    results.append({'model':name, 'elements':len(elements), 'ordered_pairs':len(elements)**2,
                    'witness_identity_pairs':len(elements)**2, 'noncommuting_pairs':noncommuting})

# S4 has nonabelian derived group A4. A real nonzero evaluation rejects an
# evaluator or witness routine that accidentally forces every group to pass.
negative = None
for x,y in product(permutations(range(4)), repeat=2):
    value = evaluate(w,x,y)
    if value != (0,1,2,3):
        negative = {'x':x,'y':y,'word_value':value}
        break
assert negative is not None

# The intrinsic word remains nonempty after explicit free-basis automorphisms.
substitutions = [ {'x':'xy','y':'y'}, {'x':'y','y':'x'}, {'x':'X','y':'y'} ]
basis_results = []
for sub in substitutions:
    sub.update({'X':inverse_word(sub['x']), 'Y':inverse_word(sub['y'])})
    reduced = freely_reduce(''.join(sub[a] for a in w))
    assert reduced
    basis_results.append({'x':sub['x'],'y':sub['y'],'reduced_witness':reduced,'length':len(reduced)})

# Both nonidentity images survive individually in S3, while their second-derived
# word dies. Individual generator survival therefore cannot certify injectivity.
x,y = (1,0,2),(1,2,0)
assert x != (0,1,2) != y
assert evaluate(c,x,y) != (0,1,2)
assert evaluate(w,x,y) == (0,1,2)

chis = [Fraction(b*c+a*c+a*b-a*b*c,a*b*c) for a,b,c in [(2,3,7),(2,4,5),(3,3,4),(2,3,6),(2,3,5)]]
assert list(map(str,chis)) == ['-1/42','-1/20','-1/12','0','1/30']

print(json.dumps({'result':'PASS','free_reduced_witness':w,'free_reduced_length':len(w),
 'metabelian_permutation_models':results,'nonmetabelian_S4_negative_control':negative,
 'free_basis_automorphisms':basis_results,'surviving_noncommuting_generators_do_not_imply_injectivity':True,
 'orbifold_euler_characteristics_with_boundary_controls':list(map(str,chis)),
 'limits':['Finite permutation checks do not prove the universal law.',
           'No topology classification, slope exhaustion, novelty, or source fidelity is certified by this script.']},indent=2,sort_keys=True))
