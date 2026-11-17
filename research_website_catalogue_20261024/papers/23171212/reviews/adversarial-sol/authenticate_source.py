"""Opaque whole-source byte/mode/topology authentication for exactly row 175."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23171212/sources')
O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23171212/reviews/adversarial-sol')

def need(test, text):
    if not test:
        raise RuntimeError(text)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

fp = pin(S / 'SOURCE_FINAL.json')
mp = pin(S / 'SOURCE_MANIFEST.json')
need(fp == {'bytes': 909, 'SHA256': '4aaaf545371268d0e4e3014e5ac11498c8482b792581e7afa95fae9412adbb61', 'mode': '0o644'}, 'Source FINAL differs')
need(mp == {'bytes': 20723, 'SHA256': '842831f3bfeb0d75d810d18fe30dad582d0e2615c5c7db2252d68db4c2aaf428', 'mode': '0o644'}, 'Source manifest differs')
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in manifest['files']}
need(len(expected) == len(manifest['files']), 'Duplicate manifest name')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
actual, dirs = {}, {}
need(stat.S_ISDIR(S.lstat().st_mode), 'Nonordinary source root')
for path in S.rglob('*'):
    rel = path.relative_to(S).as_posix()
    info = path.lstat()
    if stat.S_ISREG(info.st_mode):
        actual[rel] = pin(path)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Symlink/special node: ' + rel)
        dirs[rel] = oct(stat.S_IMODE(info.st_mode))
need(len(actual) == 87 and actual == expected, 'Source bytes/modes/extent differ')
need(len(dirs) == 5 and dirs == {x['path']: x['mode'] for x in manifest['directories']}, 'Source directories/modes differ')
need(oct(stat.S_IMODE(S.stat().st_mode)) == manifest['root_mode'], 'Source root mode differs')
receipt = {'schema': 'opaque-before-science-source-authentication-v1',
    'UTC': datetime.now(timezone.utc).isoformat(), 'record': 23171212, 'row': 175,
    'SOURCE_FINAL': fp, 'SOURCE_MANIFEST': mp, 'source_files': 87, 'source_child_directories': 5,
    'all_buffers_modes_topology_authenticated': True, 'semantic_mathematical_body_reading': False,
    'scientific_program_execution': False, 'root_peer_archived_support_foreign_bodies_opened': False,
    'source_namespace_modified': False, 'publication_authority': False}
target = O / 'SOURCE_CUSTODY.json'
need(not target.exists(), 'Refusing repeat receipt')
target.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
