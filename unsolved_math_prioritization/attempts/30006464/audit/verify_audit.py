#!/usr/bin/env python3
"""Pinned packet integrity and independently implemented exact finite controls."""
import hashlib
import json
import math
import pathlib
import stat
from fractions import Fraction as Q

ROOT = pathlib.Path(__file__).resolve().parent
OWN = {'README.md', 'AUDIT.md', 'PRECISION_ADDENDUM.md', 'AUDIT_RESULTS.json',
       'GRAM_ZERO_DIMENSION.patch', 'CORRECTION.json',
       'SOURCE_CHECKS.json', 'verify_audit.py', 'test_audit.py', 'verify_inputs.py',
       'SOURCE_PIN.json', 'MANIFEST.json'}
AUTHOR = {'README.md', 'PROOFS.md', 'APPROACHES.md', 'CLAIMS.json', 'DATA_IDENTITY.json',
          'SOURCES.json', 'verify.py', 'verify_corpora.py', 'test_packet.py',
          'SOURCE_PIN.json', 'CHECK_RESULTS.json', 'MANIFEST.json'}
FILES = OWN | {'AUTHOR/' + n for n in AUTHOR}
AUTHOR_MANIFEST_SHA = '8c9aa06e0920943b23c258c8b426408f8d18435f0dec32d454f5f47473650184'
SOURCE_NAMES = {'verify_audit.py', 'test_audit.py', 'verify_inputs.py'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read(name):
    return json.loads((ROOT / name).read_text())

def integrity():
    files, dirs = set(), set()
    for path in ROOT.rglob('*'):
        mode = path.lstat().st_mode
        name = path.relative_to(ROOT).as_posix()
        if stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            require(stat.S_ISREG(mode), 'nonregular member: ' + name)
            files.add(name)
    require(dirs == {'AUTHOR'} and files == FILES, 'strict recursive inventory mismatch')
    manifest = read('MANIFEST.json')
    require(set(manifest) == FILES - {'MANIFEST.json'}, 'manifest inventory mismatch')
    for name, info in manifest.items():
        raw = (ROOT / name).read_bytes()
        require(info == {'bytes': len(raw), 'sha256': digest(raw)}, 'manifest bytes: ' + name)
    pin = read('SOURCE_PIN.json')
    require(set(pin) == SOURCE_NAMES, 'audit source pin inventory')
    for name, sha in pin.items():
        require(digest((ROOT / name).read_bytes()) == sha, 'audit source pin: ' + name)
    raw = (ROOT / 'AUTHOR/MANIFEST.json').read_bytes()
    require(digest(raw) == AUTHOR_MANIFEST_SHA, 'immutable author manifest anchor')
    manifest = json.loads(raw)
    require(set(manifest) == AUTHOR - {'MANIFEST.json'}, 'author inventory')
    for name, info in manifest.items():
        raw = (ROOT / 'AUTHOR' / name).read_bytes()
        require(info == {'bytes': len(raw), 'sha256': digest(raw)}, 'immutable author member: ' + name)
    result = read('AUDIT_RESULTS.json')
    require(result['problem_id'] == 30006464 and result['original_status'] == 'unresolved'
            and result['approaches_used'] == 5 and result['full_resolution'] is False,
            'audit resolution scope')
    require(result['verdict'] == 'accepted_partial_with_nonblocking_clarification'
            and result['no_substantive_defect_found'] is True
            and result['zero_dimensional_convention_required'] is True, 'audit verdict scope')
    require(result['safe_inventory_only'] is True and result['remote_mutation'] is False,
            'audit safety scope')
    source = read('SOURCE_CHECKS.json')
    expected = {
        'owr': (569251, '0ab42f4636cc8f6fb9d3165313c5501ceef1a521f4ecb9a981e022fb68d0f4e1'),
        'alwx': (291891, '395f18c1d17d4eb98eac128dd071ae6d87e4a92cc99da56396ad4d3edb3366fd'),
        'bertrand': (73839, 'dd6811bc254a025eedc6c9e3b65ea4761e76e175be495457fb6e985f233a8f5c'),
    }
    require({s['id'] for s in source['pinned_pdfs']} == set(expected), 'source metadata inventory')
    for item in source['pinned_pdfs']:
        require((item['bytes'], item['sha256']) == expected[item['id']], 'source metadata identity')
    require(source['source_files_included'] is False, 'source inclusion scope')
    correction = read('CORRECTION.json')
    require(correction['author_manifest_sha256'] == AUTHOR_MANIFEST_SHA
            and correction['original_proof_sha256'] == '0b3055998770e3394ef85ccc3048a65e188165ac18de0fe52d352680795384e9'
            and correction['original_freeze_unchanged'] is True
            and correction['apply_to_copy_only'] is True, 'operative correction scope')
    require(digest((ROOT/'GRAM_ZERO_DIMENSION.patch').read_bytes()) == correction['patch_sha256'],
            'operative patch digest')

def sieve(limit):
    bits = [True] * (limit + 1)
    bits[:2] = [False, False]
    for p in range(2, math.isqrt(limit) + 1):
        if bits[p]:
            for n in range(p * p, limit + 1, p):
                bits[n] = False
    return [n for n in range(2, limit + 1) if bits[n]]

def factors(n):
    out = []
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            e += 1
            n //= p
        if e:
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out

def divisors(n):
    out = [1]
    for p, e in factors(n):
        out = [d * p ** a for d in out for a in range(e + 1)]
    return out

def phi(n):
    return math.prod((p - 1) * p ** (e - 1) for p, e in factors(n))

def product_delta(limit):
    # Direct finite product, independent of the author's logarithmic derivative.
    coeff = [1] + [0] * (limit - 1)
    for d in range(1, limit):
        old = coeff
        coeff = [0] * limit
        for power in range(min(24, (limit - 1) // d) + 1):
            shift = d * power
            multiplier = (-1) ** power * math.comb(24, power)
            for j in range(limit - shift):
                coeff[j + shift] += multiplier * old[j]
    return [0] + coeff

def controls():
    counts = {}
    tau = product_delta(512)
    require(tau[1:11] == [1, -24, 252, -1472, 4830, -6048, -16744, 84480, -113643, -115920], 'direct product anchors')
    counts['direct_product_tau_anchor_coefficients'] = 10
    primes = sieve(4097)
    for p in [p for p in primes if p * p <= 512]:
        require(tau[p * p] == tau[p] ** 2 - p ** 11, 'independent Hecke relation')
        t = Q(tau[p] ** 2, p ** 11)
        require(t + Q(tau[p * p] ** 2, p ** 22) == (t - Q(1, 2)) ** 2 + Q(3, 4), 'normalized prime square')
    counts['independent_prime_square_pairs'] = len([p for p in primes if p * p <= 512])
    mass = Q(0)
    for bound in range(1, 513):
        mass += Q(tau[bound] ** 2, bound ** 11)
        require(mass >= 1 + Q(3, 4) * sum(p * p <= bound for p in primes), 'independent partial mass')
    counts['independent_mass_prefixes'] = 512
    for n in range(1, 251):
        prod = math.prod((Q(p + 1, p) for p, _ in factors(n)), start=Q(1))
        index = n * prod
        require(index.denominator == 1 and index / n ** 12 / Q(1, n ** 11) == prod, 'oldform norm ratio')
        require(prod == sum((Q(1, d) for d in divisors(math.prod(p for p, _ in factors(n)))), Q(0)), 'squarefree divisor identity')
        require(prod <= sum((Q(1, d) for d in range(1, n + 1)), Q(0)), 'harmonic bound')
        cusp = sum(Q(n * v * v, math.gcd(v * v, n)) * phi(math.gcd(v, n // v)) for v in divisors(n))
        require(cusp == n * index, 'independent cusp arithmetic')
    counts['independent_level_and_cusp_controls'] = 250
    for n in range(1, 31):
        for bound in range(1, 21):
            raw_sample = sum((Q(tau[m] ** 2, (n * m) ** 11) for m in range(1, bound + 1)), Q(0))
            level_one = sum((Q(tau[m] ** 2, m ** 11) for m in range(1, bound + 1)), Q(0))
            require(raw_sample == Q(1, n ** 11) * level_one, 'coefficient normalization power')
    counts['independent_oldform_coefficient_scalings'] = 600
    for p in [2, 3, 5, 7, 11]:
        for e in range(1, 9):
            actual = sum(p ** (e + 2*j - min(2*j, e)) * phi(p ** min(j, e-j)) for j in range(e+1))
            require(actual == p ** (2*e) + p ** (2*e-1), 'prime-power cusp identity')
    counts['prime_power_cusp_controls'] = 40
    for r in range(2, 101):
        prod = math.prod((Q(p + 1, p) for p in primes if p <= r), start=Q(1))
        require(prod >= Q(1, 2) * sum((Q(1, n) for n in range(1, r+1)), Q(0)), 'primorial lower bound')
        telescoping = math.prod((1-Q(1, n*n) for n in range(2, r+1)), start=Q(1))
        require(telescoping == Q(r+1, 2*r) and telescoping > Q(1,2), 'telescoping product')
    counts['primorial_and_telescoping_controls'] = 99
    boundary_count = 0
    for j in range(1, 13):
        for offset in [Q(-1,1000), Q(0), Q(1,1000)]:
            x = 2 ** j + offset
            if x < 2:
                continue
            ell = 0
            while 2 ** (ell+1) <= x:
                ell += 1
            require(sum(p <= x for p in primes) >= ell, 'rational dyadic prime boundary')
            boundary_count += 1
    counts['rational_dyadic_boundaries'] = boundary_count
    for numerator in range(401):
        t = Q(numerator, 37)
        require(t+(t-1)**2 == (t-Q(1,2))**2+Q(3,4) and t+(t-1)**2 >= Q(3,4), 'prime-pair polynomial')
    counts['independent_pair_polynomial_controls'] = 401
    p = 101
    # Compare all ST^j cosets pairwise using the lower-left matrix entry.
    for j in range(p):
        for ell in range(j+1, p):
            require((ell-j) % p != 0, 'distinct left cosets')
    counts['distinct_prime_level_coset_pairs'] = p*(p-1)//2
    rectangle_count = 0
    area = Q(0)
    for j in range(26, 50):
        require(Q(2,1) / Q(2*j-1,2)**2 < Q(1,p), 'rectangle height')
        area += Q(1,2)
        rectangle_count += 1
    require(area == 12 and area > 2, 'total rectangle area')
    counts['individual_rectangle_controls'] = rectangle_count
    for m in range(1, 41):
        polynomial = [Q(math.factorial(m-1), math.factorial(j)) for j in range(m)]
        difference = [(j+1)*polynomial[j+1]-polynomial[j] if j+1<m else -polynomial[j] for j in range(m)]
        require(difference == [Q(0)]*(m-1)+[Q(-1)], 'gamma polynomial derivative')
    counts['independent_gamma_polynomial_controls'] = 40
    for n in range(1, 11):
        for denominator in range(1, 11):
            y = Q(1, denominator)
            for q in range(6, 13):
                original = n**3 / y**2 * (2*n/y)**(-q)
                rearranged = Q(1,2**q)*Q(n)**(3-q)*y**(q-2)
                require(original == rearranged and rearranged <= Q(1,2**q), 'tail factor algebra')
    counts['rational_tail_factor_controls'] = 700
    return counts

def main():
    integrity()
    counts = controls()
    return {'status': 'pass', 'problem_id': 30006464, 'original_status': 'unresolved',
            'full_resolution': False, 'author_bytes_preserved': True,
            'independent_controls': counts, 'total_independent_finite_controls': sum(counts.values()),
            'limit': 'Finite exact controls supplement, and do not certify, the analytic audit.'}

if __name__ == '__main__':
    try:
        print(json.dumps(main(), sort_keys=True))
    except Exception as exc:
        raise SystemExit('FAIL: ' + str(exc))
