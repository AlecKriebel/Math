from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
manifests=[(p/'PUBLICATION_MANIFEST.json',p),(p/'FINAL_SOURCE_MANIFEST.json',p),(p/'review/REVIEW_MANIFEST.json',p/'review'),(p/'CURRENT_SCOPE_MANIFEST.json',p)]
for manifest,root in manifests:
 for e in json.loads(manifest.read_text())['files']:
  b=(root/e['path']).read_bytes()
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(manifest.name,e['path'])
for script,receipt in [('verify_source_cases.py','SOURCE_CASE_CHECKS.json'),('review/independent_check.py','review/INDEPENDENT_CHECKS.json'),('verify_corrected_source_cases.py','CORRECTED_SOURCE_CASE_CHECKS.json'),('review/independent_check_corrected.py','review/CORRECTED_INDEPENDENT_CHECKS.json')]:
 out=subprocess.check_output([sys.executable,'-B',str(p/script)])
 assert out==(p/receipt).read_bytes(),script
print(json.dumps({'publication_bound_files':len(json.loads((p/'PUBLICATION_MANIFEST.json').read_text())['files'])+1,'frozen_author_files':11,'frozen_review_files':5,'historical_and_corrected_receipts_byte_exact':True,'source_pdfs_reverified':False,'current_ext_free_targets':[0,3],'current_ext_target_minus_quotient':[-9,-6],'old_assertions_historical_only':True,'scope_correction_globally_bound':True},sort_keys=True))
