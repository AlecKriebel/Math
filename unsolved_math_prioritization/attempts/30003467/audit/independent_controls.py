#!/usr/bin/env python3
"""Independent audit controls. Does not certify the external disk construction."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

PIN = '1f2b1644d763a9c3b87bb391ab135e2501b86458fa36e9d050da544b0e111dbf'
MODES = [[], ['-O'], ['-OO']]

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(p):
    return {x.name: (x.stat().st_size, sha(x)) for x in p.iterdir() if x.is_file()}

def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def rebind(p):
    write(p / 'MANIFEST.json', {'schema': 1, 'files': [
        {'name': q.name, 'bytes': q.stat().st_size, 'sha256': sha(q)}
        for q in sorted(p.iterdir()) if q.name != 'MANIFEST.json']})
    return sha(p / 'MANIFEST.json')

def run(p, mode, pin=PIN, source=None):
    cmd = [sys.executable, '-B'] + mode + [str(p / 'verify_packet.py'), '--expected-manifest', pin]
    if source is not None:
        cmd += ['--source-root', str(source)]
    return subprocess.run(cmd, cwd=p.parent, capture_output=True, text=True,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

def independent_math():
    # New rational fixtures and an independently written transfer formula.
    cases = comparisons = boundary_cases = 0
    for shift in [Fraction(-3, 2), Fraction(0), Fraction(7, 5)]:
        pts = [(Fraction(a, 2) + shift, Fraction(b, 3) - shift)
               for a in range(-6, 7) for b in range(-6, 7)]
        for cx, cy in itertools.product(range(-2, 3), repeat=2):
            center = (Fraction(cx, 2) + shift, Fraction(cy, 3) - shift)
            ds = [(p[0] - center[0])**2 + (p[1] - center[1])**2 for p in pts]
            for r2 in [Fraction(1, 9), Fraction(1, 4), Fraction(1), Fraction(13, 9), Fraction(4)]:
                original = {i for i, d in enumerate(ds) if d < r2}
                need(bool(original), 'Bad independent fixture')
                inner_max = max(ds[i] for i in original)
                # A different convex combination from the packet implementation.
                rr = (2 * inner_max + r2) / 3
                need(0 < rr < r2, 'Invalid independent shrink')
                need(original == {i for i, d in enumerate(ds) if d <= rr}, 'Incidence changed')
                need(all(d != rr for d in ds), 'New incidence not strict')
                cases += 1
                comparisons += len(ds)
                boundary_cases += int(any(d == r2 for d in ds))
    # Independently construct H(T), with levels counted in vertices, not edges.
    tree_checks = []
    for m in [1, 2, 3, 4]:
        paths = [()]
        for depth in range(1, m):
            paths.extend(itertools.product(range(m), repeat=depth))
        idx = {p: i for i, p in enumerate(paths)}
        edges = []
        for p in paths:
            if len(p) < m - 1:
                edges.append(tuple(idx[p + (i,)] for i in range(m)))
            else:
                edges.append(tuple(idx[p[:i]] for i in range(len(p) + 1)))
        need(all(len(e) == m and len(set(e)) == m for e in edges), 'Uniformity failed')
        checked = 0
        if m <= 3:
            for c in itertools.product(range(2), repeat=len(paths)):
                need(any(len({c[i] for i in e}) == 1 for e in edges), 'Tree became two-colorable')
                checked += 1
        tree_checks.append({'m': m, 'vertices': len(paths), 'edges': len(edges),
                            'exhaustive_two_color_assignments': checked})
    # H3(2): one-vertex base extended by the H2(2) triangle is K4.
    k4edges = list(itertools.combinations(range(4), 2))
    for c in itertools.product(range(3), repeat=4):
        need(any(c[i] == c[j] for i, j in k4edges), 'K4 became three-colorable')
    # A finite set-system model tests the quantifier collection independently.
    # It is deliberately NOT presented as a disk-realization certificate.
    witness_family = set()
    for c in itertools.product(range(3), repeat=10):
        classes = [[i for i, x in enumerate(c) if x == color] for color in range(3)]
        e = tuple(next(v for v in classes if len(v) >= 4)[:4])
        witness_family.add(e)
    tested = 0
    for c in itertools.product(range(3), repeat=10):
        need(any(len({c[i] for i in e}) == 1 for e in witness_family), 'Fixed-family reduction failed')
        tested += 1
    return {'rational_transfer_cases': cases, 'point_incidence_comparisons': comparisons,
            'original_boundary_cases': boundary_cases, 'tree_hypergraphs': tree_checks,
            'K4_three_colorings_checked': 81, 'abstract_fixed_family_colorings_checked': tested,
            'abstract_fixed_family_edges': len(witness_family),
            'geometry_scope': 'NO_EXTERNAL_GEOMETRIC_REALIZATION_REPLAY'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('packet', type=Path)
    ap.add_argument('--sources', type=Path)
    args = ap.parse_args()
    packet = args.packet.resolve()
    sources = args.sources.resolve() if args.sources else None
    before = inventory(packet)
    need(sha(packet / 'MANIFEST.json') == PIN, 'Frozen pin differs')
    mf = json.loads((packet / 'MANIFEST.json').read_text())
    need(set(before) == {'MANIFEST.json'} | {f['name'] for f in mf['files']}, 'Independent inventory mismatch')
    for f in mf['files']:
        need(before[f['name']] == (f['bytes'], f['sha256']), 'Independent digest mismatch')
    c = json.loads((packet / 'CLAIM.json').read_text())
    for k, v in {'problem_id': 30003467, 'disposition': 'already_solved', 'answer': 'negative',
                 'approaches': 0, 'colors': 3, 'threshold': 4, 'exact_trace_size': 4,
                 'novelty_claim': False, 'dual_resolution_claim': False,
                 'fixed_radius_counterexample_claim': False, 'explicit_geometric_certificate': False}.items():
        need(type(c[k]) is type(v) and c[k] == v, 'Independent scope mismatch: ' + k)
    positives = source_passes = readonly = rejections = 0
    variants = ['truncated_manifest', 'duplicate_schema', 'schema_bool', 'nan', 'negative_size',
                'bytes_bool', 'duplicate_name', 'absolute_name', 'traversal', 'missing_proof',
                'extra_directory', 'proof_symlink', 'manifest_symlink', 'wrong_pin',
                'threshold_three', 'threshold_bool', 'dual', 'four_colors', 'fixed_radius',
                'positive_answer', 'one_attempt', 'novelty', 'wrong_exact_trace', 'bad_receipt',
                'malformed_claim', 'extra_claim_key', 'source_missing']
    with tempfile.TemporaryDirectory(prefix='independent-pseudodisk-') as tmp:
        tmp = Path(tmp)
        for j, mode in enumerate(MODES):
            p = tmp / ('positive-' + str(j))
            shutil.copytree(packet, p)
            result = run(p, mode)
            need(result.returncode == 0, 'Positive control: ' + result.stderr)
            need(json.loads(result.stdout)['source_verification'].startswith('NOT_RUN'), 'Missing-source state hidden')
            positives += 1
            if sources:
                result = run(p, mode, source=sources)
                need(result.returncode == 0, 'Source replay failed: ' + result.stderr)
                need(json.loads(result.stdout)['source_verification'] == 'PASS_EXTERNAL_BYTE_PINS_AND_SELECTED_RECORD', 'Unexpected source state')
                source_passes += 1
            for name in variants:
                q = tmp / (str(j) + '-' + name)
                shutil.copytree(packet, q)
                pin = PIN
                source = None
                if name == 'truncated_manifest': (q / 'MANIFEST.json').write_text('{'); pin = sha(q / 'MANIFEST.json')
                elif name == 'duplicate_schema': (q / 'MANIFEST.json').write_text('{"schema":1,"schema":1,"files":[]}'); pin = sha(q / 'MANIFEST.json')
                elif name == 'nan': (q / 'MANIFEST.json').write_text('{"schema":NaN,"files":[]}'); pin = sha(q / 'MANIFEST.json')
                elif name in ['schema_bool', 'negative_size', 'bytes_bool', 'duplicate_name', 'absolute_name', 'traversal']:
                    m = json.loads((q / 'MANIFEST.json').read_text())
                    if name == 'schema_bool': m['schema'] = True
                    if name == 'negative_size': m['files'][0]['bytes'] = -1
                    if name == 'bytes_bool': m['files'][0]['bytes'] = True
                    if name == 'duplicate_name': m['files'].append(m['files'][0].copy())
                    if name == 'absolute_name': m['files'][0]['name'] = '/PROOF.md'
                    if name == 'traversal': m['files'][0]['name'] = '../PROOF.md'
                    write(q / 'MANIFEST.json', m); pin = sha(q / 'MANIFEST.json')
                elif name == 'missing_proof': (q / 'PROOF.md').unlink()
                elif name == 'extra_directory': (q / 'unlisted').mkdir()
                elif name == 'proof_symlink': (q / 'PROOF.md').unlink(); (q / 'PROOF.md').symlink_to(packet / 'PROOF.md')
                elif name == 'manifest_symlink': (q / 'MANIFEST.json').unlink(); (q / 'MANIFEST.json').symlink_to(packet / 'MANIFEST.json')
                elif name == 'wrong_pin': pin = '0' * 64
                elif name == 'source_missing': source = tmp / 'absent'
                elif name == 'bad_receipt':
                    r = json.loads((q / 'MATH_RESULTS.json').read_text()); r['point_trace_checks'] -= 1
                    write(q / 'MATH_RESULTS.json', r); pin = rebind(q)
                else:
                    claim = json.loads((q / 'CLAIM.json').read_text())
                    mutations = {'threshold_three': ('threshold', 3), 'threshold_bool': ('threshold', True),
                                 'dual': ('coloring', 'dual_regions'), 'four_colors': ('colors', 4),
                                 'fixed_radius': ('fixed_radius_counterexample_claim', True),
                                 'positive_answer': ('answer', 'positive'), 'one_attempt': ('approaches', 1),
                                 'novelty': ('novelty_claim', True), 'wrong_exact_trace': ('exact_trace_size', 5)}
                    if name == 'malformed_claim': claim = []
                    elif name == 'extra_claim_key': claim['unapproved_claim'] = True
                    else:
                        key, value = mutations[name]; claim[key] = value
                    write(q / 'CLAIM.json', claim); pin = rebind(q)
                result = run(q, mode, pin=pin, source=source)
                need(result.returncode != 0, 'Malformed input accepted: ' + name)
                rejections += 1
        p = tmp / 'readonly-relocation'
        shutil.copytree(packet, p)
        ro_before = inventory(p)
        for f in p.iterdir(): f.chmod(0o444)
        p.chmod(0o555)
        try:
            need(not os.access(p, os.W_OK), 'Read-only fixture not enforced for this user')
            for mode in MODES:
                result = run(p, mode)
                need(result.returncode == 0, 'Read-only verifier failed: ' + result.stderr)
                readonly += 1
            need(inventory(p) == ro_before, 'Read-only packet changed')
        finally:
            p.chmod(0o755)
            for f in p.iterdir(): f.chmod(0o644)
    need(before == inventory(packet), 'Frozen author packet changed')
    result = {'audit': 'PASS', 'author_manifest_sha256': PIN, 'bound_author_files': len(mf['files']),
              'normal_optimized_modes': ['normal', '-O', '-OO'], 'positive_runs': positives,
              'source_replay_runs': source_passes, 'enforced_readonly_runs': readonly,
              'independent_mutation_types': len(variants), 'independent_mutation_rejections': rejections,
              'original_unchanged': True, 'math': independent_math()}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
