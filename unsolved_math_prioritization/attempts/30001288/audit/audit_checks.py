#!/usr/bin/env python3
"""Independent exact finite audit and executable verifier regression tests.

No motivic, Chow, Lawson, or Hodge-theoretic claim is decided by this program.
Run in both normal and optimized wrapper modes. Each wrapper explicitly launches
both normal and optimized child interpreters; wrapper optimization is not assumed
to propagate. The original packet is only read. All corruptions use temp copies.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import collections
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile

ORIGINAL_PIN = 'e3849b16c9617fdbb72cd81ce14dd282ed2fbd1b64d01664e4c14411ac2cb892'
CORRECTED_PIN = '8dcbfa59690c015db89b9d0ef5e5c35258fbc3bbda70618799446dd147b4e518'
PAYLOADS = {
    'CHECK_RESULTS.json', 'FORMULATION.md', 'GAPS.md', 'GATE.md',
    'GATE_METADATA.json', 'MATHEMATICS.md', 'OUTCOME.json', 'README.md',
    'SOURCES.md', 'SOURCE_METADATA.json', 'checks.py',
}
COUNTS = collections.Counter()


class AuditFailure(RuntimeError):
    pass


def need(condition, category):
    COUNTS[category] += 1
    if not condition:
        raise AuditFailure(category)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_verify(base, expected_digest):
    """Externally pin the manifest, validate inventory, then verify payloads.

    The digest argument must come from a separately trusted audit record. A
    self-consistent rehash of modified content is not an authenticated original.
    """
    path = base / 'AUTHOR_MANIFEST.json'
    if path.is_symlink() or not path.is_file():
        raise AuditFailure('missing or symlinked manifest')
    if digest(path) != expected_digest:
        raise AuditFailure('external manifest pin mismatch')
    obj = json.loads(path.read_text())
    if obj.get('schema_version') != 1 or obj.get('problem_id') != 30001288:
        raise AuditFailure('manifest identity or schema mismatch')
    if obj.get('manifest_excludes') != ['AUTHOR_MANIFEST.json']:
        raise AuditFailure('unexpected manifest exclusions')
    entries = obj.get('files')
    if not isinstance(entries, list):
        raise AuditFailure('manifest files must be a list')
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {'file', 'bytes', 'sha256'}:
            raise AuditFailure('malformed manifest entry')
        name = entry['file']
        if not isinstance(name, str) or name not in PAYLOADS or name in seen:
            raise AuditFailure('unsafe, unexpected, or duplicate payload name')
        seen.add(name)
        size = entry['bytes']
        sha = entry['sha256']
        if type(size) is not int or size < 0:
            raise AuditFailure('invalid payload byte count')
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            raise AuditFailure('invalid payload digest')
        payload = base / name
        if payload.is_symlink() or not payload.is_file():
            raise AuditFailure('missing or symlinked payload')
        data = payload.read_bytes()
        if len(data) != size or hashlib.sha256(data).hexdigest() != sha:
            raise AuditFailure('payload byte count or digest mismatch')
    if seen != PAYLOADS:
        raise AuditFailure('manifest coverage mismatch')
    actual = {p.name for p in base.iterdir()}
    if actual != PAYLOADS | {'AUTHOR_MANIFEST.json'}:
        raise AuditFailure('packet inventory mismatch')
    return obj


def determinant(a):
    """Leibniz determinant, independent of the author's Gaussian elimination."""
    n = len(a)
    total = Q(0)
    for perm in permutations(range(n)):
        term = Q((-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n)))
        for i, j in enumerate(perm):
            term *= a[i][j]
        total += term
    return total


def minor_rank(a):
    if not a:
        return 0
    n = len(a[0])
    if any(len(row) != n for row in a):
        raise ValueError('ragged independent matrix')
    for r in range(min(len(a), n), 0, -1):
        for rows in combinations(range(len(a)), r):
            for cols in combinations(range(n), r):
                if determinant([[a[i][j] for j in cols] for i in rows]):
                    return r
    return 0


def row_reduce(a, width=None):
    b = [[Q(x) for x in row] for row in a]
    n = len(b[0]) if b else (width or 0)
    pivots = []
    for j in range(n):
        i = next((i for i in range(len(pivots), len(b)) if b[i][j]), None)
        if i is None:
            continue
        r = len(pivots)
        b[r], b[i] = b[i], b[r]
        scale = b[r][j]
        b[r] = [x / scale for x in b[r]]
        for i in range(len(b)):
            if i != r:
                scale = b[i][j]
                b[i] = [x - scale * y for x, y in zip(b[i], b[r])]
        pivots.append(j)
    return b, pivots


