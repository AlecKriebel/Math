"""Prepare a scoped historical-route progress operator from the reviewed template."""
from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'root_checkpoint_305_priority_progress_033.py').read_text()
s=s.replace('checkpoint_305_priority_progress_033','checkpoint_305_priority_routes_034')
s=s.replace("parent=='68db06cb1aae791432bb45ba865bf344ce5b348a'","parent=='74ed422e0f5716d10c51e5b8ced380d82bfab7cd'")
s=s.replace('bounded_priority_percent=35','bounded_priority_percent=85').replace('bounded_priority_percent\':35','bounded_priority_percent\':85')
s=s.replace('descending_305_workflow_percent=35','descending_305_workflow_percent=40').replace('workflow_percent=35','workflow_percent=40').replace('workflow_percent\':35','workflow_percent\':40')
s=s.replace('Record PR305 bounded-priority primary-source comparisons','Record PR305 closed historical routes and classical implications')
lines=s.splitlines()
for i,line in enumerate(lines):
    if line.startswith('s=load(P/\'SHARED_GIT_WINDOW_STATUS.json\');s.update(utc=utc(),descending_git_checkpoint_preparing=True'):
        lines[i]="s=load(P/'SHARED_GIT_WINDOW_STATUS.json');s.update(utc=utc(),descending_git_checkpoint_preparing=True,descending_checkpoint_scope='Two historical families closed and authenticated; classical implications and fresh ROOT controls retained. New triangle adversary active, no integrated priority/paper/merge/publication clearance.',descending_305_bounded_priority_percent=85,descending_305_workflow_percent=40)"
    if line.startswith("with (P/'RESEARCH_LOG.md').open('a') as f:f.write"):
        lines[i]="with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\\n- '+utc()+' — PR305 two independent historical routes closed, fully read and authenticated; every final file/mode/native capture checked and exact controls freshly reproduced. Phase-constancy failure follows old signed-triangle/Fierobe results. ROOT restricted triangular E/M old-results implication is under a NEW targeted adversary. No full-domain prior E/M proof located in inspected sources; even E and generic complex methods are old. Six unavailable final editions and finite coverage disclosed. No integrated priority/paper/merge/publication clearance. Math100%,bounded priority85%,workflow40%; persistent goal active.\\n')"
    if line.startswith("readme=A/'README.md';body=readme.read_text();"):
        lines[i]="readme=A/'README.md';body=readme.read_text();body+='\\nCurrent historical-route checkpoint: two independent routes closed and ROOT-authenticated. Classical negative-constancy implication verified; restricted N3 equality/multiplier old-results implication under new targeted adversary. Mathematics100%; bounded priority85%; PR workflow40%. No integrated priority or publication clearance.\\n';readme.write_text(body)"
    if line.startswith("assert all('/priority_' not in n"):
        lines[i]="assert all('/sources_private/' not in n and '/root_sources_private/' not in n and '/root_priority_recent_private/' not in n and '/root_priority_current_private/' not in n and '/root_classical_nonconstancy_private' not in n and '/root_priority_triangular_private/' not in n and '/triangle_priority_adversary_20261005/' not in n and not n.endswith(('.pdf','.png','.txt')) for n in paths)"
s='\n'.join(lines)+'\n'
files=["RESEARCH_LOG.md","SHARED_GIT_WINDOW_STATUS.json","inventory.json","checkpoint_305_priority_progress_033_receipt.json","KNOWN_HELD_FILES_FOR_FUTURE_PEER_WINDOW_305.json","root_known_held_inventory_305.py",Path(__file__).name]
own=['README.md','RESEARCH_LOG.md','ROOT_CLASSICAL_NONCONSTANCY_ACQUISITION.json','ROOT_CLASSICAL_NONCONSTANCY_COROLLARY.md','ROOT_CLASSICAL_NONCONSTANCY_SEAL.json','ROOT_PRIORITY_GENERAL_CUSTODY.json','ROOT_PRIORITY_FOCAL_CUSTODY.json','ROOT_TRIANGULAR_OLD_IMPLICATION.md','root_fetch_classical_nonconstancy.py','root_fetch_classical_nonconstancy_v02.py','root_check_classical_triangle_formula.py','root_check_classical_triangle_formula_v02.py','root_seal_classical_priority.py','root_authenticate_priority_general.py','root_authenticate_priority_focal.py','root_triangle_priority_bridge.py','root_triangle_priority_bridge_v02.py']
families={
 'priority_general_20261004':['CRITERIA_FREEZE.md','FULL_PRIORITY_REPORT.md','DERIVATIONS.md','SOURCE_READ_LEDGER.md','SELF_REVIEW.md','STOP_WRITING.md','NATIVE_SOURCE_REGISTRY.json','SOURCE_SEAL.json','SOURCE_SEAL.sha256','check_bridges.py','source_custody.py','validate_custody.py','seal_audit.py','RESEARCH_LOG.md'],
 'priority_focal_20261004':['FROZEN_ACCEPTANCE_CRITERIA.md','CRITERIA_FREEZE.json','FOCAL_PRIORITY_COMPARISON.md','SEARCH_TRAIL.md','SOURCE_CUSTODY.json','CLAIM_COMPARISON.json','FINAL_SELF_CHECK.md','CLOSURE.json','FINAL_SEAL.json','classical_boundary_control.py','classical_boundary_control_initial.py','run_custody.py','verify_custody.py','seal_audit.py','build_metadata.py','RESEARCH_LOG.md']}
labels=['root_classical_nonconstancy_sources_actual001','root_classical_nonconstancy_sources_actual002','root_querret_primary_page283_actual001','root_classical_triangle_formula_actual001','root_classical_triangle_formula_actual002','root_classical_priority_seal_actual001','root_priority_general_custody_actual001','root_priority_general_bridge_actual001','root_known_held_inventory_actual001','root_triangle_priority_algebra_actual001','root_triangle_priority_algebra_actual002','root_priority_focal_custody_actual001','root_priority_focal_control_actual001','root_priority_focal_verifier_actual001','root_priority_v1_table_render_actual001']
new="files=[P/n for n in "+repr(files)+"]+[Path(__file__).resolve()]\n"
# __file__ belongs to the generated operator, while the preparer is separately held.
new+="files+=[A/n for n in "+repr(own)+"]\n"
new+="for family,names in "+repr(families)+".items(): files+=[A/family/n for n in names]\n"
new+="for label in "+repr(labels)+":\n files+=[A/'root_runs_private'/label/n for n in ['execution_spec.json','execution.json','stdout.bin','stderr.bin']]\n"
start=s.index('files=[P/n for n in');end=s.index("allow=P/(NAME+'_allowlist.json')",start)
s=s[:start]+new+s[end:]
assert 'bounded priority35%' not in s and 'workflow35%' not in s
assert "parent=='74ed422e0f5716d10c51e5b8ced380d82bfab7cd'" in s
out=P/'root_checkpoint_305_priority_routes_034.py';out.write_text(s)
print('Prepared only; operator has not run:',out)
