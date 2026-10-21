"""Exact supplemental checks; this script does not prove the topological lemmas."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
AUDIT_ROOT = HERE.parents[1]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def run():
    ident = [[Q(1), Q(0)], [Q(0), Q(1)]]
    a = [[Q(3, 5), Q(-4, 5)], [Q(4, 5), Q(3, 5)]]
    b = [[3, -4], [4, 3]]
    transpose = [[a[j][i] for j in range(2)] for i in range(2)]
    assert mul(transpose, a) == ident
    assert a[0][0] * a[1][1] - a[0][1] * a[1][0] == 1
    b2 = mul(b, b)
    assert [[b2[i][j] - 6 * b[i][j] + 25 * ident[i][j] for j in range(2)] for i in range(2)] == [[0, 0], [0, 0]]
    # These exact coefficients support, but do not replace, the written induction.
    assert 6 % 5 == 1 and 25 % 5 == 0 and 6 % 5 != 0
    assert 3 - 1 >= 2 and 2 - 1 < 2
    assert [Q(0), Q(2, 3), Q(1)] == sorted({Q(0), Q(2, 3), Q(1)})

    pinned = json.loads((AUDIT_ROOT / 'ORIGINAL_SNAPSHOT.json').read_text())
    actual = {}
    for name, expected in pinned['files'].items():
        path = AUDIT_ROOT / 'original' / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == expected, name
        actual[name] = digest
    assert len(actual) == 27
    assert actual['unsolved_math_prioritization/attempts/30002555/public/PROOF.md'] == '78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464'

    fresh = json.loads((HERE / 'PRIMARY_EVIDENCE_MANIFEST.json').read_text())
    old = json.loads((AUDIT_ROOT / 'original/unsolved_math_prioritization/attempts/30002555/public/SOURCES.json').read_text())
    by_name = {record['name']: record for record in fresh['records']}
    comparison = {}
    for source, name in zip(old['sources'], ['owr2014_15.pdf', 'rmv2017.pdf', 'arsvw_v2.pdf']):
        assert by_name[name]['sha256'] == source['sha256']
        assert by_name[name]['bytes'] == source['bytes']
        comparison[source['id']] = {'current_bytes_match_old_metadata': True, 'historical_receipt_authenticated': False}
    assert len(fresh['visual_inspection']) == 20
    # Raw source bodies remain optional private evidence, excluded from public replay.
    checked = []
    for record in fresh['records']:
        local = HERE / 'private' / record['name']
        if local.exists():
            assert local.stat().st_size == record['bytes']
            assert hashlib.sha256(local.read_bytes()).hexdigest() == record['sha256']
            checked.append(record['name'])
    return {'exact_matrix_identities': True, 'recurrence_modulus_coefficients': True,
            'boundary_threshold_n3_vs_n2': True, 'original_files_checked': len(actual),
            'original_all_unchanged': True, 'primary_current_hash_comparison': comparison,
            'private_source_files_hash_checked_when_available': checked,
            'actual_visual_inspection_records': 20,
            'limits': 'Checks supplement the written proof; they do not prove proper discontinuity, nondisplaceability, novelty, or historical retrieval dates.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
