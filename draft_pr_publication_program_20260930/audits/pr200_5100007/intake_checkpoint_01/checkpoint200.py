"""PR200 original custody and active mathematical-review checkpoint; no ref move."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr200_5100007/';PREVIOUS=PREFIX+'audits/pr196_30004690/'
PRIOR=P/'audits/pr196_30004690/publication_lifecycle_01/completion01'
HEAD='379a959609958f1e28f68f1ab6e42970ca9d1641';MUTABLE={PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def read(p):return json.loads(p.read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 p=P/'audits/pr196_30004690/publication_lifecycle_01/finish196.py';sp=importlib.util.spec_from_file_location('completed196_lowlevel',p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);rv,c,h,n=v.load();h.m.TREE_CACHE_PATH=A/'INTAKE_PRIVATE_TREE_CACHE.json';return c,h,rv

def baseline(c):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json');x=read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['completion_metadata_accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN']
 assert r['commit']==a['checkpoint_commit']=='6c8b86db81962e9e89d180fd36c427eafab96645' and len(r['selected_files'])==a['selected_files']==1660
 assert r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='757d0d1398cf6877b9a3cfc908b7d98efec9af1936c398968e202841f58589ce'
 assert pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 assert (a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['advance_to_next_PR_authorized_now'])==(43,27,196,True)
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}

def original(h):
 p=h.api('pulls/200');assert p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False
 assert p['created_at']==p['updated_at']=='2026-10-01T05:03:51Z'

def overlay(h,parent,stamp):
 inputs=read(D/'INPUT_PINS.json');out={}
 for rel,x in inputs['safe_authored_inputs'].items():
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
  b=p.read_bytes();assert pin(b)==x,rel;out[CASE+rel]=b
 custody=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');assert custody['original_head']==HEAD and custody['original_QUEUE_status']=='claimed_solved' and len(custody['files'])==19
 for rel,x in custody['files'].items():
  b=out[CASE+'original_submitted_head/'+rel];assert pin(b)=={k:x[k] for k in ['bytes','sha256']} and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 out[CASE+'intake_checkpoint_01/INPUT_PINS.json']=(D/'INPUT_PINS.json').read_bytes();out[CASE+'intake_checkpoint_01/checkpoint200.py']=Path(__file__).read_bytes()
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:out[PREVIOUS+'publication_lifecycle_01/completion01/'+name]=(PRIOR/name).read_bytes()
 intake_dir=P/'ordered_intakes_after_PR196_20261015'
 for f in sorted(intake_dir.iterdir()):
  if f.is_file() and not f.is_symlink() and f.name!='PRIVATE_TREE_CACHE.json':
   assert f.stat().st_mode&0o777==0o444,f;out[PREFIX+'ordered_intakes_after_PR196_20261015/'+f.name]=f.read_bytes()
 intakepath=PREFIX+'ordered_intakes_after_PR196_20261015/PR200_ORIGINAL_STATUS_INTAKE.json'
 assert out[intakepath]==(A/'ORIGINAL_STATUS_INTAKE.json').read_bytes()
 families=['pr200_direct_geometry','pr200_algebra_reproduction','pr200_source_quantifiers'];status='ORIGINAL_CLAIMED_SOLVED_FROZEN_THREE_NEW_MATHEMATICAL_FAMILIES_ACTIVE_UNCLEARED'
 remain='Finish independent focal geometry/elliptic-function, algebra/direct-orbit reproduction and literal-source/quantifier audits; Root verification, then deep priority only if mathematics passes. No publication or merge clearance.'
 case={'UTC':stamp,'PR':200,'problem_id':5100007,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':'1 substantive original author turn; original metadata prior_campaign_attempt_found false, no model/effort attestation','original_QUEUE_effort_cell':'1/5','status':status,'case_percent':15,'exact_claim':'k115: for a fixed pair of nested nondegenerate confocal ellipses supporting primitive N=0mod4 Poncelet billiards, product of distances from successive boundary-tangent intersection vertices to either boundary-ellipse focus is phase invariant; primitive stars included. Cyclic elliptic-function divisor cancellation requires independent verification.','source_provenance_warning':'Literal arxiv2004.12497v11 defines two confocal ELLIPSES, Table2 rowk115 proof? at29Oct2020. Publisher2021 title differs; complete journal/source dependency mapping pending. Imported generic caustic/open triage does not establish broader scope or current worldwide openness.','original_archive_files':19,'independent_mathematical_families':families,'independent_mathematical_families_active':True,'mathematical_clearance':False,'mathematical_result_valid':False,'source_contract_clearance':False,'priority_audit_complete':False,'priority_clearance':False,'historical_novelty_or_firstness_established':False,'publication_ready':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':43,'published_count':27,'last_completed_PR':196,'remaining_required_steps':remain,'goal_complete':False}
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case);out[CASE+'RESEARCH_LOG.md']=(D/'INITIAL_RESEARCH_LOG.md').read_bytes()
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_completed'],p['advance_to_next_PR_authorized_now'])==(196,43,27,196,True,True)
 retired=[k for k in p if k.startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']]
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':196,'prior_phase':'actual_completed_before200_original_intake','values':{k:p[k] for k in retired}})
 for k in retired:p.pop(k,None)
 p['skipped_since_last_completion']=[197,198,199]
 p.update(UTC=stamp,updated_UTC=stamp,current_PR=200,current_problem_id=5100007,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget=case['original_effort'],current_PR_workflow_percent=15,current_workflow_estimate_percent=15,current_status=status,current_completed=False,current_closed=False,current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=False,current_mathematics_cleared=False,current_mathematical_result_valid=False,current_independent_mathematical_audit_active=True,current_independent_mathematical_audit_families=3,current_independent_mathematical_audit_families_complete=0,current_independent_mathematical_audit_names=families,current_source_contract_clearance=False,current_source_provenance_warning=case['source_provenance_warning'],current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr200_5100007/CURRENT_CASE_STATUS.json',current_exact_claim=case['exact_claim'],current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,next_numeric_intake_cursor=200,conditional_next_numeric_intake_cursor=201,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=200,next_status_only_intake_performed=False,latest_ordered_intake_record='ordered_intakes_after_PR196_20261015/PR200_ORIGINAL_STATUS_INTAKE.json',latest_ordered_intake_records=['ordered_intakes_after_PR196_20261015/PR'+str(i)+'_ORIGINAL_STATUS_INTAKE.json' for i in [197,198,199,200]],persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR196 actually completed;43completed/27published,last196. PR200 original exactclaimed_solved eligibility and19-file custody frozen; three NEW math families active, allclearancefalse. Literal source is confined to nested confocal ellipses; dated proof-gap metadata is not current priority evidence. Cursor200/conditional201/advancefalse.',program_snapshot_authority_condition='PR200 intake15 postimage effective only after actual true-parent/fullscope/all-current-selected-identities acceptance. No mathematical,priority,publication,merge or next-intake authority.')
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR200 intake15%: immutable original HEAD379a959609958f1e28f68f1ab6e42970ca9d1641,19native files, exact20path delta and originalclaimed_solved/1of5 effort frozen. After actual PR196 completion43completed/27published,last196, status-only197already_solved,198already_solved,199originalqueued skipped without mathematical review or PR action. PR200 three NEW independent mathematical families active; each instructed to freeze before favorable reports. Root source-first freeze before candidate records literal nested-confocal-ELLIPSE scope, primitiveN/winding/period/divisor challenges and independent tangent-locus derivation. No math/source/priority/publication clearance. Cursor200/conditional201/advancefalse; broader goal active.\n'
 for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=h.body_at(PREFIX+name,parent)+note.encode()
 return out

def selected(c,b,out):
 for path,bod in out.items():
  assert path.startswith(CASE) or path in MUTABLE or path.startswith(PREVIOUS+'publication_lifecycle_01/completion01/') or path.startswith(PREFIX+'ordered_intakes_after_PR196_20261015/')
  if path in b and path not in MUTABLE:assert c.byte_pin(bod)==b[path],path
 assert 'unsolved_math_prioritization/QUEUE.md' not in out and not any(x.startswith('unsolved_math_prioritization/attempts/') for x in out)
 return {**b,**{path:c.byte_pin(bod) for path,bod in out.items()}}
def message(d):return 'Record PR200 immutable original custody and three independent mathematical audits active\n\n43completed/27published,last196. Literal confocal-ellipse scope and primitive-period quantifiers under review; no mathematical or publication clearance.\nPR200 intake selected-map SHA256: '+d

def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex);co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex));assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for path,x in ex.items():assert h.lookup(r['tree'],path)==('100644','blob',x['git_blob']),path
 assert h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and set(r['changed_paths'])<=set(r['overlay_paths'])

def prepare(c,h,rv,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=rv.v.queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);original(h);assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);dest=D/gen;dest.mkdir();raw=enc(ack);save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',raw);out[CASE+'intake_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=raw;ex=selected(c,inherited,out)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':path,'mode':'100644','type':'blob','content':bod.decode()} for path,bod in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(path for path,x in ex.items() if h.lookup(pt,path)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r));verify(c,h,r,ex);observed=h.api('git/ref/heads/main')['object']['sha'];pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':co,'expected_main':parent,'observed_MAIN':observed,'exact_true_parent_full_foreign_tree_all_selected_identities_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'all_clearances_false':True};save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre));print(json.dumps({'expected_main':parent,'observed_main':observed,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))

def accept(c,h,rv,gen):
 base=baseline(c);d=D/gen;r=read(d/'PREPARATION.json');ack=read(d/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],'unsolved_math_prioritization/QUEUE.md':ack['current_QUEUE']};out=overlay(h,r['expected_main'],r['UTC']);out[CASE+'intake_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(d/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out);verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=rv.v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);original(h)
 for path,bod in out.items():assert c.byte_pin(bod)==ex[path] and h.lookup(tree,path)==('100644','blob',ex[path]['git_blob'])
 body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(d/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':200,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'source_contract_clearance':False,'priority_clearance':False,'publication_ready':False,'case_percent':15,'fully_completed_count':43,'published_count':27,'last_completed_PR':196,'next_numeric_intake_cursor':200,'advance_to_next_PR_authorized_now':False,'goal_complete':False};save(d/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h,rv=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,rv,sys.argv[2])
