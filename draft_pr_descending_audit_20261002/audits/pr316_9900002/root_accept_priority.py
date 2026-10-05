"""Bind fully read priority proofs and source scope; no branch or publication action."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

A = Path(__file__).resolve().parent
F = A / 'priority_independent'
C = A / 'classical_priority_adversary'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(p):
    return dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()),
                mode=oct(p.stat().st_mode & 0o7777))

expected = {
    F / 'FINAL_PRIORITY_REPORT.md': 'c2e8bfa7c197e0398f2f27d12b9064f5af1503aeb09d485f20211c3b0d3cb12b',
    F / 'SLOW_VARIATION_COROLLARY.md': 'bc8f4d2c49ed9c5a7da9be3c67e423e3b7e74cb25d06f556091ae15e7143a1cc',
    F / 'FINAL_SHA256.json': '22c41e6e9da9157d4d04fe85da73e24bfd1135e5bb24392f51cb8a5a69c06aa4',
    F / 'FREEZE_RECEIPT.json': '9a809a63dd90579b64750e4b4e8099067da521972c5388bc9b2dd0505880649a',
    C / 'report.md': 'c75f864b828e2fd180b4144de13867bed220ab4cfe71cf29bc11856066c89f1e',
    C / '00_independent_assessment_frozen.md': '498faee71b3ecde3fdb1c8cc94f78447e55307a95d790ef17e730c8a64956690',
    F / 'slow_tail_adversary/report.md': '2b4bbdf65b5206b9d98deca06e86938ce6498568f6487182e457f5592d5f081f',
    F / 'slow_tail_adversary/research_log.md': 'b349e4900c229a3c3d56f2dbea1be472a4f3509beb3c68077df1b0021b6a94ac',
}
for p, digest in expected.items():
    require(sha(p.read_bytes()) == digest, 'Read priority artifact changed: ' + str(p))
manifest = load(F / 'FINAL_SHA256.json')
require(len(manifest['files']) == 132, 'Unexpected closed priority evidence count')
require(len({x['path'] for x in manifest['files']}) == 132, 'Duplicate evidence paths')
for entry in manifest['files']:
    p = Path(entry['path'])
    require(p.is_relative_to(F) and p.is_file() and not p.is_symlink(), 'Evidence path escaped')
    require(p.stat().st_size == entry['bytes'] and sha(p.read_bytes()) == entry['sha256']
            and format(p.stat().st_mode & 0o7777, 'o') == entry['mode'] == '444',
            'Closed evidence binding failed: ' + str(p))
receipt = load(F / 'FREEZE_RECEIPT.json')
require(len(receipt['permission_transitions']) == 130, 'Unexpected freeze count')
require(receipt['explicit_644_to_444_count'] == 127 and receipt['already_444_count'] == 3,
        'Unexpected mode history')
for entry in receipt['permission_transitions']:
    p = Path(entry['path'])
    require(p.is_relative_to(F) and sha(p.read_bytes()) == entry['sha256']
            and p.stat().st_size == entry['bytes'] and entry['new_mode'] == '444'
            and entry['previous_mode'] in ['644', '444'], 'Mode/history binding failed')
require(len(receipt['all24_first_stage_pins_verified']) == 24, 'Missing early source pins')
for entry in receipt['all24_first_stage_pins_verified']:
    require(entry['ok'] and sha(Path(entry['path']).read_bytes()) == entry['sha256'],
            'Early source bytes changed')
gate = load(A / 'ROOT_PRIORITY_SOURCE_GATE.json')
for name, old in gate['held_files'].items():
    require(sha((F / name).read_bytes()) == old['sha256']
            and old['mode'] == '0o644' and pin(F / name)['mode'] == '0o444',
            'Early priority bytes or explicit mode transition mismatch')
decision = load(C / 'decision.json')
require(decision['recommended_operational_status'] == 'already_solved'
        and decision['classical_input_authenticated']
        and decision['explicit_elementary_admissible_example_verified']
        and not decision['candidate_read'] and not decision['other_reviewer_reports_read']
        and decision['remaining_mathematical_gap_for_audited_target'] == 'none',
        'Fresh historical adversary has unresolved proof gap')
source = C / 'evidence/erickson1970_original_article.pdf'
require(sha(source.read_bytes()) == decision['primary_article_sha256']
        == '65716b4789f1f1b06400a286bb216fee368783c2eca7df750d2fe00d791b773b',
        'Independent primary article changed')
require((F / 'evidence/erickson1970_mirror.pdf').read_bytes() == source.read_bytes(),
        'Two independently obtained original article binaries differ')
actual_runs = []
for p in sorted((C / 'executions').glob('*.json')):
    entry = load(p)
    for stream in ['stdout', 'stderr']:
        require(sha((C / entry[stream]).read_bytes()) == entry[stream + '_sha256'],
                'Actual source acquisition stream changed')
    for path, digest in entry['input_code_sha256'].items():
        require(sha(Path(path).read_bytes()) == digest, 'Actual acquisition input changed')
    actual_runs.append(dict(record=str(p), argv=entry['argv'],
                           started_utc=entry['started_utc'], ended_utc=entry['completed_utc'],
                           exit_code=entry['exit_code']))
criteria = A / 'priority_correction_review/INDEPENDENT_SOURCE_CRITERIA.md'
require(sha(criteria.read_bytes()) == '51e989a13290c5c3ace41717cb0e63d6a14fddf91a0cbece53218d6e001baeb9',
        'Correction reviewer source-first assessment changed')
(A / 'ROOT_CORRECTION_REVIEW_SOURCE_GATE.json').write_text(json.dumps(dict(
    utc=utc(), status='ROOT_ENTIRE_SOURCE_CRITERIA_READ_BEFORE_EXPLICIT_PACKET_RELEASE',
    held_file=pin(criteria), path=str(criteria),
    record_timing='Written after the explicit release message; complete semantic read occurred before that release. No retroactive before-release byte-check timestamp asserted.',
    capacity_failure='Reviewer first turn ended with selected-model-at-capacity after source freeze; continued with unchanged model and preserved context',
    candidate_and_packet_release_authorized=True), indent=2) + '\n')
out = dict(
    utc=utc(), status='PASS_PR316_CLASSICAL_COROLLARY_PRIORITY_ADJUDICATION',
    pr=316, original_submitted_head='c96a3b2019ed3d6aabe0612b31491161dcb275e8',
    original_submitted_status='claimed_solved', author_turns='1/5',
    submitted_mathematics_accepted=True, mathematical_completion_percent=100,
    bounded_priority_audit_completion_percent=100, workflow_completion_percent=55,
    adjudicated_operational_status='already_solved',
    exact_status_qualification='General existential negative answer is an exact elementary consequence of authenticated1970 index-zero renewal asymptotics; no earlier explicit announcement answering the later named question authenticated',
    strongest_verified_classical_result='For positive finite-a.s. iid ordinary renewal increments with slowly varying tail, every positive deterministic normalization that is asymptotically tight converges to zero in probability; the continuous logarithmic-tail law is an admissible non-lattice infinite-mean example with an elementary proof',
    submitted_lacunary_example_outside_regular_variation=True,
    submitted_construction_historical_priority='Unestablished; absence of a located predecessor is not a firstness certificate',
    prior_explicit_named_solution_authenticated=False, firstness_certified=False,
    root_entire_semantic_reads=['Final independent priority report and complete corollary',
                               'Complete conditional fresh adversary proof and log',
                               'Complete independently sourced classical adversary proof, decision and log',
                               'Fresh correction reviewer source-first criteria'],
    root_primary_visual_read_scope='Erickson printedpp265–266; extractedpp263–266. Article binary identical in two independently obtained mirror acquisitions. No full29-page article read claimed.',
    bound_read_artifacts={str(p): pin(p) for p in expected},
    closed_priority_evidence_pins_verified=132, first_stage_source_pins_verified=24,
    actual_freeze_mode_changes=127, historical_mode_transitions_explicit=True,
    independent_native_source_acquisition_runs_bound=actual_runs,
    independence_limit='Directed root hypothesis to priority family; its source-first freeze/core deduction predated incidental list_agents summaries. Two conditional/source-backed fresh corollary adversaries had no candidate/reviewer-report access. Full limitation retained in priority report.',
    source_access_limit='Thorisson relevant indexed institutional primary definitions and Problem1.2 verified; full original binary/visual access unavailable. Classical article mirror provenance disclosed, official-host byte comparison unavailable.',
    remaining_work=['Fresh corrected-packet adversarial review and exact finalization',
                    'Publish current wrapper/queue priority correction with verified preservation',
                    'Leave corrected already_solved draft unmerged per current scope and advance descending intake'],
    branch_or_PR_change_by_this_program=False, paper_authorized=False, merge_authorized=False,
    zenodo_upload=False, doi=None, tracker_append=False, external_individual_communication=False,
    persistent_goal_complete=False)
(A / 'ROOT_PRIORITY_ADJUDICATION.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(utc=out['utc'], status=out['status'],
                      operational_status='already_solved', evidence_pins=132,
                      primary_mirror_binary_sha256=decision['primary_article_sha256'],
                      mathematical_gap='none', explicit_prior_named_answer='not authenticated',
                      paper=False, merge=False, workflow_percent=55), indent=2))
