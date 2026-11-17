"""Exact opaque source custody only; read no mathematical text or program semantics."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/sources')
O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/reviews/adversarial-sol')

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary source node: '+str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

manifest_pin = pin(S/'SOURCE_MANIFEST.json')
final_pin = pin(S/'SOURCE_FINAL.json')
need(manifest_pin['bytes'] == 60052 and manifest_pin['SHA256'] == '3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b', 'Source manifest differs')
need(final_pin['bytes'] == 910 and final_pin['SHA256'] == '46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886', 'Source FINAL differs')
manifest = json.loads((S/'SOURCE_MANIFEST.json').read_bytes())
expected = {entry['path']: entry for entry in manifest['files']}
need(len(expected) == len(manifest['files']), 'Duplicate source manifest name')
expected.update({'SOURCE_MANIFEST.json': manifest_pin, 'SOURCE_FINAL.json': final_pin})
paths, directories = [], []
for path in S.rglob('*'):
    info = path.lstat()
    rel = str(path.relative_to(S))
    if stat.S_ISREG(info.st_mode):
        paths.append(rel)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Symlink or special source node: '+rel)
        directories.append(rel)
need(sorted(paths) == sorted(expected) and len(paths) == 196, 'Source regular-file extent differs')
need(sorted(directories) == sorted(x['path'] for x in manifest['directories']) and len(directories) == 21, 'Source directory extent differs')
need(oct(stat.S_IMODE(S.stat().st_mode)) == manifest['root_mode'], 'Source root mode differs')
for rel, entry in expected.items():
    path = S/rel
    need(path.resolve().is_relative_to(S.resolve()), 'Escaped source manifest path')
    actual = pin(path)
    need(all(actual[k] == entry[k] for k in ['bytes', 'SHA256', 'mode']), 'Source bytes or mode differ: '+rel)
for entry in manifest['directories']:
    need(oct(stat.S_IMODE((S/entry['path']).stat().st_mode)) == entry['mode'], 'Source directory mode differs')
receipt = {'schema': 'whole-source-first-custody-authentication-v1',
    'UTC': datetime.now(timezone.utc).isoformat(), 'record': 23411227, 'row': 172,
    'source_manifest': manifest_pin, 'source_FINAL': final_pin,
    'ordinary_files': len(paths), 'child_directories': len(directories),
    'all_actual_ignored_source_buffers_modes_and_topology_match': True,
    'source_namespaces_modified': False, 'scientific_semantic_reading_or_execution': False,
    'root_peer_archived_opinion_foreign_proof_and_native_code_bodies_read': False,
    'publication_authority': False}
out = O/'SOURCE_CUSTODY.json'
need(not out.exists(), 'Custody receipt already exists; refusing repeat')
out.write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt))
