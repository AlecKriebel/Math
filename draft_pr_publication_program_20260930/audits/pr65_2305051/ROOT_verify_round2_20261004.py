"""Read back the completed fresh review without changing its frozen evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys
import zipfile

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A = Path(__file__).resolve().parent
S = A / 'whole_package_round2_20261004'
K = A / 'publication_package_v1'
F = A / 'ROOT_round2_review_readback_20261004'
F.mkdir(exist_ok=False)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def safe_relative(name):
    p = Path(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'Unsafe relative path')
    return p

def inventory(folder):
    result = {}
    for p in folder.rglob('*'):
        require(not p.is_symlink(), 'Symlink in evidence or package')
        if p.is_file():
            body = p.read_bytes()
            result[str(p.relative_to(folder))] = {'bytes': len(body), 'sha256': sha(body)}
    return result

manifest_body = (S / 'EVIDENCE_MANIFEST.json').read_bytes()
manifest_sha = sha(manifest_body)
require(manifest_sha == 'c702c53f4be2c697aa174d74a64694861f76f19e0923f28f8572272e0c31034d', 'Review manifest drift')
require((S / 'EVIDENCE_MANIFEST.sha256').read_text().split()[0] == manifest_sha, 'Review digest drift')
manifest = json.loads(manifest_body)
listed = {}
for row in manifest['files']:
    safe_relative(row['path'])
    require(row['path'] not in listed, 'Duplicate review member')
    listed[row['path']] = {k: row[k] for k in ('bytes', 'sha256')}
review_inventory = inventory(S)
require(len(listed) == 81, 'Unexpected review member count')
require(set(review_inventory) == set(listed) | {'EVIDENCE_MANIFEST.json', 'EVIDENCE_MANIFEST.sha256'}, 'Review inventory drift')
require(all(review_inventory[name] == row for name, row in listed.items()), 'Review file drift')

verdict = json.loads((S / 'VERDICT.json').read_bytes())
require(verdict['status'] == 'CLEAN_BOUNDED_INDEPENDENT_REVIEW_NO_REQUIRED_REPAIRS_FOUND' and verdict['required_repairs'] == [], 'Review is not clean')
require(sha((S / verdict['report']).read_bytes()) == verdict['report_sha256'] == '48766545cb01e115f6b737d0f3fc9495deb3a5e4efc9e0080301682ab4982417', 'Report pin drift')
require(sha((S / 'FIRST_CONCLUSION.json').read_bytes()) == verdict['first_conclusion_sha256'], 'First-conclusion drift')
require(verdict['immutable_science_head'] == '5cc1602c05d79502defb07cec7027963149494d2', 'Wrong immutable head')

driver_sha = sha((S / 'audit_operations.py').read_bytes())
records = []
for p in sorted((S / 'execution').glob('*/record.json')):
    row = json.loads(p.read_bytes())
    label = p.parent.name
    require(row['label'] == label and isinstance(row['pid'], int) and row['pid'] > 0 and row['driver_pid'] > 0, 'Actual process identity missing')
    require(row['driver_sha256'] == driver_sha and row['argv'] and all(isinstance(v, str) for v in row['argv']), 'Driver/argv drift')
    times = [dt.datetime.fromisoformat(row[key]) for key in ('declared_utc', 'spawn_observed_utc', 'completed_utc')]
    require(all(t.tzinfo is not None for t in times) and times == sorted(times), 'Invalid process chronology')
    require(row['exit_code'] == (1 if label == 'reject_optimized' else 0), 'Unexpected process exit')
    for stream in ('stdout', 'stderr'):
        body = (p.parent / (stream + '.bin')).read_bytes()
        require(len(body) == row[stream + '_bytes'] and sha(body) == row[stream + '_sha256'], 'Process stream drift')
    records.append({'label': label, 'pid': row['pid'], 'exit_code': row['exit_code'], 'argv': row['argv']})
require(len(records) == 7, 'Unexpected process count')
custody = json.loads((S / 'CUSTODY_RESULTS.json').read_bytes())
require(custody['independently_recomputed_trees'] == 3543 and custody['historical_operator_matches_receipt'] and custody['current_operator_is_different_and_disclosed'], 'Custody conclusion drift')
require((S / 'CUSTODY_RESULTS.json').read_bytes() == (S / 'execution/independent_custody/stdout.bin').read_bytes(), 'Custody result not bound to captured output')

package_inventory = inventory(K)
require(len(package_inventory) == 34, 'Unexpected package inventory')
require({name: row['sha256'] for name, row in package_inventory.items()} == verdict['package_pins'], 'Live package differs from reviewed package')
for snapshot_name in ('PACKAGE_BEFORE.json', 'PACKAGE_FINAL.json'):
    snapshot = json.loads((S / snapshot_name).read_bytes())
    snapshot_inventory = {row['path']: {key: row[key] for key in ('bytes', 'sha256')} for row in snapshot['files']}
    require(snapshot_inventory == package_inventory, 'Package snapshot drift')

source_manifest = json.loads((K / 'MANIFEST.json').read_bytes())
require((K / 'MANIFEST.sha256').read_text().split()[0] == sha((K / 'MANIFEST.json').read_bytes()), 'Source manifest digest drift')
source_listed = {}
for row in source_manifest['files']:
    safe_relative(row['path'])
    require(row['path'] not in source_listed, 'Duplicate source member')
    source_listed[row['path']] = {key: row[key] for key in ('bytes', 'sha256')}
excluded = {'MANIFEST.json', 'MANIFEST.sha256', 'note.pdf', 'blaschke-bloch-verification-v1.zip'}
require(len(source_listed) == 30 and set(source_listed) == set(package_inventory) - excluded, 'Source inventory drift')
require(all(package_inventory[name] == row for name, row in source_listed.items()), 'Source member drift')
with zipfile.ZipFile(K / 'blaschke-bloch-verification-v1.zip') as archive:
    names = archive.namelist()
    require(len(names) == len(set(names)) == 32 and set(names) == set(package_inventory) - {'note.pdf', 'blaschke-bloch-verification-v1.zip'}, 'Archive inventory drift')
    for name in names:
        safe_relative(name)
        require(archive.read(name) == (K / name).read_bytes(), 'Archive member drift')

disposable = S / 'disposable_package'
receipt = json.loads((disposable / 'execution/EXECUTIONS.json').read_bytes())
require(receipt['harness_pid'] == 22006 and receipt['harness_sha256'] == package_inventory['run_verification.py']['sha256'], 'Replay harness drift')
require(len(receipt['executions']) == 4, 'Unexpected nested replay count')
nested = []
for row in receipt['executions']:
    require(row['child_pid'] > 0 and row['exit_code'] == 0, 'Nested replay failure')
    require('-E' in row['argv'] and '-B' in row['argv'] and '-O' not in row['argv'] and '-OO' not in row['argv'], 'Replay assertions not enabled')
    script = Path(row['argv'][-1])
    require(script.is_relative_to(disposable) and sha(script.read_bytes()) == row['script_sha256_before_execution'], 'Replay script drift')
    for stream in ('stdout', 'stderr'):
        body = (disposable / safe_relative(row[stream + '_path'])).read_bytes()
        require(len(body) == row[stream + '_bytes'] and sha(body) == row[stream + '_sha256'], 'Nested process stream drift')
        require(body == (K / row[stream + '_path']).read_bytes(), 'Replay differs from original bounded output')
    nested.append({'label': row['label'], 'child_pid': row['child_pid'], 'exit_code': row['exit_code'], 'bounded_receipt': row['bounded_receipt']})
expected = {'author': ('exact_assertions', 2884), 'legacy_independent': ('assertions_passed', 37154), 'factorization': ('exact_assertions', 4534)}
for row in nested:
    if row['label'] in expected:
        key, count = expected[row['label']]
        require(row['bounded_receipt'][key] == count, 'Replay count drift')
    else:
        require(row['label'] == 'analytic' and row['bounded_receipt']['status'] == 'bounded_diagnostic_only_not_proof', 'Diagnostic scope drift')

result = {'status': 'PASS: completed fresh round2 and current package byte custody', 'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_controller_pid': os.getpid(), 'review_manifest_sha256': manifest_sha, 'review_members_verified': len(listed), 'actual_review_processes': records, 'actual_nested_replays': nested, 'recomputed_trees_in_review_evidence': 3543, 'package_regular_files_verified': len(package_inventory), 'source_manifest_members_verified': len(source_listed), 'archive_members_verified': 32, 'review_report_sha256': verdict['report_sha256'], 'required_repairs': [], 'current_artifacts': {name: package_inventory[name] for name in ('note.tex', 'note.pdf', 'blaschke-bloch-verification-v1.zip', 'MANIFEST.json', 'zenodo-deposit.json')}, 'priority_clearance': False, 'publication_authorized': False, 'git_or_native_status_mutations': False, 'new_replay_performed': False, 'scope': 'ROOT byte/stream custody readback. The independent written mathematical review is separate; bounded replay is not universal proof, novelty or publication authorization.'}
(F / 'READBACK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
