"""PR212 actual-source adversary. All operational effects are owned fakes.

Compile frozen production files unchanged in a temporary checkout. Real process
and network dispatch are denied. Fixture transport/lock identity adapters and
scoped e.put/os.open failure-injection hooks are used. Full Seed/Runtime refresh
bodies remain unchanged and executable.
Synthetic Root-shaped objects are never operational authority.
"""
from pathlib import Path
import ast,base64,calendar,contextlib,copy,datetime,hashlib,io,itertools,json,os,signal,socket,subprocess,sys,tempfile,types
D=Path(__file__).absolute().parent
A=D.parent
P=A/'native_administrative_preparation_01'
MP={'bytes':2195,'sha256':'7a0e69c0d7b7a31d642a054f96124729c42b808c03e47aab6b371091796e66e7'}
SP={'bytes':43897,'sha256':'16e5e3a15cc4cf34554aabf0b094b34996064c1abb05c008e26b47b00bf18ce8'}
CHECKS=[]
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def need(ok,msg):
    if type(ok)is not bool or not ok:raise AssertionError(msg)
def yes(ok,label):need(ok,label);CHECKS.append({'test':label,'outcome':'PASS'})
def no(fn,label,reason=None):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,OSError)as e:
        if reason is not None:need(reason in str(e),'Wrong refusal reason for '+label+': '+str(e))
        CHECKS.append({'test':label,'outcome':'EXPECTED_REFUSAL','exception':type(e).__name__,'reason':str(e)[:250]})
    else:raise AssertionError('Unexpected acceptance: '+label)
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists()and not p.is_symlink():p.chmod(0o644)
    p.write_bytes(b);p.chmod(0o444)
def module(p):
    m=types.ModuleType('independent_fixture_'+p.stem);m.__file__=str(p)
    exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def tup(v):return None if v is None else dict(zip(['mode','type','sha'],v))
def deny(*a,**k):raise AssertionError('Real network/process operation forbidden')

