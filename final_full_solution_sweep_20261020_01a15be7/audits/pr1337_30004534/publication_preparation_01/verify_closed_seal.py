# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Read-only complete-directory seal verifier, including nested manifests."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
m=json.loads((P/'MANIFEST.json').read_bytes())
want=m['files']
actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and p!=P/'MANIFEST.json'}
if actual!=set(want):raise RuntimeError('closed member-set mismatch')
for n,v in want.items():
 p=P/n
 if p.is_symlink():raise RuntimeError('symlink '+n)
 b=p.read_bytes()
 if len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise RuntimeError('sealed bytes '+n)
print(json.dumps({'status':'PASS','members':len(want),'bytes':sum(v['bytes'] for v in want.values()),'manifest_sha256':hashlib.sha256((P/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))
