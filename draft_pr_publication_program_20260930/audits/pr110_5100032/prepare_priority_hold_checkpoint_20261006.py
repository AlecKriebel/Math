from pathlib import Path
import datetime,json,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2];selected=set()
def add(p):
    if not p.is_file() or p.is_symlink():raise RuntimeError('regular file')
    if any(x in p.parts for x in ['private_sources','private_review_materials','private_source_extracts','primary_sources_private','root_primary_read_private','private_operational_archive']):raise RuntimeError('private')
    selected.add(p.relative_to(C).as_posix())
d=A/'priority_cross_family_adjudication_20261006'
for r in json.loads((d/'OUTPUT_MANIFEST.json').read_text())['payload']:add(d/r['path'])
for name in ['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','CLOSING_AUTHENTICATION.json']:add(d/name)
for name in ['final_seal','verify_closing_envelope']:
    for p in (d/'actual_operations'/name).iterdir():
        if p.is_file():add(p)
for name in ['finalize_priority_hold_20261006.py','prepare_priority_hold_checkpoint_20261006.py','ROOT_CROSS_FAMILY_PRIORITY_AUTHENTICATION_20261006.json','ROOT_PRIORITY_HOLD_GATE_20261006.json','ROOT_PRIORITY_CHECKPOINT_AUTHENTICATION_20261006.json','authenticate_priority_checkpoint_20261006.py','RESEARCH_LOG.md']:add(A/name)
for name in ['priority_scoped_main_checkpoint','priority_checkpoint_full_body_readback','current_PR110_read_only_state_check','prior_PR107_read_only_closure_confirmation','root_cross_family_priority_final_authentication_and_hold']:
    for p in (A/'actual_operations'/name).iterdir():
        if p.is_file():add(p)
for directory in [A/'root_priority_checkpoint_authentication_20261006',P/'audits/pr108_30003996/actual_checkpoints/PR110_priority_20261006']:
    for p in directory.rglob('*'):
        if p.is_file():add(p)
for name in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']:add(P/name)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
note='\n'+now+' — Final bounded PR110 priority/HOLD checkpoint prepared (workflow30%; source/math100%; selected-candidate priority90%; publication0%). Fresh adjudication and root gate/custody selected with actual checkpoint completion/readback envelopes; copyrighted primary bodies excluded. Required M1/source-access question remains pending; no earlier full covering result and no already_solved action. Dedicated source/math and priority inputs remain immutable. No native or publication changes; goal active/incomplete.\n'
for log in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with log.open('a') as f:f.write(note)
selection=A/'PRIORITY_HOLD_CHECKPOINT_SELECTION_20261006.json';selected.add(selection.relative_to(C).as_posix())
r={'schema':'pr110-priority-hold-checkpoint-exact-selection/v1','UTC':now,'actual_operator_PID':os.getpid(),'expected_parent':'df785fabee95665ee1782d61b24e32acec049dc6','paths':sorted(selected),'source_math_percent':100,'selected_candidate_priority_percent':90,'workflow_estimate_percent':30,'priority_clearance':False,'new_central_proof_search_turns':0,'copyrighted_private_bodies_excluded':True,'source_access_question_pending':True,'current_PR_not_disposed':True}
selection.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='paths'}));print('path_count',len(selected))
