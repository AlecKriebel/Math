"""Directly compare the classical failed-clause union with allowed banks.

This is a successor diagnostic.  The earlier completed checker and outputs are
left byte-for-byte intact.  No submitted or sibling program is imported.
"""
import hashlib
import itertools
import json
import math
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def earlier_union(k, formula, primes):
    # The literal Stockmeyer--Meyer construction: invalid variable codes,
    # together with the ONE Boolean falsifying residue for each clause.
    invalid = any(k % p not in (0, 1) for p in primes)
    failed = any(all(k % primes[abs(lit) - 1] == int(lit < 0)
                     for lit in clause) for clause in formula)
    return invalid or failed


def allowed_cycles(formula, primes):
    cycles = [(p, {0, 1}) for p in primes]
    for clause in formula:
        ids = sorted({abs(lit) - 1 for lit in clause})
        modulus = math.prod(primes[i] for i in ids)
        allowed = set()
        # Build from satisfying Boolean assignments, then locate their CRT
        # representative by a bounded local scan.  This is independent of
        # the direct failed-residue implementation above.
        for bits in itertools.product((0, 1), repeat=len(ids)):
            assignment = dict(zip(ids, bits))
            if any(bool(assignment[abs(lit) - 1]) == (lit > 0)
                   for lit in clause):
                hits = [r for r in range(modulus)
                        if all(r % primes[i] == assignment[i] for i in ids)]
                need(len(hits) == 1, 'local CRT representative not unique')
                allowed.add(hits[0])
        cycles.append((modulus, allowed))
    return cycles


def run():
    primes = (3, 5, 7)
    triples = [tuple(s * (i + 1) for i, s in enumerate(signs))
               for signs in itertools.product((-1, 1), repeat=3)]
    formulas = [[c for i, c in enumerate(triples) if flags >> i & 1]
                for flags in range(256)]
    short = [tuple(s * (i + 1) for i, s in zip(ids, signs))
             for length in (1, 2)
             for ids in itertools.combinations(range(3), length)
             for signs in itertools.product((-1, 1), repeat=length)]
    formulas += [[c] for c in short]
    formulas += [[(1,), (-1,)], [(1,), (-1, 2), (-2, 3)],
                 [(-1,), (1, 2), (-2, -3)], [(1, 2), (-1, -2)]]
    total = 0
    digest = hashlib.sha256()
    nonboolean_clause_complement_examples = []
    for formula in formulas:
        cycles = allowed_cycles(formula, primes)
        satisfactory = []
        for k in range(math.prod(primes)):
            union = earlier_union(k, formula, primes)
            banks = all(k % q in allowed for q, allowed in cycles)
            need(union != banks, 'classical union is not bank complement')
            if banks:
                satisfactory.append(k)
            total += 1
            digest.update(bytes((int(union), int(banks))))
        direct_sat = any(all(any(bool(bits[abs(lit) - 1]) == (lit > 0)
                                    for lit in clause) for clause in formula)
                         for bits in itertools.product((0, 1), repeat=3))
        need(bool(satisfactory) == direct_sat, 'full CRT/SAT existential mismatch')
    # Local clause complements need not equal the one failed Boolean residue:
    # extra non-Boolean residues are already in the variable-invalid union.
    clause = ((1, 2, 3),)
    q, allowed = allowed_cycles(clause, primes)[-1]
    for k in range(q):
        local_complement = k not in allowed
        one_failed_boolean = all(k % p == 0 for p in primes)
        if local_complement and not one_failed_boolean:
            need(any(k % p not in (0, 1) for p in primes),
                 'extra clause-complement residue not variable-invalid')
            nonboolean_clause_complement_examples.append(k)
    need(nonboolean_clause_complement_examples, 'expected genuine local distinction')
    faults = []
    for name, damaged, expected in (
            ('union replaced by intersection',
             all(3 % p not in (0, 1) for p in primes),
             earlier_union(3, (), primes)),
            ('satisfying literal used as failed residue',
             any(1 % p not in (0, 1) for p in primes) or 1 % primes[0] == 1,
             earlier_union(1, ((1,),), primes))):
        try:
            need(damaged == expected, 'literal classical-union mismatch')
        except ValueError:
            faults.append(name)
        else:
            raise ValueError('damaged classical-union implication survived')
    return {'status': 'PASS_LITERAL_CLASSICAL_UNION_COMPARISON',
            'formula_cases': len(formulas), 'residue_positions': total,
            'union_complement_digest': digest.hexdigest(),
            'extra_nonboolean_clause_complement_count': len(nonboolean_clause_complement_examples),
            'first_extra_residues': nonboolean_clause_complement_examples[:8],
            'damaged_implications_rejected': faults,
            'scope': 'Exact finite comparison only. The universal proof and qualification are in the priority derivations.'}


if __name__ == '__main__':
    if '--self-test-invalid' in sys.argv:
        need(False, 'unconditional invalid successor control')
    print(json.dumps(run(), indent=2, sort_keys=True))
