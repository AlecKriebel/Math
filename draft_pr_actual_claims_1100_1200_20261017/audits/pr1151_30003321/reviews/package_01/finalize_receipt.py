from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).absolute().parent;X=R/'extracted';A=X/'draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
source=json.loads((X/'SOURCE_MANIFEST.json').read_text())
for n,w in source.items():
 if pin(X/n)!=w:raise ValueError('extracted reviewed input changed '+n)
initial=json.loads((R/'INITIAL_PINS.json').read_text())['pins']
for n,w in initial.items():
 if pin(X/n)!=w:raise ValueError('private retained six changed '+n)
artifacts={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or 'extracted' in p.relative_to(R).parts or p.name in {'RECEIPT.json','RECEIPT.sha256'}:continue
 artifacts[p.relative_to(R).as_posix()]=pin(p)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review':'package_01','decision':'ISSUES_FOUND','reviewed_original_six_pins':initial,'initial_pin_receipt':pin(R/'INITIAL_PINS.json'),'final_original_live_pin_receipt':pin(R/'FINAL_ORIGINAL_EDITION_PINS.json'),'final_live_original_check_utc':json.loads((R/'FINAL_ORIGINAL_EDITION_PINS.json').read_text())['utc'],'private_retained_original_six_still_identical':True,'source_manifest_pin':pin(X/'SOURCE_MANIFEST.json'),'all_144_source_members_reauthenticated':True,'source_members':source,'all_substantive_scripts_results_seals_receipts_and_render_artifacts':artifacts,'primary_input_reads':json.loads((R/'READING_SCOPE.json').read_text())['primary_read_scopes'],'project_instructions':{'path':'/Users/alec/Documents/Math/AGENTS.md',**pin(Path('/Users/alec/Documents/Math/AGENTS.md'))},'pdf_skill':{'path':'/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md',**pin(Path('/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md'))},'executions':[{'entry':'extracted/verification/verify_all.py','modes':['normal','optimized'],'exit_each':0,'receipt_match':'byte-exact frozen REPLAY_RECEIPT.json; 2 positives+8 failures each'},{'entry':'extracted/current13/verify_release.py','modes':['normal','optimized'],'exit_each':0,'outputs_identical':True},{'entry':'extracted/build_package.py','modes':['normal'],'exit_each':0,'all_six_identity_rebuild':True},{'entry':'extracted/verification/self_test.py','modes':['normal','optimized'],'exit_each':0,'checks_per_mode':28,'outputs_identical':True},{'entry':'own_controls.py','modes':['normal+optimized cases'],'exit':0,'malformed_fixture_rejections':14},{'entry':'historical_replay/*/*.py','modes':['normal_asserts_active'],'processes':4,'exit_each':0,'semantic_results_match_except_timestamps':True}],'limitations':'This receipt authenticates the original reviewed edition. It does not review or pin subsequent repairs. Optional external source-body custody checks were not replayed; full copies are intentionally absent. Receipt does not hash itself; RECEIPT.sha256 is separate.'}
p=R/'RECEIPT.json';p.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');(R/'RECEIPT.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  RECEIPT.json\n')
print(json.dumps({'decision':'ISSUES_FOUND','issue_count':2,'source_members':len(source),'own_artifacts':len(artifacts),'receipt':pin(p),'report':pin(R/'REPORT.md'),'decision_file':pin(R/'DECISION.json')},indent=2))
