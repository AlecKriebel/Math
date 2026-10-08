"""ROOT conditional program-three postimages; no provider or program writes."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import copy,json,os
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
P=C/'draft_pr_publication_program_20260930';A=P/'audits/pr148_5100002';D=Path(__file__).resolve().parent/'ROOT_POSTIMAGES_01'
def require(v,msg):
    if not v:raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'mode':p.stat().st_mode&511,'sha256':sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
gate=P/'audits/pr147_5100001/ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json'
require(pin(gate)['sha256']=='d69d5b9d92422969f69156ebf2fca144eba1ca7d8dc78cb76cb2ab83e0f1f7c5','actual previous completion')
mathgate=A/'ROOT_MATHEMATICAL_GATE_20261008.json'
require(pin(mathgate)['sha256']=='7c19c3bb1b1ac652360b989655c324ce6b7c241c5780bba91fa91eb073ea7883','ROOT mathematical acceptance')
mg=read(mathgate);require(mg['mathematical_clearance'] is True and mg['mandatory_mathematical_findings']==[],'math gate status')
goalpath=A/'ROOT_GOAL_TOOL_OBSERVATION_20261008.json';goal=read(goalpath)
require(goal['actual_tool_response']['goal']['status']=='active','actual persistent goal remains active')
before={name:pin(P/name) for name in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
old=read(P/'CURRENT_PROGRESS.json');current=copy.deepcopy(old);g=read(gate)
require(old['current_PR']==147 and old['fully_completed_count']==26 and old['published_count']==14,'accepted prior scope')
current['historical_preparation_snapshots'].append({'UTC':old['UTC'],'status':'COMPLETED_PR147_SUPERSEDED_AS_CURRENT','prior_current_fields':{k:v for k,v in old.items() if k.startswith('current_')},'actual_final_acceptance':pin(gate),'note':'Exact dated prior current fields retained. The genuine separate final receipt supplies actual completed publication/install/readback/commit facts.'})
current['historical_completed_case_records'].append({'PR':147,'fields':{k:v for k,v in old.items() if k.startswith('last_completed_')},'actual_final_acceptance':pin(gate),'note':'Prior completion-family fields are retained without retroactively altering its earlier conditional postimage.'})
for key in list(current):
    if key.startswith('current_'):del current[key]
now=datetime.now(timezone.utc).isoformat()
current.update(UTC=now,updated_UTC=now,actual_active_metadata_preparer_PID=os.getpid(),actual_final_metadata_preparer_PID=None,
    current_PR=148,current_problem_id=5100002,current_code='AMR-050-0002',current_original_head='538fd2584f7dc7375e4eaa91d73daddde3d073cd',current_original_budget='1/5',current_original_literal_status='claimed_solved',
    current_original_author_approach_ledger_present=True,current_original_author_approach_ledger_path='turns.json',current_original_substantive_author_approach_count=1,current_actual_timestamped_author_chat_turn_ledger_present=False,current_original_native_transition_ledger_present=False,current_new_central_proof_search_turns=0,
    current_original20_archive_preserved=True,current_original20_preservation_scope='All20 frozen original bodies preserved; active guarded support intentionally differs and is separately pinned.',
    current_source_authentication_percent=100,current_mathematical_audit_percent=100,current_mathematical_clearance=True,current_mathematical_gate='audits/pr148_5100002/ROOT_MATHEMATICAL_GATE_20261008.json',current_mathematical_gate_sha256=pin(mathgate)['sha256'],
    current_mathematical_target=mg['target'],current_mathematical_scope=mg['strongest_verified_result'],current_mathematical_scope_limits=mg['scope_limits'],current_source_convention_refinement=mg['source_convention_refinement'],
    current_disposition='mathematics_verified_priority_audit_in_progress',current_PR_workflow_percent=30,current_workflow_estimate_percent=30,current_core_disposition_complete=False,
    current_priority_audit_percent=0,current_priority_clearance=False,current_priority_gate=None,current_priority_gate_sha256=None,current_priority_status='independent_priority_families_in_progress',current_priority_audit_scope='Exact named conjecture history, general invariant mechanisms, and known six-period geometry are being investigated independently. No novelty or publication decision yet.',
    current_novelty_established=False,current_absolute_priority_established=False,current_exclusive_priority_established=False,current_independent_discovery_established=False,current_copying_or_collaboration_inferred=False,current_PR50_exception_used=False,
    current_publication_package_prepared=False,current_publication_package_review_clearance=False,current_publication_package_review_status='not_prepared',current_publication_package_reviews_required=True,current_publication_ready=False,current_publication_upload_clearance=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,
    current_native_completion_acceptance=None,current_native_completion_acceptance_sha256=None,current_native_disposition_checkpoint_commit=None,current_native_local_installed_path_count=0,current_native_public_changed_path_count=0,current_native_status=None,current_native_export_state='NOT_PREPARED_OR_PERFORMED',
    current_closed_without_merging=False,current_closed_without_publication=False,current_actual_closing_comment_url=None,current_completion_metadata_checkpoint_pending=False,
    current_active_checkpoint_pending=True,active_checkpoint_commit=None,active_checkpoint_acceptance_receipt=None,active_checkpoint_actual_readback_required=True,active_checkpoint_source_plan_review_required=True,active_checkpoint_publication_performed_by_this_preparation=False,active_checkpoint_local_installation_performed_by_this_preparation=False,advance_to_next_PR_authorized_now=False,
    persistent_goal_complete=False,persistent_goal_status='active',persistent_goal_status_at_last_tool_read='active',persistent_goal_API_last_observed_UTC=goal['observed_UTC'],persistent_goal_API_updatedAt=goal['actual_tool_response']['goal']['updatedAt'],persistent_goal_status_observation_source='audits/pr148_5100002/ROOT_GOAL_TOOL_OBSERVATION_20261008.json',persistent_goal_status_observation_sha256=pin(goalpath)['sha256'],persistent_goal_status_observation_is_dated_ROOT_readback=True,
    last_completed_PR=147,last_published_PR=147,last_completed_metadata_checkpoint_commit=g['final_commit'],last_completed_actual_final_gate='audits/pr147_5100001/ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json',last_completed_final_completion_readback='audits/pr147_5100001/ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json',last_completed_actual_writer_release='audits/pr147_5100001/ROOT_FINAL_PROGRAM_WRITER_RELEASE_20261008.json',
    latest_ordered_intake_record='ordered_intake_20261008/after_PR147/ROOT_INTAKE_ACCEPTANCE.json',next_numeric_intake_cursor=149,next_eligible_PR_after_current_completion=None,next_eligible_order_requires_fresh_status_check=True,
    workflow_estimate_percent=round(26/99*100,2),fully_completed_fraction_percent=round(26/99*100,2),workflow_estimate_definition='26 of the dated99 eligible cases are fully completed,14 published; active148 workflow30%. Denominator is the preserved dated census, not a claim of a new live total.',
    program_snapshot_UTC_semantics='This UTC records conditional preparation. Actual scoped push, separate local program3 installation, independent full readback and release will be supplied by a separate genuine ROOT receipt after those actions.',
    program_snapshot_semantics='Current148 mathematics is accepted. Priority/publication/native are pending. Previous147 is actually complete and its exact final receipt is recorded.',
    program_snapshot_authority_condition='These postimages become the selected current program checkpoint only after exact reviewed publication, local installation, full readback and owned barrier release; no future actual commit or receipt is preclaimed.',
    completion_metadata_checkpoint_pending_at_snapshot=False)
current['last_completed_transaction_receipt_reference'].update(metadata_commit=g['final_commit'],metadata_actual_PID=g['actual_ROOT_PID'],metadata_actual_UTC=g['UTC'],final_metadata_readback='audits/pr147_5100001/ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json',final_metadata_readback_sha256=pin(gate)['sha256'])
remaining='Complete and adversarially adjudicate the three independent bounded priority audits; prepare a paper only if the claimed resolution survives. Then follow whole-package fresh review/repair loops, exact Zenodo publication, one tracker row, original-head disposition and actual native/final acceptance. This active program checkpoint itself still requires actual source/data/plan review, scoped publication/install/readback and release.'
current.update(current_remaining_required_steps=remaining,remaining_current_step=remaining,next_step=remaining)
current['current_supporting_repairs_accepted']=['Explicit scientific guards in author/inherited and two independent support implementations','Frozen reviewed-source binding and fresh per-run output/process-closure receipts; historical original scripts untouched']
require(current['fully_completed_eligible_PRs']==old['fully_completed_eligible_PRs'] and current['published_PRs']==old['published_PRs'],'no counts/case-list increment')
note='\n\n## '+now+' — PR148 mathematical checkpoint; case30%, mathematics100%, priority in progress;26/99 completed,14published\n\nPR147 is actually complete at final checkpoint '+g['final_commit']+', accepted by ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json SHA'+pin(gate)['sha256']+'. Its DOI10.5281/zenodo.23231145 and actual tracker row57 remain complete. The fresh after147 status-only intake selected literal claimed_solved PR148 at original538fd2584f7dc7375e4eaa91d73daddde3d073cd, problem5100002/AMR-050-0002. No later PR has been reviewed.\n\nThe literal Table2 k108 quotient is refuted by two convex primitive six-period orbits on one continuous physical confocal billiard family. Exact values11664/3125 and3645/1024 differ by553311/3200000. Independent finite-chord/reflection geometry and projective tangent-map/support-area derivations pass; direct T³=antipode supplies family closure. Internal-angle convention is calibrated by source k101; no corrected all-period invariant is proved. Original assertion-only verification is historical. Active support uses explicit guards, source pins and8 fresh closed ROOT normal/optimized reproductions; meaningful negative controls reject in both modes. The wrapper\u2019s initial status-schema diagnostic is retained and corrected, with no stale PASS accepted. ROOT math gate SHA'+pin(mathgate)['sha256']+'.\n\nPriority is in progress in independent exact-history, general-invariant and known-six-period-geometry families. No novelty, paper, DOI, tracker, native disposition or merge/close is accepted for148. Original effort1/5 is ONE reported approach in turns.json; no timestamped author chat-turn or native-transition ledger is supplied, and audit adds zero central proof-search turns. Frozen original20 and prior histories remain preserved. Persistent goal is ACTIVE unfinished. These are conditional preparation postimages: actual checkpoint publication, local program3 installation, independent full readback and barrier release remain pending and will have a separate actual receipt. Earlier paragraphs below/above remain dated historical evidence, with this entry supplying the latest current state.\n'
D.mkdir(exist_ok=False)
bodies={'CURRENT_PROGRESS.json':(json.dumps(current,indent=2,sort_keys=True)+'\n').encode(),'CURRENT_PROGRESS.md':(P/'CURRENT_PROGRESS.md').read_bytes()+note.encode(),'RESEARCH_LOG.md':(P/'RESEARCH_LOG.md').read_bytes()+note.encode()}
post={}
for name,body in bodies.items():
    with (D/name).open('xb') as f:f.write(body);os.fchmod(f.fileno(),420)
    post[name]=pin(D/name)
record={'schema':'pr148-root-active-program-render/v1','UTC':now,'actual_ROOT_PID':os.getpid(),'before':before,'postimages':post,'source':pin(Path(__file__).resolve()),'baseline_gate':pin(gate),'mathematical_gate':pin(mathgate),'goal_record':pin(goalpath),'publication_installation_or_final_acceptance_performed':False,'case_percent':30,'completed_count':26,'published_count':14}
(D/'RENDER_RESULT.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'CONDITIONAL_ACTIVE148_POSTIMAGES_ONLY','render':pin(D/'RENDER_RESULT.json')}))
