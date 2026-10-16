#!/usr/bin/env python3
"""Finite reconstruction of quotient witness extraction; no theorem claim."""
import itertools
import json
from pathlib import Path

TERMS = 4  # c, x1, x2, x3
PAIRS = list(itertools.combinations(range(TERMS), 2))


def quotient(equations):
    reach = [[i == j for j in range(TERMS)] for i in range(TERMS)]
    for a, b in equations:
        reach[a][b] = reach[b][a] = True
    for k in range(TERMS):
        for i in range(TERMS):
            for j in range(TERMS):
                reach[i][j] |= reach[i][k] and reach[k][j]
    # Least representative makes the witness selection canonical.
    reps = tuple(min(j for j in range(TERMS) if reach[i][j])
                 for i in range(TERMS))
    return reps, tuple(sorted(set(reps)))


def eq(a, b):
    return ('eq', a, b)


FORMULAS = [
    ('top',), ('bottom',), ('or', ()), ('and', ()),
    ('exists', 4, eq(4, 0)),
    ('exists', 4, ('and', (eq(4, 1), eq(4, 2)))),
    ('or', tuple(eq(i, j) for i in range(TERMS) for j in range(TERMS))),
    ('and', (('or', (eq(1, 0), eq(1, 2))),
             ('exists', 4, ('or', (eq(4, 3), eq(4, 0)))))),
    ('exists', 4, ('exists', 5, ('and', (eq(4, 1), eq(5, 4), eq(5, 2))))),
]
FORMULAS += [eq(i, j) for i in range(TERMS) for j in range(TERMS)]


def truth(formula, env, domain):
    kind = formula[0]
    if kind == 'top': return True
    if kind == 'bottom': return False
    if kind == 'eq': return env[formula[1]] == env[formula[2]]
    if kind == 'and': return all(truth(f, env, domain) for f in formula[1])
    if kind == 'or': return any(truth(f, env, domain) for f in formula[1])
    if kind == 'exists':
        return any(truth(formula[2], env | {formula[1]: q}, domain)
                   for q in domain)
    raise ValueError(kind)


def extract(formula, env_terms, reps, domain):
    """Certificate records term equality, selected disjunct, and witness term."""
    kind = formula[0]
    if kind == 'top': return ('top',)
    if kind == 'bottom': return None
    if kind == 'eq':
        a, b = env_terms[formula[1]], env_terms[formula[2]]
        return ('eq', a, b) if reps[a] == reps[b] else None
    if kind == 'and':
        children = tuple(extract(f, env_terms, reps, domain) for f in formula[1])
        return ('and', children) if all(p is not None for p in children) else None
    if kind == 'or':
        for index, f in enumerate(formula[1]):
            child = extract(f, env_terms, reps, domain)
            if child is not None: return ('or', index, child)
        return None
    if kind == 'exists':
        for representative in domain:
            extended = env_terms | {formula[1]: representative}
            child = extract(formula[2], extended, reps, domain)
            if child is not None: return ('exists', representative, child)
        return None
    raise ValueError(kind)


def verify_certificate(formula, certificate, env_terms, valuation):
    kind = formula[0]
    assert certificate[0] == kind
    if kind == 'top': return
    if kind == 'eq':
        a, b = env_terms[formula[1]], env_terms[formula[2]]
        assert certificate[1:] == (a, b)
        assert valuation[a] == valuation[b]
        return
    if kind == 'and':
        assert len(formula[1]) == len(certificate[1])
        for child, proof in zip(formula[1], certificate[1]):
            verify_certificate(child, proof, env_terms, valuation)
        return
    if kind == 'or':
        verify_certificate(formula[1][certificate[1]], certificate[2], env_terms, valuation)
        return
    if kind == 'exists':
        witness_term = certificate[1]
        assert 0 <= witness_term < TERMS
        verify_certificate(formula[2], certificate[2],
                           env_terms | {formula[1]: witness_term}, valuation)
        return
    raise AssertionError('No falsity certificate is possible')


def main():
    certificates = semantic_checks = presentations = 0
    for flags in itertools.product((False, True), repeat=len(PAIRS)):
        equations = [pair for pair, use in zip(PAIRS, flags) if use]
        reps, domain = quotient(equations)
        qenv = dict(enumerate(reps))
        tenv = dict(enumerate(range(TERMS)))
        for formula in FORMULAS:
            certificate = extract(formula, tenv, reps, domain)
            assert (certificate is not None) == truth(formula, qenv, domain)
            if certificate is None: continue
            certificates += 1
            for size in range(1, TERMS + 1):
                for tail in itertools.product(range(size), repeat=TERMS - 1):
                    valuation = (0,) + tail
                    if not all(valuation[a] == valuation[b] for a, b in equations): continue
                    verify_certificate(formula, certificate, tenv, valuation)
                    assert truth(formula, dict(enumerate(valuation)), range(size))
                    semantic_checks += 1
        presentations += 1
    result = {'status': 'PASS', 'finite_only': True,
              'equality_presentations': presentations,
              'formula_templates': len(FORMULAS),
              'extracted_certificates': certificates,
              'certificate_checks_on_models': semantic_checks}
    Path(__file__).with_name('independent_witness_results.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
