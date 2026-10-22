"""One-use owned synthetic full frozen inspect path; never a live Root terminal."""
import ast,base64,copy,hashlib,json,os,pathlib,stat,types,datetime,sys
HERE=pathlib.Path(__file__).absolute().parent
SOURCE=HERE.parent/'native_completion_preparation_01'
BINDINGS=json.loads((HERE/'REVIEWED_SOURCE_BINDINGS.json').read_text())
SOURCE_MANIFEST_PIN=BINDINGS['manifest_pin']
TERMINAL_PIN=BINDINGS['terminal_pin']
CONSUMER_PIN=BINDINGS['consumer_pin']
def need(x,msg):
    if type(x) is not bool or not x:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(j):return (json.dumps(j,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(path,value,raw=False):
    body=value if raw else enc(value);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:need(f.write(body)==len(body),'Short owned fixture write')
    path.chmod(0o444);return {'path':str(path),**pin(body)}
def module(path,name):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def main():
    def deny_effects(event,args):
        if event in ('subprocess.Popen','os.system','os.exec','socket.connect','socket.connect_ex','socket.bind'):raise RuntimeError('Network/subprocess forbidden in owned roundtrip')
    sys.addaudithook(deny_effects)
    need(HERE.name=='native_completion_source_adversary_01' and HERE.parent.name=='pr218_30006020','Only dedicated owned fixture')
    source_raw=SOURCE.joinpath('SOURCE_MANIFEST.json').read_bytes()
    need(pin(source_raw)==SOURCE_MANIFEST_PIN,'Frozen02 source manifest pin')
    manifest=json.loads(source_raw);need(6<=len(manifest['files'])<=20,'Finite frozen payloads')
    checkout=HERE/'_synthetic_roundtrip_checkout_03';need(not checkout.exists(),'One-use fixture output must be absent')
    program=checkout/'draft_pr_publication_program_20260930';case=program/'audits/pr218_30006020'
    B=case/'native_completion_preparation_01';B.mkdir(parents=True)
    for row in manifest['files']:
        need(pathlib.Path(row['path']).name==row['path'],'Finite basename copy')
        raw=(SOURCE/row['path']).read_bytes();need(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'Frozen payload drift')
        put(B/row['path'],raw,True)
    put(B/'SOURCE_MANIFEST.json',source_raw,True)
    h=module(B/'native218_model.py','owned_fixture_h');e=module(B/'native218_primitives.py','owned_fixture_e')
    q=module(B/'completion_checkpoint.py','owned_fixture_q');t=module(B/'ROOT_TERMINAL_INSPECTION.py','owned_fixture_t')
    need(pin((B/'ROOT_TERMINAL_INSPECTION.py').read_bytes())==TERMINAL_PIN,'Exact terminal source')
    need(h.CHECKOUT==q.CHECKOUT==e.CHECKOUT==t.CHECKOUT==checkout,'All subjects remain in synthetic checkout')
    c=h.core();objects={};blobs={};commits={}
    def blob(raw):
        oid=h.native('blob',raw);blobs[oid]=raw;return ('100644','blob',oid)
    def tree(flat):
        trie={}
        for path,item in flat.items():
            node=trie;parts=path.split('/')
            for part in parts[:-1]:node=node.setdefault(part,{})
            node[parts[-1]]=item
        def walk(node):
            rows=[]
            for name,item in node.items():rows.append((name,'040000','tree',walk(item)) if isinstance(item,dict) else (name,*item))
            rows.sort(key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
            oid=c.tree_hash(rows)
            objects[oid]={'sha':oid,'truncated':False,'tree':[dict(path=n,mode=m,type=k,sha=s) for n,m,k,s in rows]}
            return oid
        return walk(trie)
    empty=c.tree_hash([]);objects[empty]={'sha':empty,'truncated':False,'tree':[]}
    own=b'|218|30006020 / OWR-14298589-005|a|b|c|d|e|queued|0/5|f|g|h|\n'
    parent_queue=b'|foreign|999999|original fixture foreign row|\n'+own
    descendant_queue=b'|foreign|999999|updated fixture foreign row|\n'+own
    baseline=h.source_baseline()
    parentflat={h.QUEUE:blob(parent_queue),h.ATTEMPT+'/proof.txt':blob(b'synthetic protected proof bytes\n'),
        h.SHARED+'/preprint/metadata.json':blob(enc({'scope':'synthetic protected metadata'})),
        h.VIEWS[2]:blob(enc({**h.baseline_facts(),**baseline,'dated_eligible_total':99})),
        h.VIEWS[3]:blob(b'prior progress\n'),h.VIEWS[4]:blob(b'prior program log\n'),
        'foreign-executable':('100755','blob',h.native('blob',b'synthetic executable')),
        'foreign-symlink':('120000','blob',h.native('blob',b'synthetic target')),
        'foreign-gitlink':('160000','commit','9'*40),'foreign-empty':('040000','tree',empty)}
    parent_tree=tree(parentflat)
    identity={'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-18T01:00:00Z'}
    def native_commit(root,parents,message,date='2026-10-18T01:00:00Z'):
        import calendar
        seconds=calendar.timegm(datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ').timetuple())
        raw=('tree '+root+'\n'+''.join('parent '+p+'\n' for p in parents)+
            'author Alec Kriebel <me@aleckriebel.com> '+str(seconds)+' +0000\n'+
            'committer Alec Kriebel <me@aleckriebel.com> '+str(seconds)+' +0000\n\n'+message).encode()
        oid=h.native('commit',raw)
        commits[oid]={'sha':oid,'tree':{'sha':root},'parents':[{'sha':p} for p in parents],
            'author':{**identity,'date':date},'committer':{**identity,'date':date},'message':message[:-1]}
        return oid
    parent=native_commit(parent_tree,['1'*40],'Synthetic parent only\n')
    facts=h.phase_facts();conditional={**facts,'conditional_proposal_only':True}
    overlay={h.VIEWS[0]:enc(conditional),h.VIEWS[1]:b'synthetic case history\n'+h.phase_marker()+b'\n',
        h.VIEWS[2]:enc({**conditional,**h.completion_memberships(),'dated_eligible_total':99}),
        h.VIEWS[3]:b'synthetic progress\n'+h.phase_marker()+b'\n',
        h.VIEWS[4]:b'prior program log\nsynthetic append\n'+h.phase_marker()+b'\n',
        h.CASE+'synthetic_selected_summary.md':b'SYNTHETIC OWNED FIXTURE ONLY\n'}
    candidateflat={**parentflat,**{p:blob(b) for p,b in overlay.items()}}
    candidate_tree=tree(candidateflat)
    cm={'commit_author':identity,'commit_committer':identity,'commit_message':h.COMMIT_MESSAGE}
    request,candidate=h.commit_request(cm,candidate_tree,[parent])
    need(native_commit(candidate_tree,[parent],h.COMMIT_MESSAGE)==candidate,'Canonical C construction')
    descendantflat={**candidateflat,h.QUEUE:blob(descendant_queue),'foreign-descendant.txt':blob(b'foreign fixture update\n')}
    descendant_tree=tree(descendantflat)
    descendant=native_commit(descendant_tree,[candidate],'Synthetic foreign descendant only\n','2026-10-18T01:00:01Z')
    class NativeFixture:
        """No subprocess or network. Actual_GET_origins is simulated provenance."""
        def __init__(self,name):
            self.name=name;self.number=0;self.actual_GET_origins={};self.reads=[]
            self.journal=e.journal_new('ROOT_COMPLETE218_READ_'+name)
        def __call__(self,method,path,body=None):
            need(method=='GET' and body is None,'Synthetic observer GET-only')
            self.reads.append(path)
            if path=='git/ref/heads/main':return {'ref':'refs/heads/main','object':{'type':'commit','sha':descendant}}
            if path=='pulls/218':return copy.deepcopy(pr)
            if path.startswith('git/trees/'):return copy.deepcopy(objects[path.rsplit('/',1)[1]])
            if path.startswith('git/commits/'):return copy.deepcopy(commits[path.rsplit('/',1)[1]])
            if path.startswith('compare/'):
                before,after=path[8:].split('...');todo=[after];seen=set()
                while todo:
                    oid=todo.pop()
                    if oid in seen:continue
                    seen.add(oid);todo.extend(p['sha'] for p in commits.get(oid,{}).get('parents',[]))
                need(before in seen,'Synthetic ancestry absent')
                return {'status':'identical' if before==after else 'ahead','merge_base_commit':{'sha':before}}
            need(path.startswith('git/blobs/'),'Unexpected synthetic route')
            oid=path.rsplit('/',1)[1];raw=blobs[oid]
            value={'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
            if path not in self.actual_GET_origins:
                self.number+=1;prefix='SYNTHETIC_'+str(self.number)
                response=put(self.journal/(prefix+'_RAW.json'),value)
                stderr=put(self.journal/(prefix+'_STDERR.txt'),b'',True)
                receipt=put(self.journal/(prefix+'_RECEIPT.json'),{'method':'GET','path':path,'exit':0,
                    'raw_stdout':response,'raw_stderr':stderr,'synthetic_transport_only':True})
                self.actual_GET_origins[path]={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math',
                    'route':path,'raw_response':response,'raw_stderr':stderr,'receipt':receipt['path'],
                    'receipt_pin':{k:receipt[k] for k in ('bytes','sha256')},'SYNTHETIC_NOT_REAL_GITHUB':True}
            return copy.deepcopy(value)
    pr={'number':218,'title':'30006020: audited intermediate-area cylinder theorem and published preprint',
        'state':'closed','draft':False,'merged':True,'merged_at':'2026-10-15T07:35:42Z','merge_commit_sha':h.MERGED,
        'head':{'sha':h.CURRENT,'ref':'dot/math-30006020'},'base':{'ref':'main'},'body':'SYNTHETIC PR FIXTURE'}
    api=NativeFixture('INSPECT');trees=c.NativeTrees(api)
    pre={path:trees.lookup(parent_tree,path) for path in overlay}
    expected,leaves,dirs=h.expected(c,trees,parent_tree,overlay,pre)
    need(expected==candidate_tree,'Full native candidate tree rebuild')
    protected_nodes={p:dict(zip(('mode','type','sha'),trees.lookup(parent_tree,p))) for p in (h.ATTEMPT,h.SHARED)}
    science_path=h.ATTEMPT+'/proof.txt';science_tuple=parentflat[science_path]
    protected_body={'path':science_path,'mode':science_tuple[0],'type':science_tuple[1],'sha':science_tuple[2],**pin(blobs[science_tuple[2]])}
    lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';put(lockpath,e.LOCK_BYTES,True);lockstat=lockpath.stat()
    lock={'path':h.PROGRAM+lockpath.name,'device':lockstat.st_dev,'inode':lockstat.st_ino,**pin(e.LOCK_BYTES)}
    refsdir=B/'_private_SYNTHETIC_REFS'
    def record(name,obj):
        return put(refsdir/('SYNTHETIC_'+name+'.json'),{**obj,'SYNTHETIC_FIXTURE_ONLY':True})
    admission={'parent':parent,'parent_tree':parent_tree,'candidate':candidate,'tree':candidate_tree}
    admission_ref=record('admission',admission)
    manifest_ref=record('logical',{'scope':'synthetic selected-postimage fixture'})
    logical_gate=record('logical_gate',{'scope':'synthetic typed prerequisite only'})
    admission_gate=record('admission_gate',{'scope':'synthetic typed prerequisite only'})
    evidence={role:record(role,{'PR':218,'accepted':True}) for role in ('math','custody','priority','adoption')}
    native_ref=record('native_identity',{'scope':'synthetic opaque state, not real submitted PR custody'})
    ready={'schema':'pr218-root-case-ready-adoption-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':218,'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,
        'existing_publication_adoption_accepted':True,'two_sequential_fresh_whole_package_reviews_accepted':True,
        'original_and_current_claimed_solved_eligibility_preserved':True,'already_merged_original_PR_verified':True,
        'existing_DOI_and_unique_tracker_row_reused':True,'no_new_provider_publication_or_tracker_append':True,
        'existing_scientific_package_frozen':True,'prior_PR217_status_only_skip_accepted':True,
        'native_identity_receipt':native_ref,'current_head':h.CURRENT,'original_merge_commit':h.MERGED,
        'existing_publication_DOI':h.EXISTING_DOI,'existing_tracker_range':h.EXISTING_TRACKER,
        'evidence_references':evidence,'numeric_advance_authorized_by_this_file':False}
    evidence={**evidence,'case_ready':record('case_ready',ready)}
    m={**cm,'facts':facts,'writer_lock':lock,'local_views':[{'path':p,'preimage':None,'source':None} for p in h.VIEWS],
        'protected_queue':dict(zip(('mode','type','sha'),parentflat[h.QUEUE])),'protected_queue_row_pin':pin(own),
        'protected_nodes':protected_nodes,'protected_bodies':[protected_body],'expected_changed_paths':sorted(leaves),
        'expected_new_directories':sorted(dirs),'retired_candidates':[],'evidence_references':evidence,
        'native_identity_receipt':native_ref,'current_PR_opaque_body_pin':pin(h.compact(pr['body']).encode())}
    for path in h.VIEWS:put(checkout/path,overlay[path],True)
    runtime_gate=record('runtime_source_gate',{'schema':'SYNTHETIC_RUNTIME_SOURCE_ACCEPTANCE',
        'source_manifest_pin':SOURCE_MANIFEST_PIN,'protocol_pin':pin((B/'completion_checkpoint.py').read_bytes()),
        'admission_ref':admission_ref,'case_ready_ref':evidence['case_ready']})
    class RuntimeFixture:
        """Controlled native/admission/readiness inputs, real exact source/gate readers."""
        def __init__(self):
            self.h,self.e,self.c=h,e,c;self.m=m;self.admission=admission;self.pre=pre;self.overlay=overlay
            self.pool=h.NativeBodyProofs();self.refresh_count=0
            self.admission_pin={k:admission_ref[k] for k in ('bytes','sha256')}
            self.seed=types.SimpleNamespace(s=types.SimpleNamespace(read_regular=q.read_regular),
                source_pin=pin((B/'completion_checkpoint.py').read_bytes()),source_manifest_pin=SOURCE_MANIFEST_PIN,
                manifest_pin={k:manifest_ref[k] for k in ('bytes','sha256')},
                logical_gate_pin={k:logical_gate[k] for k in ('bytes','sha256')})
        def refresh(self):
            # Production nofollow source-closure/read-ref and typed gate validators.
            need(t.source_closure()==(TERMINAL_PIN,SOURCE_MANIFEST_PIN),'Runtime exact source closure')
            gate=h.root_ref(runtime_gate)
            h.matches(gate,{'schema':'SYNTHETIC_RUNTIME_SOURCE_ACCEPTANCE','source_manifest_pin':SOURCE_MANIFEST_PIN,
                'protocol_pin':self.seed.source_pin,'admission_ref':admission_ref,'case_ready_ref':evidence['case_ready']},
                'Actual pinned synthetic runtime gate changed')
            h.validate_ready_value(m,evidence,h.root_ref(evidence['case_ready']))
            need(h.exact(h.root_ref(admission_ref),{**admission,'SYNTHETIC_FIXTURE_ONLY':True}),'Pinned fixture admission')
            self.refresh_count+=1;return self
    rt=RuntimeFixture()
    def verify_immutable(rt,observer):
        rt.refresh();ts=c.NativeTrees(h.GetOnly(observer));q.protected(rt,ts,parent_tree,False)
        rebuilt,changed,newdirs=h.expected(c,ts,parent_tree,overlay,pre)
        need(rebuilt==candidate_tree and changed==leaves and newdirs==dirs,'Exact synthetic parent/candidate scope')
        request,oid=h.commit_request(m,candidate_tree,[parent])
        value=observer('GET','git/commits/'+candidate)
        need(oid==candidate and value['sha']==candidate and value['tree']['sha']==candidate_tree
             and [p['sha'] for p in value['parents']]==[parent],'Canonical immutable C/T/one parent')
        h.matches(value['author'],identity,'Canonical author');h.matches(value['committer'],identity,'Canonical committer')
        h.commit_message_readback(h.COMMIT_MESSAGE,value['message'])
        changed,newdirs,deleted=ts.changes(parent_tree,candidate_tree)
        need(changed==leaves and newdirs==dirs and deleted==set(),'Full native changes preserve foreign tuples')
        selected,queue=q.body_associations(rt,observer,ts,candidate_tree)
        return {'schema':'pr218-completion-immutable-candidate-verification-v1','evidence_scope':q.IMMUTABLE_SCOPE,
            'protocol_pin':rt.seed.source_pin,'source_manifest_pin':SOURCE_MANIFEST_PIN,
            'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,
            'admission_pin':rt.admission_pin,'parent':parent,'parent_tree':parent_tree,'candidate':candidate,'tree':candidate_tree,
            'selected_count':len(selected),'selected_files':selected,'changed_leaves':sorted(changed),
            'new_directories':sorted(newdirs),'deleted_directories':[],'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
            'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
            'mutable_Main_observed_or_spoofed':False,'actual_CAS_or_completion_inferred':False,'synthetic_fixture_only':True}
    def main_closure(rt,observer):
        rt.refresh();before=observer('GET','git/ref/heads/main')['object']['sha']
        value=observer('GET','git/commits/'+before)
        comp=observer('GET','compare/'+candidate+'...'+before)
        need(comp['status']=='ahead' and comp['merge_base_commit']['sha']==candidate,'Synthetic actual descendant ancestry')
        root=value['tree']['sha'];ts=c.NativeTrees(h.GetOnly(observer))
        selected,queue=q.body_associations(rt,observer,ts,root,True)
        h.validate_pr_metadata(observer('GET','pulls/218'),m)
        need(observer('GET','git/ref/heads/main')['object']['sha']==before,'Coherent native before/after R')
        return {'actual_MAIN_observed':before,'actual_MAIN_tree':root,'CAS_target':candidate,'CAS_target_tree':candidate_tree,
            'selected_postimage_paths_verified':len(selected),'protected_body_paths_verified':1,
            'protected_opaque_attempt_audit_verified':True,'Main_QUEUE_observation':queue,
            'fresh_merged_PR_status_observation':{'HEAD':h.CURRENT,'state':'closed','draft':False,'merged':True,
                'current_status':'claimed_solved','original_merge_commit':h.MERGED,'same_selected_PR_identity':True},
            'coherent_before_after_ref':True,'CAS_or_completion_inferred_from_ancestry':False,
            'perpetual_or_write_time_Main_equality_claimed':False,
            'native_final_ref_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    fixture_driver=types.SimpleNamespace(CHECKOUT=checkout,actual_cas=q.actual_cas,verify_immutable=verify_immutable,
        main_closure=main_closure,checked_pointer=q.checked_pointer,local_states=q.local_states)
    proofrefs=[record('native_proof_'+str(i),verify_immutable(rt,NativeFixture('PROOF_'+str(i)))) for i in range(2)]
    common={'PR':218,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':SOURCE_MANIFEST_PIN,
        'admission_pin':rt.admission_pin,'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,
        'candidate':candidate,'tree':candidate_tree,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY}
    preCAS=record('preCAS',{**common,'schema':'pr218-root-completion-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'accepted':True,'immutable_candidate_verification_accepted':True,'independent_GET_candidate_verification_accepted':True,
        'verification_reports':proofrefs})
    ready_ref=record('ready',{'schema':'pr218-completion-locked-CAS-ready-v1','evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS',
        'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,'parent':parent,'candidate':candidate,
        'original_stable_lock_held':True,'guard_pid':1234})
    request_ref=record('request',{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
        'expected_sha':parent,'sha':candidate,'force':False})
    response_ref=record('response',{'isError':False,'structuredContent':{'success':True}})
    readback_ref=record('readback',{'ref':'refs/heads/main','object':{'type':'commit','sha':descendant}})
    readback_receipt=record('readback_receipt',{'method':'GET','path':'git/ref/heads/main','exit':0,
        'stdout_pin':{k:readback_ref[k] for k in ('bytes','sha256')}})
    poll=record('poll',{'session_id':42,'exit_code':None,'output':'SIMULATED STILL-RUNNING FIXTURE SESSION'})
    live=record('live',{'schema':'pr218-root-postCAS-same-live-guard-confirmation-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'accepted':True,'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'actual_lock_guard_ready_pin':{k:ready_ref[k] for k in ('bytes','sha256')},
        'actual_tool_response_pin':{k:response_ref[k] for k in ('bytes','sha256')},
        'actual_readback_response_pin':{k:readback_ref[k] for k in ('bytes','sha256')},
        'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
        'original_lock_continuity_from_linear_held_source_and_same_live_session':True,
        'guard_pid':1234,'session_id':42,'actual_same_session_poll_response':poll})
    cas_ref=record('CAS',{**common,'schema':'pr218-root-completion-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math','facts':facts,'parent':parent,
        'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
        'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'preCAS_acceptance':preCAS,
        'actual_lock_guard_ready':ready_ref,'actual_tool_request':request_ref,'actual_tool_response':response_ref,
        'actual_readback_response':readback_ref,'actual_readback_receipt':readback_receipt,
        'post_CAS_same_live_guard_confirmation':live,'actual_MAIN_after_CAS':descendant})
    observation=main_closure(rt,api);syncjournal=e.journal_new('ROOT_COMPLETE218_SYNC_FIXTURE')
    sync=put(syncjournal/'ACTUAL_FIVE_SYNC.json',{'schema':'pr218-completion-actual-five-sync-v1',
        'evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE','protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
        'CAS_target':candidate,'CAS_target_tree':candidate_tree,'all_five_local_postimages_verified':True,
        'facts':facts,'external_Root_terminal_acceptance_inferred':False,'SYNTHETIC_FIXTURE_ONLY':True})
    pointer=put(B/'ROOT_ACTUAL_COMPLETION_POINTER.json',{'schema':'pr218-completion-actual-five-pointer-v1',
        'evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE','protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
        'CAS_target':candidate,'CAS_target_tree':candidate_tree,'all_five_local_postimages_verified':True,
        'recorded_under_original_stable_lock':True,'external_Root_terminal_acceptance_inferred':False,
        'sync_path':sync['path'],'sync_pin':{k:sync[k] for k in ('bytes','sha256')},'SYNTHETIC_FIXTURE_ONLY':True})
    config={'manifest':manifest_ref,'logical_gate':logical_gate,'admission':admission_ref,'Root_gate':admission_gate,
        'actual_CAS':cas_ref,'pointer':pointer,'sync':sync,'extension_source':None,'extension_acceptance':None,
        'journal':'ROOT_COMPLETE218_READ_ROOT_TERMINAL_FIXTURE','receipt_name':'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'}
    source_acceptance=record('terminal_source_acceptance',{'schema':t.SOURCE_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY',
        'PR':218,'accepted':True,'terminal_source_pin':TERMINAL_PIN,'terminal_source_manifest_pin':SOURCE_MANIFEST_PIN,
        'approved_driver_pin':t.DRIVER_PIN,'receipt_schema':t.RECEIPT_SCHEMA,
        'Root_full_source_read':True,'independent_source_review_accepted':True,'transport_policy':t.transport_policy(config),
        'source_acceptance_is_not_actual_terminal_or_numeric_authority':True})
    config['source_acceptance']=source_acceptance;source_refreshes=[]
    def refresh_source():
        # Exact production context.refresh path, dependency-explicit invocation.
        own_pin,manifest_pin=t.source_closure()
        t.check_source_acceptance(t.decode(t.raw_ref(config['source_acceptance'])),own_pin,manifest_pin,t.transport_policy(config))
        source_refreshes.append({'source_pin':own_pin,'manifest_pin':manifest_pin,
            'source_acceptance_pin':{k:source_acceptance[k] for k in ('bytes','sha256')}})
        return own_pin,manifest_pin
    # The unchanged inspect path holds a real flock on only the synthetic lock.
    journal=e.journal_new(config['journal'])
    result=t.inspect(fixture_driver,rt,t.GetOnly(api),config,refresh_source,journal)
    natural=put(HERE/'NATURAL_INSPECT_RESULT.json',result)
    published=pathlib.Path(result['terminal_receipt']['path'])
    need(published==case/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json' and published.is_relative_to(checkout),'Only synthetic natural terminal name')
    raw=t.readonly(published)
    need(pin(raw)=={k:result['terminal_receipt'][k] for k in ('bytes','sha256')},'Natural inspect result binds full published bytes')
    proof=t.decode(raw);need(proof['source_gates_verified'] is True and proof['source_gate_checks']['refreshes_completed_before_record']>=2,'Executed source checks recorded')
    need(proof['candidate']!=proof['actual_MAIN_observed'] and proof['protected_body_paths_verified']==1,'Distinct C/R and truthful protected count')
    consumer_path=B/'completion_consumer.py'
    need(pin(consumer_path.read_bytes())==CONSUMER_PIN,'Exact real consumer source')
    consumer=module(consumer_path,'real_after218_consumer')
    accepted=consumer.completion_proof(raw,{k:result['terminal_receipt'][k] for k in ('bytes','sha256')})
    consumer_negatives=[]
    for key,bad in (('PR',218.0),('fully_completed_count',55.0),('fully_completed_count',54),('published_count',38),
                    ('source_gates_verified',False),('advance_to_next_PR_authorized_now',False),
                    ('current_head','95ba37055ebf1e7b4f9d76aa43816c9978c7bce8'),
                    ('existing_tracker_range',"'Math Puzzles'!A105:D105"),
                    ('CAS_target','7'*40),('CAS_or_completion_inferred_from_ancestry',True),
                    ('selected_postimage_paths_verified',0),('protected_body_paths_verified',65)):
        badraw=enc({**proof,key:bad});refused=False
        try:consumer.completion_proof(badraw,pin(badraw))
        except RuntimeError:refused=True
        need(refused,'Real after218 consumer mutation must refuse '+key)
        consumer_negatives.append({'key':key,'mutation':bad,'refused':True})
    stale_memberships=copy.deepcopy(proof);stale_memberships['fully_completed_eligible_PRs'].insert(-1,217)
    badraw=enc(stale_memberships);refused=False
    try:consumer.completion_proof(badraw,pin(badraw))
    except RuntimeError:refused=True
    need(refused,'Status-only skip cannot enter actual memberships')
    consumer_negatives.append({'key':'fully_completed_eligible_PRs','mutation':'insert217','refused':True})
    consumer_negative_result=put(HERE/'CONSUMER_NEGATIVE_RESULTS.json',{'scope':'OWNED_SYNTHETIC_ONLY','all_refused':True,'checks':consumer_negatives})
    consumer_result=put(HERE/'CONSUMER_ROUNDTRIP_RESULT.json',{'scope':'OWNED_SYNTHETIC_INSPECT_ROUNDTRIP_ONLY',
        'accepted_by_real_completion_proof':True,'consumer_source_pin':CONSUMER_PIN,'natural_inspect_result':natural,
        'published_terminal':result['terminal_receipt'],'candidate':accepted['candidate'],
        'actual_MAIN_observed':accepted['actual_MAIN_observed'],'actual_live_or_Root_authority':False})
    source_refresh_log=put(HERE/'EXECUTED_SOURCE_GATE_REFRESHES.json',{'scope':'OWNED_SYNTHETIC_ONLY',
        'terminal_source_callback_count':len(source_refreshes),'terminal_callbacks':source_refreshes,
        'runtime_refresh_count':rt.refresh_count,'source_callback':'Production source_closure + raw_ref + check_source_acceptance + transport_policy.',
        'runtime_callback':'Production nofollow readers/source_closure/matches/validate_ready_value over pinned synthetic prerequisite records.',
        'full_production_Seed_Runtime_or_actual_Root_review_claimed':False})
    # Source-gate tamper is rejected by the same actual pinned refresh callback.
    gatepath=pathlib.Path(source_acceptance['path']);gatebytes=gatepath.read_bytes()
    gatepath.chmod(0o644);gatepath.write_bytes(gatebytes+b' ');gatepath.chmod(0o444)
    refused=False
    try:refresh_source()
    except RuntimeError:refused=True
    need(refused,'Pinned source-gate mutation must refuse')
    gatepath.chmod(0o644);gatepath.write_bytes(gatebytes);gatepath.chmod(0o444)
    refresh_source()
    # Current file third state rejects through production local_states.
    view=checkout/h.VIEWS[0];viewraw=view.read_bytes();view.chmod(0o644);view.write_bytes(b'{}\n');view.chmod(0o444)
    refused=False
    try:q.local_states(rt,all_post=True)
    except RuntimeError:refused=True
    need(refused,'A third local state must refuse')
    view.chmod(0o644);view.write_bytes(viewraw);view.chmod(0o444)
    q.local_states(rt,all_post=True)
    need(t.readonly(published)==raw and stat.S_IMODE(published.stat().st_mode)==0o444,'Retained exact readonly published bytes')
    # Source01 and02 are not modified by this owned execution.
    need(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==SOURCE_MANIFEST_PIN,'Frozen02 manifest remains unchanged')
    for row in manifest['files']:need(pin((SOURCE/row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'Original02 payload remains unchanged')
    report={'schema':'pr218-owned-full-inspect-roundtrip-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'SYNTHETIC_INSPECT_PATH_NOT_ACTUAL_ROOT_TERMINAL_OR_NATIVE_AUTHORITY','preparation_percent':100,
        'harness_reuse_origin':{'bytes':30186,'sha256':'36cdd550f03d77a0be37642f5496902aef8a27780653fd57b0375133afde20e9'},
        'frozen_terminal_pin':TERMINAL_PIN,'frozen_source_manifest_pin':SOURCE_MANIFEST_PIN,
        'unchanged_full_inspect_executed':True,'production_terminal_constructor_and_exclusive_publisher_executed':True,
        'real_fixture_flock_not_original_project_lock':True,'published_terminal':result['terminal_receipt'],
        'natural_inspect_result':natural,'consumer_result':consumer_result,'consumer_negative_result':consumer_negative_result,'source_gate_refreshes':source_refresh_log,
        'source_gate_tamper_refused':True,'third_local_state_refused':True,
        'terminal_source_gate_refresh_count_in_inspect':len(source_refreshes)-1,'runtime_refresh_count':rt.refresh_count,
        'selected_native_body_paths':len(overlay),'protected_body_paths':1,'candidate':candidate,'tree':candidate_tree,
        'synthetic_descendant_R':descendant,'synthetic_descendant_root':descendant_tree,
        'native_observer_route_calls':len(api.reads),'raw_native_origin_scope':'Explicit synthetic local provider, never github.com network.',
        'real_q_functions_executed':['actual_cas','accepted_verifications','body_associations','protected','checked_pointer','local_states'],
        'fixture_dependencies':['RuntimeFixture replaces operational Seed/Runtime/native-identity/admission gates with pinned, explicitly synthetic prerequisites.',
          'Fixture verify_immutable and main_closure use real NativeTrees/SHA1/SHA256/native body origins/full scoped diffs and fixed PR metadata validator; real submitted original/prepared/merge histories are not replayed.',
          'CAS tool responses/same-live polls/preCAS reviews and readiness flags are synthetic records, not actual Root actions or reviews.',
          'No actual concurrent GET worker transport or full original context(config) entrypoint is executed; no operational Seed/Runtime/load_inputs gate claim.'],
        'network_Git_provider_ref_PR_original_lock_actual_global_five_effects':False,
        'new_55_39_actual_completion_or_219_intake_authority':False}
    return put(HERE/'ROUNDTRIP_REPORT.json',report)
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))

