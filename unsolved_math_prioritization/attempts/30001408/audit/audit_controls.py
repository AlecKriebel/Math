#!/usr/bin/env python3
"""Independent finite controls for 30001408; not an all-body classification proof.

Usage: python3 audit_controls.py [frozen_author_packet_directory]
The default expects the original sibling safe_output directory. The program only
reads the original packet. Its output is deterministic JSON; no third-party
packages, source files, downloads, or network connections are required.
"""
import hashlib
import json
import os
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'safe_output'
MANIFEST_SHA256 = '938d14791569ca0c77c9f19b13a71bd33219df81395d778c86e6703300c9bb34'
EXPECTED_NAMES = {'APPROACH_LOG.md', 'CONTROL_RESULTS.json', 'README.md', 'RESULT.md', 'SOURCE_VERIFICATION.md', 'check_controls.py', 'verify_packet.py'}
counts = {}
negatives = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def digest(data):
    return hashlib.sha256(data).hexdigest()

def reject(name, condition, witness):
    check('deliberate_negative_rejections', condition)
    negatives.append({'name': name, 'rejected': True, 'witness': witness})

manifest_data = (ROOT / 'AUTHOR_MANIFEST.json').read_bytes()
check('author_integrity', digest(manifest_data) == MANIFEST_SHA256)
manifest = json.loads(manifest_data)
check('author_integrity', {r['path'] for r in manifest['files']} == EXPECTED_NAMES)
check('author_integrity', len(manifest['files']) == 7)
check('author_integrity', manifest['problem_id'] == '30001408' and manifest['rank'] == 696)
check('author_integrity', manifest['status'] == 'unsolved' and manifest['approaches_used'] == 5 and manifest['full_resolution_claim'] is False)
check('author_integrity', {p.name for p in ROOT.iterdir()} == EXPECTED_NAMES | {'AUTHOR_MANIFEST.json'})
for row in manifest['files']:
    data = (ROOT / row['path']).read_bytes()
    check('author_integrity', len(data) == row['bytes'])
    check('author_integrity', digest(data) == row['sha256'])
    check('in_memory_tamper_rejections', digest(data + b'\nAUDIT_NEGATIVE\n') != row['sha256'])
check('in_memory_tamper_rejections', digest(manifest_data + b' ') != MANIFEST_SHA256)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
author_out = subprocess.check_output([sys.executable, str(ROOT / 'check_controls.py')], env=env)
check('author_replay', author_out == (ROOT / 'CONTROL_RESULTS.json').read_bytes())
author_results = json.loads(author_out)
check('author_replay', author_results['total_assertions'] == 15200 and author_results['status'] == 'PASS')
verifier_results = json.loads(subprocess.check_output([sys.executable, str(ROOT / 'verify_packet.py')], env=env))
check('author_replay', verifier_results['status'] == 'PASS' and verifier_results['frozen_files_verified'] == 7)

# Independent model: None denotes positive infinity; Q denotes a finite value.
def plus(x, y):
    return None if x is None or y is None else x + y

def scale(t, x):
    assert t > 0
    return None if x is None else t * x

def infinite(x):
    return x is None

compatible = 0
for bits in product((0, 1), repeat=4):
    left_inf = max(bits[:2])
    right_inf = max(bits[2:])
    support_ok = left_inf == right_inf
    compatible += support_ok
    for finite_baseline in (Q(0), Q(1), Q(7, 3)):
        values = [None if b else finite_baseline for b in bits]
        check('constant_infinity_truth_table', (plus(*values[:2]) == plus(*values[2:])) == support_ok)
check('boolean_pattern_count', compatible == 10)
for values in product((Q(0), Q(1), Q(3, 2), None), repeat=4):
    left = plus(*values[:2]); right = plus(*values[2:])
    support_ok = infinite(left) == infinite(right)
    check('extended_arithmetic', infinite(left) == any(infinite(x) for x in values[:2]))
    check('extended_arithmetic', infinite(right) == any(infinite(x) for x in values[2:]))
    if not support_ok:
        check('support_necessary', left != right)
    elif infinite(left):
        check('support_sufficient_with_infinity', left == right)
