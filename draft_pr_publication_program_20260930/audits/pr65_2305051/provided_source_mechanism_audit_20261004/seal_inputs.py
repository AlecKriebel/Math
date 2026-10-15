#!/usr/bin/env python3
"""Create metadata-only audit verdict and freeze supplied sources privately."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path('/Users/alec/.cache/codex-pr65-priority-20261004/mechanism-independent-20261004')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sources = json.loads((HERE / 'SOURCES.json').read_text())
copies = CACHE / 'sources'
copies.mkdir(exist_ok=True)
frozen = []
for source in sources['sources'][:4]:
    original = Path(source['path'])
    data = original.read_bytes()
    assert hashlib.sha256(data).hexdigest() == source['sha256']
    dest = copies / original.name
    dest.write_bytes(data)
    frozen.append({'path': str(dest), 'sha256': source['sha256'], 'bytes': len(data)})

verdict = {
    'audit_family': 'explicit real-variable algorithm and ordinary-density obstruction',
    'audit_completed_utc': now,
    'pr': 65,
    'target': 'Holland Problem 5.51 / 2305051',
    'supplied_claimed_solved_head': '5cc1602c05d79502defb07cec7027963149494d2',
    'head_verification_scope': 'immutable/current identifier supplied by ROOT; no independent GitHub query',
    'original_candidate_sha256': '0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4',
    'original_proof_turns_changed': False,
    'method_origin_verified': 'Kahane fixed rule as printed by Piranian 1966 pp.260-261',
    'old_bloch_bridge_verified': 'Duren-Shapiro-Shields 1966 pp.248-250, repeated p.252',
    'submitted_vs_old': 'different deterministic child ordering of the same absorbed unit-step mechanism',
    'literal_copy_of_fixed_rule': False,
    'demonstrated_new_measure_mechanism': False,
    'new_benefit_of_submitted_ordering_verified': False,
    'all_point_ordinary_density_obstruction': 'verified, including grid endpoints and circle seam',
    'circular_zygmund_constant_verified': 24,
    'effective_midpoint_stages_from_old_rule': True,
    'full_holland_answer_printed_in_these_two_1966_sources': False,
    'full_target_from_old_rule': 'deduction conditional on correctly stated classical factorization and converse-Fatou inputs; assigned to analytic family',
    'historical_priority_final_articulation': 'unestablished',
    'closed_form_zero_list': 'not supplied by the old papers or the submitted candidate',
    'historical_meaning_of_explicit': 'unresolved; effective recursion and closed-form zero enumeration distinguished',
    'original_discovery_clearance': 'withheld',
    'qualified_pr50_publication_exception_used': False,
    'source_reading': {'piranian_complete_text': True, 'piranian_all_8_pages_visual': True,
                       'duren_complete_text': True, 'duren_all_8_pages_visual': True},
    'independence': {'first_conclusion_saved_before_other_review_opinions': True,
                     'other_review_opinion_bodies_read': False},
    'strongest_verified_result': 'old fixed rule defines atomless singular mass-one circle measure, global Zygmund primitive, no finite positive ordinary density anywhere, Bloch Herglotz transform by printed 1966 criterion, and effective midpoint Cayley approximants',
    'remaining_gaps': ['analytic converse-Fatou and factorization verification by separate family',
                       'historical priority of final pure-Blaschke Cayley articulation',
                       'original historical threshold intended by explicit'],
    'package_corrections': ['date fixed-rule antecedent to Piranian1966 pp.260-261 with Kahane credit',
                            'cite DSS1966 pp.248-250 as direct Bloch bridge',
                            'update stale full-body-not-read disclosures',
                            'do not promote mechanism novelty or worldwide priority'],
    'bounded_checks': {'generations': '0-9', 'local_child_cases': 225, 'facing_edge_cases': 1586,
                       'universal_proof_replaced_by_samples': False},
    'mutations': {'own_audit_files_only': True, 'git_index': False, 'native_app': False,
                  'pr': False, 'publication': False, 'shared_editor': False,
                  'external_human_contact': False},
    'completion_percent_this_audit': 100,
}
(HERE / 'VERDICT.json').write_text(json.dumps(verdict, indent=2) + '\n')
api_reads = {'recorded_utc': now,
             'timestamp_semantics': 'metadata record time; individual API invocation UTC was not supplied by view_image',
             'api': 'functions.exec/tools.view_image',
             'pid': None,
             'pid_semantics': 'API call, not an observed subprocess; no invented PID',
             'read_images': [{'path': str(CACHE / (paper + '-' + str(n) + '.png')),
                              'sha256': hashlib.sha256((CACHE / (paper + '-' + str(n) + '.png')).read_bytes()).hexdigest(),
                              'printed_page': start+n-1}
                             for paper, start in [('piranian',255),('duren',247)] for n in range(1,9)],
             'pdf_render_receipt_ids': ['0011', '0012'],
             'private_frozen_source_copies': frozen}
(HERE / 'API_READS.json').write_text(json.dumps(api_reads, indent=2) + '\n')
receipt = json.loads((HERE / 'FIRST_CONCLUSION.receipt.json').read_text())
assert hashlib.sha256((HERE / 'FIRST_CONCLUSION.md').read_bytes()).hexdigest() == receipt['sha256']
assert not receipt['prior_review_bodies_read']
assert json.loads((HERE / 'CHECKS.json').read_text())['stage_maximum'] == 9
print(json.dumps({'prepared_utc': now, 'first_conclusion_hash_unchanged': True,
                  'private_source_copies_verified': len(frozen), 'visual_pages_recorded': 16,
                  'verdict': 'mechanism preexisting1966; no novelty/priority clearance'}, indent=2))
