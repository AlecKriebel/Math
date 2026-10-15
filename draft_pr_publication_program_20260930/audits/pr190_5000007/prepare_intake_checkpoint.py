"""Record original-status intake and the early, uncleared PR190 source audit on MAIN."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
A=Path(__file__).resolve().parent;P=A.parent.parent
s=importlib.util.spec_from_file_location('base184',P/'audits/pr184_10300044/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.m.TREE_CACHE_PATH=A/'INTAKE_IMMUTABLE_TREE_CACHE.json'
api,require,save,lookup,changed_leaves,body_at,pin=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin
PREFIX=m.PREFIX;CASE=PREFIX+'audits/pr190_5000007/';HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def check_open():
 p=api('pulls/190');require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] and not p['merged'],'Original190head/statechanged')
def prepare(generation):
 require(generation.isalnum(),'Generation must be alphanumeric');check_open();e=api('git/ref/heads/main')['object']['sha'];parent=api('git/commits/'+e)
 j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require(j['fully_completed_count']==38 and j['published_count']==22 and j['last_completed_PR']==184,'Accepted census changed')
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());require(status['original_QUEUE_status']=='claimed_solved' and not status['mathematical_clearance'] and status['case_percent']==15,'Intake scientific stage drift')
 manifest=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text());require(len(manifest['files'])==22 and manifest['original_head']==HEAD,'Original manifest drift')
 names=['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','ORIGINAL_FILE_MANIFEST.json','ROOT_SCIENTIFIC_ASSESSMENT_01.md','ROOT_PRIMARY_SOURCE_ACQUISITION_01.json','prepare_intake_checkpoint.py']
 for x in manifest['files']:
  n='original_submission/files/'+x['path'];b=(A/n).read_bytes();require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Original body drift');names.append(n)
 overlay={CASE+n:A/n for n in names}
 for number in range(185,191):
  f='status_intakes_after_pr184/PR'+str(number)+'_ORIGINAL_STATUS_INTAKE.json';overlay[PREFIX+f]=P/f
 prior='audits/pr184_10300044/ROOT_FINAL_FACTUAL_ACCEPTANCE.json';overlay[PREFIX+prior]=P/prior
 for k in list(j):
  if k.startswith('current_'):del j[k]
 stamp=now();j.update(UTC=stamp,updated_UTC=stamp,current_PR=190,current_problem_id=5000007,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget=status['original_effort'],current_status=status['status'],current_PR_workflow_percent=15,current_workflow_estimate_percent=15,current_mathematics_cleared=False,current_mathematical_result_valid=None,current_priority_clearance=False,current_publication_ready=False,current_Zenodo_published=False,current_tracker_updated=False,current_original_PR_merged=False,current_closed=False,current_source_formulation_issue=True,current_source_disambiguation_not_author_authenticated=True,current_record='audits/pr190_5000007/CURRENT_CASE_STATUS.json',current_remaining_required_steps=status['remaining_required_steps'],skipped_since_last_completion=[185,186,187,188,189],next_numeric_intake_cursor=191,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False,program_snapshot_semantics='PR184 actual factual acceptance complete:38completed/22published. Original185–189unsolved skipped untouched. Original190claimed_solved22files authenticated; primary source ambiguity and promising parity-selected geometry identified, three independent mathematical audits active. No mathematical/priority/publication clearance; no PR disposition.')
 out=A/('intake_preparation_'+generation);out.mkdir(exist_ok=False);save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+stamp+' — PR184 factual completion accepted,38completed/22published. Original185–189unsolved status-only skipped untouched. PR190/5000007 originalhead'+HEAD+' claimed_solved, effort unknown/5(interrupted),22originalfiles pinned. Workflow15%: source ambiguity identified, parity-selected geometry promising, three independent audits active; literal bare-angle claim false for two face diagonals. No mathematical/priority/publication clearance or PR disposition. Broader goal active.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at(PREFIX+n,e)+note.encode())
 overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});pins={n:{**pin(p),'local_path':str(p)} for n,p in sorted(overlay.items())}
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':[{'path':n,'mode':'100644','type':'blob','content':p.read_text()} for n,p in sorted(overlay.items())]})
 m.m.m.h.warm_selected_directories([parent['tree']['sha'],tree['sha']],pins);changed={n for n,x in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',x['git_blob'])}
 require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Foreign full-tree delta')
 for n,x in pins.items():require(lookup(tree['sha'],n)==('100644','blob',x['git_blob']),'Prepared selected identity drift')
 co=api('git/commits','POST',{'message':'Record PR184 completion and ordered PR190 source audit intake\n\n38completed/22published; original185–189unsolved skipped untouched. PR190claimed_solved original22files preserved, source formulation issue identified; mathematical and priority audits pending. No QUEUE/nativeattempt/PRdisposition changes; foreign MAIN preserved.','tree':tree['sha'],'parents':[e]})
 result={'UTC':stamp,'status':'PREPARED_MAIN_NOT_MOVED','expected_main':e,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':co['sha'],'selected_files':pins,'changed_paths':sorted(changed),'case_percent':15,'completed':38,'published':22,'QUEUE_or_native_attempt_or_PR_disposition_changes':0}
 save(A/'INTAKE_CHECKPOINT_PREPARATION.json',result);check_open();require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; rebuild fresh generation');print(json.dumps({'expected_main':e,'commit':co['sha'],'tree':tree['sha'],'selected':len(pins)}))
def accept():
 r=json.loads((A/'INTAKE_CHECKPOINT_PREPARATION.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']],'Actual parent/tree drift')
 m.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],r['selected_files']);require(changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']),'Actual full scope drift')
 for n,x in r['selected_files'].items():require(lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Actual selected identity drift')
 main=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint not on MAIN')
 for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'ORIGINAL_FILE_MANIFEST.json',PREFIX+'audits/pr184_10300044/ROOT_FINAL_FACTUAL_ACCEPTANCE.json']:
  b=body_at(n,main);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh accepted byte drift')
 check_open();j={'UTC':now(),'status':'ACTUAL_ORDERED_PR190_INTAKE_FULL_SCOPE_AND_NATIVE_READBACK_ACCEPTED','checkpoint_commit':r['commit'],'main_observed':main,'selected_files':len(r['selected_files']),'all_foreign_base_paths_preserved':True,'skipped_PRs_untouched':[185,186,187,188,189],'PR':190,'original_head':HEAD,'case_percent':15,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'fully_completed_count':38,'published_count':22,'goal_complete':False};save(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json',j);print(json.dumps(j))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')