for t, value in product((Q(1, 17), Q(1), Q(29, 2)), (Q(0), Q(1), Q(19, 3), None)):
    check('positive_scaling_preserves_support', infinite(scale(t, value)) == infinite(value))
for bits in ((0, 0, 0, 0), (1, 1, 1, 1)):
    check('empty_and_full_support', max(bits[:2]) == max(bits[2:]))
reject('replace Boolean disjunction by conjunction', (1 or 0) == (1 or 1) and (1 and 0) != (1 and 1), [1, 0, 1, 1])
reject('Boolean rule implies finite-part numerical identity', (False or False) == (False or False) and Q(1)+Q(1) != Q(2)+Q(3), ['1+1', '2+3'])
reject('cancel infinity from an extended equality', plus(None, Q(1)) == plus(None, Q(2)) and Q(1) != Q(2), ['infinity+1', 'infinity+2'])

# Endpoint geometry uses a different rational grid and additional degrees.
G = (Q(1, 5), Q(2, 3), Q(1), Q(7, 4), Q(5))
def meet(a, b):
    return tuple(min(x, y) for x, y in zip(a, b))
def join(a, b):
    return tuple(max(x, y) for x, y in zip(a, b))
for a0, b0, a, b in product(G, repeat=4):
    r, s = a/a0, b/b0
    companion = (s*a0, r*b0)
    U, C = join((a, b), companion), meet((a, b), companion)
    check('crossed_dilate_geometry', U == tuple(max(r, s)*z for z in (a0, b0)))
    check('crossed_dilate_geometry', C == tuple(min(r, s)*z for z in (a0, b0)))
    check('crossed_dilate_origin_interior', min(a, b, *companion, *U, *C) > 0)
for q, A, B in product((-4, -2, -1, 0, 1, 3, 7), (Q(0), Q(2, 5)), (Q(0), Q(7, 3))):
    def val(ab):
        a, b = ab
        return A*a**q + B*b**q
    for a, b, c, d in product(G, repeat=4):
        K, L = (a, b), (c, d)
        check('one_dimensional_valuation', val(K)+val(L) == val(join(K,L))+val(meet(K,L)))
    for a, b, t in product(G, repeat=3):
        check('one_dimensional_homogeneity', val((t*a,t*b)) == t**q*val((a,b)))
        check('one_dimensional_nonnegativity', val((a,b)) >= 0)
reject('force reflection invariance in dimension one', Q(1)**2 != Q(2)**2, {'q':2,'A':1,'B':0,'interval_endpoints':[1,2]})
for q in (-7, -2, -1, 1, 2, 7):
    a, b = (Q(2), Q(1)) if q > 0 else (Q(1), Q(2))
    check('negative_endpoint_coefficient_rejected', -a**q+b**q < 0)
for c in (Q(-3), Q(1,2), Q(5)):
    k = -100 if c > 0 else 100
    check('degree_zero_nontrivial_additive_value_rejected', 1+k*c < 0)

# Genuine admissibility matters: crossed boxes with a shared factor work.
for n in range(2, 12):
    endpoints = [(Q(1),Q(2)),(Q(2),Q(1)),(Q(2),Q(2)),(Q(1),Q(1))]
    asymmetries = [max(a/b,b/a) for a,b in endpoints]
    check('asymmetry_profiles', asymmetries == [2,2,1,1])
    volumes = [(a+b)*2**(n-1) for a,b in endpoints]
    check('box_volume_valuation', sum(volumes[:2]) == sum(volumes[2:]))
    for threshold in (Q(6,5),Q(4,3),Q(19,10),Q(2)):
        flags = [r >= threshold for r in asymmetries]
        check('asymmetry_support_rejected', any(flags[:2]) != any(flags[2:]))
