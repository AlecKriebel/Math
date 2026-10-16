#!/usr/bin/env python3
"""Build the explicit deterministic PR1047 authored support archive."""
import hashlib
import json
import pathlib
import stat
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / 'pr1047_supportkit_v1.0.zip'

def safe_file(name):
    path = pathlib.PurePosixPath(name)
    if path.is_absolute() or not path.parts or any(p in ('', '.', '..') for p in path.parts) or '\\' in name:
        raise ValueError('Unsafe member: ' + name)
    candidate = ROOT.joinpath(*path.parts)
    if any(p.is_symlink() for p in [candidate, *candidate.parents] if p != ROOT.parent):
        raise ValueError('Symlink member or ancestor: ' + name)
    if not candidate.is_file() or not stat.S_ISREG(candidate.stat().st_mode):
        raise ValueError('Nonregular member: ' + name)
    if candidate.resolve().is_relative_to(ROOT) is False:
        raise ValueError('Outside package: ' + name)
    return candidate

# Load a pinned local guard without relying on sys.path under isolated Python.
import importlib.util
spec = importlib.util.spec_from_file_location('pr1047_terminal_stage', ROOT / 'scripts/terminal_stage.py')
terminal_stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(terminal_stage)
terminal_stage.verify_terminal(ROOT)

names = json.loads((ROOT / 'ALLOWLIST.json').read_text())['members']
if names != sorted(set(names)) or 'MANIFEST.json' in names or 'zenodo-deposit.json' in names or any(n.endswith('.zip') for n in names):
    raise ValueError('Invalid explicit allowlist or circular member')
pins = json.loads((ROOT / 'TERMINAL_INPUT_PINS.json').read_text())
if pins['schema'] != 'pr1047-terminal-input-pins-v1' or pins['self_excluded'] is not True:
    raise RuntimeError('Invalid terminal input pins')
expected = []
for name in names:
    if name == 'TERMINAL_INPUT_PINS.json': continue
    data = safe_file(name).read_bytes()
    expected.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
if pins['files'] != expected:
    raise RuntimeError('Pinned terminal input bytes changed')
entries = []
for name in names:
    data = safe_file(name).read_bytes()
    entries.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
manifest = {'schema': 'pr1047-supportkit-1.0', 'hash_algorithm': 'SHA-256', 'members': names + ['MANIFEST.json'],
            'self_reference_policy': 'Manifest has no self-hash; terminal pins exclude only themselves; external proposed final seal/integrity and original preparation pins are outside ZIP.', 'stage':'terminal_two_clean_whole_reviews_administration', 'publication_ready':True, 'published':False, 'publication_sequence_hold':'preceding PR1032 priority cursor; services blocked', 'entries': entries}
(ROOT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_STORED) as archive:
    for name in sorted(names + ['MANIFEST.json']):
        data = safe_file(name).read_bytes()
        member = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
        member.create_system = 3
        member.external_attr = (stat.S_IFREG | 0o644) << 16
        member.compress_type = zipfile.ZIP_STORED
        archive.writestr(member, data)
with zipfile.ZipFile(ARCHIVE) as archive:
    if archive.testzip() is not None or archive.namelist() != sorted(names + ['MANIFEST.json']):
        raise RuntimeError('ZIP CRC or membership mismatch')
print(json.dumps({'archive': ARCHIVE.name, 'members': len(names) + 1, 'bytes': ARCHIVE.stat().st_size,
                  'sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), 'crc': 'PASS', 'deterministic': True}))
