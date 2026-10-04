#!/usr/bin/env python3
"""Read completed captures and perform full bytes and recursive typed comparisons."""
from pathlib import Path
import json
from capture_operator import bind
B=Path(__file__).resolve().parent;S=B.parent/'source_snapshot'
def typed(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
rows=[]
for label,scriptname,original,output,expect in [('author','verify.py',S/'verify.py','verification.json',S/'verification.json'),('submitted','submitted_verify.py',S/'review/submitted_verify.py','verification.json',S/'verification.json'),('old_independent','independent_checks.py',S/'review/independent_checks.py','independent_results.json',S/'review/independent_results.json')]:
 d=B/'private_replays'/label;c=B/(label+'_system_corrected_unchanged_replay_capture');r=json.loads((c/'CAPTURE.json').read_bytes())
 a=(d/output).read_bytes();e=expect.read_bytes();v=json.loads(a);ev=json.loads(e)
 assert r['completed'] and r['returncode']==0 and (d/scriptname).read_bytes()==original.read_bytes()
 assert a==e and typed(v,ev)
 row={'label':label,'completed_capture':bind(c/'CAPTURE.json'),'original_source':bind(original),'private_source':bind(d/scriptname),'complete_output':bind(d/output),'complete_original_receipt':bind(expect),'source_full_bytes_equal':True,'result_full_bytes_equal':True,'result_recursive_typed_equal':True}
 if label=='submitted':
  q={k:x for k,x in v.items() if k!='checks'};t=json.loads((S/'review/submitted_results.json').read_bytes());assert typed(q,t);row['trimmed_submitted_receipt_typed_equal']=True
 rows.append(row)
negative=[]
for n in ['wrong_square','false_general_vanishing','null_equals_absent_fallback','primitive_from_cover']:
 c=B/('own_'+n+'_capture');r=json.loads((c/'CAPTURE.json').read_bytes());assert r['completed'] and r['returncode']!=0
 negative.append({'mode':n,'capture':bind(c/'CAPTURE.json'),'expected_failure':True})
positive=json.loads((B/'own_positive_symbolic_form_corrected_capture/CAPTURE.json').read_bytes());assert positive['completed'] and positive['returncode']==0
own=json.loads((B/'own_exact_results.json').read_bytes());assert own['passed']==len(own['labels'])
out={'helpers':rows,'positive_own_controls':own['passed'],'own_result':bind(B/'own_exact_results.json'),'negative_controls':negative,'retained_real_failures':['author_default_runtime_failed_capture','author_unchanged_replay_capture','replay_suite_outer_capture','replay_suite_system_corrected_outer_capture','own_positive_capture'],'corrections':['Use existing /usr/bin/python3 -B with SymPy1.14.0; no installation.','Compare the lower-link solution set to the exact closed interval, rather than comparing equivalent syntactic inequality forms.'],'old_PASS_transferred':False,'no_Floer_or_global_proof':True}
(B/'REPLAY_COMPARISON_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'unchanged_helpers':len(rows),'complete_byte_and_typed_matches':len(rows),'own_positive':own['passed'],'expected_negative_failures':len(negative)},indent=2))