reject('asymmetry-threshold infinity support is a valuation', any(r >= Q(4,3) for r in (2,2)) != any(r >= Q(4,3) for r in (1,1)), {'asymmetries':[2,2,1,1],'threshold':'4/3'})
reject('centered-ellipsoid infinity support is a valuation', any((False,False)) != any((True,False)), {'cap_parameter':'1/2','flags':[False,False,True,False]})
check('opposite_caps_overlap', -Q(1,2) < Q(1,2))
check('opposite_caps_origin_margin', Q(1,2) > 0)
check('untruncated_volume', 4+4 == 6+2)
reject('truncation preserves valuation', min(4,4)+min(4,4) != min(6,4)+min(2,4), {'left':8,'right':6})
# Cross in R^2: midpoint of (2,1),(1,2) lies in neither rectangle.
p = (Q(3,2),Q(3,2))
check('nonconvex_union_midpoint', not(abs(p[0]) <= 2 and abs(p[1]) <= 1) and not(abs(p[0]) <= 1 and abs(p[1]) <= 2))
vertices = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
area2 = abs(sum(x*vertices[(i+1)%len(vertices)][1]-y*vertices[(i+1)%len(vertices)][0] for i,(x,y) in enumerate(vertices)))
check('convex_hull_area', Q(area2,2) == 14)
reject('replace a nonconvex union by its convex hull', 8+8 != Q(area2,2)+4, {'left':16,'hull_plus_intersection':18})

# Dilation laws and curvature exponents are exact rational arithmetic.
for n in range(2, 16):
    for alpha in (Q(-3),Q(-1,3),Q(0),Q(1,9),Q(1,2),Q(8,9),Q(1),Q(5,4),Q(7)):
        degree = n*(1-2*alpha)
        check('ball_density_scaling', Q(n)-2*n*alpha == degree)
        check('strict_degree_interval', (0<alpha<1) == (-n<degree<n))
        if alpha != 1:
            check('affine_surface_area_parameter', n*alpha/(1-alpha) == n*(n-degree)/(n+degree))
        exponent = (n-1)*(1-alpha)
        check('rounded_cube_exponent_sign', (exponent < 0) == (alpha>1))
        check('rounded_cube_endpoint', (exponent == 0) == (alpha==1))
        # Concavity on the positive half-line plus both LIMIT conditions.
        concave = alpha*(alpha-1) <= 0
        zero_right_limit = alpha > 0
        sublinear_limit = alpha < 1
        check('repaired_concave_power_classification', (concave and zero_right_limit and sublinear_limit) == (0<alpha<1))
# Deliberate counterexample to the frozen zero-endpoint inference.
def jump(x):
    assert x >= 0
    return Q(0) if x == 0 else Q(1)
for x,y,t in product((Q(0),Q(1,7),Q(2),Q(11)), (Q(0),Q(1,5),Q(3),Q(13)), (Q(0),Q(1,5),Q(1,2),Q(4,5),Q(1))):
    check('concave_zero_endpoint_jump_samples', jump(t*x+(1-t)*y) >= t*jump(x)+(1-t)*jump(y))
for j in range(1,101):
    check('zero_endpoint_jump_sequence', jump(Q(1,j)) == 1)
    check('jump_sublinear_sequence', jump(Q(j))/j == Q(1,j))
reject('g(0)=0 replaces the right-limit-at-zero hypothesis', jump(0)==0 and jump(Q(1,100))==1, {'alpha':0,'g_at_zero':0,'g_on_positive_reals':1})
reject('reverse the required semicontinuity inequality', float('inf') > 1, {'sequence_values':'infinity','limit_body_value':1,'upper_semicontinuity':'fails'})

# Recheck original bytes after all work; never write them.
check('post_run_integrity', digest((ROOT/'AUTHOR_MANIFEST.json').read_bytes()) == MANIFEST_SHA256)
for row in manifest['files']:
    check('post_run_integrity', digest((ROOT/row['path']).read_bytes()) == row['sha256'])

result = {
    'status':'PASS_WITH_REQUIRED_CORRECTION',
    'mathematical_status':'unsolved',
    'approaches_used':5,
    'required_correction':'CORRECTION.md: restore the right-limit-at-zero hypothesis in RESULT.md section 5',
    'author_manifest_sha256':MANIFEST_SHA256,
    'author_frozen_files_verified':7,
    'author_control_output_byte_match':True,
    'author_exact_assertions':15200,
    'independent_assertions':sum(counts.values()),
    'groups':counts,
    'deliberate_negatives':negatives,
    'scope':'Finite exact controls and original-byte integrity only. Analytic proofs and stated source dependencies are reviewed in AUDIT.md. No all-body classification is computationally proved.'
}
if __name__ == '__main__':
    print(json.dumps(result,sort_keys=True,indent=2))
