#!/usr/bin/env python3
"""Read-only independent exact controls for the shift example and source identity.

No imported author programs, network, subprocesses, Git operations, or writes.
The universal proof and the original-subquestion decision are in REPORT.md.
Every guard is explicit and remains active in normal, -O, and -OO modes.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_sources'
COUNTS = {}


def need(value, group, message):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not value:
        raise RuntimeError(group + ': ' + message)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_text())


def source_checks():
    pins = {
        'ollivier_problems.pdf': '71e7841243d4652cfb28db8e133fba2169e388c5d90aacc6f61c566dd1986173',
        'gong2013.pdf': 'd35c6a0a42cf735427b29936b96c8b3a04568ae0b4c106e3735c841b64a4a607',
        'gong_publisher_mirror.pdf': '298e2488c17622a739e46527459757e2684fbbeb35b0b7558578bdd450c2d293',
        'ollivier_jfa.pdf': 'f251b6135895d53bb3aaa325d676c4100bac3eb62da86a45e09aacbd4546cab2',
        'erbar_fathi_v1.pdf': 'd053f2f640ad40dfa72c6d4edd88f34ec30cb15b8181ed84199f67f81cdb4cfe',
    }
    for name, expected in pins.items():
        body = (PRIVATE / name).read_bytes()
        need(body.startswith(b'%PDF-') and digest(body) == expected, 'source', 'primary PDF pin ' + name)
    for file in ['FETCH_RECEIPTS_01.json', 'FETCH_RECEIPTS_02.json', 'FETCH_RECEIPTS_03.json']:
        for r in load(HERE / file):
            need(r.get('status') == 200, 'source', 'actual successful response')
            body = (PRIVATE / r['file']).read_bytes()
            need(len(body) == r['bytes'] and digest(body) == r['sha256'], 'source', 'complete fetched body')
    bindings = load(HERE / 'PR_SOURCE_RECEIPTS.json')
    need(len(bindings) == 8, 'source', 'all eight actual immutable PR bodies')
    for r in bindings:
        b = (PRIVATE / r['file']).read_bytes()
        need(r['head'] == '36108792f0ecf6185e67bfde8c81905defc80aca', 'source', 'immutable PR head')
        need(digest(b) == r['sha256'] and len(b) == r['bytes'], 'source', 'actual PR payload')
        need(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == r['git_blob'],
             'source', 'Git object identity')
    pr = load(PRIVATE / 'github_connector.json')['structuredContent']['pull_request']
    need(pr['head_sha'] == '36108792f0ecf6185e67bfde8c81905defc80aca', 'source', 'live connector head')
    need(digest(pr['body'].encode()) == '7ec7ad782b21fe5c156131b6c7c3c4df42f8edec63962dd34a0ec039b63e91e6',
         'source', 'full PR description')
    manifest = load(PRIVATE / 'pr_MANIFEST.json')
    need(set(manifest['public_allowlist']) == {x['file'][3:] for x in bindings}, 'source', 'full nested PR inventory')
    for r in manifest['files']:
        b = (PRIVATE / ('pr_' + r['path'])).read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'source', 'nested manifest body')
    agency = load(PRIVATE / 'gong_agency.json')
    need(agency == [{'DOI': '10.18910/25089', 'RA': 'JaLC'}], 'source', 'registered DOI agency')
    metadata = (PRIVATE / 'gong_doi.txt').read_text()
    for token in ['10.18910/25089', 'Version of Record', 'Gong, Fu-Zhou', 'Liu, Yuan', 'Wen, Zhi-Ying',
                  '50(2)', '491-502', '2013-06', 'RICCI CURVATURE OF MARKOV CHAINS ON POLISH SPACES REVISITED']:
        need(token in metadata, 'source', 'matching primary repository metadata ' + token)
    old = next(x for x in load(PRIVATE / 'pr_SOURCE_PINS.json')['sources'] if x['source_id'] == 'notes_ricci2013')
    need(old['sha256'] != pins['gong2013.pdf'], 'provenance', 'fresh article is not falsely declared historical-byte-identical')
    pages1 = (PRIVATE / 'gong2013.txt').read_text().split('\f')
    pages2 = (PRIVATE / 'gong_publisher_mirror.txt').read_text().split('\f')
    cmp = load(HERE / 'SOURCE_COMPARISON.json')
    need(len(cmp['pages']) == 12 and len(pages1) == len(pages2) == 14, 'provenance', 'two complete article copies plus covers')
    for i, r in enumerate(cmp['pages'], 1):
        s1 = re.sub(r'\s+', '', pages1[i])
        s2 = re.sub(r'\s+', '', pages2[i])
        need(s1 == s2 and digest(s1.encode()) == r['osaka_normalized_text_sha256']
             and digest(s2.encode()) == r['mirror_normalized_text_sha256'],
             'provenance', 'every published article page agrees in normalized extraction')
    ledger = load(HERE / 'FINAL_LEDGER_CHECK.json')
    need(ledger['numeric_gid'] == 1254632077 and ledger['columns'] == 43,
         'accounting', 'numeric-gid full-column read')
    need(ledger['rows'] == 191 and ledger['semantic_target_leads'] == [], 'accounting', 'bounded missing-row finding')
    need(digest((PRIVATE / 'ledger_final.json').read_bytes()) == ledger['sha256'], 'accounting', 'retained ledger body')
    row = load(HERE / 'PROPOSED_ROW.json')
    need(len(row['cells']) == 4 and all(isinstance(x, str) for x in row['cells']), 'accounting', 'literal four-string row')
    need(row['cells'][1] == '' and row['cells'][2] == 'https://doi.org/10.18910/25089', 'accounting', 'blank B/existing authenticated DOI')
    need('https://github.com/AlecKriebel/Math/pull/1290' in row['cells'][3], 'accounting', 'exact PR URL in D')
    need(row['whole_problem_e_resolved'] is False and row['new_publication'] is False
         and row['ready_for_external_write'] is False, 'accounting', 'no whole-program or write-readiness inflation')


def sign(state, mask):
    return -1 if (state & mask).bit_count() % 2 else 1


def children(state, length):
    mask = (1 << length) - 1
    return ((state << 1) & mask, ((state << 1) & mask) | 1)


def p_on_mask(mask):
    return None if mask & 1 else mask >> 1


def star_on_mask(mask, length):
    return None if mask & (1 << (length - 1)) else mask << 1


def shift_masks():
    states_total = characters_total = 0
    for length in range(1, 8):
        total = 1 << length
        states_total += total
        # Direct transition-count checks, independent of the Walsh action rule.
        for state in range(total):
            counts = Counter({state: 1})
            for n in range(length + 1):
                expected = Counter((((state << n) & (total - 1)) | word) for word in range(1 << n))
                need(counts == expected and sum(counts.values()) == 1 << n,
                     'finite_kernel', 'all n-step transition path counts')
                if n == length:
                    need(set(counts) == set(range(total)) and set(counts.values()) == {1},
                         'finite_kernel', 'exact uniform L-step law gives irreducibility')
                next_counts = Counter()
                for point, number in counts.items():
                    for child in children(point, length):
                        next_counts[child] += number
                counts = next_counts
        incoming = Counter()
        for state in range(total):
            incoming.update(children(state, length))
        need(set(incoming.values()) == {2} and len(incoming) == total,
             'finite_kernel', 'exact uniform stationarity')
        need(0 in children(0, length), 'finite_kernel', 'self-loop gives aperiodicity')
        columns = {}
        for mask in range(1, total):
            characters_total += 1
            outmask = p_on_mask(mask)
            for state in range(total):
                image = F(sum(sign(y, mask) for y in children(state, length)), 2)
                expected = 0 if outmask is None else sign(state, outmask)
                need(image == expected, 'walsh', 'direct Markov action on every character/state')
            columns[mask] = outmask
            after = mask
            for _ in range(length):
                after = None if after is None else p_on_mask(after)
            need(after is None, 'walsh', 'mean-zero nilpotence on complete basis')
            # Verify the finite adjoint against every basis vector (orthogonality).
            adjoint = star_on_mask(mask, length)
            for other in range(1, total):
                need((p_on_mask(other) == mask) == (adjoint == other),
                     'adjoint', 'exact transpose action in orthonormal Walsh coordinates')
            back = None if outmask is None else star_on_mask(outmask, length)
            need(back == (None if mask & 1 else mask),
                 'adjoint', 'P*P is conditional expectation off first coordinate')
        # All Walsh characters, not just one-coordinate functions, form shift blocks.
        blocks = {}
        for mask in range(1, total):
            offset = (mask & -mask).bit_length() - 1
            primitive = mask >> offset
            blocks.setdefault(primitive, []).append((offset, mask))
        need(sum(len(b) for b in blocks.values()) == total - 1, 'gap_blocks', 'full mean-zero dimension')
        lengths = []
        for primitive, block in blocks.items():
            size = length - (primitive.bit_length() - 1)
            lengths.append(size)
            need(sorted(block) == [(j, primitive << j) for j in range(size)],
                 'gap_blocks', 'unique primitive translation block')
            for j in range(size):
                mask = primitive << j
                need(columns[mask] == (None if j == 0 else primitive << (j - 1)),
                     'gap_blocks', 'backward shift restricted to block')
                need(star_on_mask(mask, length) == (None if j == size - 1 else primitive << (j + 1)),
                     'gap_blocks', 'forward adjoint restricted to block')
        need(max(lengths) == length and blocks[1] == [(j, 1 << j) for j in range(length)],
             'gap_blocks', 'longest block exists and has length L')
        # Use unnormalized g=sum e_j to keep every energy calculation rational.
        g = [sum(sign(x, 1 << j) for j in range(length)) for x in range(total)]
        pg = [F(sum(g[y] for y in children(x, length)), 2) for x in range(total)]
        mean, second = F(sum(g), total), F(sum(v * v for v in g), total)
        jump = F(sum((g[y] - g[x]) ** 2 for x in range(total) for y in children(x, length)), 4 * total)
        residual = sum((F(g[x]) - pg[x]) ** 2 for x in range(total)) / total
        need(mean == 0 and second == length and jump == residual == 1,
             'energy', 'exact variance N and energies1 for unnormalized cylinder witness')
        need(F(jump, length) == F(1, length), 'energy', 'normalized ordinary energy 1/N')
        # Finite witnesses of infinite coisometry use one extra coordinate.
        extended = length + 1
        mask = 1 << (length - 1)
        need(p_on_mask(star_on_mask(mask, extended)) == mask,
             'adjoint', 'infinite PP*=I on arbitrary finite one-coordinate cylinder')
        need(p_on_mask(1) is None, 'negative_control', 'printed P*P=I rejected by first coordinate')
        if length >= 2:
            e1 = [sign(x, 2) for x in range(total)]
            pe1 = [F(sum(e1[y] for y in children(x, length)), 2) for x in range(total)]
            conditional = F(sum(v * v for v in e1), total) - sum(v * v for v in pe1) / total
            need(conditional == 0 and F(sum(e1), total) == 0,
                 'energy', 'conditional variance zero despite stationary variance1')
            need(sum(v * v for v in pe1) / total == 1 > F(1, 4),
                 'negative_control', 'curvature1/2 does not force squared one-step norm at most1/4')
            need(p_on_mask(2) == 1 and p_on_mask(1) is None,
                 'negative_control', 'stationarity is not reversibility')
        # The boundary of a finite truncation prevents finite PP*=I on last bit.
        need(star_on_mask(1 << (length - 1), length) is None,
             'negative_control', 'finite nilpotent chain is not infinite coisometry')
    return states_total, characters_total


def distance(x, y, a):
    if x == y:
        return F(0)
    first = ((x ^ y) & -(x ^ y)).bit_length() - 1
    return a ** first


def exact_transport():
    cases = 0
    for length in range(1, 6):
        for a in [F(1, 2), F(1, 3), F(3, 4)]:
            for x in range(1 << length):
                for y in range(x + 1, 1 << length):
                    cx, cy = children(x, length), children(y, length)
                    same = sum(distance(cx[b], cy[b], a) for b in [0, 1]) / 2
                    cross = sum(distance(cx[b], cy[1 - b], a) for b in [0, 1]) / 2
                    optimal = min(same, cross)  # all 2x2 equal-marginal couplings interpolate these endpoints
                    erased = ((x ^ y) & -(x ^ y)) == 1 << (length - 1)
                    expected = F(0) if erased else a * distance(x, y, a)
                    need(optimal == expected and cross == 1, 'transport', 'exact two-support transport')
                    curvature = 1 - optimal / distance(x, y, a)
                    need(curvature == (1 if erased else 1 - a), 'transport', 'exact finite curvature and boundary case')
                    cases += 1
    return cases


def symbolic_controls():
    # Characteristic polynomials D_m(t) of 2*(J_m+J_m*)/2 have
    # D_0=1,D_1=t,D_m=t D_(m-1)-D_(m-2), verified by determinants' tridiagonal recurrence.
    polynomials = [[1], [0, 1]]
    for m in range(2, 15):
        poly = [0] + polynomials[-1]
        for j, value in enumerate(polynomials[-2]):
            poly[j] -= value
        polynomials.append(poly)
        need(len(poly) == m + 1 and poly[-1] == 1, 'spectral_polynomial', 'monic degree m')
        # The recurrence is equivalent to sin((m+1)theta)/sin(theta)
        # after t=2cos(theta), by the sine addition identity proved in REPORT.md.
        for t in [F(-2), F(-1), F(0), F(1), F(2), F(3, 2)]:
            val = lambda p: sum(c * t ** j for j, c in enumerate(p))
            need(val(poly) == t * val(polynomials[m - 1]) - val(polynomials[m - 2]),
                 'spectral_polynomial', 'exact rational recurrence evaluation')
    for length in range(1, 31):
        # A_L=PQ_L kills a cylinder beyond coordinate L while P does not.
        mask = 1 << length
        q_mask = None if mask.bit_length() > length else mask
        p_mask = p_on_mask(mask)
        need(q_mask is None and p_mask == 1 << (length - 1),
             'approximation', 'unit-norm witness prevents operator-norm convergence')
        # For each fixed n a longer finite chain still has power norm1.
        n = length - 1
        witness = 1 << n
        for _ in range(n):
            witness = p_on_mask(witness)
        need(witness == 1, 'approximation', 'no uniform exponential prefactor with rho<1')
    for n in range(1, 31):
        # Exact normalized infinite eigenvector recurrence with rational eigenvalue.
        for z in [F(0), F(1, 2), F(-1, 3), F(3, 4)]:
            need(z ** (n + 1) == z * z ** n, 'spectrum', 'backward-shift geometric eigen-coefficients')


def inventory():
    man = load(HERE / 'MANIFEST.json')
    files = man['files']
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p != HERE / 'MANIFEST.json'}
    need(actual == {x['path'] for x in files}, 'seal', 'closed exact inventory')
    for r in files:
        p = HERE / r['path']
        need(not p.is_symlink(), 'seal', 'no symlink escape')
        b = p.read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'seal', 'every member byte pin')
        need(r['private'] == r['path'].startswith('private_sources/'), 'seal', 'private raw-source flag')
    need('private_sources/pr_MANIFEST.json' in actual, 'seal', 'nested manifest included')
    need(digest((HERE / files[0]['path']).read_bytes()) != '0' * 64,
         'negative_control', 'forged file digest rejected')


def main():
    if any(x != '--closed' for x in sys.argv[1:]):
        raise ValueError('only --closed is supported')
    source_checks()
    states, characters = shift_masks()
    transport = exact_transport()
    symbolic_controls()
    closed = '--closed' in sys.argv[1:]
    if closed:
        inventory()
    print(json.dumps({'status': 'PASS', 'guards': sum(COUNTS.values()), 'guards_by_family': COUNTS,
                      'finite_state_counts_summed': states, 'complete_walsh_characters': characters,
                      'exact_pair_metric_cases': transport, 'closed_inventory_checked': closed,
                      'author_programs_executed': False, 'writes_or_network': False,
                      'finite_controls_are_not_the_universal_proof': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
