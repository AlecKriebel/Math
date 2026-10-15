"""Authenticate the fresh final-body comparison and append a bounded priority gate."""
from pathlib import Path
import datetime, hashlib, json, os
A = Path(__file__).resolve().parent.parent
D = A / 'm1_final_journal_supplement_20261006'
R = A / 'm1_final_journal_adversary_20261006'
P = A.parents[1]
def require(c,m):
    if not c: raise RuntimeError(m)
def pin(p):
    b=p.read_bytes(); return {'path':str(p.relative_to(A)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
def authenticate(p,row):
    b=p.read_bytes(); require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],str(p)); return b
seal=R/'SEAL_RECEIPT.json'
require(pin(seal)['sha256']=='3269b2790d521c4428deeebecd97917db03ec2730a737535955a0ec05eaa08d2','seal drift')
s=json.loads(seal.read_text()); m=json.loads(authenticate(R/s['manifest']['path'],s['manifest']))
require(s['sealed_complete'] and len(m['public_outputs'])==6,'incomplete')
for row in m['public_outputs']: authenticate(R/row['path'],row)
inputs=json.loads((R/'INPUT_PINS.json').read_text())
for row in inputs['inputs']+inputs['private_auxiliaries']: authenticate(Path(row['path']),row)
verification=json.loads((R/'VERIFICATION.json').read_text())
require(verification['all_pass'] and len(verification['runs'])==2,'agent verification')
for run in verification['runs']:
    require(run['exit_code']==0,'failed run')
    for stream in ['stdout','stderr']:
        b=run[stream].encode();require(len(b)==run[stream+'_bytes'] and hashlib.sha256(b).hexdigest()==run[stream+'_sha256'],'run stream')
root_runs=[]
for label,mode in [('m1_independent_root_replay_normal_20261006',0),('m1_independent_root_replay_optimized_20261006',1)]:
    q=A/'actual_operations'/label; e=json.loads((q/'execution.json').read_text())
    require(e['exit_code']==0,'root replay')
    for stream in ['stdout','stderr']:authenticate(q/e[stream]['path'],e[stream])
    out=json.loads((q/'stdout.bin').read_text())
    require(out['status']=='PASS' and out['optimization']==mode and out['full_byte_pins_checked']==37 and len(out['rotation_cases'])==28,'root coverage')
    root_runs.append({'label':label,'actual_child_PID':e['child_PID'],'exit_code':0,'execution_pin':pin(q/'execution.json')})
