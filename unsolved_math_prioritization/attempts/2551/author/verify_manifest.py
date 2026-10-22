#!/usr/bin/env python3
"""Strict integrity and deterministic-control replay; optional scholarly hash check."""
import argparse,hashlib,json,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=pathlib.Path);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parent
m=json.loads((r/'AUTHOR_MANIFEST.json').read_text())
actual={p.name for p in r.iterdir() if p.is_file()}
expected={x['path'] for x in m['files']}|{'AUTHOR_MANIFEST.json'}
assert actual==expected,('inventory',sorted(actual^expected))
for x in m['files']:
 b=(r/x['path']).read_bytes();assert len(b)==x['bytes'];assert hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
p=subprocess.run([sys.executable,str(r/'verify_math.py')],capture_output=True,check=True)
assert p.stdout==(r/'CHECK_RESULTS.json').read_bytes(),'control replay mismatch'
source_count=0
if a.source_dir:
 for s in json.loads((r/'SOURCE_VERIFICATION.json').read_text())['sources']:
  if 'local_verification_name' not in s:continue
  b=(a.source_dir/s['local_verification_name']).read_bytes()
  assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256'],s['title']
  source_count+=1
print(json.dumps({'status':'PASS','manifest_files':len(m['files']),'exact_controls':json.loads(p.stdout)['total_checks'],'scholarly_pdf_hashes_checked':source_count},sort_keys=True))
