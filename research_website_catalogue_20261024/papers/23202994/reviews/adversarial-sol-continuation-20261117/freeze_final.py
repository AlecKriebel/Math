"""Finite local custody seal; no scientific execution or source mutation."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
TERMINALS = ('FINAL_MANIFEST.json', 'FINAL_SEAL.json')
def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
def sha(data):
    return hashlib.sha256(data).hexdigest()
def digest(path):
    return sha(path.read_bytes())
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

# Independently recheck the entire two immutable namespaces at final closure.
after_path = ROOT / 'GUARDS_AFTER.json'
before_path = ROOT / 'GUARDS_BEFORE.json'
after = json.loads(after_path.read_text())
before = json.loads(before_path.read_text())
checks = []
for record in after['roots']:
    label = record['label']
    baseline = next(x for x in before['roots'] if x['label'] == label)
    assert record['entries'] == baseline['entries'] and record['before_after_exact']
    base = Path(record['root'])
    paths = [base, *sorted(base.rglob('*'))]
    actual_names = {'.' if p == base else p.relative_to(base).as_posix() for p in paths}
    assert actual_names == {x['path'] for x in record['entries']}
    for row in record['entries']:
        path = base if row['path'] == '.' else base / row['path']
        info = path.lstat()
        assert oct(stat.S_IMODE(info.st_mode)) == row['mode']
        if row['kind'] == 'file':
            assert stat.S_ISREG(info.st_mode)
            data = path.read_bytes()
            assert len(data) == row['bytes'] and sha(data) == row['sha256']
        else:
            assert stat.S_ISDIR(info.st_mode) and (not any(path.iterdir())) == row['empty']
    checks.append({'label': label, 'root': str(base), 'files': record['files'],
                   'child_directories': record['child_directories'], 'full_exact_guard': True,
                   'inventory_sha256': sha(encoded(record['entries']))})
closure = ROOT / 'FINAL_EXACT_GUARDS.json'
assert not closure.exists()
closure.write_bytes(encoded({'UTC': now(), 'before_sha256': digest(before_path),
    'after_sha256': digest(after_path), 'independent_final_recheck': checks,
    'source_and_old_initial_writes': 0}))

receipt = ROOT / 'CODE_READ_RECEIPTS.json'
assert not receipt.exists()
receipt.write_bytes(encoded({'UTC': now(), 'programs': [
    {'path': name, 'sha256': digest(ROOT / name), 'complete_body_personally_read_before_execution': True}
    for name in ['custody_guard.py', 'primary_identity.py', 'native_run_once.py', 'freeze_final.py']],
    'scientific_native_attempts': 1, 'other_program_roles': 'passive custody/identity and one native execution recorder'}))

freeze_ns = time.time_ns()
stamp = now()
with (ROOT / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('- ' + stamp + ': Final full source39/15 and old INITIAL20/0 byte/mode/hidden/empty/topology rechecks match entry guards. The finite continuation is complete and frozen with all actual local primary/native files included. Review100%; audited-chain assessment95%; publication completion is not assessed. One native route only; follow_up:null. STOP.\n')
result_path = ROOT / 'RESULT.json'
result = json.loads(result_path.read_text())
result['review_status'] = 'complete; frozen final packet'
result['completed_utc'] = stamp
result_path.write_bytes(encoded(result))

handles = {}
for name in TERMINALS:
    handles[name] = (ROOT / name).open('xb')
paths = [ROOT, *sorted(ROOT.rglob('*'))]
for path in paths:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), path
for path in paths:
    if path.is_file():
        path.chmod(0o444)
for path in sorted(paths, key=lambda p: len(p.parts), reverse=True):
    if path.is_dir():
        path.chmod(0o555)

entries = []
for path in [ROOT, *sorted(ROOT.rglob('*'))]:
    info = path.lstat()
    relative = '.' if path == ROOT else path.relative_to(ROOT).as_posix()
    kind = 'directory' if path.is_dir() else 'file'
    row = {'path': relative, 'kind': kind, 'mode': oct(stat.S_IMODE(info.st_mode)),
           'hidden': any(p.startswith('.') and p not in ('.', '..') for p in Path(relative).parts),
           'mtime_ns': info.st_mtime_ns}
    if kind == 'directory':
        row['empty'] = not any(path.iterdir())
    elif relative in TERMINALS:
        row.update(bytes=0, sha256=None, empty=False, mtime_ns=freeze_ns,
                   content_hash_excluded=True, reason='Only the already-created recursive terminal pair hashes are excluded.')
    else:
        data = path.read_bytes()
        row.update(bytes=len(data), sha256=sha(data), empty=(not data))
    entries.append(row)
counts = {'files': sum(r['kind'] == 'file' for r in entries),
          'child_directories': sum(r['kind'] == 'directory' for r in entries) - 1,
          'hidden_files': sum(r['kind'] == 'file' and r['hidden'] for r in entries),
          'empty_files': sum(r['kind'] == 'file' and r['empty'] for r in entries),
          'empty_directories': sum(r['kind'] == 'directory' and r['empty'] for r in entries)}
manifest = {'schema': 'finite-actual-continuation-v1', 'root': str(ROOT), 'frozen_utc': stamp,
            'scope': 'Entire actual owned continuation, including hidden/ignored primary copies, native copy, literal empty streams, and all directories.',
            'hash_exclusions': list(TERMINALS), 'counts': counts, 'entries': entries}
sizes = {name: 0 for name in TERMINALS}
for attempt in range(20):
    for row in entries:
        if row['path'] in TERMINALS:
            row['bytes'] = sizes[row['path']]
    manifest_bytes = encoded(manifest)
    seal = {'schema': 'finite-actual-continuation-seal-v1', 'root': str(ROOT),
            'frozen_utc': stamp, 'manifest_sha256': sha(manifest_bytes), 'counts': counts,
            'terminal_sizes': sizes, 'root_mode': '0o555', 'file_modes': '0o444',
            'source_and_old_initial_exact_guard': digest(closure),
            'native_execution_receipt_sha256': digest(ROOT / 'NATIVE_RUN.json'),
            'native_attempts': 1, 'full_actual_scope_including_ignored': True,
            'recursive_content_hash_exclusions_only': list(TERMINALS),
            'review_completion_percent': 100, 'audited_chain_estimate_percent': 95,
            'follow_up': None, 'stop_after_seal': True}
    seal_bytes = encoded(seal)
    new_sizes = {TERMINALS[0]: len(manifest_bytes), TERMINALS[1]: len(seal_bytes)}
    if new_sizes == sizes:
        break
    sizes = new_sizes
else:
    raise AssertionError('terminal size fixed point did not converge')
handles[TERMINALS[0]].write(manifest_bytes)
handles[TERMINALS[1]].write(seal_bytes)
for stream in handles.values():
    stream.flush()
    os.fsync(stream.fileno())
    stream.close()
for name in TERMINALS:
    os.utime(ROOT / name, ns=(freeze_ns, freeze_ns))

# Verify the final actual tree after closing the last writable descriptors.
actual_paths = [ROOT, *sorted(ROOT.rglob('*'))]
assert len(actual_paths) == len(entries)
for row, path in zip(entries, actual_paths):
    info = path.lstat()
    assert oct(stat.S_IMODE(info.st_mode)) == row['mode']
    assert info.st_mtime_ns == row['mtime_ns']
    if row['kind'] == 'file':
        data = path.read_bytes()
        assert len(data) == row['bytes'] and (not data) == row['empty']
        if row['sha256'] is not None:
            assert sha(data) == row['sha256']
    else:
        assert (not any(path.iterdir())) == row['empty']
assert digest(ROOT / TERMINALS[0]) == seal['manifest_sha256']
print(json.dumps({'frozen_utc': stamp, 'counts': counts,
    'FINAL_MANIFEST_sha256': digest(ROOT / TERMINALS[0]),
    'FINAL_SEAL_sha256': digest(ROOT / TERMINALS[1]),
    'guards': checks, 'all_files_0444_all_directories_0555': True, 'stop': True}))
