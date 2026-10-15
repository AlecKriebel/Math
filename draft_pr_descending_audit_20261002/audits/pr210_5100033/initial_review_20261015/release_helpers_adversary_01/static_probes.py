"""Read-only input audit and pure counterexample models; no helper is imported/run.

Run with python3 -B. The sole write is this directory's PROBE_RESULTS.json.
No network, provider, Git, index, ref, environment or credential access is used.
Counterexamples are explicitly source-derived models, not executions of helpers.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import dis
import hashlib
import json
import zipfile

OUT = Path(__file__).resolve().parent
CASE = OUT.parent.parent
R = CASE / 'preprint'
D = CASE / 'initial_review_20261015'
U = R / 'pr_update/5100033'
ROOT = CASE.parents[2]
HELPERS = ['publish_preprint.py', 'append_verified_tracker.py',
           'integrate_reviewed_pr.py', 'verify_and_merge.py']


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def matches(path, row):
    if not path.is_file():
        return False
    raw = path.read_bytes()
    return len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']


def assertion_opcodes(code):
    total = sum(i.opname == 'LOAD_ASSERTION_ERROR' or
                (i.opname == 'LOAD_COMMON_CONSTANT' and i.argrepr == 'AssertionError')
                for i in dis.get_instructions(code))
    return total + sum(assertion_opcodes(c) for c in code.co_consts
                       if isinstance(c, type(code)))


result = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Source-only supporting helper adversary; not a manuscript review',
    'helper_top_levels_executed': 0, 'helper_imports': 0,
    'network_calls': 0, 'provider_writes': 0, 'git_index_ref_writes': 0,
    'counterexample_method': 'Independent pure models of explicitly cited predicates',
}
result['helper_pins'] = [pin(CASE / 'publication' / n) for n in HELPERS]
result['supporting_input_pins'] = [pin(p) for p in [
    R / 'metadata.json', R / 'deposit.json', R / 'PACKAGE_MANIFEST.json',
    D / 'INTAKE.json', D / 'ROOT_NATIVE_TEMPLATE_ADAPTATION_NOTES.json',
    ROOT / 'zenodo_deposit_tool/README.md', ROOT / 'zenodo_deposit_tool/zenodo.py',
]]
result['clearance_exists'] = (R / 'FINAL_CLEARANCE.json').exists()
sources = {n: (CASE / 'publication' / n).read_text() for n in HELPERS}
result['source_parse_and_optimization'] = {}
for name, source in sources.items():
    tree = ast.parse(source)
    result['source_parse_and_optimization'][name] = {
        'parses': True,
        'ast_asserts': sum(isinstance(n, ast.Assert) for n in ast.walk(tree)),
        'assert_opcodes_normal': assertion_opcodes(compile(source, name, 'exec', optimize=0)),
        'assert_opcodes_optimized': assertion_opcodes(compile(source, name, 'exec', optimize=1)),
    }

package = json.loads((R / 'PACKAGE_MANIFEST.json').read_text())
result['package_submission_pins_match'] = all(matches(R / x['path'], x)
                                               for x in package['submission_files'])
result['submission_files'] = package['submission_files']
result['deposit_metadata_equals_metadata_json'] = (
    json.loads((R / 'deposit.json').read_text())['metadata'] ==
    json.loads((R / 'metadata.json').read_text()))
result['native_manifest_checks'] = {}
for name in ['MANIFEST.json', 'PUBLICATION_MANIFEST.json', 'CURRENT_PACKET_MANIFEST.json']:
    m = json.loads((U / name).read_text())
    result['native_manifest_checks'][name] = {
        'entries': len(m['files']),
        'mismatches': [x['path'] for x in m['files'] if not matches(U / x['path'], x)],
    }
intake = json.loads((D / 'INTAKE.json').read_text())
result['original20_checks'] = []
for base in [D / 'submitted/unsolved_math_prioritization/attempts/5100033',
             U / 'history/original_submission_20261015', R / 'verification/original_submission']:
    bad = []
    for row in intake['original_source_files']:
        rel = row['native_path'].split('attempts/5100033/', 1)[1]
        if not matches(base / rel, row):
            bad.append(rel)
    result['original20_checks'].append({'root': str(base), 'files': 20, 'mismatches': bad})
prefix = 'k605a_outer_focal_pedal_product/pr_update/5100033/'
with zipfile.ZipFile(R / 'k605a-source-verification.zip') as archive:
    names = {p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()}
    archive_names = {x.removeprefix(prefix) for x in archive.namelist() if x.startswith(prefix)}
    result['zip_native_binding'] = {
        'archive_entries': len(archive.namelist()), 'native_files': len(names),
        'same_path_set': names == archive_names,
        'all_native_bytes_equal': all((U / n).read_bytes() == archive.read(prefix + n)
                                     for n in names),
    }
families = ['source_domain_adversary_01', 'physical_geometry_adversary_01',
            'meromorphic_divisor_adversary_01', 'priority_author_updates_01',
            'priority_classical_general_01', 'whole_manuscript_adversary_01',
            'whole_manuscript_adversary_02']
result['family_manifest_checks'] = {}
for family in families:
    folder = D / family
    seals = [p for p in [folder / 'AUTHORED_MANIFEST.json', folder / 'MANIFEST.json',
                         folder / 'SAFE_AUTHORED_MANIFEST.json'] if p.exists()]
    record = {'candidate_count': len(seals), 'entries': None, 'mismatches': []}
    if len(seals) == 1:
        m = json.loads(seals[0].read_text())
        rows = m.get('authored_files', m.get('files', m.get('entries')))
        record['entries'] = len(rows)
        record['manifest'] = pin(seals[0])
        for row in rows:
            if 'relative_path' in row:
                p = folder / row['relative_path']
            else:
                p = folder / row['path']
                if not p.exists():
                    p = D / row['path']
            if (not p.resolve().is_relative_to(folder.resolve()) or p.is_symlink()
                    or not matches(p, row)):
                record['mismatches'].append(str(p))
    result['family_manifest_checks'][family] = record

# F1: the source checks two distinct sets separately, never requiring equality.
cleared = [{'path': x['path'], 'bytes': x['bytes'], 'sha256': x['sha256']}
           for x in package['submission_files']]
other = [{'name': 'k605a-outer-focal-pedal-areas.pdf', 'size': 7, 'sha256': 'd' * 64},
         {'name': 'k605a-source-verification.zip', 'size': 9, 'sha256': 'e' * 64}]
result['counterexamples'] = {
    'F1_disjoint_cleared_and_deposit_files': {
        'cleared_files': cleared, 'hypothetical_kit_files': other,
        'clearance_hash_loop_passes': result['package_submission_pins_match'],
        'metadata_unchanged': True, 'len_local_files_is_two': len(other) == 2,
        'stage_inspect_downloads_can_all_match_other_files': True,
        'source_has_no_equality_between_these_sets': True,
        'false_final_exact_reviewed_claim_reachable': True,
    },
    'F2_stale_publication_receipt': {
        'old_receipt_flags_submitted_and_verified': True,
        'later_clearance_valid_for_revised_package': True,
        'same_doi_in_tracker_receipt': True,
        'later_clearance_files_differ_from_old_receipt': True,
        'append_integrate_merge_accept_these_boolean_flags': True,
        'no_source_comparison_rejects_file_or_metadata_mismatch': True,
    },
    'F3_failed_public_readback': {
        'hypothetical_download_error': 'HTTP 403 or SHA-256 mismatch',
        'source_catches_error_and_keeps_running': True,
        'source_still_sets_metadata_and_files_verified': True,
        'source_still_sets_exact_reviewed_frozen_files_published': True,
        'doi_not_resolved_is_not_rejected_downstream': True,
    },
    'F4_uncertain_merge_reentry': {
        'PR_MERGED_receipt_absent': True, 'NATIVE_MERGE_REQUEST_exists': True,
        'hypothetical_prior_PUT_succeeded_response_lost': True,
        'hypothetical_reentry_reads_stale_open_unmerged_expected_head': True,
        'source_reentry_guard_ignores_existing_merge_request': True,
        'another_PUT_reachable': True,
    },
}
new_doi = '10.5281/zenodo.99900002'
existing_rows = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'],
                 ['https://arxiv.org/abs/2004.12497v11', '',
                  'https://doi.org/10.5281/zenodo.99900001', 'AMR-050-0033 / 5100033']]
found_by_source = [(i, row) for i, row in enumerate(existing_rows, 1)
                   if any(new_doi in str(cell) for cell in row)]
result['counterexamples']['F5_duplicate_problem_before_append'] = {
    'existing_rows': existing_rows, 'new_doi': new_doi,
    'same_problem_present': True, 'matches_under_source_doi_only_predicate': found_by_source,
    'source_reaches_append_when_attempt_absent': not found_by_source,
}
result['counterexamples']['O1_two_process_once_only_interleaving'] = {
    'schedule': ['A checks marker absent', 'B checks marker absent',
                 'A writes ordinary marker', 'B overwrites ordinary marker',
                 'A calls provider', 'B calls provider'],
    'markers_not_exclusive_creations_and_no_whole_run_lock': True,
    'stage_and_append_single_attempt_not_enforced_under_this_schedule': True,
}
result['counterexamples']['O2_native_tree_receipt_binding'] = {
    'source_walk': 'native_blob starts from p[tree]; source never GETs git/commits/head',
    'included_pins_tree_not_rebound_to_actual_commit_at_merge_time': True,
    'science_and_submission_content_readbacks_do_use_actual_head': True,
    'requirement_gap': 'All collateral pins rely on an internally consistent prepared receipt',
}
result['counterexamples']['O3_expected_branch_not_checked'] = {
    'expected_branch': 'dot/math-5100033',
    'expected_branch_literal_present_in_integration_source':
        'dot/math-5100033' in sources['integrate_reviewed_pr.py'],
    'actual_patch_branch_is_taken_from_PR_response': True,
    'exact_original_head_guard_present': True,
}

# Current queue transformation is modeled independently; no helper code executes.
original_row = intake['queue_row']
foreign_row = '| foreign row must survive byte-for-byte |'
main_queue = 'header\n' + original_row + '\n' + foreign_row + '\n'
fields = original_row.split('|')
fields[7] = ' 2020 '
fields[8] = ' claimed_solved '
fields[9] = ' 1/5 '
fields[11] = ' [Audited odd outer focal-pedal area product; credited preprint](attempts/5100033/FINAL_DISPOSITION.md) '
fields[12] = ' https://doi.org/' + new_doi + ' '
target = '|'.join(fields)
new_queue = main_queue.replace(original_row, target)
result['queue_patch_model'] = {
    'only_target_row_changes': new_queue.replace(target, original_row) == main_queue,
    'foreign_row_preserved': foreign_row in new_queue,
    'year': target.split('|')[7].strip(), 'author_turns': target.split('|')[9].strip(),
    'status': target.split('|')[8].strip(),
}
result['review_completion_percent'] = 100
(OUT / 'PROBE_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'review_completion_percent': 100,
                  'output': str(OUT / 'PROBE_RESULTS.json'),
                  'helper_top_levels_executed': 0, 'network_calls': 0,
                  'provider_writes': 0, 'git_index_ref_writes': 0}, indent=2))
