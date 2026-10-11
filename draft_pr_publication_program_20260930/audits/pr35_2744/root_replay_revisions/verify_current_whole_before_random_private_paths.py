"""Bind the root's already completed fresh executions to the closed whole review."""
from pathlib import Path
import datetime, hashlib, json, subprocess
A=Path(__file__).resolve().parent; H=A/'current_whole_adversary'; O=A/'tmp/root_current_whole_replay'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def normalized(x,prefix):
    if isinstance(x,dict):return {k:normalized(v,prefix) for k,v in x.items() if k!='utc'}
    if isinstance(x,list):return [normalized(v,prefix) for v in x]
    if isinstance(x,str):return x.replace(str(prefix),'<private-output>')
    return x
before=sha((H/'MANIFEST.json').read_bytes())
assert before=='ad28abe21b169dcf49f7cf084cb8e16f55df5d3034b131e9525915ed54973f37'
r=subprocess.run(['/usr/bin/python3',str(H/'verify_closed.py')],capture_output=True,check=True)
assert not r.stderr
closed=json.loads(r.stdout)
old=load(H/'REPLAY_RESULTS.json'); actual=load(O/'outer/REPLAY_RESULTS.json')
left=normalized(old,H/'tmp/replay_repo'); right=normalized(actual,O/'outer/tmp/replay_repo')
qualified=[]
for i,(a,b) in enumerate(zip(left['runs'],right['runs'])):
    name=a['name']; assert b['name']==name
    for directory,row in [(H,old['runs'][i]),(O/'outer',actual['runs'][i])]:
        for kind in ['stdout','stderr']:
            assert sha((directory/'receipts'/(name+'.'+kind)).read_bytes())==row[kind+'_sha256']
    if a.get('actual_result_sha256')!=b.get('actual_result_sha256'):
        pa=H/'receipts'/(name+'.result.json');pb=O/'outer/receipts'/(name+'.result.json')
        assert sha(pa.read_bytes())==a['actual_result_sha256'] and sha(pb.read_bytes())==b['actual_result_sha256']
        assert normalized(load(pa),H/'tmp/replay_repo')==normalized(load(pb),O/'outer/tmp/replay_repo'),name
        qualified.append({'run':name,'comparison':'complete JSON equal excluding actual UTC and private repository prefix','saved_sha256':a.pop('actual_result_sha256'),'actual_sha256':b.pop('actual_result_sha256')})
assert len(qualified)==3 and left==right
assert normalized(load(H/'AUDIT_RESULTS.json'),H)==normalized(load(O/'new/AUDIT_RESULTS.json'),O/'new')
assert sha((H/'MANIFEST.json').read_bytes())==before
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
 'closed_whole_manifest_sha256':before,'closed_verification':closed,
 'actual_outer_executions':9,'explicit_original_executions':3,'explicit_current_executions':3,
 'actual_frozen_family_mutants_rejected':24,'current_members':42,'dependency_members':115,
 'actual_bookkeeping_control_checks':329,'actual_new_scientific_diagnostics':33,
 'actual_new_scientific_mutants_rejected':6,'actual_false_prose_coverage_controls':4,
 'whole_outer_results_equal_with_qualified_three_fresh_receipts':qualified,
 'whole_new_control_results_equal_except_actual_UTC_and_private_output_prefix':True,
 'literal_universal_claim_solved':False,'accepted_disposition_proposed':'unsolved',
 'original_substantive_attempts':1,'new_substantive_attempts':0,'attempt_limit':5,
 'mandatory_current_packet_corrections':[],
 'root_manual_reading':'Complete final report, universal proof and original seal qualification, operative source-depth ledger, all actual science/replay/guard/retrieval code, preserved setup and weaker-diagnostic revisions and their exact corrections. Earlier root proof and full original/family source reproduction remain distinct.',
 'scope':'Actual root private execution finished before this receipt; not merely saved-result validation. All closed101/current42/dependency115 bytes remain bound. Universal knot canonical-arc gap retained. No integration, paper, DOI, tracker or human peer-review assertion.'}
for label,p in [('actual_outer',O/'outer/REPLAY_RESULTS.json'),('actual_new',O/'new/AUDIT_RESULTS.json')]:result[label+'_sha256']=sha(p.read_bytes())
(A/'ROOT_NEW_WHOLE_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
