"""Bounded pure lifecycle guards; never invoke a real phase/backend/API."""
from pathlib import Path
import ast,copy,hashlib,json,os,stat,sys,tempfile,types
D=Path(__file__).absolute().parent
modules={};sources={};results=[]
for name in ('support206','ready206','lifecycle206','make_native206'):
    path=D/(name+'.py');raw=path.read_bytes();module=types.ModuleType('prepared_'+name);module.__file__=str(path)
    exec(compile(raw,str(path),'exec'),module.__dict__);modules[name]=module;sources[name+'.py']={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
S,R,L,N=(modules[name] for name in ('support206','ready206','lifecycle206','make_native206'))
N.configure(S);R.configure(S);L.configure(S,R,N)


def need(ok,message):
    if not ok:raise RuntimeError(message)
def same(a,b):need(a==b,'Expected equality')
def check(name,fn):fn();results.append({'name':name,'pass':True})
def reject(name,fn):
    def run():
        try:fn()
        except (RuntimeError,ValueError,KeyError,TypeError,FileNotFoundError,OSError):return
        raise RuntimeError('Expected rejection '+name)
    check(name,run)
def change(value,**kw):r=copy.deepcopy(value);r.update(kw);return r


check('No default authority/backend',lambda:same((S._authority_pin,S._backend),(None,None)))
reject('Missing future exact Root source adoption',S.authority)
reject('Production runtime refused without future authority',S.runtime)
check('Exactly four configured phase callbacks',lambda:same(set(S._drivers),set(S.PHASES)))
check('Explicit ordinary and optimized control mode',lambda:same(sys.flags.optimize in (0,1),True))
for filename in sources:
    tree=ast.parse((D/filename).read_bytes())
    for node in ast.walk(tree):
        if isinstance(node,ast.ImportFrom):need(node.module=='pathlib','Unexpected import')
        if isinstance(node,ast.Import):need(all(n.name in {'base64','copy','datetime','fcntl','hashlib','json','os','re','stat','sys','tempfile'} for n in node.names),'Unexpected project import')
    check('Only fixed stdlib imports '+filename,lambda:same(True,True))
for bad in ('../escape','/root','a//b','a/./b','a/../b','a\\b','a\0b',''):
    reject('Unsafe path '+repr(bad),lambda bad=bad:S.rel(bad))
for bad in ('','../gen','Upper','a-b','a'*50):reject('Unsafe generation '+repr(bad),lambda bad=bad:S.generation(bad))
reject('Boolean byte length rejected',lambda:S.bytepin({'bytes':True,'sha256':'0'*64}))
reject('Duplicate JSON key rejected',lambda:S.decode(b'{"x":1,"x":2}'))
reject('NaN JSON rejected',lambda:S.decode(b'{"x":NaN}'))
reject('Oversized selected map rejected',lambda:S.digest({str(i):S.bpin(b'x') for i in range(S.MAX_SELECTED+1)}))
calls=[];fake_api=types.SimpleNamespace(api=lambda *a,**k:calls.append((a,k)))
for path,method in [('git/refs/heads/main','PATCH'),('pulls/206','POST'),('users/private','GET')]:reject('Forbidden endpoint '+path,lambda path=path,method=method:S.api(fake_api,path,method,{}))
check('Forbidden endpoints never reach injected API',lambda:same(calls,[]))

# Existing actual evidence is read only. No actual phase/backend is invoked.
baseline=S.baseline_custody();custody,old=S.originals();q,base,head=S.queue_rows();fixed=S.fixed_gates()
check('Actual custody4416 map/digest',lambda:same((len(baseline['selected_files']),S.digest(baseline['selected_files'])),(4416,S.BASE_DIGEST)))
check('Actual original21/55033 archive',lambda:same((len(old),sum(map(len,old.values()))),(21,55033)))
check('BASE123 versus original HEAD511',lambda:same((S.pin(base),S.pin(head)),(S.BASE_ROW,S.HEAD_ROW)))
check('Fixed actual four Root gate pins',lambda:same(set(fixed),set(S.FIXED_GATES)))
check('Correct historical row identifier/date, no invented row count',lambda:same((S.SOURCE_FACTS['RGK_row_identifier'],S.SOURCE_FACTS['RGK_row_date'],S.SOURCE_FACTS['RGK_row_date_meaning'],'historical_target_row' in S.SOURCE_FACTS,'historical_table_entries' in S.SOURCE_FACTS),('k903,a','10/20','October2020',False,False)))
check('Every integer repetition explicitly qualified',lambda:same(('every integer r>=1' in S.SOURCE_FACTS['repetition_multiplicity'],'every integer r>=1' in S.CLAIM),(True,True)))
check('Correct Chavez and exact Ferudun same-mechanism credit',lambda:same((S.SOURCE_FACTS['Chavez_DOI'],S.SOURCE_FACTS['Ferudun_DOI'],S.SOURCE_FACTS['Ferudun_same_target_and_substantially_same_mechanism']),('10.1007/s40598-020-00154-8','10.5281/zenodo.23096994',True)))

foreign=base.replace(b'5100062 / AMR-050-0062',b'9999999 / AMR-999-9999');protected=base.replace(b'5100062 / AMR-050-0062',b'30004690 / AMR-999-9998')
queue=b'header\n'+base+foreign+protected;selected={S.Q:S.bpin(queue),S.ALL_NATIVE+'30004690/proof.md':S.bpin(b'protected')}
new=queue.replace(foreign,foreign.replace(b'queued',b'claimed_solved'));bad=queue.replace(protected,protected.replace(b'queued',b'claimed_solved'))
check('Unprotected foreign QUEUE row acknowledged',lambda:same([x['problem_id'] for x in S.reconcile_rows(queue,new,selected,base)],['9999999']))
reject('Own submitted HEAD cannot replace BASE in MAIN',lambda:S.reconcile_rows(queue,queue.replace(base,head),selected,base))
reject('Protected foreign native row cannot change',lambda:S.reconcile_rows(queue,bad,selected,base))
check('Historical bad-to-bad laundering mechanism explicit',lambda:same(S.reconcile_rows(bad,bad,selected,base),[]))
reject('Original-checkpoint good-to-receipt bad rejected',lambda:S.reconcile_rows(queue,bad,selected,base))
for doi in ('reserved','10.5281/zenodo.0','10.5281/zenodo.12x'):
    reject('Proposed/invalid DOI cannot produce published row '+doi,lambda doi=doi:S.published_row(doi))
doi='10.5281/zenodo.123';published=S.published_row(doi);merged_queue=S.replace_queue(queue,doi)
check('Merge changes exactly one own row',lambda:same([i for i,(a,b) in enumerate(zip(queue.splitlines(),merged_queue.splitlines())) if a!=b],[1]))
check('Exact accepted published row after95',lambda:same(S.reconcile_rows(merged_queue,merged_queue,{**selected,S.Q:S.bpin(merged_queue)},published),[]))
reject('BASE row cannot be accepted after95',lambda:S.reconcile_rows(queue,queue,selected,published))
reject('Published row cannot be accepted before95',lambda:S.reconcile_rows(merged_queue,merged_queue,selected,base))
reject('Merge cannot replace HEAD511 as MAIN preimage',lambda:S.replace_queue(queue.replace(base,head),doi))

pin=S.pin(b'SYNTHETIC ONLY');package='publication_package_SYNTHETIC'
gate={'schema':'pr206-root-publication-ready-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'problem_id':5100062,'original_head':S.HEAD,'claim':S.CLAIM,'source_facts':copy.deepcopy(S.SOURCE_FACTS),'metadata':{'title':'SYNTHETIC TEST TITLE'},'package':package,'package_seal':pin}
for key in ('publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','current_verifier_source_accepted'):gate[key]=True
for key in ('historical_priority_established','theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','current_openness_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged'):gate[key]=False
events=[{'review_number':i,'whole_package_scope':True,'open_findings':0,'directory':'SYNTHETIC_review'+str(i),'Root_acceptance_file':'SYNTHETIC_ROOT'+str(i)+'.json','verdict':'CLEANPASS','reviewed_package':package,'reviewed_package_seal':pin} for i in (1,2)]
gate['whole_package_review_events']=events
check('Pure final gate shape with two actual-shaped synthetic events',lambda:S.validate_gate_shape(gate))
reject('Two author math reviews cannot replace complete events',lambda:S.validate_gate_shape(change(gate,whole_package_review_events=[])))
reject('One package review is insufficient',lambda:S.validate_gate_shape(change(gate,whole_package_review_events=events[:1])))
reject('Nonclean final review rejected',lambda:S.validate_gate_shape(change(gate,whole_package_review_events=[events[0],change(events[1],verdict='FINDINGS',open_findings=1)])))
reject('Final wrong seal rejected',lambda:S.validate_gate_shape(change(gate,whole_package_review_events=[events[0],change(events[1],reviewed_package_seal=S.pin(b'other'))])))
reject('Literal row10-of20 misinterpretation rejected',lambda:S.validate_gate_shape(change(gate,source_facts={**S.SOURCE_FACTS,'historical_target_row':10,'historical_table_entries':20})))
reject('Odd-only repetition contract rejected',lambda:S.validate_gate_shape(change(gate,claim=S.CLAIM.replace('every integer r>=1','only odd r'))))
for flag in ('actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','historical_priority_established','independent_discovery_certified','current_openness_established'):
    reject('Future/priority fact rejected at90 '+flag,lambda flag=flag:S.validate_gate_shape(change(gate,**{flag:True})))

# Independently content-addressed synthetic native trees; bounded DAG expansion.
def native_tree_id(rows):
    pairs=[]
    for row in rows:
        key=row['path'].encode()+(b'/' if row['type']=='tree' else b'')
        pairs.append((key,row['mode'].lstrip('0').encode()+b' '+row['path'].encode()+b'\0'+bytes.fromhex(row['sha'])))
    raw=b''.join(x for _,x in sorted(pairs));return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
class SyntheticTrees:
    def __init__(self,rows,objects=None):self.root=native_tree_id(rows);self.objects={self.root:rows,**(objects or {})};self.calls=0
    def lookup(self,tree,prefix):return ('040000','tree',self.root)
    def api(self,endpoint):
        self.calls+=1;need(self.calls<=100,'Synthetic native hard call limit');oid=endpoint.rsplit('/',1)[1]
        return {'sha':oid,'truncated':False,'tree':copy.deepcopy(self.objects[oid])}
leaf={'path':'leaf','mode':'100644','type':'blob','sha':S.bpin(b'SYNTHETIC')['git_blob']}
h=SyntheticTrees([dict(leaf,path='proof'+str(i)) for i in range(31)])
check('Independent authenticated native31 flat tree',lambda:same(len(S.native_leaves(h,'a'*40,S.NATIVE)),31))
sub=[dict(leaf,path='leaf'+str(i)) for i in range(500)];subid=native_tree_id(sub);top=[{'path':'dir'+str(i),'mode':'040000','type':'tree','sha':subid} for i in range(61)]
h=SyntheticTrees(top,{subid:sub});peak=[0]
def native_trace(frame,event,arg):
    if event=='line' and frame.f_code.co_name=='descend' and frame.f_code.co_filename==str(D/'support206.py'):
        peak[0]=max(peak[0],len(frame.f_locals.get('result',{})))
    return native_trace
sys.settrace(native_trace)
try:reject('Valid shared DAG expansion stops on incremental global budget',lambda:S.native_leaves(h,'a'*40,S.NATIVE))
finally:sys.settrace(None)
check('No native result map ever exceeds30000 leaves',lambda:same(peak[0]<=S.MAX_CHANGED,True))
check('Shared native subtree is authenticated once',lambda:same(h.calls,2))
native_budget_probe={'largest_materialized_map':peak[0],'global_leaf_limit':S.MAX_CHANGED,'global_expanded_row_work_limit':S.MAX_NATIVE_WORK,'GET_calls':h.calls,'theoretical_leaves':30500}
h=SyntheticTrees([{'path':'dir','mode':'040000','type':'tree','sha':subid}],{subid:sub});h.objects[h.root][0]['sha']='f'*40
reject('Invalid parent hash rejected before descent',lambda:S.native_leaves(h,'a'*40,S.NATIVE))
check('No child GET before parent object authentication',lambda:same(h.calls,1))
def chain(depth):
    rows=[leaf];objects={}
    for i in range(depth):
        oid=native_tree_id(rows);objects[oid]=rows;rows=[{'path':'d','mode':'040000','type':'tree','sha':oid}]
    return SyntheticTrees(rows,objects)
h=chain(64);check('Explicit64 native depth boundary accepted',lambda:same(len(S.native_leaves(h,'a'*40,S.NATIVE)),1))
h=chain(65);reject('Native depth65 rejected before unbounded recursion',lambda:S.native_leaves(h,'a'*40,S.NATIVE))
h=SyntheticTrees([dict(leaf,path='x'*256)]);reject('Native entry byte-name bound enforced',lambda:S.native_leaves(h,'a'*40,S.NATIVE))
h=SyntheticTrees([dict(leaf,path='x'*255)]);reject('Native full path bound enforced before leaf insertion',lambda:S.native_leaves(h,'a'*40,'x'*1000+'/'))

# Original metadata must be authenticated before it can become a ready90 baseline.
real_original_raw=S.frozen('ORIGINAL_PR_METADATA.json',S.ORIGINAL_METADATA)
check('Fixed original metadata pin equals authenticated custody entry',lambda:same(S.bpin(real_original_raw),baseline['selected_files'][S.CASE+'ORIGINAL_PR_METADATA.json']))
metadata_reads=[];real_api,real_frozen=S.api,S.frozen
altered_original=S.decode(real_original_raw);altered_original.update(title='SYNTHETIC UNACKNOWLEDGED TITLE',body='SYNTHETIC UNACKNOWLEDGED BODY',updated_at='2030-01-01T00:00:00Z')
with tempfile.TemporaryDirectory(prefix='pure_metadata_pin_',dir=D) as md_folder:
    old_root=S.ROOT;S.ROOT=Path(md_folder)
    md_path=S.ROOT/S.CASE/'ORIGINAL_PR_METADATA.json';md_path.parent.mkdir(parents=True);md_path.write_bytes(S.enc(altered_original));md_path.chmod(0o444)
    S.api=lambda h,endpoint:copy.deepcopy(altered_original) if endpoint=='pulls/206' else need(False,'Unexpected synthetic metadata API')
    try:reject('Tampered local original matching changed current PR rejected under unchanged metadata authority',lambda:R.original(None,{}))
    finally:S.api,S.ROOT=real_api,old_root
    check('Original metadata fixed authority remains unchanged',lambda:same(S.ORIGINAL_METADATA,S.pin(real_original_raw)))

# Pure operations receipt binding controls: no actual authority, phase or backend.
op_uploads={'synthetic.tex':S.pin(b'TEX'),'synthetic.pdf':S.pin(b'PDF'),'synthetic.zip':S.pin(b'ZIP')}
op_gate={**gate,'package_safe_files':copy.deepcopy(op_uploads),'intended_upload_files':copy.deepcopy(op_uploads)}
op_context={'gate_pin':pin,'ready_pointer_pin':pin,'ready_acceptance_pin':pin,'checkpoint_commit':'1'*40,'package':package,'package_seal':pin,'manifest_pin':pin}
op_pub={'schema':'pr206-root-publication-receipt-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'state':'published','actual_publication_verified':True,'metadata_exact_verified':True,'all_three_public_download_SHA256_verified':True,'context':op_context,'package':package,'gate_sha256':pin['sha256'],'metadata_normalizations':[],'id':123,'doi':doi,'doi_url':'https://doi.org/'+doi,'record_url':'https://zenodo.org/records/123','metadata':copy.deepcopy(op_gate['metadata']),'package_safe_files':copy.deepcopy(op_uploads),'intended_upload_files':copy.deepcopy(op_uploads),'original_head':S.HEAD,'problem_id':5100062,'doi_resolution':{'http_status':200,'status':'resolved'},'files':[{'name':n,'size':v['bytes'],'sha256':v['sha256']} for n,v in op_uploads.items()],'public_downloads':[{'name':n,'bytes':v['bytes'],'sha256':v['sha256'],'url':'https://synthetic.invalid/'+n,'final_url':'https://synthetic.invalid/'+n} for n,v in op_uploads.items()]}
op_subset=('id','doi','doi_url','record_url','metadata','package','package_safe_files','intended_upload_files','original_head','problem_id')
op_tracker={'schema':'pr206-root-tracker-receipt-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'doi':doi,'context':op_context,'gate_sha256':pin['sha256'],'row':S.tracker_row(op_gate,doi),'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'range':"'Math Puzzles'!A1:D1",'original_preappend_baseline':{'file':'SYNTHETIC_baseline.json','pin':pin,'row_count':1,'counter_sha256':'0'*64},'publication_facts':{key:copy.deepcopy(op_pub[key]) for key in op_subset}}
for key in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','two_fresh_full_readbacks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):op_tracker[key]=True
real_ready_context,real_artifact,real_frozen=S.ready_context,S.artifact,S.frozen
def pure_operations(pub,tracker):
    pub=copy.deepcopy(pub);tracker=copy.deepcopy(tracker);pub_raw=S.enc(pub);tracker['publication_receipt']=S.pin(pub_raw)
    S.ready_context=lambda:(op_gate,op_context)
    S.artifact=lambda name,*args:copy.deepcopy(pub if name=='ROOT_PUBLICATION_RECEIPT.json' else tracker) if name in ('ROOT_PUBLICATION_RECEIPT.json','ROOT_TRACKER_RECEIPT.json') else need(False,'Unexpected synthetic operations artifact')
    S.frozen=lambda name,*args:pub_raw if name=='ROOT_PUBLICATION_RECEIPT.json' else need(False,'Unexpected synthetic operations file')
    try:return S.operations()
    finally:S.ready_context,S.artifact,S.frozen=real_ready_context,real_artifact,real_frozen
check('Exact synthetic operations copied publication and tracker subset bindings',lambda:same(pure_operations(op_pub,op_tracker)[3],op_context))
for key in ('metadata','package_safe_files','intended_upload_files','original_head','problem_id'):
    missing={k:v for k,v in op_pub.items() if k!=key}
    reject('Missing copied publication field '+key,lambda missing=missing:pure_operations(missing,op_tracker))
    broken=change(op_pub,**{key:'SYNTHETIC CORRUPTION'})
    reject('Corrupted copied publication field '+key,lambda broken=broken:pure_operations(broken,op_tracker))
for value in (False,None):
    tracker=copy.deepcopy(op_tracker)
    if value is None:del tracker['two_fresh_full_readbacks']
    else:tracker['two_fresh_full_readbacks']=value
    reject('Tracker full readbacks missing/false '+str(value),lambda tracker=tracker:pure_operations(op_pub,tracker))
for key in op_subset:
    tracker=copy.deepcopy(op_tracker);del tracker['publication_facts'][key]
    reject('Missing tracker publication fact '+key,lambda tracker=tracker:pure_operations(op_pub,tracker))
    tracker=copy.deepcopy(op_tracker);tracker['publication_facts'][key]='SYNTHETIC CORRUPTION'
    reject('Corrupted tracker publication fact '+key,lambda tracker=tracker:pure_operations(op_pub,tracker))
tracker=copy.deepcopy(op_tracker);tracker['publication_facts']['extra']='SYNTHETIC'
reject('Extra tracker publication fact rejected',lambda:pure_operations(op_pub,tracker))
tracker={k:v for k,v in op_tracker.items() if k!='publication_facts'}
reject('Missing whole tracker publication facts rejected',lambda:pure_operations(op_pub,tracker))

data={'gate':gate,'gate_pin':pin,'package':package,'package_seal':pin,'whole_package_reviews_completed':2,'DOI':doi,'record_id':123,'tracker_range':"'Math Puzzles'!A1:D1",'publication_receipt_pin':pin,'tracker_receipt_pin':pin,'predecessor':{'directory':S.OWN+'SYNTHETIC_prior/'}}
path=S.CASE+'SYNTHETIC_evidence.md';out={path:b'synthetic'};expected={**selected,path:S.bpin(out[path])}
for phase in S.PHASES:
    d=S.driver(phase);f=S.facts(phase,data,True);pre_f=S.facts(phase,data,False)
    check('Phase callback percent '+phase,lambda phase=phase,f=f:same(f['case_percent'],S.PHASES[phase][1]))
    check('Prepared phase retains48/32 '+phase,lambda pre_f=pre_f:same({k:pre_f[k] for k in S.BASE_COUNTS},S.BASE_COUNTS))
    if phase!='completion':check('Actual incomplete counters '+phase,lambda f=f:same((f['completed'],{k:f[k] for k in S.BASE_COUNTS}),(False,S.BASE_COUNTS)))
    else:check('Only actual100 increments49/33',lambda f=f:same((f['completed'],{k:f[k] for k in S.DONE_COUNTS}),(True,S.DONE_COUNTS)))
    parent='2'*40;parents=d['parents'](parent)
    check('Exact native parent list '+phase,lambda phase=phase,parents=parents:same(parents,[parent,S.HEAD] if phase=='merge' else [parent]))
    r={'schema':'pr206-lifecycle-preparation-v1','phase':phase,'PR':206,'case_percent':S.PHASES[phase][1],'original_head':S.HEAD,'commit':'1'*40,'expected_main':parent,'parent_tree':'3'*40,'tree':'4'*40,'selected_files':expected,'selected_map_sha256':S.digest(expected),'overlay_paths':sorted(out),'changed_paths':[path]}
    co={'sha':r['commit'],'parents':[{'sha':p} for p in parents],'tree':{'sha':r['tree']},'message':S.message(phase,S.digest(expected))}
    check('Pure exact parent/full foreign candidate guard '+phase,lambda phase=phase,r=r,co=co,parents=parents:S.check_candidate(phase,r,co,r['parent_tree'],expected,out,{path},{path},parents))
    reject('Foreign changed leaf rejected '+phase,lambda phase=phase,r=r,co=co,parents=parents:S.check_candidate(phase,r,co,r['parent_tree'],expected,out,{path},{path,'foreign'},parents))
    reject('Wrong parent rejected '+phase,lambda phase=phase,r=r,co=co,parents=parents:S.check_candidate(phase,r,change(co,parents=[{'sha':'9'*40}]),r['parent_tree'],expected,out,{path},{path},parents))
    ack={'UTC':'2026-10-16T20:00:00+00:00','synthetic':True};mapping={'selected_files':expected,'selected_map_sha256':S.digest(expected),'foreign_QUEUE_reconciliation_after_checkpoint':ack}
    receipt={'schema':'pr206-lifecycle-actual-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','UTC':'2026-10-16T20:00:00+00:00','PR':206,'phase':phase,'accepted':True,'case_percent':S.PHASES[phase][1],'checkpoint_commit':r['commit'],'parents':parents,'sole_parent':None if phase=='merge' else parent,'main_observed':'5'*40,'actual_tree':'6'*40,'original_head':S.HEAD,'selected_files':len(expected),'selected_map_sha256':S.digest(expected),'actual_current_selected_map_sha256':S.digest(expected),'actual_current_map_file':S.pin(S.enc(mapping)),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'original_native_custody_retained':True,'actual_original_PR_head':S.HEAD,'actual_original_PR_is_draft':phase=='ready','actual_original_PR_state':'open' if phase=='ready' else 'closed','facts':f,**{key:f[key] for key in S.RECEIPT_ALIASES}}
    check('Strict complete accepted-map guard '+phase,lambda phase=phase,receipt=receipt,mapping=mapping,r=r,f=f,parents=parents:S.check_acceptance(phase,receipt,mapping,r,expected,f,parents))
    for field in sorted(receipt):
        partial={k:v for k,v in receipt.items() if k!=field}
        reject('Missing actual receipt field '+phase+':'+field,lambda phase=phase,partial=partial,mapping=mapping,r=r,f=f,parents=parents:S.check_acceptance(phase,partial,mapping,r,expected,f,parents))
    for label,forged in [('QUEUE-only',{S.Q:expected[S.Q]}),('extra path',{**expected,S.CASE+'EXTRA':S.bpin(b'bad')}),('changed protected pin',{**expected,S.ALL_NATIVE+'30004690/proof.md':S.bpin(b'bad')})]:
        mm=change(mapping,selected_files=forged,selected_map_sha256=S.digest(forged));aa=change(receipt,selected_files=len(forged),actual_current_selected_map_sha256=S.digest(forged),actual_current_map_file=S.pin(S.enc(mm)))
        reject('V1 acceptance-map gap rejected '+phase+':'+label,lambda phase=phase,aa=aa,mm=mm,r=r,f=f,parents=parents:S.check_acceptance(phase,aa,mm,r,expected,f,parents))
    reject('Wrong actual PR fresh-state evidence '+phase,lambda phase=phase,receipt=receipt,mapping=mapping,r=r,f=f,parents=parents:S.check_acceptance(phase,change(receipt,actual_original_PR_head='9'*40),mapping,r,expected,f,parents))
    prior_case={'PR':206,'original_head':S.HEAD,'case_percent':S.PHASES[phase][0],'completed':False,**S.BASE_COUNTS}
    prior_progress={'current_PR':206,'current_PR_workflow_percent':S.PHASES[phase][0],'current_unrecognized_stale_gate':True,'current_DOI':'OLD','conditional_next_numeric_intake_cursor':999,'program_snapshot_old':'OLD','published_PRs':list(range(1,33)),'fully_completed_eligible_PRs':list(range(1,49)),'dated_eligible_total':99,'last_completed_DOI':'PRESERVE205',**S.BASE_COUNTS}
    cc,pp=S.project(phase,prior_case,prior_progress,'2026-10-16T20:00:00+00:00',data)
    check('Stale current aliases retired '+phase,lambda pp=pp:same((pp.get('current_unrecognized_stale_gate'),pp.get('conditional_next_numeric_intake_cursor')),(None,None)))
    if phase!='completion':check('Projected90/95/98 incomplete counters '+phase,lambda cc=cc,pp=pp:same((cc['completed'],{k:cc[k] for k in S.BASE_COUNTS},{k:pp[k] for k in S.BASE_COUNTS}),(False,S.BASE_COUNTS,S.BASE_COUNTS)))
    else:check('Conditional100 arrays/counters explicit',lambda cc=cc,pp=pp:same((cc['completed'],cc['completion_postimage_effective_only_after_own_actual_MAIN_acceptance_sync_pointer'],len(pp['fully_completed_eligible_PRs']),len(pp['published_PRs']),pp['next_numeric_intake_cursor']),(True,True,49,33,207)))
    if phase=='ready':check('Ready90 has no future DOI/tracker/merge',lambda cc=cc:same((cc['DOI'],cc['tracker_range'],cc['actual_publication_verified'],cc['actual_original_PR_merged']),(None,None,False,False)))
    if phase=='factual':check('Factual98 remains completedfalse and no own actual factual assertion',lambda cc=cc:same((cc['completed'],cc['actual_factual_accepted']),(False,False)))

# The current native constructor is exercised as a pure byte proposal only.
portable=S.frozen('current_verifier_preparation_02/portable_exact_verifier.py',S.PORTABLE,False);proof=b'% SYNTHETIC proof-source protocol control only\n'
native_g={**gate,'package_seal_file':'PACKAGE_SEAL.json','manuscript_source_file':'synthetic.tex','manuscript_pdf_file':'synthetic.pdf','package_safe_files':{'synthetic.tex':S.pin(proof)}}
p={'id':123,'doi':doi};t={'doi':doi,'range':"'Math Puzzles'!A1:D1"}
for stage in N.STAGES:
    f={'schema':'pr206-native-actual-facts-v1','original_head':S.HEAD,'UTC':'2026-10-16T20:00:00+00:00','package_seal':S.pp(package+'/PACKAGE_SEAL.json',pin),'publication_ready_gate':S.pp(S.PUBLICATION_GATE,pin),'publication_receipt':S.pp('ROOT_PUBLICATION_RECEIPT.json',pin),'tracker_receipt':S.pp('ROOT_TRACKER_RECEIPT.json',pin)}
    if stage!='published_pending_merge':f['merge_receipt']=S.pp('SYNTHETIC_merge/ACCEPTANCE.json',pin)
    if stage=='actual_factual_accepted_completion_pending':f['factual_receipt']=S.pp('SYNTHETIC_factual/ACCEPTANCE.json',pin)
    rendered=N.render(stage,f,old,portable,proof,native_g,p,t)
    check('Pure native exact31 path set '+stage,lambda rendered=rendered:same(set(rendered),{S.NATIVE+n for n in set(old)|set(N.ADDED)}))
    check('Both current executable paths exact accepted21804 '+stage,lambda rendered=rendered:same((rendered[S.NATIVE+'verify_triangles.py'],rendered[S.NATIVE+'independent_review/independent_check.py']),(portable,portable)))
    check('Exact proof-source copy '+stage,lambda rendered=rendered:same(rendered[S.NATIVE+'CURRENT_PROOF_SOURCE.tex'],proof))
    for filename in ('source_record.json','source_manifest.json','PUBLICATION_STATUS.json','SOURCE_CORRECTION.json'):
        current=S.decode(rendered[S.NATIVE+filename])['current']
        check('Correct current source facts '+stage+filename,lambda current=current:same((current['source_facts'],current['program_completion_accepted'],current['completed']),(S.SOURCE_FACTS,False,False)))
    check('Archive bytes unchanged by pure rendering '+stage,lambda:same(sum(len(S.frozen('original_submitted_head/'+name)) for name in old),55033))
    reject('Tampered portable rejected '+stage,lambda stage=stage,f=f:N.render(stage,f,old,portable+b'x',proof,native_g,p,t))
    reject('Unreviewed proof copy rejected '+stage,lambda stage=stage,f=f:N.render(stage,f,old,portable,proof+b'x',native_g,p,t))
    reject('Future completion fact rejected by native schema '+stage,lambda stage=stage,f=f:N.render(stage,{**f,'completion_receipt':S.pp('FUTURE',pin)},old,portable,proof,native_g,p,t))

# Bounded local filesystem guards operate solely in an owned temporary fixture.
real_root=S.ROOT
with tempfile.TemporaryDirectory(prefix='pure_lifecycle_guard_',dir=D) as directory:
    S.ROOT=Path(directory)
    for path in S.VIEWS:(S.ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    lock=S.ROOT/S.PROGRAM_VIEW_LOCK;lock.write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);lock.chmod(0o444)
    fixture_counter=[0]
    def owned_sync():
        fixture_counter[0]+=1;g=S.generation('fixture'+str(fixture_counter[0]));(S.ROOT/g).mkdir(parents=True)
        with S.WriterOwnership():return S.sync_images(images(),g)
    def reset():
        for i,path in enumerate(S.VIEWS):
            f=S.ROOT/path
            if f.is_symlink() or f.is_file():f.unlink()
            elif f.exists():f.rmdir()
            f.write_bytes(('old'+str(i)).encode())
    def images():return [(path,S.pin(('old'+str(i)).encode()),('post'+str(i)).encode()) for i,path in enumerate(S.VIEWS)]
    reset();check('Synthetic all-five atomic sync',lambda:same(len(owned_sync()),5))
    check('Synthetic all-five readonly regular readback',lambda:same(all(stat.S_ISREG((S.ROOT/path).lstat().st_mode) and stat.S_IMODE((S.ROOT/path).lstat().st_mode)==0o444 for path in S.VIEWS),True))
    for kind in ('symlink','dangling symlink','directory','FIFO'):
        reset();bad_path=S.ROOT/S.VIEWS[-1];bad_path.unlink()
        if kind=='symlink':bad_path.symlink_to(S.ROOT/S.VIEWS[0])
        elif kind=='dangling symlink':bad_path.symlink_to(S.ROOT/'absent')
        elif kind=='directory':bad_path.mkdir()
        else:os.mkfifo(bad_path)
        reject('All-five precheck rejects '+kind,lambda:owned_sync())
        check('No earlier replacement when fifth type invalid '+kind,lambda:same((S.ROOT/S.VIEWS[0]).read_bytes(),b'old0'))
        if kind=='directory':bad_path.rmdir()
        else:bad_path.unlink()
    reset();reject('Stale per-file preimage rejected',lambda:S.atomic(S.VIEWS[0],b'new',S.pin(b'stale')))
    real_replace=S.os.replace;counter=[0]
    def fail_second(src,dst):
        counter[0]+=1
        if counter[0]==2:raise OSError('Synthetic replacement failure')
        return real_replace(src,dst)
    S.os.replace=fail_second
    try:reject('Mid-sync failure returns no success',lambda:owned_sync())
    finally:S.os.replace=real_replace
    check('Explicit per-file partial-postimage limit',lambda:same((S.ROOT/S.VIEWS[0]).read_bytes(),b'post0'))
    check('Failed staged/preimage evidence retained in owned generation',lambda:same(bool([f.name for f in Path(directory).rglob('*') if f.name.startswith('.pr206_')]),True))
S.ROOT=real_root

parsed=ast.parse((D/'support206.py').read_bytes());functions={n.name:ast.unparse(n) for n in parsed.body if isinstance(n,ast.FunctionDef)}
check('All phases bind full prepared acceptance map',lambda:same('expected' in functions['_accepted'] and 'check_acceptance' in functions['_accepted'],True))
check('Receipt continuity independently starts from checkpoint full expected',lambda:same("_native_state(c, h, phase, data, r, expected, receipt['main_observed'])" in functions['_accepted'],True))
check('Fresh checks retain authenticated receipt ancestry',lambda:same("'compare/' + receipt['main_observed'] + '...' + main" in functions['_fresh_accepted'],True))
check('Historical pointers still require fresh MAIN ancestry',lambda:same("'compare/' + a['main_observed'] + '...' + main" in functions['actual'],True))
check('Pointer requires successful five-sync and exact readonly postimages',lambda:same('LOCAL_GLOBAL_FIVE_SYNC.json' in functions['pointer'] and 'read(path) == out[path]' in functions['pointer'],True))
check('Actual90 PR fields come from freshly returned original guard',lambda:same("observed_pr['head']['sha']" in functions['accept'] and "observed_pr['draft']" in functions['accept'] and "observed_pr['state']" in functions['accept'],True))

report={'schema':'pr206-lifecycle-pure-offline-controls-v1','optimization':sys.flags.optimize,'native_budget_probe':native_budget_probe,'checks':len(results),'all_pass':all(x['pass'] for x in results),'results':results,'sources':sources,'limits':['No real prepare/verify/accept/sync/pointer/bind phase; no native backend injection/import, API/network, adapter/cache, ref, PR, MAIN, actual global-five or pointer action.','Module callbacks were configured only for pure synthetic facts/guards. Future Root source/publication authority remains absent.','Existing custody/archive/fixed-gate data was checked read-only; current portable bytes were hashed/copied in memory, never executed.','Native render and receipt/gate fixtures are explicitly synthetic proposals, not actual future Root receipts or publication facts.','Filesystem fixtures are bounded temporary children of this new preparation folder; atomicity is per file, not a five-file transaction.','Tests do not certify future external direct8/adapter alias/callback cleanup, authenticated transport, live leases/CAS, services or independent operational review.']}
print(json.dumps(report,indent=2,sort_keys=True))
