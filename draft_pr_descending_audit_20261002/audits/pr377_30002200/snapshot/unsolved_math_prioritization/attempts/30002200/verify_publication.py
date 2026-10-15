from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
for manifest,root in [(p/'PUBLICATION_MANIFEST.json',p),(p/'FINAL_SOURCE_MANIFEST.json',p),(p/'review/REVIEW_MANIFEST.json',p/'review')]:
 for e in json.loads(manifest.read_text())['files']:
  b=(root/e['path']).read_bytes()
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(manifest.name,e['path'])
for script,receipt in [('verify_source_cases.py','SOURCE_CASE_CHECKS.json'),('review/independent_check.py','review/INDEPENDENT_CHECKS.json')]:
 out=subprocess.check_output([sys.executable,str(p/script)])
 assert out==(p/receipt).read_bytes(),script
print(json.dumps({'publication_bound_files':18,'frozen_author_files':11,'frozen_review_files':5,'receipts_byte_exact':True,'source_pdfs_reverified':False},sort_keys=True))
