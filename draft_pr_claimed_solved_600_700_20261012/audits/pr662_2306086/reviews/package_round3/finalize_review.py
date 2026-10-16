#!/usr/bin/env python3
"""Recheck exact inputs and freeze this review, writing only beside this file."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

R = Path(__file__).absolute().parent
A = R.parents[1]
REPO = A.parents[2]

def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def need(condition, label):
    if not condition:
        raise ValueError(label)

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

inputs = json.loads((R / 'FINAL_INPUT_RECHECK.json').read_bytes())
need(all(pin(A / name) == record for name, record in inputs['files'].items()), 'late input drift')
state = {'HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip(),
         'branch': subprocess.check_output(['git', 'symbolic-ref', 'HEAD'], cwd=REPO).decode().strip(),
         'index': pin(REPO / '.git/index')}
need(state == inputs['shared_git_state'], 'shared main/index drift')
normal = json.loads((R / 'INDEPENDENT_CHECKS.normal.json').read_bytes())
optimized = json.loads((R / 'INDEPENDENT_CHECKS.optimized.json').read_bytes())
need(normal['status'] == optimized['status'] == 'PASS', 'independent tests')
need(normal['checks'] == 83 and optimized['checks'] == 82, 'independent count')
need(normal['results'][:-1] == optimized['results'], 'shared independent normal/optimized outcomes')
routine = [json.loads((R / ('OFFLINE_CONTROL_RESULTS.' + mode + '.json')).read_bytes())
           for mode in ('normal', 'optimized')]
need(all(report['status'] == 'PASS' and report['checks'] == 147 for report in routine), 'routine tests')
need(routine[0]['results'] == routine[1]['results'] and routine[0]['source_sha256'] == routine[1]['source_sha256'], 'routine equality')
need(routine[0]['source_sha256']['prepare_integration.py'] == 'ca78faf9d061262f694098e2a8588a1a1a53eb8d203c6eab28091cdb9727a61b', 'repaired helper source binding')
optional = json.loads((R / 'OPTIONAL_NUMERICAL_REPLAY.json').read_bytes())
need(optional['status'] == 'PASS' and optional['numerical_certification'] is False and optional['optimizer_rerun'] is False, 'optional replay')
baseline = json.loads((A / 'GWS_GENERATION_INCIDENT_DOCS_BASELINE_CHECK.json').read_bytes())
need(baseline['same_bytes'] is True and len(baseline['other_95_files']['matching_files']) == 95
     and baseline['other_95_files']['differing_files'] == [], 'incident known earlier baseline')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs['final_rechecked_utc'] = now
inputs['all_59_final_pins_still_match'] = True
write(R / 'FINAL_INPUT_RECHECK.json', inputs)
with (R / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + now + ': All59 final input pins and shared main/HEAD/index rechecked unchanged. '
                 'Independent82 shared ordinary/optimized outcomes and147 routine outcomes match; '
                 'real proposed-layout and optional uncertified numerical replay pass. '
                 'Fresh final verdict0mandatory/0optional against the scoped package and repaired operations. '
                 'Reviewer-side generator incident and known earlier baseline equivalence are disclosed; '
                 'no cloud writes, cleanup or restoration. Completion estimate:100% of this bounded review.\n')
paper = inputs['files']['publication/real_schlicht_preschwarzian.pdf']
archive = inputs['files']['publication/real_schlicht_verification.zip']
verdict = {
    'schema': 'pr662-whole-package-review-verdict-v1',
    'reviewer_id': '/root/pr662_package_round3', 'utc': now,
    'pr': 662, 'problem_id': '2306086', 'original_head': 'e31701151c331a6eed9224fb37a75a374ea1043e',
    'verdict': 'PASS_SCOPED_QUALITATIVE_PACKAGE_AND_TIMESTAMP_REPAIRED_OPERATIONS',
    'mandatory_findings': 0, 'optional_findings': 0, 'findings': [], 'findings_waived': False,
    'subtask_completion_estimate_percent': 100,
    'qualitative_scope_only': True, 'historical_firstness_certified': False,
    'present_openness_certified': False, 'sharp_radius_determined': False,
    'human_peer_review': False, 'AI_tools_used_extensively': True,
    'paper_pdf': paper, 'verification_zip': archive,
    'repaired_integration_helper_sha256': 'ca78faf9d061262f694098e2a8588a1a1a53eb8d203c6eab28091cdb9727a61b',
    'actual_publication_confirmed_utc': '2026-10-15T05:09:10.098518+00:00',
    'actual_integration_prepared_utc': '2026-10-15T05:19:04.314562+00:00',
    'exact_publication_instant_invented': False,
    'reviewed_prepared_commit': 'ba75255a589e3262a2188455af82f5ad371e9357',
    'reviewed_prepared_tree': '457b7dd96936f7005d39a688f0dc5d0dbd277581',
    'independent_controls_normal': 83, 'independent_controls_optimized': 82,
    'shared_independent_outcomes_equal': True, 'frozen_author_controls_per_mode': 147,
    'actual_proposed_layout_replayed_with_real_receipts': True,
    'optional_numerical_replayed_uncertified': True,
    'actual_published_doi': '10.5281/zenodo.23384924',
    'actual_tracker_range': "'Math Puzzles'!A94:D94",
    'actual_tracker_receipt_historical_dependency_preserved': True,
    'all_target_scientific_and_operation_sources_unchanged': True,
    'all_actual_publication_and_tracker_receipts_unchanged': True,
    'no_shared_git_mutations_by_reviewer': True, 'no_cloud_writes_or_external_outreach': True,
    'all_reviewer_writes_confined_to_review_folder': False,
    'reviewer_local_generator_incident_disclosed': True,
    'incident_current_content_matches_known_Oct13_baseline': True,
    'incident_immediate_precommand_byte_snapshot_available': False,
    'no_incident_restore_or_delete_performed': True,
    'incident_report': 'OPERATOR_SIDE_EFFECT.json',
    'incident_report_sha256': pin(R / 'OPERATOR_SIDE_EFFECT.json')['sha256'],
    'findings_sha256': pin(R / 'FINDINGS.md')['sha256'],
    'final_inputs_sha256': pin(R / 'FINAL_INPUT_RECHECK.json')['sha256'],
    'acceptance_boundary': 'Exact reviewed tree only; adding this review attestation requires regenerated tree checks. Published eleven scientific inputs and historical actual receipts must retain their bytes. Final live gate and branch/merge readbacks remain required.',
    'future_unprepared_transport_approved': False,
}
write(R / 'VERDICT.json', verdict)
files = {p.name: pin(p) for p in sorted(R.iterdir()) if p.is_file() and p.name != 'FINAL_FREEZE.json'}
write(R / 'FINAL_FREEZE.json', {'schema': 'pr662-round3-review-freeze-v1', 'utc': now,
      'reviewer_id': '/root/pr662_package_round3', 'file_count': len(files), 'files': files,
      'tmp_raw_renders_and_fixtures_excluded': True, 'completion_estimate_percent': 100})
print(json.dumps({'status': 'PASS', 'mandatory_findings': 0, 'optional_findings': 0,
                  'review_files': len(files), 'verdict_sha256': pin(R / 'VERDICT.json')['sha256'],
                  'findings_sha256': pin(R / 'FINDINGS.md')['sha256'],
                  'final_freeze_sha256': pin(R / 'FINAL_FREEZE.json')['sha256']}))
