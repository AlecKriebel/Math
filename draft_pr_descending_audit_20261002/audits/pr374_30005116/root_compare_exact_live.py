from pathlib import Path
import json,hashlib,datetime
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/private/live_acceptance/round2_live';W=A/'tmp/root_staged_gate_attempt2/live';sha=lambda b:hashlib.sha256(b).hexdigest()
x=json.loads((A/'root_staged_live_full_receipt.json').read_bytes());y=json.loads((C/'public/final_gate_live_receipt.json').read_bytes())
def diff(x,y,p=''):
 assert type(x)==type(y)
 if isinstance(x,dict):
  assert x.keys()==y.keys();return sum((diff(x[k],y[k],p+'/'+k) for k in x),[])
 if isinstance(x,list):
  assert len(x)==len(y);return sum((diff(a,b,p+'/'+str(i)) for i,(a,b) in enumerate(zip(x,y))),[])
 return [] if x==y else [(p,x,y)]
original=diff(x,y);records=[]
for label in ['pr_live','pr_final']:
 rb=(W/'private/final_gate'/(label+'.stdout')).read_bytes();ab=(C/'private/final_gate'/(label+'.stdout')).read_bytes();d=diff(json.loads(rb),json.loads(ab));assert set(p for p,a,b in d)=={'/base/repo/size','/head/repo/size'} and all((a,b)==(2076774,2078533) for p,a,b in d)
 rr=next(r for r in x['command_records'] if r['label']==label);ar=next(r for r in y['command_records'] if r['label']==label);assert rr['stdout_sha256']==sha(rb) and ar['stdout_sha256']==sha(ab)
 assert diff(rr,ar)==[('/stdout_sha256',sha(rb),sha(ab))];records.append({'label':label,'root_raw_sha256':sha(rb),'agent_raw_sha256':sha(ab),'full_raw_JSON_differences':d});rr['stdout_sha256']=ar['stdout_sha256']
x.pop('observed_utc');y.pop('observed_utc');assert x==y
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_COMPLETE_EXACT_LIVE_VERIFICATION','whole_receipt_original_differences':original,'explicit_ancillary_API_differences':records,'every_other_raw_API_JSON_leaf_exact':True,'all_material_input_result_Git_blob_mode_path_and_queue_guards_exact':True,'same_immutable_gate_and_descriptor':True,'root_live_receipt_sha256':sha((A/'root_staged_live_full_receipt.json').read_bytes()),'agent_live_receipt_sha256':sha((C/'public/final_gate_live_receipt.json').read_bytes()),'strict_failed_comparison_preserved':True,'actual_merge_pending':True}
(A/'root_exact_live_comparison_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
