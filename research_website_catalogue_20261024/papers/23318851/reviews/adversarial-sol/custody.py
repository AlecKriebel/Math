"""Passive complete source-custody reader; no scientific imports or source execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23318851/sources'
A = P / 'papers/23318851/reviews/adversarial-sol'
EXCLUDED = {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def snap():
    rows = []
    for p in [S, *sorted(S.rglob('*'))]:
        st = p.lstat()
        r = {'path': '.' if p == S else str(p.relative_to(S)),
             'mode_octal': oct(stat.S_IMODE(st.st_mode)),
             'hidden': any(x.startswith('.') for x in p.relative_to(S).parts)}
        if stat.S_ISDIR(st.st_mode):
            r.update(kind='directory', empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b = p.read_bytes()
            r.update(kind='file', bytes=len(b), sha256=sha(b), md5=hashlib.md5(b).hexdigest())
        else:
            r.update(kind='other', target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows

assert sha((S / 'SOURCE_FINAL.json').read_bytes()) == 'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'
assert sha((S / 'SOURCE_MANIFEST.json').read_bytes()) == 'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8'
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
assert set(manifest['excluded_control_files']) == EXCLUDED
assert manifest['file_count'] == 93 and manifest['directory_count'] == 17
rows = snap()
assert sum(r['kind'] == 'file' for r in rows) == 95
assert sum(r['kind'] == 'directory' for r in rows) == 17
assert not any(r['kind'] == 'other' for r in rows)
actual = {r['path']: r for r in rows if r['path'] not in EXCLUDED}
expected = {r['path']: r for r in manifest['entries']}
assert set(actual) == set(expected)
for name, entry in expected.items():
    assert all(actual[name].get(k) == v for k, v in entry.items()), name
assert sha((S / 'zenodo-files/gram_locus_note.pdf').read_bytes()) == 'ac0839eae1d0e83e0c47d3c840968363ce9271c83cc9ee88156197601b4d0018'
target = sys.argv[1]
assert target in ['CUSTODY_BEFORE.json', 'CUSTODY_AFTER.json']
assert not (A / target).exists()
if target == 'CUSTODY_AFTER.json':
    before = json.loads((A / 'CUSTODY_BEFORE.json').read_text())
    assert before['entries'] == rows
data = {'UTC': datetime.now(timezone.utc).isoformat(), 'source': str(S),
        'files': 95, 'child_directories': 16, 'source_manifest_authenticated': True,
        'all_actual_bytes_modes_hidden_empty_topology': True,
        'before_after_exact': target == 'CUSTODY_AFTER.json', 'entries': rows}
(A / target).write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({k: v for k, v in data.items() if k != 'entries'}))
