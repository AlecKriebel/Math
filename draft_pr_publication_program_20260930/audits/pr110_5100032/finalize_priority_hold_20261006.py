from pathlib import Path
import datetime,fnmatch,hashlib,json,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2];D=A/'priority_cross_family_adjudication_20261006'
def require(c,m):
    if not c:raise RuntimeError(m)
def check(p,r):
    require(p.is_file() and not p.is_symlink(),'regular body '+str(p));b=p.read_bytes()
    require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'body pin '+str(p));return b
b=(D/'OUTPUT_MANIFEST.json').read_bytes();require(hashlib.sha256(b).hexdigest()=='c6d478dd5f31ff554cfb69af22d934ea9c6bfdddee589a63bad7285e5b49c040','manifest')
m=json.loads(b);seen=set()
for r in m['payload']:
    p=D/r['path'];require(p.resolve().is_relative_to(D) and r['path'] not in seen,'path');seen.add(r['path'])
    require(r['path'] not in m['excluded_files'] and not any(r['path'].startswith(x) for x in m['excluded_prefixes']),'excluded payload');check(p,r)
require(len(seen)==m['public_payload_count']==28 and sum(x['bytes'] for x in m['payload'])==m['public_payload_bytes']==258696,'counts')
s=json.loads((D/'SEAL_RECEIPT.json').read_text())
for k in ('manifest','report','verdict'):check(D/s[k]['path'],s[k])
v=json.loads((D/'VERDICT.json').read_text());require(v['recommended_state']=='HOLD_FOR_ESSENTIAL_IDENTIFIED_VERSION_GAP' and [x['id'] for x in v['required_findings']]==['M1'],'hold verdict')
require(v['bounded_substantive_novelty_supported'] and not v['already_solved_supported'] and not v['earlier_full_cover_found'] and not v['priority_clearance'] and not v['publication_clearance'],'bounded verdict')
ia=json.loads((D/'INPUT_AUTHENTICATION.json').read_text())
for r in ia['original_and_policy_inputs']:check(A/r['path'],r)
inputs=0
for fam in ia['families']:
    for k in ('manifest','receipt','report','verdict'):check(A/fam[k]['path'],fam[k])
    fm=json.loads((A/fam['manifest']['path']).read_text());rows=fm.get('payload',fm.get('public_payload_bodies'))
    for r in rows:check(A/fam['folder']/r['path'],r)
    inputs+=len(rows)
require(inputs==ia['public_payload_bodies_authenticated']==514,'input bodies')
custody=json.loads((D/'CUSTODY_AND_READ_SCOPE.json').read_text())
for r in custody['private_metadata_only_pins']:check(A/r['path'],r)
require(len(custody['private_metadata_only_pins'])==custody['private_body_pins_authenticated']==256,'private count')
book=json.loads((A/'priority_exact_invariant_history_20261006/IMPA_AUTHOR_SOURCE_CUSTODY.json').read_text())
for r in book['body_rows']:
    b=check(A/'priority_exact_invariant_history_20261006'/book['private_extraction_root']/r['path'],r)
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['Git_blob_OID'],'book Git body')
require(len(book['body_rows'])==145,'book count')
for control in custody['actual_normal_optimized_controls']:
    result=json.loads(check(A/control['result_pin']['path'],control['result_pin']))
    r=json.loads(check(A/control['execution_pin']['path'],control['execution_pin']))
    require(r['child_PID']==control['actual_PID'] and r['exit_code']==control['exit_code']==0 and result['optimization']==control['optimization'],'actual control')
    require(result.get('explicit_checks',result.get('checks'))==control['explicit_checks'],'control count')
require(len(custody['actual_normal_optimized_controls'])==4,'control modes')
ops=[]
for f in sorted((D/'actual_operations').glob('*/execution.json')):
    r=json.loads(f.read_text())
    for k in ('stdout','stderr'):check(f.parent/r[k]['path'],r[k])
    require(r['exit_code']==0 and r['UTC_start']<=r['UTC_end'],'actual completed operation')
    ops.append({'label':f.parent.name,'child_PID':r['child_PID'],'recorder_PID':r['recorder_PID'],'exit_code':r['exit_code']})