def nullspace(a, n):
    reduced, pivots = row_reduce(a, n)
    basis = []
    for j in range(n):
        if j not in pivots:
            v = [Q(int(i == j)) for i in range(n)]
            for i, p in enumerate(pivots):
                v[p] = -reduced[i][j]
            basis.append(v)
    return basis


def apply(a, v):
    if any(len(row) != len(v) for row in a):
        raise AuditFailure('matrix-vector dimension mismatch')
    return [sum(Q(x) * y for x, y in zip(row, v)) for row in a]


def exact_controls(original):
    author = runpy.run_path(str(original / 'checks.py'), run_name='audited_module')
    matrix_cases = 0
    for m in range(1, 4):
        for n in range(1, 4):
            for entries in product((-1, 0, 1), repeat=m * n):
                a = [entries[i*n:(i+1)*n] for i in range(m)]
                r = minor_rank(a)
                need(author['rank'](a) == r, 'author_rank_vs_determinant_minors')
                need(len(row_reduce(a)[1]) == r, 'audit_reduction_vs_determinant_minors')
                matrix_cases += 1

    for m in range(25):
        for p in range(m + 3):
            terms = [(j, p-j) for j in range(m+1) if 0 <= p-j <= 1]
            need(len(terms) == (0 if p > m+1 else 1 if p in (0, m+1) else 2), 'independent_chow_components')
            need(sum(q == 1 for _, q in terms) == int(1 <= p <= m+1), 'independent_chow_connected')
            if 1 <= p <= m+1:
                r = m+1-p
                terms_lawson = [(r-i, 2*r+1-2*i) for i in range(m+1)]
                survivors = [i for i, (q, k) in enumerate(terms_lawson) if q == 0 and k == 1]
                need(survivors == [r], 'independent_lawson_index_survivor')
                need(all(k < 0 or q > 0 or (q, k) == (0, 1) for q, k in terms_lawson), 'independent_lawson_exhaustive_cases')
                need((m-r, 1) in terms, 'independent_chow_lawson_alignment')
        for i in range(m+1):
            for j in range(m+1):
                exponent = (m-i)+j
                coefficient_of_top_class = int(exponent == m)
                need(coefficient_of_top_class == int(i == j), 'projector_polynomial_pushforward')

    relation_pairs = 0
    for n in (2, 3):
        rows = list(product((-1, 0, 1), repeat=n))
        for av in rows:
            a = [av]
            ka = nullspace(a, n)
            need(all(not any(apply(a, v)) for v in ka), 'independent_kernel_vectors')
            need(len(ka) == n-minor_rank(a), 'independent_kernel_dimension')
            for wv in rows:
                w = [wv]
                inclusion = all(not any(apply(w, v)) for v in ka)
                need(inclusion == (minor_rank(a+w) == minor_rank(a)), 'kernel_inclusion_iff_rowspace_inclusion')
                relation_pairs += 1
    for n in range(1, 7):
        for a_rank in range(n+1):
            a = [[int(j == i) for j in range(n)] for i in range(a_rank)]
            for w_rank in range(n+1):
                w = [[int(j == i) for j in range(n)] for i in range(w_rank)]
                inclusion = all(not any(apply(w, v)) for v in nullspace(a, n))
                need(inclusion == (w_rank <= a_rank), 'unequal_quotient_dimension_inclusion')
                if inclusion:
                    need(a_rank-w_rank == len(nullspace(w, n))-len(nullspace(a, n)), 'induced_quotient_kernel_dimension')

    boundary_cases = 0
    for h in range(7):
        for n in range(1, 9):
            for seed in range(7):
                a = [[((i+2)*(j+3)+seed*(2*i-j)) % 13-6 for i in range(n)] for j in range(h)]
                full = a + [[1]*n]
                # Integral column operations: retain column 0, subtract it
                # from all others. Then subtract a[j][0] times the degree row.
                transformed = [[row[0]]+[row[i]-row[0] for i in range(1,n)] for row in full]
                for j in range(h):
                    transformed[j] = [x-a[j][0]*y for x,y in zip(transformed[j], transformed[-1])]
                need(all(row[0] == 0 for row in transformed[:-1]), 'boundary_unimodular_degree_elimination')
                need(transformed[-1] == [1]+[0]*(n-1), 'boundary_unit_degree_block')
                differences = [row[1:] for row in transformed[:-1]]
                need(len(row_reduce(full)[1]) == 1+len(row_reduce(differences)[1]), 'boundary_rank_direct_sum')
                need(h+1-len(row_reduce(full)[1]) == h-len(row_reduce(differences)[1]), 'boundary_quotient_rank')
                boundary_cases += 1

    split_cases = 0
    for c in range(1, 7):
        for d in range(1, 5):
            for k in range(c+1):
                for seed in range(3):
                    section = [[((i+1)*(j+2)+seed) % 5-2 for j in range(d)] for i in range(c)]
                    for j in range(d):
                        s = [section[i][j] for i in range(c)]+[int(i == j) for i in range(d)]
                        need(s[c:] == [int(i == j) for i in range(d)], 'arbitrary_component_section')
                        reflected = s[:k]+s[c:]
                        need(reflected[k:] == s[c:], 'reflected_component_section')
                    # The canonical inclusion of the connected summand uses
                    # no entry of the chosen section.
                    for i in range(c):
                        image = [int(j == i) for j in range(k)]+[0]*d
                        need(not any(image[k:]), 'canonical_connected_inclusion')
                        need(image[:k] == [int(j == i) for j in range(k)], 'section_independent_connected_map')
                    split_cases += 1

    for n in range(1, 8):
        basis = [[int(i == j) for j in range(n)] for i in range(n)]
        for a in range(n+1):
            for j in range(n):
                original_rank = len(row_reduce(basis[:a])[1])
                enlarged_rank = len(row_reduce(basis[:a]+[basis[j]])[1])
                need(enlarged_rank-original_rank == int(j >= a), 'weight_zero_period_saturation_rank')
    return {'matrix_cases': matrix_cases, 'relation_map_pairs': relation_pairs,
            'boundary_cases': boundary_cases, 'arbitrary_split_cases': split_cases}


