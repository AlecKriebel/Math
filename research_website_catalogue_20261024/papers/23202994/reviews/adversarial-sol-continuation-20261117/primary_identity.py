"""Passive byte identity comparison against deposited source manifests."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'sources/archives/01-source-and-verification.zip.extracted/sources'
upstream = json.loads((SOURCE / 'UPSTREAM_MANIFEST.json').read_text())
prefixes = {
    'main': 'preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/',
    'atomic': 'preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026/',
}
expected = {r['path']: r for r in upstream['files']}
rows = []
for family, prefix in prefixes.items():
    base = ROOT / 'primary/openai' / family
    for path in sorted(base.rglob('*')):
        if not path.is_file():
            continue
        remote = prefix + path.relative_to(base).as_posix()
        record = expected[remote]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert (len(data), digest) == (record['bytes'], record['sha256']), remote
        rows.append({'local_path': path.relative_to(ROOT).as_posix(), 'repository_path': remote,
                     'commit': upstream['pinned_commit'], 'bytes': len(data), 'sha256': digest,
                     'matches_deposited_pin': True})

names = {
    'hardin_saff_0311024v3.pdf': 'hardin-saff-math-ph-0311024v3.pdf',
    'brauchart_hardin_saff_1202.4037v1.pdf': 'brauchart-hardin-saff-1202.4037v1.pdf',
    'brauchart_hardin_saff_235.pdf': 'brauchart-hardin-saff-235.pdf',
    'kuijlaars_saff_159.pdf': 'kuijlaars-saff-159.pdf',
}
classical = []
for record in json.loads((SOURCE / 'classical/SOURCE_MANIFEST.json').read_text())['files']:
    path = ROOT / 'primary' / names[record['file']]
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert (len(data), digest) == (record['size_bytes'], record['sha256']), path
    classical.append({'local_path': path.relative_to(ROOT).as_posix(), 'url': record['url'],
                      'edition_label': record['version'], 'bytes': len(data), 'sha256': digest,
                      'matches_deposited_pin': True})
target = ROOT / 'PRIMARY_IDENTITY.json'
assert not target.exists()
target.write_text(json.dumps({'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'upstream_commit': upstream['pinned_commit'], 'upstream_files': rows,
    'classical_pdfs': classical, 'network_retries': 0,
    'semantics': 'Byte identities only; no author opinion or mathematical conclusion authenticated.'}, indent=2) + '\n')
print(json.dumps({'upstream_files': len(rows), 'classical_pdfs': len(classical), 'all_match': True}))
