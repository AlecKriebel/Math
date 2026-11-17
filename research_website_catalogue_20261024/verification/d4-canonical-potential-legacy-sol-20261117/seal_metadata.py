"""Finite own D4 correspondence metadata seal; no publication authority."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/d4-canonical-potential-legacy-sol-20261117')
FAILURE = A.parent / 'mink-riesz-k3-runtime-sol-20261117/d4-legacy-failure-20261117'
SHA = '6d40fe7729300d78abc36afaff60aaee3ab5bcc8d206f3e2b1f2b0591eb1149a'
TERMINALS = ['MANIFEST.json', 'FINAL.json']

def require(value, reason):
    if not value:
        raise RuntimeError(reason)

def now():
    return datetime.now(timezone.utc).isoformat()

def load(name):
    return json.loads((A / name).read_bytes())

def pin(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'regular own metadata file')
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def put(name, value):
    with (A / name).open('w' if name in TERMINALS else 'x') as handle:
        handle.write(json.dumps(value, indent=2) + '\n')

def main():
    require(Path(__file__).resolve() == A / 'seal_metadata.py', 'fixed saved metadata source')
    require(not any(os.path.lexists(A / name) for name in TERMINALS + ['SEAL_EXECUTION.json']), 'one fresh finite seal')
    require(not os.path.lexists(FAILURE), 'private failure-only path absent on success')
    started = now()
    result, execution, data = load('RESULTS.json'), load('EXECUTION.json'), load('IDENTITY_DATA.json')
    require(result['status'] == 'PASS_NO_EXACT_WORK_LEGACY_CORRESPONDENCE_IN_FIXED_VIEWS' and
            result['completion_percent_assigned_correspondence_only'] == 100 and result['whole_guard_before_after_exact'],
            'retained complete bounded correspondence result')
    require(execution['invocations'] == 1 and execution['exit_code'] == 0 and execution['reader_retries'] == 0,
            'one externally observed successful reader invocation')
    require(execution['scientific_source_helper_import_execution_AST_compile_help_or_tests'] == 0,
            'no scientific or helper action')
    require(pin(A / 'read_legacy_once.py') == {'bytes': 25916, 'SHA256': SHA, 'mode': '0644'}, 'exact executed reader source')
    reading = load('READ_ATTESTATION.json')
    require(reading['source'] == {'bytes': 25916, 'lines': 429, 'SHA256': SHA} and
            reading['entire_final_saved_source_personally_read_after_final_edit'] and
            reading['reader_invocations_before_attestation'] == 0, 'entire reader read before invocation')
    seal_read = load('SEAL_READ_ATTESTATION.json')
    require(seal_read['source'] == pin(A / 'seal_metadata.py') and seal_read['entire_saved_source_personally_read'] and
            seal_read['sealer_invocations_before_attestation'] == 0, 'entire metadata source read before invocation')
    require(load('BEFORE.json')['snapshot'] == load('AFTER.json')['snapshot'], 'whole fixed snapshots exact')
    before = load('BEFORE.json')['snapshot']
    require((before['docs']['regular_files'], before['docs']['child_directories']) == (257, 50) and
            (before['source']['regular_files'], before['source']['child_directories']) == (72, 7) and
            (before['writer']['regular_files'], before['writer']['child_directories']) == (30, 1), 'actual fixed extents')
    views = data['views']
    require(len(views) == 3 and [x['files'] for x in views] == [257, 254, 254] and
            all(x['all_archive_member_count'] == 2607 and not x['whole_native_asset_matches'] and
                not x['strong_text_identity_candidates'] for x in views), 'three complete bounded negative views')
    require(all(len(x['concrete_false_positives']) == 3 and
                all(y['whole_article_identical_to_personally_read_physical_article'] and
                    y['differing_whole_public_article_saved_for_personal_read'] is None and not y['exact_target']
                    for y in x['concrete_false_positives']) for x in views), 'all whole false-positive articles read by exact identity')
    require(len(data['readonly_local_Git_reads_derived_only']) == result['readonly_local_Git_batches'] == 13 and
            all(x['exit_code'] == 0 and x['network_protocols_disabled'] for x in data['readonly_local_Git_reads_derived_only']),
            'all local data reads successful without network')
    require(not data['raw_private_index_config_or_journals_copied'], 'private raw evidence remains private')
    require(all(result[name] is None for name in ['canonical', 'legacy_correspondence', 'redirect', 'follow_up']) and
            not result['future_publication_or_action_authority'], 'no correspondence or action authority')
    require('No exact-work legacy correspondence was found' in (A / 'REPORT.md').read_text() and
            '100% of the assigned bounded task complete' in (A / 'RESEARCH_LOG.md').read_text(), 'final report and checkpoint')
    for name in ['READER.stdout.txt', 'READER.stderr.txt', 'SEAL.stdout.txt', 'SEAL.stderr.txt']:
        require(pin(A / name) == {'bytes': 0, 'SHA256': hashlib.sha256(b'').hexdigest(), 'mode': '0644'}, 'literal empty stream ' + name)
    expected = {'read_legacy_once.py', 'CRITERIA.md', 'RESEARCH_LOG.md', 'READ_ATTESTATION.json', 'ADVERSARIAL_REVIEW.md',
                'BEFORE.json', 'AFTER.json', 'IDENTITY_DATA.json', 'RESULTS.json', 'READER.stdout.txt', 'READER.stderr.txt',
                'EXECUTION.json', 'DISCOVERY.md', 'REPORT.md', 'seal_metadata.py', 'SEAL_READ_ATTESTATION.json',
                'SEAL.stdout.txt', 'SEAL.stderr.txt'}
    require({path.name for path in A.iterdir()} == expected, 'finite exact pre-seal scope')
    existing = {path.name: pin(path) for path in sorted(A.iterdir())}
    put('SEAL_EXECUTION.json', {'schema': 'D4-correspondence-metadata-normal-completion-v1', 'UTC_start': started,
        'UTC_data_end': now(), 'invocations': 1, 'exit_code_at_normal_completion': 0,
        'external_tool_exit_observation_required': True, 'metadata_only': True, 'reader_or_helper_execution': False, 'follow_up': None})
    for name in TERMINALS:
        with (A / name).open('xb') as handle:
            handle.write(b'')
    st = A.lstat()
    require(stat.S_ISDIR(st.st_mode), 'real own root')
    rootmode = format(stat.S_IMODE(st.st_mode), '04o')
    rows, seen = [], {(st.st_dev, st.st_ino)}
    for path in sorted(A.iterdir()):
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'flat unique actual own regular files')
        seen.add((st.st_dev, st.st_ino))
        if path.name not in TERMINALS:
            value = pin(path)
            rows.append({'path': path.name, **value, 'empty': value['bytes'] == 0, 'hidden': path.name.startswith('.')})
    require(len(rows) == 19 and rootmode == '0755' and all(pin(A / name) == value for name, value in existing.items()),
            'complete unchanged 21-file zero-childdir metadata packet')
    put('MANIFEST.json', {'schema': 'finite-D4-legacy-correspondence-manifest-v1', 'UTC': now(), 'root': str(A),
        'root_mode': rootmode, 'regular_files': 21, 'child_directories': 0, 'payload_files': rows,
        'directories': [{'path': '.', 'mode': rootmode, 'empty': False, 'hidden': False}],
        'exact_already_created_terminal_recursive_hash_exclusions': TERMINALS,
        'terminal_modes': {name: pin(A / name)['mode'] for name in TERMINALS}, 'other_exclusions': [],
        'all_hidden_empty_ignored_actual_modes_and_topology_included': True,
        'no_future_subtree_or_basename_exclusions': True, 'external_terminal_pins_required': True})
    put('FINAL.json', {'schema': 'D4-legacy-correspondence-final-v1', 'UTC': now(),
        'status': 'FROZEN_NO_EXACT_WORK_LEGACY_CORRESPONDENCE_IN_FIXED_VIEWS',
        'completion_percent_assigned_correspondence_only': 100, 'record': '23439776', 'row': 171,
        'physical_docs_files_childdirs': [257, 50], 'native_released_docs_blob_counts': [254, 254],
        'local_commit_docs_pairs': result['local_commit_docs_pairs'], 'recursive_archive_members_per_view': [2607] * 3,
        'whole_native_asset_matches': 0, 'strong_outer_text_identity_candidates': 0,
        'concrete_false_positive_articles_personally_read': 3, 'whole_historical_false_articles_identical': True,
        'whole_native_docs_source_writer_specific_root_before_after_exact': True,
        'source_files_childdirs': [72, 7], 'writer_files_childdirs': [30, 1],
        'reader_invocations': 1, 'reader_exit': 0, 'metadata_sealer_invocations': 1,
        'metadata_exit_zero_requires_external_tool_observation': True,
        'pre_reader_missing_path_discovery_observations_retained': True, 'reader_failures': 0,
        'private_failure_only_directory_absent': True, 'private_opaque_data_copied': False,
        'scientific_source_helper_import_execution_AST_compile_help_or_tests': False,
        'Git_mutations_network_W_Sheet_deploy_redirect_or_outreach': False,
        'alternate_PDF_all_editions_worldwide_actual_UI_or_future_publication_certificate': False,
        'canonical': None, 'legacy_correspondence': None, 'redirect': None, 'AA': None, 'follow_up': None,
        'future_publication_or_action_authority': False, 'manifest': pin(A / 'MANIFEST.json'),
        'report': pin(A / 'REPORT.md'), 'regular_files': 21, 'child_directories': 0, 'root_mode': rootmode, 'frozen': True})

if __name__ == '__main__':
    main()
