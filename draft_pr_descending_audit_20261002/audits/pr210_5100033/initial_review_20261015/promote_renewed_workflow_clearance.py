"""After genuine clean source05 acceptance, authorize the exact repaired workflow.

Only replaces local clearance; no provider, sheet, Git or PR action. Historical
published clearance/evidence remain immutable. Fresh read-only receipt rebinding
is still necessary before the actual native integration can pass its guards.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os
D=Path(__file__).resolve().parent;R=D.parent/'preprint';P=D.parent/'publication'
H=D/'history/release_helpers_review03_frozen'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
root=load(D/'ROOT_RELEASE_HELPER_REVIEW05_ACCEPTANCE.json')
assert root['clean_version_bound_acceptance'] is True
assert root['mandatory_findings']==root['optional_findings']==[]
assert root['all_three_source04_findings_resolved'] is True
assert root['candidate_sha256']==sha(D/'RENEWED_CLEARANCE_CANDIDATE.json')
candidate=load(D/'RENEWED_CLEARANCE_CANDIDATE.json')
assert candidate['release_cleared'] is False and candidate['candidate_only'] is True
assert candidate['release_helpers']==root['reviewed_helpers']
assert candidate['supplemental_readonly_reconciliation']==root['reviewed_supplemental_reconciler']
for row in candidate['release_helpers']:
    q=P/row['path'];assert q.stat().st_size==row['bytes'] and sha(q)==row['sha256']
q=D/candidate['supplemental_readonly_reconciliation']['path'];row=candidate['supplemental_readonly_reconciliation']
assert q.stat().st_size==row['bytes'] and sha(q)==row['sha256']
S=D/'release_helpers_adversary_05';manifest=S/'AUTHORED_MANIFEST.json'
assert sha(manifest)==root['manifest_sha256']
for row in load(manifest)['files']:
    q=S/row['path'];assert q.resolve().is_relative_to(S.resolve()) and not q.is_symlink()
    assert q.stat().st_size==row['bytes'] and sha(q)==row['sha256']
assert sha(S/'REPORT.md')==root['report_sha256']
assert (R/'FINAL_CLEARANCE.json').read_bytes()==(H/'FINAL_CLEARANCE.json').read_bytes()
assert sha(H/'FINAL_CLEARANCE.json')==candidate['prior_published_clearance_sha256']
for name in ['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json','STAGE_ATTEMPT.json',
             'PUBLISH_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json',
             'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']:
    assert (P/name).read_bytes()==(H/name).read_bytes()
assert not (P/'NATIVE_PREPARE_ATTEMPT.json').exists() and not (P/'PR_PREPARED.json').exists()
clear=dict(candidate);clear.pop('candidate_only');clear.pop('supporting_source05_pending')
clear.update(schema='PR210-genuine-renewed-workflow-clearance-v1',utc=datetime.now(timezone.utc).isoformat(),
    release_cleared=True,case_completion_percent=90,supporting_source_reviews_completed=5,
    final_supporting_source_review=dict(family='release_helpers_adversary_05',manifest_sha256=root['manifest_sha256'],
        report_sha256=root['report_sha256'],mandatory_findings=[],optional_findings=[]),
    initial_publication_receipts_preserved_under_previous_binding=True,
    read_only_binding_reconciliation_still_required=True)
clear['accepted_root_receipts'] += [dict(path=name,sha256=sha(D/name)) for name in [
    'ROOT_SOURCE04_REPAIR_ACCEPTANCE.json','ROOT_ACTUAL_MAIN_PLACEHOLDER_CONTROLS.json',
    'ROOT_READONLY_RECONCILIATION_REPAIR_CONTROLS.json','ROOT_RELEASE_HELPER_REVIEW05_ACCEPTANCE.json']]
raw=(json.dumps(clear,indent=2)+'\n').encode();temp=R/'FINAL_CLEARANCE.renewed-tmp'
with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
os.replace(temp,R/'FINAL_CLEARANCE.json')
spec=importlib.util.spec_from_file_location('pr210_renewed_pure_binding',P/'release_binding.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);g.sync_directory(R)
ctx=g.context(R)
result=dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=90,
    previous_published_clearance_sha256=sha(H/'FINAL_CLEARANCE.json'),new_clearance_sha256=sha(R/'FINAL_CLEARANCE.json'),
    release_binding=g.binding(ctx),same_exact_published_pair=ctx['expected_files'],metadata_unchanged=True,
    final_source05_manifest_sha256=root['manifest_sha256'],final_source05_report_sha256=root['report_sha256'],
    mandatory_findings=[],optional_findings=[],source04_all_three_mechanisms_resolved=True,
    fresh_readonly_reconciliation_required_before_native_action=True,additional_stage_publish_append_calls=0,
    actual_native_merge_pending=True,goal_active_incomplete=True)
out=D/'RENEWED_WORKFLOW_CLEARANCE_RECEIPT.json'
with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
state=load(D/'CURRENT_AUDIT_STATE.json');state.update(utc=result['utc'],completion_percent=90,case_completion_percent=90,
    stage='renewed_source05_clearance_readonly_receipt_reconciliation_next',
    current_stage='renewed_source05_clearance_readonly_receipt_reconciliation_next',
    final_clearance_sha256=result['new_clearance_sha256'],release_helper_source_review05_active=False,
    release_helper_source_reviews_completed=5,release_helper_source_review_active=False,new_source05_acceptance_pending=False,
    preprint_upload_cleared=True,renewed_release_binding_reconciliation_pending=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+result['utc']+' — PR21090%: clean fresh source05 and root acceptance sealed. Genuine renewed clearance binds unchanged scientific pair/metadata plus repaired7sources and exact original record23398175/MathPuzzles113/immutable historical evidence. Initial genuine publication/tracker/intents retained under archived9f1a clearance; strictly read-only revalidation/rebinding next, no new stage/publish/append authorized. Native merge remains.\n')
print(json.dumps(result,indent=2))
