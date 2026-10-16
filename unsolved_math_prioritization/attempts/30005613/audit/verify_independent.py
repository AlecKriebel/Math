#!/usr/bin/env python3
"""Independent exact finite checks; no PDE solver or formal proof certificate.

Optional external inputs are read only. They are never copied into the output.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile


def digest(b):
    return hashlib.sha256(b).hexdigest()


counts = Counter()


def require(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] += 1


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def diag(values):
    return [[Q(x) if i == j else Q(0) for j in range(len(values))]
            for i, x in enumerate(values)]


def transpose(a):
    return [list(c) for c in zip(*a)]


def matmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def transform(u, a):
    return matmul(matmul(u, a), transpose(u))


def subtract(a, b):
    return [[x-y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def frobenius2(a):
    return sum((x*x for row in a for x in row), Q(0))


def finite_diagnostics():
    # The exact finite sum plus remainder validates the constants, not an
    # infinite-dimensional convergence claim.
    for n in range(1, 65):
        tail = Q(1, 2**(n+1))
        require('tail_below_rank_threshold', tail < 1)
        require('birth_plus_future_error', Q(1, 2**n)+tail == 3*tail)
        for m in range(n+1, n+13):
            partial = sum((Q(1, 2**(j+2)) for j in range(n, m)), Q(0))
            require('exact_tail_remainder', partial+Q(1, 2**(m+1)) == tail)
    for j in range(1, 25):
        for ell in range(1, 25):
            birth = max(j, ell)
            require('test_enters', j <= birth and ell <= birth)
            require('test_stays', j <= birth+17 and ell <= birth+17)

    # Independent dynamic-programming enumeration of exactly the sums that
    # could cause a resonance in the tested interval 2<a<3.
    protected = (Q(1, 2), Q(5, 4), Q(3), Q(11, 7))
    max_sum = 108
    attainable = {0}
    examples = []
    for d in range(1, 8):
        attainable = {s+m*m for s in attainable for m in range(1, 11)
                      if s+m*m <= max_sum}
        require('multiindex_bound', 11*11 > 4*3*3*max(protected))
        if d < 2:
            continue
        candidates = [Q(2)+Q(k, 37) for k in range(1, 37)]
        valid = [a for a in candidates
                 if all(Q(s, 4) != lam*a*a
                        for s in attainable for lam in protected)]
        require('nonresonant_candidate_exists', bool(valid))
        a = valid[0]
        require('candidate_in_open_interval', 2 < a < 3)
        for s in attainable:
            require('all_possible_resonances_excluded',
                    all(Q(s, 4) != lam*a*a for lam in protected))
        examples.append({'dimension': d, 'half_width': str(a),
                         'possible_integer_sums': len(attainable)})

    # Finite geometric sanity checks are independent of spectral estimates.
    widths = [Q(1)+Q(3*n, 2) for n in range(20)]
    centers = [Q(1)]
    for n in range(19):
        centers.append(centers[-1]+widths[n]+widths[n+1])
        require('cube_growth', widths[n]+1 < widths[n+1] < widths[n]+2)
        p = centers[n]+widths[n]
        require('adjacent_faces', p == centers[n+1]-widths[n+1])
        delta = Q(1, 2**(n+3))
        require('positive_window_bound', 0 < delta < min(widths[n]/2, Q(1, 2**(n+1))))
        require('window_left_half_inside_old_cube', centers[n]-widths[n] < p-delta < p)
        require('window_right_half_inside_new_cube', p < p+delta < centers[n+1]+widths[n+1])

    # Five two-dimensional births. Each new pair is a full degenerate
    # spectral block; old pairs can split. Several small rational rotations
    # couple old coordinates to the newly introduced pair.
    N = 10
    u = eye(N)
    previous = {}
    for n in range(1, 6):
        if n > 1:
            for j in range(2*n-2):
                t = Q(1, 2**(n+11+j))
                c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
                v = eye(N)
                target = 2*n-2+(j % 2)
                v[j][j] = v[target][target] = c
                v[j][target], v[target][j] = -s, s
                require('rational_rotation', c*c+s*s == 1)
                u = matmul(u, v)
        require('orthogonality', matmul(transpose(u), u) == eye(N))
        eigenvalues = []
        for j in range(N):
            if j >= 2*n:
                mu = Q(0)
            else:
                base = Q(1, j//2+2)
                offset = Q((-1)**j, 2**(n+10)) if j < 2*n-2 else Q(0)
                mu = base+offset
                require('positive_contraction_eigenvalue', 0 < mu <= 1)
            eigenvalues.append(mu)
        r = transform(u, diag(eigenvalues))
        require('resolvent_model_selfadjoint', r == transpose(r))
        current = {}
        for k in range(1, n+1):
            p = transform(u, diag([int(j < 2*k) for j in range(N)]))
            current[k] = p
            require('projection_selfadjoint', p == transpose(p))
            require('projection_idempotent', matmul(p, p) == p)
            require('projection_rank', sum(p[j][j] for j in range(N)) == 2*k)
            require('exact_commutation', matmul(p, r) == matmul(r, p))
            if k > 1:
                require('nested_ranges', matmul(current[k-1], p) == current[k-1])
            if k < n:
                eps = Q(1, 2**((n-1)+2))
                require('transport_operator_norm_upper_bound',
                        frobenius2(subtract(p, previous[k])) < eps*eps)
        require('birth_tests_exactly_captured',
                current[n] == diag([int(j < 2*n) for j in range(N)]))
        previous = current

    # Resonance/multiplicity failure witness: an individual spectral
    # projection need not approach a selected old coordinate projection.
    old = diag([1, 0])
    plus = [[Q(1, 2), Q(1, 2)], [Q(1, 2), Q(1, 2)]]
    minus = subtract(eye(2), plus)
    distance = subtract(plus, old)
    require('rank_one_drift_squared', matmul(distance, distance) == diag([Q(1, 2)]*2))
    for m in range(1, 33):
        t = Q(1, 2**m)
        b = [[Q(1), t], [t, Q(1)]]
        require('split_plus_cluster', matmul(b, plus) == [[(1+t)*x for x in row] for row in plus])
        require('split_minus_cluster', matmul(b, minus) == [[(1-t)*x for x in row] for row in minus])
        require('whole_space_remains_protected', matmul(eye(2), b) == b)
    return examples


def author_checks(directory, archive):
    directory = Path(directory)
    manifest = json.loads((directory/'MANIFEST.json').read_text())
    require('author_manifest_identity', digest((directory/'MANIFEST.json').read_bytes()) ==
            '4ae99f0866dc70b2a60fd88707bb20acf5be845be4c7af4d635ac3b62b9349ff')
    for entry in manifest['files']:
        b = (directory/entry['path']).read_bytes()
        require('author_file_size', len(b) == entry['bytes'])
        require('author_file_hash', digest(b) == entry['sha256'])
    out = subprocess.check_output([sys.executable, str(directory/'verify.py')])
    frozen = (directory/'verification.json').read_bytes()
    require('author_output_byte_reproduction', out == frozen)
    require('author_assertion_count', json.loads(out)['assertions'] == 4187)
    result = {'manifest_sha256': digest((directory/'MANIFEST.json').read_bytes()),
              'all_manifest_files_match': True, 'author_assertions': 4187,
              'output_byte_reproduced': True,
              'proof_sha256': digest((directory/'PROOF.md').read_bytes())}
    if archive:
        archive = Path(archive)
        b = archive.read_bytes()
        require('author_archive_size', len(b) == 16490)
        require('author_archive_hash', digest(b) ==
                '2d15c0f1f7b094c92bafb6d2fed6d3b212c597adf9043c9f49c737a6f082e09e')
        with zipfile.ZipFile(archive) as z:
            require('author_archive_crc', z.testzip() is None)
            require('author_archive_entry_set', set(z.namelist()) ==
                    {x['path'] for x in manifest['files']} | {'MANIFEST.json'})
            for name in z.namelist():
                require('author_archive_entry_bytes', z.read(name) == (directory/name).read_bytes())
        result['archive'] = {'bytes': len(b), 'sha256': digest(b)}
    return result


DATASETS = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}


def corpus_checks(args):
    loaded = {}
    metadata = {}
    for name, (size, sha) in DATASETS.items():
        b = Path(getattr(args, name)).read_bytes()
        require('full_corpus_size', len(b) == size)
        require('full_corpus_hash', digest(b) == sha)
        loaded[name] = json.loads(b)
        metadata[name+'.json'] = {'bytes': len(b), 'sha256': digest(b),
                                 'top_level_records': len(loaded[name])}
    matches = [p for p in loaded['problems'] if str(p.get('id')) == '30005613']
    descriptors = [p for p in loaded['catalog'] if str(p.get('id')) == '30005613']
    require('unique_problem_id', len(matches) == 1)
    require('unique_catalog_id', len(descriptors) == 1)
    p, c = matches[0], descriptors[0]
    require('unique_problem_code', sum(x.get('problem_number') == p['problem_number']
                                    for x in loaded['problems']) == 1)
    require('code_identity', p['problem_number'] == c['problem_number'] == 'OWR-14297736-021')
    require('catalog_rank', c['rank'] == 800)
    reports = loaded['research_results']
    require('no_matching_report_key', p['problem_number'] not in reports)
    statement = p['statement'].encode('utf-8')
    require('statement_bytes', len(statement) == 198)
    require('statement_hash', digest(statement) == c['statement_hash'] ==
            '783db58de5f1183fa9abd1cbacee659b6029b8d4ab61dd04b0fb47fb986d9ea2')
    review = digest(json.dumps([p, {}], sort_keys=True).encode())
    require('review_hash', review == c['review_hash'] ==
            '6e61514d4909027d8a16bfdf209631bea89c9bee55339e5091c5f485cb756a69')
    return {'datasets': metadata, 'statement_bytes': len(statement),
            'statement_sha256': digest(statement), 'review_sha256': review,
            'review_hash_algorithm': 'SHA256(json.dumps([problem, empty_report], sort_keys=True).encode())',
            'unique_numeric_id_and_problem_code': True, 'research_result_match': False}


def source_pdf_checks(directory):
    expected = {
        'paper.pdf': (194167, '32081b2bf77ed26dd3ed2d05538f0a6e6b836159f1db9628d5778d47352d90ac'),
        'survey.pdf': (2413179, 'd9d296eec2dcebc5b5cb7ce97257f4efb0ab3203f1265dc317be05f804899d30'),
        'report.pdf': (1182028, '2d209e9c46fdf6fd1d80a8acff5ea86c7bedab5b5fdc01fdd4b856a3fbe06d62'),
    }
    result = {}
    for name, (size, sha) in expected.items():
        b = (Path(directory)/name).read_bytes()
        require('source_pdf_size', len(b) == size)
        require('source_pdf_hash', digest(b) == sha)
        result[name] = {'bytes': len(b), 'sha256': digest(b)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, default=Path(__file__).resolve().parent/'author')
    parser.add_argument('--author-zip', type=Path)
    for name in DATASETS:
        parser.add_argument('--'+name.replace('_', '-'), dest=name, type=Path)
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    if any(getattr(args, n) for n in DATASETS) and not all(getattr(args, n) for n in DATASETS):
        parser.error('Full-corpus mode requires all three dataset paths.')
    examples = finite_diagnostics()
    author = author_checks(args.author_dir, args.author_zip)
    result = {'status': 'PASS', 'arithmetic': 'exact Python Fraction arithmetic',
              'author': author, 'nonresonant_examples': examples}
    if args.catalog:
        result['corpora'] = corpus_checks(args)
    if args.source_dir:
        result['source_pdfs'] = source_pdf_checks(args.source_dir)
    result['assertions'] = sum(counts.values())
    result['groups'] = dict(sorted(counts.items()))
    result['scope'] = 'Finite diagnostics and integrity checks; analytic proof independently reviewed in AUDIT.md and ANALYTIC_CHECKS.md.'
    result['not_verified_by_code'] = [
        'Mosco convergence or operator norm convergence for actual domains',
        'the infinite-dimensional pure point theorem',
        'numerical apertures or an effective spectral gap',
        'historical priority or completeness of literature searches']
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
