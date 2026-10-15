#!/usr/bin/env python3
"""Byte-bind all genuine exposed peer payloads and every original Git blob."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bind(path, kind):
    require(path.is_file() and not path.is_symlink(), 'Missing or indirect input '+str(path))
    data = path.read_bytes()
    return {'path': str(path.relative_to(CASE)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'kind': kind}


records = []
peer_counts = []
for family in ['geometry_scope', 'spectral_adversary', 'reproduction']:
    folder = CASE/'reviews'/family
    manifest_path = folder/'PUBLIC_FILES.json'
    manifest = json.loads(manifest_path.read_text())
    require(manifest['pr'] == 445 and str(manifest['problem_id']) == '30002737' and
            manifest['frozen_head'] == HEAD, 'Peer identity mismatch')
    records.append(bind(manifest_path, 'completed_peer_manifest'))
    for entry in manifest['files']:
        rel = entry.get('review_relative_path', entry['path'])
        require(not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'Unsafe peer path')
        path = folder/rel
        row = bind(path, 'completed_peer_payload')
        require(row['bytes'] == entry['bytes'] and row['sha256'] == entry['sha256'], 'Peer seal changed '+str(path))
        records.append(row)
    result = json.loads((folder/'RESULT.json').read_text())
    for field in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']:
        require(type(result[field]) is int, 'Peer count is not an integer')
    peer_counts.append({'family': family, 'payloads': len(manifest['files']),
                        **{field: result[field] for field in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']}})

for name in ['ROOT_MATHEMATICAL_RECONSTRUCTION.md', 'ROOT_SOURCE_READBACK.json',
             'ROOT_PRIMARY_SOURCE_RECEIPT.json', 'SOURCE_RECEIPT.json']:
    records.append(bind(CASE/name, 'authorized_root_input'))

receipt = json.loads((CASE/'SOURCE_RECEIPT.json').read_text())
require(receipt['head_sha'] == HEAD, 'Original receipt wrong head')
for entry in receipt['files']:
    path = CASE/'source_snapshot'/entry['path']
    row = bind(path, 'original_frozen_candidate')
    require(row['bytes'] == entry['bytes'] and row['sha256'] == entry['sha256'], 'Source receipt mismatch')
    git = subprocess.run(['git', 'show', HEAD+':'+entry['path']], capture_output=True)
    require(git.returncode == 0, 'Git original missing: '+git.stderr.decode(errors='replace'))
    require(git.stdout == path.read_bytes(), 'Original differs from frozen Git object')
    row['exact_frozen_git_match'] = True
    records.append(row)

initial = json.loads((HERE/'INITIAL_BINDINGS.json').read_text())
for entry in initial['records']:
    path = Path(entry['path'])
    data = path.read_bytes()
    require(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], 'Independent initial input changed')
initial_doc = bind(HERE/'INITIAL_RECONSTRUCTION.md', 'independent_initial_checkpoint')
require(initial_doc['sha256'] == '630b044983db4deb7a695037ce1ed49d2a193498cded21cf345b9054c95e3fa4', 'Initial reconstruction changed')
records.append(initial_doc)
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'pr': 445, 'problem_id': 30002737, 'frozen_head': HEAD,
          'reviewer': '/root/pr445_whole_math_adversary',
          'all_genuine_peer_manifests_verified': True, 'entire_peer_payloads_loaded_and_interpreted': True,
          'initial_input_records_unchanged': len(initial['records']),
          'all_originals_match_git': len(receipt['files']), 'peer_counts': peer_counts, 'records': records}
(HERE/'INPUT_BINDINGS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'peer_counts': peer_counts, 'bound_records': len(records), 'originals': len(receipt['files'])}, indent=2))
