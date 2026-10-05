#!/usr/bin/env python3
"""Check the complete public audit allowlist and all byte identities."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'MANIFEST.json').read_text())
expected={r['path']:r for r in m['files']}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json' and '__pycache__' not in p.parts}
assert actual==set(expected),{'missing':sorted(set(expected)-actual),'extra':sorted(actual-set(expected))}
for name,row in expected.items():
 p=root/name;assert not p.is_symlink();b=p.read_bytes()
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],name
assert all(Path(n).suffix in {'.md','.json','.py'} for n in actual)
assert not any(any(x in Path(n).parts for x in ['private','private_sources','__pycache__']) for n in actual)
print(json.dumps({'status':'PASS','files_checked':len(expected),'scope':'Audit package byte identity and allowlist only.'},sort_keys=True))
