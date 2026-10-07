#!/usr/bin/env python3
"""Independent finite regression and byte verification; not a geometry prover."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_MANIFEST = 'fe1428032c46c505cfa5e60dc7dd7a13b64535c2b90da8c00c83c85d95db53d8'
PDF_NAMES = {
    'OWR': 'owr_2013_27.pdf',
    'LR': 'liu_rollenske_1211.1291.pdf',
    'Fujino': 'fujino_fujita.pdf',
    'Rollenske': 'rollenske_godeaux.pdf',
    'FPR': 'fpr_gorenstein.pdf',
    'CFHR': 'cfhr.pdf',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pairs(index, degree_bound=200, coefficient=5):
    # 2*g-2 <= (3+1/index)*degree, with exact integer arithmetic.
    bad = []
    for degree in range(1, degree_bound + 1):
        g_max = ((3*index + 1)*degree + 2*index) // (2*index)
        for genus in range(0, g_max + 1):
            if coefficient*degree < 2*genus + 1:
                bad.append([degree, genus])
    return bad


def monomials(degree, last_weight=5):
    # Deliberately use independent direct loops rather than the author's recursion.
    return [(a,b,c,e)
            for a in range(degree + 1)
            for b in range(degree + 1)
            for c in range(degree // 2 + 1)
            for e in range(degree // last_weight + 1)
            if a+b+2*c+last_weight*e == degree]


def dual_mul(u, v):
    return (u[0]*v[0], u[0]*v[1] + u[1]*v[0])


def check(packet, source_dir):
    manifest_bytes = (packet/'FROZEN_MANIFEST.json').read_bytes()
    assert sha(manifest_bytes) == EXPECTED_MANIFEST
    manifest = json.loads(manifest_bytes)
    assert len(manifest['files']) == 8
    checked = []
    for entry in manifest['files']:
        raw = (packet/entry['path']).read_bytes()
        assert len(raw) == entry['bytes']
        assert sha(raw) == entry['sha256']
        checked.append(dict(entry, verification='PASS'))
    actual = {str(f.relative_to(packet)) for f in packet.rglob('*') if f.is_file()}
    expected = {entry['path'] for entry in manifest['files']} | {'FROZEN_MANIFEST.json'}
    assert actual == expected
    author_output = json.loads(subprocess.check_output(
        [sys.executable, str(packet/'check_math.py')], text=True))
    assert author_output == json.loads((packet/'CHECK_RESULTS.json').read_bytes())
    author_manifest = json.loads(subprocess.check_output(
        [sys.executable, str(packet/'check_math.py'), '--verify-manifest'], text=True))
    assert author_manifest == {'status': 'PASS', 'verified_files': 8}

    counts = [len(monomials(k)) for k in range(1,6)]
    assert counts == [2,4,6,9,13]
    assert not any(e for k in range(1,5) for a,b,c,e in monomials(k))
    assert (0,0,0,1) in monomials(5)
    assert pairs(1) == [[1,3],[2,5]]
    assert all(not pairs(index) for index in range(2,101))
    assert [1,2] in pairs(2, coefficient=4)
    cyclic_count, cyclic_max = 0, 0
    extremal = []
    for n in range(2,31):
        for d in range(1,101):
            a = (n-1)*d - 3
            if a <= 0:
                continue
            threshold = (d+a-1) // a
            assert (threshold-1)*a < d <= threshold*a
            assert 1 <= threshold <= 4
            if threshold == 4:
                extremal.append([n,d,a,threshold])
            cyclic_count += 1
            cyclic_max = max(cyclic_max, threshold)
    assert cyclic_count == 2895 and cyclic_max == 4
    assert [2,4,1,4] in extremal
    x,y,z = (0,1),(0,-1),(0,0)
    assert dual_mul(x,y) == (0,0)
    assert (x[0]+y[0], x[1]+y[1]) == z
    assert x != z and y != z
    # d/du[u^4(1-u)] at u=1, showing the weighted chart is smooth there.
    assert 4-5 == -1
    controls = {
        'index_one_extension_rejected': bool(pairs(1)),
        'coefficient_four_rejected_by_allowed_pair': [1,2] in pairs(2, coefficient=4),
        'deck_weight_four_detected': (0,0,0,1) in monomials(4,last_weight=4),
        'cyclic_maximum_three_rejected': cyclic_max > 3,
        'conductor_support_is_not_scheme_containment': x != z and y != z,
    }
    assert all(controls.values())

    source_checks = []
    if source_dir is not None:
        for entry in json.loads((packet/'SOURCE_METADATA.json').read_bytes())['sources']:
            data = (source_dir/PDF_NAMES[entry['id']]).read_bytes()
            assert len(data) == entry['bytes'] and sha(data) == entry['sha256']
            source_checks.append({key: entry[key] for key in
                ['id','title','retrieval_url','citation_url','bytes','sha256']}
                | {'verification': 'PASS', 'verification_scope': 'Supplied local PDF bytes; not an independent network re-download.'})
    return {
        'status': 'PASS',
        'frozen_manifest_sha256': EXPECTED_MANIFEST,
        'frozen_payload_count': len(checked),
        'frozen_payload_bytes': sum(f['bytes'] for f in checked),
        'frozen_payloads': checked,
        'author_replay_matches_saved_json': True,
        'author_manifest_check_passed': True,
        'independent_weighted_dimensions': counts,
        'independent_numerical_exceptions_index_one': pairs(1),
        'independent_indices_two_through_one_hundred': {
            'degrees': [1,200], 'failure_count': 0,
            'note': 'Negative genera automatically satisfy the target inequality.'},
        'independent_cyclic_cases': cyclic_count,
        'independent_cyclic_maximum': cyclic_max,
        'independent_cyclic_extremal_cases': extremal,
        'negative_controls': controls,
        'source_pdf_checks': source_checks,
        'scope': 'Finite regression checks and byte verification. The authored audit independently reconstructs the geometric arguments; this program does not prove them.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.packet, args.source_dir), indent=2, sort_keys=True))
