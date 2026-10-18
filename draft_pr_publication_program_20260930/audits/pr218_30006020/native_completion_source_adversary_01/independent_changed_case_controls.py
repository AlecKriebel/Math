"""Bounded owned PR218 changed-case controls. No network or live effect entrypoint."""
import base64, copy, datetime, hashlib, json, os, pathlib, sys, tempfile, types
HERE=pathlib.Path(__file__).absolute().parent
SOURCE=HERE.parent/'native_completion_preparation_01'
RESULTS=[]
def need(x,msg):
    if type(x) is not bool or not x:raise RuntimeError(msg)
def yes(x,name):
    need(x,name);RESULTS.append({'name':name,'kind':'positive','passed':True})
def no(fn,name):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,FileExistsError,OSError,AttributeError):
        RESULTS.append({'name':name,'kind':'expected_refusal','passed':True});return
    raise RuntimeError('Expected refusal: '+name)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:need(f.write(b)==len(b),'Complete owned write')
    p.chmod(0o444);return {'path':str(p),**pin(b)}
def module(p,n):
    m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def deny_effects(event,args):
    if event in ('subprocess.Popen','os.system','os.exec','socket.connect','socket.connect_ex','socket.bind'):
        raise RuntimeError('No network or subprocess permitted in controls: '+event)
