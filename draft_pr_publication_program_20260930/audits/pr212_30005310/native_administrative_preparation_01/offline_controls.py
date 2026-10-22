"""Owned synthetic controls only. Never production CLI, gh, real lock or current5."""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,sys,tempfile,types
BASE=Path(__file__).absolute().parent

def module(path,raw):
    m=types.ModuleType(path.stem);m.__file__=str(path);exec(compile(raw,str(path),'exec'),m.__dict__);return m

def run():
    checks=[]
    def yes(value,label):
        if not value:raise RuntimeError(label)
        checks.append(label)
    def no(call,label):
        try:call()
        except (RuntimeError,TypeError,ValueError,KeyError,OSError):checks.append(label)
        else:raise RuntimeError('Expected refusal '+label)
    h=module(BASE/'native212_model.py',(BASE/'native212_model.py').read_bytes())
    source=(BASE/'administrative_checkpoint.py').read_bytes()
    q=module(BASE/'administrative_checkpoint.py',source)
    e=module(BASE/'native212_primitives.py',(BASE/'native212_primitives.py').read_bytes())
    c=h.core()
    def queue_row(code=b'30005310 / OWR-11695865-009',status=b'claimed_solved',rank=b'212'):
        cells=[b'']*14;cells[1]=b' '+rank+b' ';cells[2]=b' '+code+b' ';cells[3]=b' fixture '
        cells[8]=b' '+status+b' ';cells[9]=b' 1/5 '
        return b'|'.join(cells)+b'\n'
    own=queue_row();foreign=queue_row(b'999999 / FOREIGN',b'unsolved',b'999')
    yes(h.own_queue_row(b'header\n'+own+foreign)[0]==own,'canonical_unique_own_row_returns_original_bytes')
    for prefix,name in [(b' ','space1'),(b'  ','space2'),(b'   ','space3'),(b'\t','tab')]:
        no(lambda prefix=prefix:h.own_queue_row(own+prefix+own),'indented_duplicate_'+name+'_refused')
        no(lambda prefix=prefix:h.own_queue_row(prefix+own),'indented_single_'+name+'_refused')
    for bad,name in [(own[1:],'missing_initial_pipe'),(own[:-2]+b'\n','missing_final_pipe'),
                     (own.replace(b'|',b'|',1).replace(b' fixture |',b' fixture '),'missing_column_delimiter'),
                     (queue_row(b'30005310 / WRONG'),'wrong_own_code'),
                     (queue_row(b'30005310x'),'malformed_own_ID_code'),
                     (queue_row(b'`30005310 / OWR-11695865-009`'),'backtick_own_code'),
                     (queue_row(b'[30005310 / OWR-11695865-009](https://example.invalid)'),'linked_own_code')]:
        no(lambda bad=bad:h.own_queue_row(own+bad),'malformed_duplicate_'+name+'_refused')
    no(lambda:h.own_queue_row(own+own),'canonical_duplicate_refused')
    for name in ('ROOT_ADMIN212_READ_X/RAW.json','ROOT_ADMIN212_SYNC_X/VIEW_0.json','ROOT_ADMIN212_CANDIDATE_X/RAW.json','_private_native/body.txt'):
        yes(not h.public_path(h.CASE+name),'operational_private_target_refused_'+name)
    identity={'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-17T22:00:00Z'}
    cm={'commit_author':identity,'commit_committer':identity,'commit_message':'Archive PR212 administrative untouched nonclaimed disposition\n'}
    body,oid=h.commit_request(cm,'1'*40,['2'*40])
    yes(body['parents']==['2'*40] and h.hexid(oid),'neutral_one_parent_canonical_commit_positive')
    for msg in ('Closes #212\n','Fixes https://github.com/AlecKriebel/Math/issues/212\n','Resolves #212\n',cm['commit_message']+'x'):
        no(lambda msg=msg:h.commit_request({**cm,'commit_message':msg},'1'*40,['2'*40]),'auto_closing_or_changed_message_refused_'+str(len(checks)))
    for parents in ([h.CURRENT],[h.ORIGINAL],['2'*40,h.CURRENT]):
        no(lambda parents=parents:h.commit_request(cm,'1'*40,parents),'snapshot_or_merge_parent_refused_'+str(len(checks)))
    yes(h.phase_facts()['fully_completed_count']==53 and h.phase_facts()['published_count']==37
        and h.phase_facts()['last_completed_PR']==211 and h.phase_facts()['completed_eligible_workflow'] is False
        and h.phase_facts()['advance_to_next_PR_authorized_now'] is False,'administrative_facts_not_new_completed_or_actual_cursor_authority')
    yes(e.api_argv('GET','pulls/212',False)[2:6]==['--hostname','github.com','--method','GET'],'canonical_explicit_GitHub_hostname')
    astree=ast.parse(source)
    cand=next(n for n in astree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate')
    posts=[n for n in ast.walk(cand) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
           and n.func.id=='api' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='POST']
    yes(len(posts)==2 and [n.args[1].value for n in posts]==['git/trees','git/commits'],'exact_two_immutable_POST_sites_no_PR_ref_blob_writer')
    immutable=next(n for n in astree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_immutable')
    parent=next(n for n in astree.body if isinstance(n,ast.FunctionDef) and n.name=='parent_state')
    yes('git/ref/heads/main' not in ast.unparse(immutable)+ast.unparse(parent),'immutable_proof_no_Main_read_or_spoof')
    with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as temporary:
        root=Path(temporary)/'checkout';program=root/'draft_pr_publication_program_20260930'
        case=program/'audits/pr212_30005310';b=case/'native_administrative_preparation_01';b.mkdir(parents=True)
        def write(path,raw):
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():path.chmod(0o644)
            path.write_bytes(raw);path.chmod(0o444)
        for name in ('native212_model.py','native212_primitives.py','native_trees_readonly.py','administrative_checkpoint.py','BASELINE_MEMBERSHIP.json'):
            write(b/name,(BASE/name).read_bytes())
        v=module(b/'administrative_checkpoint.py',source)
        hh=module(b/'native212_model.py',(b/'native212_model.py').read_bytes())
        ee=module(b/'native212_primitives.py',(b/'native212_primitives.py').read_bytes())
        core=hh.core()
        def enc(obj):return (json.dumps(obj,sort_keys=True,indent=2)+'\n').encode()
        def record(name,obj):
            data=enc({**obj,'synthetic_fixture_only_not_authority':True});p=case/'fixture_receipts'/name
            write(p,data);return {'path':str(p),**h.pin(data)}
        # Existing accepted Root bytes are copied solely as hash-bound input data.
        evidence={}
        for role,path in h.ROOT_EVIDENCE_PATHS.items():
            raw=(BASE.parent/path).read_bytes();write(case/path,raw)
            evidence[role]={'path':str(case/path),**h.pin(raw)}
        prior=(BASE.parent.parent/'pr211_5100063/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json').read_bytes()
        baseline=h.source_baseline()
        native_progress=enc({**h.baseline_facts(),**baseline,'dated_eligible_total':99})
        native_global_log=b'old PR211 history bytes\n'
        local_bodies={h.VIEWS[0]:b'{"local_case_percent":75}\n',h.VIEWS[1]:b'local case audit history\n',
            h.VIEWS[2]:native_progress,h.VIEWS[3]:b'old global md\n',
            h.VIEWS[4]:native_global_log+b'local administrative work\n'}
        post_json=enc({**h.phase_facts(),'conditional_proposal_only':True,'completed':False,
                       **baseline,'dated_eligible_total':99,'active_publication_DOI':None,'active_tracker_range':None})
        overlay={h.VIEWS[0]:post_json,h.VIEWS[1]:local_bodies[h.VIEWS[1]]+b'conditional admin\n'+h.phase_marker()+b'\n',
            h.VIEWS[2]:post_json,h.VIEWS[3]:b'conditional admin\n'+h.phase_marker()+b'\n',
            h.VIEWS[4]:local_bodies[h.VIEWS[4]]+b'conditional admin\n'+h.phase_marker()+b'\n',
            h.PRIOR_TERMINAL_PATH:prior}
        for role,path in h.ROOT_EVIDENCE_PATHS.items():overlay[h.CASE+path]=(case/path).read_bytes()
        objects={};blobs={};commits={};refvalue=['a'*40];calls=[]
        def blob(raw):
            oid=h.native('blob',raw);blobs[oid]=raw;return oid
        def tree(rows):
            rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
            oid=c.tree_hash(rows);objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':m,'type':t,'sha':o} for n,m,t,o in rows]}
            return oid
        def make_root(leaves):
            trie={}
            for path,value in leaves.items():
                node=trie
                for part in path.split('/')[:-1]:node=node.setdefault(part,{})
                node[path.split('/')[-1]]=value
            def descend(node):
                return tree([(n,'040000','tree',descend(x)) if type(x) is dict else (n,*x) for n,x in node.items()])
            return descend(trie)
        # Actual immutable PR tree metadata/currentQUEUE body are fixture inputs;
        # no science source is executed or mathematically interpreted.
        native_maps=json.loads((BASE.parent/'native_custody_01/AUTHENTICATED_NATIVE_TREES.json').read_bytes())
        for oid,rows in native_maps.items():
            yes_oid=tree([(name,*value) for name,value in rows.items()])
            if yes_oid!=oid:raise RuntimeError('Actual native metadata fixture hash')
        prqueue=(BASE.parent/'native_custody_01/_private_native/current/unsolved_math_prioritization/QUEUE.md').read_bytes()
        if blob(prqueue)!=h.CURRENT_QUEUE:raise RuntimeError('Actual PRQUEUE fixture identity')
        opaque=tree([('opaque.txt','100755','blob',blob(b'old opaque bytes\n'))])
        mainqueue=b'header\n'+own+foreign
        leaves={h.QUEUE:('100644','blob',blob(mainqueue)),
            h.ATTEMPT:('040000','tree',opaque),h.SHARED:('040000','tree',opaque),
            h.VIEWS[2]:('100644','blob',blob(native_progress)),h.VIEWS[3]:('100644','blob',blob(b'old global md\n')),
            h.VIEWS[4]:('100644','blob',blob(native_global_log)),
            'foreign/executable':('100755','blob',blob(b'foreign\n')),
            'foreign/link':('120000','blob',blob(b'foreign-target')),
            'foreign/gitlink':('160000','commit','9'*40),'foreign/empty':('040000','tree',tree([]))}
        parent_root=make_root(leaves);pre={path:leaves.get(path) for path in overlay}
        for value in overlay.values():blob(value)
        wanted,changed,dirs=h.expected(c,c.NativeTrees(lambda method,path:copy.deepcopy(objects[path.rsplit('/',1)[1]])),parent_root,overlay,pre)
        tuple_json=lambda value:None if value is None else dict(zip(('mode','type','sha'),value))
        files=[]
        for index,(path,raw) in enumerate(overlay.items()):
            name='_fixture_packet/body'+str(index);write(b/name,raw)
            files.append({'path':path,'source':name,**h.pin(raw),'git_blob':h.native('blob',raw),'preimage':tuple_json(pre[path])})
        local=[]
        for index,path in enumerate(h.VIEWS):
            name='_fixture_packet/local'+str(index);write(b/name,local_bodies[path]);write(root/path,local_bodies[path])
            local.append({'path':path,'source':name,'preimage':h.pin(local_bodies[path])})
        m={'schema':'pr212-conditional-administrative-logical-packet-v1','PR':212,'problem_id':'30005310',
            'phase':'administrative100','facts':h.phase_facts(),'files':files,'total_files':len(files),
            'total_bytes':sum(map(len,overlay.values())),'local_views':local,'protected_queue':tuple_json(leaves[h.QUEUE]),
            'protected_queue_row_pin':h.pin(own),'protected_nodes':{p:tuple_json(leaves[p]) for p in (h.ATTEMPT,h.SHARED)},
            'current_PR_opaque_body_pin':h.pin(h.compact('opaque fixture body').encode()),
            'expected_new_directories':sorted(dirs),'expected_changed_paths':sorted(changed),
            'carryforward':[{'path':h.PRIOR_TERMINAL_PATH,**h.PRIOR_TERMINAL_PIN}],
            'commit_author':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
            'commit_committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},
            'commit_message':cm['commit_message'],'retired_candidates':[],'body_proof_policy':h.BODY_POLICY,
            'QUEUE_policy':h.QUEUE_POLICY,'writer_lock':h.WRITER_LOCK_REFERENCE,'evidence_references':evidence}
        selected_names=('native212_model.py','native212_primitives.py','native_trees_readonly.py','administrative_checkpoint.py','BASELINE_MEMBERSHIP.json')
        sm={'schema':'pr212-administrative-source-manifest-v1','source_only':True,'self_excluded':True,
            'files':[{'path':n,**h.pin((b/n).read_bytes())} for n in selected_names]}
        write(b/'SOURCE_MANIFEST.json',enc(sm));sm_pin=h.pin(enc(sm));protocol_pin=h.pin(source)
        audits=[record('audit'+str(i)+'.json',{'synthetic_audit':i}) for i in range(2)]
        def logical_refs(obj):
            data=enc(obj);write(b/'_fixture_packet/manifest.json',data);mp={'path':str(b/'_fixture_packet/manifest.json'),**h.pin(data)}
            gate={'schema':'pr212-root-administrative-logical-packet-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':212,
                'accepted':True,'manifest_pin':h.pin(data),'source_manifest_pin':sm_pin,'protocol_pin':protocol_pin,
                'primitive_pin':q.PRIMITIVE_PIN,'facts':h.phase_facts(),'public_selection_reviewed':True,
                'administrative_disposition_review_accepted':True,'no_PR_or_publication_actions':True,
                'all53_37_memberships_unchanged':True,'QUEUE_policy':h.QUEUE_POLICY,'Root_full_source_read':True,
                'independent_source_adversarial_review_accepted':True,'independent_exact_packet_review_accepted':True,'audit_receipts':audits}
            gp=record('logical_gate.json',gate);return mp,gp
        mp,gp=logical_refs(m)
        seed=v.Seed(mp,gp);yes(seed.logical['facts']==h.phase_facts(),'full_new_typed_logical_input_gate_fixture_positive')
        def bad_manifest(change):
            bad=copy.deepcopy(m);change(bad);a,g=logical_refs(bad);return hh.load_inputs(a,g,sm_pin,protocol_pin,q.PRIMITIVE_PIN)
        no(lambda:bad_manifest(lambda x:x['facts'].update(fully_completed_count=54)),'false54_completed_fact_refused')
        no(lambda:bad_manifest(lambda x:x['facts'].update(publication_ready=True)),'publication_ready_admin_fact_refused')
        no(lambda:bad_manifest(lambda x:x.update(commit_message='Closes #212\n')),'logical_autoclosing_message_refused')
        no(lambda:bad_manifest(lambda x:x.update(QUEUE_policy='WHOLE_QUEUE_MAY_CHANGE_FREELY')),'weakened_QUEUE_policy_refused')
        # Restore only fixture data after negatives.
        mp,gp=logical_refs(m);seed=v.Seed(mp,gp)
        author={**m['commit_author'],'date':identity['date']}
        a={'schema':'pr212-administrative-parent-admission-v1','PR':212,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE',
           'protocol_pin':seed.source_pin,'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
           'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
           'parent':'a'*40,'parent_tree':parent_root,'parents':['a'*40],'created_UTC':identity['date'],
           'commit_author':author,'commit_committer':author,'commit_message':m['commit_message'],
           'tree':wanted,'candidate':'0'*40,'candidate_journal':'ROOT_ADMIN212_CANDIDATE_FIXTURE'}
        effective={**m,'expected_parent':a['parent'],'expected_parent_tree':parent_root,'commit_author':author,'commit_committer':author}
        request,a['candidate']=h.commit_request(effective,wanted,[a['parent']])
        v.checked_admission(seed,a);yes(True,'typed_new_admission_neutral_one_parent_positive')
        bad=copy.deepcopy(a);bad['parents'].append(h.CURRENT)
        no(lambda:v.checked_admission(seed,bad),'admission_snapshot_second_parent_refused')
        bad=copy.deepcopy(a);bad['facts']['fully_completed_count']=53.0
        no(lambda:v.checked_admission(seed,bad),'deep_float_fact_type_refused')
        after={**leaves,**{p:('100644','blob',h.native('blob',raw)) for p,raw in overlay.items()}}
        yes(make_root(after)==wanted,'independent_full_archive_tree_expected')
        commits.update({h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':h.ORIGINAL_PARENT}]},
            h.CURRENT:{'sha':h.CURRENT,'tree':{'sha':h.CURRENT_TREE},'parents':[{'sha':h.ORIGINAL}]},
            a['parent']:{'sha':a['parent'],'tree':{'sha':parent_root},'parents':[{'sha':h.ANCHOR}]},
            a['candidate']:{'sha':a['candidate'],'tree':{'sha':wanted},'parents':[{'sha':a['parent']}],
                'author':author,'committer':author,'message':m['commit_message']}})
        pr={'number':212,'title':'30005310: Credited prior counterexamples to literal numerical scenarios',
            'state':'open','draft':True,'merged':False,'merged_at':None,'commits':3,'head':{'sha':h.CURRENT,'ref':'math/30005310-colored-threshold-wip'},
            'base':{'ref':'main'},'body':'opaque fixture body'}
        def ahead(first,last):
            seen=set();todo=[last]
            while todo:
                x=todo.pop()
                if x==first:return True
                if x in seen:continue
                seen.add(x);todo.extend(r['sha'] for r in commits.get(x,{}).get('parents',[]))
            return False
        class Observer:
            def __init__(self,journal):
                self.journal=journal;self.actual_GET_origins={};self.number=0;self.reads=[];self.trip_after_view0=None
            def __call__(self,method,path,body=None):
                if method!='GET' or body is not None:raise RuntimeError('Synthetic GET only')
                self.number+=1;self.reads.append(path)
                if path=='git/ref/heads/main':
                    if self.trip_after_view0 is not None and self.trip_after_view0.exists():commits[refvalue[0]]['tree']['sha']=self.bad_root
                    return {'object':{'sha':refvalue[0]}}
                if path=='pulls/212':return copy.deepcopy(pr)
                if path.startswith('compare/'):
                    x,y=path[8:].split('...');return {'status':'ahead' if ahead(x,y) else 'diverged','merge_base_commit':{'sha':x if ahead(x,y) else '0'*40}}
                oid=path.rsplit('/',1)[1]
                if path.startswith('git/commits/'):return copy.deepcopy(commits[oid])
                if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
                if path.startswith('git/blobs/'):
                    raw=blobs[oid];value={'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
                    prefix='blob_'+oid;out=self.journal/(prefix+'.stdout.json');err=self.journal/(prefix+'.stderr.txt');rec=self.journal/(prefix+'.receipt.json')
                    data=enc(value)
                    if not out.exists():
                        ee.put_raw(self.journal,out.name,data);ee.put_raw(self.journal,err.name,b'')
                        response={'path':str(out),**h.pin(data)};stderr={'path':str(err),**h.pin(b'')}
                        receipt={'method':'GET','path':path,'exit':0,'raw_stdout':response,'raw_stderr':stderr}
                        ee.put(self.journal,rec.name,receipt)
                    else:
                        response={'path':str(out),**h.pin(out.read_bytes())};stderr={'path':str(err),**h.pin(err.read_bytes())}
                    self.actual_GET_origins[path]={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','route':path,
                        'receipt':str(rec),'receipt_pin':h.pin(rec.read_bytes()),'raw_response':response,'raw_stderr':stderr}
                    return value
                raise RuntimeError('Unexpected fixture route')
        journal=ee.journal_new('ROOT_ADMIN212_READ_FIXTURE');observer=Observer(journal)
        rt=types.SimpleNamespace(seed=seed,h=hh,e=ee,c=core,m=effective,admission=a,
            admission_pin={'bytes':1,'sha256':'1'*64},gate_pin={'bytes':1,'sha256':'2'*64},
            overlay=overlay,pre=pre,pool=hh.NativeBodyProofs())
        rt.refresh=lambda:rt
        refvalue[0]='f'*40;proof=v.verify_immutable(rt,observer)
        yes(proof['full_scope_verified'] and len(proof['selected_files'])==len(overlay),'full_new_native_selected_body_and_foreign_scope_proof')
        yes('git/ref/heads/main' not in observer.reads,'immutable_native_proof_ignores_moving_Main')
        before_reads=len(observer.reads);v.verify_immutable(rt,observer)
        yes(not any(x.startswith('git/blobs/') for x in observer.reads[before_reads:]),'checked_actual_envelope_bytes_reused_only_within_API_instance')
        separate=Observer(ee.journal_new('ROOT_ADMIN212_READ_INDEPENDENT'));rt.pool=hh.NativeBodyProofs();v.verify_immutable(rt,separate)
        yes(any(x.startswith('git/blobs/') for x in separate.reads),'new_independent_API_refetches_native_bodies')
        commits[a['candidate']]['message']=m['commit_message'][:-1]
        yes(v.verify_immutable(rt,observer)['commit_message_readback']['terminal_LFs_omitted']==1,'canonical_oneLF_readback_fix_retained')
        commits[a['candidate']]['message']=m['commit_message']+'\n'
        no(lambda:v.verify_immutable(rt,observer),'changed_extraLF_commit_message_refused')
        commits[a['candidate']]['message']=m['commit_message']
        descendant='b'*40;foreign_queue=b'header\n'+own+queue_row(b'999999 / FOREIGN',b'already_solved',b'999')
        descroot=make_root({**after,h.QUEUE:('100644','blob',blob(foreign_queue)),'foreign/new':('100644','blob',blob(b'new foreign\n'))})
        commits[descendant]={'sha':descendant,'tree':{'sha':descroot},'parents':[{'sha':a['candidate']}]};refvalue[0]=descendant
        observed=v.main_closure(rt,observer)
        yes(observed['actual_MAIN_observed']==descendant and observed['Main_QUEUE_observation']['observed_QUEUE_oid']!=m['protected_queue']['sha']
            and observed['CAS_target']==a['candidate'],'preserving_descendant_foreign_QUEUE_rows_allowed_C_R_separate')
        changed_own=queue_row(status=b'already_solved')
        badroot=make_root({**after,h.QUEUE:('100644','blob',blob(b'header\n'+changed_own+foreign))})
        commits[descendant]['tree']['sha']=badroot
        no(lambda:v.main_closure(rt,observer),'descendant_own_MainQUEUE_row_change_refused')
        duproot=make_root({**after,h.QUEUE:('100644','blob',blob(own+b' '+own+foreign))})
        commits[descendant]['tree']['sha']=duproot
        no(lambda:v.main_closure(rt,observer),'native_descendant_indented_duplicate_row_refused')
        commits[descendant]['tree']['sha']=make_root({**after,h.ATTEMPT:('040000','tree',tree([]))})
        no(lambda:v.main_closure(rt,observer),'descendant_opaque_attempt_change_refused')
        commits[descendant]['tree']['sha']=make_root({**after,next(iter(overlay)):('100644','blob',blob(b'changed post'))})
        no(lambda:v.main_closure(rt,observer),'descendant_selected_postimage_change_refused')
        commits[descendant]['tree']['sha']=descroot
        pr['merged']=True
        no(lambda:v.main_closure(rt,observer),'PR_unexpected_merge_refused')
        pr['merged']=False
        lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(lockpath,ee.LOCK_BYTES);st=lockpath.stat()
        rt.m={**effective,'writer_lock':{**h.WRITER_LOCK_REFERENCE,'device':st.st_dev,'inode':st.st_ino}}
        with ee.WriterLock(rt.m['writer_lock']) as lock:
            refvalue[0]=a['parent'];v.lease_guard(rt,observer,lock);yes(True,'fixture_original_held_lock_parent_lease_positive')
            refvalue[0]=descendant
            no(lambda:v.lease_guard(rt,observer,lock),'preCAS_stale_parent_rejected_even_if_descendant_owned_good')
        v.local_states(rt);yes(True,'separate_native_absence_and_local_existing5_preimages_supported')
        write(root/h.VIEWS[0],b'third state')
        no(lambda:v.local_states(rt,resume=True),'local_third_state_refused')
        write(root/h.VIEWS[0],overlay[h.VIEWS[0]]);v.local_states(rt,resume=True)
        yes(True,'local_mixed_exact_pre_post_supported')
        write(root/h.VIEWS[0],local_bodies[h.VIEWS[0]])
        refvalue[0]=a['parent'];v.reserve_candidate_oid(rt)
        yes(True,'canonical_candidate_OID_durable_fixture_reservation')
        rt.admission={**a,'candidate_journal':'ROOT_ADMIN212_CANDIDATE_RENAMED'}
        no(lambda:v.reserve_candidate_oid(rt),'renamed_journal_cannot_retry_same_candidateOID')
        rt.admission=a

        # Full actual-CAS parser and sync run only on owned synthetic receipts,
        # synthetic native observer and fixture lock. No production gate exists.
        reports=[record('native_proof_'+str(i)+'.json',v.verify_immutable(rt,obs))
                 for i,obs in enumerate((observer,separate))]
        common={'PR':212,'protocol_pin':seed.source_pin,'source_manifest_pin':seed.source_manifest_pin,
                'admission_pin':rt.admission_pin,'logical_manifest_pin':seed.manifest_pin,'logical_gate_pin':seed.logical_gate_pin,
                'candidate':a['candidate'],'tree':a['tree'],'body_proof_policy':hh.BODY_POLICY,'QUEUE_policy':hh.QUEUE_POLICY}
        pre_accept=record('preCAS.json',{**common,'schema':'pr212-root-administrative-preCAS-acceptance-v1',
            'evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'immutable_candidate_verification_accepted':True,
            'independent_GET_candidate_verification_accepted':True,'verification_reports':reports})
        ready=record('ready.json',{'schema':'pr212-administrative-locked-CAS-ready-v1',
            'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS','protocol_pin':seed.source_pin,
            'admission_pin':rt.admission_pin,'parent':a['parent'],'candidate':a['candidate'],
            'original_stable_lock_held':True,'guard_pid':1234})
        reqobj={'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
                'expected_sha':a['parent'],'sha':a['candidate'],'force':False}
        request_ref=record('request.json',reqobj)
        response_ref=record('response.json',{'isError':False,'structuredContent':{'success':True}})
        readback_ref=record('readback.json',{'ref':'refs/heads/main','object':{'type':'commit','sha':descendant}})
        readback_receipt=record('readback_receipt.json',{'method':'GET','path':'git/ref/heads/main','exit':0,
            'stdout_pin':{k:readback_ref[k] for k in ('bytes','sha256')}})
        pollref=record('poll.json',{'session_id':42,'exit_code':None,'output':'still running'})
        liveobj={'schema':'pr212-root-postCAS-same-live-guard-confirmation-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'accepted':True,'protocol_pin':seed.source_pin,'admission_pin':rt.admission_pin,
            'actual_lock_guard_ready_pin':{k:ready[k] for k in ('bytes','sha256')},
            'actual_tool_response_pin':{k:response_ref[k] for k in ('bytes','sha256')},
            'actual_readback_response_pin':{k:readback_ref[k] for k in ('bytes','sha256')},
            'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
            'original_lock_continuity_from_linear_held_source_and_same_live_session':True,
            'guard_pid':1234,'session_id':42,'actual_same_session_poll_response':pollref}
        liveref=record('live_confirmation.json',liveobj)
        casobj={**common,'schema':'pr212-root-administrative-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math','facts':hh.phase_facts(),
            'parent':a['parent'],'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
            'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'preCAS_acceptance':pre_accept,
            'actual_lock_guard_ready':ready,'actual_tool_request':request_ref,'actual_tool_response':response_ref,
            'actual_readback_response':readback_ref,'actual_readback_receipt':readback_receipt,
            'post_CAS_same_live_guard_confirmation':liveref,'actual_MAIN_after_CAS':descendant}
        casref=record('actual_CAS_fixture.json',casobj);refvalue[0]=descendant
        yes(v.actual_cas(rt,casref,observer)['actual_MAIN_after_CAS']==descendant,
            'actual_CAS_parser_requires_qualified_distinct_C_R_synthetic_evidence_positive')
        for name,change in [('unknown',lambda x:x.update(unknown_outcome=True)),
                            ('missing_live',lambda x:x.pop('post_CAS_same_live_guard_confirmation')),
                            ('no_actual_CAS',lambda x:x.update(actual_Root_MCP_CAS_performed=False))]:
            bad=copy.deepcopy(casobj);change(bad);badref=record('bad_CAS_'+name+'.json',bad)
            no(lambda badref=badref:v.actual_cas(rt,badref,observer),'actual_CAS_'+name+'_refused')
        bad=copy.deepcopy(casobj);bad['actual_tool_request']=record('force_request.json',{**reqobj,'force':True})
        badref=record('bad_force.json',bad)
        no(lambda:v.actual_cas(rt,badref,observer),'force_true_external_request_refused')
        badpoll=record('exited_poll.json',{'session_id':42,'exit_code':0,'output':'exited'})
        bad=copy.deepcopy(casobj);bad['post_CAS_same_live_guard_confirmation']=record('exited_live.json',{**liveobj,'actual_same_session_poll_response':badpoll})
        badref=record('bad_exit.json',bad)
        no(lambda:v.actual_cas(rt,badref,observer),'exited_guard_ready_file_not_lock_continuity')
        failure_journal=ee.journal_new('ROOT_ADMIN212_SYNC_FAILURE_FIXTURE')
        observer.trip_after_view0=failure_journal/'VIEW_0.json'
        observer.bad_root=badroot
        no(lambda:v.sync(rt,observer,failure_journal,casref),'sync_observed_bad_owned_state_after_first_install_stops')
        yes((failure_journal/'VIEW_0.json').exists()
            and not (failure_journal/'VIEW_1.json').exists()
            and not (b/'ROOT_ACTUAL_ADMINISTRATIVE_POINTER.json').exists(),
            'failed_sync_mixed_local_state_has_no_pointer_or_second_install')
        yes((root/h.VIEWS[0]).read_bytes()==overlay[h.VIEWS[0]]
            and (root/h.VIEWS[1]).read_bytes()==local_bodies[h.VIEWS[1]],'first_install_only_retained_as_qualified_mixed_state')
        observer.trip_after_view0=None;commits[descendant]['tree']['sha']=descroot
        v.local_states(rt,resume=True)
        resumed=ee.journal_new('ROOT_ADMIN212_SYNC_RESUME_FIXTURE')
        result=v.sync(rt,observer,resumed,casref)
        yes(result['all_five_local_postimages_verified'] and result['actual_MAIN_observed']==descendant
            and result['external_Root_terminal_acceptance_inferred'] is False,
            'actual_source_five_perfile_resume_preserves_descendant_and_withholds_terminal_authority')
        yes(all((root/path).read_bytes()==body for path,body in overlay.items() if path in h.VIEWS),
            'all_five_fixture_posts_exact_after_resume')
        yes(v.checked_pointer(rt,casref)==h.pin((b/'ROOT_ACTUAL_ADMINISTRATIVE_POINTER.json').read_bytes()),
            'actual_source_pointer_binds_exact_sync_and_C_R')

        oldlock=rt.m['writer_lock'];lockpath.unlink();write(lockpath,ee.LOCK_BYTES)
        no(lambda:ee.WriterLock(oldlock).__enter__(),'same_payload_replaced_fixture_inode_refused')
        no(lambda:v.actual_cas(rt,None,observer),'descendant_never_substitutes_actual_Root_CAS')
    return {'schema':'pr212-administrative-source-offline-controls-v1','status':'PASS','check_count':len(checks),'checks':checks,
        'protocol_pin':h.pin(source),'production_CLI_executions':0,'network_Git_real_lock_currentfive_or_provider_actions':False,
        'actual_Root_packets_gates_admissions_CAS_or_admin_terminals_created':False,
        'source_or_module_monkeypatches':False,'ordinary_owned_synthetic_contexts_and_observers':True}

if __name__=='__main__':
    if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
        raise RuntimeError('Use -E -S -B -P')
    print(json.dumps(run(),sort_keys=True,indent=2))