def mutate(base, kind):
    manifest_path = base/'AUTHOR_MANIFEST.json'
    if kind == 'payload_same_size':
        p = base/'README.md'; b = p.read_bytes(); p.write_bytes(b'!'+b[1:])
    elif kind == 'payload_appended':
        p = base/'README.md'; p.write_bytes(p.read_bytes()+b'\n')
    elif kind == 'missing_payload':
        (base/'README.md').unlink()
    elif kind == 'missing_manifest':
        manifest_path.unlink()
    elif kind == 'invalid_manifest_json':
        manifest_path.write_text('{')
    elif kind == 'unlisted_file':
        (base/'UNLISTED.txt').write_text('source-free corruption control\n')
    elif kind == 'false_control':
        p = base/'checks.py'
        s = p.read_text()
        if "require(1 != 0, 'literal_p1_component_mismatch')" not in s:
            raise AuditFailure('false-control mutation did not match')
        p.write_text(s.replace("require(1 != 0, 'literal_p1_component_mismatch')", "require(1 == 0, 'literal_p1_component_mismatch')"))
    else:
        m = json.loads(manifest_path.read_text())
        e = next(x for x in m['files'] if x['file'] == 'README.md')
        if kind == 'recorded_size_wrong':
            e['bytes'] += 1
        elif kind == 'recorded_digest_wrong':
            e['sha256'] = '0'*64
        elif kind == 'omitted_entry':
            m['files'].remove(e)
        elif kind == 'duplicated_entry':
            m['files'].append(dict(e))
        elif kind == 'coherently_rehashed_payload':
            p = base/'README.md'; p.write_bytes(p.read_bytes()+b'\n')
            e['bytes'] = p.stat().st_size; e['sha256'] = digest(p)
        else:
            raise AuditFailure('unknown corruption kind')
        manifest_path.write_text(json.dumps(m, indent=2)+'\n')


def run_child(packet, optimized, extra=None):
    args = [sys.executable] + (['-O'] if optimized else [])
    args += [str(packet/'checks.py'), '--verify-manifest'] if extra is None else ['-c', extra]
    proc = subprocess.run(args, capture_output=True, text=True, timeout=90)
    return {'returncode': proc.returncode,
            'manifest_pass_printed': 'Manifest integrity: PASS' in proc.stdout,
            'stdout_sha256': hashlib.sha256(proc.stdout.encode()).hexdigest(),
            'stderr_exception_type': proc.stderr.rstrip().splitlines()[-1].split(':', 1)[0] if proc.stderr else None}


