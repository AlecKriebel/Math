#!/usr/bin/env python3
"""Independent actual continued-candidate audit; immutable baseline reads only."""
import pathlib,types,os,json,sys,stat
ROOT=pathlib.Path(__file__).resolve().parent
v=types.ModuleType('independent_continued_verifier');v.__file__=str(ROOT/'verify_actual_candidate.py')
exec(compile(pathlib.Path(v.__file__).read_bytes(),v.__file__,'exec'),v.__dict__)
# Reuse the already reviewed independent preservation helpers. The new actual
# routine below is a revised copy, never a prepared-source-derived conclusion.
globals().update({k:z for k,z in v.__dict__.items() if k not in {'__name__','__file__','__doc__','__builtins__'}})
OLD=A/'native_execution_programs_v1/workspaces/candidate_d9eb646c1dd70e89'
D=A/'native_post_assess_carryforward_v3_20261006'
def actual(p,before,candidate,historical):
    # Filled only for genuine supplied output; never creates a candidate or gate.
    r=obj(regular(candidate/'CANDIDATE_RECEIPT.json'));check(r['schema']=='pr110-actual-post-assess-carryforward-candidate/v1' and r['packet_sha256']==PACKET_SHA,'Actual candidate identity')
    check(candidate==A/'native_post_assess_carryforward_v3_20261006/workspaces'/('candidate_'+PACKET_SHA[:16]),'Exact exclusive candidate')
    check(r['main_parent']==p['main_parent'] and r['original_head']==HEAD and not r['native_export_executed'] and r['Git_mutations']==0 and r['service_writes']==0,'Private-only actual candidate')
    check(regular(OLD/'EXECUTION_INPUTS.json')==regular(PACKET),'Staged immutable actual packet')
    for name,s in p['program_files'].items():check(regular(OLD/name)==audit(s),'Staged exact four sources')
    control_b=regular(OLD/'WORKER_CONTROL.json');control=obj(control_b);worker=obj(regular(OLD/'WORKER_RESULT.json'))
    check(worker['outcome']=='success' and worker['native_assess_call_attempted'] is True and worker['native_assess_completed'] is True,'Literal native assess completed')
    check(worker['actual_worker_PID']==r['native_assess_actual_PID'] and worker['control_sha256']==sha(control_b) and worker['validated_control']==control,'Actual worker/control correspondence')
    check(control['resources']==p['resources'] and control['fixture'] is False and set(control['pre_assess_pins'])==set(NAMES)|{'assessment.json'},'Complete genuine thirteen-preimage worker control')
    oldstates=obj(before['state.json']);oldass=obj(before['assessments.json']);overlay=p['assessment_overlay']
    after={name:regular(OLD/'private_native_backend'/name,worker['output_pins'][name]) for name in NAMES}
    event=obj(regular(candidate/'offer'/PREFIX/'IMPORT_BASELINE.json'))
    check(event['at']==p['import_UTC'] and event['event']=='dated_import_of_authenticated_author_count' and event['turns_used']==2 and event['status']=='claimed_solved' and event['original_structured_ledger_present'] is False and event['new_central_proof_search_turns']==0,'One honest dated two-turn import event')
    expected_state={**oldstates,K:event};expected_hist=before['history.jsonl']+json.dumps(event,ensure_ascii=False).encode()+b'\n'
    for name in NAMES:
        pre=historical[name]
        if name=='state.json':pre=(json.dumps(expected_state,ensure_ascii=False,indent=2)+'\n').encode()
        if name=='history.jsonl':pre=expected_hist
        check(control['pre_assess_pins'][name]==pin(pre),'Actual pre-assess full pin independently derived '+name)
    check(control['pre_assess_pins']['assessment.json']==pin(canon({**oldass[K],**overlay})),'Exact reviewed metadata-only assessment input')
    for name in ['queue.py','manifest.json','policy.json','SHORTLIST.md']:check(after[name]==before[name],'Immutable native runtime input')
    newstates=obj(after['state.json']);check(ordered(newstates)==ordered(expected_state),'All state objects and key order preserved, with one import')
    check(after['history.jsonl']==expected_hist,'Full history prefix and exactly one honest import')
    newass=obj(after['assessments.json']);check(list(newass)==list(oldass),'All assessment outer key order')
    for key in oldass:
        if key!=K:check(ordered(newass[key])==ordered(oldass[key]),'Unrelated assessment full object/key order')
    expected={**oldass[K],**overlay,'clear_holds':{}};check(canon({k:v for k,v in newass[K].items() if k!='reviewed_at'})==canon({k:v for k,v in expected.items() if k!='reviewed_at'}),'Target changes only reviewed descriptive metadata')
    check(stamp(worker['UTC_start']).replace(microsecond=0)<=stamp(newass[K]['reviewed_at'])<=stamp(worker['UTC_end']),'Actual assessment timestamp lies inside worker')
    suffix=after['assessment_history.jsonl'][len(before['assessment_history.jsonl']):]
    check(after['assessment_history.jsonl'].startswith(before['assessment_history.jsonl']) and len(suffix.splitlines())==1 and obj(suffix)=={'id':K,**newass[K]},'Full assessment history prefix and exactly one current target event')
    offered={x['path']:regular(candidate/'offer'/x['path'],x['after']) for x in r['affected_paths']}
    check(len(offered)==len(r['affected_paths']) and len(offered)<=256,'Unique complete offered path set')
    found={str(f.relative_to(candidate/'offer')) for f in (candidate/'offer').rglob('*') if f.is_file()};check(found==set(offered),'No missing or extra offer member')
    for name,s in p['attempt_offer_sources'].items():check(offered[name]==audit(s),'Every authenticated source offer preserved exactly')
    generated=['IMPORT_BASELINE.json','HISTORICAL_DESK_ASSESSMENT.json','assessment.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md']
    check(set(offered)==set(p['attempt_offer_sources'])|{'unsolved_math_prioritization/'+n for n in DERIVED if after[n]!=before[n]}|{PREFIX+n for n in generated},'Exact reviewed target/generated/eight-global offer')
    for name in ['assessments.json','state.json']:
        check(ordered(obj(offered['unsolved_math_prioritization/'+name]))==ordered(obj(after[name])),'Actual scoped metadata retains every worker object/type/key order '+name)
    for name in ['history.jsonl','assessment_history.jsonl']:
        check(offered['unsolved_math_prioritization/'+name]==after[name],'Offered full ledger retains actual worker bytes '+name)
    check(obj(offered[PREFIX+'assessment.json'])==newass[K],'Offered target assessment equals actual native target')
    check(obj(offered[PREFIX+'HISTORICAL_DESK_ASSESSMENT.json'])==oldass[K],'Historical desk assessment equals complete main baseline')
    evidence=obj(offered[PREFIX+'PUBLICATION_EVIDENCE.json']);acceptance=obj(offered[PREFIX+'ACCEPTANCE_EVIDENCE.json'])
    check(evidence['DOI']=='10.5281/zenodo.23191247' and evidence['Sheet_range']=="'Math Puzzles'!A32:D32" and evidence['original_head']==HEAD and evidence['review_hash']==p['identity']['review_hash'] and evidence['statement_hash']==p['identity']['statement_hash'] and evidence['packet_sha256']==PACKET_SHA and evidence['original_budget']=='2/5' and evidence['new_central_proof_search_turns']==0,'Full generated publication identity and literal effort')
    check(acceptance['schema']=='pr110-reviewed-full-resolution-native-continuation-candidate/v1' and acceptance['actual_continuation_PID']==r['operator_PID'] and acceptance['successful_existing_worker_PID']==23360 and acceptance['native_assess_calls_during_continuation']==0 and acceptance['holds_cleared'] is False and acceptance['candidate_only'] is True and acceptance['native_export_executed'] is False and acceptance['live_native_acceptance_executed'] is False and acceptance['fresh_candidate_review_required'] is True,'Generated dated evidence stays honest about private candidate')
    check(b'No reassessment' in offered[PREFIX+'README.md'] and b'All three stopped workspaces remain intact and nonexportable' in offered[PREFIX+'README.md'],'Generated readme correctly describes continuation and preserved failure')
    oldcat=obj(before['catalog.json']);newcat=obj(offered['unsolved_math_prioritization/catalog.json']);check([x['id'] for x in oldcat]==[x['id'] for x in newcat],'All catalog physical list positions')
    generated_cat=obj(after['catalog.json']);generated_map={x['id']:x for x in generated_cat};check(len(generated_map)==len(generated_cat)==len(oldcat) and set(generated_map)=={x['id'] for x in oldcat},'Actual native regeneration complete identity set')
    explained=[]
    for old in oldcat:
        g=generated_map[old['id']]
        if old['id']==K:continue
        changed={key for key in set(old)|set(g) if key not in old or key not in g or ordered(old[key])!=ordered(g[key])}
        check(changed<={'rank','local_status','turns_used','eligible'},'Native regeneration did not change unrelated scores/source/metadata')
        if changed-{'rank'}:
            st=newstates.get(old['id'],{});assessment=newass.get(old['id'],{})
            if old['present']:
                default='queued' if assessment.get('decision')=='candidate' else 'deferred' if assessment.get('decision') in ['defer','exclude'] else 'unreviewed'
                if default=='queued' and old['holds']:default='unreviewed'
                if assessment.get('resolution')=='already_solved' and assessment.get('review_hash')==old['review_hash']:default='already_solved'
                status=st.get('status',default);turns=st.get('turns_used',0)
            else:status=st.get('status',old['local_status']);turns=old['turns_used']
            eligible=bool(old['present'] and not old['holds'] and status in ['queued','unreviewed','ready'] and turns<5)
            check(g['local_status']==status and type(g['turns_used']) is int and g['turns_used']==turns and g['eligible'] is eligible,'Each restored unrelated projection drift has an exact native explanation')
            explained.append({'id':old['id'],'fields':sorted(changed),'baseline_preserved':True})
    check(r['unrelated_projection_drift_restored']==explained,'Every reported unrelated projection restoration independently reproduced')
    for x,y in zip(oldcat,newcat):
        if x['id']!=K:check(ordered(x)==ordered(y),'Full unrelated catalog object/key/score/rank preservation')
        else:
            allowed={'local_status','turns_used','eligible','rank','desk_note'}
            check(ordered({k:v for k,v in x.items() if k not in allowed})==ordered({k:v for k,v in y.items() if k not in allowed}),'Target source/score/holds/metadata preserved')
            check(list(x)==list(y) and y['local_status']=='claimed_solved' and y['turns_used']==2 and y['eligible'] is False and y['rank'] is None and y['desk_note']==overlay['note'],'Target scoped native projection')
    oldcsv=csv_rows(before['ranking.csv']);newcsv=csv_rows(offered['unsolved_math_prioritization/ranking.csv']);check(len(oldcsv)==len(newcsv) and oldcsv[0]==newcsv[0],'CSV header/count')
    columns=oldcsv[0][0];idcol=columns.index('id');target_count=0
    for old,new in zip(oldcsv[1:],newcsv[1:]):
        check(old[0][idcol]==new[0][idcol],'All physical CSV row positions')
        if old[0][idcol]!=K:check(old[1]==new[1],'Every unrelated CSV physical byte')
        else:
            target_count+=1;d0=dict(zip(columns,old[0]));d1=dict(zip(columns,new[0]));allowed={'local_status','turns_used','eligible','rank','desk_note'}
            check({k:v for k,v in d0.items() if k not in allowed}=={k:v for k,v in d1.items() if k not in allowed},'Target CSV scores/source fields retained')
            check(d1['local_status']=='claimed_solved' and d1['turns_used']=='2' and d1['eligible']=='False' and d1['rank']=='' and d1['desk_note']==overlay['note'],'Target CSV projection')
    check(target_count==1,'Exactly one target CSV row')
    oldqueue=before['QUEUE.md'].splitlines(keepends=True);newqueue=offered['unsolved_math_prioritization/QUEUE.md'].splitlines(keepends=True);check(len(oldqueue)==len(newqueue),'Full campaign line count')
    qchanges=[]
    for i,(old,new) in enumerate(zip(oldqueue,newqueue)):
        if old==new:continue
        qchanges.append(i);cells0=old.decode().split('|');cells1=new.decode().split('|');check(cells0[2].strip()==K+' / AMR-050-0032','Only target campaign row')
        check([v for j,v in enumerate(cells0) if j not in {8,9,11,12}]==[v for j,v in enumerate(cells1) if j not in {8,9,11,12}],'Campaign separate scores/rank/fields preserved')
        check(cells1[8].strip()=='claimed_solved' and cells1[9].strip()=='2/5' and cells1[11].strip()==p['campaign_note'] and cells1[12].strip()=='https://doi.org/10.5281/zenodo.23191247','Exact reviewed campaign delta')
    check(len(qchanges)==1,'Exactly one campaign line changed')
    check('unsolved_math_prioritization/SHORTLIST.md' not in offered,'Old SHORTLIST is not exported')
    oldsummary=obj(before['summary.json']);summary=obj(offered['unsolved_math_prioritization/summary.json'])
    check(list(summary)==list(oldsummary),'Summary top-level key order')
    for k in oldsummary:
        if k not in {'records','eligible','assessed','holds'}:check(ordered(summary[k])==ordered(oldsummary[k]),'Unrelated summary metadata retained')
    check(summary['records']==15458 and summary['assessed']==len(newass) and summary['eligible']==sum(x['eligible'] for x in newcat) and summary['holds']==dict(collections.Counter(h.split(':')[0] for x in newcat for h in x['holds'])),'Scoped summary derived from offered full catalog')
    # Apply the complete representation independently, without importing the generator.
    for row in r['affected_paths']:
        name=row['path'];old=before.get(name.removeprefix('unsolved_math_prioritization/')) if name in {'unsolved_math_prioritization/'+n for n in NAMES} else None
        check(row['before']==(None if old is None else pin(old)),'Every actual offered current preimage pin')
    applier=types.ModuleType('independent_complete_patch_application');applier.__file__=str(ROOT/'verify_linear_diff.py');exec(compile(pathlib.Path(applier.__file__).read_bytes(),applier.__file__,'exec'),applier.__dict__)
    expected_diff=regular(candidate/'DIFF.txt',r['DIFF_pin']);entry_application=applier.apply_all(expected_diff,before,offered)
    check(len(entry_application)==84 and len(expected_diff)<=1024*1024,'Every84 actual DIFF entry exact fully applied, cap retained')
    return {'candidate_receipt_pin':pin(regular(candidate/'CANDIDATE_RECEIPT.json')),'DIFF_pin':pin(expected_diff),'offered_files':len(offered),'actual84_complete_DIFF_application':entry_application,'independent_patch_application_guards':applier.checks,'unrelated_catalog_records_preserved':len(oldcat)-1,'unrelated_assessments_preserved':len(oldass)-1,'unrelated_physical_CSV_rows_preserved':len(oldcsv)-2,'native_process_and_outer_custody':'Requires separately supplied actual outer receipt and independent final audit'}
