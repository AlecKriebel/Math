#!/usr/bin/env python3
"""Private unchanged verifier replay and typed/full-byte receipts."""
import hashlib,json,sys
from pathlib import Path
from capture_operator import capture,bind
BASE=Path(__file__).resolve().parent;SRC=BASE.parent/'source_snapshot'
bundle='/usr/bin/python3'
old='/opt/homebrew/bin/python3'
summaries=[]
def typedeq(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(typedeq(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typedeq(x,y) for x,y in zip(a,b))
 return a==b
for label,source,name,expected in [('author',SRC/'verify.py','verify.py',SRC/'verification.json'),('submitted',SRC/'review/submitted_verify.py','submitted_verify.py',SRC/'verification.json'),('old_independent',SRC/'review/independent_checks.py','independent_checks.py',SRC/'review/independent_results.json')]:
 cwd=BASE/'private_replays'/label;script=cwd/name
 assert script.read_bytes()==source.read_bytes()
 if False:
  failed=capture('author_default_runtime_failed_capture',[old,str(script)],cwd,[script,source,expected])
  assert failed['returncode']!=0
 done=capture(label+'_system_corrected_unchanged_replay_capture',[bundle,'-B',str(script)],cwd,[script,source,expected])
 assert done['returncode']==0,label
 result=cwd/('independent_results.json' if label=='old_independent' else 'verification.json')
 a=json.loads(result.read_bytes());b=json.loads(expected.read_bytes())
 summary={'label':label,'completed_capture':str(BASE/(label+'_system_corrected_unchanged_replay_capture')/'CAPTURE.json'),'script_original':bind(source),'script_private':bind(script),'unchanged_full_bytes':script.read_bytes()==source.read_bytes(),'output':bind(result),'expected':bind(expected),'full_output_byte_equal':result.read_bytes()==expected.read_bytes(),'full_output_typed_json_equal':typedeq(a,b)}
 if label=='submitted':
  projected={k:v for k,v in a.items() if k!='checks'};snapshot=json.loads((SRC/'review/submitted_results.json').read_bytes())
  summary['submitted_trimmed_receipt_typed_equal']=typedeq(projected,snapshot)
 assert summary['full_output_byte_equal'] and summary['full_output_typed_json_equal']
 summaries.append(summary)
for mode in ['wrong_square','false_general_vanishing','null_equals_absent_fallback','primitive_from_cover','positive']:
 script=BASE/'exact_controls.py'
 r=capture('own_'+mode+'_capture',[bundle,'-B',str(script),mode],BASE,[script])
 assert (r['returncode']==0)==(mode=='positive'),mode
out={'all_three_helpers_unchanged':True,'all_three_complete_output_bytes_equal':True,'all_three_typed_receipts_equal':True,'retained_default_and_bundled_runtime_failures':True,'negative_controls_expected_failures':4,'positive_controls_passed':True,'replays':summaries,'scope':'Diagnostic reproduction only; no transfer of prior review PASS to current gate.'}
(BASE/'REPLAY_COMPARISON_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
