"""Prepare bounded SOURCE index/readiness; does not run ROOT-only closure helpers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from packet_common import HERE, row, validate

def main():
    assert not (HERE / 'SELF_MANIFEST.json').exists()
    assert not (HERE / 'INDEX.json').exists() and not (HERE / 'READY.json').exists()
    controls = json.loads((HERE / 'INDEPENDENT_RESULTS.json').read_text())
    negatives = json.loads((HERE / 'NEGATIVE_RESULTS.json').read_text())
    unused = json.loads((HERE / 'UNUSED_RESULTS.json').read_text())
    custody = json.loads((HERE / 'CUSTODY_RESULTS.json').read_text())
    v = {'schema': 'pr55-independent-product-volume-verdict/v1',
         'utc': datetime.now(timezone.utc).isoformat(),
         'verdict': 'PASS_SCOPED_COMBINATORIAL_COMPARISON_WITH_IMPORTED_GKZ',
         'problem_id': '30006309', 'source_problem': 'OWR-14299288-015',
         'literal_original_status_and_turns': 'claimed_solved 1/5',
         'mandatory_mathematical_fixes': [],
         'scope': 'Smooth complete very ample toric embedding, degree at least two; first-factor coefficient torus projection; established GKZ foundations.',
         'universal_product_volume_derivation': True,
         'both_inclusions_support_function_derivation': True,
         'source_exact_mechanism_match': True,
         'independence': 'No old checker, old reviewer or other fresh review read or imported; original-source custody was checked in place.',
         'finite_controls': {'assertions': controls['assertions'], 'product_triangulations': controls['product_triangulations'],
                             'nonstaircase_triangulations': controls['nonstaircase_triangulations'],
                             'finite_difference_max_n': controls['finite_difference_max_n'],
                             'scaled_square_equal_column_refinements': 36,
                             'complete_unused_column_configurations': unused['configurations'],
                             'implemented_negative_alternatives_rejected': len(negatives['rejected_alternatives'])},
         'novelty': 'unestablished; priority audit still required',
         'source_precision': {'raw_report_key': 'ABSENT; no raw value', 'archive_wrapper': 'present null placeholder',
                              'SQL_report': 'non-NULL TEXT {}', 'generic_response_count': 'not separately supplied'},
         'native_acceptance_or_remote_action_authority': False,
         'ROOT_personal_read_attestation': False,
         'review_completion_percent': 100,
         'global_publication_completion_not_claimed': True}
    (HERE / 'VERDICT.json').write_text(json.dumps(v, indent=2) + '\n')
    with (HERE / 'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+v['utc']+' — Universal proof, independently implemented product/massive-face controls, explicit complete unused-column configurations, primary-source checks and in-place original custody are complete. Scientific review completion estimate 100% within stated scope; priority, ROOT personal reading/closure, native acceptance and publication remain separate. No mathematical blocker found.\n')
    files = sorted(p for p in HERE.rglob('*') if p.is_file())
    assert len(files) + 3 <= 65 and sum(p.stat().st_size for p in files) < 900000
    for p in files:
        assert not p.is_symlink(); p.chmod(0o444)
    directories = sorted({HERE} | {p for p in HERE.rglob('*') if p.is_dir()})
    assert all(p.stat().st_mode & 0o777 == 0o755 for p in directories)
    index = {'schema': 'pr55-product-volume-adversary-source-index/v1',
             'utc': datetime.now(timezone.utc).isoformat(),
             'files': [row(p) for p in files],
             'directories': [{'path': str(p), 'mode': p.stat().st_mode & 0o777} for p in directories],
             'immutable_external_references': custody['immutable_external_references'],
             'self_exclusions': ['INDEX.json', 'READY.json', 'SELF_MANIFEST.json']}
    (HERE / 'INDEX.json').write_text(json.dumps(index, indent=2) + '\n'); (HERE / 'INDEX.json').chmod(0o444)
    ready = {'schema': 'pr55-product-volume-adversary-source-ready/v1',
             'utc': datetime.now(timezone.utc).isoformat(), 'index_sha256': row(HERE / 'INDEX.json')['sha256'],
             'prepared_file_count': len(files) + 2,
             'payload_file_count_excluding_index_ready': len(files),
             'payload_bytes': sum(p.stat().st_size for p in files),
             'verdict': v['verdict'], 'mandatory_mathematical_fixes': [],
             'ROOT_personal_read_attestation': False, 'root_closure_required_after_preparer_exit': True,
             'closer_or_reader_executed_by_preparer': False, 'self_manifest_present_at_handoff': False,
             'priority_audit_completion_claimed': False, 'native_acceptance_or_remote_action_authority': False,
             'builder_has_no_separate_process_capture': True,
             'builder_process_completion_not_certified_by_this_record': True,
             'review_completion_percent': 100}
    (HERE / 'READY.json').write_text(json.dumps(ready, indent=2) + '\n'); (HERE / 'READY.json').chmod(0o444)
    _, _, actual = validate(False)
    print(json.dumps({'status': 'PASS_PREPARED_PRODUCT_VOLUME_SOURCE_ONLY', 'prepared_files': len(actual),
                      'ready': row(HERE / 'READY.json'), 'index': row(HERE / 'INDEX.json')}, sort_keys=True))

if __name__ == '__main__':
    main()
