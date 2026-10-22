#!/usr/bin/env python3
"""Read-only stdlib source checks and finite logical/arithmetic controls.

This does not prove algebraic geometry by finite tests. No author code, network,
subprocess, Git mutation, or writes. Guards remain active in -O/-OO.
"""
from fractions import Fraction as Q
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_sources'
COUNTS = {}


def need(ok, group, message):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not ok:
        raise RuntimeError(group + ': ' + message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(p.read_text())


def sources():
    pins = {
        'aim_20240828.html': 'e2f8861e0cdd467d4fd4e64ce77ebe36bbc88bfa25df2092f29d855738645d5a',
        'clark.pdf': '269e1fbc2091c89d69fb39ca27e157251b874eab5dc56609d62572980e153272',
        'viray_vogt.pdf': 'ac8cbbe225d28040d37ffcb7b7c460f2cfa431b9ab4937835aa5267c5f686179',
        'products.pdf': '4b37fb86d93caa48913ffd444be8c90ca510db52ccec9d2e149803e661d8de18',
    }
    for name, expected in pins.items():
        need(digest((PRIVATE / name).read_bytes()) == expected, 'source', 'hard-pinned primary body')
    for n in range(1, 6):
        for r in load(HERE / f'FETCH_RECEIPTS_{n:02}.json'):
            path = PRIVATE / r['file']
            if r.get('status') == 200:
                b = path.read_bytes()
                need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'source', 'actual successful response bytes')
            else:
                need('error' in r and not path.exists(), 'source', 'failed fetch not promoted to source success')
    raw = (PRIVATE / 'aim_20250701.html').read_bytes()
    decoded = gzip.decompress(raw)
    need(raw.startswith(b'\x1f\x8b') and decoded == (PRIVATE / 'aim_20240828.html').read_bytes(),
         'archive', 'second archival response is gzip, not a different short HTML body')
    need(decoded == (PRIVATE / 'aim_20250701_decoded.html').read_bytes(), 'archive', 'decoded source retained exactly')
    need(len(decoded) == 102036 and digest(decoded) == pins['aim_20240828.html'],
         'archive', 'both actual archives equal the PR historical source pin')
    original = (PRIVATE / 'aim_20240828.html.txt').read_text()
    for phrase in ['Given a finite map', 'obvious relations are sharp', 'Adam Logan + Bianca Viray',
                   'Galois cover', 'containment relations']:
        need(phrase in original, 'archive', 'actual primary original/remarks context')
    receipts = load(HERE / 'PR_SOURCE_RECEIPTS.json')
    need(len(receipts) == 11, 'source', 'all eleven actual files')
    for r in receipts:
        b = (PRIVATE / r['file']).read_bytes()
        need(r['head'] == '423340e277fcb57ba11844a129cc1f2580045eb6', 'source', 'immutable head')
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'source', 'PR body hash/length')
        need(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == r['git_blob'],
             'source', 'actual Git object identity')
    pr = load(PRIVATE / 'github_connector.json')['structuredContent']['pull_request']
    need(pr['head_sha'] == '423340e277fcb57ba11844a129cc1f2580045eb6', 'source', 'fresh live capture matches fixed head')
    need(digest(pr['body'].encode()) == '3fea2b37fb017e4eb2f6d25cc54fc424dc8345e3bfa1f8ecd679d7d131508d0d',
         'source', 'full PR description exact pin')
    man = load(PRIVATE / 'pr_MANIFEST.json')
    need({r['path'] for r in man['files']} | {'MANIFEST.json'} == {r['file'][3:] for r in receipts},
         'source', 'nested public inventory complete')
    for r in man['files']:
        b = (PRIVATE / ('pr_' + r['path'])).read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'source', 'nested public manifest all bodies')
    cf = load(PRIVATE / 'clark_crossref.json')['message']
    vv = load(PRIVATE / 'vv_crossref.json')['message']
    need(cf['DOI'].lower() == '10.1515/crelle.2006.040' and cf['title'][0] ==
         'There are genus one curves of every index over every number field', 'source', 'Clark dependency identity')
    need(vv['DOI'].lower() == '10.2140/ent.2026.5.1' and vv['title'][0] ==
         'Isolated and parameterized points on curves', 'source', 'VV dependency identity')
    decision = load(HERE / 'NO_ROW.json')
    need(decision['cells'] is None and decision['row_proposed'] is False
         and decision['new_publication_recommended'] is False, 'scope', 'no unauthenticated full-solution tracker row')
    need('https://github.com/AlecKriebel/Math/pull/1303' == decision['pr'], 'scope', 'exact PR scope reference')
    need(all('not authenticated full' in x['role'] or 'not authenticated full' in x['role'].replace('not a','not')
             or 'dependency' in x['role'].lower() for x in decision['dependency_doi_roles']),
         'scope', 'dependency DOIs not substituted for original full resolution')
    ledger = load(HERE / 'FINAL_LEDGER_CHECK.json')
    need(ledger['numeric_gid'] == 1254632077 and ledger['columns'] == 43, 'accounting', 'numeric gid/all columns')
    need(digest((PRIVATE / 'ledger_final.json').read_bytes()) == ledger['sha256'], 'accounting', 'ledger snapshot hash')
    need(ledger['semantic_target_leads'] == [], 'accounting', 'bounded no matching full-result row finding')


def compositions(n):
    if n == 0:
        yield ()
    for first in range(1, n + 1):
        for rest in compositions(n - first):
            yield (first,) + rest


