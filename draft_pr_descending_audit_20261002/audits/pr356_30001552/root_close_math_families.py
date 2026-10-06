"""Approved one-time administrative closure, then complete read-only verification."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess

A = Path(__file__).resolve().parent
PY = '/opt/homebrew/bin/python3.11'
CAP = A / 'root_replay_private' / 'family_closure_001'
AUTH = A / 'ROOT_MATH_FAMILY_CLOSURE_AUTHORIZATION.json'

def now(): return datetime.now(timezone.utc).isoformat()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def put(path, value):
    assert not path.exists(), str(path)
    path.write_text(json.dumps(value, indent=2) + '\n')
def inv(root):
    files = {}; dirs = {'.': stat.S_IMODE(root.stat().st_mode)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink(), str(p)
        rel = p.relative_to(root).as_posix()
        if p.is_file():
            files[rel] = {'bytes': p.stat().st_size, 'sha256': sha(p), 'mode': stat.S_IMODE(p.stat().st_mode)}
        else:
            assert p.is_dir(), str(p)
            dirs[rel] = stat.S_IMODE(p.stat().st_mode)
    return {'files': files, 'directories': dirs}
def freeze(root):
    for p in root.rglob('*'):
        if p.is_file(): p.chmod(0o444)
    for p in sorted((p for p in root.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        p.chmod(0o555)
    root.chmod(0o555)
def native(name, argv):
    pin = {'utc': now(), 'argv': argv, 'cwd': str(A), 'program_sha256': sha(Path(argv[2]))}
    put(CAP / (name + '.before.json'), pin)
    (CAP / (name + '.executed_source.py')).write_bytes(Path(argv[2]).read_bytes())
    started = now()
    result = subprocess.run(argv, cwd=A, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    ended = now()
    (CAP / (name + '.stdout')).write_bytes(result.stdout)
    (CAP / (name + '.stderr')).write_bytes(result.stderr)
    record = {'started_utc': started, 'finished_utc': ended, **pin,
              'exit_code': result.returncode, 'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr),
              'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
              'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
    put(CAP / (name + '.after.json'), record)
    assert result.returncode == 0 and result.stderr == b'', record
    return load(CAP / (name + '.stdout')), record

assert not CAP.exists() and not AUTH.exists(), 'Closure is one-time; do not overwrite prior native evidence.'
controls = load(A / 'ROOT_INDEPENDENT_CONTROLS_REPLAY.json')
assert controls['status'] == 'PASS_THREE_WHOLE_NATIVE_INDEPENDENT_CONTROL_OUTPUTS'
assert all(r['exit_code'] == 0 and r['stderr_bytes'] == 0 and r['entire_stdout_exact_expected_bytes']
           and r['namespace_entire_files_directories_modes_unchanged'] for r in controls['runs'])
assert load(A / 'ROOT_FROZEN_GIT_VERIFICATION.json')['status'] == 'PASS_LITERAL_GIT_ALL17_PREVIOUSLY_API_FROZEN_FILES'
signed = A / 'signed_graph_review/proposed_namespace'
word = A / 'word_overlap_review'
definition = A / 'definition_counterexample_review'
roots = {'signed_graph': signed, 'word_overlap': word, 'definition_counterexamples': definition}
plans = {
    'signed_graph': (A / 'signed_graph_review/CLOSURE_PLAN_003.json', 'ac927770d9ee89a6bb3ff9f986da579ad9fc7715ebd3f2ce4f48cf571f098a03'),
    'word_overlap': (word / 'NAMESPACE_PLAN_V2.json', '2f9129cf0e5c06b3a9a238026d23471301890423803fd2eae63ae835ca6378f1'),
    'definition_counterexamples': (definition / 'private/PACKAGE_PLAN_V2.json', None),
}
before = {name: inv(root) for name, root in roots.items()}
for name, (path, expected) in plans.items():
    if expected: assert sha(path) == expected, name
sp = load(plans['signed_graph'][0]); wp = load(plans['word_overlap'][0]); dp = load(plans['definition_counterexamples'][0])
assert set(before['signed_graph']['files']) == set(sp['files'])
for rel, data in sp['files'].items():
    assert all(before['signed_graph']['files'][rel][k] == data[k] for k in ('bytes', 'sha256'))
assert set(before['word_overlap']['files']) == {e['path'] for e in wp['files']} | {'NAMESPACE_PLAN_V2.json'}
for data in wp['files']:
    assert all(before['word_overlap']['files'][data['path']][k] == data[k] for k in ('bytes', 'sha256'))
assert {p.removeprefix('public/') for p in before['definition_counterexamples']['files'] if p.startswith('public/')} == set(dp['public_namespace'])
assert all(p.startswith(('public/', 'private/')) for p in before['definition_counterexamples']['files'])
assert sha(word / 'seal_once_v2.py') == '41629fe6fb51f4b35e6e140088d5e4a5e9085bddd9223b67e7fecc2b08cfb3c0'
generated = {
    'signed_graph': {'public/PUBLIC_INVENTORY.json', 'private/PRIVATE_INVENTORY.json', 'public/CLOSURE_SEAL.json'},
    'word_overlap': {'public/PUBLIC_MANIFEST.json', 'public/PUBLIC_CLOSURE.json', 'PRIVATE_MANIFEST.json', 'SEALED_NAMESPACE.json'},
    'definition_counterexamples': {'public/PUBLIC_MANIFEST.json', 'private/PRIVATE_MANIFEST.json', 'private/PACKAGE_SEAL.json', 'private/PACKAGE_SEAL.sha256'},
}
assert all(not any((roots[name] / rel).exists() for rel in names) for name, names in generated.items())
CAP.mkdir(parents=True)
approval = {'utc': now(), 'status': 'ROOT_APPROVED_CONCRETE_ONE_TIME_MATHEMATICAL_AUDIT_CLOSURE',
            'root_driver_sha256': sha(Path(__file__)), 'source_proofs_reports_control_code_verifiers_plans_full_read': True,
            'independent_whole_control_receipt_sha256': sha(A / 'ROOT_INDEPENDENT_CONTROLS_REPLAY.json'),
            'plans': {n: {'path': str(p.relative_to(A)), 'sha256': sha(p)} for n, (p, _) in plans.items()},
            'namespaces_before': before, 'permitted_generated_files': {n: sorted(v) for n,v in generated.items()},
            'permitted_log_append_only': {'word_overlap': 'research_log.md', 'definition_counterexamples': 'private/research_log.md'},
            'verdict': 'Universal theorem passes all three analytical audits; finite controls are supplemental.',
            'limitations': ['No priority conclusion, paper acceptance, human peer review, merge or publication is authorized by this administrative closure.',
                            'Historical 68413 original-source mode is not reproduced.']}
put(AUTH, approval)
put(CAP / 'root_driver_preexecution_pin.json', {'utc': now(), 'sha256': sha(Path(__file__)), 'authorization_sha256': sha(AUTH)})
# Signed package: preserve all48 approved payloads; seal is the final generated record.
for scope, filename in [('public', 'PUBLIC_INVENTORY.json'), ('private', 'PRIVATE_INVENTORY.json')]:
    payload = {p: v for p,v in sp['files'].items() if p.startswith(scope + '/')}
    put(signed / scope / filename, {'files': payload, 'scope': scope, 'schema': 'signed-graph-closure-v3'})
put(signed / 'public/CLOSURE_SEAL.json', {'status': 'SEALED_ONCE_READ_ONLY', 'closed_utc': now(),
    'public_inventory_sha256': sha(signed / 'public/PUBLIC_INVENTORY.json'),
    'private_inventory_sha256': sha(signed / 'private/PRIVATE_INVENTORY.json'),
    'private_payload_file_count': 42, 'public_payload_file_count': 6,
    'root_authorization_sha256': sha(AUTH), 'approved_plan_sha256': sha(plans['signed_graph'][0]),
    'completion_percent': 100, 'no_further_namespace_writes': True, 'novelty_not_certified': True})
freeze(signed)
# Word package uses the fully read, pinned agent-prepared one-shot closer.
native('word_one_time_closer', [PY, '-B', str(word / 'seal_once_v2.py')])
# Definition package follows the approved curated plan. Retain original log bytes as a prefix.
with (definition / 'private/research_log.md').open('a') as out:
    out.write('\n## ' + now() + ' — Root-approved final administrative closure\n\nRoot fully read the reports, independent programs, namespace verifier and plan. Root independently reproduced the complete 238373-assertion stdout. Generate curated manifests and one seal once; files444/directories555; no later namespace writes. Mathematical family audit completion estimate:100%. Priority and preprint acceptance remain root-owned and pending.\n')
for scope in ('public', 'private'):
    records = [{'path': p, 'bytes': v['bytes'], 'sha256': v['sha256']}
               for p,v in inv(definition)['files'].items() if p.startswith(scope + '/')]
    put(definition / scope / (scope.upper() + '_MANIFEST.json'), {'files': records, 'scope': scope,
         'schema': 'definition-audit-closure-v2', 'root_authorization_sha256': sha(AUTH)})
seal = definition / 'private/PACKAGE_SEAL.json'
put(seal, {'status': 'SEALED_ONCE_READ_ONLY', 'closed_utc': now(),
           'public_manifest_sha256': sha(definition / 'public/PUBLIC_MANIFEST.json'),
           'private_manifest_sha256': sha(definition / 'private/PRIVATE_MANIFEST.json'),
           'root_authorization_sha256': sha(AUTH), 'approved_plan_sha256': sha(plans['definition_counterexamples'][0]),
           'completion_percent': 100, 'no_further_namespace_writes': True, 'novelty_not_certified': True})
(definition / 'private/PACKAGE_SEAL.sha256').write_text(sha(seal) + '  PACKAGE_SEAL.json\n')
freeze(definition)
closed = {n: inv(r) for n,r in roots.items()}
allowed_logs = {'word_overlap': 'research_log.md', 'definition_counterexamples': 'private/research_log.md'}
for name, old in before.items():
    new = closed[name]
    assert set(new['files']) == set(old['files']) | generated[name]
    assert set(new['directories']) == set(old['directories'])
    for path, data in old['files'].items():
        if path == allowed_logs.get(name):
            # An append is the only approved change; compare the entire prior prefix from its retained root replay inventory.
            assert (roots[name]/path).stat().st_size > data['bytes']
            assert hashlib.sha256((roots[name]/path).read_bytes()[:data['bytes']]).hexdigest() == data['sha256']
        else: assert new['files'][path]['sha256'] == data['sha256'] and new['files'][path]['bytes'] == data['bytes']
    assert all(v['mode'] == 0o444 for v in new['files'].values())
    assert all(v == 0o555 for v in new['directories'].values())
verification_runs = []
for name, root in roots.items():
    for mode in ('full', 'public'):
        argv = [PY, '-B', str(root/'public/verify_namespace.py')]
        if name == 'signed_graph': argv += ['--namespace', str(root), '--mode', mode]
        elif name == 'word_overlap': argv += ['--root', str(root), '--mode', 'full' if mode=='full' else 'public-only']
        else:
            argv += ['--root', str(root), '--mode', mode]
            if mode == 'full': argv += ['--candidate-root', str(A/'snapshot/problems/30001552_antimorphic_periods')]
        output, run = native(name + '_' + mode + '_closed', argv)
        if name == 'signed_graph': assert output['status'] == ('PASS_FULL_SAVED_EVIDENCE' if mode=='full' else 'PASS_PUBLIC_INVENTORY_ONLY')
        else: assert output['status'] == 'PASS'
        if name == 'definition_counterexamples':
            assert output['errors'] == [] and all(c['pass'] is True for c in output['checks'])
        assert inv(root) == closed[name], 'Read-only verifier modified a closed namespace'
        verification_runs.append({'name': name, 'mode': mode, **run})
receipt = {'utc': now(), 'status': 'PASS_THREE_CLOSED_MATH_FAMILIES_FULL_AND_PUBLIC_VERIFIERS',
           'authorization_sha256': sha(AUTH), 'whole_closed_namespaces': closed,
           'native_verifications': verification_runs, 'capture': str(CAP.relative_to(A)),
           'mathematical_audit_completion_percent': 100, 'priority_and_preprint_pending': True}
put(A/'ROOT_CLOSED_MATH_FAMILIES.json', receipt)
print(json.dumps({'status': receipt['status'], 'mathematical_audit_completion_percent': 100,
                  'closed_file_counts': {n:len(v['files']) for n,v in closed.items()},
                  'verification_runs': verification_runs}, indent=2))
