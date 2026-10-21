"""PROPOSED PR193 intake checkpoint; inert import, no ref/disposition/intake actions.

Explicit future prepare creates native objects only. Root separately adopts the
candidate; accept verifies current MAIN. Original submission code is data only.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr193_30004563/'
HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81';NATIVE='unsolved_math_prioritization/attempts/30004563/'
PREV='audits/pr191_5000005/final_receipt_checkpoint_preparation_01/'
PROG=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'];QUEUE='unsolved_math_prioritization/QUEUE.md'
def require(ok,message):
 if not ok:raise RuntimeError(message)
def read(p):return json.loads(Path(p).read_text())
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encoded(j):return (json.dumps(j,indent=2)+'\n').encode()
def fresh(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def load():
 inputs=read(D/'SOURCE_INPUTS.json');root=P/'audits/pr191_5000005';require(pin(root/'lifecycle_common.py')==inputs['installed191_common'] and pin(root/'ROOT_PUBLICATION_GATE.json')==inputs['installed191_gate'] and pin(P/PREV/'prepare_checkpoint.py')==inputs['prior_checkpoint_helper'],'Approved prior utilities changed')
 return module('accepted191_for_intake193',root/'lifecycle_common.py'),module('accepted191_receipt_checkpoint',P/PREV/'prepare_checkpoint.py')
def original_open(h):
 p=h.api('pulls/193');require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and not p['merged'],'Original PR193 head/open/draft changed')
def safe_path(n):
 require(isinstance(n,str) and not Path(n).is_absolute() and '..' not in Path(n).parts and not any(v in n.lower() for v in ['private_sources','tree_cache','__pycache__']) and Path(n).suffix.lower() not in ['.pdf','.png','.jpg','.jpeg'],'Nonpublic input path')
 p=P/n;require(p.resolve().is_relative_to(P.resolve()) and not p.is_symlink(),'Unsafe public input path');return p

def sources(c):
 inputs=read(D/'SOURCE_INPUTS.json');out={}
 for n,x in inputs['public_programme_relative_files'].items():
  p=safe_path(n);require(pin(p)==x,'Pinned intake source changed '+n);out[PREFIX+n]=p.read_bytes()
 seal=read(D/'FINAL_SEAL.json')
 for x in seal['manifest']:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Helper source seal drift')
 for n in read(D/'PUBLIC_SAFE_ALLOWLIST.json')['files']:
  p=D/n;require(p.parent==D and p.is_file() and not p.is_symlink(),'Unsafe helper source');out[PREFIX+D.relative_to(P).as_posix()+'/'+n]=p.read_bytes()
 return out

def queue_row_id(line):
 cells=line.split('|')
 return int(cells[2].strip().split()[0]) if len(cells)>3 and re.fullmatch('[0-9]+',cells[2].strip().split()[0] if cells[2].strip() else '') else None

def reviewed_queue_bytes(c,before,after,q):
 """Only the exact two Root-reviewed foreign-row replacements are permitted."""
 require(c.byte_pin(before)==q['prior_identity'] and c.byte_pin(after)==q['identity'],'Reviewed historical/current QUEUE byte pin differs')
 old=before.decode().splitlines(keepends=True);new=after.decode().splitlines(keepends=True);require(len(old)==len(new),'Reviewed QUEUE line inventory differs')
 delta=[{'problem_id':queue_row_id(b),'before':b,'after':a} for b,a in zip(old,new) if b!=a]
 require(delta==q['exact_changed_lines'] and [x['problem_id'] for x in delta]==[30005244,30006628] and all(queue_row_id(x['after'])==x['problem_id'] for x in delta),'QUEUE changes exceed exact reviewed two foreign rows')
 for pid in [5000005,30004563]:
  rows=[b for b in old if queue_row_id(b)==pid];require(len(rows)==1 and rows==[b for b in new if queue_row_id(b)==pid],'Own191/193 QUEUE row changed')

def inherited_baseline(c,h,r,a,inputs):
 q=inputs['reviewed_inherited_queue'];e=read(A/'ROOT_INTAKE_FOREIGN_DRIFT_01.json');p=read(A/'ROOT_REVIEWED_INHERITED_QUEUE_PIN_01.json')
 require(q['path']==QUEUE and q['source_MAIN']=='cd00326651f2f9c0ffdd0e250dbeaae8148fcf89' and q['identity']=={'bytes':432443,'sha256':'0aac194fd38a9347bc34d01e2a9d501869eb21a66f7f4bb68512145f7874d40d','git_blob':'db667ab8e5eab5cabe907f00d7ba2eebba496a3f'} and q['prior_identity']==r['selected_files'][QUEUE] and q['changed_foreign_problem_ids']==[30005244,30006628] and q['unchanged_own_problem_ids']==[5000005,30004563] and q['QUEUE_is_inherited_not_written'] is True,'Unapproved inherited QUEUE baseline')
 require(e['MAIN']==p['observed_main']==q['source_MAIN'] and e['tree']==q['source_tree'] and e['prior_checkpoint']==r['commit'] and len(e['drift'])==1 and e['drift'][0]['path']==p['path']==QUEUE and e['drift'][0]['prior_identity']==q['prior_identity'] and e['drift'][0]['actual_identity']==['100644','blob',q['identity']['git_blob']] and {k:p[k] for k in ['bytes','sha256','git_blob']}==q['identity'] and p['mode']=='100644' and p['reviewed_only_foreign_rows']==[30005244,30006628] and p['own193_and191_rows_unchanged'] is True and p['QUEUE_mutation_performed'] is False,'Root reviewed QUEUE receipts disagree')
 require(h.api('git/commits/'+q['source_MAIN'])['tree']['sha']==q['source_tree'],'Reviewed QUEUE source tree differs');reviewed_queue_bytes(c,h.body_at(QUEUE,a['main_observed']),h.body_at(QUEUE,q['source_MAIN']),q)
 inherited={**r['selected_files'],QUEUE:q['identity']};require(len(inherited)==937 and {n for n in inherited if inherited[n]!=r['selected_files'][n]}=={QUEUE},'Inherited baseline changes more than QUEUE');c.selected_current(h,q['source_MAIN'],inherited,q['source_tree']);return inherited

def context(c,old,current=True):
 inputs=read(D/'SOURCE_INPUTS.json');h=c.helpers();original_open(h);sources(c)
 r=read(P/PREV/'checkpoint_receipt01/CHECKPOINT_PREPARATION.json');a=read(P/PREV/'checkpoint_receipt01/CHECKPOINT_ACCEPTANCE.json');fa=read(P/'audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json')
 require(pin(P/'audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json')==r['factual_receipt'],'Prior factual receipt changed');old.verify_candidate(c,h,r,r['selected_files'],fa)
 require(a['status']=='ACTUAL_PR191_FINAL_RECEIPT_CHECKPOINT_PARENT_FULL_DELTA_CURRENT_IDENTITIES_ACCEPTED' and a['checkpoint_commit']==r['commit']==inputs['prior_checkpoint_commit'] and a['main_observed']==inputs['prior_observed_MAIN'] and a['selected_files']==len(r['selected_files'])==937 and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and (a['fully_completed_count'],a['published_count'],a['next_numeric_intake_cursor'])==(40,24,192) and a['goal_complete'] is False,'Prior actual completion/cursor authority differs')
 c.selected_current(h,a['main_observed'],r['selected_files'],r['tree']);main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Prior accepted checkpoint not on MAIN')
 inherited=inherited_baseline(c,h,r,a,inputs)
 if current:c.selected_current(h,main,inherited,inputs['reviewed_inherited_queue']['source_tree'])
 status=read(A/'CURRENT_CASE_STATUS.json');i192=read(P/'status_intakes_after_pr191/PR192_ORIGINAL_STATUS_INTAKE.json');i193=read(P/'status_intakes_after_pr191/PR193_ORIGINAL_STATUS_INTAKE.json');manifest=read(A/'ORIGINAL_FILE_MANIFEST.json')
 require((status['PR'],status['problem_id'],status['original_head'],status['case_percent'],status['original_QUEUE_status'],status['original_effort'])==(193,30004563,HEAD,20,'claimed_solved','2/5') and all(status[k] is False for k in ['mathematical_clearance','priority_clearance','publication_ready','actual_Zenodo_published','actual_tracker_updated','actual_original_PR_merged','goal_complete']),'Current case is not the pinned unreviewed20% intake')
 require(i192['PR']==192 and i192['original_QUEUE_status']=='already_solved' and i192['decision']=='SKIP_UNTOUCHED_NON_CLAIMED_SOLVED' and i192['mathematical_review_performed'] is False and i192['PR_or_QUEUE_or_native_attempt_mutations']==0,'PR192 must remain status-only skip')
 require((i193['PR'],i193['problem_id'],i193['original_head'],i193['original_QUEUE_status'],i193['original_effort'])==(193,30004563,HEAD,'claimed_solved','2/5') and i193['mathematical_review_performed'] is False and not (P/'status_intakes_after_pr191/PR194_ORIGINAL_STATUS_INTAKE.json').exists(),'Wrong/unqualified intake or later194 intake')
 require(manifest['original_head']==HEAD and len(manifest['files'])==19,'Original19 custody differs');co=h.api('git/commits/'+HEAD);require(co['tree']['sha']==manifest['original_commit_tree'] and [x['sha'] for x in co['parents']]==manifest['original_commit_parents'],'Original193 commit metadata differs');h.m.m.h.warm_selected_directories([co['tree']['sha']],[x['path'] for x in manifest['files']])
 for x in manifest['files']:
  p=safe_path('audits/pr193_30004563/original_submission/files/'+x['path']);require(x['path'].startswith(NATIVE) and c.byte_pin(p.read_bytes())=={k:x[k] for k in ['bytes','sha256','git_blob']} and p.stat().st_mode&0o777==0o444 and h.lookup(co['tree']['sha'],x['path'])==(x['mode'],'blob',x['git_blob']),'Original193 archived byte/blob/mode differs')
 return h,r,a,status,i192,i193,main,inherited

def programme(before,stamp,status,i193,prior,acceptance_path):
 """Pure whole postimage: prior current191 fields become explicit history."""
 require((before['current_PR'],before['fully_completed_count'],before['published_count'],before['last_completed_PR'],before['next_numeric_intake_cursor'])==(191,40,24,191,192),'Prior programme ownership/census/cursor differs')
 j=copy.deepcopy(before);aliases={'actual_factual_checkpoint_accepted','completion_metadata_checkpoint_pending_at_snapshot','remaining_current_step','next_step','program_snapshot_authority_condition','program_snapshot_semantics','active_checkpoint_acceptance_receipt','latest_ordered_intake_record','last_actual_intake_checkpoint_commit','last_actual_intake_checkpoint_release','next_numeric_intake_cursor','advance_to_next_PR_authorized_now','next_status_only_intake_performed','next_intake_requires_actual_completion_receipt'}
 retired={k:copy.deepcopy(v) for k,v in before.items() if k.startswith(('current_','conditional_','next_','actual_factual_','active_checkpoint_','program_snapshot_')) or k in aliases or k=='completion_receipt_checkpoint_effective_after_actual_current_MAIN_acceptance'};j.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':191,'actual_completion_checkpoint':prior['checkpoint_commit'],'values':retired})
 for k in retired:j.pop(k,None)
 j.update(UTC=stamp,updated_UTC=stamp,current_PR=193,current_problem_id=30004563,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget='2/5',current_status=status['status'],current_PR_workflow_percent=20,current_workflow_estimate_percent=20,current_mathematics_cleared=False,current_mathematical_clearance=False,current_mathematical_result_valid=None,current_counterexample_claim_under_NEW_independent_audit=True,current_independent_mathematical_audit_families=3,current_priority_clearance=False,current_publication_ready=False,current_publication_package_reviews_complete=False,current_publication_package_reviews_required=True,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_original_PR_merged=False,current_original_PR_open_draft=True,current_closed=False,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr193_30004563/CURRENT_CASE_STATUS.json',current_exact_primary_target='audits/pr193_30004563/ROOT_EXACT_PRIMARY_TARGET_01.json',current_primary_target_verified=True,current_mathematical_scope='Submitted alpha16 five-center counterexample is under three NEW independent audits. Published Remark4.8 realization setting allows crossings; proper embeddings are a separate target. No maximum, mathematical, priority or publication clearance.',current_remaining_required_steps=status['remaining_required_steps'],remaining_current_step=status['remaining_required_steps'],next_step='Complete current193 independent audits and qualified workflow before any194 intake.',next_numeric_intake_cursor=193,conditional_next_numeric_intake_cursor=194,conditional_next_intake_requires_actual_factual_acceptance=True,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=193,next_intake_requires_explicit_writer_release=False,next_eligible_PR_after_current_completion=None,next_eligible_order_requires_fresh_status_check=True,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False,latest_ordered_intake_record='status_intakes_after_pr191/PR193_ORIGINAL_STATUS_INTAKE.json',active_checkpoint_acceptance_receipt=acceptance_path,program_snapshot_authority_condition='Effective only after actual true-parent/full-delta/all-current-identities intake checkpoint acceptance; no mathematical, priority, publication or PR-disposition clearance.',program_snapshot_semantics='PR191 actual completion and own receipt accepted:40completed/24published. Original192 already_solved status-only skip untouched. Original193 claimed_solved2/5 archived19; exact primary target verified; submitted alpha16 five-center claim under three NEW independent audits, workflow20%. No193 clearance/disposition or194 intake.')
 j['skipped_since_last_completion']=list(before.get('skipped_since_last_completion',[]))
 if 192 not in j['skipped_since_last_completion']:j['skipped_since_last_completion'].append(192)
 require(all(j[k]==v for k,v in before.items() if k.startswith('last_completed_') or k.startswith('last_published_')) and j['fully_completed_eligible_PRs']==before['fully_completed_eligible_PRs'] and j['published_PRs']==before['published_PRs'],'Prior completed census/history changed')
 return j

def overlay(c,h,parent,stamp,status,i193,prior,gen):
 require(max(c.valid_stamp(status['UTC']),c.valid_stamp(i193['UTC']),c.valid_stamp(prior['UTC']))<=c.valid_stamp(stamp)<=c.valid_stamp(c.now()),'Intake recording timestamp is stale/future')
 out=sources(c);before=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));out[PREFIX+'CURRENT_PROGRESS.json']=encoded(programme(before,stamp,status,i193,prior,'audits/pr193_30004563/intake_checkpoint_preparation_02/checkpoint_'+gen+'/INTAKE_CHECKPOINT_ACCEPTANCE.json'))
 note='\n'+stamp+' — Actual PR191 own completion receipt recorded,40completed/24published. PR192 already_solved status-only SKIP_UNTOUCHED, no mathematical review or disposition. PR193/30004563 original '+HEAD+' claimed_solved2/5, original19 byte-exact archived as data. Exact primary target verified; submitted alpha16 five-center counterexample under three NEW independent audits. Remark4.8 realization permits crossings; proper embeddings separate. Workflow20%, mathematical/priority/publication clearance false; no PR/QUEUE/native mutation and no194 intake. Broader goal active.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+n]=h.body_at(PREFIX+n,parent)+note.encode()
 return out

def message(digest):return 'Record ordered PR193 unreviewed20% intake; PR192 status-only skipped;40completed/24published\n\nNo mathematical/priority/publication clearance or PR/QUEUE/native changes; no194 intake.\nPR193 intake selected-map SHA256: '+digest

def verify(c,h,r,selected,allowed):
 require(QUEUE not in allowed and QUEUE not in r['changed_paths'] and selected[QUEUE]==read(D/'SOURCE_INPUTS.json')['reviewed_inherited_queue']['identity'],'QUEUE must remain protected inherited baseline');co=h.api('git/commits/'+r['commit']);parent=h.api('git/commits/'+r['expected_main'])['tree']['sha'];require(h.lookup(parent,QUEUE)==('100644','blob',selected[QUEUE]['git_blob']),'True parent QUEUE changed after reviewed inheritance');require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']] and parent==r['parent_tree'],'Actual intake parent/tree differs');require(r['selected_files']==selected and r['overlay_paths']==sorted(allowed) and r['selected_map_sha256']==c.selected_digest(selected) and co['message']==message(r['selected_map_sha256']),'Exact intake map/message/overlay differs');h.m.m.h.warm_selected_directories([parent,r['tree']],selected)
 for n,x in selected.items():require(h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Prepared intake identity differs '+n)
 changed={n for n,x in selected.items() if h.lookup(parent,n)!=('100644','blob',x['git_blob'])};require(changed==set(r['changed_paths'])==h.changed_leaves(parent,r['tree']) and changed<=set(allowed),'Actual intake full-tree foreign/undeclared delta')

def prepare(c,old,gen):
 require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Use a fresh generation');h,prior,a,status,i192,i193,parent,inherited=context(c,old,True);dest=D/('checkpoint_'+gen);dest.mkdir(exist_ok=False);stamp=c.now();out=overlay(c,h,parent,stamp,status,i193,a,gen);mutable={PREFIX+n for n in PROG}
 for n,b in out.items():
  require(not n.startswith('unsolved_math_prioritization/') and (n in mutable or n.startswith(PREFIX+'audits/pr193_30004563/') or n.startswith(PREFIX+'status_intakes_after_pr191/') or n.startswith(PREFIX+PREV)),'Nonowned intake overlay')
  if n in prior['selected_files'] and n not in mutable:require(c.byte_pin(b)==prior['selected_files'][n],'Protected prior191 identity changed '+n)
 selected={**inherited,**{n:c.byte_pin(b) for n,b in out.items()}};pt=h.api('git/commits/'+parent)['tree']['sha'];tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':n,'mode':'100644','type':'blob','content':b.decode()} for n,b in sorted(out.items())]});digest=c.selected_digest(selected);co=h.api('git/commits','POST',{'message':message(digest),'tree':tree['sha'],'parents':[parent]});h.m.m.h.warm_selected_directories([pt,tree['sha']],selected);changed=sorted(n for n,x in selected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob']))
 r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree['sha'],'commit':co['sha'],'selected_files':selected,'selected_map_sha256':digest,'changed_paths':changed,'overlay_paths':sorted(out),'prior_preparation':pin(P/PREV/'checkpoint_receipt01/CHECKPOINT_PREPARATION.json'),'prior_acceptance':pin(P/PREV/'checkpoint_receipt01/CHECKPOINT_ACCEPTANCE.json'),'inherited_queue':read(D/'SOURCE_INPUTS.json')['reviewed_inherited_queue'],'MAIN_moved':False};fresh(dest/'INTAKE_CHECKPOINT_PREPARATION.json',encoded(r));verify(c,h,r,selected,out);original_open(h);require(h.api('git/ref/heads/main')['object']['sha']==parent,'MAIN advanced; preserve generation and retry fresh');print(json.dumps({'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected':len(selected),'changed':len(changed),'MAIN_moved':False}))

def accept(c,old,gen):
 require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Unsafe generation');dest=D/('checkpoint_'+gen);r=read(dest/'INTAKE_CHECKPOINT_PREPARATION.json');h,prior,a,status,i192,i193,main,inherited=context(c,old,False);require(r['prior_preparation']==pin(P/PREV/'checkpoint_receipt01/CHECKPOINT_PREPARATION.json') and r['prior_acceptance']==pin(P/PREV/'checkpoint_receipt01/CHECKPOINT_ACCEPTANCE.json'),'Prior actual completion source changed');require(r['inherited_queue']==read(D/'SOURCE_INPUTS.json')['reviewed_inherited_queue'],'Prepared inherited QUEUE binding changed');c.selected_current(h,r['expected_main'],inherited,read(D/'SOURCE_INPUTS.json')['reviewed_inherited_queue']['source_tree']);out=overlay(c,h,r['expected_main'],r['UTC'],status,i193,a,gen);selected={**inherited,**{n:c.byte_pin(b) for n,b in out.items()}};verify(c,h,r,selected,out);require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Intake checkpoint is not on MAIN');tree=c.selected_current(h,main,selected,r['tree'])
 require(c.byte_pin(h.body_at(QUEUE,main))==selected[QUEUE],'Fresh actual inherited QUEUE bytes differ')
 for n,b in out.items():require(h.body_at(n,main)==b,'Fresh intake/public/archive byte differs '+n)
 original_open(h);result={'UTC':c.now(),'PR':193,'original_head':HEAD,'status':'ACTUAL_ORDERED_PR193_INTAKE_TRUE_PARENT_FULL_DELTA_ALL_CURRENT_IDENTITIES_ACCEPTED','checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(selected),'preserved_prior_selected_paths':937,'prior_identities_unchanged_before_programme_overrides':936,'exact_prior_identities_preserved':933,'reviewed_inherited_QUEUE':read(D/'SOURCE_INPUTS.json')['reviewed_inherited_queue']['identity'],'QUEUE_written':False,'only_prior_content_overrides':PROG,'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':40,'published_count':24,'case_percent':20,'skipped_status_only_PRs':[192],'native_QUEUE_PR_disposition_changes':0,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'next_numeric_intake_cursor':193,'conditional_next_numeric_intake_cursor':194,'advance_to_next_PR_authorized_now':False,'goal_complete':False};fresh(dest/'INTAKE_CHECKPOINT_ACCEPTANCE.json',encoded(result));print(json.dumps(result))

if __name__=='__main__':
 require(sys.dont_write_bytecode,'Use Python -B');require(len(sys.argv)==3 and sys.argv[1] in ['prepare','accept'],'Usage: prepare_intake_checkpoint.py prepare|accept fresh_generation');c,old=load();c.production_entrypoint(prepare if sys.argv[1]=='prepare' else accept,c,old,sys.argv[2])