def verifier_regressions(original, corrected):
    cases = ['valid', 'payload_same_size', 'payload_appended', 'recorded_size_wrong',
             'recorded_digest_wrong', 'missing_payload', 'missing_manifest',
             'invalid_manifest_json', 'unlisted_file', 'omitted_entry',
             'duplicated_entry', 'coherently_rehashed_payload', 'false_control']
    disabled = {'payload_same_size', 'payload_appended', 'recorded_size_wrong', 'recorded_digest_wrong'}
    unclaimed = {'unlisted_file', 'omitted_entry', 'duplicated_entry', 'coherently_rehashed_payload'}
    results = []
    with tempfile.TemporaryDirectory(prefix='motivic-audit-') as temp:
        for label, source, pin in [('original', original, ORIGINAL_PIN), ('corrected', corrected, CORRECTED_PIN)]:
            for case in cases:
                copy = Path(temp)/(label+'_'+case)
                shutil.copytree(source, copy)
                if case != 'valid':
                    mutate(copy, case)
                try:
                    strict_verify(copy, pin)
                    anchored_pass = True
                except (AuditFailure, OSError, ValueError, KeyError, TypeError):
                    anchored_pass = False
                need(anchored_pass == (case == 'valid'), 'externally_pinned_inventory_verifier')
                for optimized in (False, True):
                    result = run_child(copy, optimized)
                    expected_pass = case == 'valid' or case in unclaimed or (label == 'original' and optimized and case in disabled)
                    need((result['returncode'] == 0) == expected_pass, 'child_exit_expectation')
                    need(result['manifest_pass_printed'] == expected_pass, 'child_manifest_message_expectation')
                    if case == 'valid':
                        args = [sys.executable]+(['-O'] if optimized else [])+[str(copy/'checks.py')]
                        p = subprocess.run(args, capture_output=True, text=True, timeout=90)
                        need(p.returncode == 0, 'child_frozen_results_exit')
                        need(json.loads(p.stdout) == json.loads((source/'CHECK_RESULTS.json').read_text()), 'child_frozen_results_exact_equality')
                    results.append(dict(packet=label, case=case, child_optimized=optimized,
                                        expected_acceptance=expected_pass, anchored_acceptance=anchored_pass, **result))
            ragged = "import runpy; d=runpy.run_path("+repr(str(source/'checks.py'))+"); d['rank']([[1], [1,0]])"
            for optimized in (False, True):
                result = run_child(source, optimized, ragged)
                expected_pass = label == 'original' and optimized
                need((result['returncode'] == 0) == expected_pass, 'ragged_matrix_exception_expectation')
                results.append(dict(packet=label, case='ragged_matrix', child_optimized=optimized,
                                    expected_acceptance=expected_pass, **result))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--corrected-packet', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    original = args.packet.resolve(); corrected = args.corrected_packet.resolve()
    strict_verify(original, ORIGINAL_PIN)
    strict_verify(corrected, CORRECTED_PIN)
    before = {p.name:digest(p) for p in original.iterdir() if p.is_file()}
    exact = exact_controls(original)
    regressions = verifier_regressions(original, corrected)
    after = {p.name:digest(p) for p in original.iterdir() if p.is_file()}
    need(before == after, 'frozen_original_unchanged')
    result = {
        'schema_version': 1, 'problem_id': 30001288, 'status': 'PASS',
        'wrapper_optimization_level': sys.flags.optimize,
        'child_optimization_levels_explicitly_exercised': [0, 1],
        'original_manifest_sha256': ORIGINAL_PIN, 'corrected_manifest_sha256': CORRECTED_PIN,
        'scope': 'Exact finite algebra and executable verifier tests only; not a proof of motivic comparison.',
        'case_counts': exact, 'check_counts': dict(sorted(COUNTS.items())),
        'total_checks': sum(COUNTS.values()), 'verifier_regressions': regressions,
        'original_optimized_integrity_bypass_confirmed': True,
        'minimal_patch_rejects_all_claimed_payload_integrity_corruptions': True,
        'minimal_patch_does_not_claim_manifest_authentication_or_inventory_coverage': True,
        'externally_pinned_audit_verifier_rejected_every_corrupted_copy': True,
    }
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
