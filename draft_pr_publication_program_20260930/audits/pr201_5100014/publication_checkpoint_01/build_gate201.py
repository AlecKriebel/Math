"""Freeze the actual accepted PR201 package and review evidence; no remote mutation."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent.parent
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def frozen(p):
 assert p.is_file() and not p.is_symlink(),str(p)
 p.chmod(0o444);return pin(p)
pkg=A/'publication_package_v2';seal=read(pkg/'PACKAGE_SEAL.json')
assert pin(pkg/'PACKAGE_SEAL.json')=={'bytes':90105,'sha256':'89bbfc82c0ae2b80fca046671681f94cef28f130d01df4a3b52036efd7a95ad5'}
safe=dict(seal['package_safe_files']);safe['PACKAGE_SEAL.json']=pin(pkg/'PACKAGE_SEAL.json')
for rel,x in safe.items():assert frozen(pkg/rel)==x,rel
events=[]
for i,verdict,raw,package,manifest in [(1,'REPAIRS_REQUIRED','NOT_CLEANPASS','publication_package_v1','AUTHORED_MANIFEST.json'),(2,'CLEANPASS','CLEANPASS','publication_package_v2','SAFE_AUTHORED_MANIFEST.json')]:
 d=A/('whole_package_adversary_'+str(i).zfill(2));sf=read(d/manifest)['files'];sf={**sf,manifest:pin(d/manifest)}
 for rel,x in sf.items():assert frozen(d/rel)==x,rel
 acc='ROOT_WHOLE_PACKAGE_REVIEW_'+str(i).zfill(2)+'_ACCEPTANCE.json';ac=read(A/acc)
 assert ac['normalized_verdict']==verdict and ac['reviewed_package_seal']==pin(A/package/'PACKAGE_SEAL.json')
 events.append({'agent':'/root/'+d.name.replace('whole_package','pr201_whole_package'),'directory':d.name,'verdict':verdict,'raw_agent_verdict':raw,'reviewed_package':package,'reviewed_package_seal':pin(A/package/'PACKAGE_SEAL.json'),'safe_manifest':manifest,'safe_files':sf,'Root_acceptance_file':acc,'Root_acceptance_pin':frozen(A/acc),'qualification':'Entire v1 reviewed; original-archive omission required repair.' if i==1 else 'NEW from-scratch entire final v2 reviewed after all repairs; no substantive issue.'})
others={}
def add(rel):others[rel]=frozen(A/rel)
for rel in ['ROOT_LOCAL_DEPOSIT_CHECK_01.json','ROOT_LOCAL_DEPOSIT_CHECK_02.json','ROOT_PACKAGE_PRE_REVIEW_01.json','native_publication_preparation_01/make_native.py','native_publication_preparation_01/QUEUE_ROW_PREPARATION.json','publication_operations_01/publish_exact.py','publication_operations_01/update_tracker.py','publication_lifecycle_01/finish201.py','publication_lifecycle_01/ROOT_PREPARATION_CHECK.json','publication_lifecycle_01/ROOT_PREPUBLICATION_HELPER_CHECK_02.json','publication_checkpoint_01/build_gate201.py']:
 add(rel)
for dirname in ['root_review02_custody_replay']:
 for p in sorted((A/dirname).rglob('*')):
  if p.is_file():add(str(p.relative_to(A)))
for p in sorted((A/'package_build_01').rglob('*')):
 if p.is_file() and p.suffix in {'.json','.py','.md','.stdout','.stderr','.txt'} and '__pycache__' not in p.parts:add(str(p.relative_to(A)))
# Preserve the exact earlier review target and failed-archive evidence as history.
for p in sorted((A/'publication_package_v1').rglob('*')):
 if p.is_file():add(str(p.relative_to(A)))
g={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'problem_id':5100014,'original_head':'90bdb85235979f2ffa7496b9b689036654e55200','original_QUEUE_status':'claimed_solved','original_effort':'OriginalQUEUE1/5; original metadata/log report one substantive author turn, actual model/effort unverified; later audits and publication separate.','publication_ready_gate_accepted':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_priority_established':False,'theorem_novelty_established':False,'proof_method_novelty_established':False,'independent_discovery_certified':False,'current_worldwide_openness_certified':False,'mathematical_gate':pin(A/'ROOT_MATHEMATICAL_GATE_01.json'),'priority_editorial_gate':pin(A/'ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json'),'publication_form':'Attributed alternative flag-curve proof of the exact contemporaneous Ferudun theorem, with classical and Chavez-Caliz inputs credited.','exact_contemporary_references':['10.5281/zenodo.23087221','10.5281/zenodo.23088516'],'timeline_scope':'Observed Oct1 PR/deposit/registration fields; not first-public-visibility or independence certification. Manuscript and expanded checks dated Oct16.','package':pkg.name,'package_seal':pin(pkg/'PACKAGE_SEAL.json'),'package_safe_files':safe,'intended_upload_files':seal['upload_files'],'metadata':seal['metadata_exact'],'whole_package_review_loop_complete':True,'fresh_final_review_after_documented_editorial_repairs':True,'whole_package_review_events':events,'review_sequence':'NEW01 entire v1 NOT_CLEANPASS for omitted promised original archive; Root repaired archive and package documentation in v2; NEW02 entire exact final v2 CLEANPASS. No later publication payload change.','other_safe_files':others,'local_deposit_check':pin(A/'ROOT_LOCAL_DEPOSIT_CHECK_02.json'),'Root_all_reports_derivations_code_ledgers_and_receipts_read':True,'Root_full_math_and_priority_reproductions_accepted':True,'Root_fresh_final_package_and_history_integrity_replay_accepted':True,'Root_all_six_current_PDF_pages_individually_inspected':True,'built_in_LaTeX_compilation_successfully_checked':True,'extensive_AI_use':True,'unrefereed':True,'conventional_human_peer_review':False,'formal_proof_assistant_certification':False,'actual_publication_not_yet_claimed':True,'actual_tracker_not_yet_claimed':True,'actual_merge_not_yet_claimed':True,'case_workflow_estimate_percent':90,'advance_to_PR202':False,'goal_complete':False}
p=A/'ROOT_PUBLICATION_GATE_01.json'
with p.open('x') as out:json.dump(g,out,indent=2);out.write('\n')
p.chmod(0o444)
print(json.dumps({'gate':pin(p),'package_files':len(safe),'review_events':[(x['verdict'],len(x['safe_files'])) for x in events],'other_safe_files':len(others),'workflow_percent':90,'no_remote_mutation':True}))
