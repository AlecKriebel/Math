"""Passive closure using personally inspected actual native and 74+3 import schemas."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = P / 'papers/23204176/reviews/adversarial-sol-finalization-20261117'
OLD = P / 'papers/23204176/reviews/adversarial-sol-continuation-20261117'
S = P / 'papers/23204176/sources'
I = P / 'papers/23204176/reviews/adversarial-sol'
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def enc(v):
    return (json.dumps(v, indent=2, ensure_ascii=False) + '\n').encode()

def snap(root):
    rows = []
    for p in [root, *sorted(root.rglob('*'))]:
        st = p.lstat()
        r = {'path': '.' if p == root else str(p.relative_to(root)),
             'mode': oct(stat.S_IMODE(st.st_mode)),
             'hidden': any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):
            r.update(kind='directory', empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b = p.read_bytes()
            r.update(kind='file', bytes=len(b), SHA256=sha(b))
        else:
            r.update(kind='other', target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows

def omap(root):
    return {r['path']: {k: v for k, v in r.items() if k not in ['path', 'hidden']} for r in snap(root)}

def count(rows):
    return {'files': sum(r['kind'] == 'file' for r in rows),
            'child_directories': sum(r['kind'] == 'directory' for r in rows) - 1,
            'hidden_paths': sum(r['hidden'] for r in rows),
            'empty_directories': [r['path'] for r in rows if r['kind'] == 'directory' and r['empty']],
            'empty_files': [r['path'] for r in rows if r['kind'] == 'file' and r['bytes'] == 0]}

assert not (A / 'DIAGNOSIS.json').exists() and not (A / 'FINAL.json').exists()
assert not any((A / n).exists() for n in TERMINALS)
protected = json.loads((A / 'PROTECTED_BEFORE.json').read_text())
for key, root in [('source', S), ('INITIAL', I), ('old_failed_continuation', OLD)]:
    assert protected[key] == snap(root), key
prior = json.loads((OLD / 'CUSTODY_BEFORE.json').read_text())
assert protected['source'] == prior['source']
assert protected['INITIAL'] == prior['old_INITIAL']
assert count(protected['source'])['files'] == 43 and count(protected['source'])['child_directories'] == 7
assert count(protected['INITIAL'])['files'] == 20 and count(protected['INITIAL'])['child_directories'] == 1
assert not (OLD / 'FINAL.json').exists() and not any((OLD / n).exists() for n in TERMINALS)
before = json.loads((OLD / 'NATIVE_INPUT_BEFORE.json').read_text())
after = json.loads((OLD / 'NATIVE_INPUT_AFTER.json').read_text())
assert set(before) == {'source', 'isolated'}
assert set(after) == {'source', 'isolated', 'all_original_inputs_exact'}
assert type(after['all_original_inputs_exact']) is bool and after['all_original_inputs_exact']
assert before['source'] == after['source'] == before['isolated']
added = set(after['isolated']) - set(before['isolated'])
assert added == {'reproduced', 'reproduced/paper.pdf', 'reproduced/reproduction.json'}
removed = set(before['isolated']) - set(after['isolated'])
changed = {n: [v, after['isolated'].get(n)] for n, v in before['isolated'].items() if v != after['isolated'].get(n)}
assert not removed and not changed
assert omap(S / 'archives/01-source-and-verification.zip.extracted') == before['source']
actual = omap(OLD / 'native-isolated')
assert actual == after['isolated']
assert {n: actual[n] for n in before['isolated']} == before['isolated']
assert omap(OLD / 'native-temporary') == {'.': {'mode': '0o755', 'kind': 'directory', 'empty': True}}
run = json.loads((OLD / 'NATIVE_RUN.json').read_text())
assert run['attempts'] == 1 and run['exit'] == 0 and run['repairs_retries_interpreter_switches_installs'] == 0
for stem in ['stdout', 'stderr']:
    b = (OLD / ('NATIVE.' + stem + '.bin')).read_bytes()
    assert len(b) == run[stem + '_bytes'] and sha(b) == run[stem + '_SHA256']
assert run['stdout_bytes'] == 311 and run['stderr_bytes'] == 0
assert sha((OLD / 'native-isolated/reproduced/paper.pdf').read_bytes()) == '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'
pins = json.loads((OLD / 'PRIMARY_IMPORT_RECEIPT.json').read_text())
classical = [r for r in pins['files'] if r['path'].startswith('classical-primary/')]
pinned = [r for r in pins['files'] if not r['path'].startswith('classical-primary/')]
assert len(pins['files']) == 77 and len(classical) == 3 and len(pinned) == pins['pinned_files'] == 74
assert set(r['path'] for r in pinned) == set(str(p.relative_to(OLD / 'primary-pinned')) for p in (OLD / 'primary-pinned').rglob('*') if p.is_file())
for r in pins['files']:
    p = OLD / r['path'] if r['path'].startswith('classical-primary/') else OLD / 'primary-pinned' / r['path']
    b = p.read_bytes()
    assert len(b) == r['bytes'] and sha(b) == r['sha256'], r['path']
now = datetime.now(timezone.utc).isoformat()
diagnosis = {'UTC': now, 'old_finalizer_exit': 1, 'old_finalizer_rerun': False,
    'old_finalizer_invalid_criterion': 'Whole BEFORE/AFTER JSON equality includes reporting metadata and expected generated output paths',
    'before_schema': {k: type(v).__name__ for k, v in before.items()},
    'after_schema': {k: type(v).__name__ for k, v in after.items()},
    'top_level_metadata_added': {'all_original_inputs_exact': True},
    'source_map_exact': True, 'all_original_isolated_records_exact': True,
    'removed_original_paths': sorted(removed), 'changed_original_records': changed,
    'generated_additions': {n: after['isolated'][n] for n in sorted(added)},
    'current_whole_isolated_matches_saved_after': True,
    'native_temporary_directory_empty_mode0755': True,
    'original_input_projection': 'Restrict current isolated map to every path in saved BEFORE; all names, types, bytes, hashes, modes and original directory empty states equal exactly',
    'new_closure_attempt1_failure': 'Auxiliary receipt array has 77 records: 74 pinned plus 3 classical; closure.py and failure receipt preserved, not rerun or modified',
    'actual_import_receipt_schema': {'array_records': 77, 'pinned_records': 74, 'classical_records': 3},
    'all_77_import_receipt_file_bytes_exact': True,
    'failure_stream_limit': 'Passive failures preserved as transcriptions of tool results, not claimed binary subprocess captures; scientific native stdout/stderr are actual saved bytes',
    'genuine_protected_input_mutation': False, 'new_scientific_routes': 0,
    'old_failed_lane_whole_scope': count(protected['old_failed_continuation'])}
(A / 'DIAGNOSIS.json').write_bytes(enc(diagnosis))
guard_after = {'UTC': now, 'source': snap(S), 'INITIAL': snap(I), 'old_failed_continuation': snap(OLD)}
assert all(protected[k] == guard_after[k] for k in ['source', 'INITIAL', 'old_failed_continuation'])
(A / 'PROTECTED_AFTER.json').write_bytes(enc(guard_after))
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n' + now + ': Original native input projection exact; only explicit reporting boolean and three ordinary output paths differ. First new closure also stopped on the 74+3 receipt-schema assumption; preserved closure.py and its failure receipt, separate fully read closure-v2 uses the inspected schema under root routine-correction authorization. No old lane writes or scientific reruns. Whole source43/7, INITIAL20/1 and old failed lane exact. Separate passive closure100%; freeze and stop.\n')
final = {'UTC': now, 'row': 191, 'kind': 'Separate passive diagnosis and finite closure; no new science',
    'completion_percent': 100, 'follow_up': None, 'old_failed_continuation': str(OLD),
    'old_finalizer_exit': 1, 'old_finalizer_pass_claimed': False, 'old_finalizer_rerun': False,
    'new_passive_closure_attempts': 2, 'first_new_closure_failure_preserved': True,
    'old_failed_continuation_whole_scope': count(protected['old_failed_continuation']),
    'whole_source_INITIAL_old_failed_lane_exact': True, 'actual_original_native_inputs_exact': True,
    'explicit_expected_generated_paths': sorted(added), 'metadata_difference': ['all_original_inputs_exact'],
    'genuine_protected_input_mutation': False, 'all_74_pins_and_3_classical_receipt_files_exact': True,
    'native_scientific_attempts_total': 1, 'native_scientific_exit': 0,
    'native_stdout_bytes': 311, 'native_stderr_bytes': 0, 'new_scientific_routes_installs_repairs_retries': 0,
    'scientific_report': str(OLD / 'ADVERSARIAL_REVIEW.md'),
    'exposure_and_limits': str(OLD / 'EXPOSURE_AND_READING_LEDGER.md'),
    'mathematical_findings_withheld_from_messages': True, 'root_owns_scientific_adoption': True,
    'stop': 'Whole old failed continuation guarded and immutable; separate closure frozen; quiescent'}
(A / 'FINAL.json').write_bytes(enc(final))
for name in TERMINALS:
    (A / name).write_bytes(b'')
rows = snap(A)
for r in rows:
    if r['path'] in TERMINALS:
        r['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
scope = count(rows)
scope['empty_files'] = [n for n in scope['empty_files'] if n not in TERMINALS]
manifest = {'UTC': now, 'root': str(A), **scope, 'actual_all_bytes_modes_hidden_empty_topology': True,
            'only_recursive_hash_exclusions': sorted(TERMINALS), 'entries': rows}
seal = {'UTC': now, 'frozen': True, 'root': str(A), **scope,
    'manifest_bytes': 0, 'manifest_SHA256': '0' * 64,
    'FINAL_SHA256': sha((A / 'FINAL.json').read_bytes()), 'DIAGNOSIS_SHA256': sha((A / 'DIAGNOSIS.json').read_bytes()),
    'PROTECTED_BEFORE_SHA256': sha((A / 'PROTECTED_BEFORE.json').read_bytes()),
    'PROTECTED_AFTER_SHA256': sha((A / 'PROTECTED_AFTER.json').read_bytes()),
    'whole_old_failed_lane_scope': count(protected['old_failed_continuation']),
    'whole_source_INITIAL_old_failed_lane_exact': True,
    'only_recursive_hash_exclusions': sorted(TERMINALS), 'seal_SHA256': 'EXCLUDED_TERMINAL_RECURSIVE_HASH',
    'old_finalizer_failure_preserved': True, 'new_closure_attempt1_failure_preserved': True,
    'native_scientific_attempts': 1, 'native_scientific_exit': 0,
    'completion_percent': 100, 'follow_up': None, 'stop': True}
for _ in range(20):
    mb = enc(manifest)
    seal['manifest_bytes'] = len(mb)
    seal['manifest_SHA256'] = sha(mb)
    sb = enc(seal)
    sizes = {'FINAL_MANIFEST.json': len(mb), 'FINAL_SEAL.json': len(sb)}
    if all(r['bytes'] == sizes[r['path']] for r in rows if r['path'] in TERMINALS):
        break
    for r in rows:
        if r['path'] in TERMINALS:
            r['bytes'] = sizes[r['path']]
else:
    raise AssertionError('Terminal size fixed point failed')
(A / 'FINAL_MANIFEST.json').write_bytes(mb)
(A / 'FINAL_SEAL.json').write_bytes(sb)
actual_rows = snap(A)
for r in actual_rows:
    if r['path'] in TERMINALS:
        r['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual_rows == rows and count(actual_rows) == scope
assert all(protected[k] == snap(root) for k, root in [('source', S), ('INITIAL', I), ('old_failed_continuation', OLD)])
print(json.dumps({'UTC': now, 'frozen': True, **scope,
    'manifest_bytes': len(mb), 'manifest_SHA256': sha(mb), 'seal_bytes': len(sb), 'seal_SHA256': sha(sb),
    'FINAL_SHA256': seal['FINAL_SHA256'], 'DIAGNOSIS_SHA256': seal['DIAGNOSIS_SHA256'],
    'old_failed_lane': count(protected['old_failed_continuation']),
    'whole_source_INITIAL_old_failed_lane_exact': True, 'native_scientific_attempts': 1,
    'native_scientific_exit': 0, 'completion_percent': 100}))
