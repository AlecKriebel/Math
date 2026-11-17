"""Passive finite custody only; never imports or runs any project source."""
from pathlib import Path
import datetime, hashlib, json, stat, sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
L = P / 'verification/thompson-cstar-editorial-sol-20261117'
S = P / 'papers/23204212/sources'
PINNED = {
    S / 'SOURCE_FINAL.json': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
    S / 'SOURCE_MANIFEST.json': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
    P / 'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md': '71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501',
    P / 'verification/root-clearance-23204212-20261117.json': 'cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c',
    Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/research.css'): 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a',
}

def row(path, relative):
    st = path.lstat()
    r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode))}
    if stat.S_ISDIR(st.st_mode):
        r.update(kind='directory', empty=not any(path.iterdir()))
    else:
        assert stat.S_ISREG(st.st_mode), ('unexpected node kind', str(path))
        b = path.read_bytes()
        r.update(kind='file', bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), md5=hashlib.md5(b).hexdigest())
    return r

assert len(sys.argv) == 2 and sys.argv[1] in ('before', 'after')
phase = sys.argv[1]
out = L / ('CUSTODY_' + phase.upper() + '.json')
assert not out.exists(), ('refuse overwrite', str(out))
paths = [S] + sorted(S.rglob('*'), key=lambda p: p.relative_to(S).as_posix())
entries = [row(p, '.' if p == S else p.relative_to(S).as_posix()) for p in paths]
files = sum(r['kind'] == 'file' for r in entries)
dirs = sum(r['kind'] == 'directory' for r in entries) - 1
assert (files, dirs) == (55, 14), (files, dirs)
specific = []
for p, sha in PINNED.items():
    r = row(p, str(p))
    assert r['sha256'] == sha, ('pinned input mismatch', str(p), r['sha256'])
    specific.append(r)
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
assert manifest['excluded_control_files'] == ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json']
payload = [r for r in entries if r['path'] not in manifest['excluded_control_files']]
assert payload == manifest['entries'], 'source finite manifest differs'
if phase == 'after':
    before = json.loads((L / 'CUSTODY_BEFORE.json').read_text())
    assert entries == before['source_entries'], 'source input bytes/modes/topology changed'
    assert specific == before['specific_inputs'], 'specific editorial inputs changed'
result = {
    'schema': 'thompson-editorial-passive-custody-v1',
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'phase': phase, 'source_root': str(S), 'source_files': files,
    'source_child_directories': dirs, 'source_entries': entries,
    'specific_inputs': specific, 'source_manifest_exact': True,
    'before_after_exact': True if phase == 'after' else None,
    'scope_excludes': ['moving P as a whole', 'W except exact shared CSS input', 'Git/native/index/refs', 'other editorial or scientific packets'],
}
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'phase': phase, 'source_files': files, 'source_child_directories': dirs, 'source_manifest_exact': True, 'before_after_exact': result['before_after_exact'], 'receipt': str(out)}))
