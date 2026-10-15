#!/usr/bin/env python3
"""Independent finite checks of the frozen argument; not an unbounded proof."""
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


def check(bound, injections):
    # The carrier A_n has n+1 elements and basepoint 0.
    outgoing = {}
    for source in range(bound + 1):
        outgoing[source] = []
        for target in range(bound + 1):
            for image in product(range(target + 1), repeat=source):
                function = (0,) + image
                if injections and len(set(function)) != len(function):
                    continue
                outgoing[source].append((target, function))

    c = -1
    eq = lambda left, right: ('eq', left, right)
    neg = lambda proposition: ('neg', proposition)
    all_ = lambda proposition: ('all', proposition)
    ex = lambda proposition: ('ex', proposition)
    base_equality = eq(0, c)
    beta = all_(neg(neg(base_equality)))
    alpha = neg(beta)
    extra = ex(neg(base_equality))

    @lru_cache(None)
    def truth(n, environment, formula):
        operation = formula[0]
        if operation == 'eq':
            value = lambda term: 0 if term == c else environment[term]
            return value(formula[1]) == value(formula[2])
        if operation == 'top':
            return True
        if operation == 'bot':
            return False
        if operation == 'and':
            return all(truth(n, environment, part) for part in formula[1])
        if operation == 'or':
            return any(truth(n, environment, part) for part in formula[1])
        if operation == 'ex':
            return any(truth(n, environment + (element,), formula[1])
                       for element in range(n + 1))
        if operation == 'all':
            return all(truth(m, tuple(function[a] for a in environment) + (element,), formula[1])
                       for m, function in outgoing[n]
                       for element in range(m + 1))
        if operation == 'neg':
            return all(not truth(m, tuple(function[a] for a in environment), formula[1])
                       for m, function in outgoing[n])
        raise AssertionError(operation)

    rows = []
    for n in range(bound + 1):
        rows.append({'n': n, 'beta': truth(n, (), beta),
                     'alpha': truth(n, (), alpha), 'extra': truth(n, (), extra)})
        expected_beta = (not injections) or bound == 0
        assert rows[-1]['beta'] == expected_beta
        assert rows[-1]['alpha'] == (not expected_beta)
        assert rows[-1]['extra'] == (injections and n > 0)

    # Formula naturality is the pointwise geometric mechanism used by R.
    # Empty joins, empty meets, nested existentials and equalities in a
    # conjunction/disjunction are deliberately included.
    geometric = [
        ('top',), ('bot',), eq(0, c), eq(0, 1),
        ('or', ()), ('and', ()),
        ('or', (eq(0, c), eq(0, 1))),
        ('and', (eq(0, c), eq(0, 1))),
        ex(('and', (eq(2, 0), eq(2, 1)))),
        ex(('or', (eq(2, c), eq(2, 1)))),
        ex(ex(('and', (eq(2, 0), eq(3, 1), eq(2, 3))))),
        ('and', (ex(eq(2, 0)), ('or', (eq(0, c), eq(0, 1))))),
    ]
    values = {}
    naturality_checks = 0
    for n in range(bound + 1):
        for environment in product(range(n + 1), repeat=2):
            for formula in geometric:
                value = truth(n, environment, formula)
                values[(n, environment, formula)] = value
                for target, function in outgoing[n]:
                    transported = tuple(function[a] for a in environment)
                    assert not value or truth(target, transported, formula)
                    naturality_checks += 1
    return {'bound': bound, 'injections': injections,
            'arrows': sum(len(arrows) for arrows in outgoing.values()),
            'rows': rows, 'geometric_naturality_checks': naturality_checks}, values


def main():
    outputs = []
    for bound in range(4):
        all_maps, c_values = check(bound, False)
        injections, d_values = check(bound, True)
        assert c_values == d_values
        all_maps['geometric_values_identical_after_restriction'] = True
        outputs.extend([all_maps, injections])
    result = {'status': 'PASS',
              'scope': 'finite site boundary checks only, not infinitary/unbounded completeness',
              'runs': outputs}
    target = Path(__file__).with_name('independent_boundary_results.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
