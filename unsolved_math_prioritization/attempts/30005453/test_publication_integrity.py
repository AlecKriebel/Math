#!/usr/bin/env python3
"""Negative controls for the portable publication and exact three-cell queue patch."""
from pathlib import Path
import importlib.util, json, shutil, sys, tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publication_verifier', ROOT / 'verify_publication.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def rejected(action, name):
    try:
        action()
    except (ValueError, FileNotFoundError, KeyError):
        return
    raise RuntimeError('Negative control accepted: ' + name)


v.verify(ROOT)
with tempfile.TemporaryDirectory(prefix='reinforcement-publication-controls-') as td:
    temp = Path(td)
    cases = ('changed_proof', 'missing_file', 'extra_file', 'changed_zip', 'symlink', 'extra_directory')
    for label in cases:
        root = temp / label
        shutil.copytree(ROOT, root)
        if label == 'changed_proof':
            p = root / 'author_v2/PROOF.md'; p.write_bytes(p.read_bytes() + b'changed\n')
        elif label == 'missing_file':
            (root / 'v2_acceptance/REPORT.md').unlink()
        elif label == 'extra_file':
            (root / 'source.pdf').write_bytes(b'%PDF-')
        elif label == 'changed_zip':
            p = next((root / 'frozen_archives').glob('*V2_PROPOSED*.zip'))
            b = bytearray(p.read_bytes()); b[100] ^= 1; p.write_bytes(b)
        elif label == 'symlink':
            p = root / 'author_v2/README.md'; p.unlink(); p.symlink_to('../README.md')
        else:
            (root / 'unlisted_directory').mkdir()
        rejected(lambda: v.verify(root), label)
    qroot = temp / 'queue'; qroot.mkdir()
    old = b'| 798 | 30005453 / OWR-12697708-006 | title | 0.1 | 5.5 | 3 | 2023 | queued | 0/5 |  |  |  |\n'
    c = old.decode().rstrip('\n').split('|'); before = c[:]
    c[8] = ' claimed_solved '; c[9] = ' 4/5 '; c[11] = ' qualified corrected theorem '
    base = b'stale header\n' + old + b'untouched tail\n'
    updated = b'stale header\n' + ('|'.join(c)+'\n').encode() + b'untouched tail\n'
    bp, up = temp/'base.md', temp/'updated.md'; bp.write_bytes(base); up.write_bytes(updated)
    record = {'base': v.identity(base), 'updated': v.identity(updated), 'row_line_1_based': 2,
              'changes': [{'column': n, 'old': before[j].strip(), 'new': c[j].strip()}
                          for j, n in ((8, 'Status'), (9, 'Turns'), (11, 'Findings'))]}
    rp = qroot / 'QUEUE_DELTA.json'; rp.write_text(json.dumps(record))
    v.verify_queue(qroot, bp, up)
    mutated = updated.replace(b'untouched tail', b'changed tail')
    up.write_bytes(mutated); record['updated'] = v.identity(mutated); rp.write_text(json.dumps(record))
    rejected(lambda: v.verify_queue(qroot, bp, up), 'unrelated queue edit with updated hash')
    mutated = updated.replace(b'| 0.1 |', b'| 0.2 |')
    up.write_bytes(mutated); record['updated'] = v.identity(mutated); rp.write_text(json.dumps(record))
    rejected(lambda: v.verify_queue(qroot, bp, up), 'fourth queue cell edit with updated hash')
print(json.dumps({'status': 'PASS', 'negative_controls': 8,
                  'payload_mutations_rejected': 6, 'unauthorized_queue_edits_rejected': 2}, sort_keys=True))
