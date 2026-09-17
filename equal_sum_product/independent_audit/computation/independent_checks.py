#!/usr/bin/env python3
"""Independent exact controls and differential checks. Finite tests are not a proof."""
from pathlib import Path
from fractions import Fraction
from itertools import product
from math import prod
import datetime
import importlib.util
import json
import random
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]  # Repository's equal_sum_product package root.
spec = importlib.util.spec_from_file_location('submitted_checker', PACKAGE/'src/verify_matrix.py')
submitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(submitted)

# Direct declarative predicate, with no imports from the submitted audit code.
def definition(matrix, minimum=3, declared=None):
    if not isinstance(matrix, list) or len(matrix) < minimum:
        return False
    if not all(isinstance(row, list) for row in matrix):
        return False
    if len(matrix[0]) < 2 or len({len(row) for row in matrix}) != 1:
        return False
    entries = sum(matrix, [])
    if not all(type(x) is int and x >= 1 for x in entries):
        return False
    if len(set(entries)) != len(entries):
        return False
    quantities = [sum(row) for row in matrix] + [prod(column) for column in zip(*matrix)]
    if len(set(quantities)) != 1:
        return False
    return declared is None or (type(declared) is int and declared > 0 and declared == quantities[0])

result = {'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'finite_tests_are_not_universal_proof':True}
controls = {}
for path in sorted((PACKAGE/'certificates').glob('*.json')):
    obj = json.loads(path.read_text())
    if 'matrix' not in obj:
        continue
    a = obj['matrix']
    rows = [sum(r) for r in a]
    columns = [prod(c) for c in zip(*a)]
    controls[path.name] = {'row_sums':rows,'column_products':columns,'distinct_entries':len(set(sum(a,[]))), 'reciprocal_sum':str(sum(Fraction(1,x) for x in sum(a,[]))), 'valid_at_min_rows_2':definition(a,2,obj.get('N'))}
    assert submitted.verify(a, min_rows=2, expected_N=obj.get('N'))['valid'] == definition(a,2,obj.get('N'))
result['independent_controls'] = controls
assert controls['source_two_rows.json']['valid_at_min_rows_2']
assert sum(v['valid_at_min_rows_2'] for v in controls.values()) == 1

cases = 0
for m,n in [(1,2),(2,2),(2,3),(3,2)]:
    for values in product(range(0,6), repeat=m*n):
        a = [list(values[i*n:(i+1)*n]) for i in range(m)]
        for minimum in (1,2,3):
            assert submitted.verify(a,min_rows=minimum)['valid'] == definition(a,minimum)
            cases += 1
result['exhaustive_checker_comparisons']={'shapes':[[1,2],[2,2],[2,3],[3,2]],'values':[0,5],'min_rows':[1,2,3],'predicate_comparisons':cases}

source = json.loads((PACKAGE/'certificates/source_two_rows.json').read_text())['matrix']
rng = random.Random(20260917)
accepted = 0
for _ in range(200):
    order = list(range(10)); rng.shuffle(order)
    a = [[row[j] for j in order] for row in source]
    if rng.randrange(2): a.reverse()
    assert definition(a,2,840) and submitted.verify(a,min_rows=2,expected_N=840)['valid']
    accepted += 1
result['valid_source_permutations'] = accepted

bad_values = [None, True, False, 2.0, '2', {}, [], 0, -2, float('nan'), float('inf')]
for x in bad_values:
    a = [row.copy() for row in source]; a[0][0] = x
    assert submitted.verify(a,min_rows=2)['valid'] is False
for a in [None,True,4,{},[],[[]],[[],[],[]],[[1,2],None],[[1,2],[3]],[[1],[2],[3]]]:
    assert submitted.verify(a)['valid'] is False
result['additional_invalid_entry_cases']=len(bad_values)
result['additional_invalid_shape_cases']=10

# Both polynomials have degree at most 2 in each of x,y,z. Agreement on the
# 3x3x3 Cartesian grid determines their coefficients uniquely, proving identity.
for x,y,z in product(range(3), repeat=3):
    lhs = 2*(x*x*y*y+x*x*z*z+y*y*z*z-x*y*z*(x+y+z))
    rhs = (x-y)**2*z*z+(x-z)**2*y*y+(y-z)**2*x*x
    assert lhs == rhs
result['independent_polynomial_identity']={'grid':[0,1,2], 'evaluations':27,'degree_bound_per_variable':2,'method':'Exact tensor-grid polynomial identity test; universal given checked degree bound.'}

column_count=0
for m in range(3,6):
    for c in product(range(1,8),repeat=m):
        left = Fraction(sum(c),prod(c))
        right = sum(Fraction(1,x*x) for x in c)
        assert left <= right
        column_count += 1
result['independent_all_row_bound']={'m':[3,5],'entry_range':[1,7],'ordered_columns':column_count,'exact_rational':True}

# All integer-set instances in a different universe than submitted tests.
sets = 0
for mask in range(1,1<<13):
    values = [i+1 for i in range(13) if mask&(1<<i)]
    square_sum = sum(Fraction(1,x*x) for x in values)
    assert square_sum <= 2-Fraction(1,len(values)) < 2
    sets += 1
result['independent_distinct_sets']={'universe':[1,13],'nonempty_subsets':sets}

# Explicit hypothesis boundaries, calculated without the submitted checker.
assert sum(Fraction(1,2) for _ in range(4)) == 2
assert Fraction(2+2+2,2*2*2) == 3*Fraction(1,4)
# Subunit positive reals do not satisfy the cyclic reduction in general.
half_column = [Fraction(1,2)] * 4
assert sum(half_column) / prod(half_column) == 32
assert sum(1 / x**2 for x in half_column) == 16
result['boundary_notes']=['Repeated entries can satisfy row/column equality: three rows, four columns, every entry 2.', 'Integer lower bound 1 is essential to the omitted-factor comparison; e.g. four entries 1/2 give normalized column sum 32 and inverse-square sum 16.']
result['status']='passed'
(HERE/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='independent_controls'},indent=2))
