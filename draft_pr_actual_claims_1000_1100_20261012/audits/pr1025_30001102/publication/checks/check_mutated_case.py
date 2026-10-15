#!/usr/bin/env python3
"""Report intended failures of five actual independently validated source faults."""
import json
import pathlib
import sys


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise ValueError('-I -S -B required')
    here = pathlib.Path(__file__).resolve().parent
    mutations = json.loads((here / 'SOURCE_MUTATIONS.json').read_text())
    if len(sys.argv) != 2 or sys.argv[1] not in mutations:
        raise ValueError('exact fixed mutation required')
    label = sys.argv[1]
    row = mutations[label]
    source = (here / 'independent_exact_check.py').read_text()
    if source.count(row['before']) != 1:
        raise ValueError('source mutation anchor not unique')
    source = source.replace(row['before'], row['after'], 1)
    try:
        exec(compile(source, '<independent-actual-source-fault>', 'exec'),
             {'__name__': '__main__'})
    except RuntimeError as error:
        print(json.dumps({'status': 'INTENDED_REJECTION', 'mutation': label,
                          'reason': str(error)}, sort_keys=True))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
