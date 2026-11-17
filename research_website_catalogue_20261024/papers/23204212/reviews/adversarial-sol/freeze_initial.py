"""Seal only this owned INITIAL lane; never execute or modify source payloads."""
import hashlib
import json
import os
from pathlib import Path
import stat
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
TERMINALS = ('INITIAL_MANIFEST.json', 'INITIAL_SEAL.json')
assert ROOT.name == 'adversarial-sol'
assert ROOT.parent.parent.name == '23204212'
assert json.loads((ROOT / 'SOURCE_AFTER.json').read_text())['before_after_exact'] is True
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
file_count = sum(e['kind'] == 'file' for e in entries)
child_dirs = sum(e['kind'] == 'directory' for e in entries) - 1
manifest = {'schema': 'finite-initial-manifest-v1', 'UTC': stamp, 'root': str(ROOT),
            'file_count': file_count, 'child_directory_count': child_dirs,
            'directory_count_including_root': child_dirs + 1,
            'recursive_hash_exclusions': list(TERMINALS), 'entries': entries}
seal = {'schema': 'independent-initial-seal-v1', 'UTC': stamp, 'root': str(ROOT),
        'status': 'FROZEN_INITIAL_ONLY_PENDING_ROOT_CHECKPOINT_AND_EXPLICIT_RESUME',
        'initial_gate_completion_percent': 100, 'estimated_full_scientific_review_percent': 20,
        'file_count': file_count, 'child_directory_count': child_dirs,
        'source_before_after_exact': True, 'source_file_count': 55,
        'source_child_directory_count': 14,
        'source_final_sha256': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
        'source_manifest_sha256': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
        'original_tex_lines': 95, 'original_tex_bytes': 12344,
        'native_pdf_pages_text_read': 4, 'fresh_page_images_individually_viewed': 4,
        'support_scientific_payloads_read': 0, 'imported_primary_proof_bodies_read': 0,
        'source_scientific_execution_count': 0, 'scientific_verdict': None,
        'initial_manifest_sha256': '0' * 64}
def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
for attempt in range(20):
    manifest_bytes = encode(manifest)
    seal['initial_manifest_sha256'] = hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes = encode(seal)
    sizes = {'INITIAL_MANIFEST.json': len(manifest_bytes), 'INITIAL_SEAL.json': len(seal_bytes)}
    if all(e['bytes'] == sizes[e['path']] and e['empty'] is False
           for e in entries if e['path'] in TERMINALS):
        break
    for entry in entries:
        if entry['path'] in TERMINALS:
            entry.update(bytes=sizes[entry['path']], empty=False)
else:
    raise RuntimeError('Terminal size fixed point did not converge')
for name, data in [('INITIAL_MANIFEST.json', manifest_bytes), ('INITIAL_SEAL.json', seal_bytes)]:
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
assert hashlib.sha256((ROOT / 'INITIAL_MANIFEST.json').read_bytes()).hexdigest() == seal['initial_manifest_sha256']
print(json.dumps({'UTC': stamp, 'files': file_count, 'child_directories': child_dirs,
                  'root_mode': oct(stat.S_IMODE(ROOT.stat().st_mode)),
                  'terminal_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                      for name in TERMINALS}}, indent=2))
