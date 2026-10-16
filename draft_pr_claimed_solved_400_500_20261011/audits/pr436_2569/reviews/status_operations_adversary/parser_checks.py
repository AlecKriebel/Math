#!/usr/bin/env python3
"""Frozen selected-row parser tests only; no API invocation or proof reads."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import sys

CASE = Path(__file__).resolve().parents[2]
PRIVATE = CASE / 'private_sources/status_operations_adversary'
SOURCE = CASE / 'status_operation.py'
spec = importlib.util.spec_from_file_location('frozen_parser', SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
original = (CASE / 'private_sources/status_operation/QUEUE.before.md').read_bytes()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

checks = []
changed, newrow = m.replace_status(original)
before, after = original.splitlines(keepends=True), changed.splitlines(keepends=True)
different = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
require(len(before) == len(after) and len(different) == 1, 'changed more than one line')
oldline, newline = before[different[0]], after[different[0]]
oldcells, newcells = oldline.split(b'|'), newline.split(b'|')
require(len(oldcells) == len(newcells), 'column count changed')
require([i for i,(a,b) in enumerate(zip(oldcells,newcells)) if a != b] == [8], 'not exact Status field')
require(oldcells[9] == newcells[9] == b' 5/5 ', '5/5 changed')
require(changed == original.replace(oldline, newline, 1), 'other bytes changed')
require(hashlib.sha256(changed).hexdigest() == 'e50d06e91a26966ad942acf7cf8ed6b3545cf0cdc69d1d76ec6f51559410d1d6', 'wrong planned payload')
checks.append('frozen real QUEUE: one exact Status field, 5/5, every other byte preserved')

synthetic = b'| Status | ID / code | Turns |\n| claimed_solved | 2569 / KOU-21.60 | 5/5 |\n'
require(m.selected_row(synthetic)[3] == 0, 'header index ignored')
checks.append('reordered synthetic header selects status at column zero')
for name, data in [
 ('duplicate exact target', original + oldline),
 ('missing target', b'| Status | ID / code |\n'),
 ('target author turns changed', original.replace(oldline, oldline.replace(b'5/5',b'5/4'),1)),
 ('target status changed', original.replace(oldline, oldline.replace(b'claimed_solved',b'in_progress'),1)),
 ('target display field changed', original.replace(oldline,oldline.replace(b'0.1275',b'0.1276'),1)),
 ('missing header', m.EXPECTED_ROW.encode()+b'\n'),
]:
    try:
        m.replace_status(data)
    except RuntimeError:
        checks.append(name + ' fails closed')
    else:
        raise RuntimeError(name + ' accepted')

result={'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'queue_sha256':hashlib.sha256(original).hexdigest(),'new_queue_sha256':hashlib.sha256(changed).hexdigest(),
        'python_optimization':sys.flags.optimize,'checks':checks,'check_count':len(checks),
        'network_calls':0,'real_mutation_calls':0,'new_proof_attempts':0,'verdict':'PASS'}
out=PRIVATE/('parser_results_O.json' if sys.flags.optimize else 'parser_results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
