#!/usr/bin/env python3
"""Exact source-binding, permutation, and homology controls for topology01.

No network, no topology classification computation, no Git writes.
This script writes only stdout. An optional argument selects the original
attempt directory; by default it reads the sibling audit snapshot.
"""
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ATTEMPT = (Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else
           HERE.parents[1] / 'original/unsolved_math_prioritization/attempts/30004404')
PACKAGE = ATTEMPT / 'package'
EXPECTED_MANIFEST = '4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8'
digest = lambda data: hashlib.sha256(data).hexdigest()

manifest_data = (PACKAGE / 'FROZEN_MANIFEST.json').read_bytes()
assert digest(manifest_data) == EXPECTED_MANIFEST
manifest = json.loads(manifest_data)
listed = {x['path'] for x in manifest['files']}
assert {str(x.relative_to(PACKAGE)) for x in PACKAGE.rglob('*') if x.is_file()} == listed | {'FROZEN_MANIFEST.json'}
for entry in manifest['files']:
    data = (PACKAGE / entry['path']).read_bytes()
    assert len(data) == entry['bytes'] and digest(data) == entry['sha256']

snapshot = json.loads((HERE.parents[1] / 'ORIGINAL_SNAPSHOT.json').read_text())
assert snapshot['head'] == 'e4b27ac757babc1aea75149ea986ed2beea438f9'
original_root = ATTEMPT.parents[2]
for entry in snapshot['files']:
    data = (original_root / entry['path']).read_bytes()
    assert len(data) == entry['size'] and digest(data) == entry['sha256']

# Independent finite quotient certificate: a nonidentity value of w under
# a homomorphism F_2 -> S_4 proves that w is not the identity free word.
identity = tuple(range(4))
def multiply(p, q):
    return tuple(p[q[i]] for i in range(4))

def inverse(p):
    return tuple(p.index(i) for i in range(4))

def commutator(p, q):
    return multiply(multiply(multiply(p, q), inverse(p)), inverse(q))

def evaluate(text, x, y):
    images = {'x': x, 'X': inverse(x), 'y': y, 'Y': inverse(y)}
    result = identity
    for letter in text:
        result = multiply(result, images[letter])
    return result

word = 'xyXYxxyXYXyxxYXX'
nonidentity = []
checked = 0
for x in permutations(range(4)):
    for y in permutations(range(4)):
        c = commutator(x, y)
        d = multiply(multiply(x, c), inverse(x))
        w = commutator(c, d)
        assert evaluate(word, x, y) == w
        if w != identity:
            nonidentity.append({'x': x, 'y': y, 'c': c, 'd': d, 'w': w})
        checked += 1
assert nonidentity
assert all(word[i].swapcase() != word[i+1] for i in range(len(word)-1))
assert len(word) == 16
# Every subgroup of S_3 is metabelian. Embedded permutations fixing 3 must
# satisfy this word, guarding against a broken commutator implementation.
s3_pairs = 0
for x in permutations(range(4)):
    if x[3] != 3:
        continue
    for y in permutations(range(4)):
        if y[3] == 3:
            assert evaluate(word, x, y) == identity
            s3_pairs += 1
assert s3_pairs == 36

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    return sum((-1)**j * matrix[0][j] * determinant(
        [row[:j] + row[j+1:] for row in matrix[1:]]) for j in range(n))

seifert = []
for slope, orders in [(1, (2,3,7)), (2, (2,4,5)), (3, (3,3,4))]:
    a,b,c = orders
    chi = Fraction(1,a)+Fraction(1,b)+Fraction(1,c)-1
    e = -1+Fraction(1,a)+Fraction(1,b)+Fraction(1,c)
    order = abs(a*b*c*e)
    # A compatible Seifert abelianization presentation, used only for the
    # absolute determinant. Orientation changes do not change its order.
    matrix = [[a,0,0,1],[0,b,0,1],[0,0,c,1],[1,1,1,1]]
    assert order == abs(determinant(matrix)) == slope
    assert chi < 0
    seifert.append({'positive_slope':slope,'base_cone_orders':orders,
                    'orbifold_chi':str(chi),'absolute_homology_order':int(order)})
assert [x['orbifold_chi'] for x in seifert] == ['-1/42','-1/20','-1/12']
assert seifert[1]['absolute_homology_order'] != seifert[2]['absolute_homology_order']

# Source bytes match independently retrieved receipts, rather than assuming
# that matching titles or OCR imply identical source versions.
fetched = {x['file']:x for x in json.loads((HERE/'SOURCE_DOWNLOAD_RECEIPTS.json').read_text())}
source_filenames = {
    'S1':'owr2020_8.pdf', 'S2':'thurston_ch4.pdf',
    'S3':'brittenham_wu_p32.pdf', 'S4':'vu_the_khoi_0803519.pdf',
    'S5':'gukov_manolescu_surgeries.pdf', 'S6':'imt2604_01697v1.pdf',
}
source_matches=[]
for original in json.loads((PACKAGE/'SOURCE_RECEIPTS.json').read_text())['sources']:
    source_id = original['source_id']
    independent = fetched[source_filenames[source_id]]
    assert original['sha256'] == independent['sha256']
    assert original['bytes'] == independent['bytes']
    source_matches.append(source_id)

# Reproduce both pre-existing controls, but do not use their finite tests as
# evidence for an all-rational topology theorem.
old_runs=[]
for script, expected in [
    (PACKAGE/'controls/check.py', PACKAGE/'controls/expected.json'),
    (ATTEMPT/'audit-independent/independent_checks.py', ATTEMPT/'audit-independent/independent_results.json'),
]:
    result = subprocess.run([sys.executable, str(script)], capture_output=True, check=True)
    assert result.stderr == b''
    assert result.stdout == expected.read_bytes()
    old_runs.append({'script':str(script.relative_to(ATTEMPT)),
                     'expected_sha256':digest(result.stdout),'byte_identical':True})

print(json.dumps({
    'result':'PASS',
    'scope':'Exact controls; all-slope topology comes from the written source audit.',
    'candidate_manifest_sha256':EXPECTED_MANIFEST,
    'candidate_authored_files_verified':len(listed),
    'acquisition_snapshot_files_verified':len(snapshot['files']),
    'declared_pr_head_from_acquisition_receipt':snapshot['head'],
    'independent_source_receipts_matching_candidate':source_matches,
    'S4_ordered_pairs':checked,
    'S4_nonidentity_word_pairs':len(nonidentity),
    'first_S4_witness_zero_based_image_lists':nonidentity[0],
    'embedded_S3_metabelian_pairs_with_identity_word':s3_pairs,
    'free_reduced_word':word,
    'free_reduced_length':len(word),
    'seifert_checks':seifert,
    'middle_source_equality_S2_equals_minus_Sminus3_fails_homology_order':True,
    'pre_existing_controls':old_runs,
    'limitations':[
        'Permutation evaluation proves the abstract free word is nontrivial; it is not a knot quotient calculation.',
        'Finite homology does not imply finite fundamental group.',
        'No finite computation here proves an exceptional surgery classification.',
        'Source receipts verify byte identity, not truth of the imported theorems.',
    ],
}, indent=2, sort_keys=True))
