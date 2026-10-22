#!/usr/bin/env python3
"""Integrity and exact finite controls; not a proof assistant for the theorem."""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys


class Invalid(ValueError):
    pass


def need(test, message):
    if not test:
        raise Invalid(message)


def integer(x, minimum=0):
    need(type(x) is int and x >= minimum, 'invalid exact integer')
    return x


def exact_keys(x, expected):
    need(type(x) is dict and set(x) == set(expected), 'invalid object schema')


def pairs(items):
    result = {}
    for k, v in items:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def no_constant(_):
    raise Invalid('non-finite JSON number')


def no_float(_):
    raise Invalid('inexact JSON number')


def decode(b):
    return json.loads(b.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=no_constant, parse_float=no_float)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def digest(x):
    need(type(x) is str and re.fullmatch('[0-9a-f]{64}', x) is not None,
         'invalid SHA256')
    return x


MEMBERS = {'REPORT.md', 'README.md', 'SOURCES.json', 'CLAIMS.json',
           'FIXTURES.json', 'verify.py', 'controls.py'}


def inventory(root, pin):
    need(root.is_dir() and not root.is_symlink(), 'root is not a real directory')
    entries = list(root.iterdir())
    need({p.name for p in entries} == MEMBERS | {'MANIFEST.json'}, 'inventory mismatch')
    need(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular member')
    b = (root / 'MANIFEST.json').read_bytes()
    need(sha(b) == digest(pin), 'external manifest pin mismatch')
    man = decode(b)
    exact_keys(man, ['schema', 'problem_id', 'files'])
    need(integer(man['schema']) == 1 and integer(man['problem_id']) == 2508,
         'manifest identity mismatch')
    need(type(man['files']) is list, 'invalid manifest list')
    seen = set()
    for ent in man['files']:
        exact_keys(ent, ['path', 'bytes', 'sha256'])
        p = ent['path']
        need(type(p) is str and p in MEMBERS and p not in seen, 'unsafe or duplicate member')
        seen.add(p)
        b = (root / p).read_bytes()
        need(len(b) == integer(ent['bytes']) and sha(b) == digest(ent['sha256']),
             'payload identity mismatch')
    need(seen == MEMBERS, 'manifest coverage mismatch')


def fraction(x):
    need(type(x) is list and len(x) == 2, 'invalid rational pair')
    a, b = integer(x[0]), integer(x[1], 1)
    q = Q(a, b)
    need(q.numerator == a and q.denominator == b, 'noncanonical rational')
    return q


def ceil(x):
    return -((-x.numerator) // x.denominator)


def finite_checks(root):
    f = decode((root / 'FIXTURES.json').read_bytes())
    exact_keys(f, ['schema', 'parameters', 'finite_evidence_only'])
    need(integer(f['schema']) == 1 and f['finite_evidence_only'] is True, 'fixture scope')
    need(type(f['parameters']) is list and len(f['parameters']) == 80, 'fixture coverage')
    expected = [(L, eta) for L in range(1, 17)
                for eta in [Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(4)]]
    arithmetic = 0
    for rec, (L, eta) in zip(f['parameters'], expected):
        exact_keys(rec, ['L', 'eta', 'epsilon', 'n0'])
        need(integer(rec['L'], 1) == L and fraction(rec['eta']) == eta, 'parameter coverage')
        q = (1 + eta) * L
        eps = fraction(rec['epsilon'])
        need(eps == min(Q(1, 4), eta / (4 * (1 + q))), 'epsilon value')
        need(0 < eps < min(Q(1, 2), eta / (2 * (1 + q))), 'epsilon range')
        gap = (eta - eps) / q - eps
        need(gap > 0, 'nonpositive linear margin')
        threshold = (1 + 1 / q) / gap
        n0 = integer(rec['n0'], 1)
        need(n0 == threshold.numerator // threshold.denominator + 1, 'threshold value')
        for n in [n0, n0 + 1, n0 + L, 2 * n0 + 17, 10**12 + n0]:
            D = ceil((1 + eps) * n)
            N = n // L
            need((1 + eps) * n <= D < (1 + eps) * n + 1, 'ceiling bound')
            need(D - 1 < (1 + eps) * n, 'strict maximal degree')
            need(Q(N) - Q(D) / q >= n * (eta - eps) / q - 1 - 1 / q,
                 'floor ceiling loss')
            need(n * gap > 1 + 1 / q, 'asymptotic margin')
            # B is an integer satisfying B < D/q and B <= N.
            Bmax = min(N, ceil(Q(D) / q) - 1)
            need(N - Bmax > eps * n, 'integer robust count')
            arithmetic += 1
    # Normalized angles θ/π on a rational grid; exhaustive multisets include
    # repeated nodes and both endpoints. This is finite evidence only.
    patterns = 0
    for n in range(1, 9):
        for angles in itertools.combinations_with_replacement([Q(i, 4) for i in range(5)], n):
            for L in range(1, min(n, 4) + 1):
                for eta in [Q(1, 10), Q(1), Q(4)]:
                    eps = min(Q(1, 4), eta / (4 * (1 + (1 + eta) * L)))
                    D = ceil((1 + eps) * n)
                    spans = [angles[b + L - 1] - angles[b]
                             for b in range(0, n - L + 1, L)]
                    q = (1 + eta) * L
                    B = sum(D * h > q for h in spans)
                    G = len(spans) - B
                    need(sum(spans) <= 1, 'disjoint-span inequality')
                    need(B < Q(D) / q, 'bad-block bound')
                    need(G >= Q(n // L) - Q(D) / q, 'good-block lower bound')
                    patterns += 1
    return {'parameter_cases': 80, 'large_n_arithmetic_cases': arithmetic,
            'finite_block_patterns': patterns}


def metadata(root):
    c = decode((root / 'CLAIMS.json').read_bytes())
    expected = {
        'problem_id': 2508, 'problem_number': 'EP-1133', 'rank': 1037,
        'classification': 'PRIOR_SOLUTION_VERIFIED_RELATIVE_TO_IMPORTED_THEOREMS',
        'new_approaches': 0, 'new_discovery_claimed': False,
        'community_acceptance_verified': False, 'proof_assistant_verified': False,
        'unresolved_gap_in_checked_deduction': False,
        'imported_density_theorem_reproved': False,
        'effective_constants_in_C_claimed': False,
        'finite_checks_prove_theorem': False,
        'repeated_nodes_covered': True, 'complex_polynomials_covered': True}
    need(c == expected and all(type(c[k]) is type(v) for k, v in expected.items()),
         'claim scope mismatch')
    s = decode((root / 'SOURCES.json').read_bytes())
    exact_keys(s, ['schema', 'checked_utc', 'dataset_pins', 'selected_record_sha256',
                   'research_entry_present', 'scholarly_sources', 'retrieval_notes'])
    need(integer(s['schema']) == 1 and s['research_entry_present'] is False,
         'source scope mismatch')
    digest(s['selected_record_sha256'])
    need([x['name'] for x in s['dataset_pins']] == ['problems.json', 'research_results.json'],
         'dataset identity labels')
    need([x['id'] for x in s['scholarly_sources']] == ['candidate', 'density', 'original'],
         'scholarly identity labels')
    for ent in s['dataset_pins'] + s['scholarly_sources']:
        integer(ent['bytes'], 1)
        digest(ent['sha256'])
    need(s['scholarly_sources'][0]['publication_status'] == 'draft_manuscript',
         'candidate acceptance overclaim')
    need(s['scholarly_sources'][1]['imported_result'] == 'Theorem 1 necessity, real-line specialization',
         'density dependency mismatch')
    return s


def source_checks(source, args):
    paths = [args.problems, args.research, args.candidate_pdf, args.density_pdf, args.original_pdf]
    if not any(paths):
        return {'performed': False, 'reason': 'external source files not supplied'}
    need(all(paths), 'source replay requires all five external files')
    entries = source['dataset_pins'] + source['scholarly_sources']
    source_bytes = []
    for p, ent in zip(paths, entries):
        need(p.is_file() and not p.is_symlink(), 'invalid source input')
        b = p.read_bytes()
        need(len(b) == ent['bytes'] and sha(b) == ent['sha256'], 'external source mismatch')
        source_bytes.append(b)
    # Exact whole-file pins authenticate the corpus, which can contain floats.
    records = json.loads(source_bytes[0])
    need(type(records) is list, 'problem corpus shape')
    selected = [r for r in records if r.get('id') == 2508]
    need(len(selected) == 1 and selected[0].get('problem_number') == 'EP-1133', 'selected problem match')
    canonical = json.dumps(selected[0], sort_keys=True, ensure_ascii=False,
                           separators=(',', ':'), allow_nan=False).encode('utf-8')
    need(sha(canonical) == source['selected_record_sha256'], 'selected record identity')
    research = json.loads(source_bytes[1])
    need(type(research) is dict and 'EP-1133' not in research, 'research absence match')
    for b in source_bytes[2:]:
        need(b.startswith(b'%PDF-'), 'scholarly source is not PDF')
    return {'performed': True, 'whole_file_pins_matched': 5,
            'selected_record_matches': 1, 'research_entry_present': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--manifest-sha256', required=True)
    for x in ['problems', 'research', 'candidate-pdf', 'density-pdf', 'original-pdf']:
        ap.add_argument('--' + x, type=Path)
    args = ap.parse_args()
    inventory(args.root, args.manifest_sha256)
    src = metadata(args.root)
    out = {'status': 'PASS', 'problem_id': 2508, 'new_approaches': 0,
           'proof_assistant_verification': False, 'finite_evidence': finite_checks(args.root),
           'source_replay': source_checks(src, args)}
    print(json.dumps(out, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    try:
        main()
    except (Invalid, ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        sys.exit(1)
