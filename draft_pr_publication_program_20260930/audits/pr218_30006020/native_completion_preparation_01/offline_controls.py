"""Synthetic changed-case controls; no live API, Git, original-lock or current-five access."""
import ast,copy,datetime,hashlib,json,os,pathlib,tempfile,types
BASE=pathlib.Path(__file__).absolute().parent
RESULTS=[]
def need(x,msg):
    if type(x) is not bool or not x:raise RuntimeError(msg)
def yes(x,name):need(x,name);RESULTS.append({'control':name,'PASS':True})
def no(fn,name):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,FileExistsError,OSError,AttributeError):
        RESULTS.append({'control':name,'PASS':True});return
    raise RuntimeError('Expected refusal: '+name)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def module(path,name):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def write(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)
    path.chmod(0o444);return {'path':str(path),**pin(raw)}
def main():
    # Byte-exact modules are imported in an owned synthetic checkout; no patches.
    with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as temporary:
        checkout=pathlib.Path(temporary)/'checkout';program=checkout/'draft_pr_publication_program_20260930'
        case=program/'audits/pr218_30006020';fixture=case/'native_completion_preparation_01';fixture.mkdir(parents=True)
        names=('native218_model.py','native218_primitives.py','native_trees_readonly.py','completion_checkpoint.py',
               'concurrent_get_extension.py','ROOT_TERMINAL_INSPECTION.py','BASELINE_MEMBERSHIP.json','completion_consumer.py')
        for name in names:write(fixture/name,(BASE/name).read_bytes())
        h=module(fixture/'native218_model.py','fixture_model');e=module(fixture/'native218_primitives.py','fixture_primitives')
        q=module(fixture/'completion_checkpoint.py','fixture_driver');t=module(fixture/'ROOT_TERMINAL_INSPECTION.py','fixture_terminal')
        baseline=h.source_baseline();facts=h.phase_facts()
        yes(len(baseline['fully_completed_eligible_PRs'])==54 and len(baseline['published_PRs'])==38,'exact_prior54_38_memberships')
        yes(facts['fully_completed_count']==55 and facts['published_count']==39
            and facts['numeric_advance_conditional_on_actual_Root_terminal'] is True
            and facts['advance_to_next_PR_authorized_now'] is False,'54_38_proposals_remain_conditional')
        yes(h.baseline_facts()['next_numeric_intake_cursor']==215,'prior_native_cursor213_not_inferred214')
        casepost={**facts,'conditional_proposal_only':True};progress={**casepost,**h.completion_memberships(),'dated_eligible_total':99}
        lists=t.accounting(h,{'facts':facts},casepost,progress,baseline)
        yes(lists['new_memberships']==h.completion_memberships(),'production_accounting_adds_only218')
        for key in baseline:
            for badlist,label in ((baseline[key],'missing218'),(baseline[key]+[212,218],'adds_admin212'),(baseline[key]+[213,218],'adds_skip213')):
                bad=copy.deepcopy(progress);bad[key]=badlist
                no(lambda bad=bad:t.accounting(h,{'facts':facts},casepost,bad,baseline),key+'_'+label)
        no(lambda:t.accounting(h,{'facts':facts},casepost,{**progress,'fully_completed_count':55.0},baseline),'float_counter_refused')
        no(lambda:t.accounting(h,{'facts':facts},{**casepost,'conditional_proposal_only':False},progress,baseline),'actual_authority_in_five_proposal_refused')
        mark=h.phase_marker();h.markdown_current(b'old PR211/PR212 history\n'+mark+b'\n','completion100',True)
        yes(True,'append_last_unique214_marker_with_old_history')
        for raw,label in ((mark+b'\n'+mark+b'\n','duplicate'),(mark+b'\ntrailing','not_last'),(mark.replace(b'FACTS ',b'FACTS\t')+b'\n','malformed')):
            no(lambda raw=raw:h.markdown_current(raw,'completion100',True),'marker_'+label)
        own=b'30006020 / OWR-14298589-005'
        cells=[b'',b'218',own,b'a',b'b',b'c',b'd',b'e',b'claimed_solved',b'1/5',b'f',b'g',b'h',b'']
        row=b'|'.join(cells)+b'\n'
        yes(h.own_queue_row(row)[0]==row,'canonical_own_queue_row_bytes')
        yes(h.own_queue_row(b'| other | 99999 | edited foreign |\n'+row)[0]==row,'foreign_QUEUE_change_preserves_exact_own_row')
        for prefix in (b' ',b'  ',b'   ',b'\t'):
            no(lambda prefix=prefix:h.own_queue_row(row+prefix+row),'indented_duplicate_'+repr(prefix))
        for replacement,label in ((bytes([96])+own+bytes([96]),'backticks'),(b'['+own+b'](x)','link'),(b'30006020','bare'),(b'30006020 / bad','wrongcode')):
            no(lambda replacement=replacement:h.own_queue_row(row+row.replace(own,replacement)),'noncanonical_duplicate_'+label)
        for alt,label in ((row[1:],'optional_pipe'),(row.rstrip(b'\n')+b' | extra\n','extra_column'),(row.replace(b' | ',b' ',1),'missing_delimiter')):
            no(lambda alt=alt:h.own_queue_row(row+alt),'malformed_duplicate_'+label)
        cm={k:{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-18T01:00:00Z'} for k in ('commit_author','commit_committer')}
        cm['commit_message']=h.COMMIT_MESSAGE
        request,oid=h.commit_request(cm,'a'*40,['b'*40])
        yes(h.hexid(oid) and request['parents']==['b'*40],'neutral_canonical_one_parent_commit')
        for i,text in enumerate(('Closes #218\n','Fixes https://github.com/AlecKriebel/Math/pull/218\n','Resolves AlecKriebel/Math#218\n',h.COMMIT_MESSAGE+'Fixes #218\n',h.COMMIT_MESSAGE.rstrip())):
            no(lambda text=text:h.commit_request({**cm,'commit_message':text},'a'*40,['b'*40]),'auto_close_or_nonexact_message_'+str(i))
        for i,parents in enumerate(([h.ORIGINAL],[h.CURRENT],[h.MERGED],['a'*40,'b'*40])):
            no(lambda parents=parents:h.commit_request(cm,'a'*40,parents),'snapshot_or_remerge_parent_'+str(i))
        pr={'number':218,'title':'30006020: audited intermediate-area cylinder theorem and published preprint',
            'state':'closed','draft':False,'merged':True,'merged_at':'2026-10-15T07:35:42Z','merge_commit_sha':h.MERGED,
            'head':{'sha':h.CURRENT,'ref':'dot/math-30006020'},'base':{'ref':'main'},'body':'opaque fixture'}
        pm={'current_PR_opaque_body_pin':h.pin(h.compact(pr['body']).encode())}
        yes(h.validate_pr_metadata(pr,pm) is pr,'production_merged_PR_metadata_validator_positive')
        for key,value in (('state','open'),('draft',True),('merged',False),('merged',1),('merge_commit_sha','c'*40),('merged_at',None)):
            no(lambda key=key,value=value:h.validate_pr_metadata({**pr,key:value},pm),'merged_PR_wrong_'+key+'_'+str(value))
        for key,value in (('sha','e'*40),('ref','other')):
            bad=copy.deepcopy(pr);bad['head'][key]=value
            no(lambda bad=bad:h.validate_pr_metadata(bad,pm),'prepared_HEAD_'+key+'_drift')
        no(lambda:h.validate_pr_metadata({**pr,'body':'changed'},pm),'opaque_PR_body_drift')
        refs={k:{'path':str(case/(k+'.json')),'bytes':2,'sha256':hashlib.sha256(b'{}').hexdigest()} for k in ('math','custody','priority','adoption')}
        native_ref={'path':str(case/'synthetic_native_identity.json'),'bytes':2,'sha256':hashlib.sha256(b'{}').hexdigest()}
        rm={'native_identity_receipt':native_ref}
        ready={'schema':'pr218-root-case-ready-adoption-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':218,'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,
            'existing_publication_adoption_accepted':True,'two_sequential_fresh_whole_package_reviews_accepted':True,
            'original_and_current_claimed_solved_eligibility_preserved':True,'already_merged_original_PR_verified':True,
            'existing_DOI_and_unique_tracker_row_reused':True,'no_new_provider_publication_or_tracker_append':True,
            'existing_scientific_package_frozen':True,'prior_PR217_status_only_skip_accepted':True,
            'native_identity_receipt':native_ref,'current_head':h.CURRENT,'original_merge_commit':h.MERGED,
            'existing_publication_DOI':h.EXISTING_DOI,'existing_tracker_range':h.EXISTING_TRACKER,
            'evidence_references':refs,'numeric_advance_authorized_by_this_file':False}
        h.validate_ready_value(rm,refs,ready);yes(True,'production_future_case_ready_validator_complete_synthetic_value')
        for key in ('mathematical_review_accepted','priority_review_accepted','existing_publication_adoption_accepted','two_sequential_fresh_whole_package_reviews_accepted','prior_PR217_status_only_skip_accepted'):
            bad=copy.deepcopy(ready);bad.pop(key)
            no(lambda bad=bad:h.validate_ready_value(rm,refs,bad),'missing_future_Root_gate_'+key)
        for key,value in (('existing_publication_DOI','10.1/new'),('existing_tracker_range',"'Math Puzzles'!A106:D106"),('numeric_advance_authorized_by_this_file',True),('no_new_provider_publication_or_tracker_append',False)):
            no(lambda key=key,value=value:h.validate_ready_value(rm,refs,{**ready,key:value}),'adoption_reuse_boundary_'+key)
        raw=b'tree '+b'a'*40+b'\nparent '+b'b'*40+b'\nauthor X <x@x> 1 +0000\ncommitter X <x@x> 1 +0000\ngpgsig SIGNATURE\n signed\n \n\nmessage\n'
        rr=write(fixture/'raw_signed_commit.txt',raw)
        cr={'sha':h.native('commit',raw),'tree':'a'*40,'parents':['b'*40],'raw_commit':rr}
        yes(h.authenticated_commit(cr) is cr,'verbatim_signed_commit_final_empty_fold_authenticated')
        for key,value in (('sha','d'*40),('tree','d'*40),('parents',['d'*40])):
            no(lambda key=key,value=value:h.authenticated_commit({**cr,key:value}),'raw_commit_wrong_'+key)
        badref=write(fixture/'raw_signed_commit_missing_fold.txt',raw.replace(b'\n \n\n',b'\n\n'))
        no(lambda:h.authenticated_commit({**cr,'raw_commit':badref}),'signed_final_empty_fold_identity_bearing')
        for component in ('ROOT_COMPLETE218_CANDIDATE_X','ROOT_COMPLETE218_READ_X',
                          'ROOT_COMPLETE218_SYNC_X','ROOT_COMPLETE218_FAST_READ_X',
                          'ROOT_COMPLETE218_SYNC_FAST_X','ROOT_COMPLETE218_FAST_WORK_deadbeef_0',
                          'ROOT_COMPLETE218_READ_ROOT_TERMINAL_X','root_admin218_candidate_legacy'):
            path=h.CASE+'native_completion_preparation_01/'+component+'/00001.RAW_STDOUT.json'
            yes(h.public_path(path) is False,'operational_component_refused_'+component)
        yes(h.public_path(h.CASE+'native_completion_preparation_01/native218_model.py') is True,
            'positive_public_source_still_allowed')
        carrybody={'schema':'pr218-root-prior-operational-carry-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':218,'accepted':True,'prior_terminal_pin':h.PRIOR_TERMINAL_PIN,
            'finite_positive_public_selection_reviewed':True,'files':[{'path':path,**p} for path,p in h.CARRY_REQUIRED.items()],
            'SYNTHETIC_FIXTURE_ONLY':True}
        carryref=write(case/'SYNTHETIC_ROOT_CARRY_ACCEPTANCE.json',enc(carrybody))
        carries=[{'path':path,**p} for path,p in h.carry_inventory(carryref).items()]
        yes(len(h.validate_carryforward(carries,carryref))==5,'exact_required_actual214_and215_to218_positive_carry')
        for changed,label in ((carries[:-1],'missing'),(carries+[carries[0]],'duplicate'),([{**carries[0],'path':h.CASE+'unknown.json'}]+carries[1:],'unknown_path'),([{**carries[0],'sha256':'f'*64}]+carries[1:],'body_drift')):
            no(lambda changed=changed:h.validate_carryforward(changed,carryref),'carry_'+label)
        badcarry={**carrybody,'files':carrybody['files']+[{'path':h.PROGRAM+'audits/pr214_30005244/ROOT_COMPLETE214_READ_X/00001.RAW_STDOUT.json','bytes':1,'sha256':'a'*64}]}
        badcarryref=write(case/'SYNTHETIC_BAD_CARRY.json',enc(badcarry))
        no(lambda:h.carry_inventory(badcarryref),'legacy_raw_journal_carry_refused')
        yes(h.CURRENT_TREE!=h.MERGED_TREE and h.CURRENT_PARENTS!=h.MERGED_PARENTS,'prepared_and_actual_merge_roots_parents_separate')
        for component in ('ROOT_COMPLETE214_READ_X','ROOT_ADMIN212_SYNC_X','ROOT_COMPLETE209_CANDIDATE_X','raw','00001.RAW_STDOUT.json'):
            yes(not h.public_path(h.CASE+'nested/'+component+'/summary.json'),'legacy_or_raw_public_path_refused_'+component)
        ref=write(fixture/'sealed.txt',b'good\n');yes(h.sealed('sealed.txt',{k:ref[k] for k in ('bytes','sha256')})==b'good\n','readonly_source_pin_positive')
        (fixture/'sealed.txt').chmod(0o644);(fixture/'sealed.txt').write_bytes(b'evil\n');(fixture/'sealed.txt').chmod(0o444)
        no(lambda:h.sealed('sealed.txt',{k:ref[k] for k in ('bytes','sha256')}),'source_body_drift_refused')
        (fixture/'link.txt').symlink_to(fixture/'sealed.txt');no(lambda:h.read_regular(fixture/'link.txt'),'nofollow_source_symlink_refused')
        yes(e.api_argv('GET','pulls/218',False)[1:4]==['api','--hostname','github.com'],'explicit_canonical_GitHub_host')
        dispatched=[];guarded=h.GetOnly(lambda *args:dispatched.append(args) or {})
        no(lambda:guarded('POST','git/commits',{}),'GET_firewall_refuses_POST')
        yes(dispatched==[],'refused_route_not_dispatched')
        no(lambda:guarded('GET','pulls/212'),'wrong_case_route_refused')
        lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(lockpath,e.LOCK_BYTES);st=lockpath.stat()
        spec={'path':h.PROGRAM+lockpath.name,'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
        with e.WriterLock(spec) as held:held.check();yes(True,'owned_fixture_original_mechanism_lock_held')
        replacement=program/'replacement.lock';write(replacement,e.LOCK_BYTES);os.replace(replacement,lockpath)
        no(lambda:e.WriterLock(spec).__enter__(),'same_payload_different_inode_refused')
        rt=types.SimpleNamespace(h=h,e=e,m={'retired_candidates':[]},admission={'candidate':oid,'candidate_journal':'fixture1'},
            admission_pin=pin(b'fixture-admission'),seed=types.SimpleNamespace(source_pin=pin(b'fixture-source')))
        q.reserve_candidate_oid(rt);rt.admission['candidate_journal']='fixture2'
        no(lambda:q.reserve_candidate_oid(rt),'canonical_OID_ledger_prevents_renamed_retry')
        consumer_path=fixture/'completion_consumer.py'
        need(pin(consumer_path.read_bytes())=={'bytes': 3463, 'sha256': '6bc6360e78083c5d62db4856999189d280ad06a434eab5b510dfd0f6b5b65ddd'},'Exact new pure consumer')
        consumer=module(consumer_path,'after218_pure_consumer')
        ref={'path':str(case/'SYNTHETIC_REF_NOT_ACTUAL.json'),'bytes':2,'sha256':hashlib.sha256(b'{}').hexdigest()}
        config={k:ref for k in ('manifest','logical_gate','admission','Root_gate','actual_CAS','pointer','sync','source_acceptance')}
        config.update(extension_source=None,extension_acceptance=None)
        rt.admission.update(parent='1'*40,parent_tree='2'*40,tree='3'*40)
        rt.overlay={h.CASE+'fixture_public.txt':b'fixture'}
        rt.m.update(facts=facts,protected_bodies=[],protected_queue={'mode':'100644','type':'blob','sha':'4'*40},
            protected_queue_row_pin=pin(row),evidence_references={'case_ready':ref},native_identity_receipt=ref)
        observation={'actual_MAIN_observed':'5'*40,'actual_MAIN_tree':'6'*40,'CAS_target':oid,'CAS_target_tree':'3'*40,
            'selected_postimage_paths_verified':1,'protected_body_paths_verified':0,'coherent_before_after_ref':True,
            'CAS_or_completion_inferred_from_ancestry':False,'perpetual_or_write_time_Main_equality_claimed':False,
            'native_final_ref_UTC':'2026-10-18T01:00:00Z'}
        proof={'candidate':oid,'tree':'3'*40,'full_scope_verified':True,'all_selected_native_bodies_verified':True,
            'foreign_native_tuples_preserved':True,'changed_leaves':[next(iter(rt.overlay))],'new_directories':[]}
        actual={'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
            'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False}
        args=(rt,config,pin(b'terminal-source'),pin(b'source-manifest'),actual,proof,fixture/'synthetic_proof.json',pin(enc(proof)),
            pin(b'pointer'),pin(b'sync'),[],lists,observation,{},fixture/'synthetic_journal',2)
        record=t.terminal_record(*args);generated=t.enc(record);accepted=consumer.completion_proof(generated,pin(generated))
        yes(accepted['candidate']!=accepted['actual_MAIN_observed'] and accepted['fully_completed_count']==55,'production_record_generated_bytes_real_consumer_C_distinct_R')
        no(lambda:t.terminal_record(*args[:-1],1),'unexecuted_source_refresh_refused')
        for key,value in (('unknown_outcome',True),('actual_Root_MCP_CAS_performed',False),('original_lock_held_across_actual_Root_CAS',False)):
            aa=list(args);aa[4]={**actual,key:value}
            no(lambda aa=aa:t.terminal_record(*aa),'terminal_missing_actual_CAS_'+key)
        for key,value in (('source_gates_verified',False),('actual_original_PR_merged',False),('adopted_existing_publication',False),('fully_completed_count',54.0),('CAS_target','7'*40)):
            raw=t.enc({**record,key:value})
            no(lambda raw=raw:consumer.completion_proof(raw,pin(raw)),'real_consumer_wrong_'+key)
        published=case/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json';guards=[]
        result=t.exclusive_root_receipt(e,published,b'owned fixture only\n',lambda:guards.append('mutable'),lambda:guards.append('identity'))
        yes(result['exclusive_atomic_publication'] and guards==['mutable','identity','identity'],'repaired_V2_publisher_guard_order')
        no(lambda:t.exclusive_root_receipt(e,published,b'new\n',lambda:None,lambda:None),'existing_terminal_never_overwritten')
        published.unlink()
        class FailingOps:
            def __init__(self):self.linked=False
            def fsync(self,fd):
                if self.linked:raise OSError('synthetic after-link durability uncertainty')
                return os.fsync(fd)
            def link(self,*a,**kw):os.link(*a,**kw);self.linked=True
            def unlink(self,*a,**kw):return os.unlink(*a,**kw)
        try:t.exclusive_root_receipt(e,published,b'uncertain owned fixture\n',lambda:None,lambda:None,local_ops=FailingOps())
        except t.TerminalPublicationUncertain as error:
            yes(error.details['automatic_retry_overwrite_or_unlink_final_forbidden'] is True and published.exists(),'postpublication_uncertainty_preserves_final_without_success')
        else:raise RuntimeError('Uncertain final publication accepted')
        generated_pin=pin(generated)
    return {'schema':'pr218-inactive-source-offline-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'OWNED_SYNTHETIC_SOURCE_CONTROLS_ONLY','checks':len(RESULTS),'all_passed':True,'controls':RESULTS,
        'generated_production_terminal_record_pin':generated_pin,'generated_record_scope':'SYNTHETIC_INPUTS_ONLY_NOT_A_ROOT_RECEIPT',
        'real_consumer_source_pin':{'bytes': 3463, 'sha256': '6bc6360e78083c5d62db4856999189d280ad06a434eab5b510dfd0f6b5b65ddd'},
        'network_Git_original_lock_current_five_provider_ref_PR_effects':False,
        'actual_packets_gates_admissions_candidates_or_terminal_receipts_created':False,
        'limitations':['No live readiness/native identity gate or exact logical packet tested.',
        'No real network, immutable POST, Root CAS, original lock, five sync or actual terminal executed.',
        'Inherited full-scope/concurrent mechanisms are compared by exact byte/AST provenance; old control counts are not claimed rerun.',
        'Real production record constructor and frozen consumer use explicit synthetic prerequisites; this establishes format integration only.']}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))

