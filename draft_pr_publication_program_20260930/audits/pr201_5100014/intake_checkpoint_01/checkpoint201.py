"""PR201 immutable custody and active mathematical-review checkpoint; no ref move."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr201_5100014/';PREVIOUS=PREFIX+'audits/pr200_5100007/'
PRIOR=P/'audits/pr200_5100007/publication_lifecycle_01/completion01'
HEAD='90bdb85235979f2ffa7496b9b689036654e55200';Q='unsolved_math_prioritization/QUEUE.md'
MUTABLE={PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def read(p):return json.loads(p.read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 f=P/'audits/pr200_5100007/publication_lifecycle_01/finish200.py';s=importlib.util.spec_from_file_location('completed200_lowlevel',f);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);c,h,rv,n=v.load();h.m.TREE_CACHE_PATH=A/'INTAKE_PRIVATE_TREE_CACHE.json';return c,h,rv
def baseline(c):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json');x=read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['completion_metadata_accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN']
 assert r['commit']==a['checkpoint_commit']=='34c92cb5cfb47a0055d6e5c86b7528f78d762848' and len(r['selected_files'])==a['selected_files']==2110
 assert r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='6ada87c86d0697e20ee3cc247cc3ad91d06e2143fc272674e26a86f5cedac4cd'
 assert pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 assert (a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['advance_to_next_PR_authorized_now'])==(44,28,200,True)
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def original(h):
 p=h.api('pulls/201');assert p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False
 assert p['created_at']==p['updated_at']=='2026-10-01T05:18:49Z'
def queue_reconcile(c,h,base,parent):
 old=h.body_at(Q,base['commit']);new=h.body_at(Q,parent);assert c.byte_pin(old)==base['selected_files'][Q]
 protected={n.split('/')[2] for n in base['selected_files'] if n.startswith('unsolved_math_prioritization/attempts/')};protected.add('5100014')
 ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True);assert len(ol)==len(nl);changes=[]
 for i,(x,y) in enumerate(zip(ol,nl)):
  if x==y:continue
  def ident(b):
   z=b.decode().split('|');assert len(z)==14 and z[1].strip().isdigit();return z[2].strip().split(' / ')[0]
  pid=ident(x);assert ident(y)==pid and pid not in protected;changes.append({'one_based_line':i+1,'foreign_problem_id':pid,'old_line':pin(x),'new_line':pin(y)})
 assert [x for x in ol if b'| 5100014 / AMR-050-0014 |' in x]==[x for x in nl if b'| 5100014 / AMR-050-0014 |' in x]
 return {**base['selected_files'],Q:c.byte_pin(new)},{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_actual_commit':base['commit'],'observed_actual_MAIN':parent,'scope':'Authenticate concurrent foreign QUEUE bytes only, without mathematical endorsement. Own checkpoint never writes QUEUE.','old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_own_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_QUEUE_bytes_identical':True,'all_protected_own_QUEUE_rows_identical':True}
def overlay(h,parent,stamp):
 inputs=read(D/'INPUT_PINS.json');out={}
 for rel,x in inputs['safe_authored_inputs'].items():
  f=A/rel;assert f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444;b=f.read_bytes();assert pin(b)==x,rel;out[CASE+rel]=b
 custody=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');assert custody['original_head']==HEAD and custody['original_QUEUE_status']=='claimed_solved' and len(custody['files'])==24
 for rel,x in custody['files'].items():
  b=out[CASE+'original_submitted_head/'+rel];assert pin(b)=={k:x[k] for k in ['bytes','sha256']} and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 out[CASE+'intake_checkpoint_01/INPUT_PINS.json']=(D/'INPUT_PINS.json').read_bytes();out[CASE+'intake_checkpoint_01/checkpoint201.py']=Path(__file__).read_bytes()
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:out[PREVIOUS+'publication_lifecycle_01/completion01/'+name]=(PRIOR/name).read_bytes()
 intake_dir=P/'ordered_intakes_after_PR200_20261016'
 for f in sorted(intake_dir.iterdir()):
  if f.is_file() and not f.is_symlink() and f.name!='PRIVATE_TREE_CACHE.json':
   assert f.stat().st_mode&0o777==0o444,f;out[PREFIX+'ordered_intakes_after_PR200_20261016/'+f.name]=f.read_bytes()
 intakepath=PREFIX+'ordered_intakes_after_PR200_20261016/PR201_ORIGINAL_STATUS_INTAKE.json';assert out[intakepath]==(A/'ORIGINAL_STATUS_INTAKE.json').read_bytes()
 families=['pr201_source_analytic_audit','pr201_direct_geometry_audit','pr201_algebra_reproduction_audit'];status='ORIGINAL_CLAIMED_SOLVED_FROZEN_THREE_NEW_MATHEMATICAL_FAMILIES_ACTIVE_UNCLEARED'
 remain='Finish independent literal-source/analytic, direct Euclidean geometry and exact-algebra/physical-orbit reproduction audits; Root proof/source/code verification before deep priority. No publication or merge clearance.'
 claim='k303,a: for a fixed strictly nested nondegenerate confocal ellipse pair with noncircular boundary and primitive N=2mod4, product of signed outer tangent-polygon area and its pedal signed area from every fixed real M is phase invariant; all primitive star windings must be checked.'
 warning='arxiv2004.12497v11 Section2 equation1 explicitly signed area, Section3.4/Table4p6 k303,a product A-prime A-prime-M, N=2mod4, all M; distinct journal Table4p346 matches. Least period is an explicit theorem convention, not verbatim printed in table. Repeated odd orbits can fail; no union-area, circle or hyperbolic extension inferred. Dated proof? is not current worldwide openness.'
 case={'UTC':stamp,'PR':201,'problem_id':5100014,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':'Original turns/log report one substantive author turn; actual model/effort unverified; later audits not silently counted as original effort','original_QUEUE_effort_cell':'1/5','status':status,'case_percent':15,'exact_claim':claim,'source_provenance_warning':warning,'original_archive_files':24,'independent_mathematical_families':families,'independent_mathematical_families_active':True,'mathematical_clearance':False,'mathematical_result_valid':False,'source_contract_clearance':False,'priority_audit_complete':False,'priority_clearance':False,'historical_novelty_or_firstness_established':False,'publication_ready':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':44,'published_count':28,'last_completed_PR':200,'remaining_required_steps':remain,'goal_complete':False}
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case);out[CASE+'RESEARCH_LOG.md']=(D/'INITIAL_RESEARCH_LOG.md').read_bytes()
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_completed'],p['advance_to_next_PR_authorized_now'])==(200,44,28,200,True,True)
 retired=[k for k in p if k.startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']]
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':200,'prior_phase':'actual_completed_before201_original_intake','values':{k:p[k] for k in retired}})
 for k in retired:p.pop(k,None)
 p['skipped_since_last_completion']=[]
 p.update(UTC=stamp,updated_UTC=stamp,current_PR=201,current_problem_id=5100014,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget=case['original_effort'],current_PR_workflow_percent=15,current_workflow_estimate_percent=15,current_status=status,current_completed=False,current_closed=False,current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=False,current_mathematics_cleared=False,current_mathematical_result_valid=False,current_independent_mathematical_audit_active=True,current_independent_mathematical_audit_families=3,current_independent_mathematical_audit_families_complete=0,current_independent_mathematical_audit_names=families,current_source_contract_clearance=False,current_source_provenance_warning=warning,current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr201_5100014/CURRENT_CASE_STATUS.json',current_exact_claim=claim,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,next_numeric_intake_cursor=201,conditional_next_numeric_intake_cursor=202,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=201,next_status_only_intake_performed=False,latest_ordered_intake_record='ordered_intakes_after_PR200_20261016/PR201_ORIGINAL_STATUS_INTAKE.json',latest_ordered_intake_records=['ordered_intakes_after_PR200_20261016/PR201_ORIGINAL_STATUS_INTAKE.json'],persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR200 actually completed;44completed/28published,last200. PR201 original claimed_solved eligibility and24-file custody frozen. Three NEW math families independently frozen and active; all clearances false. Literal signed-area outer-pedal product, every fixed M, primitive N2mod4 scope under adversarial review. Cursor201/conditional202/advancefalse.',program_snapshot_authority_condition='Intake15 postimage effective only after actual true-parent/fullforeignscope/everyselectedidentity acceptance. No mathematical, priority, publication, merge or next-intake authority.')
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR201 intake15percent: original HEAD90bdb85235979f2ffa7496b9b689036654e55200,24native files54661B, exact25path delta and originalclaimed_solved/1of5 authenticated. Root source-first signed-area contract and pre-candidate shoelace reduction recorded; three NEW materially distinct independent mathematical families frozen and active. Least-period convention and repeated-odd-orbit obstruction require explicit qualification. No math/source/priority/publication clearance. PR200 actually complete44completed/28published,last200; cursor201/conditional202/advancefalse, broader goal active.\n'
 for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=h.body_at(PREFIX+name,parent)+note.encode()
 return out
def selected(c,b,out):
 for k,z in out.items():
  assert k.startswith(CASE) or k in MUTABLE or k.startswith(PREVIOUS+'publication_lifecycle_01/completion01/') or k.startswith(PREFIX+'ordered_intakes_after_PR200_20261016/')
  if k in b and k not in MUTABLE:assert c.byte_pin(z)==b[k],k
 assert Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out)
 return {**b,**{k:c.byte_pin(z) for k,z in out.items()}}
def message(d):return 'Record PR201 immutable original custody and independent mathematical audits active\n\n44completed/28published,last200. Signed outer-pedal product for every fixed M and primitive N2mod4 under review; all clearances false.\nPR201 intake selected-map SHA256: '+d
def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex);co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex));assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for k,x in ex.items():assert h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),k
 assert h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and set(r['changed_paths'])<=set(r['overlay_paths'])
def prepare(c,h,rv,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);original(h);assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);dest=D/gen;dest.mkdir();raw=enc(ack);save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',raw);out[CASE+'intake_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=raw;ex=selected(c,inherited,out)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':z.decode()} for k,z in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'PR':201,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r));verify(c,h,r,ex);observed=h.api('git/ref/heads/main')['object']['sha'];save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':co,'expected_main':parent,'observed_MAIN':observed,'exact_trueparent_fullforeignscope_everyselectedidentity_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'all_clearances_false':True}));print(json.dumps({'expected_main':parent,'observed_main':observed,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))
def accept(c,h,rv,gen):
 base=baseline(c);d=D/gen;r=read(d/'PREPARATION.json');ack=read(d/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(h,r['expected_main'],r['UTC']);out[CASE+'intake_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(d/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out);verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(d/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'source_contract_clearance':False,'priority_clearance':False,'publication_ready':False,'case_percent':15,'fully_completed_count':44,'published_count':28,'last_completed_PR':200,'next_numeric_intake_cursor':201,'advance_to_next_PR_authorized_now':False,'goal_complete':False};save(d/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h,rv=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,rv,sys.argv[2])

