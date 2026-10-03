#!/usr/bin/env python3
"""Read-only original/history consistency after independent core formed."""
import datetime,difflib,hashlib,json,pathlib,os
root=pathlib.Path(__file__).resolve().parent
original=root.parent/'original_preparation_family/original'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for row in (original/'review/FINAL_SHA256SUMS').read_text().splitlines():
    expected,name=row.split(None,1);p=original/'review'/name
    assert sha(p)==expected;checks.append({'path':'review/'+name,'sha256':expected})
assert (root/'reproduction/verify.py').read_bytes()==(original/'verify.py').read_bytes()
assert (root/'reproduction/KNOWN_RESULT.md').read_bytes()==(original/'KNOWN_RESULT.md').read_bytes()
assert (root/'reproduction/verification.json').read_bytes()==(original/'verification.json').read_bytes()
old=original/'review/author_reproduction/KNOWN_RESULT.md'
assert sha(old)=='8b9103c862380ea8d93b9d89d6dc03e06b0b90e3d6cb8453bdf1453ba1180cf4'
assert sha(original/'KNOWN_RESULT.md')=='3cf3b548da6d0fbddd0577f02b7cfae056e30bee44ca0af2ba967d304c2fdbb8'
for n in ('verify.py',):
    assert (original/n).read_bytes()==(original/'review/author_reproduction'/n).read_bytes()==(original/'review/final_reproduction'/n).read_bytes()
assert (original/'KNOWN_RESULT.md').read_bytes()==(original/'review/final_reproduction/KNOWN_RESULT.md').read_bytes()
assert (original/'verification.json').read_bytes()==(original/'review/final_reproduction/verification.json').read_bytes()==(original/'review/final_reproduction/stdout.json').read_bytes()
hist=json.loads((original/'review/independent_controls.json').read_bytes())
assert sum(hist['by_category'].values())==hist['assertions_passed']==20173
author=json.loads((original/'verification.json').read_bytes())
assert sum(author['by_category'].values())==author['assertions_passed']==6665
pre=original/'review/author_reproduction/verification.json'
previous=json.loads(pre.read_bytes()); final=dict(author);previous.pop('artifact_sha256');final.pop('artifact_sha256');assert previous==final
diff=''.join(difflib.unified_diff(old.read_text().splitlines(True),(original/'KNOWN_RESULT.md').read_text().splitlines(True),fromfile='historic_frozen',tofile='final'))
(root/'historical_candidate_diff.txt').write_text(diff)
out={'operator':'PR59 mathematical subagent','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'FINAL_SHA256SUMS_entries_verified':checks,'author_source_exact_copy':True,'author_receipt_byte_equal':True,
     'old_candidate_sha256':sha(old),'final_candidate_sha256':sha(original/'KNOWN_RESULT.md'),
     'historic_author_checkers_byte_equal':True,'historic_receipt_equal_except_artifact_hash':True,
     'historic_independent_stored_count_sum':20173,'historic_independent_checker_executed':False,
     'all_final_reproduction_bytes_equal_to_publication':True,'historical_diff_saved':True}
(root/'consistency_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
