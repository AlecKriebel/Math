from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2];old=P/'audits/pr104_600008'
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
t=datetime.datetime.now(datetime.timezone.utc).isoformat();D=A/'original_source_authentication_20261006'
s=load(D/'ORIGINAL_BLOB_MANIFEST.json');pair=load(D/'SOURCEPAIR_AUTHENTICATION.json');primary=load(A/'primary_sources_20261006/RETRIEVAL_MANIFEST.json')
require(s['source_head']=='cc2ae01897135b35bee135917819e782a220f2c1' and s['literal_status']=='claimed_solved','eligible source')
require(pair['submitted_source_equals_raw_and_SQL'] and pair['authenticated_no_join_prior_report'] and pair['catalog_review_hash_verified'],'source pair')
require(len(primary['records'])==2 and all(x['matches_submitted_pin'] and x['extraction']['exit_code']==0 for x in primary['records']),'primary sources')
for pin in s['files']:
 b=Path(pin['preserved_path']).read_bytes();require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'original source pin changed')
progress=load(P/'CURRENT_PROGRESS.json');require(progress['last_completed_PR']==104 and progress['fully_completed_count']==15 and not progress['last_completed_audit_checkpoint_push_pending'],'prior completion')
progress={k:v for k,v in progress.items() if not k.startswith('current_')}
progress.update(UTC=t,updated_UTC=t,current_PR=107,current_problem_id=30003997,current_original_head=s['source_head'],current_original_literal_status='claimed_solved',current_original_budget='1/5',
 current_new_central_proof_search_turns=0,current_source_authentication_complete=True,current_source_authentication_percent=100,
 current_source_authentication_record='audits/pr107_30003997/original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json',
 current_sourcepair_record='audits/pr107_30003997/original_source_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json',
 current_primary_sources_record='audits/pr107_30003997/primary_sources_20261006/RETRIEVAL_MANIFEST.json',
 current_fresh_math_agents=['pr107_reduction_all_trees_adversary_20261006','pr107_independent_reproduction_adversary_20261006','pr107_source_objective_complexity_adversary_20261006'],
 current_mathematical_audit_percent=20,current_mathematical_clearance=False,current_priority_clearance=False,current_priority_audit_percent=0,
 current_publication_ready=False,current_publication_percent=0,current_native_integration_complete=False,current_DOI=None,current_tracker_range=None,current_merge_commit=None,
 current_PR_workflow_percent=10,current_workflow_estimate_percent=10,current_human_disposition_question_pending=False,
 latest_ordered_intake_record='ordered_intake_20261006/after_PR104/INTAKE_AFTER_PR104.json',next_numeric_intake_cursor=108,next_eligible_PR_after_current_completion=None,
 skipped_since_last_completion=[{'PR':105,'literal_status':'unsolved'},{'PR':106,'literal_status':'unsolved'}],
 remaining_current_step='Complete independent mathematical audit of PR107, then deep priority audit if mathematics passes.',
 next_step='Independent all-tree reduction, computation and exact source/complexity families running.',persistent_goal_status='active',persistent_goal_complete=False,
 completion_metadata_checkpoint_pending_at_snapshot=False)
dump(P/'CURRENT_PROGRESS.json',progress)
line=t+' — PR107 current draft eligible head cc2ae018 authenticated, all21 incoming regular bodies/source/prior no-join, complete primary OWR contribution and Karp theorem verified at exact submitted PDF hashes. Three independent mathematical families launched without shared conclusions; ROOT independently reconstructed all-tree reduction and edge/encoding boundaries. Original1/5, added central proof-search0. Source100%, mathematics20%, priority0%, PR107workflow10%; program15/99=15.15%. PR105/106 skipped entirely on literal unsolved status. No novel-resolution/publication/merge clearance. Primary checkout/index untouched.\n'
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with f.open('a') as out:out.write('\n'+line)
paths=[P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'ROOT_INDEPENDENT_RECONSTRUCTION_20261006.md',A/'authenticate_original_source.py',A/'authenticate_source_pair.py',A/'retrieve_primary_sources.py',A/'record_cli.py',A/'scoped_checkpoint.py',A/'record_intake_checkpoint.py',A/'primary_sources_20261006/RETRIEVAL_MANIFEST.json']
paths.extend(f for f in D.rglob('*') if f.is_file() and not f.is_symlink())
for folder in [A/'actual_operations',P/'ordered_intake_20261006/after_PR104']:
 paths.extend(f for f in folder.rglob('*') if f.is_file() and not f.is_symlink())
for name in ['ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json','record_closure_release_readback.py','intake_after_PR104.py','COMPLETION_CHECKPOINT_SELECTION_20261006.json']:paths.append(old/name)
for label in ['complete_prior_disposition','completion_metadata_release','closure_release_readback','ordered_intake_after_PR104']:
 paths.extend(f for f in (old/'actual_operations'/label).iterdir() if f.is_file())
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:paths.append(old/'actual_checkpoints/closure_completion_release'/name)
paths.append(old/'RESEARCH_LOG.md')
rels=sorted(set(str(f.relative_to(C)) for f in paths));require(all((C/f).is_file() for f in rels),'missing selected source')
dump(A/'INTAKE_CHECKPOINT_SELECTION_20261006.json',{'UTC':t,'actual_operator_PID':os.getpid(),'paths':rels,'expected_main_parent':'f151ff76e924632d8415120375329c6e12a2f457','primary_fulltexts_excluded':True,'mathematical_or_priority_clearance':False})
print(json.dumps({'PR':107,'selected_paths':len(rels),'selected_bytes':sum((C/f).stat().st_size for f in rels),'workflow_percent':10,'program_percent':15/99*100}))
