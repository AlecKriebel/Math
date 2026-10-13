"""Create exact clearance only after ROOT's closed clean NEW whole review."""
from root_submission_gate import *

assert not (A/'PUBLISHING_CLEARANCE.json').exists()
f = load(A/'ROOT_PREPRINT02_ADJUDICATION.json')
assert f['status'] == 'PASS_ROOT_CLOSED_CLEAN_FULL_PREPRINT_REVIEW' and f['unresolved_findings'] == 0
assert f['complete_report_read'] and f['independent_reproduction_verified']
assert f['sealed_review_authenticated'] and f['source_gate_unchanged'] and f['all_released_inputs_unchanged']
closed = load(A/'ROOT_FINAL_CLOSED_EVIDENCE.json')
assert closed['status'] == 'ALL_CURRENT_SCIENTIFIC_AND_REVIEW_FROZEN_FILES_BOUND'
assert pin(A/'ROOT_PREPRINT02_ADJUDICATION.json') == closed['final_review_adjudication']
for n,e in closed['closed_scientific_files'].items():
    assert pin(A/n) == e
for n,e in closed['historical_build_evidence_files'].items():
    assert pin(A/n) == e
q = load(Q/'MANIFEST.json')
assert len(q) == 12
package = {str(p.relative_to(Q)):pin(p) for p in Q.rglob('*') if p.is_file()}
assert set(package) == set(q) | {'MANIFEST.json'}
for n,e in q.items():
    assert package[n] == {**e,'mode':'0444'}
submission = load(O/'SUBMISSION_MANIFEST.json')
assert len(submission['formal_files']) == 4
formal = {n:pin(O/n) for n in FORMAL}
assert all(formal[n] == e for n,e in submission['formal_files'].items())
assert package['MANIFEST.json']['sha256'] == submission['source_package_manifest_sha256']
assert package['MANIFEST.json']['sha256'] == 'e08af5edc9c4aed6ccb4b92b3b2e8ea0505a02e762b27c31efbacf00d7b8f683'
assert formal['SUBMISSION_MANIFEST.json']['sha256'] == '043de76e326db5b5ba1af7fe2c7442bef1eed2d04de36654605045ce61f40383'
assert formal['mtp2-edge-closure-note.tex']['sha256'] == package['mtp2_edge_closure.tex']['sha256']
assert formal['mtp2-edge-closure-note.pdf']['sha256'] == package['output/pdf/mtp2_edge_closure.pdf']['sha256']
assert (O/'zenodo-deposit.json').read_bytes() == (Q/'zenodo-deposit.json').read_bytes()
metadata = load(O/'zenodo-deposit.json')
assert metadata['metadata'] == load(A/'publication_preparation/DRAFT_ZENODO_METADATA.json')
assert set(metadata) == {'metadata','files'} and len(metadata['metadata']) == 11
assert metadata['metadata']['publication_type'] == 'preprint'
assert metadata['metadata']['creators'] == [{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]
assert {x['path'] for x in metadata['files']} == {'mtp2-edge-closure-note.pdf','mtp2-edge-closure-verification.zip'}
immutable_names = ['snapshot_manifest.json','ROOT_MATHEMATICAL_ACCEPTANCE.json','ROOT_PRIORITY_DECISION_03.json',
    'ROOT_PREPRINT01_ADJUDICATION.json','ROOT_PREPRINT_REPAIR_V02.json','ROOT_PREPRINT02_SOURCE_GATE.json',
    'ROOT_PREPRINT02_ADJUDICATION.json','ROOT_FINAL_CLOSED_EVIDENCE.json','CURRENT_CORRECTIONS.json',
    'publication_preparation/DRAFT_ZENODO_METADATA.json']
immutable = {n:pin(A/n) for n in immutable_names}
immutable.update(closed['historical_build_evidence_files'])
out = {'recorded_utc':utc(),'status':'READY_AFTER_GLOBAL_REPAIRS_AND_NEW_FULL_PREPRINT_REVIEW',
    'original_head':ORIGINAL_HEAD,'original_status':'claimed_solved','original_author_turn_count':'2/5',
    'final_clean_review':2,'unresolved_findings':0,'historical_review01_findings_retained':True,
    'first_review_repairs':['R1','R2','R3'],'final_review_closure':'ROOT_PREPRINT02_ADJUDICATION.json',
    'formal_submission_files':formal,'package_files':package,'immutable_root_artifacts':immutable,
    'closed_scientific_files':closed['closed_scientific_files'],
    'historical_first_priority_certified':False,'unrefereed':True,'extensive_AI_use':True,'human_peer_review_claimed':False,
    'mathematical_percent':100,'bounded_priority_percent':100,'workflow_percent':75,
    'merge_performed':False,'zenodo_publication_performed':False,'tracker_append_performed':False,
    'remaining_steps':['exact_live_PR_refresh_and_merge','exact_postmerge_tree_and_submission_verification',
                       'production_Zenodo_stage_inspect_publish_public_file_and_metadata_readback',
                       'fresh_GWS_duplicate_scan_one_append_and_exact_readback','scoped_completion_checkpoint'],
    'persistent_goal_complete':False}
with (A/'PUBLISHING_CLEARANCE.json').open('x') as h:
    h.write(json.dumps(out,indent=2)+'\n')
current_clearance()
stamp = utc()
window()
s = load(A/'CURRENT_PACKAGE_STATUS.json')
s.update(recorded_utc=stamp,status='READY_AFTER_NEW_CLEAN_WHOLE_REVIEW',second_full_review_active=False,
         second_full_review_closed=True,publication_ready=True,workflow_percent=75,unresolved_findings=0)
(A/'CURRENT_PACKAGE_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
inv = load(P/'inventory.json')
row = next(x for x in inv['items'] if x['number'] == 311)
assert row['submitted_status'] == row['original_submitted_status'] == 'claimed_solved'
row.update(audit_workflow_percent=75,workflow_percent=75,preprint_ready=True,publication_ready=True,
           final_clean_review=2,disposition='preprint_cleared_exact_merge_publication_pending')
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
shared = load(P/'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp,descending_311_workflow_percent=75,descending_311_preprint_ready=True,
              descending_311_preprint_review_02_complete=True,descending_311_preprint_review_02_whole_review_active=False)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as h:
        h.write('\n'+stamp+' — PR311 exact v02 publishing clearance created only after ROOT full-read/authenticated/reproduced NEWwhole-review02 with zero unresolved findings. All prior scientific seal payloads and readonly proof/priority/review files,31released inputs,13package members and five formal files remain bound; original29files and2/5 preserved. All three first-review defects repaired globally and historical adverse records retained. Math100%,boundedpriority100%,workflow75%; actual merge, production deposit, public readback and exact-once GWS registration remain pending. No historical-first or human-peer-review certificate; persistent goal active.\n')
print(json.dumps({'recorded_utc':out['recorded_utc'],'status':out['status'],'formal_file_count':len(formal),
    'package_file_count':len(package),'closed_scientific_file_count':len(out['closed_scientific_files']),
    'workflow_percent':75,'merge_performed':False,'persistent_goal_complete':False},indent=2))