def main():
    sys.addaudithook(deny_effects)
    expected=json.loads((HERE/'REVIEWED_SOURCE_BINDINGS.json').read_text())
    raw=(SOURCE/'SOURCE_MANIFEST.json').read_bytes();yes(pin(raw)==expected['manifest_pin'],'frozen_manifest_matches_reviewed_pin')
    sm=json.loads(raw)
    with tempfile.TemporaryDirectory(prefix='_synthetic_controls_',dir=HERE) as temporary:
        checkout=pathlib.Path(temporary)/'checkout';case=checkout/'draft_pr_publication_program_20260930/audits/pr218_30006020'
        B=case/'native_completion_preparation_01';B.mkdir(parents=True)
        for row in sm['files']:
            body=(SOURCE/row['path']).read_bytes();yes(pin(body)=={k:row[k] for k in ('bytes','sha256')},'frozen_payload_'+row['path']);write(B/row['path'],body)
        write(B/'SOURCE_MANIFEST.json',raw)
        h=module(B/'native218_model.py','owned_control_model');t=module(B/'ROOT_TERMINAL_INSPECTION.py','owned_control_terminal')
        q=module(B/'completion_checkpoint.py','owned_control_driver');e=module(B/'native218_primitives.py','owned_control_primitives')
        yes(h.CHECKOUT==q.CHECKOUT==t.CHECKOUT==e.CHECKOUT==checkout,'all_sources_bound_only_owned_checkout')
        yes(t.source_closure()==(pin((B/'ROOT_TERMINAL_INSPECTION.py').read_bytes()),pin(raw)),'real_terminal_source_closure')
        yes(h.exact(h.phase_facts(),t.FIXED_FACTS),'model_terminal_fixed_facts_identical')
        baseline=h.source_baseline();facts=h.phase_facts();progress={**facts,'conditional_proposal_only':True,**h.completion_memberships(),'dated_eligible_total':99};casepost={**facts,'conditional_proposal_only':True}
        yes(len(baseline['fully_completed_eligible_PRs'])==54 and len(baseline['published_PRs'])==38,'baseline_exact54_38')
        yes(all(n not in arr for arr in baseline.values() for n in (212,213,215,216,217,218)),'status_skips_never_memberships')
        yes(facts['fully_completed_count']==55 and facts['published_count']==39 and facts['next_numeric_intake_cursor']==219 and facts['advance_to_next_PR_authorized_now'] is False,'conditional55_39_cursor219_advancefalse')
        yes(h.CURRENT_TREE!='fb365e1f22c7d4487980d49af574ec3679ce6b96' and h.MERGED_TREE=='fb365e1f22c7d4487980d49af574ec3679ce6b96','prepared_and_merge_roots_distinct')
        yes(h.CURRENT_PARENTS==[h.ORIGINAL,'2f6aa7a8a4c2456c335be24d64ba9c071d599944'] and h.MERGED_PARENTS==['3fe2f64accb5a057e6eddb64bac73eb573be6eab',h.CURRENT],'exact_distinct_ordered_parents')
        lists=t.accounting(h,{'facts':facts},casepost,progress,baseline);yes(lists['new_memberships']==h.completion_memberships(),'production_accounting_adds_only218')
        for key in baseline:
            for bad,label in ((baseline[key],'missing218'),(baseline[key]+[214,218],'duplicate214'),(baseline[key]+[215,218],'adds_skip215'),(baseline[key]+[217,218],'adds_skip217')):
                no(lambda key=key,bad=bad:t.accounting(h,{'facts':facts},casepost,{**progress,key:bad},baseline),key+'_'+label)
        no(lambda:t.accounting(h,{'facts':facts},casepost,{**progress,'fully_completed_count':55.0},baseline),'float_count_refused')
        no(lambda:t.accounting(h,{'facts':facts},{**casepost,'conditional_proposal_only':False},progress,baseline),'false_actual_authority_in_five_refused')
        mark=h.phase_marker();h.markdown_current(b'old214\n<!-- PR214_NATIVE_PHASE_FACTS historical -->\n'+mark+b'\n','completion100',True);yes(True,'new218_last_marker_preserves_historical214')
        for value,label in ((mark+b'\n'+mark+b'\n','duplicate'),(mark+b'\ntrailing','not_last'),(mark.replace(b'FACTS ',b'FACTS\t')+b'\n','malformed')):
            no(lambda value=value:h.markdown_current(value,'completion100',True),'marker_'+label)
        for component in ('ROOT_COMPLETE218_CANDIDATE_X','ROOT_COMPLETE218_READ_ROOT_TERMINAL_X','ROOT_COMPLETE218_FAST_WORK_X','root_admin218_old','ROOT_COMPLETE214_READ_X','root_admin214_old','ROOT_COMPLETE212_SYNC_X','root_admin212_old','_private_origins','private_provider_responses','packet_working','journal_raw','runtime_source','_runtime','sandbox_fixture','_synthetic_fixture','extracted','objects','inputs'):
            yes(h.public_path(h.CASE+'nested/'+component+'/response.json') is False,'public_refuses_'+component)
        yes(h.public_path(h.CASE+'native_completion_preparation_01/native218_model.py') is True,'public_positive_source')
        for name in ('00001.RAW_STDOUT.json','00001.raw_stderr.txt','00001.API_RECEIPT.json','raw_response.json','_raw_provider.json'):
            yes(h.public_path(h.CASE+'apparently_public/'+name) is False,'raw_origin_filename_refused_'+name)
        for path in (h.ATTEMPT+'/proof.tex',h.SHARED+'/metadata.json',h.QUEUE,h.VIEWS[0]):yes(h.public_path(path) is False,'public_refuses_protected_'+path)
        own=b'30006020 / OWR-14298589-005';row=b'|218|'+own+b'|a|b|c|d|e|claimed_solved|1/5|f|g|h|\n'
        yes(h.own_queue_row(row)[0]==row,'canonical_current1_5_row')
        for alternative,label in ((b' '+row,'indented'),(row[1:],'no_outer_pipe'),(row.replace(own,b'30006020'),'bare_id'),(row.replace(own,b'`'+own+b'`'),'backtick_id')):
            no(lambda alternative=alternative:h.own_queue_row(row+alternative),'own_duplicate_'+label)
        yes(h.own_queue_row(b'| foreign|new|\n'+row)[0]==row,'foreign_rows_preserve_unique_exact_own')
        pr={'number':218,'title':'30006020: audited intermediate-area cylinder theorem and published preprint','state':'closed','draft':False,'merged':True,'merged_at':'2026-10-15T07:35:42Z','merge_commit_sha':h.MERGED,'head':{'sha':h.CURRENT,'ref':'dot/math-30006020'},'base':{'ref':'main'},'body':'owned opaque fixture'}
        pm={'current_PR_opaque_body_pin':pin(h.compact(pr['body']).encode())};h.validate_pr_metadata(pr,pm);yes(True,'actual218_metadata_positive')
        for key,value in (('number',218.0),('merged',1),('merged',False),('state','open'),('merge_commit_sha','4abf30daa991860a275b3d25745159852757ad35'),('body','changed')):
            no(lambda key=key,value=value:h.validate_pr_metadata({**pr,key:value},pm),'metadata_refuses_'+key+'_'+str(value))
        refs={k:{'path':str(case/(k+'.json')),'bytes':2,'sha256':hashlib.sha256(b'{}').hexdigest()} for k in ('math','custody','priority','adoption')};nr=refs['custody']
        ready={'schema':'pr218-root-case-ready-adoption-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':218,'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,'existing_publication_adoption_accepted':True,'two_sequential_fresh_whole_package_reviews_accepted':True,'original_and_current_claimed_solved_eligibility_preserved':True,'already_merged_original_PR_verified':True,'existing_DOI_and_unique_tracker_row_reused':True,'no_new_provider_publication_or_tracker_append':True,'existing_scientific_package_frozen':True,'prior_PR217_status_only_skip_accepted':True,'native_identity_receipt':nr,'current_head':h.CURRENT,'original_merge_commit':h.MERGED,'existing_publication_DOI':h.EXISTING_DOI,'existing_tracker_range':h.EXISTING_TRACKER,'evidence_references':refs,'numeric_advance_authorized_by_this_file':False}
        h.validate_ready_value({'native_identity_receipt':nr},refs,ready);yes(True,'complete_typed_future_readiness_positive')
        for key in ('mathematical_review_accepted','two_sequential_fresh_whole_package_reviews_accepted','prior_PR217_status_only_skip_accepted'):
            bad=dict(ready);bad.pop(key);no(lambda bad=bad:h.validate_ready_value({'native_identity_receipt':nr},refs,bad),'missing_readiness_'+key)
        for key,value in (('numeric_advance_authorized_by_this_file',True),('existing_tracker_range',"'Math Puzzles'!A105:D105"),('existing_publication_DOI','10.5281/zenodo.23390551')):
            no(lambda key=key,value=value:h.validate_ready_value({'native_identity_receipt':nr},refs,{**ready,key:value}),'readiness_identity_'+key)
        cm={k:{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-18T01:00:00Z'} for k in ('commit_author','commit_committer')};cm['commit_message']=h.COMMIT_MESSAGE
        request,oid=h.commit_request(cm,'a'*40,['b'*40]);yes(request['parents']==['b'*40] and h.hexid(oid),'one_fresh_parent_neutral_archive')
        for parents in ([h.ORIGINAL],[h.CURRENT],[h.MERGED],['a'*40,'b'*40]):no(lambda parents=parents:h.commit_request(cm,'a'*40,parents),'snapshot_parent_'+str(parents))
        no(lambda:h.commit_request({**cm,'commit_message':'Closes #218\n'},'a'*40,['b'*40]),'auto_close_message_refused')
        rawcommit=b'tree '+b'a'*40+b'\nparent '+b'b'*40+b'\nauthor X <x@x> 1 +0000\ncommitter X <x@x> 1 +0000\ngpgsig SIGNED\n folded\n \n\nmessage\n';rr=write(B/'signed.txt',rawcommit)
        cr={'sha':h.native('commit',rawcommit),'tree':'a'*40,'parents':['b'*40],'raw_commit':rr};yes(h.authenticated_commit(cr)==cr,'signed_raw_empty_fold_preserved')
        no(lambda:h.authenticated_commit({**cr,'parents':['c'*40]}),'raw_ordered_parent_mismatch')
        dispatch=[];go=h.GetOnly(lambda *args:dispatch.append(args) or {})
        no(lambda:go('GET','pulls/214'),'wrong_prior_PR_route_refused');no(lambda:go('POST','git/commits',{}),'GET_firewall_POST_refused');yes(dispatch==[],'refused_routes_not_dispatched')
        yes(e.api_argv('GET','pulls/218',False)[1:4]==['api','--hostname','github.com'],'canonical_github_hostname')
        carryrows=[{'path':p,**v} for p,v in h.CARRY_REQUIRED.items()]
        carrying={'schema':'pr218-root-prior-operational-carry-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':218,'accepted':True,'prior_terminal_pin':h.PRIOR_TERMINAL_PIN,'finite_positive_public_selection_reviewed':True,'files':carryrows}
        cref=write(case/'CARRY_SYNTHETIC.json',enc(carrying));yes(len(h.validate_carryforward(carryrows,cref))==5,'minimum_exact214_terminal_and215_218_intakes')
        for altered,label in ((carryrows[:-1],'missing218_intake'),(carryrows+[carryrows[0]],'duplicate'),([{**carryrows[0],'sha256':'f'*64}]+carryrows[1:],'pin_drift')):
            no(lambda altered=altered:h.validate_carryforward(altered,cref),'carry_'+label)
        for p in (h.OLD_CASE+'native_completion_preparation_02/ROOT_COMPLETE214_READ_X/raw.json',h.CASE+'unknown.json',h.OLD_CASE+'private_provider/raw.json'):
            bad={**carrying,'files':carryrows+[{'path':p,**pin(b'bad')}]};br=write(case/('badcarry'+str(len(RESULTS))+'.json'),enc(bad));no(lambda br=br:h.carry_inventory(br),'unsafe_carry_'+p)
        rt=types.SimpleNamespace(h=h,e=e,m={'retired_candidates':[]},admission={'candidate':oid,'candidate_journal':'one'},admission_pin=pin(b'admission'),seed=types.SimpleNamespace(source_pin=pin(b'source')))
        q.reserve_candidate_oid(rt);rt.admission['candidate_journal']='renamed';no(lambda:q.reserve_candidate_oid(rt),'one_use_oid_not_just_journal')
        lockpath=checkout/(h.PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock');write(lockpath,e.LOCK_BYTES);st=lockpath.stat();spec={'path':h.PROGRAM+lockpath.name,'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
        yes(len(e.LOCK_BYTES)==153,'original_lock_payload153')
        with e.WriterLock(spec) as held:held.check();yes(True,'only_owned_fixture_lock_acquired')
        replacement=write(lockpath.with_name('replacement.lock'),e.LOCK_BYTES);os.replace(replacement['path'],lockpath);no(lambda:e.WriterLock(spec).__enter__(),'same_lock_bytes_changed_inode_refused')
        final=case/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json';guards=[]
        published=t.exclusive_root_receipt(e,final,b'OWNED PUBLICATION CONTROL ONLY\n',lambda:guards.append('mutable'),lambda:guards.append('identity'))
        yes(published['exclusive_atomic_publication'] is True and guards==['mutable','identity','identity'] and final.read_bytes()==b'OWNED PUBLICATION CONTROL ONLY\n','real_publisher_success_exclusive_guard_order')
        no(lambda:t.exclusive_root_receipt(e,final,b'replacement\n',lambda:None,lambda:None),'fixed_terminal_never_overwritten');final.unlink()
        def stop():raise RuntimeError('Owned final mutable guard refusal')
        no(lambda:t.exclusive_root_receipt(e,final,b'unpublished\n',stop,lambda:None),'publisher_prelink_mutable_guard_failure')
        yes(not final.exists(),'failed_mutable_guard_has_no_final')
        class FailingOps:
            def __init__(self,stage):self.stage=stage;self.linked=False
            def fsync(self,fd):
                if self.linked and self.stage=='afterlink_fsync':raise OSError('Owned postlink durability failure')
                return os.fsync(fd)
            def link(self,*a,**kw):
                if self.stage=='link_error':raise OSError('Owned link error before success')
                os.link(*a,**kw);self.linked=True
            def unlink(self,*a,**kw):return os.unlink(*a,**kw)
        for stage,want_final in (('link_error',False),('afterlink_fsync',True)):
            try:t.exclusive_root_receipt(e,final,b'uncertain owned publication\n',lambda:None,lambda:None,local_ops=FailingOps(stage))
            except t.TerminalPublicationUncertain as error:
                yes(error.details['automatic_retry_overwrite_or_unlink_final_forbidden'] is True and final.exists() is want_final,'publisher_uncertainty_'+stage)
            else:raise RuntimeError('Publisher uncertainty accepted '+stage)
            if final.exists():final.unlink()
        def identity_stop():raise RuntimeError('Owned postlink source identity refusal')
        try:t.exclusive_root_receipt(e,final,b'identity uncertain owned publication\n',lambda:None,identity_stop)
        except t.TerminalPublicationUncertain as error:
            yes(final.exists() and error.details['automatic_retry_overwrite_or_unlink_final_forbidden'] is True,'publisher_postlink_identity_failure_preserves_final')
        else:raise RuntimeError('Postlink identity failure accepted')
    yes(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==expected['manifest_pin'],'original_frozen_manifest_unchanged')
    return {'schema':'pr218-independent-changed-case-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'OWNED_SYNTHETIC_COMPONENTS_ONLY','checks':len(RESULTS),'positive':sum(r['kind']=='positive' for r in RESULTS),'expected_refusal':sum(r['kind']=='expected_refusal' for r in RESULTS),'all_passed':True,'controls':RESULTS,'full_inspect_roundtrip_here':False,'network_original_lock_global_five_Git_native_ref_PR_provider_tracker_effects':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
