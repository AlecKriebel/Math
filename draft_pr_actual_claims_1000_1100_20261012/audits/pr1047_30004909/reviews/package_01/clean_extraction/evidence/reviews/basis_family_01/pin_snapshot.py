#!/usr/bin/env python3
"""Read-only input identity check; writes only inside this review directory."""
import hashlib, json, pathlib, subprocess, sys
from datetime import datetime, timezone
sys.dont_write_bytecode = True
ROOT = pathlib.Path('/Users/alec/Documents/Math')
AUDIT = ROOT / 'draft_pr_actual_claims_1000_1100_20261012/audits/pr1047_30004909'
OUT = AUDIT / 'reviews/basis_family_01'
HEAD = '56b3a35182e5cb04b05e41f5017e47caf50582c1'
PREFIX = 'unsolved_math_prioritization/attempts/30004909/'
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def git(*args, data=None):
    return subprocess.run(['git', '-C', str(ROOT), *args], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
require(pathlib.Path.cwd().resolve() == ROOT, 'unexpected cwd')
require(len(sys.argv) == 2 and sys.argv[1] in ('initial', 'final'), 'expected initial or final')
phase = sys.argv[1]
pins_bytes = (AUDIT / 'SUBMITTED_PINS.json').read_bytes()
pins = json.loads(pins_bytes)
require(pins['head_oid'] == HEAD, 'pinned commit mismatch')
require(pins['pr'] == 1047 and pins['problem_id'] == 30004909, 'unexpected target')
require(git('cat-file', '-t', HEAD).strip() == b'commit', 'head is not a commit')
require(git('rev-parse', HEAD).decode().strip() == HEAD, 'head object mismatch')
commit_bytes = git('cat-file', 'commit', HEAD)
computed_head = hashlib.sha1(b'commit ' + str(len(commit_bytes)).encode() + b'\0' + commit_bytes).hexdigest()
require(computed_head == HEAD, 'actual commit content hash differs')
tree_oid = git('rev-parse', HEAD + '^{tree}').decode().strip()
tree_bytes = git('cat-file', 'tree', tree_oid)
computed_tree = hashlib.sha1(b'tree ' + str(len(tree_bytes)).encode() + b'\0' + tree_bytes).hexdigest()
require(computed_tree == tree_oid, 'actual root tree content hash differs')
fulltree = git('ls-tree', '-r', '--full-tree', '-z', HEAD)
entries = {}
for entry in fulltree.split(b'\0'):
    if entry:
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[name.decode()] = {'mode': mode, 'kind': kind, 'oid': oid}
originals = sorted(p['repository_path'] for p in pins['files'])
require(len(originals) == 9 and len(set(originals)) == 9, 'expected nine distinct originals')
package_names = sorted(name for name in entries if name.startswith(PREFIX))
require(package_names == originals, 'fulltree package is not exactly nine pinned files')
local_names = sorted(str(p.relative_to(AUDIT)) for p in (AUDIT / 'submitted').iterdir() if p.is_file())
require(local_names == sorted(p['snapshot_path'] for p in pins['files']), 'snapshot package completeness mismatch')
rows = []
for pin in pins['files']:
    rp, sp = pin['repository_path'], pin['snapshot_path']
    require(rp.startswith(PREFIX) and sp.startswith('submitted/'), 'unexpected input path')
    payload = (AUDIT / sp).read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == pin['sha256'] and len(payload) == pin['bytes'], 'snapshot SHA-256/length mismatch: ' + sp)
    require(entries[rp]['mode'] == '100644' and entries[rp]['kind'] == 'blob', 'unexpected tree entry: ' + rp)
    object_payload = git('cat-file', 'blob', entries[rp]['oid'])
    require(payload == object_payload, 'snapshot differs from pinned actual Git blob: ' + rp)
    computed_blob = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
    require(computed_blob == entries[rp]['oid'], 'actual blob SHA-1 mismatch: ' + rp)
    rows.append({'repository_path': rp, 'snapshot_path': sp, 'bytes': len(payload), 'sha256': digest, **entries[rp]})
record = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(), 'head_oid': HEAD, 'actual_commit_object_sha1': computed_head, 'root_tree_oid': tree_oid, 'actual_root_tree_object_sha1': computed_tree, 'fulltree_sha256': hashlib.sha256(fulltree).hexdigest(), 'fulltree_entries': len(entries), 'fulltree_encoding': 'git ls-tree -r --full-tree -z', 'submitted_pins_sha256': hashlib.sha256(pins_bytes).hexdigest(), 'submitted_pins_bytes': len(pins_bytes), 'exact_package_completeness': True, 'files': rows, 'status': 'PASS'}
if phase == 'final':
    initial = json.loads((OUT / 'INPUT_PINS_INITIAL.json').read_text())
    for key in ('head_oid', 'root_tree_oid', 'fulltree_sha256', 'fulltree_entries', 'submitted_pins_sha256', 'submitted_pins_bytes', 'files'):
        require(record[key] == initial[key], 'input mutation since initial pins: ' + key)
    record['unchanged_since_initial'] = True
(OUT / ('INPUT_PINS_' + phase.upper() + '.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'phase': phase, 'utc': record['utc'], 'head_oid': HEAD, 'root_tree_oid': tree_oid, 'fulltree_entries': len(entries), 'all_nine_blob_bytes_match': True, 'submitted_pins_sha256': record['submitted_pins_sha256'], 'status': 'PASS'}, sort_keys=True))
