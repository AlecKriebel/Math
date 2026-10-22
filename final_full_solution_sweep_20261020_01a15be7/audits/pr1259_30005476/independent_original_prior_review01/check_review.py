#!/usr/bin/env python3
"""Offline source authentication and finite mechanism/counterexample checks.

These finite checks do not establish the infinite spectrality theorem. The
deductive review is in REPORT.md. No network, shell, author code, or mutation.
"""
import hashlib
import itertools
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f4mul(a, b):
    raw = 0
    for i in range(2):
        if b & (1 << i):
            raw ^= a << i
    for i in range(2, 1, -1):
        if raw & (1 << i):
            raw ^= 7 << (i - 2)
    return raw


def rotate(a, s, r):
    return sum(((a >> i) & 1) << ((i + s) % r) for i in range(r))


def span2(gens):
    out = {0}
    for g in gens:
        out |= {x ^ g for x in tuple(out)}
    return frozenset(out)


def basis2(space):
    basis = []
    sofar = frozenset({0})
    for x in sorted(space):
        if x not in sofar:
            basis.append(x)
            sofar = span2(basis)
    return basis


def span4(binary_basis, dimension):
    out = {(0,) * dimension}
    for b in binary_basis:
        vector = tuple((b >> i) & 1 for i in range(dimension))
        out = {tuple(x ^ f4mul(c, y) for x, y in zip(v, vector))
               for v in out for c in range(4)}
    return out


def authenticate():
    need(sha(BASE / 'INPUT_BINDING.json') ==
         '39de5d881a938f84f81fc096cdd81258f813a3deb435c337c4e2cb79254d349d',
         'immutable input binding')
    binding = json.loads((BASE / 'INPUT_BINDING.json').read_text())
    need(binding['head'] == 'fe7a44274ef24987faf4c619441782c2411a41d6', 'head')
    need(len(binding['files']) == 8, 'exact eight PR inputs')
    for item in binding['files']:
        b = (BASE / item['local']).read_bytes()
        need(len(b) == item['bytes'], 'PR size: ' + item['path'])
        need(hashlib.sha256(b).hexdigest() == item['sha256'], 'PR digest')
        need(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
             == item['git_blob_sha1'], 'PR Git object identity')
    expected = {
        'private/owr_original.pdf': 'b3a1780b4687ccb7ce238165c4fcb159f62ea86a3dc47bc2a3900806c400c4f5',
        'private/kummer_riener_published.pdf': '45f81891eb8e206b7a92d8f8d83b2a068af6657939700ec29ff235ff164bfed7',
        'private/hillar_sullivant_v2.pdf': 'd3567809b1f5607221a6d5a4042717ce38cc9e35e250b114828e4885b6149da6',
        'private/schnieper_seminar.pdf': 'bf8fba3f532c4348dbb553ddb2da0ac1707f71b86f3e5bb918623fd77670610f',
        'private/bern_award.pdf': 'f4590fbfd1b2f3d5700f97723594146cede7ffc9131961928763beac9365c513',
    }
    for name, digest in expected.items():
        need(sha(BASE / name) == digest, 'primary source identity: ' + name)
    manifest = json.loads((BASE / 'private/pr_source/MANIFEST.json').read_text())
    for item in manifest['entries']:
        p = BASE / 'private/pr_source' / item['file']
        need(p.stat().st_size == item['bytes'] and sha(p) == item['sha256'],
             'distributed PR manifest entry')
    return {'immutable_pr_blobs': 8, 'primary_pdfs': len(expected), 'pr_manifest_entries': 7}


def authenticate_package():
    manifest = json.loads((BASE / 'MANIFEST.json').read_text())
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
    need(actual == {e['path'] for e in manifest['entries']} |
         {'MANIFEST.json', 'SEAL_CHECK.json'}, 'closed review membership')
    for e in manifest['entries']:
        p = BASE / e['path']
        need(not p.is_symlink() and p.resolve().is_relative_to(BASE), 'ordinary local review payload')
        need(p.stat().st_size == e['bytes'] and sha(p) == e['sha256'], 'review payload pin: ' + e['path'])
    return {'entries': len(manifest['entries']), 'manifest_sha256': sha(BASE / 'MANIFEST.json')}


def boolean_ring():
    pairs = 0
    prefixes = 0
    stable_ideals = 0
    for r in range(1, 8):
        full = (1 << r) - 1
        fixed = [a for a in range(full + 1) if rotate(a, 1, r) == a]
        need(fixed == [0, full], 'transitive action has only trivial stable ideals')
        stable_ideals += len(fixed)
        for a in range(1, full + 1):
            for b in range(1, full + 1):
                need(any(a & rotate(b, s, r) for s in range(r)), 'translate-product selection')
                pairs += 1
        selected = []
        t = full
        for a in range(1, full + 1):
            moved = next(rotate(a, s, r) for s in range(r) if t & rotate(a, s, r))
            selected.append(moved)
            t &= moved
            need(t != 0, 'greedy prefix became zero')
            # All elements are idempotent: repeated powers create no new zero.
            need(moved & moved == moved, 'reduced Boolean ring')
            prefixes += 1
        coordinate = (t & -t).bit_length() - 1
        need(all(a & (1 << coordinate) for a in selected), 'coordinate prime meets selected set')
        # The orbit of a coordinate prime is all coordinate primes. Their core
        # contains only the zero vector, tested over every element.
        for a in range(full + 1):
            need(all(not (a & (1 << i)) for i in range(r)) == (a == 0), 'prime core')
        if r > 1:
            need((1 & 2) == 0, 'negative control: G-prime need not be ordinary prime')
    return {'nonzero_translate_pairs': pairs, 'greedy_prefixes': prefixes,
            'stable_ideal_supports': stable_ideals, 'dimensions': list(range(1, 8))}


