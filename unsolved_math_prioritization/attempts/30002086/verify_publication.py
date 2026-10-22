#!/usr/bin/env python3
"""Verify packet hashes and replay exact controls without modifying frozen files."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
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
for source,receipt,count in [('release/checks/check.py','release/checks/result.json',41),('audit/audit_controls.py','audit/audit_controls.json',50)]:
 with tempfile.TemporaryDirectory(prefix='shrinker-audit-') as td:
  p=Path(td)/Path(source).name;shutil.copyfile(D/source,p)
  proc=subprocess.run([sys.executable,str(p)],cwd=td,capture_output=True,text=True,check=True)
  result=Path(td)/Path(receipt).name
  assert result.read_bytes()==(D/receipt).read_bytes(),receipt
  data=json.loads(result.read_text());assert data['all_passed'] and data['passed']==count
print(json.dumps({'status':'PASS','public_files':len(expected),'frozen_author_files':8,'frozen_audit_files':6,'author_controls':41,'independent_controls':50,'receipts_byte_identical':True,'scope':'Partial-result integrity and algebra checks only; full review is audit/AUDIT_REPORT.md.'},indent=2,sort_keys=True))
