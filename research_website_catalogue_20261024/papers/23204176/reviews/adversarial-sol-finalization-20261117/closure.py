"""One bounded passive closure: actual schemas, exact input projection and whole guards."""
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

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def snap(root):
    rows = []
    for path in [root, *sorted(root.rglob('*'))]:
        st = path.lstat()
        name = '.' if path == root else str(path.relative_to(root))
        row = {'path': name, 'mode': oct(stat.S_IMODE(st.st_mode)),
               'hidden': any(x.startswith('.') for x in path.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):
            row.update(kind='directory', empty=not any(path.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            data = path.read_bytes()
            row.update(kind='file', bytes=len(data), SHA256=sha(data))
        else:
            row.update(kind='other', target=os.readlink(path) if path.is_symlink() else None)
        rows.append(row)
    return rows

def original_map(root):
    return {r['path']: {k: v for k, v in r.items() if k not in ['path', 'hidden']} for r in snap(root)}

def counts(rows):
    return {'files': sum(r['kind'] == 'file' for r in rows),
            'child_directories': sum(r['kind'] == 'directory' for r in rows) - 1,
            'hidden_paths': sum(r['hidden'] for r in rows),
            'empty_directories': [r['path'] for r in rows if r['kind'] == 'directory' and r['empty']],
            'empty_files': [r['path'] for r in rows if r['kind'] == 'file' and r['bytes'] == 0]}

assert not (A / 'PROTECTED_BEFORE.json').exists()
assert not (A / 'FINAL.json').exists()
assert not any((A / n).exists() for n in TERMINALS)
start = datetime.now(timezone.utc).isoformat()
protected_before = {'UTC': start, 'source': snap(S), 'INITIAL': snap(I), 'old_failed_continuation': snap(OLD)}
(A / 'PROTECTED_BEFORE.json').write_bytes(encode(protected_before))
prior_before = json.loads((OLD / 'CUSTODY_BEFORE.json').read_text())
prior_after = json.loads((OLD / 'CUSTODY_AFTER.json').read_text())
assert protected_before['source'] == prior_before['source'] == prior_after['source']
assert protected_before['INITIAL'] == prior_before['old_INITIAL'] == prior_after['old_INITIAL']
assert counts(protected_before['source'])['files'] == 43
assert counts(protected_before['source'])['child_directories'] == 7
assert counts(protected_before['INITIAL'])['files'] == 20
assert counts(protected_before['INITIAL'])['child_directories'] == 1
assert sha((I / 'INITIAL_MANIFEST.json').read_bytes()) == '54154aca5b5fbcd8c6199c9182b95cccf52a4db1e1865753f7929c74b65d72ce'
assert sha((I / 'INITIAL_SEAL.json').read_bytes()) == 'c2d4d655fa7e04df3a03975ea168feb63c9fb3979b3f1c7404b019af4176ac2c'
assert not (OLD / 'FINAL.json').exists()
assert not any((OLD / n).exists() for n in TERMINALS)
failure = json.loads((OLD / 'FINALIZATION_FAILURE.json').read_text())
assert failure['exit'] == 1 and failure['attempts'] == 1
assert failure['failing_expression'] == 'assert native_before == native_after'
before = json.loads((OLD / 'NATIVE_INPUT_BEFORE.json').read_text())
after = json.loads((OLD / 'NATIVE_INPUT_AFTER.json').read_text())
assert set(before) == {'source', 'isolated'}
assert set(after) == {'source', 'isolated', 'all_original_inputs_exact'}
assert type(after['all_original_inputs_exact']) is bool and after['all_original_inputs_exact']
assert isinstance(before['source'], dict) and isinstance(before['isolated'], dict)
assert isinstance(after['source'], dict) and isinstance(after['isolated'], dict)
assert before['source'] == after['source'] == before['isolated']
expected_additions = {'reproduced', 'reproduced/paper.pdf', 'reproduced/reproduction.json'}
added = set(after['isolated']) - set(before['isolated'])
removed = set(before['isolated']) - set(after['isolated'])
changed = {n: {'before': row, 'after': after['isolated'].get(n)}
           for n, row in before['isolated'].items() if row != after['isolated'].get(n)}
assert added == expected_additions and not removed and not changed
actual_source = original_map(S / 'archives/01-source-and-verification.zip.extracted')
actual_isolated = original_map(OLD / 'native-isolated')
assert actual_source == before['source']
assert actual_isolated == after['isolated']
projected = {n: actual_isolated[n] for n in before['isolated']}
assert projected == before['isolated']
assert after['isolated']['reproduced'] == {'mode': '0o755', 'kind': 'directory', 'empty': False}
assert after['isolated']['reproduced/paper.pdf']['SHA256'] == '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'
assert after['isolated']['reproduced/reproduction.json']['SHA256'] == '1a4035ebb61118a7872c81d86f1d413c226292105378929d33926b8681bbd75a'
assert original_map(OLD / 'native-temporary') == {'.': {'mode': '0o755', 'kind': 'directory', 'empty': True}}
run = json.loads((OLD / 'NATIVE_RUN.json').read_text())
assert run['attempts'] == 1 and run['exit'] == 0
assert run['repairs_retries_interpreter_switches_installs'] == 0
for stream in ['stdout', 'stderr']:
    data = (OLD / ('NATIVE.' + stream + '.bin')).read_bytes()
    assert len(data) == run[stream + '_bytes'] and sha(data) == run[stream + '_SHA256']
assert run['stdout_bytes'] == 311 and run['stderr_bytes'] == 0
pins = json.loads((OLD / 'PRIMARY_IMPORT_RECEIPT.json').read_text())
assert len(pins['files']) == pins['pinned_files'] == 74
for item in pins['files']:
    data = (OLD / 'primary-pinned' / item['path']).read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['path']
diagnosis = {
    'UTC': datetime.now(timezone.utc).isoformat(),
    'old_finalizer_attempts': 1, 'old_finalizer_exit': 1,
    'old_finalizer_rerun_or_modified': False,
    'old_failure_receipts': {'FINALIZATION_FAILURE.json': sha((OLD / 'FINALIZATION_FAILURE.json').read_bytes()),
                             'FINALIZATION_FAILURE.stderr.txt': sha((OLD / 'FINALIZATION_FAILURE.stderr.txt').read_bytes())},
    'failure_stream_limit': 'Old passive finalizer stderr file is a preserved transcription of the tool result, not a claimed binary subprocess capture. Scientific native streams were captured as actual bytes.',
    'before_schema': {k: type(v).__name__ for k, v in before.items()},
    'after_schema': {k: type(v).__name__ for k, v in after.items()},
    'top_level_added_reporting_metadata': {'all_original_inputs_exact': True},
    'top_level_removed': [], 'source_map_exact': True,
    'original_isolated_input_projection_exact': True,
    'original_isolated_common_record_changes': changed,
    'original_isolated_paths_removed': sorted(removed),
    'explicit_expected_generated_additions': {n: after['isolated'][n] for n in sorted(added)},
    'current_isolated_whole_map_exact_to_saved_after': True,
    'native_temporary_cache': 'directory exists, mode0755, empty; no cache payload',
    'invalid_criterion': 'Whole BEFORE/AFTER JSON equality includes extra reporting metadata and ordinary generated outputs; use exact projection onto the original input namespace, enumerate additions separately.',
    'genuine_protected_input_mutation_found': False,
    'scientific_reruns': 0, 'source_repairs': 0,
    'all_74_pinned_imported_files_still_exact': True,
    'full_old_failed_lane_scope': counts(protected_before['old_failed_continuation'])
}
(A / 'DIAGNOSIS.json').write_bytes(encode(diagnosis))
protected_after = {'UTC': datetime.now(timezone.utc).isoformat(), 'source': snap(S),
                   'INITIAL': snap(I), 'old_failed_continuation': snap(OLD)}
assert all(protected_before[k] == protected_after[k] for k in ['source', 'INITIAL', 'old_failed_continuation'])
(A / 'PROTECTED_AFTER.json').write_bytes(encode(protected_after))
now = datetime.now(timezone.utc).isoformat()
with (A / 'RESEARCH_LOG.md').open('a') as log:
    log.write('\n' + now + ': Actual full schemas diagnosed. Only the explicit reporting boolean and three expected generated output paths differ; all original input records and actual current buffers/modes are exact. All source43/7, INITIAL20/1 and whole old failed lane paths/bytes/modes/hidden/empty topology match before/after. No scientific rerun or old-writer retry. Separate passive closure100%; terminal manifest/seal follows, then quiescence.\n')
final = {'UTC': now, 'row': 191, 'Zenodo_record': '23204176',
         'kind': 'Separate passive diagnosis and finite closure; no new science',
         'completion_percent': 100, 'follow_up': None,
         'old_continuation': str(OLD), 'old_finalizer_exit': 1,
         'old_finalizer_pass_claimed': False, 'old_failed_namespace_unchanged': True,
         'whole_old_namespace': counts(protected_before['old_failed_continuation']),
         'source43_7_and_INITIAL20_1_complete_exact': True,
         'actual_original_native_input_projection_exact': True,
         'separately_enumerated_expected_output_paths': sorted(added),
         'metadata_difference': ['all_original_inputs_exact'],
         'genuine_protected_input_mutation': False,
         'native_scientific_attempts_total': 1, 'native_scientific_exit': 0,
         'native_stdout_bytes': 311, 'native_stderr_bytes': 0,
         'new_scientific_routes_installs_repairs_retries': 0,
         'scientific_report': str(OLD / 'ADVERSARIAL_REVIEW.md'),
         'reading_exposure_limits': str(OLD / 'EXPOSURE_AND_READING_LEDGER.md'),
         'mathematical_findings_withheld_from_messages': True,
         'root_owns_scientific_adoption': True,
         'stop': 'Freeze both full old failed namespace and this separate complete closure; quiescent'}
(A / 'FINAL.json').write_bytes(encode(final))
for name in TERMINALS:
    (A / name).write_bytes(b'')
rows = snap(A)
for row in rows:
    if row['path'] in TERMINALS:
        row['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
scope = counts(rows)
scope['empty_files'] = [n for n in scope['empty_files'] if n not in TERMINALS]
manifest = {'UTC': now, 'root': str(A), **scope,
            'all_actual_paths_modes_bytes_hidden_empty_topology': True,
            'only_recursive_hash_exclusions': sorted(TERMINALS), 'entries': rows}
seal = {'UTC': now, 'frozen': True, 'root': str(A), **scope,
        'manifest': 'FINAL_MANIFEST.json', 'manifest_bytes': 0, 'manifest_SHA256': '0' * 64,
        'FINAL_SHA256': sha((A / 'FINAL.json').read_bytes()),
        'PROTECTED_BEFORE_SHA256': sha((A / 'PROTECTED_BEFORE.json').read_bytes()),
        'PROTECTED_AFTER_SHA256': sha((A / 'PROTECTED_AFTER.json').read_bytes()),
        'DIAGNOSIS_SHA256': sha((A / 'DIAGNOSIS.json').read_bytes()),
        'old_failed_continuation_whole_scope': counts(protected_before['old_failed_continuation']),
        'source_INITIAL_old_failed_lane_exact': True,
        'only_recursive_hash_exclusions': sorted(TERMINALS),
        'seal_SHA256': 'EXCLUDED_TERMINAL_RECURSIVE_HASH',
        'old_finalizer_failure_preserved': True, 'old_finalizer_retry': False,
        'native_scientific_attempts': 1, 'native_scientific_exit': 0,
        'completion_percent': 100, 'follow_up': None, 'stop': True}
for _ in range(20):
    mb = encode(manifest)
    seal['manifest_bytes'] = len(mb)
    seal['manifest_SHA256'] = sha(mb)
    sb = encode(seal)
    sizes = {'FINAL_MANIFEST.json': len(mb), 'FINAL_SEAL.json': len(sb)}
    if all(r['bytes'] == sizes[r['path']] for r in rows if r['path'] in TERMINALS):
        break
    for row in rows:
        if row['path'] in TERMINALS:
            row['bytes'] = sizes[row['path']]
else:
    raise AssertionError('Terminal size fixed point failed')
(A / 'FINAL_MANIFEST.json').write_bytes(mb)
(A / 'FINAL_SEAL.json').write_bytes(sb)
actual = snap(A)
for row in actual:
    if row['path'] in TERMINALS:
        row['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual == rows
assert counts(actual) == scope
assert all(protected_before[k] == snap(root) for k, root in [('source', S), ('INITIAL', I), ('old_failed_continuation', OLD)])
print(json.dumps({'UTC': now, 'frozen': True, **scope,
                  'manifest_bytes': len(mb), 'manifest_SHA256': sha(mb),
                  'seal_bytes': len(sb), 'seal_SHA256': sha(sb),
                  'FINAL_SHA256': seal['FINAL_SHA256'],
                  'DIAGNOSIS_SHA256': seal['DIAGNOSIS_SHA256'],
                  'old_failed_lane': counts(protected_before['old_failed_continuation']),
                  'source_INITIAL_old_failed_lane_exact': True,
                  'old_finalizer_rerun': False, 'native_scientific_attempts': 1,
                  'native_scientific_exit': 0, 'completion_percent': 100}))
