"""Prepare a scoped MAIN checkpoint for repaired v2; no PR disposition."""
from pathlib import Path
import ast
A=Path(__file__).resolve().parent
s=(A/'prepare_package_checkpoint_01.py').read_text()
s=s.replace("'ROOT_PRIORITY_GATE_01.json'","'ROOT_PRIORITY_GATE_02.json'").replace('publication_package_v1/FINAL_REVIEW_PACKET_MANIFEST.json','publication_package_v2/FINAL_REVIEW_PACKET_MANIFEST.json')
s=s.replace("['publication_package_v1','integration_preparation/native_template_pending_01','root_independent_replays_02']","['publication_package_v1','publication_package_v2','integration_preparation/native_template_pending_01','integration_preparation/native_template_pending_02','root_independent_replays_02']")
needle=' names=sorted(set(names))'
extra="""
 names += ['ROOT_PRIORITY_GATE_01.json','ROOT_WHOLE_REVIEW_INPUT_02.json','PACKAGE_V2_ASSEMBLY_01.json','PR_METADATA_PROPOSAL_02.json','TRACKER_ROW_PROPOSAL_02.json','assemble_publication_package_v2.py','prepare_native_template_pending_02.py','prepare_review_repair_v2.py','ROOT_GLOBAL_REPAIR_02.json','ROOT_DOI_FILE_IDENTITY_20261015_01.json','authenticate_doi_files_20261015.py','ROOT_RESUMPTION_REVALIDATION_20261015_02.json','capture_resumption_20261015_02.py','CURRENT_PROOF_PRE_WHOLE_REVIEW01.md','integration_preparation/CURRENT_TEMPLATE_PRE_WHOLE_REVIEW01.json','integration_preparation/NATIVE_TEMPLATE_PENDING_02_MANIFEST.json','PACKAGE_CHECKPOINT_ACCEPTANCE_01.json','prepare_review_repair_checkpoint_02.py']
 names += ['whole_package_review_01_final/'+n for n in json.loads((A/'whole_package_review_01_final/SAFE_AUTHORED_ALLOWLIST.json').read_text())['key_files']]
"""
if s.count(needle)!=1:raise ValueError('Scope adapter drift')
s=s.replace(needle,extra+needle)
s=s.replace('EXACT_QUALIFIED_RESEARCH_NOTE_PACKET_FIRST_NEW_WHOLE_REVIEW_ACTIVE','REPAIRED_V2_QUALIFIED_PACKET_NEXT_NEW_WHOLE_REVIEW_ACTIVE').replace('current_PR_workflow_percent=62','current_PR_workflow_percent=68').replace('current_workflow_estimate_percent=62','current_workflow_estimate_percent=68').replace("'case_percent':62","'case_percent':68").replace('workflow62%','workflow68%').replace('38completed/22published unchanged. Qualified four-page PR190 research-note packet,146-entry ZIP,49-file native repair draft protected.','38completed/22published unchanged. Qualified four-page PR190 v2 packet and native repair draft protected; completed first whole review required present DOI-file identity wording correction, now globally repaired.').replace('First NEW whole-package review','Next NEW whole-package review').replace('First NEW whole-package adversary','Next NEW whole-package adversary').replace('first NEW whole-package review active','next NEW whole-package review active').replace('First NEW whole-package review active','Next NEW whole-package review active')
s=s.replace('package_checkpoint_','repair_checkpoint_').replace('PACKAGE_CHECKPOINT_PREPARATION_01.json','REPAIR_CHECKPOINT_PREPARATION_02.json').replace('PACKAGE_CHECKPOINT_ACCEPTANCE_01.json','REPAIR_CHECKPOINT_ACCEPTANCE_02.json')
# Keep the previous accepted packet receipt as historical evidence, not self-reference.
s=s.replace("'REPAIR_CHECKPOINT_ACCEPTANCE_02.json','prepare_review_repair_checkpoint_02.py'","'PACKAGE_CHECKPOINT_ACCEPTANCE_01.json','prepare_review_repair_checkpoint_02.py'")
s=s.replace("for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'ROOT_PRIORITY_GATE_02.json',CASE+'publication_package_v1/dodecahedron_endpoint.tex',CASE+'publication_package_v1/zenodo-deposit.json'", "for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'ROOT_PRIORITY_GATE_02.json',CASE+'publication_package_v2/dodecahedron_endpoint.tex',CASE+'publication_package_v2/zenodo-deposit.json'")
s=s.replace('Record PR190 qualified research-note draft and completed bounded priority audit','Record PR190 full-review repair and new exact v2 research-note packet')
s=s.replace('No DOI/tracker/merge yet;38completed/22published unchanged;broadergoalactive.','Current DOI-version files of overlapping work match inspected copies, superseding historical access failures. No own DOI/tracker/merge yet;38completed/22published unchanged;broadergoalactive.')
s=s.replace('prepare_repair_checkpoint_01.py','prepare_package_checkpoint_01.py').replace("pin(A/'publication_package_v1'/n)","pin(A/'publication_package_v2'/n)").replace('146entry supportZIP','repaired exact supportZIP').replace('first NEW whole-package adversary active','next NEW whole-package adversary active')
s=s.replace("'prepare_review_repair_checkpoint_02.py']","'prepare_review_repair_checkpoint_02.py','run_review_repair_checkpoint_02.py']")
s=s.replace("'run_review_repair_checkpoint_02.py']","'run_review_repair_checkpoint_02.py','ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json','ROOT_V2_VISUAL_ACCEPTANCE.json','bind_v2_for_whole_review_02.py','authenticate_whole_review.py']")
ast.parse(s)
(A/'run_review_repair_checkpoint_02.py').write_text(s)
print('Prepared v2 scientific/checkpoint scope; no remote actions.')
