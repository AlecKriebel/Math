"""Exact row177 opaque byte/mode/topology custody only, before science reading."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23205181/sources')
O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23205181/reviews/adversarial-sol')

def need(test, message):
    if not test: raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(info.st_mode)}

mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 15220, 'SHA256': '1ab94ae569aaaeb9f2c4be323a9a9729ca5f96e2b671478af8fc6d537c55c454', 'mode': 420}, 'Source manifest differs')
need(fp == {'bytes': 826, 'SHA256': '92ea655765128b7b1f538bee8c13ecbbc62058f8909ff3afdf3ce4787487a6c0', 'mode': 420}, 'Source FINAL differs')
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in manifest['files']}
need(len(expected) == len(manifest['files']), 'Duplicate source path')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
files, dirs = {}, {}
need(stat.S_ISDIR(S.lstat().st_mode), 'Nonordinary source root')
for path in S.rglob('*'):
    info = path.lstat()
    rel = path.relative_to(S).as_posix()
    if stat.S_ISREG(info.st_mode): files[rel] = pin(path)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Symlink/special source node')
        dirs[rel] = stat.S_IMODE(info.st_mode)
need(files == expected and len(files) == 69, 'Source bytes/modes/extent differ')
need(dirs == {x['path']: x['mode'] for x in manifest['directories']} and len(dirs) == 10, 'Source directory topology/modes differ')
need(stat.S_IMODE(S.stat().st_mode) == manifest['root_mode'] == 493, 'Source root mode differs')
receipt = {'schema': 'opaque-whole-source-authenticated-before-science-v1', 'UTC': datetime.now(timezone.utc).isoformat(),
    'record': 23205181, 'row': 177, 'SOURCE_MANIFEST': mp, 'SOURCE_FINAL': fp,
    'actual_files': 69, 'child_directories': 10, 'whole_buffers_modes_topology_match': True,
    'mathematical_manuscript_PDF_program_support_results_opinions_foreign_body_reading': False,
    'scientific_program_execution': False, 'source_namespace_modified': False,
    'publication_authority': False}
target = O / 'SOURCE_CUSTODY.json'
need(not target.exists(), 'Refusing repeated custody receipt')
target.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
