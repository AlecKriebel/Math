"""PR205 custody10 using audited native guards. Root alone runs remote phases."""
import sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent
CASE='draft_pr_publication_program_20260930/audits/pr205_5100030/';PREFIX='draft_pr_publication_program_20260930/';OWN=CASE+'custody_checkpoint_01/'
HEAD='e8d7e925d19698edcb75822e40ca5ac820eb4388';Q='unsolved_math_prioritization/QUEUE.md';PID='5100030'
VIEWS=[CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md']+[PREFIX+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')]
BASE_DIR=A.parent/'pr204_5100012/publication_lifecycle_02/completion100_01'
BASE_COMMIT='0758ddcedaf499e2a1ebc3fb319965c7ba069a12';BASE_TREE='85c0ad98002c3a5bd88aa8ba68b4e87926a36f83';BASE_DIGEST='e57fa93c4ad51ef0cfbdaf721a4503919f0bc38b67acc8588ff70e6b69376bcc'
BASE_ACCEPT={'bytes':3062,'sha256':'78c14ec78414ac5c2d68ad29c58d16bf0925b64a60b99dc37e118873237b08fb'}
BASE_MAP={'bytes':1229790,'sha256':'ea5dbc2961b65472f8d2088d83ee9e8094f71e5521eda615aac9c7645809059b'}
CUSTODY_PIN={'bytes':7313,'sha256':'967da7f97505e7c25b332535b1d468f23e20c0eb1204196710f074885c942f5e'}
QUEUE_RECEIPT_PIN={'bytes':1785,'sha256':'4f7ff59a64cd99331711ece68a960baf52267397532cc4f48a2d3ae25ec87ec9'}
INTAKE_PIN={'bytes':4046,'sha256':'a719ec4d6cdd1a36620f02df1f18ae06fd5a3e5804972d1a3d96b349e88fb178'}
BASE_ROW_PIN={'bytes':121,'sha256':'f66cda83ff5e83157122daa3a7d24c36974172aa8c5c77161b1da43cbf1e8774'}
METADATA_FILES=('original_git_metadata/ORIGINAL_COMMIT.json','original_git_metadata/RANGE_BASE_COMMIT.json','original_git_metadata/ORIGINAL_LINEAR_CHAIN.json','original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json')
OWN_FILES={'freeze_original205.py','checkpoint_intake205.py','run_intake205_with_tree_cache.py','offline_intake_guards.py','CHECKPOINT_CONTRACT.md','CUSTODY_RECHECK.json','ORIGINAL_DECLARED_SOURCE_HASHES.json','BASELINE_AUTHORITY.json','INTAKE10_PREPARATION_CONTRACT.json','OFFLINE_INTAKE_GUARDS.json','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json'}
STATUS='ORIGINAL_PR205_CUSTODY_RECORDED_MATHEMATICS_AND_PRIORITY_UNCLEARED'
REMAIN='Root must assess independent mathematical families and primary-source contract, repair/verify original checks, then bounded priority/editorial/publication gates. Original favorable review is historical evidence only. No theorem, paper, deposit, tracker, merge or206 intake authorized by custody10.'
def need(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bpin(raw):return {**pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def enc(value):return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
def read(path):return json.loads(path.read_bytes())
def safe(path):need(isinstance(path,str) and path and not path.startswith('/') and '\\' not in path and all(p not in ('','.','..') for p in path.split('/')),'Unsafe relative path');return path
def frozen(path,expected=None):
    p=A
    for part in safe(path).split('/'):p=p/part;need(not p.is_symlink(),'Symlink artifact '+path)
    need(p.is_file() and p.stat().st_mode&0o777==0o444,'Readonly regular artifact '+path);raw=p.read_bytes()
    if expected is not None:need(pin(raw)==expected,'Artifact pin drift '+path)
    return raw
def save(path,raw):
    need(path.resolve().is_relative_to(D),'Generation output scope')
    with path.open('xb') as stream:need(stream.write(raw)==len(raw),'Short record');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    fsync_dir(path.parent)
def fsync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
def generation(name):need(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation');return D/name
core=A.parent/'pr204_5100012/custody_checkpoint_01/checkpoint204.py';raw=core.read_bytes();need(pin(raw)=={'bytes':33976,'sha256':'520171b2a762625cd58a08873dea7b1795671c492af138d86958b1928c603593'},'Audited native guard source pin')
s=importlib.util.spec_from_file_location('pr205_private_native_custody_guards',core);v=importlib.util.module_from_spec(s);exec(compile(raw,str(core),'exec'),v.__dict__)
# Only the private module instance's case scope/callbacks are adapted; old files unchanged.
v.CASE=CASE;v.HEAD=HEAD;v.VIEWS=VIEWS;v.A=A
def message(digest):return 'PR205 custody10: exact submitted originals and BASE versus HEAD queue custody\n\nMathematics/source/priority/publication NOT CLEARED.47completed31published,last204,cursor205,advancefalse. No QUEUE or native attempt write.\nSelected-map SHA256: '+digest
def unchanged_pr():
    p=v.get('pulls/205');m=json.loads(frozen('ORIGINAL_PR_METADATA.json'))
    need(p['head']['sha']==HEAD and p['head']['ref']=='dot/math-5100030' and p['base']['ref']=='main','Original PR205 HEAD/branch/base')
    for k in ('title','body','state','draft','merged','created_at','updated_at','commits','changed_files'):need(p[k]==m[k],'Original PR205 metadata changed '+k)
    need(p['state']=='open' and p['draft'] is True and p['merged'] is False,'Original PR205 open draft unchanged')
v.message=message;v.unchanged_pr=unchanged_pr
def baseline():
    ar=(BASE_DIR/'ACCEPTANCE.json').read_bytes();mr=(BASE_DIR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes();need(pin(ar)==BASE_ACCEPT and pin(mr)==BASE_MAP,'Actual204 receipt/map pins');a=json.loads(ar);x=json.loads(mr)
    need(a['accepted'] is True and a['completion_metadata_accepted'] is True and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and a['checkpoint_commit']==a['main_observed']==BASE_COMMIT and a['actual_tree']==BASE_TREE,'Actual204 completion authority')
    need(len(x['selected_files'])==4084 and hashlib.sha256(json.dumps(x['selected_files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==x['selected_map_sha256']==a['actual_current_selected_map_sha256']==BASE_DIGEST,'All4084 selected identities')
    need((a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['next_numeric_intake_cursor'])==(47,31,204,205),'Actual204 counters');return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':x['selected_files'],'selected_map_sha256':BASE_DIGEST}
def inputs():
    j=read(D/'SAFE_AUTHORED_MANIFEST.json');need(set(j['files'])==OWN_FILES-{'SAFE_AUTHORED_MANIFEST.json'},'Exact205 authored allowlist')
    for name,x in j['files'].items():frozen('custody_checkpoint_01/'+name,x)
    c=json.loads(frozen('ORIGINAL_SUBMISSION_CUSTODY.json',CUSTODY_PIN));q=json.loads(frozen('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',QUEUE_RECEIPT_PIN));frozen('ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json',INTAKE_PIN)
    frozen('ORIGINAL_PR_METADATA.json',c['original_PR_metadata'])
    need(c['original_head']==q['original_head']==HEAD and c['file_count']==len(c['files'])==17 and c['total_native_bytes']==sum(x['bytes'] for x in c['files'].values())==41845 and c['original_QUEUE_status']=='claimed_solved' and c['original_QUEUE_effort_cell']=='1/5','205 original custody extent')
    need(pin(q['base_own_row']['text'].encode())==BASE_ROW_PIN and q['BASE_status']=='queued' and q['BASE_effort']=='0/5' and q['HEAD_status']=='claimed_solved' and q['HEAD_effort']=='1/5' and q['foreign_QUEUE_rows_identical'] is True,'205 BASE/HEAD distinction')
    for name,x in c['files'].items():need(bpin(frozen('original_submitted_head/'+name))=={k:x[k] for k in ('bytes','sha256','git_blob')},'Original205 archive drift '+name)
    material=set(METADATA_FILES)|{'ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json','ORIGINAL_SUBMISSION_CUSTODY.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','ORIGINAL_PR_METADATA.json'}|{'original_submitted_head/'+n for n in c['files']}
    need(set(j['original_material'])==material,'Exact original material allowlist')
    for name,x in j['original_material'].items():frozen(name,x)
    return c,q
def reconcile(c,h,b,parent):
    old=v.native_body(h,Q,b['commit']);new=v.native_body(h,Q,parent);need(c.byte_pin(old)==b['selected_files'][Q],'Prior accepted QUEUE pin');ol,nl=old.splitlines(keepends=True),new.splitlines(keepends=True);need(len(ol)==len(nl),'Foreign QUEUE line count')
    protected={k.split('/')[2] for k in b['selected_files'] if k.startswith('unsolved_math_prioritization/attempts/')}|{PID};changes=[]
    for i,(x,y) in enumerate(zip(ol,nl)):
        if x==y:continue
        def ident(z):
            cells=z.decode().split('|');need(len(cells)==14 and cells[1].strip().isdigit(),'Malformed changed QUEUE row');return cells[2].strip().split(' / ')[0]
        problem=ident(x);need(ident(y)==problem and problem not in protected,'Own/protected QUEUE row changed');changes.append({'one_based_line':i+1,'foreign_problem_id':problem,'old':bpin(x),'new':bpin(y)})
    marker=b'| 5100030 / AMR-050-0030 |';own_old=[x for x in ol if marker in x];own_new=[x for x in nl if marker in x]
    need(len(own_old)==len(own_new)==1 and own_old==own_new and pin(own_new[0])==BASE_ROW_PIN,'Own205 exact BASE121 row must remain unchanged, never HEAD371')
    return {**b['selected_files'],Q:c.byte_pin(new)},{'UTC':now(),'baseline_actual_commit':b['commit'],'observed_MAIN':parent,'old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_and_protected_and_own_QUEUE_bytes_identical':True,'own_checkpoint_writes_no_QUEUE_bytes':True}
def project(p,stamp):
    p=json.loads(enc(p));need((p['current_PR'],p['current_PR_workflow_percent'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'])==(204,100,47,31,204),'Prior204 actual completion view')
    retired={k:p[k] for k in p if k.lower().startswith(('current_','next_','conditional_','program_snapshot_')) or k in ('advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records')}
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_phase':'ACTUAL_COMPLETION_BEFORE205_CUSTODY10','actual_completion_commit':BASE_COMMIT,'actual_completion_receipt_pin':BASE_ACCEPT,'values':retired})
    for k in retired:del p[k]
    effort='Submitted QUEUE reports1/5; author interaction turns and actual model/reasoning effort unverified. Three Git commits are not three author turns.'
    case={'UTC':stamp,'PR':205,'problem_id':5100030,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','original_effort':effort,'original_author_commit_count':3,'original_archive_files':17,'original_native_bytes':41845,'status':STATUS,'case_percent':10,'claim_source':'original_submitted_head/CANDIDATE_PROOF.md','submitted_favorable_review_scope':'Historical original submission; not adopted as current mathematical or priority clearance','source_contract_clearance':False,'mathematical_clearance':False,'mathematical_result_valid':None,'priority_clearance':False,'priority_audit_complete':False,'historical_novelty_or_firstness_established':False,'independent_discovery_certified':False,'literal_simultaneity_established':False,'mathematical_families_assigned_by_Root':3,'mathematical_family_output_acceptance_contributed_by_custody':0,'theorem_accepted':False,'paper_prepared':False,'publication_ready':False,'deposit_prepared':False,'actual_Zenodo_published':False,'actual_publication_verified':False,'actual_tracker_updated':False,'actual_tracker_row_verified':False,'actual_original_PR_merged':False,'completed':False,'DOI':None,'record_id':None,'tracker_range':None,'current_new_publication_ledger':[],'remaining_required_steps':REMAIN,'fully_completed_count':47,'published_count':31,'last_completed_PR':204,'next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
    p.update(UTC=stamp,updated_UTC=stamp,current_PR=205,current_problem_id=5100030,current_status=STATUS,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_QUEUE_effort_cell='1/5',current_original_effort=effort,current_original_PR_state='open',current_original_PR_open_draft=True,current_original_PR_merged=False,current_closed=False,current_closed_without_merge=False,current_completed=False,current_PR_workflow_percent=10,current_workflow_estimate_percent=10,current_original_archive_files=17,current_original_native_bytes=41845,current_source_contract_clearance=False,current_mathematical_clearance=False,current_mathematical_result_valid=None,current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_literal_simultaneity_established=False,current_theorem_accepted=False,current_paper_prepared=False,current_publication_ready=False,current_deposit_prepared=False,current_Zenodo_published=False,current_actual_publication_verified=False,current_DOI=None,current_record_id=None,current_tracker_updated=False,current_tracker_range=None,current_actual_tracker_row_verified=False,current_original_PR_actual_merged=False,current_new_publication_ledger=[],current_mathematical_families_assigned_by_Root=3,current_mathematical_family_output_acceptance_contributed_by_custody=0,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=205,conditional_next_numeric_intake_cursor=206,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=205,next_status_only_intake_performed=False,persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR205 original custody10 only.17files41845B and complete18path own-only original delta authenticated; BASE121queued0/5 differs from HEAD371claimed_solved1/5. Mathematics/priority/publication NOT CLEARED.47completed31published,last204,cursor205,advancefalse.',program_snapshot_authority_condition='Only effective after Root actual MAIN singletrueparent/fullforeign/everyselected acceptance. Custody supplies no mathematical/scientific publication gate.')
    p.update(current_record='audits/pr205_5100030/CURRENT_CASE_STATUS.json',latest_ordered_intake_record='audits/pr205_5100030/ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json',current_mathematics_cleared=False,current_priority_novelty_clearance=False,current_theorem_novelty_cleared=False,current_formula_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_qualified_attributed_note_editorially_cleared=False,current_editorial_manuscript_preparation_authorized=False,current_package_prepared=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_whole_package_review_loop_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_verification_code_publication_clearance=False)
    return case,p
def overlay(c,h,parent,stamp):
    custody,q=inputs();out={}
    names=['ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json','ORIGINAL_SUBMISSION_CUSTODY.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','ORIGINAL_PR_METADATA.json']+list(METADATA_FILES)+['original_submitted_head/'+n for n in custody['files']]+['custody_checkpoint_01/'+n for n in OWN_FILES]
    for path in names:out[CASE+path]=frozen(path)
    raw=v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent);case,p=project(json.loads(raw),stamp);out[CASE+'CURRENT_CASE_STATUS.json']=enc(case);out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
    note=('\n'+stamp+' — PR205 original custody10:17files41845B/10native trees/complete18path own-only original delta; originalclaimed_solved1/5 is eligibility, no current mathematics/priority clearance. BASE121queued0/5 and HEAD371claimed_solved1/5 explicitly distinguished; no native attempt/QUEUE write.47completed31published,last204,cursor205/advancefalse. '+REMAIN+'\n').encode();out[CASE+'RESEARCH_LOG.md']=('# PR205 custody\n').encode()+note
    for path in (PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md'):out[path]=v.native_body(h,path,parent)+note
    need(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out),'No QUEUE/native overlay')
    return out
def run(mode,name):
    need(mode in ('prepare','verify','accept'),'Phase');inputs();b=baseline();c,h,rv,n=v.load();dest=generation(name)
    if mode=='prepare':
        need(not dest.exists(),'Fresh generation required');parent=h.api('git/ref/heads/main')['object']['sha'];need(h.api('compare/'+BASE_COMMIT+'...'+parent)['status'] in ('identical','ahead'),'MAIN lacks actual204 completion');inherited,ack=reconcile(c,h,b,parent);pt=c.selected_current(h,parent,inherited,BASE_TREE);v.validate_caches(h);unchanged_pr();stamp=now();pre={}
        for path in VIEWS:
            local=ROOT/path;remote=v.native_body(h,path,parent)
            if path.startswith(CASE):need(remote is None and not local.exists(),'New205 case views must be absent');pre[path]=None
            else:need(local.is_file() and not local.is_symlink() and pin(local.read_bytes())==pin(remote),'Global3 must match fresh parent');pre[path]=pin(remote)
        out=overlay(c,h,parent,stamp);dest.mkdir();save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
        entries=[{'path':k,'mode':'100644','type':'blob','content':raw.decode('utf-8')} for k,raw in sorted(out.items())];tr=h.api('git/trees','POST',{'base_tree':pt,'tree':entries})['sha'];co=h.api('git/commits','POST',{'tree':tr,'parents':[parent],'message':message(c.selected_digest(expected))})['sha']
        r={'UTC':stamp,'PR':205,'case_percent':10,'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tr,'commit':co,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':pre,'MAIN_moved':False,'mathematical_clearance':False,'priority_clearance':False,'advance_to_next_PR_authorized_now':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');need(r['PR']==205 and r['case_percent']==10 and r['original_head']==HEAD,'Prepared intake identity');parent=r['expected_main'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**b['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,r['UTC']);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
    v.verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ('prepare','verify'):
        need(main==parent,'MAIN lease changed; fresh generation required')
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc({'UTC':now(),'PR':205,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'case_percent':10,'mathematical_clearance':False,'priority_clearance':False,'actual_MAIN_acceptance':False}))
        print(json.dumps({'mode':mode,'PR':205,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'no_MAIN_ref_mutation':True}));return
    need(h.api('compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Actual MAIN lacks intake');current,post=reconcile(c,h,r,main);tree=c.selected_current(h,main,current,r['tree']);v.validate_caches(h);unchanged_pr()
    for path,raw in out.items():need(c.byte_pin(raw)==expected[path] and h.lookup(tree,path)==('100644','blob',expected[path]['git_blob']),'Actual overlay identity '+path)
    body=enc({'selected_files':current,'selected_map_sha256':c.selected_digest(current),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':205,'accepted':True,'case_percent':10,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'selected_files':len(current),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(current),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'fully_completed_count':47,'published_count':31,'last_completed_PR':204,'next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False,'goal_complete':False};save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def sync(name):
    inputs();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json');need(a['accepted'] is True and a['PR']==205 and a['case_percent']==10 and a['checkpoint_commit']==r['commit'] and a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()),'Actual205 custody acceptance required')
    c,h,rv,n=v.load();need(c.selected_digest(mp['selected_files'])==mp['selected_map_sha256']==a['actual_current_selected_map_sha256'],'Actual selected digest');main=h.api('git/ref/heads/main')['object']['sha'];need(h.api('compare/'+r['commit']+'...'+main)['status'] in ('identical','ahead'),'Actual intake absent');current,ack=reconcile(c,h,{'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':mp['selected_files']},main);c.selected_current(h,main,current,a['actual_tree']);v.validate_caches(h);unchanged_pr();images=[]
    for path in VIEWS:
        local=ROOT/path;post=v.native_body(h,path,r['commit']);need(c.byte_pin(post)==r['selected_files'][path],'Sync postimage');prior=pin(local.read_bytes()) if local.exists() else None;need(not local.is_symlink() and prior in (r['local_five_expected_preimages'][path],pin(post)),'Unexpected local five preimage');images.append((path,local,prior,post))
    for path,local,prior,post in images:
        need((pin(local.read_bytes()) if local.exists() else None)==prior,'Local five changed after precheck')
        if prior!=pin(post):
            tmp=local.with_name(local.name+'.pr205_custody_sync_tmp')
            with tmp.open('xb') as f:need(f.write(post)==len(post),'Short local view');f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
            os.replace(tmp,local);fsync_dir(local.parent)
        local.chmod(0o444);need(local.read_bytes()==post,'Local five readback')
    save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc({'UTC':now(),'PR':205,'actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':[{'path':path,'postimage':pin(post)} for path,local,prior,post in images],'fresh_MAIN_revalidated':main,'foreign_QUEUE_reconciliation':ack,'fully_completed_count':47,'published_count':31,'last_completed_PR':204,'next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False}));print(json.dumps({'all_five_synced':True,'PR':205}))
if __name__=='__main__':
    need(len(sys.argv)==3,'prepare/verify/accept/sync GEN')
    if sys.argv[1]=='sync':sync(sys.argv[2])
    else:run(sys.argv[1],sys.argv[2])