v=json.loads((R/'VERDICT.json').read_text())
require(v['missing_final_source_access_hold_resolved'] and not v['direct_covering_theorem_found'] and not v['exact_claim_proof_citation_found'] and not v['identified_logical_transfer_of_published_invariant_to_exact_antipedal_sum'],'verdict')
body=json.loads((D/'ROOT_FULL_BODY_READ.json').read_text())
require(body['full_journal_text_and_all_11_pages_root_read'] and body['full_9_page_precursor_text_root_read'],'root read')
for row in body['source_pins']:authenticate(D/row['path'],row)
old=json.loads((A/'ROOT_PRIORITY_HOLD_GATE_20261006.json').read_text())
require(old['decision']=='HOLD_FOR_M1_FINAL_JOURNAL_COMPARISON' and old['bounded_substantive_novelty_supported'] and not old['earlier_full_cover_found'],'old combined adjudication')
live=json.loads((A/'actual_operations/m1_supplied_source_live_PR110_20261006/stdout.bin').read_text())
require(live['state']=='OPEN' and live['isDraft'] and live['headRefOid']==old['original_head'] and live['mergedAt'] is None,'live head')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
auth={'schema':'pr110-root-M1-supplement-authentication/v1','UTC':now,'actual_operator_PID':os.getpid(),'public_payloads_full_body_authenticated':len(m['public_outputs']),'private_and_context_inputs_root_replayed':37,'agent_manifest':pin(R/'OUTPUT_MANIFEST.json'),'agent_seal':pin(seal),'root_full_report_and_verdict_read':True,'actual_root_runs':root_runs,'source_pins_not_redistributed':True,'M1_resolved':True,'workflow_percent':35,'publication_percent':0}
(A/'ROOT_M1_FINAL_COMPARISON_AUTHENTICATION_20261006.json').write_text(json.dumps(auth,indent=2)+'\n')
gate={'schema':'pr110-root-bounded-priority-clearance-after-M1/v1','UTC':now,'actual_operator_PID':os.getpid(),'PR':110,'problem_id':5100032,'original_head':old['original_head'],'original_literal_status':'claimed_solved','original_effort':'2/5','new_central_proof_search_turns':0,'mathematical_clearance':True,'M1_journal_final_comparison_cleared':True,'bounded_priority_clearance':True,'bounded_substantive_novelty_supported':True,'novelty_scope':'New proof contribution for the source authors ordinary positive focal antipedal k603 equality, within inspected primary/version corpus; no absolute-first assertion.','candidate_contribution':old['candidate_contribution'],'earlier_full_cover_found':False,'already_solved_disposition_supported':False,'prior_combined_hold_gate':pin(A/'ROOT_PRIORITY_HOLD_GATE_20261006.json'),'M1_supplement_authentication':pin(A/'ROOT_M1_FINAL_COMPARISON_AUTHENTICATION_20261006.json'),'retained_nonessential_limits':old['retained_nonessential_limits'],'reporting_conditions':old['reporting_conditions_after_gap_resolution'],'paper_preparation_authorized':True,'whole_publication_package_reviews_complete':False,'publication_ready':False,'publish_or_merge_authorized_at_this_gate':False,'priority_work_percent':100,'workflow_percent':35,'publication_percent':0,'persistent_goal_complete':False,'persistent_goal_status':'active'}
(A/'ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json').write_text(json.dumps(gate,indent=2)+'\n')
f=P/'CURRENT_PROGRESS.json';q=json.loads(f.read_text())
q.update({'UTC':now,'updated_UTC':now,'current_M1_fresh_adversarial_review_pending':False,'current_M1_journal_comparison_cleared':True,'current_priority_clearance':True,'current_novelty_established':True,'current_novelty_scope':'Bounded substantive proof contribution; source authors observation credited; no absolute-first/global-openness claim.','current_priority_gate':'audits/pr110_5100032/ROOT_PRIORITY_CLEARANCE_AFTER_M1_20261006.json','current_priority_audit_percent':100,'current_required_priority_findings':[],'current_blocked_audit_passed':False,'current_remaining_step':'Prepare concise paper and portable support, then first whole-package adversarial review/global repair and NEW second whole-package review; only then publish, track and integrate/merge.','current_PR_workflow_percent':35,'current_workflow_estimate_percent':35,'next_step':'Prepare PR110 publication package; follow fresh whole-package adversarial loop before any service action.'})
f.write_text(json.dumps(q,indent=2,sort_keys=True)+'\n')
entry=now+' — PR110 essential M1 cleared by supplied complete journal body, independent sealed review and actual root normal/O replays (37 full-byte inputs,28 odd-period transfer controls). Complete final/precursor read; no antipedal covering theorem/citation/valid transfer found. Combined three-family plus new adjudicator bounded novelty now cleared; observation/classical mechanisms credited and nonessential corpus limits retained. Paper preparation authorized; publication/merge remain gated on fresh whole-package reviews. Workflow35%, source/math/priority100%, publication0%; full program17/99=17.17%, new proof turns0. Historical hold/audit seals preserved.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with p.open('a') as handle:handle.write('\n'+entry)
print(json.dumps({'UTC':now,'actual_operator_PID':os.getpid(),'M1_resolved':True,'bounded_priority_clearance':True,'paper_preparation_authorized':True,'publication_ready':False,'workflow_percent':35}))
