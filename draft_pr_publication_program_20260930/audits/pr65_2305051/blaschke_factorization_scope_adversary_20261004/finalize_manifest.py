#!/usr/bin/env python3
"""Validate receipts and frozen inputs, then manifest the completed audit."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent
START = datetime.datetime.now(datetime.timezone.utc).isoformat()
auth = json.loads((BASE / 'AUTHENTICATED_INPUTS.json').read_text())
source = BASE.parent / 'original_source_authentication_20261004' / 'original'
for entry in auth['artifacts']:
    body = (source / entry['path']).read_bytes()
    assert hashlib.sha256(body).hexdigest() == entry['sha256']
    assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == entry['git_blob_expected']
records = [json.loads(line) for line in (BASE / 'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
for record in records:
    assert record['returncode'] == 0
    for stream in ('stdout', 'stderr'):
        assert hashlib.sha256((BASE / record[stream + '_path']).read_bytes()).hexdigest() == record[stream + '_sha256']
controls = json.loads((BASE / 'EXACT_CONTROL_RESULTS.json').read_text())
assert controls['status'] == 'PASS' and controls['exact_assertions'] == 4534
assert controls['script_sha256'] == hashlib.sha256((BASE / 'exact_factorization_controls.py').read_bytes()).hexdigest()
verdict = json.loads((BASE / 'VERDICT.json').read_text())
assert verdict['immutable_head'] == auth['head'] == '5cc1602c05d79502defb07cec7027963149494d2'
assert verdict['original_substantive_attempts'].startswith('2/5 unchanged')
assert verdict['essential_gaps'] == [] and verdict['mandatory_corrections'] == []
execution = {
    'actual_process_argv': [sys.executable, *sys.argv],
    'cwd': str(Path.cwd()),
    'started_utc': START,
    'validated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checks': {'original_bodies_unchanged': len(auth['artifacts']),
               'captured_command_receipts_and_stream_hashes': len(records),
               'bounded_exact_controls': controls['exact_assertions']},
    'result': 'PASS',
    'note': 'Final manifest generation is recorded here rather than through the stream recorder, '
            'so all completed stream sidecars can be included in the manifest.',
}
(BASE / 'FINAL_MANIFEST_EXECUTION.json').write_text(json.dumps(execution, indent=2) + '\n')
artifacts = []
for path in sorted(BASE.rglob('*')):
    if not path.is_file() or path.name == 'SELF_MANIFEST.json':
        continue
    data = path.read_bytes()
    artifacts.append({'path': str(path.relative_to(BASE)), 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(),
                      'mode': oct(path.stat().st_mode & 0o777)})
manifest = {
    'immutable_head': auth['head'],
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Completed assigned-family audit; includes all files under this audit directory except this manifest itself.',
    'artifact_count': len(artifacts),
    'artifacts': artifacts,
}
(BASE / 'SELF_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'result': 'PASS', 'manifest_artifacts': len(artifacts),
                  'unchanged_original_bodies': len(auth['artifacts']),
                  'captured_commands': len(records)}, indent=2))