closing=json.loads((D/'CLOSING_AUTHENTICATION.json').read_text())
for k in ('manifest','seal_receipt','actual_closing_execution'):check(D/closing[k]['path'],closing[k])
require(closing['actual_sealer_PID']==s['actual_sealer_PID']==48116 and closing['actual_closing_recorder_PID']==48108 and closing['actual_verifier_PID']==48128,'closing metadata')
require(any(x['label']=='final_seal' and x['child_PID']==48116 and x['recorder_PID']==48108 for x in ops),'actual sealer envelope')
require(any(x['label']=='verify_closing_envelope' and x['child_PID']==48128 for x in ops),'actual verification envelope')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
pins={}
for name in ('REPORT.md','VERDICT.json','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','CLOSING_AUTHENTICATION.json'):
    b=(D/name).read_bytes();pins[name]={'path':str((D/name).relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
auth={'schema':'pr110-root-cross-family-priority-complete-custody/v1','UTC':now,'actual_operator_PID':os.getpid(),'root_final_REPORT_VERDICT_fully_read':True,'own_public_payload_count':28,'input_public_payloads_authenticated':514,'private_file_pins_authenticated':256,'author_book_Git_blob_bodies_authenticated':145,'actual_control_modes_authenticated':4,'actual_operations':ops,'pins':pins,'required_findings':v['required_findings'],'bounded_substantive_novelty_supported':True,'already_solved_supported':False,'priority_or_publication_clearance':False,'new_central_proof_search_turns':0,'workflow_estimate_percent':30}
(A/'ROOT_CROSS_FAMILY_PRIORITY_AUTHENTICATION_20261006.json').write_text(json.dumps(auth,indent=2,sort_keys=True)+'\n')
gate={'schema':'pr110-root-priority-adjudicated-hold/v1','UTC':now,'actual_operator_PID':os.getpid(),'PR':110,'problem_id':5100032,'code':'AMR-050-0032','original_head':v['original_head'],'original_effort':'2/5','new_central_proof_search_turns':0,'decision':'HOLD_FOR_M1_FINAL_JOURNAL_COMPARISON','source_and_math_complete':True,'bounded_substantive_novelty_supported':True,'novelty_established_for_publication':False,'earlier_full_cover_found':False,'already_solved_disposition_supported':False,'required_findings':v['required_findings'],'retained_nonessential_limits':v['nonessential_bounded_audit_limits'],'candidate_contribution':v['supported_candidate_contribution'],'reporting_conditions_after_gap_resolution':v['reporting_conditions_after_gap_resolution'],'no_unrestricted_or_absolute_priority_claim':True,'paper_prepared':False,'published':False,'native_integration_complete':False,'PR_merged_or_closed':False,'live_readback':{'PR110_actual_child_PID':44472,'PR110_head_unchanged_and_open_draft':True,'PR107_actual_child_PID':44485,'PR107_previously_closed_unmerged':True},'priority_checkpoint':'df785fabee95665ee1782d61b24e32acec049dc6','priority_checkpoint_full_body_authentication':'ROOT_PRIORITY_CHECKPOINT_AUTHENTICATION_20261006.json','source_access_question_pending':True,'persistent_goal_status':'active','persistent_goal_complete':False,'full_program_completed':17,'dated_eligible_total':99,'published_count':10,'source_math_percent':100,'bounded_priority_adjudication_percent':100,'selected_candidate_priority_work_percent':90,'workflow_estimate_percent':30,'work_percent_is_not_probability_of_novelty':True}
(A/'ROOT_PRIORITY_HOLD_GATE_20261006.json').write_text(json.dumps(gate,indent=2,sort_keys=True)+'\n')
f=P/'CURRENT_PROGRESS.json';r=json.loads(f.read_text());r.update({'UTC':now,'updated_UTC':now,'current_priority_audit_percent':90,'current_priority_adjudication_complete':True,'current_priority_clearance':False,'current_novelty_established':False,'current_bounded_substantive_novelty_support':True,'current_already_solved_disposition_supported':False,'current_required_priority_findings':v['required_findings'],'current_priority_gate':'audits/pr110_5100032/ROOT_PRIORITY_HOLD_GATE_20261006.json','current_priority_adjudicator_authentication':'audits/pr110_5100032/ROOT_CROSS_FAMILY_PRIORITY_AUTHENTICATION_20261006.json','current_priority_checkpoint_commit':'df785fabee95665ee1782d61b24e32acec049dc6','current_priority_checkpoint_remote_verified':True,'current_priority_checkpoint_complete_body_readback':'audits/pr110_5100032/ROOT_PRIORITY_CHECKPOINT_AUTHENTICATION_20261006.json','current_human_source_access_question_pending':True,'current_human_disposition_question_pending':False,'current_remaining_step':'One essential identified final-journal comparison M1. Independent math and combined bounded priority audits complete; no paper/publication/native integration or PR110 disposition.','remaining_current_step':'Obtain legitimate full journal final DOI10.1007/s10883-022-09608-y and audit actual statements/proofs against k603 and the read precursor. Access gap alone does not support already_solved.','next_step':'Resolve M1 in a separately sealed supplement; if no full covering prior, proceed with paper/review/publication under bounded priority limits. If a covering prior exists, supply exact mapping and close as already_solved.','persistent_goal_status':'active','persistent_goal_complete':False})
f.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
note='\n### '+now+' — PR110 fresh combined priority adjudication complete; HOLD M1 (workflow30%; source/math100%; bounded adjudication100%; selected-candidate priority90%; publication0%)\n\nNEW independent cross-family reviewer sealed28 public bodies, independently rechecked514 family payloads,256 private pins,145 author-book Git blobs and4 genuine normal/O transfer controls. Root read the full final report/verdict and authenticated every own/input payload and closing envelope. Three fresh families plus this new adjudicator find positive bounded substantive novelty evidence for the ordinary-norm difference/all-period closure proof; no full covering prior was found, so already_solved closure is unsupported. Familiar geometric constructions, the known focal-height product, generic telescoping, numerical observation and even symmetry must be credited. Required M1 is the complete2022/2023 final of Estimating Elliptic Billiard Invariants with Spatial Integrals, DOI10.1007/s10883-022-09608-y: its full9-page2021 precursor is read, but the revised11-page final statements/proofs remain unavailable. Materiality is based on the identified later source-author follow-up, not failed access or the pending question. Final-book/Lockwood/experiment limits remain explicit finite-corpus bounds. No paper, DOI, tracker row, native acceptance, merge or close for PR110. Actual read-only GH44472 confirms original110head/open draft; GH44485 reconfirms previously closed/unmerged107. Priority checkpointdf785fabee95665ee1782d61b24e32acec049dc6 was pushed and root42938 independently checked all1481 committed/current full bodies. Research goal active/incomplete;17/99 completed,10 published; new central proof turns0. Awaiting the pending human legitimate-access answer; no repeated outreach or access searches.\n'
for log in (A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md'):
    with log.open('a') as out:out.write(note)
print(json.dumps({'UTC':now,'actual_operator_PID':os.getpid(),'decision':gate['decision'],'bounded_novelty_supported':True,'already_solved_supported':False,'priority_clearance':False,'source_access_question_pending':True,'workflow_estimate_percent':30,'new_central_proof_search_turns':0}))