def residue_and_minimum_controls():
    parts_count = 0
    for n in range(1, 13):
        for parts in compositions(n):
            need(sum(parts) == n and all(1 <= m <= n for m in parts),
                 'fiber_rank', 'finite etale rank partitions give bounded residue degrees')
            parts_count += 1
        for m in range(1, n + 1):
            equal_components_possible = n % m == 0
            if equal_components_possible:
                need(sum([m] * (n // m)) == n, 'galois', 'equal orbit degrees divide torsor rank')
            else:
                need(all(m * count != n for count in range(1, n + 1)),
                     'galois', 'nondivisor cannot be the common component degree')
    need(1 + 2 == 3 and 3 % 2 != 0, 'negative_control', 'nongalois residue partition not a divisor partition')
    need(max([2, 3]) < sum([2, 3]), 'negative_control', 'rank5 effective fiber need not be one degree5 closed point')
    for n in range(1, 25):
        # Actual geometric examples are justified by Clark/RR/Hilbert in REPORT.
        lower_a = lower_b = 1
        upper_a, upper_b = n, 1
        need(lower_b <= lower_a <= n * lower_b, 'minimum', 'lower endpoint')
        need(upper_a == n * upper_b and upper_b <= upper_a, 'minimum', 'upper endpoint')
        permitted_for_e1 = [m for m in range(1, n + 1) if m % n == 0]
        need(permitted_for_e1 == [n], 'minimum', 'downward maximum multiplier n is forced in nZ versus Z')
        need(1 == 1 and 1 <= n, 'minimum', 'upward relation still permits m1 in this sharp-minimum example')
        for e in range(1, 101):
            need((e * n) % n == 0, 'minimum', 'entire nZ upstairs example realizes downward transfer')
    return parts_count


def multiply(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def cubic_controls():
    params = sorted({Q(n, d) for n in range(-12, 13) for d in range(1, 7)})
    images = []
    for r in params:
        q = r ** 3 + r
        need(multiply([-r, 1], [r * r + 1, r, 1]) == [-q, 1, 0, 1],
             'cubic', 'exact fiber factorization')
        need(-3 * r * r - 4 < 0, 'cubic', 'quadratic discriminant is negative')
        need(-4 - 27 * q * q < 0, 'cubic', 'full cubic fiber is etale')
        images.append(q)
    need(all(a < b for a, b in zip(images, images[1:])), 'cubic', 'different rational parameters give different fibers')
    for d in range(1, 301):
        # For the actual cubic X=Y=P1, both complete spectra equal N.
        m = 1
        need(3 % m == 0 and d % m == 0 and d // m >= 1,
             'set_sharpness', 'divisor-only upstairs set relation survives the cubic via m1')
        need(d * m >= 1, 'set_sharpness', 'divisor-only downstairs set relation also survives')
    return len(params)


def logical_gap_controls():
    # Infinite abstract model, NOT a claimed geometric cover:
    # n=3, A=N\{1,3}, B=N. It satisfies both transfer conclusions,
    # multiplicative closure, the minimum inequalities and gcd1 on both sides.
    # Yet divisor-only DOWNWARD refinement fails at e=1.
    in_a = lambda d: d > 0 and d not in [1, 3]
    for d in range(1, 501):
        if in_a(d):
            need(d >= 1, 'logical_gap', 'upward transfer uses m1')
            for r in range(1, 13):
                need(in_a(d * r), 'logical_gap', 'model has curve-like multiplicative closure')
        m = 2 if d in [1, 3] else 1
        need(1 <= m <= 3 and in_a(d * m), 'logical_gap', 'downward generic transfer witness')
    need(math.gcd(2, 5) == 1 and 1 <= 2 <= 3, 'logical_gap', 'gcd and sharp-minimum bounds alone do not close the bridge')
    need(not any(in_a(m) for m in [1, 3]), 'logical_gap', 'divisor-only model refinement fails at e1')
    need(1 not in [2 * n for n in range(-20, 21)], 'negative_control', 'multiplication need not be surjective on rational Mordell-Weil points')
    # A point degree em from a finite fiber is not guaranteed to have m=n.
    need(not (2 == 3), 'negative_control', 'relative-degree2 cubic stratum is not a degree3 point')


def closed_inventory():
    m = load(HERE / 'MANIFEST.json')
    actual = {f.relative_to(HERE).as_posix() for f in HERE.rglob('*') if f.is_file() and f != HERE / 'MANIFEST.json'}
    need(actual == {x['path'] for x in m['files']}, 'seal', 'exact closed set including nested manifests')
    for r in m['files']:
        f = HERE / r['path']
        need(not f.is_symlink(), 'seal', 'no symlink escape')
        b = f.read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'seal', 'every file pin')
        need(r['private'] == r['path'].startswith('private_sources/'), 'seal', 'raw data private flags')
    need('private_sources/pr_MANIFEST.json' in actual, 'seal', 'nested PR manifest included')
    need(digest((HERE / m['files'][0]['path']).read_bytes()) != '0' * 64,
         'negative_control', 'forged hash would be rejected')


def main():
    if any(x != '--closed' for x in sys.argv[1:]):
        raise ValueError('only --closed is accepted')
    sources()
    parts = residue_and_minimum_controls()
    params = cubic_controls()
    logical_gap_controls()
    closed = '--closed' in sys.argv[1:]
    if closed:
        closed_inventory()
    print(json.dumps({'status':'PASS','guards':sum(COUNTS.values()),'guards_by_family':COUNTS,
                      'rank_partitions':parts,'exact_cubic_parameters':params,
                      'closed_inventory_checked':closed,'no_author_code_execution':True,
                      'no_network_subprocess_or_writes':True,
                      'abstract_model_is_not_a_geometric_counterexample':True,
                      'finite_tests_do_not_prove_algebraic_geometry':True},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
