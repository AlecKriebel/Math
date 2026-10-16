"""Executable adversarial identity/format/scope controls for this priority audit.

Scope descriptions are human primary-source readings. Controls show that certain
invalid transfers are rejected; they are not an algorithm for literature novelty.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import re

TASK_DIR = Path(__file__).resolve().parent
WORKSPACE = TASK_DIR.parents[3]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_manifest(path, expected):
    document = json.loads(path.read_text())
    mismatches = []
    entries = document.get('files', document.get('first_party_artifacts'))
    if entries is None:
        raise ValueError('Unrecognized closed manifest schema')
    for entry in entries:
        member = path.parent / entry['path']
        recorded_size = entry.get('size', entry.get('bytes'))
        if not member.is_file() or member.stat().st_size != recorded_size or sha(member) != entry['sha256']:
            mismatches.append(entry['path'])
    return {'manifest_sha256': sha(path), 'expected_manifest_sha256': expected,
            'manifest_hash_matches': sha(path) == expected, 'members': len(entries),
            'mismatches': mismatches, 'read_only': True}

def homogeneous_scope(target_pi1, derivative_data):
    return target_pi1 == 0 and not derivative_data

def priority_evidence_gate(evidence):
    # These inputs encode manual source assessments; the gate does not make them.
    if evidence.get('exact_primary_antecedent_read'):
        return 'prior_solution'
    if evidence.get('equivalent_primary_theorem_verified'):
        return 'prior_solution'
    return 'novelty_unestablished'

if __name__ == '__main__':
    controls = []
    def add(name, observed, required, meaning):
        controls.append({'name': name, 'observed': observed, 'required': required,
                         'pass': observed == required, 'meaning': meaning})
    sources = TASK_DIR / 'sources'
    literal = (sources / 'question.tex').read_text()
    add('literal_exact_target_present', 'homotopy classification of totally real immersions' in literal, True,
        'The literal Q7 target is present; neighboring real-form uniformization is a separate question.')
    add('frozen_candidate_identity', sha(TASK_DIR.parent / 'source_snapshot' / 'CANDIDATE.md'),
        '501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050', 'Hash binds the compared candidate, not novelty.')
    add('received_survey_primary_byte_identity', sha(sources / 'survey_hal_v1_received.pdf'),
        'eb83de6334edafdbae8a9bd744fdc8c9abebbb05736bc9694a579203dfdfe81a',
        'Raw shared primary bytes independently bound; no root assessment is an input.')
    fv = (sources / 'fv2018.txt').read_text()
    add('reject_2018_as_2020_proposition_8_1', bool(re.search(r'Proposition\s+8\.1', fv)), False,
        'Actual 2018 text cannot serve as the later sphere proposition and proof.')
    for name in ['fv2020_publisher_response.pdf', 'survey_hal_file.pdf', 'surgeries_published.pdf']:
        add('reject_wrong_format_' + name, (sources / name).read_bytes().startswith(b'%PDF-'), False,
            'An HTTP 200 response with a .pdf suffix is not evidence of publisher PDF possession.')
    add('distinct_v1_and_v2_reduction_bytes', sha(sources / 'reductions2024.pdf') == sha(sources / 'reductions2024_v2.pdf'), False,
        'Actual v1 and v2 bytes differ; no version identity is inferred.')
    original = (sources / 'fv2018.pdf').read_bytes()
    add('reject_single_byte_source_mutation', hashlib.sha256(original + b'\0').hexdigest() == sha(sources / 'fv2018.pdf'), False,
        'Tampered bytes fail the identity comparison. No mathematical claim is thereby tested.')
    dj = (sources / 'derdzinski_arxiv.txt').read_text()
    add('earliest_dj_three_dimensional_surjectivity_note', 'surjectivity part of the above' in dj and 'n = 3' in dj, True,
        'The note is present in the 2006 primary variant, not merely in a later publication.')
    determinant_index = math.gcd(4, 2)
    add('frame_target_pi1_order', determinant_index, 2,
        'Own low-homotopy deduction from determinant weights: frame target is not simply connected.')
    add('reject_plain_koshkin_on_frame_target', homogeneous_scope(determinant_index, True), False,
        'Koshkin Theorem 3 assumptions cannot be discarded when substituting the frame target.')
    add('accept_koshkin_underlying_flag_scope', homogeneous_scope(0, False), True,
        'Underlying flag-map classification is within the prior theorem; derivative data is additional.')
    add('reject_metadata_only_novelty_certificate', priority_evidence_gate({'author_identity': True, 'model_hash': True}), 'novelty_unestablished',
        'Actual classifier control: neither model nor author identity supplies the required primary antecedent assessment.')
    add('reject_negative_search_only_novelty_certificate', priority_evidence_gate({'no_search_matches': True}), 'novelty_unestablished',
        'Actual classifier control: negative search results cannot certify novelty.')
    add('positive_prior_solution_control', priority_evidence_gate({'exact_primary_antecedent_read': True}), 'prior_solution',
        'If an exact primary antecedent is actually read and established, the verdict must change. This is a control, not an assertion that one was found.')
    closed = [
        (TASK_DIR.parents[1] / 'pr31_10000043' / 'primary_scope_family' / 'MANIFEST.json', '940701486b22fe02ab8467e5b43a13544ec7ab6d8250fd30ea39bfa077539572'),
        (TASK_DIR.parent / 'primary_scope_family' / 'MANIFEST.json', 'c4d4122c1e55874c980a3cc01cd69c978717954522f8bda0ff1dc257147a3fe0')]
    preservation = [check_manifest(path, expected) for path, expected in closed]
    result = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'controls': controls,
              'closed_family_preservation': preservation,
              'all_controls_pass': all(row['pass'] for row in controls),
              'closed_families_unchanged': all(row['manifest_hash_matches'] and not row['mismatches'] for row in preservation),
              'universal_math_certificate': False, 'novelty_certificate': False,
              'limits': 'Scope gates depend on independently recorded primary readings. The program detects specific invalid substitutions, not every possible equivalent predecessor.'}
    (TASK_DIR / 'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
