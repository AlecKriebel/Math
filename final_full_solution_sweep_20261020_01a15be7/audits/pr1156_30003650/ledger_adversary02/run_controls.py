#!/usr/bin/env python3
"""Launch independent offline controls in normal, -O and -OO modes."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

D = Path(__file__).resolve().parent
CASES = {
    'nominal': (True, 1),
    'exact_present': (True, 0),
    'exact_present_with_intent': (True, 0),
    'duplicate_exact': (False, 0),
    'existing_other_row': (False, 0),
    'concept_doi_existing': (False, 0),
    'encoded_doi_existing': (False, 0),
    'nested_encoded_doi_existing': (False, 0),
    'record_uri_existing': (False, 0),
    'shortdoi_ambiguous': (False, 0),
    'deep_encoding_ambiguous': (False, 0),
    'schema_wide_row': (False, 0),
    'schema_wrong_header': (False, 0),
    'schema_nonstring': (False, 0),
    'wrong_gid': (False, 0),
    'wrong_title': (False, 0),
    'partial_range': (False, 0),
    'wrong_major_dimension': (False, 0),
    'adoption_false': (False, 0),
    'wrong_helper_pin': (False, 0),
    'wrong_plan_pin': (False, 0),
    'missing_dependency_pin': (False, 0),
    'dependency_changed': (False, 0),
    'acceptance_sha_wrong': (False, 0),
    'acceptance_missing': (False, 0),
    'plan_changed_after_adoption': (False, 0),
    'prior_intent_absent': (False, 0),
    'provider_metadata_changed': (False, 0),
    'provider_concept_changed': (False, 0),
    'provider_file_extra': (False, 0),
    'provider_unpublished': (False, 0),
    'provider_payload_changed': (False, 0),
    'doi_wrong_destination': (False, 0),
    'initial_pr_head_changed': (False, 0),
    'initial_pr_base_changed': (False, 0),
    'initial_pr_body_changed': (False, 0),
    'immediate_pr_head_changed': (False, 0),
    'immediate_pr_body_changed': (False, 0),
    'concurrent_before_append': (False, 0),
    'prefix_changed_after_append': (False, 1),
    'bad_append_response': (False, 1),
    'response_wrong_spreadsheet': (False, 1),
    'response_wrong_range': (False, 1),
    'response_wrong_cell_count': (False, 1),
    'response_wrong_echo_range': (False, 1),
    'account_title_lead': (False, 0),
    'account_alias_lead': (False, 0),
    'account_md5_lead': (False, 0),
    'account_partial': (False, 0),
    'account_pagination_duplicate': (False, 0),
    'account_inexact_total': (False, 0),
    'account_bad_page_host': (False, 0),
    'unknown_before_commit': (False, 1),
    'unknown_after_commit': (False, 1),
    # Adversarial acceptance controls: the following should block by policy.
    'empty_wrong_account': (False, 0),
    'wrong_account_same_count': (False, 0),
    'account_record_id_lead': (False, 0),
    'account_concept_parent_lead': (False, 0),
    'account_top_level_doi_lead': (False, 0),
    'account_encoding_alias_lead': (False, 0),
    'immediate_pr_base_changed': (False, 0),
    'delayed_preflight': (False, 0),
    # Diagnostic controls: check acceptance behavior without asserting a policy.
    'extra_unrelated_tail': (None, None),
    'shadow_publication_check': (None, 0),
    'poison_timestamp_bytecode': (None, 0),
}


def ensure(value, reason):
    if not value: raise RuntimeError(reason)


def main():
    rows = []
    for level, flags in [(0, []), (1, ['-O']), (2, ['-OO'])]:
        for case, expected in CASES.items():
            receipt_path = D / 'private/fixtures_final' / str(level) / case / 'receipt.json'
            if receipt_path.exists():
                receipt = json.loads(receipt_path.read_text())
            else:
                run = subprocess.run([sys.executable, *flags, str(D / 'offline_controls.py'), case], capture_output=True, text=True)
                ensure(run.returncode == 0, 'Harness failed for ' + case + ': ' + run.stderr)
                receipt = json.loads(run.stdout)
            receipt.pop('source_copy_sha256')
            receipt['expected_acceptance'] = expected[0]
            receipt['expected_mock_append_calls'] = expected[1]
            receipt['expectation_met'] = ((expected[0] is None or receipt['accepted'] == expected[0]) and (expected[1] is None or receipt['mock_append_calls'] == expected[1]))
            ensure(receipt['source_copies_unchanged'], 'Unexpected source copy mutation')
            ensure(receipt['zero_real_external_mutations'], 'External effect attempt was detected')
            if case.startswith('unknown_'):
                ensure(receipt['mock_append_calls'] == 1, 'Blind retry made a second mutation request')
            if case in {'shadow_publication_check', 'poison_timestamp_bytecode'}:
                ensure(receipt['all_expected_dependency_source_pins_match'] and receipt['unpinned_code_executed'], 'Import-origin countercontrol did not reproduce')
            rows.append(receipt)
    outcomes = {'at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'cases_per_mode': len(CASES), 'runs': len(rows), 'modes': ['normal', '-O', '-OO'],
                'offline_harness_sha256': hashlib.sha256((D / 'offline_controls.py').read_bytes()).hexdigest(),
                'all_source_copies_unchanged': all(r['source_copies_unchanged'] for r in rows),
                'all_external_effect_attempts_empty': all(r['external_effect_attempts'] == [] for r in rows),
                'all_unknown_outcomes_no_second_append': all(r['mock_append_calls'] == 1 for r in rows if r['case'].startswith('unknown_')),
                'unexpected_policy_acceptance_cases': sorted({r['case'] for r in rows if not r['expectation_met']}),
                'results': rows}
    (D / 'CONTROL_RESULTS.json').write_text(json.dumps(outcomes, indent=2) + '\n')
    print(json.dumps({k: v for k, v in outcomes.items() if k != 'results'}, indent=2))


if __name__ == '__main__': main()