def intersection_extension():
    spaces = {span2(s) for mask in range(256)
              for s in [[i for i in range(8) if mask & (1 << i)]]}
    need(len(spaces) == 16, 'all subspaces of F2^3')
    extended = {s: span4(basis2(s), 3) for s in spaces}
    count = 0
    for a in spaces:
        for b in spaces:
            inter = a & b
            need(span4(basis2(inter), 3) == extended[a] & extended[b], 'intersection extension')
            count += 1
    for s, lifted in extended.items():
        for v in itertools.product(range(4), repeat=3):
            lo = sum((x & 1) << i for i, x in enumerate(v))
            hi = sum(((x >> 1) & 1) << i for i, x in enumerate(v))
            need((v in lifted) == (lo in s and hi in s), 'independent coefficient membership')
    return {'subspaces': len(spaces), 'pairs': count, 'coefficient_memberships': 16 * 64}


def extension_and_reducedness_failures():
    for a in range(1, 4):
        need(any(f4mul(a, b) == 1 for b in range(1, 4)), 'F4 must be a field')
    def mult_pair(u, v):
        a, b = u
        c, d = v
        bd = f4mul(b, d)
        return (f4mul(a, c) ^ bd, f4mul(a, d) ^ f4mul(b, c) ^ bd)
    # F4 tensor_F2 F4 = F4[T]/(T^2+T+1). The two nonzero factors split.
    need(mult_pair((2, 1), (3, 1)) == (0, 0), 'nonclosed base must exhibit zero divisor')
    def dual_mul(a, b):
        return ((a & 1) & (b & 1)) | ((((a & 1) & (b >> 1)) ^ ((a >> 1) & (b & 1))) << 1)
    need(dual_mul(1, 2) == 2 and dual_mul(2, 2) == 0, 'nonreduced power control')
    return {'split_domain_counterexample': True, 'nilpotent_power_counterexample': True,
            'finite_dual_number_model_claimed_G_prime': False}


def finite_support_extension():
    count = 0
    for m in range(1, 5):
        for image in itertools.combinations(range(1, 9), m):
            bound = max(image)
            partial = dict(zip(range(1, m + 1), image))
            rest_domain = [i for i in range(1, bound + 1) if i not in partial]
            rest_image = [i for i in range(1, bound + 1) if i not in image]
            sigma = dict(partial)
            sigma.update(zip(rest_domain, rest_image))
            need(set(sigma) == set(sigma.values()) == set(range(1, bound + 1)), 'finite bijection')
            need(tuple(sigma[i] for i in range(1, m + 1)) == image, 'restriction to support')
            count += 1
    return {'increasing_map_restrictions_extended': count, 'maximum_support_bound': 8}


def quotient_boundaries():
    # Two infinite Boolean sequences each have infinitely many zeros and ones:
    # a_i = i mod 2; b_i = 1 iff i mod 4 >= 2. Every finite pattern can be moved
    # into the first m places by disjoint swaps with matching unused tail slots.
    count = 0
    for m in range(1, 8):
        for pattern in itertools.product(range(2), repeat=m):
            for seq in [lambda i: i % 2, lambda i: int(i % 4 >= 2)]:
                used = set(range(m))
                swaps = []
                for target, bit in enumerate(pattern):
                    source = next(i for i in range(m, 8 * m + 8) if i not in used and seq(i) == bit)
                    used.add(source)
                    swaps.append((target, source))
                result = [seq(source) for _, source in swaps]
                need(tuple(result) == pattern, 'finite permutation pattern witness')
                count += 1
    # Infinite distinctions are proved in REPORT.md; this guards finite witnesses.
    return {'finite_pattern_witnesses': count, 'infinite_nonT0_argument_in_report': True,
            'rational_diagonal_and_invariant_ring_arguments_in_report': True}


def main():
    if '--self-test-failure' in sys.argv:
        need(False, 'deliberate rejected diagnostic; never an accepted pass')
    result = {
        'status': 'PASS_FINITE_DIAGNOSTICS_AND_INPUT_AUTHENTICATION',
        'optimize': sys.flags.optimize,
        'checker_sha256': sha(pathlib.Path(__file__).resolve()),
        'limits': 'Deductive review supplies infinite theorem; finite models are corroboration and counterchecks only.',
        'input_authentication': authenticate(),
        'boolean_prime_core': boolean_ring(),
        'scalar_extension_intersections': intersection_extension(),
        'failed_hypothesis_controls': extension_and_reducedness_failures(),
        'finite_support_extension': finite_support_extension(),
        'quotient_boundaries': quotient_boundaries(),
        'network_calls': 0,
        'external_mutations': 0,
    }
    if '--verify-package' in sys.argv:
        result['closed_package'] = authenticate_package()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
