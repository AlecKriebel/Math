#!/usr/bin/env python3
"""Read-only execution of the reviewed root candidate function and controls."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
path = HERE.parent / 'repair_queue.py'
spec = importlib.util.spec_from_file_location('reviewed_root_candidate', path)
root = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root)
before = (HERE / 'INITIAL_QUEUE_cab3546c2.md').read_bytes()
expected = (HERE.parent / 'QUEUE_CANDIDATE.md').read_bytes()
after, changes, names = root.candidate(before)
assert after == expected
lines, columns, rows = root.parse(before)


def mutate(identity, field, value):
    revised = lines.copy()
    n, cells = rows[identity]
    cells = cells.copy()
    cells[1 + columns.index(field)] = ' ' + value + ' '
    revised[n] = '|'.join(cells) + ('\n' if revised[n].endswith('\n') else '')
    return ''.join(revised).encode()


fixtures = [
    ('genuine Chat URL cannot be moved', mutate(root.IDS[0], 'Chat', 'https://chatgpt.com/c/actual-link')),
    ('occupied Findings cannot be overwritten', mutate(root.IDS[0], 'Findings', 'prior accepted finding')),
    ('duplicated selected wellformed identity', before + lines[rows[root.IDS[0]][0]].encode()),
    ('duplicated literal header', before + next(x for x in lines if x.startswith('| Rank | ID / code |')).encode()),
    ('missing selected identity', before.replace(b'10000062 / AMR-099-0062', b'99999001 / AMR-099-0062')),
]
out = []
for label, data in fixtures:
    try:
        root.candidate(data)
    except (AssertionError, KeyError) as error:
        out.append({'label': label, 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Negative control accepted: ' + label)
print(json.dumps({'verdict': 'PASS', 'candidate_sha256': hashlib.sha256(after).hexdigest(),
                  'exact_candidate_reproduced': True, 'actual_root_function_controls': out,
                  'shared_files_written': 0}, indent=2))
