"""Data-only full source/INITIAL custody snapshots; no scientific imports."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'papers/23204176/reviews/scope-sol-continuation-20261117'
SOURCE = P / 'papers/23204176/sources'
INITIAL = P / 'papers/23204176/reviews/scope-sol'
PINS = {SOURCE / 'SOURCE_MANIFEST.json': '53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb',
        SOURCE / 'SOURCE_FINAL.json': 'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8',
        INITIAL / 'INITIAL_MANIFEST.json': '15b2e64dd6cdd843fd5ebfe38eb5aa3c11dbb711a9f724b65e037bf91eb44984',
        INITIAL / 'INITIAL_SEAL.json': 'e2e5b09208be50b17cf92ad91808cad8957facc26c36a4baa8b440f5917c3a11'}


def need(value, label):
    if not value:
        raise AssertionError(label)


def inventory(root):
    rows = []
    def visit(path):
        s = path.lstat()
        rel = path.relative_to(root).as_posix()
        row = {'path': rel, 'mode_octal': oct(stat.S_IMODE(s.st_mode)),
               'hidden_component': any(p.startswith('.') and p != '.' for p in Path(rel).parts)}
        if stat.S_ISDIR(s.st_mode):
            children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
            row.update(kind='directory', empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        else:
            need(stat.S_ISREG(s.st_mode), 'regular source/INITIAL objects only')
            data = path.read_bytes()
            row.update(kind='file', bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), md5=hashlib.md5(data).hexdigest())
            rows.append(row)
    visit(root)
    return rows


phase = sys.argv[1]
need(phase in ('before', 'after'), 'explicit data phase')
result = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'entries': {}}
for path, expected in PINS.items():
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'immutable terminal pin ' + str(path))
for root, manifest_name, files, childdirs, terminals in [
    (SOURCE, 'SOURCE_MANIFEST.json', 43, 7, {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}),
    (INITIAL, 'INITIAL_MANIFEST.json', 30, 0, {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'})
]:
    rows = inventory(root)
    need(sum(r['kind'] == 'file' for r in rows) == files, 'whole file count')
    need(sum(r['kind'] == 'directory' for r in rows) == childdirs + 1, 'whole directory count')
    actual = {r['path']: r for r in rows}
    manifest = json.loads((root / manifest_name).read_bytes())
    expected = {r['path']: r for r in manifest['entries']}
    need(set(actual) == set(expected) | terminals, 'whole finite actual topology')
    for path, row in expected.items():
        for key, value in row.items():
            if key != 'terminal_control':
                need(actual[path][key] == value, 'actual manifest field ' + path + ' ' + key)
    need(all(actual[p]['kind'] == 'file' and actual[p]['mode_octal'] == '0o644' for p in terminals), 'exact terminal topology')
    result['entries'][str(root)] = rows
if phase == 'after':
    old = json.loads((OWN / 'CUSTODY_BEFORE.json').read_bytes())
    need(result['entries'] == old['entries'], 'whole source and old INITIAL before/after exact')
    result['whole_before_after_exact'] = True
target = OWN / ('CUSTODY_' + phase.upper() + '.json')
need(not target.exists(), 'fresh own snapshot')
target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps({'phase': phase, 'source_files': 43, 'source_childdirs': 7, 'INITIAL_files': 30,
                  'INITIAL_childdirs': 0, 'exact': True, 'snapshot_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))
