"""PR196 original custody and active mathematical-review checkpoint; no ref move."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr196_30004690/';PREVIOUS=PREFIX+'audits/pr195_30004601/'
PRIOR=P/'audits/pr195_30004601/publication_lifecycle_01/completion01'
HEAD='a229ac722a3b1733bcb590a5f796b4a52f68cc73';MUTABLE={PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def read(p):return json.loads(p.read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 p=P/'audits/pr195_30004601/publication_lifecycle_01/finish195.py';assert pin(p.read_bytes())=={'bytes':19382,'sha256':'2826de94c05ce15b181e007b95712519139c26ad57fd253ee36fe9d31aee4ad5'}
 s=importlib.util.spec_from_file_location('approved195completed_lowlevel',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);c,h,n=m.load();h.m.TREE_CACHE_PATH=A/'INTAKE_PRIVATE_TREE_CACHE.json';return c,h

def baseline(c):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json');assert a['accepted'] is True and a['completion_metadata_accepted'] is True and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True
 assert r['commit']==a['checkpoint_commit']=='328a76238a7b9e003faa104c0ee8574e7655b321' and len(r['selected_files'])==a['selected_files']==1485
 assert r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='7f6043a0d309bbb527828fa83be797f8416057351e54e4f5be2c8f702ec545b5'
 assert (a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['advance_to_next_PR_authorized_now'])==(42,26,195,True)
 return r

def original(h):
 p=h.api('pulls/196');assert p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False
 assert p['created_at']==p['updated_at']=='2026-10-01T04:51:43Z'

def overlay(h,parent,stamp):
 inputs=read(D/'INPUT_PINS.json');out={}
 for rel,x in inputs['safe_authored_inputs'].items():
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
  b=p.read_bytes();assert pin(b)==x,rel;out[CASE+rel]=b
 custody=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');assert custody['original_head']==HEAD and custody['original_QUEUE_status']=='claimed_solved' and len(custody['files'])==19
 for rel,x in custody['files'].items():
  b=out[CASE+'original_submitted_head/'+rel];assert pin(b)=={k:x[k] for k in ['bytes','sha256']} and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 out[CASE+'intake_checkpoint_01/INPUT_PINS.json']=(D/'INPUT_PINS.json').read_bytes();out[CASE+'intake_checkpoint_01/checkpoint196.py']=Path(__file__).read_bytes()
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json']:out[PREVIOUS+'publication_lifecycle_01/completion01/'+name]=(PRIOR/name).read_bytes()
 intake=read(A/'ORIGINAL_STATUS_INTAKE.json');intakepath=PREFIX+'ordered_intakes_after_PR195_20261015/PR196_ORIGINAL_STATUS_INTAKE.json';out[intakepath]=enc(intake)
 families=['pr196_contact_geometry_adversary','pr196_legendre_regular_adversary','pr196_original_source_adversary'];status='ORIGINAL_CLAIMED_SOLVED_FROZEN_THREE_NEW_MATHEMATICAL_FAMILIES_ACTIVE_UNCLEARED'
 remain='Finish independent geometry/potential-theory, Legendre-regularity and literal-source contract audits; Root adversarial verification and source normalization, then deep priority audit if mathematics passes. No publication or merge clearance.'
 case={'UTC':stamp,'PR':196,'problem_id':30004690,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':'4 recovered substantive author turns; historical interrupted consumption unknown/nonzero, not reset','original_QUEUE_effort_cell':'4/5','status':status,'case_percent':15,'exact_claim':'Smooth strictly Kahler fibre boundary data on P1 times circle whose weak Bedford–Taylor homogeneous CMA solution fails to be twice differentiable at a genuine interior point, using finite-time positive-length Hele–Shaw contact arc, strict Green slope gap and Legendre curvature jump.','source_provenance_warning':'Original OWR contribution announces/sketches interior construction and qualifies its smoothness step; imported open/unresolved triage label is not literal source evidence. Strict-positive candidate/full proof and source relation under review.','original_archive_files':19,'independent_mathematical_families':families,'independent_mathematical_families_active':True,'mathematical_clearance':False,'mathematical_result_valid':False,'source_contract_clearance':False,'priority_audit_complete':False,'priority_clearance':False,'historical_novelty_or_firstness_established':False,'publication_ready':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':42,'published_count':26,'last_completed_PR':195,'remaining_required_steps':remain,'goal_complete':False}
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case);out[CASE+'RESEARCH_LOG.md']=(D/'INITIAL_RESEARCH_LOG.md').read_bytes()
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_completed'],p['advance_to_next_PR_authorized_now'])==(195,42,26,195,True,True)
 retired=[k for k in p if k.startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']]
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':195,'prior_phase':'actual_completed_before196_original_intake','values':{k:p[k] for k in retired}})
 for k in retired:p.pop(k,None)
 p.update(UTC=stamp,updated_UTC=stamp,current_PR=196,current_problem_id=30004690,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget=case['original_effort'],current_PR_workflow_percent=15,current_workflow_estimate_percent=15,current_status=status,current_completed=False,current_closed=False,current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=False,current_mathematics_cleared=False,current_mathematical_result_valid=False,current_independent_mathematical_audit_active=True,current_independent_mathematical_audit_families=3,current_independent_mathematical_audit_families_complete=0,current_independent_mathematical_audit_names=families,current_source_contract_clearance=False,current_source_provenance_warning=case['source_provenance_warning'],current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr196_30004690/CURRENT_CASE_STATUS.json',current_exact_claim=case['exact_claim'],current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,next_numeric_intake_cursor=196,conditional_next_numeric_intake_cursor=197,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=196,next_status_only_intake_performed=False,latest_ordered_intake_record='ordered_intakes_after_PR195_20261015/PR196_ORIGINAL_STATUS_INTAKE.json',latest_ordered_intake_records=['ordered_intakes_after_PR195_20261015/PR196_ORIGINAL_STATUS_INTAKE.json'],persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR195 actually completed;42completed/26published,last195. PR196 original exactclaimed_solved eligibility and19-file custody frozen; three NEW math families active, allclearancefalse. Literal source announces/sketches interior route; imported open metadata untrusted. Cursor196/conditional197/advancefalse.',program_snapshot_authority_condition='PR196 intake15 postimage effective only after actual true-parent/fullscope/all-current-selected-identities acceptance. No mathematical,priority,publication,merge or next-intake authority.')
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR196 intake15%: original HEADa229ac722a3b1733bcb590a5f796b4a52f68cc73 and19native files frozen; submitted20-commit range/20path scope checked, finalparentQUEUEmetadata-only. Originalclaimed_solved; historical unknown/nonzero interrupted effort plus4recovered turns preserved. Three NEW independent math families active, each froze mechanism before favorable reports. Root initial proof/source checks note originalOWR already announces/sketches interior construction with a qualified smoothness step; imported open triage is too strong. All math/source/priority/publication clearancefalse.42completed/26published,last195;cursor196/advancefalse; broader goal active.\n'
 for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=h.body_at(PREFIX+name,parent)+note.encode()
 return out

def selected(c,b,out):
 for path,bod in out.items():
  assert path.startswith(CASE) or path in MUTABLE or path.startswith(PREVIOUS+'publication_lifecycle_01/completion01/') or path==PREFIX+'ordered_intakes_after_PR195_20261015/PR196_ORIGINAL_STATUS_INTAKE.json'
  if path in b and path not in MUTABLE:assert c.byte_pin(bod)==b[path],path
 assert 'unsolved_math_prioritization/QUEUE.md' not in out and not any(x.startswith('unsolved_math_prioritization/attempts/') for x in out)
 return {**b,**{path:c.byte_pin(bod) for path,bod in out.items()}}
def message(d):return 'Record PR196 immutable original custody and three independent mathematical audits active\n\n42completed/26published,last195. Source open-status characterization requires correction; no mathematical or publication clearance.\nPR196 intake selected-map SHA256: '+d

def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex);co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex));assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for path,x in ex.items():assert h.lookup(r['tree'],path)==('100644','blob',x['git_blob']),path
 assert h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and set(r['changed_paths'])<=set(r['overlay_paths'])

def prepare(c,h,gen):
 base=baseline(c);parent=h.api('git/ref/heads/main')['object']['sha'];pt=c.selected_current(h,parent,base['selected_files'],base['tree']);original(h);assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();out=overlay(h,parent,stamp);ex=selected(c,base['selected_files'],out);dest=D/gen;dest.mkdir(exist_ok=False)
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':path,'mode':'100644','type':'blob','content':bod.decode()} for path,bod in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(path for path,x in ex.items() if h.lookup(pt,path)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r));verify(c,h,r,ex);assert h.api('git/ref/heads/main')['object']['sha']==parent;print(json.dumps({'expected_main':parent,'commit':co,'tree':tree,'selected':len(ex),'changed':len(r['changed_paths'])}))

def accept(c,h,gen):
 base=baseline(c);r=read(D/gen/'PREPARATION.json');out=overlay(h,r['expected_main'],r['UTC']);ex=selected(c,base['selected_files'],out);verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha'];assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];tree=c.selected_current(h,main,ex,r['tree']);original(h)
 for path,bod in out.items():assert c.byte_pin(bod)==ex[path] and h.lookup(tree,path)==('100644','blob',ex[path]['git_blob'])
 a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':196,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':False,'source_contract_clearance':False,'priority_clearance':False,'publication_ready':False,'case_percent':15,'fully_completed_count':42,'published_count':26,'last_completed_PR':195,'next_numeric_intake_cursor':196,'advance_to_next_PR_authorized_now':False,'goal_complete':False};save(D/gen/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h=load();{'prepare':prepare,'accept':accept}[sys.argv[1]](c,h,sys.argv[2])
