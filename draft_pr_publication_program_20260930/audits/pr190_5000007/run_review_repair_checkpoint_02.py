"""Release a scoped draft packet/checkpoint on fresh MAIN; no PR disposition."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
A=Path(__file__).resolve().parent;P=A.parent.parent
s=importlib.util.spec_from_file_location('base184',P/'audits/pr184_10300044/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.m.TREE_CACHE_PATH=A/'PACKAGE_CHECKPOINT_IMMUTABLE_TREE_CACHE.json'
api,require,save,lookup,changed_leaves,body_at,pin=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin
PREFIX=m.PREFIX;CASE=PREFIX+'audits/pr190_5000007/';HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def prcheck():
 p=api('pulls/190');require(p['head']['sha']==HEAD and p['state']=='open' and p['draft'] and not p['merged'],'Original190state/head drift')
def own_paths():
 spec=importlib.util.spec_from_file_location('math190',A/'prepare_mathematical_checkpoint.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 names=b.scope()+['MATHEMATICAL_CHECKPOINT_ACCEPTANCE_01.json','ROOT_PRIORITY_GATE_02.json','accept_priority_findings.py','ROOT_WHOLE_REVIEW_INPUT_01.json','PACKAGE_V1_ASSEMBLY_01.json','PR_METADATA_PROPOSAL_01.json','TRACKER_ROW_PROPOSAL_01.json','assemble_publication_package_v1.py','prepare_native_template_pending_01.py','prepare_package_checkpoint_01.py','capture_independent_replays_02.py','ROOT_REPLAY_INTERRUPTION_01.json','ROOT_OWN_REGENERABLE_RENDER_CLEANUP_01.json','integration_preparation/CURRENT_TEMPLATE.json']
 for folder in ['publication_package_v1','publication_package_v2','integration_preparation/native_template_pending_01','integration_preparation/native_template_pending_02','root_independent_replays_02']:
  names += [p.relative_to(A).as_posix() for p in (A/folder).rglob('*') if p.is_file()]
 for d,n,key in [('primary_priority_adversary','FINAL_SEAL.json','manifest'),('current_literature_priority_adversary','FINAL_SEAL.json','files')]:
  j=json.loads((A/d/n).read_text());names += [d+'/'+x['path'] for x in j[key]]+[d+'/'+n]

 names += ['ROOT_PRIORITY_GATE_01.json','ROOT_WHOLE_REVIEW_INPUT_02.json','PACKAGE_V2_ASSEMBLY_01.json','PR_METADATA_PROPOSAL_02.json','TRACKER_ROW_PROPOSAL_02.json','assemble_publication_package_v2.py','prepare_native_template_pending_02.py','prepare_review_repair_v2.py','ROOT_GLOBAL_REPAIR_02.json','ROOT_DOI_FILE_IDENTITY_20261015_01.json','authenticate_doi_files_20261015.py','ROOT_RESUMPTION_REVALIDATION_20261015_02.json','capture_resumption_20261015_02.py','CURRENT_PROOF_PRE_WHOLE_REVIEW01.md','integration_preparation/CURRENT_TEMPLATE_PRE_WHOLE_REVIEW01.json','integration_preparation/NATIVE_TEMPLATE_PENDING_02_MANIFEST.json','PACKAGE_CHECKPOINT_ACCEPTANCE_01.json','prepare_review_repair_checkpoint_02.py','run_review_repair_checkpoint_02.py','ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json','ROOT_V2_VISUAL_ACCEPTANCE.json','bind_v2_for_whole_review_02.py','authenticate_whole_review.py']
 names += ['whole_package_review_01_final/'+n for n in json.loads((A/'whole_package_review_01_final/SAFE_AUTHORED_ALLOWLIST.json').read_text())['key_files']]
 names=sorted(set(names))
 for n in names:require((A/n).is_file() and not (A/n).is_symlink() and not any('private' in x.lower() or 'chrome' in x.lower() for x in Path(n).parts),'Unsafe selected checkpoint file')
 return names
def prepare(gen):
 require(re.fullmatch('[a-z0-9_]+',gen),'Bad generation');prcheck();priority=json.loads((A/'ROOT_PRIORITY_GATE_02.json').read_text());require(priority['bounded_priority_audit_complete'] and not priority['historical_priority_clearance'] and priority['qualified_note_route_authorized_by_human'],'Qualified priority gate')
 pack=json.loads((A/'publication_package_v2/FINAL_REVIEW_PACKET_MANIFEST.json').read_text())
 for n,x in pack['payloads'].items():require(pin(A/'publication_package_v2'/n)['sha256']==x['sha256'],'Protected payload drift')
 names=own_paths();e=api('git/ref/heads/main')['object']['sha'];parent=api('git/commits/'+e);j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require(j['fully_completed_count']==38 and j['published_count']==22 and j['last_completed_PR']==184 and j['current_PR']==190 and j['current_original_head']==HEAD,'Own campaign census/case drift')
 out=A/('repair_checkpoint_'+gen);out.mkdir(exist_ok=False);stamp=now()
 j.update(UTC=stamp,updated_UTC=stamp,current_status='REPAIRED_V2_QUALIFIED_PACKET_NEXT_NEW_WHOLE_REVIEW_ACTIVE',current_PR_workflow_percent=68,current_workflow_estimate_percent=68,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_mathematical_scope='Imported bare-angle exclusion false by exactly two face diagonals; explicitly adopted parity-selected endpoint theorem proved.',current_priority_clearance=False,current_bounded_priority_audit_complete=True,current_full_priority_body_coverage_complete=False,current_historical_firstness_or_guaranteed_novelty_certified=False,current_qualified_note_route_authorized=True,current_source_author_authenticated_erratum=False,current_source_unique_intent_certified=False,current_current_primary_overlap_verified=True,current_publication_ready=False,current_publication_package_reviews_complete=False,current_Zenodo_published=False,current_tracker_updated=False,current_original_PR_merged=False,current_closed=False,current_remaining_required_steps='Next NEW whole-package review; global repairs and another NEW complete review until clean; exact Zenodo/tracker, original-head-safe disposition and factual acceptance.',advance_to_next_PR_authorized_now=False,persistent_goal_complete=False,program_snapshot_semantics='38completed/22published unchanged. Qualified four-page PR190 v2 packet and native repair draft protected; completed first whole review required present DOI-file identity wording correction, now globally repaired. Classical AAH/Troubetzkoy inputs and exact current Ferudun overlap credited; dates and body/version gaps disclosed, nofirstness/independence or authenticated source-intent correction. Next NEW whole-package review active; this MAIN checkpoint is draft findings, not DOI publication or PR disposition.')
 save(out/'CURRENT_PROGRESS.json',j);note='\n\n'+stamp+' — PR190 workflow68%: bounded two-family priority audit complete with historicalfirstness unresolved, exact current Ferudun overlap credited. Protected4-page paper/source/metadata/repaired exact supportZIP and49-file native draft prepared; next NEW whole-package adversary active. Mathematics is explicitly two-part: bare-angle false, adopted parity-selected theorem true. No author-authenticated source correction or certified novelty/independence. Current DOI-version files of overlapping work match inspected copies, superseding historical access failures. No own DOI/tracker/merge yet;38completed/22published unchanged;broadergoalactive.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at(PREFIX+n,e)+note.encode())
 overlay={CASE+n:A/n for n in names};overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});pins={n:{**pin(p),'local_path':str(p)} for n,p in sorted(overlay.items())};entries=[]
 for n,p in sorted(overlay.items()):
  b=p.read_bytes();x={'path':n,'mode':'100644','type':'blob'}
  try:x['content']=b.decode()
  except UnicodeDecodeError:
   z=api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'});require(z['sha']==pins[n]['git_blob'],'Binary identity drift');x['sha']=z['sha']
  entries.append(x)
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries});m.m.m.h.warm_selected_directories([parent['tree']['sha'],tree['sha']],pins)
 changed={n for n,x in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',x['git_blob'])};require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Foreign full-tree delta')
 for n,x in pins.items():require(lookup(tree['sha'],n)==('100644','blob',x['git_blob']),'Prepared selected identity drift')
 co=api('git/commits','POST',{'message':'Record PR190 full-review repair and new exact v2 research-note packet\n\nExplicit two-part mathematics; classical inputs and contemporaneous exact overlap credited. Protected four-page manuscript, exact controls/support, native repairs draft and metadata proposals. Next NEW whole-package review active; no DOI publication/tracker/PR disposition.38completed/22published unchanged; foreign MAIN preserved.','tree':tree['sha'],'parents':[e]})
 rec={'UTC':stamp,'expected_main':e,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':co['sha'],'selected_files':pins,'changed_paths':sorted(changed),'case_percent':68,'completed':38,'published':22,'publication_ready':False,'QUEUE_native_attempt_PR_disposition_changes':0};save(A/'REPAIR_CHECKPOINT_PREPARATION_02.json',rec);prcheck();require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced: rebuild fresh generation');print(json.dumps({'expected_main':e,'commit':co['sha'],'tree':tree['sha'],'selected':len(pins),'changed':len(changed)}))
def accept():
 r=json.loads((A/'REPAIR_CHECKPOINT_PREPARATION_02.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [p['sha'] for p in co['parents']]==[r['expected_main']],'Actual parent/tree drift');m.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],r['selected_files']);require(changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']),'Actual full tree scope drift')
 for n,x in r['selected_files'].items():require(lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Actual selected identity drift')
 main=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint not on MAIN')
 for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'ROOT_PRIORITY_GATE_02.json',CASE+'publication_package_v2/dodecahedron_endpoint.tex',CASE+'publication_package_v2/zenodo-deposit.json',CASE+'integration_preparation/CURRENT_TEMPLATE.json']:
  b=body_at(n,main);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh native body drift')
 prcheck();j={'UTC':now(),'status':'ACTUAL_QUALIFIED_DRAFT_PACKET_CHECKPOINT_FULL_SCOPE_AND_FRESH_NATIVE_BYTES_ACCEPTED','PR':190,'original_head':HEAD,'checkpoint_commit':r['commit'],'main_observed':main,'tree':r['tree'],'parent':r['expected_main'],'selected_files':len(r['selected_files']),'changed_paths':len(r['changed_paths']),'all_foreign_base_paths_preserved':True,'case_percent':68,'bounded_priority_audit_complete':True,'historical_priority_clearance':False,'publication_ready':False,'whole_package_review_active':True,'completed':38,'published':22,'goal_complete':False};save(A/'REPAIR_CHECKPOINT_ACCEPTANCE_02.json',j);print(json.dumps(j))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')

