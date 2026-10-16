"""Prepare a non-authorizing, exact-state candidate for the fresh source05 audit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent/'preprint';P=D.parent/'publication'
H=D/'history/release_helpers_review03_frozen'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pin=lambda p:dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p))
load=lambda p:json.loads(p.read_text())
old=load(H/'FINAL_CLEARANCE.json')
assert sha(H/'FINAL_CLEARANCE.json')=='9f1a0e3829d6d44719e894fa653b878170dac1bd434244f8c73cf973de90cc6a'
assert (R/'FINAL_CLEARANCE.json').read_bytes()==(H/'FINAL_CLEARANCE.json').read_bytes()
manifest=load(H/'ARCHIVE_MANIFEST.json')
rows={x['path']:x for x in manifest['files']}
assert len(rows)==len(manifest['files'])==14
for name,row in rows.items():assert pin(H/name)==row
for name in ['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json','STAGE_ATTEMPT.json',
    'PUBLISH_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json',
    'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']:
    assert (P/name).read_bytes()==(H/name).read_bytes()
z=load(H/'ZENODO_VERIFIED_PUBLICATION.json');t=load(H/'TRACKER_VERIFIED_APPEND.json')
assert z['id']==23398175 and z['doi']=='10.5281/zenodo.23398175'
assert t['updated_range']=="'Math Puzzles'!A113:D113" and t['append_count']==1
for row in old['submission_files']+[old['source_manifest'],old['manuscript_source']]:assert pin(R/row['path'])==row
assert sha(R/'metadata.json')==old['publication_metadata_sha256']
assert sha(R/'PACKAGE_MANIFEST.json')==old['package_manifest_sha256']
assert sha(R/'deposit.json')==old['deposit_manifest_sha256']
candidate=dict(old)
candidate.update(schema='PR210-renewed-workflow-clearance-candidate-v1',utc=datetime.now(timezone.utc).isoformat(),
    release_cleared=False,candidate_only=True,supporting_source05_pending=True,
    case_completion_percent=85,prior_published_clearance_sha256=sha(H/'FINAL_CLEARANCE.json'),
    release_helpers=[pin(p) for p in sorted(P.glob('*.py'))],
    supplemental_readonly_reconciliation=pin(D/'reconcile_published_release_readonly.py'),
    initial_publication_tracker_state=dict(
        record_id=z['id'],doi=z['doi'],doi_url=z['doi_url'],record_url=z['record_url'],
        spreadsheet_id=t['spreadsheet_id'],sheet_id=t['sheet_id'],sheet_title='Math Puzzles',
        updated_range=t['updated_range'],values=t['values'],archive_manifest=pin(H/'ARCHIVE_MANIFEST.json'),
        publication_receipt=rows['ZENODO_VERIFIED_PUBLICATION.json'],
        tracker_receipt=rows['TRACKER_VERIFIED_APPEND.json'],stage_intent=rows['STAGE_ATTEMPT.json'],
        publish_intent=rows['PUBLISH_ATTEMPT.json']),
    actual_deposit_tracker_native_actions_not_yet_performed=False,
    actual_deposit_and_tracker_complete=True,actual_native_merge_pending=True,
    counts_before_native_merge=[43,21,20,0],
    final_supporting_source_review={'pending_family':'release_helpers_adversary_05'},
    renewed_clearance_reason='Only native MAIN placeholder guard and strictly read-only receipt rebinding repaired; no scientific file, metadata, deposit manifest, record or tracker row change. No additional stage/publish/append authorized.')
out=D/'RENEWED_CLEARANCE_CANDIDATE.json';assert not out.exists()
out.write_text(json.dumps(candidate,indent=2)+'\n')
print(json.dumps(dict(candidate_sha256=sha(out),release_cleared=False,
    current_helper_pins=candidate['release_helpers'],supplemental=candidate['supplemental_readonly_reconciliation'],
    original_archive_manifest_sha256=sha(H/'ARCHIVE_MANIFEST.json')),indent=2))
