"""In-memory source mutations must fail the independent endpoint oracle.

Reads the immutable packet, never edits its files, and uses explicit exceptions
under normal Python, -O, and -OO. No new mathematical search is performed.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import os
import sys
import types

sys.dont_write_bytecode = True
import independent_exact_audit as audit


def run():
    source = (audit.PACKET / 'tests/exact_model.py').read_text()
    original = audit.author
    e4 = tuple(combinations(range(4), 2))
    fixtures = {
        'star': (4, e4, [3]*6, 6, (0, 1, 2), Q(3, 2)),
        'parallel': (2, ((0, 1), (0, 1), (1, 1)), [2, 3, 0], 5, (0,), Q(2)),
        'zero': (4, e4, [4, 4, 4, 0, 0, 0], 4, (0, 3, 5), Q(0)),
        'rank_zero': (1, ((0, 0),), [0], 7, (), Q(7)),
    }
    for args in fixtures.values():
        audit.certify_endpoint(*args)
    mutations = [
        ('drop_subset_facets', '        if d > 0:', '        if d < 0:', 'star'),
        ('round_down_rational_endpoint', '    return min(bounds)',
         '    v, why = min(bounds)\n    return (Fraction(v.numerator // v.denominator), why)', 'star'),
        ('drop_selected_coordinate_bounds',
         "    bounds += [(Fraction(w[i]), ('edge', i)) for i in tree]", '    bounds += []', 'parallel'),
        ('drop_nonnegative_mass_endpoint', "    bounds = [(Fraction(k), ('mass',))]", '    bounds = []', 'rank_zero'),
        ('replace_zero_by_positive_endpoint', '    return min(bounds)',
         "    return (Fraction(1), ('mutated_zero',)) if min(bounds)[0] == 0 else min(bounds)", 'zero'),
    ]
    killed = []
    for name, old, new, fixture in mutations:
        audit.need(source.count(old) == 1, 'mutation target must be unique: ' + name)
        module = types.ModuleType('mutant_' + name)
        exec(compile(source.replace(old, new), '<in-memory-' + name + '>', 'exec'), module.__dict__)
        audit.author = module
        try:
            audit.certify_endpoint(*fixtures[fixture])
        except (RuntimeError, ValueError) as exc:
            killed.append({'mutant': name, 'rejected': True, 'exception': type(exc).__name__, 'diagnostic': str(exc)})
        else:
            raise RuntimeError('source mutant survived: ' + name)
        finally:
            audit.author = original
    return {'passed': True, 'uid': os.getuid(), 'euid': os.geteuid(),
            'optimization': sys.flags.optimize, 'source_mutants_rejected': killed,
            'source_files_written': False, 'new_research_approaches': 0}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
