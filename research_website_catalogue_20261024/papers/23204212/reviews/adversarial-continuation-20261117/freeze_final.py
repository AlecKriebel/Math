"""Finite final custody seal of this new owned continuation only."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
TERMINALS = ('FINAL_MANIFEST.json', 'FINAL_SEAL.json')
assert ROOT.name == 'adversarial-continuation-20261117'
assert ROOT.parent.parent.name == '23204212'
guard = json.loads((ROOT / 'CUSTODY_AFTER.json').read_text())
assert guard['before_after_exact'] is True
native = json.loads((ROOT / 'NATIVE_RECEIPT.json').read_text())
assert native['native_attempt_number'] == 1 and native['exit_code'] == 0 and native['inputs_exact']
coverage = json.loads((ROOT / 'PRIMARY_COVERAGE.json').read_text())
assert coverage['actual_directory_files'] == coverage['main_internal_import_closure_files'] == 68
assert coverage['all_actual_directory_files_personally_read']
assert not any((ROOT / name).exists() for name in TERMINALS)
handles = {name: (ROOT / name).open('w+b') for name in TERMINALS}
freeze_ns = time.time_ns()
stamp = datetime.fromtimestamp(freeze_ns / 1e9, timezone.utc).isoformat()
objects = [ROOT] + sorted(ROOT.rglob('*'))
for path in objects:
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)
    os.chmod(path, 0o555 if path.is_dir() else 0o444)
    os.utime(path, ns=(freeze_ns, freeze_ns))
entries = []
for path in objects:
    info = path.lstat()
    relative = str(path.relative_to(ROOT))
    entry = {'path': relative, 'mode_octal': oct(stat.S_IMODE(info.st_mode)),
             'mtime_ns': info.st_mtime_ns}
    if path.is_dir():
        entry.update(kind='directory', empty=not any(path.iterdir()))
    else:
        data = path.read_bytes()
        entry.update(kind='file', bytes=len(data), empty=not data,
                     sha256=None if relative in TERMINALS else hashlib.sha256(data).hexdigest())
        if relative in TERMINALS:
            entry['recursive_content_hash_excluded'] = True
    entries.append(entry)
files = sum(e['kind'] == 'file' for e in entries)
childdirs = sum(e['kind'] == 'directory' for e in entries) - 1
manifest = {'schema': 'finite-private-continuation-manifest-v1', 'UTC': stamp, 'root': str(ROOT),
            'file_count': files, 'child_directory_count': childdirs,
            'directory_count_including_root': childdirs + 1,
            'recursive_content_hash_exclusions': list(TERMINALS), 'entries': entries}
seal = {'schema': 'private-continuation-final-seal-v1', 'UTC': stamp, 'root': str(ROOT),
        'status': 'FROZEN_COMPLETE_PRIVATE_REVIEW_ROOT_ADOPTION_PENDING',
        'file_count': files, 'child_directory_count': childdirs,
        'authorized_bounded_review_completion_percent': 100,
        'estimated_complete_independently_reproducible_verification_percent': 95,
        'protected_before_after_exact': True,
        'protected_roots': {label: {k: v for k, v in value.items() if k != 'entries'}
                            for label, value in guard['roots'].items()},
        'protected_after_guard_sha256': hashlib.sha256((ROOT / 'CUSTODY_AFTER.json').read_bytes()).hexdigest(),
        'actual_upstream_primary_pdf_pages_read': 13,
        'actual_upstream_lean_files_personally_read': 68,
        'actual_upstream_lean_lines': 9457, 'actual_upstream_lean_bytes': 372798,
        'native_unmodified_finite_route_attempts': 1, 'native_exit_code': 0,
        'fresh_lean_kernel_build_attempts': 0,
        'root_or_peer_current_scientific_reports_read': 0,
        'report_sha256': hashlib.sha256((ROOT / 'FINAL_REPORT.md').read_bytes()).hexdigest(),
        'followup': None, 'publication_or_mutation_authority': None,
        'final_manifest_sha256': '0' * 64}
def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
for attempt in range(20):
    manifest_bytes = encode(manifest)
    seal['final_manifest_sha256'] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    sizes = {'FINAL_MANIFEST.json': len(manifest_bytes), 'FINAL_SEAL.json': len(seal_bytes)}
    if all(e['bytes'] == sizes[e['path']] and e['empty'] is False
           for e in entries if e['path'] in TERMINALS):
        break
    for entry in entries:
        if entry['path'] in TERMINALS:
            entry.update(bytes=sizes[entry['path']], empty=False)
else:
    raise RuntimeError('Terminal size fixed point did not converge')
for name, data in [('FINAL_MANIFEST.json', manifest_bytes), ('FINAL_SEAL.json', seal_bytes)]:
    handle = handles[name]
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
    handle.close()
    os.utime(ROOT / name, ns=(freeze_ns, freeze_ns))
assert [str(p.relative_to(ROOT)) for p in [ROOT] + sorted(ROOT.rglob('*'))] == [e['path'] for e in entries]
for entry in entries:
    path = ROOT / entry['path']
    info = path.lstat()
    assert oct(stat.S_IMODE(info.st_mode)) == entry['mode_octal']
    assert info.st_mtime_ns == entry['mtime_ns']
    if entry['kind'] == 'file':
        data = path.read_bytes()
        assert len(data) == entry['bytes'] and (not data) == entry['empty']
        if entry['sha256'] is not None:
            assert hashlib.sha256(data).hexdigest() == entry['sha256']
    else:
        assert (not any(path.iterdir())) == entry['empty']
assert hashlib.sha256((ROOT / 'FINAL_MANIFEST.json').read_bytes()).hexdigest() == seal['final_manifest_sha256']
print(json.dumps({'UTC': stamp, 'files': files, 'child_directories': childdirs,
                  'root_mode': oct(stat.S_IMODE(ROOT.stat().st_mode)),
                  'report_sha256': seal['report_sha256'],
                  'terminal_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                      for name in TERMINALS}}, indent=2))
