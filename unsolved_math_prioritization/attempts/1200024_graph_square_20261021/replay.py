"""Fail-closed frozen inventory, followed by offline exact replay. Stdlib only."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import stat
import sys

BASE = Path(__file__).resolve().parent
# Frozen inventory is inspected without opening any payload or manifest content.
NAMES = {'RESULT.md', 'grandparent_proof.md', 'grandparent_exact_resistance.md',
         'SQUARE_BOUND.md', 'square_flow_certificate.json.gz', 'verify_square_certificate.py',
         'operator_notes.md', 'unimodular_projection_comparison.md', 'independent_replay.py',
         'check_finite_reductions.py', 'ADVERSARIAL_REVIEW.md', 'PROJECTION.md',
         'CODE_PROVENANCE.json', 'AST_PROVENANCE.json', 'mutation_checks.py', 'replay.py',
         'MANIFEST.json'}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def no_sockets(event, args):
    if event.startswith('socket.'):
        raise PermissionError('network forbidden in frozen replay')

sys.addaudithook(no_sockets)
sys.dont_write_bytecode = True
entries = list(os.scandir(BASE))
need({e.name for e in entries} == NAMES, 'inventory mismatch before payload content read')
need(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries), 'nonregular inventory entry')
manifest = json.loads((BASE / 'MANIFEST.json').read_text())
need(set(manifest['files']) == NAMES - {'MANIFEST.json'}, 'manifest inventory mismatch')
for filename, record in manifest['files'].items():
    raw = (BASE / filename).read_bytes()
    need(len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], 'hash mismatch: ' + filename)

if '--inventory-only' in sys.argv:
    print(json.dumps({'verdict': 'PASS', 'inventory_files': len(NAMES), 'payload_hashes': len(manifest['files'])}))
else:
    reports = {}
    for filename in ('verify_square_certificate.py', 'independent_replay.py', 'check_finite_reductions.py', 'mutation_checks.py'):
        previous = sys.argv
        output = io.StringIO()
        try:
            sys.argv = [str(BASE / filename), str(BASE / 'square_flow_certificate.json.gz')]
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(BASE / filename), run_name='__main__')
        finally:
            sys.argv = previous
        report = json.loads(output.getvalue())
        need(report['verdict'] == 'PASS', filename + ' failed')
        reports[filename] = report
    print(json.dumps({'verdict': 'PASS', 'optimized': sys.flags.optimize, 'inventory_files': len(NAMES), 'socket_events_denied': True, 'reports': reports}, indent=2))
