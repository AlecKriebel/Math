"""Freeze only this owned finite factual-audit packet."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parent
TERMINALS = ('FINAL_MANIFEST.json', 'FINAL_SEAL.json')
assert ROOT.name == 'binary-gram-locus-editorial-fact-sol-20261117'
assert (ROOT / 'reader.exit.txt').read_text().strip() == '0'
assert json.loads((ROOT / 'CUSTODY_AFTER.json').read_text())['before_after_exact']
assert json.loads((ROOT / 'FINAL.json').read_text())['issues'] == []
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
    entry = {'path': relative, 'mode': oct(stat.S_IMODE(info.st_mode)), 'mtime_ns': info.st_mtime_ns,
             'hidden': any(p.startswith('.') for p in Path(relative).parts if p != '.')}
    if path.is_dir():
        entry.update(kind='directory', empty=not any(path.iterdir()))
    else:
        data = path.read_bytes()
        entry.update(kind='file', bytes=len(data), empty=not data,
                     SHA256=None if relative in TERMINALS else hashlib.sha256(data).hexdigest())
        if relative in TERMINALS:
            entry['recursive_content_hash_excluded'] = True
    entries.append(entry)
files = sum(e['kind'] == 'file' for e in entries)
dirs = sum(e['kind'] == 'directory' for e in entries) - 1
manifest = {'schema': 'finite-fact-audit-manifest-v1', 'UTC': stamp, 'root': str(ROOT),
            'files': files, 'child_directories': dirs,
            'only_recursive_content_hash_exclusions': list(TERMINALS), 'entries': entries}
seal = {'schema': 'private-fact-audit-final-seal-v1', 'UTC': stamp, 'root': str(ROOT),
        'status': 'PASS_PRIVATE_FACT_AUDIT_FROZEN_ROOT_ADOPTION_PENDING',
        'files': files, 'child_directories': dirs, 'completion_percent': 100,
        'source95_16_writer21_1_before_after_exact': True,
        'data_reader_attempts': 1, 'data_reader_exit': 0,
        'source_scientific_producer_helper_execution': 0,
        'publication_or_future_action_authority': False, 'follow_up': None,
        'FINAL_SHA256': hashlib.sha256((ROOT / 'FINAL.json').read_bytes()).hexdigest(),
        'report_SHA256': hashlib.sha256((ROOT / 'FACT_REPORT.md').read_bytes()).hexdigest(),
        'manifest_SHA256': '0' * 64}
def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
for attempt in range(20):
    manifest_bytes = encode(manifest)
    seal['manifest_SHA256'] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    sizes = {'FINAL_MANIFEST.json': len(manifest_bytes), 'FINAL_SEAL.json': len(seal_bytes)}
    if all(e['bytes'] == sizes[e['path']] and e['empty'] is False for e in entries if e['path'] in TERMINALS):
        break
    for entry in entries:
        if entry['path'] in TERMINALS:
            entry.update(bytes=sizes[entry['path']], empty=False)
else:
    raise RuntimeError('No terminal size fixed point')
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
    assert oct(stat.S_IMODE(info.st_mode)) == entry['mode'] and info.st_mtime_ns == entry['mtime_ns']
    if entry['kind'] == 'file':
        data = path.read_bytes()
        assert len(data) == entry['bytes'] and (not data) == entry['empty']
        if entry['SHA256'] is not None:
            assert hashlib.sha256(data).hexdigest() == entry['SHA256']
    else:
        assert (not any(path.iterdir())) == entry['empty']
assert hashlib.sha256((ROOT / 'FINAL_MANIFEST.json').read_bytes()).hexdigest() == seal['manifest_SHA256']
print(json.dumps({'UTC': stamp, 'files': files, 'child_directories': dirs,
                  'FINAL_SHA256': seal['FINAL_SHA256'], 'report_SHA256': seal['report_SHA256'],
                  'terminal_SHA256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in TERMINALS}}, indent=2))