class F:
    def __init__(self,root,extra=False):
        self.root=root;self.program=root/'draft_pr_publication_program_20260930';self.case=self.program/'audits/pr212_30005310';self.b=self.case/'native_administrative_preparation_01';self.b.mkdir(parents=True)
        sm=json.loads((P/'SOURCE_MANIFEST.json').read_bytes())
        for n in [r['path']for r in sm['files']]+['SOURCE_MANIFEST.json','SOURCE_EXTERNAL_SEAL.json']:write(self.b/n,(P/n).read_bytes())
        self.v=module(self.b/'administrative_checkpoint.py');self.h=module(self.b/'native212_model.py');self.e=module(self.b/'native212_primitives.py');self.c=self.h.core()
        h=self.h;self.objects={};self.blobs={};self.commits={};self.edges={};self.calls=[];self.posts=[];self.ref_hook=None;self.ref_reads=0;self.post_fail=None
        maps=json.loads((A/'native_custody_01/AUTHENTICATED_NATIVE_TREES.json').read_bytes())
        for oid,entries in maps.items():need(self.tree({n:tuple(v)for n,v in entries.items()})==oid,'fixture canonical original/current tree')
        self.head_queue=(A/'native_custody_01/_private_native/current/unsolved_math_prioritization/QUEUE.md').read_bytes()
        need(self.blob(self.head_queue)==h.CURRENT_QUEUE,'fixture actual current HEAD queue body')
        self.head_row=h.own_queue_row(self.head_queue)[0]
        localqueue=Path('/Users/alec/Documents/Math/unsolved_math_prioritization/QUEUE.md').read_bytes()
        self.main_row=h.own_queue_row(localqueue)[0]
        need(pin(self.main_row)=={'bytes':166,'sha256':'b192db8bf68c86e83dd5be05cd38bfd0f65ccad7b29c63a9c54f00bd66258ff3'},'Root-confirmed actual Main queued row')
        need(pin(self.head_row)==h.CURRENT_ROW and self.main_row!=self.head_row,'Main queued row distinct from HEAD already_solved row')
        self.foreign_row=b'| 999 | 99999999 / FOREIGN | audit | x | x | x | x | queued | 0/5 | x | x | x |\n'
        self.main_queue=b'# Independent synthetic Main QUEUE\n'+self.main_row+self.foreign_row
        self.pr=json.loads((A/'admin_status_confirmation_01/01.stdout.json').read_bytes())
        baseline=json.loads((self.b/'BASELINE_MEMBERSHIP.json').read_bytes())
        nativeprogress=enc({**h.baseline_facts(),**baseline,'dated_eligible_total':99,'active_PR':211})
        self.local_before={h.VIEWS[0]:b'{"local_case_percent":75}\n',h.VIEWS[1]:b'Independent fixture existing case log\n',h.VIEWS[2]:nativeprogress,h.VIEWS[3]:b'Existing program progress\n',h.VIEWS[4]:b'Existing native program history\nLocal extra audit history\n'}
        self.native_log=b'Existing native program history\n'
        post=enc({**h.phase_facts(),**baseline,'dated_eligible_total':99,'conditional_proposal_only':True,'completed':False,'active_publication_DOI':None,'active_tracker_range':None})
        self.overlay={h.VIEWS[0]:post,h.VIEWS[1]:self.local_before[h.VIEWS[1]]+b'Qualified administrative proposal\n'+h.phase_marker()+b'\n',h.VIEWS[2]:post,h.VIEWS[3]:b'Qualified administrative proposal\n'+h.phase_marker()+b'\n',h.VIEWS[4]:self.local_before[h.VIEWS[4]]+b'Qualified administrative proposal\n'+h.phase_marker()+b'\n'}
        evidence={}
        for role,name in h.ROOT_EVIDENCE_PATHS.items():
            raw=(A/name).read_bytes();need(pin(raw)==h.ROOT_EVIDENCE[role],'Actual Root evidence copy pin');write(self.case/name,raw);evidence[role]={'path':str(self.case/name),**pin(raw)};self.overlay[h.CASE+name]=raw
        prior=(A.parent/'pr211_5100063/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json').read_bytes();need(pin(prior)==h.PRIOR_TERMINAL_PIN,'Actual prior211 terminal copy');self.overlay[h.PRIOR_TERMINAL_PATH]=prior
        if extra:self.overlay[h.CASE+'EXTRA_AUTHORED_AUDIT.md']=b'Independent dynamic11th selected body\n'
        self.before={h.QUEUE:('100644','blob',self.blob(self.main_queue)),h.SHARED:('040000','tree','17906f1a6fe6b919752c0b68c4288ae300b526de'),h.VIEWS[2]:('100644','blob',self.blob(nativeprogress)),h.VIEWS[3]:('100644','blob',self.blob(self.local_before[h.VIEWS[3]])),h.VIEWS[4]:('100644','blob',self.blob(self.native_log)),h.OLD_CASE+'EXISTING_FOREIGN.md':('100644','blob',self.blob(b'old case foreign file\n')),'foreign/executable':('100755','blob',self.blob(b'executable\n')),'foreign/symlink':('120000','blob',self.blob(b'../target')),'foreign/gitlink':('160000','commit','9'*40),'foreign/empty':('040000','tree',self.tree({}))}
        self.parent_root=self.build(self.before);self.parent=self.commit(self.parent_root,[h.ANCHOR],b'Independent synthetic Main parent\n')
        self.after={**self.before,**{p:('100644','blob',self.blob(b))for p,b in self.overlay.items()}};self.target_root=self.build(self.after)
        self.pre={p:self.before.get(p)for p in self.overlay}
        files=[];local=[]
        for i,(p,raw)in enumerate(sorted(self.overlay.items())):
            n='_fixture_inputs/selected_'+str(i)+'.body';write(self.b/n,raw);files.append({'path':p,'source':n,**pin(raw),'git_blob':self.blob(raw),'preimage':tup(self.pre[p])})
        for i,p in enumerate(h.VIEWS):
            n='_fixture_inputs/local_'+str(i)+'.body';write(self.b/n,self.local_before[p]);write(root/p,self.local_before[p]);local.append({'path':p,'source':n,'preimage':pin(self.local_before[p])})
        self.logical={'schema':'pr212-conditional-administrative-logical-packet-v1','PR':212,'problem_id':'30005310','phase':'administrative100','facts':h.phase_facts(),'files':files,'total_files':len(files),'total_bytes':sum(map(len,self.overlay.values())),'local_views':local,'protected_queue':tup(self.before[h.QUEUE]),'protected_queue_row_pin':pin(self.main_row),'protected_nodes':{h.ATTEMPT:None,h.SHARED:tup(self.before[h.SHARED])},'current_PR_opaque_body_pin':pin(h.compact(self.pr['body']).encode()),'expected_new_directories':sorted(self.dirs(self.after)-self.dirs(self.before)),'expected_changed_paths':sorted(self.overlay),'carryforward':[{'path':h.PRIOR_TERMINAL_PATH,**h.PRIOR_TERMINAL_PIN}],'commit_author':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},'commit_committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com'},'commit_message':'Archive PR212 administrative untouched nonclaimed disposition\n','retired_candidates':[],'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,'writer_lock':h.WRITER_LOCK_REFERENCE,'evidence_references':evidence}
        self.mp,self.gp=self.logical_refs(self.logical,'positive')
        self.seed=self.v.Seed(self.mp,self.gp);self.h,self.e,self.c=self.seed.h,self.seed.e,self.seed.c
        h=self.h
        date='2026-10-17T23:00:00Z';identity={**self.logical['commit_author'],'date':date}
        self.admission={'schema':'pr212-administrative-parent-admission-v1','PR':212,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,'logical_manifest_pin':self.seed.manifest_pin,'logical_gate_pin':self.seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,'parent':self.parent,'parent_tree':self.parent_root,'created_UTC':date,'commit_author':identity,'commit_committer':identity,'commit_message':self.logical['commit_message'],'parents':[self.parent],'tree':self.target_root,'candidate':'0'*40,'candidate_journal':'ROOT_ADMIN212_CANDIDATE_INDEPENDENT'}
        self.request,self.target=h.commit_request({**self.logical,'commit_author':identity,'commit_committer':identity},self.target_root,[self.parent]);self.admission['candidate']=self.target
        self.commits[self.target]={'sha':self.target,'tree':{'sha':self.target_root},'parents':[{'sha':self.parent}],**{k:self.request[k]for k in ['author','committer','message']}};self.edges[self.target]=[self.parent]
        self.commits.update({h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':h.ORIGINAL_PARENT}]},h.CURRENT:{'sha':h.CURRENT,'tree':{'sha':h.CURRENT_TREE},'parents':[{'sha':h.ORIGINAL}]}})
        self.ar=self.record('admission.json',self.admission,annotate=False)
        self.ag={'schema':'pr212-root-administrative-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':212,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,'admission_pin':pin(enc(self.admission)),'logical_manifest_pin':self.seed.manifest_pin,'logical_gate_pin':self.seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,'parent_only_parameterization_reviewed':True,'one_use_two_immutable_POSTs_authorized':True,'no_ref_writer_or_PR_action_authority':True,'completed_and_published_lists_unchanged':True,'Root_full_source_read':True,'independent_source_review_accepted':True,'parent_only_admissions_without_new_peer_review_approved':True}
        self.gr=self.record('admission_gate.json',self.ag);self.rt=self.v.Runtime(self.seed,self.ar,self.gr)
        # Keep exact production logical lock policy. Translate only its inode
        # identity to this temporary checkout for genuine flock algorithm tests.
        self.lockpath=self.program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(self.lockpath,self.e.LOCK_BYTES);st=self.lockpath.stat();self.fixture_lock={**h.WRITER_LOCK_REFERENCE,'device':st.st_dev,'inode':st.st_ino}
        self.original_lock=self.e.WriterLock
        def fixture_lock(expected):
            need(h.exact(expected,h.WRITER_LOCK_REFERENCE),'unchanged production writer-lock binding before fixture substitution')
            return self.original_lock(self.fixture_lock)
        self.e.WriterLock=fixture_lock
        self.e.run_bounded=self.transport
        self.ref=self.parent
    def dirs(self,leaves):
        out=set()
        for p,t in leaves.items():
            ps=p.split('/')
            for i in range(1,len(ps)):out.add('/'.join(ps[:i]))
            if t[:2]==('040000','tree'):out.add(p)
        return out
    def blob(self,b):
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();self.blobs[oid]=b;return oid
    def tree(self,rows):
        rows=sorted(rows.items(),key=lambda r:r[0].encode()+(b'/'if r[1][0]=='040000'else b''));raw=b''.join((v[0].lstrip('0')+' '+n).encode()+b'\0'+bytes.fromhex(v[2])for n,v in rows);oid=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest();self.objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':v[0],'type':v[1],'sha':v[2]}for n,v in rows]};return oid
    def build(self,leaves):
        trie={}
        for p,t in leaves.items():
            node=trie
            for n in p.split('/')[:-1]:node=node.setdefault(n,{})
            node[p.split('/')[-1]]=t
        def walk(n):return self.tree({k:('040000','tree',walk(v))if type(v)is dict else v for k,v in n.items()})
        return walk(trie)
    def commit(self,root,parents,msg=b'Independent synthetic foreign append\n'):
        sec=calendar.timegm(datetime.datetime(2026,10,17,23,1).timetuple());ident='Alec Kriebel <me@aleckriebel.com> '+str(sec)+' +0000';raw=('tree '+root+'\n'+''.join('parent '+p+'\n'for p in parents)+'author '+ident+'\ncommitter '+ident+'\n\n').encode()+msg;oid=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest();self.commits[oid]={'sha':oid,'tree':{'sha':root},'parents':[{'sha':p}for p in parents],'message':msg.decode(),'author':{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-17T23:01:00Z'},'committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-17T23:01:00Z'}};self.edges[oid]=parents;return oid
    def ancestor(self,a,b):
        todo=[b];seen=set()
        while todo:
            x=todo.pop()
            if x==a:return True
            if x not in seen:seen.add(x);todo.extend(self.edges.get(x,[]))
        return False
    def observer(self,method,path,body=None):
        need(method=='GET'and body is None,'native fake GET only');self.calls.append(path)
        if path=='git/ref/heads/main':
            self.ref_reads+=1
            return {'ref':'refs/heads/main','object':{'type':'commit','sha':self.ref_hook(self.ref_reads)if self.ref_hook else self.ref}}
        if path=='pulls/212':return copy.deepcopy(self.pr)
        if path.startswith('compare/'):
            a,b=path.split('/')[1].split('...');ok=self.ancestor(a,b);return {'status':'ahead'if ok and a!=b else 'identical'if a==b else'diverged','merge_base_commit':{'sha':a if ok else'0'*40}}
        oid=path.rsplit('/',1)[1]
        if path.startswith('git/trees/'):return copy.deepcopy(self.objects[oid])
        if path.startswith('git/commits/'):return copy.deepcopy(self.commits[oid])
        if path.startswith('git/blobs/'):
            b=self.blobs[oid];return {'sha':oid,'size':len(b),'encoding':'base64','content':base64.b64encode(b).decode()}
        raise AssertionError('Unexpected fake native route')
    def transport(self,argv,request):
        need(argv[:5]==[self.e.GH,'api','--hostname','github.com','--method']and argv[6].startswith('repos/AlecKriebel/Math/'),'fixed explicit transport host/repository')
        method,path=argv[5],argv[6][len('repos/AlecKriebel/Math/'):]
        if method=='GET':value=self.observer(method,path)
        else:
            need(method=='POST'and path in ['git/trees','git/commits'],'immutable fake POST route only');obj=self.h.decode(request);self.posts.append((path,obj))
            if self.post_fail==path:raise RuntimeError('Synthetic uncertain immutable dispatch')
            if path=='git/trees':
                need(obj=={'base_tree':self.parent_root,'tree':[{'path':p,'mode':'100644','type':'blob','content':b.decode()}for p,b in sorted(self.overlay.items())]},'fake exact selected tree request');value={'sha':self.target_root}
            else:need(self.h.exact(obj,self.request),'fake exact neutral oneparent commit request');value={'sha':self.target}
        return types.SimpleNamespace(returncode=0,stdout=enc(value),stderr=b'')
    def record(self,name,obj,annotate=True):
        if annotate:obj={**obj,'synthetic_fixture_only_not_authority':True}
        p=self.case/'_synthetic_authority'/name;raw=enc(obj);write(p,raw);return {'path':str(p),**pin(raw)}
    def logical_refs(self,m,label):
        raw=enc(m);p=self.b/'_fixture_inputs'/('logical_'+label+'.json');write(p,raw);mr={'path':str(p),**pin(raw)}
        audits=[self.record('audit_'+str(i)+'.json',{'synthetic_audit':i})for i in [1,2]]
        g={'schema':'pr212-root-administrative-logical-packet-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':212,'accepted':True,'manifest_pin':pin(raw),'source_manifest_pin':MP,'protocol_pin':SP,'primitive_pin':self.v.PRIMITIVE_PIN,'facts':self.h.phase_facts(),'public_selection_reviewed':True,'administrative_disposition_review_accepted':True,'no_PR_or_publication_actions':True,'all53_37_memberships_unchanged':True,'QUEUE_policy':self.h.QUEUE_POLICY,'Root_full_source_read':True,'independent_source_adversarial_review_accepted':True,'independent_exact_packet_review_accepted':True,'audit_receipts':audits}
        return mr,self.record('logical_gate_'+label+'.json',g)
    def api(self,label):return self.e.API(self.h,self.e.journal_new('ROOT_ADMIN212_READ_'+label),mutate=False)
    def descendant(self,queue=None,changes=None,parents=None,label=b'foreign'):
        leaves={**self.after,**(changes or{})}
        if queue is not None:leaves[self.h.QUEUE]=('100644','blob',self.blob(queue))
        root=self.build(leaves);return self.commit(root,parents or[self.target],b'Independent descendant '+label+b'\n')
    def reset(self,bits):
        for p,b in zip(self.h.VIEWS,bits):write(self.root/p,self.overlay[p]if b else self.local_before[p])
    def cas_records(self,reports):
        rt=self.rt;v=self.v;h=self.h
        common={'PR':212,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,'admission_pin':rt.admission_pin,'logical_manifest_pin':self.seed.manifest_pin,'logical_gate_pin':self.seed.logical_gate_pin,'candidate':self.target,'tree':self.target_root,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY}
        self.pre_ref=self.record('preCAS.json',{**common,'schema':'pr212-root-administrative-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'immutable_candidate_verification_accepted':True,'independent_GET_candidate_verification_accepted':True,'verification_reports':[self.record('proof_'+str(i)+'.json',o)for i,o in enumerate(reports)]})
        self.ready=self.record('ready.json',{'schema':'pr212-administrative-locked-CAS-ready-v1','evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS','protocol_pin':self.seed.source_pin,'admission_pin':rt.admission_pin,'parent':self.parent,'candidate':self.target,'original_stable_lock_held':True,'guard_pid':1234})
        self.req_obj={'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main','expected_sha':self.parent,'sha':self.target,'force':False};req=self.record('request.json',self.req_obj);response=self.record('response.json',{'isError':False,'structuredContent':{'success':True}})
        readback=self.record('readback.json',{'ref':'refs/heads/main','object':{'type':'commit','sha':self.ref}});receipt=self.record('readback_receipt.json',{'method':'GET','path':'git/ref/heads/main','exit':0,'stdout_pin':{k:readback[k]for k in ['bytes','sha256']}})
        poll=self.record('poll.json',{'session_id':123456,'exit_code':None,'output':''})
        self.live_obj={'schema':'pr212-root-postCAS-same-live-guard-confirmation-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'protocol_pin':self.seed.source_pin,'admission_pin':rt.admission_pin,'actual_lock_guard_ready_pin':{k:self.ready[k]for k in ['bytes','sha256']},'actual_tool_response_pin':{k:response[k]for k in ['bytes','sha256']},'actual_readback_response_pin':{k:readback[k]for k in ['bytes','sha256']},'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,'original_lock_continuity_from_linear_held_source_and_same_live_session':True,'guard_pid':1234,'session_id':123456,'actual_same_session_poll_response':poll}
        live=self.record('live.json',self.live_obj)
        self.cas_obj={**common,'schema':'pr212-root-administrative-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math','facts':h.phase_facts(),'parent':self.parent,'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'actual_MAIN_after_CAS':self.ref,'preCAS_acceptance':self.pre_ref,'actual_lock_guard_ready':self.ready,'actual_tool_request':req,'actual_tool_response':response,'actual_readback_response':readback,'actual_readback_receipt':receipt,'post_CAS_same_live_guard_confirmation':live}
        self.cas=self.record('actual_CAS.json',self.cas_obj);return self.cas

def repinned_packet_tests(f):
    h,v=f.h,f.v
    def bad(change,label):
        m=copy.deepcopy(f.logical);change(m);mr,gr=f.logical_refs(m,'bad_'+label)
        no(lambda:v.Seed(mr,gr),'repinned_logical_'+label)
    for field,value in [('fully_completed_count',54),('published_count',38),('last_completed_PR',212),('completed_eligible_workflow',True),('publication_ready',True),('advance_to_next_PR_authorized_now',True),('goal_complete',True),('fully_completed_count',53.0)]:
        bad(lambda m,k=field,x=value:m['facts'].update({k:x}),field+'_'+str(value))
    bad(lambda m:m.update(QUEUE_policy='ANCESTRY_ONLY'),'weaken_QUEUE_policy')
    bad(lambda m:m.update(body_proof_policy='SOURCE_BODY_EQUALS_NATIVE'),'source_impersonates_GET')
    cases=json.loads((D/'CONCRETE_COMMIT_AND_QUEUE_CASES_01.json').read_bytes())
    for i,row in enumerate(cases['autoclosing_commit_negatives']):
        bad(lambda m,x=row['message']:m.update(commit_message=x),'auto_close_message_'+str(i))
        no(lambda x=row['message']:h.commit_request({**f.rt.m,'commit_message':x},f.target_root,[f.parent]),'canonical_commit_auto_close_'+str(i))
        no(lambda x=row['message']:v.checked_admission(f.seed,{**f.admission,'commit_message':x}),'typed_admission_auto_close_'+str(i))
    for parents in [[h.ORIGINAL],[h.CURRENT],[f.parent,h.CURRENT],[f.parent,h.ORIGINAL]]:
        no(lambda parents=parents:h.commit_request(f.rt.m,f.target_root,parents),'archive_cannot_include_PR_snapshot_parent_'+str(len(CHECKS)))
    for field,value in [('accepted',1),('one_use_two_immutable_POSTs_authorized',False),('completed_and_published_lists_unchanged',False),('independent_source_review_accepted',False)]:
        ref=f.record('bad_admission_gate_'+field+'.json',{**f.ag,field:value})
        no(lambda ref=ref:v.Runtime(f.seed,f.ar,ref),'actual_Runtime_gate_'+field)
    # Repin the changed selected JSON body as well as the outer logical gate.
    for field,value in [('completed',True),('active_publication_DOI','10.0/notours'),('active_tracker_range','A1:D1'),('current_PR',211)]:
        m=copy.deepcopy(f.logical);r=next(x for x in m['files']if x['path']==h.VIEWS[0]);body=h.decode(f.overlay[h.VIEWS[0]]);body[field]=value;raw=enc(body);n='_fixture_inputs/bad_post_'+field+'.body';write(f.b/n,raw);m['total_bytes']+=len(raw)-r['bytes'];r.update(source=n,**pin(raw),git_blob=h.native('blob',raw));mr,gr=f.logical_refs(m,'bad_post_'+field)
        no(lambda mr=mr,gr=gr:v.Seed(mr,gr),'repinned_selected_post_'+field)

def origin_tests(f):
    h=f.h;oid=f.blob(b'Independently authenticated synthetic native bytes\n');route='git/blobs/'+oid
    no(lambda:h.NativeBodyProofs().get(f.observer,oid),'raw_body_without_actual_API_origin_refused')
    a=f.api('ORIGIN_POSITIVE');n=len(f.calls);a('GET',route);p=h.NativeBodyProofs();yes(p.get(a,oid)==f.blobs[oid]and len(f.calls)==n+1,'actual_API_precache_origin_retained_without_fabricated_GET')
    b=f.api('ORIGIN_SECOND');n=len(f.calls);yes(h.NativeBodyProofs().get(b,oid)==f.blobs[oid]and len(f.calls)==n+1,'new_API_instance_performs_own_actual_fake_transport_GET')
    for field,value in [('sha','0'*40),('size',True),('encoding','utf8'),('content',base64.b64encode(b'other').decode())]:
        api=f.api('ORIGIN_BAD_'+field.upper());api('GET',route);origin=api.actual_GET_origins[route];response=Path(origin['raw_response']['path']);raw=h.decode(response.read_bytes());raw[field]=value;rr=enc(raw);write(response,rr);origin['raw_response']={'path':str(response),**pin(rr)};receipt=Path(origin['receipt']);rec=h.decode(receipt.read_bytes());rec['raw_stdout']=origin['raw_response'];write(receipt,enc(rec));origin['receipt_pin']=pin(enc(rec))
        no(lambda api=api:h.NativeBodyProofs().get(api,oid),'repinned_inner_raw_native_'+field)
    for field,value in [('method','POST'),('path','git/ref/heads/main'),('exit',False)]:
        api=f.api('ORIGIN_BAD_RECEIPT_'+field.upper());api('GET',route);origin=api.actual_GET_origins[route];receipt=Path(origin['receipt']);rec=h.decode(receipt.read_bytes());rec[field]=value;write(receipt,enc(rec));origin['receipt_pin']=pin(enc(rec));no(lambda api=api:h.NativeBodyProofs().get(api,oid),'repinned_receipt_'+field)
    api=f.api('ORIGIN_STDERR');api('GET',route);write(Path(api.actual_GET_origins[route]['raw_stderr']['path']),b'changed')
    no(lambda:h.NativeBodyProofs().get(api,oid),'raw_stderr_file_pin_changed')
    api=f.api('ORIGIN_MISSING');api('GET',route);Path(api.actual_GET_origins[route]['raw_response']['path']).unlink()
    no(lambda:h.NativeBodyProofs().get(api,oid),'raw_response_missing_despite_hash_receipt')

def queue_and_scope_tests(f):
    h,v,rt=f.h,f.v,f.rt
    f.ref='f'*40;api=f.api('IMMUTABLE_ONE');proof=v.verify_immutable(rt,api)
    yes(proof['selected_count']==len(f.overlay)and proof['changed_leaves']==sorted(f.overlay)and not proof['deleted_directories'],'full_immutable_dynamic_selected_scope_'+str(len(f.overlay)))
    yes('git/ref/heads/main'not in f.calls and proof['mutable_Main_observed_or_spoofed']is False,'immutable_proof_no_mutable_Main_read_or_spoof')
    yes(proof['Main_QUEUE_observation']['own_row_pin']==pin(f.main_row)and proof['Main_QUEUE_observation']['candidate_QUEUE_oid']!=h.CURRENT_QUEUE,'candidate_preserves_Main_queued_not_HEAD_already_solved')
    other=f.api('IMMUTABLE_TWO');second=v.verify_immutable(rt,other)
    yes(other is not api and all(r['actual_native_GET_origin']['raw_response']['path']!=second['selected_files'][p]['actual_native_GET_origin']['raw_response']['path']for p,r in proof['selected_files'].items()),'two_separate_API_complete_selected_GET_origins')
    foreign=f.main_queue.replace(f.foreign_row,f.foreign_row.replace(b'queued',b'already_solved'))
    child=f.descendant(foreign,{'foreign/append':('100644','blob',f.blob(b'other writer'))},label=b'preserving')
    f.ref=child;observation=v.main_closure(rt,f.api('DESCENDANT_POSITIVE'))
    q=observation['Main_QUEUE_observation']
    yes(observation['actual_MAIN_observed']==child and observation['CAS_target']==f.target and q['observed_QUEUE_oid']!=q['candidate_QUEUE_oid']and q['own_row_pin']==pin(f.main_row),'foreign_QUEUE_descendant_allowed_distinct_C_R_QUEUE_OIDs')
    yes(observation['fresh_corrected_PR_status_observation']['current_status']=='already_solved'and h.own_queue_row(foreign)[1][8].strip()==b'queued','Main_queued_and_current_PR_already_solved_are_separate_roles')
    sibling=f.descendant(foreign,parents=[f.parent],label=b'sibling');f.ref=sibling
    no(lambda:v.main_closure(rt,f.api('SIBLING')),'same_owned_bytes_sibling_without_C_ancestry')
    cases=[('canonical_duplicate',f.main_queue+f.main_row),('HEAD_row_transplant',f.main_queue.replace(f.main_row,f.head_row)),('missing_own',f.main_queue.replace(f.main_row,b''))]
    for i,prefix in enumerate([b' ',b'  ',b'   ',b'\t']):cases.append(('indented_duplicate_'+str(i),f.main_queue+prefix+f.main_row));cases.append(('indented_single_'+str(i),f.main_queue.replace(f.main_row,prefix+f.main_row)))
    code=b'30005310 / OWR-11695865-009'
    for name,repl in [('backtick',b'`'+code+b'`'),('linked',b'['+code+b'](https://example.invalid/)'),('wrongcode',b'30005310 / WRONG'),('missing_initialpipe',None),('missing_finalpipe',None)]:
        row=f.main_row.replace(code,repl)if repl is not None else f.main_row[1:]if name=='missing_initialpipe'else f.main_row[:-2]+b'\n'
        cases.append((name+'_duplicate',f.main_queue+row));cases.append((name+'_single',f.main_queue.replace(f.main_row,row)))
    for i,(name,body)in enumerate(cases):
        f.ref=f.descendant(body,label=name.encode());no(lambda i=i:v.main_closure(rt,f.api('BAD_QUEUE_'+str(i))),'full_native_descendant_QUEUE_'+name)
    f.ref=f.descendant(foreign,{h.QUEUE:('100755','blob',f.blob(foreign))},label=b'queue_mode')
    # descendant() reassignsqueue only when supplied; avoid overriding mode.
    f.ref=f.descendant(None,{h.QUEUE:('100755','blob',f.blob(foreign))},label=b'queue_executable')
    no(lambda:v.main_closure(rt,f.api('QUEUE_MODE')),'native_QUEUE_mode_change_refused')
    for i,p in enumerate(f.overlay):
        f.ref=f.descendant(foreign,{p:('100755','blob',h.native('blob',f.overlay[p]))},label=('owned'+str(i)).encode());no(lambda i=i:v.main_closure(rt,f.api('OWNED_'+str(i))),'ancestral_selected_tuple_change_'+str(i))
    for name,p,t in [('attempt_introduced',h.ATTEMPT,('040000','tree',f.tree({}))),('oldaudit_changed',h.SHARED,('040000','tree',f.tree({})))]:
        f.ref=f.descendant(foreign,{p:t},label=name.encode());no(lambda name=name:v.main_closure(rt,f.api(name.upper())),'protected_'+name)
    f.ref=child;saved=f.pr['merged'];f.pr['merged']=True;no(lambda:v.main_closure(rt,f.api('PR_MERGED')),'current_open_draft_unexpected_merge');f.pr['merged']=saved
    f.ref_reads=0;f.ref_hook=lambda n:child if n==1 else sibling
    no(lambda:v.main_closure(rt,f.api('MOVING_REF')),'ref_moves_during_bound_R_and_QUEUE_proof');f.ref_hook=None
    # WholeCQUEUE remains exact even when a changed body preserves own row.
    wrongroot=f.build({**f.after,h.QUEUE:('100644','blob',f.blob(foreign))})
    bad=copy.deepcopy(f.admission);bad['tree']=wrongroot;mm={**rt.m};req,bad['candidate']=h.commit_request(mm,wrongroot,[f.parent]);f.commits[bad['candidate']]={'sha':bad['candidate'],'tree':{'sha':wrongroot},'parents':[{'sha':f.parent}],**{k:req[k]for k in ['author','committer','message']}}
    # A direct explicitly synthetic context tests the actual immutable verifier
    # against an independently canonical but unselected wholeQUEUE mutation.
    badrt=types.SimpleNamespace(**rt.__dict__);badrt.admission=bad
    no(lambda:v.verify_immutable(badrt,f.api('C_WHOLE_QUEUE_CHANGED')),'candidate_C_cannot_change_even_foreign_QUEUE_rows')
    f.ref=child;return proof,second,child,sibling

def local_and_effect_tests(f,reports,child,sibling):
    h,v,e,rt=f.h,f.v,f.e,f.rt
    for bits in itertools.product([False,True],repeat=5):f.reset(bits);v.local_states(rt,resume=True);yes(True,'local_32_mixed_'+''.join('1'if x else'0'for x in bits))
    for slot in range(5):
        for bits in itertools.product([False,True],repeat=4):
            mask=list(bits);mask.insert(slot,False);f.reset(mask);write(f.root/h.VIEWS[slot],b'third state');no(lambda:v.local_states(rt,resume=True),'local_80_third_'+str(slot)+'_'+''.join('1'if x else'0'for x in bits))
    f.reset([False]*5);f.ref=f.parent
    result=v.candidate(rt);yes(len(f.posts)==2 and result['candidate']==f.target,'actual_candidate_driver_exact_two_fake_POSTs_full_new_API_proof')
    before=len(f.posts);alter={**f.admission,'candidate_journal':'ROOT_ADMIN212_CANDIDATE_RENAMED'};ar=f.record('renamed_admission.json',alter,False);gr=f.record('renamed_gate.json',{**f.ag,'admission_pin':{k:ar[k]for k in ['bytes','sha256']}});rr=v.Runtime(f.seed,ar,gr)
    no(lambda:v.candidate(rr),'canonical_candidate_same_OID_fresh_admission_journal_no_redispatch');yes(len(f.posts)==before,'same_candidate_zero_additional_dispatches')
    f.ref=child;cas=f.cas_records(reports);api=f.api('ACTUAL_CAS_PARSE');v.actual_cas(rt,cas,api);yes(True,'new_admin_actual_CAS_parser_distinct_preserving_R_fixture')
    no(lambda:v.actual_cas(rt,None,api),'ancestry_or_equal_ref_cannot_replace_actual_CAS')
    for k,x in [('unknown_outcome',True),('actual_Root_MCP_CAS_performed',False),('original_lock_held_across_actual_Root_CAS',False),('post_CAS_same_live_guard_confirmation',None)]:
        bad=f.record('bad_cas_'+k+'.json',{**f.cas_obj,k:x});no(lambda bad=bad:v.actual_cas(rt,bad,api),'actual_CAS_provenance_'+k)
    req=f.record('bad_force_request.json',{**f.req_obj,'force':True});bad=f.record('bad_force_CAS.json',{**f.cas_obj,'actual_tool_request':req});no(lambda:v.actual_cas(rt,bad,api),'actual_external_CAS_force_true_refused')
    poll=f.record('exited_poll.json',{'session_id':123456,'exit_code':0,'output':''});live=f.record('exited_live.json',{**f.live_obj,'actual_same_session_poll_response':poll});bad=f.record('exited_cas.json',{**f.cas_obj,'post_CAS_same_live_guard_confirmation':live});no(lambda:v.actual_cas(rt,bad,api),'ready_file_with_exited_session_not_continuity')
    pointer=f.b/'ROOT_ACTUAL_ADMINISTRATIVE_POINTER.json';oldput=e.put;fired=[False]
    # Full real Runtime.refresh, not a no-op: alter its pinned admission-gate
    # bytes immediately after the first install's receipt. Next guard refuses.
    gatepath=Path(f.gr['path']);gateraw=gatepath.read_bytes()
    def interrupt_put(directory,name,value):
        oldput(directory,name,value)
        if name=='VIEW_0.json'and not fired[0]:fired[0]=True;write(gatepath,gateraw+b' ')
    e.put=interrupt_put;f.reset([False]*5)
    try:no(lambda:v.sync(rt,f.api('SYNC_INTERRUPTED_API'),e.journal_new('ROOT_ADMIN212_SYNC_INPUT_INTERRUPTED'),cas),'full_Runtime_changed_admission_gate_stops_next_effect')
    finally:e.put=oldput;write(gatepath,gateraw)
    yes(fired[0]and not pointer.exists()and[(f.root/p).read_bytes()==f.overlay[p]for p in h.VIEWS]==[True,False,False,False,False],'qualified_onepost_fourpre_no_pointer_after_real_input_guard')
    inode=(f.root/h.VIEWS[0]).stat().st_ino;receipt=v.sync(rt,f.api('SYNC_RESUMED_API'),e.journal_new('ROOT_ADMIN212_SYNC_INPUT_RESUMED'),cas)
    yes((f.root/h.VIEWS[0]).stat().st_ino==inode and receipt['all_five_local_postimages_verified'],'full_Runtime_mixed_resume_skips_existing_post_inode')
    yes(receipt['facts']['fully_completed_count']==53 and receipt['facts']['published_count']==37 and receipt['facts']['advance_to_next_PR_authorized_now']is False and receipt['external_Root_terminal_acceptance_inferred']is False,'admin_sync_never_count54_publish_or_grant213')
    v.checked_pointer(rt,cas);v.local_states(rt,all_post=True);yes(True,'new_admin_pointer_exact_receipt_allfive_and_R_body')
    pointer.unlink();f.reset([False]*5);f.ref=child
    # Exact per-effect failure at the temp/install boundary using real Runtime.
    original_open=os.open;fired=[False];j=e.journal_new('ROOT_ADMIN212_SYNC_TEMP_BOUNDARY')
    def opened(path,*a,**k):
        fd=original_open(path,*a,**k)
        if isinstance(path,str)and path.startswith('.pr212-administrative-')and not fired[0]:fired[0]=True;write(gatepath,gateraw+b' ')
        return fd
    os.open=opened
    try:no(lambda:v.sync(rt,f.api('TEMP_BOUNDARY_API'),j,cas),'full_Runtime_input_guard_after_temp_before_install')
    finally:os.open=original_open;write(gatepath,gateraw)
    yes(fired[0]and all((f.root/p).read_bytes()==f.local_before[p]for p in h.VIEWS)and not pointer.exists(),'guarded_temp_never_installs_wrong_authority')
    # Allfive local posts cannot rescue a bad native state before final pointer.
    for boundary in ['VIEW_4.json','ACTUAL_FIVE_SYNC.json']:
        f.reset([False]*5);f.ref=child;j=e.journal_new('ROOT_ADMIN212_SYNC_BAD_FINAL_'+('VIEW'if boundary.startswith('VIEW')else'RECEIPT'))
        def badput(directory,name,value):
            oldput(directory,name,value)
            if name==boundary:f.ref=sibling
        e.put=badput
        try:no(lambda:v.sync(rt,f.api('BAD_FINAL_'+str(len(CHECKS))),j,cas),'bad_native_after_'+boundary+'_no_promotion')
        finally:e.put=oldput;f.ref=child
        yes(not pointer.exists()and all((f.root/p).read_bytes()==f.overlay[p]for p in h.VIEWS),'allfive_local_still_no_pointer_'+boundary)
    f.reset([True,False,True,True,True]);no(lambda:v.local_states(rt,all_post=True),'terminal_mixed_prepost_refused')
    with f.original_lock(f.fixture_lock)as lock:
        saved=lock.pid;lock.pid=-1;no(lock.check,'same_generic_lock_PID_guard_new_context');lock.pid=saved
    oldinode=f.fixture_lock['inode'];new=f.lockpath.with_name('replacement');write(new,e.LOCK_BYTES);os.replace(new,f.lockpath);no(lambda:f.original_lock(f.fixture_lock).__enter__(),'same_payload_replaced_fixture_inode_refused')
    f.fixture_lock['inode']=f.lockpath.stat().st_ino

def run():
    need(pin((P/'SOURCE_MANIFEST.json').read_bytes())==MP and pin((P/'administrative_checkpoint.py').read_bytes())==SP,'Root exact frozen source pins')
    sm=json.loads((P/'SOURCE_MANIFEST.json').read_bytes())
    for r in sm['files']:yes(pin((P/r['path']).read_bytes())=={k:r[k]for k in ['bytes','sha256']},'frozen_source_'+r['path'])
    socket.socket=deny;socket.create_connection=deny;subprocess.Popen=deny
    with tempfile.TemporaryDirectory(prefix='_synthetic_independent_',dir=D)as tmp:
        f=F(Path(tmp)/'checkout');yes(len(f.overlay)==10,'independent_small_dynamic_packet10_not192or202')
        repinned_packet_tests(f);origin_tests(f);p1,p2,c,s=queue_and_scope_tests(f);local_and_effect_tests(f,[p1,p2],c,s)
    with tempfile.TemporaryDirectory(prefix='_synthetic_independent_extra_',dir=D)as tmp:
        f=F(Path(tmp)/'checkout',extra=True);f.ref='f'*40;proof=f.v.verify_immutable(f.rt,f.api('DYNAMIC_ELEVEN'))
        yes(proof['selected_count']==11 and len(proof['changed_leaves'])==11,'second_dynamic_scope11_actual_full_verifier')
    return {'schema':'pr212-independent-actual-source-adversarial-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_manifest_pin':MP,'protocol_pin':SP,'checks':CHECKS,'check_count':len(CHECKS),'production_source_or_packet_gate_or_admission_CAS_terminal_created':False,'production_CLI_network_Git_original_lock_currentfive_PR_provider_or_otherchat_effects':False,'unchanged_production_source_compiled_in_temporary_fixture':True,'actual_Seed_Runtime_refresh_API_origin_and_candidate_sync_paths_exercised':True,'fixture_adapters':['executor_transport','lock_inode_identity'],'fixture_fault_injection_hooks':['e.put','os.open'],'full_Seed_Runtime_refresh_bodies_unmodified':True,'temporary_synthetic_Root_records_not_authority':True}
if __name__=='__main__':
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Python -E -S -B -P required')
    print(json.dumps(run(),sort_keys=True,indent=2))
