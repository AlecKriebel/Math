#!/usr/bin/env python3
"""Self-exclusion hash manifest of all first-party audit files, or verify it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
NAME='MANIFEST.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def roster():
    return sorted(p for p in HERE.rglob('*') if p.is_file() and
                  'tmp' not in p.relative_to(HERE).parts and
                  '__pycache__' not in p.relative_to(HERE).parts and
                  p.name!=NAME and not p.name.endswith('.pyc'))
if '--verify' in sys.argv:
    manifest=json.loads((HERE/NAME).read_text())
    paths=roster()
    assert [str(p.relative_to(HERE)) for p in paths]==[f['path'] for f in manifest['files']]
    for p,item in zip(paths,manifest['files']):
        assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],str(p)
    print(json.dumps({'status':'passed','all_first_party_files_bound':len(paths),
                      'manifest_self_excluded':True}))
else:
    paths=roster()
    manifest={'utc':datetime.now(timezone.utc).isoformat(),
              'head':'90a81313f3f65a7914fb6d5a9950fa087ea7467e',
              'algorithm':'SHA-256',
              'self_exclusion':NAME+' excludes itself to avoid a circular hash; finalize_integrity.py is included',
              'foreign_exclusion':'Ignored tmp holds downloaded PDF/HTML/text/renders/replay runtime byproducts; none are first-party deliverables',
              'bytecode_exclusion':'__pycache__ and .pyc are runtime byproducts',
              'early_seal_sha256':sha(HERE/'EARLY_SEAL.md'),
              'files':[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths]}
    (HERE/NAME).write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'manifest_files':len(paths),'early_seal_sha256':manifest['early_seal_sha256']}))
