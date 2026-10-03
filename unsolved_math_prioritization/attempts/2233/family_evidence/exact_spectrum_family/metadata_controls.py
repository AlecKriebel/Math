#!/usr/bin/env python3
"""Read immutable foreign records and validate metadata, without executing them."""
from pathlib import Path
import hashlib
import json
import os
import stat

HERE=Path(__file__).resolve().parent
A=HERE.parent
original=A/'source_snapshot_v2'
manifest=json.loads((A/'snapshot_manifest_v2.json').read_text())
files=[]
for row in manifest['files']:
    p=original/row['path'];raw=p.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    assert sha==row['sha256'] and len(raw)==row['size'],row['path']
    mode=stat.S_IMODE(p.stat().st_mode)
    assert mode==0o444,(row['path'],mode)
    files.append({'path':row['path'],'sha256':sha,'bytes':len(raw),'filesystem_mode':oct(mode)})
review=(original/'review/PARTIAL.md').read_bytes()
final=(original/'PARTIAL.md').read_bytes()
old=b'Separate adversarial review is pending.'
new=b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.'
assert review.count(old)==1
assert review.replace(old,new)==final
author=json.loads((original/'check_results.json').read_text())
submitted=json.loads((original/'review/submitted_results.json').read_text())
assert author==submitted
assert author['partial_sha256']==hashlib.sha256(review).hexdigest()
assert author['partial_sha256']!=hashlib.sha256(final).hexdigest()
independent=json.loads((original/'review/independent_results.json').read_text())
assert len(independent['checks'])==independent['passed']==1263
assert independent['failed']==0
assert all(value=='PASS' for key,value in independent['checks'].items())
assert sum(key.startswith('proper_forbidden_equality_') for key in independent['checks'])==independent['proper_polynomial_checks']==162
assert independent['reviewed_sha256']==hashlib.sha256(review).hexdigest()
assert (original/'check_spectra.py').read_bytes()==(original/'review/submitted_check_spectra.py').read_bytes()
assert json.loads((original/'source_record.json').read_text())==json.loads((A/'pinned_problem.json').read_text())
prior=json.loads((A/'pinned_prior_report.json').read_text())
assert prior=={}
print(json.dumps({'pid':os.getpid(),'head':manifest['head'],'base':manifest['base'],
  'immutable_snapshot_verified_files':files,'review_to_final_exact_header_only_equivalence':True,
  'author_and_reviewer_submitted_receipts_equal':True,
  'stored_author_receipt_binds_reviewed_snapshot':author['partial_sha256'],
  'expected_final_author_execution_hash':hashlib.sha256(final).hexdigest(),
  'all_1263_original_review_check_entries_read_and_pass':True,
  'copied_author_script_byte_identical':True,'source_record_equals_pinned_problem':True,
  'prior_record':'Root-disclosed exact key absent; {} SQL fallback is not a fetched prior report'},indent=2))
