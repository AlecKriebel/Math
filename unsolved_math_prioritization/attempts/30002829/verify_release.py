#!/usr/bin/env python3
"""Read-only release integrity and exact-result replay; not a proof certificate."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise SystemExit('Assertions must be active: remove -O/-OO and PYTHONOPTIMIZE.')

BASE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

manifest_bytes = (BASE / 'MANIFEST.json').read_bytes()
manifest = json.loads(manifest_bytes)
require((BASE / 'MANIFEST.sha256').read_text().strip() == digest(manifest_bytes) + '  MANIFEST.json', 'release manifest binding')
entries = manifest['allowlisted_files']
names = [entry['path'] for entry in entries]
require(len(names) == len(set(names)), 'duplicate manifest paths')
require(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names), 'unsafe manifest paths')
paths = list(BASE.rglob('*'))
require(not any(p.is_symlink() for p in paths), 'symlinks forbidden')
actual = {p.relative_to(BASE).as_posix() for p in paths if p.is_file()}
require(actual == set(names) | {'MANIFEST.json', 'MANIFEST.sha256'}, 'release file allowlist mismatch')
require({p.relative_to(BASE).as_posix() for p in paths if p.is_dir()} == {'author', 'audit'}, 'release directory allowlist mismatch')
for entry in entries:
    data = (BASE / entry['path']).read_bytes()
    require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'payload mismatch: ' + entry['path'])

for folder, expected in [('author', '42c019f66712f8ebf980f3da6033cf83448c8ffa79aff937f520bccb029c29d6'), ('audit', '0ce6bdd25d64464a0cd980e3ae5b87cba37e050ad945f26278bb1bd0e7ed1f15')]:
    root = BASE / folder
    raw = (root / 'MANIFEST.json').read_bytes()
    require(digest(raw) == expected, folder + ' frozen manifest changed')
    for entry in json.loads(raw)['allowlisted_files']:
        data = (root / entry['path']).read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], folder + ' frozen payload changed')

require(digest((BASE / 'audit/CONTROLLING_CORRECTIONS.md').read_bytes()) == '14977e85f6d8ef8dff6316045d116d1da9ebf6845a5b657c10278b09e98b399a', 'controlling corrections changed')
status = read_json(BASE / 'release_status.json')
require(status['status'] == 'unsolved' and status['turns'] == '5/5', 'target disposition')
require(status['authoritative_corrections'] == 'audit/CONTROLLING_CORRECTIONS.md', 'correction authority')
require(status['relative_obstructions_only'], 'relative scope')
for key in ['old_model_side_open_sufficient', 'full_unsaturated_fivefold_intersection_integral', 'fourfold_rationality_resolved', 'fivefold_unirationality_resolved', 'fivefold_rationality_resolved', 'novelty_claim', 'global_current_openness_claim']:
    require(status[key] is False, 'invalid claim: ' + key)
neighbor = status['neighbor_30002830']
require(neighbor['coverage'] == 'partial_method_specific_overlap' and neighbor['attempt_budget_consumed'] == 0 and neighbor['row_changed'] is False, 'neighbor scope')

env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
run = subprocess.run([sys.executable, '-B', str(BASE / 'audit/replay_audit.py'), '--original-safe', str(BASE / 'author')], cwd=BASE, env=env, capture_output=True, text=True)
require(run.returncode == 0, 'audit replay failed: ' + run.stderr)
require(not run.stderr, 'unexpected audit stderr')
replay = json.loads(run.stdout)
require(replay['status'] == 'passed' and replay['original_packet_reverified'] and replay['independent_checks'] == 115 and replay['negative_controls'] == 11, 'audit replay result')
require(read_json(BASE / 'author/verification_results.json')['check_count'] == 32, 'author check count')
print(json.dumps({'status': 'passed', 'release_manifest_sha256': digest(manifest_bytes), 'release_payload_count': len(entries), 'author_checks': 32, 'independent_checks': 115, 'negative_controls_included': 11, 'original_packets_preserved': True, 'controlling_corrections_bound': True, 'assertions_active': True, 'writes_performed': False, 'scope': 'Corrected partial results only; exact original targets unresolved.'}, indent=2))
