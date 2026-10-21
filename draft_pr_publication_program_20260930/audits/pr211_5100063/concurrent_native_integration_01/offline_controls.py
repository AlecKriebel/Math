"""Bounded local cache/pure native/synthetic-effect controls; no live API/lock.

Production source is compiled unchanged into a separate owned fixture ancestry.
Its public functions receive ordinary synthetic contexts/observers. Actual CLI
Seed/Runtime authorization is not bypassed or represented as accepted by tests.
"""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,subprocess,sys,tempfile,types

BASE=Path(__file__).absolute().parent


def module(path,raw):
    result=types.ModuleType(path.stem);result.__file__=str(path)
    exec(compile(raw,str(path),'exec'),result.__dict__);return result


def run():
    checks=[]
    def yes(ok,name):
        if not ok:raise RuntimeError(name)
        checks.append(name)
    def no(call,name):
        try:call()
        except (RuntimeError,ValueError,TypeError,KeyError,OSError):checks.append(name)
        else:raise RuntimeError('Expected refusal: '+name)
    raw=(BASE/'concurrent_checkpoint.py').read_bytes()
    q=module(BASE/'concurrent_checkpoint.py',raw);seed=q.Seed();h,c=seed.h,seed.c
    yes(len(seed.overlay)==192 and len(seed.bodies)==202 and sum(map(len,seed.bodies.values()))==2756787,
        'all_actual_Root202_GET_cache_objects_reparsed_locally_no_network')
    manifest=h.decode((q.CACHE/'BODY_CACHE_MANIFEST.json').read_bytes());obj=manifest['objects'][0]
    response=(q.CACHE/obj['raw_response']['path']).read_bytes();receipt=(q.CACHE/obj['receipt']['path']).read_bytes()
    yes(q.validate_object(h,obj,response,receipt,b'')==seed.bodies[obj['oid']],'actual_GET_raw_receipt_native_body_positive')
    no(lambda:q.validate_object(h,obj,response+b' ',receipt,b''),'raw_envelope_pin_corruption_refused')
    no(lambda:q.validate_object(h,obj,response,receipt+b' ',b''),'receipt_pin_corruption_refused')
    no(lambda:q.validate_object(h,obj,response,receipt,b'bad'),'stderr_corruption_refused')
    def changed_receipt(changes):
        bad=h.decode(receipt);bad.update(changes);changed=q.enc(bad);row=copy.deepcopy(obj);row['receipt'].update(q.pin(changed))
        return q.validate_object(h,row,response,changed,b'')
    for changes,label in [({'method':'POST'},'method'),({'path':'git/ref/heads/main'},'mutable_route'),
                          ({'exit':False},'bool_exit'),({'exit':1},'failed_exit'),({'no_retry':False},'retry')]:
        no(lambda changes=changes:changed_receipt(changes),'cache_'+label+'_refused')
    def changed_body(changes):
        bad=h.decode(response);bad.update(changes);changed=q.enc(bad);row=copy.deepcopy(obj);row['raw_response'].update(q.pin(changed))
        rec=h.decode(receipt);rec['stdout']=row['raw_response'];recraw=q.enc(rec);row['receipt'].update(q.pin(recraw))
        return q.validate_object(h,row,changed,recraw,b'')
    for changes,label in [({'sha':'0'*40},'oid'),({'size':float(obj['body_pin']['bytes'])},'floating_size'),
                          ({'encoding':'utf8'},'encoding'),({'content':'invalid!'},'base64')]:
        no(lambda changes=changes:changed_body(changes),'cache_native_'+label+'_refused')
    tree=ast.parse(raw)
    immutable=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_immutable')
    parent=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='parent_state')
    yes('git/ref/heads/main' not in ast.unparse(immutable)+ast.unparse(parent),'immutable_verifier_and_parent_auth_never_read_or_spoof_mutable_Main')
    cand=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate')
    posts=[n for n in ast.walk(cand) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
           and n.func.id=='api' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='POST']
    yes(len(posts)==2 and [n.args[1].value for n in posts]==['git/trees','git/commits'],'exact_two_immutable_POST_sites_no_blob_or_ref_writer')
    yes('reserve_candidate_oid(rt)' in ast.unparse(cand),'canonical_candidate_reservation_precedes_POSTs')
    def pipe_case(payload,expected=None,timeout=.02,blocking=True,close=True):
        r,w=os.pipe();os.set_blocking(r,blocking);calls=[]
        try:
            if payload:os.write(w,payload)
            if close:os.close(w);w=None
            def check():calls.append(True)
            if expected is None:no(lambda:q.wait_actual_CAS_reference(r,check,timeout),'CAS_ack_pipe_refusal_'+str(len(checks)))
            else:yes(q.wait_actual_CAS_reference(r,check,timeout)==expected,'CAS_ack_pipe_positive_'+str(len(checks)))
            yes(os.get_blocking(r)==blocking and len(calls)>0,'CAS_ack_descriptor_flag_restored_and_guard_checked_'+str(len(checks)))
        finally:
            os.close(r)
            if w is not None:os.close(w)
    pipe_case(b'{}\n',b'{}')
    pipe_case(b'{}\n',b'{}',blocking=False)
    pipe_case(b'{}'+b' '*4093+b'\n',b'{}'+b' '*4093)
    pipe_case(b'{}'+b' '*4093+b'\nX')
    pipe_case(b'{}\nX')
    pipe_case(b'{}\n{}\n')
    pipe_case(b'{}')
    pipe_case(b'')
    pipe_case(b'',close=False)
    pipe_case(b'X'*4097)
    with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as tmp:
        root=Path(tmp)/'checkout';program=root/'draft_pr_publication_program_20260930'
        case=program/'audits/pr211_5100063';native=case/'native_adoption_preparation_01';native.mkdir(parents=True)
        virtual=case/'concurrent_native_integration_01/concurrent_checkpoint.py'
        virtual.parent.mkdir();v=module(virtual,raw)
        eraw=(q.NATIVE/'native211_future_executor.py').read_bytes()
        epath=native/'native211_future_executor.py';epath.write_bytes(eraw);epath.chmod(0o444)
        e=module(epath,eraw)
        def write(path,body):
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():path.chmod(0o644)
            path.write_bytes(body);path.chmod(0o444)
        objects={};blobs={};requests=[];overrides={};refvalue=['a'*40]
        def blob(body):
            oid=h.native('blob',body);blobs[oid]=body;return oid
        def tree(rows):
            rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
            oid=c.tree_hash(rows)
            objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':m,'type':t,'sha':o} for n,m,t,o in rows]}
            return oid
        plan=h.decode((q.NATIVE/'ROOT_PLAN_ADOPTION100_STDOUT_06.json').read_bytes())
        added=set(plan['new_directories'])
        yes(len(added)==25,'fixed_earlier_plan25_directory_names_used_only_for_synthetic_fixture_shape')
        existing=set()
        for path in seed.overlay:
            parts=path.split('/')
            for i in range(1,len(parts)):
                prefix='/'.join(parts[:i])
                if prefix not in added:existing.add(prefix)
        def root_tree(leaves):
            trie={}
            for path in sorted(existing,key=lambda p:p.count('/')):
                node=trie
                for part in path.split('/'):node=node.setdefault(part,{})
            for path,value in leaves.items():
                node=trie
                for part in path.split('/')[:-1]:node=node.setdefault(part,{})
                node[path.split('/')[-1]]=value
            def descend(node):
                return tree([(n,'040000','tree',descend(value)) if type(value) is dict else (n,*value) for n,value in node.items()])
            return descend(trie)
        native_maps=h.decode((q.CASE/'native_custody_01/FINAL_NATIVE_TREES_SUPPLEMENT.json').read_bytes())
        for oid in (h.SHARED_TREE,'6103bc250915076cca7cfde6607f89e173294723'):
            entries=native_maps[oid]
            yes(tree([(n,r['mode'],r['type'],r['sha']) for n,r in entries.items()])==oid,'canonical_protected_fixture_tree_'+oid)
        baseline=h.decode(h.sealed('BASELINE_MEMBERSHIP.json',h.BASELINE_PIN))
        baseline_body=q.enc({**h.baseline_facts(),**baseline})
        local_bodies={r['path']:h.sealed(r['source'],r['preimage']) if r['preimage'] else None for r in seed.logical['local_views']}
        native_bodies={h.VIEWS[2]:baseline_body,h.VIEWS[3]:b'prior static fixture\n',h.VIEWS[4]:local_bodies[h.VIEWS[4]]}
        queue=h.tuple_pin(seed.logical['protected_queue'])
        leaves={path:('100644','blob',blob(body)) for path,body in native_bodies.items()}
        leaves.update({h.ATTEMPT[:-1]:('040000','tree',h.ATTEMPT_TREE),h.SHARED:('040000','tree',h.SHARED_TREE),h.QUEUE:queue,
            'foreign/empty':('040000','tree',tree([])),'foreign/executable':('100755','blob',blob(b'exec\n')),
            'foreign/symlink':('120000','blob',blob(b'target')),'foreign/gitlink':('160000','commit','9'*40)})
        parent_tree=root_tree(leaves)
        overlay=seed.overlay;pre={path:leaves.get(path) for path in overlay}
        fake_seed=types.SimpleNamespace(h=h,e=e,c=c,s=seed.s,source_pin=seed.source_pin,source_manifest_pin=seed.source_manifest_pin,
            logical=seed.logical,overlay=overlay,pre=pre,reused=seed.reused,bodies=seed.bodies)
        m={**seed.logical,'expected_parent':'a'*40,'expected_parent_tree':parent_tree}
        a={'schema':'pr211-concurrent-parent-admission-v1','PR':211,
            'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
            'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':q.MP,'logical_gate_pin':q.GP,
            'cache_manifest_pin':q.CM,'cache_acceptance_pin':q.CA,'facts':m['facts'],
            'parent':'a'*40,'parent_tree':parent_tree,'parents':['a'*40],'created_UTC':'2026-10-17T20:30:00Z',
            'commit_author':{**m['commit_author'],'date':'2026-10-17T20:30:00Z'},
            'commit_committer':{**m['commit_committer'],'date':'2026-10-17T20:30:00Z'},
            'commit_message':m['commit_message'],'candidate_journal':'ROOT_CONCURRENT_CANDIDATE_FIXTURE',
            'tree':'0'*40,'candidate':'0'*40}
        wanted,changed,dirs=h.expected(c,c.NativeTrees(lambda method,path:copy.deepcopy(objects[path.rsplit('/',1)[1]])),parent_tree,overlay,pre)
        yes(changed==set(overlay) and len(dirs)==25,'synthetic_scope_exact192_25')
        a['tree']=wanted;m.update(commit_author=a['commit_author'],commit_committer=a['commit_committer'])
        request,a['candidate']=h.commit_request(m,wanted,[a['parent']])
        v.checked_admission(fake_seed,a);yes(True,'typed_admission_single_parent_dates_fixed_logical_positive')
        for key,value,label in [('facts',{**a['facts'],'published_count':37.0},'floating_fact'),('commit_message',a['commit_message']+'x','message'),
                                ('parents',['b'*40],'parent_list'),('candidate',next(iter(q.RETIRED)),'retired')]:
            bad=copy.deepcopy(a);bad[key]=value
            no(lambda bad=bad:v.checked_admission(fake_seed,bad),'admission_'+label+'_refused')
        bad=copy.deepcopy(a);bad['commit_author']['email']='substitute@example.invalid'
        no(lambda:v.checked_admission(fake_seed,bad),'admission_identity_substitution_refused')
        after={**leaves,**{path:('100644','blob',blob(body)) for path,body in overlay.items()}}
        yes(root_tree(after)==wanted,'independent_full_candidate_tree_matches_expected')
        commits={
            h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':'a3bdcb55173cb41866a58aded968b68d6a14d1a4'}]},
            h.PREPARED:{'sha':h.PREPARED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.ORIGINAL},{'sha':h.PREPARED_SECOND_PARENT}]},
            h.MERGED:{'sha':h.MERGED,'tree':{'sha':h.MERGED_TREE},'parents':[{'sha':h.MERGE_FIRST_PARENT},{'sha':h.PREPARED}]},
            a['parent']:{'sha':a['parent'],'tree':{'sha':parent_tree},'parents':[{'sha':h.ANCHOR}]},
            a['candidate']:{'sha':a['candidate'],'tree':{'sha':wanted},'parents':[{'sha':a['parent']}],
                            'author':request['author'],'committer':request['committer'],'message':request['message']}}
        pr={'number':211,'head':{'sha':h.PREPARED},'base':{'ref':'main'},'state':'closed','draft':False,'merged':True,
            'merge_commit_sha':h.MERGED,'merged_at':h.MERGED_AT}
        def observer(method,path,body=None):
            need= q.need;need(method=='GET' and body is None,'Synthetic GET only')
            requests.append(path)
            if path in overrides:return copy.deepcopy(overrides[path])
            if path=='git/ref/heads/main':return {'object':{'sha':refvalue[0]}}
            if path=='pulls/211':return copy.deepcopy(pr)
            if path.startswith('compare/'):return {'status':'ahead','merge_base_commit':{'sha':path.split('/')[1].split('...')[0]}}
            oid=path.rsplit('/',1)[1]
            if path.startswith('git/commits/'):return copy.deepcopy(commits[oid])
            if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
            if path.startswith('git/blobs/'):
                body=blobs[oid];return {'sha':oid,'size':len(body),'encoding':'base64','content':base64.b64encode(body).decode()}
            raise RuntimeError('Unknown fixture route')
        rt=types.SimpleNamespace(seed=fake_seed,h=h,e=e,c=c,m=m,admission=a,admission_pin={'bytes':1,'sha256':'1'*64},
            gate_pin={'bytes':1,'sha256':'2'*64},overlay=overlay,pre=pre,reused=seed.reused,bodies=seed.bodies)
        rt.refresh=lambda:rt
        refvalue[0]='f'*40;requests.clear()
        proof=v.verify_immutable(rt,observer)
        yes(proof['full_scope_verified'] and len(proof['selected_files'])==192 and len(proof['protected_existing_bodies'])==10,
            'full_unmodified_immutable_verifier_actual202_cache_native192_scope')
        yes('git/ref/heads/main' not in requests,'moving_Main_not_observed_or_spoofed_by_immutable_verifier')
        yes(not any(x.startswith('git/blobs/') and x.rsplit('/',1)[1] in seed.bodies for x in requests),
            '202_actual_GET_bodies_reused_explicitly_without_refetch_or_synthetic_GET')
        commits[a['candidate']]['message']=request['message'][:-1]
        yes(v.verify_immutable(rt,observer)['commit_message_readback']['terminal_LFs_omitted']==1,'canonical_message_oneLF_representation')
        commits[a['candidate']]['message']=request['message']+'\n'
        no(lambda:v.verify_immutable(rt,observer),'canonical_message_extraLF_refused')
        commits[a['candidate']]['message']=request['message']
        for key,value,label in [('tree',{'sha':'0'*40},'tree'),('parents',[{'sha':'0'*40}],'parent'),
                                ('author',{**request['author'],'email':'changed@example.invalid'},'author')]:
            old=commits[a['candidate']][key];commits[a['candidate']][key]=value
            no(lambda:v.verify_immutable(rt,observer),'candidate_'+label+'_refused');commits[a['candidate']][key]=old
        descendant='b'*40;descroot=root_tree({**after,'foreign/new_file':('100644','blob',blob(b'foreign independent work'))})
        commits[descendant]={'sha':descendant,'tree':{'sha':descroot},'parents':[{'sha':a['candidate']}]}
        refvalue[0]=descendant
        observed=v.main_closure(rt,observer)
        yes(observed['actual_MAIN_observed']==descendant and observed['CAS_target']==a['candidate']
            and observed['actual_MAIN_tree']!=observed['CAS_target_tree'],'foreign_descendant_accepted_distinct_C_R_roots')
        yes(observed['CAS_or_completion_inferred_from_ancestry'] is False and observed['perpetual_or_write_time_Main_equality_claimed'] is False,
            'descendant_never_infers_CAS_or_perpetual_Main')
        compare='compare/'+a['candidate']+'...'+descendant;overrides[compare]={'status':'diverged','merge_base_commit':{'sha':'0'*40}}
        no(lambda:v.main_closure(rt,observer),'sibling_or_unverified_ancestry_refused');overrides.clear()
        badroot=root_tree({**after,next(iter(overlay)):('100644','blob',blob(b'tampered owned'))})
        commits[descendant]['tree']['sha']=badroot
        no(lambda:v.main_closure(rt,observer),'descendant_changed_owned_postimage_refused')
        commits[descendant]['tree']['sha']=root_tree({**after,h.QUEUE:('100644','blob',blob(b'changedQUEUE'))})
        no(lambda:v.main_closure(rt,observer),'descendant_whole_QUEUE_change_refused')
        commits[descendant]['tree']['sha']=descroot
        refs=[0]
        def changing(method,path,body=None):
            value=observer(method,path,body)
            if path=='git/ref/heads/main':
                refs[0]+=1
                if refs[0]==2:value={'object':{'sha':'c'*40}}
            return value
        no(lambda:v.main_closure(rt,changing),'Main_move_across_bound_R_root_observation_refused')
        for row in m['local_views']:write(root/row['path'],local_bodies[row['path']])
        v.local_states(rt);yes(True,'fixture_separate_local5_exact_preimages')
        write(root/m['local_views'][0]['path'],b'third state')
        no(lambda:v.local_states(rt,resume=True),'fixture_third_local_state_refused')
        write(root/m['local_views'][0]['path'],overlay[m['local_views'][0]['path']])
        v.local_states(rt,resume=True);yes(True,'fixture_mixed_exact_pre_post_resume_positive')
        write(root/m['local_views'][0]['path'],local_bodies[m['local_views'][0]['path']])
        lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(lockpath,e.LOCK_BYTES);st=lockpath.stat()
        m['writer_lock']={**m['writer_lock'],'device':st.st_dev,'inode':st.st_ino}
        with e.WriterLock(m['writer_lock']) as lock:
            refvalue[0]=a['parent'];v.lease_guard(rt,observer,lock);yes(True,'fixture_original_inode_lock_fresh_parent_preflight')
            refvalue[0]=descendant;no(lambda:v.lease_guard(rt,observer,lock),'stale_preCAS_parent_refused_even_valid_future_descendant')
        refvalue[0]=a['parent']
        v.reserve_candidate_oid(rt);yes(True,'fixture_exclusive_canonical_candidate_OID_reservation')
        rt.admission={**a,'candidate_journal':'ROOT_CONCURRENT_CANDIDATE_RENAMED'}
        rt.admission_pin={'bytes':2,'sha256':'3'*64}
        no(lambda:v.reserve_candidate_oid(rt),'same_candidate_OID_new_admission_journal_cannot_redispatch')
        rt.admission={**a,'candidate':next(iter(q.RETIRED))}
        no(lambda:v.reserve_candidate_oid(rt),'retired04_06_mutation_reservation_refused')
        # Full original fixture lock checks are inherited; no real global lock opened.
        replacement=lockpath.with_name('replacement');write(replacement,e.LOCK_BYTES);os.replace(replacement,lockpath)
        no(lambda:e.WriterLock(m['writer_lock']).__enter__(),'same_payload_replaced_fixture_inode_refused')
        # Actual-CAS parser and sync use only clearly synthetic owned records.
        # No Runtime authorization/Root gate is produced or represented as real.
        rt.admission=a;rt.admission_pin={'bytes':1,'sha256':'1'*64}
        st=lockpath.stat();m['writer_lock']={**m['writer_lock'],'device':st.st_dev,'inode':st.st_ino}
        refvalue[0]=descendant
        no(lambda:v.actual_cas(rt,None,observer),'descendant_without_separate_actual_CAS_record_refused')
        def record(name,obj):
            data=q.enc({**obj,'synthetic_fixture_only_not_authority':True})
            path=case/'synthetic_receipts'/name;write(path,data);return {'path':str(path),**q.pin(data)}
        reports=[record('proof'+str(i)+'.json',proof) for i in (1,2)]
        precas=record('precas.json',{'schema':'pr211-root-concurrent-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':211,'accepted':True,'protocol_pin':seed.source_pin,'admission_pin':rt.admission_pin,
            'logical_manifest_pin':q.MP,'logical_gate_pin':q.GP,'candidate':a['candidate'],'tree':a['tree'],
            'immutable_candidate_verification_accepted':True,'independent_GET_candidate_verification_accepted':True,
            'cache_manifest_pin':q.CM,'cache_acceptance_pin':q.CA,'verification_reports':reports})
        ready=record('ready.json',{'schema':'pr211-concurrent-locked-CAS-ready-v1',
            'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS','protocol_pin':seed.source_pin,
            'admission_pin':rt.admission_pin,'parent':a['parent'],'candidate':a['candidate'],'original_stable_lock_held':True,'guard_pid':1234})
        req=record('request.json',{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
            'expected_sha':a['parent'],'sha':a['candidate'],'force':False})
        response=record('response.json',{'isError':False,'structuredContent':{'success':True}})
        readback=record('readback.json',{'ref':'refs/heads/main','object':{'type':'commit','sha':a['candidate']}})
        receipt=record('readback-receipt.json',{'method':'GET','path':'git/ref/heads/main','exit':0,
            'stdout_pin':{k:readback[k] for k in ('bytes','sha256')}})
        poll=record('poll.json',{'session_id':54321,'output':'','exit_code':None})
        confirmation_obj={'schema':'pr211-root-postCAS-same-live-guard-confirmation-v1',
            'evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'protocol_pin':seed.source_pin,
            'admission_pin':rt.admission_pin,'guard_pid':1234,'session_id':54321,
            'actual_lock_guard_ready_pin':{k:ready[k] for k in ('bytes','sha256')},
            'actual_tool_response_pin':{k:response[k] for k in ('bytes','sha256')},
            'actual_readback_response_pin':{k:readback[k] for k in ('bytes','sha256')},
            'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
            'original_lock_continuity_from_linear_held_source_and_same_live_session':True,
            'actual_same_session_poll_response':poll}
        confirmation=record('confirmation.json',confirmation_obj)
        cas_obj={'schema':'pr211-root-concurrent-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':211,'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math',
            'protocol_pin':seed.source_pin,'source_manifest_pin':seed.source_manifest_pin,'admission_pin':rt.admission_pin,
            'logical_manifest_pin':q.MP,'logical_gate_pin':q.GP,'cache_manifest_pin':q.CM,'cache_acceptance_pin':q.CA,
            'facts':m['facts'],'parent':a['parent'],'candidate':a['candidate'],'tree':a['tree'],
            'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
            'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,
            'actual_MAIN_after_CAS':a['candidate'],'preCAS_acceptance':precas,'actual_lock_guard_ready':ready,
            'actual_tool_request':req,'actual_tool_response':response,'actual_readback_response':readback,
            'actual_readback_receipt':receipt,'post_CAS_same_live_guard_confirmation':confirmation}
        cas=record('cas.json',cas_obj)
        v.actual_cas(rt,cas,observer);yes(True,'synthetic_actual_CAS_request_result_readback_parser_positive')
        for changes,label in [({'unknown_outcome':True},'unknown_outcome'),({'actual_Root_MCP_CAS_performed':False},'planned_only'),
                              ({'original_lock_held_across_actual_Root_CAS':False},'lock_not_held')]:
            bad=record('bad_'+label+'.json',{**cas_obj,**changes})
            no(lambda bad=bad:v.actual_cas(rt,bad,observer),'actual_CAS_'+label+'_refused')
        force_req=record('force_request.json',{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
            'expected_sha':a['parent'],'sha':a['candidate'],'force':True})
        bad=record('bad_force.json',{**cas_obj,'actual_tool_request':force_req})
        no(lambda:v.actual_cas(rt,bad,observer),'force_true_actual_request_refused')
        missing_confirmation=record('bad_missing_confirmation.json',{k:value for k,value in cas_obj.items()
            if k!='post_CAS_same_live_guard_confirmation'})
        no(lambda:v.actual_cas(rt,missing_confirmation,observer),'ready_file_alone_not_lock_continuity')
        wrong_pid=record('wrong_pid.json',{**confirmation_obj,'guard_pid':1235})
        bad=record('bad_pid.json',{**cas_obj,'post_CAS_same_live_guard_confirmation':wrong_pid})
        no(lambda:v.actual_cas(rt,bad,observer),'other_guard_PID_not_same_live_session')
        exited_poll=record('exited_poll.json',{'session_id':54321,'output':'','exit_code':0})
        exited=record('exited_confirmation.json',{**confirmation_obj,'actual_same_session_poll_response':exited_poll})
        bad=record('bad_exited.json',{**cas_obj,'post_CAS_same_live_guard_confirmation':exited})
        no(lambda:v.actual_cas(rt,bad,observer),'exited_session_not_continuity')
        # Inject an owned-state change after first per-file receipt. The next
        # guarded effect must stop, retain a qualified mixed state and no pointer.
        changed_once=[False]
        def effect_put(directory,name,value):
            e.put(directory,name,value)
            if name=='VIEW_0.json' and not changed_once[0]:
                changed_once[0]=True;refvalue[0]='d'*40
                commits[refvalue[0]]={'sha':refvalue[0],'tree':{'sha':badroot},'parents':[{'sha':descendant}]}
        rt.e=types.SimpleNamespace(WriterLock=e.WriterLock,ParentHandle=e.ParentHandle,put=effect_put,local_pin=e.local_pin)
        sync_journal=e.journal_new('ROOT_CONCURRENT_SYNC_INTERRUPTED')
        no(lambda:v.sync(rt,observer,sync_journal,cas),'owned_change_between_local_effects_suppresses_promotion')
        pointer=native/'ROOT_ACTUAL_CONCURRENT_ADOPTION100_POINTER.json'
        yes(not pointer.exists(),'failed_mixed_sync_has_no_pointer')
        statuses=[e.local_pin(h,root/r['path']) for r in m['local_views']]
        yes(statuses[0]==q.pin(overlay[m['local_views'][0]['path']])
            and statuses[1:]==[r['preimage'] for r in m['local_views'][1:]],'failed_sync_qualified_one_post_four_pre')
        # Follow a fresh restoring descendant rather than editing an immutable
        # object or moving Main backward in the fixture.
        refvalue[0]='e'*40
        commits[refvalue[0]]={'sha':refvalue[0],'tree':{'sha':descroot},'parents':[{'sha':'d'*40}]}
        rt.e=e
        resumed=e.journal_new('ROOT_CONCURRENT_SYNC_RESUMED')
        result=v.sync(rt,observer,resumed,cas)
        yes(result['actual_MAIN_observed']=='e'*40 and result['CAS_target']==a['candidate']
            and result['all_five_local_postimages_verified'] is True,'resume_actual_CAS_mixed_state_under_original_fixture_lock')
        yes(result['external_Root_terminal_acceptance_inferred'] is False
            and result['perpetual_or_write_time_Main_equality_claimed'] is False,'sync_not_terminal_or_perpetual_Main_authority')
        v.checked_pointer(rt,cas);v.local_states(rt,all_post=True)
        yes(pointer.exists(),'pointer_only_after_five_posts_and_fresh_descendant_validation')
    return {'schema':'pr211-concurrent-native-offline-controls-v1','status':'PASS','checks':checks,'check_count':len(checks),
        'protocol_pin':q.pin(raw),'actual_native_cache_objects_reparsed_locally':202,
        'source_or_module_monkeypatches':False,'owned_synthetic_contexts_only':True,
        'network_Git_production_lock_current_five_or_provider_actions':False,
        'actual_admissions_Root_gates_CAS_or_completion_generated':False}


if __name__=='__main__':
    if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
            and not sys.flags.optimize):raise RuntimeError('Use -E -S -B -P')
    print(json.dumps(run(),sort_keys=True,indent=2))
