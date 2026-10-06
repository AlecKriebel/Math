#!/usr/bin/env python3
"""Pure carryforward framing/scope controls; no assess/main/actions/services."""
import pathlib,types,os,json,copy,ast,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,path):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m;exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
v=module('independent_carry_preexecution_helpers',W/'verify_actual_candidate.py');A=v.A;D=A/'native_post_assess_carryforward_v3_20261006';OLD=A/'native_execution_programs_v1/workspaces/candidate_d9eb646c1dd70e89'
def ap(path):return {'path':str(path.relative_to(A)),**v.regular(path,retain=False)}
def main():
    started=v.now();mode='optimized' if sys.flags.optimize else 'normal';payload=v.obj(v.regular(D/'OUTPUT_MANIFEST.json'));seal=v.obj(v.regular(D/'SEAL_RECEIPT.json'))
    v.check(v.pin(v.regular(D/'OUTPUT_MANIFEST.json'))=={k:seal['manifest_pin'][k] for k in ['bytes','sha256']} and payload['file_count']==len(payload['files'])==14 and payload['total_bytes']==201649 and sum(z['bytes'] for z in payload['files'])==201649,'Exact final sealed linear carryforward payload')
    for s in payload['files']:v.regular(D/s['path'],s)
    c=module('independent_reviewed_carry_source',D/'post_assess_carryforward_v3.py');a=module('independent_reviewed_phase_v3',D/'native_acceptance_actions_v4.py');p=v.obj(v.regular(v.PACKET));before=v.prepare(p)
    oldsource=ast.parse(v.regular(A/'native_post_assess_carryforward_v2_20261006/post_assess_carryforward.py'));newsource=ast.parse(v.regular(D/'post_assess_carryforward_v3.py'))
    for name in ['need','canon','hp','now','load_module','startup_read','audit','corrected_protocol','original_preconditions','verify_seed']:
        x=next(n for n in oldsource.body if isinstance(n,ast.FunctionDef) and n.name==name);y=next(n for n in newsource.body if isinstance(n,ast.FunctionDef) and n.name==name);v.check(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False),'Entire previously reviewed narrow continuation guard unchanged '+name)
    phaseold=ast.parse(v.regular(A/'native_post_assess_carryforward_v2_20261006/native_acceptance_actions_v3.py'));phasenew=ast.parse(v.regular(D/'native_acceptance_actions_v4.py'))
    for n in phaseold.body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='load_gate':
            y=next(z for z in phasenew.body if isinstance(z,type(n)) and z.name==n.name);v.check(ast.dump(n,include_attributes=False)==ast.dump(y,include_attributes=False),'All unchanged previous phase definitions '+n.name)
    body=v.audit(p['program_files']['protocol.py']);strict=c.load_module('independent_historical_strict',body,A/'native_execution_programs_v1/protocol.py');scopedp=c.corrected_protocol(strict,body,A/'native_execution_programs_v1/protocol.py')
    f=A/'current_main_carryforward_input_20261006/CURRENT_INTEGRATION_INPUTS.json';integration,q0,q1,delta=a.validate_integration_inputs(ap(f),p)
    v.check(q0==before['QUEUE.md'],'Full historical queue pin equals independent original Git read')
    stopped=a.verify_stopped_continuation(ap(A/'native_post_assess_carryforward_v2_20261006/STOPPED_CONTINUATION_INVENTORY.json'));v.check(sorted(stopped['files'],key=lambda x:x['path'])==sorted(v.obj(v.regular(W/'REMOTE_MAIN_STOP_RESULT.json'))['full_stopped_workspace_inventory'],key=lambda x:x['path']),'Second stop inventory independently identical')
    cpu=a.verify_stopped_CPU_continuation(ap(D/'STOPPED_CPU_CONTINUATION_INVENTORY.json'));owncpu=v.obj(v.regular(W/'CPU_STOP_CUSTODY_RESULT.json'));v.check(cpu['files']==owncpu['full_inventory'] and len(cpu['checked_artifacts'])==142,'All129 CPU-stopped bodies independently identical/full142 outer artifacts')
    linear=v.regular(D/'linear_full_diff.py');normal=v.obj(v.regular(W/'LINEAR_DIFF_CONTROL_normal.json'));optimized=v.obj(v.regular(W/'LINEAR_DIFF_CONTROL_optimized.json'));v.check(normal['helper_pin']==optimized['helper_pin']==ap(D/'linear_full_diff.py') and normal['all84_actual_stopped_offers_applied_exactly'] is True and optimized['all84_actual_stopped_offers_applied_exactly'] is True,'Exact helper independently applies full84 in normal/O')
    seed=v.obj(v.regular(A/'native_post_assess_continuation_v1_20261006/SEED_INVENTORY.json'));c.verify_seed(a,seed)
    worker=v.obj(v.regular(OLD/'WORKER_RESULT.json'));after={n:v.regular(OLD/'private_native_backend'/n,worker['output_pins'][n]) for n in v.NAMES};event=scopedp.imported_baseline(p['import_UTC'],scopedp.ORIGINAL_ROW_SHA,scopedp.ORIGINAL_LOG_SHA);historical,drift=scopedp.scoped_outputs(before,after,p['assessment_overlay'],event,p['campaign_note'],'10.5281/zenodo.23191247');current_before={**before,'QUEUE.md':q1};current,currentdrift=scopedp.scoped_outputs(current_before,after,p['assessment_overlay'],event,p['campaign_note'],'10.5281/zenodo.23191247')
    root=v.obj(v.regular(A/'ROOT_FAILED_NATIVE_RUN_AUTHENTICATION_20261006.json'));v.check({n:v.pin(b) for n,b in historical.items()}==root['proposed_derived_pins'],'Full actual historical scoped replay still agrees')
    v.check(currentdrift==drift and all(current[n]==historical[n] for n in current if n!='QUEUE.md'),'Seven other derived outputs and drift exactly equal across two baselines')
    lines0=q1.splitlines(keepends=True);lines1=current['QUEUE.md'].splitlines(keepends=True);changed=[i for i,(x,y) in enumerate(zip(lines0,lines1)) if x!=y];v.check(len(lines0)==len(lines1) and len(changed)==1 and lines0[changed[0]].decode().split('|')[2].split('/')[0].strip()==v.K and lines0[307]==lines1[307],'Only target row changes; current independent problem row308 retained byte-exact')
    controls=[];controlroot=W/('linear_carryforward_mutants_'+mode);controlroot.mkdir(exist_ok=False)
    def artifact(name,data):
        path=controlroot/name;path.open('xb').write(data);return ap(path)
    def rejected(label,item,packet=p):
        spec=artifact(label+'.json',v.canon(item))
        try:a.validate_integration_inputs(spec,packet)
        except (ValueError,RuntimeError):controls.append(label);return
        raise RuntimeError('Guard accepted mutant '+label)
    for key,value in [('main_parent',p['main_parent']),('original_assessed_main_parent',integration['main_parent']),('original_worker_not_reassessed',False),('target_QUEUE_row_unchanged',False),('science_priority_publication_tracker_unchanged',False),('changed_physical_row_number',True)]:
        x=copy.deepcopy(integration);x[key]=value;rejected(key,x)
    x=copy.deepcopy(integration);x['native_baseline']['state.json']['sha256']='0'*64;rejected('unrelated_native_body',x)
    x=copy.deepcopy(integration);x['changed_paths']=x['changed_paths'][:-1];rejected('missing_declared_path',x)
    for label,mutantdelta in [('foreign_added_path',delta.replace(b'unsolved_math_prioritization/attempts/30005460/FROZEN_MANIFEST.json',b'unsolved_math_prioritization/attempts/5100032/FROZEN_MANIFEST.json')),('wrong_delta_status',delta.replace(b'A\0',b'D\0',1))]:
        x=copy.deepcopy(integration);x['Git_delta_pin']=artifact(label+'.delta.bin',mutantdelta);rejected(label,x)
    x=copy.deepcopy(integration);modified=q1.replace(lines0[changed[0]],lines0[changed[0]].replace(b'2/5',b'3/5') if b'2/5' in lines0[changed[0]] else lines0[changed[0]].replace(b'0/5',b'3/5'));v.check(modified!=q1,'Meaningful target-row mutant');spec=artifact('target_row_modified.bin',modified);x['current_QUEUE_pin']=spec;x['native_baseline']['QUEUE.md']={**x['native_baseline']['QUEUE.md'],**v.pin(modified)};rejected('target_row_modified',x)
    x=copy.deepcopy(integration);modified=q1.replace(lines0[307],lines0[307].replace(b'30005460 /',b'30005461 /'));spec=artifact('foreign_row_identity.bin',modified);x['current_QUEUE_pin']=spec;x['native_baseline']['QUEUE.md']={**x['native_baseline']['QUEUE.md'],**v.pin(modified)};rejected('foreign_row_identity',x)
    rejected('historical_packet_main_falsified',copy.deepcopy(integration),packet={**p,'main_parent':integration['main_parent']})
    for path in [A/'publication_build_v1/record_native_carryforward_v3.py',A/'publication_build_v1/record_native_action_v4.py',A/'publication_build_v1/commission_post_assess_carryforward_v3.py',A/'publication_build_v1/commission_native_action_v4.py']:v.regular(path)
    v.check(not (D/'workspaces/candidate_d9eb646c1dd70e89').exists(),'No hypothetical output promoted')
    result={'schema':'pr110-independent-carryforward-preexecution-controls/v1','UTC_start':started,'UTC_end':v.now(),'actual_reviewer_PID':os.getpid(),'mode':mode,'checks':v.checks,'fixture_controls_only':True,'actual_source_definition_imports_and_pure_replay_only':True,'main_or_assess_or_action_or_service_executed':False,'mutation_rejections':controls,'sealed_payload_files_authenticated':payload['file_count'],'stopped_CPU_continuation_inventory_pin':ap(D/'STOPPED_CPU_CONTINUATION_INVENTORY.json'),'linear_diff_program_pin':ap(D/'linear_full_diff.py'),'original_resource_policy_unchanged':True,'all_three_stopped_workspaces_preserved':True,'historical_scoped_pins_match_root':True,'seven_other_derived_outputs_and_drift_unchanged':True,'current_other_problem_QUEUE_row308_byteexact':True,'current_scoped_pins':{n:v.pin(b) for n,b in current.items()},'both_stopped_workspaces_preserved':True,'packet_sha256':v.PACKET_SHA,'program_pin':ap(D/'post_assess_carryforward_v3.py'),'action_program_pin':ap(D/'native_acceptance_actions_v4.py'),'integration_inputs_pin':ap(f),'stopped_continuation_inventory_pin':ap(A/'native_post_assess_carryforward_v2_20261006/STOPPED_CONTINUATION_INVENTORY.json'),'outer_launcher_pin':ap(A/'publication_build_v1/record_native_carryforward_v3.py'),'future_action_outer_pin':ap(A/'publication_build_v1/record_native_action_v4.py'),'verification_source_pin':v.pin(pathlib.Path(__file__).read_bytes()),'future_candidate_approved':False,'Git_mutations':0,'service_calls':0,'native_assess_calls':0}
    v.save('LINEAR_CARRYFORWARD_PREEXEC_CONTROLS_'+mode+'.json',result);v.save('LINEAR_CARRYFORWARD_PREEXEC_GIT_READS_'+mode+'.json',{'actual_reviewer_PID':os.getpid(),'actual_processes':v.journal});print(json.dumps({k:z for k,z in result.items() if k not in ['mutation_rejections','current_scoped_pins']}))
if __name__=='__main__':main()
