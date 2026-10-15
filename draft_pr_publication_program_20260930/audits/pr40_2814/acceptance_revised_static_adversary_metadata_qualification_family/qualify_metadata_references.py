#!/usr/bin/env python3
"""Own adjacent administrative qualification, preserving the closed31-member review."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
F = A / 'acceptance_revised_static_adversary_family'
S = A / 'acceptance_execution_preparation_family/integration_source_revision'


def insist(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def write(name, obj):
    with (HERE / name).open('x') as stream:
        stream.write(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def main():
    before = (F / 'FIRST_PARTY_MANIFEST.json').read_bytes()
    insist(sha(before) == '0480281a6dd9629183d1d7e2ad98b098a3b5eae8b8b423dbc4bc72eda85403cf', 'Closed review manifest changed')
    manifest = json.loads(before)
    insist(len(manifest['files']) == 31, 'Exact31 reviewed members')
    for row in manifest['files']:
        raw = (F / row['path']).read_bytes()
        insist(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Closed review member changed')
    old_assessment, old_coverage = load(F / 'ASSESSMENT.json'), load(F / 'READ_COVERAGE.json')
    raw_note = (F / 'METADATA_GENERATION_FAILURE.md').read_bytes()
    later = b"The tool returned exit_code1. Its complete visible combined output is retained below. The tool did not expose the operating-system PID or separate stdout/stderr channel bytes or start/end UTC clocks for this uncaptured invocation; those are unavailable, not fabricated. The command and complete metadata-writing source are retained in the conversation's preceding tool call and the complete supplied source is copied verbatim into FAILED_METADATA_WRITER_RECONSTRUCTION.py as a retrospective reconstruction, not a claimed prelaunch snapshot. Unlike the two substantive actual subprocess captures, this observation is not promoted as a full four-file process capture. The corrected metadata writer is saved separately and its final metadata explicitly preserves this observation."
    earlier = b"The tool returned exit_code1. Its complete visible combined output is retained below. The tool did not expose the operating-system PID or separate stdout/stderr channel bytes or start/end UTC clocks for this uncaptured invocation; those are unavailable, not fabricated. The command and complete metadata-writing source are retained in the conversation's preceding tool call. Unlike the two actual subprocess captures, this observation is not promoted as a full four-file process capture. The corrected metadata writer is saved separately and its final metadata explicitly preserves this observation."
    insist(raw_note.count(later) == 1, 'Exact changed metadata paragraph')
    original_note = raw_note.replace(later, earlier, 1)
    old_ref = old_coverage['own_earlier_metadata_line_count_failure']
    insist(len(original_note) == old_ref['bytes'] and sha(original_note) == old_ref['sha256'], 'Retrospective original note does not match the dated actual metadata pin')
    insist(old_ref == old_assessment['own_metadata_generation_failure_retained'], 'Both dated original note references must agree')
    with (HERE / 'ORIGINAL_DATED_FAILURE_OBSERVATION.md').open('xb') as stream:
        stream.write(original_note)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    scope = {'schema': 'pr40-static-review-metadata-reference-correction/v1', 'utc': now,
             'closed_review_manifest': pin(F / 'FIRST_PARTY_MANIFEST.json'),
             'closed_review_members': 31, 'reviewed_preparation_manifest_sha256': '65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e',
             'dated_original_failure_note_reconstructed_exactly_to_old_pin': pin(HERE / 'ORIGINAL_DATED_FAILURE_OBSERVATION.md'),
             'complete_current_failure_note': pin(F / 'METADATA_GENERATION_FAILURE.md'),
             'retrospective_failed_writer_source': pin(F / 'FAILED_METADATA_WRITER_RECONSTRUCTION.py'),
             'closed_old_assessment': pin(F / 'ASSESSMENT.json'), 'closed_old_coverage': pin(F / 'READ_COVERAGE.json'),
             'qualification': 'Adding the retrospective-source sentence changed only the own failure note after its two metadata pins. This adjacent full metadata correction preserves the sealed review and both dated notes; no scientific, candidate-source, control-output, process-capture or actual-execution conclusion changes.',
             'mandatory_candidate_defects': [], 'candidate_scientific_or_source_changes': False,
             'reviewed_helper_import_compile_execution': False, 'actual_future_acceptance_claimed': False,
             'original_substantive_attempts': 0, 'new_substantive_attempts': 0, 'audit_turns': 0,
             'full_problem_solved': False, 'novelty_claimed': False, 'metadata_qualification_completion_percent': 100,
             'mathematical_discovery_completion_percent': 0}
    write('CORRECTION.json', scope)
    coverage = copy.deepcopy(old_coverage)
    for row in coverage['source_programs']:
        row['path'] = (S / row['path']).relative_to(R).as_posix()
    coverage['full_input_identity_and_typed_structure_inspection'] = pin(F / 'inspect_revised_inputs_actual_capture/stdout.bin')
    coverage['own_earlier_metadata_line_count_failure'] = pin(F / 'METADATA_GENERATION_FAILURE.md')
    coverage.update(utc=now, metadata_reference_correction=pin(HERE / 'CORRECTION.json'), reference_paths_anchor='repository_relative')
    write('CURRENT_READ_COVERAGE.json', coverage)
    assessment = copy.deepcopy(old_assessment)
    for key in ['own_actual_capture_receipts', 'own_complete_results']:
        assessment[key] = [pin(F / row['path']) for row in old_assessment[key]]
    for key in ['report', 'own_corrected_metadata_writer_capture']:
        assessment[key] = pin(F / old_assessment[key]['path'])
    assessment['read_coverage'] = pin(HERE / 'CURRENT_READ_COVERAGE.json')
    assessment['own_metadata_generation_failure_retained'] = pin(F / 'METADATA_GENERATION_FAILURE.md')
    assessment.update(utc=now, metadata_reference_correction=pin(HERE / 'CORRECTION.json'), reference_paths_anchor='repository_relative')
    write('CURRENT_ASSESSMENT.json', assessment)
    with (HERE / 'RESEARCH_LOG.md').open('x') as stream:
        stream.write('# PR40 revised static metadata qualification\n\n## ' + now + ' — Exact adjacent correction\n\nPreserved the closed31-member static review and reconstructed its dated failure note exactly to the old SHA/size. Corrected the two full current metadata objects in this new adjacent root with repository-relative references. All reviewed candidate sources, mathematical scope, actual control/capture results and qualified clean verdict are unchanged. No reviewed helper execution or Git/native/shared/remote write. Qualification100%; discovery0%; original0/5,new0,audit0. Root owns publication and actual acceptance.\n')
    rows = []
    for path in sorted(HERE.iterdir()):
        insist(path.is_file() and not path.is_symlink(), 'Regular qualification member only')
        raw = path.read_bytes()
        rows.append({'path': path.name, 'bytes': len(raw), 'sha256': sha(raw)})
    write('FIRST_PARTY_MANIFEST.json', {'schema': 'pr40-static-metadata-qualification-closure/v1',
          'closed_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'self_excluded_paths': ['FIRST_PARTY_MANIFEST.json'],
          'files_count': len(rows), 'files': rows, 'foreign_excluded_prefixes': [], 'scratch_exclusions': [],
          'status': 'PASS_QUALIFIED_SOURCE_ONLY_METADATA_REFERENCES_CORRECTED',
          'static_review_manifest_sha256': sha(before), 'original_substantive_attempts': 0,
          'new_substantive_attempts': 0, 'audit_turns': 0, 'full_problem_solved': False,
          'metadata_qualification_completion_percent': 100, 'mathematical_discovery_completion_percent': 0})
    insist((F / 'FIRST_PARTY_MANIFEST.json').read_bytes() == before, 'Original sealed review changed')
    for path in HERE.iterdir():
        path.chmod(0o444)
    print(json.dumps({'status': 'PASS_QUALIFIED_SOURCE_ONLY_METADATA_REFERENCES_CORRECTED', 'authored_members': len(rows),
                      'manifest_sha256': sha((HERE / 'FIRST_PARTY_MANIFEST.json').read_bytes()),
                      'current_assessment': pin(HERE / 'CURRENT_ASSESSMENT.json'),
                      'current_coverage': pin(HERE / 'CURRENT_READ_COVERAGE.json')}))


if __name__ == '__main__':
    main()
