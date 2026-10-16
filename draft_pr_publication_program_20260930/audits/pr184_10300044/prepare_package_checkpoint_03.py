"""Frozen selected publication-candidate checkpoint; no native PR disposition."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
A=Path(__file__).resolve().parent;P=A.parent.parent
s=importlib.util.spec_from_file_location('base179',P/'audits/pr179_10800007/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.TREE_CACHE_PATH=A/'integration_preparation/IMMUTABLE_TREE_CACHE.json'
api,require,save,lookup,changed_leaves,body_at,pin=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin
PREFIX=m.PREFIX;CASE=PREFIX+'audits/pr184_10300044/';HEAD='fbd6561971368a0867df83453454427863d7f910'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def sourcegate():
 p=api('pulls/184');require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] and not p['merged'],'Original PR state changed')
def prepare(gen):
 require(re.fullmatch('package_checkpoint_[a-z0-9_]+',gen),'Generation');sourcegate();e=api('git/ref/heads/main')['object']['sha'];parent=api('git/commits/'+e)
 plan=json.loads((A/'PACKAGE_CHECKPOINT_SCOPE_03.json').read_text())
 for x in plan['files']:require(pin(A/x['path'])['sha256']==x['sha256'],'Frozen scope drift '+x['path'])
 j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require(j['fully_completed_count']==37 and j['published_count']==21 and j['last_completed_PR']==179 and j['current_PR']==184,'Campaign changed')
 stamp=now();j.update(UTC=stamp,updated_UTC=stamp,current_status='V2_BIBLIOGRAPHIC_REPAIR_ACCEPTED_THIRD_NEW_COMPLETE_PACKAGE_REVIEW_IN_PROGRESS',current_PR_workflow_percent=65,current_workflow_estimate_percent=65,current_mathematics_cleared=True,current_priority_clearance=False,current_bounded_priority_audit_complete=True,current_historical_firstness_or_guaranteed_novelty_certified=False,current_full_priority_body_coverage_complete=False,current_qualified_note_route_authorized=True,current_publication_ready=False,current_Zenodo_published=False,current_tracker_updated=False,current_original_PR_merged=False,current_remaining_required_steps='Successive NEW full-package review/repair loops until clean, exact Zenodo/tracker and original-head-safe disposition.',advance_to_next_PR_authorized_now=False,persistent_goal_complete=False)
 out=A/gen;out.mkdir(exist_ok=False);save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+stamp+' — PR184 workflow65%: secondNEWwhole-package review found sole bibliographic source-gap author error; Rootverifiedprimarypublishermetadata and repaired currentv2README/ZIP/nativepending02, preserving v1/pending01 history. PDF/TeX/code/depositmetadata unchanged. ThirdNEWcomplete-v2adversarialreview active. Mathematicscleared, historicalpriorityunresolved with explicit unread-source/version gaps. No deposit/tracker/nativeattempt/QUEUE/PRdisposition changes.37completed/21published unchanged; goalactive.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at(PREFIX+n,e)+note.encode())
 overlay={CASE+n:A/n for n in plan['case_paths']};overlay[CASE+'PACKAGE_CHECKPOINT_SCOPE_03.json']=A/'PACKAGE_CHECKPOINT_SCOPE_03.json';overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']})
 pins={n:{**pin(f),'local_path':str(f)} for n,f in sorted(overlay.items())};entries=[]
 for n,f in sorted(overlay.items()):
  b=f.read_bytes();x={'path':n,'mode':'100644','type':'blob'}
  try:x['content']=b.decode()
  except UnicodeDecodeError:
   blob=api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'});require(blob['sha']==pins[n]['git_blob'],'Binary blob');x['sha']=blob['sha']
  entries.append(x)
 t=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries});m.m.h.warm_selected_directories([parent['tree']['sha'],t['sha']],pins)
 changed={n for n,x in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',x['git_blob'])};require(changed_leaves(parent['tree']['sha'],t['sha'])==changed,'Foreign delta')
 for n,x in pins.items():require(lookup(t['sha'],n)==('100644','blob',x['git_blob']),'Selected blob')
 co=api('git/commits','POST',{'message':'Checkpoint PR184 bibliographic repair and corrected publication candidate\n\nMathematicscleared; classical ingredients credited, historicalpriority unresolved with explicit body/version gaps. V2 current-source author correction, old snapshots preserved; third new whole-package review ongoing. No native attempt/QUEUE/PR disposition or publication.37completed/21published unchanged.','tree':t['sha'],'parents':[e]})
 result={'UTC':stamp,'expected_main':e,'parent_tree':parent['tree']['sha'],'tree':t['sha'],'commit':co['sha'],'selected_files':pins,'changed_paths':sorted(changed),'generation':gen,'case_percent':65,'completed':37,'published':21,'publication_ready':False,'historical_priority_clearance':False};save(A/'PACKAGE_CHECKPOINT_PREPARATION_03.json',result);sourcegate();require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; rebuild from fresh tip');print(json.dumps({'expected_main':e,'commit':co['sha'],'selected':len(pins),'changed':len(changed)}))
def accept():
 r=json.loads((A/'PACKAGE_CHECKPOINT_PREPARATION_03.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']],'Actual parents/tree')
 m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],r['selected_files']);require(changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']),'Actual scope')
 for n,x in r['selected_files'].items():require(lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Actual selected blob')
 actual=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Commit not onMAIN')
 for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'publication_package_v1/zenodo-deposit.json',CASE+'publication_package_v1/taut_godbillon_vey.pdf',CASE+'publication_package_v1/verification-package.zip']:
  b=body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh selected bytes')
 sourcegate();out={'UTC':now(),'status':'ACTUAL_COMPLETE_PACKAGE_CHECKPOINT_FULL_SCOPE_AND_NATIVE_BYTES_ACCEPTED','checkpoint_commit':r['commit'],'main_observed':actual,'foreign_MAIN_paths_preserved':True,'original_PR_draft_head_preserved':HEAD,'case_percent':65,'completed':37,'published':21,'publication_ready':False,'goal_complete':False};save(A/'PACKAGE_CHECKPOINT_ACCEPTANCE_03.json',out);print(json.dumps(out))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')
