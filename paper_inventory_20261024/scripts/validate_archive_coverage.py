"""Independent whole-archive PDF semantic coverage audit; no network or remote mutations.

This separate audit does not write the canonical grouping files owned by the
corpus auditor. The family mapping was checked against all first-page titles and
member paths; exact candidate copies are additionally recognized by MD5.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parents[1]

def load(relative):
    return json.loads((HERE / relative).read_text())

def family(member):
    p = member.lower()
    mappings = [
        ('dimension_three_keller_degree/monodromy_realizability/weighted_lift_symmetric/', 'candidate:keller-weighted-lift-full-family'),
        ('dimension_three_keller_degree/rung1_generic_degree/', 'candidate:keller-generic-degree-spectrum'),
        ('/cube_component_exit/', 'candidate:keller-cube-component-exit'),
        ('/fixed_divisor_e2_quadratic_pencils/', 'candidate:keller-fixed-quadratic-pencil-quartic-exclusion'),
        ('/fixed_linear_cubic_pencil/', 'candidate:keller-fixed-linear-cubic-pencil-quartic-exclusion'),
        ('/exact_delta4_exclusion/', 'candidate:keller-exact-delta4-exclusion'),
        ('discovery_01_symmetric_monodromy/', 'candidate:full-symmetric-monodromy'),
        ('discovery_02_explicit_vanishing_counterexample/', 'candidate:explicit-vanishing-counterexample'),
        ('discovery_03_small_vanishing_counterexample/', 'candidate:symmetric-keller-and-vanishing'),
        ('discovery_04_wreath_monodromy/', 'candidate:wreath-monodromy'),
        ('discovery_05_sic21_counterexample/', 'candidate:sic21-counterexample'),
        ('discovery_06_unipotent_three_point/', 'candidate:unipotent-three-point'),
        ('discovery_07_unified_consequences/', 'candidate:unified-consequences'),
        ('cyclic_bell_tsirelson_bound/', 'candidate:cyclic-bell-tsirelson-bound'),
        ('cyclic_randomness_counterexample/', 'candidate:cyclic-bell-randomness-counterexample'),
        ('cyclic_bell_exact_values_and_randomness/', 'candidate:cyclic-bell-exact-values-and-randomness'),
        ('eternal_domination_lovasz_theta/', 'candidate:eternal-domination-lovasz-theta'),
        ('exceptional_ybe_spectrum/', 'candidate:exceptional-ybe-constraints'),
        ('exceptional_ybe_d4/', 'main:22013710'),
        ('gamma_theta_eternal_domination/paper/order12_frontier/', 'candidate:gamma-theta-order-12-frontier'),
        ('gamma_theta_eternal_domination/paper/order13_k3_complete/', 'candidate:gamma-theta-order-13-k3'),
        ('gamma_theta_eternal_domination/', 'candidate:gamma-theta-order-12-frontier'),
        ('hadamard_668_search/papers/eliahou_repair_obstructions/', 'candidate:hadamard-668-repair-obstructions'),
        ('hadamard_668_search/papers/lp333_fixed_compression/', 'candidate:hadamard-668-lp333'),
        ('hadamard_668_search/papers/semiregular_c37_conference/', 'candidate:hadamard-668-conference-lifts'),
        ('h668-eliahou-repair-obstructions.pdf', 'candidate:hadamard-668-repair-obstructions'),
        ('h668-lp333-fixed-compression.pdf', 'candidate:hadamard-668-lp333'),
        ('h668-semiregular-c37-conference-lifts.pdf', 'candidate:hadamard-668-conference-lifts'),
        ('local_obstructions_668.pdf', 'candidate:hadamard-668-repair-obstructions'),
        ('lalonde20_quantum_coloring/', 'candidate:lalonde-quantum-coloring'),
        ('minimum_bell_randomness/', 'candidate:permutation-blind-bell-randomness'),
        ('noncommutative_comparative_statics/', 'candidate:noncommutative-comparative-statics'),
        ('permutation_cell_unlearning_audit/', 'candidate:permutation-cell-auditing'),
        ('qubit_povm_pvm_minimum_settings/', 'main:21699161'),
        ('ramsey55_endpoint_capacity/', 'candidate:ramsey-endpoint-capacity'),
        ('weakly_reversible_continuum_no_common_factor/', 'candidate:reversible-mass-action-continuum'),
        ('bimolecular_positive_recurrence', 'main:22089551'),
        ('k2p_k3p_theta_trinet_collision/', 'main:22136869'),
        ('k2p_level2_identifiability_closure/', 'main:22168797'),
        ('k2p_same_neutral_referee_audit_', 'main:22168797'),
        ('k3p_level2_identifiability_final/', 'main:22178672'),
        ('maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/', 'main:22729355'),
        ('qbio_mass_action_turing_topology_phase3/', 'candidate:stationary-diffusion-driven-instability-complexity'),
        ('finite_rational_reductions_convex_to_polytope_neural_codes/', 'candidate:finite-rational-reductions-neural-codes'),
        ('relative_polygonalization_prescribed_traces_convex_neural_codes/', 'candidate:relative-polygonalization-neural-codes'),
        ('t3_2_positive_workload_final/', 'candidate:t3-two-linkage-positive-recurrence'),
        ('s_tc_jc_sharp_boundary/', 'main:22089373'),
        ('s_tc_jc_landmark_closure/', 'main:22089373'),
        ('/biorxiv_submission/', 'main:22089373'),
        ('/history/baseline_before_final_omega/', 'main:22089373'),
        ('/history/rejected_outcome_q/', 'main:22089373'),
        ('paper_ii_simultaneous_amplification_', 'main:22089807'),
        ('paper_i_complete_graph_extremality_', 'main:22089748'),
        ('paper_ii_simultaneous_amplification_referee_package_', 'main:22089807'),
        ('universal_simultaneous_amplification/phase4_landmark_closure/paper_lower_threshold/', 'candidate:simultaneous-amplification-below-three-halves'),
        ('universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/', 'main:22089807'),
        ('universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality/', 'main:22089748'),
        ('no_universal_death_birth_amplifier.pdf', 'candidate:no-universal-death-birth-amplifier'),
    ]
    docs = re.search(r'/docs/papers/([^/]+)/', p)
    if docs:
        slug = docs.group(1)
        return {'exceptional-ybe-d4': 'main:22013710'}.get(slug, 'candidate:' + slug)
    for needle, reference in mappings:
        if needle in p:
            return reference
    return None

def is_support(member):
    p = member.lower()
    terms = ['/figures/', '/external_audit/', '/review_packet/', '/outreach/',
             'technical-summary', 'technical_summary', 'technical-supplement',
             'technical_appendix', 'supplement', 'reader_supplement', 'cover_letter',
             'referee-guide', 'referee_guide', 'specialist-audit', 'specialist_audit',
             'k2p_displayed_tree_clarification.pdf', 'final_sharp_boundary_theorem.pdf']
    return any(term in p for term in terms)

def main():
    archive = load('sources/archive_papers.json')
    candidates = load('sources/supplemental_candidates.json')['candidates']
    main_rows = load('sources/corpus_records.json')['records']
    candidate_ids = {c['candidate_id'] for c in candidates}
    candidate_hashes = {c['md5']: c['candidate_id'] for c in candidates}
    main_ids = {r['id'] for r in main_rows if r['classification'] == 'paper'}
    dispositions, failures = [], []
    for row in archive['papers']:
        pdf = Path(row['pdf_path'])
        data = pdf.read_bytes()
        if len(data) != row['bytes'] or hashlib.md5(data).hexdigest() != row['member_md5'] or hashlib.sha256(data).hexdigest() != row['member_sha256']:
            failures.append(row['member'])
        exact = candidate_hashes.get(row['member_md5'])
        reference = 'candidate:' + exact if exact else family(row['member'])
        support = is_support(row['member']) and not exact
        disposition = 'support' if support else ('maincorpus' if reference and reference.startswith('main:') else 'editionofcandidate')
        valid_reference = (reference and ((reference.startswith('candidate:') and reference.split(':', 1)[1] in candidate_ids) or
                                          (reference.startswith('main:') and int(reference.split(':', 1)[1]) in main_ids)))
        if not valid_reference:
            failures.append('unmapped:' + row['member'])
        dispositions.append({'crc32': row['crc32'], 'bytes': row['bytes'],
            'member_sha256': row['member_sha256'], 'title': row['title'],
            'disposition': disposition, 'reference': reference, 'exact_canonical_candidate': bool(exact),
            'basis': 'exact candidate MD5' if exact else 'first-page/title and archived source-family path',
            'member': row['member'], 'source_deposit_id': row['source_deposit_id'], 'text_path': row['text_path'],
            'document_status': 'Rejected historical outcome Q draft; no promotion or submission recommendation' if '/history/rejected_outcome_q/' in row['member'] else 'See canonical work-group adjudication'})
    for row in archive['exact_matches_to_main_corpus']:
        if not row.get('direct_pdf_md5_sha256_match'):
            failures.append('unverified-primary-copy:' + str(row['main_corpus_id']))
        dispositions.append({'crc32': row['crc32'], 'bytes': row['bytes'], 'disposition': 'maincorpus',
            'member_sha256': row.get('member_sha256'), 'member_md5': row.get('member_md5'),
            'reference': f"main:{row['main_corpus_id']}", 'basis': 'Exact public archive member bytes matched to primary PDF using MD5 and SHA256, in addition to ZIP CRC32/size',
            'source_occurrences': row['all_archive_occurrences']})
    keys = [(r['crc32'], r['bytes']) for r in dispositions]
    if len(keys) != len(set(keys)) or len(keys) != archive['candidate_unique_pdf_payloads']:
        failures.append('payload coverage is not exact')
    exact_candidate_ids = {candidate_hashes[r['member_md5']] for r in archive['papers'] if r['member_md5'] in candidate_hashes}
    repo_only = sorted(candidate_ids - exact_candidate_ids)
    candidate_payload_count = len(dispositions)
    external_path = HERE / 'sources/corpus_external_archive_pdfs.json'
    external = json.loads(external_path.read_text())['pdfs'] if external_path.exists() else []
    for row in external:
        data = Path(row['pdf_path']).read_bytes()
        if len(data) != row['bytes'] or hashlib.md5(data).hexdigest() != row['member_md5'] or hashlib.sha256(data).hexdigest() != row['member_sha256']:
            failures.append('external-byte-mismatch:' + row['member'])
        dispositions.append({'crc32': row['crc32'], 'bytes': row['bytes'], 'member_sha256': row['member_sha256'],
            'disposition': row['disposition'], 'reference': row.get('reference', 'external-literature:' + Path(row['member']).name),
            'basis': row['basis'], 'member': row['member'], 'source_deposit_id': row['source_deposit_id'],
            'title': row.get('observed_title', row.get('pdf_metadata_title', '')), 'visual_review': row.get('visual_review', '')})
    expected_all = {(m['crc32'], m['bytes']) for a in load('sources/archive_listings.json')['archives']
                    for m in a['selected_members'] if m['member'].lower().endswith('.pdf')}
    observed_all = [(d['crc32'], d['bytes']) for d in dispositions]
    if set(observed_all) != expected_all or len(observed_all) != len(set(observed_all)):
        failures.append('Complete ZIP PDF payload set differs from dispositions')
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'independent_of': 'canonical work_group_adjudication category assignments',
        'scope': 'All 276 distinct PDF payloads in the 20 excluded published ZIPs, including 16 literature/support files initially filtered by path',
        'payloads': len(dispositions), 'disposition_counts': dict(Counter(r['disposition'] for r in dispositions)),
        'manuscript_candidate_payloads': candidate_payload_count, 'filtered_literature_support_payloads': len(external),
        'canonical_candidates': len(candidates), 'exact_archive_candidate_payloads': len(exact_candidate_ids),
        'candidate_ids_without_archive_payload': repo_only, 'unknown_payloads': len(failures), 'failures': failures,
        'conclusion': f"No additional unnamed manuscript family is left outside the {len(candidates)}-candidate supplement and direct corpus" if not failures else 'Unresolved cases remain',
        'limitations': 'This verifies scope, source identities and family coverage, not correctness or historical novelty. Source-family support classification does not promote every embedded draft to a standalone publication.',
        'dispositions': dispositions}
    output = HERE / 'reviews/archive_coverage_independent.json'
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'dispositions'}, indent=2))

if __name__ == '__main__': main()
