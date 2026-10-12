#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib,json,datetime
here=Path(__file__).resolve().parent
orig=here.parent/'original_source_authentication_20261006/original_attempt'
rows=[]
for family,original,file in [('author',orig/'verification.json','verification.json'),('old_review',orig/'independent_review/independent_results.json','independent_results.json')]:
 for mode in ['normal','optimized']:
  p=here/'exact_replays'/f'{family}_{mode}'/file
  b,pb=original.read_bytes(),p.read_bytes()
  if b!=pb:raise RuntimeError('exact saved receipt byte mismatch')
  fixed=here/'suggested_guard_repairs'/f'{family}_{mode}'/file
  fd=json.loads(fixed.read_text());od=json.loads(b)
  stripped={k:v for k,v in fd.items() if k not in ('guard_mode','verifier_sha256')}
  if stripped!=od:raise RuntimeError('repaired scientific receipt differs')
  rows.append({'family':family,'mode':mode,'original_receipt_bytes':len(b),'original_receipt_sha256':hashlib.sha256(b).hexdigest(),'exact_replay_byte_identical':True,'repaired_receipt_bytes':fixed.stat().st_size,'repaired_receipt_sha256':hashlib.sha256(fixed.read_bytes()).hexdigest(),'repaired_receipt_scientific_fields_identical':True,'repaired_added_metadata':['guard_mode','verifier_sha256']})
d=json.loads((here/'independent_results.json').read_text());shared=[r for r in d['formula_records'] if r['family'].startswith('full_')]
cl=Counter();treecases=unsat=0
for r in shared:
 treecases+=r['tree_count'];unsat+=not r['sat'];cl.update(r['classes'])
old=json.loads((orig/'independent_review/independent_results.json').read_text())['statistics']
computed={'formulas':len(shared),'unsatisfiable_formulas':unsat,'tree_formula_cases':treecases,
 'noncanonical_trees':cl['missing_tf']+cl['clause_nonleaves']+cl['missing_tf_and_nonleaves'],
 'without_hub_edge':cl['missing_tf']+cl['missing_tf_and_nonleaves'],
 'extra_clause_edges':cl['clause_nonleaves']+cl['missing_tf_and_nonleaves'],'canonical_trees':cl['structured']}
if not all(old[k]==v for k,v in computed.items()):raise RuntimeError('independent shared census disagrees with old review')
a=json.loads((here/'independent_results.json').read_text());b=json.loads((here/'independent_results_optimized.json').read_text())
metadata=['started_utc','completed_utc','python_optimized']
if {k:v for k,v in a.items() if k not in metadata}!={k:v for k,v in b.items() if k not in metadata}:raise RuntimeError('independent modes scientific outputs disagree')
badproof=here/'badproof_controls/original_optimized/independent_results.json'
if badproof.read_bytes()!=(orig/'independent_review/independent_results.json').read_bytes():raise RuntimeError('badproof optimized historical receipt not byte-identical')
comparison={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_and_repaired_receipts':rows,'independent_shared_full_suite_statistics':computed,'shared_full_suite_equals_old_review_on_every_comparable_field':True,'own_normal_optimized_scientific_outputs_identical':True,'own_mode_metadata_differences':metadata,'actual_journal_metadata_is_fresh':['absolute cwd','run timestamps','platform/python version','runner SHA','command -O flag'],'corrupted_proof_historical_optimized_receipt_byte_identical':True,'warning':'Byte-identical optimized assert-based receipts are not verification evidence; actual controls prove checks are suppressed.'}
(here/'receipt_comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
print(json.dumps(comparison,indent=2))
