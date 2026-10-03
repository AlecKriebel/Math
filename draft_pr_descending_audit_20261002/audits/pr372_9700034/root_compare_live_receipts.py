"""Compare complete independent exact-live receipts with explicit instance differences."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary';root_path=A/'root_exact_live_full_receipt.json';agent_path=C/'REPAIRED_LIVE_RECEIPT.json';r=json.loads(root_path.read_bytes());c=json.loads(agent_path.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert r['status']==c['status']=='PASS_EXACT_LIVE_SCOPED_GATE' and r['failures']==c['failures']==[]
diff=json.loads((A/'root_live_full_difference_inventory.json').read_bytes());raw=json.loads((A/'root_live_raw_pr_difference_inventory.json').read_bytes());root_instance=str((A/'tmp/root_clean_live/private_live/root_exact_live').resolve());agent_instance=str((C/'private_live/REPAIRED_LIVE').resolve());classified=[]
for entry in diff:
 p=entry['path'];left=entry['root'];right=entry['agent']
 if p in ['/started_utc','/completed_utc'] or p.endswith('/utc') or p.startswith('/summary/fresh_primary_inputs/') and p.endswith(('/started_utc','/completed_utc')):
  datetime.datetime.fromisoformat(left);datetime.datetime.fromisoformat(right);kind='recorded observation time'
 elif p.startswith('/complete_replays/') and '/command/' in p:
  assert left.startswith(root_instance+'/') and right==agent_instance+left[len(root_instance):],entry;kind='exact corresponding private execution path'
 elif p.startswith('/api_receipts/') and p.endswith('/stdout_sha256'):
  i=int(p.split('/')[2]);label=r['api_receipts'][i]['label'];assert label==c['api_receipts'][i]['label'] and label in ['initial_pr','late_pr']
  rb=(A/'tmp/root_clean_live/private_live/root_exact_live/api'/f'{label}.stdout').read_bytes();cb=(C/'private_live/REPAIRED_LIVE/api'/f'{label}.stdout').read_bytes();assert sha(rb)==left and sha(cb)==right
  assert {x['path'] for x in raw[label]}=={'/head/repo/pushed_at','/base/repo/pushed_at'} and len(raw[label])==2
  # Recompute the entire raw JSON comparison, not a claim based on stored counts.
  rp=json.loads(rb);cp=json.loads(cb)
  for side in ['head','base']:
   expected=next(x for x in raw[label] if x['path']==f'/{side}/repo/pushed_at');assert rp[side]['repo']['pushed_at']==expected['root'] and cp[side]['repo']['pushed_at']==expected['agent'];rp[side]['repo']['pushed_at']=cp[side]['repo']['pushed_at']
  assert rp==cp,'other raw PR API difference';kind='full raw API differs only at the two recorded repository pushed_at leaves'
 else:raise AssertionError(('unexpected full receipt difference',entry))
 classified.append({'path':p,'kind':kind})
 # Having validated each exact difference, substitute only that one compared leaf.
 pieces=p.split('/')[1:];node=r
 for piece in pieces[:-1]:node=node[int(piece)] if isinstance(node,list) else node[piece]
 if isinstance(node,list):node[int(pieces[-1])]=right
 else:node[pieces[-1]]=right
assert r==c,'complete receipt mismatch after the explicitly validated instance differences'
root_runs=A/'tmp/root_clean_live/private_live/root_exact_live/runs';agent_runs=C/'private_live/REPAIRED_LIVE/runs'
for replay in c['complete_replays']:
 for suffix in ['stdout','stderr']:
  rb=(root_runs/f'{replay["label"]}.{suffix}').read_bytes();cb=(agent_runs/f'{replay["label"]}.{suffix}').read_bytes();assert rb==cb and sha(rb)==replay[suffix+'_sha256']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_COMPLETE_ROOT_AGENT_EXACT_LIVE_COMPARISON','root_receipt_sha256':sha(root_path.read_bytes()),'agent_receipt_sha256':sha(agent_path.read_bytes()),'all_51761_full_checks_equal':len(c['checks'])==51761,'all_nine_complete_stdout_stderr_and_whole_results_equal':len(c['complete_replays'])==9,'only_instance_differences':classified,'raw_pr_ancillary_differences':raw,'full_nested_receipts_equal_after_only_enumerated_validated_leaves':True,'no_target_body_claim_queue_tree_source_or_gate_guard_normalization':True}
(A/'root_live_full_comparison_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'all_checks':len(c['checks']),'all_complete_replays':len(c['complete_replays']),'explicit_instance_differences':len(classified),'agent_receipt_sha256':out['agent_receipt_sha256']}))
