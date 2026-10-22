#!/usr/bin/env python3
"""Offline packet-integrity checks. This is not a mathematical proof checker."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
passed = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    passed.append(name)


def read(name):
    return json.loads((ROOT / name).read_text())


t = read('TARGET.json')
check('target_identity', (t['id'], t['code'], t['rank']) ==
      (30000576, 'OWR-1323-013', 658))
check('all_target_hypotheses_present', t['hypotheses'] == {
    'field': 'complex', 'space': 'separable Banach',
    'operators': 'bounded linear', 'continuity': 'strongly continuous (C0)',
    'parameter': 'real t >= 0',
    'chaos': 'hypercyclicity and dense semigroup-periodic vectors'})
check('both_positive_time_questions_retained', t['questions'] == [
    'all positive time maps chaotic?', 'some positive time map chaotic?'])
check('attribution_not_new_proof', t['evidence_level'] == 'attribution-only'
      and not t['new_mathematical_result_claimed']
      and not t['original_resolution_proof_inspected']
      and not t['original_resolution_all_hypotheses_directly_checked']
      and t['independent_audit_required'])
check('five_approaches_not_fabricated', t['proof_attempts_completed'] == 0)
sources = read('SOURCE_MANIFEST.json')['sources']
by_id = {x['id']: x for x in sources}
check('resolving_doi_and_access_limit', by_id['BB2009']['doi'] ==
      '10.1112/blms/bdp055' and by_id['BB2009']['pdf'] is None
      and not by_id['BB2009']['fulltext_inspected'])
check('original_and_corroborating_pdfs_identified', all(
    by_id[x]['pdf']['bytes'] > 100000 and
    len(by_id[x]['pdf']['sha256']) == 64 for x in ['OWR2006', 'MP2011', 'CLMP2017']))
dataset = read('DATASET_VERIFICATION.json')
check('both_corpus_files_matched', len(dataset['files']) == 2 and all(
    x['match'] and x['observed'] == x['expected'] for x in dataset['files']))
check('no_matching_fallback_report', dataset['matching_problem_records'] == 1
      and dataset['matching_report_keys'] == 0)
prior = read('PRIOR_ATTEMPT_CHECK.json')
check('live_queue_not_claimed_updated', prior['live_queue_status'] == 'queued'
      and prior['live_queue_turns'] == '0/5')
manifest = read('FREEZE_MANIFEST.json')
listed = {x['path']: x for x in manifest['files']}
actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
          if p.is_file() and p.name != 'FREEZE_MANIFEST.json'}
check('exact_safe_allowlist', set(listed) == actual)
for name, entry in listed.items():
    content = (ROOT / name).read_bytes()
    assert len(content) == entry['bytes'], name
    assert hashlib.sha256(content).hexdigest() == entry['sha256'], name
check('all_safe_file_hashes_match', True)
check('no_copied_source_documents', not any(
    x.endswith(('.pdf', '.html', '.png', '.zip')) or
    Path(x).name in ['problems.json', 'research_results.json'] or
    'private' in Path(x).parts for x in actual))
check('test_scope_disclosed', 'not validate' in
      (ROOT / 'LIMITATIONS.md').read_text())
print(json.dumps({'status': 'pass', 'tests_passed': passed,
                  'mathematical_proof_verified': False,
                  'fresh_independent_audit_performed': False}, indent=2))
