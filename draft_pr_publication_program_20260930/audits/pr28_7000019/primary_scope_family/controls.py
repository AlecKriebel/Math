#!/usr/bin/env python3
"""First-party source, scope, quantifier and normalization controls.

No submitted code is imported. These are falsifiable diagnostics, not a proof
certificate for Reichel's theorem or the full fixed-width question.
"""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
HEAD = '90a81313f3f65a7914fb6d5a9950fa087ea7467e'
PREFIX = 'unsolved_math_prioritization/attempts/7000019/'
checks = []
mutants = []


def check(name, condition, mechanism):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'pass': True, 'mechanism': mechanism})


def reject(name, wrong, correct, witness):
    check('reject_' + name, wrong != correct, witness)
    mutants.append({'name': name, 'rejected': True,
                    'wrong': str(wrong), 'correct': str(correct),
                    'witness': witness})


def digest(b):
    return hashlib.sha256(b).hexdigest()


def run():
    initial = json.loads((ROOT / 'EARLY_SEAL.json').read_text())
    check('early_seal_still_exact', all(
        digest((ROOT / f['path']).read_bytes()) == f['sha256']
        for f in initial['items']), 'Pre-packet reconstruction is immutable.')
    snapshot = json.loads((ROOT / 'ORIGINAL_SNAPSHOT_RECEIPT.json').read_text())
    check('all_17_snapshot_files_match_git', len(snapshot['files']) == 17 and all(
        digest(subprocess.check_output(['git', 'show', HEAD + ':' + f['path']]))
        == f['sha256'] for f in snapshot['files']),
        'Read exact detached Git head, not current working-tree files.')
    compare = json.loads((ROOT / 'MANIFEST_COMPARISON.json').read_text())
    check('manifest_all_files_and_18_path_scope', len(compare) == 18 and all(
        x.get('git_bytes_sha256_blob_match_manifest', x.get('pass', False))
        for x in compare), 'QUEUE is included in the 18 changed paths.')
    p = ROOT / '.tmp/original_snapshot' / PREFIX
    proof = (p / 'PROOF.md').read_text()
    source = json.loads((p / 'source_record.json').read_text())
    check('original_target_has_fixed_h_and_diameter', 'constant h < d' in
          source['statement'] and 'inradius' not in source['statement'],
          'Raw source target differs from the restricted theorem.')
    check('partial_theorem_preserves_inradius_regularity_global_C',
          'S = ∂K be of class C^{2,α}' in proof and
          'h<2r_{\\rm in}(K)' in proof and 'for one constant C' in proof,
          'Check the exact frozen theorem statement.')
    data = json.loads((ROOT / 'DATASET_CORRECT_JOIN_ADDENDUM.json').read_text())
    local = json.loads((ROOT / 'DATASET_LOCAL_RECEIPT.json').read_text())
    check('raw_prior_unique_code_join', data['prior_join_key'] ==
          'AMR-069-0019' and data['code_multiplicity'] == 1 and
          data['raw_prior_equal_frozen'],
          'Prior reports join by problem_number; numeric-ID lookup is wrong.')
    check('readonly_sql_and_upstream_lfs', local['sql']['record_equal_frozen']
          and local['sql']['prior_equal_frozen'] and
          all(data['upstream_lfs_matches_local'].values()) and
          data['sqlite_metadata_revision'] ==
          [['37e53eabe540fb458758e198be61634bd02ee008']],
          'The immutable upstream LFS OIDs match locally hashed raw JSON.')
    historical = json.loads((ROOT / 'HISTORICAL_HEADER_AND_SOURCE_RECEIPT.json').read_text())
    check('fresh_primary_PDF_bytes_match_original', all(
          historical['all_original_download_hashes_match_fresh'].values()),
          'Fresh independent downloads, not original cache reuse.')
    older = json.loads((ROOT / 'GHOMI_EARLIER_SOURCE_RECEIPT.json').read_text())
    txt = (ROOT / '.tmp/sources/ghomi2004.txt').read_text()
    check('historical_2004_question_documented', older['literal_pdf_page_index'] == 4
          and 'Last revised October 21, 2004.' in txt and 'Problem 22' in txt,
          'Earliest source found is author-hosted 2004 Problem 22, not 2019.')
    kim = (ROOT / '.tmp/sources/kimkim2012.txt').read_text()
    check('KimKim_small_height_limit_quantifier',
          'sufficiently small t > 0' in kim and 't→0' in kim and
          'Theorem 3' in kim and 'Lemma 8' in kim,
          'The adjacent result takes a varying-height limit.')
    replay = json.loads((ROOT / 'UNCHANGED_REPLAY_RECEIPT.json').read_text())
    check('unchanged_legacy_replays_byte_exact', len(replay['runs']) == 3 and all(
          x['script_unchanged'] and x['exit'] == 0 and
          x['byte_exact_against_frozen'] for x in replay['runs']),
          'Author, copied author, and old reviewer outputs reproduce exactly.')

    # Exact kernel controls include the saturated branch omitted by the old
    # proof's restricted-domain formula. Divide the orientation integral by 4pi.
    a, r = F(1), F(1, 2)
    kernel = lambda half, radius: F(1) if radius <= half else half / radius
    check('clipped_kernel_boundary', kernel(a, a) == 1,
          'The two kernel branches agree at distance equal to half-height.')
    reject('extend_Newton_branch_inside_cutoff', a / r, kernel(a, r),
           'a=1, distance=1/2: probability is 1, not 2.')
    reject('forget_full_to_half_height', F(2) / F(4),
           kernel(F(1), F(4)),
           'h=2, a=1, distance=4: normalized direction probability is 1/4.')
    R, h = F(2), F(3)
    area_over_pi, raw_potential_over_pi = 2 * R * h, 4 * R
    check('sphere_normalization_from_geometric_control',
          area_over_pi / (h / 2) == raw_potential_over_pi == 8,
          'Sphere R=2, h=3 has C/pi=12, U/pi=8.')
    reject('drop_half_height_in_potential', area_over_pi / h,
           raw_potential_over_pi,
           'C/a=2C/h, not C/h; the radius-2 sphere separates the two.')
    reject('apply_normalized_jump_to_raw_U', (F(-1), F(0)), (F(0), F(-4)),
           'Represent derivative as constant + pi*coefficient: raw U has -4*pi;'
           ' for Psi=U/(4pi), the derivative is -1. The two pairs preserve units.')

    # A periodic square-wave density is independent of the old cosine control.
    # It is a one-dimensional diagnostic only, not a realizable surface claim.
    def integral_square(left, right):
        total = F(0)
        while left < right:
            k = left.numerator // left.denominator
            middle = F(k) + F(1, 2)
            end = min(right, middle if left < middle else F(k + 1))
            density = F(3, 2) if left < middle else F(1, 2)
            total += density * (end - left)
            left = end
        return total

    check('one_period_integral_control', all(
          integral_square(t, t + 1) == 1
          for t in [F(0), F(1, 4), F(1, 2), F(3, 4), F(2)]),
          'Positive square-wave density has fixed-length integrals equal to 1.')
    reject('fixed_height_implies_all_small_heights',
           integral_square(F(0), F(1, 2)),
           integral_square(F(1, 2), F(1)),
           'The same density has half-height areas 3/4 and 1/4.')
    reject('diameter_bound_guarantees_open_core', True, F(3, 2) < F(1),
           'Ellipsoid semiaxes (3,1,1), h=3: h<diameter=6, a>inradius=1.'
           ' The ellipsoid is a parameter diagnostic, not a slab counterexample.')
    reject('nonstrict_inradius_bound_guarantees_open_core', True, F(1) < F(1),
           'Same ellipsoid, h=2: equality a=r_in=1 gives no point with dist>a.')
    check('tetrahedron_face_distance_average',
          tuple(sum(v[j] for v in [(1, 1, 1), (1, -1, -1),
                                   (-1, 1, -1), (-1, -1, 1)])
                for j in range(3)) == (0, 0, 0),
          'All point-dependent face-distance offsets average to the centered value.')
    reject('minimum_width_bound_implies_inradius_bound', True,
           F(3, 2) ** 2 < F(4, 3),
           'Regular tetrahedron has min width 2, (2r_in)^2=4/3, h=3/2.'
           ' It is not claimed to satisfy constant strip areas.')
    reject('one_interior_value_replaces_open_set', F(0), F(1),
           'Harmonic function x_1 equals zero at the origin but equals one at (1,0,0).')
    reject('nested_spheres_are_convex_body_boundary', True, F(1, 2) == F(2),
           'The radius-1/2 component is strictly inside the radius-2 convex hull.'
           ' It cannot be part of the convex hull boundary.')

    contract = dict(dimension=3, boundary='C2alpha', convex_body=True,
                    halfheight_strictly_below_inradius=True,
                    slab_constant_global=True, full_target_solved=False,
                    historical_novelty_certified=False,
                    external_peer_review_certified=False,
                    current_worldwide_open_status_certified=False)
    def errors(x):
        return [k for k, v in contract.items() if x.get(k) != v]
    check('partial_contract_valid', not errors(contract),
          'The contract separately labels every assumption and uncertified claim.')
    for field, value in [('dimension', 4), ('boundary', 'arbitrary'),
                         ('convex_body', False),
                         ('halfheight_strictly_below_inradius', False),
                         ('slab_constant_global', False),
                         ('full_target_solved', True),
                         ('historical_novelty_certified', True),
                         ('external_peer_review_certified', True),
                         ('current_worldwide_open_status_certified', True)]:
        bad = copy.deepcopy(contract)
        bad[field] = value
        check('contract_mutant_' + field, errors(bad) == [field],
              'This alteration changes a needed hypothesis or promotes an unverified claim.')
        mutants.append({'name': 'contract_' + field, 'rejected': True,
                        'rejected_fields': errors(bad)})

    result = {'status': 'PASS_CONTROLS_ONLY', 'target_head': HEAD,
              'control_count': len(checks), 'mutants_rejected': len(mutants),
              'checks': checks, 'mutants': mutants,
              'scope': 'Independent finite diagnostics plus source/artifact consistency;'
              ' manual argument and direct Reichel theorem reading supply universal partial validation.',
              'full_target_solved': False,
              'future_candidate_bytes_certified': False}
    (ROOT / 'CONTROLS_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ['checks', 'mutants']}, indent=2))


if __name__ == '__main__':
    run()
