"""Bind genuinely completed whole and ROOT records; repair SOURCE formats, never execute it."""
from pathlib import Path
import datetime as dt, difflib, hashlib, json, os, stat
H=Path(__file__).resolve().parent; A=H.parent; R=A.parents[2]; W=A/'current_whole_adversary_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,v):
    b=v.encode() if type(v) is str else (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    with (H/n).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def check(z):
    p=R/z['path'];assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents);b=p.read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256']
    if 'full_mode' in z:assert type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    rootpath=A/'ROOT_WHOLE_CURRENT_REVIEW.json';assert sha(rootpath.read_bytes())=='ed0cc07fd852881a0b9a9893e6c2ec7f25e6e6d2f3d1bfb26bfa88a7a0b17b54';root=load(rootpath)
    assert root['schema']=='pr46-root-complete-closed-whole-inspection/v1' and root['status']=='PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION' and root['future_execution_approved'] is False and root['future_acceptance_approved'] is False and root['mandatory_corrections']==[]
    for flag in ['personal_report_and_verdict_fully_read','all_first_party_whole_bytes_and_modes_checked','all_external_individual_whole_bytes_checked','exact_self_only_recursive_closure_checked','closing_and_postexit_capture_chronology_checked','ROOT_actual_inner45_complete_read','frozen_inner43_honest_prefix','dated_native4_current_HEAD_not_future_acceptance_authority']:assert root[flag] is True
    mf=load(W/'MANIFEST.json');assert sha((W/'MANIFEST.json').read_bytes())=='be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2' and mf['files_count']==245 and mf['self_excluded']==['MANIFEST.json']
    assert len(root['normalized_complete_first_party_members'])==245 and len(root['normalized_complete_external_input_bindings'])==1877
    for z in root['normalized_complete_first_party_members']+root['normalized_complete_external_input_bindings']+root['ROOT_evidence_and_actual_prerequisite_bindings']:check(z)
    assert root['complete_VERDICT_object']==load(W/'VERDICT.json') and root['complete_VERDICT_object']['verdict']=='PASS_EXACT_CURRENT_KNOWN_RESULT_NO_MANDATORY_CORRECTION'
    for group in root['complete_actual_closing_and_postclosing_readback_captures']:
        for z in group['complete_members']:check(z)
        cap=load(R/group['capture']['path']);assert cap==group['complete_capture'] and cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0
    outer=R/'draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr46_whole_ROOT_record_authoring_v2_actual_capture';cap=load(outer/'CAPTURE.json');assert cap['pid']==14371 and cap['exit_code']==0 and cap['actual_execution'] is True and cap['completed'] is True
    for channel in ['stdout','stderr']:
        z=cap[channel];body=(outer/z['path']).read_bytes();assert len(body)==z['bytes'] and sha(body)==z['sha256']
    assert load(outer/'stdout.bin')['record']['sha256']==sha(rootpath.read_bytes())
    previous=load(H/'INPUT_BINDINGS.json');assert previous['whole_binding_completed'] is False
    put('EXPECTED_WHOLE_MANIFEST.json',mf);put('EXPECTED_WHOLE_VERDICT.json',root['complete_VERDICT_object']);put('EXPECTED_ROOT_WHOLE_REVIEW.json',root);put('EXPECTED_EXTERNAL_INPUT_INVENTORY.json',load(W/'READBACK_RESULT.json'))
    inputs=previous.copy();inputs.update(whole_binding_completed=True,closed_whole_manifest=pin(W/'MANIFEST.json'),closed_whole_result=pin(W/'VERDICT.json'),closed_whole_report=pin(W/'AUDIT.md'),closed_root_whole_inspection=pin(rootpath),closed_whole_external_inventory=pin(W/'READBACK_RESULT.json'),external_input_count=1877,external_input_rows=[{**z,'path':str(R/z['path'])} for z in root['normalized_complete_external_input_bindings']],root_whole_read_completed_utc=root['created_utc'])
    pins=dict(inputs['pins'])
    paths=[rootpath,W/'MANIFEST.json',W/'VERDICT.json',W/'AUDIT.md',W/'READBACK_RESULT.json',A/'author_ROOT_whole_review_v2.py',A/'ROOT_WHOLE_REVIEW_V2_PRELAUNCH_SOURCE.py']+[p for p in outer.iterdir() if p.is_file()]
    for group in root['complete_actual_closing_and_postclosing_readback_captures']:paths += [R/z['path'] for z in group['complete_members']]
    for path in paths:pins[str(path.relative_to(R))]=pin(path)
    inputs['pins']=pins;(H/'INPUT_BINDINGS.json').write_text(json.dumps(inputs,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
    archive=H/'PRE_WHOLE_AND_FORMAT_SOURCE';archive.mkdir();delta=[]
    for name in ['pr46_guards.py','independent_controls.py']:
        p=H/name;before=p.read_text();(archive/name).write_bytes(p.read_bytes());after=before
        if name=='pr46_guards.py':
            after=after.replace("WHOLE_VERDICT = 'PASS_WHOLE_CURRENT_SCOPED_NO_MANDATORY_CORRECTION'", "WHOLE_VERDICT = 'PASS_EXACT_CURRENT_KNOWN_RESULT_NO_MANDATORY_CORRECTION'")
            old="        if z['path'].endswith('.json'): parse(regular(base,z['path']).read_bytes())\n        if z['path'].endswith('.jsonl'):\n            raw=regular(base,z['path']).read_bytes(); require(not raw or raw.endswith(b'\\n'),'Incomplete JSONL')\n            for line in raw.splitlines(): parse(line)"
            new="""        raw=regular(base,z['path']).read_bytes()
        if z['path'].endswith('.json'):
            # Historical literal empty failed stdout is preserved, never a PASS object.
            if z['path']=='family_evidence/projective_algebra_family/failed01_run_stdout.json' and Path(base) in {C,K}:
                require(raw==b'' and z['bytes']==0 and z['sha256']=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','Exact literal empty failed stdout only')
            else:parse(raw)
        if z['path'].endswith('.jsonl'):
            archives={'original_preparation_archive/original_native_selected/assessment_history.jsonl':'0c7d72e9e188763a743e59ea13367ba23d66bf8dbaa5c67d7d0f325cee8ffeb5','original_preparation_archive/original_native_selected/history.jsonl':'cd650a0dec4b3ff77299d73300268e7bd465484f4b296636336f28ecdd79ae31'}
            if z['path'] in archives and Path(base) in {C,K}:
                require(sha(raw)==archives[z['path']],'Exact historically named JSONL selected-history object bytes');record=parse(raw);required(record,{'selection_only':True,'selected_problem_id':ID,'complete_selected_objects':[],'priority_or_claim_verification':False},'Historical selected-history JSON object, not event ledger')
            else:
                require(not raw or raw.endswith(b'\\n'),'Incomplete actual JSONL')
                for item in raw.splitlines():parse(item)"""
            assert old in after;after=after.replace(old,new)
            after=after.replace("keyset(z,{'path','bytes','sha256'},'Complete absolute excluded input identity')", "keyset(z,{'path','bytes','sha256','full_mode'},'Complete absolute excluded input identity')")
            after=after.replace("names.add(p.relative_to(R).as_posix())", "require(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Full excluded input mode changed');names.add(p.relative_to(R).as_posix())",1)
            anchor="    require(root['future_execution_approved'] is False,'Whole reading supplies no future execution approval');"
            after=after.replace(anchor,"    required(root,{'schema':'pr46-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','candidate_manifest_sha256':CURRENT_SHA,'closed_whole_manifest_sha256':wm['sha256'],'first_party_members':245,'individually_bound_foreign_inputs':1877,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_external_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'closing_and_postexit_capture_chronology_checked':True,'ROOT_actual_inner45_complete_read':True,'frozen_inner43_honest_prefix':True,'dated_native4_current_HEAD_not_future_acceptance_authority':True,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved_by_project':False,'future_execution_approved':False,'future_acceptance_approved':False,'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'human_peer_review_claimed':False},'Entire standalone genuine ROOT known-result whole record');\n"+anchor)
        else:
            after=after.replace("root=H/'OWN_READONLY_GIT'", "root=H/'OWN_READONLY_GIT_V2'")
            after=after.replace("if z['path'].endswith('.json') and raw:parse(raw)","if p.parent==C and z['path'].endswith('.json') and raw:parse(raw)")
            after=after.replace("if z['path'].endswith('.jsonl'):","if p.parent==C and z['path'].endswith('.jsonl'):")
            after=after.replace("            for line in raw.splitlines():parse(line)","            if z['path'] in {'original_preparation_archive/original_native_selected/assessment_history.jsonl','original_preparation_archive/original_native_selected/history.jsonl'}:parse(raw)\n            else:\n                for line in raw.splitlines():parse(line)")
            after=after.replace("check('honest pending whole gate',inputs['whole_binding_completed'] is False and inputs['closed_whole_manifest'] is None and inputs['closed_whole_result'] is None and inputs['closed_root_whole_inspection'] is None)","check('genuine now completed whole binding',inputs['whole_binding_completed'] is True and inputs['closed_whole_manifest']['sha256']=='be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2' and inputs['closed_root_whole_inspection']['sha256']=='ed0cc07fd852881a0b9a9893e6c2ec7f25e6e6d2f3d1bfb26bfa88a7a0b17b54');inspect_manifest(A/'current_whole_adversary_family/MANIFEST.json',245)\n    for z in inputs['external_input_rows']:\n        b=read(Path(z['path']),z);check('normalized actual external full mode '+z['path'],stat.S_IMODE(Path(z['path']).stat().st_mode)==z['full_mode'])")
            after=after.replace("check('proposed no child approval production text',all('PENDING_ROOT' in texts[n] or n not in [] for n in production))", "check('proposed explicit ROOT authority gates in source text',\"root_binding_input\" in texts['pr46_guards.py'] and \"g.require(a.execute\" in texts['seal_final_evidence.py'] and \"g.args(p)\" in texts['verify_post_acceptance.py'])")
        p.write_text(after);delta.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='PRE_WHOLE_AND_FORMAT_SOURCE/'+name,tofile=name))
    put('GENUINE_WHOLE_AND_FORMAT_REPAIR.patch',''.join(delta));status=load(H/'SOURCE_STATUS.json');status.update(status='BOUND_GENUINE_CLOSED_WHOLE_PENDING_PRIVATE_CONTROLS_AND_ROOT_SOURCE_REVIEW',whole_binding_completed=True);(H/'SOURCE_STATUS.json').write_text(json.dumps(status,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'SOURCE_BOUND_GENUINE_WHOLE_ROOT','root_whole_record_sha256':sha(rootpath.read_bytes()),'closed_whole_payload_files':245,'complete_external_rows':1877,'ROOT_actual_author_pid':14371,'future_ROOT_acceptance_approved':False,'production_executed':False},sort_keys=True))
if __name__=='__main__':main()
