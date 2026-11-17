"""Passive complete custody guards for original source and frozen INITIAL."""
import hashlib
import json
from pathlib import Path
import stat
import sys
from datetime import datetime, timezone

LANE = Path(__file__).resolve().parent
PAPER = LANE.parent.parent
SOURCE = PAPER / 'sources'
INITIAL = LANE.parent / 'adversarial-sol'
PINS = {
    'source': {'SOURCE_FINAL.json': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
               'SOURCE_MANIFEST.json': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be'},
    'initial': {'INITIAL_SEAL.json': '1736dd12f41d54b4b1177114d1c4f5e47400ff9e8d48f66616ff8a86ded6cda7',
                'INITIAL_MANIFEST.json': '25ce42f37df872ba62a7bd5e33d017133217e1e1854735a48f7c439ee3a13590'},
}

def inventory(root):
    entries = []
    for path in [root] + sorted(root.rglob('*')):
        info = path.lstat()
        entry = {'path': str(path.relative_to(root)), 'mode_octal': oct(stat.S_IMODE(info.st_mode)),
                 'mtime_ns': info.st_mtime_ns}
        if stat.S_ISDIR(info.st_mode):
            entry.update(kind='directory', empty=not any(path.iterdir()))
        elif stat.S_ISREG(info.st_mode):
            data = path.read_bytes()
            entry.update(kind='file', bytes=len(data), empty=not data,
                         sha256=hashlib.sha256(data).hexdigest(), md5=hashlib.md5(data).hexdigest())
        else:
            raise RuntimeError('Unexpected source topology: ' + str(path))
        entries.append(entry)
    return entries

phase = sys.argv[1]
assert phase in ('before', 'after')
result = {'UTC': datetime.now(timezone.utc).isoformat(), 'phase': phase, 'roots': {}}
for label, root, files, childdirs, manifest_name in [
    ('source', SOURCE, 55, 14, 'SOURCE_MANIFEST.json'),
    ('initial', INITIAL, 18, 0, 'INITIAL_MANIFEST.json')]:
    entries = inventory(root)
    actual = {entry['path']: entry for entry in entries}
    assert sum(e['kind'] == 'file' for e in entries) == files
    assert sum(e['kind'] == 'directory' for e in entries) - 1 == childdirs
    for name, digest in PINS[label].items():
        assert actual[name]['sha256'] == digest, (label, name)
    manifest = json.loads((root / manifest_name).read_text())
    assert {e['path'] for e in manifest['entries']} | set(PINS[label]) == set(actual)
    for expected in manifest['entries']:
        observed = actual[expected['path']]
        for key in ('kind', 'mode_octal', 'empty', 'bytes', 'sha256', 'md5', 'mtime_ns'):
            if key in expected and expected[key] is not None:
                assert observed[key] == expected[key], (label, expected['path'], key)
    result['roots'][label] = {'path': str(root), 'file_count': files,
                             'child_directory_count': childdirs, 'pins': PINS[label],
                             'manifest_exact': True, 'entries': entries}
if phase == 'after':
    previous = json.loads((LANE / 'CUSTODY_BEFORE.json').read_text())
    assert previous['roots'] == result['roots'], 'Protected custody changed'
    result['before_after_exact'] = True
(LANE / ('CUSTODY_' + phase.upper() + '.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'UTC': result['UTC'], 'phase': phase, 'protected': {
    label: {k: v for k, v in data.items() if k != 'entries'}
    for label, data in result['roots'].items()},
    'before_after_exact': result.get('before_after_exact')}, indent=2))
