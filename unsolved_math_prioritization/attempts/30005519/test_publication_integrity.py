#!/usr/bin/env python3
"""Negative controls for exact inventory, frozen bytes, and queue verification."""
from pathlib import Path
import importlib.util
import json
import shutil
import sys
import tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publication_verifier', ROOT / 'verify_publication.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def rejected(action, message):
    try:
        action()
    except (RuntimeError, FileNotFoundError, ValueError):
        return
    raise RuntimeError('Negative control accepted: ' + message)


v.verify(ROOT)
with tempfile.TemporaryDirectory(prefix='symmetric-publication-controls-') as td:
    temp = Path(td)
    cases = ['changed_file', 'missing_file', 'extra_file', 'changed_archive']
    for label in cases:
        root = temp / label
        shutil.copytree(ROOT, root)
        if label == 'changed_file':
            p = root / 'author/PROOF.md'
            p.write_bytes(p.read_bytes() + b'\nmutation\n')
        elif label == 'missing_file':
            (root / 'audit/CORRECTIONS.md').unlink()
        elif label == 'extra_file':
            (root / 'unexpected.txt').write_text('unmanifested')
        else:
            p = next((root / 'frozen_archives').glob('*AUTHOR*.zip'))
            b = bytearray(p.read_bytes()); b[100] ^= 1; p.write_bytes(b)
        rejected(lambda: v.verify(root), label)
    # A small synthetic queue tests isolation without embedding the actual queue.
    qroot = temp / 'synthetic_queue'; qroot.mkdir()
    old = b'| 799 | 30005519 / OWR-13750332-001 | target | 0.1 | 5.5 | 3 | 2023 | queued | 0/5 |  |  |  |\n'
    c = old.decode().rstrip('\n').split('|')
    before = list(c); c[8] = ' already_solved '; c[9] = ' 1/5 '; c[11] = ' qualified prior PASS '
    new = ('|'.join(c) + '\n').encode()
    base = b'pre-existing header\n' + old + b'untouched tail\n'
    updated = b'pre-existing header\n' + new + b'untouched tail\n'
    d = {'base': v.identity(base), 'updated': v.identity(updated), 'row_line_1_based': 2,
         'changes': [{'column': n, 'old': before[j].strip(), 'new': c[j].strip()}
                     for j, n in [(8, 'Status'), (9, 'Turns'), (11, 'Findings')]]}
    bp, up = temp / 'base.md', temp / 'updated.md'; bp.write_bytes(base); up.write_bytes(updated)
    (qroot / 'QUEUE_DELTA.json').write_text(json.dumps(d))
    v.verify_queue(qroot, bp, up)
    changed = updated.replace(b'untouched tail', b'edited tail')
    up.write_bytes(changed); d['updated'] = v.identity(changed)
    (qroot / 'QUEUE_DELTA.json').write_text(json.dumps(d))
    rejected(lambda: v.verify_queue(qroot, bp, up), 'unrelated queue edit with updated hash')
print(json.dumps({'status': 'PASS', 'negative_controls': 5,
                  'payload_mutations_rejected': 4, 'unrelated_queue_edit_rejected': True}, sort_keys=True))
