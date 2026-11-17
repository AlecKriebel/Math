from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'

def load(p):
    return json.loads(p.read_text())

def h(p):
    return sha256(p.read_bytes()).hexdigest()

def tree(root):
    result = {}
    for p in [root] + sorted(root.rglob('*')):
        s = p.lstat()
        assert not stat.S_ISLNK(s.st_mode), p
        rel = p.relative_to(root).as_posix()
        row = {'kind': 'directory' if p.is_dir() else 'file',
               'mode': oct(stat.S_IMODE(s.st_mode))}
        if p.is_file():
            row.update(bytes=s.st_size, sha256=h(p))
        result[rel] = row
    return result

specs = [
    ('riesz-surface-editorial-sol-20261117', 'MANIFEST.json',
     '13164254fa6596772435ad817efacf99ab035bf418a07d601687f44846b50db6',
     '4d48b3304f6e1de25e53092ef489f9bb5f02259e26ad4c751df4146e16b5ef4d', 28, 1),
    ('riesz-surface-fact-sol-20261117', 'MANIFEST.json',
     'cdc48545930844c0b05e0349e67b4620171b14c65e3b6f4bd51eab90aa6b83ad',
     'd15b745ee1f651fe8ada00992b98f280fa800f88c2084575ddf17c83ddf853d8', 17, 0),
    ('riesz-surface-legacy-sol-20261117', 'FINAL_MANIFEST.json',
     'bfdbc49c8703d6b7c82f6a97c4a4fc8015850e2d987f7b8aaf608b0247f0ef14',
     '5e214952454f33de3f1e926cf9ee93377b21fd9fe8881547b2ca9f1cc87145f2', 113, 17),
]
results = []
for name, mf, mh, fh, nf, nd in specs:
    root = V / name
    assert h(root / mf) == mh
    assert h(root / 'FINAL.json') == fh
    d = load(root / mf)
    current = tree(root)
    controls = {mf, 'FINAL.json'}
    if name.startswith('riesz-surface-editorial'):
        rows = [{'path': '.', 'kind': 'directory', 'mode': d['root_mode']}]
        rows += [dict(r, kind='directory') for r in d['directories']]
        rows += [dict(r, kind='file', sha256=r['SHA256']) for r in d['payload_files']]
        rows += d['terminal_control_topology']
    else:
        rows = d['entries']
    assert set(current) == {r['path'] for r in rows}, name
    for r in rows:
        c = current[r['path']]
        assert c['kind'] == r['kind'], (name, r['path'], 'kind')
        assert c['mode'] == r.get('mode', r.get('mode_octal')), (name, r['path'], 'mode')
        if c['kind'] == 'file' and r['path'] not in controls:
            assert c['bytes'] == r['bytes'] and c['sha256'] == r['sha256'], (name, r['path'])
    files = sum(x['kind'] == 'file' for x in current.values())
    dirs = sum(x['kind'] == 'directory' for x in current.values()) - 1
    assert (files, dirs) == (nf, nd)
    results.append(dict(root=str(root.relative_to(P)), files=files, child_directories=dirs,
                        manifest=mf, manifest_sha256=mh, final_sha256=fh,
                        complete_fresh_tree=current))

snapshot = load(V / 'riesz-surface-fact-sol-20261117/BEFORE.json')['SOURCE']
source_root = Path(snapshot['root'])
source = tree(source_root)
assert set(source) == {r['path'] for r in snapshot['entries']}
for r in snapshot['entries']:
    c = source[r['path']]
    assert c['kind'] == r['kind'] and c['mode'] == r['mode']
    if c['kind'] == 'file':
        assert c['bytes'] == r['bytes'] and c['sha256'] == r['sha256']
assert sum(x['kind'] == 'file' for x in source.values()) == 39
assert sum(x['kind'] == 'directory' for x in source.values()) - 1 == 15
out = dict(schema='root-riesz-private-editorial-adoption-v1',
           UTC=datetime.now(timezone.utc).isoformat(), record_id='23202994', sheet_row=190,
           status='ACCEPTED_PRIVATE_COPY_ONLY',
           root_actual_reading='Entire actual article HEAD/BODY/MAIN, model, BibTeX, writer report, independent fact FINAL/report and legacy FINAL/report read personally. Scientific interpretation inherited from root full manuscript and supporting proof review, not an inventory assessment.',
           finite_authentication=results, source_full_exact=source,
           scope='Private copy accepted; future staging must use the current website baseline.',
           legacy_finding='No genuine correspondence in the three bounded inspected corpora; no global historical or live absence claim.',
           canonical_url=None, AA=None, publication_authority=False, follow_up=None)
target = V / 'root-riesz-surface-editorial-adoption-20261117.json'
assert not target.exists()
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'file': str(target), 'sha256': h(target),
                  'authenticated_files': 28 + 17 + 113 + 39, 'child_directories': 1 + 0 + 17 + 15}))
