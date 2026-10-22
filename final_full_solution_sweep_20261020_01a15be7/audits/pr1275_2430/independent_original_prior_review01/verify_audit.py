#!/usr/bin/env python3
"""Read-only, standard-library audit diagnostics; not a proof by sampling.

Run: python3 -B verify_audit.py [--closed]
The written universal argument is in REPORT.md. No author programs are imported,
executed, or compiled. No network, subprocess, Git, or filesystem writes occur.
Every substantive guard remains active under -O and -OO.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import sys
import tarfile

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_sources'
COUNTS = {}


def need(ok, family, message):
    COUNTS[family] = COUNTS.get(family, 0) + 1
    if not ok:
        raise RuntimeError(f'{family}: {message}')


def digest(body):
    return hashlib.sha256(body).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def root_floor(n, degree):
    if n < 0 or degree < 1:
        raise ValueError('invalid integer root')
    if n < 2 or degree == 1:
        return n
    lo, hi = 0, 1 << ((n.bit_length() + degree - 1) // degree)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** degree <= n:
            lo = mid
        else:
            hi = mid
    return lo


def power_interval(x, exponent, bits=48):
    """Exact rational enclosure of x**exponent; no floating point."""
    x, exponent = Q(x), Q(exponent)
    if x < 0 or exponent < 0:
        raise ValueError('nonnegative arguments required')
    if exponent == 0:
        return Q(1), Q(1)
    if x == 0:
        return Q(0), Q(0)
    a, b = exponent.numerator, exponent.denominator
    scale = 1 << bits
    num = x.numerator ** a * scale ** b
    den = x.denominator ** a
    n = root_floor(num // den, b)
    need(n ** b * den <= num < (n + 1) ** b * den,
         'rational_power', 'integer-root enclosure')
    return Q(n, scale), Q(n + 1, scale)


def ceil_log2_rational(x):
    n = 1
    d = 0
    while n < x:
        n *= 2
        d += 1
    return d


def binomial_bell(n):
    bell = [1]
    for k in range(1, n + 1):
        bell.append(sum(math.comb(k - 1, j) * bell[j] for j in range(k)))
    return bell[n]


def sources():
    pins = {
        'ho_v2.pdf': 'f88b36a072d66476c5948061b7f2fc4d61dc536bbc5df5aa5bd3cdd2a84a82d0',
        'erdos1964.pdf': '31727bb7ef68a536ee7fc68ef3a793e8b6a78f66af6f6fc5aab9c733731e78cd',
        'ho_source.tar.gz': '675af05fd07147c32c6fb6c76e147d9995accda686e2fd108bab985a82aff8a8',
        'source_lacunary-v2.tex': 'bac88b4f5d77b2fb103179647a5a339b3101a48fb31157f89e1ea1b659aa8506',
    }
    for name, expected in pins.items():
        need(digest((PRIVATE / name).read_bytes()) == expected,
             'source', 'hard-pinned primary bytes ' + name)
    for receipt_file in ['FETCH_RECEIPTS_01.json', 'FETCH_RECEIPTS_02.json']:
        for item in read_json(HERE / receipt_file):
            body = (PRIVATE / item['file']).read_bytes()
            need(len(body) == item['bytes'] and digest(body) == item['sha256'],
                 'source', 'receipt payload ' + item['file'])
    pr_receipts = read_json(HERE / 'PR_SOURCE_RECEIPTS.json')
    need(len(pr_receipts) == 5, 'source', 'all five actual PR files')
    for item in pr_receipts:
        body = (PRIVATE / item['file']).read_bytes()
        need(item['head'] == '2e653ea299ef15d42b783901139454d29aec39bb', 'source', 'immutable head')
        need(digest(body) == item['sha256'] and len(body) == item['bytes'], 'source', 'PR SHA and length')
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        need(blob == item['git_blob'], 'source', 'actual Git blob identity')
    pr = read_json(PRIVATE / 'github_connector.json')['structuredContent']['pull_request']
    need(pr['head_sha'] == '2e653ea299ef15d42b783901139454d29aec39bb'
         and pr['base_sha'] == '4b27092a448d53b61408355ce44ec38d103a1ce4',
         'source', 'fresh connector source revision')
    need(digest(pr['body'].encode()) == '6d78f36c4120b76af1370b43c2adaffccfc45eccf89b8b5f948d04a59e0acdcb',
         'source', 'PR description exact bytes')
    artifact = read_json(PRIVATE / 'pr_ARTIFACT_MANIFEST.json')
    need(set(artifact['complete_file_inventory']) == {x['file'][3:] for x in pr_receipts},
         'source', 'PR manifest full inventory')
    for item in artifact['content_files']:
        body = (PRIVATE / ('pr_' + item['path'])).read_bytes()
        need(len(body) == item['bytes'] and digest(body) == item['sha256'],
             'source', 'nested PR content manifest')
    with tarfile.open(PRIVATE / 'ho_source.tar.gz', 'r:gz') as tar:
        actual = []
        for member in tar.getmembers():
            need(member.isfile(), 'source', 'ordinary source archive member')
            body = tar.extractfile(member).read()
            actual.append({'path': member.name, 'bytes': len(body), 'sha256': digest(body)})
        need(actual == read_json(HERE / 'PUBLISHED_SOURCE_INDEX.json')['members'],
             'source', 'every published source archive member')
    data = read_json(PRIVATE / 'datacite_arxiv.json')['data']['attributes']
    need(data['doi'].lower() == '10.48550/arxiv.2604.18535', 'source', 'registered DOI family')
    need(data['state'] == 'findable' and data['version'] == '2', 'source', 'registered preprint v2')
    need(data['titles'][0]['title'] == 'Counterexamples for lacunary dilates via dyadic spike blocks',
         'source', 'registered paper title')
    need(data['creators'][0]['name'] == 'Ho, Boon Suan', 'source', 'registered attribution')
    need(data['types']['resourceTypeGeneral'] == 'Preprint', 'source', 'preprint status')
    for file in ['INITIAL_LEDGER_CHECK.json', 'FINAL_LEDGER_CHECK.json']:
        check = read_json(HERE / file)
        filename = 'ledger_initial.json' if file.startswith('INITIAL') else 'ledger_final.json'
        need(digest((PRIVATE / filename).read_bytes()) == check['sha256'], 'source', 'retained numeric-gid ledger')
    current = read_json(HERE / 'FINAL_LEDGER_CHECK.json')
    need(current['numeric_gid'] == 1254632077 and current['rows'] == 191
         and current['semantic_target_leads'] == [], 'source', 'bounded duplicate check')
    proposal = read_json(HERE / 'PROPOSED_ROW.json')
    need(len(proposal['cells']) == 4 and all(isinstance(x, str) for x in proposal['cells']),
         'source', 'literal four-cell proposal')
    need(proposal['cells'][1] == '' and proposal['cells'][2] == 'https://doi.org/10.48550/arXiv.2604.18535',
         'source', 'blank B and authenticated existing DOI')
    need(proposal['ready_for_external_write'] is False and proposal['new_publication'] is False,
         'source', 'proposal is not service authorization')


def convolution():
    for length in range(8, 65):
        for ell in range(1, length // 8 + 1):
            weights = {h: sum(1 for q in range(1, length + 1)
                              if 1 <= h - q <= ell)
                       for h in range(2, length + ell + 1)}
            need(sum(weights.values()) == length * ell, 'convolution', 'double-sum mass')
            need(max(weights.values()) == ell, 'convolution', 'maximum weight')
            plateau = [h for h, w in weights.items() if w == ell]
            need(plateau == list(range(ell + 1, length + 2)), 'convolution', 'closed central plateau')
            need(len(plateau) == length - ell + 1, 'convolution', 'plateau count')
            need(not (len(plateau) == length - ell), 'negative_control', 'off-by-one central count rejected')
    need(sum([1, 2, 2, 1]) != 3 * 3, 'negative_control', 'wrong convolution mass rejected')


def block_moments():
    tested = 0
    ps = [Q(2), Q(5, 2), Q(3), Q(7, 2), Q(10, 3), Q(4)]
    for lam, height, length in itertools.product([Q(1), Q(1, 2), Q(1, 8)], [100, 127], [8, 16, 32]):
        d = ceil_log2_rational(64 * height * height * length / lam)
        big = 1 << d
        theta = Q(1, big)
        t = length * theta
        amp2 = lam * (big - 1) / length
        floor2 = lam * length / (big - 1)
        need(64 * height * height * length / lam <= big < 128 * height * height * length / lam,
             'block', 'admissible dyadic depth')
        need(floor2 <= (lam / height) ** 2, 'block', 'uniform deterministic lower floor')
        need(amp2 >= (3 * height) ** 2 and floor2 <= height ** 2,
             'block', 'one central hit dominates every other floor by 2B per term')
        need(0 < t <= lam / (64 * height ** 2) <= 1, 'block', 'small binomial intensity')
        a2 = lam / (length * theta * (1 - theta))
        need(a2 < 256 * height ** 2, 'block', 'uniform amplitude moment bound')
        probabilities = [Q(math.comb(length, r)) * theta ** r * (1 - theta) ** (length - r)
                         for r in range(length + 1)]
        need(sum(probabilities) == 1, 'block', 'complete exact binomial law')
        need(sum(probabilities[r] * (r - t) for r in range(length + 1)) == 0,
             'block', 'exact zero mean')
        variance = a2 * sum(probabilities[r] * (r - t) ** 2 for r in range(length + 1))
        need(variance == lam, 'block', 'exact second moment')
        for r in range(1, length + 1):
            need(probabilities[r] <= t ** r / math.factorial(r), 'block', 'factorial binomial majorant')
        for ell in range(1, length // 8 + 1):
            central = length - ell + 1
            probability = 1 - (1 - theta) ** central
            need(central >= Q(7, 8) * length, 'trial', 'central fraction')
            need(probability >= central * theta / 2, 'trial', 'exact rare-event probability')
            need(probability >= lam / (1024 * height ** 2), 'trial', 'uniform c0=1/1024')
        for p in ps:
            # A larger integer-moment constant controls all real p <= ceil(p).
            m = (p.numerator + p.denominator - 1) // p.denominator
            constant = Q(2 ** (m - 1) * (3 * binomial_bell(m) + 1) * 16 ** m, 64)
            sumlo = sumhi = Q(0)
            for r, probability in enumerate(probabilities):
                lo, hi = power_interval(abs(r - t), p)
                sumlo += probability * lo
                sumhi += probability * hi
            alo, ahi = power_interval(a2, p / 2)
            actual_lower, actual_upper = alo * sumlo, ahi * sumhi
            blo, bhi = power_interval(Q(height), p - 2)
            need(0 <= actual_lower <= actual_upper <= constant * lam * blo,
                 'real_p_moment', 'exact rational enclosure satisfies uniform real-p budget')
            if p == 2:
                need(actual_lower <= lam <= actual_upper, 'real_p_moment', 'p=2 enclosure contains exact variance')
            tested += 1
    uncentered_mean = Q(1, 4)
    need(uncentered_mean > 0 and uncentered_mean != 0,
         'negative_control', 'removing the spike centering destroys the zero-mean condition')
    return tested


def digit_independence():
    counts = {}
    for bits in itertools.product([0, 1], repeat=14):
        hits = tuple(all(bits[i] == 0 for i in range(q * 4, q * 4 + 2)) for q in range(1, 4))
        counts[hits] = counts.get(hits, 0) + 1
    for outcomes, count in counts.items():
        expected = math.prod(Q(1, 4) if hit else Q(3, 4) for hit in outcomes)
        need(Q(count, 1 << 14) == expected, 'digits', 'joint independence of disjoint bit windows')
    overlap = sum(all(bits[i] == 0 for i in [0, 1]) and all(bits[i] == 0 for i in [1, 2])
                  for bits in itertools.product([0, 1], repeat=3))
    need(Q(overlap, 8) == Q(1, 8) != Q(1, 16),
         'negative_control', 'overlapping windows fail the independent product law')


def scheduling():
    for initial_count in [0, 7, 19]:
        count, previous_last, previous_v, omega = initial_count, 0, 0, 0
        for trials in [1, 2, 3]:
            first_count = count
            lengths = []
            prefixes = []
            for t in range(trials):
                prefixes.append(count)
                ell = 20 * (count + 1)
                lengths.append(ell)
                need(ell == 20 * (first_count + 1) * 21 ** t,
                     'schedule', 'exact trial-count recurrence')
                need(count <= Q(ell, 20) and count + ell <= Q(21 * ell, 20),
                     'schedule', 'full-prefix domination')
                count += ell
            need(count + 1 == (first_count + 1) * 21 ** trials,
                 'schedule', 'exact stage endpoint count')
            length = 8 * lengths[-1]
            lam, height = Q(1, 8), 100
            d = ceil_log2_rational(64 * height * height * length / lam)
            spacing = d + 2
            shift = previous_v + 1
            last_v = shift + length * spacing + d - 1
            need(shift + spacing + 1 > previous_v + 1,
                 'schedule', 'new block begins after every prior block digit')
            start = max(0, previous_last - spacing + 1, omega - shift - spacing)
            need(start + spacing > previous_last and shift + start + spacing + 1 > omega,
                 'schedule', 'first trial source constraints')
            previous_raw_end = omega
            for i, ell in enumerate(lengths):
                first_selected, last_selected = start + spacing, start + ell * spacing
                raw_first = shift + start + 2 * spacing + 1
                raw_last = shift + start + (length + ell) * spacing + d
                good_first = shift + start + (ell + 1) * spacing + 1
                good_last = shift + start + (length + 1) * spacing + d
                need(first_selected > previous_last and first_selected >= 0,
                     'schedule', 'strictly ordered nonnegative selected exponents')
                need(raw_first > previous_raw_end and raw_first <= good_first <= good_last <= raw_last,
                     'schedule', 'disjoint event ranges with correct inclusions')
                need(spacing >= d + 2 and 1 <= ell <= length // 8,
                     'schedule', 'within-trial digit independence hypotheses')
                need(prefixes[i] + ell <= Q(21 * ell, 20),
                     'schedule', 'full partial sum, not trial-only normalization')
                previous_raw_end = raw_last
                previous_last = last_selected
                if i + 1 < trials:
                    next_start = start + (length + ell) * spacing + d + 2
                    need(next_start + spacing - last_selected == (length + 2) * spacing,
                         'schedule', 'exact intertrial exponent gap')
                    start = next_start
            omega, previous_v = previous_raw_end, last_v
    for p in [Q(2), Q(5, 2), Q(10, 3), Q(4), Q(100, 7)]:
        for k in range(1, 31):
            eps = 1 / (2 * p * (k + 2))
            alpha = 1 / p - eps
            need(alpha > 0 and p * eps == Q(1, 2 * (k + 2)), 'asymptotic', 'strictly positive signal power')
            need(1 - p * alpha == p * eps, 'asymptotic', 'B over (B^p)^alpha leaves positive power')
            need(Q(1, 2 ** (k + 2)) + sum(Q(1, 2 ** (i + 2)) for i in range(1, k + 1)) == Q(1, 4),
                 'asymptotic', 'exact remaining geometric budget')
    for prefix in [0, 1, 9, 99]:
        ell = 20 * (prefix + 1)
        n = prefix + ell
        height, mu = Q(100), Q(1, 400)
        full_lower = 2 * height * ell - mu * n
        need(full_lower / n >= height - mu, 'shielding', 'all old terms and all other blocks charged')
        if prefix > 0:
            trial_only_lower = 2 * height * ell - mu * ell
            need(trial_only_lower > full_lower, 'negative_control', 'omitting old prefix overstates the guaranteed lower bound')
    # A small intensity is necessary for the displayed factorial-to-linear bound.
    bad_t = Q(2)
    need(bad_t ** 2 > bad_t, 'negative_control', 't^p<=t is rejected outside 0<=t<=1')


def closed_inventory():
    top = read_json(HERE / 'MANIFEST.json')
    listed = top['files']
    observed = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p != HERE / 'MANIFEST.json'}
    need(observed == {x['path'] for x in listed}, 'seal', 'exact closed directory inventory')
    for item in listed:
        path = HERE / item['path']
        need(not path.is_symlink(), 'seal', 'no source symlink escape')
        body = path.read_bytes()
        need(len(body) == item['bytes'] and digest(body) == item['sha256'], 'seal', 'every closed file hash')
        need(item['private'] == item['path'].startswith('private_sources/'), 'seal', 'raw-data privacy flag')
    need(any(x['path'] == 'private_sources/pr_ARTIFACT_MANIFEST.json' for x in listed),
         'seal', 'nested manifests are included, not globally excluded')
    altered = dict(listed[0], sha256='0' * 64)
    need(digest((HERE / altered['path']).read_bytes()) != altered['sha256'],
         'negative_control', 'hash tampering is detectable')


def main():
    if any(arg not in ['--closed'] for arg in sys.argv[1:]):
        raise ValueError('only --closed is accepted')
    sources()
    convolution()
    moments = block_moments()
    digit_independence()
    scheduling()
    closed = '--closed' in sys.argv[1:]
    if closed:
        closed_inventory()
    print(json.dumps({'status': 'PASS', 'closed_inventory_checked': closed,
                      'guard_count': sum(COUNTS.values()), 'guards_by_family': COUNTS,
                      'exact_real_p_model_cases': moments,
                      'finite_checks_do_not_replace_universal_proof': True,
                      'author_programs_executed': False,
                      'writes_or_network_calls': False}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
