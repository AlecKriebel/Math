#!/usr/bin/env python3
"""Report only intended guard failures from two fixed actual-source mutations."""
import json
import pathlib
import sys

MUTATIONS = {
    'missing_parameter_shift': (
        'meprime = [[one, ba(e, ee)], [one, one]]',
        'meprime = [[one, e], [one, one]]'),
    'fixed_ring_identity': (
        'return (a[0], a[1], a[1] ^ a[2])', 'return a'),
}


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise ValueError('-I -S -B required')
    if len(sys.argv) != 2 or sys.argv[1] not in ['none', *MUTATIONS]:
        raise ValueError('exact intended case required')
    mutant = sys.argv[1]
    source = (pathlib.Path(__file__).resolve().parent /
              'verify_functor_identities_explicit_guards.py').read_text()
    if mutant != 'none':
        before, after = MUTATIONS[mutant]
        if source.count(before) != 1:
            raise ValueError('mutation anchor is not unique')
        source = source.replace(before, after, 1)
    try:
        exec(compile(source, '<independent-guard-adaptation>', 'exec'),
             {'__name__': '__main__'})
    except RuntimeError as error:
        print(json.dumps({'ok': False, 'mutant': mutant, 'failure': str(error)},
                         sort_keys=True))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