def main():
    started=now();original=obj(regular(PACKET));historical=prepare(original)
    review=obj(regular(ROOT/'LINEAR_CARRYFORWARD_PREEXEC_ADVERSARY.json'))
    integration=obj(audit(review['integration_inputs_pin']))
    p={**original,'main_parent':integration['main_parent'],'native_baseline':integration['native_baseline']}
    before={}
    for name,spec in p['native_baseline'].items():
        before[name]=git_blob(p,name);check(pin(before[name])=={k:spec[k] for k in ['bytes','sha256']},'Current full integration preimage independently reproduced')
    check(all(before[n]==historical[n] for n in before if n!='QUEUE.md'),'Eleven other current/native bodies remain equal to assessed baseline')
    check(pin(before['QUEUE.md'])=={k:integration['current_QUEUE_pin'][k] for k in ['bytes','sha256']},'Exact current whole QUEUE is the offer/DIFF baseline')
    candidate=D/'workspaces'/('candidate_'+PACKET_SHA[:16])
    receipt=obj(regular(candidate/'CANDIDATE_RECEIPT.json'))
    check(not os.path.lexists(candidate/'FAILURE.json'),'Actual continued candidate has no failure')
    check(receipt['native_assess_calls_during_continuation']==0 and type(receipt['native_assess_calls_during_continuation']) is int and receipt['holds_cleared'] is False and receipt['empty_clear_holds_generated_metadata_only'] is True and receipt['original_failure_preserved'] is True,'Actual no-reassessment/hold/failure facts')
    check(receipt['native_assess_actual_PID']==receipt['successful_existing_worker_PID']==23360 and receipt['failed_original_operator_PID']==23224 and receipt['actual_continuation_PID']==receipt['operator_PID'] and receipt['operator_PID'] not in [23224,23360],'Actual continuation and existing old worker distinguished')
    check(receipt['source_workspace']==str(OLD),'Exact immutable old worker source')
    audit(receipt['continuation_program_pin']);audit(receipt['continuation_action_program_pin']);audit(receipt['failed_run_root_authentication_pin'])
    check(receipt['continuation_program_pin']==review['program_pin'] and receipt['continuation_action_program_pin']==review['action_program_pin'],'Exact independently reviewed continuation/action source')
    seed=obj(audit(receipt['seed_inventory_pin']));names=set();total=0
    for s in seed['files']:regular(OLD/s['path'],s);names.add(s['path']);total+=s['bytes']
    check(names=={str(f.relative_to(OLD)) for f in OLD.rglob('*') if f.is_file()} and len(names)==61 and total==49629753,'Original whole failure seed inventory remains exact')
    check(receipt['source_failure_pin']==regular(OLD/'FAILURE.json',retain=False) and receipt['source_worker_result_pin']==regular(OLD/'WORKER_RESULT.json',retain=False),'Actual preserved failure/result correspondence')
    check(receipt['integration_inputs_pin']==review['integration_inputs_pin'] and receipt['original_assessed_main_parent']==original['main_parent'] and receipt['main_parent']==p['main_parent'],'Actual historical/current input binding')
    stopped=obj(audit(receipt['stopped_continuation_inventory_pin']));stoproot=pathlib.Path(stopped['source_workspace'])
    for entry in stopped['files']:regular(stoproot/entry['path'],entry)
    check({str(f.relative_to(stoproot)) for f in stoproot.rglob('*') if f.is_file()}=={z['path'] for z in stopped['files']} and obj(regular(stoproot/'FAILURE.json'))['candidate_must_not_be_exported'] is True,'Second actual stop preserved and nonexportable')
    check(receipt['linear_diff_program_pin']==review['linear_diff_program_pin'] and receipt['stopped_CPU_continuation_inventory_pin']==review['stopped_CPU_continuation_inventory_pin'] and receipt['original_resource_policy_unchanged'] is True and receipt['preserved_CPU_limit_stop_PID']==59213,'Exact new linear repair and all-third-stop bindings')
    audit(receipt['linear_diff_program_pin']);cpu=obj(audit(receipt['stopped_CPU_continuation_inventory_pin']));cpuroot=pathlib.Path(cpu['source_workspace']);owncpu=obj(regular(ROOT/'CPU_STOP_CUSTODY_RESULT.json'))
    check(cpu['files']==owncpu['full_inventory'],'Third stopped actual inventory matches independent full raw audit')
    for entry in cpu['files']:regular(cpuroot/entry['path'],entry,retain=False)
    for entry in cpu['checked_artifacts']:audit(entry)
    check({str(f.relative_to(cpuroot)) for f in cpuroot.rglob('*') if f.is_file()}=={z['path'] for z in cpu['files']} and all(not os.path.lexists(cpuroot/n) for n in ['DIFF.txt','CANDIDATE_RECEIPT.json','FAILURE.json']),'Third kernel stop remains exact and nonexportable/no synthetic receipt')
    check(receipt['native_status']=='claimed_solved' and receipt['turns_used']==2 and receipt['new_central_proof_search_turns']==0 and receipt['nonempty_prior_preserved'] is True,'Actual native literal status/effort preserved')
    result=actual(p,before,candidate,historical)
    inventory=[]
    for f in candidate.rglob('*'):
        st=f.lstat();check(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe entire actual continued candidate inventory')
        if stat.S_ISREG(st.st_mode):inventory.append({'path':str(f.relative_to(candidate)),**regular(f,retain=False)})
    capacity=receipt['capacity_before_final_receipt'];check(capacity['files']+1==len(inventory) and capacity['bytes']+regular(candidate/'CANDIDATE_RECEIPT.json',retain=False)['bytes']==sum(x['bytes'] for x in inventory),'Actual final receipt allocation/file accounting')
    check(len(inventory)<=p['parent_policy']['file_count_cap'] and sum(x['bytes'] for x in inventory)<=p['parent_policy']['allocation_cap'],'Actual whole output allocation remains bounded')
    result.update(schema='pr110-independent-actual-carryforward-candidate-reproduction/v1',UTC_start=started,UTC_end=now(),actual_reviewer_PID=os.getpid(),checks=v.checks,packet_sha256=PACKET_SHA,continuation_source_sha256=receipt['continuation_program_pin']['sha256'],action_source_sha256=receipt['continuation_action_program_pin']['sha256'],verification_source_pin=pin(pathlib.Path(__file__).read_bytes()),Git_mutations=0,native_assess_calls=0,service_calls=0,full_candidate_inventory=inventory,resource_memory_advisory_exceeded_by_old_worker=True,hard_memory_limit_claimed=False,actual_output_review_complete=True,execution_clearance=False)
    save('ACTUAL_LINEAR_CARRYFORWARD_CANDIDATE_RESULT.json',result);save('ACTUAL_LINEAR_CARRYFORWARD_CANDIDATE_GIT_READ_JOURNAL.json',{'actual_reviewer_PID':os.getpid(),'UTC':now(),'processes':journal})
    print(json.dumps({k:z for k,z in result.items() if k!='full_candidate_inventory'}))
if __name__=='__main__':main()
