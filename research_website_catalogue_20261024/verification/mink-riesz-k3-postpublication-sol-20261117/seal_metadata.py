"""Finite own-packet metadata seal only. No production action authority."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-postpublication-sol-20261117')
PRIVATE_FAILURE = A.parent / 'mink-riesz-k3-runtime-sol-20261117/postpublication-audit-failure-20261117'
COMMIT = '4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
PARENT = '217d41c0a9344aed9caacee7aed31d4f23b77e47'
TREE = 'a9c5a4f3e30eb976bbe4f9c1872e14a92e22cc7e'
CHECKER_SHA = '12731fb5a5c8ae8014afc8a517724db9ce51b904f28fa97fed76b2101bf59f5b'
EMPTY_SHA = hashlib.sha256(b'').hexdigest()
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
    require(stat.S_ISREG(st.st_mode), 'regular own payload only')
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def put(name, obj):
    path = A / name
    data = (json.dumps(obj, indent=2) + '\n').encode()
    with path.open('wb' if name in TERMINALS else 'xb') as handle:
        handle.write(data)

def main():
    require(Path(__file__).resolve() == A / 'seal_metadata.py', 'fixed saved metadata source')
    require(not any(os.path.lexists(A / x) for x in TERMINALS + ['SEAL_EXECUTION.json']),
            'one fresh own metadata seal')
    require(not os.path.lexists(PRIVATE_FAILURE), 'no conditional private failure directory on success')
    started = now()
    result, execution, details = load('RESULTS.json'), load('EXECUTION.json'), load('DETAILS.json')
    require(result['status'] == 'PASS_LOCAL_POSTPUBLICATION_AUDIT_ONLY', 'successful retained local result')
    require(result['completion_percent_assigned_local_audit_only'] == 100 and
            result['whole_fixed_custody_before_after_exact'] and result['one_fresh_checker_invocation_only'],
            'complete single-invocation bounded local result')
    require((result['commit'], result['parent'], result['tree']) == (COMMIT, PARENT, TREE), 'fixed commit pins')
    require(result['follow_up'] is None and result['AA'] is None and not result['future_action_authority'],
            'no action authority')
    for field in ['production_helper_or_old_audit_import_execution_AST_compile_help_test_or_retry',
                  'network_or_repository_public_source_config_Sheet_deploy_redirect_contact_mutation',
                  'actual_UI_live_deployment_remote_persistence_or_scientific_certificate']:
        require(result[field] is False, 'bounded non-action declaration ' + field)
    require(execution['invocations'] == 1 and execution['exit_code'] == 0 and execution['checker_retry'] == 0,
            'external tool observed one audit exit zero')
    require(execution['production_helpers_or_old_audit_import_execution_AST_compile_help_or_tests'] == 0 and
            not execution['private_opaque_streams_authorities_journals_or_raw_indices_copied'],
            'no production execution or private raw evidence copying')
    require(pin(A / 'audit_local.py') == {'bytes': 61032, 'SHA256': CHECKER_SHA, 'mode': '0644'},
            'exact executed checker buffer')
    reader = load('READ_ATTESTATION.json')
    require(reader['source'] == {'bytes': 61032, 'lines': 906, 'SHA256': CHECKER_SHA} and
            reader['entire_final_saved_source_personally_read_after_final_edit_before_invocation'] and
            reader['checker_invocations_before_attestation'] == 0, 'complete prior reader attestation')
    seal_read = load('SEAL_READ_ATTESTATION.json')
    source_pin = pin(A / 'seal_metadata.py')
    require(seal_read['source'] == source_pin and seal_read['entire_saved_source_personally_read'] and
            seal_read['metadata_sealer_invocations_before_attestation'] == 0, 'full metadata source read before run')
    for name in ['AUDIT.stdout.txt', 'AUDIT.stderr.txt', 'SEAL.stdout.txt', 'SEAL.stderr.txt']:
        require(pin(A / name) == {'bytes': 0, 'SHA256': EMPTY_SHA, 'mode': '0644'}, 'literal empty stream ' + name)
    before, after = load('BEFORE.json'), load('AFTER.json')
    require(before['snapshot'] == after['snapshot'], 'complete retained fixed before-after equality')
    require(details['physical_public_files_childdirs_articles_XML'] == [803, 387, 133, 134] and
            details['article_HEAD_span_counts'] == [8, 7, 7], 'whole public and article counts')
    aggregates = details['aggregates']
    require(aggregates['baseline_counts'] == [130, 130, 131] and aggregates['candidate_counts'] == [133, 133, 134] and
            aggregates['independent_index_span_count'] == aggregates['supplied_index_span_count'] == 3 and
            aggregates['independent_XML_span_count'] == aggregates['supplied_XML_span_count'] == 1 and
            aggregates['XML_comparison_includes_root_children_text_tail_attribute_order'], 'complete aggregate proof counts')
    index = details['index']
    require(index['before_records'] == 58730 and index['after_records'] == 58743 and
            index['whole_untouched_records'] == 58728 and index['selected_exact_zero_stat_records'] == 15,
            'whole raw record proof counts')
    require(index['after'] == {'bytes': 9062142, 'SHA256': '6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179'} and
            result['index'] == {**index['after'], 'mode': '0644'}, 'actual successor index pin')
    require(index['TREE']['nodes'] == 983 and index['TREE']['valid'] == 977 and
            len(index['TREE']['invalid_paths']) == 6, 'complete TREE node proof counts')
    commit = details['commit']
    require(commit['OID'] == COMMIT and commit['tree'] == TREE and commit['single_parent'] == PARENT and
            commit['parent_leaves'] == 58730 and commit['new_leaves'] == 58743 and
            commit['delta'] == '13A2M' and commit['all15_blobs_byte_exact'], 'complete local commit proof')
    native = details['native_semantics']
    require(native['foreign_paths'] == native['staged_deletions'] == 0 and
            native['foreign_before_SHA256'] == native['foreign_after_SHA256'], 'derived foreign staging preservation')
    require(len(details['receipts_derived_only']) == 4 and
            all(x['attempt'] == 1 and x['exit_code'] == 0 for x in details['receipts_derived_only']) and
            details['private_raw_journals_outputs_indices_not_copied'], 'retained private receipt observations only')
    require(len(details['local_Git_object_reads_derived_only']) == 13 and
            all(x['exit_code'] == 0 and x['network_protocols_disabled'] for x in details['local_Git_object_reads_derived_only']),
            'bounded successful local object reads')
    require('independent local postpublication audit passed' in (A / 'REPORT.md').read_text() and
            '100% of the assigned local postpublication audit complete' in (A / 'RESEARCH_LOG.md').read_text(),
            'final bounded report and checkpoint')
    expected = {'audit_local.py', 'CRITERIA.md', 'ENVIRONMENT_FAILURE.md', 'RESEARCH_LOG.md',
                'PRIVATE_FAILURE_DISPOSITION.md', 'ADVERSARIAL_REVIEW.md', 'READ_ATTESTATION.json',
                'AUDIT.stdout.txt', 'AUDIT.stderr.txt', 'BEFORE.json', 'AFTER.json', 'DETAILS.json', 'RESULTS.json',
                'EXECUTION.json', 'REPORT.md', 'seal_metadata.py', 'SEAL_READ_ATTESTATION.json',
                'SEAL.stdout.txt', 'SEAL.stderr.txt'}
    require({p.name for p in A.iterdir()} == expected, 'finite exact pre-seal file set')
    existing = {p.name: pin(p) for p in sorted(A.iterdir())}
    put('SEAL_EXECUTION.json', {'schema': 'independent-postpublication-metadata-normal-completion-v1',
        'UTC_start': started, 'UTC_data_end': now(), 'invocations': 1, 'exit_code_at_normal_completion': 0,
        'external_tool_exit_observation_required': True, 'metadata_only': True,
        'production_helper_or_main_audit_execution': False, 'follow_up': None})
    for name in TERMINALS:
        with (A / name).open('xb') as handle:
            handle.write(b'')
    rows, dirs, seen = [], [], set()
    def hidden(relative):
        return any(part.startswith('.') for part in Path(relative).parts if part != '.')
    def walk(path):
        st = path.lstat()
        require(stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'unique real own directory')
        seen.add((st.st_dev, st.st_ino))
        children = sorted(path.iterdir(), key=lambda p: p.name)
        relative = path.relative_to(A).as_posix()
        dirs.append({'path': relative, 'mode': format(stat.S_IMODE(st.st_mode), '04o'),
                     'empty': not children, 'hidden': hidden(relative)})
        for child in children:
            st = child.lstat()
            if stat.S_ISDIR(st.st_mode):
                walk(child)
            else:
                require(stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'unique real own file')
                seen.add((st.st_dev, st.st_ino))
                relative = child.relative_to(A).as_posix()
                if relative not in TERMINALS:
                    value = pin(child)
                    rows.append({'path': relative, **value, 'empty': value['bytes'] == 0, 'hidden': hidden(relative)})
    walk(A)
    require(len(dirs) == 1 and len(rows) == 20 and dirs[0]['mode'] == '0755', 'finite own 22-file zero-childdir packet')
    require(all(pin(A / name) == value for name, value in existing.items()), 'no prior own payload changed while sealing')
    put('MANIFEST.json', {'schema': 'finite-independent-postpublication-local-audit-manifest-v1', 'UTC': now(),
        'root': str(A), 'root_mode': dirs[0]['mode'], 'regular_files': len(rows) + 2, 'child_directories': 0,
        'payload_files': rows, 'directories': dirs,
        'exact_already_created_terminal_recursive_hash_exclusions': TERMINALS,
        'terminal_modes': {name: pin(A / name)['mode'] for name in TERMINALS}, 'other_exclusions': [],
        'all_hidden_empty_ignored_modes_and_topology_included': True,
        'no_future_subtree_or_basename_exclusions': True, 'external_terminal_pins_required': True})
    put('FINAL.json', {'schema': 'independent-postpublication-local-audit-final-v1', 'UTC': now(),
        'status': 'PASS_LOCAL_POSTPUBLICATION_AUDIT_ONLY_FROZEN',
        'completion_percent_assigned_local_audit_only': 100, 'commit': COMMIT, 'tree': TREE, 'parent': PARENT,
        'index': result['index'], 'physical_public_files_childdirs_articles_XML': [803, 387, 133, 134],
        'commit_delta': '13A2M', 'commit_parent_leaves': 58730, 'commit_new_leaves': 58743,
        'whole_untouched_raw_index_records': 58728, 'selected_exact_zero_stat_records': 15,
        'TREE_nodes': 983, 'TREE_valid_nodes': 977, 'TREE_invalid_nodes': 6,
        'article_HEAD_span_counts': [8, 7, 7], 'aggregate_old_HTML_JSON_XML': [130, 130, 131],
        'aggregate_new_HTML_JSON_XML': [133, 133, 134], 'aggregate_independent_index_XML_spans': [3, 1],
        'foreign_paths_observed': 0, 'staged_deletions_observed': 0,
        'whole_fixed_custody_before_after_exact': True, 'passive_checker_invocations': 1,
        'passive_checker_exit_code': 0, 'metadata_sealer_invocations': 1,
        'metadata_exit_zero_requires_external_tool_observation': True,
        'initial_pre_reader_environment_ENOSPC_failure_retained': True, 'current_checker_failures': 0,
        'conditional_private_failure_directory_absent': True, 'private_raw_evidence_copied': False,
        'all_prior_failure_and_source_packets_immutable': True, 'retained_production_receipts_attempts_exits': [[1, 0]] * 4,
        'production_helper_or_old_audit_import_execution_AST_compile_help_test_or_retry': False,
        'network_or_repository_public_source_config_Sheet_deploy_redirect_contact_mutation': False,
        'actual_UI_live_deployment_remote_persistence_science_copy_priority_or_future_action_certificate': False,
        'manifest': pin(A / 'MANIFEST.json'), 'report': pin(A / 'REPORT.md'), 'execution': pin(A / 'EXECUTION.json'),
        'regular_files': len(rows) + 2, 'child_directories': 0, 'root_mode': dirs[0]['mode'],
        'follow_up': None, 'AA': None, 'future_action_authority': False, 'frozen': True})

if __name__ == '__main__':
    main()
