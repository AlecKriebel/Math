"""Inert bounded PR195 intake checkpoint. Root alone executes prepare/adopt/accept."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr195_30004601/';HEAD='e776a961293116775fed2cb2a3019d577b84c04a';QUEUE='unsolved_math_prioritization/QUEUE.md'
PROGRAMME={PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
PRIOR=P/'audits/pr193_30004563/actual_completion_reconciliation_preparation_01/generation_receipt01'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def read(p):return json.loads(Path(p).read_bytes())
def encoded(j):return (json.dumps(j,indent=2)+'\n').encode()
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fresh(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 for n,x in read(D/'SOURCE_INPUTS.json')['utility_pins'].items():require(pin(P/n)==x,'Approved low-level source changed '+n)
 def module(name,p):
  s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 c=module('byte_current_helpers_only',P/'audits/pr191_5000005/lifecycle_common.py');h=module('native_objects_only',P/'audits/pr190_5000007/prepare_final_scoped_merge.py');h.m.TREE_CACHE_PATH=A/'INTAKE_PRIVATE_TREE_CACHE.json';return c,h

def sources():
 i=read(D/'SOURCE_INPUTS.json');out={}
 for n,x in i['public_files'].items():
  p=P/n;require(pin(p)==x and not p.is_symlink(),'Pinned public intake source changed '+n);out[PREFIX+n]=p.read_bytes()
 for x in read(D/'FINAL_SEAL.json')['manifest']:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Own sealed intake source changed')
 for n in read(D/'PUBLIC_SAFE_ALLOWLIST.json')['files']:out[PREFIX+D.relative_to(P).as_posix()+'/'+n]=(D/n).read_bytes()
 j=read(D/'CASE_BASELINE20.json');require(j['PR']==195 and j['original_head']==HEAD and j['case_percent']==20 and j['mathematical_clearance'] is False and j['priority_audit_complete'] is False and j['publication_ready'] is False and j['completed'] is False,'Initial20 snapshot changed');out[CASE+'CURRENT_CASE_STATUS.json']=(D/'CASE_BASELINE20.json').read_bytes();out[CASE+'RESEARCH_LOG.md']=(D/'CASE_LOG_BASELINE20.md').read_bytes()
 custody=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');require(custody['original_head']==HEAD and len(custody['files'])==23,'Original23 custody differs')
 for n,x in custody['files'].items():require(pin(A/'original_submitted_head'/n)=={k:x[k] for k in ['bytes','sha256']},'Original archived body drift '+n)
 return out

def verify_object(c,h,r,expected,message):
 require(r['selected_files']==expected and r['selected_map_sha256']==c.selected_digest(expected),'Exact combined map changed/pruned');co=h.api('git/commits/'+r['commit']);pt=h.api('git/commits/'+r['expected_main'])['tree']['sha'];require(co['tree']['sha']==r['tree'] and pt==r['parent_tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']] and co['message']==message,'True parent/tree/operative message differs');h.m.m.h.warm_selected_directories([pt,r['tree']],expected)
 for n,x in expected.items():require(h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Prepared selected identity differs '+n)
 changed={n for n,x in expected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob'])};require(changed==set(r['changed_paths'])==h.changed_leaves(pt,r['tree']) and changed<=set(r['overlay_paths']),'Full tree has foreign/undeclared delta')

def prior_message(digest):return 'Record PR193 actual completed metadata from prior factual receipt;41completed/25published\n\n10.5281/zenodo.23392409; scientific/package/original/QUEUE bytes preserved; actual native completion metadata reconciled.194 status-only intake only after own actual checkpoint acceptance; broader goal active.\nPR193 actual-completion selected-map SHA256: '+digest

def row_id(line):
 cells=line.split('|');v=cells[2].strip().split() if len(cells)>3 else [];return int(v[0]) if v and v[0].isdigit() else None

def baseline(c,h,current):
 sources();r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'CHECKPOINT_ACCEPTANCE.json');pm=read(PRIOR/'ROOT_PRE_MOVE_VERIFICATION.json');expected=r['selected_files'];require(len(expected)==1258 and r['commit']=='44cf280eb6468af9ae17d17120d23709cabad4c6','Prior exact1258 map/commit differs');verify_object(c,h,r,expected,prior_message(c.selected_digest(expected)))
 require(a['accepted'] is True and a['status']=='ACTUAL_PR193_FINAL_RECEIPT_NATIVE_METADATA_RECONCILIATION_CHECKPOINT_ACCEPTED' and a['checkpoint_commit']==r['commit'] and a['sole_parent']==r['expected_main'] and a['selected_files']==1258 and a['selected_map_sha256']==c.selected_digest(expected) and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and (a['fully_completed_count'],a['published_count'],a['last_completed_PR'])==(41,25,193) and a['next_status_only_intake_authorized'] is True and a['goal_complete'] is False,'Prior actual own-completion acceptance differs')
 require(pm['commit']==r['commit'] and pm['expected_main']==r['expected_main'] and pm['tree']==r['tree'] and pm['selected']==1258 and pm['sole_parent_verified'] is True and pm['full_changed_leaf_scope_verified'] is True and pm['combined_selected_identities_verified'] is True and pm['MAIN_moved'] is False,'Prior Root pre-move receipt differs');require(c.selected_current(h,a['main_observed'],expected,r['tree'])==a['actual_tree'],'Prior actual observed1258 identities/tree differ');require(h.api('compare/'+r['commit']+'...'+a['main_observed'])['status'] in ['identical','ahead'],'Prior accepted checkpoint ancestry differs')
 g=read(A/'ROOT_INTAKE_REVIEWED_INHERITED_QUEUE_01.json');require(g['historical_checkpoint_main']==a['main_observed'] and g['historical_queue_pin']==expected[QUEUE] and g['unchanged_own_problem_ids']==[30004563,30004601] and g['Root_full_diff_read'] is True and g['all_other_selected_identities_unchanged'] is True and g['mutation_performed'] is False and g['QUEUE_overlay_authorized'] is False,'Root reviewed QUEUE inheritance differs');old=h.body_at(QUEUE,a['main_observed']);new=h.body_at(QUEUE,g['observed_main']);require(c.byte_pin(old)==g['historical_queue_pin'] and c.byte_pin(new)==g['current_queue_pin'],'Exact historical/current QUEUE pin differs');before=old.decode().splitlines(keepends=True);after=new.decode().splitlines(keepends=True);delta=[{'problem_id':row_id(x),'before':x,'after':y} for x,y in zip(before,after) if x!=y];require(len(before)==len(after) and delta==g['exact_changed_lines'] and [x['problem_id'] for x in delta]==g['changed_foreign_problem_ids'] and all(x['problem_id'] not in g['unchanged_own_problem_ids'] and x['problem_id']==row_id(x['after']) for x in delta),'QUEUE changes exceed Root-reviewed foreign lines')
 for problem in g['unchanged_own_problem_ids']:
  own=[x for x in before if row_id(x)==problem];require(len(own)==1 and own==[x for x in after if row_id(x)==problem],'Own193/195 QUEUE row changed')
 inherited={**expected,QUEUE:g['current_queue_pin']};require(c.selected_current(h,g['observed_main'],inherited,g['observed_tree'])==g['observed_tree'],'Root-reviewed current inherited full1258 identity map differs');require(c.byte_pin((A/'ROOT_PRIOR_PROGRAMME_SNAPSHOT_01.json').read_bytes())==g['progress_snapshot_pin']==expected[PREFIX+'CURRENT_PROGRESS.json'],'Root prior programme snapshot differs')
 main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Prior193 own checkpoint not on current MAIN')
 if current:c.selected_current(h,main,inherited,g['observed_tree'])
 return inherited,main,r,a

def original(h):
 p=h.api('pulls/195');require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False,'Original195 HEAD/open draft state differs')

def programme(before,stamp):
 require((before['fully_completed_count'],before['published_count'],before['last_completed_PR'],before['dated_eligible_total'])==(41,25,193,99) and before['current_PR']==193,'True-parent prior193/census differs');require(len(set(before['fully_completed_eligible_PRs']))==len(before['fully_completed_eligible_PRs'])==41 and len(set(before['published_PRs']))==len(before['published_PRs'])==25 and 193 in before['fully_completed_eligible_PRs'] and 195 not in before['fully_completed_eligible_PRs'] and 195 not in before['published_PRs'],'Prior unique completed/published census differs');j=copy.deepcopy(before)
 retired=[k for k in before if k.startswith(('current_','next_','conditional_','active_','actual_factual_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','completion_metadata_checkpoint_pending_at_snapshot','remaining_current_step','next_step','latest_ordered_intake_record']]
 j.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':193,'prior_phase':'actual_completed_before_PR195_initial_intake','values':{k:copy.deepcopy(before[k]) for k in retired}})
 for k in retired:j.pop(k,None)
 j.update(UTC=stamp,updated_UTC=stamp,current_PR=195,current_problem_id=30004601,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget='prior unknown; 1 recovered',current_PR_workflow_percent=20,current_workflow_estimate_percent=20,current_status='INITIAL_INTAKE_NEW_MATHEMATICAL_AUDITS_ACTIVE_UNCLEARED',current_completed=False,current_closed=False,current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=False,current_mathematics_cleared=False,current_mathematical_result_valid=False,current_independent_mathematical_audit_active=True,current_independent_mathematical_audit_families=3,current_independent_mathematical_audit_families_complete=0,current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr195_30004601/CURRENT_CASE_STATUS.json',current_exact_claim=read(D/'CASE_BASELINE20.json')['exact_claim'],current_remaining_required_steps='Three independent mathematical audits and Root authentication; deep priority audit; package and successive NEW whole-package reviews; actual publication/tracker/originalHEAD-safe merge/factual acceptance.',next_numeric_intake_cursor=195,conditional_next_numeric_intake_cursor=196,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=195,next_status_only_intake_performed=False,latest_ordered_intake_record='status_intakes_after_pr193/PR195_ORIGINAL_STATUS_INTAKE.json',skipped_PR194_status_only='unsolved; SKIP_UNTOUCHED_NON_CLAIMED_SOLVED; no mathematics or disposition performed',remaining_current_step='Complete current195 independent mathematical validation; no clearance or publication authority.',next_step='Continue current195 audits; no196 intake before actual195 completion.',program_snapshot_authority_condition='Initial20% intake snapshot effective only after this checkpoint actual true-parent/full-delta/all-current-identities acceptance; no scientific/publication or next-intake authority.',program_snapshot_semantics='Current195 original claimed_solved, prior effort unknown plus1 recovered; three NEW mathfamilies active and uncleared.194 skipped untouched.41completed/25published,last193,dated99; cursor195/conditional196/advancefalse; broader goal active.',fully_completed_fraction_percent=41.4,workflow_estimate_percent=41.4,workflow_estimate_definition='41/dated99 completed,25 published; dated denominator is not a fresh eligibility census.',peer_pause_or_exclusive_writer_window_assumed=False,persistent_goal_complete=False)
 require({k:v for k,v in before.items() if k.startswith(('last_completed_','last_published_'))}=={k:v for k,v in j.items() if k.startswith(('last_completed_','last_published_'))},'Prior193 completion metadata changed');return j

def overlay(h,parent,stamp):
 out=sources();before=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));out[PREFIX+'CURRENT_PROGRESS.json']=encoded(programme(before,stamp));note='\n'+stamp+' — PR195 initial intake20%: immutable original claimed_solved HEAD archived23files; prior effort unknown plus1 recovered. Three NEW mathematical families active, no mathematical/priority/publication clearance.194 unsolved skipped untouched.41completed/25published,last193; cursor195/conditional196/advancefalse. No QUEUE/native/PR mutation or196 intake; broader goal active.\n'
 for name in [PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[name]=h.body_at(name,parent)+note.encode()
 return out

def selected(c,base,out):
 require(QUEUE not in out and all(n.startswith(CASE) or n.startswith(PREFIX+'status_intakes_after_pr193/') or n in PROGRAMME or n.startswith(PREFIX+'audits/pr193_30004563/') for n in out),'Unowned intake overlay')
 for n,b in out.items():
  if n in base and n not in PROGRAMME:require(c.byte_pin(b)==base[n],'Protected prior identity would change '+n)
 return {**base,**{n:c.byte_pin(b) for n,b in out.items()}}

def message(digest):return 'Record PR195 initial20% intake;41completed/25published,last193\n\nOriginal claimed_solved; three NEW mathematical families active, all clearance false.194 unsolved skipped untouched. No QUEUE/native/PR changes or196 intake.\nPR195 intake selected-map SHA256: '+digest

def prepare(c,h,gen):
 base,parent,_,_=baseline(c,h,True);original(h);stamp=now();out=overlay(h,parent,stamp);expected=selected(c,base,out);dest=D/('checkpoint_'+gen);dest.mkdir(exist_ok=False);pt=h.api('git/commits/'+parent)['tree']['sha'];entries=[{'path':n,'mode':'100644','type':'blob','content':b.decode()} for n,b in sorted(out.items())];tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries});co=h.api('git/commits','POST',{'message':message(c.selected_digest(expected)),'tree':tree['sha'],'parents':[parent]});h.m.m.h.warm_selected_directories([pt,tree['sha']],expected);changed=sorted(n for n,x in expected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob']));r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree['sha'],'commit':co['sha'],'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':changed,'MAIN_moved':False};fresh(dest/'PREPARATION.json',encoded(r));verify_object(c,h,r,expected,message(c.selected_digest(expected)));require(QUEUE not in changed,'QUEUE changed');original(h);require(h.api('git/ref/heads/main')['object']['sha']==parent,'MAIN advanced; preserve generation/retry fresh');print(json.dumps({'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected':len(expected),'changed':len(changed),'MAIN_moved':False}))

def accept(c,h,gen):
 r=read(D/('checkpoint_'+gen)/'PREPARATION.json');base,main,prior,_=baseline(c,h,False);c.selected_current(h,r['expected_main'],base,prior['tree']);out=overlay(h,r['expected_main'],r['UTC']);expected=selected(c,base,out);require(r['overlay_paths']==sorted(out) and QUEUE not in r['changed_paths'],'Intake overlay/QUEUE scope differs');verify_object(c,h,r,expected,message(c.selected_digest(expected)));require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Intake candidate not on MAIN');tree=c.selected_current(h,main,expected,r['tree'])
 for n,b in out.items():require(h.body_at(n,main)==b,'Fresh full intake body differs '+n)
 require(c.byte_pin(h.body_at(QUEUE,main))==base[QUEUE],'Protected inherited QUEUE body changed');original(h);a={'UTC':now(),'PR':195,'original_head':HEAD,'accepted':True,'status':'ACTUAL_PR195_INITIAL20_TRUE_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED','checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(expected),'selected_map_sha256':c.selected_digest(expected),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_output_bodies_verified':True,'QUEUE_native_PR_unchanged':True,'fully_completed_count':41,'published_count':25,'last_completed_PR':193,'case_percent':20,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'next_numeric_intake_cursor':195,'conditional_next_numeric_intake_cursor':196,'advance_to_next_PR_authorized_now':False,'goal_complete':False};fresh(D/('checkpoint_'+gen)/'INTAKE_CHECKPOINT_ACCEPTANCE.json',encoded(a));print(json.dumps(a))

if __name__=='__main__':
 require(sys.dont_write_bytecode,'Use Python -B');c,h=load();(prepare if sys.argv[1]=='prepare' else accept)(c,h,sys.argv[2])
