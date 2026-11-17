"""Authenticate four frozen packets and record bounded root stage acceptance."""
from pathlib import Path
import hashlib, json, stat
from datetime import datetime, timezone

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
sha = lambda b: hashlib.sha256(b).hexdigest()
packets = [
 ('mink-riesz-k3-stage-sol-20261117', 'OWNED_MANIFEST.json', '2aa8bb250f77212d60903f69f64390f86a8ce7544218453b2d169c957d8e588f', 'cd6b884ff5efce7c5873307cdc7bf308b72c801c3ba5868660ba261dcc22c8dc', 1635, 770),
 ('mink-riesz-k3-stage-audit-sol-20261117', 'MANIFEST.json', '3dab7883aaf53c71b8afcb49a5599fb0ead3d54d87e2c5d1a4d17919e2a37e04', 'ab248a8f6e16c18bf2e6c2fee3b6df674c2c05ca731a06cf82498c647452f945', 28, 0),
 ('mink-riesz-k3-stage-audit-continuation-sol-20261117', 'MANIFEST.json', '2dcda99d4e5577405d9fefceb4efdab9d3f895998dbe868d897f2f3c6660c7f6', '11f217ddb3065106e0c1b6692ba7dbe7f923d3f1999c679bbcaaa2a6f19991e2', 30, 0),
 ('mink-riesz-k3-stage-audit-html-fragments-sol-20261117', 'MANIFEST.json', 'f8207dd322c76addc52bafa3b5472a268f4d6924fce7ea38bdc64036bc82a4a0', '8e46e120ca55158bc9e623bb4348263591ac75d405393ff1b85e1b746092f517', 22, 0),
]
authenticated = []
for name, manifest_name, final_sha, manifest_sha, nf, nd in packets:
    base = P / 'verification' / name
    assert sha((base / 'FINAL.json').read_bytes()) == final_sha
    assert sha((base / manifest_name).read_bytes()) == manifest_sha
    m = json.loads((base / manifest_name).read_bytes())
    files, dirs = {}, {'.': base}
    for f in base.rglob('*'):
        assert not f.is_symlink(), f
        if f.is_file(): files[f.relative_to(base).as_posix()] = f
        elif f.is_dir(): dirs[f.relative_to(base).as_posix()] = f
        else: raise AssertionError(f)
    assert (len(files), len(dirs)-1) == (nf, nd)
    rows = {r['path']: r for r in m['payload_files']}
    assert set(files) == set(rows) | {manifest_name, 'FINAL.json'}
    for rel, row in rows.items():
        f = files[rel]; data = f.read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['SHA256'], f
        assert f'{stat.S_IMODE(f.stat().st_mode):04o}' == row['mode'], f
    declared_dirs = {r['path']: r for r in m['directories']}
    assert set(dirs) == set(declared_dirs)
    for rel, f in dirs.items():
        assert f'{stat.S_IMODE(f.stat().st_mode):04o}' == declared_dirs[rel]['mode'], f
    for rel in [manifest_name, 'FINAL.json']:
        assert f'{stat.S_IMODE(files[rel].stat().st_mode):04o}' == '0644'
    authenticated.append({'path': str(base), 'files': nf, 'child_directories': nd,
                          'FINAL_SHA256': final_sha, 'manifest_SHA256': manifest_sha})
result = {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'ACCEPTED_PRIVATE_STAGE_ONLY',
          'authenticated_packets': authenticated, 'actual_root_reading':
          ['whole 435-line builder, PLAN, REPORT, FINAL', 'all HEAD and aggregate closed spans',
           'third audit actual REPORT, FINAL, CRITERIA and static branch review',
           'both failed audit actual failure/closure reports and dispositions'],
          'accepted_projection': '13A2M,15 Git paths,6 new directories;803 files/387 directories/133 articles/134 sitemap entries',
          'history': 'Builder0, first metadata seal1, distinct metadata seal0; independent audits1,1,0. Earlier failures remain failures.',
          'stage_percent': 100, 'scientific_reviewed': 142, 'goal_active_incomplete': True,
          'actual_UI': False, 'publication_certificate': False, 'AA': None, 'future_action_authority': False}
out = P / 'verification/root-mink-riesz-k3-stage-adoption-20261117.json'
with out.open('x') as f: json.dump(result, f, indent=2); f.write('\n')
print(json.dumps(result))
