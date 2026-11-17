"""Exact row184 opaque metadata-only custody before scientific reading."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/22983519/sources'
O = P / 'papers/22983519/reviews/adversarial-sol'

def need(ok, message):
    if not ok: raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary source file')
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(info.st_mode)}

mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp == {'bytes': 17481, 'SHA256': 'e05b1df4559bac1a55fac1cfbda2a6aa6428d675e0ce7fbf708766037d425ace', 'mode': 420}, 'Source manifest differs')
need(fp == {'bytes': 826, 'SHA256': '7449712c5c396fde640b7497b20f97fb174593071fce71ca80ff763a23df4954', 'mode': 420}, 'Source FINAL differs')
m = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in m['files']}
need(len(expected) == len(m['files']) == 69, 'Source duplicate/extent')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
files, dirs = {}, {}
need(stat.S_ISDIR(S.lstat().st_mode), 'Nonordinary source root')
for path in sorted(S.rglob('*')):
    info = path.lstat()
    rel = path.relative_to(S).as_posix()
    if stat.S_ISREG(info.st_mode): files[rel] = pin(path)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Symlink/special source node')
        dirs[rel] = stat.S_IMODE(info.st_mode)
need(files == expected and len(files) == 71, 'Source whole buffers/modes/extent differ')
need(dirs == {x['path']: x['mode'] for x in m['directories']} and len(dirs) == 14, 'Source topology differs')
need(stat.S_IMODE(S.stat().st_mode) == m['root_mode'] == 493, 'Source root mode differs')
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
need([x['key'] for x in ready['native_assets']] == ['SHA256SUMS.txt', 'source-and-verification.zip', 'paper.pdf'], 'Native order differs')
for asset in ready['native_assets']:
    path = Path(asset['path'])
    need(path.parent == S / 'assets', 'Asset outside source')
    need(pin(path)['bytes'] == asset['bytes'] and pin(path)['SHA256'] == asset['SHA256'], 'Native asset differs')
    need(hashlib.md5(path.read_bytes()).hexdigest() == asset['MD5'], 'Native MD5 differs')
receipt = {'schema': 'source-whole-custody-before-science-v1', 'UTC': datetime.now(timezone.utc).isoformat(),
    'row': 184, 'record': 22983519, 'SOURCE_MANIFEST': mp, 'SOURCE_FINAL': fp,
    'whole_source_files': 71, 'child_directories': 14, 'buffers_modes_topology_match': True,
    'all_three_native_size_MD5_SHA256_verified': True,
    'scientific_manuscript_PDF_program_opinions_foreign_bodies_read_before_receipt': False,
    'source_namespace_modified': False, 'publication_authority': False}
target = O / 'SOURCE_CUSTODY.json'
need(not target.exists(), 'Refusing repeated custody')
target.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
