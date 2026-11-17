"""Finite passive guard and terminal packet writer; no project imports/execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = P / 'papers/23204176/reviews/adversarial-sol-continuation-20261117'
S = P / 'papers/23204176/sources'
I = P / 'papers/23204176/reviews/adversarial-sol'
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def snap(root):
    rows = []
    for path in [root, *sorted(root.rglob('*'))]:
        st = path.lstat()
        rel = '.' if path == root else str(path.relative_to(root))
        row = {'path': rel, 'mode': oct(stat.S_IMODE(st.st_mode)),
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

assert not (A / 'FINAL.json').exists()
assert not any((A / name).exists() for name in TERMINALS)
before = json.loads((A / 'CUSTODY_BEFORE.json').read_text())
after = json.loads((A / 'CUSTODY_AFTER.json').read_text())
assert before['source'] == after['source'] == snap(S)
assert before['old_INITIAL'] == after['old_INITIAL'] == snap(I)
assert sha((I / 'INITIAL_MANIFEST.json').read_bytes()) == '54154aca5b5fbcd8c6199c9182b95cccf52a4db1e1865753f7929c74b65d72ce'
assert sha((I / 'INITIAL_SEAL.json').read_bytes()) == 'c2d4d655fa7e04df3a03975ea168feb63c9fb3979b3f1c7404b019af4176ac2c'
native_before = json.loads((A / 'NATIVE_INPUT_BEFORE.json').read_text())
native_after = json.loads((A / 'NATIVE_INPUT_AFTER.json').read_text())
assert native_before == native_after
archive = S / 'archives/01-source-and-verification.zip.extracted'
for kind, root in [('source', archive), ('isolated', A / 'native-isolated')]:
    actual = {r['path']: {k: v for k, v in r.items() if k not in ['path', 'hidden']} for r in snap(root)}
    for name, expected in native_before[kind].items():
        assert actual[name] == expected, (kind, name)
native = json.loads((A / 'NATIVE_RUN.json').read_text())
assert native['attempts'] == 1 and native['exit'] == 0
assert native['repairs_retries_interpreter_switches_installs'] == 0
for stem in ['stdout', 'stderr']:
    data = (A / ('NATIVE.' + stem + '.bin')).read_bytes()
    assert len(data) == native[stem + '_bytes']
    assert sha(data) == native[stem + '_SHA256']
assert native['stdout_bytes'] == 311 and native['stderr_bytes'] == 0
assert sha((A / 'native-isolated/reproduced/paper.pdf').read_bytes()) == '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'
primary = json.loads((A / 'PRIMARY_IMPORT_RECEIPT.json').read_text())
assert len(primary['files']) == primary['pinned_files'] == 74
for item in primary['files']:
    data = (A / 'primary-pinned' / item['path']).read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['path']

now = datetime.now(timezone.utc).isoformat()
final = {
    'UTC': now, 'row': 191, 'Zenodo_record': '23204176',
    'scope': 'Independent adversarial scientific continuation; finite ordinary written-proof review',
    'completion_percent': 100,
    'completion_interpretation': 'Authorized bounded review and evidence closure; not formal theorem certainty',
    'review_outcome': 'No verified central fatal defect located within the explicitly recorded reading and check scope',
    'unconditional_independent_discovery_or_formal_certificate_claimed': False,
    'root_disposition_required': True, 'follow_up': None,
    'reports': ['ADVERSARIAL_REVIEW.md', 'EXPOSURE_AND_READING_LEDGER.md', 'CHECKPOINT_DERIVATIONS.md', 'RESEARCH_LOG.md'],
    'source_files': 43, 'source_child_directories': 7,
    'old_INITIAL_files': 20, 'old_INITIAL_child_directories': 1,
    'complete_source_and_INITIAL_byte_mode_topology_guards': True,
    'pinned_upstream_commit': primary['pinned_commit'], 'pinned_upstream_files_authenticated': 74,
    'complete_central_mixed_manuscript_lines_read': 4805,
    'complete_central_CM_proof_chain_read': True,
    'exact_reading_limits': 'EXPOSURE_AND_READING_LEDGER.md',
    'native_attempts': 1, 'native_exit': 0, 'native_stdout_bytes': 311, 'native_stderr_bytes': 0,
    'native_elapsed_seconds': native['elapsed_seconds'],
    'native_scope': 'Source integrity, bounded finite algebra, ordinary PDF build; no geometric certificate',
    'native_repairs_retries_installs_interpreter_switches': 0,
    'source_or_INITIAL_mutations': 0, 'children': 0, 'external_contact_or_outreach': 0,
    'current_peer_or_root_mathematical_reports_read': False,
    'native_API_version_field': None, 'native_API_version_field_absent': True,
    'printed_declared_date': '2026-10-06',
    'native_pdf_SHA256': '483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612',
    'coordination': 'Mathematical mechanisms and verdicts withheld; root handles final disposition',
    'stop_after_terminal_seal': True
}
(A / 'FINAL.json').write_bytes(encoded(final))
for name in TERMINALS:
    (A / name).write_bytes(b'')
rows = snap(A)
for row in rows:
    if row['path'] in TERMINALS:
        row['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
files = [r for r in rows if r['kind'] == 'file']
dirs = [r for r in rows if r['kind'] == 'directory']
assert not any(r['kind'] == 'other' for r in rows)
manifest = {'UTC': now, 'root': str(A), 'files': len(files), 'child_directories': len(dirs) - 1,
            'all_actual_paths_modes_hidden_empty_topology': True,
            'only_hash_exclusions': sorted(TERMINALS), 'entries': rows}
seal = {'UTC': now, 'frozen': True, 'root': str(A), 'files': len(files),
        'child_directories': len(dirs) - 1, 'manifest': 'FINAL_MANIFEST.json',
        'manifest_bytes': 0, 'manifest_SHA256': '0' * 64,
        'FINAL_SHA256': sha((A / 'FINAL.json').read_bytes()),
        'CUSTODY_AFTER_SHA256': sha((A / 'CUSTODY_AFTER.json').read_bytes()),
        'source_and_INITIAL_complete_exact': True,
        'native_attempts': 1, 'native_exit': 0,
        'completion_percent': 100, 'follow_up': None,
        'only_recursive_hash_exclusions': sorted(TERMINALS),
        'seal_SHA256': 'EXCLUDED_TERMINAL_RECURSIVE_HASH',
        'stop': 'Frozen whole namespace; no subsequent writes authorized in this lane'}
for _ in range(20):
    mb = encoded(manifest)
    seal['manifest_bytes'] = len(mb)
    seal['manifest_SHA256'] = sha(mb)
    sb = encoded(seal)
    sizes = {'FINAL_MANIFEST.json': len(mb), 'FINAL_SEAL.json': len(sb)}
    if all(r['bytes'] == sizes[r['path']] for r in rows if r['path'] in TERMINALS):
        break
    for row in rows:
        if row['path'] in TERMINALS:
            row['bytes'] = sizes[row['path']]
else:
    raise AssertionError('Terminal size fixed point did not converge')
(A / 'FINAL_MANIFEST.json').write_bytes(mb)
(A / 'FINAL_SEAL.json').write_bytes(sb)
actual = snap(A)
for row in actual:
    if row['path'] in TERMINALS:
        row['SHA256'] = 'EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual == rows
assert sha((A / 'FINAL_MANIFEST.json').read_bytes()) == seal['manifest_SHA256']
assert before['source'] == snap(S) and before['old_INITIAL'] == snap(I)
print(json.dumps({'UTC': now, 'frozen': True, 'files': len(files), 'child_directories': len(dirs) - 1,
                  'manifest_bytes': len(mb), 'manifest_SHA256': sha(mb),
                  'seal_bytes': len(sb), 'seal_SHA256': sha(sb),
                  'FINAL_SHA256': seal['FINAL_SHA256'], 'source_and_INITIAL_exact': True,
                  'native_attempts': 1, 'native_exit': 0, 'completion_percent': 100}))
