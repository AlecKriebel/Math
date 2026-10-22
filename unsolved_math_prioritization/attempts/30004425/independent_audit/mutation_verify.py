#!/usr/bin/env python3
"""Check four deliberately corrupted copies of the frozen author's verifier.

Usage: python3 mutation_verify.py /path/to/author/safe_freeze
No source is rewritten. Each altered string runs in an isolated subprocess.
"""
from pathlib import Path
import json
import subprocess
import sys

author = Path(sys.argv[1])
source = (author / 'verify.py').read_text()
original = subprocess.run([sys.executable, '-c', source], capture_output=True)
if original.returncode or original.stdout != (author / 'VERIFICATION_RESULTS.json').read_bytes():
    raise AssertionError('Unchanged author replay does not match')
mutations = [
    ('wrong_second_matrix_sign', '(0,0,3,-1))', '(0,0,3,1))'),
    ('wrong_standard_reduction', 'v=B if which==1 else C', 'v=C if which==1 else B'),
    ('off_by_one_standard_cutoff', 'if a[1]<11', 'if a[1]<12'),
    ('wrong_flip_orientation', 'return -z+endpoints1(x)[0]+endpoints2(x)[1]', 'return z+endpoints1(x)[0]+endpoints2(x)[1]'),
]
results = []
for name, old, new in mutations:
    if source.count(old) != 1:
        raise AssertionError('Mutation target is not unique: '+name)
    result = subprocess.run([sys.executable, '-c', source.replace(old,new)], capture_output=True)
    if result.returncode == 0 or b'AssertionError' not in result.stderr:
        raise AssertionError('Expected mathematical rejection missing: '+name)
    results.append({'mutation':name,'result':'REJECTED','exit_code':result.returncode,'exception':'AssertionError'})
print(json.dumps({'result':'PASS','unmodified_author_replay':'PASS and byte-identical','mutations':results,'author_files_modified':False},indent=2))
