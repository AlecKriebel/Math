#!/usr/bin/env python3
"""Read-only public-packet integrity and full-output replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent
M=json.loads((D/'PUBLICATION_MANIFEST.json').read_text())
expected={r['path'] for r in M['files']}|{'PUBLICATION_MANIFEST.json'}
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}
assert actual==expected,(actual-expected,expected-actual)
for r in M['files']:
 b=(D/r['path']).read_bytes()
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
for name,m in [('release','AUTHOR_MANIFEST.json'),('audit','AUDIT_MANIFEST.json')]:
 for r in json.loads((D/name/m).read_text())['files']:
  b=(D/name/r['path']).read_bytes()
  assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
author=subprocess.check_output([sys.executable,str(D/'release/checks/check.py')],cwd=D)
audit=subprocess.check_output([sys.executable,str(D/'audit/controls/audit_controls.py'),str(D/'release')],cwd=D)
assert author==(D/'release/checks/result.json').read_bytes()
assert audit==(D/'audit/controls/audit_result.json').read_bytes()
print(json.dumps({'status':'PASS','public_files':len(expected),'frozen_author_files':8,'frozen_audit_files':6,'author_controls':21,'audit_controls':22,'full_receipts_byte_identical':True,'scope':'Integrity and algebra controls; the complete mathematical review is audit/AUDIT.md.'},indent=2,sort_keys=True))
