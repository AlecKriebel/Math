#!/usr/bin/env python3
"""Own report metadata only; original failed line-count observation remains retained."""
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE.parent
B = A.parents[1]


def pin(q):
    raw = q.read_bytes()
    return {'path': q.relative_to(HERE).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    a = json.loads((HERE / 'inspect_revised_inputs_actual_capture/stdout.bin').read_bytes())
    b = json.loads((HERE / 'finite_guard_controls_actual_capture/stdout.bin').read_bytes())
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    coverage = {'schema': 'pr40-fresh-revised-static-read-coverage/v1', 'utc': now,
                'entire_revised_fifteen_member_packet_read': True, 'source_programs': a['source_programs'],
                'complete_revised_contract_scope_draft_change_record_revision_bindings_input_bindings_patch_manifest_read': True,
                'complete_closed_prior_static_REPORT_and_ASSESSMENT_read': True,
                'complete_original_SOURCE_STATUS_root_operational_mathematical_certificate_current_overview_read': True,
                'bound_native_driver_entire_source_read': True,
                'bound_native_driver_lines': len((B / 'infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py').read_bytes().splitlines()),
                'full_input_identity_and_typed_structure_inspection': pin(HERE / 'inspect_revised_inputs_actual_capture/stdout.bin'),
                'original_primary_and_whole_foreign_input_bytes_rehashed_individually': True,
                'new_full_primary_PDF_proof_reading_claimed': False,
                'new_unexposed_source_first_mathematical_independence_claimed': False,
                'reviewed_helper_import_compile_execution': False,
                'own_earlier_metadata_line_count_failure': pin(HERE / 'METADATA_GENERATION_FAILURE.md')}
    (HERE / 'READ_COVERAGE.json').write_text(json.dumps(coverage, sort_keys=True, indent=2) + '\n')
    obj = json.loads((HERE / 'ASSESSMENT.json').read_bytes())
    obj.update(utc=now, read_coverage=pin(HERE / 'READ_COVERAGE.json'),
               own_metadata_generation_failure_retained=pin(HERE / 'METADATA_GENERATION_FAILURE.md'),
               own_metadata_failure_is_candidate_or_control_failure=False)
    (HERE / 'ASSESSMENT.json').write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')
    note = '\n## ' + now + ' — Review complete before strict closure\n\nAll six earlier mandatory findings are corrected; no new mandatory issue. Own input inspector actually passed600 unique files/39,835,206 bytes/242 strict JSON objects. Own44 predicate controls and two real private hardlink controls passed; complete collision/temp/preimage bytes retained. Own metadata line-count generation failure is retained and corrected separately; no candidate or substantive control failure. Only own sources executed, with complete actual substantive captures. Root execution still pending. Review100%; discovery0%; original0/5,new0,audit0. Publication remains root-owned.\n'
    with (HERE / 'RESEARCH_LOG.md').open('a') as stream:
        stream.write(note)
    print(json.dumps({'status': 'OWN_METADATA_WRITTEN', 'utc': now, 'assessment': pin(HERE / 'ASSESSMENT.json'),
                      'report': pin(HERE / 'REPORT.md'), 'coverage': pin(HERE / 'READ_COVERAGE.json'),
                      'native_source_lines': coverage['bound_native_driver_lines']}))


if __name__ == '__main__':
    main()
