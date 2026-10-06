#!/usr/bin/env python3
"""Seal this priority adjudication only; no repository or service mutations."""
from pathlib import Path
import datetime
import hashlib
import json

D = Path(__file__).resolve().parent
A = D.parent
utc = datetime.datetime.now(datetime.UTC).isoformat()


def pin(p, relative):
    body = p.read_bytes()
    return {'path': relative, 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest()}


def save(name, value):
    (D / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


normal = json.loads((D / 'verification_normal.json').read_text())
optimized = json.loads((D / 'verification_optimized.json').read_text())
if normal != optimized or normal['status'] != 'PASS' or normal['explicit_guards'] != 206:
    raise ValueError('actual completed normal/optimized results disagree')
initial = json.loads((D / 'INDEPENDENT_INITIAL_CONCLUSIONS.json').read_text())
family_dirs = [
    'historical_priority_adversary_20261006',
    'modern_citation_priority_adversary_20261006',
    'quasiperiodic_counterexample_priority_20261006',
]
families = []
for folder in family_dirs:
    base = A / folder
    files = ['REPORT.md', 'RESULT.json', 'OUTPUT_MANIFEST.json']
    if (base / 'SOURCE_MANIFEST.json').is_file():
        files.append('SOURCE_MANIFEST.json')
    if (base / 'SOURCE_TABLE.json').is_file():
        files.append('SOURCE_TABLE.json')
    families.append({'family': folder, 'final_report_read': True,
                     'all_portable_member_pins_checked': True,
                     'members_authenticated': normal['family_manifest_members_authenticated'][folder],
                     'pins_relative_to_A111': [pin(base / f, folder + '/' + f) for f in files]})

sources = [
    {'name': 'Parker–Goluskin arXiv2510.14870v2',
     'url': 'https://arxiv.org/pdf/2510.14870v2',
     'official_record': 'https://arxiv.org/abs/2510.14870v2',
     'version_date': '2026-01-21',
     'read_printed_pages': [2, 5, 7], 'rendered_and_visually_inspected': True,
     'body_provenance': 'Copied source-family authenticated PDF; exact byte pin verified; official version record independently opened.',
     'private_body_pin': pin(D / 'private_primary_sources/parker_goluskin_v2.pdf', 'private_primary_sources/parker_goluskin_v2.pdf')},
    {'name': 'Zelik author dlyap.pdf',
     'url': 'https://sergey-zelik.co.uk/publications/dlyap.pdf',
     'associated_official_article': 'https://www.aimsciences.org/article/doi/10.3934/cpaa.2008.7.971',
     'official_publication': 'On the Lyapunov dimension of cascade systems, CPAA7(4):971–985 (2008); DOI10.3934/cpaa.2008.7.971',
     'actual_author_version_title': 'A remark on a uniform Lyapunov dimension of cascade systems',
     'version_date': 'undated actual author body',
     'read_printed_pages': [10, 11, 12], 'rendered_and_visually_inspected': True,
     'body_provenance': 'Actual own bounded HTTPS GET agrees byte-for-byte with copied source-family PDF; official article metadata independently opened.',
     'author_journal_body_identity_authenticated': False,
     'private_body_pin': pin(D / 'private_primary_sources/zelik_dlyap_own_get.pdf', 'private_primary_sources/zelik_dlyap_own_get.pdf')},
    {'name': 'Eden1989 M2AN article',
     'url': 'https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf',
     'read_printed_pages': [408, 409, 410, 411], 'visually_inspected_printed_pages': [409, 411],
     'body_provenance': 'Read actual source-family authenticated PDF; body not copied into this folder.',
     'private_body_pin_relative_to_A111': pin(A / 'primary_source_scope_adversary_20261006/private_primary_sources/eden1989.pdf',
         'primary_source_scope_adversary_20261006/private_primary_sources/eden1989.pdf')},
]
save('SOURCE_AND_FAMILY_MANIFEST.json', {
    'schema': 'pr111-priority-adjudicator-input-source-family-pins/v1',
    'UTC': utc, 'sources': sources, 'family_reports': families,
    'candidate_and_imported_inputs': initial['candidate'],
    'independent_initial_conclusions_pin': pin(D / 'INDEPENDENT_INITIAL_CONCLUSIONS.json', 'INDEPENDENT_INITIAL_CONCLUSIONS.json'),
    'copyright_bodies_are_private_and_excluded': True,
    'personally_read_body_ranges_only': True,
})
save('RESULT.json', {
    'schema': 'pr111-cross-family-priority-adjudication/v1', 'UTC': utc,
    'PR': 111, 'original_head': '8a7270989d7064a4b97badecaa4b311db5e6d49f',
    'problem_id': 4900006, 'problem_number': 'AMR-048-0006',
    'assigned_bounded_adjudication_complete': True, 'adjudication_completion_percent': 100,
    'persistent_program_best_guess_percent': 18 / 99 * 100,
    'math_gate_changed': False, 'mathematics_accepted': True,
    'original_genuinely_open_target_established': False,
    'novel_original_open_problem_resolution_established': False,
    'entire_R5_mathematical_strength_beyond_simple_prior_example': True,
    'exact_prior_entire_R5_theorem_authenticated': False,
    'substantive_research_novelty_of_stronger_theorem_established': False,
    'prior_author_named_Eden_disproof_authenticated': False,
    'Zelik_author_journal_body_identity_authenticated': False,
    'publication_as_claimed_solved_original_open_problem_cleared': False,
    'already_solved_disposition_scope': 'Broad imported manifold-inclusive target/classical obstruction only, not an attribution of the entire strengthened R5 theorem.',
    'recommended_disposition': 'Do not publish/merge as a novel decisive original-open-problem resolution. Preserve stronger verified mathematics. Any source-wording/already-resolved closure must explicitly distinguish valid R5 theorem, broad classical obstruction, and unresolved exact strengthened priority.',
    'fresh_package_R1_R2_performed': False,
    'new_central_proof_search_turns': 0, 'subdelegation': False,
    'checks': normal,
    'mutations': {'Git': False, 'index': False, 'refs': False, 'PR': False,
                  'publication': False, 'service': False, 'source_cache': False},
    'external_human_contact': False, 'human_peer_review_performed': False,
    'remaining_material_gaps': ['Original1989 thesis', 'Eden–Foias–Temam1991 body',
        'Eden1990 body', 'Leonov–Lyashko1993 body', '2020 dimension book chapter body',
        'Zelik exact journal body/version identity'],
})
with (D / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n' + utc + ' — All three finalized family reports read; all45 portable members authenticated. '
                 'Normal and optimized checks both passed206 explicit guards. Assigned adjudication100% complete; '
                 'persistent program18.18%; publication/novelty clearance not achieved. No service or repository mutation.\n')
members = []
for p in sorted(D.iterdir()):
    if p.is_file() and p.name != 'OUTPUT_MANIFEST.json':
        if p.suffix in ('.pdf', '.png', '.txt'):
            raise ValueError('Unexpected copyright-body-like top-level output: ' + p.name)
        members.append(pin(p, p.name))
save('OUTPUT_MANIFEST.json', {
    'schema': 'pr111-cross-family-priority-portable-output/v1', 'UTC': utc,
    'members': members, 'excluded': ['private_primary_sources/', '__pycache__/'],
    'self_hash_omitted': True, 'scope': 'Dedicated adjudicator folder only; original analysis, verification controls and metadata.',
    'copyright_bodies_or_renders_included': False,
})
for item in members:
    if pin(D / item['path'], item['path']) != item:
        raise ValueError('Sealed member changed: ' + item['path'])
print(json.dumps({'status': 'SEALED_READBACK_PASS', 'members': len(members),
                  'output_manifest': pin(D / 'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.json'),
                  'report': pin(D / 'REPORT.md', 'REPORT.md'),
                  'result': pin(D / 'RESULT.json', 'RESULT.json')}, indent=2))
