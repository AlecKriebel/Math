"""Record ROOT's personally adjudicated, bounded priority decision."""
import datetime
import hashlib
import json
import os
from pathlib import Path

audit = Path(__file__).resolve().parent.parent
program = audit.parents[1]
destination = audit / 'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.json'
note = audit / 'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.md'
if destination.exists() or note.exists():
    raise SystemExit('preserve the dated decision; do not overwrite')

def pin(p):
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'full_mode': p.stat().st_mode & 0o7777}

candidate = pin(audit / 'reviewed_candidate/CANDIDATE.md')
if candidate['sha256'] != '8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12':
    raise SystemExit('reviewed mathematical input changed')
access = audit / 'priority_access_revisit_20261003'
mechanism = audit / 'priority_mechanism_revisit_20261003/full_article_followup_20261003'
capture = program / 'audits/pr45_9900007'
metadata = json.loads((capture / 'root_pr18_eligible_metadata_after_fullbody_actual_capture/stdout.bin').read_bytes())
if metadata['headRefOid'] != '99e403e85d38d92b021198c4a57bbad3cd8775ba' or metadata['state'] != 'OPEN' or metadata['isDraft'] is not True:
    raise SystemExit('current eligible PR identity differs')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
decision = {
    'schema': 'pr18-root-current-bounded-priority-adjudication/v1', 'utc': now, 'actual_author_pid': os.getpid(),
    'status': 'PASS_BOUNDED_PRIORITY_PROCEED_TO_FIXED_PREPRINT_PACKAGE_REVIEW',
    'original_pr': 18, 'problem_id': 30001075, 'original_head': metadata['headRefOid'],
    'eligible_submitted_status': 'claimed_solved', 'current_pr_metadata': metadata,
    'reviewed_mathematical_input': candidate,
    'math_gate': 'Universal Conjecture4 proof passes ROOT reading and three previously credited independent mathematical families.',
    'exact_claim': 'The union of complete affine lines actually meeting three pairwise disjoint arbitrary convex subsets of R3 and contained in a supporting plane of each is contained in a Lebesgue-null set.',
    'stronger_countable_union_of_2_manifolds_claim': False,
    'named_combined_article_access_hold': 'RESOLVED_BY_COMPLETE_USER_SUPPLIED_PUBLISHED_BODY_AND_THREE_PERSONAL_READINGS',
    'supersedes_current_access_hold_in_historical_priority_assessments': True,
    'historical_priority_records_preserved': True,
    'root_entire_published_text_read': True, 'root_all_rendered_pages_read': False,
    'root_complete_rendered_pages_read': [677, 678, 683, 684, 689, 690, 691, 692, 693, 701],
    'published_article_pages': 30, 'published_article_bytes': 596169,
    'published_article_sha256': '478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc',
    'complete_body_comparisons': [
        pin(audit / 'root_priority_fulltext_20261003/ROOT_COMPARISON.md'),
        pin(access / 'REPORT.md'), pin(access / 'FULL_ARTICLE_COMPARISON.md'),
        pin(access / 'VERDICT.json'), pin(access / 'FINAL_ARTICLE_READ_RECORD.json'),
        pin(access / 'SOURCE_MANIFEST.json'), pin(mechanism / 'REPORT_FULL_ARTICLE.md'),
        pin(mechanism / 'SOURCE_RECEIPT_FULL_ARTICLE.json')
    ],
    'actual_source_evidence': [pin(capture / name / 'CAPTURE.json') for name in [
        'root_pr18_supplied_priority_article_extraction_actual_capture',
        'root_pr18_supplied_priority_article_render_actual_capture',
        'root_pr18_final_article_access_SOURCE_close_absolute_actual_capture',
        'root_pr18_final_article_access_SOURCE_readback_absolute_actual_capture',
        'root_pr18_full_article_mechanism_frozen_source_actual_capture',
        'root_pr18_eligible_metadata_after_fullbody_actual_capture']],
    'failed_relative_invocations_preserved': [
        'root_pr18_final_article_access_SOURCE_close_actual_capture',
        'root_pr18_final_article_access_SOURCE_readback_actual_capture'],
    'failed_invocations_scope': 'Both refused the literal relative argv before any custody mutation. Subsequent absolute invocations passed without source changes.',
    'exact_positive_prior_resolution_located': False,
    'full_article_additions_directly_checked': ['Finite k-flat weak-net lifting, printed683–684', 'Mnëv homotopy universality for3<=k<=d-3, printed693'],
    'historical_open_provenance': ['Official2008 OWR Conjecture4, printed2552', 'Full official-author-host manuscript archived2011-04-01 still asks compact nullness, printed11; archive/copy date not publication date'],
    'priority_scope': 'Earlier deep exact/mechanism/access audits plus fresh primary2026 searches and complete2023/2024 article. No sufficient prior proof or complete implication found in inspected evidence.',
    'priority_limit': 'Bounded literature audit, no exhaustive worldwide search or earliest-proof/current-openness certificate. Historical manuscript identity with September2008 citation remains unproved.',
    'no_specific_mathematical_or_priority_block_remaining': True,
    'allowed_next_step': 'Finalize a self-contained preprint and supporting package, then run the requested fresh independent whole-package adversarial review and repair loop.',
    'preprint_package_ready': False, 'new_package_adversarial_reviews_completed': 0,
    'original_attempts': '1/5', 'new_central_attempts': 0, 'new_mathematical_family_credit_from_priority_readers': 0,
    'pr18_publication_workflow_estimate_percent': 65, 'new_discovery_percent': 0,
    'zenodo_publication': False, 'doi': None, 'tracker_row': None, 'native_acceptance_or_merge': False,
    'outside_individual_contact': False
}
prose = '''# Current ROOT priority decision for PR18

The specific combined-article access hold is resolved. ROOT and two independent priority reviewers personally read all30 pages of Cheong–Goaoc–Holmsen's published 2023/2024 article, including both additions missing from earlier components and every presented proof. No sufficient prior resolution or complete implication to the exact spatial tritangent nullness claim was located. The full evidence is bound in the companion JSON and the three authored comparisons. Earlier access-only findings remain accurate dated history and are superseded for the present decision.

The mathematical gate remains passed for arbitrary disjoint convex sets: no closedness, boundedness, smoothness, genericity or full-dimensionality restriction has been introduced. The target is OWR44/2008 Conjecture4, not its stronger Conjecture3. ROOT reread the complete candidate and literal original statement. The earlier three independent mathematical families remain separately credited; this priority revisit adds no new proof-family or discovery credit.

The original open-problem provenance is the official2008 statement and the complete official-author-host manuscript preserved by a2011 archive capture, which still asks the compact nullness question. The capture and PDFcreation dates are not publication dates, and identity with the September2008 cited manuscript remains unproved. The recent article's finite incidence/existence and open-set meeting-transversal topology results do not supply metric control of supporting-line spatial sweeps. Its newly read k-flat and Mnëv additions likewise do not provide that conclusion.

The bounded priority audit found no located prior solution or material conflict. It cannot certify exhaustive worldwide priority or earliest proof. The preprint may frame its proved theorem as the resolution of the exact historical Conjecture4 and credit all standard tools and prior background. It must retain the documented bounded-search qualification and extensiveAI/unrefereed/no conventional human peer review disclosure.

Proceed to finalize the complete publication package and the requested fresh independent adversarial review→repair→new fresh review loop. The manuscript is not yet a fixed reviewed package. This decision creates no deposit, DOI, tracker row, native acceptance or PR merge. PR18 publication workflow estimate65%; new mathematical discovery in this revisit0%. Subsequent PRs remain in eligible-number order18,50,55,57 and onward; nonclaimed statuses remain excluded.
'''
for p, raw in [(destination, (json.dumps(decision, indent=2) + '\n').encode()), (note, prose.encode())]:
    with p.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    p.chmod(0o444)
entry = '\n' + now + ' — ROOT resolves the named combined-article priority hold after full published-body reading and two independent fullbody comparisons. All frozen source readbacks pass; no sufficient prior resolution or complete adapter found. Current bounded priority decision permits fixed preprint-package preparation/review, never exhaustive-first-proof certification. Original1/5,new0; publication workflow65%, discovery0%; no DOI/tracker/native acceptance.\n'
for p in [audit / 'RESEARCH_LOG.md', program / 'RESEARCH_LOG.md']:
    with p.open('a') as f:
        f.write(entry)
print(json.dumps({'status': decision['status'], 'utc': now, 'pid': os.getpid(), 'decision': pin(destination), 'note': pin(note)}, indent=2))
